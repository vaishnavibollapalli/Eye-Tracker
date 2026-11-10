"use strict";
/* Poster Cluster Explorer -- front end. Everything is drawn in poster image
   pixels: draw() sets a transform from image pixels to the canvas. */

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const canvas = $("#canvas");
const ctx = canvas.getContext("2d");

const TRAIL_MS = 800;     // fading trail length, as in make_cluster_animations.py
const MAX_GAP_MS = 50;    // hide the dot when no valid sample for this long (blink / track loss)
const HEAT_GAMMA = 0.55;
const HEAT_STOPS = [      // position, rgb, alpha
  [0.00, [0, 0, 255], 0.00],
  [0.12, [0, 0, 255], 0.00],
  [0.22, [0, 60, 255], 0.35],
  [0.35, [0, 230, 255], 0.60],
  [0.55, [40, 230, 40], 0.75],
  [0.75, [255, 235, 0], 0.85],
  [1.00, [230, 20, 20], 0.95],
];

const AVG = "__avg";       // replay option: all participants
const TYPE_NAMES = { text: "Text", image: "Image", shape: "Shape", background: "Background" };
const TYPE_ORDER = ["text", "image", "shape", "background"];

const state = {
  posters: [], poster: null, img: null, base: null, scale: 1, dpr: 1,
  method: "hierarchical", kMode: "auto", view: "clusters",
  history: [], current: null, nextId: 1, runToken: 0, quiet: false,
  picked: {},              // poster id -> settings of the run last shown (used by the compare page)
  heat: { key: null, canvas: null },
  replay: { pid: null, gaze: null, sampleRegion: null, now: 0, playing: false, last: null },
  gazeCache: new Map(),
};

/* ------------------------------------------------------------ helpers -- */

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (v, d) => (v == null ? "–" : Number(v).toFixed(d));
const px = (n) => n / state.scale;   // screen pixels -> image pixels
const pidNum = (pid) => parseInt(pid.slice(1), 10);

const typeBadge = (t) => `<span class="type ${t}">${TYPE_NAMES[t] || t}</span>`;
const pct = (v) => `${Math.round(v * 100)}%`;
const secs = (ms) => `${(ms / 1000).toFixed(1)} s`;

/* "Text 'Title …'" plus, when the region is mixed, what else it covers */
function contentHTML(c, withAlso = true) {
  if (!c) return "–";
  let html = `${typeBadge(c.type)}${esc(c.label)}`;
  if (withAlso && c.share != null && c.share < 0.75) {
    const others = c.parts.slice(1).filter((p) => p.share >= 0.1)
      .map((p) => `${esc(p.label)} ${pct(p.share)}`);
    html += ` <span class="muted">${pct(c.share)}</span>`;
    if (others.length) html += `<span class="also">also: ${others.join(", ")}</span>`;
  }
  return html;
}
const rchip = (r, extra = "") => (r
  ? `<span class="rchip" style="background:${r.color}">R${r.num}${extra ? ` <small>${extra}</small>` : ""}</span>`
  : `<span class="rchip" style="background:#888">–</span>`);

function rgba(hex, a) {
  const n = parseInt(hex.slice(1), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
}

async function api(url, opts) {
  const r = await fetch(url, opts);
  let body = null;
  try { body = await r.json(); } catch { /* not JSON */ }
  if (!r.ok) throw new Error((body && body.error) || `Server error ${r.status} ${r.statusText}`);
  return body;
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error("Could not load the poster image"));
    img.src = src;
  });
}

function setStatus(text, error = false) {
  const el = $("#status");
  el.textContent = text;
  el.classList.toggle("error", error);
}
function showMsg(text) { const m = $("#stage-msg"); m.textContent = text; m.hidden = false; }
function hideMsg() { $("#stage-msg").hidden = true; }

function lowerBound(a, v) { let lo = 0, hi = a.length; while (lo < hi) { const m = (lo + hi) >> 1; if (a[m] < v) lo = m + 1; else hi = m; } return lo; }
function upperBound(a, v) { let lo = 0, hi = a.length; while (lo < hi) { const m = (lo + hi) >> 1; if (a[m] <= v) lo = m + 1; else hi = m; } return lo; }

function setSeg(id, attr, value) {
  $$(`#${id} button`).forEach((b) => b.classList.toggle("on", b.dataset[attr] === value));
}

function debounce(fn, ms) {
  let t;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}

/* ------------------------------------------------------------ controls - */

function updateOutputs() {
  $("#tolerance-out").textContent = Number($("#tolerance").value).toFixed(2);
  $("#k-out").textContent = $("#k").value;
  $("#eps-out").textContent = $("#eps").value;
  $("#min-samples-out").textContent = $("#min-samples").value;
  const ht = $("#heat-time");
  $("#heat-time-out").textContent = ht.value === ht.max ? "all" : `${ht.value} s`;
  $("#heat-radius-out").textContent = `${$("#heat-radius").value}%`;
  $("#heat-opacity-out").textContent = Number($("#heat-opacity").value).toFixed(2);
  $("#params-hierarchical").hidden = state.method !== "hierarchical";
  $("#params-dbscan").hidden = state.method !== "dbscan";
  $("#k-auto").hidden = state.kMode !== "auto";
  $("#k-fixed").hidden = state.kMode !== "fixed";
}

function readParams() {
  const p = { poster: state.poster.id, method: state.method };
  if (state.method === "hierarchical") {
    p.linkage = $("#linkage").value;
    p.k_mode = state.kMode;
    if (state.kMode === "fixed") p.k = +$("#k").value;
    else Object.assign(p, { k_min: +$("#k-min").value, k_max: +$("#k-max").value, tolerance: +$("#tolerance").value });
  } else {
    Object.assign(p, { eps: +$("#eps").value, min_samples: +$("#min-samples").value });
  }
  return p;
}

