#!/bin/bash
# rd1 lane 8 -- the verifier again, over log 268 as it FINALLY stands (lane
# rd1_l7 read it before section 9.4 carried its own tally). The lane name is
# new because a lane name is used once.
set -u
P=PseudoCoupHQ
echo "[1/1] check_conventions_log_claims.py --verify over the final log 268"
timeout 3000 python3 "$P/Research/op_pipeline/check_conventions_log_claims.py" \
  --verify --timeout 20 \
  "$P/DevComms/log_268_rd1_the_guard_dominates_the_operation.md"
echo "  exit: $?"
