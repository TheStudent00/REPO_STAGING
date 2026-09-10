#!/bin/bash
# t2_l14_the_shift_statement.sh -- task t2, lane 14: why the shifter's
# lemma cannot be STATED in either print form, with both texts and both
# answers.
#
# Lane 13 proved the adder, the comparisons, the widening and the
# bitwise schemas in Lean at every width and left the shifter refused
# BEFORE Lean with WIDTH_UNRESOLVED.  The brief names the shifter's
# lemma as one of the two it asks for, so the cause is looked at rather
# than recorded and left.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.compiler_graph.gate.lean
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=1

i=1
echo "[$i/$total] THE SHIFTER'S STATEMENT, in both print forms"
python3 - "$C" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[1] + "/lean")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline/lean")
import z3
import schemas as S
import run_lemmas_t2 as L

for width, word, wanted in [(16, 8, "shift_up"), (128, 64, "shift_up"),
                            (16, 8, "shift_down_arithmetic")]:
    rows, widths = L.operations(S.SHIFT_ROTATE, width, word)
    for name, term in rows:
        if name != wanted:
            continue
        posed = L.narrowed(term, word)
        built, _order, _instances = S.lower(posed, word)
        for form in L.PRINT_FORMS:
            left_text, left_node = L.printed(posed, form)
            right_text, right_node = L.printed(built, form)
            result = None
            if z3.is_bv(left_node):
                result = left_node.size()
            left = L.translated(left_text, widths, result)
            right = L.translated(right_text, widths, result)
            print("---- %s at %d over %d, the %r form" % (name, width, word, form))
            print("   left:  %s" % left_text[:300])
            print("   left refused:  %s" % (left["refused"],))
            print("   right: %s" % right_text[:600])
            print("   right refused: %s" % (right["refused"],))
            continue
        continue
    continue
PY
echo
echo "lane done"
