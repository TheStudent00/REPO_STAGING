#!/bin/bash
# TASK 96 round 19, lane 5.  Separate the form change from the
# instrument change, and dump the three wrapped texts per unit.
set -x
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "[1/5] the analysis"
python3 t96_analysis.py 2>&1 | tail -20

echo "[2/5] THE INSTRUMENT QUESTION: gate.py's own six checks against FORM 1's text"
python3 - <<'PY'
import json
d = json.load(open("t96_analysis.json"))
for r in d["records"]:
    one = r["form_one_under_this_instrument"]
    if not one.get("asked"):
        print("%-58s not asked: %s" % (r["unit"], one["why"]))
        continue
    f = one["the_first_failure"]
    print("%-58s structural route available to FORM 1: %s"
          % (r["unit"],
             one["the_structural_route_is_available_to_form_one"]))
    if f is not None:
        print("      first failure: %s" % f["note"][:200])
print()
print(json.dumps(d["the_instrument_question"], indent=1,
                 sort_keys=True))
PY

echo "[3/5] the solver route, said separately from the verdict"
python3 - <<'PY'
import json
d = json.load(open("t96_analysis.json"))
for r in d["records"]:
    for name in ("form_two", "form_three"):
        row = r[name]
        if row["outcome"] == "REFUSED":
            print("%-58s %-11s REFUSED %s"
                  % (r["unit"], name, row["refusal_cause"]))
            continue
        s = row["solver_route"]
        passed = 0
        for c in row["the_six_checks"]:
            if c["passed"]:
                passed = passed + 1
        print("%-58s %-11s verdict=%-22s solver_answered=%-5s "
              "checks=%d/6  120000ms=%s"
              % (r["unit"], name, row["verdict"],
                 s["the_solver_answered"], passed,
                 (row["gate_at_120000ms"] or {}).get("verdict")))
        if s["what_it_had_no_model_for"]:
            print("      the solver had no model for: %s"
                  % s["what_it_had_no_model_for"])
PY

echo "[4/5] the shortest unit's three texts, in full"
python3 - <<'PY'
import json
d = json.load(open("t96_canonical.json"))
for r in d["records"]:
    if not r["unit"].endswith("NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER"):
        continue
    print("UNIT", r["unit"])
    print()
    print("-- FORM 1, region36 + canon36_universal (superseded) --")
    old = r["the_superseded_form"]
    if old["wrapped_text"] is None:
        print("REFUSED:", old["refusal"])
    else:
        for line in old["wrapped_text"].split("; "):
            print("   ", line)
    for key, title in (("the_canonical_form", "FORM 2 (Part A)"),
                       ("the_canonical_form_with_the_seventh_block",
                        "FORM 3 (Part B)")):
        print()
        print("-- %s --" % title)
        f = r[key]
        if f["outcome"] == "REFUSED":
            print("REFUSED (%s): %s" % (f["refusal_cause"],
                                        f["refusal"]))
            continue
        for line in f["wrapped_text"].split("; "):
            print("   ", line)
PY

echo "[5/5] the preludes and epilogues of all eleven, both forms"
python3 - <<'PY'
import json
d = json.load(open("t96_canonical.json"))
for r in d["records"]:
    print("=== %s" % r["unit"])
    for key, title in (("the_canonical_form", "FORM 2"),
                       ("the_canonical_form_with_the_seventh_block",
                        "FORM 3")):
        f = r[key]
        if f["outcome"] == "REFUSED":
            print("  %-7s REFUSED (%s)" % (title, f["refusal_cause"]))
            continue
        print("  %-7s prelude: %s" % (title, f["prelude"]))
        print("  %-7s epilogue: %s" % ("", f["epilogue"]))
PY
echo done
