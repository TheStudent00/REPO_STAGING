#!/usr/bin/env bash
# t101 lane 9 -- the final lane: re-run every command log 213 pastes,
# after §3.2's quotation was narrowed to fold.py's arrow-free lines.
# The verifier is never modified.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_213 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 20 \
  --json /out/t101_l9_claims2_log213.json \
  PseudoCoupHQ/DevComms/log_213_task_t101_dominant_types_dwarf_flag.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
