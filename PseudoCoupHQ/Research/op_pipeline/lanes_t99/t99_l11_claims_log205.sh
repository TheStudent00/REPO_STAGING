#!/usr/bin/env bash
# t99 lane 11 -- final verifier pass over log_205, after the git-show
# fix (lane 10 found `cd` tool_absent; this uses `git -C` instead).
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_205 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /out/t99_l11_claims_log205.json \
  PseudoCoupHQ/DevComms/log_205_task_99_recording_gaps.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
