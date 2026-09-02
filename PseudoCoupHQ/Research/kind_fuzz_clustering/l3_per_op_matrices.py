#!/usr/bin/env python3
"""l3_per_op_matrices.py -- the settled PER-OPERATOR matrices.

the owner ruled the design 2026-08-20 in conversation (settled, not
proposed); recorded in Planning/node_0_3_research/
node_0_3_2_kind_fuzz_clustering/SUPPORT_conversion_spec.md, dated
section "per-operator matrices".

Each `language.operator` gets its OWN rectangular matrix.  No shared
cross-language row space, no padding rows for holders a language
lacks.  One PROBE per row.  Columns identical on every row of every
matrix:

  probe_id,
  lhs_holder, lhs_value_class, lhs_bytes, lhs_canonical,
  lhs_canonical_exact,
  rhs_holder, rhs_value_class, rhs_bytes, rhs_canonical,
  rhs_canonical_exact,
  output_type, output_literal, output_canonical,
  output_canonical_exact,
  REFUSE, RAISE, ABORT, raise_kind

Canonical forms (the owner's rulings, exact):
  numeric    [sign, mant, expo], sign in {-1,0,1}, mant in [1,2)
             (floating-point normalization; integer mants were
             REJECTED -- the decomposition is not unique), expo an
             integer.  Zero = [0, 0, ].  Specials stay words: inf,
             -inf, nan, negzero.  The readable decimal mant is
             rounded to 18 fractional digits and marked with a
             leading `~` when the decimal is not exact; the
             *_canonical_exact column carries the mant as an exact
             rational (or integer) at full precision.
  text       [NFC utf-8 hex, byte_len, codepoint_len, grapheme_len],
             grapheme fallback as documented in l3_matrix_extended.py.
  container  [sorted values | key_format | order_flag] per the spec.

Inputs (lhs/rhs bytes + canonical) are filled on EVERY row: they are
known from the value class and the rep's read-rule, independent of
outcome.  A rep's read-rule applies: ctypes.c_int64 holding bytes
8000000000000000 canonicalizes as [-1, 1, 63] (the rep flips the
reading) while an unbounded int reads [1, 1, 63].

REFUSE rows: the static languages' acceptance_<lang>_A2/A1.json
refusals appear as rows with inputs filled (at the acceptance stage's
representative value class, BASE_ORDER of l3_accept.py), outputs
empty, REFUSE=1.  codegen_refuse rows inside the answers files join
them with their own value classes.  ABORT is the stopped-by-OS
outcome; its rows carry inputs, empty outputs, ABORT=1 (the OS return
code stays in the answers file).

Filename escaping: an operator that is entirely [a-z_] after
space->underscore keeps its spelling; every other operator is spelled
character by character from a fixed table (+ -> plus, < -> lt, ...).
The reverse mapping is written to matrices/README.md.

Assembly only.  No probe runs.
"""

import csv
import decimal
import json
import os
import struct
import sys
import time
import unicodedata
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from l3_matrix_extended import grapheme_count, _canon_value, \
    container_coords, ACCEPT_FILES                                 # noqa
from l3_answers import NINE, THREE                                 # noqa
from l3_wordops import ADMIT as WORD_ADMIT                         # noqa

OUT_DIR = os.path.join(HERE, "matrices")

COLUMNS = ["probe_id",
           "lhs_holder", "lhs_value_class", "lhs_bytes",
           "lhs_canonical", "lhs_canonical_exact",
           "rhs_holder", "rhs_value_class", "rhs_bytes",
           "rhs_canonical", "rhs_canonical_exact",
           "output_type", "output_literal", "output_canonical",
           "output_canonical_exact",
           "REFUSE", "RAISE", "ABORT", "raise_kind"]

decimal.getcontext().prec = 60

# ------------------------------------------------------------------
# the abstract value classes
# ------------------------------------------------------------------

WHOLE = {"base_zero": 0, "base_42": 42, "p53_plus1": (1 << 53) + 1,
         "i64max": (1 << 63) - 1, "i64max_plus1": (1 << 63),
         "u64max": (1 << 64) - 1}
# fractional classes: the shared double literal, plus the special words
FRAC_NUM = {"base_1_5": 1.5, "base_pi": 3.141592653589793,
            "point1": 0.1}
FRAC_SPECIAL = {"inf": "inf", "nan": "nan", "negzero": "negzero"}
TEXT = {"base_empty": "", "base_hello": "hello",
        "base_lines": "line one\nline two",
        "clef": "\U0001D11E", "eacute": "é",
        "escapes": 'quote " backslash \\ tab\there'}
SEQ = {"base": [1, 2, 3], "bigint": [9223372036854775808],
       "empty": [], "mixed": [1, "two", 3.0, True, None],
       "strs": ["a", "b"]}
