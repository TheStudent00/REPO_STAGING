#!/usr/bin/env bash
# t99 lane 12 -- final verifier pass over log_205, after fixing the
# git-show command (lane 10: cd tool_absent; lane 11: git -C
# misread as subcommand "PseudoCoupHQ" -- both replaced by
# --git-dir/--work-tree flags here).
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_205 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /out/t99_l12_claims_log205.json \
  PseudoCoupHQ/DevComms/log_205_task_99_recording_gaps.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
