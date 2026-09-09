#!/usr/bin/env bash
# t97 lane 6 -- THE RESIDUE of pass 2: every unit that pass 2's 4096 MB
# leg still could not finish, given MORE room and MORE time again, one
# slice at a time so the whole instance is behind a single sub-process.
#
# THE BUDGET, larger again on both axes and stated:
#   per-unit address-space ceiling 18432 MB  (leg a gave 4096 MB,
#                                             pass 1 gave 1536 MB)
#   per-unit wall clock            3600 s    (leg a gave 1800 s,
#                                             pass 1 gave 120 s)
#   One slice, so 18,432 MB is the only ceiling the instance's 20 GB
#   has to hold at once.
#   NAMED ABORT: ABORT_MEMORY_T97 if the parent passes 6 GB.
set -u
cd PseudoCoupHQ/Research/op_pipeline
python3 term97_walk.py pass2 18432 3600 b 0 1 "term97_pass2_a_slice*.json"
echo "exit $?"
