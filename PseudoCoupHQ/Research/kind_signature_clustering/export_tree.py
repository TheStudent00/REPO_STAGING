#!/usr/bin/env python3
"""export_tree.py — export the agglomerative merge tree from
similarity_matrix.npz as merge_tree.json for the dendrogram explorer.

Reads spectrum.py's stored linkage matrix Z (does not touch spectrum.py).
Each merge-tree node carries: its merge height ("h", 0 for leaves), the
number of leaves in its sub-tree ("size"), and — for leaves — the
"language:kind" label. Node structure is nested: every joined node lists
its two sub-nodes under "subs". The stability band of a node is derivable
in the viewer as [own h, super-node h), so it is not duplicated here.

Vocabulary rule: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def export(npz_path=None, out_path=None):
    npz_path = npz_path or os.path.join(HERE, "similarity_matrix.npz")
    out_path = out_path or os.path.join(HERE, "merge_tree.json")
    d = np.load(npz_path)
    labels = [str(x) for x in d["labels"]]
    Z = d["Z"]
    n = len(labels)
    nodes = {i: {"label": labels[i], "h": 0.0, "size": 1} for i in range(n)}
    for i, row in enumerate(Z):
        a, b, h = int(row[0]), int(row[1]), float(row[2])
        sa, sb = nodes.pop(a), nodes.pop(b)
        nodes[n + i] = {"h": round(h, 6),
                        "size": sa["size"] + sb["size"],
                        "subs": [sa, sb]}
    root = nodes[n + len(Z) - 1]
    with open(out_path, "w") as f:
        json.dump({"n_leaves": n, "root": root}, f)
    print("wrote %s (%d leaves)" % (out_path, n))
    return out_path


if __name__ == "__main__":
    export()
