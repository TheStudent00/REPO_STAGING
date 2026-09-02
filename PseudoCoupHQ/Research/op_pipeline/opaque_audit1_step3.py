#!/usr/bin/env python3
"""opaque_audit1_step3.py -- STEP 3 cluster-quality comparison.

Diffs tree_match2's 333 cross-language exact clusters against
tree_match3's 289, by (type_pair, normalized_root) identity (machine
form -- never the operator token), and classifies every LOST and every
GAINED cluster as opaque-keyed (losing it is good / gaining it is
questionable -- an opaque-keyed cluster is a candidate false merge, so
GAINING one under tree_match3 would be a regression, and none is
expected) vs real-structure-keyed (losing it is a regression / gaining
it is real new signal).

THE SPELLING BAN: cluster identity for the diff is (type_pair,
normalized_root) -- both machine form (a type-pair from the probe's
recorded types, and a z3-normalized expression), never the operator
token. `operator` is read only for the per-member display rows.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

import opaque_audit1_step1 as A1                                 # noqa: E402

is_opaque_only = A1.is_opaque_only


def cluster_key(c):
    return (c["type_pair"], c["normalized_root"])


def load_cross_lang(path):
    doc = json.load(open(path))
    return {cluster_key(c): c for c in doc["exact_normalized_root"]
            if c["cross_language"]}


def classify(c):
    return "opaque-keyed" if is_opaque_only(c["normalized_root"]) \
        else "real-structure-keyed"


def main():
    m2 = load_cross_lang(os.path.join(HERE, "tree_matches2.json"))
    m3 = load_cross_lang(os.path.join(HERE, "tree_matches3.json"))

    lost_keys = set(m2.keys()) - set(m3.keys())
    gained_keys = set(m3.keys()) - set(m2.keys())
    kept_keys = set(m2.keys()) & set(m3.keys())

    lost = [m2[k] for k in lost_keys]
    gained = [m3[k] for k in gained_keys]

    lost_opaque = [c for c in lost if classify(c) == "opaque-keyed"]
    lost_real = [c for c in lost if classify(c) == "real-structure-keyed"]
    gained_opaque = [c for c in gained if classify(c) == "opaque-keyed"]
    gained_real = [c for c in gained if classify(c) == "real-structure-keyed"]

    print("cross-language clusters: tree_match2=%d tree_match3=%d "
          "kept=%d lost=%d gained=%d" %
          (len(m2), len(m3), len(kept_keys), len(lost), len(gained)))
    print()
    print("LOST (333 -> not in 289): %d total" % len(lost))
    print("  opaque-keyed (losing is GOOD -- false merge removed): %d"
          % len(lost_opaque))
    print("  real-structure-keyed (losing is a REGRESSION -- real "
          "signal lost): %d" % len(lost_real))
    print()
    print("GAINED (in 289, not in 333): %d total" % len(gained))
    print("  opaque-keyed (gaining would be QUESTIONABLE): %d"
          % len(gained_opaque))
    print("  real-structure-keyed (gaining is real NEW signal): %d"
          % len(gained_real))

    if lost_real:
        print()
        print("=== every real-structure-keyed LOST cluster (regression "
              "candidates -- must be checked by hand) ===")
        for c in lost_real:
            member_ids = ["%s/%s(op=%s)" % (m["lang"], m["n"],
                                             m["operator"])
                          for m in c["members"]]
            print("key=%r type_pair=%s size=%d langs=%s" %
                  (c["normalized_root"], c["type_pair"],
                   len(c["members"]), c["languages"]))
            for mid in member_ids:
                print("    ", mid)

    if gained_opaque:
        print()
        print("=== every opaque-keyed GAINED cluster (new false merges "
              "-- must be checked by hand) ===")
        for c in gained_opaque:
            member_ids = ["%s/%s(op=%s)" % (m["lang"], m["n"],
                                             m["operator"])
                          for m in c["members"]]
            print("key=%r type_pair=%s size=%d langs=%s" %
                  (c["normalized_root"], c["type_pair"],
                   len(c["members"]), c["languages"]))
            for mid in member_ids:
                print("    ", mid)

    def dump_cluster(c):
        return dict(
            normalized_root=c["normalized_root"],
            type_pair=c["type_pair"],
            member_count=len(c["members"]),
            languages=c["languages"],
            members=["%s/%s(op=%s)" % (m["lang"], m["n"], m["operator"])
                     for m in c["members"]],
        )

    out = dict(
        role="generator provenance",
        note="output of opaque_audit1_step3.py -- STEP 3 cluster-quality "
             "diff, programmatically verified over the full 333/289 "
             "cross-language cluster populations",
        tree_match2_cross_lang_count=len(m2),
        tree_match3_cross_lang_count=len(m3),
        kept_count=len(kept_keys),
        lost_count=len(lost),
        lost_opaque_count=len(lost_opaque),
        lost_real_count=len(lost_real),
        gained_count=len(gained),
        gained_opaque_count=len(gained_opaque),
        gained_real_count=len(gained_real),
        lost_real_clusters=[dump_cluster(c) for c in lost_real],
        gained_opaque_clusters=[dump_cluster(c) for c in gained_opaque],
    )
    out_path = os.path.join(HERE, "opaque_audit1_step3_result.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print()
    print("wrote", out_path)


if __name__ == "__main__":
    main()
