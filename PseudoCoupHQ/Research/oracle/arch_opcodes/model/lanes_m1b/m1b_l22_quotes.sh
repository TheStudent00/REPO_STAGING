#!/usr/bin/env bash
# m1b_l22_quotes.sh -- task m1b: the objects the report quotes, each
# printed by the command that reads it, so that a quotation of code is
# a transcript the verifier re-runs rather than an attribution.
set -euo pipefail

echo "[1/6] the one width rule, as model_table.py states it"
sed -n '185,196p' /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py

echo "[2/6] reference.build_binary's one-operand branch, after the change"
sed -n '785,801p' /projects/PseudoCoupHQ/Research/op_pipeline/reference.py

echo "[3/6] the three operand shapes added to model_translate.shapes_for"
sed -n '253,255p' /projects/PseudoCoupHQ/Research/op_pipeline/lean/model_translate.py

echo "[4/6] the two readings model_table.py added to the attestation"
sed -n '838,843p;861,866p' /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py

echo "[5/6] the guard's exempt list, which holds mnem exactly"
sed -n '106,109p' /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py

echo "[6/6] grep -c exempt over the files this task added"
grep -c exempt /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.md /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.py /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode/per_opcode.py
echo "[6/6] done"
