#!/usr/bin/env bash
# t97 lane 3 -- PASS 1 of the two-pass walk, at the ORDINARY budget.
# 322 canon40 inputs remain; they are cut into six slices that run side
# by side inside this one lane, each its own pristine parent forking one
# sub-process per unit.
#
# THE BUDGET, and why these numbers:
#   per-unit address-space ceiling 1536 MB.  probe97b measured the
#   record for c/regen_1859 IDENTICAL at 1536, 3072 and 6144 MB, so this
#   ceiling is a bound and not a change to the answer.
#   per-unit wall clock 120 s.  The sample's slowest unit was 3.09 s.
#   six slices x 1536 MB = 9,216 MB of sub-process ceiling, plus six
#   parents measured at ~62 MB each, inside the instance's 16 GB.
#   NAMED ABORT: ABORT_MEMORY_T97 if a parent's own peak passes 6 GB.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
for i in 0 1 2 3 4 5; do
  python3 term97_walk.py pass1 1536 120 "$i" 6 > "/work/t97_pass1_slice$i.log" 2>&1 &
done
wait
for i in 0 1 2 3 4 5; do
  echo "======== slice $i ========"
  tail -4 "/work/t97_pass1_slice$i.log"
done
echo
echo "======== the six slice logs, joined ========"
cat /work/t97_pass1_slice*.log
