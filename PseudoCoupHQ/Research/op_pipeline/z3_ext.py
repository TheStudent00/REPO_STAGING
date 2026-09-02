#!/usr/bin/env python3
"""z3_ext.py -- tier 1 of the equivalence work: a WIDER z3 translation.

`verdicts.py` is the lap of record and is not touched by this file.  It
imports it, re-reads the verdicts it wrote, and re-asks ONLY the pairs
that verdicts.py left UNDECIDED for a reason this file can now answer.
Every other verdict is carried forward exactly as it stands.

What is added, and only what the undecided forms actually use
------------------------------------------------------------
1. IEEE floating point, through z3's own FP theory.  The lifted forms
   in this corpus are SSE scalar-in-vector forms -- `Add64F0x2`,
   `Sub32F0x4`, `CmpEQ64F0x2` -- which compute one lane and copy the
   rest of the register through.  They are modelled that way: the lane
   is converted to an IEEE float, operated on, and written back into
   the bit pattern; the other lanes are the first operand's bits.

   The conversions `F32toF64`, `F64toF32`, `I32StoF64`, `I64StoF64`
   and their neighbours are modelled as z3 conversions.

   `CmpF64` / `CmpF32` return libVEX's FOUR-VALUE comparison code, not
   a boolean: 0x45 unordered, 0x01 less-than, 0x00 greater-than, 0x40
   equal.  UNORDERED IS A SEPARATE ANSWER and is modelled as one.

   ROUNDING MODE.  A VEX rounding-mode operand that is a constant is
   decoded (0 nearest-even, 1 -inf, 2 +inf, 3 zero).  A rounding-mode
   operand that is read out of the guest's SSE control word is NOT
   assumed to be nearest-even: it becomes ONE SHARED symbolic rounding
   mode, the same variable on both sides, because both units run on
   the same machine with the same control word.  A proof under it is a
   proof for every rounding mode, which is stronger than pinning it.
   Where no rounding-mode operand exists at all -- the SSE lane ops
   carry none -- VEX's default, nearest-even, is used.

2. `amd64g_calculate_rflags_c`, the carry flag out of libVEX's lazy
   flag machinery.  Modelled for the groups that OCCUR in this corpus
   and named: SUB (widths 8/16/32/64) and, alongside it because they
   cost nothing and are the same table, ADD, LOGIC and COPY.  Every
   other group raises and the pair stays UNDECIDED saying which group.

3. `amd64g_calculate_condition` with cc_op COPY.  verdicts.py models
   ADD, SUB and LOGIC; COPY is what a floating-point compare leaves --
   `ucomisd` writes the flag bits themselves, VEX hands them straight
   through, and the condition is read off the BITS (CF bit 0, PF bit
   2, ZF bit 6, SF bit 7, OF bit 11).  This is what turns a `CmpF64`
   form into a decidable one.

4. The 128-bit bitwise vector operations `XorV128`, `AndV128`,
   `OrV128`, `NotV128`.  These are bit operations of a wider width and
   nothing more.  Anything genuinely lane-crossing -- a shuffle, a
   pack, a horizontal add -- is NOT modelled and says so.

The two scopes a tier-1 verdict can carry, both printed
-------------------------------------------------------
FULL WIDTH.  The claim is over every bit both units define.

SCALAR LANE.  A unit that computes a 64-bit float in a 256-bit `ymm`
register also carries 192 bits it never wrote and never read.  Two
compilers can leave different rubbish there and still compute the same
number.  So when the full-width claim fails, the claim is re-asked on
the widest common lane that succeeds -- 128, then 64, then 32 bits --
and the verdict RECORDS the width it holds at.  A verdict whose scope
is 32 bits is not the same statement as one whose scope is 256, and
the file never lets the two be read as one.

The ABI precondition, applied to bool and to nothing else
---------------------------------------------------------
verdicts.md states the limit: z3 is asked about every bit pattern a
register can hold, while an ABI promises a `bool` arrives as 0 or 1.
Here, and ONLY where both sides' operand type is `bool`, the
constraint `in0, in1 in {0,1}` is added and the previously UNMATCHED
pairs are re-asked.  A pair that moves carries `abi_precondition:
true`, so the weaker claim is never confused with the unconditional
one.

usage:
  z3_ext.py                write verdicts2.json and verdicts2.md
  z3_ext.py --selfcheck    the FP translation's own guard tests
"""

import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sem_anchored as SA                                     # noqa: E402
import arch_sem as AS                                         # noqa: E402
import verdicts as V                                          # noqa: E402

import z3                                                     # noqa: E402

Z3_TIMEOUT_MS = 20000

Unsupported = V.Unsupported


# ======================================================= width plumbing
#
# RULE.  The width written on an expression node is arch_sem's, and for
# the VECTOR COMPARE operators it is wrong: `_bin_width` sees a name
# beginning `Cmp` and returns 1, while `CmpEQ32F0x4` produces 128 bits.
# Nothing here edits arch_sem.  Instead every operand is FITTED to the
# width the operation needs, and the width an operation produces is
# taken from this file's own table rather than from the node.

def fit(x, n):
    """the same bit pattern, in exactly n bits."""
    w = x.size()
    if w == n:
        return x
    if w > n:
        return z3.Extract(n - 1, 0, x)
    return z3.ZeroExt(n - w, x)


def ones(n):
    return z3.BitVecVal((1 << n) - 1, n)


# ============================================================ IEEE floats

