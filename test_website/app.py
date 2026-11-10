"""
Poster Cluster Explorer -- a small local website.

Pick a poster, cluster it with hierarchical clustering or DBSCAN, change the
parameters and compare the results, then look at the chosen clustering as a
heatmap and as a real-time replay of one participant's gaze.

Clustering is python/clustering.py, the same code demo.py and
make_cluster_animations.py use, so results here match theirs.

Usage (from the repository root):
    python test_website/app.py                  then open http://127.0.0.1:5000
    python test_website/app.py --rebuild-cache  re-read Renamed Signals/

The first start reads every participant's recordings (a minute or two) and
caches them in test_website/_cache/; later starts take seconds.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import math
import pickle
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from flask import Flask, abort, jsonify, request, send_file
from PIL import Image
from werkzeug.exceptions import HTTPException

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "python"))

import make_cluster_animations as mca  # noqa: E402  (poster list, data loading, drawing helpers)
from clustering import cluster_dbscan, cluster_hierarchical_auto, region_stats  # noqa: E402

CACHE_FILE = HERE / "_cache" / "poster_data.pkl"
CACHE_VERSION = 1
LINKAGES = ["complete", "average", "ward", "single"]

app = Flask(__name__, static_folder=str(HERE / "static"), static_url_path="/static")
POSTERS: dict[str, dict] = {}   # slug -> poster record (see build_data)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


# ---------------------------------------------------------------- data ------

def build_data() -> dict[str, dict]:
    """Every poster's fixations (image pixels) and every participant's raw
    gaze samples, read once from Renamed Signals/."""
    fixations = {stim: [] for stim in mca.PARAMS}
    gaze = {stim: {} for stim in mca.PARAMS}
    for i in range(1, mca.N_PARTICIPANTS + 1):
        pid = f"p{i}"
        print(f"  reading {pid} / p{mca.N_PARTICIPANTS}", end="\r", flush=True)
        for stim, (fix, samples) in mca.load_participant(pid, mca.PARAMS).items():
            fixations[stim].append(fix)
            gaze[stim][pid] = samples
    print()

    posters = {}
    for stim, params in mca.PARAMS.items():
        if not fixations[stim]:
            print(f"  ! no data for {stim}, left out")
            continue
        img_path = mca.POSTER_DIR / params["file"]
        img = Image.open(img_path).convert("RGB")
        w, h = img.size
        sx, sy = w / mca.SCREEN_W, h / mca.SCREEN_H

        fix = pd.concat(fixations[stim], ignore_index=True)
        fix = fix[fix["duration"] >= mca.MIN_FIXATION_MS].reset_index(drop=True)
        fix["x"] *= sx
        fix["y"] *= sy

        scaled = {}
        for pid, (t, x, y, duration) in gaze[stim].items():
            scaled[pid] = (t.astype(np.float64), (x * sx).astype(np.float32),
                           (y * sy).astype(np.float32), float(duration))

        posters[slugify(stim)] = {
            "stim": stim, "file": img_path.name, "width": w, "height": h,
            "bounds": [int(v) for v in mca.content_bounds(img)],
            "defaults": {k: params[k] for k in ("linkage", "eps", "min_samples")},
            "fix": fix, "gaze": scaled,
        }
    return posters


def load_data(rebuild: bool) -> dict[str, dict]:
    key = (CACHE_VERSION, tuple(mca.PARAMS))
    if CACHE_FILE.exists() and not rebuild:
        with open(CACHE_FILE, "rb") as fh:
            cached = pickle.load(fh)
        if cached.get("key") == key:
            return cached["posters"]
        print("Poster list changed, rebuilding cache.")
    print("Reading participant recordings (first run only)...")
    posters = build_data()
    CACHE_FILE.parent.mkdir(exist_ok=True)
    with open(CACHE_FILE, "wb") as fh:
        pickle.dump({"key": key, "posters": posters}, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return posters


# ---------------------------------------------------------------- helpers ---

def num(v, digits=4):
    """JSON-safe number: NaN/inf become null."""
    if v is None:
        return None
    v = float(v)
    return round(v, digits) if math.isfinite(v) else None


def column(a, digits=1):
    a = np.asarray(a, dtype=float)
    return [round(v, digits) if math.isfinite(v) else None for v in a.tolist()]


def get_poster(slug):
    poster = POSTERS.get(slug)
    if poster is None:
        abort(404, f"unknown poster {slug!r}")
    return poster


def arg(body, name, cast, lo, hi):
    try:
        value = cast(body[name])
    except (KeyError, TypeError, ValueError):
        abort(400, f"missing or invalid {name}")
    if not lo <= value <= hi:
        abort(400, f"{name} must be between {lo} and {hi}")
    return value


# ---------------------------------------------------------------- routes ----

@app.errorhandler(HTTPException)
def http_error(e):
    """Errors as JSON, so the page can show the message."""
    return jsonify({"error": e.description}), e.code


@app.errorhandler(Exception)
def server_error(e):
    app.logger.exception("request failed")
    return jsonify({"error": f"Server error: {type(e).__name__}: {e}"}), 500


@app.get("/")
def index():
    return send_file(HERE / "static" / "index.html")


@app.get("/api/posters")
def posters():
    return jsonify([{
        "id": slug, "name": p["stim"], "width": p["width"], "height": p["height"],
        "bounds": p["bounds"], "defaults": p["defaults"],
        "n_participants": len(p["gaze"]), "n_fixations": len(p["fix"]),
    } for slug, p in POSTERS.items()])


@app.get("/api/posters/<slug>/image")
def poster_image(slug):
    return send_file(mca.POSTER_DIR / get_poster(slug)["file"], max_age=3600)


@app.post("/api/cluster")
def cluster():
    body = request.get_json(force=True) or {}
    poster = get_poster(body.get("poster"))
    method = body.get("method")
    fix, w, h = poster["fix"], poster["width"], poster["height"]

    log = io.StringIO()   # clustering.py prints its working; keep the console readable
    with contextlib.redirect_stdout(log):
        if method == "hierarchical":
            linkage = body.get("linkage")
            if linkage not in LINKAGES:
                abort(400, f"linkage must be one of {LINKAGES}")
            if body.get("k_mode") == "fixed":
                k = arg(body, "k", int, 2, 30)
                k_min, k_max, tolerance = 6, 14, 0.15   # only for the reference score table
            else:
                k = None
                k_min = arg(body, "k_min", int, 2, 30)
                k_max = arg(body, "k_max", int, k_min, 30)
                tolerance = arg(body, "tolerance", float, 0, 1)
            clust = cluster_hierarchical_auto(fix, poster["stim"], linkage, w, h,
                                              k=k, k_min=k_min, k_max=k_max, tolerance=tolerance)
            label = (f"Hierarchical ({linkage}), "
                     + (f"k={k}" if k else f"auto k {k_min}-{k_max}, tol {tolerance:g}"))
        elif method == "dbscan":
            eps = arg(body, "eps", float, 1, 500)
            min_samples = arg(body, "min_samples", int, 1, 500)
            clust = cluster_dbscan(fix, poster["stim"], eps, min_samples, w, h)
            label = f"DBSCAN, eps={eps:g}, min_samples={min_samples}"
        else:
            abort(400, "method must be hierarchical or dbscan")

    if clust is None:
        return jsonify({"error": "This setting found fewer than 2 clusters. "
                                 "For DBSCAN, try a larger eps or a smaller min_samples."}), 422

    stats = region_stats(clust)
    data = clust["data"]
    num_of = dict(zip(stats["rank_map"]["region"], stats["rank_map"]["region_num"]))
    table = stats["table"].set_index("region")

    regions = []
    for region, n in sorted(num_of.items(), key=lambda kv: kv[1]):
        rows = data[data["region"] == region]
        pts = rows[["x", "y"]].to_numpy()
        hull = mca.hull_points(pts)
        regions.append({
            "num": int(n),
            "color": mca.COLORS[int(n) % len(mca.COLORS)],
            "pct_gaze": num(table.loc[region, "pct_gaze"], 2),
            "pct_first_fix": num(table.loc[region, "pct_first_fix"], 2),
            "n_fixations": int(len(rows)),
            "n_participants": int(rows["participant"].nunique()),
            "center": column(pts.mean(axis=0)),
            "hull": [column(p) for p in hull] if hull is not None else [],
        })

    region_num = data["region"].map(num_of).astype(int)
    recommended = mca.pick_participant({"m": (clust, stats)}, poster["gaze"])

    scores = None
    if "scores" in clust:
        scores = [{"k": int(r.k), "sil": num(r.sil), "db": num(r.db), "ch": num(r.ch, 1),
                   "score": num(r.score)} for r in clust["scores"].itertuples()]

    return jsonify({
        "label": label,
        "method": method,
        "k": int(clust["k"]),
        "selected_k": int(clust.get("selected_k", clust["k"])),
        "metrics": {"sil": num(clust["sil"]), "db": num(clust["db"]), "ch": num(clust["ch"], 1)},
        "n_points": int(len(data)),
        "n_input": int(len(fix)),
        "scores": scores,
        "regions": regions,
        "recommended": recommended,
        "fixations": {
            "pid": data["participant"].tolist(),
            "x": column(data["x"]), "y": column(data["y"]),
            "dur": column(data["duration"], 0),
            "t_start": column(data["t_start"]), "t_end": column(data["t_end"]),
            "region": region_num.tolist(),
        },
    })


@app.get("/api/gaze/<slug>/<pid>")
def gaze(slug, pid):
    poster = get_poster(slug)
    if pid not in poster["gaze"]:
        abort(404, f"no gaze for {pid}")
    t, x, y, duration = poster["gaze"][pid]
    return jsonify({"pid": pid, "duration": duration,
                    "t": column(t), "x": column(x), "y": column(y)})


@app.get("/api/participants/<slug>")
def participants(slug):
    poster = get_poster(slug)
    out = []
    for pid, (_, x, _, _) in poster["gaze"].items():
        out.append({"pid": pid, "valid": num(np.isfinite(x).mean(), 3)})
    out.sort(key=lambda r: int(r["pid"][1:]))
    return jsonify(out)


def main():
    ap = argparse.ArgumentParser(description="Poster Cluster Explorer")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--rebuild-cache", action="store_true",
                    help="re-read Renamed Signals/ instead of using the cache")
    args = ap.parse_args()

    POSTERS.update(load_data(args.rebuild_cache))
    print(f"{len(POSTERS)} posters ready.")
    print(f"Open http://127.0.0.1:{args.port} in your browser (Ctrl+C to stop).")
    app.run(host="127.0.0.1", port=args.port, debug=False)


if __name__ == "__main__":
    main()
