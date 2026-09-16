#!/bin/bash
# lp3_l27_zero_extend_residual.sh -- the residual of the c.mul certificate
# (v9: zero_extend unfolded), the library's BitVec helpers, two variants.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof; cd $P
F=$A/walk_handful_all_v9/Walk_probe_mul.lean
echo "=== the library's BitVec helpers"
ls $P/.lake/packages/; B=$(ls $P/.lake/packages/*/Sail/BitVec.lean 2>/dev/null | head -1); echo "$B"; grep -nE "^namespace|^end |^(@\[[^]]*\] )?def |^abbrev " "$B" | head -60 | cut -c1-120
echo "=== the residual, as is (first 40 goal lines)"
timeout 300 lake env lean $F > /work/R0.out 2>&1; echo "rc=$?"; sed -n '/unsolved goals/,$p' /work/R0.out | grep -vE "warning|linter|Hint|^\s*$" | sed -n '9,48p' | cut -c1-200
for v in "Sail.BitVec.zeroExtend" "Sail.BitVec.zeroExtend, BitVec.setWidth, BitVec.zeroExtend, BitVec.toNat_setWidth"; do
  echo "=== variant: + $v"
  sed "s/^    RETIRE_SUCCESS, reg_name_forwards, to_bits, Sail.BitVec.extractLsb, zero_reg,$/    RETIRE_SUCCESS, reg_name_forwards, to_bits, Sail.BitVec.extractLsb, zero_reg, $v,/" $F > /work/Rv.lean
  timeout 300 lake env lean /work/Rv.lean > /work/Rv.out 2>&1; echo "rc=$?"; grep -E "error" /work/Rv.out | head -3 | cut -c1-200; sed -n '/unsolved goals/,$p' /work/Rv.out | grep -vE "warning|linter|Hint|^\s*$" | sed -n '9,30p' | cut -c1-200
done
echo done
