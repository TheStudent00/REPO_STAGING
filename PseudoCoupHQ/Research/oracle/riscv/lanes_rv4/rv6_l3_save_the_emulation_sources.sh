#!/bin/bash
# save every rendered RISC-V emulation source (c, cpp, go, rust; both routes) as files
set -u
P=PseudoCoupHQ; G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv; OP=$P/Research/op_pipeline; EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work; mkdir -p /work/rv6src
timeout 1800 python3 "$G/rv6_sources.py" run "$OP" "$OP" "$EMU" "$RV/twins.json" "$RV/model_table_rv.json" "$G/rv6_sources_run" "$G/emulations_riscv64" /work/rv6src
echo "  exit: $?"; ls "$G/emulations_riscv64" | wc -l; du -sh "$G/emulations_riscv64"
