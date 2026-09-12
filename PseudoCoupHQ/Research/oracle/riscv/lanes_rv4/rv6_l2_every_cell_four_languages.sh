#!/bin/bash
# rv6: every RISC-V cell, both routes, ship flags, c cpp go rust. A sample of
# six cells first (so a route that refuses by name shows before the run),
# then the whole population, then the count.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv6gocache GOPATH=/work/rv6gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv6b /work/rv6s2
echo "[1/3] the sample, six cells: started $(date -u +%FT%TZ)"
timeout 900 python3 "$G/rv6_all_langs.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/rv6_sample" "$G/src_rv6_sample" /work/rv6s2 6
echo "  exit: $?"
echo "[2/3] every cell, four languages: started $(date -u +%FT%TZ)"
timeout 7000 python3 "$G/rv6_all_langs.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/rv6_all" "$G/src_rv6_all" /work/rv6
echo "  finished $(date -u +%FT%TZ)"
echo "[3/3] the count, beside rv3's 117 of 255"
timeout 900 python3 "$G/rv_general.py" count "$G/rv6_all" "$RV/twins.json" "$RV/certificates_riscv64_rv3.jsonl" "$RV/rv_loop.jsonl"
echo "  exit: $?"
