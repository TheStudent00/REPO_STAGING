#!/usr/bin/env node
// verify_row_graph.js -- headless (DOM-less) sanity for the two-tier
// ROW agreement-graph explorer.
//
// Same shape as verify_graph_interval.js: domstub.js cannot carry this
// page (the explorer draws on a <canvas> and domstub's elements have no
// getContext), so this file supplies a canvas-shaped stub, RUNS the
// page's own script verbatim, and then checks the things the picture
// stands on:
//
//   1  JSON consistency, and the embed equals the standalone JSON;
//   2  every connector endpoint is a real node;
//   3  INTERNAL connectors: exactly one per row node, joining it to its
//      own lang.op central node -- never to anything else;
//   4  EXTERNAL connectors: only between row nodes of DIFFERENT
//      operators, only where the input ladder digests are identical,
//      and ALL such pairs are present (nothing missing, nothing
//      invented);
//   5  the page's live counters equal an INDEPENDENT union-find
//      computed here, at several thresholds, with the internal toggle
//      both on and off and at two draw caps -- two methods, one answer;
//   6  the page's one inline script runs clean under the canvas stub,
//      the autofit interval runs, and after a physics step every node
//      is finite and inside the hard boundary.
//
// VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
// the OS-stopped outcome is ABORT.
//
// No external packages.

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const HERE = __dirname;
const HTML = path.join(HERE, "row_graph_explorer.html");
const JSONP = path.join(HERE, "row_graph.json");

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
  // <select> defaults the page relies on
  made.cap.value = "10000";
  made.cmode.value = "lang";
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
  // `const G = ...` at a script's top level is lexical, so it never
  // lands on the context object; the page runs VERBATIM and hands its
  // own bindings out at the end.
  vm.runInContext(scripts[0] +
    "\n;globalThis.__EXP={G:G,refresh:refresh,step:step,EXT:EXT,INT:INT};",
    ctx, { filename: "explorer.js" });
  console.log("  [script] the page's one inline script ran with no throw");

  const { G, refresh, step } = ctx.__EXP;

  // ------------------------------------------- 1  embed == JSON
  if (G.nodes.length !== json.nodes.length ||
      G.edges.length !== json.edges.length)
    throw new Error("embed and standalone JSON disagree on size");
  for (const k of ["n_row_nodes", "n_central_nodes", "n_internal_edges",
                   "n_external_edges", "comparable_universe",
                   "render_cap"])
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
  console.log(`  [kinds] ${rowN.length} row nodes + ${cenN.length} central nodes; ${intE.length} internal + ${extE.length} external connectors; header counts agree`);

  // ------------------------------------------- 3  endpoints
  const byId = new Map(json.nodes.map(n => [n.id, n]));
  for (const e of json.edges) {
    if (!byId.has(e.a) || !byId.has(e.b))
      throw new Error("connector endpoint is not a node: " + e.a + " ~ " + e.b);
    if (!(e.weight >= 0 && e.weight <= 1))
      throw new Error("weight outside [0,1] on " + e.a + " ~ " + e.b);
  }
  console.log("  [refs] every connector endpoint is a node, every weight in [0,1]");

  // ------------------------------------------- 4  internal rule
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
    if (e.no_comparison !== (e.n_co_rows === 0))
      throw new Error("no_comparison does not equal n_co_rows==0 on " + e.a);
  }
  for (const n of rowN)
    if (!seen.has(n.id)) throw new Error("row node has no internal connector: " + n.id);
  console.log(`  [internal] exactly one internal connector per row node (${seen.size}), each to its OWN lang.op central node; no_comparison == (n_co_rows == 0) and always weight 1.0`);

  // ------------------------------------------- 5  external rule
  const byKey = new Map();
  for (const n of rowN) {
    if (!byKey.has(n.input_key)) byKey.set(n.input_key, []);
    byKey.get(n.input_key).push(n);
  }
  const pairSeen = new Set();
  for (const e of extE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (a.kind !== "row" || b.kind !== "row")
      throw new Error("external connector touches a central node: " + e.a + " ~ " + e.b);
    if (a.central === b.central)
      throw new Error("external connector inside ONE operator (that is what internal connectors are for): " + e.a + " ~ " + e.b);
    if (a.input_key !== b.input_key)
      throw new Error("external connector across DIFFERENT input ladders: " + e.a + " ~ " + e.b);
    if (e.n_samples !== a.n_samples || e.n_samples !== b.n_samples)
      throw new Error("external connector n_samples disagrees with its row nodes");
    if (Math.abs(e.weight - e.n_matched / e.n_samples) > 1e-6)
      throw new Error("weight is not n_matched / n_samples on " + e.a + " ~ " + e.b);
    if (e.cross_language !== (a.language !== b.language))
      throw new Error("cross_language flag is wrong on " + e.a + " ~ " + e.b);
    const k = [e.a, e.b].sort().join(" ");
    if (pairSeen.has(k)) throw new Error("duplicate external connector: " + k);
    pairSeen.add(k);
  }
  // completeness: every cross-operator pair sharing a digest must exist
  let want = 0;
  for (const group of byKey.values())
    for (let i = 0; i < group.length; i++)
      for (let j = i + 1; j < group.length; j++)
        if (group[i].central !== group[j].central) {
          want++;
          const k = [group[i].id, group[j].id].sort().join(" ");
          if (!pairSeen.has(k))
            throw new Error("missing external connector for a comparable pair: " + k);
        }
  if (want !== extE.length)
    throw new Error(`comparable cross-operator pairs ${want} != external connectors ${extE.length}`);
  console.log(`  [external] all ${extE.length} join row nodes of DIFFERENT operators with IDENTICAL input ladders (${byKey.size} distinct ladder pairs); weight == n_matched/n_samples; cross_language correct; no duplicate, none missing, none invented`);

  // ------------------------------------------- 6  live counters
  // the page's stated draw rule, reproduced independently here
  function independent(t, showInternal, capN) {
    const ext = json.edges.filter(e => e.kind === "external")
      .map((e, i) => ({ e, i }))
      .filter(o => o.e.weight >= t)
      .sort((p, q) => (q.e.weight - p.e.weight) || (p.i - q.i))
      .slice(0, capN)
      .map(o => o.e);
    const inte = showInternal ? intE : [];
    const idx = new Map(json.nodes.map((n, i) => [n.id, i]));
    const p = json.nodes.map((_, i) => i);
    const f = x => { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; };
    for (const e of inte.concat(ext)) {
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
        made.thr.value = String(t);
        made.showint.checked = showInternal;
        made.cap.value = String(capN);
        refresh();
        const shown = made.stats.textContent;
        const m = shown.match(RE);
        if (!m) throw new Error("unreadable counter: " + shown);
        const w = independent(t / 100, showInternal, capN);
        if (+m[1] !== rowN.length || +m[2] !== cenN.length)
          throw new Error("node counters wrong: " + shown);
        if (+m[3] !== w.ext || +m[4] !== w.int || +m[5] !== w.comps)
          throw new Error(`counter disagrees at t=${t / 100} internal=${showInternal} cap=${capN}: page "${shown}" vs independent ext=${w.ext} int=${w.int} comps=${w.comps}`);
        checks++;
      }
    }
  }
  console.log(`  [counters] ${checks} threshold x internal-toggle x draw-cap settings: the page's live row/central/external/internal/component counts equal an independent union-find, every one`);

  // ------------------------------------------- 7  the toggles bite
  made.thr.value = "85"; made.cap.value = "10000";
  made.showint.checked = true; refresh();
  const on = made.stats.textContent;
  made.showint.checked = false; refresh();
  const off = made.stats.textContent;
  if (on === off)
    throw new Error("the internal-connector toggle changes nothing -- it is not wired");
  console.log(`  [internal toggle wired] t=0.85 with internal connectors: "${on}"; without: "${off}"`);

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

  // the draw cap must be stated on screen when it bites
  made.thr.value = "0"; made.cap.value = "1000"; refresh();
  if (!/DRAW CAP IN FORCE/.test(made.rule.textContent))
    throw new Error("the draw cap bites but the page does not say so");
  console.log(`  [draw cap stated] "${made.rule.textContent.split("DRAW CAP IN FORCE: ")[1]}"`);

  // ------------------------------------------- 8  physics
  made.thr.value = "85"; made.cap.value = "10000"; refresh();
  if (timers.length === 0) throw new Error("no autofit interval registered");
  timers.forEach(f => f());
  console.log("  [autofit] the periodic fit ran with no throw");
  for (let i = 0; i < 600; i++) step();
  const bad = G.nodes.filter(n => !isFinite(n.x) || !isFinite(n.y) ||
                                  Math.hypot(n.x, n.y) > 2601);
  if (bad.length)
    throw new Error(bad.length + " nodes left the boundary -- the layout exploded");
  console.log("  [physics] after 600 steps every one of " + G.nodes.length +
    " nodes is finite and inside the hard boundary (grid repulsion, clamped linear springs, velocity clamp, gravity, boundary)");

  // it must SETTLE, not merely stay inside the boundary: 947 nodes is
  // heavier than the 43 of the pilot, so measure the drift
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

  // ------------------------------------------- 9  self-contained
  if (/<script\s+src/i.test(html)) throw new Error("external script tag present");
  if (html.includes("__GRAPH__")) throw new Error("placeholder not substituted");
  if (/https?:\/\//.test(html.replace(/https?:\/\/[^"']*w3\.org[^"']*/g, "")))
    throw new Error("an off-machine URL is present");
  console.log("  [self-contained] data embedded, placeholder gone, no external script, no CDN");

  console.log("HEADLESS VERIFY: all checks pass");
}

run();
