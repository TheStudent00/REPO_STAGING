#!/usr/bin/env python3
"""make_dendrogram.py -- write dendrogram_sweep.html from clusters_final.json.

The visual for layer 3 phase 4.  It is a copy-and-adapt of the earlier
`Research/kind_signature_clustering/dendrogram_explorer.html` (and of
`make_explorer_all.py`, which adapted it for the full ecosystem), so that
the owner is looking at a familiar picture:

  - the same icicle rendering, where every node is a rectangle spanning
    its leaf range horizontally and its STABILITY BAND vertically -- the
    range of thresholds over which that cluster exists and does not move;
  - the same threshold axis on the left, the same draggable dashed
    #ff2d78 threshold line, the same live "N clusters" tag and count;
  - the same #ffd400 outline on the segments that ARE the clusters at the
    current threshold, and the same self-check that warns to the console
    if the highlighted count and the computed count ever disagree;
  - the same search box, reset button, hover card and colour legend;
  - leaf colour = language (the analogue of the earlier file's category
    colour), internal colour = gray-to-purple by language-mix entropy,
    so a wide purple block is a cross-language cluster at a glance.

Three things differ, and all three are demanded by the phase:

  1. the axis is SIMILARITY, not merge height, so it reads in the same
     direction as every threshold in the log: high at the top, and the
     picture coarsens as the line is dragged DOWN.
  2. all 229 operation signatures are leaves and every one is LABELLED
     `language.operation` -- at 229 leaves the labels fit, which they did
     not at 8,329.
  3. a second panel carries the CLUSTER-COUNT-VERSUS-THRESHOLD CURVE with
     the stability plateaus shaded, because decision 14 makes the sweep
     the deliverable rather than any single cut.

Self-contained: no CDN, no d3, no network.  The earlier explorer pulled
d3 from cdnjs, which means it does not work from disk without a network;
this one is plain SVG and hand-written scales, so `file://` is enough.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

LANG_COLOR = {
    "go": "#00ADD8", "rust": "#dea584", "cpp": "#f34b7d",
    "swift": "#F05138", "dart": "#00B4AB", "csharp": "#178600",
    "kotlin": "#A97BFF", "java": "#b07219", "typescript": "#3178c6",
    "python": "#3572A5", "ruby": "#701516", "php": "#4F5D95",
}


def build_tree(data):
    """merge history -> a nested tree with a leaf order and a band per node.

    A node's BAND is [death, birth]: `birth` is the similarity at which it
    came into existence as a cluster (its own merge similarity, or 1.0 for
    a leaf) and `death` is its super-node's birth, the similarity at which
    it stopped being a cluster in its own right.  The band's WIDTH is
    exactly how stable that cluster is under the sweep, which is the one
    number the picture is for.
    """
    keys = sorted(k for k, s in data["signatures"].items() if s["domain"])
    sigs = data["signatures"]
    node = {}
    for i, k in enumerate(keys):
        node[i] = dict(id=i, label=k,
                       language=sigs[k]["language"],
                       operation=sigs[k]["operation"],
                       domain=len(sigs[k]["domain"]),
                       route=sigs[k].get("route", ""),
                       birth=1.0, subs=[])
    for m in data["merge_history"]:
        a, b, n = m["left"]["id"], m["right"]["id"], m["node"]
        node[n] = dict(id=n, label=None, birth=m["similarity"],
                       subs=[node[a], node[b]])
    root = node[max(node)]

    order = []

    def walk(r, death):
        r["death"] = death
        if r["label"] is not None:
            r["x0"] = len(order)
            order.append(r["label"])
            r["x1"] = len(order)
            r["counts"] = {r["language"]: 1}
            r["size"] = 1
            return
        for s in r["subs"]:
            walk(s, r["birth"])
        r["x0"] = r["subs"][0]["x0"]
        r["x1"] = r["subs"][-1]["x1"]
        r["size"] = sum(s["size"] for s in r["subs"])
        c = {}
        for s in r["subs"]:
            for k, v in s["counts"].items():
                c[k] = c.get(k, 0) + v
        r["counts"] = c

    walk(root, 0.0)

    flat = []

    def flatten(r):
        flat.append(dict(id=r["id"], label=r["label"], x0=r["x0"], x1=r["x1"],
                         birth=round(r["birth"], 6),
                         death=round(r["death"], 6),
                         size=r["size"], counts=r["counts"],
                         subs=[s["id"] for s in r["subs"]],
                         language=r.get("language"),
                         operation=r.get("operation"),
                         domain=r.get("domain")))
        for s in r["subs"]:
            flatten(s)

    flatten(root)
    return dict(n_leaves=len(keys), leaf_order=order, nodes=flat,
                root_id=root["id"])


TEMPLATE = r"""<!doctype html>
<meta charset="utf-8">
<title>Operation clustering &mdash; the threshold sweep</title>
<style>
 :root { color-scheme: light dark; }
 body { font: 14px/1.5 ui-sans-serif, system-ui, sans-serif;
        margin: 0; padding: 18px 24px; }
 h1 { font-size: 18px; margin: 0 0 4px; }
 h2 { font-size: 15px; margin: 22px 0 4px; }
 .meta { opacity: .65; margin-bottom: 10px; font-size: 13px; }
 #bar { display: flex; gap: 14px; align-items: center; flex-wrap: wrap;
        margin-bottom: 8px; }
 input { font: inherit; padding: 4px 8px; border-radius: 6px;
         border: 1px solid rgba(128,128,128,.5); background: transparent;
         color: inherit; width: 220px; }
 button { font: inherit; padding: 3px 10px; border-radius: 6px;
          border: 1px solid rgba(128,128,128,.5); background: transparent;
          color: inherit; cursor: pointer; }
 .legend { display: flex; gap: 12px; font-size: 12px; align-items: center;
           flex-wrap: wrap; }
 .sw { display: inline-block; width: 11px; height: 11px; border-radius: 2px;
       margin-right: 4px; vertical-align: -1px; }
 #count { font-weight: 650; font-variant-numeric: tabular-nums; }
 #chart, #curve { position: relative; overflow-x: auto; }
 svg { display: block; user-select: none; }
 #tip { position: fixed; pointer-events: none; display: none;
        max-width: 420px; font-size: 12px; line-height: 1.4;
        background: rgba(30,30,30,.96); color: #eee; padding: 8px 10px;
        border-radius: 6px; z-index: 5; }
 #tip .hd { font-weight: 650; margin-bottom: 3px; }
 .hint { font-size: 12px; opacity: .6; margin-top: 6px; }
 table { border-collapse: collapse; font-size: 12px; margin-top: 6px; }
 th, td { border: 1px solid rgba(128,128,128,.35); padding: 2px 8px;
          text-align: left; }
 td.n { text-align: right; font-variant-numeric: tabular-nums; }
