#!/usr/bin/env bash
# ap5_l14_guard_t100_edges_b.sh -- task ap5: the FOURTH guard the brief
# names, and it is the one that belongs to `align_by_row` itself:
# "task t100's proved-edge count (`pool100_edges.json`: the number of
# proved edges, before and after, unchanged -- `align_by_row` is the
# pool's own aligner)".
#
# WHAT IS ASKED, and why it is asked this way.  `align_by_row` is what
# puts BOTH sides of every pool100 edge on one set of IN rows, so a
# change to it could move any of task t100's verdicts.  The change is
# one BRANCH, taken exactly when a row's family is spelled `X87_<k>`.
# So the guard is three readings and not one:
#
#  [1] THE COUNT the brief names: the proved edges of
#      `pool100_edges.json` as the artifact holds them.
#  [2] THE BRANCH'S REACH: every arrival family named by every edge of
#      that file, asked whether any is an x87 family.  One that is
#      would be an edge whose verdict could move; none means the new
#      branch is unreachable for the whole pool.
#  [3] THE ALIGNER RE-RUN, edge for edge: for every edge's own input
#      rows, `align_by_row`'s substitution as it stands NOW against the
#      substitution the function made BEFORE this task -- the two lines
#      it had, written here in the lane as a reference implementation
#      and labelled as such, never in the shared file.  A single
#      difference is a failed guard.
#
# THE NAME: lane `ap5_l11` was this lane with a defect of its own -- it
# tallied every field whose name was `outcome` or `verdict` without
# looking at what such a field HOLDS, and on this file one of them
# holds a mapping, so it stopped on `TypeError: unhashable type:
# 'dict'`.  A lane name is used ONCE (the standing rule of
# 2026-09-07), so this is a new one and ap5_l11 stays on the record
# with its defect.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.
# `pool100_edges.json` is 67 MB on disk; it is read ONCE, and the
# edges are walked in one pass with only the counters kept.
set -euo pipefail
cd PseudoCoupHQ/Research/op_pipeline
python3 - <<'PY'
import json
import os
import resource
import sys

OP = "PseudoCoupHQ/Research/op_pipeline"
sys.path.insert(0, OP)
import z3
import reference as R
import pool100_entry_equivalence as P100

ABORT_KB = 6 * 1024 * 1024


def guard(where):
    got = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP5: %d kB at %s" % (got, where))
    print("   peak resident at %s: %d kB" % (where, got))


def align_by_row_before_task_ap5(term, rows):
    """THE FUNCTION AS IT STOOD BEFORE THIS TASK, transcribed here in
    the lane so the two can be compared, and written nowhere else.  It
    is `pool100_entry_equivalence.align_by_row`'s body of record up to
    2026-09-09."""
    substitution = []
    for index, row in enumerate(rows):
        seed = z3.BitVec("seed_%s" % row["family"], row["bits"])
        common = z3.BitVec("IN_%d" % index, row["bits"])
        substitution.append((seed, common))
    if not substitution:
        return None
    return substitution


EDGES = os.path.join(OP, "pool100_edges.json")
print("[1/3] the count the brief names")
print("   %s (%d bytes)" % (EDGES, os.path.getsize(EDGES)))
document = json.load(open(EDGES))
print("   the file's own top-level fields: %s" % sorted(document))
edges = document.get("edges") or []
print("   edges on the file: %d" % len(edges))
print("   an edge's own fields, LITERAL: %s" % sorted(edges[0]))
print("")
print("   every SCALAR field of an edge, tallied by value:")
counted = {}
for edge in edges:
    for name in sorted(edge):
        value = edge[name]
        if isinstance(value, (dict, list)):
            continue
        counted.setdefault(name, {})
        key = "%s" % value
        counted[name][key] = counted[name].get(key, 0) + 1
for name in sorted(counted):
    print("   by `%s`:" % name)
    for value in sorted(counted[name]):
        print("      %-40s %d" % (value[:40], counted[name][value]))
print("")
print("   THE PROVED-EDGE COUNT the brief names, by every field of an")
print("   edge that states one:")
for name in ["edge_applies", "both_terms_proved_against_own_body",
             "proved", "state", "runner_word"]:
    yes = 0
    for edge in edges:
        value = edge.get(name)
        if value is True or value == "proved" or value == "unsat":
            yes = yes + 1
    print("      edges whose `%s` says proved: %d of %d"
          % (name, yes, len(edges)))
guard("section 1")

print("")
print("[2/3] the branch's reach over the whole pool")
families = {}
x87 = 0
for edge in edges:
    for side in ("a", "b"):
        for family in ((edge.get("arrival_families_under_canon40")
                        or {}).get(side) or []):
            families[family] = families.get(family, 0) + 1
            if family.startswith("X87_") and family[4:].isdigit():
                x87 = x87 + 1
    for entry in (edge.get("inputs") or []):
        for key in ("family_a", "family_b"):
            family = entry.get(key)
            if family is None:
                continue
            families[family] = families.get(family, 0) + 1
            if family.startswith("X87_") and family[4:].isdigit():
                x87 = x87 + 1
print("   distinct arrival families over every edge: %d" % len(families))
print("   they are: %s" % ", ".join(sorted(families)))
print("   family readings that are an x87 family: %d" % x87)
guard("section 2")

print("")
print("[3/3] the aligner re-run, edge for edge")
same = 0
differ = []
empty = 0
for edge in edges:
    rows = []
    for entry in (edge.get("inputs") or []):
        rows.append({"row": entry.get("row"),
                     "family": entry.get("family_a"),
                     "bits": entry.get("bits")})
    was = align_by_row_before_task_ap5(None, rows)
    if was is None:
        empty = empty + 1
        continue
    now = []
    for index, row in enumerate(rows):
        family = row["family"] or ""
        if family.startswith("X87_") and family[4:].isdigit():
            now.append((z3.Const("seed_%s" % family, R.X87_SORT),
                        z3.Const("IN_%d" % index, R.X87_SORT)))
            continue
        now.append((z3.BitVec("seed_%s" % row["family"], row["bits"]),
                    z3.BitVec("IN_%d" % index, row["bits"])))
    left = [(a.sexpr(), a.sort().sexpr(), b.sexpr()) for a, b in was]
    right = [(a.sexpr(), a.sort().sexpr(), b.sexpr()) for a, b in now]
    if left == right:
        same = same + 1
    else:
        differ.append((edge.get("a"), edge.get("b"), left, right))
print("   edges whose substitution is identical before and after: %d"
      % same)
print("   edges with no input row at all (nothing to substitute): %d"
      % empty)
print("   edges whose substitution DIFFERS: %d" % len(differ))
for a, b, left, right in differ[:10]:
    print("      %s / %s" % (a, b))
    print("         before: %s" % left)
    print("         after : %s" % right)
guard("section 3")
print("done")
PY
