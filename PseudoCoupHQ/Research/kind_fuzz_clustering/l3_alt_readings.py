#!/usr/bin/env python3
"""l3_alt_readings.py -- the three ALTERNATIVE readings of the same
238 operator leaves, built beside the product reading and not instead
of it.

The product reading is decision 27 (log 031, carried to twelve in log
033): the similarity of two operation signatures is

    J x A

where J is the Jaccard of their DOMAINS -- the sets of input cells
each one accepts -- and A is the rate at which they give the same
answer on the cells they BOTH accept.

the owner ruled on 2026-08-20 that the product has a bias worth reading
around, and that each way around it is built as its own visual rather
than argued about.  A product of two factors cannot say which factor
moved.  Two signatures that never disagree once can still sit far
apart because one of them accepts more, and the product spends the
whole of A's evidence on a J that was small for a reason that has
nothing to do with disagreement.  `go.+' against `java.+' is the
standing case: A is exactly 1.000 and the product is 0.094.

Three readings are built here, each a re-read of `clusters_all12.json'
and nothing else.  No probe runs.  No lane runs.

  AGREEMENT ONLY      similarity = A.  "where both speak, do they
                      agree."  Domain size is not consulted at all.
                      Needs a SUPPORT THRESHOLD, decision 55, because
                      an A computed over three shared cells is not a
                      rate.
  CONTAINMENT         similarity = C x A, where
                      C = |shared cells| / |smaller domain|.
                      Nesting costs nothing: a signature wholly
                      inside another scores C = 1.  Genuine partial
                      overlap still costs.
  DOMAIN ONLY         similarity = J.  Answers ignored.  This is the
                      control log 033 already computed as a summary;
                      here it becomes a tree of its own so it can be
                      set beside the agreement tree pair for pair.

Products: `clusters_agreement.json', `clusters_containment.json',
`clusters_domain.json', and `two_tree_disagreement.json' -- the pairs
the agreement tree and the domain tree place differently, which is the
node's nests-versus-overlaps case list read off two trees instead of
asserted.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# --- decision 55 ------------------------------------------------------
# The minimum number of shared input cells a pair must have before its
# agreement rate is read at all.
#
# Why 32 and not another number.  A is a rate.  Over 32 shared cells a
# single cell moves it by 0.031, which is fine enough that the third
# decimal the trees are cut on means something.  Over 8 shared cells one
# cell moves it by 0.125 and the rate is a coin, not a measurement.  32
# is the smallest power of two at which one cell is worth less than
# three points, and it is half the 64-cell shared form grid, so it is
# also sayable without arithmetic: a pair must meet on at least half a
# grid's worth of cells.
#
# What happens to a pair below it: the pair is UNSUPPORTED.  It is not
# given a similarity of zero, because zero is a claim -- it would say
# the two never agree, which is exactly what was not measured.  It is
# left out of the average when two groups are compared, and if two
# groups share no supported pair at all their similarity is 0.0 and the
# merge is recorded as unsupported.  The count of both is published.
#
# Cost to overturn: re-run with SUPPORT set to another number.  16 and
# 64 are computed as a sensitivity check on every run and printed.
SUPPORT = 32
SENSITIVITY = (16, 64)


# --- the machinery ----------------------------------------------------
def load():
    return json.load(open(os.path.join(HERE, "clusters_all12.json")))


def leaf_keys(data):
    return sorted(k for k, s in data["signatures"].items() if s["domain"])


def matrices(data, keys):
    """J, A, C, support -- every one an n x n array over `keys'.

    J and A are READ from the artifact's own edge table, not recomputed,
    so these readings and the product reading rest on the same numbers.
    C is computed from the domains, which the artifact also carries.
    """
    n = len(keys)
    idx = {k: i for i, k in enumerate(keys)}
    dom = [set(data["signatures"][k]["domain"]) for k in keys]
    J = np.zeros((n, n))
    A = np.zeros((n, n))
    SH = np.zeros((n, n))
    for name, e in data["edges"].items():
        a, b = name.split(" :: ")
        if a not in idx or b not in idx:
            continue
        i, j = idx[a], idx[b]
        J[i, j] = J[j, i] = e["jaccard"]
        # a pair sharing no input cell carries agreement `null' in the
        # artifact, because no rate was measured.  It is read as 0.0
        # here and it is ALSO unsupported under decision 55, so the
        # zero never reaches an average in the agreement reading.
        A[i, j] = A[j, i] = (e["agreement"] or 0.0)
        SH[i, j] = SH[j, i] = e["shared_inputs"]
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            m = min(len(dom[i]), len(dom[j]))
            v = (len(dom[i] & dom[j]) / m) if m else 0.0
            C[i, j] = C[j, i] = v
    np.fill_diagonal(J, 1.0)
    np.fill_diagonal(A, 1.0)
    np.fill_diagonal(C, 1.0)
    return J, A, C, SH, dom


