#!/usr/bin/env bash
# t91_l6_reference_evidence.sh -- TASK 91, lane 6: the evidence for
# PART A (one simulator, not four) and PART B (the two defects), each
# claim quoted from the artifact rather than from any note.
#
# WHAT IS SHOWN, in order:
#   A1  the header line every superseded simulator now carries.
#   A2  every simulator the gate can reach, read off the imports of
#       `gate.py` -- the file that decides every term verdict.
#   B1  the remainder: the machine's SRem against the z3 operator, run
#       on the counterexample log 153 section 5 names (7, -3).
#   B2  the machine stack and the x87 stack on the MachineState class.
#   B3  the x87 CONTROL WORD: a census of every arch opcode any body in
#       the corpus spells that reads or writes it.  The opcode_table
#       CORE's rule is "no entry invented for an opcode no body
#       contains", so this census is what decides whether a control
#       word must be modelled at all.
#   B4  the x87 unit log 153 section 4.3 printed as UNDECIDED on both
#       routes, walked through the ONE reference today.
#   B5  a machine-stack unit walked the same way.
#
# THE MEMORY BOUND: one canon38 source document at a time for the
# census; cap 6000 MB, abort named T91_MEMORY_ABORT.
#
# Product: /out/t91_reference_evidence.json
set -uo pipefail

cd /projects/PseudoCoupHQ/Research/op_pipeline || exit 2
mkdir -p /out

echo "== A1: the header line each superseded simulator carries =="
for f in canon9_behaviour_check.py canon10_behaviour_check.py canon12_behaviour_check.py; do
  echo "--- $f line 2 ---"
  sed -n '2p' "$f"
done

echo ""
echo "== A2: every module gate.py imports =="
grep -n "^import \|^from " gate.py

echo ""
echo "== A2b: does gate.py import any canon behaviour checker? =="
grep -c "^import canon[0-9]*_behaviour_check" gate.py

echo ""
echo "== B1..B5 =="
python3 - <<'PY'
import glob
import json
import os
import resource
import sys

HERE = "/projects/PseudoCoupHQ/Research/op_pipeline"
sys.path.insert(0, HERE)

import gate as GATE
import layer4c
import reference as REF
import z3

MEMORY_CAP_MB = 6000
MEMORY_ABORT = "T91_MEMORY_ABORT"
out = {}


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check(stage):
    now = peak()
    if now > MEMORY_CAP_MB:
        raise SystemExit("%s: %.1f MB passed the cap of %d MB during %s"
                         % (MEMORY_ABORT, now, MEMORY_CAP_MB, stage))
    return now


# ---- B1: the remainder ---------------------------------------------
print("B1: THE REMAINDER, on log 153 section 5's own counterexample")
a = z3.BitVecVal(7, 32)
b = z3.BitVecVal(-3, 32)
solver = z3.Solver()
machine = z3.simplify(z3.SRem(a, b))
operator_form = z3.simplify(a % b)
print("    LITERAL -- z3.SRem(7, -3) at 32 bits = %s  (signed %d)"
      % (machine, machine.as_signed_long()))
print("    LITERAL -- the z3 operator on the same two = %s  (signed %d)"
      % (operator_form, operator_form.as_signed_long()))
out["remainder"] = {
    "SRem_7_minus_3": machine.as_signed_long(),
    "z3_operator_7_minus_3": operator_form.as_signed_long(),
}
source = open(os.path.join(HERE, "reference.py")).read()
lines = source.split("\n")
division = []
for index, line in enumerate(lines):
    if "SRem" in line or "URem" in line or "SDiv" in line or \
            "UDiv" in line:
        division.append("%d: %s" % (index + 1, line.rstrip()))
print("    LITERAL -- every division line in reference.py:")
for line in division:
    print("      %s" % line)
out["reference_division_lines"] = division

# ---- B2: the two stacks on the state -------------------------------
print("")
print("B2: THE MACHINE STACK AND THE X87 STACK on MachineState")
state = REF.MachineState()
print("    LITERAL -- MachineState().stack = %r" % state.stack)
print("    LITERAL -- MachineState().x87   = %r" % state.x87)
methods = []
for name in sorted(dir(REF.MachineState)):
    if name.startswith("_"):
        continue
    if "push" in name or "pop" in name or "x87" in name or \
            "stack" in name:
        methods.append(name)
print("    LITERAL -- the stack and x87 methods: %s" % ", ".join(methods))
out["machine_state"] = {
    "stack_keys": sorted(state.stack),
    "x87_keys": sorted(state.x87),
    "methods": methods,
    "x87_sort": str(REF.X87_SORT) if hasattr(REF, "X87_SORT") else None,
}

# ---- B3: the x87 control word census -------------------------------
print("")
print("B3: THE X87 CONTROL WORD -- every body in the corpus, counted")
CONTROL_WORD_OPCODES = ("fldcw", "fnstcw", "fstcw", "fldenv", "fnstenv",
                        "fstenv", "fnsave", "frstor", "fldz", "finit",
                        "fninit", "fnclex", "fclex")
