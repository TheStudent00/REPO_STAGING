#!/usr/bin/env bash
# ap3_l12_run_the_loop_with_the_fix_off.sh -- task ap3, FIX 4: the
# IDENTICAL loop with task h2's normalise-before-render OFF.
#
# THE QUESTION, open since task h2 and item 4 of log_244's awaiting-the owner
# list.  Task h2's fix 1 hands the renderer the term the pipeline's own
# normaliser leaves rather than the `order_commutative(simplify(term))`
# task h1 handed it.  It was measured on task h2's 24 places and was a
# no-op on all 24; a task-name gate then kept it OFF for `g1b`, `g1c`
# and the whole of task ap1's loop; task ap2 turned it on ALONGSIDE
# FIVE OTHER FIXES.  So what it does at the scale of a thousand runs
# has never been measured on its own.
#
# THE MEASUREMENT: the same 253 cells, the same order, the same
# ceilings, both of this task's own fixes ON, and one switch moved.
# The runs go onto their OWN store (`autopoly3_off_runs.jsonl`) and
# their own source folder (`src3_off/`), so this lane cannot write the
# loop of record and cannot read it.  `autopoly3.py fix4` is what reads
# the two.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3, checked
# after every run.
set -euo pipefail
mkdir -p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/src3_off
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 autopoly3.py off_run
