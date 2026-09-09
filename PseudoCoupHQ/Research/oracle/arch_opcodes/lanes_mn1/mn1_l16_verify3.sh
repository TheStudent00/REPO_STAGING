#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: check_conventions_log_claims.py --verify over log_235, third pass"
cd PseudoCoupHQ
python3 Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 \
  DevComms/log_235_task_mn1_mnem_field_rename.md
echo "[1/1] done"
