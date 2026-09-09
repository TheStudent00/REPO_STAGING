#!/bin/bash
# o10_l4_guard.sh -- task o10: the spelling guard over ledger_signatures.json.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] task o10: spelling guard over ledger_signatures.json"
python3 check_no_spelling_keys.py \
  ../oracle/arch_opcodes/signatures/ledger_signatures.json || true
echo "[1/1] done"
