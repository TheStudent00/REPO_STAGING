#!/usr/bin/env bash
# m1b_l8_sweep.sh -- task m1b: model_table.py sweep, re-run whole.
# The sweep is re-run over the WHOLE table, not over the x87 mnemonics
# alone, for one mechanical reason: `key_width` is a new field on
# EVERY row, and a row's `row_id` is its position in the sweep's own
# output, which the three added shapes move. A partial re-run would
# leave two row-id spaces in one document.
# What it re-measures: the three x87 operand shapes now in
# `model_translate.shapes_for`, and `reference.build_binary`'s
# one-operand branch, which no longer gives `add`, `and`, `or`, `sub`
# and `xor` the accumulator-pair widening multiply.
# MEMORY BOUND: 16 GB resident, named abort ABORT_MEMORY_M1B
# (resource.getrusage, checked every 5,000 rows); m1's own run of this
# command peaked at 190 MB. Peak RSS is printed by the script.
set -euo pipefail
echo "[1/1] task m1b: model_table.py sweep"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py sweep
echo "[1/1] done"
