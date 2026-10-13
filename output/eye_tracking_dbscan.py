
from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon as MplPolygon
from PIL import Image


HERE = Path(__file__).resolve().parent            
PROJECT = HERE.parent
BASE_DIR = PROJECT / "Renamed Signals"            
POSTER_IMG_DIR = PROJECT / "posters"
OUT_DIR = HERE / "DBSCAN output"
CACHE = OUT_DIR / "_cache"

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

# canvas transform: screen coords (1920x1200) -> the 1936x1208 plot canvas
CROP_X0, CROP_Y0 = 7, 68
CROP_X1, CROP_Y1 = 1943, 1276
CROP_W, CROP_H = CROP_X1 - CROP_X0, CROP_Y1 - CROP_Y0      # 1936 x 1208
OFFSET_X, SCALE_X = 7, 1936 / 1920
OFFSET_Y, SCALE_Y = 68, 1208 / 1200

# DBSCAN grid search (mirrors eye_tracking_dbscan.R)
MIN_SAMPLES_GRID = [8, 10, 12, 15, 18, 20, 25, 30]
EPS_GRID = [18, 20, 22, 25, 28, 30, 35, 40, 45, 50, 55, 60, 70, 80]
# narrowed from (3,7): fewer/larger regions read as more distinct and are
# less prone to the adjacent-region bleed you get when k pushes toward 7
K_RANGE = (3, 5)
NOISE_RANGE = (0.02, 0.25)

# pre-clustering outlier filter: a fixation whose distance to its OUTLIER_K-th
# nearest neighbour is far above the pack (robust median + MAD cutoff) is a
# stray/isolated point, not a member of any real attention region -- dropping
# it keeps those strays from dragging a region's boundary out to meet them.
OUTLIER_K = 10
OUTLIER_MAD_MULT = 3.0


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


# STEP 1: extract & transform fixations for every poster, every participant

GAZE_COLS = ["Fixation Index", "Fixation X", "Fixation Y",
             "Fixation Start", "Fixation End", "Fixation Duration"]


def _read_imotions(path: Path, marker: str = "#DATA") -> pd.DataFrame:
    """iMotions CSVs carry a multi-row metadata header ended by a #DATA line;
    the real column header is the line right after it."""
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


def load_fixations(posters: dict, refresh: bool) -> pd.DataFrame:
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE / "fixations_master.csv"
    if cache_file.exists() and not refresh:
        df = pd.read_csv(cache_file)
        have = set(df["poster"].unique())
        if set(posters).issubset(have):
            print(f"Using cached fixations: {cache_file}  ({len(df)} rows)")
            return df[df["poster"].isin(posters)].copy()
        print("Cache is missing some requested posters -- re-extracting.")
    print("Extracting fixations from raw iMotions exports (this takes a few minutes)...")
    df = extract_all_fixations(posters)
    # merge with any existing cache so we don't lose other posters
    if cache_file.exists():
        old = pd.read_csv(cache_file)
        old = old[~old["poster"].isin(posters)]
        df_all = pd.concat([old, df], ignore_index=True)
    else:
        df_all = df
    df_all.to_csv(cache_file, index=False)
    print(f"Cached -> {cache_file}  ({len(df_all)} rows total)")
    return df


