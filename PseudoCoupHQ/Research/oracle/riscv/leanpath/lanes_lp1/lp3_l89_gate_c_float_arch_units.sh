#!/bin/bash
# lp3_l89_gate_c_float_arch_units.sh -- THE GATE for the float arch-units (the owner, 2026-09-15:
# a small run whose table is read before anything wider; nothing wider runs after it): a
# dozen c arch-units containing float arch-opcodes, walked against the WORKING COPY of the
# emit (/work/proof_float, built by lane l88 with 27 float axioms given their Kinds.lean bodies).
#
# WHY: the walk of the c corpus (runs/handful_c) refused 248 units with "no certified pure form
# for ILLEGAL". This lane measures what is true now that (a) the 27 operations have bodies,
# (b) the effects rule reads the float clauses that call them (strip.propose_effects, its 12
# certificates checked one file at a time with a negative control), and (c) the walk takes
# float arguments and a float answer (walk.compose_effects).
#
# Nothing is selected by an operator token. The clauses are found by their bodies calling one
# of the operations with a body. The dozen: refused by the old walk because Sail's decoder
# answered ILLEGAL for a word, both holders float holders (a representation every compiled
# two-holder unit of which was refused that way), ordered by probe number, by stride. The
# measurement in step 5 names no instruction: the clause names come from the strip record.
# Fetches nothing. Writes runs/gate_c_floats.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof_float; X=/work/Lean_IM_pr_exec; PLIB=LeanIM
S5=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
OP=PseudoCoupHQ/Research/op_pipeline
G=$A/runs/gate_c_floats
cd $A; rm -rf $G; mkdir -p $G; t0=$(date +%s)
[ -f $P/.lake/build/lib/lean/LeanIM/RiscvExtras.olean ] || { echo "FLAG: the working copy is not built (lane l88)"; exit 3; }

echo "[1/6] the strip record of the float clauses in the working copy, merged over the corpus record  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import re, sys
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
sys.path.insert(0, A)
from leanpath import strip as ST
cache = A + "/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/LeanIM"
kinds = open(A + "/lp1_harness/leanpath_src/Kinds.lean").read()
bodies = re.findall(r"^def\s+(riscv_\w+)\s*:", re.search(r"^namespace Axioms\s*$(.*?)^end Axioms", kinds, re.S | re.M).group(1), re.M)
axioms = set(re.findall(r"^axiom\s+(\w+)\s*:", open(cache + "/RiscvExtras.lean").read(), re.M))
pat = re.compile(r"(?<![\w'])(" + "|".join(b for b in bodies if b in axioms) + r")(?![\w'])")
only = {c["name"] for c in ST.clauses_of(cache) if pat.search("\n".join(c["body"]))}
print("  clauses whose bodies call one of the operations with a body: %d" % len(only), flush=True)
ST.run("/work/proof_float", "LeanIM", A + "/runs/gate_c_floats/strip_float", 900, only)
PY
python3 $A/float_emit/gate_floats.py merge --base $S5 --new $G/strip_float/strip.json --out $G/strip_merged.json

echo "[2/6] the dozen, by rule over data  ($(( $(date +%s) - t0 ))s)"
python3 $A/float_emit/gate_floats.py select --units $A/runs/handful_c/units.json \
  --walk "$A/runs/handful_c/walk_[0-3]/walk.json" --out $G/units.json
python3 $OP/check_no_spelling_keys.py $G/units.json 2>&1 | tail -1

echo "[3/6] the walk: Sail's decoder, compose with the pure forms, certify in the working copy  ($(( $(date +%s) - t0 ))s)"
export WALK_JOBS=4 WALK_MAX_WORDS=400
python3 -u -m leanpath walk $P $X $PLIB $G/strip_merged.json $G/units.json $G/walk 600 > $G/walk.log 2>&1
grep -E "decode:|no-effect|CERTIFIED|REFUSED|FAILED|walk:|Traceback" $G/walk.log | cut -c1-200
python3 $OP/check_no_spelling_keys.py $G/walk/walk.json 2>&1 | tail -1

echo "[4/6] the eye table  ($(( $(date +%s) - t0 ))s)"
python3 $A/float_emit/gate_floats.py table --units $G/units.json --old-walk "$A/runs/handful_c/walk_[0-3]/walk.json" \
  --new-walk $G/walk/walk.json --out $G/eye_table.md | cut -c1-400

echo "[5/6] what decoding a float word needs, measured  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, re
A = "PseudoCoupHQ/Research/oracle/riscv/leanpath"
rows = [r for r in json.load(open(A + "/runs/gate_c_floats/strip_float/strip.json"))["rows"] if r["verdict"] == "CERTIFIED"]
names = [r["clause"][len("execute_"):] for r in rows]
for label, d in (("the evaluable build the walk decodes with", "/work/Lean_IM_pr_exec/LeanIMPrExecutable"),
                 ("the working copy (the whole emit)", "/work/proof_float/LeanIM")):
    t = open(d + "/InstsEnd.lean").read().split("\n")
    start = next(i for i, ln in enumerate(t) if re.match(r"^(noncomputable )?def encdec_backwards ", ln))
    end = next(i for i in range(start + 1, len(t)) if t[i].strip() == "")
    defs = open(d + "/Defs.lean").read()
    m = re.search(r"^inductive instruction where(.*?)(?=^\s*deriving|^\S)", defs, re.S | re.M)
    ctors = set(re.findall(r"\|\s*(\w+)", m.group(1))) if m else set()
    print("  %-44s decoder lines %6d; instruction constructors %4d; of the %d certified float clauses' constructors, present: %d"
          % (label, end - start, len(ctors), len(names), sum(n in ctors for n in names)))
PY
grep -E "Built LeanIMPrExecutable\.InstsEnd " /work/lake_pr.log 2>/dev/null | head -1 | sed 's/^/  the evaluable build compiling its instructions module, from its own build log: /'

echo "[6/6] two certificates of the record, and what Lean says they depend on in the rebuilt copy  ($(( $(date +%s) - t0 ))s)"
for f in $(python3 -c "import json; r=[x['lean_file'] for x in json.load(open('$G/strip_float/strip.json'))['rows'] if x.get('shape')=='effects']; print(r[0], r[-1])"); do
  python3 $A/float_emit/negative_control.py $f 2>&1 | cut -c1-200 | head -16
done
echo "gate wall seconds=$(( $(date +%s) - t0 ))"
echo done
