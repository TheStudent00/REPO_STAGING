#!/usr/bin/env bash
# t101b lane 7 -- the conventions verifier over this task's own
# DevComms log, per LAW.md's "Final lane" rule.
set -u
echo "[1/1] check_conventions_log_claims.py"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_217_task_t101b_dominant_types_join.md
rc=$?
echo "check_conventions_log_claims.py exit ${rc}"
exit ${rc}
