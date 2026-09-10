#!/usr/bin/env bash
# ex1_l12_interp_the_seventy_e.sh -- task ex1, step 6, fifth pass, and
# the one thing left was not a dialect at all: THE INTERPRETED ROUTE
# WAS SKIPPING A DRIVER FIX THE COMPILED ROUTE RUNS.
#
# Task h2's fix 2, `handful.projected_lane`: a vector cell's place
# carries the whole 128-bit register, and the lane the operation writes
# is projected out of it before anything is rendered.  Without it the
# term reads `Extract(127, 32, v0)` and the ONE renderer's own planner
# refuses `vector arrival used beyond its low lane` -- which is exactly
# what all fourteen `addss` and `cvtsi2sd` runs of the previous passes
# recorded, while THE SAME TWO CELLS render, compile, carve and prove
# on cpp in this task's own compiled loop.  Lane ex1_l11 measured that
# the two cells files hold the same row and the same term, so the
# difference was in the route and not in the cell.  The fix is now
# called from the interpreted route at the same point, over the same
# objects.
#
# The fourth pass's store is kept as `expand1_interp_pass4.jsonl`.
# Nothing is deleted.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX1.  This pass also builds the pipeline's own walk,
# which task ap4 measured at about 260 MB.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/4] the fourth pass's store, kept under its own name"
if [ -f expand1_interp.jsonl ] && [ ! -f expand1_interp_pass4.jsonl ]; then
    mv expand1_interp.jsonl expand1_interp_pass4.jsonl
    echo "   expand1_interp.jsonl -> expand1_interp_pass4.jsonl"
    wc -l expand1_interp_pass4.jsonl
else
    echo "   nothing to move"
fi

echo ""
echo "[2/4] the seventy"
python3 expand1.py interp_run

echo ""
echo "[3/4] the aggregate"
python3 expand1.py interp_aggregate

echo ""
echo "[4/4] the table"
python3 expand1.py interp_table
echo "done"
