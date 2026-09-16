#!/bin/bash
# sl1 lane 2z (named to run before lane 30 in the daemon's sorted sweep)
# -- the cause of rv6's 580 NO_TERM rows: every TRANSLATED row of
# model_table_rv.json re-run through the drop-in exactly as
# rv_loop.riscv_terms does, the exception printed per row instead of
# swallowed; the causes counted.
set -u
export HOME=/work
RV=PseudoCoupHQ/Research/oracle/riscv
mkdir -p /work/sl1z; export SL1_WORK=/work/sl1z
echo "[1/1] every model-table line through the drop-in, the refusal named"
timeout 1500 python3 - <<'PYEOF'
import json, sys, time, traceback
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import riscv_reference as RV, model_table_rv as MRV
reference = RV.RiscvReference()
rows = json.load(open("PseudoCoupHQ/Research/oracle/riscv/model_table_rv.json"))["rows"]
seen = set(); causes = {}; ok = 0; bad = 0; t = time.time()
for row in rows:
    if row["outcome"] != "TRANSLATED" or not row.get("mapping"): continue
    key = (row["mnem"], row["shape"], row["key_width"])
    if key in seen: continue
    seen.add(key)
    try:
        written, condition, line = MRV.run_line(reference, row["mnem"], row["operands"])
        ok += 1
    except Exception as p:
        bad += 1
        cause = "%s: %s" % (type(p).__name__, str(p)[:150])
        causes.setdefault(cause[:110], []).append("%s %s" % (row["mnem"], row["shape"]))
print("cells %d: ok %d, refused %d, %.0f s" % (len(seen), ok, bad, time.time() - t))
for cause, cells in sorted(causes.items(), key=lambda x: -len(x[1])):
    print("%4d  %s" % (len(cells), cause)); print("        ", " ".join(cells[:12]))
PYEOF
echo "done $(date -u +%FT%TZ)"
