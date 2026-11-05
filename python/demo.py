from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from clustering import cluster_hierarchical_auto, cluster_dbscan, region_stats

BASE_DIR   = Path(r"E:\Eye-Tracker\Renamed Signals")
POSTER_DIR = Path(r"E:\Eye-Tracker\posters")
OUT_DIR    = Path(__file__).resolve().parent / "output_py"

SE_SKIP = 17
GZ_SKIP = 8
N_PARTICIPANTS = 48
MIN_FIXATION_MS = 100

# ═══════════════════════════════════════════════════════════════════
#  EDIT YOUR PARAMETERS HERE
# ═══════════════════════════════════════════════════════════════════
PARAMS = {
    "Armin Hofman- 1955":  {"linkage": "complete",     "eps": 35, "min_samples": 15},
    "Barry Ceck - 1988":   {"linkage": "complete", "eps": 35, "min_samples": 15},
    "bookcover":           {"linkage": "ward",     "eps": 40, "min_samples": 10},
    "David Carson - 1990": {"linkage": "complete",     "eps": 45, "min_samples": 10},
    "David Carson":        {"linkage": "average",  "eps": 40, "min_samples": 12},
    "nancy":               {"linkage": "ward",     "eps": 45, "min_samples": 10},
    "Paul Rand, 1947":     {"linkage": "ward",     "eps": 40, "min_samples": 12},
    "Paula Scher - 1995":  {"linkage": "complete", "eps": 35, "min_samples": 15},
}
# ═══════════════════════════════════════════════════════════════════

POSTERS_TO_RUN = list(PARAMS.keys())
OUT_DIR.mkdir(exist_ok=True)

def load_one(pid, stim):
    p = BASE_DIR / pid
    se_path = p / "Native_SlideEvents.csv"
    gz_path = p / "ET_RExtAPI-GazeAnalysis.csv"
    if not (se_path.exists() and gz_path.exists()): return None
    
    se = pd.read_csv(se_path, skiprows=SE_SKIP, low_memory=False)
    se["Timestamp"] = pd.to_numeric(se["Timestamp"], errors="coerce")
    ev = se[se["SourceStimuliName"] == stim]
    if ev.empty: return None
    
    t0 = ev.loc[ev["SlideEvent"].isin(["StartMedia", "StartSlide"]), "Timestamp"]
    t1 = ev.loc[ev["SlideEvent"].isin(["EndMedia",   "EndSlide"]),   "Timestamp"]
    if t0.empty or t1.empty: return None
    t0, t1 = float(t0.iloc[0]), float(t1.iloc[0])

    gz = pd.read_csv(gz_path, skiprows=GZ_SKIP, low_memory=False, on_bad_lines="skip")
    fix_cols = ["Fixation Start", "Fixation End", "Fixation X", "Fixation Y", "Fixation Duration", "Fixation Index"]
    if not all(c in gz.columns for c in fix_cols): return None
    
    fix = gz[fix_cols].copy()
    for c in fix_cols: fix[c] = pd.to_numeric(fix[c], errors="coerce")
    fix = fix.dropna(subset=["Fixation Start", "Fixation Index"]).drop_duplicates("Fixation Index")
    if fix.empty: return None
    
    fw = fix[(fix["Fixation Start"] >= t0) & (fix["Fixation Start"] <= t1)].copy()
    if fw.empty: return None
    
    fw["participant"] = pid
    fw["x"]           = fw["Fixation X"]
    fw["y"]           = fw["Fixation Y"]
    fw["duration"]    = fw["Fixation Duration"]
    fw["rel_start"]   = fw["Fixation Start"] - fw["Fixation Start"].min()
    fw["rel_end"]     = fw["Fixation End"]   - fw["Fixation Start"].min()
    return fw[["participant", "x", "y", "duration", "rel_start", "rel_end"]]

def find_poster_image(poster_label):
    candidates = [poster_label, poster_label.replace(" ", "_"), poster_label.replace(" ", "")]
    for name in candidates:
        for ext in [".png", ".jpg", ".jpeg", ".PNG"]:
            p = POSTER_DIR / (name + ext)
            if p.exists(): return p
    return None

