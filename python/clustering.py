import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.neighbors import NearestNeighbors


def _all_metrics(X, labels):
    if len(set(labels)) < 2: return {"sil": -1.0, "db": np.inf, "ch": 0.0}
    mask = labels >= 0
    if mask.sum() < 2: return {"sil": -1.0, "db": np.inf, "ch": 0.0}
    X_clean = X[mask]
    labels_clean = labels[mask]
    if len(set(labels_clean)) < 2: return {"sil": -1.0, "db": np.inf, "ch": 0.0}

    return {
        "sil": silhouette_score(X_clean, labels_clean),
        "db": davies_bouldin_score(X_clean, labels_clean),
        "ch": calinski_harabasz_score(X_clean, labels_clean)
    }


def _filter_outliers_auto(poster_df, img_w, img_h):
    """
    AUTOMATIC OUTLIER HANDLING:
    Step 1: Filter to screen bounds (0..1920, 0..1200)
    Step 2: Filter to poster aspect ratio (drop letterbox bars)
    Step 3: Drop isolated points (nearest-neighbor distance > threshold)
    """
    df = poster_df.copy()
    
    # Bounds for the posters
    df = df[(df["x"] >= 0) & (df["x"] <= 1920) & (df["y"] >= 0) & (df["y"] <= 1200)]
    
    # dropping pillarbox
    screen_ratio = 1920 / 1200
    img_ratio = img_w / img_h
    
    if abs(screen_ratio - img_ratio) > 0.05:
        scale = min(1920 / img_w, 1200 / img_h)
        draw_w = img_w * scale
        draw_h = img_h * scale
        
        x_offset = (1920 - draw_w) / 2
        y_offset = (1200 - draw_h) / 2
        
        df = df[
            (df["x"] >= x_offset) & (df["x"] <= x_offset + draw_w) &
            (df["y"] >= y_offset) & (df["y"] <= y_offset + draw_h)
        ]
    
    # 3. Nearest neighbor distance filter - drop points that are isolated
    if len(df) > 10:
        X = df[["x", "y"]].to_numpy()
        nn = NearestNeighbors(n_neighbors=2).fit(X)
        distances, _ = nn.kneighbors(X)
        
        max_distance = np.sqrt(1920**2 + 1200**2) * 0.1
        keep_mask = distances[:, 1] <= max_distance
        df = df[keep_mask]
    
    return df.reset_index(drop=True)


def cluster_hierarchical_auto(poster_df, poster_name, linkage_method, img_w, img_h):
    poster_df = _filter_outliers_auto(poster_df, img_w, img_h)
    
    X = poster_df[["x", "y"]].to_numpy()
    w = poster_df["duration"].to_numpy()
    Z = linkage(X, method=linkage_method, metric="euclidean")

    scores = []
    for k in range(6, 15):
        labels = fcluster(Z, t=k, criterion="maxclust")
        if len(set(labels)) < 2: continue
        m = _all_metrics(X, labels)
        scores.append({"k": k, "sil": m["sil"], "db": m["db"], "ch": m["ch"]})

    if not scores: return None
    df = pd.DataFrame(scores)
    
    df["sil_n"] = (df["sil"] - df["sil"].min()) / (df["sil"].max() - df["sil"].min() + 1e-9)
    df["db_n"]  = (df["db"].max() - df["db"]) / (df["db"].max() - df["db"].min() + 1e-9)
    df["ch_n"]  = (df["ch"] - df["ch"].min()) / (df["ch"].max() - df["ch"].min() + 1e-9)
    
    df["score"] = (df["sil_n"] + df["db_n"] + df["ch_n"]) / 3.0
    
    # TOLERANCE-BASED SELECTION: pick largest k within 0.05 of the peak; im picking .4
    max_score = df["score"].max()
    tolerance = 0.15
    candidates = df[df["score"] >= (max_score - tolerance)]
    best_row = candidates.loc[candidates["k"].idxmax()]
    best_k = int(best_row["k"])

    print(f"\n[Hierarchical - {linkage_method}] {poster_name}")
    print(df.to_string(index=False, float_format="%.3f"))
    print(f"-> Selected k={best_k} (Tolerance-based choice)")

    labels = fcluster(Z, t=best_k, criterion="maxclust")
    
    total_dur = w.sum()
    for r in set(labels):
        pct = w[labels == r].sum() / total_dur
        if pct < 0.01: labels[labels == r] = -1

    valid_mask = labels >= 0
    poster_df = poster_df[valid_mask].copy()
    X = X[valid_mask]
    w = w[valid_mask]
    labels = labels[valid_mask]

    centers = []
    for r in sorted(set(labels)):
        mask = labels == r
        centers.append([np.average(X[mask, 0], weights=w[mask]), np.average(X[mask, 1], weights=w[mask])])

    out = poster_df.assign(region=labels)
    return {
        "method": f"hierarchical-{linkage_method}", "data": out,
        "centers": np.array(centers), "k": len(set(labels)), "linkage": linkage_method,
        "sil": best_row["sil"], "db": best_row["db"], "ch": best_row["ch"]
    }


