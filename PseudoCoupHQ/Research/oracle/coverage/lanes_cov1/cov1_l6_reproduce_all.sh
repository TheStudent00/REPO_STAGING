#!/bin/bash
# cov1 lane 6 -- run every verify_*.py helper and the guard, verbatim,
# so log_266 can carry each as a `$ ` shell transcript. Read-only.
set -u
P=PseudoCoupHQ
OP=$P/Research/op_pipeline
COV=$P/Research/oracle/coverage
echo "[1/5] guard"
python3 "$OP/check_no_spelling_keys.py" "$COV/bank_x86.json" "$COV/bank_riscv64.json" "$COV/coverage_x86.json" "$COV/coverage_riscv64.json"
echo "[2/5] matrices"
python3 "$COV/verify_matrices.py"
echo "[3/5] blockers"
python3 "$COV/verify_blockers.py"
echo "[4/5] length view"
python3 "$COV/verify_length.py"
echo "[5/5] defects"
python3 "$COV/verify_defects.py"
