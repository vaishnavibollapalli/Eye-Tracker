"""
=============================================================================
Compare DBSCAN / Agglomerative / Divisive clustering results per poster and
pick a winner.
=============================================================================
Reads the k_selection.csv each clustering script already writes (its top row,
after sorting by the combined silhouette + Davies-Bouldin separation score,
IS the method's chosen k and its metrics).

IMPORTANT: that per-method "score" column is normalised against only that
method's OWN 3-5 candidate k values, so it always tops out near 1.0 for
whichever k that method itself preferred -- comparing those numbers directly
across methods would be comparing different scales and would trivially
favour whichever method ran last. Instead, this script re-normalises
silhouette and Davies-Bouldin across the THREE METHODS' final results for
each poster, then picks the winner from that shared scale.

DBSCAN's silhouette/Davies-Bouldin are also computed only on its non-noise
points (the rest get folded in afterward by 1-NN), while Agglomerative/
Divisive score every point -- so DBSCAN's cross-method score is additionally
discounted by its own noise fraction, so it can't win just by grading its
own easiest subset of points.

Outputs:
  output/Hierarchical Clustering/method_comparison.csv
  output/Hierarchical Clustering/method_comparison.md
=============================================================================
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def separation_score(sil: np.ndarray, db: np.ndarray) -> np.ndarray:
    """Same formula each clustering script uses internally (silhouette up,
    Davies-Bouldin down, each min-max normalised, averaged 50/50) -- applied
    here across the THREE METHODS' results so they land on one shared scale."""
    def norm(a):
        lo, hi = np.min(a), np.max(a)
        return np.ones_like(a, dtype=float) if hi - lo < 1e-12 else (a - lo) / (hi - lo)
    return 0.5 * norm(sil) + 0.5 * (1 - norm(db))

HERE = Path(__file__).resolve().parent
METHODS = {
    "DBSCAN":        (HERE / "DBSCAN output", "dbscan_k_selection.csv"),
    "Agglomerative": (HERE / "Hierarchical Clustering" / "Agglomerative", "k_selection.csv"),
    "Divisive":      (HERE / "Hierarchical Clustering" / "Divisive", "k_selection.csv"),
}
OUT_DIR = HERE / "Hierarchical Clustering"


def poster_display_name(poster_key: str, label: str) -> str:
    return label


def load_poster_list():
    # any one method's folder lists every poster that was actually clustered
    base, _ = next(iter(METHODS.values()))
    return sorted(p.name for p in base.iterdir() if p.is_dir())


def main():
    rows = []
    for poster in load_poster_list():
        per_method = {}
        for method, (base, fname) in METHODS.items():
            f = base / poster / fname
            if not f.exists():
                continue
            df = pd.read_csv(f)
            if df.empty:
                continue
            top = df.iloc[0]
            noise = float(top["noise_frac"]) if "noise_frac" in df.columns else 0.0
            per_method[method] = dict(
                k=int(top["k"] if "k" in df.columns else top["n_clusters"]),
                silhouette=float(top["silhouette"]),
                davies_bouldin=float(top["davies_bouldin"]),
                noise_pct=noise * 100,
                noise_frac=noise,
            )
        if not per_method:
            continue

        # re-normalise silhouette/Davies-Bouldin across THIS poster's three
        # method results (not each method's own internal k-candidates), so
        # the comparison is on one shared scale; then discount DBSCAN by its
        # own noise fraction so excluded points don't inflate its score.
        names = list(per_method)
        sil_arr = np.array([per_method[m]["silhouette"] for m in names])
        db_arr = np.array([per_method[m]["davies_bouldin"] for m in names])
        cross_scores = separation_score(sil_arr, db_arr)
        for m, s in zip(names, cross_scores):
            noise = per_method[m]["noise_frac"]
            per_method[m]["raw_score"] = float(s)
            per_method[m]["adj_score"] = float(s) * (1 - noise)

        winner = max(per_method, key=lambda m: per_method[m]["adj_score"])
        w = per_method[winner]
        others = [m for m in per_method if m != winner]
        reason_bits = [f"highest separation score ({w['adj_score']:.3f}"
                       + (f" after a {w['noise_pct']:.0f}% noise discount" if w["noise_pct"] > 0.5 else "")
                       + f"), silhouette {w['silhouette']:.3f}, Davies-Bouldin {w['davies_bouldin']:.3f}"]
        for m in others:
            o = per_method[m]
            reason_bits.append(f"{m} scored {o['adj_score']:.3f} "
                               f"(silhouette {o['silhouette']:.3f}, DB {o['davies_bouldin']:.3f}"
                               + (f", {o['noise_pct']:.0f}% noise" if o["noise_pct"] > 0.5 else "") + ")")
        reason = f"{winner} wins: " + "; ".join(reason_bits) + "."

        row = dict(poster=poster, winner=winner, reason=reason)
        for m, vals in per_method.items():
            for k, v in vals.items():
                row[f"{m}_{k}"] = v
        rows.append(row)

    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "method_comparison.csv", index=False)

    md = ["# Clustering Method Comparison -- per poster", ""]
    for _, r in out.iterrows():
        md.append(f"## {r['poster']}")
        md.append(f"**Winner: {r['winner']}**  -  {r['reason']}")
        md.append("")
        tbl = []
        for m in METHODS:
            pfx = f"{m}_"
            if f"{pfx}k" not in r or pd.isna(r.get(f"{pfx}k")):
                continue
            tbl.append(dict(method=m, k=int(r[f"{pfx}k"]), silhouette=round(r[f"{pfx}silhouette"], 3),
                            davies_bouldin=round(r[f"{pfx}davies_bouldin"], 3),
                            noise_pct=round(r[f"{pfx}noise_pct"], 1),
                            separation_score=round(r[f"{pfx}adj_score"], 3)))
        md.append(pd.DataFrame(tbl).to_markdown(index=False))
        md.append("")
    (OUT_DIR / "method_comparison.md").write_text("\n".join(md), encoding="utf-8")

    print(out[["poster", "winner", "reason"]].to_string(index=False))
    print(f"\nWrote {OUT_DIR / 'method_comparison.csv'}")
    print(f"Wrote {OUT_DIR / 'method_comparison.md'}")


if __name__ == "__main__":
    main()