SORT = {16: z3.Float16, 32: z3.Float32, 64: z3.Float64,
        128: z3.Float128}

RNE = z3.RoundNearestTiesToEven()


def as_fp(x, w):
    """w bits of a bit pattern, read as the IEEE float they encode."""
    return z3.fpBVToFP(fit(x, w), SORT[w]())


def as_bits(f):
    """an IEEE float, written back as the bit pattern it encodes."""
    return z3.fpToIEEEBV(f)


# VEX's IRRoundingMode, which is the SSE encoding: 0 nearest-even,
# 1 toward -inf, 2 toward +inf, 3 toward zero.
def rounding_mode(bits):
    if z3.is_bv_value(bits):
        return _RM_CONST[bits.as_long() & 3]
    low = fit(bits, 2)
    out = z3.RoundTowardZero()
    out = z3.If(low == 2, z3.RoundTowardPositive(), out)
    out = z3.If(low == 1, z3.RoundTowardNegative(), out)
    out = z3.If(low == 0, RNE, out)
    return out


_RM_CONST = {0: z3.RoundNearestTiesToEven(),
             1: z3.RoundTowardNegative(),
             2: z3.RoundTowardPositive(),
             3: z3.RoundTowardZero()}


# ---- the SSE scalar-in-vector lane operations --------------------------
#
# `Add64F0x2` adds the LOW LANE of two 128-bit registers and leaves the
# high lane holding the first operand's high lane.  That is what the
# hardware does and it is modelled literally.

LANE = re.compile(r"^(Add|Sub|Mul|Div|Min|Max|CmpEQ|CmpLT|CmpLE|CmpUN)"
                  r"(32|64)F0x(2|4)$")

FPBIN = {
    "Add": lambda rm, a, b: z3.fpAdd(rm, a, b),
    "Sub": lambda rm, a, b: z3.fpSub(rm, a, b),
    "Mul": lambda rm, a, b: z3.fpMul(rm, a, b),
    "Div": lambda rm, a, b: z3.fpDiv(rm, a, b),
    "Min": lambda rm, a, b: z3.fpMin(a, b),
    "Max": lambda rm, a, b: z3.fpMax(a, b),
}

FPCMP = {
    "CmpEQ": lambda a, b: z3.fpEQ(a, b),
    "CmpLT": lambda a, b: z3.fpLT(a, b),
    "CmpLE": lambda a, b: z3.fpLEQ(a, b),
    "CmpUN": lambda a, b: z3.Or(z3.fpIsNaN(a), z3.fpIsNaN(b)),
}


def lane_op(head, w, a, b):
    """one 128-bit result: the lane computed, the rest copied."""
    a = fit(a, 128)
    b = fit(b, 128)
    x = as_fp(z3.Extract(w - 1, 0, a), w)
    y = as_fp(z3.Extract(w - 1, 0, b), w)
    if head in FPBIN:
        low = as_bits(FPBIN[head](RNE, x, y))
    elif head in FPCMP:
        # a lane compare answers in the lane's own width, all ones or
        # all zeros.  The compares are ORDERED: a NaN makes CmpEQ false.
        low = z3.If(FPCMP[head](x, y), ones(w), z3.BitVecVal(0, w))
    else:
        raise Unsupported("SSE lane operation not modelled: %s%dF0x?"
                          % (head, w))
    return z3.Concat(z3.Extract(127, w, a), low)


# ---- libVEX's four-value floating point comparison ---------------------
#
# guest_amd64 hands `ucomisd`'s answer through `CmpF64`, whose result is
# not a boolean.  libvex_ir.h:
#     Ircr_UN = 0x45   Ircr_LT = 0x01   Ircr_GT = 0x00   Ircr_EQ = 0x40
# The numbers are the amd64 flag bits themselves -- CF is bit 0, PF is
# bit 2, ZF is bit 6 -- which is why the lifted form goes on to mask
# with 0x45 and hand the result to the condition helper as cc_op COPY.

CR_UN = 0x45
CR_LT = 0x01
CR_GT = 0x00
CR_EQ = 0x40


def cmp_f(a, b, w):
    x = as_fp(a, w)
    y = as_fp(b, w)
    un = z3.Or(z3.fpIsNaN(x), z3.fpIsNaN(y))
    out = z3.BitVecVal(CR_GT, 32)
    out = z3.If(z3.fpEQ(x, y), z3.BitVecVal(CR_EQ, 32), out)
    out = z3.If(z3.fpLT(x, y), z3.BitVecVal(CR_LT, 32), out)
    out = z3.If(un, z3.BitVecVal(CR_UN, 32), out)
    return out


# ---- the conversions ---------------------------------------------------

CONV_UNARY = {
    # name: (result width, how)
    "F32toF64": (64, "f2f"),
    "F64toF32": (32, "f2f"),
    "I32StoF64": (64, "s2f"),
    "I32UtoF64": (64, "u2f"),
    "I32StoF32": (32, "s2f"),
    "I64StoF64": (64, "s2f"),
    "I64StoF32": (32, "s2f"),
    "I64UtoF64": (64, "u2f"),
    "F64toI32S": (32, "f2s"),
    "F64toI64S": (64, "f2s"),
    "F32toI32S": (32, "f2s"),
    "F32toI64S": (64, "f2s"),
}

