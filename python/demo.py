from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial import ConvexHull

from clustering import cluster_hierarchical_auto, cluster_dbscan, region_stats

BASE_DIR   = Path(r"E:\Eye-Tracker\Renamed Signals")
POSTER_DIR = Path(r"E:\Eye-Tracker\posters")
OUT_DIR    = Path(__file__).resolve().parent / "output_py"

SE_SKIP = 17
GZ_SKIP = 8
N_PARTICIPANTS = 48
MIN_FIXATION_MS = 100

PARAMS = {
    "Armin Hofman- 1955":  {"linkage": "complete", "eps": 30, "min_samples": 15},
    "Barry Ceck - 1988":   {"linkage": "complete", "eps": 35, "min_samples": 15},
    "bookcover":           {"linkage": "complete", "eps": 30, "min_samples": 10},
    "David Carson - 1990": {"linkage": "complete", "eps": 30, "min_samples": 10},
    "David Carson":        {"linkage": "average",  "eps": 30, "min_samples": 12},
    "Ella Rosenblatt- 2021":    {"linkage": "average",  "eps": 30, "min_samples": 12},
    "Iris Chung- 2015":         {"linkage": "complete", "eps": 35, "min_samples": 10},
    "Jan Tschichold-1927-Die Frau ohne Namen":      {"linkage": "complete", "eps": 35, "min_samples": 10},
    "Jan Tschichold-1938-Der":  {"linkage": "complete", "eps": 35, "min_samples": 10},
    "Jan Tschichold-1938-Der":  {"linkage": "complete", "eps": 35, "min_samples": 10},
    "nancy":               {"linkage": "complete", "eps": 35, "min_samples": 10},
    "Paul Rand, 1947":     {"linkage": "complete", "eps": 30, "min_samples": 12},
    
    "Paula Scher - 1995":  {"linkage": "complete", "eps": 35, "min_samples": 15},
    "Scott Barry- 2010":               {"linkage": "complete", "eps": 35, "min_samples": 10},
    "Sean Alatorre":               {"linkage": "complete", "eps": 35, "min_samples": 10},
}

POSTERS_TO_RUN = list(PARAMS.keys())
OUT_DIR.mkdir(exist_ok=True)

HIGH_CONTRAST_COLORS = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", 
    "#a65628", "#f781bf", "#999999", "#1b9e77", "#d95f02"
]

def get_image_content_bounds(img_path):
    """
    Automatically detects the bounding box of the actual poster content,
    ignoring white, black, or solid-color borders.
    """
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img)
    
    # Sample the corners to find the border color
    patch = 10
    corners = [
        arr[:patch, :patch].reshape(-1, 3).mean(axis=0),
        arr[:patch, -patch:].reshape(-1, 3).mean(axis=0),
        arr[-patch:, :patch].reshape(-1, 3).mean(axis=0),
        arr[-patch:, -patch:].reshape(-1, 3).mean(axis=0)
    ]
    
    # Create a mask where pixels match ANY corner color
    border_mask = np.zeros(arr.shape[:2], dtype=bool)
    for c in corners:
        dist = np.linalg.norm(arr - c, axis=2)
        border_mask |= (dist < 40) # tolerance
        
    # Find the rows and columns that are not poster border
    content_rows = np.where(~border_mask.all(axis=1))[0]
    content_cols = np.where(~border_mask.all(axis=0))[0]
    
    if len(content_rows) == 0 or len(content_cols) == 0:
        return 0, 0, img.width, img.height
        
    y_min, y_max = content_rows[0], content_rows[-1]
    x_min, x_max = content_cols[0], content_cols[-1]
    
    return x_min, y_min, x_max, y_max


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

