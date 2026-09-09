#!/usr/bin/env bash
# ap1_l3_aggregate_probe.sh -- task ap1: the aggregate, the report, the
# reproduction table and the spelling guard, run over the TWENTY sample
# runs and not over the loop.
#
# WHY BEFORE THE LONG RUN: every one of those four steps reads the whole
# store and none of them has been run yet. Finding a defect in them
# after three hours of compute would cost the compute; finding it here
# costs fourteen seconds. The products this lane writes are overwritten
# by the same commands after the loop finishes.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/5] the aggregate"
python3 autopoly.py aggregate
echo "[2/5] the report"
python3 autopoly.py report
echo "[3/5] the tally"
python3 autopoly.py tally
echo "[4/5] the handful, reproduced"
python3 autopoly.py reproduce
echo "[5/5] the spelling guard, unmodified, over every json this task writes"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_cells.json \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.json
