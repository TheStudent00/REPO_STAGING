#!/bin/bash
# t4_l15_the_constructions_z3_fallback.sh -- task t4, lane 15: z3 asked
# about every construction NO LEAN THEOREM CLOSED, at every (width,
# word) the census names.
#
# THE BRIEF'S OWN ORDER, section 1: "proved ONCE per kind, general in n
# and W, as a Lean lemma in the form t2 used for its eight; where a
# lemma does not close in the task's budget, the instantiation is proved
# by z3 at every width the store uses".  So z3 is the fallback and is
# not asked where a theorem already answered; `store_rest` reads
# `lemmas_t4*.json` and poses the remainder.
#
# THE CEILING IS THE BRIEF'S HARD 30 SECONDS and is never raised.  It is
# a SOFT ceiling in z3 -- checked between propagations and not during
# bit-blasting -- so a wide multiply overshoots it, and what the row
# records is the seconds ACTUALLY TAKEN: lane `t4_l10` step [5/6]
# measured 218.984 s for the multiplier at 128 bits.  The solver's own
# memory is bounded at 4 GB under the task's 6 GB, so a solver that
# grows past it answers `unknown` rather than being stopped by the
# operating system.
#
#   [1/5] part 1 of 4
#   [2/5] part 2 of 4
#   [3/5] part 3 of 4
#   [4/5] part 4 of 4
#   [5/5] the proof table, rebuilt with every row now on disk
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=5

i=1
echo "[$i/$total] part 1 of 4"
timeout 4800 python3 "$G/check_constructions.py" store_rest 1 4
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] part 2 of 4"
timeout 4800 python3 "$G/check_constructions.py" store_rest 2 4
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] part 3 of 4"
timeout 4800 python3 "$G/check_constructions.py" store_rest 3 4
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] part 4 of 4"
timeout 4800 python3 "$G/check_constructions.py" store_rest 4 4
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] the proof table, rebuilt"
timeout 900 python3 "$G/collect_proofs.py" build
echo "  exit: $?"

echo ""
echo "peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
