#!/usr/bin/env python3
"""make_dominance_lattice_vg.py -- dominance_lattice_vg.html.

The value-grain rerun of log 041's lattice picture, drawn beside it
rather than over it.  `dominance_lattice.html' stays exactly as it was
and still shows the two-order reading; this page shows the ONE order
the owner's ruling leaves standing.

What changed in the picture, and why:

  * A node is no longer a DOMAIN CLASS.  It is a VECTOR CLASS: the
    leaves whose value-grain signatures are identical element for
    element, answers included.  Two operations land in one box only when
    they answer the same thing to every question either was asked.
  * An edge is no longer coloured by agreement, because an edge that
    disagrees is no longer an edge.  Under the merged order a super-node
    REPEATS its sub-node, so every line drawn here is faithful by
    construction.  What log 041 drew red is simply absent.
  * Height is the number of ELEMENTS the leaf speaks on, out of 1,156,
    rather than the number of form pairs it accepts, out of 64.

That absence is the finding, so the page states it in numbers rather
than leaving a reader to notice that a diagram is sparse: each family
panel carries the count of nesting pairs the answers threw out.

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

import l3_dominance_vg as D                                   # noqa: E402
from make_dendrogram import LANG_COLOR                        # noqa: E402


def covers(reps, up):
    """the covering relation of the merged order over vector classes."""
    edges = []
    rs = set(reps)
    for x in reps:
        above = [y for y in up[x] if y in rs]
        for y in above:
            if any(y in up[z] for z in above if z != y):
                continue
            edges.append((x, y))
    return edges


def build_family(name, ks, ctx):
    vec, up, classes = ctx["vec"], ctx["up"], ctx["classes"]
    inf = set(ks)
    reps = sorted(r for r, m in classes.items() if r in inf)
    pos = {r: i for i, r in enumerate(reps)}
    nodes = []
    for r in reps:
        mem = [m for m in classes[r] if m in inf]
        langs = collections.Counter(m.split(".")[0] for m in mem)
        nodes.append(dict(
            i=pos[r], elements=len(vec[r]), leaves=len(mem), members=mem,
            langs=dict(langs), maximal=(not [y for y in up[r] if y in inf]),
            label=("%s%s" % (mem[0], "" if len(mem) == 1
                             else " +%d" % (len(mem) - 1)))))
    edges = [dict(lo=pos[a], hi=pos[b],
                  gained=len(vec[b]) - len(vec[a]))
             for a, b in covers(reps, up)]
    return dict(family=name, nodes=nodes, edges=edges,
                leaves=len(ks), classes=len(reps),
                maximal=[n["i"] for n in nodes if n["maximal"]])


PAGE = r"""<!doctype html>
<meta charset="utf-8">
<title>The dominance lattice at the VALUE GRAIN</title>
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
          text-align: left; vertical-align: top; }
 td.n { text-align: right; font-variant-numeric: tabular-nums; }
 code { font-size: 11.5px; }
 .sw { display: inline-block; width: 11px; height: 11px; border-radius: 2px;
       margin-right: 4px; vertical-align: -1px; }
 .legend { display: flex; gap: 12px; font-size: 12px; align-items: center;
           flex-wrap: wrap; }
</style>
<h1>The dominance lattice at the VALUE GRAIN &mdash; one order, and no
 god operator</h1>
<div class="meta">__NLEAVES__ operation signatures over all twelve
 languages &middot; an ELEMENT is one (lhs holder + value class, rhs
 holder + value class) question and its ANSWER TOKEN, and there are
 __GRID__ of them in the merged grid &middot; a leaf sits ABOVE another
 when it carries the SAME token on every element the lower one speaks on
 &middot; so every line drawn here is faithful by construction, and the
 red edges of <code>dominance_lattice.html</code> are simply absent
 &middot; a box is a VECTOR CLASS: leaves identical element for element
 &middot; height is elements spoken &middot; grain __GRAIN__, flagged
 and overturnable &middot; nothing was run for this page; it is a
 re-read of <code>signatures_valuegrain.json</code></div>

<h2>the owner's question at the new grain, and the answer</h2>
<div id="answer"></div>

<h2>Where <code>php.==</code> lands</h2>
<div id="phpeq"></div>
<div class="hint">The point of the rebuild. <code>php.==</code> speaks
 on every element in the grid, so under the old domain-only reading it
 was the top of the order and nothing could be above it. Under the
 merged order it is above NOTHING, because a leaf sits above another
 only where it repeats it.</div>

