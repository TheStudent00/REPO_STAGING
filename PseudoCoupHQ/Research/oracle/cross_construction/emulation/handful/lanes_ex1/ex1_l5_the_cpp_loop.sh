#!/usr/bin/env bash
# ex1_l5_the_cpp_loop.sh -- task ex1, step 4: THE LOOP.  253 cells on
# cpp, the fifth compiled target, through exactly the route tasks g1 to
# ap4 put the other four through.
#
# MEMORY BOUND: 6 GB resident on the one collecting process, named abort
# ABORT_MEMORY_EX1, checked after every run.  The sample of lane
# ex1_l4 measured 259,164 kB over its first twenty runs, and task ap4's
# own 1,012-run lane peaked at 2,427,092 kB.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/3] the loop"
python3 expand1.py run
echo ""
echo "[2/3] the aggregate"
python3 expand1.py aggregate
echo ""
echo "[3/3] the tally"
python3 expand1.py tally
echo "done"
