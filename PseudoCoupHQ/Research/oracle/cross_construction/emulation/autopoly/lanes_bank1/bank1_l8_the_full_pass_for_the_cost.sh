#!/bin/bash
# bank1_l8_the_full_pass_for_the_cost.sh -- task bank1, lane 8.
#
# WHAT THIS LANE DOES: the WHOLE re-derivation over the same five
# compiled targets -- 1,265 runs, every cell on every target, the shape
# passes ap1 to ap5 ran -- so the delta pass's cost has a MEASURED
# figure to stand against rather than an inferred one.  Same image,
# same instance, same hour, same ceilings: the only difference between
# the two numbers is which runs were attempted.
#
# It writes its own store (`bank1_full_runs.jsonl`) and its own source
# folder (`src_bank1_full`); the delta pass's store is not touched.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_BANK1; the delta pass peaked at 996,780 kB.
# CEILINGS: 3,000 ms per gate call, ONE re-pose at 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=1

i=1
echo "[$i/$total] THE FULL PASS over the five compiled targets"
python3 "$A/autopoly.py" --full run
echo
echo "lane done"