def draw_region_map(poster, clust, stats, img_path, ax, title_prefix=""):
    img = Image.open(img_path).convert("RGB")
    img_w, img_h = img.size
    sx, sy = img_w / 1920.0, img_h / 1200.0

    df = clust["data"].copy()
    df["ix"] = df["x"] * sx
    df["iy"] = df["y"] * sy

    rank_map = stats["rank_map"]
    pct_dict = dict(zip(stats["pct"]["region"], stats["pct"]["pct_gaze"]))
    r_num_dict = dict(zip(rank_map["region"], rank_map["region_num"]))

    ax.imshow(img, alpha=0.85)
    cmap = plt.get_cmap("Set1")

    for r in sorted(df["region"].unique()):
        pts = df[df["region"] == r][["ix", "iy"]].to_numpy()
        if len(pts) < 3: continue
        
        num = r_num_dict.get(r, 99)
        pct = pct_dict.get(r, 0)
        color = cmap(int(num) % 9)

        ax.scatter(pts[:, 0], pts[:, 1], s=5, color=color, alpha=0.4, edgecolors="none", zorder=2)
        cx, cy = pts[:, 0].mean(), pts[:, 1].mean()
        
        ax.scatter([cx], [cy], s=250, color="white", edgecolors="black", linewidths=2, zorder=5)
        ax.scatter([cx], [cy], s=140, color=color, edgecolors="black", linewidths=1, zorder=6)

        ax.annotate(f"R{int(num)}\n{pct:.0f}%", (cx, cy),
                    color="white", fontsize=10, fontweight="bold", ha="center", va="center",
                    xytext=(0, 25), textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.4", fc="black", ec="white", alpha=0.85, linewidth=1.5), zorder=7)

    ax.set_title(f"{title_prefix} (k={clust['k']})", fontsize=12, fontweight="bold")
    ax.axis("off")

# MAIN LOOP
for POSTER in POSTERS_TO_RUN:
    print(f"\n{'='*80}\nProcessing: {POSTER}\n{'='*80}")
    params = PARAMS[POSTER]
    img_path = find_poster_image(POSTER)
    if not img_path: continue

    fix_rows = []
    for i in range(1, N_PARTICIPANTS + 1):
        f = load_one(f"p{i}", POSTER)
        if f is not None: fix_rows.append(f)

    if not fix_rows: continue
    fix = pd.concat(fix_rows, ignore_index=True)
    fix = fix[fix["duration"] >= MIN_FIXATION_MS].reset_index(drop=True)

    # 1. HIERARCHICAL
    clust_h = cluster_hierarchical_auto(fix, POSTER, linkage_method=params["linkage"])
    if clust_h:
        stats_h = region_stats(clust_h)
        stats_h["table"].to_csv(OUT_DIR / f"{POSTER}_hierarchical_stats.csv", index=False)

    # 2. DBSCAN
    clust_d = cluster_dbscan(fix, POSTER, eps=params["eps"], min_samples=params["min_samples"])
    if clust_d:
        stats_d = region_stats(clust_d)
        stats_d["table"].to_csv(OUT_DIR / f"{POSTER}_dbscan_stats.csv", index=False)

    # 3. SIDE-BY-SIDE COMPARISON
    if clust_h and clust_d:
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        draw_region_map(POSTER, clust_h, stats_h, img_path, axes[0], f"Hierarchical ({params['linkage']})")
        draw_region_map(POSTER, clust_d, stats_d, img_path, axes[1], f"DBSCAN (eps={params['eps']}, min={params['min_samples']})")
        fig.suptitle(f"{POSTER} — Cluster Comparison", fontsize=16, fontweight="bold")
        fig.tight_layout()
        fig.savefig(OUT_DIR / f"{POSTER}_COMPARE.png", dpi=140, bbox_inches="tight")
        plt.close(fig)
        print(f"  Saved: {POSTER}_COMPARE.png")