#!/usr/bin/env bash
# m1_l4_sweep.sh -- task m1: model_table.py sweep. Runs
# model_translate.sweep (the same function that wrote model_L2.json)
# over the reference's whole opcode table, then re-runs each TRANSLATED
# attempt's own line to hold the z3 term of every place it wrote and
# prints it by term.Term.normalize. Writes model_table_rows.json.
# MEMORY BOUND: 16g resident, named abort ABORT_MEMORY_M1
# (resource.getrusage, checked every 5,000 rows); the L2 sweep ran under
# 8g. Peak RSS is printed by the script itself.
set -euo pipefail
echo "[1/1] task m1: model_table.py sweep"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py sweep
echo "[1/1] done"
