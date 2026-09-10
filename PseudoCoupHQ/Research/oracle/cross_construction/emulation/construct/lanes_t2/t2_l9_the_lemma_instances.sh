#!/bin/bash
# t2_l9_the_lemma_instances.sh -- task t2, lane 9: which (schema, width,
# word) instances the refused population actually needs a lemma for,
# read off the bank and the outer set, and nothing proved yet.
#
# The lemmas this task proves are the lemmas the population needs, and
# this lane is how that list is arrived at rather than chosen.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=1

i=1
echo "[$i/$total] THE INSTANCES THE REFUSED POPULATION NEEDS"
python3 "$C/lean/run_lemmas_t2.py" instances
echo
echo "lane done"
