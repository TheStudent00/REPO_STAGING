#!/usr/bin/env bash
# t104 lane 12 -- LAW's memory/time-limit rule applied to lane 10's own
# pass-2 tail: 184 of the 27,866 layer5-bearing units in term66_store
# failed lane 10's pass 2 (3,072 MB / 900 s, 3 workers), every one for
# MEMORY_REASON at 1-2 seconds wall (not a timeout) with sub-process
# peak resident right at the 3,072 MB ceiling.  A ceiling that small is
# a FLAG, not an answer: this lane re-runs ONLY those 184 through
# `t104_walk.py`'s own `run_pass2` (imported, not re-typed) at a higher
# ceiling and 1 worker (so the retry's own memory is bounded by that
# one ceiling and stays inside the instance's declared 8g), and reports
# whether the answer changes.  term66_store/ is never opened for
# writing; term104_store/ only gains records for units that converge
# this time.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] pass 2 retry, 7168 MB / 100 s, 1 worker"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_pass2_retry.py 7168 100
echo "exit $?"
