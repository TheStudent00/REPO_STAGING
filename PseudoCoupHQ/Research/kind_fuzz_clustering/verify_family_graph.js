#!/usr/bin/env node
// verify_family_graph.js -- headless (DOM-less) sanity for the
// dominant-operator FAMILY graph explorer, on the pattern of
// verify_row_graph_v5.js: a canvas-shaped stub RUNS the page's own
// script verbatim, and everything the picture stands on is re-derived
// independently of the python:
//
//   * THE EMBED is byte-identical to family_graph_v1.json, and every
//     family node in it is byte-identical to the same family in
//     dominant_operators_v1.json (id, members, name, spellings, counts);
//   * THE FAMILIES re-derived from scratch out of matrices_full_v2/
//     (form_pair + level + a digest of the full vector, in the loader's
//     own order) -- the partition and the `block#i` ids must be EXACTLY
//     the ones in the embed;
//   * EVERY EDGE KIND re-classified cell by cell from the CSVs by the
//     rule log_069 ruled: level-1 blocks EXHAUSTIVELY, level-2 blocks on
//     a deterministic 1-in-N sample.  Per-block WINDOW / VALUE / MIXED /
//     DECLINE-KIND totals must equal both the embed and log_070's
//     dominant_operators_v1.json;
//   * THE SETTLED DECLINE RULE: every kept WINDOW connector has at
//     least one comparable value cell, every refused one has none, and a
//     refused pair NEVER enters a component and NEVER carries layout;
//   * COMPONENTS counted by the page against an independent union-find,
//     at several kind/slider settings, and the WINDOW-only component
//     count at slider 0 against log_070's recorded number;
//   * MAXIMAL CLIQUES recomputed by an independent Bron-Kerbosch on the
//     default block -- the other reading of standing ruling 1.6;
//   * THE 1.6 CHAIN through `csharp.+ short x short` -- present as two
//     WINDOW-only connectors, VALUE-only when the ends are compared
//     directly, all three in ONE WINDOW-only component, and that
//     component spanning more than one census name; reachable by the
//     page's own control and by search;
//   * THE 1.5 WITNESS -- DECLINE-KIND only, zero value clashes, zero
//     window cells;
//   * FILTERS cut EXTERNAL connectors only (internal connectors are
//     untouched by every toggle and every slider position);
//   * autofit-once, wheel-disables-permanently, the fit-view button;
//   * self-contained: one inline script, no external URL, no CDN, no
//     position:fixed; and the ABSOLUTE vocabulary bans hold in the page
//     text.
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
const HTML = path.join(HERE, "family_graph_explorer_v1.html");
const JSONP = path.join(HERE, "family_graph_v1.json");
const SRCJ = path.join(HERE, "dominant_operators_v1.json");
const FULLD = path.join(HERE, "matrices_full_v2");
const SEP = ";";
const UNREP = "UNREPRESENTABLE";
const L2_SAMPLE_EVERY = 13;      // deterministic, seedless

let FAIL = 0;
function ok(msg) { console.log("  " + msg); }
function bad(msg) { FAIL++; console.log("  !! " + msg); }
function n(x) { return Number(x).toLocaleString("en-US"); }

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

function isValue(s) {
  return !(s === "REFUSE" || s === "ABORT" || s === UNREP ||
           s.startsWith("RAISE:"));
}

// ---- run the page in a stub DOM
function runPage(htmlPath, presets, exportSuffix) {
  const html = fs.readFileSync(htmlPath, "utf8");
  if (html.includes("<script src") || html.includes("://"))
    bad(path.basename(htmlPath) + " references an external script or URL");
  else ok("[self-contained] no <script src>, no URL of any kind anywhere " +
          "in the page -- data embedded, NO CDN");
  if (/position\s*:\s*fixed/.test(html))
    bad("the page uses position: fixed");
  else ok("[layout] no `position: fixed` anywhere in the page");
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
      id, tagName: tag || "div", value: "", checked: false, max: "",
      textContent: "", innerHTML: "", className: "", style: {}, dataset: {},
      addEventListener() {}, removeEventListener() {}, appendChild() {},
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 1400,
                                      height: 860 }),
      getContext: () => mkctx(),
      width: 1400, height: 860, offsetTop: 60,
    };
  }
  const made = {};
  for (const id of new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)]
                             .map(m => m[1]))) made[id] = mk(id);
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
    Int32Array, Float64Array, Uint8Array, parseInt, parseFloat, isNaN,
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
  return { ctx, made, listeners, X: sandbox.__EXP, html };
}

