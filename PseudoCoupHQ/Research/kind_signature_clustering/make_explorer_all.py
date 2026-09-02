#!/usr/bin/env python3
"""make_explorer_all.py — generate dendrogram_explorer_all.html: the
dendrogram explorer adapted for the full-ecosystem tree (8,329 archetype
leaves, 31,212 kinds, 411 grammars). Copy-and-adapt of
dendrogram_explorer.html, keeping the feedback-round-1 threshold-highlight
feature; changes for scale:

  - leaves are ARCHETYPES; leaf color = dominant CATEGORY (7-color
    legend), joined segments = category-mix entropy (gray -> purple);
  - hover shows multiplicity (member kind count), category mix and a
    capped "language:kind" member list;
  - deeper culling (0.6 px) and a higher default threshold (0.6) so the
    initial view stays responsive at 10x the leaf count.

The merge tree is embedded inline from merge_tree_all.json.
Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

TEMPLATE = r"""<!doctype html>
<meta charset="utf-8">
<title>Kind clustering — full-ecosystem merge tree</title>
<style>
 :root { color-scheme: light dark; }
 body { font: 14px/1.5 ui-sans-serif, system-ui, sans-serif;
        margin: 0; padding: 18px 24px; }
 h1 { font-size: 18px; margin: 0 0 4px; }
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
 #chart { position: relative; }
 svg { display: block; user-select: none; }
 #tip { position: absolute; pointer-events: none; display: none;
        max-width: 400px; font-size: 12px; line-height: 1.4;
        background: rgba(30,30,30,.95); color: #eee; padding: 8px 10px;
        border-radius: 6px; z-index: 5; }
 #tip .hd { font-weight: 650; margin-bottom: 3px; }
 .hint { font-size: 12px; opacity: .6; margin-top: 6px; }
</style>
<h1>Kind clustering — the full-ecosystem merge tree</h1>
<div class="meta">__NKINDS__ kinds of 411 grammars, deduplicated to
 __NLEAVES__ archetype leaves &middot; multiplicity-weighted average
 linkage over weighted Jaccard &middot; every horizontal line is a
 threshold slice of the spectrum</div>
<div id="bar">
 <span>threshold <span id="thval">0.600</span> &rarr;
   <span id="count">?</span> clusters</span>
 <input id="search" placeholder="search language:kind… (Enter)">
 <button id="reset">reset view</button>
 <span class="legend" id="legend"></span>
 <span class="legend"><span class="sw" style="background:#8a8a8a"></span>single-category merge
   <span class="sw" style="background:#b03ad6;margin-left:10px"></span>strong category mix</span>
</div>
<div id="chart"><div id="tip"></div></div>
<div class="hint">Drag the dashed line up (fewer clusters) or down (toward
 __NLEAVES__ archetype singletons). Scroll to zoom horizontally, drag
 background to pan. Wide vertical runs are stable clusters. Each leaf is an
 archetype: hover for its member kinds and multiplicity.</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"></script>
<script>
const TREE = __TREE__;

const CAT_COLOR = { "general-purpose":"#3572A5", "config":"#e6a23c",
                    "dsl":"#2fa86e", "notation":"#9467bd",
                    "markup":"#d64545", "query":"#17a2b8",
                    "other":"#8a8a8a" };
const CATS = Object.keys(CAT_COLOR);

// ---- flatten the merge tree ---------------------------------------------
// Each record: {x0,x1} leaf-index span, birth (own merge height), death
// (merge height of its super-node; 1.0 for the tree top), size (archetype
// leaves), mult (kind count), category counts, sub-node refs.
const nodes = [];
const leaves = [];
let nextX = 0;
function walk(nd, sup) {
  const rec = { birth: nd.h, size: nd.size, sup: sup, subs: [],
                counts: {}, mult: 0, node_id: nodes.length };
  nodes.push(rec);
  if (nd.label) {
    rec.label = nd.label;
    rec.mem = nd.mem;
    rec.mult = nd.mult;
    for (const c in nd.cats) rec.counts[c] = nd.cats[c];
    rec.x0 = nextX; rec.x1 = ++nextX;
    leaves.push(rec);
  } else {
    for (const s of nd.subs) {
      const sr = walk(s, rec);
      rec.subs.push(sr);
      rec.mult += sr.mult;
      for (const k in sr.counts) rec.counts[k] = (rec.counts[k]||0) + sr.counts[k];
    }
    rec.x0 = rec.subs[0].x0;
    rec.x1 = rec.subs[rec.subs.length-1].x1;
  }
  return rec;
}
const root = walk(TREE.root, null);
for (const r of nodes) r.death = r.sup ? r.sup.birth : 1.0;

