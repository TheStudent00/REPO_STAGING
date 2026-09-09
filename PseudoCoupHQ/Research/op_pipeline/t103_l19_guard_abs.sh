#!/bin/bash
set -e
echo "[1/2] check_no_spelling_keys.py with absolute paths"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json PseudoCoupHQ/Research/op_pipeline/interp103_term.json PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json PseudoCoupHQ/Research/op_pipeline/interp103_step.json
echo "[2/2] grep -c exempt with absolute paths"
grep -c exempt PseudoCoupHQ/Research/op_pipeline/interp103_bounds.json PseudoCoupHQ/Research/op_pipeline/interp103_canonical.json PseudoCoupHQ/Research/op_pipeline/interp103_term.json PseudoCoupHQ/Research/op_pipeline/interp103_gate_c181.json PseudoCoupHQ/Research/op_pipeline/interp103_step.json
