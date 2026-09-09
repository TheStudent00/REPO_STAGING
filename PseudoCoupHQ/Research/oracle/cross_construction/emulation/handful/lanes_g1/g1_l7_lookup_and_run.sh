#!/usr/bin/env bash
# g1_l7_lookup_and_run.sh -- task g1: the primitive lookup again, now
# recording what task o2's WIDE chaff rule would have found where the
# narrow rule found nothing, and then the FORTY RUNS.
#
# WHY THE LOOKUP IS RE-RUN: lane g1_l6 measured that only 8 of the 40
# (cell, target) pairs have a single-opcode row under task o2's NARROW
# chaff rule, which is the rule the brief names.  The reason a cell has
# none is itself a fact worth measuring rather than guessing, and the
# two rules differ by exactly one thing -- the wide rule counts a
# width-changing move or a sign extension as chaff too -- so where the
# narrow lookup finds nothing the record now says whether the wide one
# would have.  It is EVIDENCE ABOUT THE CELL and not a second route:
# the route still reads the narrow rows.
#
# THEN THE FORTY RUNS, in the same lane, so `handful3.json` is written
# end to end by one version of the program (task h1's own section 7.1
# lesson).  Each run is one lookup, one render, one compile at that
# corpus's own ship flags, one carve, and one gate call per written
# place.  The swift runs will reach the compile step and be refused
# there by the machine's own answer, which is the deliverable's swift
# column.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1, checked
# after every run.  Lane g1_l6 measured the lookup at 81,492 kB; task
# h2's own twenty runs peaked at 448,016 kB.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/3] task g1: handful.py primitive3"
python3 $H/handful/handful.py primitive3
echo "[2/3] task g1: handful.py run3"
python3 $H/handful/handful.py run3
echo "[3/3] done"
