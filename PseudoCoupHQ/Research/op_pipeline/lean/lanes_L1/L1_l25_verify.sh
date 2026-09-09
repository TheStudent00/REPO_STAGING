#!/bin/bash
# L1 lane 25 — the conventions checker re-runs this log's claims inside the
# sandbox and sorts each into matches / differs / unverifiable. The checker is
# unmodified; a DIFFERS is fixed in the log or in the claim, never here.
set -u
echo '[1/1] check_conventions_log_claims.py over log_227'
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  /projects/PseudoCoupHQ/DevComms/log_227_task_L1_lean_second_discharger.md
echo "check_conventions_log_claims.py exit $?"