function loadParams(p) {
  state.quiet = true;
  state.method = p.method;
  setSeg("method", "method", p.method);
  if (p.method === "hierarchical") {
    $("#linkage").value = p.linkage;
    state.kMode = p.k_mode;
    setSeg("k-mode", "mode", p.k_mode);
    if (p.k_mode === "fixed") $("#k").value = p.k;
    else { $("#k-min").value = p.k_min; $("#k-max").value = p.k_max; $("#tolerance").value = p.tolerance; }
  } else {
    $("#eps").value = p.eps;
    $("#min-samples").value = p.min_samples;
  }
  updateOutputs();
  state.quiet = false;
}

function applyDefaults() {
  const d = state.poster.defaults;
  state.quiet = true;
  $("#linkage").value = d.linkage;
  $("#eps").value = d.eps;
  $("#min-samples").value = d.min_samples;
  $("#k-min").value = 6; $("#k-max").value = 14; $("#tolerance").value = 0.15; $("#k").value = 8;
  state.kMode = "auto"; setSeg("k-mode", "mode", "auto");
  updateOutputs();
  state.quiet = false;
}

const autoRun = debounce(() => runClustering(), 450);
function paramsChanged() {
  updateOutputs();
  if (!state.quiet && $("#auto-run").checked) autoRun();
}

/* ------------------------------------------------------------ posters -- */

async function selectPoster(id) {
  pause();
  state.poster = state.posters.find((p) => p.id === id);
  try { localStorage.setItem("pce-poster", id); } catch { /* storage unavailable */ }
  const p = state.poster;
  $("#poster-meta").textContent = `${p.n_participants} participants · ${p.n_fixations.toLocaleString()} fixations ≥ 100 ms`;
  state.current = null;
  state.base = null;
  $("#summary").hidden = true;
  showMsg("Loading poster…");
  try {
    state.img = await loadImage(`/api/posters/${encodeURIComponent(id)}/image`);
  } catch (e) { showMsg(e.message); return; }
  if (state.poster !== p) return;
  layout();
  applyDefaults();
  renderAll();
  const runs = state.history.filter((h) => h.poster === id);
  if (runs.length) selectEntry(runs[runs.length - 1]);
  else await runClustering();
}

function layout() {
  const p = state.poster;
  if (!p || !state.img || $("#explorer").hidden) return;
  const [x0, y0, x1, y1] = p.bounds;
  const bw = x1 - x0 + 1, bh = y1 - y0 + 1;
  const stage = $("#stage");
  const availW = stage.clientWidth - 2;
  const availH = Math.max(360, window.innerHeight - 150);
  const s = Math.min(availW / bw, availH / bh);
  const dpr = window.devicePixelRatio || 1;
  const w = Math.round(bw * s * dpr), h = Math.round(bh * s * dpr);
  canvas.width = w; canvas.height = h;
  canvas.style.width = `${Math.round(bw * s)}px`;
  canvas.style.height = `${Math.round(bh * s)}px`;
  state.scale = s; state.dpr = dpr;

  const base = document.createElement("canvas");
  base.width = w; base.height = h;
  const b = base.getContext("2d");
  b.imageSmoothingQuality = "high";
  b.drawImage(state.img, x0, y0, bw, bh, 0, 0, w, h);
  state.base = base;
  draw();
}

/* ------------------------------------------------------------ clustering */

async function runClustering() {
  if (!state.poster) return;
  const params = readParams();
  if (params.method === "hierarchical" && params.k_mode === "auto" && params.k_min > params.k_max) {
    setStatus("“Search k from” must not be larger than “to”.", true);
    return;
  }
  const key = JSON.stringify(params);
  const same = state.history.find((h) => h.key === key);
  if (same) { selectEntry(same); return; }

  const token = ++state.runToken;
  $("#run").disabled = true;
  setStatus("Clustering…");
  if (!state.current) showMsg("Clustering…");
  try {
    const result = await api("/api/cluster", { method: "POST", headers: { "Content-Type": "application/json" }, body: key });
    const entry = { id: state.nextId++, key, params, result, poster: params.poster };
    state.history.push(entry);
    if (token === state.runToken && state.poster.id === params.poster) selectEntry(entry);
    else renderHistory();
  } catch (e) {
    if (token === state.runToken) {
      setStatus(e.message, true);
      if (!state.current) showMsg(e.message);
    }
  } finally {
    if (token === state.runToken) $("#run").disabled = false;
  }
}

function selectEntry(entry) {
  state.current = entry;
  state.heat.key = null;
  const res = entry.result;
  res.byNum = Object.fromEntries(res.regions.map((r) => [r.num, r]));
  state.picked[entry.poster] = entry.params;
  loadParams(entry.params);
  setStatus(`Showing: ${res.label}`);
  hideMsg();
  renderAll();
  prepareReplay();
}

/* ------------------------------------------------------------ panels --- */

function renderAll() {
  renderSummary(); renderRegions(); renderScores(); renderHistory(); fillParticipants(); draw();
}

function renderSummary() {
  const el = $("#summary");
  const res = state.current && state.current.result;
  if (!res) { el.hidden = true; return; }
  const dropped = res.selected_k - res.k;
  const note = dropped > 0
    ? `<div class="hint" style="grid-column:1/-1">k=${res.selected_k} was chosen; ${dropped} region${dropped > 1 ? "s" : ""} with under 1% of gaze dropped.</div>` : "";
  el.innerHTML = `
    <div class="title">${esc(res.label)}</div>
    <div class="metric"><span>Regions</span><b>${res.k}</b></div>
    <div class="metric"><span>Fixations used</span><b>${res.n_points.toLocaleString()}</b> <span>of ${res.n_input.toLocaleString()}</span></div>
    <div class="metric"><span>Silhouette (higher better)</span><b>${fmt(res.metrics.sil, 3)}</b></div>
    <div class="metric"><span>Davies-Bouldin (lower better)</span><b>${fmt(res.metrics.db, 3)}</b></div>
    <div class="metric"><span>Calinski-Harabasz (higher better)</span><b>${fmt(res.metrics.ch, 0)}</b></div>
    ${note}`;
  el.hidden = false;
}