SRC_WIDTH = {"F32toF64": 32, "F64toF32": 64, "I32StoF64": 32,
             "I32UtoF64": 32, "I32StoF32": 32, "I64StoF64": 64,
             "I64StoF32": 64, "I64UtoF64": 64, "F64toI32S": 64,
             "F64toI64S": 64, "F32toI32S": 32, "F32toI64S": 32}


def convert(name, rm, x):
    dst, how = CONV_UNARY[name]
    src = SRC_WIDTH[name]
    x = fit(x, src)
    if how == "f2f":
        return as_bits(z3.fpToFP(rm, as_fp(x, src), SORT[dst]()))
    if how == "s2f":
        return as_bits(z3.fpToFP(rm, x, SORT[dst]()))
    if how == "u2f":
        return as_bits(z3.fpToFPUnsigned(rm, x, SORT[dst]()))
    # a float to a signed integer.  amd64's `cvttsd2si` truncates and
    # that is the rounding mode VEX hands in, so the mode is used as
    # given rather than replaced.
    return z3.fpToSBV(rm, as_fp(x, src), z3.BitVecSort(dst))


# ================================================== the amd64 flag groups
#
# Only the carry bit is needed, and only the groups this corpus uses.
# The corpus's own `amd64g_calculate_rflags_c` calls carry cc_op 7 and
# 8, which are SUB32 and SUB64.  ADD, LOGIC and COPY are modelled beside
# them because they are the same three lines; every other group raises.

def rflags_c(oname, width, dep1, dep2):
    if oname == "SUB":
        return z3.If(z3.ULT(dep1, dep2), z3.BitVecVal(1, 64),
                     z3.BitVecVal(0, 64))
    if oname == "ADD":
        carried = z3.Not(z3.BVAddNoOverflow(dep1, dep2, False))
        return z3.If(carried, z3.BitVecVal(1, 64), z3.BitVecVal(0, 64))
    if oname == "LOGIC":
        return z3.BitVecVal(0, 64)
    if oname == "COPY":
        return z3.ZeroExt(63, z3.Extract(0, 0, dep1))
    raise Unsupported("the carry flag after %s%d is not modelled -- this "
                      "file models SUB, ADD, LOGIC and COPY only"
                      % (oname, width))


# the amd64 flag bits, by position in rflags.
CF, PF, ZF, SF, OF = 0, 2, 6, 7, 11


def _bit(x, i):
    return z3.Extract(i, i, fit(x, 64)) == z3.BitVecVal(1, 1)


def copy_condition(cname, dep1):
    """the condition read off the flag BITS themselves.  This is what
    cc_op COPY means: the lifted form already holds rflags."""
    cf = _bit(dep1, CF)
    pf = _bit(dep1, PF)
    zf = _bit(dep1, ZF)
    sf = _bit(dep1, SF)
    of = _bit(dep1, OF)
    table = {
        "O": of, "NO": z3.Not(of),
        "B": cf, "NB": z3.Not(cf),
        "Z": zf, "NZ": z3.Not(zf),
        "BE": z3.Or(cf, zf), "NBE": z3.Not(z3.Or(cf, zf)),
        "S": sf, "NS": z3.Not(sf),
        "P": pf, "NP": z3.Not(pf),
        "L": sf != of, "NL": sf == of,
        "LE": z3.Or(zf, sf != of), "NLE": z3.Not(z3.Or(zf, sf != of)),
    }
    if cname in table:
        return table[cname]
    raise Unsupported("condition %s after COPY is not modelled" % cname)


# ================================================ the extended translation

class Side(object):
    """one unit's naming, and where its variables live.

    RULE ON VARIABLE SHARING.  A register that the anchor named `in0`
    or `in1` is the SAME VALUE on both sides -- that is what the anchor
    established -- so it becomes one shared variable.  A register the
    anchor could not name is scratch, and scratch on the left has
    nothing to do with scratch on the right, so it becomes a variable
    of its own with the side's tag on it.  The one exception is a piece
    of VEX's own machinery -- the SSE control word, the x87 top of
    stack -- which is a property of the MACHINE and not of either unit,
    and so is shared."""

    def __init__(self, names, tag):
        self.names = names
        self.tag = tag
        self.scratch = []

    def var(self, phys, w):
        if phys in AS.PSEUDO:
            return "MACHINE_%s_%d" % (phys, w), False
        tok = self.names.get(phys)
        if tok is None:
            raise Unsupported("a register with no anchored name: %s" % phys)
        if tok.startswith("in") or tok in ("SP", "PC"):
            return "%s_%d" % (tok, w), False
        key = "%s_%s_%d" % (self.tag, tok, w)
        if key not in self.scratch:
            self.scratch.append(key)
        return key, True


