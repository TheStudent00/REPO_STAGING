#!/bin/bash
# TASK 96 round 19, lane 1.  Inventory only: nothing is written.
set -x
cd PseudoCoupHQ/Research/op_pipeline

echo "[1/6] the compiled population, per language, under canon40"
python3 - <<'PY'
import json
import os
total = 0
for lang in ("c", "cpp", "go", "rust", "swift"):
    path = "canon40_wrapped_%s.json" % lang
    if not os.path.exists(path):
        print("%-6s MISSING %s" % (lang, path))
        continue
    units = json.load(open(path))["units"]
    total = total + len(units)
    print("%-6s %5d units  %s" % (lang, len(units), path))
print("compiled population total: %d" % total)
PY

echo "[2/6] the %r15 count over every compiled unit's WRAPPED TEXT"
python3 - <<'PY'
import json
import resource
hits = 0
seen = 0
per = {}
for lang in ("c", "cpp", "go", "rust", "swift"):
    units = json.load(open("canon40_wrapped_%s.json" % lang))["units"]
    n = 0
    for label in units:
        text = units[label].get("wrapped_text")
        if text is None:
            continue
        seen = seen + 1
        if "%r15" in text:
            hits = hits + 1
            n = n + 1
            if n < 4:
                print("   HIT %s" % label)
    per[lang] = n
print("wrapped texts inspected: %d" % seen)
print("wrapped texts containing %%r15: %d" % hits)
print("per language: %s" % json.dumps(per, sort_keys=True))
print("peak resident size kB: %d"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY

echo "[3/6] the same count as a plain grep, independent of the loader"
for L in c cpp go rust swift; do
  printf '%-6s ' "$L"
  grep -o '"wrapped_text": "[^"]*%r15[^"]*"' canon40_wrapped_$L.json | wc -l
done

echo "[4/6] the eleven units, and where their re-carved bodies live"
python3 - <<'PY'
import json
d = json.load(open("t94_recarve.json"))
print("records: %d" % len(d["records"]))
for r in d["records"]:
    rc = r.get("recarved") or {}
    bv = rc.get("body_verbatim")
    uf = r.get("universal_form") or {}
    print("%-58s body=%-5s old_form=%-8s verdict=%s"
          % (r["unit"], len(bv) if bv else None,
             "rendered" if uf.get("universal_text") else "refused",
             r.get("new_verdict")))
PY

echo "[5/6] region36's six kinds, read off its own line 271"
sed -n '268,272p' region36.py

echo "[6/6] the canonical form's block order, read off ledger.py"
sed -n '280,283p' ledger.py
echo done
