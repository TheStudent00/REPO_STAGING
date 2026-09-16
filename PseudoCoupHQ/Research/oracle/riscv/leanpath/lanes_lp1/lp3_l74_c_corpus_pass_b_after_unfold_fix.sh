#!/bin/bash
# lp3_l74_c_corpus_pass_b_after_unfold_fix.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.system.pass_b_build over c,
# over the whole c table (l63): every arm of every certified pure form is rendered from
# operator_for (l53) and nothing else; each emulation is compiled at the
# corpus's ship flags, cut out, decoded by Sail's decoder, its meaning
# composed and certified (the walk); then proved equal to a definition
# (equals); then the eye table. Fetches nothing.
# l69: the c render again from the l68 table (l64 rendered 7 from 7 keys, all proved).
# l74: the c render from the l73 table.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
L=$P/$PLIB
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
R=$A/runs/handful_c
cd $A
echo "[1/4] render from operator_for"
rm -rf $R/pass_b; mkdir -p $R/pass_b
python3 -u -m leanpath render $L $S $R/operator_for/operator_for.json $R/units.json $R/pass_b c > $R/pass_b/render.log 2>&1
grep -E "keys usable|render:" $R/pass_b/render.log
echo "[2/4] lower, decode, compose, certify"
export WALK_JOBS=2 WALK_MAX_WORDS=400
python3 -u -m leanpath walk $P $X $PLIB $S $R/pass_b/units.json $R/pass_b/walk 600 > $R/pass_b/walk.log 2>&1
grep -E "decode:|walk:|Traceback" $R/pass_b/walk.log | cut -c1-200
echo "[3/4] prove each emulation equal to a definition"
export EQUALS_UNIT_BUDGET_S=150 EQUALS_CHUNK=12
python3 -u -m leanpath equals $P $PLIB $S $R/pass_b/walk/walk.json $R/pass_b/equals 120 64 > $R/pass_b/equals.log 2>&1
grep -E "PROVED|equals:|Traceback" $R/pass_b/equals.log | cut -c1-160 | tail -12
echo "[4/4] the eye table"
python3 -m leanpath eye_check $R/pass_b/render.json $R/pass_b/walk/walk.json $R/pass_b/equals/equals.json > $R/pass_b/eye_table.md 2>&1
grep -c "^| " $R/pass_b/eye_table.md; grep -E "PROVED|NOT PROVED" $R/pass_b/eye_table.md | wc -l; head -6 $R/pass_b/eye_table.md | cut -c1-240
echo done