KEYED = {"empty": {}, "emptykey": {"": "empty-string key"},
         "flat": {"a": 1, "b": 2, "c": 3},
         "intlike": {"1": "string-one-key", "b": 2},
         "nested": {"outer": {"inner": [1, 2]}}}
NESTING = {"mixed_depth": [1, [2, {"k": (3, None, "t")}], True],
           "seq_in_map": {"outer": {"inner": [1, 2]}},
           "seq_in_seq": [[1, 2], [3, 4]]}

# the value class an acceptance-stage (verdict) probe carries, per
# form -- BASE_ORDER of l3_accept.py resolved per form
ACCEPT_CLASS = {"whole": "base_42", "text": "base_hello",
                "fractional": "base_1_5", "truth": "true",
                "nothing": "null", "sequence": "base",
                "keyed": "flat", "nesting": "seq_in_seq"}

# ------------------------------------------------------------------
# rep read-rules -- (lang, holder) -> rule
#   ("s", bits)  bounded signed, two's complement
#   ("u", bits)  bounded unsigned
#   ("big",)     unbounded exact integer
#   ("f64",) ("f32",)  IEEE floating holder
#   ("dec",)     decimal-string-exact holder (built from the literal's
#                decimal spelling: java/kotlin BigDecimal("..."),
#                ruby BigDecimal((v).to_s), c# decimal, php BCMath)
#   ("binfrac",) exact-rational holder built FROM the binary double
#                (python Decimal(0.1)/Fraction(0.1), ruby Rational)
# ------------------------------------------------------------------

REP_RULES = {
    # go
    ("go", "int"): ("s", 64), ("go", "int32"): ("s", 32),
    ("go", "int64"): ("s", 64), ("go", "uint64"): ("u", 64),
    ("go", "float64"): ("f64",), ("go", "float32"): ("f32",),
    # rust
    ("rust", "i32"): ("s", 32), ("rust", "i64"): ("s", 64),
    ("rust", "i128"): ("s", 128), ("rust", "u64"): ("u", 64),
    ("rust", "f64"): ("f64",), ("rust", "f32"): ("f32",),
    # cpp
    ("cpp", "int32_t"): ("s", 32), ("cpp", "int64_t"): ("s", 64),
    ("cpp", "__int128"): ("s", 128), ("cpp", "uint64_t"): ("u", 64),
    ("cpp", "double"): ("f64",), ("cpp", "float"): ("f32",),
    # java
    ("java", "short"): ("s", 16), ("java", "int"): ("s", 32),
    ("java", "Integer"): ("s", 32), ("java", "long"): ("s", 64),
    ("java", "Long"): ("s", 64), ("java", "BigInteger"): ("big",),
    ("java", "double"): ("f64",), ("java", "float"): ("f32",),
    ("java", "BigDecimal"): ("dec",),
    # csharp
    ("csharp", "short"): ("s", 16), ("csharp", "int"): ("s", 32),
    ("csharp", "long"): ("s", 64), ("csharp", "ulong"): ("u", 64),
    ("csharp", "System.Numerics.BigInteger"): ("big",),
    ("csharp", "double"): ("f64",), ("csharp", "float"): ("f32",),
    ("csharp", "decimal"): ("dec",),
    # typescript
    ("typescript", "bigint"): ("big",),
    ("typescript", "number"): ("f64",),
    # swift
    ("swift", "Int"): ("s", 64), ("swift", "Int32"): ("s", 32),
    ("swift", "Int64"): ("s", 64), ("swift", "UInt64"): ("u", 64),
    ("swift", "Double"): ("f64",), ("swift", "Float"): ("f32",),
    # kotlin
    ("kotlin", "Int"): ("s", 32), ("kotlin", "Long"): ("s", 64),
    ("kotlin", "ULong"): ("u", 64), ("kotlin", "BigInteger"): ("big",),
    ("kotlin", "Double"): ("f64",), ("kotlin", "Float"): ("f32",),
    ("kotlin", "BigDecimal"): ("dec",),
    # dart
    ("dart", "int"): ("s", 64), ("dart", "BigInt"): ("big",),
    ("dart", "double (whole number)"): ("f64",),
    ("dart", "double"): ("f64",), ("dart", "num"): ("f64",),
    # python
    ("python", "int"): ("big",),
    ("python", "decimal.Decimal"): ("big",),        # whole: Decimal(42) exact
    ("python", "fractions.Fraction"): ("big",),
    ("python", "ctypes.c_int64"): ("s", 64),
    ("python", "float"): ("f64",),
    # fractional python Decimal/Fraction are built FROM the double:
    # handled below by form (binfrac overrides big for fractional)
    # ruby
    ("ruby", "Integer"): ("big",),
    ("ruby", "Rational"): ("big",),                 # whole: Rational(v,1)
    ("ruby", "BigDecimal"): ("dec",),
    ("ruby", "Float"): ("f64",),
    # php
    ("php", "int"): ("s", 64),
    ("php", "GMP (ext-gmp)"): ("big",),
    ("php", "BCMath string-carried number (ext-bcmath)"): ("big",),
    ("php", "float"): ("f64",),
}
# fractional-form overrides where the holder is built from the double
FRAC_RULE_OVERRIDE = {
    ("python", "decimal.Decimal"): ("binfrac",),
    ("python", "fractions.Fraction"): ("binfrac",),
    ("ruby", "Rational"): ("binfrac",),
}


