"""
=============================================================================
Cluster Parameter Explorer -- standalone, single-file
=============================================================================
Given a poster, tries a wide range of PARAMETERS across all three clustering
methods (not just "which k") and picks the single best (method, parameters)
combination for that poster -- rather than deciding each method's own best k
and then comparing three separate decisions, every candidate from every
method is thrown into one shared pool and ranked together.

Parameters varied per method (this is the actual "changing the parameters"
part -- previous scripts only varied k; here each method's other knobs move
too):
  DBSCAN         eps x min_samples (a grid, same idea as before)
  Agglomerative  linkage method (ward / complete / average) x k
  Divisive       split-selection strategy (bisect the highest-SSE cluster vs.
                 the largest-by-size cluster) x k

Decision rule for "the best one" (applied once, across the pooled
candidates from all three methods together):
  1. Davies-Bouldin primary -- keep candidates within 15% of the best (lowest)
  2. Silhouette secondary check -- within 15% of the best among those
  3. Crossing regions (meaningfully overlapping convex hulls, >15% of the
     smaller region's area) are disqualified outright
  4. Most clusters (largest k) wins among whatever survives

This file is intentionally standalone -- it does not import anything from
output/ (no dependency on the other clustering scripts having been run
first). It DOES reuse output/DBSCAN output/_cache/fixations_master.csv as a
fast DATA path if that cache happens to exist (it's just a CSV of already-
extracted fixations, not code); if it doesn't exist, this script falls back
to extracting fixations itself directly from Renamed Signals/.

Nothing is written to output/ by default -- this just prints a report. Pass
--save-dir to also save one diagnostic plot + a CSV of every candidate tried,
to a location of your choice (defaults to ./cluster_explorer_results next to
this script, well outside output/).

Usage:
    python cluster_param_explorer.py --poster EllaRosenblatt-2021
    python cluster_param_explorer.py                                  # all 15 posters
    python cluster_param_explorer.py --poster EllaRosenblatt-2021 --top 10
    python cluster_param_explorer.py --poster EllaRosenblatt-2021 --save-dir ./cluster_explorer_results
=============================================================================
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

HERE = Path(__file__).resolve().parent
BASE_DIR = HERE / "Renamed Signals"
POSTER_IMG_DIR = HERE / "posters"
FIXATION_CACHE = HERE / "output" / "DBSCAN output" / "_cache" / "fixations_master.csv"
N_PARTICIPANTS = 48

POSTERS = {
    "ArminHofman-1955":    ("Armin Hofman- 1955", "Armin Hofman- 1955.jpg"),
    "BarryCeck-1988":      ("Barry Ceck - 1988", "Barry Ceck - 1988.jpg"),
    "DavidCarson":         ("David Carson", "David Carson.jpg"),
    "DavidCarson-1990":    ("David Carson - 1990", "David Carson - 1990.jpg"),
    "EllaRosenblatt-2021": ("Ella Rosenblatt- 2021", "Ella Rosenblatt- 2021.jpg"),
    "IrisChung-2015":      ("Iris Chung- 2015", "Iris Chung- 2015.jpg"),
    "JanTschichold-1927-DieFrauohneNamen": (
        "Jan Tschichold-1927-Die Frau ohne Namen", "Jan Tschichold-1927-Die Frau ohne Namen.JPG"),
    "JanTschichold-1938-Der": ("Jan Tschichold-1938-Der", "Jan Tschichold-1938-Der.JPG"),
    "JoostSchmidt-1923-Saatliches": (
        "Joost Schmidt-1923-Saatliches", "Joost Schmidt-1923-Saatliches.JPG"),
    "PaulRand-1947":       ("Paul Rand, 1947", "Paul Rand, 1947.jpg"),
    "PaulaScher-1995":     ("Paula Scher - 1995", "Paula Scher - 1995.jpg"),
    "ScottBarry-2010":     ("Scott Barry- 2010", "Scott Barry- 2010.jpg"),
    "SeanAlatorre":        ("Sean Alatorre", "Sean Alatorre.jpg"),
    "bookcover":           ("bookcover", "bookcover.jpg"),
    "nancy":               ("nancy poster", "nancy.jpg"),
}

# canvas transform: screen coords (1920x1200) -> the 1936x1208 plot canvas
# the rest of this project's outputs use
CROP_X0, CROP_Y0 = 7, 68
OFFSET_X, SCALE_X = 7, 1936 / 1920
OFFSET_Y, SCALE_Y = 68, 1208 / 1200

# --- the parameters this script varies -------------------------------------
DBSCAN_EPS_GRID = [18, 22, 25, 28, 30, 35, 40, 45, 50, 55, 60, 70, 80]
DBSCAN_MIN_SAMPLES_GRID = [8, 10, 12, 15, 18, 20, 25, 30]
DBSCAN_NOISE_CEILING = 0.40

AGGLOMERATIVE_LINKAGES = ["ward", "complete", "average"]

DIVISIVE_STRATEGIES = ["largest_sse", "largest_size"]

K_RANGE = (3, 8)
OUTLIER_K, OUTLIER_MAD_MULT = 10, 3.0
DB_TOL, SIL_TOL = 0.15, 0.15
CROSS_OVERLAP_THRESHOLD = 0.15


# ---------------------------------------------------------------------------
# data loading (cache if present, self-contained extraction otherwise)
# ---------------------------------------------------------------------------
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


def _transform_xy(x, y):
    return OFFSET_X + x * SCALE_X, OFFSET_Y + y * SCALE_Y


def _extract_fixations(poster_key: str) -> pd.DataFrame:
    """Self-contained fallback: reads the raw 48-participant iMotions exports
    directly, with no dependency on any other script having run first."""
    stim_name, _img = POSTERS[poster_key]
    gaze_cols = ["Fixation Index", "Fixation X", "Fixation Y",
                "Fixation Start", "Fixation End", "Fixation Duration"]
    rows = []
    for i in range(1, N_PARTICIPANTS + 1):
        pid = f"p{i}"
        pdir = BASE_DIR / pid
        se_path, gz_path = pdir / "Native_SlideEvents.csv", pdir / "ET_RExtAPI-GazeAnalysis.csv"
        if not se_path.exists() or not gz_path.exists():
            continue
        se = _read_imotions(se_path)
        se["Timestamp"] = pd.to_numeric(se["Timestamp"], errors="coerce")
        gz = _read_imotions(gz_path)
        for c in gaze_cols:
            gz[c] = pd.to_numeric(gz[c], errors="coerce")
        fix = (gz.dropna(subset=["Fixation Start", "Fixation Index"])
                 .drop_duplicates(subset="Fixation Index", keep="first"))

        ev = se[se["SourceStimuliName"] == stim_name]
        t0 = ev.loc[ev["SlideEvent"] == "StartMedia", "Timestamp"]
        t1 = ev.loc[ev["SlideEvent"] == "EndMedia", "Timestamp"]
        if t0.empty or t1.empty:
            continue
        t0, t1 = float(t0.iloc[0]), float(t1.iloc[0])
        win = fix[(fix["Fixation Start"] >= t0) & (fix["Fixation Start"] <= t1)]
        if win.empty:
            continue
        cx, cy = _transform_xy(win["Fixation X"].to_numpy(), win["Fixation Y"].to_numpy())
        rows.append(pd.DataFrame({"participant": pid, "canvas_x": cx, "canvas_y": cy,
                                  "duration": win["Fixation Duration"].to_numpy()}))
        print(f"  extracted {pid}", file=sys.stderr)
    if not rows:
        sys.exit(f"No fixations found for poster '{poster_key}' -- check the stimulus name.")
    return pd.concat(rows, ignore_index=True)


def load_points(poster_key: str) -> tuple[np.ndarray, np.ndarray]:
    """Returns (X, weights): the poster's pooled fixation points (px, py) on
    the shared canvas, duration-weighted, with stray outliers already
    dropped."""
    if FIXATION_CACHE.exists():
        # the cache (written by output/eye_tracking_dbscan.py) keys rows by
        # the "poster_<key>" folder name, not the raw stimulus name
        df = pd.read_csv(FIXATION_CACHE)
        sub = df[df["poster"] == f"poster_{poster_key}"]
        if sub.empty:
            sys.exit(f"Cache at {FIXATION_CACHE} has no rows for 'poster_{poster_key}'.")
    else:
        print(f"No fixation cache found at {FIXATION_CACHE} -- extracting from raw exports "
             f"(this takes a few minutes)...", file=sys.stderr)
        sub = _extract_fixations(poster_key)

    px = sub["canvas_x"].to_numpy() - CROP_X0
    py = sub["canvas_y"].to_numpy() - CROP_Y0
    w = sub["duration"].to_numpy()
    X = np.column_stack([px, py])

    keep = _filter_outliers(X)
    return X[keep], w[keep]


def _filter_outliers(X: np.ndarray, k: int = OUTLIER_K, mad_mult: float = OUTLIER_MAD_MULT) -> np.ndarray:
    n = len(X)
    k_eff = min(k, n - 1)
    if k_eff < 1:
        return np.ones(n, dtype=bool)
    nn = NearestNeighbors(n_neighbors=k_eff + 1).fit(X)
    dist, _ = nn.kneighbors(X)
    knn_dist = dist[:, -1]
    med = np.median(knn_dist)
    mad = np.median(np.abs(knn_dist - med)) * 1.4826
    if mad == 0:
        return np.ones(n, dtype=bool)
    return knn_dist <= med + mad_mult * mad


# ---------------------------------------------------------------------------
# convex-hull crossing check (polygon-clip overlap AREA, not a boolean touch
# test -- a yes/no "do they touch" test flags almost every real clustering,
# since a few boundary points always graze a neighbour's hull)
# ---------------------------------------------------------------------------
def _hull(points: np.ndarray):
    if len(points) < 3:
        return None
    from scipy.spatial import ConvexHull
    try:
        return points[ConvexHull(points).vertices]
    except Exception:
        return None


def _signed_area(poly) -> float:
    n = len(poly); s = 0.0
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2


def _clip_convex(subject: list, clip: list) -> list:
    if _signed_area(clip) < 0:
        clip = clip[::-1]

    def inside(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0

    def intersect(p1, p2, a, b):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = a; x4, y4 = b
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-12:
            return p2
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

    output = list(subject)
    for i in range(len(clip)):
        if not output:
            break
        a, b = clip[i], clip[(i + 1) % len(clip)]
        input_list, output = output, []
        s = input_list[-1]
        for e in input_list:
            if inside(e, a, b):
                if not inside(s, a, b):
                    output.append(intersect(s, e, a, b))
                output.append(e)
            elif inside(s, a, b):
                output.append(intersect(s, e, a, b))
            s = e
    return output


def _overlap_fraction(poly_a, poly_b) -> float:
    inter = _clip_convex([tuple(p) for p in poly_a], [tuple(p) for p in poly_b])
    if len(inter) < 3:
        return 0.0
    area_inter = abs(_signed_area(inter))
    smaller = min(abs(_signed_area(poly_a)), abs(_signed_area(poly_b)))
    return 0.0 if smaller < 1e-9 else area_inter / smaller


def regions_cross(X: np.ndarray, labels: np.ndarray, threshold: float = CROSS_OVERLAP_THRESHOLD) -> bool:
    hulls = [h for r in sorted(set(labels)) if (h := _hull(X[labels == r])) is not None]
    for i in range(len(hulls)):
        for j in range(i + 1, len(hulls)):
            if _overlap_fraction(hulls[i], hulls[j]) > threshold:
                return True
    return False


# ---------------------------------------------------------------------------
# candidate generation -- one row per (method, parameters) combination tried
# ---------------------------------------------------------------------------
def _fold_noise(X, labels):
    """DBSCAN only: fold -1/noise points into their nearest labelled region
    (1-NN) so every point ends up with a region, the way the rest of this
    project's DBSCAN output does."""
    noise = labels == -1
    filled = labels.copy()
    if noise.any() and (~noise).any():
        knn = KNeighborsClassifier(n_neighbors=1).fit(X[~noise], labels[~noise])
        filled[noise] = knn.predict(X[noise])
    return filled


