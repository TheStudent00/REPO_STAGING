#!/bin/bash
# cov1 lane 7 -- the standing verifier over log_266, re-run after the
# transcripts of $8 were added.
set -u
echo "[1/1] verifying log_266"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_266_task_cov1_how_far_the_proved_emulations_reach.md
echo "  exit: $?"
