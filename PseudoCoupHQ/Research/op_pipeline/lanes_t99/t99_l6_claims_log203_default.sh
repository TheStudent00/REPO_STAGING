#!/usr/bin/env bash
# t99 lane 6 -- item B proof (a2).  --verify log_203, run on the
# DEFAULT instance (this lane is submitted with no --instance flag),
# where /logs IS Airlock/agent/logs -- the folder the
# t98_l* logs log_203 cites actually live in.  Expected: the same
# 14/14 score task 98 measured, unchanged, since every path IS
# reachable here.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_203, run on DEFAULT instance ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /out/t99_l6_claims_log203_default.json \
  PseudoCoupHQ/DevComms/log_203_task98_stats_explained_and_computed.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
