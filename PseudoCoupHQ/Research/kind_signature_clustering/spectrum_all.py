#!/usr/bin/env python3
"""spectrum_all.py — the full-ecosystem merge-tree spectrum (plan step 3).

Dense pairwise distances over the 8,329 ARCHETYPES of features_all.json
(v2 counts-fixed vectors, all 411 grammars, 31,212 clusterable kinds),
reusing the v2 weighted-Jaccard distance exactly:

    d(a, b) = 1 - sum(w[e] for e in Fa & Fb) / sum(w[e] for e in Fa | Fb)

(the cluster.py formula uses max(wi[e], wj[e]) over the intersection; every
element's weight is fixed by its feature family, verified identical across
all vectors at load time, so the max IS the shared weight and the whole
computation vectorizes as a sparse Gram product — checked against
cluster.distance_matrix on random pairs at build time.)

MULTIPLICITY-AWARE AVERAGE LINKAGE (the log_013 caveat). Each archetype
enters the agglomeration weighted by its member count m_i. Lance-Williams
update, with n_A = TOTAL MEMBER KINDS in cluster A (not archetype count):

    d(C, A u B) = (n_A * d(C, A) + n_B * d(C, B)) / (n_A + n_B)

Because members of one archetype are at pairwise distance exactly 0 and at
identical distance to everything else, this is EXACTLY unweighted UPGMA
over the full 31,212-kind population: the average of kind-pair distances
between two clusters equals the multiplicity-weighted average of their
archetype distances. Nothing is approximated (the owner's no-sampling rule).

Implementation: nearest-neighbor-chain agglomeration (average linkage is
reducible, so NN-chain is exact); merges re-sorted by height and relabeled
into a scipy-conformant linkage matrix Z.

Checkpointing (runtime discipline): the condensed distance matrix is
written to dist_all<suffix>.npy as soon as it is computed; a rerun loads
it instead of recomputing. The final spectrum lands in
spectrum_all<suffix>.npz (labels = archetype hashes, mult, Z, raw
condensed float32, merge-height condensed float32).

Outputs (main run): spectrum_all.npz, merge_tree_all.json (via
export_tree_all.py), top_counterparts_all.json (per-archetype top-10
nearest counterpart archetypes, presentation slice).
Query API: load_spectrum_all() / clusters_at(t).

Usage:
    python3 spectrum_all.py                      # features_all.json
    python3 spectrum_all.py --hold-out-declared  # features_all_holdout.json

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.cluster.hierarchy import cophenet, fcluster
from scipy.sparse import csr_matrix

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = 512


def load_archetypes(suffix=""):
    d = json.load(open(os.path.join(HERE, "features_all%s.json" % suffix)))
    arch = json.load(open(os.path.join(HERE, "archetypes%s.json" % suffix)))
    hashes = sorted(d["vectors"])
    vectors = [d["vectors"][h] for h in hashes]
    mult = np.array([arch[h]["size"] for h in hashes], dtype=np.float64)
    return hashes, vectors, mult, arch


def element_weights(vectors):
    """Verify each element carries ONE weight across all vectors (the
    precondition for the Gram-product vectorization) and return the map."""
    w = {}
    for v in vectors:
        for e, x in v.items():
            if e in w and w[e] != x:
                raise AssertionError("inconsistent weight for %r" % e)
            w[e] = x
    return w


def distance_square(vectors):
    """Dense square weighted-Jaccard distance matrix, float32, blockwise."""
    w = element_weights(vectors)
    elems = {e: i for i, e in enumerate(sorted(w))}
    n = len(vectors)
    rows, cols, vals = [], [], []
    for i, v in enumerate(vectors):
        for e, x in v.items():
            rows.append(i)
            cols.append(elems[e])
            vals.append(np.sqrt(x))
    X = csr_matrix((vals, (rows, cols)), shape=(n, len(elems)),
                   dtype=np.float64)
    totals = np.array([sum(v.values()) for v in vectors])
    D = np.empty((n, n), dtype=np.float32)
    for b0 in range(0, n, BLOCK):
        b1 = min(n, b0 + BLOCK)
        G = np.asarray((X[b0:b1] @ X.T).todense())     # shared-weight sums
        den = totals[b0:b1, None] + totals[None, :] - G
        blk = 1.0 - np.divide(G, den, out=np.zeros_like(G), where=den > 0)
        D[b0:b1] = blk.astype(np.float32)
    np.fill_diagonal(D, 0.0)
    return D


def spot_check(D, vectors, k=200, seed=7):
    """Verify the vectorized distances against the cluster.py formula."""
    import cluster as first_pass
    rng = np.random.default_rng(seed)
    n = len(vectors)
    idx = rng.integers(0, n, size=(k, 2))
    items = [("a", None), ("b", None)]
    for i, j in idx:
        sub = [("x", vectors[i]), ("y", vectors[j])]
        ref = first_pass.distance_matrix(sub)[0, 1]
        if abs(ref - float(D[i, j])) > 1e-5:
            raise AssertionError("distance mismatch at (%d,%d): %f vs %f"
                                 % (i, j, ref, D[i, j]))


def nn_chain_weighted_average(D, mult):
    """NN-chain agglomeration, average linkage weighted by multiplicity.
    Returns a scipy-conformant linkage matrix Z (column 3 = leaf count)."""
    n = D.shape[0]
    M = D.astype(np.float64).copy()
    np.fill_diagonal(M, np.inf)
    size = mult.astype(np.float64).copy()      # member KINDS per cluster
    leaves = np.ones(n)                        # archetype count per cluster
    node = np.arange(n)                        # cluster slot -> tree node id
    active = np.ones(n, dtype=bool)
    raw = []                                   # (id_a, id_b, h, n_leaves)
    nxt = n
    chain = []
    merges = 0
    while merges < n - 1:
        if not chain:
            chain.append(int(np.flatnonzero(active)[0]))
        while True:
            a = chain[-1]
            row = M[a]
            b = int(np.argmin(row))
            if len(chain) > 1 and row[chain[-2]] <= row[b]:
                b = chain[-2]
            if len(chain) > 1 and b == chain[-2]:
                chain.pop()
                chain.pop()
                break
            chain.append(b)
        h = float(M[a, b])
        na, nb = size[a], size[b]
        new = (na * M[a] + nb * M[b]) / (na + nb)
        M[a, :] = new
        M[:, a] = new
        M[a, a] = np.inf
        M[b, :] = np.inf
        M[:, b] = np.inf
        active[b] = False
        size[a] = na + nb
        raw.append((node[a], node[b], h, leaves[a] + leaves[b]))
        leaves[a] += leaves[b]
        node[a] = nxt
        nxt += 1
        merges += 1
    # re-sort by height, relabel to scipy convention (retry loop covers
    # equal-height rows whose sub-node happens to sort after them)
    order = sorted(range(len(raw)), key=lambda i: (raw[i][2], i))
    remap = {i: i for i in range(n)}
    Z = np.zeros((n - 1, 4))
    pending = list(order)
    out_i = 0
    while pending:
        rest = []
        for oi in pending:
            a, b, h, s = raw[oi]
            if a in remap and b in remap:
                Z[out_i] = [min(remap[a], remap[b]),
                            max(remap[a], remap[b]), h, s]
                remap[n + oi] = n + out_i
                out_i += 1
            else:
                rest.append(oi)
        if len(rest) == len(pending):
            raise AssertionError("relabel deadlock")
        pending = rest
    return Z


def build(suffix=""):
    t0 = time.time()
    hashes, vectors, mult, arch = load_archetypes(suffix)
    n = len(hashes)
    print("archetypes: %d  kinds: %d" % (n, int(mult.sum())))

    dist_ck = os.path.join(HERE, "dist_all%s.npy" % suffix)
    if os.path.exists(dist_ck):
        cond = np.load(dist_ck)
        from scipy.spatial.distance import squareform
        D = squareform(cond)
        print("distance checkpoint loaded (%.1fs)" % (time.time() - t0))
    else:
        D = distance_square(vectors)
        from scipy.spatial.distance import squareform
        cond = squareform(D, checks=False).astype(np.float32)
        np.save(dist_ck, cond)
        print("distances: %d pairs in %.1fs (checkpointed)"
              % (len(cond), time.time() - t0))
    spot_check(D, vectors)
    print("spot check vs cluster.py distance: OK")

    t1 = time.time()
    Z = nn_chain_weighted_average(D, mult)
    assert np.all(np.diff(Z[:, 2]) >= -1e-12), "non-monotone linkage"
    print("multiplicity-weighted average linkage: %.1fs" % (time.time() - t1))

    t2 = time.time()
    merge_cond = cophenet(Z).astype(np.float32)
    print("cophenetic merge heights: %.1fs" % (time.time() - t2))

    out = os.path.join(HERE, "spectrum_all%s.npz" % suffix)
    np.savez_compressed(out, labels=np.array(hashes), mult=mult, Z=Z,
                        raw_condensed=cond, merge_condensed=merge_cond)
    print("wrote %s  (total %.1fs)" % (out, time.time() - t0))

    if not suffix:
        top_counterparts(hashes, D, arch)
    return out


def top_counterparts(hashes, D, arch, k=10):
    """Presentation slice: for every archetype, the k nearest counterpart
    archetypes by raw distance, with multiplicity and sample members."""
    n = len(hashes)
    out = {}
    for i in range(n):
        row = D[i].copy()
        row[i] = np.inf
        near = np.argpartition(row, k)[:k]
        near = near[np.argsort(row[near])]
        out[hashes[i]] = {
            "size": arch[hashes[i]]["size"],
            "examples": arch[hashes[i]]["members"][:3],
            "counterparts": [
                {"hash": hashes[j], "sim": round(1.0 - float(row[j]), 4),
                 "size": arch[hashes[j]]["size"],
                 "examples": arch[hashes[j]]["members"][:3]}
                for j in near]}
    p = os.path.join(HERE, "top_counterparts_all.json")
    with open(p, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print("wrote", p)


def load_spectrum_all(suffix=""):
    d = np.load(os.path.join(HERE, "spectrum_all%s.npz" % suffix))
    return [str(x) for x in d["labels"]], d["mult"], d["Z"], \
        d["merge_condensed"]


def clusters_at(threshold, suffix=""):
    """Clusters are QUERIES against the merge tree: member-hash lists,
    largest first, at merge-height threshold."""
    labels, mult, Z, _ = load_spectrum_all(suffix)
    assign = fcluster(Z, t=threshold, criterion="distance")
    out = {}
    for lab, c in zip(labels, assign):
        out.setdefault(int(c), []).append(lab)
    return sorted((sorted(v) for v in out.values()),
                  key=lambda c: (-len(c), c[0]))


if __name__ == "__main__":
    build("_holdout" if "--hold-out-declared" in sys.argv else "")
