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

BIN = {"and", "or", "xor", "add", "sub", "mul", "udiv", "shl", "lshr",
       "ashr"}
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
    insts, ret, agg = [], None, {}
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        if line.startswith("ret "):
            rm = re.match(r"ret (i\d+) (.*)$", line)
            if rm:
                ret = (rm.group(1), _operand(rm.group(2)))
                continue
            # The `flags` variant returns C's { uint8_t flags; T v; }.  When
            # that struct needs two words the lp64 ABI returns it as an
            # array, and the fflags byte is element 0.  Take that element:
            # dce() then drops everything only the value element reached.
            ar = re.match(r"ret \[\d+ x (i\d+)\] %([\w.]+)$", line)
            if not ar:
                raise ValueError("unhandled ret %r in %s" % (line, path))
            ret = (ar.group(1), agg[ar.group(2)][0])
            continue
        am = re.match(r"%([\w.]+) = (.*)$", line)
        if not am:
            raise ValueError("unhandled line %r in %s" % (line, path))
        dst, rhs = am.group(1), _RANGE.sub("", am.group(2))
        if rhs.startswith("insertvalue"):
            im = re.match(r"insertvalue \[\d+ x i\d+\] (.*), i\d+ (\S+), (\d+)$",
                          rhs)
            if not im:
                raise ValueError("bad insertvalue %r in %s" % (rhs, path))
            agg[dst] = _agg_base(im.group(1), agg, path)
            agg[dst][int(im.group(3))] = _operand(im.group(2))
            continue
        insts.append(_inst(dst, rhs, path))
    if ret is None:
        raise ValueError("no ret in " + path)
    if rety.startswith("["):
        rety = ret[0]
    return {"name": fname, "ret": rety, "params": params,
            "insts": insts, "retval": ret}


def _agg_base(tok, agg, path):
    """The value an insertvalue builds on: a previous aggregate, an all-poison
    one, or a literal array whose settled elements are already constants."""
    tok = tok.strip()
    if tok in ("poison", "undef", "zeroinitializer"):
        return {} if tok != "zeroinitializer" else {}
    if tok.startswith("%"):
        return dict(agg[tok[1:]])
    lm = re.match(r"\[(.*)\]$", tok)
    if not lm:
        raise ValueError("bad aggregate base %r in %s" % (tok, path))
    slots = {}
    for i, el in enumerate(lm.group(1).split(",")):
        el = el.strip().split(None, 1)
        if len(el) == 2 and el[1] not in ("poison", "undef"):
            slots[i] = _operand(el[1])
    return slots


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


# ------------------------------------------------- the masked-integer three -
# python, ruby and javascript share one representation and differ only in
# spelling.  Every value is a NON-NEGATIVE unbounded integer (a `BigInt` in
# javascript) held to its width by an EXPLICIT MASK.  The mask is the only
# thing that makes a width mean anything in these languages, so it rides on
# every result that can leave the width -- add, sub, mul, shl, trunc -- and is
# omitted, deliberately, where it cannot: and, or, xor and lshr of in-range
# operands are in range already.
#
# Width 1 is the integer 0 or 1, not a boolean, so `and`, `or` and `xor` are
# the same three symbols at every width; `icmp` therefore has to CONVERT its
# boolean result, which each backend does in its own spelling.  Width 128
# costs nothing here: it is the same unbounded integer with a wider mask.
#
# The don't-care pins of the module docstring are honoured by the helpers, not
# by the language: `sf_udiv` answers zero on a zero divisor, `sf_ctlz` answers
# the bit width on zero, and a shift takes its amount modulo the width.


