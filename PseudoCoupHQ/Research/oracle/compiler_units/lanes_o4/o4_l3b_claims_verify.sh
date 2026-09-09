#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_210 (after fixing the tail-6 paste and the py comment's literal 'exempt')"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  --json PseudoCoupHQ/Research/oracle/compiler_units/log_210_claims_final.json \
  PseudoCoupHQ/DevComms/log_210_task_o4_operator_variants_by_search.md
echo "verifier exit: $?"
