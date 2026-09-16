#!/usr/bin/env python3
"""Turn each flattened single-block LLVM slice into ordinary SOURCE in c, c++,
rust and go.

Input   softfloat_slices/flattened/<op>.rm<N>.<variant>.flat.ll
Output  softfloat_slices/emulations/{c,cpp,rust,go}/<op>.{c,cpp,rs,go}

The flattened block is already SSA, already topologically ordered, already
branch-free, call-free and memory-free.  Emission is therefore a straight
one-instruction-to-one-statement walk; the only judgement calls are the
don't-care cases that LLVM spells "poison", and they are pinned here:

  * a shift whose amount is >= the operand width is taken MODULO the width,
    the same rule x86 and RISC-V hardware use, and the same rule rust's
    `wrapping_shl` uses.  In the flattened IR every such shift is followed by
    `freeze` and its result is masked away, so the choice is unobservable -
    but it is made identically in all four languages so it cannot diverge
    between them.
  * `llvm.ctlz(0)` is the bit width.  The IR asks for `is_zero_poison=true`
    and freezes the result; the flattener's own `range(i32 0, 33)` annotation
    already admits 32 as a possible answer, so bit width is the consistent
    reading.
  * `udiv` by zero yields zero.  The flattener already forces every divisor
    non-zero (`flattened.json: guarded_instructions`), so this never fires;
    it is present because rust and go panic rather than trap.
  * `freeze` is a plain copy.

No language's built-in is used where its edge case differs from LLVM's; see
`emulations/README.md` for the per-helper record.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
FLAT = os.path.join(BASE, "flattened")
OUT = os.environ.get("EMUL_OUT", os.path.join(BASE, "emulations"))

# EMUL_PIN=alt re-emits the C backend with the OPPOSITE reading of every
# don't-care: an over-wide shift yields zero instead of wrapping the amount,
# ctlz(0) yields 0 instead of the bit width, udiv by zero yields all-ones
# instead of zero.  scripts/pin_probe.sh runs that variant through the same
# SoftFloat test; agreement is what makes the pins unobservable rather than
# merely convenient.
ALT = os.environ.get("EMUL_PIN") == "alt"

WIDTH = {"i1": 1, "i8": 8, "i16": 16, "i32": 32, "i64": 64, "i128": 128}

BIN = {"and", "or", "xor", "add", "sub", "mul", "udiv", "shl", "lshr"}
CAST = {"trunc", "zext", "sext"}


# ----------------------------------------------------------------- parse ---
class Inst(object):
    __slots__ = ("dst", "op", "ty", "args", "extra")

    def __init__(self, dst, op, ty, args, extra=None):
        self.dst = dst        # destination ssa name, or None
        self.op = op          # llvm opcode, or intrinsic base name
        self.ty = ty          # result type for casts, operand type otherwise
        self.args = args      # list of (kind, value): ('v', name) | ('c', int)
        self.extra = extra    # icmp predicate, cast source type, ...


_RANGE = re.compile(r"range\(i\d+ -?\d+, -?\d+\)\s*")


def _operand(tok):
    tok = tok.strip()
    if tok.startswith("%"):
        return ("v", tok[1:])
    if tok == "true":
        return ("c", 1)
    if tok == "false":
        return ("c", 0)
    return ("c", int(tok, 0))


def parse(path):
    src = open(path).read()
    m = re.search(r"^define dso_local (.*?) @(\w+)\((.*?)\) \{$", src, re.M)
    if not m:
        raise ValueError("no define in " + path)
    rety, fname, plist = m.group(1), m.group(2), m.group(3)
    rety = rety.replace("zeroext", "").replace("signext", "").strip()
    params = []
    for p in plist.split(","):
        p = p.strip()
        if not p:
            continue
        pm = re.match(r"(i\d+)\s+(?:\w+\s+)*%([\w.]+)$", p)
        if not pm:
            raise ValueError("bad param %r in %s" % (p, path))
        params.append((pm.group(2), pm.group(1)))

    body = src[m.end():]
    body = body[:body.index("\n}\n")]
    insts, ret = [], None
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith("ret "):
            rm = re.match(r"ret (i\d+) (.*)$", line)
            ret = (rm.group(1), _operand(rm.group(2)))
            continue
        am = re.match(r"%([\w.]+) = (.*)$", line)
        if not am:
            raise ValueError("unhandled line %r in %s" % (line, path))
        dst, rhs = am.group(1), _RANGE.sub("", am.group(2))
        insts.append(_inst(dst, rhs, path))
    if ret is None:
        raise ValueError("no ret in " + path)
    return {"name": fname, "ret": rety, "params": params,
            "insts": insts, "retval": ret}


def _inst(dst, rhs, path):
    w = rhs.split(None, 1)
    opc = w[0]
    rest = w[1] if len(w) > 1 else ""
    if opc in BIN:
        mm = re.match(r"(i\d+) (\S+), (\S+)$", rest)
        return Inst(dst, opc, mm.group(1),
                    [_operand(mm.group(2)), _operand(mm.group(3))])
    if opc in CAST:
        mm = re.match(r"(?:nneg )?(i\d+) (\S+) to (i\d+)$", rest)
        return Inst(dst, opc, mm.group(3), [_operand(mm.group(2))],
                    mm.group(1))
    if opc == "freeze":
        mm = re.match(r"(i\d+) (\S+)$", rest)
        return Inst(dst, "freeze", mm.group(1), [_operand(mm.group(2))])
    if opc == "icmp":
        mm = re.match(r"(\w+) (i\d+) (\S+), (\S+)$", rest)
        return Inst(dst, "icmp", mm.group(2),
                    [_operand(mm.group(3)), _operand(mm.group(4))],
                    mm.group(1))
    if opc == "call":
        mm = re.match(r"(i\d+) @llvm\.([\w.]+)\((.*)\)$", rest)
        if not mm:
            raise ValueError("bad call %r in %s" % (rhs, path))
        ity, iname = mm.group(1), mm.group(2)
        args = []
        for a in mm.group(3).split(","):
            a = _RANGE.sub("", a.strip())
            args.append(_operand(a.split(None, 1)[1]))
        base = iname.rsplit(".", 1)[0]          # ctlz.i32 -> ctlz
        return Inst(dst, "@" + base, ity, args)
    raise ValueError("unknown opcode %r in %s" % (opc, path))


def dce(fn):
    """Drop instructions nothing reaches.  Every opcode here is pure."""
    live = set()
    if fn["retval"][1][0] == "v":
        live.add(fn["retval"][1][1])
    keep = []
    for ins in reversed(fn["insts"]):
        if ins.dst not in live:
            continue
        keep.append(ins)
        for k, v in ins.args:
            if k == "v":
                live.add(v)
    keep.reverse()
    fn["insts"] = keep
    return fn


# ------------------------------------------------------------- utilities ---
def mask(w):
    return (1 << w) - 1


def uconst(k, w):
    return k & mask(w)


def signed(k, w):
    v = k & mask(w)
    return v - (1 << w) if v >> (w - 1) else v


def sanitize(name):
    s = re.sub(r"[^A-Za-z0-9_]", "_", name)
    return "v_" + s


# ------------------------------------------------------------------- C/C++ -
C_UT = {1: "bool", 8: "uint8_t", 16: "uint16_t", 32: "uint32_t",
        64: "uint64_t", 128: "sf_u128"}
C_ST = {8: "int8_t", 16: "int16_t", 32: "int32_t", 64: "int64_t",
        128: "sf_i128"}


def c_lit(k, w):
    if w == 1:
        return "true" if k else "false"
    v = uconst(k, w)
    if w <= 32:
        return "UINT32_C(0x%x)" % v
    if w == 64:
        return "UINT64_C(0x%x)" % v
    return "sf_u128_of(UINT64_C(0x%x), UINT64_C(0x%x))" % (v >> 64,
                                                           v & mask(64))


class CBackend(object):
    lang = "c"
    ext = "c"
    header = '#include "sfemul.h"\n'

    def __init__(self):
        if ALT:
            self.header = '#include "sfemul_altpin.h"\n'

    def ut(self, w):
        return C_UT[w]

    def lit(self, k, w):
        return c_lit(k, w)

    def val(self, a, w):
        return sanitize(a[1]) if a[0] == "v" else self.lit(a[1], w)

    def wants_sval(self, pred, w):
        return pred[0] == "s" and w != 128

    def sval(self, a, w):
        """An operand in a SIGNED context."""
        if a[0] == "v":
            return "(%s)(%s)" % (C_ST[w], sanitize(a[1]))
        k = signed(a[1], w)
        return "%s(%d)" % ("INT32_C" if w <= 32 else "INT64_C", k)

    def fn_open(self, fn, rw, params):
        args = ", ".join("%s %s" % (self.ut(w), sanitize(n))
                         for n, w in params)
        return "%s %s(%s)\n{" % (self.ut(rw), fn, args or "void")

    def decl(self, ty, name, expr):
        return "    const %s %s = %s;" % (ty, name, expr)

    def ret(self, e):
        return "    return %s;\n}" % e

    def binop(self, op, w, x, y):
        t, u = self.ut(w), self.ut(w)
        if w == 1:
            return {"and": "(%s && %s)", "or": "(%s || %s)",
                    "xor": "(%s != %s)"}[op] % (x, y)
        if w == 128:
            return "sf_u128_%s(%s, %s)" % (op, x, y)
        sym = {"and": "&", "or": "|", "xor": "^", "add": "+", "sub": "-",
               "mul": "*"}.get(op)
        if sym:
            return "(%s)(%s %s %s)" % (t, x, sym, y)
        if op == "udiv":
            return "sf_udiv%d%s(%s, %s)" % (w, "_alt" if ALT else "", x, y)
        if ALT and op in ("shl", "lshr"):
            return "sf_%s%d_alt(%s, %s)" % (op, w, x, y)
        if op == "shl":
            return "(%s)((%s)(%s) << ((%s) & %d))" % (t, u, x, y, w - 1)
        if op == "lshr":
            return "(%s)((%s)(%s) >> ((%s) & %d))" % (t, u, x, y, w - 1)
        raise ValueError(op)

    def cast(self, op, sw, dw, x):
        if op == "trunc":
            if sw == 128:
                return "sf_u128_lo%d(%s)" % (dw, x)
            if dw == 1:
                return "(bool)((%s) & 1)" % x
            return "(%s)(%s)" % (self.ut(dw), x)
        if op == "zext":
            if dw == 128:
                return "sf_u128_of(0, (uint64_t)(%s))" % x
            if sw == 1:
                return "(%s)((%s) ? 1 : 0)" % (self.ut(dw), x)
            return "(%s)(%s)" % (self.ut(dw), x)
        if op == "sext":
            if sw == 1:
                if dw == 128:
                    return "sf_u128_sext1(%s)" % x
                return "(%s)((%s) ? ~(%s)0 : (%s)0)" % (
                    self.ut(dw), x, self.ut(dw), self.ut(dw))
            if dw == 128:
                return "sf_u128_sext64((uint64_t)(%s))" % x
            return "(%s)(%s)(%s)(%s)" % (self.ut(dw), C_ST[dw], C_ST[sw], x)
        raise ValueError(op)

    def icmp(self, pred, w, x, y):
        if pred in ("eq", "ne"):
            if w == 128:
                return "(%ssf_u128_eq(%s, %s))" % (
                    "" if pred == "eq" else "!", x, y)
            return "(%s %s %s)" % (x, "==" if pred == "eq" else "!=", y)
        sym = {"ult": "<", "ule": "<=", "ugt": ">", "uge": ">=",
               "slt": "<", "sle": "<=", "sgt": ">", "sge": ">="}[pred]
        if pred[0] == "u":
            if w == 128:
                return "(sf_u128_ucmp(%s, %s) %s 0)" % (x, y, sym)
            return "(%s %s %s)" % (x, sym, y)
        if w == 128:
            return "(sf_u128_scmp(%s, %s) %s 0)" % (x, y, sym)
        return "(%s %s %s)" % (x, sym, y)

    def intrinsic(self, base, w, args):
        if base == "ctlz":
            return "sf_ctlz%d%s(%s)" % (w, "_alt" if ALT else "", args[0])
        if base == "abs":
            return "sf_abs%d(%s)" % (w, args[0])
        if base == "usub.sat":
            return "sf_usubsat%d(%s, %s)" % (w, args[0], args[1])
        if base == "fshl":
            return "sf_fshl%d(%s, %s, %s)" % (w, args[0], args[1], args[2])
        raise ValueError(base)


class CppBackend(CBackend):
    lang = "cpp"
    ext = "cpp"
    header = '#include "sfemul.hpp"\n\nnamespace sfemul {\n'

    def ret(self, e):
        return "    return %s;\n}\n\n}  // namespace sfemul" % e


# -------------------------------------------------------------------- Rust -
R_UT = {1: "bool", 8: "u8", 16: "u16", 32: "u32", 64: "u64", 128: "u128"}
R_ST = {8: "i8", 16: "i16", 32: "i32", 64: "i64", 128: "i128"}


class RustBackend(object):
    lang = "rust"
    ext = "rs"
    header = ("#![allow(non_snake_case, unused_parens, unused_imports, "
              "unused_variables, unused_comparisons, clippy::all)]\n"
              "use crate::helpers::*;\n")

    def ut(self, w):
        return R_UT[w]

    def lit(self, k, w):
        if w == 1:
            return "true" if k else "false"
        return "0x%x%s" % (uconst(k, w), R_UT[w])

    def val(self, a, w):
        return sanitize(a[1]) if a[0] == "v" else self.lit(a[1], w)

    def wants_sval(self, pred, w):
        return pred[0] == "s"          # rust has a native i128

    def sval(self, a, w):
        if a[0] == "v":
            return "((%s) as %s)" % (sanitize(a[1]), R_ST[w])
        return "(%d%s)" % (signed(a[1], w), R_ST[w])

    def fn_open(self, fn, rw, params):
        args = ", ".join("%s: %s" % (sanitize(n), self.ut(w))
                         for n, w in params)
        return "pub fn %s(%s) -> %s {" % (fn, args, self.ut(rw))

    def decl(self, ty, name, expr):
        return "    let %s: %s = %s;" % (name, ty, expr)

    def ret(self, e):
        return "    %s\n}" % e

    def binop(self, op, w, x, y):
        if w == 1:
            return {"and": "(%s & %s)", "or": "(%s | %s)",
                    "xor": "(%s ^ %s)"}[op] % (x, y)
        sym = {"and": "&", "or": "|", "xor": "^"}.get(op)
        if sym:
            return "(%s %s %s)" % (x, sym, y)
        if op in ("add", "sub", "mul"):
            return "%s.wrapping_%s(%s)" % (x, op, y)
        if op == "udiv":
            return "sf_udiv_%s(%s, %s)" % (R_UT[w], x, y)
        if op == "shl":
            return "%s.wrapping_shl((%s) as u32)" % (x, y)
        if op == "lshr":
            return "%s.wrapping_shr((%s) as u32)" % (x, y)
        raise ValueError(op)

    def cast(self, op, sw, dw, x):
        if op == "trunc":
            if dw == 1:
                return "(((%s) & 1) != 0)" % x
            return "((%s) as %s)" % (x, R_UT[dw])
        if op == "zext":
            return "((%s) as %s)" % (x, R_UT[dw])
        if op == "sext":
            if sw == 1:
                return "(0%s.wrapping_sub((%s) as %s))" % (
                    R_UT[dw], x, R_UT[dw])
            return "(((%s) as %s) as %s as %s)" % (x, R_ST[sw], R_ST[dw],
                                                   R_UT[dw])
        raise ValueError(op)

    def icmp(self, pred, w, x, y):
        sym = {"eq": "==", "ne": "!=", "ult": "<", "ule": "<=", "ugt": ">",
               "uge": ">=", "slt": "<", "sle": "<=", "sgt": ">", "sge": ">="}
        return "(%s %s %s)" % (x, sym[pred], y)

    def intrinsic(self, base, w, args):
        if base == "ctlz":
            return "sf_ctlz_%s(%s)" % (R_UT[w], args[0])
        if base == "abs":
            return "sf_abs_%s(%s)" % (R_UT[w], args[0])
        if base == "usub.sat":
            return "sf_usubsat_%s(%s, %s)" % (R_UT[w], args[0], args[1])
        if base == "fshl":
            return "sf_fshl_%s(%s, %s, %s)" % (R_UT[w], args[0], args[1],
                                               args[2])
        raise ValueError(base)


# ---------------------------------------------------------------------- Go -
G_UT = {1: "bool", 8: "uint8", 16: "uint16", 32: "uint32", 64: "uint64",
        128: "U128"}
G_ST = {8: "int8", 16: "int16", 32: "int32", 64: "int64"}


class GoBackend(object):
    lang = "go"
    ext = "go"
    header = "package emul\n"

    def ut(self, w):
        return G_UT[w]

    def lit(self, k, w):
        if w == 1:
            return "true" if k else "false"
        if w == 128:
            v = uconst(k, w)
            return "U128{0x%x, 0x%x}" % (v >> 64, v & mask(64))
        return "%s(0x%x)" % (G_UT[w], uconst(k, w))

    def val(self, a, w):
        return sanitize(a[1]) if a[0] == "v" else self.lit(a[1], w)

    def wants_sval(self, pred, w):
        return pred[0] == "s" and w != 128

    def sval(self, a, w):
        if a[0] == "v":
            return "%s(%s)" % (G_ST[w], sanitize(a[1]))
        return "%s(%d)" % (G_ST[w], signed(a[1], w))

    def fn_open(self, fn, rw, params):
        args = ", ".join("%s %s" % (sanitize(n), self.ut(w))
                         for n, w in params)
        return "func %s(%s) %s {" % (fn, args, self.ut(rw))

    def decl(self, ty, name, expr):
        return "\tvar %s %s = %s" % (name, ty, expr)

    def ret(self, e):
        return "\treturn %s\n}" % e

    def binop(self, op, w, x, y):
        if w == 1:
            return {"and": "(%s && %s)", "or": "(%s || %s)",
                    "xor": "(%s != %s)"}[op] % (x, y)
        if w == 128:
            return "u128%s(%s, %s)" % (op.capitalize(), x, y)
        sym = {"and": "&", "or": "|", "xor": "^", "add": "+", "sub": "-",
               "mul": "*"}.get(op)
        if sym:
            return "(%s %s %s)" % (x, sym, y)
        if op == "udiv":
            return "sfUdiv%d(%s, %s)" % (w, x, y)
        if op in ("shl", "lshr"):
            arrow = "<<" if op == "shl" else ">>"
            return "(%s %s ((%s) & %d))" % (x, arrow, y, w - 1)
        raise ValueError(op)

    def cast(self, op, sw, dw, x):
        if op == "trunc":
            if sw == 128:
                return "u128Lo%d(%s)" % (dw, x)
            if dw == 1:
                return "((%s & 1) != 0)" % x
            return "%s(%s)" % (G_UT[dw], x)
        if op == "zext":
            if dw == 128:
                return "U128{0, uint64(%s)}" % x
            if sw == 1:
                return "sfB2u%d(%s)" % (dw, x)
            return "%s(%s)" % (G_UT[dw], x)
        if op == "sext":
            if sw == 1:
                if dw == 128:
                    return "u128Sext1(%s)" % x
                return "sfSext1u%d(%s)" % (dw, x)
            if dw == 128:
                return "u128Sext64(uint64(%s))" % x
            return "%s(%s(%s(%s)))" % (G_UT[dw], G_ST[dw], G_ST[sw], x)
        raise ValueError(op)

    def icmp(self, pred, w, x, y):
        sym = {"eq": "==", "ne": "!=", "ult": "<", "ule": "<=", "ugt": ">",
               "uge": ">=", "slt": "<", "sle": "<=", "sgt": ">", "sge": ">="}
        if w == 128:
            if pred in ("eq", "ne"):
                return "(u128Eq(%s, %s) %s true)" % (
                    x, y, "==" if pred == "eq" else "!=")
            if pred[0] == "u":
                return "(u128Ucmp(%s, %s) %s 0)" % (x, y, sym[pred])
            return "(u128Scmp(%s, %s) %s 0)" % (x, y, sym[pred])
        return "(%s %s %s)" % (x, sym[pred], y)

    def intrinsic(self, base, w, args):
        if base == "ctlz":
            return "sfCtlz%d(%s)" % (w, args[0])
        if base == "abs":
            return "sfAbs%d(%s)" % (w, args[0])
        if base == "usub.sat":
            return "sfUsubsat%d(%s, %s)" % (w, args[0], args[1])
        if base == "fshl":
            return "sfFshl%d(%s, %s, %s)" % (w, args[0], args[1], args[2])
        raise ValueError(base)


BACKENDS = ([CBackend()] if ALT
            else [CBackend(), CppBackend(), RustBackend(), GoBackend()])


# ------------------------------------------------------------------ emit ---
def emit(fn, be, entry):
    ty = {}
    for n, t in fn["params"]:
        ty[n] = WIDTH[t]
    lines = [be.header, ""]
    lines.append(be.fn_open(entry, WIDTH[fn["ret"]],
                            [(n, WIDTH[t]) for n, t in fn["params"]]))
    for ins in fn["insts"]:
        w = WIDTH[ins.ty]
        if ins.op in BIN:
            rw = w
            e = be.binop(ins.op, w, be.val(ins.args[0], w),
                         be.val(ins.args[1], w))
        elif ins.op in CAST:
            sw = WIDTH[ins.extra]
            rw = w
            e = be.cast(ins.op, sw, rw, be.val(ins.args[0], sw))
        elif ins.op == "freeze":
            rw = w
            e = be.val(ins.args[0], w)
        elif ins.op == "icmp":
            rw = 1
            rend = be.sval if be.wants_sval(ins.extra, w) else be.val
            e = be.icmp(ins.extra, w, rend(ins.args[0], w),
                        rend(ins.args[1], w))
        elif ins.op.startswith("@"):
            base = ins.op[1:]
            rw = w
            if base == "ctlz":
                e = be.intrinsic(base, w, [be.val(ins.args[0], w)])
            elif base == "abs":
                e = be.intrinsic(base, w, [be.val(ins.args[0], w)])
            elif base == "usub.sat":
                e = be.intrinsic(base, w, [be.val(ins.args[0], w),
                                           be.val(ins.args[1], w)])
            elif base == "fshl":
                e = be.intrinsic(base, w, [be.val(ins.args[0], w),
                                           be.val(ins.args[1], w),
                                           be.val(ins.args[2], w)])
            else:
                raise ValueError(base)
        else:
            raise ValueError(ins.op)
        ty[ins.dst] = rw
        lines.append(be.decl(be.ut(rw), sanitize(ins.dst), e))
    rw = WIDTH[fn["ret"]]
    lines.append(be.ret(be.val(fn["retval"][1], rw)))
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ main ---
def op_files(mode, variant):
    out = []
    for f in sorted(os.listdir(FLAT)):
        if f.endswith(".rm%d.%s.flat.ll" % (mode, variant)):
            out.append((f.split(".")[0], os.path.join(FLAT, f)))
    return out


def main():
    mode = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    variant = sys.argv[2] if len(sys.argv) > 2 else "value"
    recs = {}
    for op, path in op_files(mode, variant):
        fn = dce(parse(path))
        entry = "%s_rm%d" % (op, mode)
        widths = set()
        opcodes = set()
        intr = set()
        for ins in fn["insts"]:
            widths.add(WIDTH[ins.ty])
            if ins.op in CAST:
                widths.add(WIDTH[ins.extra])
            if ins.op.startswith("@"):
                intr.add(ins.op[1:] + ".i%d" % WIDTH[ins.ty])
                opcodes.add("call")
            elif ins.op == "icmp":
                opcodes.add("icmp." + ins.extra)
            else:
                opcodes.add(ins.op)
        rec = {"operation": op, "mode": mode, "variant": variant,
               "ir_instructions": len(fn["insts"]),
               "opcodes": sorted(opcodes), "intrinsics": sorted(intr),
               "widths": sorted(widths), "i128": 128 in widths,
               "languages": {}}
        for be in BACKENDS:
            os.makedirs(os.path.join(OUT, be.lang), exist_ok=True)
            name = entry
            if be.lang == "go":
                name = "Emu_" + entry
            text = emit(fn, be, name)
            dst = os.path.join(OUT, be.lang, "%s.%s" % (op, be.ext))
            open(dst, "w").write(text)
            rec["languages"][be.lang] = {
                "file": os.path.relpath(dst, BASE),
                "entry": name,
                "lines": text.count("\n"),
            }
        rec["signature"] = {
            "params": [WIDTH[t] for _, t in fn["params"]],
            "ret": WIDTH[fn["ret"]],
        }
        recs[op] = rec
        print("%-16s %4d insts  %s" % (op, len(fn["insts"]),
                                       "i128" if rec["i128"] else ""))
    write_glue(recs, mode)
    json.dump(recs, open(os.path.join(OUT, "_emitted.json"), "w"), indent=1)
    print("emitted %d operations x 4 languages" % len(recs))


def write_glue(recs, mode):
    """The one-per-language module wiring: declarations for c and c++, the
    crate root for rust, the module file for go."""
    ops = sorted(recs)
    have = set(recs[ops[0]]["languages"])

    def csig(rec, lang, cty):
        s = rec["signature"]
        args = ", ".join(cty[w] for w in s["params"]) or "void"
        return "%s %s(%s);" % (cty[s["ret"]], rec["languages"][lang]["entry"],
                               args)

    h = ["/* generated by scripts/emit_emulations.py */",
         "#ifndef SFEMUL_DECLS_H", "#define SFEMUL_DECLS_H", ""]
    for op in ops:
        h.append(csig(recs[op], "c", C_UT))
    h += ["", "#endif"]
    open(os.path.join(OUT, "c", "sfemul_decls.h"), "w").write("\n".join(h)
                                                              + "\n")

    if "cpp" not in have:
        return
    hp = ["// generated by scripts/emit_emulations.py",
          "#ifndef SFEMUL_DECLS_HPP", "#define SFEMUL_DECLS_HPP", "",
          "namespace sfemul {"]
    for op in ops:
        hp.append(csig(recs[op], "cpp", C_UT))
    hp += ["}  // namespace sfemul", "", "#endif"]
    open(os.path.join(OUT, "cpp", "sfemul_decls.hpp"),
         "w").write("\n".join(hp) + "\n")

    lib = ["//! RISC-V float arch-opcodes as ordinary integer rust.",
           "//! Generated by scripts/emit_emulations.py.",
           "#![allow(non_snake_case)]", "", "pub mod helpers;", ""]
    for op in ops:
        lib.append('#[path = "%s.rs"]' % op)
        lib.append("pub mod %s;" % op)
    open(os.path.join(OUT, "rust", "lib.rs"), "w").write("\n".join(lib) + "\n")

    open(os.path.join(OUT, "go", "go.mod"), "w").write(
        "module softfloat_emul\n\ngo 1.21\n")

    idx = {op: {lang: recs[op]["languages"][lang]["entry"]
                for lang in ("c", "cpp", "rust", "go")} for op in ops}
    json.dump({"mode": mode, "entries": idx},
              open(os.path.join(OUT, "_index.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