class _MaskedBackend(object):
    """Shared shape for the three unbounded-integer languages."""
    # per-language spelling, set by the subclass
    fmt_and, fmt_or, fmt_xor = "(%s & %s)", "(%s | %s)", "(%s ^ %s)"
    suffix = ""                       # "n" for javascript BigInt literals
    cast_int = "%s"                   # how a python int becomes this language's

    def ut(self, w):
        return self.UT

    def lit(self, k, w):
        return "0x%x%s" % (uconst(k, w), self.suffix)

    def val(self, a, w):
        return sanitize(a[1]) if a[0] == "v" else self.lit(a[1], w)

    def wants_sval(self, pred, w):
        return pred[0] == "s"

    def binop(self, op, w, x, y):
        m = self.lit(mask(w), w if w != 128 else 128)
        if op in ("and", "or", "xor"):
            # cannot leave the width; no mask
            return {"and": self.fmt_and, "or": self.fmt_or,
                    "xor": self.fmt_xor}[op] % (x, y)
        if op in ("add", "sub", "mul"):
            return "((%s %s %s) & %s)" % (x, {"add": "+", "sub": "-",
                                              "mul": "*"}[op], y, m)
        if op == "udiv":
            return "%s(%s, %s)" % (self.H["udiv"], x, y)
        if op == "shl":
            return "((%s << (%s & 0x%x%s)) & %s)" % (x, y, w - 1,
                                                     self.suffix, m)
        if op == "lshr":
            return "(%s >> (%s & 0x%x%s))" % (x, y, w - 1, self.suffix)
        raise ValueError(op)

    def cast(self, op, sw, dw, x):
        if op == "trunc":
            return "(%s & %s)" % (x, self.lit(mask(dw), dw))
        if op == "zext":
            return "(%s)" % x
        if op == "sext":
            return "(%s(%s, 0x%x%s) & %s)" % (self.H["sgn"], x, sw,
                                              self.suffix, self.lit(mask(dw), dw))
        raise ValueError(op)

    def sval(self, a, w):
        if a[0] == "v":
            return "%s(%s, 0x%x%s)" % (self.H["sgn"], sanitize(a[1]), w,
                                       self.suffix)
        k = signed(a[1], w)
        return "(%s%d%s)" % ("-" if k < 0 else "", abs(k), self.suffix)

    def intrinsic(self, base, w, args):
        if base == "ctlz":
            return "%s(%s, 0x%x%s)" % (self.H["ctlz"], args[0], w, self.suffix)
        if base == "abs":
            return "%s(%s, 0x%x%s)" % (self.H["abs"], args[0], w, self.suffix)
        if base == "usub.sat":
            return "%s(%s, %s)" % (self.H["usubsat"], args[0], args[1])
        if base == "fshl":
            return "%s(%s, %s, %s, 0x%x%s)" % (self.H["fshl"], args[0],
                                               args[1], args[2], w,
                                               self.suffix)
        raise ValueError(base)


# --------------------------------------------------------------- Python ----
class PythonBackend(_MaskedBackend):
    lang = "python"
    ext = "py"
    UT = "int"
    header = ("from helpers import (sf_udiv, sf_sgn, sf_ctlz, sf_abs,\n"
              "                     sf_usubsat, sf_fshl)\n")
    H = {"udiv": "sf_udiv", "sgn": "sf_sgn", "ctlz": "sf_ctlz",
         "abs": "sf_abs", "usubsat": "sf_usubsat", "fshl": "sf_fshl"}

    def fn_open(self, fn, rw, params):
        return "def %s(%s):" % (fn, ", ".join(sanitize(n) for n, _ in params))

    def decl(self, ty, name, expr):
        return "    %s = %s" % (name, expr)

    def ret(self, e):
        return "    return %s" % e

    def icmp(self, pred, w, x, y):
        sym = {"eq": "==", "ne": "!=", "ult": "<", "ule": "<=", "ugt": ">",
               "uge": ">=", "slt": "<", "sle": "<=", "sgt": ">", "sge": ">="}
        return "(1 if %s %s %s else 0)" % (x, sym[pred], y)