function entropy(counts, total) {
  let e = 0;
  for (const k in counts) { const p = counts[k]/total; e -= p*Math.log2(p); }
  return e / Math.log2(CATS.length);   // 0..1
}
const entScale = d3.interpolateLab("#8a8a8a", "#b03ad6");
function domCat(counts) {
  let best = "other", bv = -1;
  for (const k in counts) if (counts[k] > bv) { bv = counts[k]; best = k; }
  return best;
}
for (const r of nodes)
  r.fill = r.label ? CAT_COLOR[domCat(r.counts)] || "#8a8a8a"
                   : entScale(entropy(r.counts, r.mult));

function membersOf(rec, cap) {   // capped "language:kind" labels of sub-tree
  const out = [];
  (function g(r){
    if (out.length > cap) return;
    if (r.label) out.push.apply(out, r.mem);
    else r.subs.forEach(g);
  })(rec);
  return out;
}

// ---- layout --------------------------------------------------------------
const W = Math.max(900, innerWidth - 60), H = 560,
      M = { top: 8, right: 10, bottom: 24, left: 46 };
const x = d3.scaleLinear([0, TREE.n_leaves], [M.left, W - M.right]);
const y = d3.scaleLinear([1, 0], [M.top, H - M.bottom]);
let zx = x;

const svg = d3.select("#chart").append("svg").attr("width", W).attr("height", H);
svg.append("clipPath").attr("id","clip").append("rect")
   .attr("x",M.left).attr("y",0).attr("width",W-M.left-M.right).attr("height",H);
const gAxis = svg.append("g").attr("transform",`translate(${M.left-6},0)`)
   .call(d3.axisLeft(y).ticks(10));
svg.append("text").attr("transform",`translate(14,${H/2}) rotate(-90)`)
   .attr("text-anchor","middle").attr("fill","currentColor")
   .attr("font-size",12).text("merge height (threshold)");
const gMain = svg.append("g").attr("clip-path","url(#clip)");
const gRects = gMain.append("g");

let matches = new Set();
// a segment is a current cluster iff it is maximal below the threshold
function isCurrentCluster(r) { return r.birth <= thr && thr < r.death; }
function draw() {
  const [d0, d1] = zx.domain();
  // deeper culling than the 800-leaf explorer: 0.6 px minimum
  const vis = nodes.filter(r => r.x1 > d0 && r.x0 < d1 &&
                                (zx(r.x1) - zx(r.x0)) >= 0.6);
  gRects.selectAll("rect").data(vis, r => r.node_id).join("rect")
    .attr("x", r => zx(r.x0) + 0.25)
    .attr("width", r => Math.max(0.5, zx(r.x1) - zx(r.x0) - 0.5))
    .attr("y", r => y(r.death))
    .attr("height", r => Math.max(1, y(r.birth) - y(r.death)))
    .attr("fill", r => r.fill)
    .attr("stroke", r => matches.has(r.node_id) ? "#ff2d78" :
                         isCurrentCluster(r) ? "#ffd400" : "none")
    .attr("stroke-width", r => matches.has(r.node_id) ? 1.5 :
                               isCurrentCluster(r) ? 1.25 : 0)
    .attr("fill-opacity", r => r.birth > thr ? 0.3 :
                               isCurrentCluster(r) ? 1 : 0.85);
}

// ---- threshold line + cluster count -------------------------------------
let thr = 0.6;
function clustersAt(t) {
  let c = 0;
  (function g(r){ if (r.birth <= t) c++; else r.subs.forEach(g); })(root);
  return c;
}
const gThr = svg.append("g").style("cursor","ns-resize");
const thrLine = gThr.append("line").attr("x1",M.left).attr("x2",W-M.right)
  .attr("stroke","#ff2d78").attr("stroke-width",1.5).attr("stroke-dasharray","6 4");
const thrHit = gThr.append("rect").attr("x",M.left).attr("width",W-M.left-M.right)
  .attr("height",14).attr("fill","transparent");
const thrTag = gThr.append("text").attr("x",W-M.right-4).attr("text-anchor","end")
  .attr("font-size",12).attr("fill","#ff2d78").attr("font-weight",650);
