#!/bin/bash
# lp3_l82_gate_with_the_width_rule_by_use.sh -- THE GATE before any long run
# (the owner, 2026-09-15: a small run whose table is read before any wide run): a
# dozen of c's compiler-operators through EVERY stage of the plan, ending in
# the eye table:
#   compiler_corpus -> compile, decode, compose, certify (the meanings)
#   -> operator_for (subterms of Sail's definitions proved against them,
#      each key now carrying the widths its own text reads its operands at)
#   -> render (every arm of every definition, from that table only)
#   -> compile, decode, compose, certify the rendered emulations
#   -> equals (each proved equal to a definition) -> the eye table.
#
# WHY THIS RUNS: THE WIDTH RULE BY THE DEFINITION'S OWN USE (the owner, 2026-09-15).
# The rule as it stood demanded 64-bit holders for EVERY key, because a
# definition's operands are register reads. That is wrong for the W forms: their
# text reads only the low 32 bits of each register (`extractLsb x 31 0`) and
# sign-extends a 32-bit result, so the width they use of each read is 32, and
# the arch-units equal to them are held at 32-bit holders. Log 284 §10 recorded
# eight such keys of c and cpp proved into the table and refused at render, and
# left the width question open; this is its answer.
#
# THE RULE: a definition's operand width, PER READ, is the width the
# definition's own subterm uses of that read, read off the subterm's own text --
# a read sliced from bit 0 by literal bounds is used at the slice's width, a read
# used whole is used at the register's width, a read used both ways is used
# whole. A slice whose high bound is written in the architecture's own
# parameters is not a width read off the expression (it scales with the
# register: it is the operation's own use of a whole register), so the 64-bit
# shifts keep 64. `operator_for` records the widths beside each key when the key
# is built; `render` takes an arch-unit for a key when the arch-unit's holder
# widths EQUAL them. Result widths need no rule: a definition's result is the
# register.
#
# EXPECTED: the W-form definitions render from 32-bit-holder arch-units, lower
# to the one instruction each definition names, and prove by the same text; the
# 64-bit keys of the dozen keep rendering exactly as before.
#
# Nothing here selects by an operator token: the dozen is the first unit of each
# distinct certified MEANING among the c units whose holders are all one width,
# ordered so that the meanings naming a definition THE WIDTH RULE ITSELF reads
# narrower than the register come first. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
L=$P/$PLIB
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
OP=PseudoCoupHQ/Research/op_pipeline
G=$A/runs/gate_c_widths
cd $A; rm -rf $G; mkdir -p $G; t0=$(date +%s)
echo "[1/6] the dozen: one unit per distinct meaning, holders all one width, the narrow-read definitions first"
python3 - <<'PY'
import json, glob, re, sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/leanpath")
from leanpath import strip as ST, lean_tree as LZ
from leanpath.operator_for import (substitute, rename_reads, operand_widths,
                                   UNKNOWNS, REGISTER_WIDTH)
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
G = A + "/runs/gate_c_widths"
lean_dir = A + "/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM"
strip_rows = {r["clause"][len("execute_"):]: r
              for r in json.load(open(A + "/strip_6266b40c_8eb1fb6b_all_v5/strip.json"))["rows"]}
# the definitions the WIDTH RULE reads narrower than the register: the rule applied to
# the definition's own text, by the same function operator_for keys its candidates with
narrow = {}
for c in ST.clauses_of(lean_dir):
    name = c["name"][len("execute_"):]
    r = strip_rows.get(name)
    if not r or r.get("verdict") != "CERTIFIED" or r.get("shape") != "straight":
        continue
    p = ST.propose(c)
    reg_of = {v: reg for v, reg in p.get("reads", [])}
    order = []
    for _, reg in p.get("reads", []):
        if reg not in order:
            order.append(reg)
    env = {}
    try:
        for ln, text in p.get("lets", []):
            env[ln.split(":")[0].strip()] = substitute(LZ.parse(text), env)
        root = substitute(LZ.parse(p["value"]), env)
    except Exception:
        continue
    if not order or len(order) > len(UNKNOWNS):
        continue
    w = operand_widths(rename_reads(root, order, reg_of), len(order))
    if any(x != REGISTER_WIDTH for x in w):
        narrow[name] = w
print("  definitions the width rule reads narrower than the register: %d  (%s)" % (
    len(narrow), ", ".join("%s %s" % (k, v) for k, v in sorted(narrow.items()))))
meaning = {}
for p in sorted(glob.glob(A + "/runs/handful_c/walk_[0-3]/walk.json")):
    for r in json.load(open(p))["rows"]:
        if r["verdict"] == "CERTIFIED":
            meaning[r["unit"]] = r["proposal"]
units = json.load(open(A + "/runs/handful_c/units.json"))
norm = lambda s: re.sub(r"\s+", " ", s)
groups = {}
for u in sorted(units, key=lambda u: u["probe"]["n"]):
    F, h = meaning.get(u["name"]), (u.get("holders") or [])
    if F is None or len(h) < 2 or len(set(h)) != 1:
        continue
    groups.setdefault(norm(F), u)
