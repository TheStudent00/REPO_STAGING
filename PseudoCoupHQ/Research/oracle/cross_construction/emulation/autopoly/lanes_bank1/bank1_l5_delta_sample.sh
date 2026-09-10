#!/bin/bash
# bank1_l5_delta_sample.sh -- task bank1, lane 5.
#
# WHAT THIS LANE DOES: the first 20 runs of the delta pass, which is
# the memory sample the law asks for before a long lane, and the first
# proof that the reshaped loop renders, compiles, carves and gates on
# all five compiled targets through the bank-mode driver.
#
# MEMORY: bound 6 GB resident on the one collecting process, no forked
# workers, checked after EVERY run, named abort ABORT_MEMORY_BANK1.
# CEILINGS: the gate of record at 3,000 ms per place and ONE re-pose at
# 30,000 ms for an UNDECIDED -- task ap1's two ceilings, unchanged.
#
# The store is incremental: one json line per finished run, flushed and
# fsynced before the next run begins, so this lane's 20 runs are not
# re-run by lane 6.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=1

i=1
echo "[$i/$total] the delta pass, first 20 runs"
python3 "$A/autopoly.py" --bank run 20
echo
echo "lane done"
