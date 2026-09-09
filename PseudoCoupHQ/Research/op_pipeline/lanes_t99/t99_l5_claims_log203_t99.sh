#!/usr/bin/env bash
# t99 lane 5 -- item B proof (a1).  --verify log_203 FROM THE t99
# INSTANCE.  t99's own /logs holds only t99's lanes (confirmed by the
# coordinator: <runs>/t99/agent/logs is t99's own
# mount, not Airlock/agent/logs where the t98_l* lanes
# log_203 cites actually live), so every claim that cats a
# /logs/*t98* path is expected to hit the new REFUSED log_unreachable
# path here, not DIFFERS.  Claims with no such path keep whatever
# outcome they already had.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_203, run FROM t99 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /out/t99_l5_claims_log203_t99.json \
  PseudoCoupHQ/DevComms/log_203_task98_stats_explained_and_computed.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
