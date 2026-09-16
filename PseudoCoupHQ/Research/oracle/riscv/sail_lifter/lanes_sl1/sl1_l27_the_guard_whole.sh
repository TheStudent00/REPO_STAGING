#!/bin/bash
# sl1 lane 27 -- THE GUARD, the whole generated population: every
# constructor of the model's instruction type times every assignment of
# its enum-typed fields (1,551 rows), 1,000 points each, against the Sail
# model's own C simulator; the store guard_all.json, then the spelling
# guard over it.
set -u
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
OP=PseudoCoupHQ/Research/op_pipeline
mkdir -p /work/sl1h
echo "[1/3] the guard, whole population: started $(date -u +%FT%TZ)"
timeout 9000 python3 $SL/sail_guard.py $SL/guard_all /work/sl1h --points 1000 2>&1 | cut -c1-300
echo "  exit: ${PIPESTATUS[0]}  finished $(date -u +%FT%TZ)"
echo "[2/3] the census, by constructor and outcome"
python3 - <<'PYEOF'
import json
d = json.load(open("PseudoCoupHQ/Research/oracle/riscv/sail_lifter/guard_all.json"))
rows = d["rows"]
print("meta:", {k: v for k, v in d["meta"].items() if k not in ("reset_report",)})
by = {}
for r in rows:
    key = (r["constructor"], r["outcome"])
    by[key] = by.get(key, 0) + 1
causes = {}
for r in rows:
    if r["outcome"] == "REFUSED":
        c = r.get("cause", "")[:60]
        causes[c] = causes.get(c, 0) + 1
print("| constructor | outcome | rows |"); print("|---|---|---|")
for (c, o), n in sorted(by.items()): print("| %s | %s | %d |" % (c, o, n))
print("refusal causes:"); 
for c, n in sorted(causes.items(), key=lambda x: -x[1])[:40]: print("  %4d  %s" % (n, c))
dis = [r for r in rows if r["outcome"] == "DISAGREES"]
print("DISAGREES rows:", len(dis))
for r in dis[:40]: print("  ", r["constructor"], r["fields"], r.get("mnem"), r["points"], r["agree"], r["disagree"], r["examples"][:1])
print("points total:", sum(r["points"] for r in rows), "agree:", sum(r["agree"] for r in rows), "disagree:", sum(r["disagree"] for r in rows))
PYEOF
echo "[3/3] the spelling guard"
python3 $OP/check_no_spelling_keys.py $SL/guard_all.json $SL/guard_sample.json; echo "  guard rc=$?"
echo "done $(date -u +%FT%TZ)"