# ------------------------------------------------------------------
# canonical spellings
# ------------------------------------------------------------------

def canon_from_fraction(fr):
    """Fraction -> (canonical, exact-mant) strings, mant in [1,2)."""
    if fr == 0:
        return "[0, 0, ]", ""
    sign = 1 if fr > 0 else -1
    a = abs(fr)
    e = a.numerator.bit_length() - a.denominator.bit_length()
    if Fraction(2) ** e > a:
        e -= 1
    m = a / Fraction(2) ** e
    exact = (str(m.numerator) if m.denominator == 1
             else "%d/%d" % (m.numerator, m.denominator))
    d = (decimal.Decimal(m.numerator) / decimal.Decimal(m.denominator))
    q = d.quantize(decimal.Decimal(1).scaleb(-18))
    s = format(q, "f").rstrip("0").rstrip(".")
    if not s:
        s = "0"
    try:
        rounded = Fraction(s) != m
    except ValueError:
        rounded = True
    if rounded:
        s = "~" + s
    return "[%d, %s, %d]" % (sign, s, e), exact


def _desurrogate(s):
    """A UTF-16 code-unit holder (java/kotlin/c# char) can answer a
    LONE SURROGATE.  It is not encodable text; spell it \\uXXXX so the
    canonical stays honest instead of crashing."""
    if any(0xD800 <= ord(c) <= 0xDFFF for c in s):
        return "".join("\\u%04x" % ord(c)
                       if 0xD800 <= ord(c) <= 0xDFFF else c for c in s)
    return s


def fix_tree(v):
    if isinstance(v, str):
        return _desurrogate(v)
    if isinstance(v, list):
        return [fix_tree(x) for x in v]
    if isinstance(v, tuple):
        return tuple(fix_tree(x) for x in v)
    if isinstance(v, dict):
        return {fix_tree(k): fix_tree(x) for k, x in v.items()}
    return v


def canon_text(s):
    s = _desurrogate(s)
    nfc = unicodedata.normalize("NFC", s)
    b = s.encode("utf-8")
    return "[%s, %d, %d, %d]" % (nfc.encode("utf-8").hex(),
                                 len(b), len(s), grapheme_count(s))


def canon_container_obj(obj):
    if isinstance(obj, dict):
        d, order_flag = obj, "not-applicable"
    elif isinstance(obj, (list, tuple)):
        d = {i: v for i, v in enumerate(obj)}
        sv0 = [_canon_value(v) for v in obj]
        order_flag = "as-sorted" if sorted(sv0) == sv0 else "reordered"
    elif isinstance(obj, (set, frozenset)):
        d = {i: v for i, v in enumerate(sorted(obj, key=_canon_value))}
        order_flag = "unordered"
    else:
        return "unparsed:%r" % (obj,)
    kinds = set()
    for k in d:
        kinds.add("integer" if isinstance(k, (int, bool)) else
                  "text" if isinstance(k, str) else "other")
    key_format = kinds.pop() if len(kinds) == 1 else \
        ("mixed" if kinds else "empty")
    sv = sorted(_canon_value(v) for v in d.values())
    return "[%s | %s | %s]" % (",".join(sv), key_format, order_flag)


def coords_str(cc):
    """container_coords dict -> the same bracket spelling."""
    if cc.get("unparsed") is not None:
        return "unparsed:%s" % cc["unparsed"]
    sv = cc["sorted_values"]
    if not isinstance(sv, list):
        return "unparsed:"
    return "[%s | %s | %s]" % (",".join(sv), cc["key_format"],
                               cc["order_flag"])


# ------------------------------------------------------------------
# held values -- inputs, filled on every row
# ------------------------------------------------------------------

def _f_bits(f, bits):
    if bits == 64:
        return struct.pack(">d", f).hex()
    return struct.pack(">f", struct.unpack(">f", struct.pack(">f", f))[0]
                       ).hex()


UNRESOLVED = {}