# ---------------------------------------------------------------------------
# STEP 4: DBSCAN region clustering
# ---------------------------------------------------------------------------
# Two explicit stages, mirroring how eye_tracking_analysis.R chooses k for
# K-means: (A) decide the NUMBER OF REGIONS first -- for every k in K_RANGE,
# find the best silhouette score achievable at that k across the whole
# (eps, min_samples) grid; the k with the highest such score wins.
# (B) DBSCAN clustering -- re-run with that winning k's (eps, min_samples)
# to get the actual point labels. (DBSCAN has no direct "k" knob, so "fixing
# k" means fixing the density parameters that produced it.)
def cluster_poster_regions_dbscan(sub: pd.DataFrame):
    sub = sub.copy()
    sub["px"] = sub["canvas_x"] - CROP_X0
    sub["py"] = sub["canvas_y"] - CROP_Y0

    # drop stray/isolated fixations before clustering at all, so they can't
    # drag a region's boundary toward them or get folded in as fake "noise"
    keep = filter_outliers(sub[["px", "py"]].to_numpy())
    n_dropped = int((~keep).sum())
    if n_dropped:
        sub = sub.loc[keep].reset_index(drop=True)

    X = sub[["px", "py"]].to_numpy()
    w = sub["duration"].to_numpy()

    def run_grid(k_lo, k_hi, noise_lo, noise_hi):
        """Every (eps, min_samples) combo, with silhouette/DB/CH where viable."""
        tried = []
        for ms in MIN_SAMPLES_GRID:
            for eps in EPS_GRID:
                labels = DBSCAN(eps=eps, min_samples=ms).fit_predict(X)   # -1 = noise
                mask = labels != -1
                n_clusters = len(set(labels[mask]))
                noise_frac = float(np.mean(labels == -1))
                row = dict(min_samples=ms, eps=eps, n_clusters=n_clusters, noise_frac=noise_frac,
                           silhouette=np.nan, davies_bouldin=np.nan, calinski_harabasz=np.nan, ok=False)
                if (k_lo <= n_clusters <= k_hi
                        and noise_lo <= noise_frac <= noise_hi
                        and mask.sum() >= 10):
                    row["silhouette"] = silhouette_score(X[mask], labels[mask])
                    row["davies_bouldin"] = davies_bouldin_score(X[mask], labels[mask])
                    row["calinski_harabasz"] = calinski_harabasz_score(X[mask], labels[mask])
                    row["ok"] = True
                tried.append(row)
        return pd.DataFrame(tried)

    # ---- STAGE A: choose the number of regions (k) by best-achievable
    # separation -- silhouette combined with Davies-Bouldin, not silhouette
    # alone, so a k that only "scores well" by splintering off a tiny tight
    # cluster doesn't win over a k with genuinely well-separated regions.
    #
    # Fallback is graduated, not an all-or-nothing jump to an unrestricted
    # noise ceiling: an uncapped relaxation can "win" by finding a tiny,
    # ultra-dense core (great silhouette/DB on that 15-20% of points) while
    # silently 1-NN-reassigning the other 75-85% of fixations -- a deceptive
    # result, not a genuinely well-separated clustering. Each step below
    # widens the search a little; the noise ceiling never exceeds 0.40.
    attempts = [
        (K_RANGE[0], K_RANGE[1], NOISE_RANGE[0], NOISE_RANGE[1]),   # primary
        (K_RANGE[0], K_RANGE[1], NOISE_RANGE[0], 0.40),             # widen noise ceiling only
        (2, 9, NOISE_RANGE[0], 0.40),                                # widen k too, same noise cap
    ]
    relaxed = False
    tried_df = ok_df = None
    for i, (k_lo, k_hi, n_lo, n_hi) in enumerate(attempts):
        tried_df = run_grid(k_lo, k_hi, n_lo, n_hi)
        ok_df = tried_df[tried_df["ok"]].copy()
        if not ok_df.empty:
            relaxed = i > 0
            break
    else:
        raise RuntimeError("DBSCAN found no usable clustering even after relaxing the grid "
                           "(noise capped at 40% -- widen MIN_SAMPLES_GRID/EPS_GRID instead of "
                           "the noise cap if this keeps happening)")

    ok_df["score"] = separation_score(ok_df["silhouette"].to_numpy(), ok_df["davies_bouldin"].to_numpy())

    # best combined score achievable at each k -> the k selection table
    k_selection = (ok_df.loc[ok_df.groupby("n_clusters")["score"].idxmax()]
                        .sort_values("score", ascending=False)
                        .reset_index(drop=True))
    best_k_row = k_selection.iloc[0]
    chosen_k = int(best_k_row["n_clusters"])

    # ---- STAGE B: DBSCAN clustering, fixed to the (eps, min_samples) that
    # produced the chosen k with the best combined separation score
    ms, eps = int(best_k_row["min_samples"]), int(best_k_row["eps"])
    labels = DBSCAN(eps=eps, min_samples=ms).fit_predict(X)
    best = dict(min_samples=ms, eps=eps, labels=labels,
                silhouette=float(best_k_row["silhouette"]),
                davies_bouldin=float(best_k_row["davies_bouldin"]),
                score=float(best_k_row["score"]),
                n_clusters=chosen_k, noise_frac=float(best_k_row["noise_frac"]))

    labels = best["labels"]
    sub["region_raw"] = labels                     # -1 = noise, kept for reporting

    # fold noise into nearest labelled region (1-NN)
    noise_mask = labels == -1
    labels_filled = labels.copy()
    if noise_mask.any() and (~noise_mask).any():
        knn = KNeighborsClassifier(n_neighbors=1).fit(X[~noise_mask], labels[~noise_mask])
        labels_filled[noise_mask] = knn.predict(X[noise_mask])
    sub["region"] = labels_filled

    # duration-weighted centroid per final region
    region_ids = sorted(set(labels_filled))
    centers = {}
    for r in region_ids:
        idx = labels_filled == r
        centers[r] = (np.average(sub["px"].to_numpy()[idx], weights=w[idx]),
                      np.average(sub["py"].to_numpy()[idx], weights=w[idx]))

    info = dict(min_samples=best["min_samples"], eps=best["eps"],
               k=best["n_clusters"], silhouette=best["silhouette"],
               davies_bouldin=best["davies_bouldin"], score=best["score"],
               noise_frac=best["noise_frac"], relaxed=relaxed, n_dropped=n_dropped,
               region_ids=region_ids, centers=centers, tried=tried_df,
               k_selection=k_selection)
    return sub, info


