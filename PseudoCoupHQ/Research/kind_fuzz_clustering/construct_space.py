#!/usr/bin/env python3
"""construct_space.py -- the layer-3 CONSTRUCT probe space and its SIZE.

Printed BEFORE anything runs, as the node's plan of record requires of
every phase (phase 0's probe_space.py did the same job for operators).

The slot arithmetic, stated once here and nowhere else:

  V   the language's value count -- every (holder, value class) pair
      that layer 2 says loads.  A ONE-SLOT construct costs V answer
      probes.
  H   the language's holder count.  A TWO-SLOT construct costs H*H
      ACCEPTANCE probes, because in a statically checked language the
      verdict is a function of the holder pair and not of the value
      (the same reading l3_accept.py already runs on).
  M   sum over ordered holder pairs of Va*Vb -- the full value matrix.
      A TWO-SLOT construct costs M ANSWER probes.
  W   the value classes of the canonical whole-number holder, which is
      what a slice bound is drawn from.

Route C languages (python, ruby, php) have no separate acceptance
grain; execution is the only acceptance evidence there, so their
acceptance column is zero and their answer column carries everything.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_accept import holders, LANGS            # noqa: E402

ROUTE_C = {"python", "ruby", "php"}

# construct -> number of operand slots it opens.
# break and continue open no operand slot: their scaffold is fixed and
# the varying thing is WHERE the jump sits, k = 1..5.
SLOTS = {
    "access.subscript": 2,
    "access.slice": 3,
    "access.member": 1,
    "flow.if": 1,
    "flow.for": 1,
    "flow.while": 1,
    "flow.try": 1,
    "flow.break": 0,
    "flow.continue": 0,
    "binding.assign": 1,
    "binding.augassign": 2,
    "binding.unpack": 1,
}
AUG_OPS = ["+=", "-=", "*="]        # decision 9 -- the augmented three
JUMP_K = 5                          # decision 10 -- break/continue at k
WHOLE_BOUNDS = 6                    # slice bounds, capped -- decision 6


def whole_values(hs):
    for h in hs:
        if h["form"] == "whole":
            return min(len(h["values"]), WHOLE_BOUNDS)
    return 0


def space(lang):
    hs, _ = holders(lang)
    cat = json.load(open(os.path.join(HERE, "construct_catalogue.json")))
    H = len(hs)
    V = sum(len(h["values"]) for h in hs)
    M = sum(len(a["values"]) * len(b["values"]) for a in hs for b in hs)
    W = whole_values(hs)
    rows = []
    for name, n in sorted(SLOTS.items()):
        fam, role = name.split(".")
        present = cat[lang][fam][role]["present"]
        if not present:
            rows.append(dict(construct=name, present=False,
                             acceptance=0, answers=0,
                             note="grammar declares no such kind"))
            continue
        mult = len(AUG_OPS) if name == "binding.augassign" else 1
        if n == 0:
            acc, ans = 0, JUMP_K
        elif n == 1:
            acc, ans = H, V
        elif n == 2:
            acc, ans = H * H * mult, M * mult
        else:                                    # 3 slots -- slice
            acc, ans = H, V * W * W
        rows.append(dict(construct=name, present=True,
                         acceptance=acc, answers=ans, note=""))
    if lang in ROUTE_C:
        for r in rows:
            r["acceptance"] = 0
    return dict(language=lang, holders=H, values=V, value_matrix=M,
                whole_bounds=W, route_c=lang in ROUTE_C,
                constructs=rows,
                acceptance_probes=sum(r["acceptance"] for r in rows),
                answer_probes=sum(r["answers"] for r in rows))


def main():
    print("layer-3 CONSTRUCT probe space -- derived, printed before "
          "anything runs")
    print("")
    print("  language      H     V        M   acceptance     answers")
    ta = tn = 0
    for lang in LANGS:
        s = space(lang)
        json.dump(s, open(os.path.join(
            HERE, "construct_space_%s.json" % lang), "w"), indent=1)
        ta += s["acceptance_probes"]
        tn += s["answer_probes"]
        print("  %-11s %3d  %4d  %7d  %11d  %10d"
              % (lang, s["holders"], s["values"], s["value_matrix"],
                 s["acceptance_probes"], s["answer_probes"]))
    print("")
    print("  TOTAL                                %11d  %10d" % (ta, tn))
    print("  grand total probes: %d" % (ta + tn))


if __name__ == "__main__":
    main()
