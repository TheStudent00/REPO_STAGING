#!/usr/bin/env bash
# rv2 lane 22 -- the verifier over this task's own log: every claim's
# reproducing command re-run inside this instance, sorted into matches /
# differs / unverifiable. Zero DIFFERS is the bar; a claim that differs is
# fixed in the log or in the claim, never in the verifier.
set -u
OP=PseudoCoupHQ/Research/op_pipeline
LOG=PseudoCoupHQ/DevComms/log_259_rv2_the_transfer_of_a_proved_polyfill_library_to_riscv64.md
export HOME=/work
total=1

echo "[1/$total] the verifier"
python3 $OP/check_conventions_log_claims.py --verify --timeout 20 $LOG
echo "verifier rc=$?"
echo "--- lane finished"
