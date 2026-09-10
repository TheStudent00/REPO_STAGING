#!/bin/bash
# t2_l24_the_four_that_still_need_the_solver.sh -- task t2, lane 24:
# which lemma each remaining `sat` place is short of.
#
# Lane 23's pass discharged ten of the fourteen equalities by the
# schemas' Lean lemmas and four by z3.  Form 2 records which lemmas it
# held and which it found missing, so this lane prints that record for
# every place the solver still had to answer.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=1

i=1
echo "[$i/$total] EVERY CONSTRUCTED PLACE, ITS PROOF FORM AND WHAT FORM 2 WAS SHORT OF"
python3 - "$C" <<'PY'
import sys, json, os
store = os.path.join(sys.argv[1], "t2_construct_runs.jsonl")
print("| target | `mnem` | shape | `key_width` | place | proof | the lemmas form 2 was short of |")
print("|---|---|---|---|---|---|---|")
for line in open(store):
    text = line.strip()
    if not text:
        continue
    run = json.loads(text)
    if run.get("route") != "constructed":
        continue
    for place in run.get("places") or []:
        block = place.get("constructed") or {}
        equality = block.get("equality") or {}
        if not equality:
            continue
        missing = []
        for form in equality.get("forms") or []:
            if form["form"] != "lemma+gate":
                continue
            for row in form.get("lemmas_missing") or []:
                missing.append("`%s` (%s)" % (row.get("shape"),
                                              row.get("why")))
                continue
        print("| %s | `%s` | %s | %s | %s | %s | %s |"
              % (run["lang"], run["mnem"], run["shape"],
                 run["key_width"], place.get("writes"),
                 equality.get("proof"), "; ".join(missing) or "--"))
        continue
    continue
PY
echo
echo "lane done"
