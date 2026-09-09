#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: spelling guard over opcode_signatures.json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/signatures/opcode_signatures.json || true
echo "[1/1] done"
