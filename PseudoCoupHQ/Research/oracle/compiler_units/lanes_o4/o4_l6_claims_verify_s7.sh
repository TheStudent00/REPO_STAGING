#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_210 (with section 7, nested-operand extension, appended)"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  --json /projects/PseudoCoupHQ/Research/oracle/compiler_units/log_210_claims_s7.json \
  /projects/PseudoCoupHQ/DevComms/log_210_task_o4_operator_variants_by_search.md
echo "verifier exit: $?"
