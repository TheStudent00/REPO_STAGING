#!/usr/bin/env bash
# lane 1b/2 -- rerun after adding lang/unit fields to each operator
# member object so it reads as a UNIT OBJECT under the spelling guard's
# except-list, not a bare-token grouping row.
set -euo pipefail
echo "[1/1] compiler_operators_used.py (fixed member shape)"
python3 /projects/PseudoCoupHQ/Research/oracle/compiler_units/compiler_operators_used.py
echo "[1/1] done"
