#!/usr/bin/env bash
# h2_l10_verify2.sh -- task h2: the conventions verifier over this
# task's own log AGAIN, after every transcript in it was replaced with
# lane h2_l9_evidence.sh's own blocks, each carrying the command that
# produced it.
#
# WHY A SECOND PASS: lane h2_l8's first pass found 0 DIFFERS and 0
# REFUSED but also 0 MATCHES, because the transcripts were pasted with
# an attribution and no command, so nothing could be re-run. The fix is
# in the LOG, never in the verifier, which is not modified here or
# anywhere.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2; the verifier
# prints its own peak RSS.
set -euo pipefail
echo "[1/2] task h2: the conventions verifier over log 240"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_240_task_h2_two_printing_fixes.md
echo "[2/2] done"