# STEP 5: region-level statistics
def region_stats(sub: pd.DataFrame, info: dict) -> pd.DataFrame:
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

    cx = {r: info["centers"][r][0] for r in info["region_ids"]}
    cy = {r: info["centers"][r][1] for r in info["region_ids"]}

    out = pd.DataFrame({
        "region_raw_id": pd.Series(info["region_ids"], index=info["region_ids"]),
        "region_num": pd.Series(region_num),
        "n_fixations": n_fix,
        "pct_gaze_time": pct_time.round(2),
        "avg_fixation_ms": avg_span.round(1),
        "first_attention_pct": first_pct.reindex(info["region_ids"]).fillna(0).round(1),
        "avg_entry_ms": avg_entry.round(0),
        "participant_coverage_pct": coverage.round(1),
        "viewing_order": pd.Series(order_pos),
        "center_x": pd.Series(cx).round(1),
        "center_y": pd.Series(cy).round(1),
    }).sort_values("region_num").reset_index(drop=True)
    return out, order



# plots

REGION_COLORS = plt.get_cmap("tab10").colors


def _bg_image(img_file: str):
    im = Image.open(POSTER_IMG_DIR / img_file).convert("RGB").resize((CROP_W, CROP_H))
    return np.asarray(im)


def plot_clusters(sub, info, stats, poster, img_file, out_path):
    bg = _bg_image(img_file)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(bg, extent=[0, CROP_W, CROP_H, 0], alpha=0.35)

    num_of = dict(zip(stats["region_raw_id"], stats["region_num"]))
    noise = sub["region_raw"] == -1
    ax.scatter(sub.loc[noise, "px"], sub.loc[noise, "py"], s=8, c="0.4",
               marker="x", label="noise (folded to nearest)", alpha=0.6)
    for r in info["region_ids"]:
        m = (sub["region"] == r) & (~noise)
        rn = num_of[r]
        ax.scatter(sub.loc[m, "px"], sub.loc[m, "py"], s=14,
                   color=REGION_COLORS[(rn - 1) % 10], label=f"Region {rn}", alpha=0.8)
        cxp, cyp = info["centers"][r]
        ax.scatter([cxp], [cyp], s=260, color="white", edgecolor="black", marker="o", zorder=5)
        ax.text(cxp, cyp, str(rn), ha="center", va="center", fontweight="bold", zorder=6)

    ax.set_xlim(0, CROP_W); ax.set_ylim(CROP_H, 0)
    ax.set_title(f"{poster}  --  DBSCAN fixation clusters (all {sub['participant'].nunique()} participants)\n"
                 f"eps={info['eps']}px, min_samples={info['min_samples']}, "
                 f"k={info['k']} regions, {info['noise_frac']*100:.0f}% noise, "
                 f"silhouette={info['silhouette']:.3f}, Davies-Bouldin={info['davies_bouldin']:.3f}"
                 + ("   [relaxed grid]" if info["relaxed"] else ""), fontsize=11)
    ax.legend(loc="upper right", fontsize=8, framealpha=0.9)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def plot_average_gaze_path(sub, info, stats, order, poster, img_file, out_path):
    bg = _bg_image(img_file)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(bg, extent=[0, CROP_W, CROP_H, 0])
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    num_of = dict(zip(stats["region_raw_id"], stats["region_num"]))
    pct_of = dict(zip(stats["region_raw_id"], stats["pct_gaze_time"]))

    for r in info["region_ids"]:
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

    # viewing-order arrows between centroids
    for a, b in zip(order[:-1], order[1:]):
        x0, y0 = info["centers"][a]
        x1, y1 = info["centers"][b]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="white", lw=2), zorder=4)

    for r in info["region_ids"]:
        cxp, cyp = info["centers"][r]
        rn = num_of[r]
        ax.scatter([cxp], [cyp], s=120 + 26 * pct_of[r], color="black",
                   edgecolor="white", alpha=0.9, zorder=5)
        ax.text(cxp, cyp - 34, f"Region {rn}\n{pct_of[r]:.0f}% of gaze time",
                color="white", fontweight="bold", ha="center", va="bottom",
                fontsize=9, zorder=6,
                path_effects=[pe.withStroke(linewidth=3, foreground="black")])

    ax.set_xlim(0, CROP_W); ax.set_ylim(CROP_H, 0)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{poster}  --  Average Scanpath by Region (DBSCAN)\n"
                 f"k={info['k']} regions, eps={info['eps']}px, min_samples={info['min_samples']}, "
                 f"{info['noise_frac']*100:.0f}% noise re-assigned to nearest region",
                 color="white", fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, facecolor="black")
    plt.close(fig)

