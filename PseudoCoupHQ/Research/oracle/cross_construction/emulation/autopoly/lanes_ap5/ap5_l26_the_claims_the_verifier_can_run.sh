#!/usr/bin/env bash
# ap5_l26_the_claims_the_verifier_can_run.sh -- task ap5: three of log
# 249's pasted commands came back from the conventions verifier as
# REFUSED or NOT_RERUNNABLE for a defect in the COMMAND and not in the
# claim, so each is rewritten here and run, and the log takes this
# output:
#   * the x87 tally used `awk 'NF>5'`; the verifier reads that `>5` as
#     a redirection into a file named `5` and refuses to run it.  Same
#     tally through `cut` on the table's own pipes.
#   * the imm_* paste carried `->` inside the table's cells, which the
#     verifier reads as an arrow gloss; the range is cut to the counts
#     the brief asks for, above the first such row.
#   * the o8 totals were pasted as `cd ... && python3 ...` and `cd` is
#     not a program in the image; the same command with the script's
#     own directory given to python instead.
#
# MEMORY BOUND: 6 GB resident; three short-lived readers.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
run() {
  echo "@@@CMD $*"
  bash -c "$*"
  echo "@@@END"
}
run "python3 $A/autopoly5.py x87 | grep '^| ' | cut -d'|' -f3,6 | sort | uniq -c"
run "python3 $A/autopoly5.py immediate | sed -n '1,8p'"
run "python3 $H/o8_regression.py totals"
echo "done"
