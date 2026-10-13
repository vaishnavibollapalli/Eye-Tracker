"""
=============================================================================
Shared plumbing for the hierarchical clustering scripts
(eye_tracking_agglomerative.py, eye_tracking_divisive.py)
=============================================================================
Fixation extraction, canvas transform, region-level stats and the poster
plots are identical to eye_tracking_dbscan.py -- factored out here so the
agglomerative/divisive scripts only contain the clustering logic itself.
Reuses the SAME fixation cache that eye_tracking_dbscan.py wrote, so no
re-extraction from the raw 48-participant exports is needed.
=============================================================================
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from sklearn.neighbors import NearestNeighbors

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon as MplPolygon
from PIL import Image

# ---------------------------------------------------------------------------
# CONFIG (identical to eye_tracking_dbscan.py)
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent            # .../Eye-Tracker/output
PROJECT = HERE.parent
BASE_DIR = PROJECT / "Renamed Signals"            # p1 ... p48
POSTER_IMG_DIR = PROJECT / "posters"
DBSCAN_CACHE = HERE / "DBSCAN output" / "_cache" / "fixations_master.csv"

N_PARTICIPANTS = 48

POSTERS = {
    "poster_ArminHofman-1955":    ("Armin Hofman- 1955", "Armin Hofman- 1955.jpg"),
    "poster_BarryCeck-1988":      ("Barry Ceck - 1988", "Barry Ceck - 1988.jpg"),
    "poster_DavidCarson":         ("David Carson", "David Carson.jpg"),
    "poster_DavidCarson-1990":    ("David Carson - 1990", "David Carson - 1990.jpg"),
    "poster_EllaRosenblatt-2021": ("Ella Rosenblatt- 2021", "Ella Rosenblatt- 2021.jpg"),
    "poster_IrisChung-2015":      ("Iris Chung- 2015", "Iris Chung- 2015.jpg"),
    "poster_JanTschichold-1927-DieFrauohneNamen": (
        "Jan Tschichold-1927-Die Frau ohne Namen", "Jan Tschichold-1927-Die Frau ohne Namen.JPG"),
    "poster_JanTschichold-1938-Der": ("Jan Tschichold-1938-Der", "Jan Tschichold-1938-Der.JPG"),
    "poster_JoostSchmidt-1923-Saatliches": (
        "Joost Schmidt-1923-Saatliches", "Joost Schmidt-1923-Saatliches.JPG"),
    "poster_PaulRand-1947":       ("Paul Rand, 1947", "Paul Rand, 1947.jpg"),
    "poster_PaulaScher-1995":     ("Paula Scher - 1995", "Paula Scher - 1995.jpg"),
    "poster_ScottBarry-2010":     ("Scott Barry- 2010", "Scott Barry- 2010.jpg"),
    "poster_SeanAlatorre":        ("Sean Alatorre", "Sean Alatorre.jpg"),
    "poster_bookcover":           ("bookcover", "bookcover.jpg"),
    "poster_nancy":               ("nancy poster", "nancy.jpg"),
}

CROP_X0, CROP_Y0 = 7, 68
CROP_X1, CROP_Y1 = 1943, 1276
CROP_W, CROP_H = CROP_X1 - CROP_X0, CROP_Y1 - CROP_Y0      # 1936 x 1208
OFFSET_X, SCALE_X = 7, 1936 / 1920
OFFSET_Y, SCALE_Y = 68, 1208 / 1200

# narrowed from (3,7): fewer/larger regions read as more distinct and are
# less prone to the adjacent-region bleed you get when k pushes toward 7
K_RANGE = (3, 5)

# pre-clustering outlier filter: a fixation whose distance to its OUTLIER_K-th
# nearest neighbour is far above the pack (robust median + MAD cutoff) is a
# stray/isolated point, not a member of any real attention region -- dropping
# it keeps those strays from dragging a region's boundary out to meet them.
OUTLIER_K = 10
OUTLIER_MAD_MULT = 3.0

GAZE_COLS = ["Fixation Index", "Fixation X", "Fixation Y",
             "Fixation Start", "Fixation End", "Fixation Duration"]


def transform_xy(x, y):
    return OFFSET_X + x * SCALE_X, OFFSET_Y + y * SCALE_Y


def filter_outliers(points: np.ndarray, k: int = OUTLIER_K, mad_mult: float = OUTLIER_MAD_MULT) -> np.ndarray:
    """Boolean keep-mask: True for points whose local density is in line with
    the rest of the data, False for isolated/stray points."""
    n = len(points)
    k_eff = min(k, n - 1)
    if k_eff < 1:
        return np.ones(n, dtype=bool)
    nn = NearestNeighbors(n_neighbors=k_eff + 1).fit(points)
    dist, _ = nn.kneighbors(points)
    knn_dist = dist[:, -1]                       # distance to k-th neighbour (excludes self)
    med = np.median(knn_dist)
    mad = np.median(np.abs(knn_dist - med)) * 1.4826   # normal-consistent MAD
    if mad == 0:
        return np.ones(n, dtype=bool)
    return knn_dist <= med + mad_mult * mad


def separation_score(sil: np.ndarray, db: np.ndarray) -> np.ndarray:
    """Combines silhouette (higher = better) and Davies-Bouldin (lower =
    better) into one 0-1 "how distinct are these regions" score, each
    min-max normalised across the candidates being compared."""
    def norm(a):
        lo, hi = np.min(a), np.max(a)
        return np.ones_like(a, dtype=float) if hi - lo < 1e-12 else (a - lo) / (hi - lo)
    return 0.5 * norm(sil) + 0.5 * (1 - norm(db))


def _read_imotions(path: Path, marker: str = "#DATA") -> pd.DataFrame:
    with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
        skip = 0
        for i, line in enumerate(fh):
            if line.split(",")[0].strip() == marker:
                skip = i + 1
                break
        else:
            raise RuntimeError(f"no {marker} line in {path}")
    return pd.read_csv(path, skiprows=skip, low_memory=False)


def extract_all_fixations(posters: dict) -> pd.DataFrame:
    rows = []
    stim_wanted = {name: folder for folder, (name, _img) in posters.items()}
    for i in range(1, N_PARTICIPANTS + 1):
        pid = f"p{i}"
        pdir = BASE_DIR / pid
        se_path = pdir / "Native_SlideEvents.csv"
        gz_path = pdir / "ET_RExtAPI-GazeAnalysis.csv"
        if not se_path.exists() or not gz_path.exists():
            print(f"  ! missing files for {pid}, skipped")
            continue

        se = _read_imotions(se_path)
        se["Timestamp"] = pd.to_numeric(se["Timestamp"], errors="coerce")

        gz = _read_imotions(gz_path)
        for c in GAZE_COLS:
            gz[c] = pd.to_numeric(gz[c], errors="coerce")

        fix = (gz.dropna(subset=["Fixation Start", "Fixation Index"])
                 .drop_duplicates(subset="Fixation Index", keep="first"))

        for stim_name, poster_folder in stim_wanted.items():
            ev = se[se["SourceStimuliName"] == stim_name]
            t0 = ev.loc[ev["SlideEvent"] == "StartMedia", "Timestamp"]
            t1 = ev.loc[ev["SlideEvent"] == "EndMedia", "Timestamp"]
            if t0.empty or t1.empty:
                continue
            t0, t1 = float(t0.iloc[0]), float(t1.iloc[0])

            win = fix[(fix["Fixation Start"] >= t0) & (fix["Fixation Start"] <= t1)]
            if win.empty:
                continue

            cx, cy = transform_xy(win["Fixation X"].to_numpy(), win["Fixation Y"].to_numpy())
            rows.append(pd.DataFrame({
                "participant": pid,
                "poster": poster_folder,
                "canvas_x": cx,
                "canvas_y": cy,
                "duration": win["Fixation Duration"].to_numpy(),
                "rel_start": win["Fixation Start"].to_numpy() - t0,
                "rel_end": win["Fixation End"].to_numpy() - t0,
            }))
        print(f"  done: {pid}")

    if not rows:
        sys.exit("No fixations extracted -- check BASE_DIR and poster names.")
    return pd.concat(rows, ignore_index=True)


def load_fixations(posters: dict, refresh: bool = False) -> pd.DataFrame:
    """Reuses the fixation cache written by eye_tracking_dbscan.py (same
    posters, same extraction) so the raw 48-participant exports don't need
    to be re-read. Falls back to extracting from scratch if that cache is
    missing or doesn't cover all requested posters."""
    if DBSCAN_CACHE.exists() and not refresh:
        df = pd.read_csv(DBSCAN_CACHE)
        have = set(df["poster"].unique())
        if set(posters).issubset(have):
            print(f"Using cached fixations: {DBSCAN_CACHE}  ({len(df)} rows)")
            return df[df["poster"].isin(posters)].copy()
        print("Cache is missing some requested posters -- extracting.")
    print("Extracting fixations from raw iMotions exports (this takes a few minutes)...")
    return extract_all_fixations(posters)


