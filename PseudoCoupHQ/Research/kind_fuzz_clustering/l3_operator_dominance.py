#!/usr/bin/env python3
"""Operator-level dominance and the mode partition.

    python3 PseudoCoupHQ/Research/kind_fuzz_clustering/l3_operator_dominance.py

the owner's definition, 2026-08-22: operator A DOMINATES operator B when A
contains all the same profiles as B and more.  That is one level ABOVE
the profile relation built in log 055, which asked the same question of
single profiles.  This script computes the operator relation FROM the
profile relation, and then the mode partition that the guarantees rule
calls for.

Reads matrices_full/ only.  No probes.

Three objects are produced:

  operator containment
      A contains B when, for every profile of B, some profile of A in
      the same gate block dominates it.  A profile of A dominates a
      profile of B when at every key where B answers a VALUE, A answers
      the identical value.  A may answer at more keys.

  mode partition
      Inside one gate block, the profiles of one operator SPELLING
      (across languages) are partitioned by total agreement over the
      full grid.  Each part is a candidate mode -- the parts that
      cannot merge are exactly what the owner's least-modes rule turns into
      modes.  Partition is by equality, so no judgement enters here.

  residue
      A profile agreeing with no other profile in its family.  Under
      the recorded rulings these are candidates for `unspecified`
      (rust's bare `+`) or for the no-guarantee case (cpp signed
      overflow) -- flagged, never auto-classified: the guarantees
      reading is the owner's.

Vocabulary per PseudoCoupHQ/CLAUDE.md: super/sub, co-node, ABORT.
"""

import collections
import csv
import json
import os
import sys

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "matrices_full")
DECLINE_PREFIXES = ("REFUSE", "RAISE:", "ABORT", "UNREPRESENTABLE")


def is_value(cell):
    """A cell is a VALUE unless it is one of the outcome tokens."""
    return not cell.startswith(DECLINE_PREFIXES)


def read_profiles():
    """Every profile in matrices_full/, as plain dicts.  The output
    vector is split once and kept as a tuple."""
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
                    "cells": tuple(row["output_canon_vector"].split(";")),
                })
    return profiles


def dominates(a_cells, b_cells):
    """Profile A dominates profile B: at every key where B answers a
    VALUE, A answers the identical value.  A may answer at more keys.
    Both profiles are full grids, so the keys line up by position."""
    for a, b in zip(a_cells, b_cells):
        if is_value(b) and a != b:
            return False
    return True


def operator_containment(profiles):
    """A contains B when every profile of B is dominated by some
    profile of A in the same gate block.  Answers the directed pairs
    plus, for each, the evidence counts."""
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
                                  f'{pb["lhs_holder"]} {pb["rhs_holder"]}'))
            else:
                pairs.append({
                    "a": a, "b": b,
                    "n_profiles_b": len(by_op[b]),
                    "n_profiles_a": len(by_op[a]),
                    "strict": len(by_op[a]) > len(by_op[b]),
                    "witness_sample": witnesses[:3],
                })
    return pairs


def mode_partition(profiles):
    """Inside one gate block, partition one operator SPELLING's
    profiles (across languages) by total agreement over the full grid.
    Each part is a candidate mode; a part of size one whose language is
    alone is flagged as residue."""
    families = collections.defaultdict(list)
    for p in profiles:
        families[(p["operator"], p["block"])].append(p)

    out = []
    for (operator, block), members in sorted(families.items()):
        if len({m["language"] for m in members}) < 2:
            continue                      # one language: nothing to partition
        parts = collections.defaultdict(list)
        for m in members:
            parts[m["cells"]].append(m)
        rows = []
        for cells, part in parts.items():
            langs = sorted({m["language"] for m in part})
            rows.append({
                "n_members": len(part),
                "languages": langs,
                "holder_pairs": sorted({f'{m["lhs_holder"]} {m["rhs_holder"]}'
                                        for m in part})[:6],
                "n_value_cells": sum(1 for c in cells if is_value(c)),
                "n_cells": len(cells),
                "single_language": len(langs) == 1,
            })
        rows.sort(key=lambda r: (-len(r["languages"]), -r["n_members"]))
        out.append({
            "operator": operator,
            "block": block,
            "n_profiles": len(members),
            "n_parts": len(parts),
            "n_cross_language_parts": sum(1 for r in rows
                                          if len(r["languages"]) > 1),
            "parts": rows,
        })
    return out


def main():
    profiles = read_profiles()
    pairs = operator_containment(profiles)
    modes = mode_partition(profiles)

    ops = sorted({p["op_id"] for p in profiles})
    result = {
        "status": "operator-level dominance and mode partition. "
                  "ASSEMBLY ONLY -- no classification of a fracture as "
                  "guarantee-vs-no-guarantee is made here; that reading "
                  "is the owner's, per the guarantees rule.",
        "source": "matrices_full/ -- no probes run",
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
    path = os.path.join(HERE, "operator_dominance_v1.json")
    with open(path, "w") as fh:
        json.dump(result, fh, indent=1)

    print(f"profiles: {len(profiles)}   operators: {len(ops)}")
    print(f"operator containment pairs: {len(pairs)}")
    print(f"mode families (cross-language): {len(modes)}")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
