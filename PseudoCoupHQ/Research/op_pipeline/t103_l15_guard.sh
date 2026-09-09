#!/bin/bash
set -e
echo "[1/2] check_no_spelling_keys.py over every interp103_*.json"
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 check_no_spelling_keys.py interp103_bounds.json interp103_canonical.json interp103_term.json interp103_gate_c181.json interp103_step.json
echo "[2/2] grep -c exempt over the same files"
grep -c exempt interp103_bounds.json interp103_canonical.json interp103_term.json interp103_gate_c181.json interp103_step.json || true
