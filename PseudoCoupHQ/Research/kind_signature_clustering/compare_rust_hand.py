#!/usr/bin/env python3
"""compare_rust_hand.py — P-a step 7 (rust only): diff the machine
proposal (proposed_kind_map_rust.json) against the HAND draft
(PCv5 log_008_kinds_coarse_tagging_draft.md, 163 rows, 2026-08-05).

The hand draft is a COMPARISON TARGET only — it was not an input to
the generator, so agreement/disagreement is itself a finding.

Classes (one per kind):
  machine-none   — machine residue (proposed=none), whatever the hand said
  hand-open      — hand row flagged UNCERTAIN and/or DUAL; machine
                   proposed; sub-split by whether the machine's pick is
                   among the hand's candidate bucket(s)
  agree          — hand row unflagged, machine's pick equals the hand's
                   bucket (hand's PROPOSED form names normalized to the
                   ruled names)
  disagree       — hand row unflagged, machine picked something else

Writes comparison_rust_hand.json and prints the counts + disagreement
rows. Vocabulary: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
# PCv5 sits beside PseudoCoupHQ under the same Programming root, so
# the path is derived from HERE (portable across mounts).
HAND = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "PseudoCoup_v5", "DevComms",
    "log_008_kinds_coarse_tagging_draft.md"))


def load_hand():
    rows = {}
    rx = re.compile(r"^\| `([a-z_]+)` \| ([^|]+) \| [^|]* \| ([^|]*)\|")
    for line in open(HAND):
        m = rx.match(line)
        if not m:
            continue
        kind, buckets, flag = m.group(1), m.group(2), m.group(3)
        bl = [b.strip().replace(" (PROPOSED)", "")
              for b in buckets.split(" + ")]
        fl = set()
        if "DUAL" in flag:
            fl.add("DUAL")
        if "UNCERTAIN" in flag:
            fl.add("UNCERTAIN")
        rows[kind] = {"buckets": bl, "flags": sorted(fl)}
    return rows


def main():
    hand = load_hand()
    mach = json.load(open(os.path.join(
        HERE, "proposed_kind_map_rust.json")))["rows"]
    assert len(hand) == len(mach) == 163, (len(hand), len(mach))
    out = {"agree": [], "disagree": [], "hand-open-machine-matches": [],
           "hand-open-machine-differs": [], "machine-none": []}
    for r in mach:
        k = r["kind"]
        h = hand[k]
        if r["residue"]:
            out["machine-none"].append(
                {"kind": k, "hand": h["buckets"], "flags": h["flags"]})
        elif h["flags"]:
            cls = ("hand-open-machine-matches"
                   if r["proposed"] in h["buckets"]
                   else "hand-open-machine-differs")
            out[cls].append({"kind": k, "hand": h["buckets"],
                             "flags": h["flags"],
                             "machine": r["proposed"],
                             "confidence": r["confidence"]})
        elif r["proposed"] in h["buckets"]:
            out["agree"].append({"kind": k, "hand": h["buckets"],
                                 "machine": r["proposed"],
                                 "confidence": r["confidence"]})
        else:
            out["disagree"].append({"kind": k, "hand": h["buckets"],
                                    "machine": r["proposed"],
                                    "confidence": r["confidence"]})
    p = os.path.join(HERE, "comparison_rust_hand.json")
    json.dump(out, open(p, "w"), indent=1)
    print("wrote", p)
    for cls, rows in out.items():
        print("%-26s %d" % (cls, len(rows)))
    print("\nDISAGREEMENTS (hand firm, machine differs):")
    for r in out["disagree"]:
        print(" %-30s hand=%-28s machine=%s (%s)" % (
            r["kind"], "+".join(r["hand"]), r["machine"],
            r["confidence"]))
    print("\nHAND-OPEN, MACHINE DIFFERS:")
    for r in out["hand-open-machine-differs"]:
        print(" %-30s hand=%-28s [%s] machine=%s (%s)" % (
            r["kind"], "+".join(r["hand"]), ",".join(r["flags"]),
            r["machine"], r["confidence"]))


if __name__ == "__main__":
    main()
