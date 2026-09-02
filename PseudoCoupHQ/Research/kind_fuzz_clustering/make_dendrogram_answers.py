#!/usr/bin/env python3
"""make_dendrogram_answers.py -- dendrogram_answers.html from
clusters_answers.json.

Same conventions as `make_dendrogram.py` and therefore the same
conventions as `dendrogram_explorer.html` before it: the icicle
rendering, the similarity axis high at the top, the draggable dashed
#ff2d78 threshold line, the live cluster count, the #ffd400 outline on
the clusters at the current threshold, the search box, the hover card,
the plateau table and the cluster-count-versus-threshold curve with the
plateaus shaded.  Self-contained, no CDN, opens from `file://`.

What differs, and it is the phase's difference and not a style one:

  1. the distance is the ANSWER-GRAIN one -- Jaccard on domains TIMES
     the agreement rate on shared accepted input cells (decision 27) --
     so two operations sit together only if they accept the same forms
     AND compute the same values on them.
  2. the leaves are the 69 signatures of the three languages that have
     executed answers.  php's `and', `or' and `xor' are absent: they are
     VOID under decision 30.
  3. a third panel is added, which the domain-grain visual had no data
     for: the same-spelling AGREEMENT table, every operation spelled in
     two or more of the three languages, coloured by how often the two
     languages answer the same thing where both accept.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
import sys                                                    # noqa: E402
sys.path.insert(0, HERE)
from make_dendrogram import build_tree, TEMPLATE, LANG_COLOR  # noqa: E402

EXTRA = r"""
<h2>Same-spelling answer agreement</h2>
<div class="hint" style="margin-top:0">Every operation spelled in two or
 more of the three languages. The number is the fraction of INPUT CELLS
 accepted by BOTH on which the two answer sets intersect (decision 26),
 over the count of shared input cells. Green is agreement, red is
 disagreement; a blank cell means the spelling is not shared by that
 pair. This is the factor <b>A</b> of decision 27 &mdash; the thing the
 domain-grain sweep could not see.</div>
<div id="agree"></div>

<h2>The known fractures, from the answer side</h2>
<div class="hint" style="margin-top:0">The pre-canonical raw answers are
 in <code>clusters_answers.json</code> under
 <code>answer_alphabet</code>; these are the canonical tokens.</div>
<div id="worked"></div>

<script>
const AGREE = __AGREE__, WORKED = __WORKED__;
(function () {
  const pairs = ["python vs ruby", "php vs python", "php vs ruby"];
  const ops = Object.keys(AGREE).sort();
  let h = "<table><tr><th>operation</th>";
  for (const p of pairs) h += "<th>" + p + "</th>";
  h += "<th>shared cells</th></tr>";
  for (const op of ops) {
    h += "<tr><td><code>" + op.replace(/&/g, "&amp;").replace(/</g, "&lt;")
       + "</code></td>";
    let sh = 0;
    for (const p of pairs) {
      const v = AGREE[op][p];
      if (!v) { h += "<td></td>"; continue; }
      sh = Math.max(sh, v.shared_inputs);
      const g = Math.round(v.rate * 255);
      h += "<td class='n' style='background:rgba(" + (255 - g) + ","
         + g + ",90,.30)'>" + v.rate.toFixed(3) + "</td>";
    }
    h += "<td class='n'>" + sh + "</td></tr>";
  }
  document.getElementById("agree").innerHTML = h + "</table>";
  let w = "<table><tr><th>fracture</th><th>operation</th><th>input cell</th>"
        + "<th>python</th><th>ruby</th><th>php</th><th>agree</th></tr>";
  for (const r of WORKED) {
    w += "<tr><td>" + r.label + "</td><td><code>"
       + r.operation.replace(/&/g, "&amp;").replace(/</g, "&lt;")
       + "</code></td><td><code>" + r.input_cell + "</code></td>";
    for (const l of ["python", "ruby", "php"]) {
      const t = r.tokens[l];
      w += "<td><code>" + (t && t.length ? t.join("<br>") : "&mdash;")
         + "</code></td>";
    }
    w += "<td style='background:" + (r.all_agree ? "rgba(40,200,90,.25)"
       : "rgba(230,60,60,.25)") + "'>" + (r.all_agree ? "yes" : "NO")
       + "</td></tr>";
  }
  document.getElementById("worked").innerHTML = w + "</table>";
})();
</script>
"""

META = ("""__NLEAVES__ operation signatures over the THREE languages that
 have executed answers &middot; distance = Jaccard on domains &times;
 answer-agreement rate on the shared accepted input cells (decision 27)
 &middot; python 342,225 / ruby 261,382 / php 215,306 route-C probes
 &middot; average linkage, and there is NO chosen cut &mdash; the sweep
 is the result &middot; php's <code>and</code>, <code>or</code> and
 <code>xor</code> are VOID (decision 30) and absent""")


def main():
    data = json.load(open(os.path.join(HERE, "clusters_answers.json")))
    void = set(data.get("void_signatures", {}))
    for k in void:
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
                          reverse=True),
    )
    html = ((TEMPLATE + EXTRA)
            .replace("Operation clustering &mdash; the threshold sweep",
                     "Operation clustering &mdash; ANSWER GRAIN")
            .replace("""__NLEAVES__ operation signatures over 12 languages, on the
 shared 64-cell form space &middot; value matrix as the primary domain for
 the nine statically checked languages (2,221,643 probes), route-C
 behaviour for python, ruby and php &middot; average linkage over
 1&nbsp;&minus;&nbsp;Jaccard &middot; every horizontal line is a threshold
 slice, and there is NO chosen cut &mdash; the sweep is the result""",
                     META)
            .replace("__TREE__", json.dumps(tree, separators=(",", ":")))
            .replace("__SWEEP__", json.dumps(sweep, separators=(",", ":")))
            .replace("__AGREE__", json.dumps(data["spelling_agreement"],
                                             separators=(",", ":")))
            .replace("__WORKED__", json.dumps(
                [dict(label=w["label"], operation=w["operation"],
                      input_cell=w["input_cell"], tokens=w["tokens"],
                      all_agree=w["all_agree"])
                 for w in data["worked_examples"]],
                separators=(",", ":")))
            .replace("__LANGCOLOR__", json.dumps(LANG_COLOR))
            .replace("__NLEAVES__", "{:,}".format(tree["n_leaves"])))
    out = os.path.join(HERE, "dendrogram_answers.html")
    with open(out, "w") as f:
        f.write(html)
    print("wrote %s (%.2f MB, %d leaves, %d nodes)"
          % (out, len(html) / 1e6, tree["n_leaves"], len(tree["nodes"])))


if __name__ == "__main__":
    main()