<div id="bar">
 <span>family</span>
 <span id="fams"></span>
 <input id="search" placeholder="search language.operation… (Enter)">
</div>
<div id="bar2" style="margin-bottom:8px">
 <span class="legend" id="legend"></span>
</div>
<div id="lattice"><div id="tip"></div></div>
<div class="hint">A box with no line leaving the top of it is MAXIMAL:
 nothing repeats it over a wider set of questions. If a family had a
 dominant vector there would be exactly one box at the top with a path
 down to every other. Hover any box for its members.</div>

<h2>Family by family</h2>
<div id="famtable"></div>
<div class="hint">The `nesting pairs' column counts the ordered pairs
 whose SPEAKING SETS nest, which is all the old domain reading asked
 for. The `faithful' column counts how many of those survive once the
 answers are in the element. The gap between the two columns is what
 log 041's containment order was counting and this one is not.</div>

<h2>The maximal elements set against one another</h2>
<div id="maxpairs"></div>

<h2>Union candidates &mdash; the Hub-facing short list</h2>
<div id="cands"></div>
<h2>Blocked unions, with the blocking element quoted</h2>
<div id="blocked"></div>
<div class="hint">Each row names one element on which the two maximal
 leaves carry different tokens. One such element is enough to block the
 union, so one is what is shown.</div>

<script>
const FAMS = __FAMS__, S = __SUMMARY__, LANG_COLOR = __LANGCOLOR__;
function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;");
}

(function () {
  let h = "<table><tr><th>question</th><th>answer</th></tr>";
  const rows = [
    ["Does the ONE order flatten into a dominant vector?",
     S.maximal === 1 ? "yes"
       : "NO &mdash; " + S.maximal + " maximal leaves of " + S.n_leaves
         + ", where a dominant vector leaves exactly one"],
    ["How many nesting pairs survive the answers?",
     S.faithful_edges + " of " + S.nesting_pairs + " ("
       + (100 * S.faithful_edges / S.nesting_pairs).toFixed(2)
       + " percent)"],
    ["Can containment without faithfulness still happen?",
     "no &mdash; there is one order now, so the question has no "
       + "referent"],
    ["Is the order an order?",
     "checked: " + S.transitivity_checked
       + " super-chains of length two, no transitivity failure"],
    ["Under the alternative reading, a raise read as silence?",
     S.alternative_reading.maximal + " maximal leaves and "
       + S.alternative_reading.faithful_edges + " faithful edges"],
  ];
  for (const [q, a] of rows) h += "<tr><td>" + q + "</td><td>" + a
    + "</td></tr>";
  document.getElementById("answer").innerHTML = h + "</table>";
})();

(function () {
  const p = S.php_eq;
  let h = "<table><tr><th>quantity</th><th>value</th></tr>"
    + "<tr><td>elements <code>php.==</code> speaks on</td>"
    + "<td class='n'>" + p.elements_spoken + " of " + S.n_cells
    + "</td></tr>"
    + "<tr><td>leaves whose questions all sit inside its own</td>"
    + "<td class='n'>" + p.nests_inside_it + "</td></tr>"
    + "<tr><td>of those, the ones it CONTRADICTS somewhere</td>"
    + "<td class='n'>" + p.contradicted_sub_nodes + "</td></tr>"
    + "<tr><td>leaves it therefore sits above</td><td class='n'>"
    + p.sits_above + "</td></tr></table>";
  h += "<table><tr><th>denied by</th><th>element</th>"
     + "<th>that leaf answers</th><th><code>php.==</code> answers</th>"
     + "</tr>";
  for (const d of p.denying_elements.slice(0, 14)) {
    h += "<tr><td><code>" + esc(d.leaf) + "</code></td><td><code>"
       + esc(d.element) + "</code></td><td><code>"
       + esc(d.left.join(", ")) + "</code></td><td><code>"
       + esc(d.right.join(", ")) + "</code></td></tr>";
  }
  document.getElementById("phpeq").innerHTML = h + "</table>";
})();

