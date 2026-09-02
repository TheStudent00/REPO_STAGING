#!/usr/bin/env python3
"""l3_dominance.py -- the owner's dominance paradigm, built as its own reading.

the owner sketched it on 2026-08-20, verbatim:

    "the paradigm could be about the dominant vectors. if an element is
    non-zero, what others have that non-zero element. and for each of
    those others, what are their non-zero elements and what others share
    non-zero elements. does that tree flatten into a dominant vector."

Read against this node's data the sketch is exact.  Every operation
signature IS a vector over the shared 64-cell form grid, and a cell is
NON-ZERO when the operation accepts it.  "What others have that
non-zero element" is the set of operations whose domain also contains
that cell.  Following that outward from one operation, and outward
again from each operation it reaches, is the CONTAINMENT ORDER, and
asking whether it flattens is asking whether that order has a TOP.

The CORE already names the arm this belongs to.  Its trichotomy calls
a pair NESTS when one has the same answers over a wider domain, and it
says in as many words that nests IS dominance, discovered rather than
assumed.  So the order is built twice here and the two are not mixed:

  the CONTAINMENT ORDER   X sits below Y when every cell X accepts, Y
                          accepts.  Domains only.  Answers not
                          consulted.
  the DOMINANCE ORDER     X sits below Y when X sits below Y in the
                          containment order AND the two never disagree
                          on a cell they share.  This is the CORE's
                          `nests', and it is the order the owner's question
                          is really about, because a wider domain that
                          answers differently does not dominate
                          anything -- it contradicts it.

No probe runs.  No lane runs.  Everything is read from
`clusters_all12.json' and from log 041's `clusters_agreement.json'
support rule.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_alt_readings as R                                  # noqa: E402

# --- decision 56 ------------------------------------------------------
# When does one signature DOMINATE another.
#
# X is dominated by Y when three things hold at once:
#   1. every cell X accepts, Y accepts, and Y accepts at least one more;
#   2. the pair is SUPPORTED under decision 55, so an agreement rate was
#      measured at all;
#   3. that rate is exactly 1.000 -- the two never once disagree.
#
# Why exactly 1.000 and not a high threshold.  Dominance is the CORE's
# `nests' arm, and the CORE's wording is "same answers, wider domain".
# A single disagreeing cell is a measured counter-example to sameness.
# Allowing 0.99 would let one signature dominate another it demonstrably
# contradicts somewhere, which is the thing the trichotomy exists to
# keep apart.  The looser reading is computed anyway and printed beside
# it, so the cost of the strictness is visible rather than argued.
CLEAN = 1.0
LOOSE = 0.99

# --- decision 57 ------------------------------------------------------
# The containment lattice is drawn over DOMAIN CLASSES -- the groups of
# leaves whose domains are identical -- and not over leaves.  238 leaves
# carry 59 distinct domains, so a leaf-wise drawing would place 179
# nodes on top of others at the same point with the same edges.  The
# dominance order is computed over LEAVES and never over classes,
# because two leaves with one domain can answer differently, and that
# difference is exactly what dominance turns on.
#
# Cost to overturn: draw the lattice leaf-wise, which is a change of one
# grouping call.
FAMILIES = ["arithmetic", "comparison", "logical", "bitwise", "shift",
            "other"]


def load():
    data = R.load()
    keys = R.leaf_keys(data)
    J, A, C, SH, doml = R.matrices(data, keys)
    dom = {k: frozenset(data["signatures"][k]["domain"]) for k in keys}
    fam = {k: R.family(k.split(".", 1)[1]) for k in keys}
    return data, keys, A, SH, dom, fam


def classes(keys, dom, subset=None):
    """domain -> the leaves carrying exactly that domain."""
    out = collections.defaultdict(list)
    for k in (subset if subset is not None else keys):
        out[dom[k]].append(k)
    return {d: sorted(v) for d, v in out.items()}


def hasse(nodes):
    """the cover relation of set containment over `nodes'.

    An edge X -> Y is drawn only when X is inside Y and nothing sits
    strictly between them.  Removing the edges that follow from other
    edges is what makes the picture readable and it is the whole
    definition of a Hasse diagram.
    """
    below = {x: [y for y in nodes if x < y] for x in nodes}
    edges = []
    for x in nodes:
        for y in below[x]:
            if any(z < y for z in below[x] if x < z):
                continue
            edges.append((x, y))
    return edges


def maximal(nodes):
    return [x for x in nodes if not any(x < y for y in nodes)]


def dominance(keys, dom, A, SH, idx, thr=CLEAN):
    """leaf -> the leaves that DOMINATE it, under decision 56."""
    up = {k: [] for k in keys}
    pairs = 0
    for x in keys:
        for y in keys:
            if x == y or not (dom[x] < dom[y]):
                continue
            i, j = idx[x], idx[y]
            if SH[i][j] < R.SUPPORT:
                continue
            pairs += 1
            if A[i][j] >= thr:
                up[x].append(y)
    return up, pairs


def report_family(name, ks, dom, A, SH, idx, keys):
    cls = classes(keys, dom, ks)
    nodes = sorted(cls, key=lambda d: (-len(d), sorted(d)))
    mx = maximal(nodes)
    union = set().union(*nodes) if nodes else set()
    top = mx[0] if len(mx) == 1 else None
    up, _ = dominance(ks, dom, A, SH, idx)
    dmax = sorted(k for k in ks if not up[k])
    return dict(family=name, leaves=len(ks), classes=len(nodes),
                containment_maximal=len(mx),
                containment_top=(sorted(cls[top]) if top else None),
                containment_top_cells=(len(top) if top else None),
                union_cells=len(union),
                union_is_a_member=bool(any(frozenset(union) == d
                                           for d in nodes)),
                dominance_maximal=len(dmax),
                dominance_maximal_leaves=dmax[:40],
                largest_class=max((len(d) for d in nodes), default=0),
                edges=hasse(nodes), nodes=nodes, class_members=cls,
                maximal_nodes=mx)


def maximal_pairs(mx_leaves, dom, A, SH, idx, fam):
    """the maximal elements set against one another.

    Two maximal elements cannot contain one another, by definition.  So
    the only question left about them is whether their answers can be
    put together.  Three verdicts, and the boundary of each is stated:

      union candidate  they overlap, the pair is supported, and they
                       never disagree -- one operation could carry both
                       domains.
      fork             they overlap, the pair is supported, and they
                       disagree on every shared cell -- no operation
                       can carry both.
      partial          they overlap and disagree on some cells and not
                       others.
      disjoint / thin  they share no cell, or too few for decision 55.
    """
    out = []
    for i in range(len(mx_leaves)):
        for j in range(i + 1, len(mx_leaves)):
            a, b = mx_leaves[i], mx_leaves[j]
            ia, ib = idx[a], idx[b]
            shared = dom[a] & dom[b]
            sh = int(SH[ia][ib])
            ag = float(A[ia][ib])
            if not shared:
                v = "disjoint"
            elif sh < R.SUPPORT:
                v = "thin"
            elif ag >= CLEAN:
                v = "union candidate"
            elif ag == 0.0:
                v = "fork"
            else:
                v = "partial"
            out.append(dict(left=a, right=b, verdict=v,
                            shared_cells=len(shared), shared_inputs=sh,
                            agreement=round(ag, 6),
                            union_cells=len(dom[a] | dom[b]),
                            same_family=(fam[a] == fam[b]),
                            family=(fam[a] if fam[a] == fam[b] else None),
                            same_language=(a.split(".")[0]
                                           == b.split(".")[0])))
    return out


def main():
    data, keys, A, SH, dom, fam = load()
    idx = {k: i for i, k in enumerate(keys)}
    n = len(keys)
    print("leaves: %d   distinct domains: %d   grid: %d cells"
          % (n, len(classes(keys, dom)), data["shared_space_cells"]))
    print("decision 56: dominance is containment PLUS an agreement rate "
          "of exactly %.3f on the shared cells" % CLEAN)
    print("decision 57: the lattice is drawn over the %d domain classes, "
          "the dominance order is computed over the %d leaves"
          % (len(classes(keys, dom)), n))

    # --- the containment order, overall -------------------------------
    allcls = classes(keys, dom)
    nodes = sorted(allcls, key=lambda d: (-len(d), sorted(d)))
    mx = maximal(nodes)
    print("")
    print("THE CONTAINMENT ORDER, all 238 leaves in one lattice")
    print("  %d classes, %d maximal" % (len(nodes), len(mx)))
    if len(mx) == 1:
        t = mx[0]
        print("  it FLATTENS: there is exactly ONE top, a class of %d "
              "cells carrying %d leaves" % (len(t), len(allcls[t])))
        print("  the top: %s" % ", ".join(sorted(allcls[t])[:8]))
        print("           ... %d leaves in all" % len(allcls[t]))

    # --- the dominance order, overall ---------------------------------
    up, cpairs = dominance(keys, dom, A, SH, idx)
    upl, _ = dominance(keys, dom, A, SH, idx, LOOSE)
    dmax = sorted(k for k in keys if not up[k])
    dmaxl = sorted(k for k in keys if not upl[k])
    clean_edges = sum(len(v) for v in up.values())
    print("")
    print("THE DOMINANCE ORDER, the same leaves under decision 56")
    print("  %d ordered pairs are a strict containment AND supported"
          % cpairs)
    print("  %d of them never disagree once -- those are the dominance "
          "relations" % clean_edges)
    print("  %d leaves are MAXIMAL: nothing dominates them" % len(dmax))
    print("  at the looser %.2f reading it would be %d maximal leaves"
          % (LOOSE, len(dmaxl)))
    print("  so the order does NOT flatten: a dominant vector would "
          "leave exactly one")

    # --- per family ----------------------------------------------------
    byfam = collections.defaultdict(list)
    for k in keys:
        byfam[fam[k]].append(k)
    rows = []
    print("")
    print("PER FAMILY")
    print("  %-11s %6s %7s %8s %8s %6s %9s"
          % ("family", "leaves", "classes", "cont-max", "top cells",
             "union", "dom-max"))
    for f in FAMILIES:
        if f not in byfam:
            continue
        r = report_family(f, sorted(byfam[f]), dom, A, SH, idx, keys)
        rows.append(r)
        print("  %-11s %6d %7d %8d %8s %6d %9d"
              % (f, r["leaves"], r["classes"], r["containment_maximal"],
                 (str(r["containment_top_cells"])
                  if r["containment_top_cells"] else "none"),
                 r["union_cells"], r["dominance_maximal"]))

    # --- the maximal elements against one another ---------------------
    print("")
    print("THE MAXIMAL ELEMENTS SET AGAINST ONE ANOTHER (dominance "
          "order, overall)")
    mp = maximal_pairs(dmax, dom, A, SH, idx, fam)
    vc = collections.Counter(r["verdict"] for r in mp)
    for v in ("union candidate", "partial", "fork", "thin", "disjoint"):
        print("  %-16s %5d" % (v, vc[v]))
    # Cross-family pairs are counted but never headlined: `php.!=' against
    # `python.%' is a comparison set against an arithmetic, and their
    # disagreeing is a restatement of their being different operations
    # rather than a finding about either.  The readable population is
    # WITHIN one family.
    inf = [r for r in mp if r["same_family"]]
    vcf = collections.Counter(r["verdict"] for r in inf)
    print("")
    print("  within ONE family only, which is the readable population:")
    for v in ("union candidate", "partial", "fork", "thin", "disjoint"):
        print("    %-16s %5d" % (v, vcf[v]))
    forks = sorted((r for r in inf if r["verdict"] == "fork"),
                   key=lambda r: -r["shared_cells"])
    cands = sorted((r for r in inf if r["verdict"] == "union candidate"),
                   key=lambda r: (r["same_language"], -r["shared_cells"]))
    print("")
    print("  the ten widest UNION CANDIDATES within a family -- maximal "
          "elements that never disagree, cross-language first")
    for r in cands[:10]:
        print("    %-20s %-20s %-11s %3d cells shared, union %d%s"
              % (r["left"], r["right"], r["family"], r["shared_cells"],
                 r["union_cells"],
                 "   same language" if r["same_language"] else ""))
    print("")
    print("  the ten widest FORKS within a family -- maximal elements "
          "that disagree on every shared cell")
    for r in forks[:10]:
        print("    %-20s %-20s %-11s %3d cells shared, %5d input cells%s"
              % (r["left"], r["right"], r["family"], r["shared_cells"],
                 r["shared_inputs"],
                 "   same language" if r["same_language"] else ""))

    # --- the union vector ----------------------------------------------
    uni = set()
    for k in dmax:
        uni |= dom[k]
    print("")
    print("THE UNION VECTOR over the %d maximal leaves: %d of %d cells"
          % (len(dmax), len(uni), data["shared_space_cells"]))
    covered = [k for k in dmax if dom[k] == frozenset(uni)]
    print("  a single maximal leaf already carrying the whole union: %s"
          % (", ".join(sorted(covered)[:6]) if covered else "none"))

    out = dict(status="DOMINANCE LATTICE, OPERATORS, ALL TWELVE",
               built="2026-08-20",
               extends=["clusters_all12.json", "clusters_agreement.json"],
               dee_sketch=("the paradigm could be about the dominant "
                           "vectors. if an element is non-zero, what "
                           "others have that non-zero element. and for "
                           "each of those others, what are their "
                           "non-zero elements and what others share "
                           "non-zero elements. does that tree flatten "
                           "into a dominant vector."),
               decision_56=("dominance is strict domain containment plus "
                            "a supported agreement rate of exactly "
                            "1.000; a single disagreeing cell refutes "
                            "it"),
               decision_57=("the containment lattice is drawn over "
                            "domain classes and the dominance order is "
                            "computed over leaves"),
               grid_cells=data["shared_space_cells"],
               n_leaves=n, n_classes=len(nodes),
               containment_maximal=len(mx),
               containment_top_members=(sorted(allcls[mx[0]])
                                        if len(mx) == 1 else None),
               containment_top_cells=(len(mx[0]) if len(mx) == 1
                                      else None),
               containment_ordered_pairs=cpairs,
               dominance_edges=clean_edges,
               dominance_maximal=len(dmax),
               dominance_maximal_leaves=dmax,
               dominance_maximal_loose=len(dmaxl),
               union_vector_cells=len(uni),
               union_vector=sorted(uni),
               union_carried_by_one_leaf=sorted(covered),
               maximal_pair_verdicts=dict(vc),
               maximal_pair_verdicts_within_family=dict(vcf),
               union_candidates_within_family=cands,
               forks_within_family=forks[:120],
               maximal_pairs=mp,
               families=[{k: v for k, v in r.items()
                          if k not in ("edges", "nodes", "class_members",
                                       "maximal_nodes")}
                         for r in rows])
    json.dump(out, open(os.path.join(HERE, "dominance_lattice.json"), "w"),
              indent=1, sort_keys=True)
    print("")
    print("wrote dominance_lattice.json")
    return dict(data=data, keys=keys, dom=dom, fam=fam, A=A, SH=SH,
                idx=idx, rows=rows, allcls=allcls, dmax=dmax, up=up,
                report=out)


if __name__ == "__main__":
    main()
