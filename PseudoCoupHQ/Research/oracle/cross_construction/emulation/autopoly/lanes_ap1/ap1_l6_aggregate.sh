#!/usr/bin/env bash
# ap1_l6_aggregate.sh -- task ap1: the loop's 1,012 runs read once and
# turned into the aggregate, the report, the reproduction table and the
# counts, then the spelling guard over every json this task wrote.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1. The one
# read is `autopoly_runs.jsonl`, the whole store, held in memory while
# the tables are computed; the sample lane measured the same read at
# 68,000 kB over twenty runs.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/6] the store"
wc -l autopoly_runs.jsonl
echo "[2/6] the aggregate"
python3 autopoly.py aggregate
echo "[3/6] the report"
python3 autopoly.py report
echo "[4/6] the counts"
python3 autopoly.py tally
echo "[5/6] the handful, reproduced"
python3 autopoly.py reproduce
echo "[6/6] the spelling guard, unmodified"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly_cells.json \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.json
