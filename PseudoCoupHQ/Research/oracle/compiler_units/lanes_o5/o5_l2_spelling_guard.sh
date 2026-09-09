#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_no_spelling_keys.py over lowering_route_cut.json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/compiler_units/lowering_route_cut.json
echo "guard exit: $?"
