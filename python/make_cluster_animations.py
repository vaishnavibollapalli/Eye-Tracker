"""
Gaze animations with the attention clusters drawn on the poster.

For each poster in PARAMS, clusters all participants' fixations with the two
methods in clustering.py (hierarchical and DBSCAN), then replays one real
participant's recorded gaze over each result in real time. The dot and trail
take the colour of the cluster being fixated, that cluster lights up, and they
turn white during saccades.

Results go to test/ as <poster>_<method>.gif and .mp4.

Usage (from anywhere):
    python python/make_cluster_animations.py
    python python/make_cluster_animations.py --participant p12
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import imageio
import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgb
from matplotlib.patches import Polygon
from PIL import Image
from scipy.spatial import ConvexHull

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clustering import cluster_dbscan, cluster_hierarchical_auto, region_stats

ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT / "Renamed Signals"
POSTER_DIR = ROOT / "posters"
OUT_DIR = ROOT / "test"

N_PARTICIPANTS = 48
MIN_FIXATION_MS = 100
SCREEN_W, SCREEN_H = 1920, 1200

# same settings as demo.py
PARAMS = {
    "Armin Hofman- 1955": {"file": "Armin Hofman- 1955.jpg", "linkage": "complete",
                           "eps": 30, "min_samples": 15},
    "Barry Ceck - 1988":  {"file": "Barry Ceck - 1988.jpg", "linkage": "complete",
                           "eps": 35, "min_samples": 15},
}

# the first ten match demo.py so R1-R9 look the same as its COMPARE figures;
# the rest stop Barry Ceck's 14 DBSCAN regions from repeating colours
COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
          "#a65628", "#f781bf", "#999999", "#1b9e77", "#d95f02",
          "#66c2ff", "#c7e020", "#00e5c0", "#ffd400", "#b15cff"]

FPS = 25                # 40 ms per frame, which GIF can store exactly -- keeps playback real time
TRAIL_MS = 800          # how much past gaze stays visible in the fading trail
MAX_GAP_MS = 50         # no sample for longer than this (blink / track loss): hide the dot
END_HOLD_SEC = 1.0      # extra time holding the final frame
MIN_VALID_FRAC = 0.90   # a participant needs this share of valid samples to be shown
FRAME_HEIGHT = 860      # pixels
HULL_CORE_FRAC = 0.85   # outlines enclose this share of a cluster's fixations nearest its
                        # centre, so a few strays don't stretch them across the poster


def read_imotions(path: Path, usecols=None) -> pd.DataFrame:
    """iMotions CSVs have a metadata header ending in a #DATA line; the column
    names are on the line after it."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
        for i, line in enumerate(fh):
            if line.split(",")[0].strip() == "#DATA":
                return pd.read_csv(path, skiprows=i + 1, low_memory=False, usecols=usecols)
    raise RuntimeError(f"no #DATA line in {path}")


def load_participant(pid: str, stims) -> dict:
    """{stim: (fixations, gaze)} for one participant. The fixation selection
    matches demo.py's load_one. Both tables also carry times in ms from poster
    onset, so a gaze sample can be matched to the fixation it belongs to."""
    pdir = BASE_DIR / pid
    se_path, gz_path = pdir / "Native_SlideEvents.csv", pdir / "ET_RExtAPI-GazeAnalysis.csv"
    if not (se_path.exists() and gz_path.exists()):
        return {}

    se = read_imotions(se_path)
    se["Timestamp"] = pd.to_numeric(se["Timestamp"], errors="coerce")
    columns = ["Timestamp", "Interpolated Gaze X", "Interpolated Gaze Y", "Fixation Index",
               "Fixation X", "Fixation Y", "Fixation Start", "Fixation End", "Fixation Duration"]
    gz = read_imotions(gz_path, usecols=columns).apply(pd.to_numeric, errors="coerce")
    fix_all = (gz.dropna(subset=["Fixation Start", "Fixation Index"])
                 .drop_duplicates("Fixation Index"))

    result = {}
    for stim in stims:
        ev = se[se["SourceStimuliName"] == stim]
        t0 = ev.loc[ev["SlideEvent"].isin(["StartMedia", "StartSlide"]), "Timestamp"]
        t1 = ev.loc[ev["SlideEvent"].isin(["EndMedia", "EndSlide"]), "Timestamp"]
        if t0.empty or t1.empty:
            continue
        t0, t1 = float(t0.iloc[0]), float(t1.iloc[0])

        win = fix_all[fix_all["Fixation Start"].between(t0, t1)]
        if win.empty:
            continue
        first = win["Fixation Start"].min()
        fix = pd.DataFrame({
            "participant": pid,
            "x": win["Fixation X"], "y": win["Fixation Y"],
            "duration": win["Fixation Duration"],
            "rel_start": win["Fixation Start"] - first,
            "rel_end": win["Fixation End"] - first,
            "t_start": win["Fixation Start"] - t0,
            "t_end": win["Fixation End"] - t0,
        })

        samples = gz[gz["Timestamp"].between(t0, t1)]
        x = samples["Interpolated Gaze X"].to_numpy(dtype=float, copy=True)
        y = samples["Interpolated Gaze Y"].to_numpy(dtype=float, copy=True)
        bad = ~((x > 0) & (y > 0))
        x[bad], y[bad] = np.nan, np.nan
        result[stim] = (fix, (samples["Timestamp"].to_numpy() - t0, x, y, t1 - t0))
    return result


