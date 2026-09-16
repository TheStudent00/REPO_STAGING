#!/usr/bin/env python3
"""Shared spec for the INTEGER-ONLY RISC-V arch-units.

`build_arch_units_int.py` composes them, `verify_arch_units_int.py` verifies
them, and both read the tables here:

  * the operand and result TYPES of a compiler-operator, under C's usual
    arithmetic conversions and go's (much simpler) rules;
  * how an operand's bit pattern is presented in a machine register by the
    LP64 / go register ABI;
  * the INPUT PLAN -- the edge values of an integer operand and the banded
    random draw, written out once per language so all six programs draw the
    identical sequence.

Nothing here is guessed from the disassembly: the result type is C's own, and
`verify_arch_units_int.py` has the C compiler confirm it with `__typeof__`.
"""

# --------------------------------------------------------------- the types --
# tag -> (kind, width, signed)     kind: 'i' integer, 'b' boolean, 'f' float
TAG = {
    "b":   ("b", 1, False),
    "i32": ("i", 32, True),
    "u32": ("i", 32, False),
    "i64": ("i", 64, True),
    "u64": ("i", 64, False),
    "f32": ("f", 32, False),
    "f64": ("f", 64, False),
}

# the corpus's source type names -> tag
SRC_TAG = {
    "bool": "b",
    "int32_t": "i32", "int64_t": "i64", "uint64_t": "u64",
    "float": "f32", "double": "f64",
    "int32": "i32", "int64": "i64", "uint64": "u64",
    "float32": "f32", "float64": "f64",
}

# tag -> the language's spelling
C_TYPE = {"b": "_Bool", "i32": "int32_t", "u32": "uint32_t",
          "i64": "int64_t", "u64": "uint64_t", "f32": "float", "f64": "double"}
GO_TYPE = {"b": "bool", "i32": "int32", "u32": "uint32", "i64": "int64",
           "u64": "uint64", "f32": "float32", "f64": "float64"}

SLUG = {"b": "bool", "i32": "i32", "u32": "u32", "i64": "i64", "u64": "u64",
        "f32": "f32", "f64": "f64"}


def width(tag):
    return TAG[tag][1]


def kind(tag):
    return TAG[tag][0]


def signed(tag):
    return TAG[tag][2]


# ------------------------------------------------- C's arithmetic conversions --
def c_promote(t):
    """the integer promotions: _Bool -> int, everything else unchanged."""
    return "i32" if t == "b" else t


def c_usual(x, y):
    """the usual arithmetic conversions on two operand tags."""
    if "f64" in (x, y):
        return "f64"
    if "f32" in (x, y):
        return "f32"
    x, y = c_promote(x), c_promote(y)
    if x == y:
        return x
    if "u64" in (x, y):
        return "u64"
    return "i64" if 64 in (width(x), width(y)) else "i32"


C_BOOLEAN_OPS = {"==", "!=", "<", "<=", ">", ">=", "&&", "||", "!"}
C_SIZE_OPS = {"sizeof", "_Alignof", "__alignof", "__alignof__"}
# operators whose C result has the UNPROMOTED type of the operand
C_SAME_TYPE_UNARY = {"++", "--", "__extension__"}
C_BINARY = {"+", "-", "*", "/", "%", "&", "|", "^"}

GO_BOOLEAN_OPS = {"==", "!=", "<", "<=", ">", ">=", "&&", "||", "!"}
GO_SHIFTS = {"<<", ">>"}
GO_BINARY = {"+", "-", "*", "/", "%", "&", "|", "^", "&^"}


def result_tag(row):
    """-> the tag of the compiler-operator's own result type.

    For `&a` this is the tag of the STATED REDUCTION `*(&a)`: `&a` itself is a
    pointer, which is not a function of the operand bits.
    """
    op, lang = row["operator"], row["lang"]
    lhs = SRC_TAG[row["lhs_type"]]
    rhs = SRC_TAG[row["rhs_type"]] if row["rhs_type"] is not None else None
    if lang == "c":
        if op in C_SIZE_OPS:
            return "u64"                       # size_t
        if op in C_BOOLEAN_OPS:
            return "i32"                       # C comparisons answer `int`
        if op == "&" and rhs is None:
            return lhs                         # the reduction *(&a)
        if rhs is None:
            if op in C_SAME_TYPE_UNARY:
                return lhs                     # a++, --a, __extension__ a
            return c_promote(lhs)              # +a, -a, ~a
        return c_usual(lhs, rhs)
    # go
    if op in GO_BOOLEAN_OPS:
        return "b"
    if op == "&" and rhs is None:
        return lhs                             # the reduction *(&a)
    return lhs                                 # binary, shift and unary alike


