#!/bin/bash
# L2 lane 22 -- lane 21's verifier pass found 3 DIFFERS, all caused by the
# checker's own fixed working directory (/projects/PseudoCoupHQ, stated in
# its own banner) versus this task's relative paths ('check_L2.json'), one
# REFUSED by a bare `>` inside python source that the checker's naive
# command-splitter read as a shell redirect, one REFUSED because `lake` is
# not on the checker's ALLOWED_HEADS list, and two NOT_RERUNNABLE (one from
# `cd`, which resolves through `shutil.which` to nothing since it is a
# builtin not a binary, so the checker calls it tool_absent; one from a
# `\"`-escaped python source string the checker's parser could not find the
# closing quote of, so it consumed the rest of the file as "still inside
# the command" and found no output after it). This lane runs the EXACT
# literal command text log_232 section 10 will carry after the fix --
# absolute paths, no bare `>`, no `cd`, no `lake`, no backslash-escaped
# quotes -- so the pasted output is byte-identical to what the checker's
# own re-run will produce.
set -u
TOTAL=6

echo "[1/$TOTAL] the translator's census (absolute path, no bare >)"
python3 -c '
import json
d = json.load(open("/projects/PseudoCoupHQ/Research/op_pipeline/lean/model_L2.json"))
pm = d["per_mnemonic"]
print("mnemonics_in_the_table", d["mnemonics_in_the_table"])
print("definitions", d["definitions"])
print("opaque_float_primitives", len(d["opaque_float_primitives"]))
no_builder = sorted(m for m, v in pm.items() if v["no_builder"])
nothing = sorted(m for m, v in pm.items() if not v["no_builder"] and not v["translated"])
translated = sorted(m for m, v in pm.items() if v["translated"])
print("no_builder", no_builder)
print("builder_but_nothing_translated", nothing)
print("translated_count", len(translated))
'
echo "--- exit $?"

echo "[2/$TOTAL] the check's outcome tally (absolute path)"
python3 -c '
import json, collections
d = json.load(open("/projects/PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"))
rows = d["rows"]
print("total_rows", len(rows))
tally = collections.Counter()
for r in rows:
    key = r.get("closed_by") or r.get("outcome")
    tally[key] += 1
for k in sorted(tally, key=str):
    print(" ", k, tally[k])
'
echo "--- exit $?"

echo "[3/$TOTAL] REFUSED by cause and mnemonic (absolute path)"
python3 -c '
import json, collections
d = json.load(open("/projects/PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"))
rows = [r for r in d["rows"] if r["outcome"] == "REFUSED"]
pm = collections.defaultdict(collections.Counter)
for r in rows:
    pm[r.get("cause")][r["mnem"]] += 1
for cause in sorted(pm):
    print(cause, dict(pm[cause]))
'
echo "--- exit $?"

echo "[4/$TOTAL] axioms-line shape distribution (absolute path, no escaped quotes)"
python3 -c '
import json, re, collections
d = json.load(open("/projects/PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json"))
proved = [r for r in d["rows"] if r.get("closed_by")]
print("proved_total", len(proved))
print("missing_axioms", sum(1 for r in proved if not r.get("axioms")))
print("sorryAx_count", sum(1 for r in proved if "sorryAx" in (r.get("axioms") or "")))
pats = collections.Counter()
for r in proved:
    a2 = re.sub(chr(39) + "[^" + chr(39) + "]+" + chr(39), "THEOREM", r["axioms"])
    pats[(r["closed_by"], a2)] += 1
for k in sorted(pats, key=str):
    print(" ", pats[k], k)
'
echo "--- exit $?"

echo "[5/$TOTAL] the sorry keyword, whole project (absolute paths, no cd)"
grep -rln "sorry" \
    /projects/PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof/*.lean \
    /projects/PseudoCoupHQ/Research/op_pipeline/lean/archproof/Edges/*.lean \
    /projects/PseudoCoupHQ/Research/op_pipeline/lean/archproof/Main.lean \
    /projects/PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof.lean
echo "--- grep exit $? (1 = no file matched = no sorry anywhere)"

echo "[6/$TOTAL] the spelling-ban guard (absolute paths both arguments)"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    /projects/PseudoCoupHQ/Research/op_pipeline/lean/model_L2.json \
    /projects/PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json 2>&1 \
    | grep -E "^(FAIL|PASS)"
echo "--- exit $?"
