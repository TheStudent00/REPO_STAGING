#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_216"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  /projects/PseudoCoupHQ/DevComms/log_216_task_o6_go_types_oracle.md
echo "verifier exit: $?"
