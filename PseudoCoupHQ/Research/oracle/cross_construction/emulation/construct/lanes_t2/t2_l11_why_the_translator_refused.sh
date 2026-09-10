#!/bin/bash
# t2_l11_why_the_translator_refused.sh -- task t2, lane 11: the two
# causes lane 10's translator raised, with the objects behind them.
#
# Lane 10 proved the adder, the comparisons, the widening and four of
# the five bitwise operations in Lean at every width, and refused the
# shifts (ROUNDTRIP_MISMATCH), the high product (WIDTH_UNRESOLVED) and
# the select (ROUNDTRIP_MISMATCH) BEFORE Lean.  A refusal before the
# prover is a statement that could not be made, not a theorem that
# failed, so this lane prints the text, the reprint and the difference.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.compiler_graph.gate.lean
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=1

i=1
echo "[$i/$total] THE TEXTS, THE REPRINTS AND THE FIRST DIFFERENCE"
python3 - "$C" <<'PY'
import sys, os
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[1] + "/lean")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline/lean")
import z3
import schemas as S
import run_lemmas_t2 as L
import term_to_lean

def first_difference(left, right):
    for index in range(min(len(left), len(right))):
        if left[index] != right[index]:
            return index
    if len(left) == len(right):
        return None
    return min(len(left), len(right))

for schema, width, word, wanted in [
        (S.SHIFT_ROTATE, 16, 8, "shift_up"),
        (S.SHIFT_ROTATE, 128, 64, "shift_up"),
        (S.MULTIPLY, 16, 8, "product_high"),
        (S.MULTIPLY, 128, 64, "product_high"),
        (S.BITWISE, 16, 8, "select")]:
    rows, widths = L.operations(schema, width, word)
    for name, term in rows:
        if name != wanted:
            continue
        posed = L.narrowed(term, word)
        built, _order, _instances = S.lower(posed, word)
        for side, held in (("left", posed), ("right", built)):
            text, node = L.printed(held)
            result = None
            if z3.is_bv(node):
                result = node.size()
            answer = term_to_lean.translate(text, widths, result)
            print("---- %s at %d over %d, %s, the %s side"
                  % (schema, width, word, name, side))
            print("   text:    %s" % text[:400])
            print("   refused: %s" % (answer["refused"],))
            reprint = answer.get("z3_reprint")
            if reprint is not None:
                reprint = " ".join(str(reprint).split())
                flat = " ".join(text.split())
                print("   reprint: %s" % reprint[:400])
                where = first_difference(flat, reprint)
                if where is not None:
                    print("   they differ at offset %d:" % where)
                    print("      text    ...%s" % flat[max(0, where - 40):where + 60])
                    print("      reprint ...%s" % reprint[max(0, where - 40):where + 60])
            continue
        continue
    continue
PY
echo
echo "lane done"
