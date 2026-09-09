#!/usr/bin/env bash
# t99 lane 9 -- final lane.  --verify log_205 (this task's own report)
# from t99, per brief section 1.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_205 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /out/t99_l9_claims_log205.json \
  PseudoCoupHQ/DevComms/log_205_task_99_recording_gaps.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