# ----------------------------------------------------------------- Ruby ----
class RubyBackend(_MaskedBackend):
    lang = "ruby"
    ext = "rb"
    UT = "Integer"
    header = "require_relative 'helpers'\n"
    H = {"udiv": "sf_udiv", "sgn": "sf_sgn", "ctlz": "sf_ctlz",
         "abs": "sf_abs", "usubsat": "sf_usubsat", "fshl": "sf_fshl"}

    def fn_open(self, fn, rw, params):
        return "def %s(%s)" % (fn, ", ".join(sanitize(n) for n, _ in params))

    def decl(self, ty, name, expr):
        return "  %s = %s" % (name, expr)

    def ret(self, e):
        return "  %s\nend" % e

    def icmp(self, pred, w, x, y):
        sym = {"eq": "==", "ne": "!=", "ult": "<", "ule": "<=", "ugt": ">",
               "uge": ">=", "slt": "<", "sle": "<=", "sgt": ">", "sge": ">="}
        return "((%s %s %s) ? 1 : 0)" % (x, sym[pred], y)


# ----------------------------------------------------------- JavaScript ----
# BigInt, not Number: a Number is an IEEE double and loses the low bits of a
# 64-bit value, which is precisely what these slices carry.  Every literal
# therefore ends in `n` and every operand stays a BigInt end to end.
class JsBackend(_MaskedBackend):
    lang = "js"
    ext = "js"
    UT = "BigInt"
    suffix = "n"
    header = ("'use strict';\n"
              "const { sfUdiv, sfSgn, sfCtlz, sfAbs, sfUsubsat, sfFshl }"
              " = require('./helpers.js');\n")
    H = {"udiv": "sfUdiv", "sgn": "sfSgn", "ctlz": "sfCtlz",
         "abs": "sfAbs", "usubsat": "sfUsubsat", "fshl": "sfFshl"}

    def fn_open(self, fn, rw, params):
        self._fn = fn
        return "function %s(%s) {" % (fn, ", ".join(sanitize(n)
                                                    for n, _ in params))

    def decl(self, ty, name, expr):
        return "  const %s = %s;" % (name, expr)

    def ret(self, e):
        return "  return %s;\n}\nmodule.exports = { %s };" % (e, self._fn)

    def icmp(self, pred, w, x, y):
        sym = {"eq": "===", "ne": "!==", "ult": "<", "ule": "<=", "ugt": ">",
               "uge": ">=", "slt": "<", "sle": "<=", "sgt": ">", "sge": ">="}
        return "((%s %s %s) ? 1n : 0n)" % (x, sym[pred], y)


# ----------------------------------------------------------------- Java ----
# The one language here with fixed widths and NO unsigned type.  A value is
# kept as its BIT PATTERN in the natural signed container -- `boolean` at 1,
# `int` at 8, 16 and 32, `long` at 64 -- and unsignedness lives in the
# OPERATIONS, not in the type:
#
#   * at 8 and 16 the pattern is held non-negative by a mask after every
#     arithmetic result, so an unsigned compare is the ordinary `<`;
#   * at 32 and 64 two's-complement wrap already IS arithmetic modulo 2^w, so
#     add, sub and mul need no mask -- but `<` would read the sign bit, so
#     every unsigned compare goes through `Integer.compareUnsigned` /
#     `Long.compareUnsigned` and every logical right shift through `>>>`;
#   * a SIGNED compare at 8 or 16 must first sign-extend out of the masked
#     pattern (`Sf.s8`, `Sf.s16`); at 32 and 64 the pattern is the signed
#     value already.
#
# Java's shift count is taken modulo the operand width by the language itself,
# which is the same rule this emitter pins, and the `& (w-1)` is written
# anyway so the source says what it means at 8 and 16 too.  A `long` shift
# takes an `int` count, hence the cast.
J_UT = {1: "boolean", 8: "int", 16: "int", 32: "int", 64: "long",
        128: "Sf.U128"}


