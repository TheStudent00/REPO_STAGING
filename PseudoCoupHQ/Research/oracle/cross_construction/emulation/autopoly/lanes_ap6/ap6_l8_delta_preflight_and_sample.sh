#!/bin/bash
# ap6_l8_delta_preflight_and_sample.sh -- task ap6, lane 8.
#
# WHAT THIS LANE DOES: the plan of the delta pass with the whole of the
# brief's SS2 table in the driver -- the gates gone, one held cell per
# attested setter cell, the primitive lookup carrying holders, the
# narrow-answer re-pose -- and then the first 40 of its runs as THE
# MEMORY SAMPLE, so the pass's own peak is measured before the pass runs.
#
# WHAT CHANGED IN THE PLAN SINCE LANE 5: a pair carrying a setter cell
# no pass ever ran is attempted whole, on the same rule as a pair no
# pass ever ran.  Without it the delta would ask only about keys the
# bank already holds, and every new pair would be invisible to it.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_AP6; lane 7 built every held cell of every attested
# setter cell at 67,588 kB.  CEILINGS: 3,000 ms per gate call, ONE
# re-pose at 30,000 ms -- the loop's two ceilings of record, unchanged.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
total=2

i=1
echo "[$i/$total] THE PLAN of the delta pass"
python3 "$A/autopoly.py" --pass ap6_delta --bank preflight
echo

i=2
echo "[$i/$total] THE MEMORY SAMPLE: the first 40 runs of the delta"
python3 "$A/autopoly.py" --pass ap6_delta --bank run 40
echo
echo "lane done"
