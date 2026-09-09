#!/usr/bin/env bash
# ap2_l9_probe_fix1.sh -- task ap2: what the 134 runs of the cause
# `term reads state that is not an arrival register` actually read.
#
# Fix 1 renders a literal MEMORY operand as one more arriving value.
# Lane ap2_l8 measured it on exactly those 134 pairs and not one moved,
# so either the population holds no memory symbol at all or the rewrite
# does not reach it.  This lane prints the DETAIL each refusal carries
# -- which is the symbol name `families_of` refused -- for task ap1's
# runs and for the same cells run again now.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
import autopoly2 as A
import handful as H

A.use_task_ap2()
cells = A.read_json(A.CELLS)

wanted = []
for run in A.read_runs(A.AP1_RUNS):
    cause = A.cause_of(run)
    if cause is None or "not an arrival register" not in cause:
        continue
    wanted.append(run)
print("task ap1's runs with that cause: %d" % len(wanted))

# THE DETAIL TASK ap1 RECORDED, which is the symbol the refusal names.
detail = {}
for run in wanted:
    place = A.the_weakest_place(run)
    text = (place or {}).get("refusal_detail")
    detail[text] = detail.get(text, 0) + 1
print("")
print("the symbol each of task ap1's refusals names:")
for text in sorted(detail, key=lambda t: (-detail[t], str(t))):
    print("   %4d  %s" % (detail[text], text))

seen = {}
for run in wanted:
    seen[A.the_same_cell(cells, run)] = 1
print("")
print("distinct cells: %d" % len(seen))
print("")
print("| cell | place | bits | families now | refusal now | free "
      "symbols of the term |")
print("|---|---|---|---|---|---|")
import term as T
for key in sorted(seen):
    held = H.cell_input(cells, key)
    if held.get("refusal_cause") is not None:
        print("| `%s` %s %s | -- | -- | -- | %s: %s | -- |"
              % (key[0], key[1], key[2], held["refusal_cause"],
                 held.get("refusal_detail")))
        continue
    for place in held["places"]:
        names = []
        for symbol in T.free_symbols_in_order(place["term"]):
            names.append("%s:%s" % (symbol.decl().name(),
                                    symbol.sort()))
        print("| `%s` %s %s | %s | %s | %s | %s | %s |"
              % (key[0], key[1], key[2], place["writes"],
                 place.get("bits"), place.get("families"),
                 place.get("not_rendered_detail"),
                 " ".join(sorted(set(names)))))
PY
echo "done"
