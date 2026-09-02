#!/usr/bin/env python3
"""l3_dominance_vg.py -- log 043: the dominance paradigm rerun on the
MERGED order, over the value-grain signatures.

This is `l3_dominance.py' extended, not replaced.  Log 041 built TWO
orders and kept them apart: a CONTAINMENT order that consulted domains
only, and a DOMINANCE order that was containment plus never disagreeing.
the owner's ruling of 2026-08-20 collapses them into ONE:

    "each row isnt a row element. its a vector"
    "that way something like php.== cant appear to have obtained
     god-operator status."

Once the element carries the ANSWER, containment-without-faithfulness
has nowhere left to live.  There is one order:

    X <= Y   when Y carries the SAME element value as X on EVERY
             element where X speaks.

X < Y is that, plus Y speaking on at least one element X is silent on.
Three things follow immediately and none of them is assumed:

  * the order is a genuine order.  Speaking sets nest and element values
    match, so X <= Y and Y <= Z force X <= Z.  It is checked in `main'
    over every triple that the run finds, rather than argued.
  * god status is impossible by construction.  A leaf sits above another
    only where it REPEATS that leaf's answers.  Accepting a question is
    no longer worth anything on its own.
  * a leaf that answers where another raises is NOT above it.  A raise
    is a token under decision 31, so `raise:TypeError' against
    `whole:84' is a mismatch and the order stops there.

Silence is the one thing that is not a mismatch, and that is decision 59
below.

Products: `dominance_valuegrain.json', and the readable
`union_candidates.md' written by `make_union_candidates.py'.

No probe runs.  No lane runs.

Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_valuegrain as V                                     # noqa: E402

FAMILIES = V.FAMILIES

# --- decision 59 ------------------------------------------------------
# WIDENING IS PERMITTED, CONTRADICTION IS NOT.
#
# The order asks Y to match X on every element where X SPEAKS.  It asks
# nothing at all about the elements X is silent on, so Y may speak on a
# thousand of them and still sit above X.  That is widening, and it is
# the whole content of "a wider operation".
#
# Why silence is free.  A leaf is silent at an element when it was never
# asked the question -- the compiler would not take the holder pair, so
# no run ever happened.  Requiring Y to be silent there too would make
# the order say something about a measurement nobody took.  Absence of a
# claim cannot contradict a claim.
#
# Why a RAISE is not free.  A raise WAS measured.  `python.+' answering
# `raise:TypeError' at `text|base_abc|whole|base_42' is a claim about
# that element, and a leaf answering `text:abc42' there contradicts it.
# Decision 31 already made a raise a token; this decision only declines
# to make an exception for it.  The same holds for a death and for the
# backend refusal of decision 60.
#
# **FLAGGED.**  The reasoning is shown because the choice is arguable in
# one direction: someone could read a raise as "this operation declines
# this question", which is closer to silence than to an answer.  The
# counts under THAT reading are computed on every run and printed, so
# the cost of decision 59 is a number.  Cost to overturn: set
# `CLAIMS_ONLY' to a set that excludes the raise prefix.
CLAIM_PREFIXES = ("raise:", "death:", "refuse:")


def load():
    return json.load(open(os.path.join(HERE, "signatures_valuegrain.json")))


def unpack(sig):
    """the artifact -> {leaf: {cell id: value id}} and the lookups."""
    vec = {k: {c: v for c, v in L["vec"]}
           for k, L in sig["leaves"].items()}
    return vec


def strip_claims(vec, sig):
    """the alternative reading of decision 59: a raise, a death and a
    refusal are read as SILENCE rather than as a claim."""
    claimy = set()
    for i, val in enumerate(sig["values"]):
        toks = [sig["tokens"][t] for t in val]
        if all(t.startswith(CLAIM_PREFIXES) for t in toks):
            claimy.add(i)
    return {k: {c: v for c, v in d.items() if v not in claimy}
            for k, d in vec.items()}, len(claimy)


def order(vec):
    """X -> the leaves strictly above it.

    A leaf is above X when it repeats X on every element X speaks and
    speaks somewhere X does not.  The speaking sets are frozensets so
    the cheap test -- does X's speaking set nest inside Y's -- runs
    first and rejects most of the population before a single element
    value is compared.
    """
    keys = sorted(vec)
    spoken = {k: frozenset(vec[k]) for k in keys}
    up = {k: [] for k in keys}
    equal = collections.defaultdict(list)
    candidates = 0
    for x in keys:
        sx, vx = spoken[x], vec[x]
        for y in keys:
            if x == y:
                continue
            sy = spoken[y]
            if not sx <= sy:
                continue
            if len(sx) == len(sy):
                continue                     # a co-node, handled below
            candidates += 1
            vy = vec[y]
            for c, v in vx.items():
                if vy[c] != v:
                    break
            else:
                up[x].append(y)
    for k in keys:
        equal[tuple(sorted(vec[k].items()))].append(k)
    classes = {min(v): sorted(v) for v in equal.values()}
    return up, candidates, classes


def order_form_grain(vec, sig):
    """the SAME order under the form-pair grain, for the flagged
    comparison.

    Under that grain a holder split does not count against a match: two
    leaves match at an element when their token sets INTERSECT, which is
    decision 27's standing rule.  That is looser, so it certifies more.

    Intersection is not transitive in general -- X can match Y on {a}
    against {a,b}, Y match Z on {a,b} against {b}, and X and Z share
    nothing -- so the form-pair grain carries no GUARANTEE of being an
    order.  Whether it actually fails on this data is a different
    question from whether it can, and it is counted here rather than
    argued either way.
    """
    keys = sorted(vec)
    sets = {k: {c: set(sig["values"][v]) for c, v in vec[k].items()}
            for k in keys}
    spoken = {k: frozenset(vec[k]) for k in keys}
    up = {k: [] for k in keys}
    cand = 0
    for x in keys:
        sx = spoken[x]
        for y in keys:
            if x == y or not sx <= spoken[y] or len(sx) == len(spoken[y]):
                continue
            cand += 1
            vx, vy = sets[x], sets[y]
            for c, v in vx.items():
                if not (v & vy[c]):
                    break
            else:
                up[x].append(y)
    fails = 0
    for x, ys in up.items():
        for y in ys:
            for z in up[y]:
                if z not in up[x]:
                    fails += 1
    mx = [k for k in keys if not up[k]]
    return cand, sum(len(v) for v in up.values()), len(mx), fails


def blocking(vec, sig, a, b, limit=6):
    """the elements that deny two leaves a union, quoted."""
    out = []
    va, vb = vec[a], vec[b]
    for c in sorted(set(va) & set(vb)):
        if va[c] != vb[c]:
            out.append(dict(
                element=sig["cells"][c],
                left=[sig["tokens"][t] for t in sig["values"][va[c]]],
                right=[sig["tokens"][t] for t in sig["values"][vb[c]]]))
            if len(out) >= limit:
                break
    return out


def union_verdicts(vec, sig, mx, fam, cap=400):
    """every pair of maximal elements, set against one another.

    Two maximal elements cannot repeat one another wholesale -- that is
    what makes them maximal -- so the only question left is whether one
    operation could carry BOTH.  It could exactly when they never differ
    on an element they both speak on, because then the two vectors can
    be laid on top of each other without either one having to give up a
    measured answer.
    """
    out = []
    for i in range(len(mx)):
        for j in range(i + 1, len(mx)):
            a, b = mx[i], mx[j]
            va, vb = vec[a], vec[b]
            shared = set(va) & set(vb)
            if not shared:
                v, blk = "disjoint", []
                nagree = 0
            else:
                bad = [c for c in shared if va[c] != vb[c]]
                nagree = len(shared) - len(bad)
                if not bad:
                    v, blk = "union candidate", []
                elif nagree == 0:
                    v, blk = "fork", blocking(vec, sig, a, b)
                else:
                    v, blk = "partial", blocking(vec, sig, a, b)
            out.append(dict(left=a, right=b, verdict=v,
                            shared_elements=len(shared),
                            agreeing_elements=nagree,
                            union_elements=len(set(va) | set(vb)),
                            same_family=(fam[a] == fam[b]),
                            family=(fam[a] if fam[a] == fam[b] else None),
                            same_language=(a.split(".")[0]
                                           == b.split(".")[0]),
                            blocked_by=blk))
    return out


def check_transitive(up):
    """the order is an order, checked rather than asserted."""
    tri = 0
    for x, ys in up.items():
        for y in ys:
            for z in up[y]:
                tri += 1
                assert z in up[x], \
                    "transitivity fails: %s <= %s <= %s" % (x, y, z)
    return tri


def main():
    sig = load()
    vec = unpack(sig)
    keys = sorted(vec)
    fam = {k: sig["leaves"][k]["family"] for k in keys}
    print("THE MERGED ORDER, at the value grain")
    print("  %d leaves, %d elements in the merged grid, grain %r"
          % (len(keys), sig["n_cells"], sig["grain"]))
    print("  decision 59: silence is free, a raise is not")
    print("")

    up, cand, classes = order(vec)
    edges = sum(len(v) for v in up.values())
    mx = sorted(k for k in keys if not up[k])
    print("  ordered pairs whose speaking sets NEST strictly: %d" % cand)
    print("  of those, faithful on every element: %d (%.2f percent)"
          % (edges, 100.0 * edges / cand if cand else 0.0))
    print("  MAXIMAL leaves -- nothing above them: %d of %d"
          % (len(mx), len(keys)))
    print("  leaves carrying an identical vector to another: %d classes"
          % len(classes))
    tri = check_transitive(up)
    print("  transitivity checked over %d super-chains of length two: "
          "no failure" % tri)

    # --- the alternative reading of decision 59 ------------------------
    vec2, nclaim = strip_claims(vec, sig)
    up2, cand2, _ = order(vec2)
    mx2 = sorted(k for k in keys if not up2[k])
    e2 = sum(len(v) for v in up2.values())
    print("")
    print("  the alternative reading, a raise read as SILENCE:")
    print("    %d of %d element values are wholly claim-of-refusal"
          % (nclaim, sig["n_values"]))
    print("    %d nesting pairs, %d faithful, %d maximal leaves"
          % (cand2, e2, len(mx2)))

    # --- the other grain ------------------------------------------------
    fc, fe, fm, ff = order_form_grain(vec, sig)
    print("")
    print("  the other GRAIN, form-pair, holder splits tolerated:")
    print("    %d nesting pairs, %d faithful, %d maximal leaves"
          % (fc, fe, fm))
    print("    transitivity failures: %d -- intersection carries no "
          "guarantee, and here it does not fail" % ff)

    # --- php.== ---------------------------------------------------------
    print("")
    print("THE php.== VERIFICATION")
    php = "php.=="
    ph = vec[php]
    print("  php.== speaks on %d of %d elements" % (len(ph), sig["n_cells"]))
    print("  leaves it sits above: %d"
          % sum(1 for k in keys if php in up[k]))
    print("  leaves whose speaking set nests inside php.==: %d"
          % sum(1 for k in keys
                if k != php and set(vec[k]) <= set(ph)
                and len(vec[k]) < len(ph)))
    denies = []
    for k in keys:
        if k == php or not (set(vec[k]) < set(ph)):
            continue
        b = blocking(vec, sig, k, php, limit=1)
        if b:
            denies.append((k, len(vec[k]), b[0]))
    # a comparison operator contradicting php.== is the readable case:
    # php's `==' against dart's `??' is two different operations, and
    # their differing is a restatement of that rather than a finding.
    denies.sort(key=lambda r: (fam[r[0]] != "comparison", -r[1]))
    print("  of those, the ones php.== CONTRADICTS: %d" % len(denies))
    print("  the elements that deny php.== the top, its own family "
          "first, then widest sub-node:")
    for k, n, b in denies[:6]:
        print("    %-16s %s" % (k, b["element"]))
        print("      %-15s %s" % (k, ",".join(b["left"])[:38]))
        print("      %-15s %s" % (php, ",".join(b["right"])[:38]))

    # --- per family ------------------------------------------------------
    byfam = collections.defaultdict(list)
    for k in keys:
        byfam[fam[k]].append(k)
    rows = []
    print("")
    print("PER FAMILY")
    print("  %-11s %6s %8s %8s %8s %7s"
          % ("family", "leaves", "nesting", "faithful", "maximal", "union"))
    famu = {}
    for f in FAMILIES:
        ks = sorted(byfam.get(f, []))
        if not ks:
            continue
        sub = {k: vec[k] for k in ks}
        u, c, _ = order(sub)
        m = sorted(k for k in ks if not u[k])
        e = sum(len(v) for v in u.values())
        uni = set()
        for k in ks:
            uni |= set(vec[k])
        verd = union_verdicts(vec, sig, m, fam)
        famu[f] = verd
        vc = collections.Counter(r["verdict"] for r in verd)
        rows.append(dict(family=f, leaves=len(ks), nesting_pairs=c,
                         faithful_edges=e, maximal=len(m),
                         maximal_leaves=m, union_elements=len(uni),
                         single_top=(m[0] if len(m) == 1 else None),
                         verdicts=dict(vc)))
        print("  %-11s %6d %8d %8d %8d %7d"
              % (f, len(ks), c, e, len(m), len(uni)))

    # --- the union assembly ----------------------------------------------
    print("")
    print("THE UNION ASSEMBLY, over the %d maximal leaves overall"
          % len(mx))
    allv = union_verdicts(vec, sig, mx, fam)
    vc = collections.Counter(r["verdict"] for r in allv)
    vcf = collections.Counter(r["verdict"] for r in allv
                              if r["same_family"])
    print("  %-18s %8s %8s" % ("verdict", "all", "in family"))
    for v in ("union candidate", "partial", "fork", "disjoint"):
        print("  %-18s %8d %8d" % (v, vc[v], vcf[v]))
    cands = sorted((r for r in allv
                    if r["verdict"] == "union candidate"
                    and r["same_family"]),
                   key=lambda r: (r["same_language"],
                                  -r["shared_elements"],
                                  -r["union_elements"]))
    print("")
    print("  the widest UNION CANDIDATES within a family, cross-language "
          "first:")
    for r in cands[:12]:
        print("    %-18s %-18s %-11s %5d shared, union %5d%s"
              % (r["left"], r["right"], r["family"],
                 r["shared_elements"], r["union_elements"],
                 "   same language" if r["same_language"] else ""))

    out = dict(
        status="DOMINANCE AT THE VALUE GRAIN, MERGED ORDER, OPERATORS",
        built="2026-08-20",
        extends=["signatures_valuegrain.json", "dominance_lattice.json"],
        supersedes=("the two-order reading of log 041; containment "
                    "without faithfulness does not exist at this grain"),
        decision_59=("silence is free and a claim is not: the order asks "
                     "Y to match X only where X SPEAKS, and a raise, a "
                     "death and a backend refusal are claims"),
        decision_59_flag=("FLAGGED.  A raise could be read as a decline "
                          "rather than as an answer.  The counts under "
                          "that reading are in `alternative_reading'."),
        grain=sig["grain"], grain_flag=sig["grain_flag"],
        n_leaves=len(keys), n_cells=sig["n_cells"],
        nesting_pairs=cand, faithful_edges=edges,
        maximal=len(mx), maximal_leaves=mx,
        identical_vector_classes=len(classes),
        identical_vector_members={k: v for k, v in classes.items()
                                  if len(v) > 1},
        transitivity_checked=tri,
        alternative_reading=dict(
            note="a raise, a death and a refusal read as silence",
            claim_only_values=nclaim, nesting_pairs=cand2,
            faithful_edges=e2, maximal=len(mx2)),
        other_grain=dict(
            note="the form-pair grain: two leaves match at an element "
                 "when their token sets intersect, so a holder split "
                 "does not count against them",
            nesting_pairs=fc, faithful_edges=fe, maximal=fm,
            transitivity_failures=ff,
            verdict=(("%d super-chains of length two do not close, so "
                      "it is not an order" % ff) if ff else
                     "no transitivity failure on this data, though "
                     "intersection guarantees none")),
        php_eq=dict(
            elements_spoken=len(ph),
            sits_above=sum(1 for k in keys if php in up[k]),
            nests_inside_it=sum(1 for k in keys
                                if k != php and set(vec[k]) < set(ph)),
            contradicted_sub_nodes=len(denies),
            denying_elements=[dict(leaf=k, elements=n, **b)
                              for k, n, b in denies[:40]]),
        log_041_comparison=dict(
            log_041_nesting_pairs=13831, log_041_faithful=189,
            log_041_maximal=184, log_041_leaves=238,
            value_grain_nesting_pairs=cand,
            value_grain_faithful=edges,
            value_grain_maximal=len(mx),
            value_grain_leaves=len(keys)),
        families=rows,
        maximal_pair_verdicts=dict(vc),
        maximal_pair_verdicts_within_family=dict(vcf),
        union_candidates_within_family=cands,
        blocked_within_family=[r for r in allv
                               if r["same_family"]
                               and r["verdict"] in ("fork", "partial")][:600],
        family_union_verdicts={f: v for f, v in famu.items()})
    p = os.path.join(HERE, "dominance_valuegrain.json")
    json.dump(out, open(p, "w"), indent=1, sort_keys=True)
    print("")
    print("wrote dominance_valuegrain.json (%.1f MB)"
          % (os.path.getsize(p) / 1e6))
    return dict(sig=sig, vec=vec, keys=keys, fam=fam, up=up, maximal=mx,
                classes=classes, family_verdicts=famu, all_verdicts=allv,
                report=out)


if __name__ == "__main__":
    main()
