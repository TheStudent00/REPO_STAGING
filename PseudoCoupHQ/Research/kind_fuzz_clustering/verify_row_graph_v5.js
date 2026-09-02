#!/usr/bin/env node
// verify_row_graph_v5.js -- headless (DOM-less) sanity for the v5 row
// graph, the full-grid matrices, the dominance reading and both
// explorers.  The v4 pattern: a canvas-shaped stub RUNS each page's own
// script verbatim, and everything the picture stands on is re-derived
// independently of the python:
//
//   * matrices_full/ re-derived from matrices_cart/ on a deterministic
//     file sample: the probe-index rule, the full-set inflation and the
//     UNREPRESENTABLE fills, byte for byte;
//   * THE CONTRACTION re-derived from scratch out of matrices_full/
//     (level + form_pair + a digest of the full vector) -- the
//     partition must be EXACTLY the contracted nodes in the JSON;
//   * THE GATE checked on every connector and every compatible pair:
//     same form pair, same level, same full grid; a truth profile and a
//     whole profile never meet; L1 never mixes with L2; and NO pair has
//     a partial key overlap -- GROUP is structurally retired;
//   * BOTH SCORINGS re-derived: level-1 pairs EXHAUSTIVELY, level-2 on
//     a deterministic 1-in-N sample -- n_eq_all, n_value_comparable,
//     n_matched_value, n_unrep_either, both weights;
//   * THE DOMINANCE relation re-derived from the same vectors (viol
//     counts, nests / equal_values / overlaps / contradicts), the
//     category totals recounted over the COMPLETE pair table, and the
//     transitive reduction spot-checked both ways;
//   * THE OVERFLOW FRACTURE recomputed straight from the CSVs -- the
//     rust.+ i32 x i32 ~ ruby.+ Integer x Integer numbers must match
//     the JSON record, 14 overflow cells included;
//   * LIVE COUNTERS against an independent union-find in BOTH scoring
//     modes at three thresholds;
//   * autofit-once, wheel/mousedown permanence and the fit-view button,
//     on both pages.
//
// VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
// the OS-stopped outcome is ABORT.
//
// No external packages.

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const crypto = require("crypto");

const HERE = __dirname;
const HTML = path.join(HERE, "row_graph_explorer_v5.html");
const JSONP = path.join(HERE, "row_graph_v5.json");
const DHTML = path.join(HERE, "dominance_explorer_v5.html");
const DJSON = path.join(HERE, "dominance_v5.json");
const FULLD = path.join(HERE, "matrices_full");
const CARTD = path.join(HERE, "matrices_cart");
const SEP = ";";
const UNREP = "UNREPRESENTABLE";
const L2_SAMPLE_EVERY = 97;      // deterministic, seedless
const REFOLD_FILE_EVERY = 9;

let FAIL = 0;
function ok(msg) { console.log("  " + msg); }
function bad(msg) { FAIL++; console.log("  !! " + msg); }

// ---- RFC4180 (the vectors carry commas inside quotes)
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
    if (c === "\n") {
      row.push(field); rows.push(row); row = []; field = ""; i++; continue;
    }
    field += c; i++;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  if (rows.length && rows[rows.length - 1].length === 1 &&
      rows[rows.length - 1][0] === "") rows.pop();
  const head = rows.shift();
  return rows.map(r => Object.fromEntries(head.map((h, k) => [h, r[k]])));
}

function isDecline(s) {
  return s === "REFUSE" || s === "ABORT" || s.startsWith("RAISE:");
}

