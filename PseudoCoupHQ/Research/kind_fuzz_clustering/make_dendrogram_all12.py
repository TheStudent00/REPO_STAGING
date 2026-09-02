#!/usr/bin/env python3
"""make_dendrogram_all12.py -- dendrogram_all12.html from
clusters_all12.json.

Same conventions as `make_dendrogram.py' (log 030) and
`make_dendrogram_answers.py' (log 031), and therefore the same
conventions as `dendrogram_explorer.html' before both: the icicle
rendering, the similarity axis high at the top, the draggable dashed
#ff2d78 threshold line, the live cluster count, the #ffd400 outline on
the clusters at the current threshold, the search box, the hover card,
the plateau table and the cluster-count-versus-threshold curve with the
plateaus shaded.  Self-contained, no CDN, opens from `file://'.

What differs from log 031's visual, and it is the pass's difference and
not a style one:

  1. the leaves are ALL TWELVE languages -- the three whose answers were
     recorded as printed text and the nine whose answers were recorded
     as bits, bridged into one canonical token space by decisions 31 to
     42.
  2. the same-spelling agreement panel could not stay a three-column
     table at twelve languages, so it becomes a twelve-by-twelve matrix
     of the mean agreement over every operation the two languages both
     spell, with the per-operation roll-up beside it.
  3. the known-fracture panel carries twelve columns and the answers in
     it are canonical tokens reached from BITS on nine of them.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_dendrogram import build_tree, TEMPLATE, LANG_COLOR      # noqa

ORDER = ["python", "ruby", "php", "go", "rust", "cpp", "java",
         "csharp", "typescript", "swift", "kotlin", "dart"]

EXTRA = r"""
<h2>Same-spelling answer agreement, language against language</h2>
<div class="hint" style="margin-top:0">Every operation the two languages
 both spell, pooled: the number is the fraction of shared INPUT CELLS on
 which the two answer sets intersect (decision 26), over every such cell.
 Green is agreement, red is disagreement. The first three rows and
 columns are the print-grain languages of log 031; the other nine are
 the bit-grain languages of log 032, and every mixed cell has crossed
 the bridge of decisions 31 to 42. A comparison with a print-grain
 language on either side is made at 14 significant digits for floats
 (decision 34).</div>
<div id="smat"></div>

<h2>Same-spelling agreement, operation by operation</h2>
<div class="hint" style="margin-top:0">Pooled over every language pair
 that spells the operation. <b>lowest</b> and <b>highest</b> name the
 pair, so an operation whose row is wide is one the languages do not
 agree about.</div>
<div id="sops"></div>

<h2>The known fractures, from the answer side, all twelve</h2>
<div class="hint" style="margin-top:0">Canonical tokens. The
 pre-canonical raws &mdash; the printed string for three languages and
 the type-plus-bits string for nine &mdash; are in
 <code>clusters_all12.json</code> under <code>answer_alphabet</code>.
 <code>raise:</code> and <code>death:</code> are answer classes here
 (decision 31).</div>
<div id="worked" style="overflow-x:auto"></div>
"""

SCRIPT = r"""
<script>
const SMAT = __SMAT__, SOPS = __SOPS__, WORKED = __WORKED__,
      ORDER = __ORDER__;
