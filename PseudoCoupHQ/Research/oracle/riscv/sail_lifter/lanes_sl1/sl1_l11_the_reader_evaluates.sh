#!/bin/bash
# sl1 lane 11 -- the reader over the real emit: parse (counts, unread
# definitions LITERAL), the register widths it reads off RegisterType,
# the model's own reset evaluated, then the first lines of the corpus's
# carved bodies assembled to words, decoded by the emitted decoder and
# executed by the emitted execute with the x registers symbolic; every
# refusal printed by cause.
set -u
total=3
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
RV=PseudoCoupHQ/Research/oracle/riscv
E=$SL/lean_emit
mkdir -p /work/sl1e
echo "[1/$total] parse"
timeout 900 python3 $SL/lean_reader.py $E 2>&1 | head -60
echo "[2/$total] widths, reset, decode, execute"
timeout 1200 python3 - <<'PYEOF'
import json, sys, time, traceback
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv/sail_lifter")
import z3
import lean_reader as LR
import assemble as AS
E = "PseudoCoupHQ/Research/oracle/riscv/sail_lifter/lean_emit"
t = time.time()
defs, origin = LR.parse_emit(E)
print("parsed %d definitions in %.1f s" % (len(defs), time.time() - t))
widths = LR.register_widths(E)
print("register widths known: %d; x1=%s PC=%s misa=%s mstatus=%s f1=%s" % (len(widths), widths.get("x1"), widths.get("PC"), widths.get("misa"), widths.get("mstatus"), widths.get("f1")))
reader = LR.Reader(defs, widths)
machine = LR.Machine(widths)
for name in ("reset", "reset_misa", "reset_sys"):
    if name not in defs:
        print("no def", name); continue
    m2 = LR.machine_copy(machine)
    try:
        t = time.time()
        reader.call(name, [None], m2)
        print("%s () evaluated in %.1f s; registers written: %d; misa = %s" % (name, time.time() - t, len(m2.writes), z3.simplify(m2.registers["misa"]) if "misa" in m2.registers else "(untouched)"))
        machine = m2
        break
    except LR.ReadRefused as p:
        print("%s () REFUSED: %s" % (name, str(p)[:300]))
    except Exception as p:
        print("%s () FAILED: %s: %s" % (name, type(p).__name__, str(p)[:300]))
        traceback.print_exc(limit=3)
rows = json.load(open("PseudoCoupHQ/Research/oracle/riscv/carved.json"))["rows"]
lines = []
seen = set()
for row in rows:
    for line in row.get("body", [])[:1]:
        key = line.split()[0]
        if key in seen: continue
        seen.add(key); lines.append(line)
    if len(lines) >= 8: break
print("lines:", lines)
try:
    words = AS.words_of(lines, "/work/sl1e")
except AS.AssemblyRefused as p:
    print("ASSEMBLY REFUSED:", p); words = []
print("words:", [("0x%x" % w, n) for w, n in words])
for line, (word, size) in zip(lines, words):
    print("--- %s  word 0x%x (%d bytes)" % (line, word, size))
    m3 = LR.machine_copy(machine)
    try:
        t = time.time()
        if size == 4:
            instr = reader.call("encdec_backwards", [z3.BitVecVal(word, 32)], m3)
        else:
            instr = reader.call("encdec_compressed_backwards", [z3.BitVecVal(word, 16)], m3)
        print("   decoded in %.2f s: %r" % (time.time() - t, instr))
        t = time.time()
        result = reader.call("execute", [instr], m3)
        print("   executed in %.2f s: result %r" % (time.time() - t, result))
        for name, value in m3.writes[-6:]:
            if z3.is_bv(value):
                print("   wrote %s := %s" % (name, z3.simplify(value)))
            else:
                print("   wrote %s := %r" % (name, value))
    except LR.ReadRefused as p:
        print("   REFUSED:", str(p)[:400])
    except Exception as p:
        print("   FAILED: %s: %s" % (type(p).__name__, str(p)[:400]))
        traceback.print_exc(limit=4)
PYEOF
echo "[3/$total] done $(date -u +%FT%TZ)"
