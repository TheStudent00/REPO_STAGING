#!/usr/bin/env bash
# ref1 lane 26 -- LAW's final lane: re-run every command this task's log
# pasted, from this task's own instance, and print the tally.
set -euo pipefail
total=1
echo "[1/$total] the verifier over log 256"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_256_task_ref1_level0_against_an_independent_reading.md
