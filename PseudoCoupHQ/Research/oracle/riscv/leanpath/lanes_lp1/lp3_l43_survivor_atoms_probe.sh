#!/bin/bash
# lp3_l43_survivor_atoms_probe.sh -- two survivor units' fixed-width files
# run again with bv_decide's full message kept (which atoms it could not
# open), the lean-sail definitions of those helpers, and one variant with
# the helpers' own bodies unfolded. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof; cd $P
for f in $(ls $A/equals_corpus_survivors_*/Equals_lhu_gpr_gpr_16__reg_a0__go__all_constructed__ZBB_EXTOP_*_fixed_width.lean $A/equals_corpus_survivors_*/Equals_add_gpr_gpr_gpr_64__reg_a0__c__all_constructed__RTYPE_00_fixed_width.lean 2>/dev/null | head -2); do
  echo "=== $(basename $f)"; grep -E "^  try simp only" $f | cut -c1-300
  timeout 300 lake env lean $f > /work/S.out 2>&1; echo "rc=$?"; sed -n '/error/,$p' /work/S.out | grep -vE "^\s*$" | head -40 | cut -c1-200
done
echo "=== the lean-sail helpers"
grep -rnE "^(@\[[^]]*\] )?def (extractLsb|shiftLeft|shiftRight|zeroExtend|signExtend|truncate|append|toNatInt|updateSubrange|shiftl|shiftr|arithShiftr|logShiftr)\b" $P/.lake/packages/Sail/Sail/*.lean | cut -c1-220 | head -20
grep -n -A3 "def extractLsb\b" $P/.lake/packages/Sail/Sail/BitVec.lean | head -8
grep -rn -B1 -A3 "^def shift_bits_left\|^def shift_bits_right\b\|^def shift_bits_right_arith" $P/LeanIM/*.lean | head -16 | cut -c1-200
echo done
