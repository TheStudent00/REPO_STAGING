#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] operator_variants_by_search.py -- re-run after extending unwrap_and_resolve with the four nested-operand rules (nested binary-operator operand, unary recursion generalized to every language, composite/array literal written type, qualified_identifier/this/self)"
python3 /projects/PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.py
echo "[1/1] done"
