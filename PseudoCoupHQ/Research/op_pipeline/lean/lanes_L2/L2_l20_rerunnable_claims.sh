#!/bin/bash
# L2 lane 20 -- the same facts the log's prose states, as commands the
# verifier can re-run and MATCH against the pasted output. Every command
# here reads a file already on disk (model_L2.json, check_L2.json) or is a
# deterministic re-run (model_translate.py five, lake build, grep, the
# guard) rather than a fresh lean-per-theorem timing pass, so wall-clock
# numbers that vary run to run are not pasted as claims.
set -u

TOTAL=8
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
PIPE=/projects/PseudoCoupHQ/Research/op_pipeline
export HOME=/work/L2home
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] the five opcodes, end to end (re-run, deterministic)"
python3 model_translate.py five
echo "--- exit $?"

echo "[2/$TOTAL] the translator's census over all 171 mnemonics"
python3 - <<'PY'
import json
d = json.load(open("model_L2.json"))
pm = d["per_mnemonic"]
print("mnemonics_in_the_table", d["mnemonics_in_the_table"])
print("definitions", d["definitions"])
print("opaque_float_primitives", len(d["opaque_float_primitives"]))
no_builder = sorted(m for m, v in pm.items() if v["no_builder"] > 0)
nothing = sorted(m for m, v in pm.items() if v["no_builder"] == 0 and v["translated"] == 0)
translated = sorted(m for m, v in pm.items() if v["translated"] > 0)
print("no_builder", no_builder)
print("builder_but_nothing_translated", nothing)
print("translated_count", len(translated))
PY
echo "--- exit $?"

echo "[3/$TOTAL] the check's outcome tally over the 259 rows"
python3 - <<'PY'
import json, collections
d = json.load(open("check_L2.json"))
rows = d["rows"]
print("total_rows", len(rows))
tally = collections.Counter()
for r in rows:
    key = r.get("closed_by") or r.get("outcome")
    tally[key] += 1
for k in sorted(tally, key=str):
    print(" ", k, tally[k])
PY
echo "--- exit $?"

echo "[4/$TOTAL] REFUSED, by cause and mnemonic"
python3 - <<'PY'
import json, collections
d = json.load(open("check_L2.json"))
rows = [r for r in d["rows"] if r["outcome"] == "REFUSED"]
pm = collections.defaultdict(collections.Counter)
for r in rows:
    pm[r.get("cause")][r["mnem"]] += 1
for cause in sorted(pm):
    print(cause, dict(pm[cause]))
PY
echo "--- exit $?"

echo "[5/$TOTAL] every DISCREPANCY row, LITERAL"
python3 - <<'PY'
import json
d = json.load(open("check_L2.json"))
rows = [r for r in d["rows"] if r["outcome"] == "DISCREPANCY"]
print("count", len(rows))
for r in rows:
    print(r["theorem_name"], r["mnem"], r["unit"])
    print("  left :", r["left"])
    print("  right:", r["right"])
PY
echo "--- exit $?"

echo "[6/$TOTAL] the axioms-line shape distribution over all 153 proved rows"
python3 - <<'PY'
import json, re, collections
d = json.load(open("check_L2.json"))
proved = [r for r in d["rows"] if r.get("closed_by")]
print("proved_total", len(proved))
print("missing_axioms", sum(1 for r in proved if not r.get("axioms")))
print("sorryAx_count", sum(1 for r in proved if "sorryAx" in (r.get("axioms") or "")))
pats = collections.Counter()
for r in proved:
    a2 = re.sub(r"'[^']+'", "THEOREM", r["axioms"])
    pats[(r["closed_by"], a2)] += 1
for k in sorted(pats, key=str):
    print(" ", pats[k], k)
PY
echo "--- exit $?"

echo "[7/$TOTAL] lake build (whole project) and the sorry keyword"
cd archproof || exit 1
lake build 2>&1 | tail -3
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1
grep -rln "\bsorry\b" archproof/Archproof/*.lean archproof/Edges/*.lean \
    archproof/Main.lean archproof/Archproof.lean
echo "--- grep exit $? (1 = no file matched = no sorry anywhere)"

echo "[8/$TOTAL] the spelling-ban guard over every json this task wrote"
python3 "$PIPE/check_no_spelling_keys.py" model_L2.json check_L2.json \
    2>&1 | grep -E "^(FAIL|PASS)"
echo "--- exit $?"
