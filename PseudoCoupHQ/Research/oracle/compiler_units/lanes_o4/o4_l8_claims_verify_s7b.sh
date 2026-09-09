#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_210 (section 7, final, after fixing the two truncated cat pastes and the grep -c exempt paste)"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  --json PseudoCoupHQ/Research/oracle/compiler_units/log_210_claims_s7_final.json \
  PseudoCoupHQ/DevComms/log_210_task_o4_operator_variants_by_search.md
echo "verifier exit: $?"