function renderRegions() {
  const res = state.current && state.current.result;
  $("#regions tbody").innerHTML = !res ? "" : res.regions.map((r) => `
    <tr><td><i class="swatch" style="background:${r.color}"></i>R${r.num}</td>
      <td class="content-cell">${contentHTML(r.content)}</td>
      <td>${fmt(r.pct_gaze, 1)}%</td><td>${fmt(r.pct_first_fix, 0)}%</td>
      <td>${r.n_participants}</td></tr>`).join("");
}

function renderScores() {
  const res = state.current && state.current.result;
  const card = $("#scores-card");
  if (!res || !res.scores) { card.hidden = true; return; }
  card.hidden = false;
  const auto = state.current.params.k_mode === "auto";
  $("#scores-card h3").textContent = auto ? "How auto chose k" : "Scores for other k (for reference)";
  $("#scores tbody").innerHTML = res.scores.map((s) => `
    <tr class="${auto && s.k === res.selected_k ? "chosen-k" : ""}"><td>${s.k}${auto && s.k === res.selected_k ? " ✓" : ""}</td>
      <td>${fmt(s.sil, 3)}</td><td>${fmt(s.db, 3)}</td><td>${fmt(s.ch, 0)}</td><td>${fmt(s.score, 3)}</td></tr>`).join("");
}

function renderHistory() {
  const rows = state.poster ? state.history.filter((h) => h.poster === state.poster.id) : [];
  $("#history-empty").hidden = rows.length > 0;
  const best = {};
  if (rows.length > 1) {
    const vals = (f) => rows.map((h) => h.result.metrics[f]).filter((v) => v != null);
    best.sil = Math.max(...vals("sil"));
    best.db = Math.min(...vals("db"));
    best.ch = Math.max(...vals("ch"));
  }
  const cell = (h, f, d) => {
    const v = h.result.metrics[f];
    return `<td class="${v != null && v === best[f] ? "best" : ""}">${fmt(v, d)}</td>`;
  };
  $("#history tbody").innerHTML = rows.map((h) => `
    <tr data-id="${h.id}" class="${h === state.current ? "current" : ""}">
      <td>${esc(h.result.label)}</td><td>${h.result.k}</td>
      ${cell(h, "sil", 3)}${cell(h, "db", 3)}${cell(h, "ch", 0)}
      <td><button class="del" data-del="${h.id}" title="Remove this run">✕</button></td></tr>`).join("");
}

function fillParticipants() {
  const res = state.current && state.current.result;
  const pids = res ? [...new Set(res.fixations.pid)].sort((a, b) => pidNum(a) - pidNum(b)) : [];

  const who = $("#heat-who"), prevWho = who.value;
  who.innerHTML = `<option value="all">All participants</option>` + pids.map((p) => `<option>${p}</option>`).join("");
  who.value = pids.includes(prevWho) ? prevWho : "all";

  const sel = $("#replay-pid"), prev = sel.value;
  const rec = res && res.recommended;
  const ordered = rec ? [rec, ...pids.filter((p) => p !== rec)] : pids;
  sel.innerHTML = (res ? `<option value="${AVG}">All participants (average)</option>` : "")
    + ordered.map((p) => `<option value="${p}">${p === rec ? `★ ${p} (closest to the group)` : p}</option>`).join("");
  const want = state.replay.wantPid;
  if (res && want && (want === AVG || pids.includes(want))) { sel.value = want; state.replay.wantPid = null; }
  else if (pids.includes(prev) || (prev === AVG && res)) sel.value = prev;
  else if (rec) sel.value = rec;

  if (res) {
    const ht = $("#heat-time");
    const wasAll = ht.value === ht.max;
    const maxT = Math.max(1, Math.ceil(Math.max(...res.fixations.t_end.filter((v) => v != null)) / 1000));
    ht.max = maxT;
    if (wasAll || +ht.value > maxT) ht.value = maxT;
    updateOutputs();
  }
}

/* ------------------------------------------------------------ drawing -- */

function draw() {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (!state.base) return;
  ctx.drawImage(state.base, 0, 0);
  const res = state.current && state.current.result;
  if (!res || state.current.poster !== state.poster.id) return;

  const [x0, y0] = state.poster.bounds;
  const k = state.scale * state.dpr;
  ctx.setTransform(k, 0, 0, k, -x0 * k, -y0 * k);

  if (state.view === "clusters") {
    if ($("#show-points").checked) drawPoints(res);
    if ($("#show-hulls").checked) drawHulls(res, true);
    if ($("#show-labels").checked) drawLabels(res);
  } else if (state.view === "heatmap") {
    drawHeat(res);
    if ($("#heat-hulls").checked) { drawHulls(res, false); drawLabels(res); }
  } else {
    const avg = state.replay.mode === "avg" && state.replay.entry === state.current;
    if (avg) drawAverageHeat(res);
    drawHulls(res, false);
    drawLabels(res);
    if (avg) drawOrderBadges(res);
    else drawReplay(res);
  }
}

function hullPath(r) {
  ctx.beginPath();
  r.hull.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
  ctx.closePath();
}

function drawHulls(res, fill) {
  ctx.lineJoin = "round";
  for (const r of res.regions) {
    if (r.hull.length < 3) continue;
    hullPath(r);
    if (fill) { ctx.fillStyle = rgba(r.color, 0.12); ctx.fill(); }
    ctx.strokeStyle = "rgba(255,255,255,0.85)"; ctx.lineWidth = px(4.5); ctx.stroke();
    ctx.strokeStyle = r.color; ctx.lineWidth = px(2.4); ctx.stroke();
  }
}

