#!/usr/bin/env bash
# rv3 lane 10 -- the law's final lane: re-run every command this task's log
# pasted, from this task's own instance, and print the tally.  The verifier
# is not touched; a DIFFERS is fixed in the log or in the claim.
set -u
OP=PseudoCoupHQ/Research/op_pipeline
LOG=PseudoCoupHQ/DevComms/log_260_rv3_the_lifter_gains_what_clang_writes_and_the_inheritance_re_run.md
total=1

echo "[1/$total] the verifier over this task's log"
python3 "$OP/check_conventions_log_claims.py" --verify --timeout 20 "$LOG"
echo "verify rc=$?"
echo "lane rv3_l10 done"
