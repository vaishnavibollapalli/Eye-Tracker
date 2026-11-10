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
import json
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


# ---------------------------------------------------------------- content ---
# test_website/poster_content.json says what is where on each poster (text,
# image, shape, background); see the notes at the top of that file.

CONTENT_FILE = HERE / "poster_content.json"
TYPES = ("text", "image", "shape", "background")
_content = {"mtime": None, "posters": {}}


def poster_elements(slug) -> list[dict]:
    """The poster's content elements with boxes in image pixels. The file is
    read again whenever it changes, so edits apply without a restart."""
    mtime = CONTENT_FILE.stat().st_mtime if CONTENT_FILE.exists() else None
    if mtime != _content["mtime"]:
        raw = {}
        if mtime is not None:
            with open(CONTENT_FILE, encoding="utf-8") as fh:
                raw = json.load(fh).get("posters", {})
        _content.update(mtime=mtime, posters=raw)
        RESULTS.clear()   # cached results carry the old descriptions
    x0, y0, x1, y1 = POSTERS[slug]["bounds"]
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    out = []
    for el in _content["posters"].get(slug, []):
        boxes = [(x0 + b[0] / 100 * bw, y0 + b[1] / 100 * bh,
                  x0 + b[2] / 100 * bw, y0 + b[3] / 100 * bh) for b in el.get("boxes", [])]
        kind = el.get("type") if el.get("type") in TYPES else "shape"
        out.append({"label": el.get("label", "?"), "type": kind, "boxes": boxes})
    return out


def assign_elements(elements, x, y) -> np.ndarray:
    """Index of the element under each point (-1 = none). Where boxes
    overlap, the smallest box wins, so text printed on a shape counts as text."""
    best = np.full(len(x), -1)
    best_area = np.full(len(x), np.inf)
    for i, el in enumerate(elements):
        for bx0, by0, bx1, by1 in el["boxes"]:
            area = (bx1 - bx0) * (by1 - by0)
            inside = (x >= bx0) & (x <= bx1) & (y >= by0) & (y <= by1) & (area < best_area)
            best[inside] = i
            best_area[inside] = area
    return best


def describe_content(elements, element, dur) -> dict:
    """What a region contains: the content elements its fixation time falls
    on, largest share first."""
    total = dur.sum()
    if total <= 0:
        return {"label": "Unknown", "type": "background", "share": 0, "parts": []}
    shares = {}
    for e, d in zip(element.tolist(), dur.tolist()):
        shares[e] = shares.get(e, 0.0) + d
    parts = []
    for e, d in sorted(shares.items(), key=lambda kv: -kv[1])[:3]:
        if e < 0:
            parts.append({"label": "Empty area / background", "type": "background", "share": num(d / total, 3)})
        else:
            parts.append({"label": elements[e]["label"], "type": elements[e]["type"], "share": num(d / total, 3)})
    return {**parts[0], "parts": parts}


def type_share(elements, element, dur) -> dict:
    """Share of fixation time on each content type."""
    kinds = np.array([elements[e]["type"] if e >= 0 else "background" for e in element.tolist()])
    total = dur.sum()
    return {t: num(dur[kinds == t].sum() / total, 4) if total else 0 for t in TYPES}


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


class NoClusters(Exception):
    pass


def parse_params(body) -> dict:
    """Validated, normalised clustering settings (also the cache key)."""
    slug = body.get("poster")
    get_poster(slug)
    method = body.get("method")
    if method == "hierarchical":
        linkage = body.get("linkage")
        if linkage not in LINKAGES:
            abort(400, f"linkage must be one of {LINKAGES}")
        p = {"poster": slug, "method": method, "linkage": linkage}
        if body.get("k_mode") == "fixed":
            p.update(k_mode="fixed", k=arg(body, "k", int, 2, 30))
        else:
            k_min = arg(body, "k_min", int, 2, 30)
            p.update(k_mode="auto", k_min=k_min, k_max=arg(body, "k_max", int, k_min, 30),
                     tolerance=arg(body, "tolerance", float, 0, 1))
        return p
    if method == "dbscan":
        return {"poster": slug, "method": method, "eps": arg(body, "eps", float, 1, 500),
                "min_samples": arg(body, "min_samples", int, 1, 500)}
    abort(400, "method must be hierarchical or dbscan")


def default_params(slug, method) -> dict:
    d = POSTERS[slug]["defaults"]
    if method == "dbscan":
        return {"poster": slug, "method": "dbscan", "eps": d["eps"], "min_samples": d["min_samples"]}
    return {"poster": slug, "method": "hierarchical", "linkage": d["linkage"],
            "k_mode": "auto", "k_min": 6, "k_max": 14, "tolerance": 0.15}


RESULTS: dict[str, dict] = {}   # cache: settings -> result


