#!/usr/bin/env python3
"""make_dendrogram_alt.py -- the three ALTERNATIVE-reading dendrograms.

    dendrogram_agreement.html    from clusters_agreement.json
    dendrogram_containment.html  from clusters_containment.json
    dendrogram_domain.html       from clusters_domain.json

Same conventions as `make_dendrogram.py' (log 030),
`make_dendrogram_answers.py' (log 031) and `make_dendrogram_all12.py'
(log 033), and therefore the same conventions as
`dendrogram_explorer.html' before all three: the icicle rendering, the
similarity axis high at the top, the draggable dashed #ff2d78 threshold
line, the live cluster count, the #ffd400 outline on the clusters at the
current threshold, the search box, the hover card, the plateau table and
the cluster-count-versus-threshold curve with the plateaus shaded.
Self-contained, no CDN, opens from `file://'.

What differs between the three is the DISTANCE and nothing else.  The
leaves are the same 238 operation signatures in the same order, the
linkage is the same average linkage, and no cut is chosen in any of
them.  Set side by side that is the point: where two of these trees
disagree about a pair, the disagreement is attributable, because only
one thing was changed.

The three lower panels -- the twelve-by-twelve agreement matrix, the
per-operation roll-up and the known-fracture table -- are carried over
from log 033 unchanged.  They are properties of the MEASUREMENT and not
of any tree, so they read the same under every distance and they are
the common ground a reader flips between the four files on.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_dendrogram import build_tree, TEMPLATE, LANG_COLOR      # noqa
from make_dendrogram_all12 import EXTRA, SCRIPT, ORDER, OLD_META  # noqa

HEAD = "Operation clustering &mdash; the threshold sweep"

READINGS = {
    "agreement": dict(
        out="dendrogram_agreement.html",
        src="clusters_agreement.json",
        title="Operation clustering &mdash; AGREEMENT ONLY, "
              "all twelve languages",
        meta="""__NLEAVES__ operation signatures over ALL TWELVE
 languages &middot; distance = 1 &minus; A, where A is the
 answer-agreement rate on the input cells the two signatures BOTH
 accept &middot; <b>the domain is not consulted at all</b>: this tree
 asks only &ldquo;where both speak, do they agree&rdquo; &middot;
 DECISION 55 &mdash; a pair needs at least __SUPPORT__ shared input
 cells before its rate is read; __EXCLUDED__ of __TOTAL__ pairs are
 below that and are left OUT of every average rather than scored zero,
 and __NOTHING__ of them share no input cell at all &middot; average
 linkage, and there is NO chosen cut &mdash; the sweep is the result
 &middot; the product reading this one is set beside is
 <code>dendrogram_all12.html</code>""",
        hint="""This tree is the answer half of decision 27's product,
 read on its own. A pair that never disagrees sits at the top of it
 however narrow either domain is, which is exactly what the product
 could not show. <b>Read it against
 <code>dendrogram_domain.html</code></b>: a pair high here and low
 there is the CORE's <i>nests</i> case &mdash; same answers, different
 width."""),
    "containment": dict(
        out="dendrogram_containment.html",
        src="clusters_containment.json",
        title="Operation clustering &mdash; CONTAINMENT WEIGHTED, "
              "all twelve languages",
        meta="""__NLEAVES__ operation signatures over ALL TWELVE
 languages &middot; distance = 1 &minus; C&nbsp;&times;&nbsp;A, where C
 is the number of shared cells divided by the size of the SMALLER
 domain and A is the answer-agreement rate on the shared input cells
 &middot; <b>nesting costs nothing</b>: a signature wholly inside
 another scores C = 1, while genuine partial overlap still costs
 &middot; this is decision 27's product with Jaccard swapped for
 containment and nothing else changed &middot; average linkage, and
 there is NO chosen cut &mdash; the sweep is the result""",
        hint="""Jaccard punishes a narrow domain twice: once in the
 numerator it cannot fill and once in the union it enlarges.
 Containment punishes it neither way. What survives a move from
 <code>dendrogram_all12.html</code> to this file is a distance that was
 about DISAGREEMENT; what collapses was about WIDTH."""),
    "domain": dict(
        out="dendrogram_domain.html",
        src="clusters_domain.json",
        title="Operation clustering &mdash; DOMAIN ONLY, "
              "all twelve languages",
        meta="""__NLEAVES__ operation signatures over ALL TWELVE
 languages &middot; distance = 1 &minus; J, the Jaccard of the two
 domains &middot; <b>the answers are ignored entirely</b> &middot; this
 is the control log 033 published as a summary, built here as a tree of
 its own so it can be set against
 <code>dendrogram_agreement.html</code> pair for pair &middot; average
 linkage, and there is NO chosen cut &mdash; the sweep is the result""",
        hint="""This is what the clustering sees when it is told only
 which inputs each operation ACCEPTS. Set against
 <code>dendrogram_agreement.html</code>, every pair the two trees place
 differently is a nests-or-overlaps case, and the list of them is in
 <code>two_tree_disagreement.json</code>."""),
}

OLD_HINT = ("""<div class="hint">Drag the dashed line DOWN for fewer """
            """clusters (lower""")


def build(name, spec, panels):
    data = json.load(open(os.path.join(HERE, spec["src"])))
    tree = build_tree(data)
    assert tree["n_leaves"] == data["n_leaves"], (
        "leaf set disagrees with the clustering: %d vs %d"
        % (tree["n_leaves"], data["n_leaves"]))
    sweep = dict(curve=data["cluster_count_curve"],
                 plateaus=data["stability_plateaus"],
                 merge_sims=sorted((m["similarity"]
                                    for m in data["merge_history"]),
                                   reverse=True))
    meta = (spec["meta"]
            .replace("__SUPPORT__", str(data.get("support_threshold", "")))
            .replace("__EXCLUDED__",
                     "{:,}".format(data.get("pairs_excluded", 0)))
            .replace("__TOTAL__", "{:,}".format(data.get("pairs_total", 0)))
            .replace("__NOTHING__",
                     "{:,}".format(data.get("pairs_sharing_nothing", 0))))
    j = lambda o: json.dumps(o, separators=(",", ":"))         # noqa: E731
    html = ((TEMPLATE + EXTRA + SCRIPT)
            .replace(HEAD, spec["title"])
            .replace(OLD_META, meta)
            .replace(OLD_HINT,
                     '<div class="hint">' + spec["hint"]
                     + ' Drag the dashed line DOWN for fewer clusters '
                       '(lower')
            .replace("__TREE__", j(tree))
            .replace("__SWEEP__", j(sweep))
            .replace("__SMAT__", j(panels["spelling_matrix"]))
            .replace("__SOPS__", j(panels["spelling_by_operation"]))
            .replace("__ORDER__", j(ORDER))
            .replace("__WORKED__", j(
                [dict(label=w["label"], operation=w["operation"],
                      input_cell=w["input_cell"], tokens=w["tokens"],
                      all_agree=w["all_agree"])
                 for w in panels["worked_examples"]]))
            .replace("__LANGCOLOR__", j(LANG_COLOR))
            .replace("__NLEAVES__", "{:,}".format(tree["n_leaves"])))
    left = set(re.findall(r"__[A-Z][A-Z_]*__", html))
    assert not left, "unfilled placeholder: %s" % sorted(left)
    out = os.path.join(HERE, spec["out"])
    with open(out, "w") as f:
        f.write(html)
    w = data["widest_plateau"]
    print("wrote %s (%.2f MB, %d leaves, %d nodes) -- widest "
          "non-degenerate plateau [%.3f, %.3f) -> %d clusters"
          % (spec["out"], len(html) / 1e6, tree["n_leaves"],
             len(tree["nodes"]), w["low"], w["high"], w["clusters"]))


def main():
    panels = json.load(open(os.path.join(HERE, "clusters_all12.json")))
    for name, spec in READINGS.items():
        build(name, spec, panels)


if __name__ == "__main__":
    main()