function drawLabels(res) {
  ctx.font = `bold ${px(11)}px system-ui, sans-serif`;
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  for (const r of res.regions) {
    const text = `R${r.num}  ${Math.round(r.pct_gaze)}%`;
    const w = ctx.measureText(text).width + px(12), h = px(18);
    const [cx, cy] = r.center;
    ctx.beginPath();
    ctx.roundRect(cx - w / 2, cy - h / 2, w, h, px(5));
    ctx.fillStyle = rgba(r.color, 0.9); ctx.fill();
    ctx.strokeStyle = "#fff"; ctx.lineWidth = px(1); ctx.stroke();
    ctx.fillStyle = "#fff";
    ctx.fillText(text, cx, cy + px(0.5));
  }
}

function drawPoints(res) {
  const f = res.fixations, rad = px(2.6);
  for (const r of res.regions) {
    ctx.beginPath();
    for (let i = 0; i < f.region.length; i++) {
      if (f.region[i] !== r.num) continue;
      ctx.moveTo(f.x[i] + rad, f.y[i]);
      ctx.arc(f.x[i], f.y[i], rad, 0, Math.PI * 2);
    }
    ctx.fillStyle = rgba(r.color, 0.85); ctx.fill();
    ctx.strokeStyle = "rgba(0,0,0,0.6)"; ctx.lineWidth = px(0.6); ctx.stroke();
  }
}

/* heatmap: duration-weighted Gaussian density on a coarse grid */

const HEAT_LUT = (() => {
  const lut = new Uint8ClampedArray(256 * 4);
  for (let i = 0; i < 256; i++) {
    const v = i / 255;
    let j = 1;
    while (j < HEAT_STOPS.length - 1 && HEAT_STOPS[j][0] < v) j++;
    const [p0, c0, a0] = HEAT_STOPS[j - 1], [p1, c1, a1] = HEAT_STOPS[j];
    const t = Math.min(1, Math.max(0, (v - p0) / (p1 - p0)));
    for (let c = 0; c < 3; c++) lut[i * 4 + c] = c0[c] + (c1[c] - c0[c]) * t;
    lut[i * 4 + 3] = 255 * (a0 + (a1 - a0) * t);
  }
  return lut;
})();
$("#heat-legend").style.background =
  `linear-gradient(90deg, ${HEAT_STOPS.map(([p, c, a]) => `rgba(${c},${Math.max(a, 0.15)}) ${p * 100}%`).join(",")})`;

function drawHeat(res) {
  const who = $("#heat-who").value;
  const ht = $("#heat-time");
  const tmax = ht.value === ht.max ? Infinity : +ht.value * 1000;
  const radius = +$("#heat-radius").value;
  const key = `${state.current.id}|${who}|${tmax}|${radius}`;
  if (state.heat.key !== key) {
    const heat = computeHeat(res, who, tmax, radius);
    state.heat.canvas = heat && heat.canvas;
    state.heat.key = key;
  }
  paintHeat(state.heat.canvas, +$("#heat-opacity").value);
}

function paintHeat(heatCanvas, opacity) {
  if (!heatCanvas) return;
  const [x0, y0, x1, y1] = state.poster.bounds;
  ctx.save();
  ctx.globalAlpha = opacity;
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
  ctx.drawImage(heatCanvas, x0, y0, x1 - x0 + 1, y1 - y0 + 1);
  ctx.restore();
}

/* Returns {canvas, max}. norm fixes the colour scale (e.g. to the full
   viewing time's maximum, so a build-up animation is comparable frame to frame). */
function computeHeat(res, who, tmax, radiusPct, norm) {
  const [x0, y0, x1, y1] = state.poster.bounds;
  const bw = x1 - x0 + 1, bh = y1 - y0 + 1;
  const gw = 260, cell = bw / gw, gh = Math.max(1, Math.round(bh / cell));
  const sigma = (radiusPct / 100) * bw / cell;
  const R = Math.ceil(sigma * 2.5);
  const kern = new Float32Array((2 * R + 1) ** 2);
  for (let dy = -R; dy <= R; dy++)
    for (let dx = -R; dx <= R; dx++)
      kern[(dy + R) * (2 * R + 1) + dx + R] = Math.exp(-(dx * dx + dy * dy) / (2 * sigma * sigma));

  const grid = new Float32Array(gw * gh);
  const f = res.fixations;
  let used = 0;
  for (let i = 0; i < f.x.length; i++) {
    if (who !== "all" && f.pid[i] !== who) continue;
    if (f.t_start[i] > tmax) continue;
    const cx = Math.round((f.x[i] - x0) / cell), cy = Math.round((f.y[i] - y0) / cell), w = f.dur[i];
    used++;
    for (let dy = -R; dy <= R; dy++) {
      const yy = cy + dy;
      if (yy < 0 || yy >= gh) continue;
      const row = yy * gw, krow = (dy + R) * (2 * R + 1) + R;
      for (let dx = -R; dx <= R; dx++) {
        const xx = cx + dx;
        if (xx >= 0 && xx < gw) grid[row + xx] += w * kern[krow + dx];
      }
    }
  }
  if (!used) return null;
  let max = 0;
  for (const v of grid) if (v > max) max = v;
  const scaleMax = norm || max;
  const out = document.createElement("canvas");
  out.width = gw; out.height = gh;
  const g = out.getContext("2d");
  const img = g.createImageData(gw, gh);
  for (let i = 0; i < grid.length; i++) {
    // gamma < 1 so less-viewed areas stay visible next to the hottest spot
    const li = Math.min(255, Math.round(Math.pow(Math.min(1, grid[i] / scaleMax), HEAT_GAMMA) * 255)) * 4;
    img.data[i * 4] = HEAT_LUT[li];
    img.data[i * 4 + 1] = HEAT_LUT[li + 1];
    img.data[i * 4 + 2] = HEAT_LUT[li + 2];
    img.data[i * 4 + 3] = HEAT_LUT[li + 3];
  }
  g.putImageData(img, 0, 0);
  return { canvas: out, max };
}

/* ------------------------------------------------------------ replay --- */

