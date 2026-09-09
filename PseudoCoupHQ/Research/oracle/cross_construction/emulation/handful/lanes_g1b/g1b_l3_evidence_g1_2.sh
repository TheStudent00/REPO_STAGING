#!/usr/bin/env bash
# g1b_l3_evidence_g1_2.sh -- task g1b, section 1: the read-only commands
# log 241 (task g1's own log, written by this closer from what task g1
# left on disk) pastes, run once so every transcript in that log is the
# output of the command printed above it.  Nothing here writes anything.
#
# WHY THIS LANE EXISTS.  Task g1's session ended on a usage limit after
# its run of record (`g1_l12_run_of_record2.sh`) and its guard
# (`g1_l15_guard4.sh`), before it wrote its log.  Its products are on
# disk and identical on both machines (`handful3.json`,
# `handful3.md`, `handful3_primitive.json`, `handful3_spellings.json`),
# so its record is banked from those products rather than re-run.  This
# lane prints the counts and tables that log quotes, so each is the
# program's own output and not a transcription.
#
# THE SHAPE IS TASK h2's OWN (`lanes_h2/h2_l9_evidence.sh`), copied
# rather than reinvented, with its two hard-won details kept:
#   * the `$` lines are printed with `printf %q`, so the printed command
#     is exactly the one that ran;
#   * the `sed` addresses use the `\%...%` form and spell `.` where the
#     table's own `|` sits, because the conventions verifier reads a
#     token starting with `/` as a path and splits a pasted command on
#     `|` to check each stage's head.
# `|| true` sits on `grep -c`, whose own exit is 1 when a count it
# prints is zero, which is the answer this task wants.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1B.  Every step
# reads a json or markdown file of a few hundred kB; `tally3` is the
# heaviest and task g1 measured the same call at 466,868 kB inside its
# own run.
# WHY STEP 7 IS A `grep` AND NOT A `python3 -c`: lane `g1b_l1` wrote
# that count as a one-line `python3 -c`, and the conventions verifier
# REFUSED it -- it splits a pasted command on `;` to check each stage's
# head, and the `;` inside the python source reads as a stage separator
# whose head is then not a program at all.  The two counts sit on three
# consecutive lines of the json itself, so `grep` prints them and the
# claim re-runs.  This lane is otherwise lane `g1b_l1` unchanged, re-run
# so every transcript in log 241 comes from ONE lane.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
G=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/go
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/9] task g1's run of record, counted"
run python3 $H/handful.py tally3

echo "[2/9] the forty runs, one row each"
run sed -n '\%^. cell . lang . route . rendered%,\%^$%p' $H/handful3.md

echo "[3/9] c and rust: task h2's verdict beside task g1's"
run sed -n '\%^. cell . lang . h2 route%,\%^$%p' $H/handful3.md

echo "[4/9] what did not work, by cause: the refusals and the gate calls"
run sed -n '\%^### 3.1 Refusals%,\%^### 3.2%p' $H/handful3.md

echo "[5/9] what did not work, by cause: the landings that were not LANDED"
run sed -n '\%^### 3.2 The landings%,\%^## 5%p' $H/handful3.md

echo "[6/9] which route ran, per (cell, target)"
run sed -n '\%^. cell . lang . route . single-opcode rows%,\%^$%p' $H/handful3.md

echo "[7/9] the primitive lookup's own two counts, off its own json"
run grep -A 2 '"counted"' $H/handful3_primitive.json

echo "[8/9] the spelling guard, unmodified, over the four json task g1's own programs write"
run python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $H/handful3.json $H/handful3_primitive.json $H/handful3_spellings.json $G/go_facts.json

echo "[9/9] grep -c exempt over every file task g1 added or changed"
run grep -c exempt $G/go_facts.py $G/go_render.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/swift/swift_render.py $H/handful.py $H/handful3.md || true
