#!/usr/bin/env python3
"""make_dominance_lattice.py -- dominance_lattice.html.

the owner's dominance paradigm as its own visual, beside the three dendrograms
rather than inside one of them, because it is not a tree and drawing it
as one would be a lie about its shape.

The picture is a HASSE DIAGRAM per operator family.  Every node is a
DOMAIN CLASS -- one set of accepted cells, and the leaves that carry it.
A node sits above another when its domain CONTAINS the other's.  Only
the covering edges are drawn: if X is inside Y and inside Z and Z is
inside Y, the X-to-Y edge follows from the other two and is left out.
Height is the number of cells accepted, so the picture reads bottom to
top as narrow to wide.

Every edge is COLOURED BY AGREEMENT: green where every leaf pair across
the edge answers identically on all the cells they share, red where
none does.  A green chain from bottom to top is dominance in the CORE's
sense.  A red edge is a wider domain that does NOT dominate what it
contains, because it answers differently inside it.

Per family and not all at once: 238 leaves over 59 domain classes in one
lattice is a picture nobody can read, and the families are the division
the node already uses (log 040 decision 9).  Decision 57 records the
choice.  The overall lattice is not lost -- its one top and its shape
are stated in the summary panel above the diagrams, and its full edge
list is in `dominance_lattice.json'.

Self-contained: no CDN, no d3, plain SVG built in the page.  Opens from
`file://'.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_alt_readings as R                                  # noqa: E402
import l3_dominance as D                                     # noqa: E402
from make_dendrogram import LANG_COLOR                       # noqa: E402


def edge_agreement(members_x, members_y, A, SH, idx):
    """how the leaves below an edge answer against the leaves above it.

    Every pair (x, y) with x in the lower class and y in the upper one
    is scored, and only the SUPPORTED pairs count, under decision 55.
    Returned as the mean rate and the fraction of pairs that never
    disagree at all, so a green edge means something exact.
    """
    rates, clean = [], 0
    for x in members_x:
        for y in members_y:
            i, j = idx[x], idx[y]
            if SH[i][j] < R.SUPPORT:
                continue
            rates.append(float(A[i][j]))
            if A[i][j] >= D.CLEAN:
                clean += 1
    if not rates:
        return None, None, 0
    return (round(sum(rates) / len(rates), 4),
            round(clean / len(rates), 4), len(rates))


def build_family(name, ks, dom, A, SH, idx, keys):
    cls = D.classes(keys, dom, ks)
    nodes = sorted(cls, key=lambda d: (len(d), sorted(d)))
    pos = {d: i for i, d in enumerate(nodes)}
    out_nodes = []
    for d in nodes:
        mem = cls[d]
        langs = collections.Counter(k.split(".")[0] for k in mem)
        out_nodes.append(dict(
            i=pos[d], cells=len(d), leaves=len(mem), members=mem,
            langs=dict(langs),
            label=("%s%s" % (mem[0], "" if len(mem) == 1
                             else " +%d" % (len(mem) - 1)))))
    edges = []
    for x, y in D.hasse(nodes):
        mean, clean, npairs = edge_agreement(cls[x], cls[y], A, SH, idx)
        edges.append(dict(lo=pos[x], hi=pos[y], mean=mean, clean=clean,
                          pairs=npairs, gained=len(y) - len(x)))
    mx = [pos[d] for d in D.maximal(nodes)]
    mn = [pos[d] for d in nodes
          if not any(o < d for o in nodes)]
    return dict(family=name, nodes=out_nodes, edges=edges,
                maximal=mx, minimal=mn,
                union_cells=len(set().union(*nodes)) if nodes else 0,
                leaves=len(ks))


PAGE = r"""<!doctype html>
<meta charset="utf-8">
<title>The dominance lattice &mdash; does the tree flatten?</title>
<style>
 :root { color-scheme: light dark; }
 body { font: 14px/1.5 ui-sans-serif, system-ui, sans-serif;
        margin: 0; padding: 18px 24px; }
 h1 { font-size: 18px; margin: 0 0 4px; }
 h2 { font-size: 15px; margin: 22px 0 4px; }
 .meta { opacity: .65; margin-bottom: 10px; font-size: 13px; }
 .hint { font-size: 12px; opacity: .6; margin-top: 6px; }
 #bar { display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
        margin-bottom: 8px; }
 button { font: inherit; padding: 3px 10px; border-radius: 6px;
          border: 1px solid rgba(128,128,128,.5); background: transparent;
          color: inherit; cursor: pointer; }
 button.on { border-color: #ff2d78; color: #ff2d78; font-weight: 650; }
 input { font: inherit; padding: 4px 8px; border-radius: 6px;
         border: 1px solid rgba(128,128,128,.5); background: transparent;
         color: inherit; width: 220px; }
 #lattice { position: relative; overflow-x: auto; }
 svg { display: block; user-select: none; }
 #tip { position: fixed; pointer-events: none; display: none;
        max-width: 460px; font-size: 12px; line-height: 1.4;
        background: rgba(30,30,30,.96); color: #eee; padding: 8px 10px;
        border-radius: 6px; z-index: 5; }
 #tip .hd { font-weight: 650; margin-bottom: 3px; }
 table { border-collapse: collapse; font-size: 12px; margin-top: 6px; }
 th, td { border: 1px solid rgba(128,128,128,.35); padding: 2px 8px;
          text-align: left; }
 td.n { text-align: right; font-variant-numeric: tabular-nums; }
 .sw { display: inline-block; width: 11px; height: 11px; border-radius: 2px;
       margin-right: 4px; vertical-align: -1px; }
 .legend { display: flex; gap: 12px; font-size: 12px; align-items: center;
           flex-wrap: wrap; }
