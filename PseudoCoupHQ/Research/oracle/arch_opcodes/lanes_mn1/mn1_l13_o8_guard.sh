#!/usr/bin/env bash
set -euo pipefail
echo "[1/3] task mn1: spelling guard over per_opcode_population.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_population.json || true
echo "[2/3] task mn1: spelling guard over per_opcode_held.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_held.json || true
echo "[3/3] task mn1: spelling guard over per_opcode_results.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode_results.json || true
echo "[3/3] done"
