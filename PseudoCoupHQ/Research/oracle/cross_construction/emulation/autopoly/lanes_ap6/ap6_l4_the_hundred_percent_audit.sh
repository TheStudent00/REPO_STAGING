#!/bin/bash
# ap6_l4_the_hundred_percent_audit.sh -- task ap6, lane 4.
#
# WHAT THIS LANE DOES: THE AUDIT AT 100%, whole -- every one of the
# 1,227 certified (cell, target, written place, setter) keys of the five
# compiled targets re-derived from the cell's own term, over 962 runs.
# Lane 3b's twenty are on the store already and are skipped, not re-run.
#
# IT IS THE GUARD ON THE REMOVAL OF THE NINE TASK-NAME GATES.  A
# re-derived verdict that differs from its certificate ON IDENTICAL
# INPUTS -- same term text, same source sha256, same compiler and flags
# -- is an ALARM: it means the machinery and the record disagree about
# the same artifact, and the pass STOPS and names the pair.  A differing
# ARTIFACT is not an alarm: the source the driver renders has moved, so
# the record is a NEW certificate beside the old one and never in place
# of it.
#
# `--attempts off`: no uncertified key is attempted, so what this lane
# measures is re-derivation and nothing else.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_AP6; lane 3b's twenty peaked at 258,352 kB (4% of the
# bound).  CEILINGS: 3,000 ms per gate call, ONE re-pose at 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=1

i=1
echo "[$i/$total] THE 100% AUDIT, whole"
python3 "$A/autopoly.py" --pass ap6_audit --audit-share 1 \
    --attempts off --bank run
echo
echo "lane done"
