#!/bin/bash
# bank1_l6_the_delta_pass.sh -- task bank1, lane 6.
#
# WHAT THIS LANE DOES: the delta pass, whole -- every (cell, target,
# written place) the bank holds no certificate of kind `proved` or
# `agreed` for, on the five compiled targets, plus the 5% audit sample
# re-derived from the term.  707 runs of the 1,265 a full pass over
# these five targets would run.  Lane 5's 20 are on the store already
# and are skipped, not re-run.
#
# AN ALARM STOPS THE PASS, which is the brief's own rule: a re-derived
# verdict that differs from its certificate on IDENTICAL inputs means
# the machinery and the record disagree about the same artifact.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_BANK1; lane 5's twenty peaked at 255,548 kB (4% of the
# bound).  CEILINGS: 3,000 ms per gate call, ONE re-pose at 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=1

i=1
echo "[$i/$total] THE DELTA PASS, whole"
python3 "$A/autopoly.py" --bank run
echo
echo "lane done"
