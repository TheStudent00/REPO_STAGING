#!/bin/bash
# t4_l14_the_lemmas_with_the_unfolded_ceiling.sh -- task t4, lane 14: the
# lemmas again, with the fallback form's ceiling read off the size that
# decides it.
#
# LANE 13's FINDING, which located it: `lean` under `ulimit -v` on the
# very theorem that stopped lane 12 -- the multiplier at 16 bits --
# answers cleanly, "The SAT solver timed out while solving the problem".
# So the `lean` process was never what grew.  What grew was THIS task's
# own process, building the FALLBACK form: a theorem whose `let` form
# Lean refuses is then offered WRITTEN OUT, and the ceiling on that was
# read off the DISTINCT node count (190 for this multiplier) instead of
# the written-out one, which is the one number the whole of task t2's
# `construct/lean/OWED.md` section 3 is about.  The ceiling is now
# `build.unfolded_size`, which counts a step read three times three
# times.
#
#   [1/4] the two sizes side by side, so the difference is a measurement
#         and not an assertion
#   [2/4] the theorems, part 1 of 2
#   [3/4] the theorems, part 2 of 2
#   [4/4] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4; one `lean`
# process bounded at 4 GB of address space by the shell that starts it.
#
# Node: hq.research.compiler_graph.gate.lean and
#       hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=4

i=1
echo "[$i/$total] the two sizes of the multiplier, side by side"
timeout 600 python3 "$G/sizes_probe.py"
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the theorems, part 1 of 2"
timeout 9000 python3 "$G/run_lemmas_t4.py" prove 90 1 2
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the theorems, part 2 of 2"
timeout 9000 python3 "$G/run_lemmas_t4.py" prove 90 2 2
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
