#!/usr/bin/env node
// verify_row_graph_v2.js -- headless (DOM-less) sanity for the v2
// two-tier ROW agreement-graph explorer, the one scored under the owner's
// rulings A and B and laid out under ruling D.
//
// Same shape as verify_row_graph.js: domstub.js cannot carry this page
// (the explorer draws on a <canvas> and domstub's elements have no
// getContext), so this file supplies a canvas-shaped stub, RUNS the
// page's own script verbatim, and then checks the things the picture
// stands on.  What is new against the log-050 verifier:
//
//   *  RULING A is RE-IMPLEMENTED HERE, independently, straight from
//      the canon strings in matrices_interval/ and matrices_interval_c/:
//      the form classifier, the three element similarities and the
//      euclidean combine.  Every external connector's weight is
//      recomputed and must match the builder's to 1e-6.  Two
//      implementations, one answer.
//   *  RULING B is re-derived the same way: n_comparable,
//      n_excluded_declines and the rule that a pair with no comparable
//      position gets NO connector at all.
//   *  RULING D is checked twice -- the component count must be
//      IDENTICAL with the internal connectors drawn and undrawn
//      (components are external-only), and the internal springs'
//      total impulse in one physics step must be a small fraction of
//      the external springs' (internal connectors must not dominate the
//      layout).
//
// VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
// the OS-stopped outcome is ABORT.
//
// No external packages.

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const HERE = __dirname;
const HTML = path.join(HERE, "row_graph_explorer_v2.html");
const JSONP = path.join(HERE, "row_graph_v2.json");
const IV_DIRS = [path.join(HERE, "matrices_interval"),
                 path.join(HERE, "matrices_interval_c")];
const SEP = ";";
const TOL = 1e-6;

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
  if (rows.length && rows[rows.length - 1].length === 1 && rows[rows.length - 1][0] === "")
    rows.pop();
  const head = rows.shift();
  return rows.map(r => Object.fromEntries(head.map((h, k) => [h, r[k]])));
}

// ------------------------------------------------------------------
// RULING A + B, re-implemented from the spec, not from the python
// ------------------------------------------------------------------
const R3 = Math.sqrt(3);

function isDecline(c) {
  return c === "REFUSE" || c === "ABORT" || c.startsWith("RAISE:");
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
  if (parts.length !== 3) return null;          // [1, inf] / [-1, inf]
  const s = parseInt(parts[0], 10), m = parseFloat(parts[1]),
        e = parseInt(parts[2], 10);
  if (!isFinite(s) || !isFinite(m) || !isFinite(e)) return null;
  return [s, m, e];
}
function combine(ss, ms, es) {
  const d = Math.sqrt((1 - ss) ** 2 + (1 - ms) ** 2 + (1 - es) ** 2) / R3;
  return Math.max(0, Math.min(1, 1 - d));
}
function sampleSim(a, b) {
  const fa = formOf(a), fb = formOf(b);
  if (fa === "decline" || fb === "decline") return null;   // ruling B
  if (fa !== fb) return 0;                                 // ruling A
  if (fa === "numeric") {
    const pa = parseNumeric(a), pb = parseNumeric(b);
    if (!pa || !pb) return a === b ? 1 : 0;
    const ss = 1 - Math.abs(pa[0] - pb[0]) / 2;
    const ms = Math.max(0, 1 - Math.abs(pa[1] - pb[1]));
    const es = 1 / (1 + Math.abs(pa[2] - pb[2]));
    return combine(ss, ms, es);
  }
  if (fa === "text") {
    if (a === b) return 1;
    const A = a.split("|"), B = b.split("|");
    if (A.length !== 5 || B.length !== 5) return 0;
    if (A[1] === B[1]) return 1;
    const s = [2, 3, 4].map(k => 1 / (1 + Math.abs(+A[k] - +B[k])));
    return combine(s[0], s[1], s[2]);
  }
  return a === b ? 1 : 0;
}
function rowSim(va, vb) {
  let total = 0, cmp = 0, exc = 0, byte = 0;
  for (let i = 0; i < va.length; i++) {
    if (va[i] === vb[i]) byte++;
    const s = sampleSim(va[i], vb[i]);
    if (s === null) { exc++; continue; }
    cmp++; total += s;
  }
  if (cmp === 0) return null;
  return { n_comparable: cmp, n_excluded_declines: exc,
           weight: total / cmp, n_matched_byte: byte,
           weight_byte: byte / va.length };
}

