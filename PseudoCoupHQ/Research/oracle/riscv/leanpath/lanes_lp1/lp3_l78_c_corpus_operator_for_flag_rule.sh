#!/bin/bash
# lp3_l78_c_corpus_operator_for_flag_rule.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.system.pass_a_find, step 2,
# over c's compiler_corpus: the candidates are the subterms of Sail's own
# certified pure forms over their register reads, typed by Lean; every
# certified arch-unit of the c walk is proved against every candidate of its
# arity by the same stages as `equals` (evaluation at sample inputs removes;
# same text, integer level, fixed width prove); EVERY proved pair is an entry
# of Language.operator_for, carrying the unit's holder widths. Fetches nothing.
#
# WHY THIS RUNS: THE FLAG RULE. The l73 table (11 keys, 109 entries) had no
# multiply, divide or remainder subterm in it at all -- not because the proofs
# failed but because the candidate set never held one: `candidates_of_definitions`
# dropped every subterm whose free names still carried a non-register parameter
# of the pure form, and the one subterm that slipped through was refused by Lean
# at typing because a structure field read is a single identifier. The rule now
# reads a pure form at EVERY value of its non-register parameters (the same
# `enum_values` the definition side of `equals` already uses), folds the Booleans
# an assignment makes literal, counts a field read as a mention of its structure,
# orders a candidate's unknowns by the pure form's own read order, and evaluates
# a width Lean prints as a name; a `match` on a substituted constructor folds to
# its arm. Candidates 136 -> 186, of which 120 type exactly BitVec 64 in and out
# (was 97). The gate over a dozen c units (l76, l77) proved 10 keys / 10 entries
# including the multiply, the two divides and the two remainders, rendered 10
# emulations, lowered all 10 and proved all 10. This is that rule over ALL of c.
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
echo "[1/2] operator_for over every certified c arch-unit, with the flag rule"
export EQUALS_UNIT_BUDGET_S=120 EQUALS_CHUNK=12 EVAL_UNITS=40; rm -rf $R/operator_for; start=$(date +%s)
python3 -u -m leanpath operator_for $P $PLIB $S $R/walk_0/walk.json,$R/walk_1/walk.json,$R/walk_2/walk.json,$R/walk_3/walk.json $R/operator_for 120 > $R/operator_for.log 2>&1
echo "  rc=$? wall seconds=$(( $(date +%s) - start ))"
grep -E "candidates:|typed by|units with|operator_for:|Traceback|Error" $R/operator_for.log | cut -c1-200
echo "[2/2] the table, and the spelling guard"
python3 $OP/check_no_spelling_keys.py $R/operator_for/operator_for.json 2>&1 | tail -1
python3 - <<'PY'
import json
R = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c/operator_for"
try:
    j = json.load(open(R + "/operator_for.json"))
    print("  summary:", json.dumps(j["summary"]))
    for G, us in sorted(j["table"].items(), key=lambda kv: -len(kv[1])):
        at64 = sum(1 for u in us if u.get("holders") and all(h == 64 for h in u["holders"]))
        print("  %-84s %3d units (%d at 64)  e.g. %s" % (G[:84], len(us), at64, ", ".join(u["unit"] for u in us[:3])))
except Exception as e:
    print("  no table:", e)
PY
echo done
