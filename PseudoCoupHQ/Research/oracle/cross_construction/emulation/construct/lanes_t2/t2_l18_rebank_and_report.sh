#!/bin/bash
# t2_l18_rebank_and_report.sh -- task t2, lane 18: the bank rebuilt with
# this pass registered in it, the three readings, and `construct.md`.
#
# THE PASS IS REGISTERED FROM OUTSIDE THE BANK'S SOURCE.  `bank.PASSES`
# is data -- one row per pass, with its store, its reader and its
# targets -- and `construct.register_with_the_bank` appends this pass's
# row at run time, exactly as `autopoly.configure` sets the driver's
# paths from outside the driver.  `bank.py` itself is not edited: it is
# a shared file this task's brief does not name.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2; the bank is
# streamed and never held whole.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=4

i=1
echo "[$i/$total] THE BANK, rebuilt with this pass in it"
python3 "$C/construct.py" bank
echo

i=2
echo "[$i/$total] THE THREE READINGS"
python3 "$A/bank.py" readings
echo

i=3
echo "[$i/$total] construct.md"
python3 "$C/construct_report.py"
echo

i=4
echo "[$i/$total] the report, whole"
cat "$C/construct.md"
echo
echo "lane done"
