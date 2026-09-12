#!/bin/bash
# rd1 lane 9 -- the verifier once more, to check the claim section 9.4 makes
# about itself: that replacing the tally's numbers with the tally's own adds
# no claim and removes none.
set -u
P=PseudoCoupHQ
echo "[1/1] check_conventions_log_claims.py --verify over the settled log 268"
timeout 3000 python3 "$P/Research/op_pipeline/check_conventions_log_claims.py" \
  --verify --timeout 20 \
  "$P/DevComms/log_268_rd1_the_guard_dominates_the_operation.md"
echo "  exit: $?"