(function () {
  let h = "<table><tr><th>family</th><th>leaves</th><th>vector classes</th>"
        + "<th>nesting pairs</th><th>faithful</th><th>maximal</th>"
        + "<th>a dominant vector?</th><th>union candidates</th></tr>";
  for (const f of S.families) {
    h += "<tr><td>" + f.family + "</td><td class='n'>" + f.leaves
       + "</td><td class='n'>" + (FAMS[f.family]
            ? FAMS[f.family].classes : 0)
       + "</td><td class='n'>" + f.nesting_pairs + "</td><td class='n'>"
       + f.faithful_edges + "</td><td class='n'>" + f.maximal
       + "</td><td style='background:"
       + (f.maximal === 1 ? "rgba(40,200,90,.25)" : "rgba(230,60,60,.25)")
       + "'>" + (f.maximal === 1 ? "yes" : "NO") + "</td><td class='n'>"
       + (f.verdicts["union candidate"] || 0) + "</td></tr>";
  }
  document.getElementById("famtable").innerHTML = h + "</table>";
})();

(function () {
  const a = S.maximal_pair_verdicts, b = S.maximal_pair_verdicts_within_family;
  let h = "<table><tr><th>verdict</th><th>all pairs</th>"
        + "<th>within one family</th></tr>";
  for (const v of ["union candidate", "partial", "fork", "disjoint"]) {
    h += "<tr><td>" + v + "</td><td class='n'>" + (a[v] || 0)
       + "</td><td class='n'>" + (b[v] || 0) + "</td></tr>";
  }
  document.getElementById("maxpairs").innerHTML = h + "</table>";
})();

(function () {
  let h = "<table><tr><th>left</th><th>right</th><th>family</th>"
        + "<th>shared elements</th><th>union elements</th><th></th></tr>";
  for (const r of S.union_candidates_within_family) {
    h += "<tr><td><code>" + esc(r.left) + "</code></td><td><code>"
       + esc(r.right) + "</code></td><td>" + r.family
       + "</td><td class='n'>" + r.shared_elements + "</td><td class='n'>"
       + r.union_elements + "</td><td>"
       + (r.same_language ? "same language" : "&mdash;") + "</td></tr>";
  }
  document.getElementById("cands").innerHTML = h + "</table>";
  let g = "<table><tr><th>left</th><th>right</th><th>family</th>"
        + "<th>verdict</th><th>blocking element</th><th>left answers</th>"
        + "<th>right answers</th></tr>";
  for (const r of S.blocked_shown) {
    const b = r.blocked_by[0] || { element: "", left: [], right: [] };
    g += "<tr><td><code>" + esc(r.left) + "</code></td><td><code>"
       + esc(r.right) + "</code></td><td>" + r.family + "</td><td>"
       + r.verdict + "</td><td><code>" + esc(b.element)
       + "</code></td><td><code>" + esc(b.left.join(", "))
       + "</code></td><td><code>" + esc(b.right.join(", "))
       + "</code></td></tr>";
  }
  document.getElementById("blocked").innerHTML = g + "</table>";
})();

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
let current = S.families[0].family, matches = new Set();

function draw() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  const F = FAMS[current];
  const M = { top: 26, right: 20, bottom: 30, left: 92 };
  const levels = {};
  for (const nd of F.nodes)
    (levels[nd.elements] = levels[nd.elements] || []).push(nd);
  const counts = Object.keys(levels).map(Number).sort((a, b) => a - b);
  const rowH = 74, boxH = 26, colW = 186;
  const widest = Math.max.apply(null, counts.map(c => levels[c].length));
  const W = M.left + M.right + Math.max(3, widest) * colW;
  const H = M.top + M.bottom + counts.length * rowH;
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  const at = {};
  counts.forEach((c, li) => {
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
    tx.textContent = c + " elements";
    svg.appendChild(tx);
  });
  const ge = SV("g", {});
  for (const e of F.edges) {
    const a = at[e.lo], b = at[e.hi];
    const ln = SV("line", { x1: a.cx, y1: a.y, x2: b.cx, y2: b.y + b.h,
      stroke: "rgb(40,220,90)", "stroke-width": 2.2,
      "stroke-opacity": .9 });
    ln.__e = e;
    ge.appendChild(ln);
  }
  svg.appendChild(ge);
  const gn = SV("g", {});
  for (const nd of F.nodes) {
    const p = at[nd.i];
    const hit = nd.members.some(m => matches.has(m));
    const langs = Object.keys(nd.langs);
    const fill = langs.length === 1
      ? (LANG_COLOR[langs[0]] || "#8a8a8a") : "#b03ad6";
    const r = SV("rect", { x: p.x, y: p.y, width: p.w, height: p.h,
      rx: 5, fill: fill, "fill-opacity": hit ? 1 : .82,
      stroke: hit ? "#ff2d78" : (nd.maximal ? "#ffd400" : "none"),
      "stroke-width": hit ? 2 : (nd.maximal ? 1.8 : 0) });
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
  hd.textContent = current + " — " + F.leaves + " leaves, " + F.classes
    + " vector classes, " + F.maximal.length + " maximal, "
    + F.edges.length + " covering edges";
  svg.appendChild(hd);
}

