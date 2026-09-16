#!/bin/bash
# lp3_l46_index_probe.sh -- the survivors2 lhu file with the `try` removed
# from its simp call, so Lean names the identifier that breaks the
# unfolding; and lean-sail's private/protected defs listed. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof; cd $P
f=$(ls $A/equals_corpus_survivors2_*/Equals_lhu_gpr_gpr_16__reg_a0__go__all_constructed__ZBB_EXTOP_*_fixed_width.lean | head -1)
sed -E "s/^  try simp only/  simp only/" "$f" > /work/X.lean
timeout 300 lake env lean /work/X.lean > /work/X.out 2>&1; echo "rc=$?"; grep -E "error" /work/X.out | head -4 | cut -c1-220
echo "=== private / protected in lean-sail"; grep -rnE "^(private|protected) (def|abbrev)" $P/.lake/packages/Sail/Sail/*.lean | cut -c1-140 | head -12
echo "=== the simp list of that file"; grep -E "^  try simp only" "$f" | cut -c1-700
echo done