def dbscan_candidates(X: np.ndarray) -> list[dict]:
    """DBSCAN's silhouette/Davies-Bouldin are computed only on its non-noise
    "core" points -- the higher the noise fraction, the more that core is a
    cherry-picked easy subset, which inflates both metrics relative to the
    other two methods (which always score on 100% of the points). So on top
    of the hard noise ceiling, every DBSCAN candidate's silhouette/DB are
    additionally discounted by its own noise fraction before they're allowed
    into the shared candidate pool -- see *_adj below, used for ranking."""
    out = []
    for eps in DBSCAN_EPS_GRID:
        for ms in DBSCAN_MIN_SAMPLES_GRID:
            labels = DBSCAN(eps=eps, min_samples=ms).fit_predict(X)
            mask = labels != -1
            k = len(set(labels[mask]))
            noise_frac = float(np.mean(~mask))
            if not (K_RANGE[0] <= k <= K_RANGE[1]) or noise_frac > DBSCAN_NOISE_CEILING or mask.sum() < 10:
                continue
            sil = silhouette_score(X[mask], labels[mask])
            db = davies_bouldin_score(X[mask], labels[mask])
            filled = _fold_noise(X, labels)
            out.append(dict(method="DBSCAN", params=f"eps={eps}, min_samples={ms}",
                            k=k, silhouette=sil, davies_bouldin=db,
                            silhouette_adj=sil * (1 - noise_frac),
                            davies_bouldin_adj=db / max(1 - noise_frac, 0.05),
                            noise_frac=noise_frac,
                            crosses=regions_cross(X, filled), labels=filled))
    return out


