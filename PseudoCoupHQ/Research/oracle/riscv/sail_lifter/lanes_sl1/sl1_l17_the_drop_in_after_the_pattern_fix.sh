#!/bin/bash
# sl1 lane 17 -- lane 16 again after one fix: a numeric pattern against a bit-vector value compares at the value's width. The drop-in riscv_reference.py (its walk now the model's
# own decoder and execute) beside the transcription it replaced, over the
# carved bodies of carved.json: for each unit the answer term of both
# walks, z3 asked whether they are equal (3,000 ms), every refusal by
# cause; the lifter's reset report and a few terms LITERAL.
set -u
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
RV=PseudoCoupHQ/Research/oracle/riscv
mkdir -p /work/sl1f/old /work/sl1f/work
cp $SL/riscv_reference_transcription_2026-09-13.py.txt /work/sl1f/old/riscv_reference.py
echo "[1/2] the drop-in over the carved bodies, beside the transcription"
export SL1_WORK=/work/sl1f/work
timeout 1800 python3 - <<'PYEOF'
import importlib.util, json, sys, time, traceback
import z3
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import riscv_reference as NEW
spec = importlib.util.spec_from_file_location("old_reference", "/work/sl1f/old/riscv_reference.py")
OLD = importlib.util.module_from_spec(spec); spec.loader.exec_module(OLD)
t = time.time()
new_ref = NEW.RiscvReference()
lifter = new_ref.lifter
print("generated lifter ready in %.1f s: %d definitions, commit %s, unit axioms as no-ops: %d" % (time.time() - t, len(lifter.definitions), lifter.commit, len(lifter.axioms)))
for line in lifter.reset_report:
    print("  reset:", line)
old_ref = OLD.RiscvReference()
rows = json.load(open("PseudoCoupHQ/Research/oracle/riscv/carved.json"))["rows"]
print("| unit | lang | mnem | lines | old | new | equal? | seconds |")
print("|---|---|---|---|---|---|---|---|")
census = {}
for row in rows:
    body = row.get("body") or []
    if not body:
        continue
    home = "fa0" if any(l.split()[0].startswith("f") and "fmv" not in l for l in body) else "a0"
    seed = {}
    t = time.time()
    old_term = None; new_term = None; old_out = "ok"; new_out = "ok"
    try:
        st = old_ref.simulate(list(body), None, seed)
        old_term = old_ref.answer_of(st, home)
    except Exception as p:
        old_out = "%s: %s" % (type(p).__name__, str(p)[:80])
    try:
        st = new_ref.simulate(list(body), None, seed)
        new_term = new_ref.answer_of(st, home)
    except Exception as p:
        new_out = "%s: %s" % (type(p).__name__, str(p)[:120])
    verdict = "-"
    if old_term is not None and new_term is not None:
        if old_term.size() != new_term.size():
            verdict = "WIDTHS %d/%d" % (old_term.size(), new_term.size())
        else:
            s = z3.Solver(); s.set("timeout", 3000)
            s.add(old_term != new_term)
            r = s.check()
            verdict = {z3.unsat: "EQUAL", z3.sat: "DIFFER", z3.unknown: "UNDECIDED"}[r]
            if r == z3.sat:
                verdict = verdict + " " + str(s.model())[:100].replace("\n", " ")
    census[verdict.split()[0] if verdict != "-" else ("new " + new_out.split(":")[0] if new_out != "ok" else "old refused")] = census.get(verdict.split()[0] if verdict != "-" else ("new " + new_out.split(":")[0] if new_out != "ok" else "old refused"), 0) + 1
    print("| %s | %s | %s | %d | %s | %s | %s | %.2f |" % (row.get("unit"), row.get("lang"), row.get("mnem"), len(body), old_out, new_out, verdict, time.time() - t))
print("census:", census)
print("a term LITERAL, the first unit, new walk:")
row = rows[0]; st = new_ref.simulate(list(row["body"]), None, {}); print("  ", z3.simplify(new_ref.answer_of(st, "a0")))
PYEOF
echo "[2/2] sail_points' own reading of two lines through the drop-in"
timeout 600 python3 - <<'PYEOF'
import sys, time
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import z3, sail_points as SP
for line in ("add a2, a0, a1", "divw a2, a0, a1", "c.add a0, a1", "fsgnjn.d fa2, fa0, fa1"):
    t = time.time()
    try:
        homes = ("a0", "a1", "a0", "integer") if line.startswith("c.") else (("fa0", "fa1", "fa2", "float") if line.startswith("fsgnjn") else None)
        term, a, b = SP.reference_term(line, homes)
        print("%-24s %.2f s  term: %s" % (line, time.time() - t, str(z3.simplify(term))[:200].replace("\n", " ")))
        print("   at (7, 3):", SP.evaluate(term, a, b, 7, 3), " at (-1, 0):", SP.evaluate(term, a, b, -1, 0))
    except Exception as p:
        print("%-24s REFUSED %s: %s" % (line, type(p).__name__, str(p)[:300]))
PYEOF
echo "done $(date -u +%FT%TZ)"
