"""
=============================================================================
Scanpath plot + gaze-path animation + path JPG for each poster's WINNING
clustering method
=============================================================================
Reads output/Hierarchical Clustering/method_comparison.csv (written by
compare_methods.py) to find each poster's winning method, then rebuilds that
method's region path from its already-saved fixations_labelled.csv +
region_stats.csv (no re-clustering).

Three outputs per poster, into output/Poster Summary/<poster>/:
  - path.jpg              the winning method's average_gaze_path (region
                           hulls + arrows), as a jpg
  - scanpath_plot.png      numbered circles (region, sized by % of gaze
                           time) connected by straight lines in viewing
                           order, over the full-colour poster -- same visual
                           language as participant_one/<poster>/scanpath_plot.png,
                           just at the region level instead of raw fixations
  - path_animation.gif/.mp4   real-time replay of one real participant's
                           recorded gaze (120 Hz samples from Renamed Signals)
                           with a fading trail: real fixations, saccades and
                           timing, nothing interpolated between regions. Gaze
                           is not averaged across people -- that cancels out
                           the saccades. The participant shown is the one
                           whose viewing best matches the group's (see
                           rank_participants), named in the animation title.

Usage:
    python make_path_animations.py
    python make_path_animations.py --posters nancy bookcover
    python make_path_animations.py --posters nancy --participant p12
=============================================================================
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon as MplPolygon
from PIL import Image
import imageio

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hierarchical_common import (POSTERS, CROP_W, CROP_H, SCALE_X, SCALE_Y,
                                 BASE_DIR, bg_image)
from eye_tracking_dbscan import _read_imotions

HERE = Path(__file__).resolve().parent
COMPARISON_CSV = HERE / "Hierarchical Clustering" / "method_comparison.csv"
OUT_DIR = HERE / "Poster Summary"

METHOD_DIRS = {
    "DBSCAN":        HERE / "DBSCAN output",
    "Agglomerative": HERE / "Hierarchical Clustering" / "Agglomerative",
    "Divisive":      HERE / "Hierarchical Clustering" / "Divisive",
}

DOT_COLOR = "#1f8fd6"       # matches the blue gaze-point marker in participant_one's gaze_animation.gif
STROKE = [pe.withStroke(linewidth=3, foreground="black")]

FPS = 25                 # 40 ms per frame, which GIF can store exactly -- keeps playback real time
TRAIL_MS = 800           # how much past gaze stays visible in the fading trail
MAX_GAP_MS = 50          # no sample for longer than this (blink / track loss): hide the dot
END_HOLD_SEC = 1.0       # extra time holding the final frame
MIN_VALID_FRAC = 0.90    # a participant needs this share of valid samples to be shown
GIF_SCALE = 0.5          # the GIF is 400 frames; the full-size copy is the mp4


def _region_geometry(stats: pd.DataFrame):
    centers = {r: (stats.loc[stats["region_raw_id"] == r, "center_x"].iloc[0],
                   stats.loc[stats["region_raw_id"] == r, "center_y"].iloc[0])
               for r in stats["region_raw_id"]}
    pct_of = dict(zip(stats["region_raw_id"], stats["pct_gaze_time"]))
    num_of = dict(zip(stats["region_raw_id"], stats["region_num"]))
    return centers, pct_of, num_of


# ---------------------------------------------------------------------------
# scanpath_plot.png -- numbered circles + straight lines, like
# participant_one's per-participant scanpath_plot.png, at the region level
# ---------------------------------------------------------------------------
def build_scanpath_plot(stats, order, poster_label, img_file, method, out_path):
    bg = bg_image(img_file)
    centers, pct_of, num_of = _region_geometry(stats)

    def size_for(pct):
        return 260 + pct * 55

    fig, ax = plt.subplots(figsize=(12, 8), dpi=140)
    ax.imshow(bg, extent=[0, CROP_W, CROP_H, 0])

    for a, b in zip(order[:-1], order[1:]):
        xa, ya = centers[a]; xb, yb = centers[b]
        ax.plot([xa, xb], [ya, yb], color="white", linewidth=1.8, alpha=0.95, zorder=3,
               solid_capstyle="round", path_effects=[pe.withStroke(linewidth=3.6, foreground="black")])

    for r in order:
        cx, cy = centers[r]
        ax.scatter([cx], [cy], s=size_for(pct_of[r]), color=DOT_COLOR, edgecolor="white",
                  linewidth=1.6, alpha=0.88, zorder=5)
        ax.text(cx, cy, str(num_of[r]), color="white", fontweight="bold",
               ha="center", va="center", fontsize=11, zorder=6)

    ax.set_xlim(0, CROP_W); ax.set_ylim(CROP_H, 0)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"Scanpath — {poster_label}  ({method})\n"
                "Circle size = % of gaze time  |  Lines = viewing-order path  |  Number = viewing order",
                fontsize=13)

    # legend swatches use their own small, fixed size scale -- reusing the
    # on-plot size_for() here would make the 50% handle so large it visually
    # collides with the legend's own title text
    legend_vals = [10, 20, 35, 50]
    legend_sizes = [70, 110, 160, 210]
    handles = [ax.scatter([], [], s=s, color=DOT_COLOR, edgecolor="white", linewidth=1.2)
              for s in legend_sizes]
    leg = ax.legend(handles, [f"{v}%" for v in legend_vals], title="% of Gaze Time",
                    loc="upper center", bbox_to_anchor=(0.5, -0.03), ncol=4, frameon=False,
                    fontsize=9, handletextpad=0.8, columnspacing=1.4, borderaxespad=0)
    leg.get_title().set_fontsize(10)

    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# choosing whose gaze to replay
# ---------------------------------------------------------------------------
def _edit_distance(a, b) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def rank_participants(fix, stats, order):
    """Participants, most representative first. Each is scored 0 (identical to
    the group) to 1 on two things, equally weighted: the order they first
    visited the regions vs the group's viewing order, and how their gaze time
    split across regions vs the group's pct_gaze_time."""
    fix = fix[fix["region_raw"].isin(order)]
    group_share = stats.set_index("region_raw_id")["pct_gaze_time"]
    group_share = group_share / group_share.sum()

    scores = {}
    for pid, sub in fix.groupby("participant"):
        first_visits = sub.sort_values("rel_start")["region_raw"].drop_duplicates().tolist()
        order_diff = _edit_distance(first_visits, order) / max(len(first_visits), len(order))
        share = sub.groupby("region_raw")["duration"].sum()
        share = (share / share.sum()).reindex(group_share.index, fill_value=0)
        share_diff = 0.5 * (share - group_share).abs().sum()
        scores[pid] = (order_diff + share_diff) / 2
    return sorted(scores, key=scores.get)


