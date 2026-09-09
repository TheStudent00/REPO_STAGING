#!/usr/bin/env bash
# t101b lane 8 -- second (final) verifier pass, after fixing the
# fenced-block-merge and git-command issues the first pass (lane 7)
# found in log_217.
set -u
echo "[1/1] check_conventions_log_claims.py"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 /projects/PseudoCoupHQ/DevComms/log_217_task_t101b_dominant_types_join.md
rc=$?
echo "check_conventions_log_claims.py exit ${rc}"
exit ${rc}