</style>
<h1>Operation clustering &mdash; the threshold sweep</h1>
<div class="meta">__NLEAVES__ operation signatures over 12 languages, on the
 shared 64-cell form space &middot; value matrix as the primary domain for
 the nine statically checked languages (2,221,643 probes), route-C
 behaviour for python, ruby and php &middot; average linkage over
 1&nbsp;&minus;&nbsp;Jaccard &middot; every horizontal line is a threshold
 slice, and there is NO chosen cut &mdash; the sweep is the result</div>
<div id="bar">
 <span>threshold <span id="thval">0.700</span> &rarr;
   <span id="count">?</span> clusters</span>
 <input id="search" placeholder="search language.operation… (Enter)">
 <button id="reset">reset view</button>
 <label style="font-size:12px;opacity:.75">width
   <input id="zoom" type="range" min="6" max="40" value="13"
          style="width:120px;vertical-align:-4px"></label>
</div>
<div id="bar2" style="margin-bottom:8px">
 <span class="legend" id="legend"></span>
 <span class="legend" style="margin-left:10px">
   <span class="sw" style="background:#8a8a8a"></span>single-language merge
   <span class="sw" style="background:#b03ad6;margin-left:10px"></span>strong
   language mix</span>
</div>
<div id="chart"><div id="tip"></div></div>
<div class="hint">Drag the dashed line DOWN for fewer clusters (lower
 similarity) or UP toward __NLEAVES__ singletons. Every rectangle is a
 cluster and its HEIGHT is its stability band &mdash; the range of
 thresholds over which it exists unchanged. <b>Tall blocks are the stable
 readings</b>; a sliver is an artefact of where the line happens to sit.
 Hover any block for its members. Yellow outline = a cluster at the
 current threshold.</div>

