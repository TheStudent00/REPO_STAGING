#!/bin/bash
# t2_l19_the_lemmas_by_shape.sh -- task t2, lane 19: the lemmas restated
# per SHAPE and per LIMB, and the schemas re-verified beside them.
#
# WHY THE RESTATEMENT.  Lanes 10 to 15 stated one lemma per (schema,
# width) and posed it on the LOW WORD of the operation.  Neither is the
# question the tier needs answered.  A term reads a wide value through
# an extract that may name ANY limb, so a theorem about the low word
# does not carry the second one; and the widening schema rewrites an
# extract at ANY pair of offsets, so a theorem stated at two offsets does
# not carry a third.  Both holes are closed by stating the lemma at the
# SHAPE the lowering rewrote -- the operation plus its widths and offsets
# -- and once per LIMB of its answer.  The tier's lemma route asks for
# exactly those and for nothing else.
#
#   [1/4] the shapes the refused population needs
#   [2/4] the schemas at the narrow widths, whole
#   [3/4] the schemas at the widths this pipeline meets
#   [4/4] the lemmas, generated and run, 120 s of `lean` per theorem
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.compiler_graph.gate.lean
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=4

i=1
echo "[$i/$total] THE SHAPES THE REFUSED POPULATION NEEDS"
python3 "$C/lean/run_lemmas_t2.py" instances
echo

i=2
echo "[$i/$total] THE SCHEMAS AT THE NARROW WIDTHS, whole"
python3 "$C/check_schemas.py" narrow
echo

i=3
echo "[$i/$total] THE SCHEMAS AT THE WIDTHS THIS PIPELINE MEETS"
python3 "$C/check_schemas.py" wide
echo

i=4
echo "[$i/$total] THE LEMMAS, per shape and per limb"
python3 "$C/lean/run_lemmas_t2.py" prove 120
echo
echo "lane done"