def content_bounds(img: Image.Image):
    """Bounding box of the poster inside the image, ignoring solid borders
    (same rule as demo.py's get_image_content_bounds)."""
    arr = np.asarray(img)
    p = 10
    corners = [arr[:p, :p], arr[:p, -p:], arr[-p:, :p], arr[-p:, -p:]]
    border = np.zeros(arr.shape[:2], dtype=bool)
    for corner in corners:
        border |= np.linalg.norm(arr - corner.reshape(-1, 3).mean(axis=0), axis=2) < 40
    rows = np.where(~border.all(axis=1))[0]
    cols = np.where(~border.all(axis=0))[0]
    if len(rows) == 0 or len(cols) == 0:
        return 0, 0, img.width, img.height
    return cols[0], rows[0], cols[-1], rows[-1]


def hull_points(pts: np.ndarray):
    """Outline of a cluster's core. For drawing only: membership and every
    percentage still come from all of the cluster's fixations."""
    if len(pts) < 3:
        return None
    dist = np.linalg.norm(pts - np.median(pts, axis=0), axis=1)
    core = pts[dist <= np.quantile(dist, HULL_CORE_FRAC)]
    try:
        return core[ConvexHull(core).vertices]
    except Exception:
        return None


def pick_participant(clusterings, gaze_by_pid):
    """Participant whose split of gaze time across clusters is closest to the
    group's, summed over both methods, with enough valid gaze samples. Using
    one person per poster keeps the two methods' animations comparable."""
    scores = pd.Series(0.0, index=list(gaze_by_pid))
    for clust, stats in clusterings.values():
        group = stats["pct"].set_index("region")["pct_gaze"] / 100
        share = clust["data"].pivot_table(index="participant", columns="region",
                                          values="duration", aggfunc="sum", fill_value=0)
        share = share.reindex(columns=group.index, fill_value=0)
        share = share.div(share.sum(axis=1), axis=0)
        diff = (share - group).abs().sum(axis=1) / 2
        scores = scores.add(diff.reindex(scores.index, fill_value=1.0))
    for pid in scores.sort_values().index:
        if np.isfinite(gaze_by_pid[pid][1]).mean() >= MIN_VALID_FRAC:
            return pid
    return None


