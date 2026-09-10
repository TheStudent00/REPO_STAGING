#!/usr/bin/env bash
# ap5_l7_preflight_and_the_sample.sh -- task ap5: the outer set as the
# loop will walk it, and the twenty-run memory sample the law asks for
# before a thousand runs are started.
#
# MEMORY BOUND, stated as the law requires: 6 GB resident on the one
# collecting process, named abort ABORT_MEMORY_AP5, checked after every
# run by `autopoly5.check_memory`.  The sample is the first twenty runs
# of the loop's own order, written to the loop's own store, so the loop
# resumes from them rather than repeating them.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/2] preflight"
python3 autopoly5.py preflight
echo ""
echo "[2/2] the twenty-run sample"
python3 autopoly5.py run 20
echo "done"
