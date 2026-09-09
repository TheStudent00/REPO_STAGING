#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_no_spelling_keys.py over compiler_operators_used.json (final)"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/compiler_units/compiler_operators_used.json
echo "guard exit: $?"
