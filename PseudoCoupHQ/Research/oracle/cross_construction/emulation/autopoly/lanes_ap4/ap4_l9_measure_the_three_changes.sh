#!/usr/bin/env bash
# ap4_l9_measure_the_three_changes.sh -- task ap4: each change measured
# on EXACTLY the (cell, target) pairs it targets, before the loop runs.
#
#  [1] CHANGE 1, the derived arrival: task ap3's own runs whose cause
#      holds `the IN rows cannot be aligned`.
#  [2] CHANGE 3, the identity: task ap3's own runs whose cause holds
#      `this unit record carries no body`.
#  [3] CHANGE 2, the x87 stack: task ap3's own runs whose cause holds
#      `answer home or arrival on the x87 stack`, and the 30 c rows
#      inside them.
#  [4] THE PIN: which `long double` argument is at which stack slot,
#      compiled at the corpus's own ship flags, so the argument order
#      change 2's alignment reads off the displacement is a measured
#      fact and not an assumption.
#
# NOTHING IS WRITTEN to the loop's store: `measure` re-runs pairs and
# prints, it does not append.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP4.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo '[0/4] THE PIN: the stack slot of each long double argument'
python3 - <<'PY'
import os
import sys
HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, HERE)
import emulate as E
for name, body in (("a_minus_b", "return a - b;"),
                   ("b_minus_a", "return b - a;"),
                   ("a_over_b", "return a / b;"),
                   ("b_over_a", "return b / a;")):
    source = ("long double emu_probe_%s(long double a, long double b)\n"
              "{\n    %s\n}\n" % (name, body))
    got, refusal = E.compile_and_carve(source, "emu_probe_%s" % name)
    if got is None:
        print("   %-10s COMPILE OR CARVE REFUSED: %s" % (name, refusal))
        continue
    print("   %-10s %-16s -> %s" % (name, body, "; ".join(got[1])))
PY

echo ""
echo "[1/4] CHANGE 1 -- the derived arrival"
python3 autopoly4.py measure "the IN rows cannot be aligned" 2>&1 | tail -40

echo ""
echo "[2/4] CHANGE 3 -- the identity"
python3 autopoly4.py measure "carries no body" 2>&1 | tail -90

echo ""
echo "[3/4] CHANGE 2 -- the x87 stack"
python3 autopoly4.py measure "answer home or arrival on the x87 stack" 2>&1 | tail -140
echo "done"
