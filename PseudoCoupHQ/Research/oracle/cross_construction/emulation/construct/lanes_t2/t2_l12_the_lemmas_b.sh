#!/bin/bash
# t2_l12_the_lemmas_b.sh -- task t2, lane 12: lane 10 again, with each theorem offered AS BUILT before the pipeline's simplified form (lane 11 measured why): the schemas' lemmas, in
# Lean, instantiated at every width the refused population needs and at
# the doubling ladder beside it.
#
# Each theorem's two sides are GENERATED from `construct/schemas.py`
# itself -- the left is the z3 operation, the right is `schemas.lower`'s
# own output on it -- and translated by `op_pipeline/lean/term_to_lean.py`
# with its own round-trip check, so a lemma cannot state something the
# tier does not do.
#
# CEILING: 120 s of `lean` per theorem.  A time limit is a FLAG: a
# theorem that does not close inside it is recorded with its own wall
# clock and re-running it with more room is a re-run of this lane, never
# a change to what is measured.
#
# MEMORY: bound 6 GB resident for this process, named abort
# ABORT_MEMORY_T2; each `lean` is its own process and its peak is read
# from `os.wait4`.
#
# Node: hq.research.compiler_graph.gate.lean
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=1

i=1
echo "[$i/$total] THE LEMMAS, generated and run"
python3 "$C/lean/run_lemmas_t2.py" prove 120
echo
echo "lane done"
