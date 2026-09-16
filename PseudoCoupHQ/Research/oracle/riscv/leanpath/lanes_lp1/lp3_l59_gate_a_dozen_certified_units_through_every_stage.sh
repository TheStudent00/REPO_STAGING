#!/bin/bash
# lp3_l59_gate_a_dozen_certified_units_through_every_stage.sh -- THE GATE before any
# long run (the owner, 2026-09-15: "i want to verify before doing long runs"):
# twelve of c's compiler-operators, by stride through the manifest, through
# EVERY stage of the plan, ending in the eye table, in one short lane:
#   compiler_corpus -> compile, decode, compose, certify (the meanings)
#   -> operator_for (subterms of Sail's definitions proved against them)
#   -> render (every arm of every definition, from that table only)
#   -> compile, decode, compose, certify the rendered emulations
#   -> equals (each proved equal to a definition) -> the eye table.
# Nothing here selects by a name: the dozen is every 29th of the 346 c units whose
# meaning l52 certified, in manifest order (a stride over the raw manifest lands on
# float and refused probes and exercises nothing). Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
L=$P/$PLIB
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
OP=PseudoCoupHQ/Research/op_pipeline
G=$A/runs/gate_c
cd $A; rm -rf $G; mkdir -p $G; t0=$(date +%s)
echo "[1/6] the dozen: every 29th of the c units whose meaning l52 certified, in manifest order"
python3 - <<'PY'
import json, glob
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
G = A + "/runs/gate_c"
certified = set()
for p in glob.glob(A + "/runs/handful_c/walk_[0-3]/walk.json"):
    certified |= {r["unit"] for r in json.load(open(p))["rows"] if r["verdict"] == "CERTIFIED"}
units = [u for u in json.load(open(A + "/runs/handful_c/units.json")) if u["name"] in certified]
units.sort(key=lambda u: u["probe"]["n"])
dozen = units[::max(1, len(units) // 12)][:12]
json.dump(dozen, open(G + "/units.json", "w"), indent=1)
print("  certified units:", len(units), "-> the dozen:", ", ".join("%s(%s)" % (u["probe"]["operator"], u["probe"]["lhs_type"]) for u in dozen))
PY
python3 $OP/check_no_spelling_keys.py $G/units.json 2>&1 | tail -1
echo "[2/6] their meanings: compile, decode, compose, certify  ($(( $(date +%s) - t0 ))s)"
export WALK_JOBS=4 WALK_MAX_WORDS=400
python3 -u -m leanpath walk $P $X $PLIB $S $G/units.json $G/walk 600 > $G/walk.log 2>&1
grep -E "CERTIFIED|REFUSED|FAILED" $G/walk.log | cut -c1-150
echo "[3/6] operator_for: subterms of Sail's definitions proved against them  ($(( $(date +%s) - t0 ))s)"
export EQUALS_UNIT_BUDGET_S=120 EQUALS_CHUNK=12 EVAL_UNITS=40
python3 -u -m leanpath operator_for $P $PLIB $S $G/walk/walk.json $G/operator_for 120 > $G/operator_for.log 2>&1
grep -E "typed by|constant|evaluation of|matches:|operator_for:|Traceback" $G/operator_for.log | cut -c1-160
python3 $OP/check_no_spelling_keys.py $G/operator_for/operator_for.json 2>&1 | tail -1
echo "[4/6] render every arm of every definition from that table only  ($(( $(date +%s) - t0 ))s)"
mkdir -p $G/pass_b
python3 -u -m leanpath render $L $S $G/operator_for/operator_for.json $G/units.json $G/pass_b c > $G/pass_b/render.log 2>&1
grep -E "keys usable|render:" $G/pass_b/render.log; grep -vE "REFUSED|keys usable|render:" $G/pass_b/render.log | cut -c1-120 | head -12
python3 $OP/check_no_spelling_keys.py $G/pass_b/render.json 2>&1 | tail -1
echo "[5/6] the emulations: compile, decode, compose, certify; then prove each equal to a definition  ($(( $(date +%s) - t0 ))s)"
n=$(python3 -c "import json; print(len(json.load(open('$G/pass_b/units.json'))))")
if [ "$n" -gt 0 ]; then
  python3 -u -m leanpath walk $P $X $PLIB $S $G/pass_b/units.json $G/pass_b/walk 600 > $G/pass_b/walk.log 2>&1
  grep -E "CERTIFIED|REFUSED|FAILED" $G/pass_b/walk.log | cut -c1-150
  python3 -u -m leanpath equals $P $PLIB $S $G/pass_b/walk/walk.json $G/pass_b/equals 120 64 > $G/pass_b/equals.log 2>&1
  grep -E "PROVED|Traceback" $G/pass_b/equals.log | cut -c1-150 | head -12
else
  echo "  no emulation rendered: the table has no key the definitions use at this size"
fi
echo "[6/6] the eye table  ($(( $(date +%s) - t0 ))s)"
python3 -m leanpath eye_check $G/pass_b/render.json $G/pass_b/walk/walk.json $G/pass_b/equals/equals.json > $G/eye_table.md 2>&1
head -30 $G/eye_table.md | cut -c1-300
echo "gate wall seconds=$(( $(date +%s) - t0 ))"
echo done