# ---------------------------------------------------------------------------
# region-level statistics -- identical to eye_tracking_dbscan.py's version,
# generalised so it works for any label scheme (no -1/noise concept here:
# every fixation already belongs to a cluster).
# ---------------------------------------------------------------------------
def region_stats(sub: pd.DataFrame, centers: dict, region_ids: list) -> tuple[pd.DataFrame, list]:
    n_participants = sub["participant"].nunique()
    total_dur = sub["duration"].sum()

    g = sub.groupby("region")
    pct_time = g["duration"].sum() / total_dur * 100
    avg_span = g["duration"].mean()
    n_fix = g.size()

    first_fix = sub.loc[sub.groupby("participant")["rel_start"].idxmin()]
    first_pct = (first_fix["region"].value_counts() / n_participants * 100)

    entry = sub.groupby(["participant", "region"])["rel_start"].min().reset_index()
    avg_entry = entry.groupby("region")["rel_start"].mean()
    coverage = entry.groupby("region")["participant"].nunique() / n_participants * 100

    order = avg_entry.sort_values().index.tolist()
    order_pos = {r: i + 1 for i, r in enumerate(order)}

    rank = pct_time.sort_values(ascending=False)
    region_num = {r: i + 1 for i, r in enumerate(rank.index)}

    cx = {r: centers[r][0] for r in region_ids}
    cy = {r: centers[r][1] for r in region_ids}

    out = pd.DataFrame({
        "region_raw_id": pd.Series(region_ids, index=region_ids),
        "region_num": pd.Series(region_num),
        "n_fixations": n_fix,
        "pct_gaze_time": pct_time.round(2),
        "avg_fixation_ms": avg_span.round(1),
        "first_attention_pct": first_pct.reindex(region_ids).fillna(0).round(1),
        "avg_entry_ms": avg_entry.round(0),
        "participant_coverage_pct": coverage.round(1),
        "viewing_order": pd.Series(order_pos),
        "center_x": pd.Series(cx).round(1),
        "center_y": pd.Series(cy).round(1),
    }).sort_values("region_num").reset_index(drop=True)
    return out, order


