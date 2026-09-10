#!/bin/bash
# t2_l15_schemas_and_lemmas_after_the_folding.sh -- task t2, lane 15:
# the schemas re-verified and the lemmas re-run after the widening
# schema stopped writing steps that do nothing (`0 |`, `<< 0`).
#
# WHY THE FOLDING.  Lane 14 measured that the shifter's lemma could be
# stated in neither print form: the pipeline's simplified form hits the
# translator's round-trip check on a commutative EQUALITY's argument
# order, and the as-built form left a `0 |` whose numeral the
# translator's width unification cannot pin.  The second is this file's
# own doing and is now gone; the first is not this task's to change and
# is why the as-built form is the fallback.
#
#   [1/3] the schemas at the narrow widths, whole, divider included
#   [2/3] the schemas at the widths this pipeline meets
#   [3/3] the lemmas, generated and run, 120 s of `lean` per theorem
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=3

i=1
echo "[$i/$total] THE SCHEMAS AT THE NARROW WIDTHS, whole"
python3 "$C/check_schemas.py" narrow
echo

i=2
echo "[$i/$total] THE SCHEMAS AT THE WIDTHS THIS PIPELINE MEETS"
python3 "$C/check_schemas.py" wide
echo

i=3
echo "[$i/$total] THE LEMMAS, generated and run"
python3 "$C/lean/run_lemmas_t2.py" prove 120
echo
echo "lane done"
