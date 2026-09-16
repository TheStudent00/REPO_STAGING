#!/bin/bash
# rv9 lane 10 -- the conventions verifier over this task's log, from this
# task's own instance, as the law requires. The tally it prints is pasted
# into the log's section 7.5.
set -u
P=PseudoCoupHQ
OP=$P/Research/op_pipeline
LOG=$P/DevComms/log_273_rv9_the_arch_opcode_axis_the_multiply_high_cause_named.md
export HOME=/work
total=2
i=1

echo "[$i/$total] the log this lane reads, by sha256"; i=$((i+1))
sha256sum "$LOG" "$OP/check_conventions_log_claims.py"

echo "[$i/$total] the verifier"
timeout 1800 python3 "$OP/check_conventions_log_claims.py" --verify \
  --timeout 20 "$LOG"
echo "  exit: $?"
echo "lane rv9_l10 done"
