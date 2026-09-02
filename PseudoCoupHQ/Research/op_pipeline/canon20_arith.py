#!/usr/bin/env python3
"""canon20_arith.py -- JOB 3: RENDER THE PACKED FLOAT ARITHMETIC
FAMILY (condition_table6.py's own grammar) TO INSTRUCTIONS. A SELF-
CONTAINED renderer, same style as canon16_xmm.py/canon16.py (NOT
routed through gen7's AST dispatch -- this family's own WHOLE
expression is always exactly one `<ARITHOP>(P, Q)` call, no outer
wrapper, so there is nothing for gen7's tree-walking to add).

ENTRY CONTRACT: a -> %xmm0 (%rdi if a is int-typed), b -> %xmm1 or
%xmm0 (%rsi or %rdi if int-typed) per canon.designated()'s own C-
calling-rule ("register files counted separately"); answer -> %xmm0.

THE RENDER: resolve P's value into a register (its OWN designated
home if `direct`; a FRESH temp, converted via cvtsi2sd/cvtsi2ss/
cvtss2sd, if `conv`), same for Q (`const` resolves to a FRESH temp,
loaded via GP-immediate + movd/movq, THE RESOLVED CONSTANT -- see
CONST_SIGN below); copy P's register into %xmm0 (skipped if P's own
register already IS %xmm0 -- true whenever P is `direct`, per THE
DIRECT-OPERAND-IS-ALWAYS-XMM0 OBSERVATION below, but computed
generically rather than assumed, so a shape outside that observation
still renders correctly); combine Q into %xmm0 in place with the ONE
real x86 instruction real ship code itself uses (`addsd`/`subsd`/
`mulsd`/`divsd`/`addss`/`subss`/`mulss`/`divss`, AT&T `SRC,DST` --
`%xmm0 = %xmm0 <op> Qreg`, exactly P <op> Q since %xmm0 already holds
P).

THE DIRECT-OPERAND-IS-ALWAYS-XMM0 OBSERVATION (this lap's own survey,
recorded so a future reader does not have to re-derive it): in every
one of the 88 units this file's own driver (canon20.py) actually
converts, the `direct` operand's own designated home is %xmm0 --
either it IS `a` and `a` is float (home %xmm0 by the plain rule), or
it IS `b` and `a` is NOT float (home %xmm0 by the "b takes the only
float slot" rule) -- because the OTHER operand always needs
conversion, which requires it be a DIFFERENT (narrower/int) type, so
the two operands can never BOTH be native floats fighting over %xmm0
in this specific bucket. This file does not rely on the observation
holding (the code path for a `direct` operand not already in %xmm0 is
real and exercised by nothing false), it is recorded only so real
ship code's own near-universal `cvtsi2sd ...,%xmm2; addsd
%xmm2,%xmm0; ret` shape is understood as forced, not coincidental.

THE `const` OPERAND (the `++`/`--` bucket, 8 units): C/C++/Rust/
Swift/Go's own language definition of increment/decrement adds or
subtracts the literal 1 in the OPERAND'S OWN type -- CONST_SIGN reads
the unit's own recorded `operator` field (data, never a grouping key)
to pick +1.0/-1.0, `struct.pack` gives the IEEE754 bit pattern
(forced by construction, the SAME evidence class stage3_vector_
constants_report.txt already used for the float-negate sign mask),
loaded via a GP immediate + `movd`/`movq` -- this lineage's own
existing convention for materializing a resolved constant into an
XMM register (canon16_xmm.py's own `render_float_negate`, unchanged
in spirit).

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon as CANON                                           # noqa: E402
import canon16_xmm as X16                                        # noqa: E402


class Unsupported(Exception):
    pass


TEMP_POOL = X16.XMM_TEMP_POOL_ORDER

CONST_SIGN = {
    "++": 1.0,
    "--": -1.0,
}

CONV_MNEM = {
    "i32_to_f64": "cvtsi2sd",
    "i64_to_f64": "cvtsi2sd",
    "i32_to_f32": "cvtsi2ss",
    "i64_to_f32": "cvtsi2ss",
}

CONV_GP_WIDTH = {
    "i32_to_f64": 32,
    "i64_to_f64": 64,
    "i32_to_f32": 32,
    "i64_to_f32": 64,
}


def gp_reg(family, bits):
    idx = 0 if bits == 64 else 1
    return CANON.render(family, idx)


def float_bits(value, precision):
    if precision == 32:
        return struct.unpack("<I", struct.pack("<f", value))[0]
    return struct.unpack("<Q", struct.pack("<d", value))[0]


def to_signed(bits, width):
    half = 1 << (width - 1)
    full = 1 << width
    if bits >= half:
        return bits - full
    return bits


class _TempAlloc(object):
    def __init__(self):
        self.idx = 0

    def get(self):
        if self.idx >= len(TEMP_POOL):
            raise Unsupported(
                "packed float arithmetic needs more XMM temps than "
                "this file's own ordered pool has -- never measured "
                "in this corpus")
        t = TEMP_POOL[self.idx]
        self.idx = self.idx + 1
        return t


def _resolve_operand(operand, operator, precision, a_is_vector,
                      temps, lines):
    kind = operand[0]

    if kind == "direct":
        tag = operand[1]
        return CANON.designated(tag, "xmm0", a_is_vector)

    if kind == "conv":
        _, tag, convkind = operand
        temp = temps.get()
        if convkind == "f32_to_f64":
            home = CANON.designated(tag, "xmm0", a_is_vector)
            lines.append("cvtss2sd %%%s,%%%s" % (home, temp))
            return temp
        mnem = CONV_MNEM.get(convkind)
        gp_width = CONV_GP_WIDTH.get(convkind)
        if mnem is None:
            raise Unsupported(
                "unknown conversion kind %r -- no return path"
                % (convkind,))
        home = CANON.designated(tag, "rdi", a_is_vector)
        gp = gp_reg(home, gp_width)
        lines.append("%s %%%s,%%%s" % (mnem, gp, temp))
        return temp

    if kind == "const":
        temp = temps.get()
        sign = CONST_SIGN.get(operator)
        if sign is None:
            raise Unsupported(
                "packed float arithmetic const operand with an "
                "unrecognized operator %r -- no return path"
                % (operator,))
        bits = float_bits(sign * 1.0, precision)
        if precision == 32:
            imm = to_signed(bits, 32)
            lines.append("mov $%d,%%eax" % imm)
            lines.append("movd %%eax,%%%s" % temp)
        else:
            imm = to_signed(bits, 64)
            lines.append("movabs $%d,%%rax" % imm)
            lines.append("movq %%rax,%%%s" % temp)
        return temp

    raise Unsupported(
        "packed float arithmetic operand kind %r -- no return path"
        % (kind,))


def render_arith(op_kind, precision, p_operand, q_operand, operator,
                  a_is_vector):
    """[instruction lines], entry contract as in the file header. May
    raise Unsupported (honest refusal, never a guess)."""
    lines = []
    temps = _TempAlloc()

    p_reg = _resolve_operand(p_operand, operator, precision,
                              a_is_vector, temps, lines)
    q_reg = _resolve_operand(q_operand, operator, precision,
                              a_is_vector, temps, lines)

    if p_reg != "xmm0":
        copy_mnem = "movaps" if precision == 32 else "movapd"
        lines.append("%s %%%s,%%xmm0" % (copy_mnem, p_reg))

    suffix = "ss" if precision == 32 else "sd"
    arith_mnem = op_kind + suffix
    lines.append("%s %%%s,%%xmm0" % (arith_mnem, q_reg))
    lines.append("ret")
    return lines
