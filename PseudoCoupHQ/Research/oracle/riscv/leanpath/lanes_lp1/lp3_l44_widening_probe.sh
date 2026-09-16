#!/bin/bash
# lp3_l44_widening_probe.sh -- the widening leaf, probed: where lean-sail
# defines the helpers bv_decide left as atoms (shift_bits_left/right,
# extractLsb, the +++ append), and whether unfolding them lets bv_decide
# close the zero-extension (lhu) and the constructed adder. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof; cd $P
echo "=== lean-sail: namespaces and the helpers"
for f in $P/.lake/packages/Sail/Sail/*.lean; do echo "--- $(basename $f): $(grep -oE "^namespace \S+" $f | tr "\n" " ")"; grep -nE "^(@\[[^]]*\] )?(def|abbrev|instance|notation|infixl|infixr|macro)[^\n]*(shift_bits|shiftLeft|shiftRight|extractLsb|\+\+\+|HAppend|append)" $f | cut -c1-160 | head -8; done
grep -rn "shift_bits_left" $P/LeanIM/Prelude.lean $P/LeanIM/Defs.lean 2>/dev/null | head -3 | cut -c1-160
echo "=== variants on the lhu file"
F=$(ls $A/equals_corpus_survivors_*/Equals_lhu_gpr_gpr_16__reg_a0__go__all_constructed__ZBB_EXTOP_*_fixed_width.lean | head -1)
for extra in "shift_bits_left, shift_bits_right, Sail.BitVec.extractLsb, Sail.BitVec.zeroExtend" "shift_bits_left, shift_bits_right, Sail.BitVec.extractLsb, Sail.BitVec.zeroExtend, Sail.BitVec.append, HAppend.hAppend, BitVec.append" "shift_bits_left, shift_bits_right, Sail.BitVec.extractLsb, Sail.BitVec.zeroExtend, Sail.BitVec.shiftLeft, Sail.BitVec.shiftRight, Sail.BitVec.append, HAppend.hAppend, BitVec.append, BitVec.shiftLeft, BitVec.ushiftRight"; do
  sed -E "s/^  try simp only \[(.*)\]$/  try simp only [\1, $extra]/" $F > /work/V.lean
  timeout 300 lake env lean /work/V.lean > /work/V.out 2>&1; echo "+ [$extra] -> rc=$?"; grep -E "error" /work/V.out | head -2 | cut -c1-160; grep -A2 "opaque variables" /work/V.out | head -3 | cut -c1-200
done
echo "=== the adder file with the third variant"
F=$(ls $A/equals_corpus_survivors_*/Equals_add_gpr_gpr_gpr_64__reg_a0__c__all_constructed__RTYPE_00_fixed_width.lean | head -1)
sed -E "s/^  try simp only \[(.*)\]$/  try simp only [\1, shift_bits_left, shift_bits_right, Sail.BitVec.extractLsb, Sail.BitVec.zeroExtend, Sail.BitVec.shiftLeft, Sail.BitVec.shiftRight, Sail.BitVec.append, HAppend.hAppend, BitVec.append, BitVec.shiftLeft, BitVec.ushiftRight]/" $F > /work/W.lean
start=$(date +%s); timeout 600 lake env lean /work/W.lean > /work/W.out 2>&1; echo "adder -> rc=$? in $(( $(date +%s) - start ))s"; grep -E "error" /work/W.out | head -2 | cut -c1-160; grep -A2 "opaque variables" /work/W.out | head -3 | cut -c1-200
echo done
