#!/usr/bin/env bash
set -u
cd /projects/PseudoCoupHQ
echo "======== verifying log_214 (this bank's own log) ========"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 DevComms/log_214_task_t102_bank_rounds_16_19_and_founding.md
echo "---- exit $? ----"