# main

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true",
                    help="re-extract fixations from the raw exports (slow)")
    ap.add_argument("--posters", nargs="*", default=None,
                    help="subset of poster keys (without the 'poster_' prefix)")
    args = ap.parse_args()

    posters = dict(POSTERS)
    if args.posters:
        want = {f"poster_{p}" if not p.startswith("poster_") else p for p in args.posters}
        posters = {k: v for k, v in POSTERS.items() if k in want}
        if not posters:
            sys.exit(f"none of {sorted(want)} match known posters {list(POSTERS)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fixations = load_fixations(posters, args.refresh)

    summary_lines = ["# DBSCAN Region Analysis -- summary", "",
                     f"Posters: {', '.join(posters)}",
                     f"Participants pooled: {fixations['participant'].nunique()}", ""]

    for poster in posters:
        img_file = posters[poster][1]
        sub_all = fixations[fixations["poster"] == poster]
        if sub_all.empty:
            print(f"\n=== {poster}: NO fixations, skipped ===")
            summary_lines.append(f"## {poster}\n\n_No fixations found._\n")
            continue

        pdir = OUT_DIR / poster
        pdir.mkdir(parents=True, exist_ok=True)
        print(f"\n=== {poster}  ({len(sub_all)} fixations, "
              f"{sub_all['participant'].nunique()} participants) ===")

        sub, info = cluster_poster_regions_dbscan(sub_all)
        if info["n_dropped"]:
            print(f"  dropped {info['n_dropped']} stray/isolated fixations before clustering "
                  f"({info['n_dropped'] / len(sub_all) * 100:.1f}%)")
        print("  Stage A -- best separation score (silhouette + Davies-Bouldin) at each k:")
        print(info["k_selection"][["n_clusters", "min_samples", "eps", "silhouette",
                                   "davies_bouldin", "calinski_harabasz", "noise_frac", "score"]]
              .to_string(index=False))
        print(f"  -> k={info['k']} chosen (highest combined separation score across k)")
        print(f"  Stage B -- DBSCAN clustering at k={info['k']}: "
              f"eps={info['eps']}  min_samples={info['min_samples']}  "
              f"noise={info['noise_frac']*100:.1f}%  silhouette={info['silhouette']:.4f}  "
              f"Davies-Bouldin={info['davies_bouldin']:.4f}"
              + ("  [relaxed grid]" if info["relaxed"] else ""))

        stats, order = region_stats(sub, info)
        stats.to_csv(pdir / "region_stats.csv", index=False)
        sub.to_csv(pdir / "fixations_labelled.csv", index=False)
        info["tried"].to_csv(pdir / "dbscan_grid_search.csv", index=False)
        info["k_selection"].to_csv(pdir / "dbscan_k_selection.csv", index=False)

        plot_clusters(sub, info, stats, poster, img_file, pdir / "dbscan_clusters.png")
        plot_average_gaze_path(sub, info, stats, order, poster, img_file,
                               pdir / "average_gaze_path.png")

        order_nums = [int(stats.loc[stats["region_raw_id"] == r, "region_num"].iloc[0])
                      for r in order]
        print("  region stats:")
        print(stats.to_string(index=False))
        print(f"  aggregate viewing order (Region #): {' -> '.join(map(str, order_nums))}")

        summary_lines += [
            f"## {poster}", "",
            (f"- Dropped {info['n_dropped']} stray/isolated fixations before clustering "
             f"({info['n_dropped'] / len(sub_all) * 100:.1f}%)" if info["n_dropped"] else
             "- No fixations dropped as outliers"),
            f"- Number of regions (k) chosen by best combined separation score "
            f"(silhouette + Davies-Bouldin) across k={K_RANGE[0]}..{K_RANGE[1]}:",
            "",
            info["k_selection"][["n_clusters", "silhouette", "davies_bouldin", "calinski_harabasz",
                                 "eps", "min_samples", "noise_frac", "score"]]
                .rename(columns={"n_clusters": "k"}).to_markdown(index=False),
            "",
            f"- Chosen k={info['k']}  ->  DBSCAN eps={info['eps']}px, min_samples={info['min_samples']}, "
            f"silhouette={info['silhouette']:.3f}, Davies-Bouldin={info['davies_bouldin']:.3f}"
            + ("  _(relaxed grid)_" if info["relaxed"] else ""),
            f"- {info['noise_frac']*100:.1f}% of fixations were noise (folded into nearest region)",
            f"- Aggregate viewing order: {' -> '.join('R' + str(n) for n in order_nums)}",
            "",
            stats.to_markdown(index=False),
            "",
        ]

    (OUT_DIR / "DBSCAN_Region_Analysis_summary.md").write_text(
        "\n".join(summary_lines), encoding="utf-8")
    print(f"\nWrote {OUT_DIR / 'DBSCAN_Region_Analysis_summary.md'}")
    print("Done.")


if __name__ == "__main__":
    main()
