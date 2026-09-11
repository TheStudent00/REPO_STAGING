#!/bin/bash
# t4_l12_the_lemmas_per_kind_bounded.sh -- task t4, lane 12: ONE LEAN THEOREM
# PER OPERATION KIND, instantiated at every (width, word) the census
# names, with the statement written as one `let` per node.
#
# WHAT THIS SETTLES, and it is task t2's own owed item (construct/lean/
# OWED.md section 3): "a theorem's statement is the term WRITTEN OUT, a
# printed term names no intermediate, and restoring division reads its
# own previous remainder three times per step -- so the statement grows
# like 3^width", and what was owed was "a way to STATE it -- a
# translation to Lean that names intermediates (`let`)".  Lane 10 step
# [4/6] shows the translation working: the barrel shifter at 128 bits
# over a word of 128, 102 bindings, closed by `bv_decide` in 3.301 s.
#
# THE BUDGET is 90 seconds per theorem and is this task's own; a theorem
# that does not close inside it is TIMED_OUT, which is a row, and the
# instance then goes to z3 in the lane after this one.
#
# LANE 11 IS THIS LANE'S OWN MEASUREMENT, and why this one exists: the
# eleven theorems of add, subtract and negate closed at every width in
# under 1.6 s each, and `bv_decide` on the multiplier at 16 bits then
# grew until the operating system stopped the whole lane -- `Killed`,
# exit 137 -- and took the eleven with it, because the rows were written
# once at the end.  Two things are different here and nothing else is:
# one `lean` process is bounded at 4 GB of address space, so a tactic
# that grows past it fails to allocate and returns a row; and the rows
# are written after EVERY theorem.
#
#   [1/3] the theorems, part 1 of 2
#   [2/3] the theorems, part 2 of 2
#   [3/3] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4; one `lean`
# process per theorem, its own peak read from os.wait4.
#
# Node: hq.research.compiler_graph.gate.lean and
#       hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=3

i=1
echo "[$i/$total] the theorems, part 1 of 2"
timeout 9000 python3 "$G/run_lemmas_t4.py" prove 90 1 2
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the theorems, part 2 of 2"
timeout 9000 python3 "$G/run_lemmas_t4.py" prove 90 2 2
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