<h2>Cluster count against threshold &mdash; the sweep itself</h2>
<div id="curve"></div>
<div class="hint">Shaded bands are the stability plateaus: threshold ranges
 over which the clustering does not move at all. A WIDE band is a natural
 reading of the data in a way that a chosen number is not.</div>

<h2>The widest plateaus</h2>
<div id="plateaus"></div>

<script>
const TREE = __TREE__;
const SWEEP = __SWEEP__;

const LANG_COLOR = __LANGCOLOR__;
const LANGS = Object.keys(LANG_COLOR);

// ---- nodes, bands ---------------------------------------------------
const nodes = TREE.nodes;
const byId = new Map(nodes.map(r => [r.id, r]));
const leaves = nodes.filter(r => r.label !== null)
                    .sort((a, b) => a.x0 - b.x0);

function lerp(a, b, t) { return a + (b - a) * t; }
function hex(c) { return "#" + c.map(v =>
  Math.max(0, Math.min(255, Math.round(v))).toString(16)
    .padStart(2, "0")).join(""); }
const GRAY = [138, 138, 138], PURPLE = [176, 58, 214];
function entropy(counts, total) {
  let e = 0, n = 0;
  for (const k in counts) { n++; const p = counts[k] / total; e -= p * Math.log2(p); }
  return n > 1 ? e / Math.log2(LANGS.length) : 0;
}
for (const r of nodes) {
  if (r.label !== null) { r.fill = LANG_COLOR[r.language] || "#8a8a8a"; }
  else {
    const t = Math.min(1, entropy(r.counts, r.size) * 1.6);
    r.fill = hex([lerp(GRAY[0], PURPLE[0], t), lerp(GRAY[1], PURPLE[1], t),
                  lerp(GRAY[2], PURPLE[2], t)]);
  }
}
function membersOf(r, cap) {
  const out = [];
  (function g(n) {
    if (out.length > cap + 1) return;
    if (n.label !== null) { out.push(n.label); return; }
    for (const sid of n.subs) g(byId.get(sid));
  })(r);
  return out;
}

// ---- layout ---------------------------------------------------------
const M = { top: 10, right: 14, bottom: 118, left: 52 };
const H = 620;
let leafW = 13;
let W = M.left + M.right + TREE.n_leaves * leafW;
const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
document.getElementById("chart").appendChild(svg);
function SV(tag, at) {
  const e = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const k in at) e.setAttribute(k, at[k]);
  return e;
}
function xs(v) { return M.left + v * leafW; }
function ys(t) { return M.top + (1 - t) * (H - M.top - M.bottom); }
function yinv(py) { return 1 - (py - M.top) / (H - M.top - M.bottom); }

let thr = 0.70, matches = new Set();
function isCurrent(r) { return r.death < thr && thr <= r.birth; }
function clustersAt(t) {
  let c = 0;
  (function g(r) {
    if (r.birth >= t) { c++; return; }
    for (const sid of r.subs) g(byId.get(sid));
  })(byId.get(TREE.root_id));
  return c;
}
// the walk above depends on band identity; the exact count is also
// available directly from the merge history, and the two are compared
// on every move -- the same self-check the earlier explorer carried.
function clustersExact(t) {
  return TREE.n_leaves - SWEEP.merge_sims.filter(s => s >= t).length;
}

