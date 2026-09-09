#!/bin/bash
set -e
echo "[1/2] check_no_spelling_keys.py with absolute paths"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py /projects/PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_term.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_step.json
echo "[2/2] grep -c exempt with absolute paths"
grep -c exempt /projects/PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_term.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json /projects/PseudoCoupHQ/Research/op_pipeline/interp103_step.json