def compute(params: dict) -> dict:
    """Cluster one poster and describe the result. Raises NoClusters."""
    key = json.dumps(params, sort_keys=True)
    if key in RESULTS:
        return RESULTS[key]

    slug = params["poster"]
    poster = POSTERS[slug]
    fix, w, h = poster["fix"], poster["width"], poster["height"]
    with contextlib.redirect_stdout(io.StringIO()):   # clustering.py prints its working
        if params["method"] == "hierarchical":
            fixed = params["k_mode"] == "fixed"
            clust = cluster_hierarchical_auto(
                fix, poster["stim"], params["linkage"], w, h,
                k=params["k"] if fixed else None,
                k_min=6 if fixed else params["k_min"], k_max=14 if fixed else params["k_max"],
                tolerance=0.15 if fixed else params["tolerance"])
            label = (f"Hierarchical ({params['linkage']}), "
                     + (f"k={params['k']}" if fixed else
                        f"auto k {params['k_min']}-{params['k_max']}, tol {params['tolerance']:g}"))
        else:
            clust = cluster_dbscan(fix, poster["stim"], params["eps"], params["min_samples"], w, h)
            label = f"DBSCAN, eps={params['eps']:g}, min_samples={params['min_samples']}"
    if clust is None:
        raise NoClusters("This setting found fewer than 2 clusters. "
                         "For DBSCAN, try a larger eps or a smaller min_samples.")

    stats = region_stats(clust)
    data = clust["data"]
    num_of = dict(zip(stats["rank_map"]["region"], stats["rank_map"]["region_num"]))
    table = stats["table"].set_index("region")
    elements = poster_elements(slug)
    element = assign_elements(elements, data["x"].to_numpy(), data["y"].to_numpy())
    dur = data["duration"].to_numpy(dtype=float)

    # the group's viewing order, as in output/eye_tracking_analysis.R: regions
    # sorted by the mean time of each person's first fixation there
    entry = data.groupby(["participant", "region"])["rel_start"].min()
    avg_entry = entry.groupby(level="region").mean()
    coverage = entry.groupby(level="region").size() / stats["n_ppl"] * 100

    regions = []
    for region, n in sorted(num_of.items(), key=lambda kv: kv[1]):
        mask = (data["region"] == region).to_numpy()
        rows = data[mask]
        pts = rows[["x", "y"]].to_numpy()
        hull = mca.hull_points(pts)
        regions.append({
            "num": int(n),
            "color": mca.COLORS[int(n) % len(mca.COLORS)],
            "pct_gaze": num(table.loc[region, "pct_gaze"], 2),
            "pct_first_fix": num(table.loc[region, "pct_first_fix"], 2),
            "n_fixations": int(len(rows)),
            "n_participants": int(rows["participant"].nunique()),
            "avg_entry_ms": num(avg_entry[region], 0),
            "coverage": num(coverage[region], 1),
            "center": column(pts.mean(axis=0)),
            "hull": [column(p) for p in hull] if hull is not None else [],
            "content": describe_content(elements, element[mask], dur[mask]),
        })
    group_order = [int(num_of[r]) for r in avg_entry.sort_values().index]

    region_num = data["region"].map(num_of).astype(int)
    recommended = mca.pick_participant({"m": (clust, stats)}, poster["gaze"])

    scores = None
    if "scores" in clust:
        scores = [{"k": int(r.k), "sil": num(r.sil), "db": num(r.db), "ch": num(r.ch, 1),
                   "score": num(r.score)} for r in clust["scores"].itertuples()]

    result = {
        "label": label,
        "method": params["method"],
        "k": int(clust["k"]),
        "selected_k": int(clust.get("selected_k", clust["k"])),
        "metrics": {"sil": num(clust["sil"]), "db": num(clust["db"]), "ch": num(clust["ch"], 1)},
        "n_points": int(len(data)),
        "n_input": int(len(fix)),
        "scores": scores,
        "regions": regions,
        "group_order": group_order,
        "recommended": recommended,
        "elements": [{"label": e["label"], "type": e["type"]} for e in elements],
        "type_share": type_share(elements, element, dur),
        "fixations": {
            "pid": data["participant"].tolist(),
            "x": column(data["x"]), "y": column(data["y"]),
            "dur": column(data["duration"], 0),
            "t_start": column(data["t_start"]), "t_end": column(data["t_end"]),
            "region": region_num.tolist(),
            "element": element.tolist(),
        },
    }
    RESULTS[key] = result
    return result


@app.post("/api/cluster")
def cluster():
    params = parse_params(request.get_json(force=True) or {})
    try:
        return jsonify(compute(params))
    except NoClusters as e:
        return jsonify({"error": str(e)}), 422


@app.post("/api/compare")
def compare():
    """One summary per poster: the default clustering, or the settings the
    page sends for posters where a run was picked."""
    body = request.get_json(force=True) or {}
    method = body.get("method", "hierarchical")
    if method not in ("hierarchical", "dbscan"):
        abort(400, "method must be hierarchical or dbscan")
    overrides = body.get("overrides") or {}

    out = []
    for slug, poster in POSTERS.items():
        default = default_params(slug, method)
        params = default
        if slug in overrides:
            try:
                params = parse_params({**overrides[slug], "poster": slug})
            except HTTPException:
                pass   # a bad override falls back to the default
        row = {"id": slug, "name": poster["stim"], "picked": params != default}
        try:
            res = compute(params)
        except NoClusters as e:
            out.append({**row, "error": str(e)})
            continue
        by_num = {r["num"]: r for r in res["regions"]}
        first = max(res["regions"], key=lambda r: r["pct_first_fix"] or 0)
        out.append({
            **row,
            "label": res["label"], "k": res["k"],
            "most_viewed": slim_region(res["regions"][0]),
            "first_look": slim_region(first),
            "order": [slim_region(by_num[n]) for n in res["group_order"]],
            "type_share": res["type_share"],
        })
    return jsonify(out)


def slim_region(r):
    return {k: r[k] for k in ("num", "color", "pct_gaze", "pct_first_fix",
                              "avg_entry_ms", "coverage", "content")}


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
