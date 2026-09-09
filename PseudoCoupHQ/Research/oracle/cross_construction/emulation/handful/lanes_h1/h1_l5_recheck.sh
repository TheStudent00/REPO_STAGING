#!/usr/bin/env bash
# h1_l5_recheck.sh -- task h1: the four gate calls the pipeline's own
# 3,000 ms ceiling left UNDECIDED, re-posed with 300,000 ms.
#
# WHY: the law's rule -- a time limit is a FLAG, so the obligation is
# re-run with more room and whether the answer changed is reported.
# The verdict of record stays the 3,000 ms one; this answer sits beside
# it, over the same two terms with the same alignment.
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H1, checked
# after every re-pose. The run lane peaked at 445,684 kB, and a solver
# given a hundred times the wall clock can hold more, so this lane is
# where the bound is most likely to bite; it prints its peak per call.
set -euo pipefail
echo "[1/3] task h1: handful.py recheck 300000"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py recheck 300000
echo "[2/3] the report again, with the re-posed answers on it"
python3 handful.py report
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json
echo "[3/3] done"
