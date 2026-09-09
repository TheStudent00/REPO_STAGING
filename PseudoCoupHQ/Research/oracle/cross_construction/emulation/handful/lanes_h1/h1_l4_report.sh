#!/usr/bin/env bash
# h1_l4_report.sh -- task h1: handful.json -> handful.md, and the
# unmodified spelling guard over every json this task wrote.
# MEMORY: the report walks the twenty runs it is handed; the bound is
# the task's 4 GB with the named abort ABORT_MEMORY_H1.
set -euo pipefail
echo "[1/3] task h1: handful.py report"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py report
echo "[2/3] the spelling guard, unmodified, over every json this task wrote"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful_cells.json \
    /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json
echo "[3/3] done"