// ------------------------------------------------------------------
function ctx2d() {
  const noop = () => {};
  return {
    clearRect: noop, beginPath: noop, moveTo: noop, lineTo: noop,
    stroke: noop, fill: noop, arc: noop, fillRect: noop, fillText: noop,
    save: noop, restore: noop, translate: noop, scale: noop,
    setLineDash: noop,
    measureText: () => ({ width: 10 }),
    set fillStyle(v) {}, get fillStyle() { return "#000"; },
    set strokeStyle(v) {}, get strokeStyle() { return "#000"; },
    set lineWidth(v) {}, get lineWidth() { return 1; },
    set globalAlpha(v) {}, get globalAlpha() { return 1; },
    set font(v) {}, get font() { return "13px sans-serif"; },
  };
}

// `children` / `appendChild` below are the DOM's own API names, which a
// stub has to spell exactly; they are not vocabulary.
function mk(id, tag) {
  return {
    id, tagName: tag || "div", _html: "", style: {}, dataset: {},
    children: [], value: "", checked: false, className: "",
    textContent: "", width: 1400, height: 900, offsetTop: 60,
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    appendChild(c) { this.children.push(c); return c; },
    addEventListener() {}, removeEventListener() {},
    getBoundingClientRect() { return { left: 0, top: 0, width: 1400, height: 900 }; },
    setAttribute() {}, getAttribute() { return null; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    getContext() { return ctx2d(); },
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
  };
}

function run() {
  const html = fs.readFileSync(HTML, "utf8");
  const json = JSON.parse(fs.readFileSync(JSONP, "utf8"));

  // ---------------------------------------------- run the real page
  const made = {};
  for (const id of new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)]
                             .map(m => m[1]))) made[id] = mk(id);
  made.cap.value = "10000";
  made.cmode.value = "lang";
  made.vmode.value = "all";
  made.showint.checked = true;
  made.thr.value = "85";

  const document = {
    getElementById: id => made[id] || (made[id] = mk(id)),
    createElement: t => mk("<" + t + ">", t),
    querySelector: () => null, querySelectorAll: () => [],
    addEventListener() {}, body: mk("body"), documentElement: mk("html"),
  };
  const timers = [];
  const sandbox = {
    document, console,
    addEventListener() {}, removeEventListener() {},
    requestAnimationFrame() { return 0; },       // never loop
    setInterval(f) { timers.push(f); return timers.length; },
    setTimeout() { return 0; },
    innerWidth: 1400, innerHeight: 900, devicePixelRatio: 1,
    Math, JSON, Set, Map, Array, Object, String, Number, Boolean,
  };
  sandbox.window = sandbox; sandbox.self = sandbox;
  sandbox.globalThis = sandbox;

  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
    .map(m => m[1]);
  if (scripts.length !== 1)
    throw new Error("expected exactly one inline script, got " + scripts.length);
  const ctx = vm.createContext(sandbox);
  vm.runInContext(scripts[0] +
    "\n;globalThis.__EXP={G:G,refresh:refresh,step:step,EXT:EXT,INT:INT," +
    "actInt:()=>actInt,act:()=>act};",
    ctx, { filename: "explorer.js" });
  console.log("  [script] the page's one inline script ran with no throw");

  const { G, refresh, step } = ctx.__EXP;

  // ------------------------------------------- 1  embed == JSON
  if (G.nodes.length !== json.nodes.length ||
      G.edges.length !== json.edges.length)
    throw new Error("embed and standalone JSON disagree on size");
  for (const k of ["n_row_nodes", "n_central_nodes", "n_internal_edges",
                   "n_external_edges", "comparable_universe",
                   "comparable_no_position_after_ruling_b",
                   "int_spring", "ext_spring", "render_cap"])
    if (G[k] !== json[k]) throw new Error("embed disagrees on " + k);
  console.log(`  [embed] ${G.nodes.length} nodes, ${G.edges.length} connectors, identical to ${path.basename(JSONP)}`);

  // ------------------------------------------- 2  counts by kind
  const rowN = json.nodes.filter(n => n.kind === "row");
  const cenN = json.nodes.filter(n => n.kind === "central");
  const intE = json.edges.filter(e => e.kind === "internal");
  const extE = json.edges.filter(e => e.kind === "external");
  if (rowN.length + cenN.length !== json.nodes.length)
    throw new Error("a node has a kind that is neither row nor central");
  if (intE.length + extE.length !== json.edges.length)
    throw new Error("a connector has a kind that is neither internal nor external");
  if (rowN.length !== json.n_row_nodes || cenN.length !== json.n_central_nodes ||
      intE.length !== json.n_internal_edges || extE.length !== json.n_external_edges)
    throw new Error("header counts disagree with the arrays");
  const vc = {};
  for (const n of rowN) vc[n.variant] = (vc[n.variant] || 0) + 1;
  for (const k of Object.keys(json.rows_by_variant))
    if (json.rows_by_variant[k] !== vc[k])
      throw new Error("rows_by_variant disagrees on " + k);
  console.log(`  [kinds] ${rowN.length} row nodes (${Object.entries(vc).sort().map(([k, v]) => k + " " + v).join(", ")}) + ${cenN.length} central nodes; ${intE.length} internal + ${extE.length} external connectors; header counts agree`);

  // ------------------------------------------- 3  endpoints
  const byId = new Map(json.nodes.map(n => [n.id, n]));
  for (const e of json.edges) {
    if (!byId.has(e.a) || !byId.has(e.b))
      throw new Error("connector endpoint is not a node: " + e.a + " ~ " + e.b);
    if (!(e.weight >= 0 && e.weight <= 1))
      throw new Error("weight outside [0,1] on " + e.a + " ~ " + e.b);
  }
  console.log("  [refs] every connector endpoint is a node, every weight in [0,1]");

  // ------------------------------------------- 4  internal rule (E)
  const seen = new Map();
  for (const e of intE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (a.kind !== "row") throw new Error("internal connector does not start at a row node: " + e.a);
    if (b.kind !== "central") throw new Error("internal connector does not end at a central node: " + e.b);
    if (a.central !== b.id) throw new Error("internal connector joins a row node to the wrong central node: " + e.a);
    if (seen.has(e.a)) throw new Error("row node has more than one internal connector: " + e.a);
    seen.set(e.a, e);
    if (e.no_comparison && e.weight !== 1)
      throw new Error("no_comparison connector is not 1.0 by convention: " + e.a);
    if (e.no_comparison !== (e.n_co_rows_comparable === 0))
      throw new Error("no_comparison does not equal n_co_rows_comparable==0 on " + e.a);
  }
  for (const n of rowN)
    if (!seen.has(n.id)) throw new Error("row node has no internal connector: " + n.id);
  console.log(`  [internal] exactly one internal connector per row node (${seen.size}), each to its OWN lang.op central node; no_comparison == (n_co_rows_comparable == 0) and always weight 1.0 (ruling E)`);

  // ------------------------------------------- 5  the raw rows
  const out = new Map();       // row node id -> output canon vector
  const inp = new Map();       // row node id -> lhs \u0000 rhs
  for (const d of IV_DIRS) {
    const idx = JSON.parse(fs.readFileSync(path.join(d, "index.json"), "utf8"));
    for (const key of Object.keys(idx.matrices)) {
      const op = key.slice(key.indexOf(".") + 1);
      for (const r of parseCsv(fs.readFileSync(path.join(d, idx.matrices[key].file), "utf8"))) {
        const id = `${key} / ${r.probe_id} / ${r.lhs_holder} ${op} ${r.rhs_holder} / ${r.interval_id}`;
        out.set(id, r.output_canon_vector.split(SEP));
        inp.set(id, r.lhs_canon_vector + "\u0000" + r.rhs_canon_vector);
      }
    }
  }
  for (const n of rowN)
    if (!out.has(n.id))
      throw new Error("a row node has no row in the interval matrices: " + n.id);
  console.log(`  [rows] all ${rowN.length} row nodes re-read from ${IV_DIRS.length} interval matrix directories`);

  // ------------------------------------------ 6  external rule A/B
  const byKey = new Map();
  for (const n of rowN) {
    if (!byKey.has(n.input_key)) byKey.set(n.input_key, []);
    byKey.get(n.input_key).push(n);
  }
  // input_key must partition exactly as the raw input vectors do
  const byRawInput = new Map();
  for (const n of rowN) {
    const k = inp.get(n.id);
    if (!byRawInput.has(k)) byRawInput.set(k, new Set());
    byRawInput.get(k).add(n.id);
  }
  if (byRawInput.size !== byKey.size)
    throw new Error(`input_key groups ${byKey.size} != raw input groups ${byRawInput.size}`);
  const pairSeen = new Map();
  let worstW = 0, worstB = 0;
  for (const e of extE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (a.kind !== "row" || b.kind !== "row")
      throw new Error("external connector touches a central node: " + e.a + " ~ " + e.b);
    if (a.central === b.central)
      throw new Error("external connector inside ONE operator (that is what internal connectors are for): " + e.a + " ~ " + e.b);
    if (a.input_key !== b.input_key || inp.get(e.a) !== inp.get(e.b))
      throw new Error("external connector across DIFFERENT input ladders: " + e.a + " ~ " + e.b);
    if (e.n_samples !== a.n_samples || e.n_samples !== b.n_samples)
      throw new Error("external connector n_samples disagrees with its row nodes");
    if (e.n_comparable <= 0)
      throw new Error("ruling B: a connector with no comparable position exists: " + e.a + " ~ " + e.b);
    if (e.n_comparable + e.n_excluded_declines !== e.n_samples)
      throw new Error("n_comparable + n_excluded_declines != n_samples on " + e.a + " ~ " + e.b);
    if (e.cross_language !== (a.language !== b.language))
      throw new Error("cross_language flag is wrong on " + e.a + " ~ " + e.b);
    const want = rowSim(out.get(e.a), out.get(e.b));
    if (!want) throw new Error("independent scorer says NO comparable position, yet a connector exists: " + e.a + " ~ " + e.b);
    if (want.n_comparable !== e.n_comparable || want.n_excluded_declines !== e.n_excluded_declines)
      throw new Error(`ruling B disagrees on ${e.a} ~ ${e.b}: page ${e.n_comparable}/${e.n_excluded_declines} vs independent ${want.n_comparable}/${want.n_excluded_declines}`);
    if (want.n_matched_byte !== e.n_matched_byte)
      throw new Error("secondary byte-identity count disagrees on " + e.a + " ~ " + e.b);
    worstW = Math.max(worstW, Math.abs(want.weight - e.weight));
    worstB = Math.max(worstB, Math.abs(want.weight_byte - e.weight_byte));
    const k = [e.a, e.b].sort().join(" ");
    if (pairSeen.has(k)) throw new Error("duplicate external connector: " + k);
    pairSeen.set(k, e);
  }
  if (worstW > TOL || worstB > TOL)
    throw new Error(`ruling-A weight disagrees by ${worstW} (byte ${worstB})`);
  console.log(`  [external A] all ${extE.length} weights recomputed from the canon strings by an INDEPENDENT ruling-A implementation; worst disagreement ${worstW.toExponential(2)} (byte-identity secondary ${worstB.toExponential(2)}), tolerance ${TOL}`);

  // completeness under ruling B: every cross-operator pair sharing a
  // digest must exist IF it has a comparable position, and must NOT
  // exist if it has none
  let want = 0, none = 0;
  for (const group of byKey.values())
    for (let i = 0; i < group.length; i++)
      for (let j = i + 1; j < group.length; j++) {
        if (group[i].central === group[j].central) continue;
        const k = [group[i].id, group[j].id].sort().join(" ");
        const s = rowSim(out.get(group[i].id), out.get(group[j].id));
        if (s === null) {
          none++;
          if (pairSeen.has(k))
            throw new Error("ruling B: a zero-comparable pair got a connector: " + k);
        } else {
          want++;
          if (!pairSeen.has(k))
            throw new Error("missing external connector for a comparable pair: " + k);
        }
      }
  if (want !== extE.length)
    throw new Error(`comparable cross-operator pairs ${want} != external connectors ${extE.length}`);
  if (none !== json.comparable_no_position_after_ruling_b)
    throw new Error(`zero-comparable pairs ${none} != header ${json.comparable_no_position_after_ruling_b}`);
  console.log(`  [external B] ${want} cross-operator pairs share an input ladder AND have a comparable position -- all present; ${none} share a ladder but have ZERO comparable positions -- none of them has a connector, as ruling B requires`);

  // ------------------------------------------- 7  live counters
  // ruling D: the page counts components on EXTERNAL connectors ONLY,
  // whether or not internal connectors are drawn -- reproduced here
  function independent(t, showInternal, capN, variant) {
    const vok = n => variant === "all" || n.kind === "central" || n.variant === variant;
    const idx = new Map(json.nodes.map((n, i) => [n.id, i]));
    const ext = json.edges.filter(e => e.kind === "external")
      .map((e, i) => ({ e, i }))
      .filter(o => o.e.weight >= t && vok(byId.get(o.e.a)) && vok(byId.get(o.e.b)))
      .sort((p, q) => (q.e.weight - p.e.weight) || (p.i - q.i))
      .slice(0, capN)
      .map(o => o.e);
    const inte = showInternal ? intE.filter(e => vok(byId.get(e.a))) : [];
    const p = json.nodes.map((_, i) => i);
    const f = x => { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; };
    for (const e of ext) {                     // EXTERNAL ONLY
      const a = f(idx.get(e.a)), b = f(idx.get(e.b));
      if (a != b) p[a] = b;
    }
    return { ext: ext.length, int: inte.length,
             comps: new Set(json.nodes.map((_, i) => f(i))).size };
  }
  const RE = /^(\d+) row nodes \| (\d+) central nodes \| (\d+) external \| (\d+) internal \| (\d+) components$/;
  let checks = 0;
  for (const showInternal of [true, false]) {
    for (const capN of [10000, 1000, 1000000]) {
      for (const t of [100, 95, 85, 70, 50, 0]) {
        for (const variant of ["all", "shift"]) {
          made.thr.value = String(t);
          made.showint.checked = showInternal;
          made.cap.value = String(capN);
          made.vmode.value = variant;
          refresh();
          const shown = made.stats.textContent;
          const m = shown.match(RE);
          if (!m) throw new Error("unreadable counter: " + shown);
          const w = independent(t / 100, showInternal, capN, variant);
          if (+m[1] !== rowN.length || +m[2] !== cenN.length)
            throw new Error("node counters wrong: " + shown);
          if (+m[3] !== w.ext || +m[4] !== w.int || +m[5] !== w.comps)
            throw new Error(`counter disagrees at t=${t / 100} internal=${showInternal} cap=${capN} variant=${variant}: page "${shown}" vs independent ext=${w.ext} int=${w.int} comps=${w.comps}`);
          checks++;
        }
      }
    }
  }
  console.log(`  [counters] ${checks} threshold x internal-toggle x draw-cap x variant settings: the page's live row/central/external/internal/component counts equal an independent union-find, every one`);

  // ------------------------------------- 8  ruling D, component rule
  made.vmode.value = "all"; made.cap.value = "10000";
  made.thr.value = "85"; made.showint.checked = true; refresh();
  const on = made.stats.textContent, onM = on.match(RE);
  made.showint.checked = false; refresh();
  const off = made.stats.textContent, offM = off.match(RE);
  if (on === off)
    throw new Error("the internal-connector toggle changes nothing -- it is not wired");
  if (onM[5] !== offM[5])
    throw new Error(`RULING D: the component count changed when internal connectors were toggled (${onM[5]} vs ${offM[5]}); components must be EXTERNAL-ONLY`);
  console.log(`  [ruling D components] t=0.85 with internal connectors: "${on}"; without: "${off}" -- the internal count moves, the COMPONENT count does not (external-only, as ruled)`);

  made.showint.checked = true;
  made.thr.value = "100"; refresh();
  const hi = made.stats.textContent;
  made.thr.value = "0"; refresh();
  const lo = made.stats.textContent;
  if (hi === lo)
    throw new Error("the threshold changes nothing -- the slider is not wired");
  const hiM = hi.match(RE), loM = lo.match(RE);
  if (+hiM[4] !== +loM[4])
    throw new Error("the threshold cut INTERNAL connectors -- it must cut external connectors only");
  console.log(`  [threshold cuts external only] t=1.00 -> ${hiM[3]} external, t=0.00 -> ${loM[3]} external, internal unchanged at ${hiM[4]} both times`);

  made.thr.value = "0"; made.cap.value = "1000"; refresh();
  if (!/DRAW CAP IN FORCE/.test(made.rule.textContent))
    throw new Error("the draw cap bites but the page does not say so");
  console.log(`  [draw cap stated] "${made.rule.textContent.split("DRAW CAP IN FORCE: ")[1]}"`);

  // ------------------------------------- 9  ruling D, spring strength
  if (!(json.int_spring < json.ext_spring / 5))
    throw new Error(`RULING D: the internal spring ${json.int_spring} is not near zero against the external ${json.ext_spring}`);
  made.thr.value = "85"; made.cap.value = "10000"; refresh();
  for (let i = 0; i < 200; i++) step();        // let the layout form
  const pos = new Map(G.nodes.map(n => [n.id, [n.x, n.y]]));
  // the two spring laws exactly as the page writes them, applied to the
  // page's own settled positions
  const actInt = ctx.__EXP.actInt(), act = ctx.__EXP.act();
  let ti = 0;
  for (const e of actInt) {
    const a = pos.get(e.a), b = pos.get(e.b);
    let d = Math.hypot(b[0] - a[0], b[1] - a[1]); if (d < 1) d = 1;
    ti += Math.abs(Math.min((d - 70) * json.int_spring, 6));
  }
  let te = 0;
  for (const e of act) {
    const a = pos.get(e.a), b = pos.get(e.b);
    let d = Math.hypot(b[0] - a[0], b[1] - a[1]); if (d < 1) d = 1;
    te += Math.abs(Math.min((d - 140) * json.ext_spring * e.weight, 6));
  }
  const share = ti / (ti + te);
  if (share > 0.25)
    throw new Error(`RULING D: internal springs contribute ${(100 * share).toFixed(1)}% of the total spring impulse -- they dominate the layout`);
  console.log(`  [ruling D springs] internal spring constant ${json.int_spring} against external ${json.ext_spring}; over ${actInt.length} internal and ${act.length} external connectors the internal springs carry ${(100 * share).toFixed(2)}% of the total spring impulse -- a tether, not the layout`);

  // ------------------------------------------- 10  physics
  if (timers.length === 0) throw new Error("no autofit interval registered");
  timers.forEach(f => f());
  console.log("  [autofit] the periodic fit ran with no throw");
  for (let i = 0; i < 600; i++) step();
  const bad = G.nodes.filter(n => !isFinite(n.x) || !isFinite(n.y) ||
                                  Math.hypot(n.x, n.y) > 2601);
  if (bad.length)
    throw new Error(bad.length + " nodes left the boundary -- the layout exploded");
  console.log("  [physics] after 800 steps every one of " + G.nodes.length +
    " nodes is finite and inside the hard boundary (grid repulsion, clamped linear springs, velocity clamp, gravity, boundary)");

  const before = G.nodes.map(n => [n.x, n.y]);
  for (let i = 0; i < 60; i++) step();
  let drift = 0, span = 0;
  G.nodes.forEach((n, i) => {
    drift = Math.max(drift, Math.hypot(n.x - before[i][0], n.y - before[i][1]));
    span = Math.max(span, Math.hypot(n.x, n.y));
  });
  if (drift > 5)
    throw new Error(`the layout has not settled: ${drift.toFixed(2)} px of drift over 60 further steps`);
  console.log(`  [settle] 60 further steps move the busiest node ${drift.toFixed(3)} px; the picture spans ${span.toFixed(0)} px from centre -- settled, not drifting`);

  // ------------------------------------------- 11  self-contained
  if (/<script\s+src/i.test(html)) throw new Error("external script tag present");
  if (html.includes("__GRAPH__")) throw new Error("placeholder not substituted");
  if (/https?:\/\//.test(html.replace(/https?:\/\/[^"']*w3\.org[^"']*/g, "")))
    throw new Error("an off-machine URL is present");
  console.log("  [self-contained] data embedded, placeholder gone, no external script, no CDN");

  console.log("HEADLESS VERIFY: all checks pass");
}

run();