def duration_weighted_centers(sub: pd.DataFrame, region_ids: list) -> dict:
    w = sub["duration"].to_numpy()
    px = sub["px"].to_numpy(); py = sub["py"].to_numpy()
    centers = {}
    for r in region_ids:
        idx = (sub["region"] == r).to_numpy()
        centers[r] = (np.average(px[idx], weights=w[idx]), np.average(py[idx], weights=w[idx]))
    return centers


# ---------------------------------------------------------------------------
# plots (poster-overlay scatter + average gaze path) -- same visual language
# as eye_tracking_dbscan.py, minus the "noise" concept.
# ---------------------------------------------------------------------------
REGION_COLORS = plt.get_cmap("tab10").colors


def bg_image(img_file: str):
    im = Image.open(POSTER_IMG_DIR / img_file).convert("RGB").resize((CROP_W, CROP_H))
    return np.asarray(im)


def plot_clusters(sub, centers, stats, region_ids, poster, img_file, out_path, method_label, subtitle):
    bg = bg_image(img_file)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(bg, extent=[0, CROP_W, CROP_H, 0], alpha=0.35)

    num_of = dict(zip(stats["region_raw_id"], stats["region_num"]))
    for r in region_ids:
        m = sub["region"] == r
        rn = num_of[r]
        ax.scatter(sub.loc[m, "px"], sub.loc[m, "py"], s=14,
                   color=REGION_COLORS[(rn - 1) % 10], label=f"Region {rn}", alpha=0.8)
        cxp, cyp = centers[r]
        ax.scatter([cxp], [cyp], s=260, color="white", edgecolor="black", marker="o", zorder=5)
        ax.text(cxp, cyp, str(rn), ha="center", va="center", fontweight="bold", zorder=6)

    ax.set_xlim(0, CROP_W); ax.set_ylim(CROP_H, 0)
    ax.set_title(f"{poster}  --  {method_label} fixation clusters (all {sub['participant'].nunique()} participants)\n"
                 f"{subtitle}", fontsize=11)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def plot_average_gaze_path(sub, centers, stats, order, region_ids, poster, img_file, out_path,
                            method_label, subtitle):
    bg = bg_image(img_file)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(bg, extent=[0, CROP_W, CROP_H, 0])
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    num_of = dict(zip(stats["region_raw_id"], stats["region_num"]))
    pct_of = dict(zip(stats["region_raw_id"], stats["pct_gaze_time"]))

    for r in region_ids:
        pts = sub.loc[sub["region"] == r, ["px", "py"]].to_numpy()
        rn = num_of[r]
        col = REGION_COLORS[(rn - 1) % 10]
        if len(pts) >= 3:
            try:
                hull = ConvexHull(pts)
                poly = MplPolygon(pts[hull.vertices], closed=True, facecolor=col,
                                  edgecolor="white", alpha=0.30, linewidth=1.5, zorder=2)
                ax.add_patch(poly)
            except Exception:
                pass

    for a, b in zip(order[:-1], order[1:]):
        x0, y0 = centers[a]; x1, y1 = centers[b]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="white", lw=2), zorder=4)

    for r in region_ids:
        cxp, cyp = centers[r]
        rn = num_of[r]
        ax.scatter([cxp], [cyp], s=120 + 26 * pct_of[r], color="black",
                   edgecolor="white", alpha=0.9, zorder=5)
        ax.text(cxp, cyp - 34, f"Region {rn}\n{pct_of[r]:.0f}% of gaze time",
                color="white", fontweight="bold", ha="center", va="bottom",
                fontsize=9, zorder=6,
                path_effects=[pe.withStroke(linewidth=3, foreground="black")])

    ax.set_xlim(0, CROP_W); ax.set_ylim(CROP_H, 0)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{poster}  --  Average Scanpath by Region ({method_label})\n{subtitle}",
                 color="white", fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, facecolor="black")
    plt.close(fig)
