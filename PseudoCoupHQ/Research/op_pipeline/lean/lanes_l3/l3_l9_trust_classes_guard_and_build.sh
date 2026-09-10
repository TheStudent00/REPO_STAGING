#!/bin/bash
# l3 lane 9 -- the closing checks over the artifact as this task leaves it:
# the stronger-class attempt re-run against the FINAL check_L2.json, the axiom
# set of every proved row, `lake build` of the whole project, the sorry
# keyword, and the spelling-ban guard over every json this task wrote.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/l3home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/6] the stronger-class attempt, over the final check_L2.json"
python3 - <<'PY'
import json, os, resource, sys
sys.path.insert(0, 'PseudoCoupHQ/Research/op_pipeline/lean')
sys.path.insert(0, 'PseudoCoupHQ/Research/op_pipeline')
import model_translate as M
HERE = 'PseudoCoupHQ/Research/op_pipeline/lean'
CEIL = 6 * 1024 * 1024
def guard(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > CEIL:
        raise SystemExit("ABORT_MEMORY_L3: peak %d kB passed the stated "
                         "ceiling %d kB at %s" % (peak, CEIL, where))
    return peak
after = json.load(open(os.path.join(HERE, 'check_L2.json')))
before = json.load(open(os.path.join(HERE, 'check_L2.json.before_task_l3')))
before_by = dict((r['theorem_name'], r) for r in before['rows']
                 if r.get('theorem_name'))
proved = [r for r in after['rows'] if r.get('closed_by')]
native = [r for r in proved if 'ofReduceBool' in (r.get('axioms') or '')]
was_native = sorted(n for n, r in before_by.items()
                    if 'ofReduceBool' in (r.get('axioms') or ''))
print("   before: proved %d, native-evaluation axiom on %d"
      % (sum(1 for r in before['rows'] if r.get('closed_by')), len(was_native)))
print("   after : proved %d, native-evaluation axiom on %d"
      % (len(proved), len(native)))
scratch = os.path.join(HERE, 'archproof', 'Archproof', 'StrongClassTry.lean')
records = []
for index, row in enumerate(native, 1):
    tactic = M.tactic_for(row, "bv_decide").replace("bv_decide", "bv_normalize")
    label = ("%s single-opcode row %d, arch mnemonic %r, example unit %s, "
             "%d members -- the stronger-class attempt"
             % (row["lang"], row["row_index"], row["mnem"], row["unit"],
                row["member_count"]))
    handle = open(scratch, 'w')
    handle.write(M.theorem_text(label, "StrongClassTry", row, tactic))
    handle.close()
    result = M.lean_once(scratch)
    outcome, detail = M.classify(result)
    axioms = M.axiom_line(result["output"]) if outcome == "PROVED" else None
    stronger = bool(outcome == "PROVED" and axioms
                    and 'ofReduceBool' not in axioms)
    records.append({
        "theorem_name": row["theorem_name"], "unit": row["unit"],
        "lang": row["lang"], "mnem": row["mnem"],
        "row_index": row["row_index"],
        "was_native_before_task_l3": row["theorem_name"] in set(was_native),
        "bv_decide": {"closed_by": row.get("closed_by"),
                      "wall_seconds": row.get("wall_seconds"),
                      "peak_kb": row.get("peak_kb"),
                      "axioms": row.get("axioms")},
        "bv_normalize_attempt": {
            "outcome": outcome, "detail": detail,
            "wall_seconds": result["wall_seconds"],
            "peak_kb": result["peak_kb"], "axioms": axioms,
            "tactic": tactic, "lean_output": result["output"][:1200]},
        "moved_to_the_stronger_class": stronger})
    guard(row["theorem_name"])
moved = [r for r in records if r["moved_to_the_stronger_class"]]
print("   attempted %d; moved to the stronger class %d; kept bv_decide %d"
      % (len(records), len(moved), len(records) - len(moved)))
print("   attempts wall %.1f s total, highest peak RSS %d kB"
      % (sum(r["bv_normalize_attempt"]["wall_seconds"] for r in records),
         max(r["bv_normalize_attempt"]["peak_kb"] for r in records)))
handle = open(os.path.join(HERE, 'l3_trust_classes.json'), 'w')
json.dump({"what": "the trust class of every proved row of the check, and "
                   "the attempt to close the rows carrying the "
                   "native-evaluation axiom without calling the SAT solver",
           "before_file": "check_L2.json.before_task_l3",
           "rows_carrying_ofReduceBool_before": was_native,
           "rows_carrying_ofReduceBool_after":
               sorted(r['theorem_name'] for r in native),
           "attempts": records}, handle, indent=1, sort_keys=True)
handle.close()
handle = open(scratch, 'w')
handle.write("/- Scratch.  Task l3 wrote ONE stronger-class attempt at a "
             "time into this\n   file and read `lean`'s answer; the record "
             "of all of them is\n   l3_trust_classes.json.  Nothing "
             "depends on this file. -/\n")
handle.close()
print("   wrote l3_trust_classes.json; the scratch theorem file is emptied "
      "to a comment")
print("   peak RSS %d kB" % guard('end'))
PY
echo "--- exit $?"

echo "[2/6] the axiom set of every proved row, after this task"
python3 -c "
import collections, json, re
d = json.load(open('$LEANDIR/check_L2.json'))
proved = [r for r in d['rows'] if r.get('closed_by')]
print('   proved %d   missing axioms %d   sorryAx %d'
      % (len(proved), sum(1 for r in proved if not r.get('axioms')),
         sum(1 for r in proved if 'sorryAx' in (r.get('axioms') or ''))))
pats = collections.Counter()
for r in proved:
    a = re.sub(chr(39) + '[^' + chr(39) + ']+' + chr(39), 'THEOREM', r['axioms'])
    pats[(r['closed_by'], a)] += 1
for k in sorted(pats, key=str):
    print('   %4d  %s' % (pats[k], k))
"

echo "[3/6] lake build, whole project"
cd archproof || exit 1
lake build 2>&1 | tail -5
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1

echo "[4/6] the sorry keyword, whole project"
grep -rln "sorry" \
  PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof/*.lean \
  PseudoCoupHQ/Research/op_pipeline/lean/archproof/Edges/*.lean \
  PseudoCoupHQ/Research/op_pipeline/lean/archproof/Main.lean \
  PseudoCoupHQ/Research/op_pipeline/lean/archproof/Archproof.lean
echo "(grep exit $? -- 1 means no file matched)"

echo "[5/6] the spelling-ban guard, unmodified, over every json this task wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/op_pipeline/lean/check_L2.json \
    PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json \
    PseudoCoupHQ/Research/op_pipeline/lean/model_L2.json 2>&1 \
  | grep -E "^(FAIL|PASS)"

echo "[6/6] grep -c exempt over every file this task added"
grep -c exempt \
  PseudoCoupHQ/Research/op_pipeline/lean/l3_trust_classes.json \
  PseudoCoupHQ/Research/op_pipeline/lean/lanes_l3/*.sh
echo "--- exit $?"
