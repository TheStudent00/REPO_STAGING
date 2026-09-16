#!/bin/bash
# lp3_l83_c_corpus_operator_for_width_rule_by_use.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.system.pass_a_find, step 2,
# over c's compiler_corpus: the candidates are the subterms of Sail's own
# certified pure forms over their register reads, typed by Lean; every
# certified arch-unit of the c walk is proved against every candidate of its
# arity by the same stages as `equals`; EVERY proved pair is an entry of
# Language.operator_for, carrying the unit's holder widths AND, beside the key,
# the widths the key's own text reads its operands at. Fetches nothing.
#
# WHY THIS RUNS: THE WIDTH RULE BY THE DEFINITION'S OWN USE (the owner, 2026-09-15),
# over ALL of c, after the gate (l82) was read. The l78 table (23 keys, 163
# entries) is proved by the same candidates and the same stages; what it lacks
# is the widths each key reads its operands at, which `render` now compares a
# unit's holders against instead of against 64. A read sliced from bit 0 by
# literal bounds is used at the slice's width (the W forms: 32), a read used
# whole at the register's width (64). This lane rewrites the c table of record
# with those widths beside every key, so the render that follows (l84) and any
# reader of the table see the rule's input, not only its outcome.
#
# Nothing here is keyed by an instruction name or an operator token.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
OP=PseudoCoupHQ/Research/op_pipeline
R=$A/runs/handful_c
cd $A
echo "[1/2] operator_for over every certified c arch-unit, each key with its own operand widths"
export EQUALS_UNIT_BUDGET_S=120 EQUALS_CHUNK=12 EVAL_UNITS=40; rm -rf $R/operator_for; start=$(date +%s)
python3 -u -m leanpath operator_for $P $PLIB $S $R/walk_0/walk.json,$R/walk_1/walk.json,$R/walk_2/walk.json,$R/walk_3/walk.json $R/operator_for 120 > $R/operator_for.log 2>&1
echo "  rc=$? wall seconds=$(( $(date +%s) - start ))"
grep -E "candidates:|typed by|units with|operator_for:|Traceback|Error" $R/operator_for.log | cut -c1-220
echo "[2/2] the table, and the spelling guard"
python3 $OP/check_no_spelling_keys.py $R/operator_for/operator_for.json 2>&1 | tail -1
python3 - <<'PY'
import json
R = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/operator_for"
try:
    j = json.load(open(R + "/operator_for.json"))
    print("  summary:", json.dumps(j["summary"]))
    for G, us in sorted(j["table"].items(), key=lambda kv: -len(kv[1])):
        w = j["operand_widths"].get(G)
        fit = sum(1 for u in us if u.get("holders") == w)
        print("  at %-9s %3d units (%d at those widths)  %s" % (str(w), len(us), fit, G[:96]))
except Exception as e:
    print("  no table:", e)
PY
echo done
