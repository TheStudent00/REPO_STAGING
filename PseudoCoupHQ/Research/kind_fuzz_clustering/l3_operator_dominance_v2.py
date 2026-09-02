#!/usr/bin/env python3
"""l3_operator_dominance_v2.py -- re-run the EXISTING
`l3_operator_dominance.py` logic against `matrices_full_v2/` (the
log_057-fixed re-fold) instead of `matrices_full/`.

Composes the settled module's own functions (`read_profiles`,
`operator_containment`, `mode_partition`) unmodified after repointing
`FULL`; does NOT call its `main()`, because `main()` writes a hard-coded
`operator_dominance_v1.json` path and that file is the log_056 audit
product read from `matrices_full/` -- it must never be touched.  Output
goes to `operator_dominance_v2.json` instead.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_operator_dominance as D                              # noqa: E402

D.FULL = os.path.join(HERE, "matrices_full_v2")


def main():
    print("operator dominance v2 -- re-run against matrices_full_v2/ "
          "(log_057-fixed); matrices_full/ and operator_dominance_v1.json "
          "are untouched.  source: %s" % D.FULL)
    profiles = D.read_profiles()
    pairs = D.operator_containment(profiles)
    modes = D.mode_partition(profiles)

    ops = sorted({p["op_id"] for p in profiles})
    result = {
        "status": "operator-level dominance and mode partition, v2 -- "
                  "re-fold after the log_057 ruby Float canon fix. "
                  "ASSEMBLY ONLY -- no classification of a fracture as "
                  "guarantee-vs-no-guarantee is made here; that reading "
                  "is the owner's, per the guarantees rule.",
        "source": "matrices_full_v2/ -- no probes run",
        "dominance_rule": "operator A CONTAINS operator B when every "
                          "profile of B is dominated by some profile of "
                          "A in the same gate block (the owner, 2026-08-22)",
        "mode_rule": "inside a gate block, one operator spelling's "
                     "profiles partitioned by total agreement; each part "
                     "is a CANDIDATE mode; least-modes caps the set at "
                     "guarantees that exist",
        "n_profiles": len(profiles),
        "n_operators": len(ops),
        "operators": ops,
        "containment_pairs": pairs,
        "mode_families": modes,
    }
    path = os.path.join(HERE, "operator_dominance_v2.json")
    with open(path, "w") as fh:
        json.dump(result, fh, indent=1)

    print(f"profiles: {len(profiles)}   operators: {len(ops)}")
    print(f"operator containment pairs: {len(pairs)}")
    print(f"mode families (cross-language): {len(modes)}")
    print(f"wrote {path}")
    return result


if __name__ == "__main__":
    main()
