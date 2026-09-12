#!/bin/bash
# bb2_l5_the_swift_cost_curve_and_the_interpreted_rate.sh -- task bb2,
# lane 5: two rates, measured, because two of this task's own bounds
# have to be read off a run and not chosen.
#
# WHAT LANE 4 MEASURED AND WHY THIS LANE EXISTS.  At 74,674 source
# lines, clang takes 35 s, rustc 38 s and go 8 s; swiftc did not come
# back at all and its own 600-second bound fired
# (`subprocess.TimeoutExpired`, LITERAL in lane 4).  The pass runs 618
# blastable places on five targets, so what matters is not that the
# largest source is out of swift's reach but WHERE swift's knee is.
#
#   [1/3] the swift compile at three circuit sizes, c beside it
#   [2/3] one interpreted gate run on each of the seven, timed, at a
#         known gate-evaluation count -- the rate this task's own
#         interpreted work ceiling is read off
#   [3/3] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
total=3

i=1
echo "[$i/$total] the swift compile at three circuit sizes, c beside it"
echo "  -- xor gpr_gpr 8: 24 gates on the destination place"
timeout 1800 python3 "$G/bb2_run.py" cell xor gpr_gpr 8 c swift
echo "  exit: $?"
echo "  -- add gpr_gpr 32: 461 gates on the destination place"
timeout 1800 python3 "$G/bb2_run.py" cell add gpr_gpr 32 c swift
echo "  exit: $?"
echo "  -- sbb gpr_gpr 64: 2,638 gates on the destination place"
timeout 2400 python3 "$G/bb2_run.py" cell sbb gpr_gpr 64 c swift
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] one interpreted gate run on each of the seven, timed"
for L in cpython php ruby java javascript dart csharp; do
  echo "  -- add gpr_gpr 64 on $L"
  timeout 1200 python3 "$G/bb2_run.py" interp_one add gpr_gpr 64 "$L"
  echo "  exit: $?"
done
echo "  -- sbb gpr_same 64 (695 gates x 19683 points) on the three slowest"
for L in cpython php ruby; do
  echo "  -- sbb gpr_same 64 on $L, the ceiling raised for this one run"
  timeout 1800 python3 "$G/bb2_run.py" interp_one sbb gpr_same 64 "$L" 20000000
  echo "  exit: $?"
done

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
