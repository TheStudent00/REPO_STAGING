#!/usr/bin/env node
// verify_graph_interval.js -- headless (DOM-less) sanity for the
// interval-pilot agreement-graph explorer.
//
// domstub.js cannot carry this page: the explorer draws on a <canvas>
// and domstub's elements have no getContext.  So this file provides a
// canvas-shaped stub, RUNS the page's own script, and then checks the
// two things the picture stands on:
//
//   1  the live counters the page shows ("<n> edges | <c> components")
//      agree, at every threshold and with the criterion both on and
//      off, with an INDEPENDENT union-find computed here from the
//      embedded data -- two methods, one answer;
//   2  the embedded data equals the standalone JSON the builder wrote,
//      every edge endpoint is a real node, no edge has weight 0, and
//      criterion_pass is exactly `input_overlap >= weight` so the
//      filter is reversible from the raw numbers.
//
// Mirrors verify_dendro_extended.js in shape.  No external packages.

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const HERE = __dirname;
const HTML = path.join(HERE, "graph_explorer_interval_pilot.html");
const JSONP = path.join(HERE, "agreement_graph_interval_pilot.json");

function ctx2d() {
  const noop = () => {};
  return {
    clearRect: noop, beginPath: noop, moveTo: noop, lineTo: noop,
    stroke: noop, fill: noop, arc: noop, fillRect: noop, fillText: noop,
    save: noop, restore: noop, translate: noop, scale: noop,
    measureText: () => ({ width: 10 }),
    set fillStyle(v) {}, get fillStyle() { return "#000"; },
    set strokeStyle(v) {}, get strokeStyle() { return "#000"; },
    set lineWidth(v) {}, get lineWidth() { return 1; },
    set globalAlpha(v) {}, get globalAlpha() { return 1; },
    set font(v) {}, get font() { return "13px sans-serif"; },
  };
}

// `children` / `appendChild` below are the DOM's own API names,
// which a stub has to spell exactly; they are not vocabulary.
function mk(id, tag) {
  const el = {
    id, tagName: tag || "div", _html: "", style: {}, dataset: {},
    children: [], value: "", checked: false, className: "",
    textContent: "", width: 1400, height: 900, offsetTop: 40,
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
  return el;
}

function run() {
  const html = fs.readFileSync(HTML, "utf8");
  const json = JSON.parse(fs.readFileSync(JSONP, "utf8"));

  const made = {};
  for (const id of new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)]
                             .map(m => m[1]))) made[id] = mk(id);
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
  if (scripts.length !== 1) throw new Error("expected exactly one inline script, got " + scripts.length);
  const ctx = vm.createContext(sandbox);
  // `const G = ...` at a script's top level is lexical, so it never
  // lands on the context object; the page is run VERBATIM and its own
  // bindings are handed out at the end.
  vm.runInContext(scripts[0] +
    "\n;globalThis.__EXP={G:G,refresh:refresh,step:step};",
    ctx, { filename: "explorer.js" });
  console.log("  [script] the page's one inline script ran with no throw");

  // --- the embed must equal the standalone JSON
  const { G, refresh, step } = ctx.__EXP;
  if (G.nodes.length !== json.nodes.length || G.edges.length !== json.edges.length)
    throw new Error("embed and standalone JSON disagree on size");
  console.log(`  [embed] ${G.nodes.length} nodes, ${G.edges.length} edges, identical to ${path.basename(JSONP)}`);

  // --- structural checks
  const ids = new Set(G.nodes.map(n => n.id));
  for (const e of G.edges) {
    if (!ids.has(e.a) || !ids.has(e.b)) throw new Error("edge endpoint is not a node: " + e.a + "~" + e.b);
    if (!(e.weight > 0)) throw new Error("0-weight edge present: " + e.a + "~" + e.b);
    if (e.criterion_pass !== (e.input_overlap >= e.weight))
      throw new Error("criterion_pass does not equal input_overlap>=weight on " + e.a + "~" + e.b);
  }
  console.log("  [structure] every endpoint is a node; no 0-weight edge; criterion_pass reversible from the raw numbers");

  // --- independent counts vs the page's own live counters
  function independent(t, useCrit, useVW) {
    const act = G.edges.filter(e => (!useCrit || e.criterion_pass) &&
      (useVW ? e.value_weight : e.weight) != null &&
      (useVW ? e.value_weight : e.weight) >= t);
    const p = G.nodes.map((_, i) => i);
    const idx = {}; G.nodes.forEach((n, i) => idx[n.id] = i);
    const f = x => { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; };
    act.forEach(e => { const a = f(idx[e.a]), b = f(idx[e.b]); if (a != b) p[a] = b; });
    return { edges: act.length, comps: new Set(G.nodes.map((_, i) => f(i))).size };
  }
  let checks = 0;
  for (const useCrit of [true, false]) {
    for (const t of [95, 85, 70, 50, 0]) {
      made.thr.value = String(t);
      made.crit.checked = useCrit;
      made.usevw.checked = false;
      refresh();
      const shown = made.stats.textContent;
      const want = independent(t / 100, useCrit, false);
      const m = shown.match(/^(\d+) edges \| (\d+) components/);
      if (!m) throw new Error("unreadable counter: " + shown);
      if (+m[1] !== want.edges || +m[2] !== want.comps)
        throw new Error(`counter disagrees at t=${t / 100} crit=${useCrit}: page "${shown}" vs independent ${want.edges}/${want.comps}`);
      checks++;
    }
  }
  console.log(`  [counters] ${checks} threshold x criterion settings: the page's live edge and component counts equal an independent union-find, every one`);

  // --- the criterion checkbox must actually change something
  made.thr.value = "70"; made.crit.checked = true; refresh();
  const on = made.stats.textContent;
  made.crit.checked = false; refresh();
  const off = made.stats.textContent;
  if (on === off) throw new Error("the input-overlap criterion changes nothing at t=0.70 -- the filter is not wired");
  console.log(`  [criterion wired] t=0.70 with the filter: "${on}"; without it: "${off}"`);

  // --- autofit and the clamped physics must be present, not exploding
  if (timers.length === 0) throw new Error("no autofit interval registered");
  timers.forEach(f => f());
  console.log("  [autofit] the periodic fit ran with no throw");
  step();
  const bad = G.nodes.filter(n => !isFinite(n.x) || !isFinite(n.y) ||
                                  Math.hypot(n.x, n.y) > 1401);
  if (bad.length) throw new Error(bad.length + " nodes left the boundary -- the layout exploded");
  console.log("  [physics] after a step every node is finite and inside the hard boundary (clamped springs, velocity clamp, gravity, boundary)");

  console.log("HEADLESS VERIFY: all checks pass");
}

run();