def bv(e, side, env):
    """one lifted value, as a z3 bitvector.  verdicts.py's `_bv` with
    the floating point, the vector width and the flag groups added."""
    k = e[0]
    if k == "c":
        return z3.BitVecVal(e[2], e[1])
    if k == "r":
        key, _scratch = side.var(e[2], e[1])
        if key not in env:
            env[key] = z3.BitVec(key, e[1])
        return env[key]
    if k == "ex":
        inner = bv(e[3], side, env)
        need = e[2] + e[1]
        inner = fit(inner, max(inner.size(), need))
        return z3.Extract(need - 1, e[2], inner)
    if k == "zx":
        return fit(bv(e[2], side, env), e[1])
    if k == "sx":
        inner = bv(e[2], side, env)
        if inner.size() >= e[1]:
            return fit(inner, e[1])
        return z3.SignExt(e[1] - inner.size(), inner)
    if k == "ins":
        old = fit(bv(e[2], side, env), e[1])
        val = bv(e[3], side, env)
        return _insert(old, val, e[4])
    if k == "ite":
        c = bv(e[2], side, env)
        t = bv(e[3], side, env)
        f = bv(e[4], side, env)
        n = max(t.size(), f.size())
        return z3.If(c == z3.BitVecVal(1, c.size()), fit(t, n), fit(f, n))
    if k == "b":
        return binop(e, side, env)
    if k == "u":
        return unop(e, side, env)
    if k == "t":
        return triop(e, side, env)
    if k == "cc":
        return ccall(e, side, env)
    if k == "q":
        raise Unsupported("quaternary VEX op not modelled: %s" % e[2])
    if k == "op":
        raise Unsupported("the lifted form carries an opaque value [%s]"
                          % e[2])
    if k == "ld":
        raise Unsupported("the unit reads memory")
    raise Unsupported("expression kind not modelled: %s" % k)


def _insert(old, val, lo):
    w = old.size()
    vw = val.size()
    if lo == 0 and vw >= w:
        return fit(val, w)
    if lo + vw > w:
        val = z3.Extract(w - lo - 1, 0, val)
        vw = val.size()
    parts = []
    if lo + vw < w:
        parts.append(z3.Extract(w - 1, lo + vw, old))
    parts.append(val)
    if lo > 0:
        parts.append(z3.Extract(lo - 1, 0, old))
    if len(parts) == 1:
        return parts[0]
    return z3.Concat(*parts)


VECBIT = re.compile(r"^(And|Or|Xor)V(\d+)$")


def binop(e, side, env):
    op = e[2]
    a = bv(e[3], side, env)
    b = bv(e[4], side, env)

    m = LANE.match(op)
    if m:
        return lane_op(m.group(1), int(m.group(2)), a, b)

    m = VECBIT.match(op)
    if m:
        n = int(m.group(2))
        a = fit(a, n)
        b = fit(b, n)
        return {"And": a & b, "Or": a | b, "Xor": a ^ b}[m.group(1)]

    if op in ("CmpF64", "CmpF32"):
        w = 64 if op == "CmpF64" else 32
        return cmp_f(a, b, w)

    # a conversion whose first operand is the rounding mode.
    if op in CONV_UNARY:
        return convert(op, rounding_mode(a), b)

    if op.startswith("SetV128lo"):
        n = int(op[len("SetV128lo"):])
        return _insert(fit(a, 128), fit(b, n), 0)

    m = re.match(r"^(\d+)HLtoV?(\d+)$", op)
    if m:
        half = int(m.group(1))
        return z3.Concat(fit(a, half), fit(b, half))

    return _scalar_binop(e, op, a, b)


def _scalar_binop(e, op, a, b):
    """verdicts.py's own scalar table, with the operands fitted."""
    m = AS.BINWIDTH.match(op)
    head = m.group(1) if m else op
    if head in V.ARITH:
        n = max(a.size(), b.size())
        if m:
            n = int(m.group(2))
        return V.ARITH[head](fit(a, n), fit(b, n))
    if head in ("Shl", "Shr", "Sar"):
        n = a.size()
        amount = fit(b, n)
        if head == "Shl":
            return fit(a, n) << amount
        if head == "Shr":
            return z3.LShR(fit(a, n), amount)
        return fit(a, n) >> amount
    n = max(a.size(), b.size())
    a = fit(a, n)
    b = fit(b, n)
    bit = None
    if op.startswith("CmpEQ"):
        bit = a == b
    elif op.startswith("CmpNE"):
        bit = a != b
    elif re.match(r"^CmpLT\d+S$", op):
        bit = a < b
    elif re.match(r"^CmpLT\d+U$", op):
        bit = z3.ULT(a, b)
    elif re.match(r"^CmpLE\d+S$", op):
        bit = a <= b
    elif re.match(r"^CmpLE\d+U$", op):
        bit = z3.ULE(a, b)
    if bit is not None:
        return z3.If(bit, z3.BitVecVal(1, 1), z3.BitVecVal(0, 1))
    raise Unsupported("binary VEX op not modelled: %s" % op)


def unop(e, side, env):
    op = e[2]
    a = bv(e[3], side, env)
    m = AS.BINWIDTH.match(op)
    if m and m.group(1) == "Not":
        return ~fit(a, int(m.group(2)))
    m = re.match(r"^NotV(\d+)$", op)
    if m:
        return ~fit(a, int(m.group(1)))
    if op in CONV_UNARY:
        return convert(op, RNE, a)
    if op in ("AbsF64", "AbsF32"):
        w = 64 if op.endswith("64") else 32
        return as_bits(z3.fpAbs(as_fp(a, w)))
    if op in ("NegF64", "NegF32"):
        w = 64 if op.endswith("64") else 32
        return as_bits(z3.fpNeg(as_fp(a, w)))
    raise Unsupported("unary VEX op not modelled: %s" % op)


TRIOP = re.compile(r"^(Add|Sub|Mul|Div)F(32|64)$")


def triop(e, side, env):
    op = e[2]
    m = TRIOP.match(op)
    if not m:
        raise Unsupported("ternary VEX op not modelled: %s" % op)
    w = int(m.group(2))
    rm = rounding_mode(bv(e[3], side, env))
    a = as_fp(bv(e[4], side, env), w)
    b = as_fp(bv(e[5], side, env), w)
    return as_bits(FPBIN[m.group(1)](rm, a, b))


