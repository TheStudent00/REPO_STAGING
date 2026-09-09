#!/usr/bin/env bash
# t97 lane 8 -- every number log_202 states, printed off the artifacts
# themselves by `report97_numbers.py`, one section per command.  The
# log pastes these blocks verbatim, so
# `check_conventions_log_claims.py --verify` has a command to re-run
# for every figure.
set -u
cd PseudoCoupHQ/Research/op_pipeline
for section in walk flags pass2 control states pool census; do
  echo "======== report97_numbers.py $section ========"
  python3 report97_numbers.py "$section"
  echo "-- exit $?"
  echo
done
