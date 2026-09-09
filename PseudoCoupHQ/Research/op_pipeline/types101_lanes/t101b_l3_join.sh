#!/usr/bin/env bash
# t101b lane 3 -- the join proper (the original brief's §2 steps 2-5)
# over the rows lane 2 wrote: the holder table, the spellings table, the
# per-entry holders with the coverage over the type keys, the
# disagreements.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] types101_join.py ========"
python3 types101_join.py
rc=$?
echo "types101_join.py exit ${rc}"
exit ${rc}