def ccall(e, side, env):
    name = e[2]
    args = e[3]
    if name == "amd64g_calculate_condition":
        return _condition(e, args, side, env)
    if name == "amd64g_calculate_rflags_c":
        return _rflags_c(e, args, side, env)
    raise Unsupported("VEX helper call not modelled: %s" % name)


def _group(op):
    if op[0] != "c":
        raise Unsupported("the flag operation is not a constant in the "
                          "lifted form")
    oname, width = V.CC_OP.get(op[2], (None, 64))
    if oname is None:
        raise Unsupported("flag operation %d is not modelled" % op[2])
    return oname, width


def _condition(e, args, side, env):
    cond = V._peel(args[0])
    op = V._peel(args[1])
    if cond[0] != "c":
        raise Unsupported("the condition is not a constant in the lifted "
                          "form")
    cname = V.COND.get(cond[2] & 0xF)
    if cname is None:
        raise Unsupported("condition %d is not modelled" % cond[2])
    oname, width = _group(op)
    L = bv(args[2], side, env)
    R = bv(args[3], side, env)
    if oname == "COPY":
        bit = copy_condition(cname, L)
    else:
        bit = V._flag(cname, oname, width, fit(L, width), fit(R, width))
    return z3.If(bit, z3.BitVecVal(1, e[1]), z3.BitVecVal(0, e[1]))


def _rflags_c(e, args, side, env):
    oname, width = _group(V._peel(args[0]))
    dep1 = bv(args[1], side, env)
    dep2 = bv(args[2], side, env)
    out = rflags_c(oname, width, fit(dep1, width), fit(dep2, width))
    return fit(out, e[1])


# ================================================== the tier-1 pair query

LANE_WIDTHS = [256, 128, 64, 32, 16, 8]


def ladder(pairs):
    """the widths the claim is asked at, widest first.

    The first entry is the widest width both units define for every
    result -- the full-width claim.  Below it come the SSE lane widths,
    because a unit that computes a 64-bit float in a 256-bit register
    carries 192 bits it never wrote, and two compilers may leave
    different rubbish in them while computing the same number.  The
    ladder stops at 8, the width of a `bool` and of what a `setcc`
    writes -- `and $0x1,%eax` and `and $0x1,%al` compute the same
    answer and leave different bits above it.  It does not go below 8:
    a one-bit agreement says almost nothing and this file would rather
    leave a pair UNMATCHED than call one a match.  EVERY verdict below
    the full width records `scope_bits`, so the width of the claim is
    never separable from the claim."""
    top = min(min(a.size(), b.size()) for a, b in pairs)
    out = [top]
    for w in LANE_WIDTHS:
        if w < top and w not in out:
            out.append(w)
    return out


