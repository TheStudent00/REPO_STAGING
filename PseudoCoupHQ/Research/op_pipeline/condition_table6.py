#!/usr/bin/env python3
"""condition_table6.py -- JOB 3: THE PACKED FLOAT ARITHMETIC FAMILY
(Add64F0x2/Sub64F0x2/Mul64F0x2/Div64F0x2/Add32F0x4/Sub32F0x4/Mul32F0x4/
Div32F0x4). Classifies ONE unit's own `normal_path_raw` under a small,
closed grammar -- shape recognition only, no z3, no rendering; see
canon20_arith.py for those.

THE POPULATION, surveyed directly (this lap's own script, over every
not-yet-converged straight-line unit whose raw text contains one of
the eight op names above, EXCLUDING the units whose `normal_path_raw`
top-level is `ins@0(...)` -- the SAME "largest surviving tree picked
an intermediate write, not the final read" defect condition_table5.py's
own file header already found and named for the packed-mask-compare
family; NOT this file's own scope, diagnosed only): 162 units total,
122 with a clean (non-`ins@0`-top) extraction. Of those 122, the WHOLE
`normal_path_raw` is ALWAYS exactly one `<ARITHOP>(P, Q)` call (no
outer wrapper at all -- the arithmetic result IS the returned value),
and P/Q fall into a small closed set:

    ('direct', 'a')                 -- ex128@0(in0:256), a itself,
                                        already a native float/double
    ('direct', 'b')                 -- ex128@0(in1:256), b itself
    ('conv', tag, kind)             -- a type coercion of a or b into
                                        this op's own float width (see
                                        THE CONVERSION KINDS below)
    ('const', None)                 -- zx128(ld<W>/g0(OFF:64)), a
                                        compile-time float LITERAL
                                        this corpus's own real ship
                                        code loads from `.rodata` via
                                        a rip-relative operand (the
                                        SAME kind of unresolvable
                                        address stage3_vector_
                                        constants_report.txt already
                                        named for the float-negate
                                        family -- resolved here by the
                                        SAME method: the source
                                        operator names the value
                                        exactly, `++`/`--` can only
                                        ever add +1.0/-1.0 in the
                                        result's own type, per C/C++/
                                        Rust/Swift/Go's own language
                                        definition of increment/
                                        decrement on a float, so no
                                        guess is needed)

    Measured bucket sizes (122 clean units): 72 are (direct, conv) or
    (conv, direct); 16 are (direct, const) with operator in {++, --};
    24 are a THIRD shape this file does NOT classify -- the classic
    "u64/i64 -> double via a magic bit-pattern constant" idiom
    (`punpckldq`/`subpd`/`unpckhpd` in real ship's own mnem; VEX's own
    `InterleaveLO32x4`/`Sub64Fx2`/`64HLtoV128` in the lift) -- OUT OF
    SCOPE for this file (two DIFFERENT `.rodata` constants would need
    resolving, not one, and the arithmetic itself is a 2-instruction
    SEQUENCE standing in for one conversion, not a single op this
    grammar's own `('conv', ...)` shape can name) -- `classify_arith`
    returns None for it, an honest, silent skip, same as every other
    out-of-grammar shape.

THE CONVERSION KINDS (`kind`, forced by construction -- direct read of
the VEX op names pyvex's own lifter uses for CVTSI2SD/CVTSI2SS/
CVTSS2SD, cross-checked against this corpus's own real ship `mnem`
for every sampled unit, see canon20.py's own report):

    i32_to_f64   -- I32StoF64(ex32@0(inK:64))        ~ CVTSI2SD, 32-bit
    i64_to_f64   -- I64StoF64(<rounding mode>,inK:64) ~ CVTSI2SD, 64-bit
    f32_to_f64   -- F32toF64(ex32@0(inK:256))         ~ CVTSS2SD
    i32_to_f32   -- F64toF32(<rm>,I32StoF64(ex32@0(inK:64)))
                    ~ CVTSI2SS, 32-bit (int32->f64->f32 is mathematically
                    a SINGLE rounding -- int32 fits exactly in f64, so
                    no double-rounding error, matching real CVTSI2SS
                    bit-for-bit; the SAME reasoning condition_table5.py's
                    sibling file already used for `bool`-typed operands)
    i64_to_f32   -- F64toF32(<rm>,I64StoF64(<rm>,inK:64))
                    ~ CVTSI2SS, 64-bit (SAME two-step-is-one-rounding
                    argument -- int64 does NOT always fit exactly in
                    f64's 52-bit mantissa, so this one is measured, not
                    assumed: canon20_behaviour_check.py's own FPA gate
                    proves bit-for-bit equality against real CVTSI2SS
                    directly, so a rounding mismatch, if the argument
                    were wrong, would DISPROVE rather than silently
                    pass)

`inK` is `in0` (tag "a") or `in1` (tag "b") -- read directly off which
of the two appears inside the conversion, never guessed.

A `bool`-typed C/C++ operand lifts through the SAME `I32StoF64`/
`I64StoF64` atom an `int`/`int32_t` operand does (a bool occupies a
whole 32-bit GP register at the machine level; measured, canon4_units'
own real ship mnem for every `bool`-typed unit sampled uses plain
`cvtsi2ss`/`cvtsi2sd`, no different from `int`) -- so this file never
special-cases "bool", the grammar already covers it.

THE SPELLING BAN: this table is keyed by VEX op names (Add64F0x2,
I32StoF64, F64toF32, ...) and by structural operand identity
(ex128@0(in0:256) vs (in1:256), which `inK` a conversion wraps), never
by the source-language operator token (except to resolve the ONE
`++`/`--` constant sign, which is READ off the unit's own recorded
`operator` field as DATA, not used as a matching/grouping key); this
file classifies ONE unit's own expression and never groups or pairs
units.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match as TM                                        # noqa: E402

parse_expr = TM.parse_expr
serialize = TM.serialize

ARITH_OPS = {
    "Add64F0x2": ("add", 64),
    "Sub64F0x2": ("sub", 64),
    "Mul64F0x2": ("mul", 64),
    "Div64F0x2": ("div", 64),
    "Add32F0x4": ("add", 32),
    "Sub32F0x4": ("sub", 32),
    "Mul32F0x4": ("mul", 32),
    "Div32F0x4": ("div", 32),
}


def _which_in(text):
    if "in0" in text:
        return "a"
    if "in1" in text:
        return "b"
    return None


def classify_conv_expr(tree):
    """(tag, kind) for a conversion sub-expression, or None. See file
    header's own THE CONVERSION KINDS."""
    if tree[0] != "node":
        return None
    name, args = tree[1], tree[2]

    if name == "I32StoF64":
        if len(args) != 1:
            return None
        inner = args[0]
        if inner[0] != "node" or inner[1] != "ex32@0":
            return None
        tag = _which_in(serialize(inner))
        if tag is None:
            return None
        return (tag, "i32_to_f64")

    if name == "I64StoF64":
        if len(args) != 2:
            return None
        val_text = serialize(args[1])
        tag = _which_in(val_text)
        if tag is None:
            return None
        if val_text not in ("in0:64", "in1:64"):
            return None
        return (tag, "i64_to_f64")

    if name == "F32toF64":
        if len(args) != 1:
            return None
        inner = args[0]
        if inner[0] != "node" or inner[1] != "ex32@0":
            return None
        tag = _which_in(serialize(inner))
        if tag is None:
            return None
        return (tag, "f32_to_f64")

    if name == "F64toF32":
        if len(args) != 2:
            return None
        sub = classify_conv_expr(args[1])
        if sub is None:
            return None
        tag, kind = sub
        if kind == "i32_to_f64":
            return (tag, "i32_to_f32")
        if kind == "i64_to_f64":
            return (tag, "i64_to_f32")
        return None

    return None