async function prepareReplay() {
  const entry = state.current;
  const pid = $("#replay-pid").value;
  if (!entry || !pid) return;
  const ck = `${entry.poster}/${pid}`;
  const r = state.replay;

  if (pid === AVG) {
    let end = 0;
    for (const v of entry.result.fixations.t_end) if (v != null && v > end) end = v;
    if (r.pid !== ck) { r.now = r.startAt || 0; r.startAt = null; }
    Object.assign(r, { pid: ck, mode: "avg", gaze: { duration: end }, entry,
                       visits: null, region: null, sampleRegion: null });
    finishReplaySetup();
    return;
  }

  let g = state.gazeCache.get(ck);
  if (!g) {
    try {
      const raw = await api(`/api/gaze/${encodeURIComponent(entry.poster)}/${pid}`);
      g = {
        pid, duration: raw.duration, t: Float64Array.from(raw.t, (v) => (v == null ? NaN : v)),
        x: Float64Array.from(raw.x, (v) => (v == null ? NaN : v)),
        y: Float64Array.from(raw.y, (v) => (v == null ? NaN : v)),
      };
      state.gazeCache.set(ck, g);
    } catch (e) { setStatus(`Could not load gaze for ${pid}: ${e.message}`, true); return; }
  }
  if (state.current !== entry || $("#replay-pid").value !== pid) return;

  if (r.pid !== ck) { r.now = r.startAt || 0; r.startAt = null; }
  r.pid = ck;
  r.mode = "pid";
  r.gaze = g;

  // the cluster being fixated at each gaze sample (0 = saccade / not clustered)
  const f = entry.result.fixations;
  const idx = [];
  for (let i = 0; i < f.pid.length; i++) if (f.pid[i] === pid) idx.push(i);
  idx.sort((a, b) => f.t_start[a] - f.t_start[b]);
  const starts = idx.map((i) => f.t_start[i]);
  const region = new Int16Array(g.t.length);
  for (let s = 0; s < g.t.length; s++) {
    const j = upperBound(starts, g.t[s]) - 1;
    if (j >= 0 && g.t[s] <= f.t_end[idx[j]]) region[s] = f.region[idx[j]];
  }
  r.sampleRegion = region;
  r.entry = entry;
  r.visits = personVisits(entry.result, pid);
  finishReplaySetup();
}

function finishReplaySetup() {
  const r = state.replay;
  r.activeVisit = null;
  $("#scrub").max = Math.round(r.gaze.duration);
  renderViewerSummary();
  updateClock();
  draw();
}

/* One participant's fixations in time order, with consecutive fixations in
   the same region merged into one visit. */
function personVisits(res, pid) {
  const f = res.fixations;
  const idx = [];
  for (let i = 0; i < f.pid.length; i++) if (f.pid[i] === pid) idx.push(i);
  idx.sort((a, b) => f.t_start[a] - f.t_start[b]);
  const visits = [];
  for (const i of idx) {
    const last = visits[visits.length - 1];
    if (last && last.num === f.region[i]) {
      last.t_end = f.t_end[i]; last.dur += f.dur[i]; last.n++;
    } else {
      visits.push({ num: f.region[i], t_start: f.t_start[i], t_end: f.t_end[i], dur: f.dur[i], n: 1 });
    }
  }
  return visits;
}

function renderViewerSummary() {
  const el = $("#viewer-summary");
  const r = state.replay, entry = state.current;
  if (!entry || r.entry !== entry) { el.innerHTML = ""; return; }
  const res = entry.result;

  if (r.mode === "avg") {
    $("#replay-hint").textContent = "The heatmap builds up as the group's fixations add up over time (like "
      + "average_gaze_animation.gif). Each region gets its number in the group's order once the group has, "
      + "on average, reached it.";
    const most = res.regions[0];
    const first = res.regions.reduce((a, b) => (b.pct_first_fix > a.pct_first_fix ? b : a));
    const people = new Set(res.fixations.pid).size;
    el.innerHTML = `
      <h3>All participants (${people} people)</h3>
      <div class="facts">
        <div class="fact"><span class="lbl">Looked at most</span>${rchip(most)} ${Math.round(most.pct_gaze)}% of all fixation time
          <span class="what">${contentHTML(most.content)}</span></div>
        <div class="fact"><span class="lbl">Most common first look</span>${rchip(first)} first for ${Math.round(first.pct_first_fix)}% of people
          <span class="what">${contentHTML(first.content)}</span></div>
      </div>
      <h4>Regions in the order the group reached them</h4>
      <p class="hint">Ordered by the average time of each person's first look at the region (the visit order used in
        eye_tracking_analysis.R).</p>
      <ol class="order-list" id="group-order">${res.group_order.map((n) => {
        const g = res.byNum[n];
        return `<li data-t="${g.avg_entry_ms}">${rchip(g)}<span>${contentHTML(g.content, false)}</span>
          <span class="meta">reached after ${secs(g.avg_entry_ms)} on average · by ${Math.round(g.coverage)}% of people
          · ${Math.round(g.pct_gaze)}% of fixation time</span></li>`;
      }).join("")}</ol>`;
    return;
  }

  $("#replay-hint").textContent = "The dot takes the colour of the cluster being fixated and turns white during "
    + "saccades. ★ marks the participant whose viewing best matches the group's for this clustering.";
  const pid = r.pid.split("/").pop();
  const v = r.visits || [];
  if (!v.length) {
    el.innerHTML = `<h3>${esc(pid)}</h3><p class="muted">None of ${esc(pid)}'s fixations fall in a region for this clustering.</p>`;
    return;
  }
  const time = {};
  let total = 0;
  for (const x of v) { time[x.num] = (time[x.num] || 0) + x.dur; total += x.dur; }
  const longest = +Object.entries(time).sort((a, b) => b[1] - a[1])[0][0];
  const firstAt = {};
  for (const x of v) if (!(x.num in firstAt)) firstAt[x.num] = x.t_start;
  const seen = Object.keys(firstAt).map(Number).sort((a, b) => firstAt[a] - firstAt[b]);
  const firstR = res.byNum[v[0].num], longR = res.byNum[longest];

  el.innerHTML = `
    <h3>${esc(pid)}</h3>
    <div class="facts">
      <div class="fact"><span class="lbl">Looked at first</span>${rchip(firstR)} at ${secs(v[0].t_start)}
        <span class="what">${contentHTML(firstR.content)}</span></div>
      <div class="fact"><span class="lbl">Looked at longest</span>${rchip(longR)} ${secs(time[longest])}
        (${pct(time[longest] / total)} of their time in regions)
        <span class="what">${contentHTML(longR.content)}</span></div>
    </div>
    <h4>Regions in the order ${esc(pid)} first looked at them · ${seen.length} of ${res.regions.length}</h4>
    <ol class="order-list">${seen.map((n) => {
      const g = res.byNum[n];
      return `<li>${rchip(g)}<span>${contentHTML(g.content, false)}</span>
        <span class="meta">first at ${secs(firstAt[n])} · ${secs(time[n])} in total</span></li>`;
    }).join("")}</ol>
    <h4>Full path · ${v.length} visits</h4>
    <div class="chips" id="visit-chips">${v.map((x, i) => `${i ? '<span class="arrow">→</span>' : ""}<span class="rchip"
      data-i="${i}" style="background:${res.byNum[x.num].color}" title="${secs(x.t_start)} – ${secs(x.t_end)}">R${x.num}
      <small>${(x.dur / 1000).toFixed(1)} s</small></span>`).join("")}</div>`;
}