svg.addEventListener("mousemove", ev => {
  const nd = ev.target.__n, e = ev.target.__e;
  if (!nd && !e) { tip.style.display = "none"; return; }
  tip.style.display = "block";
  if (nd) {
    tip.innerHTML = "<div class='hd'>" + nd.elements + " elements, "
      + nd.leaves + " leaf" + (nd.leaves === 1 ? "" : "s") + "</div>"
      + esc(nd.members.join(", "));
  } else {
    tip.innerHTML = "<div class='hd'>covering edge, +" + e.gained
      + " elements</div>the higher leaf repeats the lower one on every "
      + "element the lower one speaks on";
  }
  tip.style.left = Math.min(ev.clientX + 14, innerWidth - 480) + "px";
  tip.style.top = (ev.clientY + 12) + "px";
});
svg.addEventListener("mouseleave", () => { tip.style.display = "none"; });

document.getElementById("fams").innerHTML = S.families
  .map(f => "<button data-f='" + f.family + "'>" + f.family + " ("
       + f.leaves + ")</button>").join(" ");
document.getElementById("legend").innerHTML =
  "<span><span class='sw' style='background:rgb(40,220,90)'></span>"
  + "edge: the higher leaf repeats the lower one exactly</span>"
  + "<span><span class='sw' style='background:#b03ad6'></span>"
  + "vector class spanning languages</span>"
  + "<span style='border:2px solid #ffd400;padding:0 5px;border-radius:3px'>"
  + "maximal</span>";

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
    for (const f of S.families) {
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
    rep = ctx["report"]
    byfam = collections.defaultdict(list)
    for k in ctx["keys"]:
        byfam[ctx["fam"][k]].append(k)
    fams = {}
    for f in D.FAMILIES:
        if f in byfam:
            fams[f] = build_family(f, sorted(byfam[f]), ctx)

    # The page carries a SUMMARY and not the whole report: the blocked
    # list runs to thousands of rows and the panel shows sixty.  Nothing
    # shown in the page is computed anywhere but in l3_dominance_vg.py.
    blocked = sorted((r for r in ctx["all_verdicts"]
                      if r["same_family"] and r["blocked_by"]),
                     key=lambda r: (r["same_language"],
                                    -r["shared_elements"]))[:60]
    slim = {k: v for k, v in rep.items()
            if k not in ("blocked_within_family", "family_union_verdicts",
                         "maximal_leaves", "identical_vector_members")}
    slim["blocked_shown"] = blocked
    slim["union_candidates_within_family"] = \
        rep["union_candidates_within_family"][:60]
    for f in slim["families"]:
        f.pop("maximal_leaves", None)
    j = lambda o: json.dumps(o, separators=(",", ":"))         # noqa: E731
    html = (PAGE
            .replace("__FAMS__", j(fams))
            .replace("__SUMMARY__", j(slim))
            .replace("__LANGCOLOR__", j(LANG_COLOR))
            .replace("__NLEAVES__", "{:,}".format(rep["n_leaves"]))
            .replace("__GRAIN__", rep["grain"])
            .replace("__GRID__", "{:,}".format(rep["n_cells"])))
    left = set(re.findall(r"__[A-Z][A-Z_]*__", html))
    assert not left, "unfilled placeholder: %s" % sorted(left)
    out = os.path.join(HERE, "dominance_lattice_vg.html")
    with open(out, "w") as fh:
        fh.write(html)
    print("")
    print("wrote %s (%.2f MB, %d families, %d vector classes drawn)"
          % (out, len(html) / 1e6, len(fams),
             sum(len(v["nodes"]) for v in fams.values())))


if __name__ == "__main__":
    main()
