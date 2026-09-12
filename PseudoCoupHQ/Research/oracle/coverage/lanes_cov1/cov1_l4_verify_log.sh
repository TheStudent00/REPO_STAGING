#!/bin/bash
# cov1 lane 4 -- the standing verifier over log_266, run from this
# instance as the law requires.
set -u
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_266_task_cov1_how_far_the_proved_emulations_reach.md
echo "  exit: $?"