def z3_pair_ext(left, right, bool_precondition=False):
    """(verdict, detail, extra).  The same shape of answer verdicts.py
    gives, decided with the wider translation."""
    forms = []
    for record in (left, right):
        blocks = record["sem"]["blocks"]
        if len(blocks) != 1:
            return ("UNDECIDED",
                    "%s op_%s is not straight-line: %d blocks"
                    % (record["lang"], record["n"], len(blocks)), {})
        events = blocks[0]["events"]
        bad = [ev for ev in events if not V.PURE_EVENT.match(ev)]
        if bad:
            return ("UNDECIDED",
                    "%s op_%s is not pure scalar dataflow: %s"
                    % (record["lang"], record["n"], "; ".join(bad)), {})
        if blocks[0]["stores"]:
            return ("UNDECIDED", "%s op_%s writes memory"
                    % (record["lang"], record["n"]), {})
        summaries, names, reason = SA.raw_summaries(
            dict(bytes=record["bytes"].split(), mnem=record["mnem"]),
            record["lang"], record["meta"])
        if summaries is None:
            return "UNDECIDED", "the lift was refused: %s" % reason, {}
        _parts, names = SA.render_anchored(summaries, names)
        forms.append((summaries[0][0], names))

    (lv, lnames), (rv, rnames) = forms
    if len(lv) != len(rv):
        return ("UNDECIDED",
                "the two units leave a different number of live results "
                "(%d and %d)" % (len(lv), len(rv)), {})

    lv = sorted(lv, key=lambda x: (AS.W(x), AS._ser(x, lnames)))
    rv = sorted(rv, key=lambda x: (AS.W(x), AS._ser(x, rnames)))

    lside = Side(lnames, "L")
    rside = Side(rnames, "R")
    env = {}
    pairs = []
    try:
        for a, b in zip(lv, rv):
            av = bv(a, lside, env)
            bv_ = bv(b, rside, env)
            pairs.append((av, bv_))
    except Unsupported as exc:
        return "UNDECIDED", "z3 was not asked: %s" % exc, {}

    pre = []
    if bool_precondition:
        # THE ABI'S PROMISE, EXACTLY.  SysV and go both say a `bool`
        # arrives with the VALUE 0 or 1 in the low byte of its
        # register.  Neither says anything about the bits above that
        # byte, so nothing is asserted about them here.
        for key, var in sorted(env.items()):
            if not key.startswith("in"):
                continue
            low = fit(var, 8)
            pre.append(z3.ULE(low, z3.BitVecVal(1, 8)))
        if not pre:
            return ("UNDECIDED",
                    "the ABI precondition was asked for but no anchored "
                    "operand reaches the result", {})

    scratch = sorted(set(lside.scratch + rside.scratch))
    steps = ladder(pairs)
    sat_at = None
    unknown_at = None

    for n in steps:
        claims = [fit(a, n) == fit(b, n) for a, b in pairs]
        got, model = _ask(claims, pre)
        if got == z3.unsat:
            full = (n == steps[0]
                    and all(a.size() == b.size() == n for a, b in pairs))
            detail = ("z3 proved the two lifted forms equal for every "
                      "input (negation unsat)")
            extra = dict(scope_bits=n, full_width=full, tier1=True,
                         result_types=[left["meta"].get("result_type"),
                                       right["meta"].get("result_type")],
                         result_rules=[left["meta"].get("result_rule"),
                                       right["meta"].get("result_rule")])
            if scratch:
                extra["scratch_registers"] = scratch
                detail += ("; the proof holds for every value of the "
                           "unanchored scratch registers %s"
                           % ", ".join(scratch))
            if not full:
                detail += ("; the claim is over the low %d bits -- the "
                           "widest width at which it holds; the two "
                           "units define %s bits of these results"
                           % (n, ", ".join("%d/%d" % (a.size(), b.size())
                                           for a, b in pairs)))
            if bool_precondition:
                extra["abi_precondition"] = True
                detail += ("; under the ABI precondition that each `bool` "
                           "operand arrives as 0 or 1 in the low byte of "
                           "its register")
            return "MATCHED", detail, extra
        if got == z3.sat:
            sat_at = (n, model)
            continue
        unknown_at = (n, got)

    if sat_at is None:
        return ("UNDECIDED", "z3 returned %s at width %d (timeout %d ms)"
                % (unknown_at[1], unknown_at[0], Z3_TIMEOUT_MS),
                dict(tier1=True))

    n, model = sat_at
    shown = ", ".join("%s = %s" % (d.name(), model[d])
                      for d in sorted(model.decls(), key=lambda d: d.name()))
    touched = [k for k in scratch if k in shown]
    extra = dict(scope_bits=n, tier1=True)
    if bool_precondition:
        extra["abi_precondition"] = True
    if touched:
        extra["scratch_registers"] = touched
        return ("UNDECIDED",
                "the two units disagree, but the disagreement is reached "
                "by assigning the unanchored scratch registers %s, which "
                "carry no operand and which the two units cannot be "
                "compared on.  z3's assignment at width %d was: %s"
                % (", ".join(touched), n, shown), extra)
    return ("UNMATCHED",
            "z3 counterexample at width %d (the two units disagree at "
            "every width tried: %s): %s"
            % (n, ", ".join(str(w) for w in steps), shown), extra)


def _ask(claims, pre):
    s = z3.Solver()
    s.set("timeout", Z3_TIMEOUT_MS)
    for p in pre:
        s.add(p)
    if len(claims) == 1:
        s.add(z3.Not(claims[0]))
    else:
        s.add(z3.Not(z3.And(*claims)))
    got = s.check()
    model = s.model() if got == z3.sat else None
    return got, model


# ================================================== which pairs are re-asked

RETRY = [
    "z3 was not asked:",
    "an unanchored register value reaches the result",
]


def retryable(pair, type_pair):
    """(True, why) when this pass can say something new about a pair."""
    if pair["verdict"] == "UNDECIDED":
        detail = str(pair.get("detail") or "")
        for head in RETRY:
            if head in detail:
                return True, "undecided: the translation was too narrow"
        return False, None
    if pair["verdict"] == "UNMATCHED" and type_pair == "bool,bool":
        return True, "unmatched bool: re-asked under the ABI precondition"
    return False, None


# ============================================================== the pass