def cluster_dbscan(poster_df, poster_name, eps, min_samples, img_w, img_h):
    poster_df = _filter_outliers_auto(poster_df, img_w, img_h)
    
    X = poster_df[["x", "y"]].to_numpy()
    w = poster_df["duration"].to_numpy()

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    labels = db.labels_
    
    labels_filled = labels.copy()
    mask = labels_filled == -1
    if mask.any() and (~mask).any():
        nn = NearestNeighbors(n_neighbors=1).fit(X[~mask])
        _, idx = nn.kneighbors(X[mask])
        labels_filled[mask] = labels_filled[~mask][idx.ravel()]

    total_dur = w.sum()
    for r in set(labels_filled):
        pct = w[labels_filled == r].sum() / total_dur
        if pct < 0.01: labels_filled[labels_filled == r] = -1

    valid_mask = labels_filled >= 0
    poster_df = poster_df[valid_mask].copy()
    X = X[valid_mask]
    w = w[valid_mask]
    labels_filled = labels_filled[valid_mask]

    k = len(set(labels_filled))
    if k < 2:
        print(f"  ! DBSCAN found {k} valid clusters. Try adjusting eps.")
        return None

    m = _all_metrics(X, labels_filled)
    centers = []
    for r in sorted(set(labels_filled)):
        mask = labels_filled == r
        centers.append([np.average(X[mask, 0], weights=w[mask]), np.average(X[mask, 1], weights=w[mask])])

    print(f"\n[DBSCAN] {poster_name} (eps={eps}, min_samples={min_samples})")
    print(f"   Filtered: {len(poster_df)} points remain")
    print(f"   Sil: {m['sil']:.3f} | DB: {m['db']:.3f} | CH: {m['ch']:.1f} | k={k}")

    out = poster_df.assign(region=labels_filled)
    return {
        "method": "dbscan", "data": out,
        "centers": np.array(centers), "k": k,
        "eps": eps, "min_samples": min_samples,
        "sil": m["sil"], "db": m["db"], "ch": m["ch"]
    }


def region_stats(clust):
    df = clust["data"].copy()
    n_ppl = df["participant"].nunique()
    total_dur = df["duration"].sum()

    pct = df.groupby("region")["duration"].sum().div(total_dur).mul(100).rename("pct_gaze").reset_index()
    first_fix = df.sort_values("rel_start").groupby("participant", as_index=False).first()
    first_pct = first_fix.groupby("region").size().div(n_ppl).mul(100).rename("pct_first_fix").reset_index()

    summary = pct.merge(first_pct, on="region", how="left").fillna(0).sort_values("pct_gaze", ascending=False).reset_index(drop=True)
    summary.insert(0, "rank", range(1, len(summary)+1))
    
    rank_map = summary[["region", "rank"]].rename(columns={"rank": "region_num"})
    
    return {"table": summary, "pct": pct, "rank_map": rank_map, "n_ppl": n_ppl}