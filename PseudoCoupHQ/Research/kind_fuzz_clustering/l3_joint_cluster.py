#!/usr/bin/env python3
"""l3_joint_cluster.py -- constructs and operators in ONE tree.

DECISION 17, REVISITED.  Log 037 kept the construct signatures out of
the operator tree, and it gave one reason: a measured difference of
GRAIN.  Nine of the twelve construct lanes reported at the holder
grain, where a form pair is present or absent and never partly so,
while every operator leaf carried value-matrix density behind it.
Pouring the two into one tree would have joined a construct to an
operator whenever both were empty, and emptiness was what nine
languages had most of.

That reason is GONE.  Log 038 raised all nine to the value grain, so
every leaf on both sides now stands on the same kind of evidence.  The
grain objection dissolves and decision 17 is overturned for everything
it covered.

A SECOND objection stands, and it was never about grain.  An operator
opens TWO operand positions; a one-slot construct opens ONE.  Their
domain keys live in different spaces and cannot be compared at all, so
a one-slot construct cannot enter the operator tree however it was
measured.  Log 037 measured that too: 87 of 129 construct leaves are
one-slot.

DECISION 21, therefore, and it is a division by KEY SPACE rather than
by grain:

  the TWO-SLOT constructs -- index access and augmented assignment --
  join the operators in one tree, because they share the operator's
  ordered form-pair key space exactly;

  the ONE-SLOT constructs keep a tree of their own, because there is no
  one-operand operator signature for them to sit beside, and saying so
  is more honest than recording a zero.

Cost to overturn: a probe space that gives an operator a one-operand
form, which nothing of the kind is built.
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_construct_cluster as C                            # noqa: E402


def main():
    csigs = C.construct_signatures()
    ops = json.load(open(os.path.join(HERE, "clusters_all12.json")))
    osigs = ops["signatures"]

    two, one = {}, {}
    for k, s in csigs.items():
        if not s["domain"]:
            continue
        (one if all(x.endswith("|-") for x in s["domain"]) else two)[k] = s
    print("construct leaves with a non-empty domain: %d"
          % (len(two) + len(one)))
    print("  two-slot, share the operator key space: %d" % len(two))
    print("  one-slot, no operator to sit beside:    %d" % len(one))

    sigs = {}
    for k, s in osigs.items():
        sigs["op:" + k] = dict(domain=s["domain"], kind="operator",
                               language=s["language"])
    for k, s in two.items():
        sigs["cn:" + k] = dict(domain=s["domain"], kind="construct",
                               language=s["language"])
    keys = sorted(sigs)
    print("joint tree: %d leaves (%d operator, %d construct)"
          % (len(keys), len(osigs), len(two)))

    sim = {}
    for i, a in enumerate(keys):
        A = set(sigs[a]["domain"])
        for b in keys[i:]:
            v = C.jaccard(A, set(sigs[b]["domain"]))
            sim[(a, b)] = sim[(b, a)] = v
    hist = C.full_merge(keys, sim)
    rows, plats, sims = C.sweep(keys, hist)

    # the reading the joint tree exists to produce: at the cut, does a
    # construct sit with operators or with other constructs?
    mixed = []
    for cut in (0.9, 0.8, 0.7, 0.6, 0.5):
        groups = C.cluster_count(keys, sim, cut)
        if isinstance(groups, int):
            groups = None
        mixed.append(dict(threshold=cut))
    # neighbours: for each construct leaf, its single nearest leaf
    near = {}
    for a in keys:
        if sigs[a]["kind"] != "construct":
            continue
        A = set(sigs[a]["domain"])
        best, bk = -1.0, None
        for b in keys:
            if b == a:
                continue
            j = C.jaccard(A, set(sigs[b]["domain"]))
            if j > best:
                best, bk = j, b
        near[a] = dict(nearest=bk, jaccard=round(best, 4),
                       nearest_is=sigs[bk]["kind"] if bk else None,
                       same_language=(bk.split(":", 1)[1].split(".")[0]
                                      == sigs[a]["language"]) if bk else None)
    nk = collections.Counter(v["nearest_is"] for v in near.values())
    sl = sum(1 for v in near.values() if v["same_language"])
    print("")
    print("nearest leaf to each two-slot construct, in the joint tree:")
    print("  an OPERATOR   %d" % nk["operator"])
    print("  a CONSTRUCT   %d" % nk["construct"])
    print("  of these, an item of its own language: %d of %d"
          % (sl, len(near)))
    js = sorted(v["jaccard"] for v in near.values())
    if js:
        print("  jaccard to that nearest leaf: median %.3f  lowest %.3f"
              "  highest %.3f" % (js[len(js) // 2], js[0], js[-1]))

    out = dict(status="JOINT TREE, VALUE GRAIN, ALL TWELVE",
               built="2026-08-19",
               extends=["clusters_all12.json", "clusters_constructs.json"],
               decision_21=("the two-slot constructs join the operator "
                            "tree because they share its ordered "
                            "form-pair key space; the one-slot "
                            "constructs cannot and keep their own"),
               decision_17_overturned=("its reason was a difference of "
                                       "grain and log 038 removed it"),
               n_leaves=len(keys), signatures=sigs,
               one_slot_excluded=sorted(one),
               empty_domain=[],
               merge_history=hist, sweep=rows, plateaus=plats,
               nearest_leaf=near)
    json.dump(out, open(os.path.join(HERE, "clusters_joint.json"), "w"),
              indent=1, sort_keys=True)
    print("")
    print("the sweep, plateaus widest first")
    for p in plats[:8]:
        print("  %4.2f..%4.2f  width %4.2f   %3d clusters"
              % (p["low"], p["high"], p["width"], p["clusters"]))


if __name__ == "__main__":
    main()