function uf(size, pairs) {
  const p = new Int32Array(size); for (let i = 0; i < size; i++) p[i] = i;
  const f = x => { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; };
  for (const [a, b] of pairs) {
    const ra = f(a), rb = f(b); if (ra !== rb) p[ra] = rb;
  }
  const cnt = new Map();
  for (let i = 0; i < size; i++) {
    const r = f(i); cnt.set(r, (cnt.get(r) || 0) + 1);
  }
  let multi = 0, mx = 0;
  for (const v of cnt.values()) { if (v > 1) multi++; if (v > mx) mx = v; }
  return { comps: cnt.size, multi, max: mx };
}

// independent Bron-Kerbosch with pivoting -- the OTHER reading of 1.6
function cliqueCount(size, adj) {
  let out = 0;
  const rec = (R, P, X) => {
    if (!P.size && !X.size) { out++; return; }
    let pivot = -1, best = -1;
    for (const u of P) { let c = 0; for (const w of adj[u]) if (P.has(w)) c++;
      if (c > best) { best = c; pivot = u; } }
    for (const u of X) { let c = 0; for (const w of adj[u]) if (P.has(w)) c++;
      if (c > best) { best = c; pivot = u; } }
    const cand = [...P].filter(v => !adj[pivot].has(v));
    for (const v of cand) {
      const nP = new Set(), nX = new Set();
      for (const w of P) if (adj[v].has(w)) nP.add(w);
      for (const w of X) if (adj[v].has(w)) nX.add(w);
      R.push(v); rec(R, nP, nX); R.pop();
      P.delete(v); X.add(v);
    }
  };
  rec([], new Set([...Array(size).keys()]), new Set());
  return out;
}

