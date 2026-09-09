#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] operator_variants_by_search.py -- per-operator variant resolution by search over the six o3 rows"
python3 /projects/PseudoCoupHQ/Research/oracle/compiler_units/operator_variants_by_search.py
echo "[1/1] done"
