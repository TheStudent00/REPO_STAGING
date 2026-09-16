#!/bin/bash
# lp3_l55_handful_c_operator_for_again.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.system.pass_a_find, step 2,
# over c's compiler_corpus: the candidates are the subterms of Sail's own
# certified pure forms over their register reads (136 of them), typed by
# Lean; every certified unit of the l52 walk is proved against every
# candidate of its arity by the same stages as `equals` (evaluation at
# sample inputs removes; same text, integer level, fixed width prove);
# EVERY proved pair is an entry of Language.operator_for. Fetches nothing.
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
cd $A
echo "[1/1] operator_for over c's corpus"
export EQUALS_UNIT_BUDGET_S=120 EQUALS_CHUNK=12 EVAL_UNITS=40; rm -rf $R/operator_for; start=$(date +%s)
python3 -u -m leanpath operator_for $P $PLIB $S $R/walk_0/walk.json,$R/walk_1/walk.json,$R/walk_2/walk.json,$R/walk_3/walk.json $R/operator_for 120 > $R/operator_for.log 2>&1
echo "  rc=$? wall seconds=$(( $(date +%s) - start ))"
grep -E "candidates:|typed by|units with|operator_for:|Traceback|Error" $R/operator_for.log | cut -c1-200
python3 - <<'PY'
import json
R="PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/operator_for"
try:
    j = json.load(open(R + "/operator_for.json"))
    print("  summary:", json.dumps(j["summary"]))
    for G, us in sorted(j["table"].items(), key=lambda kv: -len(kv[1]))[:20]:
        print("  %-60s %d units  e.g. %s" % (G[:60], len(us), ", ".join(u["unit"] for u in us[:4])))
except Exception as e:
    print("  no table:", e)
PY
echo done