/* the group's replay: fixation heatmap building up over time, on the colour
   scale of the full viewing time */
function drawAverageHeat(res) {
  const r = state.replay;
  const radius = +$("#heat-radius").value;
  const fullKey = `${state.current.id}|${radius}`;
  if (r.avgFullKey !== fullKey) {
    const full = computeHeat(res, "all", Infinity, radius);
    r.avgFullMax = full ? full.max : 1;
    r.avgFullKey = fullKey;
    r.avgKey = null;
  }
  const bucket = Math.floor(r.now / 100);
  const key = `${fullKey}|${bucket}`;
  if (r.avgKey !== key) {
    const heat = computeHeat(res, "all", (bucket + 1) * 100, radius, r.avgFullMax);
    r.avgCanvas = heat && heat.canvas;
    r.avgKey = key;
  }
  paintHeat(r.avgCanvas, 0.8);
}

function drawOrderBadges(res) {
  const r = state.replay;
  ctx.font = `bold ${px(12)}px system-ui, sans-serif`;
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  res.group_order.forEach((n, i) => {
    const g = res.byNum[n];
    if (g.avg_entry_ms > r.now) return;
    const [cx, cy] = g.center;
    const by = cy - px(22);
    ctx.beginPath();
    ctx.arc(cx, by, px(10), 0, Math.PI * 2);
    ctx.fillStyle = "#fff"; ctx.fill();
    ctx.strokeStyle = g.color; ctx.lineWidth = px(3); ctx.stroke();
    ctx.fillStyle = "#111";
    ctx.fillText(String(i + 1), cx, by + px(0.5));
  });
}

function drawReplay(res) {
  const r = state.replay;
  if (!r.gaze || r.entry !== state.current || r.mode !== "pid") return;
  const g = r.gaze, now = r.now;
  const lo = lowerBound(g.t, now - TRAIL_MS), hi = upperBound(g.t, now);

  let last = -1;
  for (let i = hi - 1; i >= lo; i--) if (Number.isFinite(g.x[i])) { last = i; break; }
  const visible = last >= 0 && now - g.t[last] <= MAX_GAP_MS;
  const region = visible ? res.byNum[r.sampleRegion[last]] : null;

  if (region && region.hull.length >= 3) {
    hullPath(region);
    ctx.fillStyle = rgba(region.color, 0.3);
    ctx.fill();
  }

  ctx.lineCap = "round";
  for (let i = Math.max(lo + 1, 1); i < hi; i++) {
    if (!Number.isFinite(g.x[i]) || !Number.isFinite(g.x[i - 1])) continue;   // a blink leaves a gap
    const age = (now - g.t[i]) / TRAIL_MS;
    const a = 0.15 + 0.85 * (1 - age), w = 1 + 2.2 * (1 - age);
    const reg = res.byNum[r.sampleRegion[i]];
    ctx.beginPath();
    ctx.moveTo(g.x[i - 1], g.y[i - 1]);
    ctx.lineTo(g.x[i], g.y[i]);
    ctx.strokeStyle = `rgba(0,0,0,${0.35 * a})`; ctx.lineWidth = px(w + 2.2); ctx.stroke();
    ctx.strokeStyle = reg ? rgba(reg.color, a) : `rgba(255,255,255,${a})`; ctx.lineWidth = px(w); ctx.stroke();
  }

  if (visible) {
    ctx.beginPath();
    ctx.arc(g.x[last], g.y[last], px(7.5), 0, Math.PI * 2);
    ctx.fillStyle = region ? region.color : "#ffffff"; ctx.fill();
    ctx.strokeStyle = "#000"; ctx.lineWidth = px(1.6); ctx.stroke();
  }
  r.region = region;
}

function updateClock() {
  const r = state.replay;
  if (!r.gaze) { $("#clock").textContent = "–"; return; }
  const where = r.region ? `  ·  in R${r.region.num}` : "";
  $("#clock").textContent = `${(r.now / 1000).toFixed(1)} s / ${(r.gaze.duration / 1000).toFixed(0)} s${where}`;
  $("#scrub").value = Math.round(r.now);

  // follow the replay in the summary
  if (r.mode === "avg") {
    $$("#group-order li").forEach((li) => li.classList.toggle("pending", +li.dataset.t > r.now));
  } else if (r.visits) {
    const i = r.visits.findIndex((v) => v.t_start <= r.now && r.now <= v.t_end);
    $$("#visit-chips .rchip").forEach((c) => {
      const k = +c.dataset.i;
      c.classList.toggle("on", k === i);
      c.classList.toggle("past", r.visits[k].t_end < r.now && k !== i);
    });
  }
}

