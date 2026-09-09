#!/usr/bin/env bash
# lane 1/1 -- run compiler_operators_used.py inside the o3 sandbox.
set -euo pipefail
echo "[1/1] compiler_operators_used.py"
python3 PseudoCoupHQ/Research/oracle/compiler_units/compiler_operators_used.py
echo "[1/1] done"