def is_reduced(row):
    return row["operator"] == "&" and row["rhs_type"] is None


def answer_register(row):
    return "fa0" if kind(result_tag(row)) == "f" else "a0"


# ------------------------------------------------------------ the input plan --
def int_edges(tag):
    """Every edge value of an integer operand of this width.

    zero, one, minus one, the signed and unsigned extremes, the value just
    inside and just outside every bit boundary, and the powers of two around
    every shift amount that matters on RV64 (31/32/33, 63/64/65) and beyond.
    """
    w = width(tag)
    mask = (1 << w) - 1 if w < 64 else 0xFFFFFFFFFFFFFFFF
    vals = set()
    for v in (0, 1, 2, 3, mask, mask - 1, mask - 2,
              1 << (w - 1), (1 << (w - 1)) - 1, (1 << (w - 1)) + 1,
              (1 << (w - 1)) - 2, (1 << (w - 1)) + 2):
        vals.add(v & mask)
    # every bit boundary, and the shift amounts at and either side of a width
    for k in (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 30, 31, 32, 33,
              52, 53, 62, 63):
        for d in (-1, 0, 1):
            vals.add(((1 << k) + d) & mask)
    # the shift counts themselves, at and above both widths
    for s in (5, 6, 7, 30, 31, 32, 33, 34, 62, 63, 64, 65, 66,
              127, 128, 255, 256):
        vals.add(s & mask)
        vals.add((-s) & mask)                  # and their negations
    return sorted(vals)


def float_edges(tag):
    """the float edge set, same shape as emul_spec.float_edges."""
    w = width(tag)
    exp, man = (8, 23) if w == 32 else (11, 52)
    bias = (1 << (exp - 1)) - 1
    top = (1 << w) - 1
    expall = (1 << exp) - 1
    manall = (1 << man) - 1
    named = [0, expall << man, (expall << man) | (1 << (man - 1)),
             (expall << man) | 1, ((expall - 1) << man) | manall, 1 << man,
             manall, 1, bias << man, (bias + 1) << man, (bias - 1) << man]
    out = set()
    for p in named:
        for q in (p, p | (1 << (w - 1))):
            for d in (-1, 0, 1):
                out.add((q + d) & top)
    return sorted(out)


def edges(tag):
    if kind(tag) == "b":
        return [0, 1]
    if kind(tag) == "f":
        return float_edges(tag)
    return int_edges(tag)


def opmask(tag):
    w = width(tag)
    return (1 << w) - 1 if w < 64 else 0xFFFFFFFFFFFFFFFF


# ------------------------------------------------- the random draw, per language --
# Exactly TWO rnd() calls per operand per banded iteration and ONE per uniform
# iteration, in the same order in all six programs, so every program sees the
# identical input sequence.

def uniform_line(lang, i, tag, indent):
    m = opmask(tag)
    if lang in ("c", "cpp"):
        return indent + "c%d = rnd() & 0x%xULL;" % (i, m)
    if lang == "rust":
        return indent + "c%d = rnd(&mut s) & 0x%xu64;" % (i, m)
    return indent + "c%d = rnd() & 0x%x" % (i, m)