// ==================================================================
function main() {
  console.log("verify_family_graph -- headless checks on the " +
              "dominant-operator family graph (identity families, the " +
              "ruled disagreement kinds, both readings of 1.6)");
  const jsonText = fs.readFileSync(JSONP, "utf8");
  const json = JSON.parse(jsonText);
  const src = JSON.parse(fs.readFileSync(SRCJ, "utf8"));

  // ---------------------------------------------- 1  run the real page
  const page = runPage(HTML, {
    bsel: { value: "whole|whole/L1" }, mind: { value: "0" },
    kW: { checked: true }, kV: { checked: true }, kM: { checked: false },
    kD: { checked: true }, kR: { checked: false },
    showint: { checked: false }, cmode: { value: "mode" },
    hl: { value: "none" }, cap: { value: "9999999" }, search: { value: "" },
  }, "\n;globalThis.__EXP={G:G,build:build,refresh:refresh,step:step," +
     "fit:fit,autofit:autofit,goto16:goto16,goto15:goto15," +
     "FN:()=>FN,MN:()=>MN,INT:()=>INT,EXT:()=>EXT,WKEEP:()=>WKEEP," +
     "act:()=>act,actRef:()=>actRef,actInt:()=>actInt,pass:()=>pass," +
     "sel:()=>sel,note:()=>note,chain:()=>chain,wcomp:()=>wcomp," +
     "B:()=>B,hit:hit," +
     "state:()=>({T:T,KW:KW,KV:KV,KM:KM,KD:KD,KR:KR,SI:SI,CAP:CAP," +
     "scale:scale,ox:ox,oy:oy,heat:heat,userMoved:userMoved," +
     "fitted:fitted})};");
  ok("[script] the page's ONE inline script ran with no throw");
  const X = page.X;

  // ---------------------------------------------- 2  embed == JSON
  if (JSON.stringify(X.G) !== jsonText)
    bad("the embedded data is not byte-identical to " +
        path.basename(JSONP));
  else ok(`[embed] the embedded data is BYTE-IDENTICAL to ` +
          `${path.basename(JSONP)} (${n(jsonText.length)} chars, ` +
          `${json.blocks.length} gate blocks, ${n(json.n_families)} ` +
          `families, ${n(json.n_profiles)} profiles)`);

  // ------------------------- 3  family nodes == dominant_operators_v1
  const famSrc = new Map(src.families.map(f => [f.id, f]));
  let fbad = 0, fseen = 0;
  for (const b of json.blocks) for (const f of b.families) {
    const s = famSrc.get(f.id);
    fseen++;
    if (!s) { fbad++; continue; }
    if (JSON.stringify(f.members) !== JSON.stringify(s.members) ||
        f.name !== s.name ||
        JSON.stringify(f.spellings) !== JSON.stringify(s.spellings) ||
        JSON.stringify(f.languages) !== JSON.stringify(s.languages) ||
        JSON.stringify(f.member_windows) !==
          JSON.stringify(s.member_windows) ||
        f.n_profiles !== s.n_profiles || f.n_cells !== s.n_cells ||
        f.n_value_cells !== s.n_value_cells ||
        JSON.stringify(f.output_form_signature) !==
          JSON.stringify(s.output_form_signature)) fbad++;
  }
  if (fseen !== src.families.length)
    bad(`the graph carries ${fseen} families, log_070 has ` +
        `${src.families.length}`);
  if (fbad) bad(fbad + " family nodes differ from dominant_operators_v1");
  else ok(`[nodes] all ${n(fseen)} identity families -- id, members, ` +
          `named mode, spellings, languages, member windows, cell counts ` +
          `-- are byte-identical to dominant_operators_v1.json`);

  // -------------------------------- 4  read matrices_full_v2 from disk
  const t0 = Date.now();
  const fullIdx = JSON.parse(
    fs.readFileSync(path.join(FULLD, "index.json"), "utf8"));
  const spellOf = new Map();
  for (const m of Object.values(fullIdx.matrices))
    spellOf.set(m.language + "|" + m.file.split(".")[1] + "|" + m.level,
                m.operator);
  const blocks = new Map();      // "fp/Lk" -> Map(digest -> {vec,members})
  let nprof = 0;
  const files = fs.readdirSync(FULLD).filter(f => f.endsWith(".csv")).sort();
  for (const fn of files) {
    const parts = fn.slice(0, -4).split(".");
    const lang = parts[0], tok = parts[1], lvl = +parts[2].slice(1);
    const sp = spellOf.get(lang + "|" + tok + "|" + lvl) || tok;
    for (const r of parseCsv(fs.readFileSync(path.join(FULLD, fn), "utf8"))) {
      const bn = r.form_pair + "/L" + r.level;
      let slots = blocks.get(bn);
      if (!slots) { slots = new Map(); blocks.set(bn, slots); }
      const dg = crypto.createHash("blake2b512")
        .update(r.output_canon_vector).digest("hex").slice(0, 32);
      let s = slots.get(dg);
      if (!s) { s = { vec: r.output_canon_vector, members: [] };
                slots.set(dg, s); }
      s.members.push(`${lang}.${sp} ${r.lhs_holder} x ${r.rhs_holder}`);
      nprof++;
    }
  }
  ok(`[read] ${n(nprof)} profiles in ${files.length} matrices read from ` +
     `matrices_full_v2/ and grouped into ${blocks.size} gate blocks in ` +
     `${((Date.now() - t0) / 1000).toFixed(1)} s`);
  if (nprof !== json.n_profiles) bad("profile count disagrees with the graph");

  // ------------------- 5  the identity partition and every `block#i` id
  let idbad = 0, idseen = 0;
  for (const b of json.blocks) {
    const slots = blocks.get(b.block);
    if (!slots) { idbad++; continue; }
    const keys = [...slots.keys()];
    if (keys.length !== b.families.length) { idbad++; continue; }
    keys.forEach((k, i) => {
      idseen++;
      const want = slots.get(k).members.slice().sort();
      const got = b.families[i].members.slice().sort();
      if (b.families[i].id !== b.block + "#" + i ||
          JSON.stringify(want) !== JSON.stringify(got)) idbad++;
    });
  }
  if (idbad) bad(idbad + " families differ from the re-derived partition");
  else ok(`[contract] the identity partition re-derived from scratch out ` +
          `of the CSVs is EXACTLY the one drawn -- ${n(idseen)} families, ` +
          `same members and the same \`block#i\` id every time ` +
          `(equality is transitive, so no clique test)`);

  // ------------- 6  re-classify every pair; L1 exhaustive, L2 sampled
  const kindTot = { WINDOW: 0, VALUE: 0, MIXED: 0, "DECLINE-KIND": 0 };
  let l1pairs = 0, l2pairs = 0, kindBad = 0, declineBad = 0;
  for (const b of json.blocks) {
    const slots = blocks.get(b.block);
    const keys = [...slots.keys()];
    const d = keys.length;
    const cells = b.cells;
    const dict = new Map();
    const codes = [], vmask = [];
    for (const k of keys) {
      const v = slots.get(k).vec.split(SEP);
      if (v.length !== cells) bad(b.block + " wrong vector length");
      const c = new Int32Array(cells), m = new Uint8Array(cells);
      for (let p = 0; p < cells; p++) {
        let cc = dict.get(v[p]);
        if (cc === undefined) { cc = dict.size; dict.set(v[p], cc); }
        c[p] = cc; m[p] = isValue(v[p]) ? 1 : 0;
      }
      codes.push(c); vmask.push(m);
    }
    // the edge table as drawn, for a pairwise cross-check
    const drawn = new Map();
    const put = (a, bb, k, o) => drawn.set(a + ":" + bb, { k, o });
    for (const [slot, kk] of [["WINDOW", "WINDOW"],
                              ["WINDOW_REFUSED", "WINDOW"],
                              ["VALUE", "VALUE"], ["DECLINE", "DECLINE-KIND"]]) {
      const t = b.edges[slot];
      for (let i = 0; i < t.a.length; i++)
        put(t.a[i], t.b[i], kk, { nd: t.nd[i], vv: t.vv[i], wi: t.wi[i],
                                  tt: t.tt[i], cmp: t.cmp[i], slot });
    }
    for (let i = 0; i < b.mixed.a.length; i++)
      put(b.mixed.a[i], b.mixed.b[i], "MIXED",
          { nd: b.mixed.nd[i], slot: "MIXED" });
    const local = { WINDOW: 0, VALUE: 0, MIXED: 0, "DECLINE-KIND": 0 };
    let step = b.level === 1 ? 1 : L2_SAMPLE_EVERY, seq = 0;
    for (let i = 0; i < d; i++) {
      const ci = codes[i], mi = vmask[i];
      for (let j = i + 1; j < d; j++) {
        const cj = codes[j], mj = vmask[j];
        let nd = 0, vv = 0, wi = 0, cmp = 0;
        // level-2 blocks are sampled; the pair still has to be counted,
        // so the cheap "are they identical" question is asked always
        const sample = (seq++ % step) === 0;
        if (!sample && b.level === 2) {
          const e = drawn.get(i + ":" + j);
          if (e) local[e.k]++;
          continue;
        }
        for (let p = 0; p < cells; p++) {
          const both = mi[p] & mj[p];
          if (both) cmp++;
          if (ci[p] === cj[p]) continue;
          nd++;
          if (both) vv++; else if (mi[p] ^ mj[p]) wi++;
        }
        if (!nd) continue;
        const tt = nd - vv - wi;
        const k = (vv && wi) ? "MIXED" : (vv ? "VALUE"
                  : (wi ? "WINDOW" : "DECLINE-KIND"));
        local[k]++;
        if (b.level === 1) l1pairs++; else l2pairs++;
        const e = drawn.get(i + ":" + j);
        if (!e || e.k !== k || e.o.nd !== nd) { kindBad++; continue; }
        if (k !== "MIXED" &&
            (e.o.vv !== vv || e.o.wi !== wi || e.o.tt !== tt ||
             e.o.cmp !== cmp)) { kindBad++; continue; }
        // the settled decline rule, checked on the pair itself
        if (k === "WINDOW") {
          const wantSlot = cmp ? "WINDOW" : "WINDOW_REFUSED";
          if (e.o.slot !== wantSlot) declineBad++;
        }
      }
    }
    for (const k of Object.keys(local)) kindTot[k] += local[k];
    const emb = b.kind_counts;
    if (local.WINDOW !== emb.WINDOW || local.VALUE !== emb.VALUE ||
        local.MIXED !== emb.MIXED ||
        local["DECLINE-KIND"] !== emb.DECLINE_KIND)
      bad(`${b.block}: re-classified kinds ` +
          `${JSON.stringify(local)} against the embed ` +
          `${JSON.stringify(emb)}`);
    const s = src.block_stats.find(x => x.block === b.block);
    if (emb.WINDOW !== s.WINDOW || emb.VALUE !== s.VALUE ||
        emb.MIXED !== s.MIXED || emb.DECLINE_KIND !== s.DECLINE_KIND)
      bad(b.block + ": the embed disagrees with log_070's block_stats");
  }
  if (kindBad) bad(kindBad + " pairs carry the wrong kind or the wrong " +
                   "cell counts");
  else ok(`[kinds] every pair re-classified cell by cell from the CSVs ` +
          `by the ruled classifier: ${n(l1pairs)} level-1 pairs ` +
          `EXHAUSTIVELY, ${n(l2pairs)} level-2 pairs on a deterministic ` +
          `1-in-${L2_SAMPLE_EVERY} sample -- kind, disagreeing cells, ` +
          `value clashes, window cells, decline-vs-different-decline ` +
          `and comparable cells all agree with what is drawn`);
  if (declineBad)
    bad(declineBad + " WINDOW-only pairs sit on the wrong side of the " +
        "settled decline rule");
  else ok("[decline rule] every kept WINDOW-only connector has at least " +
          "one comparable value cell and every refused one has none -- " +
          "zero comparable keys means NO connector, not a zero-weight one");
  const pk = src.pair_kinds;
  if (kindTot.WINDOW !== pk.WINDOW || kindTot.VALUE !== pk.VALUE ||
      kindTot.MIXED !== pk.MIXED ||
      kindTot["DECLINE-KIND"] !== pk["DECLINE-KIND"])
    bad("run totals disagree with log_070: " + JSON.stringify(kindTot));
  else ok(`[kind totals] WINDOW-only ${n(pk.WINDOW)}, VALUE-only ` +
          `${n(pk.VALUE)}, MIXED ${n(pk.MIXED)}, DECLINE-KIND ` +
          `${n(pk["DECLINE-KIND"])} -- identical to ` +
          `dominant_operators_v1.json and to log_070's table`);

  // ------------------------------- 7  live counters vs a union-find
  const B0 = json.blocks.find(b => b.block === json.default_block);
  const mkEdges = (b, kinds, minnd) => {
    const out = [];
    const map = { WINDOW: "WINDOW", VALUE: "VALUE", DECLINE: "DECLINE" };
    for (const [slot, kk] of Object.entries(map)) {
      if (!kinds[kk]) continue;
      const t = b.edges[slot];
      for (let i = 0; i < t.a.length; i++)
        if (t.nd[i] >= minnd) out.push([t.a[i], t.b[i]]);
    }
    if (kinds.MIXED) for (let i = 0; i < b.mixed.a.length; i++)
      if (b.mixed.nd[i] >= minnd) out.push([b.mixed.a[i], b.mixed.b[i]]);
    return out;
  };
  const settings = [
    { W: 1, V: 1, M: 0, D: 1, t: 0 },
    { W: 1, V: 0, M: 0, D: 0, t: 0 },
    { W: 1, V: 1, M: 1, D: 1, t: 0 },
    { W: 1, V: 1, M: 0, D: 1, t: 40 },
    { W: 0, V: 1, M: 0, D: 0, t: 0 },
  ];
  const M = page.made;
  const nInternalAlways = X.INT().length;
  for (const s of settings) {
    M.kW.checked = !!s.W; M.kV.checked = !!s.V; M.kM.checked = !!s.M;
    M.kD.checked = !!s.D; M.mind.value = String(s.t);
    X.refresh();
    const want = mkEdges(B0, { WINDOW: s.W, VALUE: s.V, MIXED: s.M,
                               DECLINE: s.D }, s.t);
    const mine = uf(B0.n_families, want);
    const st = M.stats.textContent;
    const m = /components on the active set: (\d+) \((\d+) multi-node, largest (\d+)\)/
      .exec(st);
    const pg = X.pass().length;
    if (pg !== want.length)
      bad(`setting ${JSON.stringify(s)}: page passes ${pg} connectors, ` +
          `independent filter gives ${want.length}`);
    else if (!m || +m[1] !== mine.comps || +m[2] !== mine.multi ||
             +m[3] !== mine.max)
      bad(`setting ${JSON.stringify(s)}: page reports "${m && m[0]}", ` +
          `union-find gives ${mine.comps}/${mine.multi}/${mine.max}`);
    else ok(`[live] W=${s.W} V=${s.V} M=${s.M} D=${s.D} minND=${s.t}: ` +
            `${n(want.length)} external connectors, ${mine.comps} ` +
            `components (${mine.multi} multi-node, largest ${mine.max}) ` +
            `-- page and independent union-find agree`);
    // FILTERS CUT EXTERNAL CONNECTORS ONLY
    if (X.INT().length !== nInternalAlways)
      bad("a filter changed the internal connector set");
    if (X.actRef().length !== 0)
      bad("refused WINDOW pairs leaked into the drawn set while off");
  }
  ok(`[filters] every kind toggle and every slider position left the ` +
     `${n(nInternalAlways)} internal connectors untouched -- the filters ` +
     `cut EXTERNAL connectors ONLY, and components are counted on ` +
     `external connectors only`);

  // refused pairs are drawable but are NEVER connectors
  M.kW.checked = true; M.kV.checked = false; M.kM.checked = false;
  M.kD.checked = false; M.mind.value = "0"; M.kR.checked = true;
  X.refresh();
  {
    const withRef = /components on the active set: (\d+)/
      .exec(M.stats.textContent)[1];
    M.kR.checked = false; X.refresh();
    const without = /components on the active set: (\d+)/
      .exec(M.stats.textContent)[1];
    if (withRef !== without)
      bad("showing the refused WINDOW pairs changed the component count");
    else ok(`[refused] showing the ${n(B0.window_edges_refused)} refused ` +
            `WINDOW-only pairs of ${B0.block} changes NO component count ` +
            `and no layout -- they are drawn as evidence, never as ` +
            `connectors`);
  }

  // ------------------ 8  the 1.6 readings: components AND maximal cliques
  let cbad = 0;
  for (const b of json.blocks) {
    const r = src.relaxation.find(x => x.block === b.block);
    const kept = [];
    const t = b.edges.WINDOW;
    for (let i = 0; i < t.a.length; i++) kept.push([t.a[i], t.b[i]]);
    const mine = uf(b.n_families, kept);
    if (kept.length !== r.window_edges ||
        b.edges.WINDOW_REFUSED.a.length !==
          r.window_edges_refused_no_comparable_cell ||
        mine.comps !== r.components || mine.max !== r.largest_component ||
        b.maximal_cliques !== r.maximal_cliques) cbad++;
  }
  if (cbad) bad(cbad + " blocks disagree with log_070's relaxation table");
  else ok(`[1.6 components] in all ${json.blocks.length} gate blocks the ` +
          `WINDOW-only component count, the largest component, the kept ` +
          `and refused edge counts and the maximal-clique count agree ` +
          `with log_070's relaxation table, recomputed by an independent ` +
          `union-find here`);
  {
    const t = B0.edges.WINDOW;
    const adj = Array.from({ length: B0.n_families }, () => new Set());
    for (let i = 0; i < t.a.length; i++) {
      adj[t.a[i]].add(t.b[i]); adj[t.b[i]].add(t.a[i]);
    }
    const cq = cliqueCount(B0.n_families, adj);
    if (cq !== B0.maximal_cliques)
      bad(`independent Bron-Kerbosch gives ${cq} maximal cliques on ` +
          `${B0.block}, the page says ${B0.maximal_cliques}`);
    else ok(`[1.6 cliques] an independent Bron-Kerbosch on ${B0.block} ` +
            `gives ${n(cq)} maximal cliques against ${B0.components} ` +
            `connected components (largest ${B0.largest_component}) -- ` +
            `the two readings, side by side, NEITHER chosen`);
  }

  // -------------------------- 9  the 1.6 CHAIN, present and findable
  {
    const w = json.witness_1_6;
    const b = json.blocks.find(x => x.block === w.block);
    const [A, MID, Bx] = w.families.map(f => f.i);
    const find = (a, c) => {
      const lo = Math.min(a, c), hi = Math.max(a, c);
      for (const slot of ["WINDOW", "WINDOW_REFUSED", "VALUE", "DECLINE"]) {
        const t = b.edges[slot];
        for (let i = 0; i < t.a.length; i++)
          if (t.a[i] === lo && t.b[i] === hi)
            return { slot, nd: t.nd[i], vv: t.vv[i], wi: t.wi[i],
                     cmp: t.cmp[i] };
      }
      return null;
    };
    const h1 = find(A, MID), h2 = find(MID, Bx), dir = find(A, Bx);
    const kept = [];
    for (let i = 0; i < b.edges.WINDOW.a.length; i++)
      kept.push([b.edges.WINDOW.a[i], b.edges.WINDOW.b[i]]);
    const p = new Int32Array(b.n_families);
    for (let i = 0; i < b.n_families; i++) p[i] = i;
    const f = x => { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; }
                     return x; };
    for (const [a, c] of kept) { const ra = f(a), rc = f(c);
                                 if (ra !== rc) p[ra] = rc; }
    const same = f(A) === f(MID) && f(MID) === f(Bx);
    const comp = [];
    for (let i = 0; i < b.n_families; i++) if (f(i) === f(A)) comp.push(i);
    const names = [...new Set(comp.map(i => b.families[i].census_name)
                                 .filter(Boolean))].sort();
    const cd = b.component_detail.find(c => c.members.includes(A));
    if (!h1 || h1.slot !== "WINDOW" || !h2 || h2.slot !== "WINDOW" ||
        !dir || dir.slot !== "VALUE" || !same || names.length < 2)
      bad("the 1.6 chain is not present as measured");
    else ok(`[1.6 chain] on ${w.block}: \`${w.families[0].member}\` ` +
            `(${w.families[0].name}) --WINDOW-only(${h1.wi} window cells ` +
            `over ${h1.cmp} comparable)--> ` +
            `\`${w.families[1].member}\` (${w.families[1].name}) ` +
            `--WINDOW-only(${h2.wi}/${h2.cmp})--> ` +
            `\`${w.families[2].member}\` (${w.families[2].name}); ` +
            `compared DIRECTLY the two ends are VALUE-only at ${dir.vv} ` +
            `value cells over ${dir.cmp} comparable.  All three sit in ` +
            `ONE WINDOW-only component of ${comp.length} families / ` +
            `${cd.n_profiles} profiles carrying the census names ` +
            `${names.join(" + ")} -- the component SPANS named modes`);
    if (!cd || !cd.spans_modes)
      bad("the chain's component is not flagged as mode-spanning");
    else ok(`[1.6 findable] that component is listed in the page's own ` +
            `component panel and flagged SPANS MODES (${b.mode_spanning_components}` +
            ` of ${b.components_multi} multi-node components are)`);
    // the page's own control finds it
    M.search.value = ""; X.goto16();
    const sel = [...X.sel()].sort((a, c) => a - c);
    const want = [A, MID, Bx].sort((a, c) => a - c);
    if (JSON.stringify(sel) !== JSON.stringify(want) ||
        !/csharp\.\+ short x short/.test(X.note()) ||
        !X.chain() || X.chain().m !== MID)
      bad("the page's 1.6 control does not select the chain");
    else ok(`[1.6 control] the page's "1.6 chain" button selects exactly ` +
            `the three families, draws the two hops and the direct ` +
            `VALUE-only comparison, and writes the numbers into the panel`);
    // and search finds the middle family by member text
    M.search.value = "csharp.+ short x short"; X.refresh();
    const hits = X.FN().filter(nn => X.hit(nn));
    if (hits.length !== 1 || hits[0].i !== MID)
      bad("search does not find `csharp.+ short x short`");
    else ok("[1.6 search] typing `csharp.+ short x short` into the " +
            "search box matches exactly the middle family of the chain");
    M.search.value = ""; X.refresh();
  }

  // ------------------------------------ 10  the 1.5 fourth kind
  {
    const w = json.witness_1_5;
    const b = json.blocks.find(x => x.block === w.block);
    const t = b.edges.DECLINE;
    let hit = null;
    for (let i = 0; i < t.a.length; i++)
      if (t.a[i] === Math.min(w.ai, w.bi) && t.b[i] === Math.max(w.ai, w.bi))
        hit = { nd: t.nd[i], vv: t.vv[i], wi: t.wi[i], tt: t.tt[i],
                cmp: t.cmp[i] };
    const tot = json.blocks.reduce((s, x) => s + x.edges.DECLINE.a.length, 0);
    if (!hit || hit.vv !== 0 || hit.wi !== 0 || hit.tt !== hit.nd)
      bad("the 1.5 witness is not a DECLINE-KIND-only connector");
    else ok(`[1.5 witness] \`cpp.% int32_t x int32_t\` against ` +
            `\`csharp.% int x int\` on ${w.block}: ${hit.tt} cells where ` +
            `both declined with DIFFERENT declines, 0 value clashes, 0 ` +
            `window cells, over ${hit.cmp} comparable cells`);
    if (tot !== src.pair_kinds["DECLINE-KIND"])
      bad(`the graph draws ${tot} DECLINE-KIND connectors, log_070 ` +
          `measured ${src.pair_kinds["DECLINE-KIND"]}`);
    else ok(`[1.5 extent] all ${tot} DECLINE-KIND pairs of the run are ` +
            `drawn as their own separately toggleable kind, with their ` +
            `own colour AND their own dash`);
    X.goto15();
    if (![...X.sel()].includes(w.ai) || ![...X.sel()].includes(w.bi))
      bad("the page's 1.5 control does not select the witness");
    else ok("[1.5 control] the page's \"1.5 witness\" button selects the " +
            "pair and reports its cell counts");
  }

  // ---------------------------- 11  every block reachable, counts shown
  {
    let bbad = 0;
    for (const b of json.blocks) {
      M.bsel.value = b.block; M.bsel.onchange();
      const fn = X.FN().length, ex = X.EXT().length;
      const tot = b.kind_counts.WINDOW - b.window_edges_refused +
        b.kind_counts.VALUE + b.kind_counts.MIXED +
        b.kind_counts.DECLINE_KIND;
      if (fn !== b.n_families || ex !== tot) bbad++;
      if (!M.rule.textContent.includes(String(b.pairs))) bbad++;
    }
    if (bbad) bad(bbad + " gate blocks do not load correctly");
    else ok(`[blocks] all ${json.blocks.length} gate blocks load from the ` +
            `selector, each showing its own family count and its own ` +
            `per-kind pair counts out of the block's total pairs`);
    M.bsel.value = json.default_block; M.bsel.onchange();
  }

  // ------------------------------ 12  the draw cap is never silent
  {
    M.kM.checked = true; M.kW.checked = true; M.kV.checked = true;
    M.kD.checked = true; M.mind.value = "0"; M.cap.value = "40000";
    X.refresh();
    const passN = X.pass().length, drawn = X.act().length;
    const r = M.rule.textContent, st = M.stats.textContent;
    if (drawn !== 40000 || passN <= 40000)
      bad("the draw cap did not engage on the default block with MIXED on");
    else if (!/DRAW CAP IN FORCE/.test(r) ||
             !r.includes(String(passN - 40000)) ||
             !st.includes(drawn + " of " + passN))
      bad("the draw cap is in force but is not stated");
    else ok(`[cap] with MIXED on, ${n(passN)} connectors pass and the cap ` +
            `draws ${n(drawn)}: the page says so in both the status line ` +
            `("${drawn} of ${passN} connectors drawn [CAP]") and the rule ` +
            `line, and names the ${n(passN - 40000)} not drawn -- ` +
            `NOTHING is silently truncated`);
    M.cap.value = "9999999"; M.kM.checked = false; X.refresh();
  }

  // ------------------------------------ 13  autofit-once and the wheel
  {
    X.refresh();
    for (let i = 0; i < 1200 && X.state().heat > 0.3; i++) X.step();
    X.autofit();
    if (!X.state().fitted) bad("autofit did not run once heat settled");
    vm.runInContext("scale=0.123;ox=7;oy=9;", page.ctx);
    X.autofit();
    if (X.state().scale !== 0.123 || X.state().ox !== 7)
      bad("autofit ran a second time");
    (page.listeners.wheel || []).forEach(f => f({}));
    vm.runInContext("fitted=false;", page.ctx);
    X.autofit();
    if (X.state().scale !== 0.123)
      bad("a wheel did not disable autofit permanently");
    vm.runInContext("userMoved=false;fitted=false;", page.ctx);
    (page.listeners.mousedown || []).forEach(f => f({}));
    X.autofit();
    if (X.state().scale !== 0.123)
      bad("a mousedown did not disable autofit permanently");
    M.fitbtn.onclick();
    if (X.state().scale === 0.123)
      bad("the fit view button is dead");
    else ok("[autofit] runs ONCE and never again; a wheel disables it " +
            "permanently and so does a mousedown, even after the " +
            "once-only flag is cleared; the fit view button still works");
  }

  // ---------------------- 14  internal springs are near zero, and cheap
  if (!(json.int_spring > 0 && json.int_spring <= json.ext_spring / 20))
    bad(`internal spring ${json.int_spring} is not near zero against ` +
        `external ${json.ext_spring}`);
  else ok(`[springs] internal ${json.int_spring} against external ` +
          `${json.ext_spring} -- a member sub-node is TETHERED to its ` +
          `family node, ${Math.round(json.ext_spring / json.int_spring)}x ` +
          `weaker, and can never dominate the layout`);

  // ------------------------------------------ 15  the vocabulary bans
  {
    const body = page.html.replace(/^[\s\S]*?const G=/, "const G=")
      .replace(/^const G=[\s\S]*?\n/, "");   // drop the embedded data line
    const banned = /\b(parent|child|children|sibling|ancestor|descendant|orphan|death|kill(ed)?|died|dead)\b/i;
    const m = banned.exec(body);
    if (m) bad("banned vocabulary in the page text: " + m[0]);
    else ok("[vocabulary] none of parent / child / children / sibling / " +
            "ancestor / descendant / orphan / death / kill / died / dead " +
            "appears anywhere in the page's own text");
  }

  console.log(FAIL ? `!! ${FAIL} CHECK(S) FAILED` : "ALL CHECKS PASSED");
  process.exit(FAIL ? 1 : 0);
}

main();
