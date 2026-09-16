#!/bin/bash
# sl1 lane 9 -- read-only: the grammar of the Lean the sail compiler emits,
# from its own printer (sail_lean_backend/pretty_print_lean.ml): how an
# expression, a let, an if, a match, a function application, a literal, a
# register read and a register write are printed, and the operator table.
# A reader of the emit is written against these, not against guesses.
set -u
total=3
export HOME=/work
P=$(ls /opt/opam/default/.opam-switch/sources/sail_lean_backend.0.20.2/src/sail_lean_backend/pretty_print_lean.ml 2>/dev/null || find /opt/opam -name pretty_print_lean.ml 2>/dev/null | head -1)
echo "[1/$total] the printer: $P, $(wc -l < $P) lines; its top-level definitions"
grep -n '^let rec \|^let \|^and ' $P | head -150
echo "[2/$total] the operator table and the expression printer, LITERAL"
grep -n 'op_of_id' $P | head -5
awk '/^let op_of_id/,/^let [a-z_]+ .*=$/' $P | head -80
grep -n 'E_app\|E_if\|E_let\|E_match\|E_lit\|E_var\|E_field\|E_vector\|E_block\|E_assign\|E_return\|E_throw\|E_assert\|E_cast\|E_typ\|E_id\|E_tuple\|E_struct\|E_ref\|E_exit\|E_loop\|E_for\|E_internal' $P | head -80
echo "[3/$total] doc_exp, the whole expression printer, LITERAL (first 400 lines from its definition)"
S=$(grep -n 'doc_exp' $P | head -1 | cut -d: -f1)
echo "doc_exp first mention at line $S"
L=$(grep -n '^let rec doc_exp\|^and doc_exp\|^let doc_exp' $P | head -1 | cut -d: -f1)
echo "doc_exp defined at line $L"
sed -n "${L},$((L+400))p" $P
echo "done $(date -u +%FT%TZ)"
