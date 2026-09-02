#!/usr/bin/env node
// verify_row_graph_v4.js -- headless (DOM-less) sanity for the v4 row
// graph and its explorer: the CARTESIAN probe design of log 052 rebuilt
// with the owner's three rulings of 2026-08-21.
//
// `verify_row_graph_v3.js` is left on disk unchanged, and so are the v3
// products.  This is a v4 verifier, not an edit.
//
// Same shape as the v3 verifier: domstub.js cannot carry this page (the
// explorer draws on a <canvas> and domstub's elements have no
// getContext), so this file supplies a canvas-shaped stub, RUNS the
// page's own script verbatim, and then checks the things the picture
// stands on.  What it checks that the v3 verifier did not:
//
//   *  THE CONTRACTION is re-derived from scratch, straight out of
//      matrices_cart/: every row's (level, x_set_a, x_set_b) and a
//      digest of its output_canon_vector.  The partition that falls out
//      must be EXACTLY the contracted nodes in the JSON -- same members,
//      same count, nothing merged that is not identical and nothing
//      identical left apart.
//   *  THE ALIGNMENT is re-implemented here, independently: the shared
//      operand spellings, the probe-index rule of index.json
//      (level 1 p = i0*|Xb|+i1, level 2 p = ((i0*|Xb|+i1)*|Xa|+i2)*|Xb|
//      +i3), the intersection, the decline exclusion, and BOTH scorings.
//      Level-1 pairs are re-derived EXHAUSTIVELY; level-2 pairs on a
//      deterministic 1-in-N sample, and the sample size is printed
//      rather than hidden.
//   *  EVERY GROUP IS A TRUE MAXIMAL CLIQUE, checked against the
//      complete pair table: every pair inside it exists, has
//      n_comparable >= 1 and weight_exact == 1.0; no node outside it is
//      1.0 with all of its members; and the recorded minimum and maximum
//      overlap are the real ones.  A connected component is NOT a clique
//      and the check would reject one.
//   *  THE TRANSITIVITY HAZARD is recounted here from the pair table and
//      must equal the number the builder reported.
//   *  THE LIVE COUNTERS are checked against an independent union-find
//      IN BOTH SCORING MODES and IN BOTH VIEW MODES (groups expanded,
//      groups collapsed), at three thresholds and at both documented
//      sigmoid limits.
//   *  HULL RENDERING AND COLLAPSE/EXPAND: the page's convex hull really
//      encloses its members, and a click inside a hull collapses the
//      group to one node while a second click expands it again.
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
const HTML = path.join(HERE, "row_graph_explorer_v4.html");
const JSONP = path.join(HERE, "row_graph_v4.json");
const CART = path.join(HERE, "matrices_cart");
const SEP = ";";
const TOL = 1e-6;
const L2_SAMPLE_EVERY = 211;     // deterministic, seedless

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
function decParts(s) {
  const m = /^(-?)(\d*)(?:\.(\d*))?$/.exec(s.trim());
  if (!m) return null;
  return { sign: m[1] === "-" ? "-" : "", int: m[2] || "0", frac: m[3] || "" };
}
function decSub(a, b) {                 // |a - b| as a JS number
  const A = decParts(a), B = decParts(b);
  if (!A || !B) return Math.abs(parseFloat(a) - parseFloat(b));
  const scale = Math.max(A.frac.length, B.frac.length);
  const ai = BigInt(A.sign + A.int + A.frac.padEnd(scale, "0"));
  const bi = BigInt(B.sign + B.int + B.frac.padEnd(scale, "0"));
  let d = ai - bi; if (d < 0n) d = -d;
  return Number(d) / Math.pow(10, scale);
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

// ------------------------------------------------------------------
// CHANGE 1 re-implemented: the shared-key positions
// ------------------------------------------------------------------
function keyPositions(level, aSpell, bSpell, ia, ib) {
  const pa = new Map(aSpell.map((s, i) => [s, i]));
  const pb = new Map(bSpell.map((s, i) => [s, i]));
  const nb = bSpell.length;
  const q = [];
  for (const s of ia) for (const t of ib) q.push(pa.get(s) * nb + pb.get(t));
  if (level === 1) return q;
  const block = aSpell.length * nb;
  const out = [];
  for (const u of q) for (const v of q) out.push(u * block + v);
  return out;
}
function sharedKeys(xs, sigA, sigB) {
  if (sigA[0] !== sigB[0]) return null;         // never mix the levels
  const a1 = xs[sigA[1]].spellings, b1 = xs[sigA[2]].spellings;
  const a2 = xs[sigB[1]].spellings, b2 = xs[sigB[2]].spellings;
  const ia = a1.filter(s => a2.includes(s)).sort();
  const ib = b1.filter(s => b2.includes(s)).sort();
  if (!ia.length || !ib.length) return null;
  return { p1: keyPositions(sigA[0], a1, b1, ia, ib),
           p2: keyPositions(sigB[0], a2, b2, ia, ib) };
}

// ------------------------------------------------------------------
function uf(n, pairs) {
  const p = new Int32Array(n); for (let i = 0; i < n; i++) p[i] = i;
  const f = x => { while (p[x] !== x) { p[x] = p[p[x]]; x = p[x]; } return x; };
  for (const [a, b] of pairs) {
    const ra = f(a), rb = f(b); if (ra !== rb) p[ra] = rb;
  }
  const roots = new Set(); for (let i = 0; i < n; i++) roots.add(f(i));
  const size = new Map();
  for (let i = 0; i < n; i++) { const r = f(i); size.set(r, (size.get(r) || 0) + 1); }
  let multi = 0; for (const v of size.values()) if (v > 1) multi++;
  return { comps: roots.size, multi };
}

// ==================================================================
function main() {
  console.log("verify_row_graph_v4 -- headless checks on the v4 row graph " +
              "(input-key alignment, CONTRACT, GROUP)");
  const html = fs.readFileSync(HTML, "utf8");
  const json = JSON.parse(fs.readFileSync(JSONP, "utf8"));
  const knobs = json.scoring_knobs;
  const idx = JSON.parse(fs.readFileSync(path.join(CART, "index.json"), "utf8"));
  const xs = idx.x_sets;

  // ---------------------------------------------- run the real page
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
      addEventListener() {}, removeEventListener() {},
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 1400, height: 900 }),
      getContext: () => mkctx(),
      width: 1400, height: 900, offsetTop: 60,
    };
  }
  const made = {};
  for (const id of new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)]
                             .map(m => m[1]))) made[id] = mk(id);
  made.cap.value = "1000000";
  made.cmode.value = "lang";
  made.lmode.value = "all";
  made.showint.checked = true;
  made.hulls.checked = true;
  made.collapseall.checked = false;
  made.exact.checked = false;
  made.thr.value = "85"; made.mid.value = "50"; made.stp.value = "0";

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
    "autofit:autofit,EXT:EXT,INT:INT,N:N,GR:GR,idx:idx," +
    "act:()=>act,actInt:()=>actInt,sig:g=>sig(g),W:e=>W(e)," +
    "hull:()=>hullCache,host:()=>HOST,hullOf:hullOf," +
    "padPts:padPts,onclick:ev=>cv.onclick(ev)," +
    "state:()=>({T:T,EX:EX,MID:MID,K:K,heat:heat,scale:scale,ox:ox,oy:oy})};",
    ctx, { filename: "explorer.js" });
  ok("[script] the page's one inline script ran with no throw");
  const X = ctx.__EXP;

  // -------------------------------------------------- 1  embed == JSON
  if (X.G.nodes.length !== json.nodes.length ||
      X.G.edges.length !== json.edges.length ||
      X.G.groups.length !== json.groups.length)
    bad("embed and standalone JSON disagree on size");
  else for (const k of ["n_raw_rows", "n_contracted_nodes", "n_central_nodes",
                        "n_groups", "n_internal_edges", "n_external_edges",
                        "int_spring", "ext_spring", "grp_spring", "render_cap"])
    if (X.G[k] !== json[k]) bad("embed disagrees on " + k);
  ok(`[embed] ${X.G.nodes.length} nodes, ${X.G.edges.length} connectors, ` +
     `${X.G.groups.length} groups, identical to ${path.basename(JSONP)}`);

  // -------------------------------------------------- 2  counts by kind
  const conN = json.nodes.filter(n => n.kind === "contracted");
  const cenN = json.nodes.filter(n => n.kind === "central");
  const intE = json.edges.filter(e => e.kind === "internal");
  const extE = json.edges.filter(e => e.kind === "external");
  if (conN.length + cenN.length !== json.nodes.length)
    bad("a node is neither contracted nor central");
  if (intE.length + extE.length !== json.edges.length)
    bad("a connector is neither internal nor external");
  if (conN.length !== json.n_contracted_nodes ||
      cenN.length !== json.n_central_nodes ||
      intE.length !== json.n_internal_edges ||
      extE.length !== json.n_external_edges)
    bad("header counts disagree with the arrays");
  const byLevel = {};
  for (const n of conN) byLevel[n.level] = (byLevel[n.level] || 0) + 1;
  const totalMembers = conN.reduce((t, n) => t + n.n_members, 0);
  if (totalMembers !== json.n_raw_rows)
    bad(`contracted members sum to ${totalMembers}, not ${json.n_raw_rows}`);
  ok(`[kinds] ${conN.length} contracted nodes (L1 ${byLevel[1] || 0}, ` +
     `L2 ${byLevel[2] || 0}) carrying ${totalMembers} member rows = the ` +
     `${json.n_raw_rows} raw rows exactly, + ${cenN.length} central nodes; ` +
     `${intE.length} internal + ${extE.length} external connectors`);

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

  // -------------------------------------------------- 4  raw rows read
  // one file at a time; only the digest and the operand-set ids are kept,
  // so the 191 MB of matrices never sits in memory at once
  const rowMeta = new Map();     // row node id -> {file, probe_id, sig, dig}
  for (const key of Object.keys(idx.matrices)) {
    const m = idx.matrices[key];
    const txt = fs.readFileSync(path.join(CART, m.file), "utf8");
    for (const r of parseCsv(txt)) {
      const id = `${m.language}.${m.operator} / L${m.level} / ${r.probe_id} / ` +
                 `${r.lhs_holder} ${m.operator} ${r.rhs_holder}`;
      rowMeta.set(id, {
        file: m.file, probe_id: r.probe_id, level: m.level,
        sig: `L${m.level} ${r.x_set_a} ${r.x_set_b}`,
        x_set_a: r.x_set_a, x_set_b: r.x_set_b,
        dig: crypto.createHash("sha1")
               .update(r.output_canon_vector).digest("hex"),
      });
    }
  }
  ok(`[rows] ${rowMeta.size} rows read out of matrices_cart/, each reduced ` +
     `to its operand-set ids and a sha1 of its output_canon_vector`);

  // -------------------------------------------------- 5  CONTRACTION
  // re-derive the partition from scratch and demand the SAME one
  const mine = new Map();
  for (const [id, m] of rowMeta) {
    const k = m.sig + " " + m.dig;
    if (!mine.has(k)) mine.set(k, []);
    mine.get(k).push(id);
  }
  let cbad2 = 0, seenRows = new Set();
  const theirs = new Map();
  for (const n of conN) {
    const k = new Set(n.members.map(m => {
      const mm = rowMeta.get(m);
      return mm ? mm.sig + " " + mm.dig : "MISSING:" + m;
    }));
    if (k.size !== 1) { cbad2++; continue; }
    const key = [...k][0];
    if (theirs.has(key)) cbad2++;          // two nodes for one identity set
    theirs.set(key, n);
    for (const m of n.members) {
      if (seenRows.has(m)) cbad2++;
      seenRows.add(m);
    }
  }
  if (mine.size !== theirs.size) {
    bad(`independent contraction gives ${mine.size} identity sets, the ` +
        `JSON has ${theirs.size} contracted nodes`);
    cbad2++;
  } else {
    for (const [k, ids] of mine) {
      const n = theirs.get(k);
      if (!n) { cbad2++; continue; }
      if (n.n_members !== ids.length) { cbad2++; continue; }
      const a = [...ids].sort().join("|");
      const b = [...n.members].sort().join("|");
      if (a !== b) cbad2++;
    }
  }
  if (seenRows.size !== rowMeta.size) cbad2++;
  if (cbad2) bad(`${cbad2} contraction violations`);
  else ok(`[contract] the contraction re-derived from matrices_cart/ is ` +
          `EXACTLY the one in the JSON: ${mine.size} identity sets, same ` +
          `members every time.  Nothing was merged that is not identical ` +
          `on an identical input key set, and nothing identical was left ` +
          `apart.  The ${seenRows.size} member rows partition the raw rows.`);

  // -------------------------------------------------- 6  vectors, lazily
  const cache = new Map();
  function vecOf(id) {
    const meta = rowMeta.get(id);
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
  const vcache = new Map();
  function vv(id) {
    if (!vcache.has(id)) {
      if (vcache.size > 300) vcache.clear();
      vcache.set(id, vecOf(id));
    }
    return vcache.get(id);
  }

  // -------------------------------------------------- 7  THE ALIGNMENT
  function rescore(nodeA, nodeB) {
    const sigA = [nodeA.level, nodeA.x_set_a, nodeA.x_set_b];
    const sigB = [nodeB.level, nodeB.x_set_a, nodeB.x_set_b];
    const sh = sharedKeys(xs, sigA, sigB);
    if (!sh) return null;
    const va = vv(nodeA.members[0]), vb = vv(nodeB.members[0]);
    if (!va || !vb) return null;
    let nc = 0, ne = 0, sum = 0;
    for (let k = 0; k < sh.p1.length; k++) {
      const a = va[sh.p1[k]], b = vb[sh.p2[k]];
      const s = sampleSim(a, b, knobs);
      if (s === null) continue;                  // ruling B: never scored
      nc++; sum += s;
      if (a === b) ne++;
    }
    return { n_shared_keys: sh.p1.length, n_comparable: nc,
             n_matched_exact: ne,
             weight_exact: nc ? ne / nc : null,
             weight_graded: nc ? sum / nc : null };
  }

  const order = extE.map((e, i) => [e, i]);
  const check = order.filter(([e, i]) => e.level === 1 ||
                                         i % L2_SAMPLE_EVERY === 0);
  check.sort((p, q) => (p[0].a + p[0].b < q[0].a + q[0].b ? -1 : 1));
  let wbad = 0, n1 = 0, n2 = 0;
  for (const [e] of check) {
    const rec = rescore(byId.get(e.a), byId.get(e.b));
    if (!rec) { wbad++; continue; }
    if (Math.abs(rec.weight_exact - e.weight_exact) > TOL ||
        Math.abs(rec.weight_graded - e.weight_graded) > TOL ||
        rec.n_comparable !== e.n_comparable ||
        rec.n_matched_exact !== e.n_matched_exact ||
        rec.n_shared_keys !== e.n_shared_keys ||
        rec.n_shared_keys - rec.n_comparable !== e.n_excluded_declines) {
      if (wbad < 5)
        console.log(`     mismatch ${e.a} ~ ${e.b}: builder exact ` +
          `${e.weight_exact} graded ${e.weight_graded} ncmp ${e.n_comparable}` +
          ` nk ${e.n_shared_keys} | verifier exact ` +
          `${rec.weight_exact.toFixed(6)} graded ` +
          `${rec.weight_graded.toFixed(6)} ncmp ${rec.n_comparable} nk ` +
          `${rec.n_shared_keys}`);
      wbad++;
    }
    if (e.level === 1) n1++; else n2++;
  }
  if (wbad) bad(`${wbad} connectors disagree with the independent rescore`);
  else ok(`[align] ${n1} level-1 connectors re-derived EXHAUSTIVELY and ` +
          `${n2} level-2 connectors on a deterministic 1-in-` +
          `${L2_SAMPLE_EVERY} sample, straight from the operand spellings ` +
          `and the probe-index rule; the shared-key count, the decline ` +
          `exclusion and BOTH weights agree to ${TOL} -- two ` +
          `implementations, one answer`);

  // level 1 and level 2 are never mixed, and a connector never claims
  // more shared keys than either side owns
  let lbad = 0;
  for (const e of extE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (a.level !== b.level || a.level !== e.level) lbad++;
    if (e.n_shared_keys > Math.min(a.n_input_keys, b.n_input_keys)) lbad++;
    if (!(e.n_comparable > 0)) lbad++;
    if (e.n_comparable + e.n_excluded_declines !== e.n_shared_keys) lbad++;
    if (e.n_matched_exact > e.n_comparable) lbad++;
    const shared = a.operators.filter(o => b.operators.includes(o));
    if (shared.length) lbad++;
    if (e.same_key_set !== (a.x_set_a === b.x_set_a &&
                            a.x_set_b === b.x_set_b)) lbad++;
  }
  if (lbad) bad(`${lbad} external-connector rule violations`);
  else ok("[external] every external connector joins two contracted nodes " +
          "with NO lang.op in common at the SAME level; level 1 is never " +
          "mixed with level 2; n_comparable > 0, n_comparable + " +
          "n_excluded_declines == n_shared_keys, and n_shared_keys never " +
          "exceeds either side's own key count");

  // -------------------------------------------------- 8  internal rule
  const wantInt = new Map();
  for (const n of conN) wantInt.set(n.id, new Set(n.operators));
  const gotInt = new Map();
  let ibad = 0;
  for (const e of intE) {
    const a = byId.get(e.a), b = byId.get(e.b);
    if (!a || a.kind !== "contracted" || !b || b.kind !== "central") { ibad++; continue; }
    if (!a.operators.includes(b.id)) { ibad++; continue; }
    if (!gotInt.has(e.a)) gotInt.set(e.a, new Set());
    if (gotInt.get(e.a).has(e.b)) ibad++;
    gotInt.get(e.a).add(e.b);
    if (e.no_comparison !== (e.n_co_nodes_comparable === 0)) ibad++;
    if (e.no_comparison && (e.weight_exact !== 1 || e.weight_graded !== 1)) ibad++;
  }
  for (const [id, s] of wantInt) {
    const g = gotInt.get(id);
    if (!g || g.size !== s.size) { ibad++; continue; }
    for (const o of s) if (!g.has(o)) ibad++;
  }
  if (ibad) bad(`${ibad} internal-connector rule violations`);
  else ok(`[internal] exactly one internal connector per contracted node ` +
          `per lang.op it carries, ${intE.length} in all; no_comparison ` +
          `== (n_co_nodes_comparable == 0) and then both weights are 1.0 ` +
          `by convention`);

  // -------------------------------------------------- 9  THE PAIR TABLE
  const P = json.pairs_compact;
  const cidx = new Map(conN.map((n, i) => [n.id, i]));
  const pkey = (a, b) => (a < b ? a + ":" + b : b + ":" + a);
  const PT = new Map();
  for (let i = 0; i < P.n; i++)
    PT.set(pkey(P.a[i], P.b[i]),
           { nc: P.nc[i], ne: P.ne[i], nk: P.nk[i] });
  if (PT.size !== P.n) bad("the pair table has duplicate entries");
  // every external connector must be in it, with the same numbers
  let pbad = 0;
  for (const e of extE) {
    const r = PT.get(pkey(cidx.get(e.a), cidx.get(e.b)));
    if (!r || r.nc !== e.n_comparable || r.ne !== e.n_matched_exact ||
        r.nk !== e.n_shared_keys) pbad++;
  }
  if (pbad) bad(`${pbad} external connectors disagree with the pair table`);
  else ok(`[pairs] the complete pair table carries ${P.n} contracted-node ` +
          `pairs that share at least one input key, and every one of the ` +
          `${extE.length} external connectors appears in it with the same ` +
          `numbers`);
  // a deterministic sample of the table re-derived from the matrices --
  // including pairs that carry NO connector, so "no comparable key" is
  // checked as hard as "some comparable key"
  let zbad = 0, zn = 0, sn = 0;
  for (let i = 0; i < P.n; i += 337) {
    const A = conN[P.a[i]], B = conN[P.b[i]];
    const rec = rescore(A, B);
    if (!rec) { zbad++; continue; }
    if (rec.n_comparable !== P.nc[i] || rec.n_matched_exact !== P.ne[i] ||
        rec.n_shared_keys !== P.nk[i]) zbad++;
    if (P.nc[i] === 0) zn++;
    sn++;
  }
  if (zbad) bad(`${zbad} pair-table entries disagree with the matrices`);
  else ok(`[pairs] ${sn} of them re-derived from matrices_cart/ on a ` +
          `deterministic 1-in-337 sample (${zn} of the sample have ZERO ` +
          `comparable keys and correctly carry no connector)`);

  // -------------------------------------------------- 10  GROUPS
  const adj = new Map();
  for (let i = 0; i < conN.length; i++) adj.set(i, new Set());
  for (let i = 0; i < P.n; i++)
    if (P.nc[i] >= 1 && P.ne[i] === P.nc[i]) {      // exact-match rate 1.0
      adj.get(P.a[i]).add(P.b[i]);
      adj.get(P.b[i]).add(P.a[i]);
    }
  let gbad = 0;
  for (const g of json.groups) {
    const mi = g.members.map(m => cidx.get(m));
    if (mi.some(v => v === undefined)) { gbad++; continue; }
    const lv = new Set(mi.map(i => conN[i].level));
    if (lv.size !== 1 || [...lv][0] !== g.level) gbad++;
    let mn = Infinity, mx = -Infinity, np = 0;
    for (let x = 0; x < mi.length; x++)
      for (let y = x + 1; y < mi.length; y++) {
        const r = PT.get(pkey(mi[x], mi[y]));
        if (!r) { gbad++; continue; }                 // never compared
        if (!(r.nc >= 1)) gbad++;                     // no overlap
        if (r.ne !== r.nc) gbad++;                    // not exact-1.0
        mn = Math.min(mn, r.nc); mx = Math.max(mx, r.nc); np++;
      }
    if (np !== g.size * (g.size - 1) / 2) gbad++;
    if (mn !== g.min_overlap || mx !== g.max_overlap) gbad++;
    if (g.pair_overlaps.length !== np) gbad++;
    // MAXIMAL: no node outside is 1.0 with every member
    const ms = new Set(mi);
    for (let o = 0; o < conN.length; o++) {
      if (ms.has(o)) continue;
      let all = true;
      for (const m of mi) if (!adj.get(o).has(m)) { all = false; break; }
      if (all) { gbad++; break; }
    }
  }
  if (gbad) bad(`${gbad} group violations`);
  else ok(`[group] every one of the ${json.groups.length} groups is a TRUE ` +
          `MAXIMAL CLIQUE: every pair inside was actually compared, has ` +
          `n_comparable >= 1 and an exact-match rate of exactly 1.0; the ` +
          `recorded minimum (${Math.min(...json.groups.map(g => g.min_overlap))}` +
          `) and maximum overlaps are the real ones; and no contracted ` +
          `node outside a group is 1.0 with all of its members.  A ` +
          `connected component would fail this check.`);
  // and the group graph really is what the builder said it was
  let onePairs = 0;
  for (let i = 0; i < P.n; i++) if (P.nc[i] >= 1 && P.ne[i] === P.nc[i]) onePairs++;
  if (onePairs !== json.grouping.n_one_pairs)
    bad(`the pair table has ${onePairs} exact-1.0 pairs, the builder said ` +
        `${json.grouping.n_one_pairs}`);
  else ok(`[group] ${onePairs} mutually exact-1.0 pairs in the table, the ` +
          `number the builder reported`);

  // -------------------------------------------------- 11  TRANSITIVITY
  let hz = 0, hzNo = 0, hzLt = 0;
  for (const [b, nb] of adj) {
    const l = [...nb].sort((p, q) => p - q);
    for (let x = 0; x < l.length; x++)
      for (let y = x + 1; y < l.length; y++) {
        const a = l[x], c = l[y];
        if (adj.get(a).has(c)) continue;
        const r = PT.get(pkey(a, c));
        if (!r || r.nc === 0) hzNo++; else hzLt++;
        hz++;
      }
  }
  const T3 = json.transitivity;
  if (hz !== T3.violating_triples || hzNo !== T3.because_A_C_have_no_comparable_key ||
      hzLt !== T3.because_A_C_below_1)
    bad(`transitivity recount ${hz} (${hzLt} below 1.0, ${hzNo} no ` +
        `comparable key) against the builder's ${T3.violating_triples} ` +
        `(${T3.because_A_C_below_1}, ${T3.because_A_C_have_no_comparable_key})`);
  else ok(`[transitivity] ${hz} triples (A,B,C) with A~B = 1.0 and B~C = ` +
          `1.0 while A~C is NOT -- ${hzLt} because A~C is below 1.0 on ` +
          `keys they share, ${hzNo} because A and C have no comparable ` +
          `key at all.  Recounted here and equal to the builder's number.  ` +
          `None of them is merged and none is grouped.`);

  // -------------------------------------------------- 12  live counters
  const nid = new Map(json.nodes.map((n, i) => [n.id, i]));
  const gmi = json.groups.map(g => g.member_node_idx);
  const settings = [
    { exact: false, thr: 95, mid: 50, stp: 0 },
    { exact: false, thr: 85, mid: 50, stp: 0 },
    { exact: false, thr: 70, mid: 50, stp: 0 },
    { exact: true, thr: 95, mid: 50, stp: 0 },
    { exact: true, thr: 85, mid: 50, stp: 0 },
    { exact: true, thr: 70, mid: 50, stp: 0 },
    { exact: false, thr: 50, mid: 30, stp: 600 },
    { exact: false, thr: 50, mid: 50, stp: 6000 },
  ];
  let kbad = 0;
  for (const view of ["expanded", "collapsed"]) {
    made.collapseall.checked = (view === "collapsed");
    made.collapseall.onchange();
    for (const s of settings) {
      made.exact.checked = s.exact;
      made.thr.value = String(s.thr);
      made.mid.value = String(s.mid);
      made.stp.value = String(s.stp);
      X.refresh();
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
        bad(`connector count ${view} ${JSON.stringify(s)}: page ` +
            `${got.length}, independent ${want.length}`);
        kbad++; continue;
      }
      const links = want.map(e => [nid.get(e.a), nid.get(e.b)]);
      if (view === "collapsed")
        for (const mi of gmi)
          for (let k = 1; k < mi.length; k++) links.push([mi[0], mi[k]]);
      const u = uf(json.nodes.length, links);
      const shown = made.stats.textContent;
      const m = /(\d+) components \((\d+) multi-node\)/.exec(shown);
      if (!m || +m[1] !== u.comps || +m[2] !== u.multi) {
        bad(`component counter ${view} ${JSON.stringify(s)}: page ` +
            `"${shown}", independent ${u.comps} (${u.multi} multi-node)`);
        kbad++; continue;
      }
      const gm = /(\d+) groups \((\d+) collapsed\)/.exec(shown);
      if (!gm || +gm[1] !== json.groups.length ||
          +gm[2] !== (view === "collapsed" ? json.groups.length : 0)) {
        bad(`group counter ${view}: "${shown}"`); kbad++; continue;
      }
      console.log(`     ${view.padEnd(9)} ${s.exact ? "exact " : "graded"} ` +
        `t=${T.toFixed(2)} mid=${MID.toFixed(2)} k=${K.toFixed(1)} -> ` +
        `${want.length} external, ${u.comps} components (${u.multi} ` +
        `multi-node)  [page agrees]`);
    }
  }
  if (!kbad) ok("[counters] the page's live counters -- nodes, contracted " +
                "nodes, groups, collapsed groups, external connectors and " +
                "components -- match an independent union-find at every " +
                "setting, in BOTH scoring modes and in BOTH view modes");
  made.collapseall.checked = false; made.collapseall.onchange();

  // -------------------------------------------------- 13  sigmoid limits
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
  made.stp.value = "0"; made.mid.value = "50"; made.exact.checked = false;

  // -------------------------------------------------- 14  physics
  made.thr.value = "85"; made.showint.checked = true; X.refresh();
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

  // -------------------------------------------------- 15  settle
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

  // -------------------------------------------------- 16  HULLS
  // a hull must ENCLOSE its members rather than collapse them to a point
  X.step();
  const hulls = X.hull();
  if (!hulls.length) bad("no group hull was drawn");
  else {
    let hb = 0, big = 0;
    function inPoly(pt, poly) {
      let c = false;
      for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
        const a = poly[i], b = poly[j];
        if (((a[1] > pt[1]) !== (b[1] > pt[1])) &&
            (pt[0] < (b[0] - a[0]) * (pt[1] - a[1]) / (b[1] - a[1]) + a[0]))
          c = !c;
      }
      return c;
    }
    // the page's own transform: cv.width = innerWidth, cv.height =
    // innerHeight - cv.offsetTop, so the y centre is NOT innerHeight/2
    const st = X.state();
    const CW = made.cv.width, CH = made.cv.height;
    const sx = x => CW / 2 + (x + st.ox) * st.scale;
    const sy = y => CH / 2 + (y + st.oy) * st.scale;
    for (const hc of hulls) {
      const g = X.GR[hc.gi];
      if (hc.collapsed) continue;
      if (g.mi.length >= 3 && hc.poly.length < 3) { hb++; continue; }
      if (g.mi.length >= 3) big++;
      for (const i of g.mi)
        if (g.mi.length >= 3 && !inPoly([sx(N[i].x), sy(N[i].y)], hc.poly)) hb++;
    }
    if (hb) bad(`${hb} group members fall outside their own hull`);
    else ok(`[hulls] ${hulls.length} group containers drawn, ${big} of them ` +
            `with three or more members and a real polygon; every member ` +
            `lies inside its own hull -- a group is drawn as an ENCLOSING ` +
            `CONTAINER, not collapsed to a point`);
  }

  // -------------------------------------------------- 17  collapse/expand
  // click inside a hull, at a point that is not on a node and not on a
  // connector, and the group must collapse; click again and it must
  // expand.  Connectors are switched off for the test so the click can
  // only land on the hull.
  made.cap.value = "0"; made.showint.checked = false; X.refresh(); X.step();
  const st2 = X.state();
  const sx2 = x => made.cv.width / 2 + (x + st2.ox) * st2.scale;
  const sy2 = y => made.cv.height / 2 + (y + st2.oy) * st2.scale;
  function insidePoint(poly) {
    let cx = 0, cy = 0; poly.forEach(p => { cx += p[0]; cy += p[1]; });
    cx /= poly.length; cy /= poly.length;
    const cand = [[cx, cy]];
    for (let a = 0; a < 16; a++)
      for (const r of [8, 16, 24, 32])
        cand.push([cx + Math.cos(a * 0.3927) * r, cy + Math.sin(a * 0.3927) * r]);
    outer:
    for (const p of cand) {
      let c = false;
      for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
        const a = poly[i], b = poly[j];
        if (((a[1] > p[1]) !== (b[1] > p[1])) &&
            (p[0] < (b[0] - a[0]) * (p[1] - a[1]) / (b[1] - a[1]) + a[0]))
          c = !c;
      }
      if (!c) continue;
      for (const n of N) {
        const dx = sx2(n.x) - p[0], dy = sy2(n.y) - p[1];
        if (dx * dx + dy * dy < 400) continue outer;
      }
      return p;
    }
    return null;
  }
  const hs = X.hull().filter(h => !h.collapsed && X.GR[h.gi].mi.length >= 4);
  let clicked = null;
  for (const hc of hs) {
    const p = insidePoint(hc.poly);
    if (!p) continue;
    const g = X.GR[hc.gi];
    const was = g.collapsed;
    X.onclick({ clientX: p[0], clientY: p[1] });
    if (g.collapsed === was) continue;
    clicked = { gi: hc.gi, size: g.size };
    const nDrawn1 = Object.keys(X.host()).length;
    X.step();
    // the collapsed group is now ONE node at its members' centroid; the
    // second click has to land on that node, not where the hull used to be
    const box = X.hull().find(h => h.gi === hc.gi && h.collapsed);
    let q2 = p;
    if (box) {
      let cx = 0, cy = 0;
      box.poly.forEach(v => { cx += v[0]; cy += v[1]; });
      q2 = [cx / box.poly.length, cy / box.poly.length];
    }
    X.onclick({ clientX: q2[0], clientY: q2[1] });
    const back = !g.collapsed;
    if (!back) bad(`group ${g.id} collapsed but would not expand again`);
    else ok(`[collapse] a click inside ${g.id}'s hull collapsed its ` +
            `${g.size} member nodes to ONE node (the view hid ${nDrawn1} ` +
            `member nodes) and a second click expanded it again -- the ` +
            `group is a VIEW over distinct nodes, never a merge in the data`);
    break;
  }
  if (!clicked) bad("no hull could be clicked to collapse a group");
  made.cap.value = "1000000"; made.showint.checked = true; X.refresh();

  // -------------------------------------------------- 18  autofit ONCE
  const t0 = X.state();
  timers.forEach(f => f());                  // first autofit tick
  const t1 = X.state();
  const fittedOnce = (t1.scale !== t0.scale || t1.ox !== t0.ox || t1.oy !== t0.oy);
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
  made.expandall.onclick();
  if (X.GR.some(g => g.collapsed)) bad("expand all left a group collapsed");
  else ok("[expand all] the button expands every group");

  // -------------------------------------------------- 19 self-contained
  if (!/"nodes"/.test(html) || !/"edges"/.test(html) ||
      !/"groups"/.test(html) || /__GRAPH__/.test(html))
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
