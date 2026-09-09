#!/usr/bin/env bash
# g1b_l14_verify_242.sh -- task g1b: the conventions verifier over
# log 242, this closer's own log.
#
# WHAT IT DOES: re-runs every command log 241 pastes and sorts each
# claim into matches / differs / unverifiable / refused / not-rerunnable.
# The obligation the law states is ZERO DIFFERS; a claim that differs is
# fixed in the LOG or in the claim, never in the verifier, which is not
# modified by this task and is not copied.
#
# WHY --timeout 20: the law's own number.  Every command log 241 pastes
# is a `sed`, a `grep`, a one-line `python3 -c` read, the unmodified
# spelling guard, or `handful.py tally3`, and task g1's own run measured
# the last of those inside its 1,852 s end-to-end lane; alone it is a
# read of one 370 kB json.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1B.  The
# verifier runs each command as its own process and holds only the log's
# text; `tally3` is the heaviest thing it starts.
set -euo pipefail
D=PseudoCoupHQ/DevComms
echo "[1/1] task g1b: the conventions verifier over log 242"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    $D/log_242_task_g1b_swift_and_the_widened_lookup.md