def _band_int_expr(lang, i, tag, indent):
    """Eight bands: zero, all-ones, the sign bit, a shift count in [0,130),
    a power of two +/- 1, a small value, a value just below all-ones, and a
    plain uniform draw.  Divisors of zero, shift counts at and above both
    widths and the most-negative-over-minus-one all fall out of this."""
    w = width(tag)
    m = opmask(tag)
    sign = 1 << (w - 1)
    if lang in ("c", "cpp"):
        L = [indent + "{ uint64_t u = rnd(), v = rnd();"
                      " switch ((unsigned)(u % 8)) {"]
        L.append(indent + "  case 0: c%d = 0; break;" % i)
        L.append(indent + "  case 1: c%d = 0x%xULL; break;" % (i, m))
        L.append(indent + "  case 2: c%d = 0x%xULL; break;" % (i, sign))
        L.append(indent + "  case 3: c%d = v %% 130ULL; break;" % i)
        L.append(indent + "  case 4: c%d = ((1ULL << (v %% %dULL))"
                          " + ((u >> 3) %% 3ULL)) - 1ULL; break;" % (i, w))
        L.append(indent + "  case 5: c%d = v & 0xffULL; break;" % i)
        L.append(indent + "  case 6: c%d = 0x%xULL ^ (v & 0xffULL); break;"
                 % (i, m))
        L.append(indent + "  default: c%d = v; break; }" % i)
        L.append(indent + "  c%d &= 0x%xULL; }" % (i, m))
        return L
    if lang == "rust":
        L = [indent + "{ let u = rnd(&mut s); let v = rnd(&mut s);"
                      " match u % 8 {"]
        L.append(indent + "  0 => c%d = 0u64," % i)
        L.append(indent + "  1 => c%d = 0x%xu64," % (i, m))
        L.append(indent + "  2 => c%d = 0x%xu64," % (i, sign))
        L.append(indent + "  3 => c%d = v %% 130u64," % i)
        L.append(indent + "  4 => c%d = ((1u64 << (v %% %du64))"
                          ".wrapping_add((u >> 3) %% 3u64))"
                          ".wrapping_sub(1u64)," % (i, w))
        L.append(indent + "  5 => c%d = v & 0xffu64," % i)
        L.append(indent + "  6 => c%d = 0x%xu64 ^ (v & 0xffu64)," % (i, m))
        L.append(indent + "  _ => c%d = v, }" % i)
        L.append(indent + "  c%d &= 0x%xu64; }" % (i, m))
        return L
    L = [indent + "{ u := rnd(); v := rnd(); switch u % 8 {"]
    L.append(indent + "case 0:\n" + indent + "\tc%d = 0" % i)
    L.append(indent + "case 1:\n" + indent + "\tc%d = 0x%x" % (i, m))
    L.append(indent + "case 2:\n" + indent + "\tc%d = 0x%x" % (i, sign))
    L.append(indent + "case 3:\n" + indent + "\tc%d = v %% 130" % i)
    L.append(indent + "case 4:\n" + indent + "\tc%d = (1<<(v%%%d)) +"
             " ((u >> 3) %% 3) - 1" % (i, w))
    L.append(indent + "case 5:\n" + indent + "\tc%d = v & 0xff" % i)
    L.append(indent + "case 6:\n" + indent + "\tc%d = 0x%x ^ (v & 0xff)"
             % (i, m))
    L.append(indent + "default:\n" + indent + "\tc%d = v" % i)
    L.append(indent + "}")
    L.append(indent + "c%d &= 0x%x }" % (i, m))
    return L


def _band_float_expr(lang, i, tag, indent):
    """the exponent-banded float draw, three rnd() calls, as in the float
    layer's verify_arch_units.py."""
    w = width(tag)
    exp, man = (8, 23) if w == 32 else (11, 52)
    bias = (1 << (exp - 1)) - 1
    em, mm = (1 << exp) - 1, (1 << man) - 1
    if lang in ("c", "cpp"):
        return [indent + "{ uint64_t sg = rnd() & 1ULL;"
                " uint64_t ex = (uint64_t)(%d + (int64_t)(rnd() %% 33) - 16)"
                " & 0x%xULL; uint64_t mn = rnd() & 0x%xULL;"
                " c%d = (sg << %d) | (ex << %d) | mn; }"
                % (bias, em, mm, i, w - 1, man)]
    if lang == "rust":
        return [indent + "{ let sg = rnd(&mut s) & 1u64;"
                " let ex = ((%d as i64 + ((rnd(&mut s) %% 33) as i64) - 16)"
                " as u64) & 0x%xu64; let mn = rnd(&mut s) & 0x%xu64;"
                " c%d = (sg << %d) | (ex << %d) | mn; }"
                % (bias, em, mm, i, w - 1, man)]
    return [indent + "{ sg := rnd() & 1;"
            " ex := uint64(int64(%d)+int64(rnd()%%33)-16) & 0x%x;"
            " mn := rnd() & 0x%x; c%d = (sg << %d) | (ex << %d) | mn }"
            % (bias, em, mm, i, w - 1, man)]


def band_lines(lang, tags, indent):
    out = []
    for i, t in enumerate(tags):
        if kind(t) == "f":
            out += _band_float_expr(lang, i, t, indent)
        elif kind(t) == "b":
            out.append(uniform_line(lang, i, t, indent))
        else:
            out += _band_int_expr(lang, i, t, indent)
    return out


def plan(row, n_rand, n_band):
    """-> (operand tags, edge lists, total inputs)"""
    tags = [SRC_TAG[row["lhs_type"]]]
    if row["rhs_type"] is not None:
        tags.append(SRC_TAG[row["rhs_type"]])
    ed = [edges(t) for t in tags]
    n = 1
    for e in ed:
        n *= len(e)
    return tags, ed, n + n_rand + n_band
