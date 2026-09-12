#!/bin/bash
# rv5: every RISC-V cell, both policies, ship flags, one process.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv5gocache GOPATH=/work/rv5gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv5
echo "[1/2] every cell, both policies: started $(date -u +%FT%TZ)"
timeout 5400 python3 "$G/rv5_all.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" \
  "$G/rv5_all" "$G/src_rv5_all" /work/rv5
echo "  finished $(date -u +%FT%TZ)"
echo ""
echo "[2/2] the count, beside rv3's 117 of 255"
timeout 900 python3 "$G/rv_general.py" count "$G/rv5_all" \
  "$RV/twins.json" "$RV/certificates_riscv64_rv3.jsonl" "$RV/rv_loop.jsonl"
echo "  exit: $?"
