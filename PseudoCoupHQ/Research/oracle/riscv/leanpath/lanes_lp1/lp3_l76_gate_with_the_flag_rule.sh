#!/bin/bash
# lp3_l76_gate_with_the_flag_rule.sh -- THE GATE before any long run
# (the owner, 2026-09-15: verify on a small gate first): a dozen of c's
# compiler-operators through EVERY stage of the plan, ending in the eye table:
#   compiler_corpus -> compile, decode, compose, certify (the meanings)
#   -> operator_for (subterms of Sail's definitions proved against them)
#   -> render (every arm of every definition, from that table only)
#   -> compile, decode, compose, certify the rendered emulations
#   -> equals (each proved equal to a definition) -> the eye table.
#
# l76: the gate WITH THE FLAG RULE. In l73 the multiply, divide and remainder
# units matched nothing because the candidate set held no such subterm at all:
# every subterm of `pure_DIV`/`pure_REM` still named `is_unsigned`, and
# `pure_MUL`'s one subterm named `mul_op` through its fields, which Lean
# refused at typing ("the argument mul_op.signed_rs1 has type mul_op ->
# Signedness"). The rule now reads a pure form at EVERY value of its
# non-register parameters -- the same `enum_values` the definition side of
# `equals` uses -- folds the Booleans that makes literal, counts a field read
# `p.f` as a mention of `p`, orders a candidate's unknowns by the pure form's
# own read order (a divide guard tests the divisor first), and evaluates a
# width Lean prints as a name. `render` takes its arms by the same rule.
#
# Nothing here selects by an operator token: the dozen is the first unit of each
# distinct certified MEANING among the c units held at (64, 64) whose meaning
# names a pure form that takes a non-register parameter. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
L=$P/$PLIB
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
OP=PseudoCoupHQ/Research/op_pipeline
G=$A/runs/gate_c_flags
cd $A; rm -rf $G; mkdir -p $G; t0=$(date +%s)
echo "[1/6] the dozen: one unit per distinct meaning, held at (64, 64), whose meaning takes a non-register parameter"
python3 - <<'PY'
import json, glob, re, sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath import strip as ST
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
G = A + "/runs/gate_c_flags"
lean_dir = A + "/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM"
# the clauses whose pure form takes a parameter that is not a register read
flagged = {c["name"][len("execute_"):] for c in ST.clauses_of(lean_dir) if ST.propose(c).get("others")}
meaning = {}
for p in sorted(glob.glob(A + "/runs/handful_c/walk_[0-3]/walk.json")):
    for r in json.load(open(p))["rows"]:
        if r["verdict"] == "CERTIFIED":
            meaning[r["unit"]] = r["proposal"]
units = json.load(open(A + "/runs/handful_c/units.json"))
norm = lambda s: re.sub(r"\s+", " ", s)
groups = {}
for u in sorted(units, key=lambda u: u["probe"]["n"]):
    F = meaning.get(u["name"])
    if F is None or u.get("holders") != [64, 64]:
        continue
    if not (set(re.findall(r"pure_(\w+)", F)) & flagged):
        continue
    groups.setdefault(norm(F), u)
dozen = list(groups.values())[:12]
json.dump(dozen, open(G + "/units.json", "w"), indent=1)
print("  units held at (64, 64) with a flagged meaning: %d in %d distinct meanings -> the dozen:" % (
    sum(1 for u in units if u.get("holders") == [64, 64] and meaning.get(u["name"]) and
        set(re.findall(r"pure_(\w+)", meaning[u["name"]])) & flagged), len(groups)))
for u in dozen:
    print("   %-12s %-34s %s" % (u["name"], u["probe"]["operator"] + " (" + u["probe"]["lhs_type"] + ", " + u["probe"]["rhs_type"] + ")", norm(meaning[u["name"]])[:90]))
PY
python3 $OP/check_no_spelling_keys.py $G/units.json 2>&1 | tail -1
echo "[2/6] their meanings: compile, decode, compose, certify  ($(( $(date +%s) - t0 ))s)"
export WALK_JOBS=4 WALK_MAX_WORDS=400
python3 -u -m leanpath walk $P $X $PLIB $S $G/units.json $G/walk 600 > $G/walk.log 2>&1
grep -E "CERTIFIED|REFUSED|FAILED" $G/walk.log | cut -c1-150
echo "[3/6] operator_for: subterms of Sail's definitions proved against them  ($(( $(date +%s) - t0 ))s)"
export EQUALS_UNIT_BUDGET_S=180 EQUALS_CHUNK=12 EVAL_UNITS=40
python3 -u -m leanpath operator_for $P $PLIB $S $G/walk/walk.json $G/operator_for 150 > $G/operator_for.log 2>&1
grep -E "candidates:|typed by|constant|evaluation of|matches:|operator_for:|Traceback" $G/operator_for.log | cut -c1-180
python3 $OP/check_no_spelling_keys.py $G/operator_for/operator_for.json 2>&1 | tail -1
python3 - <<'PY'
import json
G = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_c_flags"
j = json.load(open(G + "/operator_for/operator_for.json"))
print("  summary:", json.dumps(j["summary"]))
print("  %-12s %-52s %-4s %-4s %s" % ("unit", "meaning", "eval", "surv", "the subterm it proved"))
for r in j["rows"]:
    m = r["matches"][0] if r["matches"] else None
    print("  %-12s %-52s %-4s %-4s %s" % (r["unit"], r["F"][:52], r.get("evaluated"),
          r.get("survived_evaluation"), (m["G"][:70] + "  [" + m["stage"] + "]") if m else "-"))
PY
echo "[4/6] render every arm of every definition from that table only  ($(( $(date +%s) - t0 ))s)"
mkdir -p $G/pass_b
python3 -u -m leanpath render $L $S $G/operator_for/operator_for.json $G/units.json $G/pass_b c > $G/pass_b/render.log 2>&1
grep -E "keys usable|render:" $G/pass_b/render.log; grep -vE "REFUSED|keys usable|render:" $G/pass_b/render.log | cut -c1-140 | head -20
python3 $OP/check_no_spelling_keys.py $G/pass_b/render.json 2>&1 | tail -1
echo "[5/6] the emulations: compile, decode, compose, certify; then prove each equal to a definition  ($(( $(date +%s) - t0 ))s)"
n=$(python3 -c "import json; print(len(json.load(open('$G/pass_b/units.json'))))")
if [ "$n" -gt 0 ]; then
  python3 -u -m leanpath walk $P $X $PLIB $S $G/pass_b/units.json $G/pass_b/walk 600 > $G/pass_b/walk.log 2>&1
  grep -E "CERTIFIED|REFUSED|FAILED" $G/pass_b/walk.log | cut -c1-150
  python3 -u -m leanpath equals $P $PLIB $S $G/pass_b/walk/walk.json $G/pass_b/equals 150 64 > $G/pass_b/equals.log 2>&1
  grep -E "PROVED|Traceback" $G/pass_b/equals.log | cut -c1-150 | head -20
else
  echo "  no emulation rendered: the table has no key the definitions use at this size"
fi
echo "[6/6] the eye table  ($(( $(date +%s) - t0 ))s)"
python3 -m leanpath eye_check $G/pass_b/render.json $G/pass_b/walk/walk.json $G/pass_b/equals/equals.json > $G/eye_table.md 2>&1
head -40 $G/eye_table.md | cut -c1-300
echo "gate wall seconds=$(( $(date +%s) - t0 ))"
echo done
