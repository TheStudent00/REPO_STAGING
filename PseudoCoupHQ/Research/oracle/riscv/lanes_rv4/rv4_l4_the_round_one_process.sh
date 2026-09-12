#!/bin/bash
# rv4, the round as the owner asked it: t4's RISC-V driver with optimization off,
# ONE process, no pool, no clock; then the count beside rv3's 117 of 255.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv4gocache GOPATH=/work/rv4gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv4o0
echo "[1/2] the round, optimization off, one process: started $(date -u +%FT%TZ)"
timeout 3000 python3 "$G/rv4_o0.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" \
  "$G/rv4_o0" "$G/src_rv4_o0" /work/rv4o0
echo "  finished $(date -u +%FT%TZ)"
echo ""
echo "[2/2] the count, beside rv3's 117 of 255"
timeout 900 python3 "$G/rv_general.py" count "$G/rv4_o0" \
  "$RV/twins.json" "$RV/certificates_riscv64_rv3.jsonl" "$RV/rv_loop.jsonl"
echo "  exit: $?"
