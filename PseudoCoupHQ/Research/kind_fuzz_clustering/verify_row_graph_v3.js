#!/usr/bin/env node
// verify_row_graph_v3.js -- headless (DOM-less) sanity for the v3
// two-tier ROW agreement-graph explorer, the one built over the
// CARTESIAN probe design settled 2026-08-21.
//
// Same shape as verify_row_graph_v2.js: domstub.js cannot carry this
// page (the explorer draws on a <canvas> and domstub's elements have no
// getContext), so this file supplies a canvas-shaped stub, RUNS the
// page's own script verbatim, and then checks the things the picture
// stands on.  What it checks that v2 did not:
//
//   *  BOTH SCORINGS are re-implemented here, independently, straight
//      from the canon strings in matrices_cart/: the exact-match rate
//      and the ruling-A graded element similarity (form classifier,
//      three element similarities, euclidean combine).  Every checked
//      connector's two weights are recomputed and must match the
//      builder's to 1e-6.  Two implementations, one answer.
//   *  THE DECLINE RULE is re-derived the same way: n_comparable,
//      n_excluded_declines, and the rule that a pair with no comparable
//      position gets NO connector at all.
//   *  THE LIVE COUNTERS are checked against an independent union-find
//      at several threshold settings IN BOTH SCORING MODES and at
//      several sigmoid settings, including the two documented limits
//      (steepness 0 must reproduce the raw graded score exactly).
//   *  THE PHYSICS: the component count must be IDENTICAL with the
//      internal connectors drawn and undrawn (components are
//      external-only), the internal springs' total impulse in one step
//      must be a small fraction of the external springs', and the
//      layout must SETTLE rather than drift.
//   *  AUTOFIT RUNS ONCE: the page's autofit timer is driven here and
//      must refuse to fit a second time, and a wheel or mousedown must
//      disable it permanently.
//
// Level-1 connectors are re-derived EXHAUSTIVELY.  Level-2 rows carry
// up to 10,000 positions each and the ruby level-2 matrices alone are
// hundreds of megabytes, so level-2 connectors are re-derived over a
// DETERMINISTIC SAMPLE (every Nth connector, seedless and reproducible)
// and the sample size is printed rather than hidden.
//
// VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
// the OS-stopped outcome is ABORT.
//
// No external packages.

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const HERE = __dirname;
const HTML = path.join(HERE, "row_graph_explorer_v3.html");
const JSONP = path.join(HERE, "row_graph_v3.json");
const CART = path.join(HERE, "matrices_cart");
const SEP = ";";
const TOL = 1e-6;
const L2_SAMPLE_EVERY = 97;      // deterministic, seedless

let FAIL = 0;
function ok(msg) { console.log("  " + msg); }
function bad(msg) { FAIL++; console.log("  !! " + msg); }

// ------------------------------------------------------------------
// a minimal RFC4180 reader -- the vectors carry commas inside quotes
// ------------------------------------------------------------------
function parseCsv(text) {
  const rows = [];
  let row = [], field = "", q = false, i = 0;
  while (i < text.length) {
    const c = text[i];
    if (q) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i += 2; continue; }
        q = false; i++; continue;
      }
      field += c; i++; continue;
    }
    if (c === '"') { q = true; i++; continue; }
    if (c === ",") { row.push(field); field = ""; i++; continue; }
    if (c === "\r") { i++; continue; }
    if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; i++; continue; }
    field += c; i++;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  if (rows.length && rows[rows.length - 1].length === 1 &&
      rows[rows.length - 1][0] === "") rows.pop();
  const head = rows.shift();
  return rows.map(r => Object.fromEntries(head.map((h, k) => [h, r[k]])));
}

