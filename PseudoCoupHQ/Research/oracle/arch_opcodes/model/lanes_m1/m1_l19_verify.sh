#!/usr/bin/env bash
# m1_l19_verify.sh -- task m1: check_conventions_log_claims.py --verify
# over log_236, run from this task's own instance on the tower, as LAW
# requires as the final lane.
set -euo pipefail
echo "[1/1] task m1: check_conventions_log_claims.py --verify over log_236"
cd /projects/PseudoCoupHQ
python3 Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 \
  DevComms/log_236_task_m1_arch_opcode_model_table.md
echo "[1/1] done"