function draw() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  W = M.left + M.right + TREE.n_leaves * leafW;
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  // axis
  const gA = SV("g", {});
  for (let i = 0; i <= 10; i++) {
    const t = i / 10, py = ys(t);
    gA.appendChild(SV("line", { x1: M.left - 5, x2: W - M.right, y1: py,
      y2: py, stroke: "currentColor", "stroke-opacity": i % 5 ? .08 : .2 }));
    const tx = SV("text", { x: M.left - 9, y: py + 4, "text-anchor": "end",
      "font-size": 11, fill: "currentColor", "fill-opacity": .75 });
    tx.textContent = t.toFixed(1); gA.appendChild(tx);
  }
  const lab = SV("text", { transform: "translate(14," + (H / 2) + ") rotate(-90)",
    "text-anchor": "middle", fill: "currentColor", "font-size": 12 });
  lab.textContent = "similarity threshold"; gA.appendChild(lab);
  svg.appendChild(gA);

  // segments
  const g = SV("g", {});
  for (const r of nodes) {
    const y0 = ys(r.birth), y1 = ys(r.death);
    const rect = SV("rect", {
      x: xs(r.x0) + 0.25, width: Math.max(0.5, (r.x1 - r.x0) * leafW - 0.5),
      y: y0, height: Math.max(1, y1 - y0), fill: r.fill,
      "fill-opacity": r.birth < thr ? 0.3 : (isCurrent(r) ? 1 : 0.85),
      stroke: matches.has(r.id) ? "#ff2d78" : (isCurrent(r) ? "#ffd400" : "none"),
      "stroke-width": matches.has(r.id) ? 1.5 : (isCurrent(r) ? 1.25 : 0) });
    rect.__d = r;
    g.appendChild(rect);
  }
  svg.appendChild(g);

  // leaf labels
  if (leafW >= 8) {
    const gl = SV("g", {});
    for (const l of leaves) {
      const t = SV("text", {
        transform: "translate(" + (xs(l.x0) + leafW / 2 + 4) + ","
                   + (H - M.bottom + 6) + ") rotate(90)",
        "font-size": Math.min(11, leafW - 2), fill: "currentColor",
        "fill-opacity": matches.has(l.id) ? 1 : .8,
        "font-weight": matches.has(l.id) ? 700 : 400 });
      t.textContent = l.label;
      gl.appendChild(t);
    }
    svg.appendChild(gl);
  }

  // threshold line
  const py = ys(thr);
  const gt = SV("g", { style: "cursor:ns-resize" });
  gt.appendChild(SV("line", { x1: M.left, x2: W - M.right, y1: py, y2: py,
    stroke: "#ff2d78", "stroke-width": 1.5, "stroke-dasharray": "6 4" }));
  const tag = SV("text", { x: W - M.right - 4, y: py - 5,
    "text-anchor": "end", "font-size": 12, fill: "#ff2d78",
    "font-weight": 650 });
  tag.textContent = clustersAt(thr) + " clusters";
  gt.appendChild(tag);
  svg.appendChild(gt);
}

function setThr(t) {
  thr = Math.max(0, Math.min(1, t));
  const c = clustersAt(thr), e = clustersExact(thr);
  if (c !== e) console.warn("cluster count mismatch at t=" + thr
    + ": walk says " + c + ", merge history says " + e);
  document.getElementById("thval").textContent = thr.toFixed(3);
  document.getElementById("count").textContent = e;
  draw(); drawCurve();
}

