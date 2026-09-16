#!/bin/bash
# sl1 lane 23 -- lane 22 again after the duplicate-name rule (a def outranks an abbrev of the same name: flen was read from the types file as 8). Lane 22: the bridged machine keeps writes in an overlay until the instruction ends (a copy keeps its class), and the softfloat externs of the model's FFI have z3 meanings by their shape. Lane 21 had the register rule changed: a register the model never wrote reads zero (the C simulator's start), the x and f registers and PC being the walk's own. Lane 20 had two reader fixes (the last arm of an
# exhaustive match is taken; the Sail library's shift functions in the
# primitive table), plus a diagnosis of why the float family is still
# illegal after the prologue: the extension checks and fcsr, evaluated.
set -u
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
mkdir -p /work/sl1f/work
export SL1_WORK=/work/sl1f/work
echo "[1/2] the float unit after reset and the prologue"
timeout 600 python3 - <<'PYEOF'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import z3, riscv_reference as RV, lean_reader as LR, lifter as GL
ref = RV.RiscvReference(); L = ref.lifter
for line in L.reset_report + L.prologue_report: print("  ", line[:200])
for name in ("flen", "xlen"):
    try: print("  %s = %s" % (name, L.reader.call(name, [], LR.Machine(L.widths))))
    except Exception as p: print("  %s FAILED %s" % (name, p))
m = LR.Machine(L.widths, dict(L.reset_registers))
try: print("  _get_Misa_D misa =", z3.simplify(L.reader.call("_get_Misa_D", [L.reset_registers["misa"]], m)))
except Exception as p: print("  _get_Misa_D FAILED", p)
for name in ("fcsr", "misa", "mstatus", "cur_privilege"):
    v = L.reset_registers.get(name); print("  %s = %s" % (name, z3.simplify(v) if z3.is_bv(v) else v))
for ext in ("Ext_F", "Ext_D", "Ext_M", "Ext_C", "Ext_Zca", "Ext_Zicond", "Ext_Zba"):
    m = LR.Machine(L.widths, dict(L.reset_registers))
    try:
        v = L.reader.call("currentlyEnabled", [LR.Ctor(ext, [])], m); print("  currentlyEnabled %s = %s" % (ext, z3.simplify(v) if z3.is_bool(v) else v))
    except LR.ReadRefused as p: print("  currentlyEnabled %s REFUSED %s" % (ext, str(p)[:200]))
st = RV.MachineState({})
for line in ("fmv.d.x fa0, a0", "fcvt.d.w fa5, a0", "fadd.s fa0, fa1, fa2", "czero.eqz a0, a0, a1", "flt.d a0, fa0, fa1"):
    try:
        w, s = L.words_of_lines([line])[0]; instr = L.decode(w, s); print("  %s -> %s" % (line, instr))
        result, machine = L.execute(instr, st); print("     result %s writes %s" % (GL.constructor_name(result), [n for n, _ in machine.writes][:6]))
    except Exception as p: print("  %s FAILED %s %s" % (line, type(p).__name__, str(p)[:300]))
PYEOF
echo "[2/2] the comparison again"
sed -n '/^timeout 1800 python3 - <<.PYEOF.$/,/^PYEOF$/p' $SL/lanes_sl1/sl1_l19_the_drop_in_tuple_fix.sh | sed '1d;$d' > /work/sl1f/compare.py
timeout 1800 python3 /work/sl1f/compare.py 2>&1 | grep -v "^  File\|^    \|^Traceback\|^During\|^$" | cut -c1-300
echo "done $(date -u +%FT%TZ)"