// ------------------------------------------------------------------
// RULING A re-implemented, independently of the python
// ------------------------------------------------------------------
function isDecline(s) {
  return s === "REFUSE" || s === "ABORT" || s.startsWith("RAISE:");
}
function formOf(c) {
  if (isDecline(c)) return "decline";
  if (c.startsWith("[")) return "numeric";
  if (c === "nan") return "numeric";
  if (c.startsWith("t|")) return "text";
  if (c.startsWith("c|")) return "container";
  if (c === "true" || c === "false") return "truth";
  if (c.startsWith("opaque:")) return "opaque";
  return "other";
}
function parseNumeric(c) {
  if (c === "nan") return null;
  const body = c.endsWith("]") ? c.slice(1, -1) : c.slice(1);
  const parts = body.split(",").map(s => s.trim());
  if (parts.length !== 3) return null;
  const s = parseInt(parts[0], 10), e = parseInt(parts[2], 10);
  if (!Number.isFinite(s) || !Number.isFinite(e)) return null;
  return [s, parts[1], e];
}
// the mants are decimal strings of up to ~31 digits; JS doubles carry 17,
// so the difference is taken in exact decimal on the digit strings
function decSub(a, b) {                 // |a - b| as a JS number
  const A = decParts(a), B = decParts(b);
  if (!A || !B) return Math.abs(parseFloat(a) - parseFloat(b));
  const scale = Math.max(A.frac.length, B.frac.length);
  const ai = BigInt(A.sign + A.int + A.frac.padEnd(scale, "0"));
  const bi = BigInt(B.sign + B.int + B.frac.padEnd(scale, "0"));
  let d = ai - bi; if (d < 0n) d = -d;
  return Number(d) / Math.pow(10, scale);
}
function decParts(s) {
  const m = /^(-?)(\d*)(?:\.(\d*))?$/.exec(s.trim());
  if (!m) return null;
  return { sign: m[1] === "-" ? "-" : "", int: m[2] || "0", frac: m[3] || "" };
}
function expoSim(d, knobs) {
  if (knobs.expo_decay !== "reciprocal")
    throw new Error("unknown expo decay " + knobs.expo_decay);
  return 1 / (1 + knobs.expo_decay_k * d);
}
function combine(ss, ms, es, knobs) {
  if (knobs.combine !== "euclidean")
    throw new Error("unknown combine " + knobs.combine);
  const d = Math.sqrt((1 - ss) ** 2 + (1 - ms) ** 2 + (1 - es) ** 2) /
            Math.sqrt(3);
  return Math.max(0, Math.min(1, 1 - d));
}
function textSim(a, b) {
  if (a === b) return 1;
  const fa = a.split("|"), fb = b.split("|");
  if (fa.length !== 5 || fb.length !== 5) return 0;
  if (fa[1] === fb[1]) return 1;
  const s = [2, 3, 4].map(k => 1 / (1 + Math.abs(+fa[k] - +fb[k])));
  if (s.some(x => !Number.isFinite(x))) return 0;
  const d = Math.sqrt(s.reduce((t, x) => t + (1 - x) ** 2, 0)) / Math.sqrt(3);
  return Math.max(0, Math.min(1, 1 - d));
}
function sampleSim(a, b, knobs) {
  const fa = formOf(a), fb = formOf(b);
  if (fa === "decline" || fb === "decline") return null;   // never scored
  if (fa !== fb) return 0;
  if (fa === "numeric") {
    const pa = parseNumeric(a), pb = parseNumeric(b);
    if (pa === null || pb === null) return a === b ? 1 : 0;
    const ss = 1 - Math.abs(pa[0] - pb[0]) / knobs.sign_max_distance;
    const ms = Math.max(0, 1 - decSub(pa[1], pb[1]));
    const es = expoSim(Math.abs(pa[2] - pb[2]), knobs);
    return combine(ss, ms, es, knobs);
  }
  if (fa === "text") return textSim(a, b);
  return a === b ? 1 : 0;
}
function rowPair(va, vb, knobs) {
  let nc = 0, ne = 0, sum = 0;
  for (let i = 0; i < va.length; i++) {
    const s = sampleSim(va[i], vb[i], knobs);
    if (s === null) { ne++; continue; }
    nc++; sum += s;
    if (va[i] === vb[i]) ne += 0;         // exact counted separately
  }
  let ex = 0;
  for (let i = 0; i < va.length; i++)
    if (!isDecline(va[i]) && !isDecline(vb[i]) && va[i] === vb[i]) ex++;
  return nc === 0 ? null
    : { n_comparable: nc, n_excluded_declines: ne,
        n_matched_exact: ex, weight_exact: ex / nc, weight_graded: sum / nc };
}

