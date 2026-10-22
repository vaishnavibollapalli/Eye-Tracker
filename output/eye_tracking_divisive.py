"""
=============================================================================
Eye-Tracking Poster Attention Analysis -- Divisive (top-down) hierarchical
clustering
=============================================================================
Same two-stage pattern as the other two clustering scripts:
  Stage A -- choose the number of regions (k) by best silhouette across
             k=3..7.
  Stage B -- take the split tree's state at the chosen k as the final
             regions.

sklearn has no built-in divisive clustering, so this implements the
standard approach (bisecting k-means / DIANA-style): start with all
fixations in one cluster, repeatedly pick the open cluster with the
largest SSE (sum of squared distances to its own centroid) and split it
in two with k-means, until k clusters exist. Because it's genuinely
top-down, the split tree is recorded as it's built and re-drawn as a
"divisive dendrogram" -- root at the top (all fixations), branching
downward to the k leaf regions.

Outputs per poster into output/Hierarchical Clustering/Divisive/<poster>/:
  - dendrogram.png             top-down split tree, root -> k leaf regions
  - divisive_clusters.png      fixations coloured by region, over the poster
  - average_gaze_path.png      region hulls + viewing-order arrows
  - k_selection.csv            silhouette at each candidate k
  - split_tree.csv             every split: which cluster, into what sizes
  - region_stats.csv           per-region stats (same schema as DBSCAN output)
  - fixations_labelled.csv     every fixation with its region label

Usage:
    python eye_tracking_divisive.py
    python eye_tracking_divisive.py --posters EllaRosenblatt-2021
=============================================================================
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
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
OUT_DIR = HERE / "Hierarchical Clustering" / "Divisive"
SEED = 42


# ---------------------------------------------------------------------------
# the divisive (bisecting k-means) tree builder
# ---------------------------------------------------------------------------
def _sse(pts: np.ndarray) -> float:
    if len(pts) < 2:
        return 0.0
    c = pts.mean(axis=0)
    return float(((pts - c) ** 2).sum())


def bisecting_tree(X: np.ndarray, max_k: int, seed: int = SEED):
    """Builds the full top-down split tree up to max_k leaf clusters.
    Returns (nodes, tree_records, labels_by_k):
      nodes[id]        = {"indices": np.ndarray}   (final membership, id 0 = root/all points)
      tree_records      = [{"step","parent","child_a","child_b","n_a","n_b","sse_before"}, ...]
                          one entry per split, in the order performed (step = k right after the split)
      labels_by_k[k]    = np.ndarray of length N -- node-id label per point, when k clusters are open
    """
    n = len(X)
    nodes = {0: {"indices": np.arange(n)}}
    open_ids = [0]
    labels_by_k = {1: np.zeros(n, dtype=int)}
    tree_records = []
    next_id = 1

    for k in range(2, max_k + 1):
        sses = {cid: _sse(X[nodes[cid]["indices"]]) for cid in open_ids
                if len(nodes[cid]["indices"]) >= 2}
        if not sses:
            break
        split_id = max(sses, key=sses.get)
        idx = nodes[split_id]["indices"]
        km = KMeans(n_clusters=2, n_init=10, random_state=seed).fit(X[idx])
        idx_a, idx_b = idx[km.labels_ == 0], idx[km.labels_ == 1]
        id_a, id_b = next_id, next_id + 1
        next_id += 2
        nodes[id_a] = {"indices": idx_a}
        nodes[id_b] = {"indices": idx_b}
        tree_records.append(dict(step=k, parent=split_id, child_a=id_a, child_b=id_b,
                                 n_a=len(idx_a), n_b=len(idx_b), sse_before=sses[split_id]))
        open_ids.remove(split_id)
        open_ids += [id_a, id_b]

        labels = np.empty(n, dtype=int)
        for cid in open_ids:
            labels[nodes[cid]["indices"]] = cid
        labels_by_k[k] = labels.copy()

    return nodes, tree_records, labels_by_k


def cluster_poster_divisive(sub: pd.DataFrame):
    sub = sub.copy()
    sub["px"] = sub["canvas_x"] - CROP_X0
    sub["py"] = sub["canvas_y"] - CROP_Y0

    # drop stray/isolated fixations before the bisecting process even starts,
    # so a lone point can't get picked up as (half of) its own split
    keep = filter_outliers(sub[["px", "py"]].to_numpy())
    n_dropped = int((~keep).sum())
    if n_dropped:
        sub = sub.loc[keep].reset_index(drop=True)

    X = sub[["px", "py"]].to_numpy()
    nodes, tree_records, labels_by_k = bisecting_tree(X, K_RANGE[1])

    rows = []
    for k in range(K_RANGE[0], K_RANGE[1] + 1):
        if k not in labels_by_k:
            continue
        labels = labels_by_k[k]
        if len(set(labels)) < 2:
            continue
        sub_k = sub.copy(); sub_k["region"] = labels
        rows.append(dict(k=k, silhouette=silhouette_score(X, labels),
                         davies_bouldin=davies_bouldin_score(X, labels),
                         calinski_harabasz=calinski_harabasz_score(X, labels),
                         crosses=any_hulls_cross(sub_k, sorted(set(labels)))))
    k_selection = pd.DataFrame(rows)
    if k_selection.empty:
        raise RuntimeError("no viable k found for divisive clustering")
    # legacy combined score, kept for reference/comparison in the output table
    k_selection["score"] = separation_score(k_selection["silhouette"].to_numpy(),
                                            k_selection["davies_bouldin"].to_numpy())

    # the actual decision: Davies-Bouldin primary, silhouette secondary check,
    # crossing regions disqualified, most clusters wins among what survives
    decision = decide_k(k_selection)
    chosen_k = int(decision["k"])
    k_selection = k_selection.sort_values("k").reset_index(drop=True)
    k_selection["chosen"] = k_selection["k"] == chosen_k

    labels = labels_by_k[chosen_k]
    sub["region"] = labels

    region_ids = sorted(set(labels))
    centers = duration_weighted_centers(sub, region_ids)
    pruned_records = [r for r in tree_records if r["step"] <= chosen_k]

    info = dict(k=chosen_k, silhouette=float(decision["silhouette"]),
               davies_bouldin=float(decision["davies_bouldin"]),
               score=float(decision["score"]), n_dropped=n_dropped,
               crosses=bool(decision["crosses"]),
               used_crossing_fallback=bool(decision["used_crossing_fallback"]),
               region_ids=region_ids, centers=centers, k_selection=k_selection,
               tree_records=pruned_records, n_points=len(sub))
    return sub, info


# ---------------------------------------------------------------------------
# top-down dendrogram
# ---------------------------------------------------------------------------
def plot_divisive_dendrogram(info, stats, poster, out_path):
    chosen_k, records, n = info["k"], info["tree_records"], info["n_points"]
    num_of = dict(zip(stats["region_raw_id"], stats["region_num"]))

    draw = {0: {"children": None, "size": n, "step_of_split": None}}
    for r in records:
        draw[r["parent"]]["children"] = (r["child_a"], r["child_b"])
        draw[r["parent"]]["step_of_split"] = r["step"]
        draw[r["child_a"]] = {"children": None, "size": r["n_a"], "step_of_split": None}
        draw[r["child_b"]] = {"children": None, "size": r["n_b"], "step_of_split": None}

    counter = itertools.count()
    def layout(nid):
        node = draw[nid]
        if node["children"] is None:
            node["x"] = next(counter)
        else:
            a, b = node["children"]
            layout(a); layout(b)
            node["x"] = (draw[a]["x"] + draw[b]["x"]) / 2
    layout(0)

    def y_of(nid):
        node = draw[nid]
        return 0 if node["children"] is None else (chosen_k - node["step_of_split"] + 1)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    for nid, node in draw.items():
        if node["children"] is None:
            continue
        a, b = node["children"]
        yn = y_of(nid)
        xa, ya = draw[a]["x"], y_of(a)
        xb, yb = draw[b]["x"], y_of(b)
        ax.plot([xa, xa], [ya, yn], color="#7d8a87", linewidth=1.4)
        ax.plot([xb, xb], [yb, yn], color="#7d8a87", linewidth=1.4)
        ax.plot([xa, xb], [yn, yn], color="#7d8a87", linewidth=1.4)

    for nid, node in draw.items():
        if node["children"] is not None:
            continue
        rn = num_of.get(nid, None)
        col = REGION_COLORS[(rn - 1) % 10] if rn is not None else "#333333"
        ax.scatter([node["x"]], [0], s=90, color=col, edgecolor="black", zorder=5)
        ax.text(node["x"], -0.35, f"Region {rn}\nn={node['size']}", ha="center", va="top", fontsize=8)

    ax.set_xlim(-0.5, chosen_k - 0.5)
    ax.set_xticks([])
    ax.set_ylim(-1.3, chosen_k - 0.3)
    ax.set_yticks(range(0, chosen_k))
    ax.set_ylabel("split step (root at top -> final regions at bottom)")
    ax.set_title(f"{poster}  --  Divisive split tree (bisecting k-means)\n"
                f"root split down to k={chosen_k} regions (DB/silhouette/non-crossing decision)", fontsize=11)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
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

    summary_lines = ["# Divisive (Bisecting K-Means) Region Analysis -- summary", "",
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

        sub, info = cluster_poster_divisive(sub_all)
        if info["n_dropped"]:
            print(f"  dropped {info['n_dropped']} stray/isolated fixations before clustering "
                  f"({info['n_dropped'] / len(sub_all) * 100:.1f}%)")
        print("  Stage A -- candidates by k (bisecting k-means), 'crosses' = overlapping region hulls:")
        print(info["k_selection"].to_string(index=False))
        print(f"  Decision: k={info['k']} (DB primary, silhouette secondary, non-crossing, most clusters) "
              f"silhouette={info['silhouette']:.4f}  Davies-Bouldin={info['davies_bouldin']:.4f}"
              + ("  [all candidates crossed -- used anyway]" if info["used_crossing_fallback"] else ""))

        stats, order = region_stats(sub, info["centers"], info["region_ids"])
        stats.to_csv(pdir / "region_stats.csv", index=False)
        sub.to_csv(pdir / "fixations_labelled.csv", index=False)
        info["k_selection"].to_csv(pdir / "k_selection.csv", index=False)
        pd.DataFrame(info["tree_records"]).to_csv(pdir / "split_tree.csv", index=False)

        subtitle = (f"k={info['k']} regions, bisecting k-means, silhouette={info['silhouette']:.3f}, "
                   f"Davies-Bouldin={info['davies_bouldin']:.3f}")
        plot_clusters(sub, info["centers"], stats, info["region_ids"], poster, img_file,
                     pdir / "divisive_clusters.png", "Divisive (bisecting k-means)", subtitle)
        plot_average_gaze_path(sub, info["centers"], stats, order, info["region_ids"], poster, img_file,
                               pdir / "average_gaze_path.png", "Divisive", subtitle)
        plot_divisive_dendrogram(info, stats, poster, pdir / "dendrogram.png")

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

    (OUT_DIR / "Divisive_Region_Analysis_summary.md").write_text(
        "\n".join(summary_lines), encoding="utf-8")
    print(f"\nWrote {OUT_DIR / 'Divisive_Region_Analysis_summary.md'}")
    print("Done.")


if __name__ == "__main__":
    main()