// ---- drag on the threshold line -------------------------------------
let dragging = false;
svg.addEventListener("mousedown", ev => {
  const r = svg.getBoundingClientRect();
  if (Math.abs(ev.clientY - r.top - ys(thr)) < 12) { dragging = true; ev.preventDefault(); }
});
window.addEventListener("mousemove", ev => {
  if (!dragging) return;
  const r = svg.getBoundingClientRect();
  setThr(yinv(ev.clientY - r.top));
});
window.addEventListener("mouseup", () => { dragging = false; });
svg.addEventListener("click", ev => {
  const r = svg.getBoundingClientRect();
  if (ev.shiftKey) setThr(yinv(ev.clientY - r.top));
});

// ---- hover -----------------------------------------------------------
const tip = document.getElementById("tip");
svg.addEventListener("mousemove", ev => {
  const r = ev.target.__d;
  if (!r) { tip.style.display = "none"; return; }
  const CAP = 24;
  const mem = membersOf(r, CAP);
  const shown = mem.slice(0, CAP).join(", ")
    + (mem.length > CAP ? " … (" + r.size + " signatures total)" : "");
  const mix = Object.keys(r.counts).sort((a, b) => r.counts[b] - r.counts[a])
    .map(k => k + " " + r.counts[k]).join(" · ");
  tip.style.display = "block";
  tip.innerHTML = "<div class='hd'>"
    + (r.label !== null
       ? r.label + " — domain " + r.domain + " of 64 cells"
       : r.size + " signatures over " + Object.keys(r.counts).length
         + " languages")
    + "</div>" + mix + "<br>exists as a cluster for thresholds ("
    + r.death.toFixed(3) + ", " + r.birth.toFixed(3)
    + "] — stability band " + (r.birth - r.death).toFixed(3)
    + "<br>" + shown;
  tip.style.left = Math.min(ev.clientX + 14, innerWidth - 440) + "px";
  tip.style.top = (ev.clientY + 12) + "px";
});
svg.addEventListener("mouseleave", () => { tip.style.display = "none"; });

// ---- search ----------------------------------------------------------
document.getElementById("search").addEventListener("keydown", ev => {
  if (ev.key !== "Enter") return;
  const q = ev.target.value.trim().toLowerCase();
  matches = new Set();
  if (!q) { draw(); return; }
  const hit = leaves.filter(l => l.label.toLowerCase().includes(q));
  hit.forEach(l => matches.add(l.id));
  draw();
  if (hit.length) document.getElementById("chart").scrollLeft =
    Math.max(0, xs(hit[0].x0) - 300);
});
document.getElementById("reset").addEventListener("click", () => {
  matches = new Set(); document.getElementById("search").value = "";
  leafW = 13; setThr(0.70); document.getElementById("chart").scrollLeft = 0;
  document.getElementById("zoom").value = 13;
});
document.getElementById("zoom").addEventListener("input", ev => {
  leafW = +ev.target.value; draw();
});