def agglomerative_candidates(X: np.ndarray) -> list[dict]:
    out = []
    for method in AGGLOMERATIVE_LINKAGES:
        Z = linkage(X, method=method)
        for k in range(K_RANGE[0], K_RANGE[1] + 1):
            labels = fcluster(Z, t=k, criterion="maxclust")
            if len(set(labels)) < 2:
                continue
            sil = silhouette_score(X, labels)
            db = davies_bouldin_score(X, labels)
            out.append(dict(method="Agglomerative", params=f"linkage={method}",
                            k=k, silhouette=sil, davies_bouldin=db,
                            silhouette_adj=sil, davies_bouldin_adj=db, noise_frac=0.0,
                            crosses=regions_cross(X, labels), labels=labels))
    return out


def _sse(pts: np.ndarray) -> float:
    if len(pts) < 2:
        return 0.0
    c = pts.mean(axis=0)
    return float(((pts - c) ** 2).sum())


def _bisect(X: np.ndarray, max_k: int, strategy: str, seed: int = 42) -> dict[int, np.ndarray]:
    n = len(X)
    nodes = {0: np.arange(n)}
    open_ids = [0]
    labels_by_k = {1: np.zeros(n, dtype=int)}
    next_id = 1
    for k in range(2, max_k + 1):
        if strategy == "largest_sse":
            scores = {cid: _sse(X[nodes[cid]]) for cid in open_ids if len(nodes[cid]) >= 2}
        else:  # largest_size
            scores = {cid: len(nodes[cid]) for cid in open_ids if len(nodes[cid]) >= 2}
        if not scores:
            break
        split_id = max(scores, key=scores.get)
        idx = nodes[split_id]
        km = KMeans(n_clusters=2, n_init=10, random_state=seed).fit(X[idx])
        id_a, id_b = next_id, next_id + 1
        next_id += 2
        nodes[id_a] = idx[km.labels_ == 0]
        nodes[id_b] = idx[km.labels_ == 1]
        open_ids.remove(split_id); open_ids += [id_a, id_b]
        labels = np.empty(n, dtype=int)
        for cid in open_ids:
            labels[nodes[cid]] = cid
        labels_by_k[k] = labels.copy()
    return labels_by_k


