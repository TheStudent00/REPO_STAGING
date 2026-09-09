#!/bin/bash
# L2 lane 1 — what is on the machine, and what the reference's opcode
# table says about the five opcodes the brief names.
#
# Five steps: the toolchain versions; the opcode table's own inventory;
# the five entries and the source of the builder behind each; the five
# builders RUN on a synthetic line so the z3 term each produces is on
# the page; the 243-row population recomputed from single_opcode_units.json.
set -u

TOTAL=5
OP=/projects/PseudoCoupHQ/Research/op_pipeline
export HOME=/work/L2home
mkdir -p "$HOME"

echo "[1/$TOTAL] toolchain versions"
which lean lake python3
lean --version
lake --version
python3 -c "import z3; print('z3 version:', z3.get_version_string())"

echo "[2/$TOTAL] the opcode table's inventory, off reference.py itself"
cd "$OP" || exit 1
python3 - <<'PY'
import sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
import reference as R
t = R.REFERENCE.opcode_table
built = [m for m in sorted(t.entries) if t.entries[m].build is not None]
census = t.without_a_builder()
print("entries in the table: %d" % len(t.entries))
print("with a builder      : %d" % len(built))
print("census rows (no builder): %d -- %s" % (len(census), " ".join(census)))
PY

echo "[3/$TOTAL] the five entries the brief names, and their builder's source"
python3 - <<'PY'
import inspect, sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
import reference as R
t = R.REFERENCE.opcode_table
for m in ("add", "sar", "imul", "ucomiss", "cvtsi2sd"):
    e = t.entry_for(m)
    print("=== %s ===" % m)
    print("  reads : %s" % (e.reads,))
    print("  writes: %s" % (e.writes,))
    print("  build : %s" % (getattr(e.build, "__name__", e.build),))
PY

echo "--- the builder bodies, LITERAL from reference.py"
for fn in build_binary build_shift build_wide_multiply build_float_flag_only build_convert_to_float; do
  echo "----- $fn -----"
  awk -v f="def $fn(" 'index($0,f)==1{p=1} p&&/^def /&&index($0,f)!=1&&NR>s{exit} p{print; s=NR}' reference.py
done

echo "[4/$TOTAL] the five builders RUN: one synthetic line each, over symbolic seeds"
python3 - <<'PY'
import sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
import reference as R
import z3

LINES = [
    ("add",      "add %rsi,%rdi"),
    ("add",      "add %esi,%edi"),
    ("sar",      "sar %cl,%rdi"),
    ("sar",      "sar $0x3,%edi"),
    ("imul",     "imul %rsi,%rdi"),
    ("ucomiss",  "ucomiss %xmm1,%xmm0"),
    ("cvtsi2sd", "cvtsi2sd %edi,%xmm0"),
]
for mnem, line in LINES:
    state = R.MachineState()
    try:
        R.REFERENCE.step(state, line)
    except Exception as exc:
        print("%-28s REFUSED %s: %s" % (line, type(exc).__name__, exc))
        continue
    print("=== %s" % line)
    for family in sorted(state.registers):
        print("    reg %-6s := %s" % (family, R.canon and z3.simplify(state.registers[family])))
    if state.flags is not None:
        print("    flags setter %r" % (state.flags[0],))
        print("      L := %s" % (state.flags[1],))
        print("      R := %s" % (state.flags[2],))
PY

echo "[5/$TOTAL] the 243-row population, recomputed"
python3 - <<'PY'
import json, os, sys
sys.path.insert(0, '/projects/PseudoCoupHQ/Research/op_pipeline')
OP = '/projects/PseudoCoupHQ/Research/op_pipeline'
SRC = '/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json'
LANGS = ["c", "cpp", "go", "rust", "swift"]
doc = json.load(open(SRC))
rows = []
for lang in LANGS:
    for i, row in enumerate(doc["single_opcode_groups"][lang]["narrow"]):
        rows.append({"lang": lang, "row_index": i, "mnemonic": row["mnemonic"],
                     "row_body_text": row["body_text"],
                     "example_unit_id": row["example_unit_id"],
                     "member_count": row["member_count"]})
print("rows over the five compiled languages: %d" % len(rows))
per = {}
for r in rows:
    per[r["lang"]] = per.get(r["lang"], 0) + 1
print("per language: %s" % per)
mn = {}
for r in rows:
    mn[r["mnemonic"]] = mn.get(r["mnemonic"], 0) + 1
print("distinct mnemonics over the rows: %d" % len(mn))
print("mnemonic counts: %s" % sorted(mn.items(), key=lambda kv: (-kv[1], kv[0])))
PY
echo "--- lane exit $?"
