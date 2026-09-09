#!/usr/bin/env bash
# t104 lane 2 -- WHERE the differing texts live.
#
# Lane 1 measured that `term.py` as it stands prints ONE text for the
# pair log_224 section 4 shows printing two.  Three artifacts carry a
# layer-5 text for the same unit, written on three different days:
# `the_pool5.json` (2026-09-03 13:54), `term65_store/` (round 13/14,
# canon39) and `term66_store/` (canon40, finished by task 97).  This
# lane puts all three beside what the code prints today, for the six
# units log_224 names, so the report can say which artifact the gap is
# a property of.
#
# Reads only; writes t104_premise.json under the artifact folder.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/1] the three artifacts against the code"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_premise.py
echo "exit $?"