</style>
<h1>The dominance lattice &mdash; does the tree flatten into a dominant
 vector?</h1>
<div class="meta">__NLEAVES__ operation signatures over all twelve
 languages, grouped into __NCLASSES__ DOMAIN CLASSES &middot; a class
 sits ABOVE another when it accepts every cell the other accepts
 &middot; only the COVERING edges are drawn, so an edge that follows
 from two others is left out &mdash; that is what makes this a Hasse
 diagram rather than a mess &middot; height is the number of cells
 accepted, out of __GRID__ &middot; <b>edge colour is answer
 agreement</b>: green where every supported leaf pair across the edge
 answers identically on every cell they share, red where none does
 &middot; drawn PER FAMILY under decision 57, because one lattice over
 __NCLASSES__ classes is unreadable &middot; nothing here was run; it is
 a re-read of <code>clusters_all12.json</code></div>

<h2>the owner's question, and the answer</h2>
<div id="answer"></div>

<div id="bar">
 <span>family</span>
 <span id="fams"></span>
 <input id="search" placeholder="search language.operation… (Enter)">
</div>
<div id="bar2" style="margin-bottom:8px">
 <span class="legend" id="legend"></span>
</div>
<div id="lattice"><div id="tip"></div></div>
<div class="hint">Every box is a set of accepted cells and the
 operations that accept exactly that set. A box with no line leaving the
 top of it is a MAXIMAL element: no wider domain contains it. If a
 family had a dominant vector there would be exactly one box at the top
 with a green path down to everything. Hover any box for its members and
 any line for the agreement across it.</div>

<h2>Family by family</h2>
<div id="famtable"></div>
<div class="hint">A family FLATTENS when its containment order has one
 top. It flattens in the sense the owner asked about &mdash; a dominant vector
 &mdash; only when that top also never disagrees with what sits under
 it, which is the last column.</div>

<h2>The maximal elements set against one another</h2>
<div id="maxpairs"></div>
<div class="hint">Two maximal elements cannot contain one another, so
 the only question left is whether their answers can be put together.
 Counted within ONE family, because a comparison set against an
 arithmetic disagreeing is not a finding about either.</div>

<h2>Union candidates and forks</h2>
<div id="cands"></div>
<div id="forks"></div>

<script>
const FAMS = __FAMS__, SUMMARY = __SUMMARY__, LANG_COLOR = __LANGCOLOR__;
function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;");
}
function pct(v) { return v === null ? "&mdash;" : v.toFixed(3); }

