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
  - path_animation.gif/.mp4   a single dot tracing the viewing-order path
                           region to region with a short fading trail --
                           same visual language as
                           participant_one/<poster>/gaze_animation.gif,
                           again at the region level

Usage:
    python make_path_animations.py
=============================================================================
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon as MplPolygon
from PIL import Image
import imageio

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hierarchical_common import POSTERS, CROP_W, CROP_H, bg_image

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

MOVE_FRAMES = 8      # frames spent travelling between two regions (one "saccade")
DWELL_FRAMES = 7      # frames spent paused at a region
END_HOLD_FRAMES = 10  # extra frames holding the final position
TRAIL_LEN = 10         # how many past positions stay visible in the fading trail
FPS = 12


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
# path_animation.gif/.mp4 -- a moving dot with a fading trail tracing the
# viewing-order path region to region, like participant_one's
# gaze_animation.gif at the region level
# ---------------------------------------------------------------------------
def _interpolated_path(order, centers):
    """Returns (positions, current_region_or_None) per frame: a dwell at each
    region, a linear glide between consecutive regions in viewing order."""
    pts, cur = [], []
    x0, y0 = centers[order[0]]
    pts += [(x0, y0)] * DWELL_FRAMES
    cur += [order[0]] * DWELL_FRAMES
    for a, b in zip(order[:-1], order[1:]):
        xa, ya = centers[a]; xb, yb = centers[b]
        for i in range(1, MOVE_FRAMES + 1):
            t = i / MOVE_FRAMES
            pts.append((xa + (xb - xa) * t, ya + (yb - ya) * t))
            cur.append(None)
        pts += [(xb, yb)] * DWELL_FRAMES
        cur += [b] * DWELL_FRAMES
    return pts, cur


def build_trail_frames(stats, order, poster_label, img_file, method):
    bg = bg_image(img_file)
    centers, pct_of, num_of = _region_geometry(stats)
    path_pts, path_cur = _interpolated_path(order, centers)

    frames = []
    trail = deque(maxlen=TRAIL_LEN)
    for pt, cur in zip(path_pts, path_cur):
        trail.append(pt)
        fig, ax = plt.subplots(figsize=(12, 8), dpi=110)
        ax.imshow(bg, extent=[0, CROP_W, CROP_H, 0])

        n = len(trail)
        for j, (tx, ty) in enumerate(trail):
            frac = (j + 1) / n                      # 0 (oldest) .. 1 (current)
            ax.scatter([tx], [ty], s=40 + 260 * frac, color=DOT_COLOR,
                      alpha=0.15 + 0.75 * frac, edgecolor="white" if frac == 1 else "none",
                      linewidth=1.4, zorder=5)

        cap = f"Region {num_of[cur]}  •  {pct_of[cur]:.0f}% of gaze time" if cur is not None else ""
        ax.set_xlim(0, CROP_W); ax.set_ylim(CROP_H, 0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"{poster_label}  --  Gaze Path Animation ({method})\n{cap}", fontsize=13)
        fig.tight_layout()
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
        frames.append(buf)
        plt.close(fig)

    frames += [frames[-1]] * END_HOLD_FRAMES
    return frames


def main():
    if not COMPARISON_CSV.exists():
        sys.exit(f"{COMPARISON_CSV} not found -- run compare_methods.py first")
    comparison = pd.read_csv(COMPARISON_CSV)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for _, row in comparison.iterrows():
        poster, method = row["poster"], row["winner"]
        if poster not in POSTERS:
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

        frames = build_trail_frames(stats, order, label, img_file, method)

        gif_path = pdir / "path_animation.gif"
        imgs = [Image.fromarray(f) for f in frames]
        imgs[0].save(gif_path, save_all=True, append_images=imgs[1:],
                    duration=int(1000 / FPS), loop=0)
        print(f"  saved {gif_path}")

        mp4_path = pdir / "path_animation.mp4"
        writer = imageio.get_writer(mp4_path, fps=FPS, codec="libx264",
                                    quality=8, macro_block_size=1)
        for f in frames:
            writer.append_data(f)
        writer.close()
        print(f"  saved {mp4_path}")

    print("Done.")


if __name__ == "__main__":
    main()
