#!/usr/bin/env bash
# g1b_l13_evidence2.sh -- task g1b: every read-only command log 242
# pastes, run once so each transcript in that log is the output of the
# command printed above it.  Nothing here writes anything.
#
# THE SHAPE IS TASK h2's OWN (`lanes_h2/h2_l9_evidence.sh`), with its
# two hard-won details kept: the `$` lines are printed with `printf %q`,
# and the `sed` addresses use the `\%...%` form and spell `.` where a
# table's own `|` sits, because the conventions verifier reads a token
# starting with `/` as a path and splits a pasted command on `|`.  No
# `python3 -c` appears here: the verifier splits on `;` too, and python
# source carrying a `;` is then read as a stage whose head is not a
# program, which is what it REFUSED in lane `g1b_l1`.
#
# `|| true` sits on `grep -c`, whose own exit is 1 when a count it
# prints is zero, which is the answer this task wants.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1B.  The
# heaviest step is `tally3b` over a 392 kB json; `bodies3c` reads one
# 4.9 MB corpus file at a time and task g1b measured it at 81,636 kB.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/14] the swift compiler this run used, LITERAL"
run /persist/swift/usr/bin/swiftc --version

echo "[2/14] the second run of record, counted"
run python3 $H/handful.py tally3b

echo "[3/14] the forty runs on the rebuilt image, one row each"
run sed -n '\%^. cell . lang . route . rendered%,\%^$%p' $H/handful3b.md

echo "[4/14] task g1's verdict beside this run's, all forty"
run sed -n '\%^. cell . lang . g1 route%,\%^$%p' $H/handful3b.md

echo "[5/14] what did not work, by cause: the refusals and the gate calls"
run sed -n '\%^### 3.1 Refusals%,\%^### 3.2%p' $H/handful3b.md

echo "[6/14] what did not work, by cause: the landings that were not LANDED"
run sed -n '\%^### 3.2 The landings%,\%^## 4%p' $H/handful3b.md

echo "[7/14] which (cell, target) pairs the WIDENED lookup changes"
run python3 $H/handful.py changes3c

echo "[8/14] why it reaches that cell in c and in no other target"
run python3 $H/handful.py whynot3c idiv gpr_one 32

echo "[9/14] what each target's own corpus holds at that arch mnemonic"
run python3 $H/handful.py bodies3c idiv

echo "[10/14] the widened lookup's own run: the row, the route, the setup cell"
run sed -n '\%^. cell . lang . route . single-opcode rows%,\%^$%p' $H/handful3c.md

echo "[11/14] the widened lookup's own run: the verdict, beside task g1's"
run sed -n '\%^. cell . lang . g1 route%,\%^$%p' $H/handful3c.md

echo "[12/14] the parameter-plan fix: which re-posed places it can move"
run python3 $H/handful.py rechecked3b
run python3 $H/handful.py rechecked3c

echo "[13/14] the spelling guard, unmodified, over every json this task's own programs write"
run python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $H/handful3b.json $H/handful3b_primitive.json $H/handful3b_spellings.json $H/handful3c.json $H/handful3c_primitive.json

echo "[14/14] grep -c exempt over every file this task added or changed"
run grep -c exempt $H/handful.py $H/handful3b.md $H/handful3c.md $H/lanes_g1b/g1b_l8_run_of_record_b.sh $H/lanes_g1b/g1b_l11_run_of_record_c2.sh || true
