#!/usr/bin/env python3
"""l3_cart_values.py -- the CARTESIAN probe design's value sets.

the owner's design, settled 2026-08-21 and recorded in
`SUPPORT_conversion_spec.md`, section "the probe design settled
2026-08-21".  This module carries ONLY the value sets, the
representability test, the declaration text and the canonical spelling.
The lanes are emitted by `l3_cart_gen.py`; the fold is
`l3_cart_read.py`.

LEVEL 1   `y = op(x0, x1)` for ALL ordered pairs from a shared set X.
          |X_a| * |X_b| probes per row.  Exhaustive: no pairing scheme,
          no offsets, no ladder.

LEVEL 2   `z = op(op(x0, x1), op(x2, x3))`, all four operands drawn from
          a subset X' of X.  |X'_a|^2 * |X'_b|^2 probes per row.  The two
          intermediates are NEVER enumerated, deduped, capped or unioned
          -- they exist inside the expression.  Both languages evaluate
          identical expressions on identical inputs, so rows compare
          position by position with no alignment step.

THE SETS (the owner's spellings, verbatim).

  X for WHOLE (17 spellings)
      -2^63, -2^63+1, -2^53-1, -2^31, -42, -1, 0, 1, 7, 42, 1000,
      2^31-1, 2^31, 2^53-1, 2^53+1, 2^63-1, 2^64-1

  X for FRACTIONAL (16)
      -max_finite, -1.5, -1.0, -(1.0-1ulp), -0.0, +0.0,
      +min_subnormal, +min_normal, 1.0-1ulp, 1.0, 1.0+1ulp, 1.5, pi,
      2^53, max_finite, 0.1

  X for TRUTH (6)
      true, false, 0, 1, "" (empty text), nil/null
      The non-boolean members are essential: ruby's `&&`/`||`/`and`/`or`
      RETURN AN OPERAND rather than a truth value, so they are
      projections, and only distinct non-boolean operands reveal that.

ABSENCE, NOT COERCION.  A value the holder cannot represent is simply
ABSENT for that row and is recorded as such -- never silently coerced.
`representable()` is the single decision point and `absent_report()`
counts what it dropped, per row family.  Representable means EXACTLY
representable: `f32` does not hold `1.0 + 1ulp(f64)`, so that point is
absent from every `f32` row rather than quietly rounded to `1.0`.

X' FOR LEVEL 2 -- 10 points per form, both sides of every critical point
kept, the ordinary duplicates dropped.  The exact subsets are XP_WHOLE,
XP_FRAC and XP_TRUTH below and each carries its reason.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import decimal
import math
import struct
from fractions import Fraction

# ------------------------------------------------------------------
# X -- whole
# ------------------------------------------------------------------

WHOLE_SPELL = [
    ("-2^63", -(1 << 63)),
    ("-2^63+1", -(1 << 63) + 1),
    ("-2^53-1", -((1 << 53) + 1)),
    ("-2^31", -(1 << 31)),
    ("-42", -42),
    ("-1", -1),
    ("0", 0),
    ("1", 1),
    ("7", 7),
    ("42", 42),
    ("1000", 1000),
    ("2^31-1", (1 << 31) - 1),
    ("2^31", 1 << 31),
    ("2^53-1", (1 << 53) - 1),
    ("2^53+1", (1 << 53) + 1),
    ("2^63-1", (1 << 63) - 1),
    ("2^64-1", (1 << 64) - 1),
]
X_WHOLE = [v for _, v in WHOLE_SPELL]

# X' whole: both sides of 0, of 2^31, of 2^53; the two 64-bit extremes;
# one ordinary value so normal-condition behaviour is measured too.
# Dropped as ordinary duplicates: -2^63+1, -2^53-1, -42, 42, 1000, 2^64-1.
XP_WHOLE_SPELL = ["-2^63", "-1", "0", "1", "7",
                  "2^31-1", "2^31", "2^53-1", "2^53+1", "2^63-1"]
XP_WHOLE = [v for s, v in WHOLE_SPELL if s in XP_WHOLE_SPELL]

# ------------------------------------------------------------------
# X -- fractional (IEEE-754 binary64 spellings)
# ------------------------------------------------------------------

MAXFIN = 1.7976931348623157e308
MINSUB = 5e-324
MINNORM = 2.0 ** -1022
UP1 = math.nextafter(1.0, 2.0)
DN1 = math.nextafter(1.0, 0.0)

FRAC_SPELL = [
    ("-max_finite", -MAXFIN),
    ("-1.5", -1.5),
    ("-1.0", -1.0),
    ("-(1.0-1ulp)", -DN1),
    ("-0.0", -0.0),
    ("+0.0", 0.0),
    ("+min_subnormal", MINSUB),
    ("+min_normal", MINNORM),
    ("1.0-1ulp", DN1),
    ("1.0", 1.0),
    ("1.0+1ulp", UP1),
    ("1.5", 1.5),
    ("pi", math.pi),
    ("2^53", float(1 << 53)),
    ("max_finite", MAXFIN),
    ("0.1", 0.1),
]
X_FRAC = [v for _, v in FRAC_SPELL]

# X' fractional: both sides of 1.0 (1.0-1ulp, 1.0, 1.0+1ulp), both signs
# of zero plus the first value above it (+min_subnormal), both finite
# extremes, a plain negative, and one ordinary non-representable decimal.
# Dropped as ordinary duplicates: -1.5, -(1.0-1ulp), +min_normal, 1.5,
# pi, 2^53.
XP_FRAC_SPELL = ["-max_finite", "-1.0", "-0.0", "+0.0", "+min_subnormal",
                 "1.0-1ulp", "1.0", "1.0+1ulp", "0.1", "max_finite"]
XP_FRAC = [v for s, v in FRAC_SPELL if s in XP_FRAC_SPELL]

# ------------------------------------------------------------------
# X -- truth.  A truth point is a TAGGED spelling, because `0` and `1`
# here are the whole numbers and `""` is the empty text: the point of the
# set is that four of its six members are NOT booleans.
# ------------------------------------------------------------------

TRUTH_SPELL = [
    ("true", ("bool", True)),
    ("false", ("bool", False)),
    ("0", ("int", 0)),
    ("1", ("int", 1)),
    ('""', ("text", "")),
    ("nil", ("nothing", None)),
]
X_TRUTH = [v for _, v in TRUTH_SPELL]

# X' truth: all six.  The set is already smaller than the ten-point
# budget and every member is a critical point of some language's
# truthiness rule, so nothing is dropped.
XP_TRUTH_SPELL = [s for s, _ in TRUTH_SPELL]
XP_TRUTH = list(X_TRUTH)

SETS = {
    ("whole", 1): (WHOLE_SPELL, X_WHOLE),
    ("whole", 2): ([(s, v) for s, v in WHOLE_SPELL if s in XP_WHOLE_SPELL],
                   XP_WHOLE),
    ("fractional", 1): (FRAC_SPELL, X_FRAC),
    ("fractional", 2): ([(s, v) for s, v in FRAC_SPELL
                         if s in XP_FRAC_SPELL], XP_FRAC),
    ("truth", 1): (TRUTH_SPELL, X_TRUTH),
    ("truth", 2): (TRUTH_SPELL, XP_TRUTH),
}

# ------------------------------------------------------------------
# the holders that take part, per language
#   (language, form, rep) -> holder key used in the row tables
# ------------------------------------------------------------------

HOLDERS = {
    ("rust", "truth", "bool"): "bool",
    ("rust", "whole", "i32"): "i32",
    ("rust", "whole", "i64"): "i64",
    ("rust", "whole", "u64"): "u64",
    ("rust", "whole", "i128"): "i128",
    ("rust", "fractional", "f64"): "f64",
    ("rust", "fractional", "f32"): "f32",

    ("ruby", "truth", "TrueClass / FalseClass"): "TrueFalse",
    ("ruby", "whole", "Integer"): "Integer",
    ("ruby", "whole", "Rational"): "Rational",
    ("ruby", "whole", "BigDecimal"): "BigDecimal",
    ("ruby", "fractional", "Float"): "Float",
    ("ruby", "fractional", "Rational"): "Rational",
    ("ruby", "fractional", "BigDecimal"): "BigDecimal",

    # log_061, 2026-08-22 -- the interpreted shape.  Every holder key is
    # the layer-2 census's own `rep` for python, so nothing is invented
    # here; `ctypes.c_int64` is carried deliberately because the census
    # (log_031) found it contradicting the unbounded `int`.
    ("python", "truth", "bool"): "bool",
    ("python", "whole", "int"): "int",
    ("python", "whole", "decimal.Decimal"): "Decimal",
    ("python", "whole", "fractions.Fraction"): "Fraction",
    ("python", "whole", "ctypes.c_int64"): "c_int64",
    ("python", "fractional", "float"): "float",
    ("python", "fractional", "decimal.Decimal"): "Decimal",
    ("python", "fractional", "fractions.Fraction"): "Fraction",

    # log_061, 2026-08-22 -- the compiled shape.  Again the census's own
    # holders (`Research/data_representation/representations_go.json`);
    # go's `int` is a DISTINCT holder from `int64` even where the two
    # share a width, because they are distinct types to the compiler.
    ("go", "truth", "bool"): "bool",
    ("go", "whole", "int32"): "int32",
    ("go", "whole", "int64"): "int64",
    ("go", "whole", "uint64"): "uint64",
    ("go", "whole", "int"): "int",
    ("go", "fractional", "float64"): "float64",
    ("go", "fractional", "float32"): "float32",

    # ------------------------------------------------------------------
    # log_062, 2026-08-22 -- the remaining eight.  Every holder key below
    # is the layer-2 census's own `rep`
    # (`Research/data_representation/representations_<lang>.json`);
    # nothing is invented, widened or renamed here.
    #
    # WHAT IS DELIBERATELY LEFT OUT, and why -- recorded here rather than
    # buried, because a missing column is a finding:
    #
    #   * java `BigDecimal`, kotlin `BigDecimal`, c# `decimal` -- the
    #     shared runtimes (`l3_exec.RT_JAVA` / `RT_KOTLIN` / `RT_CSHARP`)
    #     encode these as `OPAQUE:` / `DEC128:`, and the settled reader
    #     (`l3_per_op_matrices.decode_enc`) decodes neither.  Emitting a
    #     column the fold cannot read is worse than not emitting it.
    #   * java `BigInteger`, kotlin `BigInteger`, c# `BigInteger` --
    #     `RT_JAVA`/`RT_KOTLIN` spell `BIGINT:` as the hex of
    #     `toByteArray()`, which is TWO'S COMPLEMENT, while `decode_enc`
    #     reads a `BIGINT:` payload as signed MAGNITUDE.  `-1` would fold
    #     as `255`.  c#'s runtime has no `BigInteger` case at all.
    #   * php `GMP` and `BCMath` -- `php-cli` is the only php package in
    #     the Airlock image (`Containerfile`), so neither extension is
    #     verified present, and BCMath's holder is a STRING carrying a
    #     number, so `$a . $b` would measure text concatenation.
    #
    # dart `BigInt` and typescript `bigint` ARE carried: `RT_DART` and
    # `RT_TS` both spell `BIGINT:` as signed magnitude, which is exactly
    # what `decode_enc` reads.  Every exclusion above is reversible by
    # correcting that one encoding and re-emitting.

    # php -- route C, dynamically dispatched, holds all six truth points
    ("php", "truth", "bool"): "bool",
    ("php", "whole", "int"): "int",
    ("php", "fractional", "float"): "float",

    # typescript -- statically checked (route A1), run under node
    ("typescript", "truth", "boolean"): "boolean",
    ("typescript", "whole", "number"): "number",
    ("typescript", "whole", "bigint"): "bigint",
    ("typescript", "fractional", "number"): "number",

    # java -- statically checked (route A1)
    ("java", "truth", "boolean"): "boolean",
    ("java", "truth", "Boolean"): "Boolean",
    ("java", "whole", "short"): "short",
    ("java", "whole", "int"): "int",
    ("java", "whole", "long"): "long",
    ("java", "whole", "Integer"): "Integer",
    ("java", "whole", "Long"): "Long",
    ("java", "fractional", "double"): "double",
    ("java", "fractional", "float"): "float",

    # kotlin -- statically checked (route A1)
    # kotlin `ULong` is NOT carried, and the reason is the same one the
    # bignum holders were dropped for: `RT_KOTLIN.enc` has no `ULong`
    # branch (it is an inline class over `Long`, not a `Long`), so every
    # answer would arrive as `OPAQUE:<hex of toString>` and the settled
    # reader would fold an unsigned column as an opaque one.  Reversible
    # by adding the branch to the runtime and re-emitting.
    ("kotlin", "truth", "Boolean"): "Boolean",
    ("kotlin", "whole", "Int"): "Int",
    ("kotlin", "whole", "Long"): "Long",
    ("kotlin", "fractional", "Double"): "Double",
    ("kotlin", "fractional", "Float"): "Float",

    # c++ -- statically checked (route A2)
    ("cpp", "truth", "bool"): "bool",
    ("cpp", "whole", "int32_t"): "int32_t",
    ("cpp", "whole", "int64_t"): "int64_t",
    ("cpp", "whole", "uint64_t"): "uint64_t",
    ("cpp", "whole", "__int128"): "__int128",
    ("cpp", "fractional", "double"): "double",
    ("cpp", "fractional", "float"): "float",

    # swift -- statically checked (route A2)
    ("swift", "truth", "Bool"): "Bool",
    ("swift", "whole", "Int"): "Int",
    ("swift", "whole", "Int32"): "Int32",
    ("swift", "whole", "Int64"): "Int64",
    ("swift", "whole", "UInt64"): "UInt64",
    ("swift", "fractional", "Double"): "Double",
    ("swift", "fractional", "Float"): "Float",

    # dart -- statically checked (route A2).  `double (whole number)` is
    # the census's own name for a WHOLE-form holder that is a binary64,
    # so its representability is double-exactness, not an integer range.
    ("dart", "truth", "bool"): "bool",
    ("dart", "whole", "int"): "int",
    ("dart", "whole", "BigInt"): "BigInt",
    ("dart", "whole", "double (whole number)"): "double_whole",
    ("dart", "fractional", "double"): "double",
    ("dart", "fractional", "num"): "num",

    # c# -- statically checked (route A1)
    ("csharp", "truth", "bool"): "bool",
    ("csharp", "whole", "short"): "short",
    ("csharp", "whole", "int"): "int",
    ("csharp", "whole", "long"): "long",
    ("csharp", "whole", "ulong"): "ulong",
    ("csharp", "fractional", "double"): "double",
    ("csharp", "fractional", "float"): "float",
}

INT_RANGE = {
    "i16": (-(1 << 15), (1 << 15) - 1),
    "i32": (-(1 << 31), (1 << 31) - 1),
    "i64": (-(1 << 63), (1 << 63) - 1),
    "u64": (0, (1 << 64) - 1),
    "i128": (-(1 << 127), (1 << 127) - 1),
}

# Holder names collide across languages -- python's unbounded `int` and
# go's 64-bit `int` are the same word for two different things -- so the
# fixed-width table is keyed by LANGUAGE first.  A holder absent from its
# language's table is unbounded.
INT_RANGE_BY_LANG = {
    "rust": INT_RANGE,
    "go": {
        "int32": INT_RANGE["i32"],
        "int64": INT_RANGE["i64"],
        "uint64": INT_RANGE["u64"],
        # go's `int` is 64-bit on every platform this line runs on;
        # `go env GOARCH` is amd64 in the container image.
        "int": INT_RANGE["i64"],
    },
    "python": {
        # `int`, `Decimal` and `Fraction` are unbounded and are absent
        # here on purpose.  `ctypes.c_int64` is the fixed-width one.
        "c_int64": INT_RANGE["i64"],
    },
    # log_062 -- the remaining eight.  A holder absent from its language's
    # table is UNBOUNDED (dart `BigInt`, typescript `bigint`); a holder
    # listed in DOUBLE_WHOLE below is neither, and is decided by
    # double-exactness instead.
    "php": {
        # php has no unsigned integer type and no bignum in core; `int`
        # is 64-bit signed on every 64-bit build.  An out-of-range
        # literal becomes a FLOAT silently, which is exactly why the
        # point has to be absent rather than written.
        "int": INT_RANGE["i64"],
    },
    "typescript": {},                    # `number` is DOUBLE_WHOLE,
                                         # `bigint` is unbounded
    "java": {
        "short": INT_RANGE["i16"],
        "int": INT_RANGE["i32"],
        "long": INT_RANGE["i64"],
        "Integer": INT_RANGE["i32"],     # the box holds exactly what the
        "Long": INT_RANGE["i64"],        # primitive holds
    },
    "kotlin": {
        "Int": INT_RANGE["i32"],
        "Long": INT_RANGE["i64"],
    },
    "cpp": {
        "int32_t": INT_RANGE["i32"],
        "int64_t": INT_RANGE["i64"],
        "uint64_t": INT_RANGE["u64"],
        "__int128": INT_RANGE["i128"],
    },
    "swift": {
        "Int": INT_RANGE["i64"],         # 64-bit on every platform this
        "Int32": INT_RANGE["i32"],       # line runs on
        "Int64": INT_RANGE["i64"],
        "UInt64": INT_RANGE["u64"],
    },
    "dart": {
        # the dart VM's `int` is 64-bit signed; `BigInt` is unbounded and
        # is absent here; `double (whole number)` is DOUBLE_WHOLE.
        "int": INT_RANGE["i64"],
    },
    "csharp": {
        "short": INT_RANGE["i16"],
        "int": INT_RANGE["i32"],
        "long": INT_RANGE["i64"],
        "ulong": INT_RANGE["u64"],
    },
}

# WHOLE-form holders that are IEEE-754 binary64.  The census names them
# itself (dart `double (whole number)`, typescript `number` under the
# whole form), and their representability is EXACTNESS AS A DOUBLE, not
# an integer range: `2^53+1`, `2^63-1` and `2^64-1` are absent from them
# while `2^63` and `2^31` are present.
DOUBLE_WHOLE = {("typescript", "number"), ("dart", "double_whole")}

# languages whose truth holder is a real boolean TYPE, so only `true` and
# `false` of the six truth points are representable.  The dynamic
# languages hold all six as themselves.
# log_062: seven of the remaining eight declare a real boolean TYPE, so
# `0`, `1`, `""` and `nil` are absent from every truth row over them --
# the same two-of-six rust and go already carry.  php is route C and
# dynamically dispatched, so it holds all six as themselves, like ruby
# and python.
STATIC_TRUTH = {"rust", "go", "typescript", "java", "kotlin", "cpp",
                "swift", "dart", "csharp"}

# holders that carry no signed zero, so `-0.0` is ABSENT from every
# fractional row over them (ruby `Rational`, python `Fraction`).
NO_SIGNED_ZERO = {("ruby", "Rational"), ("python", "Fraction")}

# holders that are IEEE-754 binary32, so a binary64 point is absent
# unless it survives the narrowing exactly.
F32_HOLDERS = {("rust", "f32"), ("go", "float32"),
               ("java", "float"), ("kotlin", "Float"), ("cpp", "float"),
               ("swift", "Float"), ("csharp", "float")}


def _as_f32(x):
    try:
        return struct.unpack(">f", struct.pack(">f", x))[0]
    except (OverflowError, struct.error):
        return math.copysign(float("inf"), x)


def _same_bits(a, b):
    return struct.pack(">d", a) == struct.pack(">d", b)


def representable(lang, form, holder, v):
    """Can this holder hold this value EXACTLY?  The only decision point.

    False means the value is ABSENT for that row -- never coerced, never
    rounded, never wrapped.
    """
    if form == "truth":
        if lang in STATIC_TRUTH:
            # a real boolean TYPE (rust `bool`, go `bool`) holds exactly
            # two of the six truth points; the other four are absent from
            # every truth row over it
            return v[0] == "bool"
        return True              # ruby / python hold all six as themselves
    if form == "whole":
        if (lang, holder) in DOUBLE_WHOLE:
            # a WHOLE-form holder that is a binary64.  `float(v) == v` is
            # an EXACT comparison in python between an int and a float,
            # so this is the exactness test and not a rounding test.
            try:
                return float(v) == v
            except OverflowError:
                return False
        lo, hi = INT_RANGE_BY_LANG.get(lang, {}).get(holder, (None, None))
        if lo is None:
            return True          # unbounded: ruby Integer/Rational/
                                 # BigDecimal, python int/Decimal/Fraction,
                                 # dart BigInt, typescript bigint
        return lo <= v <= hi
    # fractional
    if (lang, holder) in F32_HOLDERS:
        return _same_bits(float(_as_f32(v)), v) and not math.isinf(_as_f32(v))
    if (lang, holder) in NO_SIGNED_ZERO:
        # ruby `Rational` / python `Fraction` carry no signed zero, so
        # -0.0 has no exact representation in them
        return not (v == 0.0 and math.copysign(1.0, v) < 0)
    return True


def points(lang, form, holder, level):
    """the (spelling, value) points this holder actually holds, in the
    canonical order of the set -- and the spellings it cannot hold."""
    spell, _ = SETS[(form, level)]
    keep, absent = [], []
    for s, v in spell:
        if representable(lang, form, holder, v):
            keep.append((s, v))
        else:
            absent.append(s)
    return keep, absent


def set_id(lang, form, holder, level):
    """the identity of a row's operand set.  Two rows compare position by
    position only when their set ids match on both sides."""
    keep, _ = points(lang, form, holder, level)
    return "%s/L%d/%d:%s" % (form, level, len(keep),
                             ",".join(s for s, _ in keep))


# ------------------------------------------------------------------
# declaration text
# ------------------------------------------------------------------

def _rs_int_lit(holder, v):
    lo, hi = INT_RANGE[holder]
    if v == lo:
        return "%s::MIN" % holder
    if v == hi:
        return "%s::MAX" % holder
    return "%s%s" % (v, holder)


def _f_lit(x):
    """python repr round-trips and is a legal float literal in both rust
    and ruby (`5e-324`, `1.7976931348623157e+308`, `-0.0`)."""
    r = repr(x)
    if r in ("inf", "-inf", "nan"):
        raise ValueError("the cartesian sets carry finite values only")
    return r


def _rs_f_lit(holder, x):
    r = _f_lit(x)
    if "." not in r and "e" not in r and "E" not in r:
        r += ".0"
    return "%s%s" % (r, holder)


# ------------------------------------------------------------------
# go literals.  THE NEGATIVE-ZERO HAZARD, stated where it is handled:
# go's untyped constants have no signed zero at all -- the source text
# `-0.0` is the constant zero, and `var v float64 = -0.0` stores +0.0.
# The layer-2 census already spells the point `math.Copysign(0, -1)`
# (`representations_go.json`, `spell.fractional.negzero`, with the
# float32 override `float32(math.Copysign(0, -1))`), and that spelling
# is reused verbatim here rather than reinvented.
# ------------------------------------------------------------------

GO_NEGZERO = {"float64": "math.Copysign(0, -1)",
              "float32": "float32(math.Copysign(0, -1))"}


def _go_f_lit(holder, x):
    if x == 0.0 and math.copysign(1.0, x) < 0:
        return GO_NEGZERO[holder]
    r = _f_lit(x)
    if "." not in r and "e" not in r and "E" not in r:
        r += ".0"
    return r


# ------------------------------------------------------------------
# log_062 -- the remaining eight.  Two hazards decide most of what
# follows, and both are stated where they are handled:
#
#   THE EXTREME-LITERAL HAZARD.  `-9223372036854775808` is not a legal
#   `long` literal in java or c# (the token is read as `unary minus`
#   applied to a literal one past the maximum), and in php it silently
#   becomes a FLOAT.  Every language's own named constant is written
#   instead -- `Long.MIN_VALUE`, `long.MinValue`, `INT64_MIN`,
#   `Int.min`, `PHP_INT_MIN` -- so the declaration means the integer it
#   says it means.
#
#   THE FLOAT-LITERAL HAZARD.  python's `repr` round-trips and is a
#   legal double literal in every one of these languages (`5e-324`,
#   `1.7976931348623157e+308`, `-0.0`).  `-0.0` keeps its sign in all
#   eight -- go was the exception, and go is already handled above.
#   A binary32 holder only ever sees points `representable()` already
#   proved exact in binary32, so the `f` suffix never rounds.
# ------------------------------------------------------------------

def _named_int(lang, holder, v):
    """the language's own name for a holder's extreme, or None."""
    lo, hi = INT_RANGE_BY_LANG.get(lang, {}).get(holder, (None, None))
    if lo is None or v not in (lo, hi):
        return None
    top = (v == hi)
    if lang == "java":
        base = {"short": "Short", "int": "Integer", "long": "Long",
                "Integer": "Integer", "Long": "Long"}[holder]
        return "%s.%s" % (base, "MAX_VALUE" if top else "MIN_VALUE")
    if lang == "kotlin":
        return "%s.%s" % (holder, "MAX_VALUE" if top else "MIN_VALUE")
    if lang == "csharp":
        return "%s.%s" % (holder, "MaxValue" if top else "MinValue")
    if lang == "swift":
        return "%s.%s" % (holder, "max" if top else "min")
    if lang == "cpp":
        return {"int32_t": "INT32", "int64_t": "INT64",
                "uint64_t": "UINT64"}.get(holder,
                                          "") + ("_MAX" if top else "_MIN")
    if lang == "php":
        return "PHP_INT_MAX" if top else "PHP_INT_MIN"
    return None


def _f_suffixed(x, suffix):
    r = _f_lit(x)
    if "." not in r and "e" not in r and "E" not in r:
        r += ".0"
    return r + suffix


def _decl_eight(lang, form, holder, name, v):
    """the eight languages of log_062.  Returns None for anything else."""
    if lang == "php":
        if form == "truth":
            kind, val = v
            if kind == "bool":
                return "$%s = %s;" % (name, "true" if val else "false")
            if kind == "int":
                return "$%s = %d;" % (name, val)
            if kind == "text":
                return '$%s = "";' % name
            return "$%s = null;" % name
        if form == "whole":
            nm = _named_int(lang, holder, v)
            return "$%s = %s;" % (name, nm if nm else "%d" % v)
        return "$%s = %s;" % (name, _f_lit(v))

    if lang == "typescript":
        if form == "truth":
            return "let %s: boolean = %s;" % (name,
                                              "true" if v[1] else "false")
        if form == "whole":
            if holder == "bigint":
                return "let %s: bigint = %dn;" % (name, v)
            return "let %s: number = %d;" % (name, v)
        return "let %s: number = %s;" % (name, _f_lit(v))

    if lang == "java":
        if form == "truth":
            return "%s %s = %s;" % (holder, name,
                                    "true" if v[1] else "false")
        if form == "whole":
            nm = _named_int(lang, holder, v)
            if nm:
                return "%s %s = %s;" % (holder, name, nm)
            if holder == "short":
                return "short %s = (short) %d;" % (name, v)
            if holder in ("long", "Long"):
                return "%s %s = %dL;" % (holder, name, v)
            return "%s %s = %d;" % (holder, name, v)
        if holder == "float":
            return "float %s = %s;" % (name, _f_suffixed(v, "f"))
        return "double %s = %s;" % (name, _f_lit(v))

    if lang == "kotlin":
        if form == "truth":
            return "val %s: Boolean = %s" % (name,
                                             "true" if v[1] else "false")
        if form == "whole":
            nm = _named_int(lang, holder, v)
            if nm:
                return "val %s: %s = %s" % (name, holder, nm)
            if holder == "Long":
                return "val %s: Long = %dL" % (name, v)
            return "val %s: Int = %d" % (name, v)
        if holder == "Float":
            return "val %s: Float = %s" % (name, _f_suffixed(v, "f"))
        return "val %s: Double = %s" % (name, _f_lit(v))

    if lang == "cpp":
        if form == "truth":
            return "bool %s = %s;" % (name, "true" if v[1] else "false")
        if form == "whole":
            if holder == "__int128":
                # every whole point fits in a 64-bit literal on one side
                # or the other, so the 128-bit holder is built by widening
                # a 64-bit constant -- c++ has no 128-bit literal.
                if v >= 0:
                    return ("__int128 %s = (__int128)UINT64_C(%d);"
                            % (name, v))
                if v == INT_RANGE["i64"][0]:
                    return "__int128 %s = (__int128)INT64_MIN;" % name
                return "__int128 %s = (__int128)INT64_C(%d);" % (name, v)
            nm = _named_int(lang, holder, v)
            if nm:
                return "%s %s = %s;" % (holder, name, nm)
            if holder == "uint64_t":
                return "uint64_t %s = UINT64_C(%d);" % (name, v)
            if holder == "int64_t":
                return "int64_t %s = INT64_C(%d);" % (name, v)
            return "int32_t %s = %d;" % (name, v)
        if holder == "float":
            return "float %s = %s;" % (name, _f_suffixed(v, "f"))
        return "double %s = %s;" % (name, _f_lit(v))

    if lang == "swift":
        if form == "truth":
            return "let %s: Bool = %s" % (name, "true" if v[1] else "false")
        if form == "whole":
            nm = _named_int(lang, holder, v)
            return "let %s: %s = %s" % (name, holder,
                                        nm if nm else "%d" % v)
        return "let %s: %s = %s" % (name, holder, _f_lit(v))

    if lang == "dart":
        if form == "truth":
            return "bool %s = %s;" % (name, "true" if v[1] else "false")
        if form == "whole":
            if holder == "BigInt":
                return 'BigInt %s = BigInt.parse("%d");' % (name, v)
            if holder == "double_whole":
                # a WHOLE point in a binary64 holder.  A trailing `.0` is
                # written so the literal is unambiguously a double.
                return "double %s = %d.0;" % (name, v)
            return "int %s = %d;" % (name, v)
        return "%s %s = %s;" % ("double" if holder == "double" else "num",
                                name, _f_lit(v))

    if lang == "csharp":
        if form == "truth":
            return "bool %s = %s;" % (name, "true" if v[1] else "false")
        if form == "whole":
            nm = _named_int(lang, holder, v)
            if nm:
                return "%s %s = %s;" % (holder, name, nm)
            if holder == "short":
                return "short %s = (short)%d;" % (name, v)
            if holder == "long":
                return "long %s = %dL;" % (name, v)
            if holder == "ulong":
                return "ulong %s = %dUL;" % (name, v)
            return "int %s = %d;" % (name, v)
        if holder == "float":
            return "float %s = %s;" % (name, _f_suffixed(v, "f"))
        return "double %s = %s;" % (name, _f_lit(v))

    return None


def decl(lang, form, holder, name, v):
    """one `name = value` statement in the target language."""
    eight = _decl_eight(lang, form, holder, name, v)
    if eight is not None:
        return eight
    if lang == "go":
        # go is statically typed and refuses every implicit conversion,
        # so the holder's own type name is written out.  An out-of-range
        # constant is a COMPILE error, not a wrap -- which is exactly why
        # `representable()` keeps such a point out of the row entirely.
        if form == "truth":
            return "var %s bool = %s;" % (name, "true" if v[1] else "false")
        if form == "whole":
            return "var %s %s = %d;" % (name, holder, v)
        return "var %s %s = %s;" % (name, holder, _go_f_lit(holder, v))
    if lang == "python":
        if form == "truth":
            kind, val = v
            if kind == "bool":
                return "%s = %s" % (name, "True" if val else "False")
            if kind == "int":
                return "%s = %d" % (name, val)
            if kind == "text":
                return '%s = ""' % name
            return "%s = None" % name
        if form == "whole":
            if holder == "int":
                return "%s = %d" % (name, v)
            if holder == "c_int64":
                return "%s = ctypes.c_int64(%d).value" % (name, v)
            if holder == "Fraction":
                return "%s = Fraction(%d, 1)" % (name, v)
            return '%s = Decimal("%d")' % (name, v)
        if holder == "float":
            return "%s = %s" % (name, _f_lit(v))
        if holder == "Fraction":
            # `Fraction(<float literal>)` is the EXACT binary value of
            # that double, the same object ruby's `Rational(<float>)`
            # builds -- not a decimal reading of the printed digits.
            return "%s = Fraction(%s)" % (name, _f_lit(v))
        # `Decimal("<text>")` is decimal-to-decimal and therefore exactly
        # the decimal the text names, the same construction ruby's
        # `BigDecimal((v).to_s)` performs.  Never `Decimal(<float>)`,
        # which would be the double's exact binary expansion instead and
        # would disagree with `canon_point` below.
        return '%s = Decimal("%s")' % (name, _f_lit(v))
    if lang == "rust":
        if form == "truth":
            return "let %s: bool = %s;" % (name, "true" if v[1] else "false")
        if form == "whole":
            return "let %s: %s = %s;" % (name, holder, _rs_int_lit(holder, v))
        return "let %s: %s = %s;" % (name, holder, _rs_f_lit(holder, v))
    # ruby
    if form == "truth":
        kind, val = v
        if kind == "bool":
            return "%s = %s" % (name, "true" if val else "false")
        if kind == "int":
            return "%s = %d" % (name, val)
        if kind == "text":
            return '%s = ""' % name
        return "%s = nil" % name
    if form == "whole":
        if holder == "Integer":
            return "%s = %d" % (name, v)
        if holder == "Rational":
            return "%s = Rational(%d, 1)" % (name, v)
        return "%s = BigDecimal((%d).to_s)" % (name, v)
    if holder == "Float":
        return "%s = %s" % (name, _f_lit(v))
    if holder == "Rational":
        return "%s = Rational(%s)" % (name, _f_lit(v))
    return "%s = BigDecimal((%s).to_s)" % (name, _f_lit(v))


# ------------------------------------------------------------------
# canonical spelling of an INPUT point, under the v2 canon rules
# ------------------------------------------------------------------

def _signbit(x):
    return struct.pack(">d", x)[0] & 0x80


def canon_point(lang, form, holder, v, canon_num):
    """canon_num is l3_per_op_matrices_v2.canon_num (the v2 rulings)."""
    if form == "truth":
        kind, val = v
        if kind == "bool":
            return "true" if val else "false"
        if kind == "int":
            return canon_num(Fraction(val))
        if kind == "text":
            return "t|" + "|0|0|0"
        return "null"                 # the canon's own spelling for nothing
    if form == "whole":
        return canon_num(Fraction(v))
    if v == 0.0:
        return "[-1, 0.0, 0]" if _signbit(v) else "[1, 0.0, 0]"
    if holder in ("BigDecimal", "Decimal"):
        # a DECIMAL holder built from the printed text genuinely holds
        # that decimal exactly, so its canon is the decimal reading --
        # the same string `decl` used, so the two agree by construction
        # (log_057 checked this path and found it sound).
        return canon_num(Fraction(decimal.Decimal(repr(v))))
    return canon_num(Fraction(v))


# ------------------------------------------------------------------
# self-check
# ------------------------------------------------------------------

def _selfcheck():
    assert len(X_WHOLE) == len(set(X_WHOLE)) == 17
    assert len(XP_WHOLE) == 10, XP_WHOLE
    keys = [struct.pack(">d", v).hex() for v in X_FRAC]
    assert len(keys) == len(set(keys)) == 16
    assert len(XP_FRAC) == 10, XP_FRAC
    assert len(X_TRUTH) == 6 and len(XP_TRUTH) == 6
    for (lang, form, rep), holder in HOLDERS.items():
        for lvl in (1, 2):
            keep, absent = points(lang, form, holder, lvl)
            assert keep, (lang, holder, lvl)


_selfcheck()


if __name__ == "__main__":
    print("CARTESIAN value sets -- the owner 2026-08-21\n")
    for form, lvl in (("whole", 1), ("whole", 2), ("fractional", 1),
                      ("fractional", 2), ("truth", 1), ("truth", 2)):
        spell, _ = SETS[(form, lvl)]
        print("%-11s %s  (%d)" % (form, "X " if lvl == 1 else "X'",
                                  len(spell)))
        print("            %s" % ", ".join(s for s, _ in spell))
    print("\nper-holder representability (absent = the holder cannot hold "
          "the point; it is left out, never coerced)\n")
    for (lang, form, rep), holder in sorted(HOLDERS.items()):
        for lvl in (1, 2):
            keep, absent = points(lang, form, holder, lvl)
            print("  %-5s %-11s %-11s L%d  %2d kept  %2d absent%s"
                  % (lang, form, rep, lvl, len(keep), len(absent),
                     ("  [" + ", ".join(absent) + "]") if absent else ""))
