#!/bin/bash
# t4_l10_the_canonical_ceiling_and_the_lemma_smoke.sh -- task t4, lane 10:
# the three things lane 9 measured, acted on and checked.
#
# LANE 9's FINDING, and it is what this lane rests on: the render and the
# compile of a construction are cheap and fast -- `div gpr_one 64` on c
# under `all_constructed` renders 19,592 statements in 2.1 s at 88 MB
# resident and compiles and carves 20,109 instructions in 6.1 s at 90 MB
# -- and it is the GATE that runs out.  So the tier now states two
# ceilings, each with the measurement on it: the canonical form is
# offered only where the term WRITTEN OUT is under task t2's own 200,000
# nodes, and the gate is offered only where the carved body is under
# 4,000 instructions.  A place above either carries the count and the
# cause and is a row, not an ABORT.
#
#   [1/6] `adc gpr_gpr 64` on go -- the whole tier, which lanes 6, 7, 8
#         and 9 all lost to the canonical form's printed size
#   [2/6] `mul gpr_one 64` on go -- the same, above the gate's ceiling
#   [3/6] the lemma plan: which (kind, width, word) the census asks for
#   [4/6] the lemma smoke: three of them through `lean`, so the `let`
#         form is known to elaborate before a long lane is spent on it
#   [5/6] one slice of the constructions put to z3, for the timings
#   [6/6] the proof table built from whatever is on disk
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=6

i=1
echo "[$i/$total] adc gpr_gpr 64 -> go, the whole tier"
timeout 900 python3 "$G/general.py" tier adc gpr_gpr 64 go
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] mul gpr_one 64 -> go, the whole tier"
timeout 900 python3 "$G/general.py" tier mul gpr_one 64 go
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the lemma plan"
timeout 600 python3 "$G/run_lemmas_t4.py" plan
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] the lemma smoke: three instances through lean"
timeout 1800 python3 "$G/run_lemmas_t4.py" prove 180 1 49
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] one slice of the constructions put to z3"
timeout 2400 python3 "$G/check_constructions.py" store 1 24
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] the proof table built from whatever is on disk"
timeout 600 python3 "$G/collect_proofs.py" build
echo "  exit: $?"

echo ""
echo "peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
