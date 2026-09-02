#!/usr/bin/env python3
"""cluster.py — agglomerative clustering of the union of all five languages'
named kinds on the feature vectors in features.json.

THE DISTANCE FUNCTION (the documented, inspectable heart):

    d(a, b) = 1 - sum(w[e] for e in Fa & Fb) / sum(w[e] for e in Fa | Fb)

i.e. weighted Jaccard distance over the flat weighted feature sets emitted
by features.py. Weights per element are fixed by feature family there
(role presence 3, is_leaf 3, output types 2, input-type signatures 1 (0.5
for the sub-node spec), arity flags 1, booleans 1). Booleans participate as
set elements present-when-true, which makes their contribution an exact
match term. Two kinds with no overlapping features are at distance 1.

Algorithm: deterministic agglomerative clustering (average linkage by
default, Lance-Williams update), cut at a distance threshold. Agglomerative
was chosen over k-medoids because it is seed-free; "stability" is therefore
probed across the remaining free parameters (threshold, linkage) rather
than random seeds. Emits clusters.json for the primary configuration
(average linkage, threshold 0.40) plus a stability section comparing runs.

Stability metric: pair-Jaccard between two clusterings = |co-clustered
pairs in both| / |co-clustered pairs in either|.
"""
import json
import os
import itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

PRIMARY = ("average", 0.40)
VARIANTS = [("average", 0.35), ("average", 0.45), ("complete", 0.55)]


def load_items():
    feats = json.load(open(os.path.join(HERE, "features.json")))
    items = []  # (label, {element: weight})
    for lang in sorted(feats):
        for kind in sorted(feats[lang]):
            items.append((lang + ":" + kind, feats[lang][kind]["features"]))
    return items


def distance_matrix(items):
    n = len(items)
    sets = [set(f) for _, f in items]
    weights = [f for _, f in items]
    totals = [sum(f.values()) for _, f in items]
    D = np.ones((n, n))
    np.fill_diagonal(D, 0.0)
    for i in range(n):
        wi, si, ti = weights[i], sets[i], totals[i]
        for j in range(i + 1, n):
            inter = si & sets[j]
            if not inter:
                continue
            wj = weights[j]
            num = sum(max(wi[e], wj[e]) for e in inter)
            den = ti + totals[j] - num
            D[i, j] = D[j, i] = 1.0 - num / den if den else 1.0
    return D


def agglomerate(D, linkage, threshold):
    """Deterministic agglomerative clustering with Lance-Williams updates.
    Returns a list of member-index lists."""
    n = D.shape[0]
    M = D.copy()
    np.fill_diagonal(M, np.inf)
    sizes = {i: 1 for i in range(n)}
    members = {i: [i] for i in range(n)}
    active = list(range(n))
    while len(active) > 1:
        sub = M[np.ix_(active, active)]
        k = np.unravel_index(np.argmin(sub), sub.shape)
        d = sub[k]
        if d > threshold:
            break
        a, b = active[k[0]], active[k[1]]
        if a > b:
            a, b = b, a
        for c in active:
            if c in (a, b):
                continue
            if linkage == "average":
                new = (sizes[a] * M[a, c] + sizes[b] * M[b, c]) / (sizes[a] + sizes[b])
            else:  # complete
                new = max(M[a, c], M[b, c])
            M[a, c] = M[c, a] = new
        members[a] = members[a] + members[b]
        sizes[a] += sizes[b]
        del members[b], sizes[b]
        active.remove(b)
        M[b, :] = np.inf
        M[:, b] = np.inf
    return [sorted(v) for v in members.values()]


def pairs(clustering, labels):
    p = set()
    for c in clustering:
        for a, b in itertools.combinations(sorted(labels[i] for i in c), 2):
            p.add((a, b))
    return p


def main():
    items = load_items()
    labels = [l for l, _ in items]
    print(len(items), "kinds across 5 languages")
    D = distance_matrix(items)

    runs = {}
    for linkage, thr in [PRIMARY] + VARIANTS:
        clusters = agglomerate(D, linkage, thr)
        runs[(linkage, thr)] = clusters
        multi = [c for c in clusters if len(c) > 1]
        print("run linkage=%s thr=%.2f: %d clusters (%d non-singleton, "
              "largest %d)" % (linkage, thr, len(clusters), len(multi),
                              max(len(c) for c in clusters)))

    primary = runs[PRIMARY]
    primary_sorted = sorted(primary, key=lambda c: (-len(c), labels[c[0]]))
    out = {"config": {"linkage": PRIMARY[0], "threshold": PRIMARY[1],
                      "distance": "weighted Jaccard, see module docstring"},
           "clusters": {}}
    for i, c in enumerate(primary_sorted):
        out["clusters"]["c%03d" % i] = sorted(labels[j] for j in c)

    p0 = pairs(primary, labels)
    stability = {}
    for key, clusters in runs.items():
        if key == PRIMARY:
            continue
        p1 = pairs(clusters, labels)
        j = len(p0 & p1) / len(p0 | p1) if (p0 | p1) else 1.0
        stability["%s_%.2f" % key] = {
            "pair_jaccard_vs_primary": round(j, 3),
            "n_clusters": len(clusters),
        }
        print("stability vs %s thr=%.2f: pair-Jaccard %.3f" % (*key, j))
    out["stability"] = stability

    path = os.path.join(HERE, "clusters.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
