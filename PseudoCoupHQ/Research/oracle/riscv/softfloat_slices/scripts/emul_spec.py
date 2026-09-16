#!/usr/bin/env python3
"""The 67 operations' SoftFloat signatures, derived from the operation name.

Every name in the corpus is self-describing: `f64_add` is two float64 in and
one out, `f32_to_i64` is one float32 in and one int64 out, `i32_to_f16` the
other way, `f16_roundToInt` carries the runtime `exact` flag Sail passes.
Nothing here is guessed - `scripts/verify_emulations.py` cross-checks every
entry against the operand widths recorded in the flattened IR itself.
"""

FLOAT = {"f16": (16, 5, 10), "bf16": (16, 8, 7),
         "f32": (32, 8, 23), "f64": (64, 11, 52)}
INT = {"i32": (32, True), "i64": (64, True),
       "ui32": (32, False), "ui64": (64, False)}

SF_FLOAT_T = {"f16": "float16_t", "bf16": "bfloat16_t",
              "f32": "float32_t", "f64": "float64_t"}
SF_INT_T = {"i32": "int_fast32_t", "i64": "int_fast64_t",
            "ui32": "uint_fast32_t", "ui64": "uint_fast64_t"}

BINARY = ("add", "sub", "mul", "div")
COMPARE = ("eq", "le_quiet", "lt_quiet", "le", "lt")


class Operand(object):
    __slots__ = ("kind", "width", "exp", "man", "signed", "tag")

    def __init__(self, kind, width, exp=0, man=0, signed=False, tag=""):
        self.kind = kind          # 'float' | 'int' | 'bool'
        self.width = width
        self.exp = exp
        self.man = man
        self.signed = signed
        self.tag = tag            # 'f16' / 'i32' / ...

    @property
    def bias(self):
        return (1 << (self.exp - 1)) - 1

    @property
    def mask(self):
        return (1 << self.width) - 1


def flt(tag):
    w, e, m = FLOAT[tag]
    return Operand("float", w, e, m, tag=tag)


def integer(tag):
    w, s = INT[tag]
    return Operand("int", w, signed=s, tag=tag)


def boolean():
    return Operand("bool", 1, tag="bool")


def spec(op):
    """-> (params, ret, sf_call) where sf_call describes the reference call."""
    if "_to_" in op:
        src, dst = op.split("_to_", 1)
        if src in FLOAT:
            params = [flt(src)]
            ret = flt(dst) if dst in FLOAT else integer(dst)
            # the twelve float->int conversions take (a, rm, exact=true)
            extra = "rm_exact" if dst in INT else "plain"
            return params, ret, extra
        params = [integer(src)]
        return params, flt(dst), "plain"
    base, tail = op.split("_", 1)
    if tail == "mulAdd":
        return [flt(base)] * 3, flt(base), "plain"
    if tail == "sqrt":
        return [flt(base)], flt(base), "plain"
    if tail == "roundToInt":
        return [flt(base), boolean()], flt(base), "rm_exactarg"
    if tail in BINARY:
        return [flt(base)] * 2, flt(base), "plain"
    if tail in COMPARE:
        return [flt(base)] * 2, boolean(), "plain"
    raise ValueError("unknown operation " + op)


# ------------------------------------------------------------- edge cases --
def float_edges(o):
    top = o.mask
    expall = (1 << o.exp) - 1
    man = (1 << o.man) - 1
    named = [
        0,                                          # +0
        expall << o.man,                            # +inf
        (expall << o.man) | (1 << (o.man - 1)),     # quiet NaN
        (expall << o.man) | 1,                      # signalling NaN
        ((expall - 1) << o.man) | man,              # largest normal
        1 << o.man,                                 # smallest normal
        man,                                        # largest subnormal
        1,                                          # smallest subnormal
        o.bias << o.man,                            # 1.0
        (o.bias + 1) << o.man,                      # 2.0
        (o.bias - 1) << o.man,                      # 0.5
    ]
    out = set()
    for p in named:
        for q in (p, p | (1 << (o.width - 1))):     # both signs
            for d in (-1, 0, 1):                    # one ulp either side
                out.add((q + d) & top)
    return sorted(out)


def int_edges(o):
    top = o.mask
    vals = {0, 1, top, top - 1, 1 << (o.width - 1),
            (1 << (o.width - 1)) - 1, (1 << (o.width - 1)) + 1}
    for k in (1, 7, 8, 15, 16, 23, 24, 31, 32, 52, 53, 62, 63):
        if k < o.width:
            for d in (-1, 0, 1):
                vals.add(((1 << k) + d) & top)
    return sorted(v & top for v in vals)


def edges(o):
    if o.kind == "float":
        return float_edges(o)
    if o.kind == "bool":
        return [0, 1]
    return int_edges(o)


OPS = [
    "f16_add", "f16_div", "f16_eq", "f16_le", "f16_le_quiet", "f16_lt",
    "f16_lt_quiet", "f16_mul", "f16_mulAdd", "f16_roundToInt", "f16_sqrt",
    "f16_sub", "f16_to_f32", "f16_to_f64", "f16_to_i32", "f16_to_i64",
    "f16_to_ui32", "f16_to_ui64",
    "f32_add", "f32_div", "f32_eq", "f32_le", "f32_le_quiet", "f32_lt",
    "f32_lt_quiet", "f32_mul", "f32_mulAdd", "f32_roundToInt", "f32_sqrt",
    "f32_sub", "f32_to_bf16", "f32_to_f16", "f32_to_f64", "f32_to_i32",
    "f32_to_i64", "f32_to_ui32", "f32_to_ui64",
    "f64_add", "f64_div", "f64_eq", "f64_le", "f64_le_quiet", "f64_lt",
    "f64_lt_quiet", "f64_mul", "f64_mulAdd", "f64_roundToInt", "f64_sqrt",
    "f64_sub", "f64_to_f16", "f64_to_f32", "f64_to_i32", "f64_to_i64",
    "f64_to_ui32", "f64_to_ui64",
    "i32_to_f16", "i32_to_f32", "i32_to_f64",
    "i64_to_f16", "i64_to_f32", "i64_to_f64",
    "ui32_to_f16", "ui32_to_f32", "ui32_to_f64",
    "ui64_to_f16", "ui64_to_f32", "ui64_to_f64",
]
