#!/bin/bash
# lp3_l24_cregidx_residual.sh -- the residual goal of the c.mul certificate
# (v7, with creg2reg_idx unfolded), in full, and two closing variants.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof; cd $P
F=$A/walk_handful_all_v7/Walk_probe_mul.lean
echo "=== the residual, as is"
timeout 300 lake env lean $F > /work/R0.out 2>&1; echo "rc=$?"; sed -n '/unsolved goals/,$p' /work/R0.out | grep -vE "warning|linter|Hint|^\s*$" | head -70 | cut -c1-200
echo "=== variant a: the simp call followed by split_ifs/split and simp_all"
python3 - "$F" /work/Ra.lean <<'PY'
import sys,re; t=open(sys.argv[1]).read()
i=t.rfind("  simp (config := {decide := true})"); j=t.find("\nend ", i)
body=t[i:j]; t=t[:i]+body.rstrip()+"\n  all_goals (try split) <;> simp_all\n"+t[j:]
open(sys.argv[2],"w").write(t)
PY
timeout 300 lake env lean /work/Ra.lean > /work/Ra.out 2>&1; echo "rc=$?"; grep -E "error" /work/Ra.out | head -3 | cut -c1-200
echo "=== variant b: BitVec literal lemmas added to the simp set"
sed 's/^    RETIRE_SUCCESS, reg_name_forwards, to_bits, Sail.BitVec.extractLsb, zero_reg,$/    RETIRE_SUCCESS, reg_name_forwards, to_bits, Sail.BitVec.extractLsb, zero_reg, BitVec.toNat_append, BitVec.toNat_ofNat, BitVec.append_def, Sail.BitVec.append,/' $F > /work/Rb.lean
timeout 300 lake env lean /work/Rb.lean > /work/Rb.out 2>&1; echo "rc=$?"; grep -E "error" /work/Rb.out | head -3 | cut -c1-200; sed -n '/unsolved goals/,$p' /work/Rb.out | grep -vE "warning|linter|Hint|^\s*$" | head -30 | cut -c1-200
echo done
