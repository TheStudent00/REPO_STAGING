#!/usr/bin/env bash
# ap5_l25_verify_the_log.sh -- task ap5: the law's final lane.  Task 90's
# conventions verifier re-runs every command log 249 pasted and says which
# of its claims reproduce.  The obligation the law states is the DIFFERS
# column: zero, with the log fixed rather than the verifier.
#
# MEMORY BOUND: 6 GB resident; the verifier runs one short-lived process
# per claim at a 20 s ceiling and holds only the log in memory.
set -euo pipefail
cd PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_249_task_ap5_autopoly_fifth_pass.md
echo "done"
