#!/usr/bin/env bash
# ap5_l23_the_logs_claims.sh -- task ap5: run, verbatim, exactly the
# commands log 249 will paste as shell transcripts, so what the log
# carries is the output of the command beside it and not a hand-copied
# excerpt.  Every command here is a READ; none writes.
#
# MEMORY BOUND: 6 GB resident; each command is one short-lived python
# process reading `autopoly5.json`, whose own collector reported
# 114,992 kB as its largest.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
run() {
  echo "@@@CMD $*"
  bash -c "$*"
  echo "@@@END"
}
run "python3 $A/autopoly5.py tables"
run "python3 $A/autopoly5.py causes"
run "python3 $A/autopoly5.py change | sed -n '1,30p'"
run "python3 $A/autopoly5.py immediate | sed -n '1,10p'"
run "python3 $A/autopoly5.py x87 | sed -n '1,2p'"
run "python3 $A/autopoly5.py x87 | awk -F'|' 'NF>5 {gsub(/ /,\"\",\$3); gsub(/ /,\"\",\$6); print \$3, \$6}' | sort | uniq -c"
run "python3 $A/autopoly5.py repose | sed -n '1,6p'"
run "python3 $A/autopoly5.py sat | grep -v counterexample | sed -n '1,12p'"
run "wc -l $A/autopoly5_runs.jsonl"
run "python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $A/autopoly5.json"
run "python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $A/autopoly5_cells.json"
run "python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py $A/autopoly5_check_L2_rerun.json"
run "grep -c exempt $A/autopoly5.py"
run "cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful && python3 o8_regression.py totals"
echo "done"
