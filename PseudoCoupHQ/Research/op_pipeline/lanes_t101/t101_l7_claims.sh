#!/usr/bin/env bash
# t101 lane 7 -- the final lane: re-run every command log 213 pasted and
# sort each claim into matches / differs / unverifiable, from this task's
# own instance. The verifier is never modified.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_213 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 20 \
  --json /out/t101_l7_claims_log213.json \
  /projects/PseudoCoupHQ/DevComms/log_213_task_t101_dominant_types_dwarf_flag.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
