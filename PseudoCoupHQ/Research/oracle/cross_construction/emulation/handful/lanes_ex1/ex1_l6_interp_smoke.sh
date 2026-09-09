#!/usr/bin/env bash
# ex1_l6_interp_smoke.sh -- task ex1, step 5: THE SAMPLE RULE STATED
# BEFORE ANYTHING RUNS, and then the first cell on all seven
# interpreted targets, so a syntax error in a dialect is found on seven
# runs rather than on seventy.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX1; each runner is a separate short-lived process
# handed the whole sample at once.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/3] the runners, as this machine answers them"
python3 ../interp/interp_render.py runners

echo ""
echo "[2/3] THE SAMPLE RULE, LITERAL, before anything runs"
python3 expand1.py interp_sample

echo ""
echo "[3/3] the first cell on all seven targets"
python3 expand1.py interp_run 7
echo "done"
