#!/usr/bin/env python3
"""export_tree_all.py — export the full-ecosystem merge tree from
spectrum_all.npz as merge_tree_all.json for dendrogram_explorer_all.html.

Leaves are ARCHETYPES (8,329), not kinds: each leaf carries its hash, its
multiplicity ("mult" = member kind count), its per-category kind counts
("cats"), and a capped member list ("mem", up to 16 "language:kind"
labels + the total). Joined nodes list their two sub-nodes under "subs"
with merge height "h". Stability band of a node = [own h, super-node h).

Vocabulary rule: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MEM_CAP = 16


def export():
    d = np.load(os.path.join(HERE, "spectrum_all.npz"))
    hashes = [str(x) for x in d["labels"]]
    Z = d["Z"]
    arch = json.load(open(os.path.join(HERE, "archetypes.json")))
    n = len(hashes)
    nodes = {}
    for i, h in enumerate(hashes):
        a = arch[h]
        nodes[i] = {"label": h, "h": 0.0, "size": 1,
                    "mult": a["size"], "cats": a["categories"],
                    "mem": a["members"][:MEM_CAP]}
    for i, row in enumerate(Z):
        a, b, hh = int(row[0]), int(row[1]), float(row[2])
        sa, sb = nodes.pop(a), nodes.pop(b)
        nodes[n + i] = {"h": hh, "size": sa["size"] + sb["size"],
                        "subs": [sa, sb]}
    root = nodes[n + len(Z) - 1]
    out = os.path.join(HERE, "merge_tree_all.json")
    with open(out, "w") as f:
        json.dump({"n_leaves": n, "n_kinds": int(d["mult"].sum()),
                   "root": root}, f, separators=(",", ":"))
    print("wrote %s (%d archetype leaves)" % (out, n))


if __name__ == "__main__":
    export()
