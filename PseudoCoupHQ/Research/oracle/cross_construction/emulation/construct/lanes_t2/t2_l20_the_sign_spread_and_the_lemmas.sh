#!/bin/bash
# t2_l20_the_sign_spread_and_the_lemmas.sh -- task t2, lane 20: the sign
# spread written as the two shifts it is, the schemas re-verified, and
# the lemmas re-run.
#
# WHY.  Lane 19 left every remaining lemma refused BEFORE Lean with one
# cause, WIDTH_UNRESOLVED, and every one of them passes through
# `schemas.sign_word_of`, which spread the sign bit with a CONDITIONAL
# between two constants.  The translator's width unification cannot pin
# a numeral whose width only a sibling fixes.  The sign bit lifted to the
# top of the word and shifted down arithmetically is the same value in
# two operations and no constants, so the schema is written that way --
# which is smaller as well, and the renderer writes a term out once per
# read.
#
# THE PLAN'S SOURCE ALSO MOVED, and it was a defect: the shapes to prove
# were read off the BANK's width-or-kind refusals, and the bank is where
# this pass's own proofs LAND -- so once a place was proved the shape
# that carried it disappeared from the plan.  The plan now reads the
# pass's own run store as well.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.compiler_graph.gate.lean
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=4

i=1
echo "[$i/$total] THE SHAPES THE POPULATION AND THE PASS NEED"
python3 "$C/lean/run_lemmas_t2.py" instances
echo

i=2
echo "[$i/$total] THE SCHEMAS AT THE NARROW WIDTHS, whole"
python3 "$C/check_schemas.py" narrow
echo

i=3
echo "[$i/$total] THE SCHEMAS AT THE WIDTHS THIS PIPELINE MEETS"
python3 "$C/check_schemas.py" wide
echo

i=4
echo "[$i/$total] THE LEMMAS, per shape and per limb"
python3 "$C/lean/run_lemmas_t2.py" prove 120
echo
echo "lane done"