// ---- the answer panel ------------------------------------------------
(function () {
  const s = SUMMARY;
  let h = "<table><tr><th>question</th><th>answer</th></tr>";
  const rows = [
    ["Does the CONTAINMENT order flatten, overall?",
     s.containment_maximal === 1
       ? "YES &mdash; one top, a class of " + s.containment_top_cells
         + " cells carrying " + s.containment_top_members.length
         + " leaves"
       : "no &mdash; " + s.containment_maximal + " maximal classes"],
    ["Does the DOMINANCE order flatten, overall?",
     s.dominance_maximal === 1 ? "yes"
       : "NO &mdash; " + s.dominance_maximal
         + " maximal leaves, where a dominant vector leaves exactly one"],
    ["How many containments survive the answers?",
     s.dominance_edges + " of " + s.containment_ordered_pairs
       + " supported strict containments never disagree once"],
    ["What would the UNION vector look like?",
     s.union_vector_cells + " of " + s.grid_cells
       + " cells &mdash; the whole grid, and "
       + s.union_carried_by_one_leaf.length
       + " single leaves already carry it"],
  ];
  for (const [q, a] of rows) h += "<tr><td>" + q + "</td><td>" + a
    + "</td></tr>";
  document.getElementById("answer").innerHTML = h + "</table>";
})();

// ---- the family table -------------------------------------------------
(function () {
  let h = "<table><tr><th>family</th><th>leaves</th><th>domain classes</th>"
        + "<th>maximal classes</th><th>a single top?</th>"
        + "<th>union cells</th><th>maximal leaves under dominance</th>"
        + "<th>a dominant vector?</th></tr>";
  for (const f of SUMMARY.families) {
    h += "<tr><td>" + f.family + "</td><td class='n'>" + f.leaves
       + "</td><td class='n'>" + f.classes + "</td><td class='n'>"
       + f.containment_maximal + "</td><td>"
       + (f.containment_maximal === 1
          ? "yes, " + f.containment_top_cells + " cells" : "no")
       + "</td><td class='n'>" + f.union_cells + "</td><td class='n'>"
       + f.dominance_maximal + "</td><td style='background:"
       + (f.dominance_maximal === 1 ? "rgba(40,200,90,.25)"
                                    : "rgba(230,60,60,.25)") + "'>"
       + (f.dominance_maximal === 1 ? "yes" : "NO") + "</td></tr>";
  }
  document.getElementById("famtable").innerHTML = h + "</table>";
})();

// ---- the maximal-pair verdicts ---------------------------------------
(function () {
  const a = SUMMARY.maximal_pair_verdicts,
        b = SUMMARY.maximal_pair_verdicts_within_family;
  let h = "<table><tr><th>verdict</th><th>all pairs</th>"
        + "<th>within one family</th></tr>";
  for (const v of ["union candidate", "partial", "fork", "thin",
                   "disjoint"]) {
    h += "<tr><td>" + v + "</td><td class='n'>" + (a[v] || 0)
       + "</td><td class='n'>" + (b[v] || 0) + "</td></tr>";
  }
  document.getElementById("maxpairs").innerHTML = h + "</table>";
})();

(function () {
  function tbl(title, rows, cols) {
    let h = "<h3 style='font-size:13px;margin:14px 0 2px'>" + title
          + "</h3><table><tr>";
    for (const c of cols) h += "<th>" + c + "</th>";
    h += "</tr>";
    for (const r of rows) {
      h += "<tr><td><code>" + esc(r.left) + "</code></td><td><code>"
         + esc(r.right) + "</code></td><td>" + r.family
         + "</td><td class='n'>" + r.shared_cells + "</td><td class='n'>"
         + r.shared_inputs + "</td><td class='n'>"
         + r.agreement.toFixed(3) + "</td><td>"
         + (r.same_language ? "same language" : "&mdash;")
         + "</td></tr>";
    }
    return h + "</table>";
  }
  const cols = ["left", "right", "family", "shared cells",
                "shared input cells", "agreement", ""];
  document.getElementById("cands").innerHTML = tbl(
    "Union candidates &mdash; maximal elements that never disagree",
    SUMMARY.union_candidates_within_family, cols);
  document.getElementById("forks").innerHTML = tbl(
    "Forks &mdash; maximal elements that disagree on every shared cell "
    + "(widest 40 shown)",
    SUMMARY.forks_within_family.slice(0, 40), cols);
})();

// ---- the lattice ------------------------------------------------------
const NS = "http://www.w3.org/2000/svg";
function SV(tag, at) {
  const e = document.createElementNS(NS, tag);
  for (const k in at) e.setAttribute(k, at[k]);
  return e;
}
const host = document.getElementById("lattice");
const svg = document.createElementNS(NS, "svg");
host.appendChild(svg);
const tip = document.getElementById("tip");
let current = SUMMARY.families[0].family, matches = new Set();