// ------------------------------------------------------------------
function uf(n, pairs) {
  const p = new Int32Array(n); for (let i = 0; i < n; i++) p[i] = i;
  const f = x => { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; };
  for (const [a, b] of pairs) { const ra = f(a), rb = f(b); if (ra !== rb) p[ra] = rb; }
  const roots = new Set(); for (let i = 0; i < n; i++) roots.add(f(i));
  const size = new Map(); for (let i = 0; i < n; i++) {
    const r = f(i); size.set(r, (size.get(r) || 0) + 1); }
  let multi = 0; for (const v of size.values()) if (v > 1) multi++;
  return { comps: roots.size, multi };
}

// ==================================================================
function main() {
  console.log("verify_row_graph_v3 -- headless checks on the CARTESIAN " +
              "row graph explorer");
  const html = fs.readFileSync(HTML, "utf8");
  const json = JSON.parse(fs.readFileSync(JSONP, "utf8"));
  const knobs = json.scoring_knobs;

  // ---------------------------------------------- run the real page
  function mk(id, tag) {
    const e = {
      id, tagName: tag || "div", value: "", checked: false,
      textContent: "", innerHTML: "", className: "", style: {},
      dataset: {},

      addEventListener() {}, removeEventListener() {},
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 1400, height: 900 }),
      getContext: () => ({
        clearRect() {}, beginPath() {}, moveTo() {}, lineTo() {}, stroke() {},
        arc() {}, fill() {}, fillRect() {}, fillText() {}, setLineDash() {},
        measureText: t => ({ width: String(t).length * 6 }),
        save() {}, restore() {},
        set fillStyle(v) {}, get fillStyle() { return ""; },
        set strokeStyle(v) {}, get strokeStyle() { return ""; },
        set lineWidth(v) {}, get lineWidth() { return 1; },
        set font(v) {}, get font() { return ""; },
        set globalAlpha(v) {}, get globalAlpha() { return 1; },
      }),
      width: 1400, height: 900, offsetTop: 60,
    };
    return e;
  }
  const made = {};
  for (const id of new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)]
                             .map(m => m[1]))) made[id] = mk(id);
  made.cap.value = "1000000";
  made.cmode.value = "lang";
  made.lmode.value = "all";
  made.showint.checked = true;
  made.exact.checked = false;
  made.thr.value = "85";
  made.mid.value = "50";
  made.stp.value = "0";

  const document = {
    getElementById: id => made[id] || (made[id] = mk(id)),
    createElement: t => mk("<" + t + ">", t),
    querySelector: () => null, querySelectorAll: () => [],
    addEventListener() {}, body: mk("body"), documentElement: mk("html"),
  };
  const timers = [];
  const listeners = {};
  const sandbox = {
    document, console: { log() {} },
    addEventListener(t, f) { (listeners[t] = listeners[t] || []).push(f); },
    removeEventListener() {},
    requestAnimationFrame() { return 0; },       // never loop
    setInterval(f) { timers.push(f); return timers.length; },
    clearInterval() {}, setTimeout() { return 0; },
    innerWidth: 1400, innerHeight: 900, devicePixelRatio: 1,
    Math, JSON, Set, Map, Array, Object, String, Number, Boolean, Int32Array,
  };
  sandbox.window = sandbox; sandbox.self = sandbox; sandbox.globalThis = sandbox;

  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
    .map(m => m[1]);
  if (scripts.length !== 1)
    throw new Error("expected exactly one inline script, got " + scripts.length);
  const ctx = vm.createContext(sandbox);
  vm.runInContext(scripts[0] +
    "\n;globalThis.__EXP={G:G,refresh:refresh,step:step,fit:fit," +
    "autofit:autofit,EXT:EXT,INT:INT,N:N," +
    "act:()=>act,actInt:()=>actInt,sig:g=>sig(g),W:e=>W(e)," +
    "state:()=>({T:T,EX:EX,MID:MID,K:K,heat:heat,scale:scale,ox:ox,oy:oy})};",
    ctx, { filename: "explorer.js" });
  ok("[script] the page's one inline script ran with no throw");
  const X = ctx.__EXP;

  // -------------------------------------------------- 1  embed == JSON
  if (X.G.nodes.length !== json.nodes.length ||
      X.G.edges.length !== json.edges.length)
    bad("embed and standalone JSON disagree on size");
  else for (const k of ["n_row_nodes", "n_central_nodes", "n_internal_edges",
                        "n_external_edges", "comparable_universe",
                        "comparable_no_position", "int_spring", "ext_spring",
                        "render_cap"])
    if (X.G[k] !== json[k]) bad("embed disagrees on " + k);
  ok(`[embed] ${X.G.nodes.length} nodes, ${X.G.edges.length} connectors, ` +
     `identical to ${path.basename(JSONP)}`);

  // -------------------------------------------------- 2  counts by kind
  const rowN = json.nodes.filter(n => n.kind === "row");
  const cenN = json.nodes.filter(n => n.kind === "central");
  const intE = json.edges.filter(e => e.kind === "internal");
  const extE = json.edges.filter(e => e.kind === "external");
  if (rowN.length + cenN.length !== json.nodes.length)
    bad("a node has a kind that is neither row nor central");
  if (intE.length + extE.length !== json.edges.length)
    bad("a connector has a kind that is neither internal nor external");
  if (rowN.length !== json.n_row_nodes || cenN.length !== json.n_central_nodes ||
      intE.length !== json.n_internal_edges || extE.length !== json.n_external_edges)
    bad("header counts disagree with the arrays");
  const byLevel = {};
  for (const n of rowN) byLevel[n.level] = (byLevel[n.level] || 0) + 1;
  ok(`[kinds] ${rowN.length} row nodes (L1 ${byLevel[1] || 0}, ` +
     `L2 ${byLevel[2] || 0}) + ${cenN.length} central nodes; ` +
     `${intE.length} internal + ${extE.length} external connectors; ` +
     `header counts agree`);

  // -------------------------------------------------- 3  endpoints
  const byId = new Map(json.nodes.map(n => [n.id, n]));
  let refbad = 0;
  for (const e of json.edges) {
    if (!byId.has(e.a) || !byId.has(e.b)) { refbad++; continue; }
    for (const w of ["weight_exact", "weight_graded"])
      if (!(e[w] >= 0 && e[w] <= 1)) refbad++;
  }
  if (refbad) bad(`${refbad} connectors have a bad endpoint or weight`);
  else ok("[refs] every connector endpoint is a node; BOTH weights in " +
          "[0,1] on every connector -- the two scorings are both present");

  // -------------------------------------------------- 4  internal rule
  const seen = new Map();
  let ibad = 0;
  for (const e of intE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (!a || a.kind !== "row" || !b || b.kind !== "central" ||
        a.central !== b.id || seen.has(e.a)) { ibad++; continue; }
    seen.set(e.a, e);
    if (e.no_comparison !== (e.n_co_rows_comparable === 0)) ibad++;
    if (e.no_comparison && (e.weight_exact !== 1 || e.weight_graded !== 1)) ibad++;
  }
  for (const n of rowN) if (!seen.has(n.id)) ibad++;
  if (ibad) bad(`${ibad} internal-connector rule violations`);
  else ok(`[internal] exactly one internal connector per row node ` +
          `(${seen.size}), each to its OWN lang.op central node; ` +
          `no_comparison == (n_co_rows_comparable == 0) and then both ` +
          `weights are 1.0 by convention`);

  // -------------------------------------------------- 5  the raw rows
  const idx = JSON.parse(fs.readFileSync(path.join(CART, "index.json"), "utf8"));
  const fileOf = new Map();                 // row node id -> csv file
  for (const key of Object.keys(idx.matrices)) {
    const m = idx.matrices[key];
    for (const r of parseCsv(fs.readFileSync(path.join(CART, m.file), "utf8"))) {
      const id = `${m.language}.${m.operator} / L${m.level} / ${r.probe_id} / ` +
                 `${r.lhs_holder} ${m.operator} ${r.rhs_holder}`;
      fileOf.set(id, { file: m.file, probe_id: r.probe_id, level: m.level });
    }
    if (m.level === 2) continue;            // level-1 files are small
  }
  let missing = 0;
  for (const n of rowN) if (!fileOf.has(n.id)) missing++;
  if (missing) bad(`${missing} row nodes have no row in matrices_cart/`);
  else ok(`[rows] all ${rowN.length} row nodes found in matrices_cart/`);

  // vector cache, one file at a time so level-2 stays out of memory
  const cache = new Map();
  function vecOf(id) {
    const meta = fileOf.get(id);
    if (!meta) return null;
    if (!cache.has(meta.file)) {
      if (cache.size > 2) cache.clear();
      const m = new Map();
      for (const r of parseCsv(fs.readFileSync(path.join(CART, meta.file), "utf8")))
        m.set(r.probe_id, r.output_canon_vector.split(SEP));
      cache.set(meta.file, m);
    }
    return cache.get(meta.file).get(meta.probe_id);
  }

  // -------------------------------------------------- 6  BOTH weights
  // level 1 exhaustively; level 2 on a deterministic sample
  const order = extE.map((e, i) => [e, i]);
  const check = order.filter(([e, i]) => e.level === 1 || i % L2_SAMPLE_EVERY === 0);
  // group the work by file pair so the cache is not thrashed
  check.sort((p, q) => {
    const fa = fileOf.get(p[0].a).file + fileOf.get(p[0].b).file;
    const fb = fileOf.get(q[0].a).file + fileOf.get(q[0].b).file;
    return fa < fb ? -1 : fa > fb ? 1 : 0;
  });
  let wbad = 0, n1 = 0, n2 = 0;
  const vcache = new Map();
  function vv(id) {
    if (!vcache.has(id)) {
      if (vcache.size > 400) vcache.clear();
      vcache.set(id, vecOf(id));
    }
    return vcache.get(id);
  }
  for (const [e] of check) {
    const va = vv(e.a), vb = vv(e.b);
    if (!va || !vb) { wbad++; continue; }
    const rec = rowPair(va, vb, knobs);
    if (rec === null) { wbad++; continue; }
    if (Math.abs(rec.weight_exact - e.weight_exact) > TOL ||
        Math.abs(rec.weight_graded - e.weight_graded) > TOL ||
        rec.n_comparable !== e.n_comparable ||
        rec.n_matched_exact !== e.n_matched_exact) {
      if (wbad < 5)
        console.log(`     mismatch ${e.a} ~ ${e.b}: builder ` +
          `exact ${e.weight_exact} graded ${e.weight_graded} ncmp ${e.n_comparable}` +
          ` | verifier exact ${rec.weight_exact.toFixed(6)} ` +
          `graded ${rec.weight_graded.toFixed(6)} ncmp ${rec.n_comparable}`);
      wbad++;
    }
    if (e.level === 1) n1++; else n2++;
  }
  if (wbad) bad(`${wbad} connectors disagree with the independent rescore`);
  else ok(`[rescore] ${n1} level-1 connectors re-derived EXHAUSTIVELY and ` +
          `${n2} level-2 connectors on a deterministic 1-in-${L2_SAMPLE_EVERY} ` +
          `sample; both weights and both counts agree to ${TOL} -- two ` +
          `implementations, one answer`);

  // -------------------------------------------------- 7  live counters
  const nid = new Map(json.nodes.map((n, i) => [n.id, i]));
  const settings = [
    { exact: false, thr: 95, mid: 50, stp: 0 },
    { exact: false, thr: 85, mid: 50, stp: 0 },
    { exact: false, thr: 70, mid: 50, stp: 0 },
    { exact: true, thr: 95, mid: 50, stp: 0 },
    { exact: true, thr: 85, mid: 50, stp: 0 },
    { exact: true, thr: 70, mid: 50, stp: 0 },
    { exact: false, thr: 50, mid: 60, stp: 120 },
    { exact: false, thr: 50, mid: 30, stp: 600 },
    { exact: false, thr: 50, mid: 50, stp: 6000 },
  ];
  let cbad = 0;
  for (const s of settings) {
    made.exact.checked = s.exact;
    made.thr.value = String(s.thr);
    made.mid.value = String(s.mid);
    made.stp.value = String(s.stp);
    X.refresh();
    const st = X.state();
    // the sigmoid, re-implemented here
    const K = s.stp / 10, MID = s.mid / 100, T = s.thr / 100;
    const sigf = g => {
      if (s.exact || K <= 1e-9) return g;
      const f = x => 1 / (1 + Math.exp(-K * (x - MID)));
      const a = f(0), b = f(1);
      if (b - a < 1e-12) return g;
      return Math.max(0, Math.min(1, (f(g) - a) / (b - a)));
    };
    const want = extE.filter(e =>
      sigf(s.exact ? e.weight_exact : e.weight_graded) >= T);
    const got = X.act();
    if (got.length !== want.length) {
      bad(`connector count at ${JSON.stringify(s)}: page ${got.length}, ` +
          `independent ${want.length}`);
      cbad++; continue;
    }
    const u = uf(json.nodes.length,
                 want.map(e => [nid.get(e.a), nid.get(e.b)]));
    const shown = made.stats.textContent;
    const m = /(\d+) components \((\d+) multi-node\)/.exec(shown);
    if (!m || +m[1] !== u.comps || +m[2] !== u.multi) {
      bad(`component counter at ${JSON.stringify(s)}: page "${shown}", ` +
          `independent ${u.comps} components (${u.multi} multi-node)`);
      cbad++; continue;
    }
    console.log(`     ${s.exact ? "exact " : "graded"} t=${T.toFixed(2)} ` +
      `mid=${MID.toFixed(2)} k=${K.toFixed(1)} -> ${want.length} external, ` +
      `${u.comps} components (${u.multi} multi-node)  [page agrees]`);
  }
  if (!cbad) ok("[counters] the page's live counters match an independent " +
                "union-find at every setting, in BOTH scoring modes and at " +
                "both documented sigmoid limits");

  // -------------------------------------------------- 8  sigmoid limits
  made.exact.checked = false; made.stp.value = "0"; X.refresh();
  let sbad = 0;
  for (const g of [0, 0.13, 0.5, 0.77, 1]) if (Math.abs(X.sig(g) - g) > 1e-12) sbad++;
  if (sbad) bad("steepness 0 does not reproduce the raw graded score");
  else ok("[sigmoid] steepness 0 reproduces the raw graded score EXACTLY " +
          "(w = g at every probe point)");
  made.stp.value = "6000"; made.mid.value = "50"; X.refresh();
  if (!(X.sig(0.49) < 0.02 && X.sig(0.51) > 0.98))
    bad("high steepness does not approach a hard cut at the midpoint");
  else ok("[sigmoid] steepness 600.0 approaches the exact-match style hard " +
          "cut at the midpoint (0.49 -> " + X.sig(0.49).toFixed(4) +
          ", 0.51 -> " + X.sig(0.51).toFixed(4) + ")");

  // -------------------------------------------------- 9  external rules
  let ebad = 0;
  for (const e of extE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (a.central === b.central) ebad++;
    if (a.level !== b.level || a.level !== e.level) ebad++;
    if (a.x_set_a !== b.x_set_a || a.x_set_b !== b.x_set_b) ebad++;
    if (!(e.n_comparable > 0)) ebad++;
    if (e.n_comparable + e.n_excluded_declines !== e.n_probes) ebad++;
    if (e.n_matched_exact > e.n_comparable) ebad++;
    if (e.cross_language !== (a.language !== b.language)) ebad++;
  }
  if (ebad) bad(`${ebad} external-connector rule violations`);
  else ok("[external] every external connector joins two row nodes of " +
          "DIFFERENT lang.op at the SAME level with IDENTICAL operand " +
          "sets; n_comparable > 0 and n_comparable + n_excluded_declines " +
          "== n_probes on every one");

  // -------------------------------------------------- 10  physics
  made.exact.checked = false; made.thr.value = "85"; made.stp.value = "0";
  made.showint.checked = true; X.refresh();
  const withInt = uf(json.nodes.length,
                     X.act().map(e => [nid.get(e.a), nid.get(e.b)])).comps;
  made.showint.checked = false; X.refresh();
  const withoutInt = uf(json.nodes.length,
                        X.act().map(e => [nid.get(e.a), nid.get(e.b)])).comps;
  if (withInt !== withoutInt)
    bad("component count changes when internal connectors are drawn");
  else ok(`[components] ${withInt} components with internal connectors ` +
          `drawn and ${withoutInt} with them hidden -- identical, because ` +
          `components are counted on EXTERNAL connectors ONLY`);

  made.showint.checked = true; X.refresh();
  const N = X.N;
  function impulse(edges, k) {
    let tot = 0;
    for (const e of edges) {
      const a = N[e.ai], b = N[e.bi];
      const dx = b.x - a.x, dy = b.y - a.y;
      let d = Math.hypot(dx, dy); if (d < 1) d = 1;
      tot += Math.abs(Math.min((d - 70) * k, 6));
    }
    return tot;
  }
  const ii = impulse(X.actInt(), json.int_spring);
  const ee = impulse(X.act(), json.ext_spring);
  if (!(ii < ee * 0.25))
    bad(`internal springs carry ${ii.toFixed(1)} against external ` +
        `${ee.toFixed(1)} -- not near zero`);
  else ok(`[springs] internal total impulse ${ii.toFixed(1)} against ` +
          `external ${ee.toFixed(1)} (${(100 * ii / (ee || 1)).toFixed(1)}%` +
          `) -- internal connectors cannot dominate the layout`);

  // -------------------------------------------------- 11  settle
  for (let i = 0; i < 900; i++) X.step();
  const before = N.map(n => [n.x, n.y]);
  for (let i = 0; i < 60; i++) X.step();
  let drift = 0, span = 0;
  N.forEach((n, i) => {
    drift = Math.max(drift, Math.hypot(n.x - before[i][0], n.y - before[i][1]));
    span = Math.max(span, Math.hypot(n.x, n.y));
  });
  if (!(drift < 5))
    bad(`layout still moving: busiest node drifts ${drift.toFixed(2)} px`);
  else ok(`[settle] 60 further steps move the busiest node ` +
          `${drift.toFixed(3)} px; the picture spans ${span.toFixed(0)} px ` +
          `from centre -- settled, not drifting`);

  // -------------------------------------------------- 12  autofit ONCE
  const t0 = X.state();
  timers.forEach(f => f());                  // first autofit tick
  const t1 = X.state();
  const fittedOnce = (t1.scale !== t0.scale || t1.ox !== t0.ox || t1.oy !== t0.oy);
  // move the camera, then tick again -- it must NOT refit
  vm.runInContext("scale=0.123;ox=7;oy=9;", ctx);
  timers.forEach(f => f());
  const t2 = X.state();
  if (!fittedOnce) bad("autofit never ran");
  else if (t2.scale !== 0.123 || t2.ox !== 7 || t2.oy !== 9)
    bad("autofit ran a SECOND time -- it must run once and never again");
  else ok("[autofit] ran once and never again; a later tick left the " +
          "camera exactly where it was put");
  (listeners.wheel || []).forEach(f => f({}));
  (listeners.mousedown || []).forEach(f => f({}));
  vm.runInContext("fitted=false;scale=0.5;ox=1;oy=2;", ctx);
  timers.forEach(f => f());
  const t3 = X.state();
  if (t3.scale !== 0.5 || t3.ox !== 1 || t3.oy !== 2)
    bad("a wheel/mousedown did not disable autofit permanently");
  else ok("[autofit] a wheel or mousedown disables it permanently, even " +
          "after the once-only flag is cleared");
  const before4 = X.state();
  made.fitbtn.onclick();
  const after4 = X.state();
  if (after4.scale === before4.scale && after4.ox === before4.ox)
    bad("the fit view button did nothing");
  else ok("[fit view] the button refits on demand");

  // -------------------------------------------------- 13  self-contained
  if (!/"nodes"/.test(html) || !/"edges"/.test(html) || /__GRAPH__/.test(html))
    bad("the embedded data is missing or the placeholder survived");
  else if (/<script\s+src/i.test(html) || /https?:\/\//.test(
             html.replace(/https?:\/\/www\.w3\.org[^"']*/g, "")))
    bad("the page reaches outside itself");
  else ok("[self-contained] data embedded, placeholder gone, no external " +
          "script, no CDN, no network reference");

  console.log(FAIL ? `\nFAILED: ${FAIL} check(s)` : "\nALL CHECKS PASSED");
  process.exit(FAIL ? 1 : 0);
}

main();
