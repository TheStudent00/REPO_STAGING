#!/bin/bash
# l3 lane 7 -- THE TRUST CLASS OF EVERY PROVED ROW, and an attempt to move the
# rows that carry the native-evaluation axiom into the stronger class.
#
# WHAT THE TWO CLASSES ARE, said before the run.  `bv_decide` bit-blasts the
# goal, hands the formula to a SAT solver, and turns the solver's LRAT
# certificate into a Lean proof term.  Reading that certificate back in is done
# by compiled code, which is admitted through the axiom `Lean.ofReduceBool`
# (with `Lean.trustCompiler`) -- the weaker class, because the Lean COMPILER is
# then trusted beside the kernel.  A goal `bv_decide` closes in its own
# rewriting stage never calls the solver, so it carries no such axiom -- the
# stronger class.  That rewriting stage is a tactic of its own in this Lean:
# `bv_normalize` (Std/Tactic/BVDecide/Syntax.lean line 98).
#
# So the attempt this lane makes, per row, is the honest one: the same model
# definitions unfolded and then `bv_normalize` ALONE.  A row it closes has
# moved to the stronger class; a row it does not keeps its `bv_decide` proof
# and is listed with what the attempt cost.  Nothing already proved is
# disturbed: the attempt is written to one scratch theorem file and every
# ModelCheck_*.lean stays as the run that proved it left it.
#
# Memory bound: 6 GB, named abort ABORT_MEMORY_L3.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/l3home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

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

print("[1/4] the trust classes, before this task and after the composer fix")
print("   BEFORE (check_L2.json.before_task_l3): proved %d, "
      "carrying Lean.ofReduceBool %d"
      % (sum(1 for r in before['rows'] if r.get('closed_by')), len(was_native)))
print("   AFTER  (check_L2.json):                proved %d, "
      "carrying Lean.ofReduceBool %d" % (len(proved), len(native)))
now_native = set(r['theorem_name'] for r in native)
print("   of the %d rows that carried it BEFORE, still carrying it: %d"
      % (len(was_native), sum(1 for n in was_native if n in now_native)))
print("   rows that carry it now and did not before: %d"
      % len(now_native - set(was_native)))
print("      %s" % sorted(now_native - set(was_native)))

print("")
print("[2/4] the attempt: the model definitions unfolded, then bv_normalize "
      "alone, one lean process per row")
scratch = os.path.join(HERE, 'archproof', 'Archproof', 'StrongClassTry.lean')
records = []
total = len(native)
for index, row in enumerate(native, 1):
    tactic = M.tactic_for(row, "bv_decide").replace("bv_decide", "bv_normalize")
    label = ("%s single-opcode row %d, arch mnemonic %r, example unit %s, "
             "%d members -- the stronger-class attempt"
             % (row["lang"], row["row_index"], row["mnem"], row["unit"],
                row["member_count"]))
    text = M.theorem_text(label, "StrongClassTry", row, tactic)
    handle = open(scratch, 'w')
    handle.write(text)
    handle.close()
    result = M.lean_once(scratch)
    outcome, detail = M.classify(result)
    axioms = M.axiom_line(result["output"]) if outcome == "PROVED" else None
    stronger = bool(outcome == "PROVED" and axioms and
                    'ofReduceBool' not in axioms)
    records.append({
        "theorem_name": row["theorem_name"],
        "unit": row["unit"],
        "lang": row["lang"],
        "mnem": row["mnem"],
        "row_index": row["row_index"],
        "was_native_before_task_l3": row["theorem_name"] in set(was_native),
        "bv_decide": {"closed_by": row.get("closed_by"),
                      "wall_seconds": row.get("wall_seconds"),
                      "peak_kb": row.get("peak_kb"),
                      "axioms": row.get("axioms")},
        "bv_normalize_attempt": {
            "outcome": outcome,
            "detail": detail,
            "wall_seconds": result["wall_seconds"],
            "peak_kb": result["peak_kb"],
            "axioms": axioms,
            "tactic": tactic,
            "lean_output": result["output"][:1200],
        },
        "moved_to_the_stronger_class": stronger,
    })
    print("[%d/%d] %-28s %-12s %6.2f s  %7d kB  %s"
          % (index, total, row["theorem_name"], outcome,
             result["wall_seconds"], result["peak_kb"],
             "STRONGER" if stronger else (detail or "")[:70]))
    guard(row["theorem_name"])

print("")
print("[3/4] how many moved")
moved = [r for r in records if r["moved_to_the_stronger_class"]]
print("   attempted: %d" % len(records))
print("   moved to the stronger class (no Lean.ofReduceBool): %d" % len(moved))
print("   kept their bv_decide proof: %d" % (len(records) - len(moved)))
causes = {}
for r in records:
    if not r["moved_to_the_stronger_class"]:
        key = (r["bv_normalize_attempt"]["outcome"],
               (r["bv_normalize_attempt"]["detail"] or "")[:90])
        causes[key] = causes.get(key, 0) + 1
print("   by cause:")
for key in sorted(causes, key=str):
    print("      %4d  %s" % (causes[key], key))
print("   wall clock of the attempts: %.2f s total, %.3f s median"
      % (sum(r["bv_normalize_attempt"]["wall_seconds"] for r in records),
         sorted(r["bv_normalize_attempt"]["wall_seconds"]
                for r in records)[len(records)//2] if records else 0.0))
print("   peak RSS of the attempts: %d kB the highest"
      % max([r["bv_normalize_attempt"]["peak_kb"] for r in records] or [0]))

document = {
    "what": "the trust class of every proved row of the check, and the "
            "attempt to close the rows that carry the native-evaluation "
            "axiom without calling the SAT solver",
    "before_file": "check_L2.json.before_task_l3",
    "rows_carrying_ofReduceBool_before": was_native,
    "rows_carrying_ofReduceBool_after": sorted(now_native),
    "attempts": records,
}
handle = open(os.path.join(HERE, 'l3_trust_classes.json'), 'w')
json.dump(document, handle, indent=1, sort_keys=True)
handle.close()
print("   wrote l3_trust_classes.json")

print("")
print("[4/4] the four axiom sets over all 172 proved rows, after this task")
import collections, re
pats = collections.Counter()
for r in proved:
    a = re.sub(chr(39) + '[^' + chr(39) + ']+' + chr(39), 'THEOREM',
               r['axioms'] or '(none recorded)')
    pats[(r['closed_by'], a)] += 1
for k in sorted(pats, key=str):
    print("   %4d  %s" % (pats[k], k))
print("   peak RSS %d kB" % guard('end'))
PY
echo "--- exit $?"