def draw_region_map(poster, clust, stats, img_path, ax, title_prefix="", mode="points"):
    img = Image.open(img_path).convert("RGB")
    img_w, img_h = img.size
    
    # Getting the actual poster bounds
    #This was to get rid of the fixation points outside the poster
    x_min, y_min, x_max, y_max = get_image_content_bounds(img_path)
    true_w = x_max - x_min
    true_h = y_max - y_min

    df = clust["data"].copy()

    rank_map = stats["rank_map"]
    pct_dict = dict(zip(stats["pct"]["region"], stats["pct"]["pct_gaze"]))
    r_num_dict = dict(zip(rank_map["region"], rank_map["region_num"]))

    ax.imshow(img)
    
    for r in sorted(df["region"].unique()):
        pts = df[df["region"] == r][["x", "y"]].to_numpy()
        if len(pts) < 3: continue
        
        num = r_num_dict.get(r, 99)
        pct = pct_dict.get(r, 0)
        color = HIGH_CONTRAST_COLORS[int(num) % len(HIGH_CONTRAST_COLORS)]

        if mode == "points":
            ax.scatter(pts[:, 0], pts[:, 1], s=10, color=color, alpha=0.85, edgecolors="black", linewidths=0.5, zorder=2, clip_on=True)
        elif mode == "hulls":
            try:
                hull = ConvexHull(pts)
                hp = pts[hull.vertices]
                hp = np.vstack([hp, hp[0]])
                ax.plot(hp[:, 0], hp[:, 1], color="white", linewidth=4, zorder=3, alpha=0.9, clip_on=True)
                ax.plot(hp[:, 0], hp[:, 1], color=color, linewidth=2, zorder=4, clip_on=True)
                ax.fill(hp[:, 0], hp[:, 1], color=color, alpha=0.2, zorder=1, clip_on=True)
            except Exception:
                pass

        cx, cy = pts[:, 0].mean(), pts[:, 1].mean()
        ax.scatter([cx], [cy], s=350, color="white", edgecolors="black", linewidths=2, zorder=5, clip_on=True)
        ax.scatter([cx], [cy], s=200, color=color, edgecolors="black", linewidths=1, zorder=6, clip_on=True)

        ax.annotate(f"R{int(num)}\n{pct:.0f}%", (cx, cy),
                    color="white", fontsize=11, fontweight="bold", ha="center", va="center",
                    xytext=(0, 30), textcoords="offset points",
                    bbox=dict(boxstyle="round,pad=0.4", fc="black", ec="white", alpha=0.9, linewidth=1.5), 
                    zorder=7, clip_on=True)

    ax.set_title(f"{title_prefix} (k={clust['k']})", fontsize=14, fontweight="bold")
    
    # FORCE THE AXES TO THE CROPPED BOUNDS
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_max, y_min)
    ax.axis("off")


# MAIN LOOP
for POSTER in POSTERS_TO_RUN:
    print(f"\n{'='*80}\nProcessing: {POSTER}\n{'='*80}")
    params = PARAMS[POSTER]
    img_path = find_poster_image(POSTER)
    if not img_path: continue

    img = Image.open(img_path)
    img_w, img_h = img.size
    
    fix_rows = []
    for i in range(1, N_PARTICIPANTS + 1):
        f = load_one(f"p{i}", POSTER)
        if f is not None: fix_rows.append(f)

    if not fix_rows: continue
        
    fix = pd.concat(fix_rows, ignore_index=True)
    fix = fix[fix["duration"] >= MIN_FIXATION_MS].reset_index(drop=True)

    # Scale to image pixel space
    sx, sy = img_w / 1920.0, img_h / 1200.0
    fix["x"] = fix["x"] * sx
    fix["y"] = fix["y"] * sy

    # 1. HIERARCHICAL
    clust_h = cluster_hierarchical_auto(fix, POSTER, params["linkage"], img_w, img_h)
    if clust_h:
        stats_h = region_stats(clust_h)
        stats_h["table"].to_csv(OUT_DIR / f"{POSTER}_hierarchical_stats.csv", index=False)

    # 2. DBSCAN
    clust_d = cluster_dbscan(fix, POSTER, params["eps"], params["min_samples"], img_w, img_h)
    if clust_d:
        stats_d = region_stats(clust_d)
        stats_d["table"].to_csv(OUT_DIR / f"{POSTER}_dbscan_stats.csv", index=False)

    # Comparing DBSCAN and heir
    if clust_h and clust_d:
        # With cluster points
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        draw_region_map(POSTER, clust_h, stats_h, img_path, axes[0], f"Hierarchical ({params['linkage']})", mode="points")
        draw_region_map(POSTER, clust_d, stats_d, img_path, axes[1], f"DBSCAN", mode="points")
        fig.suptitle(f"{POSTER} — Clusters (Points)", fontsize=16, fontweight="bold")
        fig.tight_layout()
        fig.savefig(OUT_DIR / f"{POSTER}_COMPARE_points.png", dpi=140)
        plt.close(fig)
