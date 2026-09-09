#!/usr/bin/env bash
# lane 1c/3 -- `unit` id changed from "row_id:operator" (itself a
# colon-joined spelling shape) to an opaque "row_id#index".
set -euo pipefail
echo "[1/1] compiler_operators_used.py (unit id no longer joins the operator token)"
python3 PseudoCoupHQ/Research/oracle/compiler_units/compiler_operators_used.py
echo "[1/1] done"
