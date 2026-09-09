#!/bin/bash
set -e
echo "[1/2] interp103_step.py, re-run after the spelling-guard catch"
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 interp103_step.py >/dev/null
echo "[2/2] check_no_spelling_keys.py, re-run"
python3 check_no_spelling_keys.py interp103_bounds.json interp103_canonical.json interp103_term.json interp103_gate_c181.json interp103_step.json
grep -c exempt interp103_bounds.json interp103_canonical.json interp103_term.json interp103_gate_c181.json interp103_step.json || true