# ---------------------------------------------------------------------------
# raw gaze for one participant viewing one poster
# ---------------------------------------------------------------------------
def load_gaze(pid, stim_name):
    """(t_ms, x, y, duration_ms) relative to poster onset, or None if the
    participant has no record of this poster. x/y are NaN at invalid samples,
    in the same pixel space as the region centres."""
    pdir = BASE_DIR / pid
    se = _read_imotions(pdir / "Native_SlideEvents.csv")
    ev = se[se["SourceStimuliName"] == stim_name]
    t0 = pd.to_numeric(ev.loc[ev["SlideEvent"] == "StartMedia", "Timestamp"], errors="coerce")
    t1 = pd.to_numeric(ev.loc[ev["SlideEvent"] == "EndMedia", "Timestamp"], errors="coerce")
    if t0.empty or t1.empty:
        return None
    t0, t1 = float(t0.iloc[0]), float(t1.iloc[0])

    gz = _read_imotions(pdir / "ET_RExtAPI-GazeAnalysis.csv")
    t = pd.to_numeric(gz["Timestamp"], errors="coerce").to_numpy()
    keep = (t >= t0) & (t <= t1)
    x = pd.to_numeric(gz["Interpolated Gaze X"], errors="coerce").to_numpy()[keep].astype(float)
    y = pd.to_numeric(gz["Interpolated Gaze Y"], errors="coerce").to_numpy()[keep].astype(float)
    bad = ~((x > 0) & (y > 0))
    x[bad] = np.nan
    y[bad] = np.nan
    return t[keep] - t0, x * SCALE_X, y * SCALE_Y, t1 - t0


