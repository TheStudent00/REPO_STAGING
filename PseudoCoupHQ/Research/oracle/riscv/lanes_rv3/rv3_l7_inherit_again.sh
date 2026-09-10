#!/usr/bin/env bash
# rv3 lane 7 -- THE INHERITANCE RE-RUN, section 1 row 3.  Task rv2's own
# inheritance, with ONLY the four compile routes replaced, so the one
# thing that moved between the two runs is the IMAGE: the rust riscv64
# LINUX target, the riscv64 glibc and libstdc++ headers, and clang++
# aimed through them.
#
# THE x86 SIDE IS DELIBERATELY THE SAME ONE rv2 READ -- the
# pre-correction reference in `ref2_originals` and the model table on
# disk -- so the per-target table can be read BESIDE rv2's with the
# compile route as the only difference.  Re-deriving against ref2's
# corrected table is section 1 row 2, and it waits for ref2.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
AP=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
export HOME=/work
export GOCACHE=/work/rv3gocache GOPATH=/work/rv3gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv3inh_sample /work/rv3inh
total=3

echo "[1/$total] the bytes this lane reads"
sha256sum "$L0/reference.py" "$L0/condition_table.py" \
  "$MODEL/model_table_rows.json" "$AP/certificates.jsonl" \
  "$RV/twins.json" "$RV/riscv_reference.py"

echo "[2/$total] the sample the law asks for: the first 20 certificates"
python3 "$RV/inherit_rv3.py" run "$L0" "$OP" \
  "$MODEL/model_table_rows.json" "$RV/twins.json" \
  "$AP/certificates.jsonl" "$AP" \
  "$RV/certificates_riscv64_rv3_sample" /work/rv3inh_sample 20
echo "sample rc=$?"

echo "[3/$total] the whole inheritance"
python3 "$RV/inherit_rv3.py" run "$L0" "$OP" \
  "$MODEL/model_table_rows.json" "$RV/twins.json" \
  "$AP/certificates.jsonl" "$AP" \
  "$RV/certificates_riscv64_rv3" /work/rv3inh
echo "inherit rc=$?"
echo "lane rv3_l7 done"
