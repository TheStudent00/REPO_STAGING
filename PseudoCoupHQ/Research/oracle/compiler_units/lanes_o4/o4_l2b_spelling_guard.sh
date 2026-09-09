#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_no_spelling_keys.py over operator_variants_by_search.json (final)"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.json
echo "guard exit: $?"
