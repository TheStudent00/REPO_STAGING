#!/usr/bin/env bash
# ap5_l27_verify_the_log_b.sh -- task ap5: the law's final lane.  Task 90's
# conventions verifier re-runs every command log 249 pasted and says which
# of its claims reproduce.  The obligation the law states is the DIFFERS
# column: zero, with the log fixed rather than the verifier.
#
# THE SECOND PASS.  Lane `ap5_l25` ran this on the log's first draft:
# DIFFERS 0 already, but one claim REFUSED (`awk 'NF>5'`, read as a
# redirection into a file named `5`) and two NOT_RERUNNABLE (`cd` is
# not a program in the image; a paste carrying `->`).  Each was a
# defect in the COMMAND, not in the claim, so each was rewritten and
# re-run by lane `ap5_l26` and the log took that output.  A lane name
# is used ONCE, so this is a new name and `ap5_l25` stays on the
# record with its tally.
#
# MEMORY BOUND: 6 GB resident; the verifier runs one short-lived process
# per claim at a 20 s ceiling and holds only the log in memory.
set -euo pipefail
cd PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 \
  PseudoCoupHQ/DevComms/log_249_task_ap5_autopoly_fifth_pass.md
echo "done"