class JavaBackend(object):
    lang = "java"
    ext = "java"
    header = ""          # no imports: the helpers are `Sf.*`, same directory

    def ut(self, w):
        return J_UT[w]

    def lit(self, k, w):
        v = uconst(k, w)
        if w == 1:
            return "true" if k else "false"
        if w == 128:
            return "Sf.u128(0x%xL, 0x%xL)" % (v >> 64, v & mask(64))
        if w == 64:
            return "0x%xL" % v
        return "0x%x" % v        # hex int literals may set the sign bit

    def val(self, a, w):
        return sanitize(a[1]) if a[0] == "v" else self.lit(a[1], w)

    def wants_sval(self, pred, w):
        return pred[0] == "s" and w != 128

    def sval(self, a, w):
        """An operand read as SIGNED.  At 32 and 64 the pattern already is."""
        if a[0] == "v":
            v = sanitize(a[1])
            return "Sf.s%d(%s)" % (w, v) if w in (8, 16) else v
        k = signed(a[1], w)
        return "%dL" % k if w == 64 else "(%d)" % k

    def fn_open(self, fn, rw, params):
        # the class name is the FILE name, which `main` spells `<op>.java`,
        # and the entry is `<op>_rm<mode>` -- so the class is the entry with
        # its mode suffix removed.  Java requires the two to agree.
        cls = fn.rsplit("_rm", 1)[0]
        args = ", ".join("%s %s" % (self.ut(w), sanitize(n))
                         for n, w in params)
        return ("public final class %s {\n"
                "    public static %s %s(%s) {" % (cls, self.ut(rw), fn, args))

    def decl(self, ty, name, expr):
        return "        final %s %s = %s;" % (ty, name, expr)

    def ret(self, e):
        return "        return %s;\n    }\n}" % e

    def binop(self, op, w, x, y):
        if w == 1:
            try:
                return {"and": "(%s && %s)", "or": "(%s || %s)",
                        "xor": "(%s != %s)"}[op] % (x, y)
            except KeyError:
                raise ValueError("%s at width 1" % op)
        if w == 128:
            return "Sf.u128%s(%s, %s)" % (op.capitalize(), x, y)
        sym = {"and": "&", "or": "|", "xor": "^", "add": "+", "sub": "-",
               "mul": "*"}.get(op)
        if sym:
            e = "(%s %s %s)" % (x, sym, y)
            # 32 and 64 wrap on their own; 8 and 16 are held by the mask
            return e if w in (32, 64) or op in ("and", "or", "xor") \
                else "((%s %s %s) & 0x%x)" % (x, sym, y, mask(w))
        if op == "udiv":
            return "Sf.udiv%d(%s, %s)" % (w, x, y)
        if op in ("shl", "lshr"):
            arrow = "<<" if op == "shl" else ">>>"
            cnt = ("(int)(%s & %dL)" % (y, w - 1)) if w == 64 \
                else ("(%s & %d)" % (y, w - 1))
            e = "(%s %s %s)" % (x, arrow, cnt)
            return e if w in (32, 64) or op == "lshr" \
                else "((%s %s %s) & 0x%x)" % (x, arrow, cnt, mask(w))
        raise ValueError(op)

    def cast(self, op, sw, dw, x):
        if op == "trunc":
            if sw == 128:
                return "Sf.u128Lo%d(%s)" % (dw, x)
            if dw == 1:
                return "((%s & %s) != %s)" % (x, *(("1L", "0L") if sw == 64
                                                   else ("1", "0")))
            if sw == 64:
                return "(int)(%s)" % x if dw == 32 \
                    else "(int)(%s & 0x%xL)" % (x, mask(dw))
            return "(%s & 0x%x)" % (x, mask(dw))
        if op == "zext":
            if dw == 128:
                return "Sf.u128Zext%d(%s)" % (sw, x)
            if sw == 1:
                return "Sf.b2%s(%s)" % ("l" if dw == 64 else "i", x)
            if dw == 64:
                # an int at 32 may carry the sign bit; mask it off
                return "((long)%s & 0x%xL)" % (x, mask(sw))
            return "(%s)" % x                 # 8 or 16 into 16 or 32
        if op == "sext":
            if dw == 128:
                return "Sf.u128Sext%d(%s)" % (sw, x)
            if sw == 1:
                return "Sf.sext1%s(%s)" % ("l" if dw == 64 else "i", x)
            src = "Sf.s%d(%s)" % (sw, x) if sw in (8, 16) else x
            if dw == 64:
                return "((long)%s)" % src
            return "(%s)" % src if dw == 32 else "(%s & 0x%x)" % (src,
                                                                  mask(dw))
        raise ValueError(op)

    def icmp(self, pred, w, x, y):
        sym = {"eq": "==", "ne": "!=", "ult": "<", "ule": "<=", "ugt": ">",
               "uge": ">=", "slt": "<", "sle": "<=", "sgt": ">", "sge": ">="}
        if w == 128:
            if pred in ("eq", "ne"):
                return "(Sf.u128Eq(%s, %s) %s true)" % (
                    x, y, "==" if pred == "eq" else "!=")
            cmpf = "u128Ucmp" if pred[0] == "u" else "u128Scmp"
            return "(Sf.%s(%s, %s) %s 0)" % (cmpf, x, y, sym[pred])
        if w == 1:
            if pred in ("eq", "ne"):
                return "(%s %s %s)" % (x, sym[pred], y)
            return "(Sf.b2i(%s) %s Sf.b2i(%s))" % (x, sym[pred], y)
        if pred[0] == "u" and w in (32, 64) and pred not in ("eq", "ne"):
            box = "Integer" if w == 32 else "Long"
            return "(%s.compareUnsigned(%s, %s) %s 0)" % (box, x, y,
                                                          sym[pred])
        return "(%s %s %s)" % (x, sym[pred], y)

    def intrinsic(self, base, w, args):
        if base == "ctlz":
            return "Sf.ctlz%d(%s)" % (w, args[0])
        if base == "abs":
            return "Sf.abs%d(%s)" % (w, args[0])
        if base == "usub.sat":
            return "Sf.usubsat%d(%s, %s)" % (w, args[0], args[1])
        if base == "fshl":
            return "Sf.fshl%d(%s, %s, %s)" % (w, args[0], args[1], args[2])
        raise ValueError(base)