def classify_operand(tree):
    """('direct', tag) | ('conv', tag, kind) | ('const', None) | None.
    See file header's own grammar."""
    if tree == ("node", "ex128@0", [("leaf", "in0:256")]):
        return ("direct", "a")
    if tree == ("node", "ex128@0", [("leaf", "in1:256")]):
        return ("direct", "b")

    if tree[0] == "node" and tree[1] == "ex128@0" and \
            len(tree[2]) == 1:
        inner = tree[2][0]
        if inner[0] == "node" and inner[1] == "ins@0" and \
                len(inner[2]) == 2:
            conv = classify_conv_expr(inner[2][1])
            if conv is not None:
                tag, kind = conv
                return ("conv", tag, kind)

    if tree[0] == "node" and tree[1] == "zx128" and len(tree[2]) == 1:
        inner = tree[2][0]
        if inner[0] == "node" and inner[1].startswith("ld") and \
                "/g0" in inner[1]:
            return ("const", None)

    return None


def classify_arith(raw_text):
    """(op_kind, precision, p_operand, q_operand) or None -- see file
    header. `raw_text` must be the unit's WHOLE `normal_path_raw`
    (this family is never wrapped in this corpus's own measured
    population -- a unit whose top-level is NOT one of the eight op
    names is out of this file's own scope by construction)."""
    tree = parse_expr(raw_text.strip())
    if tree[0] != "node":
        return None
    name, args = tree[1], tree[2]
    if name not in ARITH_OPS:
        return None
    if len(args) != 2:
        return None
    op_kind, precision = ARITH_OPS[name]
    p_operand = classify_operand(args[0])
    q_operand = classify_operand(args[1])
    if p_operand is None or q_operand is None:
        return None
    return op_kind, precision, p_operand, q_operand
