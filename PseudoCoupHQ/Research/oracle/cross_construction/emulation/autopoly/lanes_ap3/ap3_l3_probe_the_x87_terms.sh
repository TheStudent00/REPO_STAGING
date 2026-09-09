#!/usr/bin/env bash
# ap3_l3_probe_the_x87_terms.sh -- task ap3: WHAT THE 32 x87 CELLS'
# TERMS ACTUALLY HOLD, before anything is written for them.
#
# Lane ap3_l2 answered the first question -- the probe lands (clang
# emits `faddp` for a `long double` add at ship flags) and not one of
# the 32 rows reads the arriving flag state, so the `no setter` cause
# is the driver demanding a composition for a row that is not a flag
# consumer.  This lane asks the second: what does each place's term
# READ, at what sort and width, and what does the arrival plan make of
# it -- because that decides whether an 80-bit holder is enough to
# render the cell or whether the arrival contract stops it first.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3; this lane
# runs no gate call and reads only the cells file.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import resource
import sys

HERE = "/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
sys.path.insert(0, HERE)
import z3
import emulate as E
import handful as H
import autopoly2 as A

A.use_task_ap2()
cells = A.read_json(A.CELLS)
wanted = {}
for run in A.read_runs(A.RUNS):
    cause = A.cause_of(run)
    if cause is None or "no setter row to compose" not in cause:
        continue
    wanted[(run["mnem"], run["shape"], run["key_width"])] = run

print("| cell | place | bits | the free symbols, with sort | families_of |")
print("|---|---|---|---|---|")
sorts = {}
for key in sorted(wanted):
    held = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
    row = H.chosen_row(cells, key, held)
    places, flags = H.terms_of_row(row)
    records = []
    for name in sorted(places or {}):
        records.append((name, H.memory_as_arrivals(places[name])))
    if flags is not None:
        records.append(("flags",
                        H.memory_as_arrivals(
                            z3.Concat(H.MT.as_bits(flags[1]),
                                      H.MT.as_bits(flags[2])))))
    for name, term in records:
        free = []
        for symbol in z3.z3util.get_vars(term):
            spelled = "%s:%s" % (symbol.decl().name(), symbol.sort())
            free.append(spelled)
            sorts[spelled.split(":", 1)[1]] = \
                sorts.get(spelled.split(":", 1)[1], 0) + 1
        try:
            families = H.families_of(term)
        except E.Refused as refusal:
            families = "REFUSED %s: %s" % (refusal.cause, refusal.detail)
        print("| `%s` %s %s | `%s` | %s | %s | %s |"
              % (key[0], key[1], key[2], name, term.size(),
                 " ".join(sorted(set(free))), families))

print("")
print("the sorts the 32 cells' terms read, and how often:")
for name in sorted(sorts, key=lambda s: (-sorts[s], s)):
    print("   %-24s %d" % (name, sorts[name]))

print("")
print("ONE CELL IN FULL, `faddl` mem_one 80 -- the row's own line and "
      "the place's term, LITERAL:")
held = {"mnem": "faddl", "shape": "mem_one", "key_width": 80}
row = H.chosen_row(cells, held["mnem"] and ("faddl", "mem_one", 80),
                   held)
print("   the row's line: %s" % row.get("text"))
print("   operands: %s" % (row.get("operands"),))
places, flags = H.terms_of_row(row)
for name in sorted(places):
    print("   place `%s`, %d bits:" % (name, places[name].size()))
    print("      %s" % places[name].sexpr().replace("\n", " "))
print("")
print("ONE MORE, `fucomi` st_st 80 -- it writes only the flags:")
held = {}
row = H.chosen_row(cells, ("fucomi", "st_st", 80), held)
print("   the row's line: %s" % row.get("text"))
places, flags = H.terms_of_row(row)
print("   places: %s" % sorted(places or {}))
if flags is not None:
    print("   the flag triple's setter name: %s" % (flags[0],))
    pair = z3.Concat(H.MT.as_bits(flags[1]), H.MT.as_bits(flags[2]))
    print("   the flag pair, %d bits:" % pair.size())
    print("      %s" % pair.sexpr().replace("\n", " ")[:2000])
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo "done"
