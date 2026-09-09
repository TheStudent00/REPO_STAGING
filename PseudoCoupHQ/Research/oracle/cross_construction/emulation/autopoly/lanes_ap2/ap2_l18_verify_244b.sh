#!/usr/bin/env bash
# ap2_l18_verify_244b.sh -- task ap2: the conventions verifier over log 244, second pass, after the three DIFFERS of the first pass were fixed IN THE CLAIMS: three transcripts had been pasted with lines elided, so each now carries on its own command line the filter that produces exactly what is pasted, or is pasted in full.
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
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_244_task_ap2_autopoly_second_pass.md
