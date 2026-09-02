#!/usr/bin/env python3
"""make_union_candidates.py -- union_candidates.md, the Hub-facing
readable product of log 043.

The question it answers, in the owner's terms: the order has many maximal
elements rather than one, so no single operation carries the node.  Can
several be LAID ON TOP of one another to make one?  Two maximal leaves
can when they never differ on an element they both speak on -- then the
combined vector is still a function from elements to answer tokens, and
neither leaf has to give up a measured answer.

Two edges count as compatible and the difference is marked rather than
hidden:

  agreeing   the two share elements and carry the same token on every
             one of them.  Real evidence that they are one operation.
  vacuous    the two share no element at all.  They cannot contradict,
             but nothing was measured either.  A union across a vacuous
             edge is an assembly, not a discovery.

Compatibility is pairwise and that is enough for a group of any size: a
union of vectors fails to be a function exactly when SOME TWO of them
differ on a shared element.  So the assemblies are the maximal cliques
of the compatibility graph, and they are enumerated exactly rather than
approximated -- the graphs here run to tens of nodes, so Bron-Kerbosch
with a pivot finishes instantly.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_dominance_vg as D                                   # noqa: E402

COMPATIBLE = ("union candidate", "disjoint")


def cliques(nodes, adj):
    """every maximal clique, Bron-Kerbosch with a pivot."""
    out = []

    def bk(r, p, x):
        if not p and not x:
            out.append(sorted(r))
            return
        piv = max(p | x, key=lambda v: len(adj[v] & p))
        for v in sorted(p - adj[piv]):
            bk(r | {v}, p & adj[v], x & adj[v])
            p = p - {v}
            x = x | {v}
    bk(set(), set(nodes), set())
    return sorted(out, key=lambda c: -len(c))


def cell(s):
    """a table cell.  An element key carries pipes -- the grid's own
    separator is `|' -- and a pipe inside a pipe table ends the cell, so
    it is escaped here and nowhere else."""
    return str(s).replace("|", "\\|")


def coverage(vec, group):
    u = set()
    for k in group:
        u |= set(vec[k])
    return len(u)


def main():
    ctx = D.main()
    vec, sig, fam = ctx["vec"], ctx["sig"], ctx["fam"]
    rep = ctx["report"]
    grid = sig["n_cells"]
    L = []
    w = L.append
    w("# union candidates at the value grain")
    w("")
    w("Built 2026-08-20 by `make_union_candidates.py`, from")
    w("`dominance_valuegrain.json`. Nothing was run to produce it.")
    w("")
    w("This is the Hub-facing half of log 043. The order rebuilt at the")
    w("value grain has **%d maximal leaves of %d**, so there is no one"
      % (rep["maximal"], rep["n_leaves"]))
    w("operation that carries the node. What follows is the next")
    w("question: which maximal operations can be laid on top of one")
    w("another without either giving up a measured answer.")
    w("")
    w("Two leaves are COMPATIBLE when they never carry different tokens")
    w("on an element they both speak on. Two kinds of compatible edge,")
    w("and the difference matters to anyone reading this as evidence:")
    w("")
    w("| edge | meaning | what it is worth |")
    w("|---|---|---|")
    w("| agreeing | they share elements and agree on every one | "
      "measured sameness |")
    w("| vacuous | they share no element at all | assembly, not "
      "evidence |")
    w("")
    w("A union of any size is possible exactly when every PAIR in it is")
    w("compatible, so the assemblies below are the maximal cliques of")
    w("that graph, enumerated exactly.")
    w("")
    w("Coverage is elements out of the %d in the merged grid." % grid)
    w("")

    summary = []
    detail = []
    for f in D.FAMILIES:
        row = next((r for r in rep["families"] if r["family"] == f), None)
        if row is None:
            continue
        mx = row["maximal_leaves"]
        verd = {(r["left"], r["right"]): r
                for r in ctx["family_verdicts"][f]}
        adj = {k: set() for k in mx}
        for (a, b), r in verd.items():
            if r["verdict"] in COMPATIBLE:
                adj[a].add(b)
                adj[b].add(a)
        # A one-member clique is not an assembly, and every family has
        # one that covers the whole grid on its own -- `php.%' does,
        # which is exactly the god-operator shape the owner's ruling was
        # aimed at, appearing again in a different table.  So the
        # assembly reported is the widest-covering clique of TWO OR
        # MORE, and a family with none is told so in as many words.
        cl = cliques(mx, adj)
        multi = [c for c in cl if len(c) > 1]
        best = (max(multi, key=lambda c: (coverage(vec, c), len(c)))
                if multi else [])
        cov = coverage(vec, best) if best else 0
        agreeing = sum(1 for r in verd.values()
                       if r["verdict"] == "union candidate")
        vacuous = sum(1 for r in verd.values()
                      if r["verdict"] == "disjoint")
        blocked = sum(1 for r in verd.values()
                      if r["verdict"] in ("fork", "partial"))
        summary.append((f, row["leaves"], row["maximal"], agreeing,
                        vacuous, blocked, len(best), cov))

        detail.append("## %s" % f)
        detail.append("")
        detail.append("%d leaves, %d of them maximal. Compatible pairs: "
                      "%d agreeing," % (row["leaves"], row["maximal"],
                                        agreeing))
        detail.append("%d vacuous. Blocked pairs: %d."
                      % (vacuous, blocked))
        detail.append("")
        cand = sorted((r for r in verd.values()
                       if r["verdict"] == "union candidate"),
                      key=lambda r: (r["same_language"],
                                     -r["shared_elements"]))
        if cand:
            detail.append("The agreeing pairs, cross-language first.")
            detail.append("")
            detail.append("| left | right | shared elements | union "
                          "elements | |")
            detail.append("|---|---|---|---|---|")
            for r in cand[:24]:
                detail.append("| `%s` | `%s` | %d | %d | %s |"
                              % (r["left"], r["right"],
                                 r["shared_elements"],
                                 r["union_elements"],
                                 "same language" if r["same_language"]
                                 else "cross-language"))
        else:
            detail.append("**No agreeing pair at all.** Every pair of "
                          "maximal leaves in")
            detail.append("this family either contradicts the other "
                          "somewhere or shares no")
            detail.append("element with it.")
        detail.append("")
        if best:
            ag = va = 0
            for i in range(len(best)):
                for jx in range(i + 1, len(best)):
                    r = (verd.get((best[i], best[jx]))
                         or verd.get((best[jx], best[i])))
                    if r["verdict"] == "union candidate":
                        ag += 1
                    else:
                        va += 1
            detail.append("The widest assembly of two or more: %d "
                          "maximal leaves covering" % len(best))
            detail.append("%d of %d elements, on %d agreeing and %d "
                          "vacuous edges." % (cov, grid, ag, va))
            detail.append("")
            detail.append("```")
            for i in range(0, len(best), 2):
                detail.append("  " + "  ".join(best[i:i + 2])[:53])
            detail.append("```")
            detail.append("")
        else:
            detail.append("**No assembly of two or more exists here.** "
                          "Every pair of maximal")
            detail.append("leaves in this family blocks, so nothing can "
                          "be laid on top of")
            detail.append("anything else.")
            detail.append("")
        blk = sorted((r for r in verd.values()
                      if r["verdict"] in ("fork", "partial")
                      and r["blocked_by"]),
                     key=lambda r: (r["same_language"],
                                    -r["shared_elements"]))
        if blk:
            detail.append("The blocked unions, with one blocking "
                          "element quoted each.")
            detail.append("")
            detail.append("| left | right | blocking element | left "
                          "answers | right answers |")
            detail.append("|---|---|---|---|---|")
            for r in blk[:20]:
                b = r["blocked_by"][0]
                detail.append("| `%s` | `%s` | `%s` | `%s` | `%s` |"
                              % (r["left"], r["right"],
                                 cell(b["element"]),
                                 cell(", ".join(b["left"])[:46]),
                                 cell(", ".join(b["right"])[:46])))
            detail.append("")

    w("## the headline, per family")
    w("")
    w("| family | leaves | maximal | agreeing pairs | vacuous pairs | "
      "blocked pairs | widest assembly | its coverage |")
    w("|---|---|---|---|---|---|---|---|")
    for r in summary:
        w("| %s | %d | %d | %d | %d | %d | %d | %d of %d |"
          % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], grid))
    w("")
    tot_agree = sum(r[3] for r in summary)
    tot_block = sum(r[5] for r in summary)
    w("**%d agreeing pairs against %d blocked, within a family.** The "
      % (tot_agree, tot_block))
    w("agreeing pairs are the whole short list of places where two "
      "maximal")
    w("operations could be one operation, and they are the answer this")
    w("log hands the Hub.")
    w("")
    L.extend(detail)
    p = os.path.join(HERE, "union_candidates.md")
    open(p, "w").write("\n".join(L) + "\n")
    print("")
    print("wrote union_candidates.md (%d lines)" % len(L))
    print("")
    print("| family | maximal | agreeing | vacuous | blocked | assembly "
          "| coverage |")
    print("|---|---|---|---|---|---|---|")
    for r in summary:
        print("| %s | %d | %d | %d | %d | %d | %d of %d |"
              % (r[0], r[2], r[3], r[4], r[5], r[6], r[7], grid))


if __name__ == "__main__":
    main()
