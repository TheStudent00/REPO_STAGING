#!/usr/bin/env bash
set -euo pipefail
echo "[1/2] task mn1: spelling guard over single_opcode_units.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json || true
echo "[2/2] task mn1: spelling guard over unique_opcodes.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json || true
echo "[2/2] done"
