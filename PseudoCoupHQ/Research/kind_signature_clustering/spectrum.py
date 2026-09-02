#!/usr/bin/env python3
"""spectrum.py — the owner's ruling 1 (2026-08-12): defer the clustering decision.

The agglomerative merge tree is the artifact, not any single slice of it.
For EVERY pair of kinds (all five languages pooled: rust, python, dart, c,
cpp; kotlin still excluded) we record the merge height at which the pair
joins under average linkage over the SAME weighted Jaccard distance as the
first pass (the distance_matrix function is imported from cluster.py, not
reimplemented). Merge height is equivalent to co-cluster fraction across the
threshold spectrum: a pair with merge height h is co-clustered at every
threshold t >= h and separated at every t < h, so similarity is defined as
    sim(a, b) = 1 - merge_height(a, b)
which is exactly the fraction of the [0, 1] threshold spectrum over which
the pair co-clusters.

Storage: similarity_matrix.npz, NOT .json. Why: 800 kinds -> 319,600 pairs;
a JSON of labeled float pairs runs ~20 MB and loads slowly, while the .npz
holds the condensed matrices in float32 (~2 MB) plus the merge tree itself
(the linkage matrix `Z`, from which any slice is reproducible). The small
loader lives in this same file: load_spectrum() / similarity() /
clusters_at(threshold).

Vocabulary: super-node / sub-node / co-node / sub-tree only. scipy's linkage
matrix row i records the two merge tree sub-nodes joined into merge-tree
node n+i at column-2 height; we only ever address rows and heights.

Usage:
    python3 spectrum.py                      # from features.json
    python3 spectrum.py --hold-out-declared  # from features_holdout.json,
                                             # writes similarity_matrix_holdout.npz
Query API (import spectrum):
    labels, Z, S = spectrum.load_spectrum()  # S = full similarity matrix
    spectrum.clusters_at(0.40)               # list of member-label lists
"""
import json
import os
import sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster, cophenet
from scipy.spatial.distance import squareform

import cluster as first_pass  # reuse the first-pass distance function AS IS

HERE = os.path.dirname(os.path.abspath(__file__))


def load_items(features_path):
    feats = json.load(open(features_path))
    items = []
    for lang in sorted(feats):
        for kind in sorted(feats[lang]):
            items.append((lang + ":" + kind, feats[lang][kind]["features"]))
    return items


def build(features_path, out_path):
    items = load_items(features_path)
    labels = np.array([l for l, _ in items])
    D = first_pass.distance_matrix(items)
    cond = squareform(D, checks=False)
    Z = linkage(cond, method="average")
    merge = cophenet(Z)  # condensed pairwise merge heights
    np.savez_compressed(out_path,
                        labels=labels,
                        raw_condensed=cond.astype(np.float32),
                        merge_condensed=merge.astype(np.float32),
                        Z=Z)
    print("wrote %s (%d kinds, %d pairs)" % (out_path, len(labels), len(merge)))
    return out_path


def load_spectrum(path=None):
    """Return (labels, Z, S) where S[i, j] = 1 - merge height = co-cluster
    fraction across the threshold spectrum. Also attaches the raw weighted
    Jaccard distances as load_spectrum.raw for tie-breaking."""
    path = path or os.path.join(HERE, "similarity_matrix.npz")
    d = np.load(path)
    labels = [str(x) for x in d["labels"]]
    S = 1.0 - squareform(d["merge_condensed"])
    np.fill_diagonal(S, 1.0)
    load_spectrum.raw = squareform(d["raw_condensed"])
    return labels, d["Z"], S


def clusters_at(threshold, path=None):
    """Clusters are QUERIES against the merge tree, not stored artifacts:
    slice the tree at `threshold` (merge-height criterion) and return member
    lists, largest first."""
    labels, Z, _ = load_spectrum(path)
    assign = fcluster(Z, t=threshold, criterion="distance")
    out = {}
    for lab, c in zip(labels, assign):
        out.setdefault(int(c), []).append(lab)
    return sorted((sorted(v) for v in out.values()),
                  key=lambda c: (-len(c), c[0]))


def stability_bands(path=None):
    """For every merge-tree node (leaf or joined), the threshold band
    [birth, death) over which its exact member set is a maximal cluster:
    birth = the node's own merge height (0 for leaves), death = the merge
    height of its super-node in the tree. Returns
    {frozenset(member_labels): (birth, death)}."""
    labels, Z, _ = load_spectrum(path)
    n = len(labels)
    members = {i: frozenset([labels[i]]) for i in range(n)}
    birth = {i: 0.0 for i in range(n)}
    death = {}
    for i, (a, b, h, _) in enumerate(Z):
        a, b = int(a), int(b)
        death[a] = death[b] = h
        members[n + i] = members[a] | members[b]
        birth[n + i] = h
    root = n + len(Z) - 1
    death[root] = 1.0
    return {members[i]: (birth[i], death[i]) for i in members}


def main():
    v2 = "--v2" in sys.argv  # decision-6 counts fix: versioned inputs/outputs
    tag = "_v2" if v2 else ""
    if "--hold-out-declared" in sys.argv:
        build(os.path.join(HERE, "features%s_holdout.json" % tag),
              os.path.join(HERE, "similarity_matrix%s_holdout.npz" % tag))
    else:
        build(os.path.join(HERE, "features%s.json" % tag),
              os.path.join(HERE, "similarity_matrix%s.npz" % tag))


if __name__ == "__main__":
    main()