// ---- the curve -------------------------------------------------------
const CW = 900, CH = 260, CM = { top: 10, right: 14, bottom: 34, left: 52 };
const csvg = SV("svg", { width: CW, height: CH });
document.getElementById("curve").appendChild(csvg);
const maxc = Math.max.apply(null, SWEEP.curve.map(p => p.clusters));
function cx(t) { return CM.left + t * (CW - CM.left - CM.right); }
function cy(n) { return CH - CM.bottom - (n / maxc) * (CH - CM.top - CM.bottom); }
function drawCurve() {
  while (csvg.firstChild) csvg.removeChild(csvg.firstChild);
  for (const p of SWEEP.plateaus) {
    if (p.degenerate || p.width < 0.012) continue;
    csvg.appendChild(SV("rect", { x: cx(p.low), y: CM.top,
      width: Math.max(1, cx(p.high) - cx(p.low)),
      height: CH - CM.top - CM.bottom, fill: "#ffd400", "fill-opacity": .18 }));
  }
  for (let i = 0; i <= 10; i++) {
    const t = i / 10;
    csvg.appendChild(SV("line", { x1: cx(t), x2: cx(t), y1: CM.top,
      y2: CH - CM.bottom, stroke: "currentColor", "stroke-opacity": .08 }));
    const tx = SV("text", { x: cx(t), y: CH - CM.bottom + 15,
      "text-anchor": "middle", "font-size": 11, fill: "currentColor",
      "fill-opacity": .75 });
    tx.textContent = t.toFixed(1); csvg.appendChild(tx);
  }
  for (const n of [0, 50, 100, 150, 200, maxc]) {
    if (n > maxc) continue;
    csvg.appendChild(SV("line", { x1: CM.left, x2: CW - CM.right, y1: cy(n),
      y2: cy(n), stroke: "currentColor", "stroke-opacity": .12 }));
    const tx = SV("text", { x: CM.left - 8, y: cy(n) + 4, "text-anchor": "end",
      "font-size": 11, fill: "currentColor", "fill-opacity": .75 });
    tx.textContent = n; csvg.appendChild(tx);
  }
  let d = "";
  const pts = SWEEP.curve.slice().sort((a, b) => a.threshold - b.threshold);
  for (let i = 0; i < pts.length; i++) {
    d += (i ? "L" : "M") + cx(pts[i].threshold) + " " + cy(pts[i].clusters);
  }
  csvg.appendChild(SV("path", { d: d, fill: "none", stroke: "#3178c6",
    "stroke-width": 2 }));
  csvg.appendChild(SV("line", { x1: cx(thr), x2: cx(thr), y1: CM.top,
    y2: CH - CM.bottom, stroke: "#ff2d78", "stroke-width": 1.5,
    "stroke-dasharray": "6 4" }));
  const t2 = SV("text", { x: cx(thr) + 5, y: CM.top + 12, "font-size": 12,
    fill: "#ff2d78", "font-weight": 650 });
  t2.textContent = clustersExact(thr) + " at " + thr.toFixed(3);
  csvg.appendChild(t2);
  const ax = SV("text", { x: CW / 2, y: CH - 4, "text-anchor": "middle",
    "font-size": 12, fill: "currentColor" });
  ax.textContent = "similarity threshold"; csvg.appendChild(ax);
}

// ---- plateau table ---------------------------------------------------
(function () {
  const rows = SWEEP.plateaus.filter(p => !p.degenerate).slice(0, 12);
  let h = "<table><tr><th>threshold range</th><th>width</th>"
        + "<th>clusters</th></tr>";
  for (const p of rows) {
    h += "<tr><td>[" + p.low.toFixed(3) + ", " + p.high.toFixed(3)
       + ")</td><td class='n'>" + p.width.toFixed(3) + "</td><td class='n'>"
       + p.clusters + "</td></tr>";
  }
  document.getElementById("plateaus").innerHTML = h + "</table>";
})();

document.getElementById("legend").innerHTML = LANGS.map(l =>
  "<span><span class='sw' style='background:" + LANG_COLOR[l]
  + "'></span>" + l + "</span>").join("");

setThr(0.70);
</script>
"""


def main():
    data = json.load(open(os.path.join(HERE, "clusters_final.json")))
    tree = build_tree(data)
    sweep = dict(
        curve=data["cluster_count_curve"],
        plateaus=data["stability_plateaus"],
        merge_sims=sorted((m["similarity"] for m in data["merge_history"]),
                          reverse=True),
    )
    html = (TEMPLATE
            .replace("__TREE__", json.dumps(tree, separators=(",", ":")))
            .replace("__SWEEP__", json.dumps(sweep, separators=(",", ":")))
            .replace("__LANGCOLOR__", json.dumps(LANG_COLOR))
            .replace("__NLEAVES__", "{:,}".format(tree["n_leaves"])))
    out = os.path.join(HERE, "dendrogram_sweep.html")
    with open(out, "w") as f:
        f.write(html)
    print("wrote %s (%.2f MB, %d leaves, %d nodes)"
          % (out, len(html) / 1e6, tree["n_leaves"], len(tree["nodes"])))


if __name__ == "__main__":
    main()
