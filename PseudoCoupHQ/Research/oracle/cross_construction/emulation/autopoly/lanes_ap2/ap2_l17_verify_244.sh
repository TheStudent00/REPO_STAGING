#!/usr/bin/env bash
# ap2_l17_verify_244.sh -- task ap2: the conventions verifier over
# log 244, the standing rule's own closing lane.
#
#   check_conventions_log_claims.py --verify --timeout 20 <log>
#
# The obligation the standing rules state is the DIFFERS column: zero.
# A claim that carries a command is re-run and its output compared; a
# claim that carries an attribution to a lane log, or is prose, is
# UNVERIFIABLE by nature and is counted as such.  The log or the claim
# is fixed, never the verifier.
set -euo pipefail
cd PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_244_task_ap2_autopoly_second_pass.md
