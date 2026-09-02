#!/usr/bin/env python3
"""make_dendrogram_constructs.py -- dendrogram_constructs.html from
clusters_constructs.json.

Same conventions as `make_dendrogram.py' (log 030) and
`make_dendrogram_all12.py' (log 033), and reusing their template rather
than restating it: the icicle rendering, the similarity axis high at the
top, the draggable dashed threshold line, the live cluster count, the
outline on the clusters at the current threshold, the search box, the
hover card, the plateau table and the cluster-count-versus-threshold
curve with the plateaus shaded.  Self-contained, no CDN, opens from
`file://'.

What differs is the leaf, and it is the pass's difference and not a
style one: a leaf is one CONSTRUCT ROLE in one language, not one
operation in one language.  The label reads `csharp.Kflow.if'.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from make_dendrogram import build_tree, TEMPLATE, LANG_COLOR      # noqa


def main():
    data = json.load(open(os.path.join(HERE, "clusters_constructs.json")))
    tree = build_tree(data)
    assert tree["n_leaves"] == data["n_leaves"], (
        "leaf count moved between the clustering and the picture: "
        "%d against %d" % (tree["n_leaves"], data["n_leaves"]))
    sweep = dict(
        curve=[[r["threshold"], r["clusters"]] for r in data["sweep"]],
        plateaus=data["plateaus"],
        merge_sims=sorted((m["similarity"] for m in data["merge_history"]),
                          reverse=True),
    )
    html = (TEMPLATE
            .replace("__TREE__", json.dumps(tree, separators=(",", ":")))
            .replace("__SWEEP__", json.dumps(sweep, separators=(",", ":")))
            .replace("__LANGCOLOR__", json.dumps(LANG_COLOR))
            .replace("__NLEAVES__", "{:,}".format(tree["n_leaves"])))
    html = html.replace("operation signatures over 12 languages",
                        "CONSTRUCT signatures over 12 languages")
    left = set(re.findall(r"__[A-Z][A-Z_]*__", html))
    assert not left, "unfilled placeholder: %s" % sorted(left)
    out = os.path.join(HERE, "dendrogram_constructs.html")
    open(out, "w").write(html)
    print("wrote %s (%.2f MB, %d leaves, %d nodes)"
          % (out, len(html) / 1e6, tree["n_leaves"], len(tree["nodes"])))


if __name__ == "__main__":
    main()