class ClusterReplay:
    """Draws the replay frame by frame. The poster and clusters are rendered
    once; each frame restores that image and draws only what moves."""

    def __init__(self, title, clust, stats, img, gaze, pid, scale):
        self.t, x, y, self.duration = gaze
        self.x, self.y = x * scale[0], y * scale[1]

        data = clust["data"]
        num_of = dict(zip(stats["rank_map"]["region"], stats["rank_map"]["region_num"]))
        pct_of = dict(zip(stats["pct"]["region"], stats["pct"]["pct_gaze"]))
        color_of = {r: COLORS[int(n) % len(COLORS)] for r, n in num_of.items()}

        x0, y0, x1, y1 = content_bounds(img)
        title_px = 62
        h_px = FRAME_HEIGHT
        w_px = 2 * round((h_px - title_px) * (x1 - x0) / (y1 - y0) / 2)
        dpi = 100
        self.fig = plt.figure(figsize=(w_px / dpi, h_px / dpi), dpi=dpi)
        self.fig.suptitle(f"{title}\nReal gaze replay: participant {pid}",
                          fontsize=12, fontweight="bold", y=0.995)
        ax = self.fig.add_axes([0, 0, 1, 1 - title_px / h_px])
        ax.imshow(img)
        ax.set_xlim(x0, x1); ax.set_ylim(y1, y0); ax.axis("off")

        # static layer: each cluster's outline and label
        self.hulls = {}
        for r in sorted(data["region"].unique()):
            pts = data.loc[data["region"] == r, ["x", "y"]].to_numpy()
            hull = hull_points(pts)
            if hull is not None:
                self.hulls[r] = hull
                ax.add_patch(Polygon(hull, fill=False, edgecolor=color_of[r], linewidth=2.2,
                                     alpha=0.95, zorder=3))
            ax.text(*np.mean(pts, axis=0), f"R{int(num_of[r])}  {pct_of[r]:.0f}%", color="white",
                    fontsize=8, fontweight="bold", ha="center", va="center", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.25", fc=color_of[r], ec="white",
                              linewidth=0.8, alpha=0.85))

        # moving layer
        self.active = Polygon([[0, 0]], closed=True, alpha=0.3, zorder=3, animated=True)
        self.trail = LineCollection([], capstyle="round", zorder=5, animated=True)
        self.trail.set_path_effects([pe.withStroke(linewidth=3.2, foreground="black", alpha=0.35)])
        self.dot, = ax.plot([], [], "o", markersize=13, markeredgecolor="black",
                            markeredgewidth=1.5, zorder=6, animated=True)
        self.clock = ax.text(0.015, 0.012, "", transform=ax.transAxes, color="white",
                             fontsize=11, fontweight="bold", ha="left", va="bottom", zorder=7,
                             animated=True, bbox=dict(boxstyle="round,pad=0.35", fc="black",
                                                      ec="white", alpha=0.8))
        ax.add_patch(self.active)
        ax.add_collection(self.trail)
        self.ax = ax

        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)

        # for each gaze sample, the cluster being fixated (None during saccades
        # and in fixations clustering left out)
        fix = data[data["participant"] == pid].sort_values("t_start")
        starts, ends = fix["t_start"].to_numpy(), fix["t_end"].to_numpy()
        regions = fix["region"].to_numpy()
        idx = np.searchsorted(starts, self.t, side="right") - 1
        inside = (idx >= 0) & (self.t <= ends[np.clip(idx, 0, None)])
        self.sample_region = [regions[i] if ok else None for i, ok in zip(idx, inside)]
        white = to_rgb("white")
        self.rgb = np.array([to_rgb(color_of[r]) if r is not None else white
                             for r in self.sample_region])
        self.num_of = num_of
        self.color_of = color_of

    def render(self, now):
        lo = np.searchsorted(self.t, now - TRAIL_MS)
        hi = np.searchsorted(self.t, now, side="right")
        t = self.t[lo:hi]
        pts = np.column_stack([self.x[lo:hi], self.y[lo:hi]])
        finite = np.isfinite(pts).all(axis=1)

        # one segment per consecutive valid pair, so a blink leaves a break in
        # the line instead of a jump the eye never made
        ok = finite[:-1] & finite[1:]
        age = (now - t[1:][ok]) / TRAIL_MS
        colors = np.column_stack([self.rgb[lo:hi][1:][ok], 0.15 + 0.85 * (1 - age)])
        self.trail.set_segments(list(np.stack([pts[:-1][ok], pts[1:][ok]], axis=1)))
        self.trail.set_color(colors)
        self.trail.set_linewidths(1.0 + 2.2 * (1 - age))

        region = None
        visible = finite.any() and now - t[finite][-1] <= MAX_GAP_MS
        if visible:
            last = np.flatnonzero(finite)[-1]
            region = self.sample_region[lo + last]
            self.dot.set_data(pts[last:last + 1, 0], pts[last:last + 1, 1])
            self.dot.set_markerfacecolor(self.color_of.get(region, "white"))

        lit = region in self.hulls
        if lit:
            self.active.set_xy(self.hulls[region])
            self.active.set_facecolor(self.color_of[region])

        where = f"    R{int(self.num_of[region])}" if region is not None else ""
        self.clock.set_text(f"{now / 1000:4.1f} s / {self.duration / 1000:.0f} s{where}")

        canvas = self.fig.canvas
        canvas.restore_region(self.background)
        if lit:
            self.ax.draw_artist(self.active)
        self.ax.draw_artist(self.trail)
        if visible:
            self.ax.draw_artist(self.dot)
        self.ax.draw_artist(self.clock)
        return np.asarray(canvas.buffer_rgba())[:, :, :3].copy()

    def close(self):
        plt.close(self.fig)