def average_linkage(keys, S, mask=None):
    """average linkage on a SIMILARITY matrix, merging the highest pair.

    `mask' marks which pairs count toward an average.  Where it is given,
    a group-against-group similarity is the mean over the supported leaf
    pairs only, and a group pair with no supported leaf pair scores 0.0.
    The bookkeeping is the standard sum-and-count update, which is exact
    for average linkage and needs no recomputation from the leaves.

    The merge history comes out in the shape `make_dendrogram.build_tree'
    already reads: leaves are 0..n-1 in the order of `keys', internal
    nodes count up from n.

    TIE-BREAKING is taken from `l3_final.merge_history' and not invented:
    the candidate pairs are scanned in the order of the live list, the
    FIRST best wins, and a new node is appended at the END of that list.
    Ties are common here -- similarity 1.000 and 0.000 both occur in
    bulk -- so the convention is what makes the domain-only reading
    reproduce log 033's own control exactly, which `main' checks.
    """
    n = len(keys)
    W = np.array(S, dtype=float)
    M = (np.ones((n, n)) if mask is None else np.array(mask, dtype=float))
    np.fill_diagonal(M, 0.0)
    cap = 2 * n + 2
    SUM = np.zeros((cap, cap))
    CNT = np.zeros((cap, cap))
    SUM[:n, :n] = W * M
    CNT[:n, :n] = M
    live = list(range(n))
    size = {i: 1 for i in range(n)}
    hist = []
    nxt = n
    unsupported = 0
    while len(live) > 1:
        sub = np.array(live)
        cn = CNT[np.ix_(sub, sub)]
        sm = SUM[np.ix_(sub, sub)]
        av = np.where(cn > 0, sm / np.where(cn > 0, cn, 1.0), 0.0)
        iu = np.triu_indices(len(sub), 1)
        # the live list is scanned row by row, so the first best in
        # row-major order over the upper triangle IS the first best
        # in `l3_final's nested loop.
        vals = av[iu]
        best = int(np.argmax(vals))
        x, y = int(iu[0][best]), int(iu[1][best])
        sim = float(vals[best])
        a, b = live[x], live[y]
        if cn[x, y] == 0:
            unsupported += 1
        hist.append(dict(node=nxt, similarity=round(sim, 6),
                         distance=round(1.0 - sim, 6),
                         left=dict(id=a, size=size[a]),
                         right=dict(id=b, size=size[b]),
                         size=size[a] + size[b],
                         supported_pairs=int(cn[x, y])))
        SUM[nxt, :] = SUM[a, :] + SUM[b, :]
        SUM[:, nxt] = SUM[:, a] + SUM[:, b]
        CNT[nxt, :] = CNT[a, :] + CNT[b, :]
        CNT[:, nxt] = CNT[:, a] + CNT[:, b]
        SUM[nxt, nxt] = CNT[nxt, nxt] = 0.0
        size[nxt] = size[a] + size[b]
        live = [c for c in live if c not in (a, b)] + [nxt]
        nxt += 1
    return hist, unsupported


def count_at(hist, n, t):
    return n - sum(1 for m in hist if m["similarity"] >= t)


def curve(hist, n):
    return [dict(threshold=round(x / 100.0, 2),
                 clusters=count_at(hist, n, x / 100.0))
            for x in range(0, 101)]


def plateaus(hist, n):
    """maximal threshold ranges over which the clustering does not move.

    The count only changes at a merge similarity, so the breakpoints ARE
    the distinct merge similarities and nothing between two of them can
    move.  No cut is chosen anywhere in this file.
    """
    sims = sorted({m["similarity"] for m in hist})
    edges = sorted({0.0, 1.0} | {s for s in sims if 0.0 <= s <= 1.0})
    out = []
    for a, b in zip(edges, edges[1:]):
        if b <= a:
            continue
        c = count_at(hist, n, (a + b) / 2.0)
        out.append(dict(low=round(a, 6), high=round(b, 6),
                        width=round(b - a, 6), clusters=c,
                        degenerate=(c <= 1 or c >= n)))
    out.sort(key=lambda d: -d["width"])
    return out


