#!/bin/bash
# cov1 lane 3 -- rerun of lane 2 (full population) after a second finding:
# units-riscv's cells_of(unit) (rv_attest.py's own function, run over the
# WHOLE go corpus rather than the hand-picked probes it was built for)
# also yields cells outside the RISC-V model table's own 255-cell
# population -- concretely `c.nop` (shape "none"), the go compiler's
# alignment pad, which twins.json holds no row for because no x86
# operation computes "do nothing". All 18 go units carrying a `c.nop`
# were the ONLY 18 of 105 go units lane 2 marked inexpressible even into
# go itself (87/105) -- verified by direct check, zero of the 18 have
# any OTHER unproved cell. build_join.py's units-riscv now takes
# twins.json and drops any cell outside its 255-row population before
# it can block a unit. The x86 side is unchanged (already verified a
# subset of model_table_attest.json's own 257 attested cells: 0 outside
# cells found). Same guard, same no-compile/no-z3 join.
set -u
P=PseudoCoupHQ
OP=$P/Research/op_pipeline
MODEL=$P/Research/oracle/arch_opcodes/model
RV=$P/Research/oracle/riscv
COV=$P/Research/oracle/coverage
CERTS=$P/Research/oracle/cross_construction/emulation/autopoly/certificates.jsonl
RV6=$P/Research/oracle/cross_construction/emulation/construct/general/rv6_all.jsonl
export HOME=/work
mkdir -p /work/cov1_full3
echo "[1/7] x86 units, full population (unchanged from lane 2): started $(date -u +%FT%TZ)"
timeout 18000 python3 "$COV/build_join.py" units-x86 "$OP" "$MODEL" "$COV/units_x86.jsonl"
echo "  exit: $?"
echo "[2/7] riscv64 units, full population, filtered to twins.json's 255-cell population: started $(date -u +%FT%TZ)"
timeout 3600 python3 "$COV/build_join.py" units-riscv "$RV" "$RV/attest_rv.json" "$RV/twins.json" "$COV/units_riscv64.jsonl"
echo "  exit: $?"
echo "[3/7] x86 bank reduction"
timeout 1800 python3 "$COV/build_join.py" bank-x86 "$CERTS" "$COV/bank_x86.json"
echo "  exit: $?"
echo "[4/7] riscv64 bank reduction"
timeout 900 python3 "$COV/build_join.py" bank-riscv "$RV6" "$COV/bank_riscv64.json"
echo "  exit: $?"
echo "[5/7] x86 matrix, full population"
timeout 1800 python3 "$COV/build_join.py" matrix "$COV/units_x86.jsonl" "$COV/bank_x86.json" "$COV/coverage_x86.json" --arch x86_64 --sources c,cpp,rust,go,swift --targets c,cpp,rust,go,swift
echo "  exit: $?"
echo "[6/7] riscv64 matrix, full population"
timeout 900 python3 "$COV/build_join.py" matrix "$COV/units_riscv64.jsonl" "$COV/bank_riscv64.json" "$COV/coverage_riscv64.json" --arch riscv64 --sources c,go --targets c,cpp,go,rust
echo "  exit: $?"
echo "[7/7] guard over every json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" \
  "$COV/bank_x86.json" "$COV/bank_riscv64.json" \
  "$COV/coverage_x86.json" "$COV/coverage_riscv64.json"
echo "  guard exit: $?"
echo "finished $(date -u +%FT%TZ)"
echo "---- full x86 matrix (fixed) ----"
cat "$COV/coverage_x86.json"
echo "---- full riscv64 matrix (fixed) ----"
cat "$COV/coverage_riscv64.json"
