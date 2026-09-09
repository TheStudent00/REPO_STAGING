#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] operator_variants_by_search.py -- re-run after excluding tuple_expression/dictionary_literal from the generalized unary fallback (their grammar's own 'value' field names only the FIRST element, not a genuine single operand -- found during verification, fixed at the cause)"
python3 /projects/PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.py
echo "[1/1] done"
