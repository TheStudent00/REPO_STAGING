#!/usr/bin/env bash
# t101b lane 4 -- re-run of the join (lane 3 exited 1: a Counter/defaultdict
# mix-up in holders_table's off_holder accumulator, fixed at cause in
# types101_join.py; see log for the one-line diff). Same work as lane 3:
# the original brief's §2 steps 2-5 over the rows lane 2 wrote -- the
# holder table, the spellings table, the per-entry holders with the
# coverage over the type keys, the disagreements.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] types101_join.py ========"
python3 types101_join.py
rc=$?
echo "types101_join.py exit ${rc}"
exit ${rc}
