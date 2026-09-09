#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] operator_variants_by_search.py -- lhs/rhs type spellings moved to per-operand unit objects (spelling field), fixing the guard's void finding"
python3 PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.py
echo "[1/1] done"
