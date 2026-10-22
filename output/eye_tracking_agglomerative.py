"""
=============================================================================
Eye-Tracking Poster Attention Analysis -- Agglomerative (bottom-up)
hierarchical clustering
=============================================================================
Same two-stage pattern as eye_tracking_dbscan.py:
  Stage A -- choose the number of regions (k) by best silhouette across
             k=3..7 (Ward-linkage agglomerative clustering at each k).
  Stage B -- take the merge history at the chosen k as the final regions.

Agglomerative clustering starts with every fixation as its own cluster and
repeatedly merges the two closest clusters (Ward linkage: the pair whose
merge increases within-cluster variance the least) until only one remains.
"Choosing k" here means cutting that merge tree at the point where exactly
k clusters remain -- unlike DBSCAN there's no eps/min_samples to search,
so the merge tree is fixed and only the CUT (k) is chosen via silhouette.

Outputs per poster into output/Hierarchical Clustering/Agglomerative/<poster>/:
  - dendrogram.png            merge tree (top 40 merges), cut line at chosen k
  - agglomerative_clusters.png  fixations coloured by region, over the poster
  - average_gaze_path.png     region hulls + viewing-order arrows
  - k_selection.csv           silhouette at each candidate k
  - region_stats.csv          per-region stats (same schema as DBSCAN output)
  - fixations_labelled.csv    every fixation with its region label

Usage:
    python eye_tracking_agglomerative.py
    python eye_tracking_agglomerative.py --posters EllaRosenblatt-2021
=============================================================================
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hierarchical_common import (
    POSTERS, K_RANGE, CROP_X0, CROP_Y0, REGION_COLORS,
    load_fixations, region_stats, duration_weighted_centers,
    plot_clusters, plot_average_gaze_path, filter_outliers, separation_score,
    any_hulls_cross, decide_k,
)

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE / "Hierarchical Clustering" / "Agglomerative"


# ---------------------------------------------------------------------------
# Stage A + B -- pick k by silhouette, cut the ward-linkage tree there
# ---------------------------------------------------------------------------
def cluster_poster_agglomerative(sub: pd.DataFrame):
    sub = sub.copy()
    sub["px"] = sub["canvas_x"] - CROP_X0
    sub["py"] = sub["canvas_y"] - CROP_Y0

    # drop stray/isolated fixations before building the merge tree at all, so
    # they can't anchor their own tiny cluster or stretch a real region's hull
    keep = filter_outliers(sub[["px", "py"]].to_numpy())
    n_dropped = int((~keep).sum())
    if n_dropped:
        sub = sub.loc[keep].reset_index(drop=True)

    X = sub[["px", "py"]].to_numpy()
    Z = linkage(X, method="ward")   # the full bottom-up merge tree, built once

    rows = []
    for k in range(K_RANGE[0], K_RANGE[1] + 1):
        labels = fcluster(Z, t=k, criterion="maxclust")
        if len(set(labels)) < 2:
            continue
        sub_k = sub.copy(); sub_k["region"] = labels
        rows.append(dict(k=k, silhouette=silhouette_score(X, labels),
                         davies_bouldin=davies_bouldin_score(X, labels),
                         calinski_harabasz=calinski_harabasz_score(X, labels),
                         crosses=any_hulls_cross(sub_k, sorted(set(labels)))))
    k_selection = pd.DataFrame(rows)
    if k_selection.empty:
        raise RuntimeError("no viable k found for agglomerative clustering")
    # legacy combined score, kept for reference/comparison in the output table
    k_selection["score"] = separation_score(k_selection["silhouette"].to_numpy(),
                                            k_selection["davies_bouldin"].to_numpy())

    # the actual decision: Davies-Bouldin primary, silhouette secondary check,
    # crossing regions disqualified, most clusters wins among what survives
    # (see hierarchical_common.decide_k for the exact rule)
    decision = decide_k(k_selection)
    chosen_k = int(decision["k"])
    k_selection = k_selection.sort_values("k").reset_index(drop=True)
    k_selection["chosen"] = k_selection["k"] == chosen_k

    labels = fcluster(Z, t=chosen_k, criterion="maxclust")   # 1..chosen_k
    sub["region"] = labels

    region_ids = sorted(set(labels))
    centers = duration_weighted_centers(sub, region_ids)

    info = dict(k=chosen_k, silhouette=float(decision["silhouette"]),
               davies_bouldin=float(decision["davies_bouldin"]),
               score=float(decision["score"]), n_dropped=n_dropped,
               crosses=bool(decision["crosses"]),
               used_crossing_fallback=bool(decision["used_crossing_fallback"]),
               region_ids=region_ids, centers=centers, k_selection=k_selection, Z=Z)
    return sub, info


def plot_dendrogram(Z, chosen_k, poster, out_path, n_points):
    fig, ax = plt.subplots(figsize=(11, 5.5))
    # cut height that yields exactly chosen_k clusters: the (n-k)-th merge height
    n = n_points
    # midpoint between the merge that creates k clusters and the previous one,
    # so the horizontal cut line sits cleanly between the two heights
    lower = Z[n - chosen_k - 1, 2] if 0 <= n - chosen_k - 1 < len(Z) else 0
    upper = Z[n - chosen_k, 2] if n - chosen_k < len(Z) else Z[-1, 2]
    cut_y = (lower + upper) / 2

    dendrogram(Z, ax=ax, truncate_mode="lastp", p=40, show_leaf_counts=True,
              leaf_font_size=8, color_threshold=cut_y, above_threshold_color="#9aa5a3")
    ax.axhline(cut_y, color="#c0392b", linestyle="--", linewidth=1.3)
    ax.text(ax.get_xlim()[1], cut_y, f"  cut at k={chosen_k}", color="#c0392b",
           fontsize=9, va="center", fontweight="bold")
    ax.set_title(f"{poster}  --  Ward-linkage merge tree (last 40 merges shown)\n"
                f"cut into k={chosen_k} regions (chosen by silhouette)", fontsize=11)
    ax.set_xlabel("fixations merged (leaf = cluster of size shown in parentheses)")
    ax.set_ylabel("merge distance (Ward)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--posters", nargs="*", default=None)
    args = ap.parse_args()

    posters = dict(POSTERS)
    if args.posters:
        want = {f"poster_{p}" if not p.startswith("poster_") else p for p in args.posters}
        posters = {k: v for k, v in POSTERS.items() if k in want}
        if not posters:
            sys.exit(f"none of {sorted(want)} match known posters {list(POSTERS)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fixations = load_fixations(posters, args.refresh)

    summary_lines = ["# Agglomerative (Ward) Region Analysis -- summary", "",
                     f"Posters: {', '.join(posters)}",
                     f"Participants pooled: {fixations['participant'].nunique()}", ""]

    for poster in posters:
        img_file = posters[poster][1]
        sub_all = fixations[fixations["poster"] == poster]
        if sub_all.empty:
            print(f"\n=== {poster}: NO fixations, skipped ===")
            continue

        pdir = OUT_DIR / poster
        pdir.mkdir(parents=True, exist_ok=True)
        print(f"\n=== {poster}  ({len(sub_all)} fixations, "
              f"{sub_all['participant'].nunique()} participants) ===")

        sub, info = cluster_poster_agglomerative(sub_all)
        if info["n_dropped"]:
            print(f"  dropped {info['n_dropped']} stray/isolated fixations before clustering "
                  f"({info['n_dropped'] / len(sub_all) * 100:.1f}%)")
        print("  Stage A -- candidates by k (Ward-linkage cut), 'crosses' = overlapping region hulls:")
        print(info["k_selection"].to_string(index=False))
        print(f"  Decision: k={info['k']} (DB primary, silhouette secondary, non-crossing, most clusters) "
              f"silhouette={info['silhouette']:.4f}  Davies-Bouldin={info['davies_bouldin']:.4f}"
              + ("  [all candidates crossed -- used anyway]" if info["used_crossing_fallback"] else ""))

        stats, order = region_stats(sub, info["centers"], info["region_ids"])
        stats.to_csv(pdir / "region_stats.csv", index=False)
        sub.drop(columns=["region_raw"], errors="ignore").to_csv(pdir / "fixations_labelled.csv", index=False)
        info["k_selection"].to_csv(pdir / "k_selection.csv", index=False)

        subtitle = (f"k={info['k']} regions, Ward linkage, silhouette={info['silhouette']:.3f}, "
                   f"Davies-Bouldin={info['davies_bouldin']:.3f}")
        plot_clusters(sub, info["centers"], stats, info["region_ids"], poster, img_file,
                     pdir / "agglomerative_clusters.png", "Agglomerative (Ward)", subtitle)
        plot_average_gaze_path(sub, info["centers"], stats, order, info["region_ids"], poster, img_file,
                               pdir / "average_gaze_path.png", "Agglomerative", subtitle)
        plot_dendrogram(info["Z"], info["k"], poster, pdir / "dendrogram.png", len(sub))

        order_nums = [int(stats.loc[stats["region_raw_id"] == r, "region_num"].iloc[0]) for r in order]
        print("  region stats:")
        print(stats.to_string(index=False))
        print(f"  aggregate viewing order (Region #): {' -> '.join(map(str, order_nums))}")

        summary_lines += [
            f"## {poster}", "",
            (f"- Dropped {info['n_dropped']} stray/isolated fixations before clustering "
             f"({info['n_dropped'] / len(sub_all) * 100:.1f}%)" if info["n_dropped"] else
             "- No fixations dropped as outliers"),
            f"- k candidates (DB primary, silhouette secondary, non-crossing, most-clusters-wins):", "",
            info["k_selection"].to_markdown(index=False), "",
            f"- Chosen k={info['k']}, silhouette={info['silhouette']:.3f}, "
            f"Davies-Bouldin={info['davies_bouldin']:.3f}"
            + ("  _(all candidates crossed -- used anyway)_" if info["used_crossing_fallback"] else ""),
            f"- Aggregate viewing order: {' -> '.join('R' + str(n) for n in order_nums)}", "",
            stats.to_markdown(index=False), "",
        ]

    (OUT_DIR / "Agglomerative_Region_Analysis_summary.md").write_text(
        "\n".join(summary_lines), encoding="utf-8")
    print(f"\nWrote {OUT_DIR / 'Agglomerative_Region_Analysis_summary.md'}")
    print("Done.")


if __name__ == "__main__":
    main()
