#!/usr/bin/env bash
# t101b lane 9 -- third (final) verifier pass, after fixing the two
# absolute-host-path python3 -c commands (container mounts the repo
# at PseudoCoupHQ, not PseudoCoupHQ)
# and the "> 0" substring inside one snippet that the checker's
# redirect-detector misread as a shell `>` into a file named "0:".
set -u
echo "[1/1] check_conventions_log_claims.py"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_217_task_t101b_dominant_types_join.md
rc=$?
echo "check_conventions_log_claims.py exit ${rc}"
exit ${rc}
