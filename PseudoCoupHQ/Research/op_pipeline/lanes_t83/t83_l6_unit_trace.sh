#!/usr/bin/env bash
# t83 lane 6 -- the unit the sample died in, traced row by row.  Every
# attached callee body walks alone in under 0.21 s and 57 MB (lane 5),
# so the runaway is not a body: it is what the caller is carrying when
# the body is walked.  This lane measures that, bounded at 3 GB and
# 300 s in a forked child so it names its own abort.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/1] c/regen_1859 -- 16 body lines, 32 ledger rows"
python3 probe83f_one_unit_trace.py canon40_regen_store/op_units2_c_c0004.json regen_1859
echo "exit $?"