paths = []
for lang in ("c", "cpp", "go", "rust", "swift"):
    paths.append(os.path.join(HERE, "canon38_wrapped_%s.json" % lang))
    paths.append(os.path.join(HERE, "canon40_wrapped_%s.json" % lang))
paths.append(os.path.join(HERE, "canon38_interp.json"))
paths.append(os.path.join(HERE, "canon40_interp.json"))
paths.extend(sorted(glob.glob(os.path.join(HERE, "canon38_regen_store",
                                           "*.json"))))
paths.extend(sorted(glob.glob(os.path.join(HERE, "canon40_regen_store",
                                           "*.json"))))
seen = {}
bodies = 0
x87_bodies = 0
for path in paths:
    if not os.path.exists(path):
        continue
    document = json.load(open(path))
    for name, record in document.get("units", {}).items():
        bodies = bodies + 1
        spells_x87 = False
        for raw in record.get("body_verbatim") or []:
            text = raw.split("!!")[0].strip()
            if text == "":
                continue
            mnemonic = text.split(" ", 1)[0]
            if mnemonic.startswith("f"):
                spells_x87 = True
            if mnemonic in CONTROL_WORD_OPCODES:
                seen.setdefault(mnemonic, [])
                if len(seen[mnemonic]) < 5:
                    seen[mnemonic].append(name)
        if spells_x87:
            x87_bodies = x87_bodies + 1
    del document
    check("the control-word census at %s" % os.path.basename(path))
print("    bodies walked (canon38 and canon40 together): %d" % bodies)
print("    bodies spelling any x87 arch opcode:          %d" % x87_bodies)
print("    control-word arch opcodes found:              %s"
      % (json.dumps(seen, sort_keys=True) if seen else "NONE"))
out["control_word_census"] = {
    "bodies_walked": bodies,
    "bodies_spelling_an_x87_opcode": x87_bodies,
    "control_word_opcodes_found": seen,
    "opcodes_looked_for": list(CONTROL_WORD_OPCODES),
}

# ---- B4 and B5: two units walked through the ONE reference ---------
print("")
print("B4/B5: TWO UNITS log 153 recorded as UNDECIDED, walked today")
WANTED = ["cpp/regen_36796", "go/op_110", "c/op_246", "cpp/regen_14397"]
found = {}
for path in paths:
    if "canon38" not in path:
        continue
    if not os.path.exists(path):
        continue
    document = json.load(open(path))
    for name in WANTED:
        if name in found:
            continue
        record = document.get("units", {}).get(name)
        if record is None:
            continue
        if "ledger" not in record:
            continue
        unit = dict(record)
        unit["unit"] = name
        found[name] = unit
    del document
    if len(found) == len(WANTED):
        break

archives = {}
path = os.path.join(HERE, "canon39_callee_units.json")
if os.path.exists(path):
    document = json.load(open(path))
    for key, unit in document.get("units", {}).items():
        toolchain = unit.get("toolchain") or key.split("/", 1)[0]
        callee = unit.get("callee") or key.split("/", 1)[-1]
        archives.setdefault(toolchain, {})
        archives[toolchain][callee] = unit

reference = REF.Reference(runtime_units=archives)
gate = GATE.Gate(reference=reference)
walked = {}
for name in WANTED:
    unit = found.get(name)
    if unit is None:
        print("    %s: not found in canon38" % name)
        continue
    print("")
    print("  %s" % name)
    body = unit.get("body_verbatim") or []
    print("    LITERAL -- body: %s" % "; ".join(
        raw.split("!!")[0].strip() for raw in body))
    row = {"body": [raw.split("!!")[0].strip() for raw in body]}
    try:
        answer, width = reference.answer_for_unit(unit)
        row["reference_answer"] = str(z3.simplify(answer))
        print("    LITERAL -- the ONE reference's answer: %s"
              % str(z3.simplify(answer))[:400])
    except Exception as problem:
        row["reference_answer"] = None
        row["reference_refusal"] = "%s: %s" % (type(problem).__name__,
                                               problem)
        print("    the reference refuses: %s" % problem)
    transcription = layer4c.transcribe(unit)
    term = transcription.out_term
    if term is None:
        row["ledger_term"] = None
        print("    the ledger builds no term for OUT-0")
    else:
        row["ledger_term"] = str(z3.simplify(term))
        print("    LITERAL -- the ledger's OUT-0 term:    %s"
              % str(z3.simplify(term))[:400])
    ship = gate.prove_term_against_ship(term, unit)
    row["route_one"] = ship.as_dict()
    print("    route one (the term against the ship body): %s"
          % ship.outcome)
    print("      %s" % (ship.reason or "")[:300])
    walked[name] = row
out["units_walked"] = walked

with open("/out/t91_reference_evidence.json", "w") as handle:
    json.dump(out, handle, indent=1, sort_keys=True)
print("")
print("PEAK RESIDENT SIZE: %.1f MB, cap %d MB" % (peak(), MEMORY_CAP_MB))
PY
