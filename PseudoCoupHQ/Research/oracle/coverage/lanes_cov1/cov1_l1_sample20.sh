#!/bin/bash
# cov1 lane 1 -- the join, sampled at 20 units per source language first,
# both architectures, so the mechanism is visible before the full run.
# No compile, no z3 solving: this is data-join bookkeeping over stores
# that already exist (model_table.py's own classifier, rv_attest.py's own
# cells_of(), the bank, rv6_all.jsonl).
set -u
P=PseudoCoupHQ
OP=$P/Research/op_pipeline
MODEL=$P/Research/oracle/arch_opcodes/model
RV=$P/Research/oracle/riscv
COV=$P/Research/oracle/coverage
CERTS=$P/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl
RV6=$P/Research/oracle/cross_construction/emulation/construct/general/rv6_all.jsonl
export HOME=/work
mkdir -p /work/cov1_sample
echo "[1/7] x86 units, sample 20/lang: started $(date -u +%FT%TZ)"
python3 "$COV/build_join.py" units-x86 "$OP" "$MODEL" "$COV/sample_units_x86.jsonl" --limit 20
echo "  exit: $?"
echo "[2/7] riscv64 units, sample 20/lang: started $(date -u +%FT%TZ)"
python3 "$COV/build_join.py" units-riscv "$RV" "$RV/attest_rv.json" "$COV/sample_units_riscv64.jsonl" --limit 20
echo "  exit: $?"
echo "[3/7] x86 bank reduction"
python3 "$COV/build_join.py" bank-x86 "$CERTS" "$COV/sample_bank_x86.json"
echo "  exit: $?"
echo "[4/7] riscv64 bank reduction"
python3 "$COV/build_join.py" bank-riscv "$RV6" "$COV/sample_bank_riscv64.json"
echo "  exit: $?"
echo "[5/7] x86 matrix, sample"
python3 "$COV/build_join.py" matrix "$COV/sample_units_x86.jsonl" "$COV/sample_bank_x86.json" "$COV/sample_coverage_x86.json" --arch x86_64 --sources c,cpp,rust,go,swift --targets c,cpp,rust,go,swift
echo "  exit: $?"
echo "[6/7] riscv64 matrix, sample"
python3 "$COV/build_join.py" matrix "$COV/sample_units_riscv64.jsonl" "$COV/sample_bank_riscv64.json" "$COV/sample_coverage_riscv64.json" --arch riscv64 --sources c,go --targets c,cpp,go,rust
echo "  exit: $?"
echo "[7/7] guard over every json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" \
  "$COV/sample_bank_x86.json" "$COV/sample_bank_riscv64.json" \
  "$COV/sample_coverage_x86.json" "$COV/sample_coverage_riscv64.json"
echo "  guard exit: $?"
echo "finished $(date -u +%FT%TZ)"
echo "---- sample x86 matrix ----"
cat "$COV/sample_coverage_x86.json"
echo "---- sample riscv64 matrix ----"
cat "$COV/sample_coverage_riscv64.json"
