#!/usr/bin/env bash
# ap1_l4_aggregate_probe2.sh -- task ap1: the aggregate, the report, the
# reproduction table and the spelling guard, run over the TWENTY sample
# runs and not over the loop.
#
# THE SECOND PASS: lane `ap1_l3_aggregate_probe.sh` failed the guard
# at the last step -- the aggregate carried a field `cell` holding the
# triple joined into one string (`and|gpr_gpr|32`), which is a row key
# carrying an operator token. The guard was right; the record is now
# written its way, the triple in three fields with the mnemonic in
# `mnem`. This lane is that same sequence again.
#
# WHY BEFORE THE LONG RUN: every one of those four steps reads the whole
# store and none of them has been run yet. Finding a defect in them
# after three hours of compute would cost the compute; finding it here
# costs fourteen seconds. The products this lane writes are overwritten
# by the same commands after the loop finishes.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/5] the aggregate"
python3 autopoly.py aggregate
echo "[2/5] the report"
python3 autopoly.py report
echo "[3/5] the tally"
python3 autopoly.py tally
echo "[4/5] the handful, reproduced"
python3 autopoly.py reproduce
echo "[5/5] the spelling guard, unmodified, over every json this task writes"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_cells.json \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.json
