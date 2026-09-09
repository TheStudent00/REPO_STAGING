#!/usr/bin/env bash
# ap1_l16_verify_243c.sh -- task ap1: the conventions verifier over this
# task's DevComms log, third pass. The second pass returned one DIFFERS: the
# preflight transcript ended with the program's own `peak resident`
# line, a real measurement that moves by a few kB between runs. It was
# fixed in the CLAIM and never in the verifier: the pasted command now
# carries `| grep -v 'peak resident'` on the line itself, so what is
# printed is what ran, and the memory figures are in section 12 where
# they belong.
#
# The obligation the law states is the DIFFERS column: zero, and a log
# fixed rather than a verifier.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP1.
set -euo pipefail
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_243_task_ap1_autopoly_first_full_loop.md
