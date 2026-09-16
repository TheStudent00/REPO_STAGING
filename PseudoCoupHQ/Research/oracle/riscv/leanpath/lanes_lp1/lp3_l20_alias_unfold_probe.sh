#!/bin/bash
# lp3_l20_alias_unfold_probe.sh -- the four walk certificates that failed in
# v5 all pass through a compressed-instruction alias; add the alias
# definition to each certificate's simp list (what the walk.py patch now
# emits) and re-run Lean on the four. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof; W=$A/walk_handful_all_v5
cd $P
for u in go_op_312 probe_mul c_op_102 c_op_498; do
  F=$W/Walk_$u.lean; G=/work/Alias_$u.lean
  sed -E 's/(strip_(C_[A-Z0-9_]+),)/\1 alias_\2,/g' $F > $G
  echo "=== $u: $(grep -oE 'alias_C_[A-Z0-9_]+,' $G | sort -u | tr '\n' ' ')"
  start=$(date +%s); timeout 600 lake env lean $G > /work/Alias_$u.out 2>&1; rc=$?
  echo "  rc=$rc seconds=$(( $(date +%s) - start )) error lines=$(grep -c error /work/Alias_$u.out)"
  grep -n "error" /work/Alias_$u.out | head -3 | cut -c1-200
  [ $rc -eq 0 ] || { echo "  --- residual (first 40 goal lines)"; sed -n '/unsolved goals/,$p' /work/Alias_$u.out | grep -vE "warning|Hint|linter|^\s*$" | head -40 | cut -c1-240; }
done
echo done