def clusters_at(keys, hist, t):
    cur = {i: [keys[i]] for i in range(len(keys))}
    alive = set(range(len(keys)))
    for m in hist:
        if m["similarity"] < t:
            continue
        a, b, i = m["left"]["id"], m["right"]["id"], m["node"]
        if a in alive and b in alive:
            cur[i] = cur[a] + cur[b]
            alive.discard(a)
            alive.discard(b)
            alive.add(i)
    return sorted((sorted(cur[i]) for i in alive),
                  key=lambda g: (-len(g), g[0]))


def achievable(hist, n):
    """count -> a threshold that yields it.

    A tree does NOT stand in every number of groups.  The count falls by
    however many merges share a similarity, so a value shared by many
    merges is a CLIFF: the tree steps over the counts in between and
    there is no threshold that shows them.  The agreement reading has
    one such cliff and it is a finding, not an inconvenience, so this
    returns what is reachable rather than pretending.
    """
    out = {n: 1.0000001}
    for v in sorted({m["similarity"] for m in hist}, reverse=True):
        out[count_at(hist, n, v)] = v
    return out


def cut_nearest(hist, n, k):
    """(threshold, achieved count) for the reachable count nearest k."""
    av = achievable(hist, n)
    best = min(av, key=lambda c: (abs(c - k), -c))
    return av[best], best


FAM_ARITH = set("+ - * / % ** // @".split())
FAM_CMP = (set("== != < <= > >= <=> === !== eq ne".split())
           | {"is", "is not", "not_eq", "instanceof", "in", "as"})
FAM_LOGIC = {"&&", "||", "!", "and", "or", "not", "xor", "??", "?:"}
FAM_SHIFT = {"<<", ">>", ">>>", "<<<", ">>=", "<<="}
FAM_BITS = {"&", "|", "^", "&^", "bitand", "bitor"}


def family(op):
    """decision 9 of log 040's mapping, copied rather than imported so
    this file reads on its own; the sets are identical."""
    if op in FAM_SHIFT:
        return "shift"
    if op in FAM_LOGIC:
        return "logical"
    if op in FAM_BITS:
        return "bitwise"
    if op in FAM_CMP:
        return "comparison"
    if op in FAM_ARITH:
        return "arithmetic"
    return "other"


def sorting(groups):
    """how a cut SORTS: by language, or by what the operation does.

    Two rates over the pairs the cut puts TOGETHER: how often the two
    are of one language, and how often they are of one operator family.
    A cut that sorts by language has the first rate high.  Both are read
    beside the count of groups that hold one language only.
    """
    same_l = tot_l = same_f = 0
    for g in groups:
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                tot_l += 1
                if g[i].split(".")[0] == g[j].split(".")[0]:
                    same_l += 1
                if (family(g[i].split(".", 1)[1])
                        == family(g[j].split(".", 1)[1])):
                    same_f += 1
    pure = sum(1 for g in groups
               if len({k.split(".")[0] for k in g}) == 1)
    return dict(pairs_together=tot_l,
                singletons=sum(1 for g in groups if len(g) == 1),
                same_language_rate=round(same_l / tot_l, 6) if tot_l else 0.0,
                same_family_rate=round(same_f / tot_l, 6) if tot_l else 0.0,
                single_language_groups=pure,
                largest_group=max(len(g) for g in groups))


def widest(plats):
    for p in plats:
        if not p["degenerate"]:
            return p
    return plats[0]


def build(keys, S, mask, name, note):
    hist, unsup = average_linkage(keys, S, mask)
    n = len(keys)
    plats = plateaus(hist, n)
    w = widest(plats)
    print("  %-14s widest non-degenerate plateau [%.3f, %.3f) -> %d "
          "clusters%s" % (name, w["low"], w["high"], w["clusters"],
                          ("   unsupported merges %d" % unsup)
                          if unsup else ""))
    return dict(merge_history=hist, cluster_count_curve=curve(hist, n),
                stability_plateaus=plats, widest_plateau=w,
                unsupported_merges=unsup, note=note,
                snapshot=clusters_at(keys, hist, (w["low"] + w["high"]) / 2))


