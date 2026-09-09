#!/usr/bin/env bash
# m1b_l25_verify2.sh -- task m1b: LAW's final lane. Re-run every command
# this task's log pasted, from this task's own instance, and sort each
# claim into matches / differs / unverifiable.
set -euo pipefail
echo "[1/1] task m1b: check_conventions_log_claims.py --verify"
cd PseudoCoupHQ
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_237_task_m1b_model_table_join_closer.md
echo "[1/1] done"
