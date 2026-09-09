#!/bin/bash
# L2 lane 19 -- the close-out verification, over the FINAL state of
# check_L2.json (after lanes 14/16/18 filled and corrected every proved
# theorem's `axioms` line):
#   [1/5] `lake build` of the whole project (Archproof.lean imports every
#         CLOSED module -- lane 14's `imports` run already wrote that;
#         this confirms the build is still exit 0 after lanes 16/18 only
#         touched check_L2.json, not any .lean file)
#   [2/5] the `sorry` keyword, whole project -- `sorryAx` in `#print axioms`
#         output can only exist if a `sorry` term/tactic exists somewhere
#   [3/5] the spelling-ban guard (check_no_spelling_keys.py, unmodified)
#         over every json this task wrote
#   [4/5] `grep -c exempt` over every file this task added
#   [5/5] the final tally over check_L2.json's rows, and the axioms-line
#         shape distribution
set -u

TOTAL=5
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
PIPE=/projects/PseudoCoupHQ/Research/op_pipeline
export HOME=/work/L2home
mkdir -p "$HOME"

echo "[1/$TOTAL] lake build (whole project)"
cd "$LEANDIR/archproof" || exit 1
time lake build
echo "--- lake build exit $?"

echo "[2/$TOTAL] sorry keyword, whole project"
cd "$LEANDIR" || exit 1
grep -rn "\bsorry\b" archproof/Archproof/*.lean archproof/Edges/*.lean \
    archproof/Main.lean archproof/Archproof.lean
echo "--- grep exit $? (1 = no match = no sorry anywhere = no sorryAx possible)"

echo "[3/$TOTAL] the spelling-ban guard over every json this task wrote"
python3 "$PIPE/check_no_spelling_keys.py" \
    "$LEANDIR/model_L2.json" "$LEANDIR/check_L2.json"
echo "--- guard exit $?"

echo "[4/$TOTAL] grep -c exempt over every file this task added"
grep -c exempt "$LEANDIR/model_L2.json" "$LEANDIR/check_L2.json" \
    "$LEANDIR/model_translate.py" \
    "$LEANDIR"/archproof/Archproof/Model.lean \
    "$LEANDIR"/archproof/Archproof/ModelCheck_*.lean \
    | awk -F: '{s+=$2} END {print "total exempt occurrences:", s+0}'

echo "[5/$TOTAL] final tally + axioms shape distribution"
python3 - <<'PY'
import json, re, collections
d = json.load(open("check_L2.json"))
rows = d["rows"]
tally = collections.Counter()
for r in rows:
    key = r.get("closed_by") or r.get("outcome")
    tally[key] += 1
for k in sorted(tally, key=str):
    print("  %-24s %d" % (k, tally[k]))
proved = [r for r in rows if r.get("closed_by")]
print("proved total:", len(proved))
print("missing axioms:", sum(1 for r in proved if not r.get("axioms")))
print("sorryAx count:", sum(1 for r in proved if "sorryAx" in (r.get("axioms") or "")))
pats = collections.Counter()
for r in proved:
    a2 = re.sub(r"'[^']+'", "THEOREM", r["axioms"])
    pats[a2] += 1
for k, v in pats.most_common():
    print(" ", v, k)
PY
echo "--- exit $?"
