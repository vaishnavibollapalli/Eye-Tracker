"""
=============================================================================
Path animation + path JPG for each poster's WINNING clustering method
=============================================================================
Reads output/Hierarchical Clustering/method_comparison.csv (written by
compare_methods.py) to find each poster's winning method, then rebuilds that
method's region hulls + viewing-order path from its already-saved
fixations_labelled.csv + region_stats.csv (no re-clustering) and animates the
regions appearing one at a time, in aggregate viewing order, with the
connecting arrows -- an animated version of that method's average_gaze_path.png.

Outputs per poster into output/Poster Summary/<poster>/:
  - path.jpg              the winning method's average_gaze_path, as a jpg
  - path_animation.gif    the build-up animation (for standalone viewing)
  - path_animation.mp4    same animation as a video (for embedding in the PPT)

Usage:
    python make_path_animations.py
=============================================================================
"""
from __future__ import annotations

import sys
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
from hierarchical_common import POSTERS, CROP_W, CROP_H, REGION_COLORS, bg_image

HERE = Path(__file__).resolve().parent
COMPARISON_CSV = HERE / "Hierarchical Clustering" / "method_comparison.csv"
OUT_DIR = HERE / "Poster Summary"

METHOD_DIRS = {
    "DBSCAN":        HERE / "DBSCAN output",
    "Agglomerative": HERE / "Hierarchical Clustering" / "Agglomerative",
    "Divisive":      HERE / "Hierarchical Clustering" / "Divisive",
}
METHOD_IMG_PREFIX = {
    "DBSCAN": "dbscan",
    "Agglomerative": "agglomerative",
    "Divisive": "divisive",
}

FPS = 1.1
HOLD_EXTRA_FRAMES = 4


def build_frames(sub: pd.DataFrame, stats: pd.DataFrame, order: list, poster_label: str,
                 img_file: str, method: str):
    bg = bg_image(img_file)
    num_of = dict(zip(stats["region_raw_id"], stats["region_num"]))
    pct_of = dict(zip(stats["region_raw_id"], stats["pct_gaze_time"]))
    centers = {r: (stats.loc[stats["region_raw_id"] == r, "center_x"].iloc[0],
                   stats.loc[stats["region_raw_id"] == r, "center_y"].iloc[0])
               for r in stats["region_raw_id"]}

    hulls = {}
    for r in stats["region_raw_id"]:
        pts = sub.loc[sub["region"] == r, ["px", "py"]].to_numpy()
        if len(pts) >= 3:
            try:
                hull = ConvexHull(pts)
                hulls[r] = pts[hull.vertices]
            except Exception:
                hulls[r] = None
        else:
            hulls[r] = None

    frames = []
    for reveal_n in range(0, len(order) + 1):
        fig, ax = plt.subplots(figsize=(12, 8), dpi=110)
        ax.imshow(bg, extent=[0, CROP_W, CROP_H, 0])
        ax.set_facecolor("black")
        fig.patch.set_facecolor("black")

        revealed = order[:reveal_n]
        for r in revealed:
            rn = num_of[r]
            col = REGION_COLORS[(rn - 1) % 10]
            if hulls[r] is not None:
                poly = MplPolygon(hulls[r], closed=True, facecolor=col, edgecolor="white",
                                  alpha=0.30, linewidth=1.5, zorder=2)
                ax.add_patch(poly)

        for a, b in zip(revealed[:-1], revealed[1:]):
            x0, y0 = centers[a]; x1, y1 = centers[b]
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                       arrowprops=dict(arrowstyle="-|>", color="white", lw=2), zorder=4)

        for r in revealed:
            cxp, cyp = centers[r]; rn = num_of[r]
            ax.scatter([cxp], [cyp], s=120 + 26 * pct_of[r], color="black",
                      edgecolor="white", alpha=0.9, zorder=5)
            ax.text(cxp, cyp - 34, f"Region {rn}\n{pct_of[r]:.0f}% of gaze time",
                   color="white", fontweight="bold", ha="center", va="bottom",
                   fontsize=9, zorder=6,
                   path_effects=[pe.withStroke(linewidth=3, foreground="black")])

        ax.set_xlim(0, CROP_W); ax.set_ylim(CROP_H, 0)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"{poster_label}  --  Viewing-Order Path ({method})", color="white", fontsize=13)
        fig.tight_layout()
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
        frames.append(buf)
        plt.close(fig)

    frames += [frames[-1]] * HOLD_EXTRA_FRAMES   # hold on the fully-revealed frame
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
        prefix = METHOD_IMG_PREFIX[method]

        fix_path = mdir / "fixations_labelled.csv"
        stats_path = mdir / "region_stats.csv"
        gaze_path_png = mdir / "average_gaze_path.png"
        if not (fix_path.exists() and stats_path.exists()):
            print(f"  ! skipping {poster} ({method}): missing labelled fixations/stats")
            continue

        print(f"=== {poster}  (winner: {method}) ===")
        sub = pd.read_csv(fix_path)
        stats = pd.read_csv(stats_path)
        order = stats.sort_values("viewing_order")["region_raw_id"].tolist()

        pdir = OUT_DIR / poster
        pdir.mkdir(parents=True, exist_ok=True)

        # path.jpg -- the winning method's own average_gaze_path.png, as a jpg
        if gaze_path_png.exists():
            Image.open(gaze_path_png).convert("RGB").save(pdir / "path.jpg", quality=92)

        frames = build_frames(sub, stats, order, label, img_file, method)

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