def divisive_candidates(X: np.ndarray) -> list[dict]:
    out = []
    for strategy in DIVISIVE_STRATEGIES:
        labels_by_k = _bisect(X, K_RANGE[1], strategy)
        for k in range(K_RANGE[0], K_RANGE[1] + 1):
            if k not in labels_by_k or len(set(labels_by_k[k])) < 2:
                continue
            labels = labels_by_k[k]
            sil = silhouette_score(X, labels)
            db = davies_bouldin_score(X, labels)
            out.append(dict(method="Divisive", params=f"split={strategy}",
                            k=k, silhouette=sil, davies_bouldin=db,
                            silhouette_adj=sil, davies_bouldin_adj=db, noise_frac=0.0,
                            crosses=regions_cross(X, labels), labels=labels))
    return out


# ---------------------------------------------------------------------------
# the decision: one flat pool, one rule, one winner
# ---------------------------------------------------------------------------
def choose_best(candidates: pd.DataFrame, db_tol=DB_TOL, sil_tol=SIL_TOL) -> pd.Series:
    """Davies-Bouldin primary, silhouette secondary, non-crossing required,
    most clusters wins among survivors -- using the noise-ADJUSTED columns
    so DBSCAN can't win just by grading its own easiest subset of points."""
    cand = candidates[~candidates["crosses"]]
    if cand.empty:
        cand = candidates   # nothing avoided crossing -- use everything rather than fail

    best_db = cand["davies_bouldin_adj"].min()
    stage1 = cand[cand["davies_bouldin_adj"] <= best_db * (1 + db_tol)]

    best_sil = stage1["silhouette_adj"].max()
    stage2 = stage1[stage1["silhouette_adj"] >= best_sil * (1 - sil_tol)]

    # most clusters wins; if several parameter settings tie on that k, the
    # best-scoring one among them (not just whichever the grid hit first)
    at_max_k = stage2[stage2["k"] == stage2["k"].max()]
    return at_max_k.loc[at_max_k["davies_bouldin_adj"].idxmin()]


