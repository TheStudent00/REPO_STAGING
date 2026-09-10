#!/bin/bash
# t2_l22_why_the_lemma_route_did_not_fire.sh -- task t2, lane 22: the
# lemma route's own record, place by place.
#
# Lane 21 ran the pass with the lemma table in place and every equality
# still fell through to z3.  Form 2 records which lemmas it HELD and
# which it found MISSING, so the cause is on the record and this lane
# prints it.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t2_brief.md
set -u

C=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct
total=2

i=1
echo "[$i/$total] THE LEMMA TABLE'S OWN KEYS"
python3 - "$C" <<'PY'
import sys, json, os
document = json.load(open(os.path.join(sys.argv[1], "lean", "lemmas_t2.json")))
rows = document["rows"]
print("rows on lemmas_t2.json: %d" % len(rows))
proved = [r for r in rows if r["outcome"] == "PROVED_BY_LEAN"]
print("of them PROVED_BY_LEAN: %d" % len(proved))
print("")
print("| schema | width | word | shape |")
print("|---|---|---|---|")
for row in proved[:8]:
    print("| %s | %s | %s | `%s` |"
          % (row["schema"], row["width"], row["word"], row["shape"]))
PY
echo

i=2
echo "[$i/$total] WHAT FORM 2 HELD AND WHAT IT FOUND MISSING, per place"
python3 - "$C" <<'PY'
import sys, json, os
store = os.path.join(sys.argv[1], "t2_construct_runs.jsonl")
seen = 0
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
        seen = seen + 1
        if seen > 4:
            continue
        print("---- %s %s %s on %s at %s"
              % (run["mnem"], run["shape"], run["key_width"],
                 run["lang"], place.get("writes")))
        print("   instances: %s" % json.dumps(block.get("instances")))
        for form in equality.get("forms") or []:
            if form["form"] != "lemma+gate":
                continue
            print("   lemmas held:    %s" % json.dumps(form.get("lemmas_held")))
            print("   lemmas missing: %s" % json.dumps(form.get("lemmas_missing")))
        continue
    continue
print("")
print("constructed places carrying an equality: %d" % seen)
PY
echo
echo "lane done"