def held(lang, holder, form, vclass):
    """-> (bytes, canonical, exact) for an input operand."""
    if form == "nothing":
        return "null", "null", ""
    if form == "truth":
        return vclass, vclass, ""
    if form == "text":
        s = TEXT.get(vclass)
        if s is None:
            return _unres(lang, holder, form, vclass)
        return s.encode("utf-8").hex(), canon_text(s), ""
    if form in ("sequence", "keyed", "nesting"):
        table = {"sequence": SEQ, "keyed": KEYED,
                 "nesting": NESTING}[form]
        obj = table.get(vclass)
        if obj is None:
            return _unres(lang, holder, form, vclass)
        return repr(obj), canon_container_obj(obj), ""
    rule = None
    if form == "fractional":
        rule = FRAC_RULE_OVERRIDE.get((lang, holder))
    if rule is None:
        rule = REP_RULES.get((lang, holder))
    if rule is None:
        return _unres(lang, holder, form, vclass)
    if form == "whole":
        v = WHOLE.get(vclass)
        if v is None:
            return _unres(lang, holder, form, vclass)
        if rule[0] in ("s", "u"):
            bits = rule[1]
            w = v % (1 << bits)
            heldv = w - (1 << bits) if (rule[0] == "s"
                                        and w >= (1 << (bits - 1))) else w
            by = format(w, "0%dx" % (bits // 4))
            c, ex = canon_from_fraction(Fraction(heldv))
            return by, c, ex
        if rule[0] == "f64" or rule[0] == "f32":
            bits = 64 if rule[0] == "f64" else 32
            f = float(v)
            if rule[0] == "f32":
                f = struct.unpack(">f", struct.pack(">f", f))[0]
            c, ex = canon_from_fraction(Fraction(f))
            return _f_bits(float(v), bits), c, ex
        # big / dec: exact integer
        by = ("-" if v < 0 else "") + format(abs(v), "x")
        c, ex = canon_from_fraction(Fraction(v))
        return by, c, ex
    # fractional
    sp = FRAC_SPECIAL.get(vclass)
    if sp is not None:
        if rule[0] in ("f64", "f32"):
            bits = 64 if rule[0] == "f64" else 32
            f = {"inf": float("inf"), "nan": float("nan"),
                 "negzero": -0.0}[sp]
            return _f_bits(f, bits), sp, ""
        return sp, sp, ""
    fv = FRAC_NUM.get(vclass)
    if fv is None:
        return _unres(lang, holder, form, vclass)
    if rule[0] == "f32":
        f = struct.unpack(">f", struct.pack(">f", fv))[0]
        c, ex = canon_from_fraction(Fraction(f))
        return _f_bits(fv, 32), c, ex
    if rule[0] == "f64" or rule[0] == "binfrac":
        c, ex = canon_from_fraction(Fraction(fv))
        by = (_f_bits(fv, 64) if rule[0] == "f64"
              else "%d/%d" % (Fraction(fv).numerator,
                              Fraction(fv).denominator))
        return by, c, ex
    if rule[0] == "dec":
        lit = {"base_1_5": "1.5", "base_pi": "3.141592653589793",
               "point1": "0.1"}[vclass]
        fr = Fraction(decimal.Decimal(lit))
        c, ex = canon_from_fraction(fr)
        return lit, c, ex
    return _unres(lang, holder, form, vclass)


def _unres(lang, holder, form, vclass):
    UNRESOLVED[(lang, holder, form, vclass)] = \
        UNRESOLVED.get((lang, holder, form, vclass), 0) + 1
    return vclass, "unresolved:%s" % vclass, ""


# ------------------------------------------------------------------
# output decoding, bit grain -- the answers_<lang>.json encodings
# ------------------------------------------------------------------

def _split_top(s, sep=","):
    out, depth, cur = [], 0, []
    for ch in s:
        if ch in "[({":
            depth += 1
        elif ch in "])}":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur or out:
        out.append("".join(cur))
    return out


def decode_enc(s):
    """full encoding string -> python value, or ('raw', s) opaque."""
    if s == "NULL" or s == "UNDEFINED" or s == "UNIT":
        return None
    if s == "PTR":
        return ("raw", s)
    if s.startswith("BOOL:"):
        return s[5:] == "true"
    if s.startswith("INT:"):
        _, bits, hx = s.split(":", 2)
        bits = int(bits)
        v = int(hx, 16)
        if v >= (1 << (bits - 1)):
            v -= (1 << bits)
        return v
    if s.startswith("UINT:"):
        _, bits, hx = s.split(":", 2)
        return int(hx, 16)
    if s.startswith("BIGINT:"):
        p = s[7:]
        neg = p.startswith("-")
        return -int(p.lstrip("-"), 16) if neg else (int(p, 16) if p else 0)
    if s.startswith("FLOAT:"):
        _, bits, hx = s.split(":", 2)
        raw = bytes.fromhex(hx)
        return struct.unpack(">d" if int(bits) == 64 else ">f", raw)[0]
    if s.startswith("STR:"):
        parts = s.split(":", 3)
        # STR:<ownlen>:<bytelen>:<hex>
        hx = parts[3] if len(parts) > 3 else ""
        try:
            return bytes.fromhex(hx).decode("utf-8")
        except ValueError:
            return ("raw", s)
    if s.startswith("CHAR:"):
        try:
            return chr(int(s[5:], 16))
        except ValueError:
            return ("raw", s)
    if s.startswith("SOME(") and s.endswith(")"):
        return decode_enc(s[5:-1])
    if s.startswith("REF(") and s.endswith(")"):
        return decode_enc(s[4:-1])
    for kind, op, cl in (("LIST", "[", "]"), ("TUP", "[", "]")):
        if s.startswith(kind + ":"):
            i = s.index("[") if "[" in s else -1
            if i < 0 or not s.endswith("]"):
                return ("raw", s)
            body = s[i + 1:-1]
            if not body:
                return []
            return [decode_enc(x) for x in _split_top(body)]
    if s.startswith("MAP:"):
        i = s.index("[") if "[" in s else -1
        if i < 0 or not s.endswith("]"):
            return ("raw", s)
        body = s[i + 1:-1]
        out = {}
        for part in _split_top(body):
            kv = _split_top(part, sep="=")
            # entries are k=>v; split on the first top-level '=>'
            j, depth = -1, 0
            for x in range(len(part) - 1):
                if part[x] in "[({":
                    depth += 1
                elif part[x] in "])}":
                    depth -= 1
                elif depth == 0 and part[x] == "=" and part[x + 1] == ">":
                    j = x
                    break
            if j < 0:
                return ("raw", s)
            k = decode_enc(part[:j])
            v = decode_enc(part[j + 2:])
            if isinstance(k, (list, dict)):
                k = repr(k)
            out[k if isinstance(k, (str, int, bool, float)) or k is None
                else repr(k)] = v
        return out
    if s.startswith("STRUCT:"):
        i = s.index("[") if "[" in s else -1
        if i < 0 or not s.endswith("]"):
            return ("raw", s)
        body = s[i + 1:-1]
        out = {}
        for part in _split_top(body):
            if "=" not in part:
                return ("raw", s)
            name, _, enc = part.partition("=")
            out[name] = decode_enc(enc)
        return out
    return ("raw", s)


def canon_output_value(v, raw_enc):
    """decoded python value -> (canonical, exact)."""
    if isinstance(v, tuple) and len(v) == 2 and v[0] == "raw":
        return "opaque:%s" % v[1][:60], ""
    if v is None:
        return "null", ""
    if isinstance(v, bool):
        return ("true" if v else "false"), ""
    if isinstance(v, int):
        return canon_from_fraction(Fraction(v))
    if isinstance(v, float):
        if v != v:
            return "nan", ""
        if v == float("inf"):
            return "inf", ""
        if v == float("-inf"):
            return "-inf", ""
        if v == 0.0 and struct.pack(">d", v)[0] & 0x80:
            return "negzero", ""
        return canon_from_fraction(Fraction(v))
    if isinstance(v, str):
        return canon_text(v), ""
    if isinstance(v, (list, dict, set, frozenset, tuple)):
        return canon_container_obj(fix_tree(v)), ""
    return "opaque:%r" % (v,), ""


# ------------------------------------------------------------------
# output decoding, print grain
# ------------------------------------------------------------------

INT_TYPES = {"int", "integer"}
FLOAT_TYPES = {"float", "double"}
BOOL_TYPES = {"bool", "boolean", "trueclass", "falseclass"}
NONE_TYPES = {"nonetype", "nilclass", "null"}
TEXT_TYPES = {"str", "string", "symbol"}


def canon_output_printed(tname, text):
    t = tname.lower()
    if t in NONE_TYPES:
        return "null", ""
    if t in BOOL_TYPES:
        low = text.strip().lower()
        if low in ("true", "1"):
            return "true", ""
        if low in ("false", "", "0"):
            return "false", ""
        return "opaque:%s" % text[:40], ""
    if t in INT_TYPES:
        try:
            return canon_from_fraction(Fraction(int(text)))
        except ValueError:
            pass
    if t in FLOAT_TYPES:
        # BINARY float/double (ruby Float, rust f32/f64 read through the
        # print grain, ...).  The printed text is a SHORTEST
        # ROUND-TRIPPING DECIMAL of a value stored in BINARY -- reading
        # those digits as an exact decimal fraction names a different
        # real number than the double itself (diagnosed log_057: the
        # max double doubled canons to a different mant depending on
        # which path is taken).  Go THROUGH the double: parse with
        # float(), then take THAT double's own exact binary value.  A
        # decimal-based type (BigDecimal, Rational, ...) does not have
        # this problem -- its printed text already IS its exact value --
        # so it keeps the direct decimal parse below.
        s = text.strip().strip("()")
        low = s.lower()
        if low in ("inf", "infinity", "+infinity"):
            return "inf", ""
        if low in ("-inf", "-infinity"):
            return "-inf", ""
        if low in ("nan", "-nan"):
            return "nan", ""
        if s in ("-0.0", "-0"):
            return "negzero", ""
        try:
            d = float(s)
        except ValueError:
            return "opaque:%s" % text[:40], ""
        if d != d:
            return "nan", ""
        if d == float("inf"):
            return "inf", ""
        if d == float("-inf"):
            return "-inf", ""
        if d == 0.0:
            return ("negzero" if struct.pack(">d", d)[0] & 0x80
                    else canon_from_fraction(Fraction(0))[0]), ""
        return canon_from_fraction(Fraction(d))
    if t in ("decimal", "bigdecimal", "rational", "fraction", "gmp", "num"):
        s = text.strip().strip("()")
        low = s.lower()
        if low in ("inf", "infinity", "+infinity"):
            return "inf", ""
        if low in ("-inf", "-infinity"):
            return "-inf", ""
        if low in ("nan", "-nan"):
            return "nan", ""
        if s in ("-0.0", "-0"):
            return "negzero", ""
        try:
            return canon_from_fraction(Fraction(s))
        except (ValueError, ZeroDivisionError):
            return "opaque:%s" % text[:40], ""
    if t in TEXT_TYPES:
        return canon_text(text), ""
    if t in ("list", "tuple", "dict", "array", "hash", "set",
             "frozenset"):
        return coords_str(container_coords(text)), ""
    try:
        return canon_from_fraction(Fraction(text.strip()))
    except (ValueError, ZeroDivisionError):
        return "opaque:%s:%s" % (tname[:20], text[:40]), ""


# ------------------------------------------------------------------
# filename escaping
# ------------------------------------------------------------------

CHAR_NAMES = {"+": "plus", "-": "minus", "*": "star", "/": "slash",
              "%": "percent", "<": "lt", ">": "gt", "=": "eq",
              "!": "bang", "&": "amp", "|": "pipe", "^": "caret",
              "~": "tilde", "?": "q", ".": "dot", "@": "at",
              ":": "colon", " ": "_"}


def op_filename(op):
    if all(c.isalpha() or c == " " for c in op):
        return op.replace(" ", "_")
    return "".join(CHAR_NAMES.get(c, c) if not c.isalnum() else c
                   for c in op)


# ------------------------------------------------------------------
# row assembly
# ------------------------------------------------------------------

def empty_row(pid, lang, lh, lf, lv, rh, rf, rv):
    lb, lc, le = held(lang, lh, lf, lv)
    rb, rc_, re_ = held(lang, rh, rf, rv)
    return {"probe_id": pid,
            "lhs_holder": lh, "lhs_value_class": lv, "lhs_bytes": lb,
            "lhs_canonical": lc, "lhs_canonical_exact": le,
            "rhs_holder": rh, "rhs_value_class": rv, "rhs_bytes": rb,
            "rhs_canonical": rc_, "rhs_canonical_exact": re_,
            "output_type": "", "output_literal": "",
            "output_canonical": "", "output_canonical_exact": "",
            "REFUSE": 0, "RAISE": 0, "ABORT": 0, "raise_kind": ""}


def rows_nine(lang):
    d = json.load(open(os.path.join(HERE, "answers_%s.json" % lang)))
    assert d.get("complete")
    per = {}
    for r in d["rows"]:
        la, rb = r["lhs"], r["rhs"]
        row = empty_row(r["id"], lang, la["holder"], la["form"],
                        la["value"], rb["holder"], rb["form"],
                        rb["value"])
        o = r["outcome"]
        if o == "answer":
            res = r["result"]
            enc = res["encoding"]
            full = enc + (":" + res["payload"] if res.get("payload", "")
                          != "" else "")
            row["output_type"] = res["type"]
            row["output_literal"] = (res.get("payload", "")
                                     if res.get("payload", "") != ""
                                     else enc)
            v = decode_enc(full)
            row["output_canonical"], row["output_canonical_exact"] = \
                canon_output_value(v, full)
        elif o == "raise":
            row["RAISE"] = 1
            row["raise_kind"] = r["raise"].strip()
        elif o == "death":
            row["ABORT"] = 1
        elif o == "codegen_refuse":
            row["REFUSE"] = 1
        else:
            continue
        per.setdefault(r["operation"], []).append(row)
    # compile-stage refusals from the acceptance artifact
    acc = json.load(open(os.path.join(HERE, ACCEPT_FILES[lang])))
    for key, cell in acc["cells"].items():
        if cell["verdict"] != "REFUSE":
            continue
        op = cell["operation"]
        lh, lf = cell["lhs"]["holder"], cell["lhs"]["form"]
        rh, rf = cell["rhs"]["holder"], cell["rhs"]["form"]
        row = empty_row("A:" + key, lang, lh, lf,
                        ACCEPT_CLASS.get(lf, ""), rh, rf,
                        ACCEPT_CLASS.get(rf, ""))
        row["REFUSE"] = 1
        per.setdefault(op, []).append(row)
    return per


def rows_three(lang):
    man = json.load(open(os.path.join(HERE, "manifest_%s.json" % lang)))
    beh = json.load(open(os.path.join(HERE,
                                      "behavior_%s_C.json" % lang)))
    assert beh.get("complete")
    holders = {h["i"]: h for h in man["holders"]}
    vnames = {h["i"]: sorted((vc[0] for vc in h["value_classes"]),
                             key=len, reverse=True)
              for h in man["holders"]}
    per = {}
    budget = 0
    for key, cell in beh["cells"].items():
        body = key[1:]
        i_s, rest = body.split("_", 1)
        j_s, rest = rest.split("_", 1)
        i, j = int(i_s), int(j_s)
        vx = vy = op = None
        for cand in vnames.get(i, []):
            if rest.startswith(cand + "_"):
                vx, rest2 = cand, rest[len(cand) + 1:]
                break
        if vx is None:
            continue
        for cand in vnames.get(j, []):
            if rest2.startswith(cand + "_"):
                vy, op = cand, rest2[len(cand) + 1:]
                break
        if vy is None:
            continue
        ha, hb = holders[i], holders[j]
        kind = cell[0]
        if kind == "BUDGET":
            budget += 1
            continue
        row = empty_row(key, lang, ha["holder"], ha["form"], vx,
                        hb["holder"], hb["form"], vy)
        if kind == "ANSWER":
            payload = cell[1]
            tname, _, text = payload.partition(":")
            row["output_type"] = tname
            row["output_literal"] = text
            row["output_canonical"], row["output_canonical_exact"] = \
                canon_output_printed(tname, text)
        elif kind == "RAISE":
            row["RAISE"] = 1
            row["raise_kind"] = str(cell[1]).strip()
        elif kind == "DEATH":
            row["ABORT"] = 1
        else:
            continue
        per.setdefault(op, []).append(row)
    if budget:
        print("  %s: %d BUDGET cells skipped (not an answer, not a "
              "refusal)" % (lang, budget))
    return per


# ------------------------------------------------------------------
# main
# ------------------------------------------------------------------

def main():
    print("per-operator matrices -- assembly over the layer-3 answers, "
          "no probe runs")
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    index = {}
    name_map = {}
    for lang in THREE + NINE:
        per = (rows_three if lang in THREE else rows_nine)(lang)
        for op, rows in sorted(per.items()):
            fn = "%s.%s.csv" % (lang, op_filename(op))
            name_map[fn] = "%s.%s" % (lang, op)
            path = os.path.join(OUT_DIR, fn)
            with open(path, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=COLUMNS)
                w.writeheader()
                for r in rows:
                    # a NUL byte cannot travel through csv; spell it.
                    w.writerow({k: (v.replace("\0", "\\x00")
                                    if isinstance(v, str) and "\0" in v
                                    else v) for k, v in r.items()})
            holders = {r["lhs_holder"] for r in rows} | \
                      {r["rhs_holder"] for r in rows}
            index["%s.%s" % (lang, op)] = dict(
                file=fn, rows=len(rows), holders=len(holders),
                value_rows=sum(1 for r in rows
                               if not (r["REFUSE"] or r["RAISE"]
                                       or r["ABORT"])),
                REFUSE=sum(r["REFUSE"] for r in rows),
                RAISE=sum(r["RAISE"] for r in rows),
                ABORT=sum(r["ABORT"] for r in rows))
        print("  %s: %d matrices (%.1f s)"
              % (lang, len(per), time.time() - t0))

    json.dump(dict(
        status="PER-OPERATOR MATRICES, ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        columns=COLUMNS, n_matrices=len(index),
        escaping="see README.md in this directory",
        matrices=index),
        open(os.path.join(OUT_DIR, "index.json"), "w"), indent=1)

    # README with the reverse filename mapping
    with open(os.path.join(OUT_DIR, "README.md"), "w") as f:
        f.write("# per-operator matrices\n\n")
        f.write("One CSV per `language.operator`; one PROBE per row; "
                "columns identical on every row of every matrix "
                "(see l3_per_op_matrices.py).\n\n")
        f.write("## filename escaping\n\n")
        f.write("A word-spelled operator that is entirely letters "
                "keeps its spelling with spaces as underscores. Any "
                "other operator is spelled character by character: "
                "%s.\n\n" % ", ".join(
                    "`%s` -> `%s`" % (k, v)
                    for k, v in sorted(CHAR_NAMES.items())))
        f.write("## reverse mapping (filename -> language.operator)\n\n")
        for fn, k in sorted(name_map.items()):
            f.write("- `%s` -> `%s`\n" % (fn, k))
    print("  %d matrices -> %s" % (len(index), OUT_DIR))

    if UNRESOLVED:
        print("  UNRESOLVED holder/value-class combinations: %d "
              "(inputs carry 'unresolved:'):" % len(UNRESOLVED))
        for k, n in sorted(UNRESOLVED.items())[:20]:
            print("    %s: %d rows" % (k, n))

    # ---------------------------------------------- sanity checks
    print("SANITY CHECKS")
    gop = index.get("go.+")
    print("  [1] go.+ rows: %d (value rows %d, REFUSE %d, RAISE %d, "
          "ABORT %d)" % (gop["rows"], gop["value_rows"], gop["REFUSE"],
                         gop["RAISE"], gop["ABORT"]))
    rows = list(csv.DictReader(open(os.path.join(OUT_DIR,
                                                 "go.plus.csv"))))
    hit = [r for r in rows if r["lhs_holder"] == "uint64"
           and {r["lhs_value_class"], r["rhs_value_class"]}
           == {"base_42", "i64max_plus1"}]
    for r in hit:
        print("  [2] go.+ uint64 %s+%s -> output %s canonical %s"
              % (r["lhs_value_class"], r["rhs_value_class"],
                 r["output_literal"], r["output_canonical"]))
    pyp = index.get("python.+")
    prow = list(csv.DictReader(open(os.path.join(OUT_DIR,
                                                 "python.plus.csv"))))
    pair = [r for r in prow
            if (r["lhs_value_class"], r["rhs_value_class"])
            == ("base_42", "i64max_plus1")]
    nr = sum(1 for r in pair if r["RAISE"] == "1")
    kinds = sorted({(r["lhs_holder"], r["rhs_holder"], r["raise_kind"])
                    for r in pair if r["RAISE"] == "1"})
    print("  [3] python.+ rows for the ordered pair "
          "base_42+i64max_plus1: %d (4 holders x 4), RAISE=1: %d %s"
          % (len(pair), nr, kinds))
    both = [r for r in prow
            if {r["lhs_value_class"], r["rhs_value_class"]}
            == {"base_42", "i64max_plus1"}]
    print("      both orderings: %d rows, RAISE=1: %d"
          % (len(both), sum(1 for r in both if r["RAISE"] == "1")))
    # verify against behavior_python_C.json directly
    beh = json.load(open(os.path.join(HERE, "behavior_python_C.json")))
    man = json.load(open(os.path.join(HERE, "manifest_python.json")))
    whole = [h["i"] for h in man["holders"] if h["form"] == "whole"]
    direct = 0
    draise = 0
    for i in whole:
        for j in whole:
            for va, vb in (("base_42", "i64max_plus1"),
                           ("i64max_plus1", "base_42")):
                c = beh["cells"].get("P%d_%d_%s_%s_+" % (i, j, va, vb))
                if c is not None:
                    direct += 1
                    if c[0] == "RAISE":
                        draise += 1
    print("      behavior_python_C.json direct count: %d cells, %d "
          "RAISE" % (direct, draise))
    # text canonical: the e-acute spellings present in the probe set
    spell = {r["lhs_bytes"] for r in prow
             if r["lhs_value_class"] == "eacute"}
    print("  [4] python.+ eacute lhs byte spellings in the probe set: "
          "%s (canonical %s)"
          % (sorted(spell),
             sorted({r["lhs_canonical"] for r in prow
                     if r["lhs_value_class"] == "eacute"})))
    # rectangularity
    bad = 0
    for fn in sorted(os.listdir(OUT_DIR)):
        if not fn.endswith(".csv"):
            continue
        ncols = {len(line) for line
                 in csv.reader(open(os.path.join(OUT_DIR, fn)))}
        if ncols != {len(COLUMNS)}:
            bad += 1
            print("  NOT RECTANGULAR: %s -> %s" % (fn, ncols))
    print("  [5] rectangularity: %d matrices, %d non-rectangular, "
          "column count %d everywhere else"
          % (len(index), bad, len(COLUMNS)))


if __name__ == "__main__":
    main()
