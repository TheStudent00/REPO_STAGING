#!/usr/bin/env bash
# t97 lane 4 -- PASS 2, by the owner's rule of 2026-09-04: everything pass 1
# FLAGGED, re-run with a stated LARGER time and memory budget, to see
# whether it changes the result.
#
# THE POPULATION: the 228 units pass 1 flagged, of the 28,192 canon40
# proves in the 322 inputs it walked.  Every one of the 228 was flagged
# for the same measured reason -- `MemoryError` written into
# `layer5_refusal`, the normalizer, with the term itself already
# TERM / PROVED_ON_SHIP.
#
# THE BUDGET, larger on both axes and stated:
#   per-unit address-space ceiling 4096 MB   (pass 1 gave 1536 MB)
#   per-unit wall clock            1800 s    (pass 1 gave 120 s)
#   The largest per-unit need actually MEASURED is 1,993,856 kB, for
#   c/regen_1869 at a 3072 MB ceiling, and that unit's peak was
#   1,993,756 kB at 6144 MB -- the same number -- so 4096 MB is above
#   a measured need and not a guess (lane t97_l2_flag_reason.sh).
#   Four slices x 4096 MB = 16,384 MB inside the instance's 20 GB.
#   THE SLICE IS CUT BY SHARD so every store shard has one writer.
#   NAMED ABORT: ABORT_MEMORY_T97 if a slice's parent passes 6 GB.
set -u
cd PseudoCoupHQ/Research/op_pipeline
for i in 0 1 2 3; do
  python3 term97_walk.py pass2 4096 1800 a "$i" 4 pass1 \
    > "/work/t97_pass2_a_slice$i.log" 2>&1 &
done
wait
for i in 0 1 2 3; do
  echo "======== slice $i ========"
  tail -12 "/work/t97_pass2_a_slice$i.log"
done
echo
echo "======== the four slice logs, joined ========"
cat /work/t97_pass2_a_slice*.log