def main():
    started = time.time()
    print("== tier 1: the wider z3 translation")
    print("   z3      %s" % z3.get_version_string())
    print("   lifter  %s" % AS.LIFTER_ID)
    sys.stdout.flush()

    prior = json.load(open(os.path.join(HERE, "verdicts.json")))
    units, excluded, excluded_rows = V.load_units()
    index = {}
    for u in units:
        index[(u["lang"], u["n"])] = u
    print("   units   %d indexed, %d excluded"
          % (len(index), sum(excluded.values())))
    sys.stdout.flush()

    todo = []
    for row in prior["rows"]:
        for pair in row["pairs"]:
            want, why = retryable(pair, row["type_pair"])
            if want:
                todo.append((row, pair, why))
    total = len(todo)
    print("   re-asking %d pairs" % total)
    sys.stdout.flush()

    moved = {"MATCHED": 0, "UNMATCHED": 0, "UNDECIDED": 0,
             "DIFFERS-BY-DESIGN": 0}
    bool_moved = 0
    done = 0
    decided = 0
    for row, pair, why in todo:
        is_bool = row["type_pair"] == "bool,bool"
        precondition = is_bool and pair["verdict"] == "UNMATCHED"
        left = _side(index, pair["left"])
        right = _side(index, pair["right"])
        if left is None or right is None:
            verdict, detail, extra = ("UNDECIDED",
                                      "a unit of the pair is not in the "
                                      "accepted set", dict(tier1=True))
        else:
            try:
                verdict, detail, extra = z3_pair_ext(left, right,
                                                     precondition)
            except Exception as exc:                       # noqa: BLE001
                verdict = "UNDECIDED"
                detail = "the tier-1 pass raised: %s: %s" % (
                    type(exc).__name__, exc)
                extra = dict(tier1=True)
        was = pair["verdict"]
        pair["tier1"] = True
        pair["tier1_reason"] = why
        pair["tier0_verdict"] = was
        pair["tier0_detail"] = pair.get("detail")
        pair["verdict"] = verdict
        pair["ground"] = "z3 over the two lifted forms (tier 1)"
        pair["detail"] = detail
        for k, v in (extra or {}).items():
            pair[k] = v
        if verdict != was:
            moved[verdict] = moved.get(verdict, 0) + 1
            if precondition and verdict == "MATCHED":
                bool_moved += 1
        if verdict != "UNDECIDED":
            decided += 1
        done += 1
        if done % 25 == 0 or done == total:
            print("progress: %d/%d decided=%d matched=%d unmatched=%d "
                  "still_undecided=%d elapsed=%ds"
                  % (done, total, decided, moved["MATCHED"],
                     moved["UNMATCHED"], done - decided,
                     int(time.time() - started)))
            sys.stdout.flush()

    tally = {}
    for row in prior["rows"]:
        for pair in row["pairs"]:
            tally[pair["verdict"]] = tally.get(pair["verdict"], 0) + 1
    prior["tally"] = tally
    prior["tier1"] = dict(
        reasked=total,
        moved=moved,
        bool_pairs_moved_under_abi_precondition=bool_moved,
        z3=z3.get_version_string(),
        wall_seconds=int(time.time() - started),
        models=["IEEE FP via z3's FP theory (SSE lane ops, the "
                "conversions, the four-value CmpF64/CmpF32)",
                "amd64g_calculate_rflags_c for SUB, ADD, LOGIC, COPY",
                "amd64g_calculate_condition for cc_op COPY",
                "the 128-bit bitwise vector operations"])

    json.dump(prior, open(os.path.join(HERE, "verdicts2.json"), "w"),
              indent=1)
    write_md(prior)

    print()
    print("== tier 1 done in %ds" % (time.time() - started))
    for v in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
        print("   %-20s %d" % (v, tally.get(v, 0)))
    print("   re-asked %d, changed %s" % (total, moved))
    print("   bool pairs moved under the ABI precondition: %d" % bool_moved)
    return 0


def _side(index, label):
    lang, op = label.split("/")
    return index.get((lang, op[3:]))


