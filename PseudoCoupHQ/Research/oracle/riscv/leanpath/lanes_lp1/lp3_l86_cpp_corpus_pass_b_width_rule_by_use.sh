#!/bin/bash
# lp3_l86_cpp_corpus_pass_b_width_rule_by_use.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.system.pass_b_build over cpp:
# every arm of every certified pure form is rendered from cpp's `operator_for`
# and from nothing else; each emulation is compiled at the corpus's ship flags,
# cut out at its symbol, decoded by Sail's own decoder, its meaning composed
# from Sail's definitions and certified (the walk); then proved equal to a
# definition (equals); then the eye table. Fetches nothing.
#
# WHY THIS RUNS: THE WIDTH RULE BY THE DEFINITION'S OWN USE, second half, over
# ALL of cpp, after the gate (l82) was read. `render` takes an arch-unit for a
# key when the arch-unit's holder widths equal the widths the key's own text
# reads its operands at -- not 64 for every key. The cpp part of the l81 render
# it replaces had 18 emulations and refused the W forms (proved into the table,
# held at 32-bit holders); this render is from the l85 table. This lane is the
# cpp part of l81 only.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
L=$P/$PLIB
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
OP=PseudoCoupHQ/Research/op_pipeline
R=$A/runs/corpus_cpp
cd $A
echo "[1/4] render every arm of every definition from operator_for only"
rm -rf $R/pass_b; mkdir -p $R/pass_b
python3 -u -m leanpath render $L $S $R/operator_for/operator_for.json $R/units.json $R/pass_b cpp > $R/pass_b/render.log 2>&1
grep -E "keys usable|    at |render:|Traceback" $R/pass_b/render.log | cut -c1-140
grep -E "uses its reads at widths" $R/pass_b/render.log | cut -c1-200
python3 $OP/check_no_spelling_keys.py $R/pass_b/render.json 2>&1 | tail -1
echo "[2/4] lower, decode, compose, certify"
export WALK_JOBS=2 WALK_MAX_WORDS=400
n=$(python3 -c "import json; print(len(json.load(open('$R/pass_b/units.json'))))" 2>/dev/null || echo 0)
echo "  $n emulations"
if [ "$n" -gt 0 ]; then
  python3 -u -m leanpath walk $P $X $PLIB $S $R/pass_b/units.json $R/pass_b/walk 600 > $R/pass_b/walk.log 2>&1
  grep -E "decode:|walk:|Traceback" $R/pass_b/walk.log | cut -c1-200
fi
echo "[3/4] prove each emulation equal to a definition"
export EQUALS_UNIT_BUDGET_S=150 EQUALS_CHUNK=12
if [ "$n" -gt 0 ]; then
  python3 -u -m leanpath equals $P $PLIB $S $R/pass_b/walk/walk.json $R/pass_b/equals 120 64 > $R/pass_b/equals.log 2>&1
  grep -E "PROVED|equals:|Traceback" $R/pass_b/equals.log | cut -c1-160 | tail -40
fi
echo "[4/4] the eye table"
python3 -m leanpath eye_check $R/pass_b/render.json $R/pass_b/walk/walk.json $R/pass_b/equals/equals.json > $R/pass_b/eye_table.md 2>&1
python3 $OP/check_no_spelling_keys.py $R/pass_b/walk/walk.json $R/pass_b/equals/equals.json 2>&1 | tail -2
grep -E "^Rendered" $R/pass_b/eye_table.md
echo "  rows proved: $(grep -c 'PROVED equal' $R/pass_b/eye_table.md)"
grep -E "PROVED equal" $R/pass_b/eye_table.md | cut -c1-120
echo done
