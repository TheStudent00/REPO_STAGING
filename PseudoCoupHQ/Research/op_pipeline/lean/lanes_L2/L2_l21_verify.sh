#!/bin/bash
# L2 lane 21 -- the LAW's mandatory final lane: check_conventions_log_claims.py
# (unmodified) over log_232, run FROM the L2 instance.
set -u
TOTAL=1
echo "[1/$TOTAL] check_conventions_log_claims.py --verify over log_232"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_232_task_L2_model_translator.md
echo "--- exit $?"