# ----------------------------------------------------------------- Lean ----
# `BitVec w` is exactly w bits wide, so none of the masking the unbounded
# languages carry is needed here: and/or/xor/add/sub/mul stay in the width by
# construction.  The pins the other backends spell out by hand are Lean's own
# defaults -- udiv by zero is zero because Nat division by zero is zero, and a
# shift past the width is zero -- except the shift AMOUNT, which LLVM leaves
# poison and the emulations wrap, so that mask is written out.
class LeanBackend(object):
    lang = "lean"
    ext = "lean"
    header = ""

    def ut(self, w):
        return "BitVec %d" % w

    def lit(self, k, w):
        return "0x%x#%d" % (uconst(k, w), w)

    def val(self, a, w):
        return sanitize(a[1]) if a[0] == "v" else self.lit(a[1], w)

    def wants_sval(self, pred, w):
        return False              # BitVec.slt/sle read the same bits signed

    def sval(self, a, w):
        return self.val(a, w)

    def fn_open(self, fn, rw, params):
        ps = " ".join("(%s : BitVec %d)" % (sanitize(n), w)
                      for n, w in params)
        return "def %s %s : BitVec %d :=" % (fn, ps, rw)

    def decl(self, ty, name, expr):
        return "  let %s : %s := %s" % (name, ty, expr)

    def ret(self, e):
        return "  %s" % e

    def binop(self, op, w, x, y):
        if op in ("and", "or", "xor", "add", "sub", "mul"):
            return "(%s %s %s)" % (x, {"and": "&&&", "or": "|||", "xor": "^^^",
                                       "add": "+", "sub": "-",
                                       "mul": "*"}[op], y)
        if op == "udiv":
            return "(BitVec.udiv %s %s)" % (x, y)
        if op in ("shl", "lshr"):
            arrow = "<<<" if op == "shl" else ">>>"
            return "(%s %s (%s &&& %s).toNat)" % (x, arrow, y,
                                                  self.lit(w - 1, w))
        if op == "ashr":
            return "(BitVec.sshiftRight %s (%s &&& %s).toNat)" % (
                x, y, self.lit(w - 1, w))
        raise ValueError(op)

    def cast(self, op, sw, dw, x):
        if op in ("trunc", "zext"):
            return "(BitVec.setWidth %d %s)" % (dw, x)
        if op == "sext":
            return "(BitVec.signExtend %d %s)" % (dw, x)
        raise ValueError(op)

    def icmp(self, pred, w, x, y):
        if pred in ("eq", "ne"):
            inner = "(%s %s %s)" % (x, "==" if pred == "eq" else "!=", y)
        else:
            fn, a, b = {"ult": ("ult", x, y), "ule": ("ule", x, y),
                        "ugt": ("ult", y, x), "uge": ("ule", y, x),
                        "slt": ("slt", x, y), "sle": ("sle", x, y),
                        "sgt": ("slt", y, x), "sge": ("sle", y, x)}[pred]
            inner = "(BitVec.%s %s %s)" % (fn, a, b)
        return "(BitVec.ofBool %s)" % inner

    def intrinsic(self, base, w, args):
        return {"ctlz": "(sfCtlz %s)",
                "abs": "(sfAbs %s)",
                "usub.sat": "(sfUsubsat %s %s)",
                "fshl": "(sfFshl %s %s %s)"}[base] % tuple(args)


