#!/usr/bin/env bash
# lane 9 -- task o3b, correction: spelling-key guard over the
# corrected six-row compiler_operators_used.json (run regardless, per
# the brief's own instruction -- this is a token census, not a
# matching/pairing task, but the guard runs over every json written
# anyway).
set -uo pipefail
echo "[1/1] check_no_spelling_keys.py over compiler_operators_used.json (six rows, task o3b correction)"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  /projects/PseudoCoupHQ/Research/oracle/compiler_units/compiler_operators_used.json
echo "guard exit: $?"