function play() {
  const r = state.replay;
  if (!r.gaze) return;
  if (r.now >= r.gaze.duration) r.now = 0;
  r.playing = true; r.last = null;
  $("#play").textContent = "❚❚";
}
function pause() {
  state.replay.playing = false;
  $("#play").textContent = "▶";
}

function tick(ts) {
  const r = state.replay;
  if (r.playing && r.gaze) {
    if (r.last != null) r.now += (ts - r.last) * +$("#speed").value;
    r.last = ts;
    if (r.now >= r.gaze.duration) {
      if ($("#replay-loop").checked) r.now = 0;
      else { r.now = r.gaze.duration; pause(); }
    }
    if (state.view === "replay") { draw(); updateClock(); }
  }
  requestAnimationFrame(tick);
}

/* ------------------------------------------------------------ compare -- */

let compareToken = 0;

function showCompare(on) {
  state.page = on ? "compare" : "explore";
  $("#compare").hidden = !on;
  $("#explorer").hidden = on;
  $(".poster-pick").hidden = on;
  $("#poster-meta").hidden = on;
  $("#compare-toggle").textContent = on ? "← Back to explorer" : "Compare all posters";
  if (on) { pause(); loadCompare(); } else layout();
}

async function loadCompare() {
  const token = ++compareToken;
  const status = $("#cmp-status");
  status.classList.remove("error");
  status.textContent = "Clustering every poster… the first time takes about 15 seconds.";
  // only runs whose settings differ from demo.py's count as picks
  const isDefault = (p) => {
    const d = state.posters.find((x) => x.id === p.poster).defaults;
    return p.method === "dbscan"
      ? p.eps === d.eps && p.min_samples === d.min_samples
      : p.linkage === d.linkage && p.k_mode === "auto" && p.k_min === 6 && p.k_max === 14 && p.tolerance === 0.15;
  };
  const overrides = {};
  if ($("#cmp-picked").checked) {
    for (const [id, p] of Object.entries(state.picked)) if (!isDefault(p)) overrides[id] = p;
  }
  const body = { method: $("#cmp-method").value, overrides };
  try {
    const rows = await api("/api/compare", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    if (token !== compareToken) return;
    renderCompare(rows);
    const picked = rows.filter((r) => r.picked).map((r) => r.name);
    status.textContent = picked.length
      ? `Using the run you picked for ${picked.join(", ")}; the other posters use demo.py's settings.`
      : "All posters use demo.py's settings. Pick a different run for a poster in the explorer to use it here.";
  } catch (e) {
    if (token === compareToken) { status.textContent = e.message; status.classList.add("error"); }
  }
}

function renderCompare(rows) {
  const ok = rows.filter((r) => !r.error);

  $("#cmp-legend").innerHTML = TYPE_ORDER.map((t) => `<span><i style="background:var(--t-${t})"></i>${TYPE_NAMES[t]}</span>`).join("")
    + `<span>R1 is each poster's most-viewed region; region colours match the explorer.</span>`;

  $("#cmp-table tbody").innerHTML = rows.map((r) => {
    const name = `<a data-poster="${esc(r.id)}">${esc(r.name)}</a>`;
    if (r.error) return `<tr><td>${name}</td><td colspan="4" class="muted">${esc(r.error)}</td></tr>`;
    const mv = r.most_viewed, fl = r.first_look;
    const order = r.order.slice(0, 5).map((g, i) => `<div>${i + 1}. ${rchip(g)} ${typeBadge(g.content.type)}${esc(g.content.label)}
      <span class="muted">${secs(g.avg_entry_ms)}</span></div>`).join("")
      + (r.order.length > 5 ? `<div class="muted">+ ${r.order.length - 5} more</div>` : "");
    const share = r.type_share;
    const bar = TYPE_ORDER.map((t) => `<i style="width:${(share[t] || 0) * 100}%;background:var(--t-${t})"
      title="${TYPE_NAMES[t]} ${pct(share[t] || 0)}"></i>`).join("");
    const legend = TYPE_ORDER.filter((t) => share[t] >= 0.005).map((t) => `${TYPE_NAMES[t]} ${pct(share[t])}`).join(" · ");
    return `<tr>
      <td>${name}<small>${esc(r.label)}${r.picked ? " · your pick" : ""}</small></td>
      <td class="content-cell">${rchip(mv)} ${Math.round(mv.pct_gaze)}% of fixation time<br>${contentHTML(mv.content)}</td>
      <td class="content-cell">${rchip(fl)} first for ${Math.round(fl.pct_first_fix)}% of people<br>${contentHTML(fl.content)}</td>
      <td><div class="order">${order}</div></td>
      <td><div class="bar">${bar}</div><div class="bar-legend">${legend}</div></td></tr>`;
  }).join("");

  // plain-language summary across posters
  const el = $("#cmp-summary");
  if (!ok.length) { el.hidden = true; return; }
  const groupBy = (key) => {
    const m = {};
    for (const r of ok) (m[r[key].content.type] ||= []).push(r.name);
    return TYPE_ORDER.filter((t) => m[t]).sort((a, b) => m[b].length - m[a].length)
      .map((t) => `<b>${TYPE_NAMES[t].toLowerCase()}</b> on ${m[t].length} (${m[t].map(esc).join(", ")})`).join("; ");
  };
  const mean = (t) => ok.reduce((s, r) => s + (r.type_share[t] || 0), 0) / ok.length;
  const top = (t) => ok.reduce((a, b) => ((b.type_share[t] || 0) > (a.type_share[t] || 0) ? b : a));
  const extremes = ["text", "image", "shape"].filter((t) => (top(t).type_share[t] || 0) > 0.05)
    .map((t) => `${TYPE_NAMES[t].toLowerCase()}: <b>${esc(top(t).name)}</b> (${pct(top(t).type_share[t])})`).join("; ");
  const differ = ok.filter((r) => r.first_look.content.type !== r.most_viewed.content.type);
  el.innerHTML = `
    <h3>Across the ${ok.length} posters</h3>
    <ul>
      <li>The most-viewed region was ${groupBy("most_viewed")}.</li>
      <li>The region people looked at first was ${groupBy("first_look")}.</li>
      <li>On average, ${pct(mean("text"))} of fixation time was on text, ${pct(mean("image"))} on images,
        ${pct(mean("shape"))} on shapes and ${pct(mean("background"))} on empty areas or background.</li>
      <li>Largest share of fixation time on ${extremes}.</li>
      <li>On ${differ.length} poster${differ.length === 1 ? "" : "s"} the first look went to a different kind of content
        than the most-viewed region${differ.length ? ` (${differ.map((r) => `${esc(r.name)}: first ${TYPE_NAMES[r.first_look.content.type].toLowerCase()}, most ${TYPE_NAMES[r.most_viewed.content.type].toLowerCase()}`).join("; ")})` : ""}.</li>
    </ul>`;
  el.hidden = false;
}

/* ------------------------------------------------------------ wiring --- */

function bind() {
  $("#poster").addEventListener("change", (e) => selectPoster(e.target.value));

  $$("#method button").forEach((b) => b.addEventListener("click", () => {
    state.method = b.dataset.method; setSeg("method", "method", state.method); paramsChanged();
  }));
  $$("#k-mode button").forEach((b) => b.addEventListener("click", () => {
    state.kMode = b.dataset.mode; setSeg("k-mode", "mode", state.kMode); paramsChanged();
  }));
  ["#linkage", "#k-min", "#k-max", "#tolerance", "#k", "#eps", "#min-samples"].forEach((s) => {
    $(s).addEventListener("input", paramsChanged);
  });
  $("#run").addEventListener("click", runClustering);
  $("#reset").addEventListener("click", () => { applyDefaults(); paramsChanged(); });

  $("#history tbody").addEventListener("click", (e) => {
    const del = e.target.closest("[data-del]");
    if (del) {
      const id = +del.dataset.del;
      const wasCurrent = state.current && state.current.id === id;
      state.history = state.history.filter((h) => h.id !== id);
      if (wasCurrent) {
        const rest = state.history.filter((h) => h.poster === state.poster.id);
        if (rest.length) selectEntry(rest[rest.length - 1]);
        else { state.current = null; renderAll(); setStatus("Run a clustering to see results."); }
      } else renderHistory();
      return;
    }
    const row = e.target.closest("tr[data-id]");
    if (row) selectEntry(state.history.find((h) => h.id === +row.dataset.id));
  });

  $$("#view button").forEach((b) => b.addEventListener("click", () => {
    state.view = b.dataset.view;
    setSeg("view", "view", state.view);
    $$(".view-controls").forEach((el) => { el.hidden = el.dataset.for !== state.view; });
    if (state.view !== "replay") pause();
    draw(); updateClock();
  }));

  ["#show-points", "#show-hulls", "#show-labels", "#heat-hulls", "#heat-who"].forEach((s) => $(s).addEventListener("change", draw));
  ["#heat-time", "#heat-radius", "#heat-opacity"].forEach((s) => $(s).addEventListener("input", () => { updateOutputs(); draw(); }));

  $("#replay-pid").addEventListener("change", prepareReplay);
  $("#play").addEventListener("click", () => (state.replay.playing ? pause() : play()));
  $("#scrub").addEventListener("input", (e) => {
    state.replay.now = +e.target.value;
    draw(); updateClock();
  });
  document.addEventListener("keydown", (e) => {
    if (e.code === "Space" && state.view === "replay" && !/INPUT|SELECT|TEXTAREA|BUTTON/.test(e.target.tagName)) {
      e.preventDefault();
      state.replay.playing ? pause() : play();
    }
  });

  window.addEventListener("resize", debounce(layout, 150));

  $("#compare-toggle").addEventListener("click", () => showCompare(state.page !== "compare"));
  $("#cmp-method").addEventListener("change", loadCompare);
  $("#cmp-picked").addEventListener("change", loadCompare);
  $("#cmp-table tbody").addEventListener("click", (e) => {
    const a = e.target.closest("[data-poster]");
    if (!a) return;
    showCompare(false);
    $("#poster").value = a.dataset.poster;
    selectPoster(a.dataset.poster);
  });
}

async function init() {
  bind();
  updateOutputs();
  requestAnimationFrame(tick);
  try {
    state.posters = await api("/api/posters");
  } catch (e) {
    showMsg(`Could not reach the server (${e.message}). Start it with: python test_website/app.py`);
    return;
  }
  const sel = $("#poster");
  sel.innerHTML = state.posters.map((p) => `<option value="${esc(p.id)}">${esc(p.name)}</option>`).join("");
  let saved = null;
  try { saved = localStorage.getItem("pce-poster"); } catch { /* storage unavailable */ }
  // a link can open a poster / view directly: #poster=nancy_poster&view=replay&t=6
  const hash = new URLSearchParams(location.hash.slice(1));
  if (saved && state.posters.some((p) => p.id === saved)) sel.value = saved;
  if (state.posters.some((p) => p.id === hash.get("poster"))) sel.value = hash.get("poster");
  const view = $(`#view button[data-view="${hash.get("view")}"]`);
  if (view) view.click();
  if (hash.has("t")) state.replay.startAt = +hash.get("t") * 1000;
  if (hash.get("who")) state.replay.wantPid = hash.get("who") === "average" ? AVG : hash.get("who");
  if (hash.get("page") === "compare") showCompare(true);
  await selectPoster(sel.value);
}

init();