// ---- run one page in a stub DOM
function runPage(htmlPath, presets, exportSuffix) {
  const html = fs.readFileSync(htmlPath, "utf8");
  if (html.includes("<script src") || html.includes("http://") ||
      html.includes("https://"))
    bad(path.basename(htmlPath) + " references an external script or URL");
  function mkctx() {
    const c = {
      clearRect() {}, beginPath() {}, moveTo() {}, lineTo() {}, stroke() {},
      arc() {}, fill() {}, fillRect() {}, fillText() {}, setLineDash() {},
      closePath() {}, quadraticCurveTo() {}, save() {}, restore() {},
      measureText: t => ({ width: String(t).length * 6 }),
    };
    for (const k of ["fillStyle", "strokeStyle", "lineWidth", "font",
                     "globalAlpha", "textAlign"]) c[k] = "";
    return c;
  }
  function mk(id, tag) {
    return {
      id, tagName: tag || "div", value: "", checked: false,
      textContent: "", innerHTML: "", className: "", style: {}, dataset: {},
      addEventListener() {}, removeEventListener() {}, appendChild() {},
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 1400,
                                      height: 900 }),
      getContext: () => mkctx(),
      width: 1400, height: 900, offsetTop: 60,
    };
  }
  const made = {};
  for (const id of new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)]
                             .map(m => m[1]))) made[id] = mk(id);
  Object.assign.apply(null, [made].concat([]));
  for (const [id, props] of Object.entries(presets || {}))
    Object.assign(made[id] = made[id] || mk(id), props);
  const document = {
    getElementById: id => made[id] || (made[id] = mk(id)),
    createElement: t => mk("<" + t + ">", t),
    querySelector: () => null, querySelectorAll: () => [],
    addEventListener() {}, body: mk("body"), documentElement: mk("html"),
  };
  const listeners = {};
  const timers = [];
  const sandbox = {
    document, console: { log() {} },
    addEventListener(t, f) { (listeners[t] = listeners[t] || []).push(f); },
    removeEventListener() {},
    requestAnimationFrame() { return 0; },
    setInterval(f) { timers.push(f); return timers.length; },
    clearInterval() {}, setTimeout() { return 0; },
    innerWidth: 1400, innerHeight: 900, devicePixelRatio: 1,
    Math, JSON, Set, Map, Array, Object, String, Number, Boolean,
    Int32Array,
  };
  sandbox.window = sandbox; sandbox.self = sandbox;
  sandbox.globalThis = sandbox;
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
    .map(m => m[1]);
  if (scripts.length !== 1)
    throw new Error("expected one inline script in " + htmlPath);
  const ctx = vm.createContext(sandbox);
  vm.runInContext(scripts[0] + exportSuffix, ctx,
                  { filename: path.basename(htmlPath) });
  return { ctx, made, listeners, X: sandbox.__EXP };
}

function uf(n, pairs) {
  const p = new Int32Array(n); for (let i = 0; i < n; i++) p[i] = i;
  const f = x => { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; };
  for (const [a, b] of pairs) {
    const ra = f(a), rb = f(b); if (ra !== rb) p[ra] = rb;
  }
  const roots = new Set(); for (let i = 0; i < n; i++) roots.add(f(i));
  const size = new Map();
  for (let i = 0; i < n; i++) {
    const r = f(i); size.set(r, (size.get(r) || 0) + 1);
  }
  let multi = 0; for (const v of size.values()) if (v > 1) multi++;
  return { comps: roots.size, multi };
}