function agColor(clean) {
  if (clean === null) return "#8a8a8a";
  const g = Math.round(clean * 200) + 40, r = Math.round((1 - clean) * 210);
  return "rgb(" + r + "," + g + ",80)";
}

function draw() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  const F = FAMS[current];
  const M = { top: 26, right: 20, bottom: 30, left: 74 };
  const levels = {};
  for (const nd of F.nodes) (levels[nd.cells] = levels[nd.cells] || []).push(nd);
  const cellCounts = Object.keys(levels).map(Number).sort((a, b) => a - b);
  const rowH = 78, boxH = 26;
  const widest = Math.max.apply(null, cellCounts.map(c => levels[c].length));
  const colW = 190;
  const W = M.left + M.right + Math.max(3, widest) * colW;
  const H = M.top + M.bottom + cellCounts.length * rowH;
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  const at = {};
  cellCounts.forEach((c, li) => {
    const y = H - M.bottom - li * rowH;
    const row = levels[c];
    row.forEach((nd, xi) => {
      const x = M.left + xi * colW + (widest - row.length) * colW / 2;
      at[nd.i] = { x: x + colW / 2 - 6, y: y - boxH / 2, w: colW - 22,
                   h: boxH, cx: x + colW / 2 - 6 + (colW - 22) / 2,
                   cy: y };
    });
    const tx = SV("text", { x: M.left - 12, y: y + 4, "text-anchor": "end",
      "font-size": 11, fill: "currentColor", "fill-opacity": .7 });
    tx.textContent = c + " cells";
    svg.appendChild(tx);
  });
  const ge = SV("g", {});
  for (const e of F.edges) {
    const a = at[e.lo], b = at[e.hi];
    const ln = SV("line", { x1: a.cx, y1: a.y, x2: b.cx, y2: b.y + b.h,
      stroke: agColor(e.clean), "stroke-width": e.clean === 1 ? 2.2 : 1.4,
      "stroke-opacity": .85 });
    ln.__e = e;
    ge.appendChild(ln);
  }
  svg.appendChild(ge);
  const gn = SV("g", {});
  for (const nd of F.nodes) {
    const p = at[nd.i];
    const isMax = F.maximal.indexOf(nd.i) >= 0;
    const hit = nd.members.some(m => matches.has(m));
    const langs = Object.keys(nd.langs);
    const fill = langs.length === 1
      ? (LANG_COLOR[langs[0]] || "#8a8a8a") : "#b03ad6";
    const r = SV("rect", { x: p.x, y: p.y, width: p.w, height: p.h,
      rx: 5, fill: fill, "fill-opacity": hit ? 1 : .82,
      stroke: hit ? "#ff2d78" : (isMax ? "#ffd400" : "none"),
      "stroke-width": hit ? 2 : (isMax ? 1.8 : 0) });
    r.__n = nd;
    gn.appendChild(r);
    const t = SV("text", { x: p.cx, y: p.y + 17, "text-anchor": "middle",
      "font-size": 11, fill: "#fff", "pointer-events": "none" });
    t.textContent = nd.label.length > 26
      ? nd.label.slice(0, 25) + "…" : nd.label;
    gn.appendChild(t);
  }
  svg.appendChild(gn);
  const hd = SV("text", { x: M.left, y: 16, "font-size": 12,
    fill: "currentColor", "fill-opacity": .8 });
  hd.textContent = current + " — " + F.leaves + " leaves, "
    + F.nodes.length + " domain classes, " + F.maximal.length
    + " maximal, union " + F.union_cells + " cells";
  svg.appendChild(hd);
}

