#!/usr/bin/env bash
# ap3_l19_verify_245c.sh -- task ap3, the CLOSING pass: the same verifier over the log with its own section 17 in place, so the tally the log states is the tally of the log as it stands.
# task's log, run from this task's own instance as the law requires.
# Zero DIFFERS is the obligation; a DIFFERS is fixed in the LOG or in
# the CLAIM and never in the verifier.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_245_task_ap3_autopoly_third_pass.md
echo "done"