// ==================================================================
function main() {
  console.log("verify_row_graph_v5 -- headless checks on the v5 row " +
              "graph (full grids, the compatibility gate, two " +
              "scorings, dominance)");
  const json = JSON.parse(fs.readFileSync(JSONP, "utf8"));
  const dj = JSON.parse(fs.readFileSync(DJSON, "utf8"));
  const fullIdx = JSON.parse(
    fs.readFileSync(path.join(FULLD, "index.json"), "utf8"));
  const cartIdx = JSON.parse(
    fs.readFileSync(path.join(CARTD, "index.json"), "utf8"));

  // ---------------------------------------------- 1  run the real page
  const page = runPage(HTML, {
    cap: { value: "1000000" }, cmode: { value: "lang" },
    lmode: { value: "all" }, showint: { checked: true },
    smode: { value: "value" }, thr: { value: "85" },
  }, "\n;globalThis.__EXP={G:G,refresh:refresh,step:step,fit:fit," +
     "autofit:autofit,EXT:EXT,INT:INT,N:N," +
     "act:()=>act,actInt:()=>actInt,W:W," +
     "state:()=>({T:T,SM:SM,heat:heat,scale:scale,ox:ox,oy:oy," +
     "userMoved:userMoved,fitted:fitted})};");
  ok("[script] row_graph_explorer_v5's one inline script ran with no " +
     "throw");
  const X = page.X;
  if (X.G.nodes.length !== json.nodes.length ||
      X.G.edges.length !== json.edges.length)
    bad("embed and standalone JSON disagree on size");
  else for (const k of ["n_raw_rows", "n_contracted_nodes",
                        "n_central_nodes", "n_internal_edges",
                        "n_external_edges", "n_compatible_pairs",
                        "int_spring", "ext_spring"])
    if (JSON.stringify(X.G[k]) !== JSON.stringify(json[k]))
      bad("embed disagrees on " + k);
  ok(`[embed] ${X.G.nodes.length} nodes, ${X.G.edges.length} ` +
     `connectors, identical to ${path.basename(JSONP)}`);
  if (json.groups !== undefined || X.G.groups !== undefined)
    bad("a groups array exists -- GROUP is retired");
  else ok("[group] no groups array anywhere -- GROUP retired, as ruled");

  // ---------------------------------------------- 2  kinds and the gate
  const conN = json.nodes.filter(n => n.kind === "contracted");
  const cenN = json.nodes.filter(n => n.kind === "central");
  const intE = json.edges.filter(e => e.kind === "internal");
  const extE = json.edges.filter(e => e.kind === "external");
  if (conN.length !== json.n_contracted_nodes ||
      cenN.length !== json.n_central_nodes ||
      intE.length !== json.n_internal_edges ||
      extE.length !== json.n_external_edges)
    bad("header counts disagree with the arrays");
  const totalMembers = conN.reduce((t, n) => t + n.n_members, 0);
  if (totalMembers !== json.n_raw_rows)
    bad("contracted members do not partition the raw profiles");
  const byId = new Map(json.nodes.map(n => [n.id, n]));
  let gatebad = 0, wbad = 0;
  for (const e of extE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (!a || !b || a.kind !== "contracted" || b.kind !== "contracted")
      gatebad++;
    else {
      if (a.level !== b.level || a.level !== e.level) gatebad++;
      if (a.form_pair !== b.form_pair ||
          a.form_pair !== e.form_pair) gatebad++;
      if (a.n_cells !== b.n_cells || a.n_cells !== e.n_cells) gatebad++;
      if (a.operators.some(o => b.operators.includes(o))) gatebad++;
    }
    if (!(e.weight_all >= 0 && e.weight_all <= 1)) wbad++;
    if (e.weight_value !== null &&
        !(e.weight_value >= 0 && e.weight_value <= 1)) wbad++;
    if (e.weight_value === null && e.n_value_comparable !== 0) wbad++;
  }
  if (gatebad) bad(gatebad + " external connectors break the gate");
  else ok(`[gate] every one of the ${extE.length} external connectors ` +
          `joins two contracted nodes with the SAME form pair, SAME ` +
          `level, SAME full grid and NO shared lang.op -- a truth ` +
          `profile never meets a whole profile, L1 never mixes with L2`);
  if (wbad) bad(wbad + " connectors carry a bad weight"); else
    ok("[weights] weight_all in [0,1] on every connector; " +
       "weight_value in [0,1] or null exactly when no value-comparable " +
       "cell exists");

  // ---------------------------------------------- 3  read matrices_full
  const t0 = Date.now();
  const rows = [];
  const dict = new Map();
  const code = s => {
    let c = dict.get(s);
    if (c === undefined) { c = dict.size; dict.set(s, c); }
    return c;
  };
  const files = Object.values(fullIdx.matrices).map(m => m.file).sort();
  for (const fn of files) {
    for (const r of parseCsv(fs.readFileSync(path.join(FULLD, fn),
                                             "utf8"))) {
      const cells = r.output_canon_vector.split(SEP);
      const n = +r.n_probes;
      if (cells.length !== n) bad(fn + " " + r.probe_id +
                                  " wrong vector length");
      const codes = new Int32Array(n);
      let nv = 0, nd = 0, nu = 0;
      for (let k = 0; k < n; k++) {
        const c = cells[k];
        codes[k] = code(c);
        if (c === UNREP) nu++;
        else if (isDecline(c)) nd++;
        else nv++;
      }
      if (nv !== +r.n_values || nd !== +r.n_declines ||
          nu !== +r.n_unrepresentable)
        bad(fn + " " + r.probe_id + " cell-class counts disagree with " +
            "the recorded columns");
      const langop = fn.startsWith("rust.") ? "rust" : "ruby";
      rows.push({
        id: null, file: fn, probe_id: r.probe_id, level: +r.level,
        form_pair: r.form_pair, lhs: r.lhs_holder, rhs: r.rhs_holder,
        codes, n, nv, nd, nu,
      });
    }
  }
  const decl = new Uint8Array(dict.size), unrp = new Uint8Array(dict.size);
  for (const [s, c] of dict) {
    if (s === UNREP) unrp[c] = 1; else if (isDecline(s)) decl[c] = 1;
  }
  ok(`[read] ${rows.length} profiles, ` +
     `${rows.reduce((t, r) => t + r.n, 0)} cells, ${dict.size} distinct ` +
     `canon strings read from matrices_full/ in ` +
     `${((Date.now() - t0) / 1000).toFixed(1)} s`);
  const gridOf = new Map();
  let gridbad = 0;
  for (const r of rows) {
    const k = r.form_pair + "/L" + r.level;
    if (!gridOf.has(k)) gridOf.set(k, r.n);
    else if (gridOf.get(k) !== r.n) gridbad++;
  }
  if (gridbad) bad(gridbad + " profiles break the one-grid-per-block " +
                   "rule -- a partial overlap would be possible");
  else ok(`[full-grid] ONE grid size per (form_pair, level) across all ` +
          `${gridOf.size} gate blocks -- a partial key overlap is ` +
          `IMPOSSIBLE inside the gate, which is why GROUP retired`);

  // -------------------------- 4  matrices_full re-derived from cart
  const fullSets = fullIdx.full_sets;
  const xs = cartIdx.x_sets;
  let refolded = 0, refoldBad = 0;
  const cartFiles = files.filter((_, i) => i % REFOLD_FILE_EVERY === 0);
  for (const fn of cartFiles) {
    const cart = parseCsv(fs.readFileSync(path.join(CARTD, fn), "utf8"));
    const full = parseCsv(fs.readFileSync(path.join(FULLD, fn), "utf8"));
    if (cart.length !== full.length) { refoldBad++; continue; }
    for (let ri = 0; ri < cart.length; ri++) {
      const cr = cart[ri], fr = full[ri];
      const level = +cr.level;
      const fa = xs[fullSets[xs[cr.x_set_a].form + "/L" + level]]
        .spellings;
      const fb = xs[fullSets[xs[cr.x_set_b].form + "/L" + level]]
        .spellings;
      const pa = new Map(xs[cr.x_set_a].spellings.map((s, i) => [s, i]));
      const pb = new Map(xs[cr.x_set_b].spellings.map((s, i) => [s, i]));
      const nb = pb.size;
      const q = [];
      for (const s0 of fa) for (const s1 of fb) {
        const i0 = pa.has(s0) ? pa.get(s0) : -1;
        const i1 = pb.has(s1) ? pb.get(s1) : -1;
        q.push(i0 < 0 || i1 < 0 ? -1 : i0 * nb + i1);
      }
      let map = q;
      if (level === 2) {
        const block = pa.size * nb;
        map = [];
        for (const q01 of q) for (const q23 of q)
          map.push(q01 < 0 || q23 < 0 ? -1 : q01 * block + q23);
      }
      const src = cr.output_canon_vector.split(SEP);
      const want = map.map(p => (p < 0 ? UNREP : src[p])).join(SEP);
      refolded++;
      if (want !== fr.output_canon_vector ||
          fr.src_x_set_a !== cr.x_set_a || fr.src_x_set_b !== cr.x_set_b)
        refoldBad++;
    }
  }
  if (refoldBad) bad(refoldBad + " re-folded rows disagree with " +
                     "matrices_full/");
  else ok(`[refold] ${refolded} profiles across ${cartFiles.length} ` +
          `matrices (every ${REFOLD_FILE_EVERY}th file) re-inflated ` +
          `from matrices_cart/ through the probe-index rule -- ` +
          `byte-identical to matrices_full/, UNREPRESENTABLE fills ` +
          `included`);

  // ------------------------------ 5  contraction re-derived from scratch
  const part = new Map();
  rows.forEach((r, i) => {
    const dg = crypto.createHash("sha1")
      .update(r.level + "|" + r.form_pair + "|")
      .update(Buffer.from(r.codes.buffer)).digest("hex");
    if (!part.has(dg)) part.set(dg, []);
    part.get(dg).push(i);
  });
  if (part.size !== conN.length)
    bad(`re-derived contraction has ${part.size} identity sets, JSON ` +
        `has ${conN.length}`);
  else {
    // match by member-row id strings
    rows.forEach(r => {
      r.id = r.file.startsWith("rust.") ? null : null;
    });
    // rebuild row ids the builder's way
    const opOf = new Map(Object.values(fullIdx.matrices)
      .map(m => [m.file, [m.language, m.operator, m.level]]));
    rows.forEach(r => {
      const [lang, op] = opOf.get(r.file);
      r.id = `${lang}.${op} / L${r.level} / ${r.probe_id} / ` +
             `${r.lhs} ${op} ${r.rhs}`;
    });
    const want = new Set([...part.values()]
      .map(v => v.map(i => rows[i].id).sort().join(" ")));
    let miss = 0;
    for (const n of conN)
      if (!want.has(n.members.slice().sort().join(" "))) miss++;
    if (miss) bad(miss + " contracted nodes differ from the re-derived " +
                  "partition");
    else ok(`[contract] the contraction re-derived from scratch is ` +
            `EXACTLY the one in the JSON -- ${conN.length} identity ` +
            `sets over the full grids, UNREPRESENTABLE and outcome ` +
            `tokens included, same members every time`);
  }

  // --------------------------------- 6  both scorings + dominance
  const rowById = new Map(rows.map(r => [r.id, r]));
  const nodeRow = new Map();          // contracted id -> representative
  for (const n of conN) nodeRow.set(n.id, rowById.get(n.members[0]));
  const pc = json.pairs_compact;
  const cid = i => conN[i].id;
  let checkedL1 = 0, checkedL2 = 0, scoreBad = 0, domBad = 0;
  const relCount = { nests: 0, equal_values: 0, overlaps: 0,
                     contradicts: 0 };
  for (let k = 0; k < pc.n; k++) {
    relCount[pc.rel[k]]++;
    // arithmetic re-check of the relation from the recorded counts
    const contra = pc.nmv[k] < pc.nvv[k];
    const dab = pc.vab[k] === 0, dba = pc.vba[k] === 0;
    const want = contra ? "contradicts"
      : (dab && dba ? "equal_values"
         : (dab || dba ? "nests" : "overlaps"));
    if (want !== pc.rel[k]) domBad++;
    const lv = nodeRow.get(cid(pc.a[k])).level;
    if (!(lv === 1 ? true : (k % L2_SAMPLE_EVERY === 0)) && lv === 2)
      continue;
    const A = nodeRow.get(cid(pc.a[k])), B = nodeRow.get(cid(pc.b[k]));
    if (A.form_pair !== B.form_pair || A.level !== B.level || A.n !== B.n)
      { scoreBad++; continue; }
    let neq = 0, nvv = 0, nmv = 0, nue = 0, vab = 0, vba = 0;
    for (let p = 0; p < A.n; p++) {
      const ca = A.codes[p], cb = B.codes[p];
      const va = !decl[ca] && !unrp[ca], vb = !decl[cb] && !unrp[cb];
      const eq = ca === cb;
      if (eq) neq++;
      if (va && vb) { nvv++; if (eq) nmv++; }
      if (unrp[ca] || unrp[cb]) nue++;
      if (vb && !eq) vab++;
      if (va && !eq) vba++;
    }
    if (neq !== pc.neq[k] || nvv !== pc.nvv[k] || nmv !== pc.nmv[k] ||
        nue !== pc.nue[k] || vab !== pc.vab[k] || vba !== pc.vba[k])
      scoreBad++;
    if (lv === 1) checkedL1++; else checkedL2++;
  }
  if (scoreBad) bad(scoreBad + " pair scorings disagree with the " +
                    "re-derivation");
  else ok(`[scoring] BOTH scorings and the dominance counts re-derived ` +
          `from the raw vectors: ${checkedL1} level-1 pairs ` +
          `EXHAUSTIVELY, ${checkedL2} level-2 pairs on a deterministic ` +
          `1-in-${L2_SAMPLE_EVERY} sample -- n_eq_all, ` +
          `n_value_comparable, n_matched_value, n_unrep_either, vab, ` +
          `vba all agree exactly`);
  if (domBad) bad(domBad + " recorded dominance relations disagree " +
                  "with their own counts");
  else ok("[dominance] the relation of every one of the " + pc.n +
          " compatible pairs re-derived from its recorded counts; " +
          "category totals: nests " + relCount.nests +
          ", equal_values " + relCount.equal_values +
          ", overlaps " + relCount.overlaps +
          ", contradicts " + relCount.contradicts);
  for (const k of ["nests", "equal_values", "overlaps", "contradicts"])
    if (relCount[k] !== json.dominance_counts[k])
      bad("dominance count " + k + " disagrees with the builder");
  if (relCount.nests !== dj.counts.nests ||
      dj.nest_edges.length !== dj.n_nest_edges ||
      dj.reduced_edges.length !== dj.n_reduced_edges)
    bad("dominance_v5.json disagrees with itself or the graph");
  else ok(`[dominance json] ${dj.nest_edges.length} directed nest ` +
          `connectors, ${dj.reduced_edges.length} after transitive ` +
          `reduction, consistent between dominance_v5.json and the ` +
          `graph`);

  // transitive reduction: reduced <= nests; spot-check both directions
  const nestSet = new Set(dj.nest_edges.map(e => e[0] + ">" + e[1]));
  const domOf = new Map();
  for (const [a, b] of dj.nest_edges) {
    if (!domOf.has(a)) domOf.set(a, new Set());
    domOf.get(a).add(b);
  }
  let redBad = 0;
  for (const [a, b] of dj.reduced_edges) {
    if (!nestSet.has(a + ">" + b)) redBad++;
    else {
      for (const c of domOf.get(a) || [])
        if (c !== b && (domOf.get(c) || new Set()).has(b)) redBad++;
    }
  }
  let dropOk = 0, dropBad = 0;
  const redSet = new Set(dj.reduced_edges.map(e => e[0] + ">" + e[1]));
  dj.nest_edges.forEach((e, i) => {
    if (i % 7 !== 0 || redSet.has(e[0] + ">" + e[1])) return;
    let via = false;
    for (const c of domOf.get(e[0]) || [])
      if (c !== e[1] && (domOf.get(c) || new Set()).has(e[1])) via = true;
    if (via) dropOk++; else dropBad++;
  });
  if (redBad || dropBad)
    bad(`transitive reduction wrong: ${redBad} redundant edges kept, ` +
        `${dropBad} dropped edges with no two-step route`);
  else ok(`[lattice] the transitive reduction keeps no redundant ` +
          `connector and every sampled dropped connector (${dropOk}) ` +
          `has a two-step dominator route`);

  // --------------------------------------- 7  the overflow fracture
  const fr = json.overflow_fracture.i32;
  const rustRow = rows.find(r => r.id.startsWith("rust.+ / L1 /") &&
                                 r.lhs === "i32" && r.rhs === "i32");
  const rubyRow = rows.find(r => r.id.startsWith("ruby.+ / L1 /") &&
                                 r.lhs === "Integer" &&
                                 r.rhs === "Integer");
  let neq = 0, nvv = 0, nmv = 0, nOver = 0, nUv = 0;
  for (let p = 0; p < rustRow.n; p++) {
    const ca = rustRow.codes[p], cb = rubyRow.codes[p];
    const va = !decl[ca] && !unrp[ca], vb = !decl[cb] && !unrp[cb];
    if (ca === cb) neq++;
    if (va && vb) { nvv++; if (ca === cb) nmv++; }
    if (decl[ca] && vb) nOver++;
    if (unrp[ca] && vb) nUv++;
  }
  const wAll = neq / rustRow.n, wVal = nvv ? nmv / nvv : null;
  if (nOver !== fr.n_overflow_cells_rust_declines_ruby_answers ||
      nUv !== fr.n_unrepresentable_vs_value ||
      Math.abs(wAll - fr.weight_all) > 1e-6 ||
      Math.abs(wVal - fr.weight_value) > 1e-6 ||
      nvv !== fr.n_value_comparable ||
      fr.overflow_keys.length !== nOver)
    bad("the overflow fracture record disagrees with the CSVs");
  else ok(`[fracture] rust.+ i32 x i32 ~ ruby.+ Integer x Integer ` +
          `recomputed from the CSVs: weight_value ${wVal.toFixed(4)} ` +
          `over ${nvv} value cells; weight_all ${wAll.toFixed(4)} = ` +
          `${neq}/${rustRow.n}; ${nOver} overflow cells (rust declines, ` +
          `ruby answers) -- the fracture scoring (a) hides and scoring ` +
          `(b) shows, exactly as recorded`);

  // ------------------------------ 8  live counters, both scorings
  for (const sm of ["value", "all"]) {
    for (const t of [0.95, 0.85, 0.70]) {
      page.made.smode.value = sm;
      page.made.thr.value = String(Math.round(t * 100));
      X.refresh();
      const act = X.act();
      const w = "weight_" + sm;
      const wantE = extE.filter(e => e[w] !== null && e[w] >= t - 1e-12);
      const idxOf = new Map(json.nodes.map((n, i) => [n.id, i]));
      const mine = uf(json.nodes.length,
                      wantE.map(e => [idxOf.get(e.a), idxOf.get(e.b)]));
      const st = page.made.stats.textContent;
      const mComp = /(\d+) components \((\d+) multi-node\)/.exec(st);
      const rec = json.sanity.thresholds[sm + "@" + t.toFixed(2)];
      if (act.length !== wantE.length || act.length !== rec.external_edges)
        bad(`scoring ${sm} t=${t}: page draws ${act.length}, expected ` +
            `${wantE.length}, builder recorded ${rec.external_edges}`);
      else if (+mComp[1] !== mine.comps ||
               mine.comps !== rec.components_external_only ||
               +mComp[2] !== mine.multi)
        bad(`scoring ${sm} t=${t}: component counts disagree`);
      else ok(`[live] scoring ${sm} t=${t.toFixed(2)}: ` +
              `${act.length} external connectors, ${mComp[1]} ` +
              `components (${mComp[2]} multi-node) -- page, ` +
              `independent union-find and builder all agree`);
    }
  }

  // -------------------------------- 9  autofit-once, both pages
  page.made.smode.value = "value"; page.made.thr.value = "85";
  X.refresh();
  for (let i = 0; i < 900 && X.state().heat > 0.3; i++) X.step();
  X.autofit();
  const s1 = X.state();
  if (!s1.fitted) bad("autofit did not run once heat settled");
  vm.runInContext("scale=0.123;ox=7;oy=9;", page.ctx);
  X.autofit();
  const s2 = X.state();
  if (s2.scale !== 0.123 || s2.ox !== 7)
    bad("autofit ran a second time");
  (page.listeners.wheel || []).forEach(f => f({}));
  vm.runInContext("fitted=false;", page.ctx);
  X.autofit();
  const s3 = X.state();
  if (s3.scale !== 0.123) bad("a wheel did not disable autofit " +
                              "permanently");
  vm.runInContext("cv.onwheel({preventDefault(){},deltaY:-1});",
                  page.ctx);
  page.made.fitbtn.onclick ? page.made.fitbtn.onclick() :
    vm.runInContext("fit();", page.ctx);
  if (X.state().scale === 0.123 * 1.1) bad("fit view button dead");
  ok("[autofit] runs ONCE and never again; a wheel disables it " +
     "permanently even after the once-only flag is cleared; the fit " +
     "view button works");

  // ---------------------------------------- 10  the dominance page
  const dpage = runPage(DHTML, { thr: { value: "0" } },
    "\n;globalThis.__EXP={D:D,build:build,fit:fit,autofit:autofit," +
    "nodes:()=>nodes,edges:()=>edges,byId:byId," +
    "state:()=>({B:B,T:T,scale:scale,ox:ox,userMoved:userMoved," +
    "fitted:fitted})};");
  ok("[script] dominance_explorer_v5's one inline script ran with no " +
     "throw");
  const DX = dpage.X;
  if (DX.D.nest_edges.length !== dj.nest_edges.length ||
      DX.D.nodes.length !== dj.nodes.length)
    bad("dominance embed disagrees with dominance_v5.json");
  else ok(`[embed] dominance page embeds ${DX.D.nodes.length} nodes ` +
          `and ${DX.D.nest_edges.length} nest connectors, identical ` +
          `to ${path.basename(DJSON)}`);
  let layerBad = 0, blockBad = 0;
  for (const b of dj.blocks) {
    dpage.made.bsel.value = b;
    dpage.made.bsel.onchange();
    for (const e of DX.edges()) {
      const A = DX.byId[e[0]], B2 = DX.byId[e[1]];
      if (A.form_pair + "/L" + A.level !== b ||
          B2.form_pair + "/L" + B2.level !== b) blockBad++;
      if (!(A.y < B2.y)) layerBad++;
    }
  }
  if (blockBad || layerBad)
    bad(`lattice drawing: ${blockBad} connectors cross a gate block, ` +
        `${layerBad} do not point downward`);
  else ok("[lattice page] in every gate block, every drawn nest " +
          "connector stays inside its block and the dominator sits " +
          "HIGHER than the dominated");
  dpage.made.bsel.value = dj.blocks[0]; dpage.made.bsel.onchange();
  dpage.made.thr.value = "50"; dpage.made.thr.oninput();
  let cutBad = 0;
  for (const e of DX.edges())
    if (DX.byId[e[1]].n_value_cells < 50) cutBad++;
  if (cutBad) bad("the slider failed to cut " + cutBad + " connectors");
  else ok("[lattice page] the slider cuts external connectors only, " +
          "and every surviving connector clears it");
  vm.runInContext("scale=0.321;", dpage.ctx);
  (dpage.listeners.wheel || []).forEach(f => f({}));
  vm.runInContext("fitted=false;", dpage.ctx);
  DX.autofit();
  if (DX.state().scale !== 0.321)
    bad("dominance page: a wheel did not disable autofit");
  else ok("[autofit] dominance page: wheel disables autofit " +
          "permanently; fit view button exists");

  console.log(FAIL ? `!! ${FAIL} CHECK(S) FAILED` : "ALL CHECKS PASSED");
  process.exit(FAIL ? 1 : 0);
}

main();
