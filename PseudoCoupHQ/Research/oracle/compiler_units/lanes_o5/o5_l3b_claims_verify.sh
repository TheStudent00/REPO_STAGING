#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_215, after the row-order fix"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  /projects/PseudoCoupHQ/DevComms/log_215_task_o5_lowering_route_cut.md
echo "verifier exit: $?"
