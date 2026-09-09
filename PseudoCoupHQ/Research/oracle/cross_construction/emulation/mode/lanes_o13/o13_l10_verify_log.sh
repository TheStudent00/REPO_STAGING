#!/bin/bash
# task o13, lane 10: the closing verifier -- re-run every reproducing
# command log_231 pastes and report the tally, zero DIFFERS required.
set -u
echo "[1/1] verify log_231"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  /projects/PseudoCoupHQ/DevComms/log_231_task_o13_mode_rendered_guard.md
echo "lane o13_l10 done"
