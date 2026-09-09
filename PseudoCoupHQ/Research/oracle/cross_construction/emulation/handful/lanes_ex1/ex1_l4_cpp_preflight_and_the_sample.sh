#!/usr/bin/env bash
# ex1_l4_cpp_preflight_and_the_sample.sh -- task ex1, step 3: the fifth
# compiled target's own probe, the outer set as the loop will walk it,
# and the twenty-run memory sample the law asks for before 253 runs are
# started.
#
# MEMORY BOUND, stated as the law requires: 6 GB resident on the one
# collecting process, named abort ABORT_MEMORY_EX1, checked after every
# run.  The sample is the first twenty runs of the loop's own order,
# written to the loop's own store, so the loop resumes from them rather
# than repeating them.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation

echo "[1/3] the cpp renderer's own probe: one term rendered, compiled and carved"
python3 cpp/cpp_render.py flags
echo ""
python3 cpp/cpp_render.py probe

echo ""
echo "[2/3] preflight"
cd autopoly
python3 expand1.py preflight

echo ""
echo "[3/3] the twenty-run sample"
python3 expand1.py run 20
echo "done"
