#!/bin/bash
# lp3_l71_cpp_rust_go_operator_for.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.system.pass_a_find, step 2,
# over c's compiler_corpus: the candidates are the subterms of Sail's own
# certified pure forms over their register reads (136 of them), typed by
# Lean; every certified unit of the l52 walk is proved against every
# candidate of its arity by the same stages as `equals` (evaluation at
# sample inputs removes; same text, integer level, fixed width prove);
# EVERY proved pair is an entry of Language.operator_for. Fetches nothing.
# l71: the swap table of cpp, rust and go, each over every certified unit of its corpus (l65).
# l63: the swap table over ALL 346 certified c units, after the gate (l62) showed every
# stage right with the width rule; the earlier full run (l56) found nothing because of the
# closed-goal defect in the proof stages, fixed since. Entries carry holder widths.
# l53 again: candidates typed by their INFERRED type (lean-sail coerces, so an
# expected type let a Nat and a 5-bit vector through and broke every evaluation);
# the evaluation in files of 40 units; provers only where a candidate survived.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
R=$A/runs/handful_c
cd $A; T0=$(date +%s)
export EQUALS_UNIT_BUDGET_S=120 EQUALS_CHUNK=12 EVAL_UNITS=40
for lang in cpp rust go; do
  R=$A/runs/corpus_$lang; rm -rf $R/operator_for
  echo "[$lang] operator_for over its certified units  ($(( $(date +%s) - T0 ))s)"
  python3 -u -m leanpath operator_for $P $PLIB $S $R/walk_0/walk.json,$R/walk_1/walk.json,$R/walk_2/walk.json,$R/walk_3/walk.json $R/operator_for 120 > $R/operator_for.log 2>&1
  grep -E "typed by|units with|evaluation over|operator_for:|Traceback" $R/operator_for.log | cut -c1-160
  python3 $A/../../../op_pipeline/check_no_spelling_keys.py $R/operator_for/operator_for.json 2>&1 | tail -1
done
echo "wall seconds=$(( $(date +%s) - T0 ))"
echo done