BACKENDS = ([CBackend()] if ALT
            else [CBackend(), CppBackend(), RustBackend(), GoBackend(),
                  JavaBackend(), PythonBackend(), RubyBackend(),
                  JsBackend()])


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
    print("emitted %d operations x %d languages"
          % (len(recs), len(BACKENDS)))


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

    # the four added 2026-09-16.  java needs no glue -- `javac *.java`
    # compiles the directory and each class is its own file -- so only the
    # three script languages get an index, and each is the same shape: a map
    # from operation name to the callable that emulates it.
    if "python" in have:
        py = ['"""Every emulated operation, by name.  Generated."""', ""]
        for op in ops:
            py.append("from %s import %s" % (op, recs[op]["languages"]["python"]["entry"]))
        py += ["", "OPS = {"]
        for op in ops:
            py.append('    "%s": %s,' % (op, recs[op]["languages"]["python"]["entry"]))
        py += ["}", ""]
        open(os.path.join(OUT, "python", "index.py"), "w").write("\n".join(py))

    if "ruby" in have:
        rb = ["# Every emulated operation, by name.  Generated.", ""]
        for op in ops:
            rb.append("require_relative '%s'" % op)
        rb += ["", "OPS = {"]
        for op in ops:
            rb.append("  '%s' => method(:%s)," % (op, recs[op]["languages"]["ruby"]["entry"]))
        rb += ["}.freeze", ""]
        open(os.path.join(OUT, "ruby", "index.rb"), "w").write("\n".join(rb))

    if "js" in have:
        js = ["'use strict';", "// Every emulated operation, by name.  Generated.", "",
              "const OPS = {"]
        for op in ops:
            js.append("  '%s': require('./%s.js').%s," % (op, op, recs[op]["languages"]["js"]["entry"]))
        js += ["};", "", "module.exports = { OPS };", ""]
        open(os.path.join(OUT, "js", "index.js"), "w").write("\n".join(js))

    idx = {op: {lang: recs[op]["languages"][lang]["entry"]
                for lang in sorted(have)} for op in ops}
    json.dump({"mode": mode, "entries": idx},
              open(os.path.join(OUT, "_index.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
