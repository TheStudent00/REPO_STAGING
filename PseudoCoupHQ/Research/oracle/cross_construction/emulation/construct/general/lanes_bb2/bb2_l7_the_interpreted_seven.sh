#!/bin/bash
# bb2_l7_the_interpreted_seven.sh -- task bb2, lane 7: the same
# bit-blast circuit written in each of the seven interpreted languages
# and run beside the definition at points.
#
# THERE IS NO CARVE AND NO GATE on this route, so the outcome is
# `agreed` and never `proved`: the emulation is SOURCE over the
# target's own value model and the check is the fuzz census's method
# over `interp_check.SAMPLE_RULE`'s own sample, edge values first, at
# most 20,000 points.  `interp_check.one_run` is CALLED; the one thing
# swapped is `interp_render.InterpRenderer`, replaced by this task's
# `GateRenderer`, which writes one named local per gate instead of the
# term in the language's own operators.
#
# THE WORK CEILING IS MEASURED, lane 5: `sbb gpr_same 64` is 695 gates
# over 19,683 points -- 13,679,685 gate evaluations -- and ran in 2.4 s
# on cpython, 2.3 s on php and 2.3 s on ruby, so two hundred million
# gate evaluations is about thirty-three seconds and sits inside the
# sixty `interp_check` is handed.  Two cells of the 176 that blast are
# above it and carry their numbers on the row.
#
#   [1/4] the sample rule, LITERAL, before anything runs
#   [2/4] the loop: 253 cells x 7 targets
#   [3/4] every timeout once more, at the longer bound
#   [4/4] the counts, of 253 on every row
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BB2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
STORE="$HQ/Research/oracle/cross_construction/emulation/autopoly/bb2_interp_runs.jsonl"
total=4

i=1
echo "[$i/$total] the sample rule, LITERAL"
python3 -c "
import sys
sys.path.insert(0, '$HQ/Research/oracle/cross_construction/emulation/interp')
sys.path.insert(0, '$HQ/Research/oracle/cross_construction/emulation/handful')
sys.path.insert(0, '$HQ/Research/op_pipeline')
sys.path.insert(0, '$HQ/Research/oracle/cross_construction/emulation')
import interp_check as IC
print(IC.SAMPLE_RULE)
"
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the loop, repeated until an attempt adds no store line"
before=0
if [ -f "$STORE" ]; then before=$(wc -l < "$STORE"); fi
for attempt in 1 2 3 4 5 6 7 8; do
  echo ""
  echo "  ---- attempt $attempt, store lines before: $before ----"
  timeout 5400 python3 "$G/bb2_run.py" interp
  echo "  exit: $?"
  after=0
  if [ -f "$STORE" ]; then after=$(wc -l < "$STORE"); fi
  echo "  store lines after: $after"
  if [ "$after" = "$before" ]; then
    echo "  the attempt added no store line: the loop is done"
    break
  fi
  before=$after
done

i=3
echo ""
echo "[$i/$total] every timeout once more, at the longer bound"
timeout 7200 python3 "$G/bb2_run.py" interp_retry
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] the counts, of 253 on every row"
timeout 900 python3 "$G/bb2_run.py" interp_table
echo "  exit: $?"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
