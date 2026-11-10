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

const state = {
  posters: [], poster: null, img: null, base: null, scale: 1, dpr: 1,
  method: "hierarchical", kMode: "auto", view: "clusters",
  history: [], current: null, nextId: 1, runToken: 0, quiet: false,
  heat: { key: null, canvas: null },
  replay: { pid: null, gaze: null, sampleRegion: null, now: 0, playing: false, last: null },
  gazeCache: new Map(),
};

/* ------------------------------------------------------------ helpers -- */

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (v, d) => (v == null ? "–" : Number(v).toFixed(d));
const px = (n) => n / state.scale;   // screen pixels -> image pixels
const pidNum = (pid) => parseInt(pid.slice(1), 10);

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
  if (!p || !state.img) return;
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
      <td>${fmt(r.pct_gaze, 1)}%</td><td>${fmt(r.pct_first_fix, 0)}%</td>
      <td>${r.n_fixations}</td><td>${r.n_participants}</td></tr>`).join("");
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
  sel.innerHTML = ordered.map((p) => `<option value="${p}">${p === rec ? `★ ${p} (closest to the group)` : p}</option>`).join("");
  if (pids.includes(prev)) sel.value = prev;

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
    drawHulls(res, false);
    drawLabels(res);
    drawReplay(res);
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
    state.heat.canvas = computeHeat(res, who, tmax, radius);
    state.heat.key = key;
  }
  if (!state.heat.canvas) return;
  const [x0, y0, x1, y1] = state.poster.bounds;
  ctx.save();
  ctx.globalAlpha = +$("#heat-opacity").value;
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = "high";
  ctx.drawImage(state.heat.canvas, x0, y0, x1 - x0 + 1, y1 - y0 + 1);
  ctx.restore();
}

function computeHeat(res, who, tmax, radiusPct) {
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
  const out = document.createElement("canvas");
  out.width = gw; out.height = gh;
  const g = out.getContext("2d");
  const img = g.createImageData(gw, gh);
  for (let i = 0; i < grid.length; i++) {
    // gamma < 1 so less-viewed areas stay visible next to the hottest spot
    const li = Math.min(255, Math.round(Math.pow(grid[i] / max, HEAT_GAMMA) * 255)) * 4;
    img.data[i * 4] = HEAT_LUT[li];
    img.data[i * 4 + 1] = HEAT_LUT[li + 1];
    img.data[i * 4 + 2] = HEAT_LUT[li + 2];
    img.data[i * 4 + 3] = HEAT_LUT[li + 3];
  }
  g.putImageData(img, 0, 0);
  return out;
}

/* ------------------------------------------------------------ replay --- */

async function prepareReplay() {
  const entry = state.current;
  const pid = $("#replay-pid").value;
  if (!entry || !pid) return;
  const ck = `${entry.poster}/${pid}`;
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

  const r = state.replay;
  if (r.pid !== ck) { r.now = r.startAt || 0; r.startAt = null; }
  r.pid = ck;
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
  $("#scrub").max = Math.round(g.duration);
  updateClock();
  draw();
}

function drawReplay(res) {
  const r = state.replay;
  if (!r.gaze || r.entry !== state.current) return;
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
  await selectPoster(sel.value);
}

init();
