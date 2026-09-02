#!/usr/bin/env python3
"""l3_operator_dominance_v2_twelve.py -- the log_057 wrapper's job, on
the TWELVE-language `matrices_full_v2/` (log_064 fold).

Composes the settled `l3_operator_dominance.py` functions
(`operator_containment`, `mode_partition`) unmodified after repointing
`FULL`; never calls that module's `main()`, because `main()` hard-codes
`operator_dominance_v1.json` -- the log_056 audit product, which must
never be touched.  Output goes to `operator_dominance_v2.json`, the
same file the log_057 wrapper wrote (that file is a pure function of
`matrices_full_v2/` and moves with it; its pre-fold state is quoted in
DevComms/log_057 and log_064).

The ONLY departure from the log_057 wrapper is `read_profiles_interned`
below: `read_profiles`'s own `split(";")` materialises one NEW string
per cell, and at 46,108,297 cells that no longer fits a small analysis
host.  Cell strings are interned through one memo dict, so every
repeated canon is ONE object.  The tuples compared, and the comparison
itself, are unchanged -- interning cannot alter equality.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
csv.field_size_limit(sys.maxsize)

import l3_operator_dominance as D                              # noqa: E402

D.FULL = os.path.join(HERE, "matrices_full_v2")


def read_profiles_interned():
    """`D.read_profiles`, cell strings shared through one memo."""
    memo = {}
    mset = memo.setdefault
    profiles = []
    for name in sorted(os.listdir(D.FULL)):
        if not name.endswith(".csv"):
            continue
        language, operator, level_tag = name[:-4].split(".")
        with open(os.path.join(D.FULL, name)) as fh:
            for row in csv.DictReader(fh):
                profiles.append({
                    "language": language,
                    "operator": operator,
                    "op_id": f"{language}.{operator}",
                    "level": int(row["level"]),
                    "form_pair": row["form_pair"],
                    "block": f'{row["form_pair"]}/L{row["level"]}',
                    "lhs_holder": row["lhs_holder"],
                    "rhs_holder": row["rhs_holder"],
                    "probe_id": row["probe_id"],
                    "cells": tuple(
                        mset(c, c)
                        for c in row["output_canon_vector"].split(";")),
                })
    return profiles


def main():
    print("operator dominance v2 -- twelve-language matrices_full_v2/ "
          "(log_064); matrices_full/ and operator_dominance_v1.json are "
          "untouched.  source: %s" % D.FULL)
    profiles = read_profiles_interned()
    print("profiles read: %d" % len(profiles))
    pairs = D.operator_containment(profiles)
    print("containment pairs: %d" % len(pairs))
    modes = D.mode_partition(profiles)

    ops = sorted({p["op_id"] for p in profiles})
    result = {
        "status": "operator-level dominance and mode partition, v2 -- "
                  "twelve-language fold (log_064, 2026-08-23). "
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