def pick_gaze(ranked, stim_name):
    """First participant in ranked order with enough valid samples."""
    for pid in ranked:
        gaze = load_gaze(pid, stim_name)
        if gaze is None or len(gaze[0]) == 0:
            continue
        valid = np.isfinite(gaze[1]).mean()
        if valid >= MIN_VALID_FRAC:
            return pid, gaze, valid
        print(f"  {pid}: only {valid:.0%} valid samples, trying next")
    return None


# ---------------------------------------------------------------------------
# path_animation.gif/.mp4 -- real-time replay with a fading trail
# ---------------------------------------------------------------------------
class GazeReplay:
    """Draws one frame of the replay at a time on a single reused figure."""

    def __init__(self, gaze, pid, fix, stats, poster_label, img_file):
        self.t, self.x, self.y, self.duration = gaze
        self.pid, self.label = pid, poster_label

        _, pct_of, num_of = _region_geometry(stats)
        fix = fix[fix["participant"] == pid].sort_values("rel_start")
        self.fix_start = fix["rel_start"].to_numpy()
        self.fix_end = fix["rel_end"].to_numpy()
        self.fix_caption = [
            f"Region {num_of[r]}  •  {pct_of[r]:.0f}% of group gaze time" if r in num_of else ""
            for r in fix["region_raw"]]

        self.fig, self.ax = plt.subplots(figsize=(12, 8), dpi=110)
        self.ax.imshow(bg_image(img_file), extent=[0, CROP_W, CROP_H, 0])
        self.trail = LineCollection([], capstyle="round", zorder=4)
        self.ax.add_collection(self.trail)
        self.dot, = self.ax.plot([], [], "o", color=DOT_COLOR, markersize=13,
                                 markeredgecolor="white", markeredgewidth=1.6, zorder=5)
        self.ax.set_xlim(0, CROP_W); self.ax.set_ylim(CROP_H, 0)
        self.ax.set_xticks([]); self.ax.set_yticks([])
        self.title = self.ax.set_title("\n", fontsize=13)
        self.fig.tight_layout()

    def _caption(self, now):
        i = np.searchsorted(self.fix_start, now, side="right") - 1
        return self.fix_caption[i] if i >= 0 and now <= self.fix_end[i] else ""

    def render(self, now):
        lo = np.searchsorted(self.t, now - TRAIL_MS)
        hi = np.searchsorted(self.t, now, side="right")
        t = self.t[lo:hi]
        pts = np.column_stack([self.x[lo:hi], self.y[lo:hi]])
        finite = np.isfinite(pts).all(axis=1)

        # one segment per consecutive valid pair, so a blink leaves a break in
        # the line instead of a jump the eye never made
        ok = finite[:-1] & finite[1:]
        segs = np.stack([pts[:-1][ok], pts[1:][ok]], axis=1)
        age = (now - t[1:][ok]) / TRAIL_MS
        colors = np.tile((*to_rgb(DOT_COLOR), 1.0), (len(age), 1))
        colors[:, 3] = 0.1 + 0.9 * (1 - age)
        self.trail.set_segments(list(segs))
        self.trail.set_color(colors)
        self.trail.set_linewidths(0.8 + 2.4 * (1 - age))

        if finite.any() and now - t[finite][-1] <= MAX_GAP_MS:
            self.dot.set_data(pts[finite][-1:, 0], pts[finite][-1:, 1])
        else:
            self.dot.set_data([], [])

        self.title.set_text(f"{self.label}  --  Real Gaze Replay (participant {self.pid})\n"
                            f"{now / 1000:4.1f} s of {self.duration / 1000:.0f} s"
                            f"      {self._caption(now)}")
        self.fig.canvas.draw()
        return np.asarray(self.fig.canvas.buffer_rgba())[:, :, :3].copy()

    def close(self):
        plt.close(self.fig)