svg.addEventListener("mousemove", ev => {
  const nd = ev.target.__n, e = ev.target.__e;
  if (!nd && !e) { tip.style.display = "none"; return; }
  tip.style.display = "block";
  if (nd) {
    tip.innerHTML = "<div class='hd'>" + nd.cells + " cells, "
      + nd.leaves + " leaf" + (nd.leaves === 1 ? "" : "s") + "</div>"
      + esc(nd.members.join(", "));
  } else {
    tip.innerHTML = "<div class='hd'>covering edge, +" + e.gained
      + " cells</div>" + e.pairs + " supported leaf pairs across it"
      + "<br>mean agreement " + pct(e.mean)
      + "<br>fraction that NEVER disagree " + pct(e.clean);
  }
  tip.style.left = Math.min(ev.clientX + 14, innerWidth - 480) + "px";
  tip.style.top = (ev.clientY + 12) + "px";
});
svg.addEventListener("mouseleave", () => { tip.style.display = "none"; });

document.getElementById("fams").innerHTML = SUMMARY.families
  .map(f => "<button data-f='" + f.family + "'>" + f.family + " ("
       + f.leaves + ")</button>").join(" ");
document.getElementById("legend").innerHTML =
  "<span><span class='sw' style='background:rgb(40,240,80)'></span>"
  + "edge: never disagrees</span>"
  + "<span><span class='sw' style='background:rgb(210,40,80)'></span>"
  + "edge: always disagrees</span>"
  + "<span><span class='sw' style='background:#8a8a8a'></span>"
  + "edge: too thin to read (decision 55)</span>"
  + "<span><span class='sw' style='background:#b03ad6'></span>"
  + "class spanning languages</span>"
  + "<span style='border:2px solid #ffd400;padding:0 5px;border-radius:3px'>"
  + "maximal</span>";

for (const b of ["fams"]) {
  const host2 = document.getElementById(b);
  if (host2 && host2.querySelectorAll) {
    for (const btn of host2.querySelectorAll("button")) {
      btn.addEventListener("click", () => {
        current = btn.getAttribute("data-f"); draw();
      });
    }
  }
}
document.addEventListener("click", ev => {
  const f = ev.target && ev.target.getAttribute
    ? ev.target.getAttribute("data-f") : null;
  if (f) { current = f; draw(); }
});
document.getElementById("search").addEventListener("keydown", ev => {
  if (ev.key !== "Enter") return;
  const q = String(ev.target.value || "").trim().toLowerCase();
  matches = new Set();
  if (q) {
    for (const f of SUMMARY.families) {
      for (const nd of FAMS[f.family].nodes) {
        for (const m of nd.members) {
          if (m.toLowerCase().includes(q)) matches.add(m);
        }
      }
    }
  }
  draw();
});
draw();
</script>
"""


def main():
    ctx = D.main()
    data, keys, dom, fam = (ctx["data"], ctx["keys"], ctx["dom"],
                            ctx["fam"])
    A, SH, idx = ctx["A"], ctx["SH"], ctx["idx"]
    byfam = collections.defaultdict(list)
    for k in keys:
        byfam[fam[k]].append(k)
    fams = {}
    for f in D.FAMILIES:
        if f in byfam:
            fams[f] = build_family(f, sorted(byfam[f]), dom, A, SH, idx,
                                   keys)
    # The page carries the SUMMARY and not the whole report: the full
    # 16,836-row maximal-pair table is in `dominance_lattice.json' and
    # embedding it would triple the file for a panel that shows forty
    # rows.  Nothing shown in the page is computed anywhere but here.
    rep = ctx["report"]
    slim = {k: v for k, v in rep.items()
            if k not in ("maximal_pairs", "union_vector",
                         "dominance_maximal_leaves")}
    j = lambda o: json.dumps(o, separators=(",", ":"))         # noqa: E731
    html = (PAGE
            .replace("__FAMS__", j(fams))
            .replace("__SUMMARY__", j(slim))
            .replace("__LANGCOLOR__", j(LANG_COLOR))
            .replace("__NLEAVES__", "{:,}".format(len(keys)))
            .replace("__NCLASSES__", str(ctx["report"]["n_classes"]))
            .replace("__GRID__", str(ctx["report"]["grid_cells"])))
    left = set(re.findall(r"__[A-Z][A-Z_]*__", html))
    assert not left, "unfilled placeholder: %s" % sorted(left)
    out = os.path.join(HERE, "dominance_lattice.html")
    with open(out, "w") as fh:
        fh.write(html)
    print("")
    print("wrote %s (%.2f MB, %d families, %d classes drawn)"
          % (out, len(html) / 1e6, len(fams),
             sum(len(v["nodes"]) for v in fams.values())))


if __name__ == "__main__":
    main()
