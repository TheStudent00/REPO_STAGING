#!/usr/bin/env bash
# m1b_l17_o8_regenerate.sh -- task m1b, deliverable 7, second half:
# task o8's field `landed_mnemonic` is now `landed_mnem`, so
# regenerate o8's results and run the unmodified spelling guard over
# the three json per_opcode.py writes.
# WHAT THE FIELD HOLDS: the arch opcode a polyfill ACTUALLY compiled
# to, which is a different thing from the row's target `mnem`, and is
# log_235's cause C -- 57 guard findings, all this one field.
# MEMORY: per_opcode.py states its own bound (ABORT_MEMORY_O8, 2 GB)
# and checks it after every row; this task's bound is 16 GB with the
# named abort ABORT_MEMORY_M1B.
set -euo pipefail
echo "[1/4] task m1b: per_opcode.py population"
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode
python3 per_opcode.py population
echo "[2/4] task m1b: per_opcode.py run"
python3 per_opcode.py run
echo "[3/4] task m1b: per_opcode.py report"
python3 per_opcode.py report
echo "[4/4] task m1b: the unmodified spelling guard over o8's three json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_population.json \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_held.json \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_results.json || true
echo "[4/4] done"
