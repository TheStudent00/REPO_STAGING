#!/usr/bin/env bash
# h1b_l1_compose_report.sh -- task h1b, the closer on task h1: the
# composition column.  `handful.py compose` adds one field,
# `composition`, to every run already on `handful.json` -- the raw
# carved body of the run's own destination place, classified into
# table cells by task m1b's own classifier -- then `handful.py report`
# regenerates `handful.md` with the new column, then the unmodified
# spelling guard runs over every json this task touches.
# MEMORY: one collecting process, the same 4 GB bound and named abort
# ABORT_MEMORY_H1 task h1 stated, since `compose` runs inside the same
# script and reads one more file (`model_table_rows.json`, 50 MB,
# sampled first and its peak RSS printed).
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
echo "[1/3] task h1b: handful.py compose"
python3 handful.py compose
echo "[2/3] task h1b: handful.py report"
python3 handful.py report
echo "[3/3] the spelling guard, unmodified, over every json this task touched"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful_cells.json \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json
echo "done"
