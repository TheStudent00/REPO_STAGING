#!/bin/bash
# task o13, lane 12: the closing verifier, second pass -- after fixing
# the one DIFFERS lane 10 found (a relative-path grep command), re-run
# every reproducing command log_231 pastes.
set -u
echo "[1/1] verify log_231, pass 2"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_231_task_o13_mode_rendered_guard.md
echo "lane o13_l12 done"
