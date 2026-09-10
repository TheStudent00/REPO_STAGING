#!/bin/bash
# bank1_l2_build_the_bank.sh -- task bank1, lane 2.
#
# WHAT THIS LANE DOES: banks every run of every pass on disk into
# certificates.jsonl, then prints the four readings of it the brief
# asks for -- the counts per kind, THE THREE READINGS (strict,
# destination-only, corpus-needed), the pairs proved by some pass and
# not by the last, and whether any store this task did not bank holds a
# proof the bank lacks.
#
# NOTHING IS RUN HERE: no render, no compile, no carve, no gate.  This
# lane reads stores other tasks wrote.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BANK1, checked
# after every store; lane 1's sample peaked at 31,000 kB.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bank1_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=5

i=1
echo "[$i/$total] BUILD: every run of every pass -> certificates.jsonl"
python3 "$A/bank.py" build
echo

i=2
echo "[$i/$total] the certificates banked per kind"
python3 "$A/bank.py" kinds
echo

i=3
echo "[$i/$total] THE THREE READINGS"
python3 "$A/bank.py" readings
echo

i=4
echo "[$i/$total] the pairs proved by some pass and not by the last"
python3 "$A/bank.py" restored
echo

i=5
echo "[$i/$total] the stores this task did not bank, audited"
python3 "$A/bank.py" backups
echo
echo "lane done"
