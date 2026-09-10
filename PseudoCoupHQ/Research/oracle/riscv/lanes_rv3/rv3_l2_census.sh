#!/usr/bin/env bash
# rv3 lane 2 -- THE CENSUS, and it is evidence rather than a decision:
# every certificate source on a compiled target, built for riscv64 on the
# new image and carved, with the mnemonics `riscv_reference.py` has no
# entry for tallied.  The x86 table's own rule is that no entry is
# invented for an opcode no body contains, so this lane is what decides
# which rows the RISC-V reference gains in lane 3.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
AP=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
export HOME=/work
export GOCACHE=/work/rv3gocache GOPATH=/work/rv3gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv3census
total=2

echo "[1/$total] the sample the law asks for: the first 20 sources"
python3 "$RV/inherit_rv3.py" census "$L0" "$OP" \
  "$RV/twins.json" "$AP/certificates.jsonl" "$AP" \
  "$RV/census_rv3_sample" /work/rv3census_sample 20
echo "sample rc=$?"

echo "[2/$total] the whole census"
python3 "$RV/inherit_rv3.py" census "$L0" "$OP" \
  "$RV/twins.json" "$AP/certificates.jsonl" "$AP" \
  "$RV/census_rv3" /work/rv3census
echo "census rc=$?"
echo "lane rv3_l2 done"
