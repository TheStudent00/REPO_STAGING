#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_no_spelling_keys.py over operator_variants_by_search.json (after the tuple_expression/dictionary_literal fix)"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  /projects/PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.json
echo "guard exit: $?"