is_narrow = lambda F: bool(set(re.findall(r"pure_(\w+)", F)) & set(narrow))
nar = [(F, u) for F, u in groups.items() if is_narrow(F)]
who = [(F, u) for F, u in groups.items() if not is_narrow(F)]
print("  distinct meanings over units held at one width: %d naming a narrow-read definition, %d naming a whole-read one" % (len(nar), len(who)))
dozen = [u for _, u in nar[:8]] + [u for _, u in who if u.get("holders") == [64, 64]][:4]
json.dump(dozen, open(G + "/units.json", "w"), indent=1)
for u in dozen:
    print("   %-12s %-24s %-9s %s" % (u["name"], u["probe"]["lhs_type"] + ", " + u["probe"]["rhs_type"],
                                      u["holders"], norm(meaning[u["name"]])[:80]))
PY
python3 $OP/check_no_spelling_keys.py $G/units.json 2>&1 | tail -1
echo "[2/6] their meanings: compile, decode, compose, certify  ($(( $(date +%s) - t0 ))s)"
export WALK_JOBS=4 WALK_MAX_WORDS=400
python3 -u -m leanpath walk $P $X $PLIB $S $G/units.json $G/walk 600 > $G/walk.log 2>&1
grep -E "CERTIFIED|REFUSED|FAILED" $G/walk.log | cut -c1-150
echo "[3/6] operator_for: subterms of Sail's definitions proved against them, each key with its own operand widths  ($(( $(date +%s) - t0 ))s)"
export EQUALS_UNIT_BUDGET_S=180 EQUALS_CHUNK=12 EVAL_UNITS=40
python3 -u -m leanpath operator_for $P $PLIB $S $G/walk/walk.json $G/operator_for 150 > $G/operator_for.log 2>&1
grep -E "candidates:|typed by|constant|evaluation of|operator_for:|Traceback" $G/operator_for.log | cut -c1-200
python3 $OP/check_no_spelling_keys.py $G/operator_for/operator_for.json 2>&1 | tail -1
python3 - <<'PY'
import json
G = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_c_widths"
j = json.load(open(G + "/operator_for/operator_for.json"))
print("  summary:", json.dumps(j["summary"]))
print("  %-10s %-44s %-5s %-4s %s" % ("unit", "meaning", "eval", "surv", "the subterm it proved"))
for r in j["rows"]:
    m = r["matches"][0] if r["matches"] else None
    print("  %-10s %-44s %-5s %-4s %s" % (r["unit"], r["F"][:44], r.get("evaluated"),
          r.get("survived_evaluation"), (m["G"][:66] + "  [" + m["stage"] + "]") if m else "-"))
print("  the table, key by key: the widths the key reads its operands at, and the holders its units are held at")
for Gk, es in sorted(j["table"].items()):
    print("   at %-10s held at %-26s %s" % (
        str(j["operand_widths"].get(Gk)),
        ", ".join(sorted({str(e.get("holders")) for e in es})), Gk[:92]))
PY
echo "[4/6] render every arm of every definition from that table only  ($(( $(date +%s) - t0 ))s)"
mkdir -p $G/pass_b
python3 -u -m leanpath render $L $S $G/operator_for/operator_for.json $G/units.json $G/pass_b c > $G/pass_b/render.log 2>&1
grep -E "keys usable|    at |render:" $G/pass_b/render.log | cut -c1-140
grep -vE "keys usable|    at |render:" $G/pass_b/render.log | grep -vE "REFUSED  no key" | cut -c1-150 | head -24
python3 $OP/check_no_spelling_keys.py $G/pass_b/render.json 2>&1 | tail -1
echo "[5/6] the emulations: compile, decode, compose, certify; then prove each equal to a definition  ($(( $(date +%s) - t0 ))s)"
n=$(python3 -c "import json; print(len(json.load(open('$G/pass_b/units.json'))))")
if [ "$n" -gt 0 ]; then
  python3 -u -m leanpath walk $P $X $PLIB $S $G/pass_b/units.json $G/pass_b/walk 600 > $G/pass_b/walk.log 2>&1
  grep -E "CERTIFIED|REFUSED|FAILED" $G/pass_b/walk.log | cut -c1-150
  python3 -u -m leanpath equals $P $PLIB $S $G/pass_b/walk/walk.json $G/pass_b/equals 150 64 > $G/pass_b/equals.log 2>&1
  grep -E "PROVED|Traceback" $G/pass_b/equals.log | cut -c1-150 | head -24
else
  echo "  no emulation rendered: the table has no key the definitions use at this size"
fi
echo "[6/6] the eye table  ($(( $(date +%s) - t0 ))s)"
python3 -m leanpath eye_check $G/pass_b/render.json $G/pass_b/walk/walk.json $G/pass_b/equals/equals.json > $G/eye_table.md 2>&1
head -40 $G/eye_table.md | cut -c1-300
echo "gate wall seconds=$(( $(date +%s) - t0 ))"
echo done
