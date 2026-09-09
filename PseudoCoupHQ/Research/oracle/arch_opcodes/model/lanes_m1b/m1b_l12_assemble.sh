#!/usr/bin/env bash
# m1b_l12_assemble.sh -- task m1b: model_table.py assemble, then
# report. The join is now keyed by (mnem, shape, key_width) on both
# sides, the coverage table over the corpus's 162 mnemonics is built
# here, and model_table.json / model_table.md are rewritten whole.
# MEMORY BOUND: 16 GB resident, named abort ABORT_MEMORY_M1B; this
# command holds the three documents at once (m1's own run peaked at
# 251 MB, on smaller documents). Peak RSS printed by the script.
set -euo pipefail
echo "[1/2] task m1b: model_table.py assemble"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py assemble
echo "[2/2] task m1b: model_table.py report"
python3 model_table.py report
echo "[2/2] done"
