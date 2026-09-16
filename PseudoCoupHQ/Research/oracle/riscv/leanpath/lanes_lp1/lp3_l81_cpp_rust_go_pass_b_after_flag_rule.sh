#!/bin/bash
# lp3_l81_cpp_rust_go_pass_b_after_flag_rule.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.system.pass_b_build over cpp,
# rust and go: every arm of every certified pure form is rendered from that
# language's `operator_for` and from nothing else; each emulation is compiled
# at the corpus's ship flags, cut out at its symbol, decoded by Sail's own
# decoder, its meaning composed from Sail's definitions and certified (the
# walk); then proved equal to a definition (equals); then the eye table.
# Fetches nothing.
#
# WHY THIS RUNS: THE FLAG RULE, second half. `render.definitions_of` takes a
# definition's arms by the same rule the candidate reader now uses -- a pure
# form read at every value of its non-register parameters -- so a definition
# whose operation IS a flag has arms at all (75 arms -> 93). The l72/l75
# renders these replace were written from tables that held no integer-level
# operation (cpp 13 rendered, rust 17, go 3). This render is from the l80
# tables.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
L=$P/$PLIB
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
OP=PseudoCoupHQ/Research/op_pipeline
cd $A; T0=$(date +%s); i=0
for lang in cpp rust go; do
  i=$((i+1)); R=$A/runs/corpus_$lang
  echo "[$i/3] $lang 1/4: render every arm of every definition from operator_for only  ($(( $(date +%s) - T0 ))s)"
  rm -rf $R/pass_b; mkdir -p $R/pass_b
  python3 -u -m leanpath render $L $S $R/operator_for/operator_for.json $R/units.json $R/pass_b $lang > $R/pass_b/render.log 2>&1
  grep -E "keys usable|render:|Traceback" $R/pass_b/render.log
  python3 $OP/check_no_spelling_keys.py $R/pass_b/render.json 2>&1 | tail -1
  n=$(python3 -c "import json; print(len(json.load(open('$R/pass_b/units.json'))))" 2>/dev/null || echo 0)
  echo "[$i/3] $lang 2/4: lower, decode, compose, certify ($n emulations)  ($(( $(date +%s) - T0 ))s)"
  if [ "$n" -gt 0 ]; then
    export WALK_JOBS=2 WALK_MAX_WORDS=400
    python3 -u -m leanpath walk $P $X $PLIB $S $R/pass_b/units.json $R/pass_b/walk 600 > $R/pass_b/walk.log 2>&1
    grep -E "decode:|walk:|Traceback" $R/pass_b/walk.log | cut -c1-200
    echo "[$i/3] $lang 3/4: prove each equal to a definition  ($(( $(date +%s) - T0 ))s)"
    export EQUALS_UNIT_BUDGET_S=150 EQUALS_CHUNK=12
    python3 -u -m leanpath equals $P $PLIB $S $R/pass_b/walk/walk.json $R/pass_b/equals 120 64 > $R/pass_b/equals.log 2>&1
    echo "  proved: $(grep -c PROVED $R/pass_b/equals.log)"
  fi
  echo "[$i/3] $lang 4/4: the eye table  ($(( $(date +%s) - T0 ))s)"
  python3 -m leanpath eye_check $R/pass_b/render.json $R/pass_b/walk/walk.json $R/pass_b/equals/equals.json > $R/pass_b/eye_table.md 2>&1
  grep -E "^Rendered" $R/pass_b/eye_table.md
  echo "  rows proved: $(grep -c 'PROVED equal' $R/pass_b/eye_table.md)"
  grep -E "PROVED equal" $R/pass_b/eye_table.md | cut -c1-120
done
echo "wall seconds=$(( $(date +%s) - T0 ))"
echo done
