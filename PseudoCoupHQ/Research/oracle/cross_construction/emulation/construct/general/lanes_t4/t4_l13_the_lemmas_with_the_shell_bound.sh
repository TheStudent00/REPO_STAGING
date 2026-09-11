#!/bin/bash
# t4_l13_the_lemmas_with_the_shell_bound.sh -- task t4, lane 13: the
# lemmas again, with the `lean` process bounded by the SHELL that starts
# it, and the bound checked on its own first.
#
# LANE 12's FINDING: ten theorems closed (add, subtract and negate at
# every width the census names, 0.46 s to 1.52 s each, the widest of
# them 129 `let` bindings) and the eleventh -- the multiplier at 16 bits
# -- grew until the operating system stopped the whole lane with no
# language-level error, exit 137, THROUGH a `resource.setrlimit` set in
# `preexec_fn`.  So the bound either did not reach the process or did
# not reach what grew.  Step [1/4] answers that question on its own file
# before any long run is spent on it.
#
#   [1/4] the bound, checked: `ulimit -v` then `lean` on the multiplier
#         at 16 bits, which is the theorem lane 12 was stopped at
#   [2/4] the theorems, part 1 of 2
#   [3/4] the theorems, part 2 of 2
#   [4/4] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4; one `lean`
# process bounded at 4 GB of address space by the shell.
#
# Node: hq.research.compiler_graph.gate.lean and
#       hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=4

i=1
echo "[$i/$total] the bound, checked on the theorem lane 12 was stopped at"
cd "$G/lean_t4"
echo "  the file: construction_multiply_w16_u64__bvmul_w16.lean"
wc -l construction_multiply_w16_u64__bvmul_w16.lean
( ulimit -v 4194304; ulimit -a | head -20 )
echo "  --- lean under the bound, at most 180 s ---"
( ulimit -v 4194304; timeout 180 lean construction_multiply_w16_u64__bvmul_w16.lean ) 2>&1 | head -30
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