def write_md(doc):
    out = []
    out.append("# the three verdicts -- tier 1")
    out.append("")
    out.append("This is `verdicts.md` with ONE change: the pairs that "
               "the first pass left UNDECIDED because its z3 translation "
               "did not cover floating point, the flag helper or the "
               "128-bit bitwise operations have been re-asked with a "
               "translation that does.  Every other verdict is carried "
               "forward unchanged and is still the first pass's.")
    out.append("")
    out.append("A re-asked pair carries `tier1`, the verdict it used to "
               "have, and the reason it was re-asked.  A pair proved "
               "equal on fewer bits than both units define carries "
               "`scope_bits`: the width the claim holds at.  A pair "
               "re-asked with the ABI's `bool` promise as a "
               "precondition carries `abi_precondition`, and that "
               "verdict is CONDITIONAL on the promise.")
    out.append("")
    out.append("**On a `scope_bits` of 8.**  Nearly every pair re-asked "
               "here is a COMPARISON or a BOOLEAN operator, whose answer "
               "is one byte: `setcc` writes one byte and leaves the "
               "seven above it holding whatever the caller left there, "
               "and `and $0x1,%eax` against `and $0x1,%al` differ in "
               "exactly those seven bytes and in nothing else.  The "
               "8-bit claim is the whole answer for such an operator and "
               "is not the whole answer for any other, which is why the "
               "width is written on every verdict and why each row also "
               "carries the two sides' own `result_type`.")
    out.append("")
    t = doc["tier1"]
    out.append("- pairs re-asked: **%d**" % t["reasked"])
    out.append("- moved to: %s" % ", ".join("%s %d" % (k, v)
                                            for k, v in sorted(
                                                t["moved"].items()) if v))
    out.append("- bool pairs that moved under the ABI precondition: "
               "**%d**" % t["bool_pairs_moved_under_abi_precondition"])
    out.append("- wall seconds: %d" % t["wall_seconds"])
    out.append("")
    out.append("## what tier 1 models")
    out.append("")
    for m in t["models"]:
        out.append("- %s" % m)
    out.append("")
    out.append("## tally")
    out.append("")
    out.append("| verdict | pairs |")
    out.append("| --- | --- |")
    for v in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
        out.append("| %s | %d |" % (v, doc["tally"].get(v, 0)))
    out.append("")
    out.append("## every pair re-asked at tier 1")
    out.append("")
    out.append("| operator | type pair | left | right | was | now | "
               "scope | detail |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in doc["rows"]:
        for p in row["pairs"]:
            if not p.get("tier1"):
                continue
            scope = str(p.get("scope_bits", "-"))
            if p.get("abi_precondition"):
                scope += " (ABI precondition)"
            out.append("| `%s` | %s | %s | %s | %s | %s | %s | %s |"
                       % (row["operator"], row["type_pair"], p["left"],
                          p["right"], p["tier0_verdict"], p["verdict"],
                          scope,
                          str(p["detail"]).replace("|", "/")[:300]))
    out.append("")
    out.append("## what is still UNDECIDED, in the tool's own words")
    out.append("")
    reasons = {}
    for row in doc["rows"]:
        for p in row["pairs"]:
            if p["verdict"] != "UNDECIDED":
                continue
            key = _reason_key(str(p.get("detail") or ""))
            reasons[key] = reasons.get(key, 0) + 1
    out.append("| pairs | reason |")
    out.append("| --- | --- |")
    for key, count in sorted(reasons.items(), key=lambda kv: -kv[1]):
        out.append("| %d | %s |" % (count, key.replace("|", "/")))
    out.append("")
    open(os.path.join(HERE, "verdicts2.md"), "w").write("\n".join(out))


def _reason_key(detail):
    m = re.search(r"not modelled: (\S+)", detail)
    if m:
        return "a VEX operation not modelled: %s" % m.group(1)
    m = re.search(r"is not modelled", detail)
    if m:
        return detail[:120]
    return detail[:120]


# ================================================================ selfcheck

def _s(bits, name, w):
    return z3.BitVec(name, w)


def selfcheck():
    """guard tests for the translation itself, each an identity that
    must hold or must fail, stated in one line."""
    print("== z3_ext selfcheck   (z3 %s)" % z3.get_version_string())
    bad = 0
    x = z3.BitVec("x", 64)
    y = z3.BitVec("y", 64)

    cases = []

    # a float compared with itself is EQ unless it is a NaN, and then
    # it is UNORDERED.  Both halves are checked.
    f = z3.fpBVToFP(x, z3.Float64())
    cases.append(("CmpF64(x,x) is EQ when x is not NaN",
                  z3.Implies(z3.Not(z3.fpIsNaN(f)),
                             cmp_f(x, x, 64) == z3.BitVecVal(CR_EQ, 32))))
    cases.append(("CmpF64(x,x) is UN when x is NaN",
                  z3.Implies(z3.fpIsNaN(f),
                             cmp_f(x, x, 64) == z3.BitVecVal(CR_UN, 32))))

    # the lane operation touches the lane and nothing else.
    a = z3.BitVec("a", 128)
    b = z3.BitVec("b", 128)
    cases.append(("Add64F0x2 leaves the high lane alone",
                  z3.Extract(127, 64, lane_op("Add", 64, a, b))
                  == z3.Extract(127, 64, a)))
    cases.append(("Add32F0x4 leaves bits 127:32 alone",
                  z3.Extract(127, 32, lane_op("Add", 32, a, b))
                  == z3.Extract(127, 32, a)))

    # widening a float to double and back is the identity away from NaN.
    g = z3.fpBVToFP(z3.Extract(31, 0, x), z3.Float32())
    wide = convert("F32toF64", RNE, z3.Extract(31, 0, x))
    back = convert("F64toF32", RNE, wide)
    cases.append(("F64toF32(F32toF64(x)) == x away from NaN",
                  z3.Implies(z3.Not(z3.fpIsNaN(g)),
                             back == z3.Extract(31, 0, x))))

    # the carry out of a subtraction is the unsigned borrow.
    cases.append(("rflags_c after SUB64 is the unsigned borrow",
                  rflags_c("SUB", 64, x, y)
                  == z3.If(z3.ULT(x, y), z3.BitVecVal(1, 64),
                           z3.BitVecVal(0, 64))))

    # the COPY condition reads the flag bits.
    cases.append(("condition Z after COPY is bit 6",
                  copy_condition("Z", x) == (z3.Extract(6, 6, x)
                                             == z3.BitVecVal(1, 1))))
    cases.append(("condition P after COPY is bit 2",
                  copy_condition("P", x) == (z3.Extract(2, 2, x)
                                             == z3.BitVecVal(1, 1))))

    # the unordered code masked with 0x45 sets CF, PF and ZF, so `P`
    # after COPY is exactly "the two floats were unordered".  This is
    # the identity the whole CmpF64 chain rests on.
    masked = cmp_f(x, y, 64) & z3.BitVecVal(0x45, 32)
    fx = z3.fpBVToFP(x, z3.Float64())
    fy = z3.fpBVToFP(y, z3.Float64())
    cases.append(("P after COPY of (CmpF64 & 0x45) is unordered",
                  copy_condition("P", z3.ZeroExt(32, masked))
                  == z3.Or(z3.fpIsNaN(fx), z3.fpIsNaN(fy))))

    for label, claim in cases:
        s = z3.Solver()
        s.set("timeout", Z3_TIMEOUT_MS)
        s.add(z3.Not(claim))
        got = s.check()
        ok = "ok  " if got == z3.unsat else "FAIL"
        if got != z3.unsat:
            bad += 1
        print("   [%s] %s   (%s)" % (ok, label, got))
        if got == z3.sat:
            print("        %s" % s.model())

    # one that MUST be refutable: a float add is not a float subtract.
    s = z3.Solver()
    s.add(lane_op("Add", 64, a, b) != lane_op("Sub", 64, a, b))
    got = s.check()
    ok = "ok  " if got == z3.sat else "FAIL"
    if got != z3.sat:
        bad += 1
    print("   [%s] Add64F0x2 and Sub64F0x2 are refutably different   (%s)"
          % (ok, got))

    print("   %d failures over %d guards" % (bad, len(cases) + 1))
    return bad


if __name__ == "__main__":
    if "--selfcheck" in sys.argv:
        sys.exit(1 if selfcheck() else 0)
    sys.exit(main())
