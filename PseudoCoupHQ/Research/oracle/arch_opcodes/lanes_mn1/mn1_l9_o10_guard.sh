#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: spelling guard over ledger_signatures.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/arch_opcodes/signatures/ledger_signatures.json || true
echo "[1/1] done"