def main():
    data = load()
    keys = leaf_keys(data)
    n = len(keys)
    print("leaves: %d (the operator population of clusters_all12.json)" % n)
    J, A, C, SH, dom = matrices(data, keys)
    sup = (SH >= SUPPORT)
    np.fill_diagonal(sup, False)
    iu = np.triu_indices(n, 1)
    tot = len(iu[0])
    ex = int((~sup)[iu].sum())
    print("decision 55: support threshold %d shared input cells" % SUPPORT)
    print("  pairs: %d total, %d supported, %d EXCLUDED as unsupported "
          "(%.1f percent)" % (tot, tot - ex, ex, 100.0 * ex / tot))
    for t in SENSITIVITY:
        e2 = int((SH < t)[iu].sum())
        print("  sensitivity: at %d the excluded count would be %d "
              "(%.1f percent)" % (t, e2, 100.0 * e2 / tot))
    zero = int((SH[iu] == 0).sum())
    print("  of the excluded, %d share NO input cell at all" % zero)

    print("")
    print("the three readings, each average linkage, no cut chosen:")
    agree = build(keys, A, sup, "agreement",
                  "similarity = A, the answer-agreement rate on the "
                  "shared input cells; domain size is not consulted; "
                  "pairs below decision 55's support are left out of "
                  "every average rather than scored zero")
    contain = build(keys, C * A, None, "containment",
                    "similarity = C x A, where C is |shared cells| "
                    "divided by the size of the SMALLER domain; a "
                    "signature wholly inside another scores C = 1 and "
                    "nesting therefore costs nothing")
    domain = build(keys, J, None, "domain-only",
                   "similarity = J, the Jaccard of the domains; the "
                   "answers are ignored entirely")

    # --- the positive control on the machinery ------------------------
    # The domain-only reading is a tree log 033 ALREADY built, as its
    # `control_domain_only' summary.  If this file's linkage is the same
    # linkage, the plateau list must come out identical.  It is checked
    # rather than assumed, because a tie-breaking difference in a matrix
    # full of exact 1.000s and 0.000s would otherwise pass unnoticed.
    # Matched by CONTENT and not by position: the control publishes only
    # its widest twelve rows and orders equal widths by the accident of a
    # sort, so requiring the same order would test the sort.  A tolerance
    # of 2e-6 is allowed on a bound, which is one unit in the last place
    # the two files round to.
    ctrl = data["control_domain_only"]["stability_plateaus"]
    mine = domain["stability_plateaus"]
    miss = [b for b in ctrl
            if not any(a["clusters"] == b["clusters"]
                       and abs(a["low"] - b["low"]) <= 2e-6
                       and abs(a["high"] - b["high"]) <= 2e-6
                       for a in mine)]
    print("")
    print("positive control: log 033's own control_domain_only publishes "
          "its widest %d plateaus" % len(ctrl))
    print("  this file's domain-only reading reproduces %d of %d, "
          "bound for bound and count for count%s"
          % (len(ctrl) - len(miss), len(ctrl),
             "" if not miss else "  MISSING: %s" % miss))
    assert not miss, "domain-only reading does not reproduce the " \
                     "artifact's own control"

    # the product reading, for the comparison table, read not rebuilt
    prod_hist = data["merge_history"]
    prod_pl = data["stability_plateaus"]
    prod_w = prod_pl[0]

    sigs = {k: dict(language=data["signatures"][k]["language"],
                    operation=data["signatures"][k]["operation"],
                    route=data["signatures"][k].get("route", ""),
                    domain=data["signatures"][k]["domain"])
            for k in keys}

    common = dict(built="2026-08-20", extends=["clusters_all12.json"],
                  n_leaves=n, signatures=sigs, empty_domain=[],
                  decision_55=("a pair needs at least %d shared input "
                               "cells before its agreement rate is read; "
                               "below that the pair is UNSUPPORTED and is "
                               "left out of every average rather than "
                               "scored zero" % SUPPORT),
                  support_threshold=SUPPORT,
                  pairs_total=tot, pairs_excluded=ex,
                  pairs_sharing_nothing=zero)

    for fn, key, blob in (("clusters_agreement.json", "AGREEMENT ONLY",
                           agree),
                          ("clusters_containment.json",
                           "CONTAINMENT WEIGHTED", contain),
                          ("clusters_domain.json", "DOMAIN ONLY", domain)):
        out = dict(common)
        out["status"] = "%s, ALL TWELVE, OPERATORS" % key
        out.update(blob)
        json.dump(out, open(os.path.join(HERE, fn), "w"), indent=1,
                  sort_keys=True)
        print("wrote %s" % fn)

    # --- MATCHED GRANULARITY ------------------------------------------
    # Log 040's decision 51 governs here and is not re-argued: two trees
    # are compared cut to the SAME number of groups, because comparing
    # one tree's 2 groups against another's 29 measures the cut and not
    # the structure.  K is the product tree's own widest non-degenerate
    # plateau count, 21, so the comparison stands where log 035 read the
    # product reading's headline.
    K = prod_w["clusters"]
    hists = dict(product=prod_hist, agreement=agree["merge_history"],
                 containment=contain["merge_history"],
                 domain_only=domain["merge_history"])
    cuts, cutk = {}, {}
    for nm, h in hists.items():
        t, kk = cut_nearest(h, n, K)
        cuts[nm] = clusters_at(keys, h, t)
        cutk[nm] = kk
    print("")
    print("matched granularity: every reading cut as near %d groups as "
          "its own tree reaches (log 040 decision 51)" % K)
    ag_reach = sorted(achievable(agree["merge_history"], n))
    near = [c for c in ag_reach if c <= 40]
    print("  the coarse counts each tree can stand in at all, up to 40:")
    for nm, h in (("product", prod_hist), ("agreement",
                                           agree["merge_history"]),
                  ("containment", contain["merge_history"]),
                  ("domain_only", domain["merge_history"])):
        r = [c for c in sorted(achievable(h, n)) if c <= 40]
        print("    %-12s %s" % (nm, ", ".join(str(c) for c in r)))
    print("  the agreement tree steps from %d groups straight to %d: "
          "there is no threshold at which it stands in %d"
          % (near[1] if len(near) > 1 else near[0], near[0], K))
    print("  %-12s %6s %8s %8s %8s %7s %6s"
          % ("reading", "groups", "same-lang", "same-fam", "1-lang",
             "largest", "1-leaf"))
    sortrows = {}
    for nm in ("product", "agreement", "containment", "domain_only"):
        g = cuts[nm]
        st = sorting(g)
        st["groups"] = len(g)
        sortrows[nm] = st
        print("  %-12s %6d %8.3f %8.3f %8d %7d %6d"
              % (nm, len(g), st["same_language_rate"],
                 st["same_family_rate"], st["single_language_groups"],
                 st["largest_group"], st["singletons"]))

    # --- the two-tree disagreement ------------------------------------
    # Reading #1 against reading #3, pair for pair, both cut to K groups.
    # A pair the agreement tree puts TOGETHER and the domain tree puts
    # APART is the CORE's `nests' arm seen directly: the two answer alike
    # wherever both answer, and they sit apart only because one accepts
    # more.
    ga, gd = cuts["agreement"], cuts["domain_only"]
    la = {k: i for i, g in enumerate(ga) for k in g}
    ld = {k: i for i, g in enumerate(gd) for k in g}
    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = keys[i], keys[j]
            ta, td = la[a] == la[b], ld[a] == ld[b]
            if ta == td:
                continue
            rows.append(dict(
                left=a, right=b,
                together_in="agreement" if ta else "domain",
                A=round(float(A[i, j]), 6), J=round(float(J[i, j]), 6),
                C=round(float(C[i, j]), 6),
                product=round(float(J[i, j] * A[i, j]), 6),
                shared_inputs=int(SH[i, j]),
                supported=bool(sup[i, j]),
                domain_left=len(dom[i]), domain_right=len(dom[j]),
                nests=bool(dom[i] <= dom[j] or dom[j] <= dom[i]),
                same_language=(a.split(".")[0] == b.split(".")[0])))
    nest_rows = [r for r in rows if r["nests"]]
    nest_rows.sort(key=lambda r: (-r["A"], -r["shared_inputs"]))
    rows.sort(key=lambda r: (-r["A"], -r["shared_inputs"]))
    print("")
    print("two-tree disagreement, agreement tree against domain tree, "
          "both cut to %d groups:" % K)
    print("  %d pairs placed differently by the two trees" % len(rows))
    print("  %d of them are a true DOMAIN CONTAINMENT -- one domain "
          "inside the other" % len(nest_rows))
    tg = sum(1 for r in rows if r["together_in"] == "agreement")
    print("  %d together only in the agreement tree, %d only in the "
          "domain tree" % (tg, len(rows) - tg))
    print("")
    print("  the ten containment pairs with the highest agreement:")
    for r in nest_rows[:10]:
        print("    %-18s %-18s A %.3f  J %.3f  product %.3f  cells %d"
              % (r["left"], r["right"], r["A"], r["J"], r["product"],
                 r["shared_inputs"]))

    # --- the watched pairs --------------------------------------------
    # `go.+' against `java.+' is the standing case for the product's
    # bias: log 033 item 4x measured A exactly 1.000 and a product of
    # 0.094.  Where the pair LANDS in each reading is the direct test,
    # so it is printed rather than left to be looked up.
    idx = {k: i for i, k in enumerate(keys)}
    watch = [("go.+", "java.+"), ("go.+", "rust.+"), ("go.+", "cpp.+"),
             ("java.+", "cpp.+"), ("java.+", "csharp.+"),
             ("go.&&", "java.&&"), ("go.==", "java.=="),
             ("go.<<", "java.<<")]
    wrows = []
    print("")
    print("the watched pairs -- where a wide-domain leaf lands against a "
          "narrow one that never disagrees with it")
    print("    %-9s %-9s %6s %6s %6s %7s %6s  %s"
          % ("left", "right", "A", "J", "C", "product", "cells",
             "together at %d groups" % K))
    for a, b in watch:
        if a not in idx or b not in idx:
            continue
        i, j = idx[a], idx[b]
        tog = {nm: (("%s" % ("yes" if
                             {k: q for q, g in enumerate(cuts[nm])
                              for k in g}[a]
                             == {k: q for q, g in enumerate(cuts[nm])
                                 for k in g}[b] else "no")))
               for nm in ("product", "agreement", "containment",
                          "domain_only")}
        wrows.append(dict(left=a, right=b, A=round(float(A[i, j]), 6),
                          J=round(float(J[i, j]), 6),
                          C=round(float(C[i, j]), 6),
                          product=round(float(J[i, j] * A[i, j]), 6),
                          shared_inputs=int(SH[i, j]), together=tog,
                          domain_left=len(dom[i]),
                          domain_right=len(dom[j]),
                          nests=bool(dom[i] <= dom[j]
                                     or dom[j] <= dom[i])))
        print("    %-9s %-9s %6.3f %6.3f %6.3f %7.3f %6d  "
              "product %s / agreement %s / containment %s / domain %s"
              % (a, b, A[i, j], J[i, j], C[i, j], J[i, j] * A[i, j],
                 SH[i, j], tog["product"], tog["agreement"],
                 tog["containment"], tog["domain_only"]))

    json.dump(dict(status="TWO-TREE DISAGREEMENT, OPERATORS",
                   built="2026-08-20",
                   extends=["clusters_agreement.json",
                            "clusters_domain.json"],
                   matched_groups=K,
                   matched_granularity_note=(
                       "log 040 decision 51: two trees are compared cut "
                       "to the same number of groups, and K is the "
                       "product tree's own widest non-degenerate "
                       "plateau count"),
                   sorting=sortrows,
                   groups_at_K={nm: cuts[nm] for nm in cuts},
                   n_disagreeing_pairs=len(rows),
                   n_containment_pairs=len(nest_rows),
                   together_in_agreement_only=tg,
                   together_in_domain_only=len(rows) - tg,
                   watched_pairs=wrows,
                   pairs=rows[:400], containment_pairs=nest_rows[:200]),
              open(os.path.join(HERE, "two_tree_disagreement.json"), "w"),
              indent=1, sort_keys=True)
    print("")
    print("wrote two_tree_disagreement.json")

    # --- the headline comparison --------------------------------------
    print("")
    print("the four readings at their own widest non-degenerate plateau")
    print("  product      [%.3f, %.3f) -> %3d clusters"
          % (prod_w["low"], prod_w["high"], prod_w["clusters"]))
    for nm, b in (("agreement", agree), ("containment", contain),
                  ("domain-only", domain)):
        w = b["widest_plateau"]
        print("  %-12s [%.3f, %.3f) -> %3d clusters"
              % (nm, w["low"], w["high"], w["clusters"]))


if __name__ == "__main__":
    main()