function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;");
}
(function () {
  let h = "<table><tr><th></th>";
  for (const b of ORDER) h += "<th>" + b + "</th>";
  h += "</tr>";
  for (const a of ORDER) {
    h += "<tr><th style='text-align:left'>" + a + "</th>";
    for (const b of ORDER) {
      const v = (SMAT[a] || {})[b];
      if (a === b || !v) { h += "<td class='n'>&middot;</td>"; continue; }
      const g = Math.round(v.rate * 255);
      h += "<td class='n' title='" + v.ops + " operations, " + v.cells
         + " shared cells' style='background:rgba(" + (255 - g) + ","
         + g + ",90,.30)'>" + v.rate.toFixed(3) + "</td>";
    }
    h += "</tr>";
  }
  document.getElementById("smat").innerHTML = h + "</table>";

  const ops = Object.keys(SOPS).sort(
    (x, y) => SOPS[x].rate - SOPS[y].rate);
  let s = "<table><tr><th>operation</th><th>language pairs</th>"
        + "<th>shared cells</th><th>agreement</th><th>lowest pair</th>"
        + "<th>highest pair</th></tr>";
  for (const op of ops) {
    const v = SOPS[op];
    const g = Math.round(v.rate * 255);
    s += "<tr><td><code>" + esc(op) + "</code></td><td class='n'>"
       + v.pairs + "</td><td class='n'>" + v.cells
       + "</td><td class='n' style='background:rgba(" + (255 - g) + ","
       + g + ",90,.30)'>" + v.rate.toFixed(3) + "</td><td>" + v.lowest
       + " <span class='n'>" + v.lowest_rate.toFixed(3)
       + "</span></td><td>" + v.highest + " <span class='n'>"
       + v.highest_rate.toFixed(3) + "</span></td></tr>";
  }
  document.getElementById("sops").innerHTML = s + "</table>";

  let w = "<table style='font-size:11px'><tr><th>fracture</th>"
        + "<th>operation</th><th>input cell</th>";
  for (const l of ORDER) w += "<th>" + l + "</th>";
  w += "<th>meet</th></tr>";
  for (const r of WORKED) {
    w += "<tr><td>" + esc(r.label) + "</td><td><code>"
       + esc(r.operation) + "</code></td><td><code>"
       + esc(r.input_cell) + "</code></td>";
    for (const l of ORDER) {
      const t = r.tokens[l];
      w += "<td><code>" + (t && t.length ? t.map(esc).join("<br>")
                                         : "&mdash;") + "</code></td>";
    }
    w += "<td style='background:" + (r.all_agree ? "rgba(40,200,90,.25)"
       : "rgba(230,60,60,.25)") + "'>" + (r.all_agree ? "yes" : "NO")
       + "</td></tr>";
  }
  document.getElementById("worked").innerHTML = w + "</table>";
})();
</script>
"""

META = ("""__NLEAVES__ operation signatures over ALL TWELVE languages
 &middot; distance = Jaccard on domains &times; answer-agreement rate on
 the shared input cells (decision 27) &middot; the three print-grain
 route-C languages of log 031 and the nine bit-grain execution languages
 of log 032, bridged by decisions 31 to 42 &middot; a
 <code>raise</code> and a <code>death</code> are answer classes
 (decision 31) &middot; average linkage, and there is NO chosen cut
 &mdash; the sweep is the result &middot; php's <code>and</code>,
 <code>or</code> and <code>xor</code> are VOID (decision 30) and absent;
 swift's 1,066 <code>CODEGEN_REFUSE</code> probes are excluded with
 their count (decision 40)""")

OLD_META = """__NLEAVES__ operation signatures over 12 languages, on the
 shared 64-cell form space &middot; value matrix as the primary domain for
 the nine statically checked languages (2,221,643 probes), route-C
 behaviour for python, ruby and php &middot; average linkage over
 1&nbsp;&minus;&nbsp;Jaccard &middot; every horizontal line is a threshold
 slice, and there is NO chosen cut &mdash; the sweep is the result"""


def main():
    data = json.load(open(os.path.join(HERE, "clusters_all12.json")))
    for k in set(data.get("void_signatures", {})):
        if k in data["signatures"]:
            data["signatures"][k]["domain"] = []
    tree = build_tree(data)
    assert tree["n_leaves"] == data["n_leaves"], (
        "leaf set disagrees with the clustering: %d vs %d"
        % (tree["n_leaves"], data["n_leaves"]))
    sweep = dict(
        curve=data["cluster_count_curve"],
        plateaus=data["stability_plateaus"],
        merge_sims=sorted((m["similarity"] for m in data["merge_history"]),
                          reverse=True))
    j = lambda o: json.dumps(o, separators=(",", ":"))     # noqa: E731
    html = ((TEMPLATE + EXTRA + SCRIPT)
            .replace("Operation clustering &mdash; the threshold sweep",
                     "Operation clustering &mdash; ANSWER GRAIN, "
                     "all twelve languages")
            .replace(OLD_META, META)
            .replace("__TREE__", j(tree))
            .replace("__SWEEP__", j(sweep))
            .replace("__SMAT__", j(data["spelling_matrix"]))
            .replace("__SOPS__", j(data["spelling_by_operation"]))
            .replace("__ORDER__", j(ORDER))
            .replace("__WORKED__", j(
                [dict(label=w["label"], operation=w["operation"],
                      input_cell=w["input_cell"], tokens=w["tokens"],
                      all_agree=w["all_agree"])
                 for w in data["worked_examples"]]))
            .replace("__LANGCOLOR__", j(LANG_COLOR))
            .replace("__NLEAVES__", "{:,}".format(tree["n_leaves"])))
    import re
    left = set(re.findall(r"__[A-Z][A-Z_]*__", html))
    assert not left, "unfilled placeholder: %s" % sorted(left)
    out = os.path.join(HERE, "dendrogram_all12.html")
    with open(out, "w") as f:
        f.write(html)
    print("wrote %s (%.2f MB, %d leaves, %d nodes)"
          % (out, len(html) / 1e6, tree["n_leaves"], len(tree["nodes"])))


if __name__ == "__main__":
    main()