def explore_poster(poster_key: str, top_n: int = 8, save_dir: Path | None = None):
    print(f"\n=== {poster_key} ===")
    X, w = load_points(poster_key)
    print(f"  {len(X)} fixations after outlier filtering")

    rows = dbscan_candidates(X) + agglomerative_candidates(X) + divisive_candidates(X)
    if not rows:
        print("  ! no viable candidates found across any method/parameter combination")
        return None
    df = pd.DataFrame(rows)

    best = choose_best(df)

    cols = ["method", "params", "k", "silhouette", "davies_bouldin",
           "silhouette_adj", "davies_bouldin_adj", "noise_frac", "crosses"]
    show = df[cols].sort_values(["crosses", "davies_bouldin_adj"], ascending=[True, True]).head(top_n)
    print(f"  top {len(show)} candidates by noise-adjusted Davies-Bouldin (non-crossing first):")
    print("  ('_adj' = silhouette/DB after discounting DBSCAN for its own noise fraction -- "
         "that's what the decision actually ranks on)")
    print(show.to_string(index=False))

    print(f"\n  WINNER: {best['method']}  ({best['params']})  k={best['k']}")
    print(f"    silhouette={best['silhouette']:.4f}  Davies-Bouldin={best['davies_bouldin']:.4f}"
         + (f"  (adjusted: sil={best['silhouette_adj']:.4f}, DB={best['davies_bouldin_adj']:.4f})"
            if best["noise_frac"] > 0 else "")
         + (f"  noise={best['noise_frac']*100:.1f}%" if best["noise_frac"] > 0 else "")
         + f"  crosses={bool(best['crosses'])}")

    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
        df.drop(columns=["labels"]).to_csv(save_dir / f"{poster_key}_candidates.csv", index=False)
        _save_plot(poster_key, X, best, save_dir / f"{poster_key}_best.png")
        print(f"  saved {save_dir / f'{poster_key}_candidates.csv'}")
        print(f"  saved {save_dir / f'{poster_key}_best.png'}")

    return best


def _save_plot(poster_key: str, X: np.ndarray, best: pd.Series, out_path: Path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    label, img_file = POSTERS[poster_key]
    im = Image.open(POSTER_IMG_DIR / img_file).convert("RGB")
    W, H = 1936, 1208
    bg = np.asarray(im.resize((W, H)))

    labels = best["labels"]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.imshow(bg, extent=[0, W, H, 0], alpha=0.4)
    cmap = plt.get_cmap("tab10")
    for i, r in enumerate(sorted(set(labels))):
        pts = X[labels == r]
        ax.scatter(pts[:, 0], pts[:, 1], s=12, color=cmap(i % 10), label=f"Region {i + 1}")
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.set_xticks([]); ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=8)
    ax.set_title(f"{label}\nBest: {best['method']} ({best['params']}), k={best['k']}, "
                f"silhouette={best['silhouette']:.3f}, DB={best['davies_bouldin']:.3f}", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--poster", default=None, help="poster key (see POSTERS dict); default: all 15")
    ap.add_argument("--top", type=int, default=8, help="how many candidates to print per poster")
    ap.add_argument("--save-dir", default=None,
                    help="also save a CSV of every candidate + a plot of the winner here "
                         "(NOT inside output/ by default -- nothing is saved unless you pass this)")
    args = ap.parse_args()

    save_dir = Path(args.save_dir).resolve() if args.save_dir else None

    posters = [args.poster] if args.poster else list(POSTERS)
    unknown = [p for p in posters if p not in POSTERS]
    if unknown:
        sys.exit(f"Unknown poster(s) {unknown}. Known: {list(POSTERS)}")

    results = {}
    for p in posters:
        results[p] = explore_poster(p, top_n=args.top, save_dir=save_dir)

    if len(posters) > 1:
        print("\n=== summary across all posters ===")
        for p, best in results.items():
            if best is None:
                print(f"  {p:42s}  (no viable candidate)")
                continue
            print(f"  {p:42s}  {best['method']:14s} {best['params']:22s} k={int(best['k'])}  "
                 f"sil={best['silhouette']:.3f}  DB={best['davies_bouldin']:.3f}")


if __name__ == "__main__":
    main()
