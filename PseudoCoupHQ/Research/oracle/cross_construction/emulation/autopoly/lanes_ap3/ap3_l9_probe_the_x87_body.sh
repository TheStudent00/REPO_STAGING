#!/usr/bin/env bash
# ap3_l9_probe_the_x87_body.sh -- task ap3: WHY the gate says the c body
# of an x87 cell "carries no body", asked of the object.
#
# Lane `ap3_l8` measured fix 2: the c rows RENDER (`long double
# emu_faddl(long double a, long double b) { return a + b; }`), COMPILE,
# and carve to `fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret`
# -- the x87 opcode the cell names.  The gate then answers UNDECIDED
# with `the carved body: the reference: this unit record carries no
# body`, which is `reference.body_lines` on a `body_verbatim` of None:
# the canonical form did not put the body on the record.  This lane
# prints the canonical-form record for one such body, field by field,
# so the cause is read rather than reasoned about.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
import autopoly3 as A
import handful as H
import emulate as E

A.use_task_ap3()
cells = A.read_json(A.CELLS)
shared = H.build_shared()
held = H.cell_input(cells, ("faddl", "mem_one", 80))
place = held["places"][0]
label = "ap3_probe_faddl"
built = H.render_one_place(place, "c", label, write=False)
print("rendered: %s" % built.get("rendered"))
got, refusal = H.compile_one_place(built["source"], built["symbol"], "c")
raw_bytes, mnem = got
print("the carved body, LITERAL: %s" % "; ".join(mnem))
recorded = E.recorded_facts("c/%s" % label, label, raw_bytes, mnem)
print("")
print("recorded_facts keys: %s" % sorted(recorded))
for name in sorted(recorded):
    value = recorded[name]
    text = repr(value)
    if len(text) > 300:
        text = text[:300] + " ..."
    print("   %-32s %s" % (name, text))
canon = H.wrapped_body(shared, raw_bytes, mnem, label, "c")
print("")
print("the canonical-form record's keys: %s" % sorted(canon))
for name in sorted(canon):
    value = canon[name]
    text = repr(value)
    if len(text) > 400:
        text = text[:400] + " ..."
    print("   %-32s %s" % (name, text))
print("")
print("body_verbatim: %r" % canon.get("body_verbatim"))
print("canon40 outcome: %r" % canon.get("outcome"))
PY
echo "done"
