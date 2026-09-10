#!/usr/bin/env bash
# hub1_l18_verifier.sh -- task hub1, lane 18: the conventions verifier over
# this task's report, as the law's final-lane obligation requires. It runs
# FROM this task's own instance and writes nothing but its own report line.
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log 252"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_252_task_hub1_hub_v1_first_form.md