def save_animation(replay, gif_path, mp4_path):
    n_frames = int(replay.duration / 1000 * FPS) + 1
    times = np.arange(n_frames) * 1000 / FPS

    def small(frame):
        im = Image.fromarray(frame)
        return im.resize((int(im.width * GIF_SCALE), int(im.height * GIF_SCALE)), Image.LANCZOS)

    # one shared palette keeps the poster from flickering and the GIF small
    samples = [small(replay.render(t)) for t in np.linspace(TRAIL_MS, times[-1], 6)]
    sheet = Image.new("RGB", (samples[0].width, samples[0].height * len(samples)))
    for i, im in enumerate(samples):
        sheet.paste(im, (0, i * im.height))
    palette = sheet.quantize(colors=256, dither=Image.Dither.NONE)

    writer = imageio.get_writer(mp4_path, fps=FPS, codec="libx264",
                                quality=8, macro_block_size=1)
    gif_frames = []
    frame = None
    for t in times:
        frame = replay.render(t)
        writer.append_data(frame)
        gif_frames.append(small(frame).quantize(palette=palette, dither=Image.Dither.NONE))
    for _ in range(int(END_HOLD_SEC * FPS)):
        writer.append_data(frame)
        gif_frames.append(gif_frames[-1])
    writer.close()

    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:],
                       duration=int(1000 / FPS), loop=0)


def main():
    ap = argparse.ArgumentParser(description="Poster summary plots and real gaze replays")
    ap.add_argument("--posters", nargs="*",
                    help="subset of poster keys (without the 'poster_' prefix)")
    ap.add_argument("--participant", help="replay this participant (e.g. p12) instead of the "
                                          "most representative one")
    args = ap.parse_args()
    want = {p if p.startswith("poster_") else f"poster_{p}" for p in args.posters or []}

    if not COMPARISON_CSV.exists():
        sys.exit(f"{COMPARISON_CSV} not found -- run compare_methods.py first")
    comparison = pd.read_csv(COMPARISON_CSV)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for _, row in comparison.iterrows():
        poster, method = row["poster"], row["winner"]
        if poster not in POSTERS or (want and poster not in want):
            continue
        label, img_file = POSTERS[poster]
        mdir = METHOD_DIRS[method] / poster

        fix_path = mdir / "fixations_labelled.csv"
        stats_path = mdir / "region_stats.csv"
        gaze_path_png = mdir / "average_gaze_path.png"
        if not (fix_path.exists() and stats_path.exists()):
            print(f"  ! skipping {poster} ({method}): missing labelled fixations/stats")
            continue

        print(f"=== {poster}  (winner: {method}) ===")
        stats = pd.read_csv(stats_path)
        order = stats.sort_values("viewing_order")["region_raw_id"].tolist()

        pdir = OUT_DIR / poster
        pdir.mkdir(parents=True, exist_ok=True)

        if gaze_path_png.exists():
            Image.open(gaze_path_png).convert("RGB").save(pdir / "path.jpg", quality=92)
            print(f"  saved {pdir / 'path.jpg'}")

        build_scanpath_plot(stats, order, label, img_file, method, pdir / "scanpath_plot.png")
        print(f"  saved {pdir / 'scanpath_plot.png'}")

        fix = pd.read_csv(fix_path)
        if "region_raw" not in fix:     # hierarchical methods store the raw id as "region"
            fix["region_raw"] = fix["region"]
        ranked = [args.participant] if args.participant else rank_participants(fix, stats, order)
        picked = pick_gaze(ranked, label)
        if picked is None:
            print(f"  ! no participant with usable gaze for {poster}, animation skipped")
            continue
        pid, gaze, valid = picked
        print(f"  replaying {pid} ({valid:.0%} valid samples)")

        replay = GazeReplay(gaze, pid, fix, stats, label, img_file)
        save_animation(replay, pdir / "path_animation.gif", pdir / "path_animation.mp4")
        replay.close()
        print(f"  saved {pdir / 'path_animation.gif'} and .mp4")

    print("Done.")


if __name__ == "__main__":
    main()