def gif_palette(sheet: Image.Image) -> Image.Image:
    """256-colour palette from the poster, with slots reserved for the cluster
    colours -- each too small on screen to survive quantizing otherwise."""
    extra = [(1.0, 1.0, 1.0), (0.0, 0.0, 0.0)]
    for color in COLORS:
        rgb = np.array(to_rgb(color))
        extra += [tuple(rgb), tuple(rgb * 0.6), tuple(rgb * 0.6 + 0.4)]
    poster = sheet.quantize(colors=256 - len(extra), dither=Image.Dither.NONE).getpalette()
    palette = Image.new("P", (1, 1))
    palette.putpalette(poster + [int(v * 255) for rgb in extra for v in rgb])
    return palette


def save_animation(replay, gif_path, mp4_path):
    n_frames = int(replay.duration / 1000 * FPS) + 1
    times = np.arange(n_frames) * 1000 / FPS

    # one shared palette keeps the poster from flickering and the GIF small
    samples = [Image.fromarray(replay.render(t)) for t in np.linspace(TRAIL_MS, times[-1], 6)]
    sheet = Image.new("RGB", (samples[0].width, samples[0].height * len(samples)))
    for i, im in enumerate(samples):
        sheet.paste(im, (0, i * im.height))
    palette = gif_palette(sheet)

    writer = imageio.get_writer(mp4_path, fps=FPS, codec="libx264", quality=8,
                                macro_block_size=1, pixelformat="yuv420p")
    gif_frames = []
    frame = None
    for t in times:
        frame = replay.render(t)
        writer.append_data(frame)
        gif_frames.append(Image.fromarray(frame).quantize(palette=palette,
                                                          dither=Image.Dither.NONE))
    for _ in range(int(END_HOLD_SEC * FPS)):
        writer.append_data(frame)
        gif_frames.append(gif_frames[-1])
    writer.close()
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:],
                       duration=int(1000 / FPS), loop=0)


def main():
    ap = argparse.ArgumentParser(description="Gaze animations with clusters on the poster")
    ap.add_argument("--participant", help="replay this participant (e.g. p12) instead of the "
                                          "most representative one")
    args = ap.parse_args()

    print("Loading participants...")
    fixations = {stim: [] for stim in PARAMS}
    gaze = {stim: {} for stim in PARAMS}
    for i in range(1, N_PARTICIPANTS + 1):
        pid = f"p{i}"
        for stim, (fix, samples) in load_participant(pid, PARAMS).items():
            fixations[stim].append(fix)
            gaze[stim][pid] = samples

    OUT_DIR.mkdir(exist_ok=True)
    for stim, params in PARAMS.items():
        print(f"\n=== {stim} ===")
        img = Image.open(POSTER_DIR / params["file"]).convert("RGB")
        img_w, img_h = img.size
        scale = (img_w / SCREEN_W, img_h / SCREEN_H)

        fix = pd.concat(fixations[stim], ignore_index=True)
        fix = fix[fix["duration"] >= MIN_FIXATION_MS].reset_index(drop=True)
        fix["x"] *= scale[0]
        fix["y"] *= scale[1]

        clusterings = {}
        hier = cluster_hierarchical_auto(fix, stim, params["linkage"], img_w, img_h)
        if hier:
            clusterings[f"Hierarchical ({params['linkage']})"] = (hier, region_stats(hier))
        dbscan = cluster_dbscan(fix, stim, params["eps"], params["min_samples"], img_w, img_h)
        if dbscan:
            clusterings["DBSCAN"] = (dbscan, region_stats(dbscan))

        pid = args.participant or pick_participant(clusterings, gaze[stim])
        if pid is None or pid not in gaze[stim]:
            print(f"  ! no usable gaze for {stim}, skipped")
            continue
        print(f"  replaying {pid}")

        slug = re.sub(r"[^a-z0-9]+", "_", stim.lower()).strip("_")
        for method, (clust, stats) in clusterings.items():
            name = f"{slug}_{'dbscan' if method == 'DBSCAN' else 'hierarchical'}"
            title = f"{stim} - {method}, k={clust['k']}"
            replay = ClusterReplay(title, clust, stats, img, gaze[stim][pid], pid, scale)
            save_animation(replay, OUT_DIR / f"{name}.gif", OUT_DIR / f"{name}.mp4")
            replay.close()
            print(f"  saved test/{name}.gif and .mp4")

    print("\nDone.")


if __name__ == "__main__":
    main()
