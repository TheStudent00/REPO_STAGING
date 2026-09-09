#!/bin/bash
# o10_l8_verify3.sh -- task o10: verify this task's DevComms log,
# rerun after fixing the two DIFFERS pass 1 found.
set -euo pipefail
cd /projects/PseudoCoupHQ
echo "[1/1] task o10: check_conventions_log_claims.py --verify (pass 3)"
python3 Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 \
  DevComms/log_225_task_o10_ledger_signature_census.md
echo "[1/1] done"
