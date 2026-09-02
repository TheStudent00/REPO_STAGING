#!/usr/bin/env python3
"""log065_readings.py -- Job 2 of log_065.  Computes operator containment
and the mode partition of `plus`/`whole|whole/L1` TWICE over
matrices_full_v2/, once per reading log_056 SS4 left open:

  VALUE reading   -- declines (REFUSE/RAISE:*/ABORT) AND UNREPRESENTABLE
                     excluded from numerator AND denominator.  Two
                     profiles are compared only at positions where BOTH
                     answer a value; the pair must have at least one such
                     position (CLAUDE.md: "zero comparable keys means NO
                     connector").  This is MY operationalisation of the
                     phrase, not a ruling -- see log_065 for the exact
                     wording.
  ALL-CELLS reading -- every position counts; outcome tokens (including
                     UNREPRESENTABLE) ride as literal answers, compared
                     by byte identity like any value.  This is the
                     reading `l3_operator_dominance.py`'s `mode_partition`
                     already implements (full-vector equality); here it
                     is also applied to containment.

No probes run.  Reads matrices_full_v2/ only.  Run under `nice -n 15`.
"""

import collections
import csv
import json
import os
import sys
import time

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "matrices_full_v2")
DECLINE_PREFIXES = ("REFUSE", "RAISE:", "ABORT", "UNREPRESENTABLE")


def is_value(cell):
    return not cell.startswith(DECLINE_PREFIXES)


def read_profiles():
    memo = {}
    mset = memo.setdefault
    profiles = []
    for name in sorted(os.listdir(FULL)):
        if not name.endswith(".csv"):
            continue
        language, operator, level_tag = name[:-4].split(".")
        with open(os.path.join(FULL, name)) as fh:
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
                    "cells": tuple(mset(c, c)
                                   for c in row["output_canon_vector"].split(";")),
                })
    return profiles


# ------------------------------------------------------------------
# the two "dominates" tests -- same signature, same outer loop
# ------------------------------------------------------------------

def dominates_all_cells(a_cells, b_cells):
    """ALL-CELLS reading: outcome tokens ride as literal answers.  A
    'dominates' B here collapses to full-vector equality (any position
    where A carries different information -- a value B lacks, or vice
    versa -- already shows as a literal mismatch), so this IS the
    containment test under this reading."""
    return a_cells == b_cells


def dominates_value(a_cells, b_cells):
    """VALUE reading: compare only positions where BOTH sides answer a
    value; require at least one such position (a nonzero denominator)
    and zero conflicts among them."""
    comparable = False
    for a, b in zip(a_cells, b_cells):
        if is_value(a) and is_value(b):
            if a != b:
                return False
            comparable = True
    return comparable


def operator_containment(profiles, dominates):
    by_op = collections.defaultdict(list)
    for p in profiles:
        by_op[p["op_id"]].append(p)
    by_op_block = collections.defaultdict(list)
    for p in profiles:
        by_op_block[(p["op_id"], p["block"])].append(p)

    ops = sorted(by_op)
    pairs = []
    for a in ops:
        for b in ops:
            if a == b:
                continue
            covered = 0
            witnesses = []
            for pb in by_op[b]:
                supers = by_op_block.get((a, pb["block"]), ())
                hit = next((pa for pa in supers
                            if dominates(pa["cells"], pb["cells"])), None)
                if hit is None:
                    break
                covered += 1
                witnesses.append((f'{hit["lhs_holder"]} {hit["rhs_holder"]}',
                                  f'{pb["lhs_holder"]} {pb["rhs_holder"]}',
                                  pb["block"]))
            else:
                pairs.append({
                    "a": a, "b": b,
                    "n_profiles_b": len(by_op[b]),
                    "n_profiles_a": len(by_op[a]),
                    "witness_sample": witnesses[:3],
                })
    return pairs


def main():
    t0 = time.time()
    profiles = read_profiles()
    print(f"profiles read: {len(profiles)}  ({time.time()-t0:.1f}s)",
          file=sys.stderr)

    t1 = time.time()
    pairs_value = operator_containment(profiles, dominates_value)
    print(f"VALUE containment: {len(pairs_value)} pairs "
          f"({time.time()-t1:.1f}s)", file=sys.stderr)

    t2 = time.time()
    pairs_all = operator_containment(profiles, dominates_all_cells)
    print(f"ALL-CELLS containment: {len(pairs_all)} pairs "
          f"({time.time()-t2:.1f}s)", file=sys.stderr)

    out = {
        "n_profiles": len(profiles),
        "value_reading": pairs_value,
        "all_cells_reading": pairs_all,
    }
    path = os.path.join(HERE, "log065_containment_readings.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {path}  total {time.time()-t0:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