function setThr(t) {
  thr = Math.max(0, Math.min(1, t));
  const py = y(thr), c = clustersAt(thr);
  thrLine.attr("y1",py).attr("y2",py);
  thrHit.attr("y",py-7);
  thrTag.attr("y",py-5).text(c + " clusters");
  d3.select("#thval").text(thr.toFixed(3));
  d3.select("#count").text(c);
  let hl = 0;
  for (const r of nodes) if (isCurrentCluster(r)) hl++;
  if (hl !== c) console.warn(
    `highlight/cluster mismatch at t=${thr}: ${hl} highlighted vs ${c} clusters`);
  draw();
}
gThr.call(d3.drag().on("drag", ev => setThr(y.invert(ev.y))));
setThr(0.6);

// ---- zoom / pan (x only) ------------------------------------------------
const zoom = d3.zoom().scaleExtent([1, 2000])
  .translateExtent([[M.left,0],[W-M.right,H]]).extent([[M.left,0],[W-M.right,H]])
  .filter(ev => !ev.target.closest || !gThr.node().contains(ev.target))
  .on("zoom", ev => { zx = ev.transform.rescaleX(x); draw(); });
svg.call(zoom);
d3.select("#reset").on("click", () =>
  svg.transition().duration(0).call(zoom.transform, d3.zoomIdentity));

// ---- hover ---------------------------------------------------------------
const tip = d3.select("#tip");
gRects.on("mousemove", ev => {
  const r = ev.target.__data__;
  if (!r) { tip.style("display","none"); return; }
  const CAP = 20;
  const mem = membersOf(r, CAP);
  const shown = mem.slice(0, CAP).join(", ") +
    (r.mult > CAP ? ` … (${r.mult} kinds total)` : "");
  const mix = CATS.filter(c => r.counts[c])
    .map(c => `${c} ${r.counts[c]}`).join(" · ");
  tip.style("display","block")
     .html(`<div class="hd">${r.label ?
            "archetype " + r.label + " — multiplicity " + r.mult :
            r.mult + " kinds / " + r.size + " archetypes"}</div>` +
           `${mix}<br>merge height ${r.birth.toFixed(3)} · stability band ` +
           `[${r.birth.toFixed(3)}, ${r.death.toFixed(3)}) — width ` +
           `${(r.death - r.birth).toFixed(3)}<br>${shown}`);
  const bb = document.getElementById("chart").getBoundingClientRect();
  tip.style("left", Math.min(ev.clientX - bb.left + 14, W - 420) + "px")
     .style("top", (ev.clientY - bb.top + 12) + "px");
}).on("mouseleave", () => tip.style("display","none"));

// ---- search --------------------------------------------------------------
d3.select("#search").on("keydown", ev => {
  if (ev.key !== "Enter") return;
  const q = ev.target.value.trim().toLowerCase();
  matches = new Set();
  if (!q) { draw(); return; }
  const hit = leaves.filter(l => l.mem.some(m => m.toLowerCase().includes(q)));
  hit.forEach(l => matches.add(l.node_id));
  if (!hit.length) { draw(); return; }
  const lo = d3.min(hit, l => l.x0), hi = d3.max(hit, l => l.x1);
  let seg = hit[0];
  while (seg.sup && !(seg.x0 <= lo && seg.x1 >= hi)) seg = seg.sup;
  matches.add(seg.node_id);
  const pad = Math.max(2, (seg.x1 - seg.x0) * 0.15);
  const k = (x.range()[1]-x.range()[0]) /
            (x(Math.min(TREE.n_leaves, seg.x1+pad)) - x(Math.max(0, seg.x0-pad)));
  svg.call(zoom.transform, d3.zoomIdentity
    .scale(Math.min(2000, Math.max(1, k)))
    .translate(-x(Math.max(0, seg.x0-pad)) + x.range()[0]/Math.min(2000,Math.max(1,k)), 0));
  zx = d3.zoomTransform(svg.node()).rescaleX(x);
  draw();
});

// legend (7 categories)
d3.select("#legend").html(CATS.map(c =>
  `<span><span class="sw" style="background:${CAT_COLOR[c]}"></span>${c}</span>`).join(""));

draw();
</script>
"""


def main():
    tree = open(os.path.join(HERE, "merge_tree_all.json")).read()
    data = json.loads(tree)
    html = (TEMPLATE
            .replace("__TREE__", tree)
            .replace("__NLEAVES__", "{:,}".format(data["n_leaves"]))
            .replace("__NKINDS__", "{:,}".format(data["n_kinds"])))
    out = os.path.join(HERE, "dendrogram_explorer_all.html")
    with open(out, "w") as f:
        f.write(html)
    print("wrote %s (%.1f MB)" % (out, len(html) / 1e6))


if __name__ == "__main__":
    main()
