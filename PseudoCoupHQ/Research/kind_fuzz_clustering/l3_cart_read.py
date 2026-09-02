#!/usr/bin/env python3
"""l3_cart_read.py -- fold the CARTESIAN lanes into `matrices_cart/`.

One row per (level, operator, lhs holder, rhs holder).  The probe axis
lives INSIDE the row as one semicolon-separated `output_canon_vector`,
exactly as the interval matrices put the sample axis inside the row.

Columns, identical on every row of every file:

  probe_id, level, form_pair, lhs_holder, rhs_holder, x_set_a, x_set_b,
  n_probes, output_canon_vector, n_values, n_declines

WHY THE OPERANDS ARE NOT REPEATED IN EVERY ROW.  Under the settled
design the operands are the full Cartesian product of two documented
sets, so repeating them per row would write the same 10,000 spellings
into hundreds of rows.  Instead each row names its two operand sets
(`x_set_a`, `x_set_b`) and `index.json` carries every set in full -- the
spellings, the canonical strings and the enumeration order.  The mapping
from probe index to operands is fixed and total:

  level 1   p = i0 * |Xb| + i1                for op(x0, x1)
  level 2   p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3
                                              for op(op(x0,x1), op(x2,x3))

so any position is reconstructible exactly, and two rows compare
position by position IF AND ONLY IF their (x_set_a, x_set_b) pair
matches -- which is the whole point of both languages evaluating
identical expressions on identical inputs.

THE LEVEL-2 INTERMEDIATES ARE NEVER ENUMERATED, deduped, capped or
unioned.  Nothing in this file materialises `op(x0,x1)`; it exists only
inside the expression the lane evaluated.

ABSENCE.  A value a holder cannot represent is absent from that holder's
set, so a row over that holder is SHORTER and carries a different
`x_set` id.  Absences are counted per row family and reported; nothing
is padded and nothing is coerced.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import collections
import csv
import json
import os
import sys
import time

csv.field_size_limit(sys.maxsize)
# typescript's `bigint` and dart's `BigInt` emit their FULL magnitude as
# signed-magnitude hex (log_062 kept them because `decode_enc` already
# reads that token), and a `**` answer can carry thousands of digits.
# CPython 3.11+ caps int->str at 4,300 digits by default as a DoS guard;
# that cap is a property of the fold host, not of the canon, so it is
# lifted here rather than truncating a measured answer.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(2_000_000)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OUT_DIR = os.path.join(HERE, "matrices_cart")
LANE_OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                        "SandboxDesign", "agent", "out"))
RAW = os.path.join(HERE, "raw")
# additive, per log_060: the runs of record still live under
# SandboxDesign, and Airlock's own `agent/out` is searched as well so a
# lane run after the migration is found without moving anything.
AIRLOCK_OUT = os.environ.get(
    "AIRLOCK_OUT",
    os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                 "Airlock", "agent", "out")))

import l3_per_op_matrices as m                                # noqa: E402
import l3_per_op_matrices_v2 as v2                            # noqa: E402
import l3_interval_read as IR                                 # noqa: E402
import l3_cart_values as CV                                   # noqa: E402
import l3_cart_gen as G                                       # noqa: E402

COLUMNS = ["probe_id", "level", "form_pair", "lhs_holder", "rhs_holder",
           "x_set_a", "x_set_b", "n_probes", "output_canon_vector",
           "n_values", "n_declines"]
SEP = ";"

is_decline = IR.is_decline

# The canon conversion goes through Fraction/Decimal and is the single
# most expensive step in the fold -- and the SAME payload recurs millions
# of times across a Cartesian sweep.  Memoising it on the raw payload
# string is a pure speed change: the function is deterministic and has no
# state, so the answer cannot differ.
_CANON = {}


def canon_cached(fn, payload):
    k = (fn.__name__, payload)
    v = _CANON.get(k)
    if v is None:
        v = fn(payload)
        _CANON[k] = v
    return v


# ------------------------------------------------------------------
# oversized answers, canonicalised WITHOUT building the number
# ------------------------------------------------------------------
# `l3_interval_read._from_top` rebuilds an oversized ruby answer as an
# exact Fraction: sign * top * 2**(bits - top.bit_length()).  On the
# interval ladder the largest such answer was a few thousand bits and
# that was fine.  The Cartesian sweep reaches `**` results of 2^31 BITS,
# where materialising the integer costs ~28 s and gigabytes EACH -- so
# the fold would never finish.
#
# It never needed the integer.  The canon is `[sign, mant, expo]` with
# expo = floor(log2|x|) and mant = |x| / 2^expo in [1,2), and BOTH follow
# from the declared bit length and the leading bits alone:
#
#     expo = bits - 1
#     mant = top / 2^(top.bit_length() - 1)      -- a SMALL fraction
#
# so the shift never has to be performed.  `_canon_shifted` below is the
# same arithmetic `canon_num` does, with the power of two carried as an
# exponent instead of a multiplication.  `_selfcheck_bignum` proves the
# two agree on sizes where the slow path is still affordable.

_MANT_DIGITS = v2.MANT_DIGITS


def _canon_shifted(sign, a0, k):
    """canon of  sign * a0 * 2**k  for a SMALL positive Fraction a0."""
    import decimal as _d
    from fractions import Fraction as _F
    if a0 == 0:
        return "[1, 0.0, 0]"
    e0 = a0.numerator.bit_length() - a0.denominator.bit_length()
    if _F(2) ** e0 > a0:
        e0 -= 1
    mant = a0 / (_F(2) ** e0)
    d = _d.Decimal(mant.numerator) / _d.Decimal(mant.denominator)
    q = d.quantize(_d.Decimal(1).scaleb(-_MANT_DIGITS))
    s = format(q, "f").rstrip("0")
    if s.endswith("."):
        s += "0"
    return "[%d, %s, %d]" % (sign, s, e0 + k)


def _top_parts(bits, hexdigits):
    """(small positive Fraction, power-of-two shift) for a declared
    oversized magnitude."""
    from fractions import Fraction as _F
    top = int(hexdigits, 16)
    if top == 0:
        return _F(0), 0
    IR.TOPBITS_USED["n"] += 1
    return _F(top), bits - top.bit_length()


def fast_ruby_canon(payload):
    """`ruby_canon` with the oversized tokens taken by the shifted path.
    Everything else is handed to the original, unchanged."""
    from fractions import Fraction as _F
    tname, _, text = payload.partition(":")
    if tname == "BIGNUM":
        s, bits, hx = text.split(":", 2)
        a0, k = _top_parts(int(bits), hx)
        if a0 == 0:
            return "[1, 0.0, 0]"
        return _canon_shifted(int(s), a0, k)
    if tname == "BIGRAT":
        s, nb, nh, db, dh = text.split(":", 4)
        na, nk = _top_parts(int(nb), nh)
        da, dk = _top_parts(int(db), dh)
        if da == 0:
            return "opaque:BIGRAT-zero-denominator"
        if na == 0:
            return "[1, 0.0, 0]"
        return _canon_shifted(int(s), _F(na, 1) / _F(da, 1), nk - dk)
    return IR.ruby_canon(payload)


def _selfcheck_bignum():
    """the shifted path against the original, on magnitudes small enough
    that building the integer is still affordable."""
    for bits, hx, sign in ((5000, "1", 1), (5000, "ffff", -1),
                           (9000, "123456789abcdef", 1),
                           (4097, "3fffffffffffffff", -1)):
        a = fast_ruby_canon("BIGNUM:%d:%d:%s" % (sign, bits, hx))
        b = IR.ruby_canon("BIGNUM:%d:%d:%s" % (sign, bits, hx))
        assert a == b, (bits, hx, a, b)
    for t in ("BIGRAT:1:5000:ff:4200:3",
              "BIGRAT:-1:6000:abcdef:4100:1"):
        assert fast_ruby_canon(t) == IR.ruby_canon(t), t


_selfcheck_bignum()


# ------------------------------------------------------------------
# python: the payload grain -> canon  (log_061, 2026-08-22)
# ------------------------------------------------------------------
# THE FLOAT PATH, stated where it is taken.  python's driver never
# prints a binary float: a `float` answer arrives as
# `FLOAT:64:<hex of struct.pack(">d", r)>`, the same token rust and go
# emit from `f64::to_bits()` and `math.Float64bits`, and it is decoded
# by the same `decode_enc` / `canon_output_value` pair.  So python's
# binary floats reach the canon through the DOUBLE'S OWN BITS and the
# log_057 fault -- reading a shortest-round-tripping decimal as an exact
# decimal -- has no path into python's canon at all.
#
# Everything else in python's vocabulary is a token ruby's reader
# already understands, chosen so on purpose rather than by luck:
#
#   | payload            | branch it lands in            | exactness |
#   | Integer:<dec>      | INT_TYPES                     | exact     |
#   | Rational:<n>/<d>   | the decimal-ish family        | exact     |
#   | Decimal:<text>     | the decimal-ish family        | exact -- a
#   |                    |                               | decimal
#   |                    |                               | type's text
#   |                    |                               | IS its value |
#   | String:<text>      | TEXT_TYPES                    | exact     |
#   | bool:True/False    | BOOL_TYPES                    | exact     |
#   | NULL               | handled below                 | exact     |
#   | BIGNUM / BIGRAT    | the shifted path, as ruby     | leading
#   |                    |                               | 512 bits  |
#   | BIGDEC             | as ruby                       | leading
#   |                    |                               | 200 digits |

def fast_python_canon(payload):
    if payload.startswith("FLOAT:"):
        v = m.decode_enc(payload)
        c, _ = m.canon_output_value(v, payload)
        return v2.fix_special(c)
    if payload == "NULL":
        return "null"
    return fast_ruby_canon(payload)


# ------------------------------------------------------------------
# go: the bit-grain encodings -> canon  (log_061, 2026-08-22)
# ------------------------------------------------------------------
# go's lane emits `<probe id>|<reflect type name>|<encoding>` and RT_GO's
# `_enc` writes every scalar as BITS -- `INT:<w>:<hex>`,
# `UINT:<w>:<hex>`, `FLOAT:<w>:<hex>`, `BOOL:true|false`.  That is
# byte-for-byte the shape rust's runtime emits, so go's payloads are read
# by `IR.rust_canon` unchanged.  No printed float exists on go's side
# either, so the log_057 fault has no path into go's canon.
go_canon = IR.rust_canon


def find_lane(name):
    for d in (LANE_OUT, RAW, AIRLOCK_OUT):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


# ------------------------------------------------------------------
# lane output -> {probe id: canon-or-outcome-token}
# ------------------------------------------------------------------

def read_rust(name):
    p = find_lane(name)
    if p is None:
        raise SystemExit("lane output not found: %s" % name)
    out, summary, timing = {}, None, None
    for line in open(p):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            summary = line
            continue
        if line.startswith("__TIMING__"):
            timing = line
            continue
        pid, _, rest = line.partition("|")
        if not pid:
            continue
        if rest.startswith("-|RAISE:"):
            out[pid] = raise_tok(rest[len("-|RAISE:"):])
        elif rest.startswith("-|ABORT"):
            out[pid] = "ABORT"
        elif rest.startswith("-|BUILDFAIL"):
            out[pid] = "REFUSE"          # the compiler would not take it
        elif rest.startswith("-|MISSING"):
            out[pid] = "ABORT"           # the process never answered for it
        elif len(rest) > 10000:
            # an oversized BIGINT payload: canonise WITHOUT caching --
            # memoising on a multi-megabyte key would pin the raw hex in
            # memory for the whole fold
            out[pid] = fast_static_canon(rest)
        else:
            out[pid] = canon_cached(fast_static_canon, rest)
    return out, summary, timing, p


# ------------------------------------------------------------------
# oversized BIGINT answers in the RUST line shape (typescript `bigint`,
# dart `BigInt`) -- the SAME problem ruby's BIGNUM token solved, arriving
# through a different door.  typescript's level-2 lane carries `**`
# answers up to 2^30 BITS spelled as full signed-magnitude hex; building
# the integer and dividing Decimals at that size never finishes.  The
# canon needs only the leading bits and the declared width, so oversized
# magnitudes take `_canon_shifted` at ruby's own 512-leading-bits grain.
# `_selfcheck_static_bigint` proves the two paths agree where the exact
# path is still affordable.
_BIG_HEX = 2000                    # exact path below this many hex digits
STATIC_TOPBITS_USED = {"n": 0}


def fast_static_canon(payload):
    """`IR.rust_canon` with oversized BIGINT magnitudes taken by the
    shifted path.  Everything else is handed to the original, unchanged."""
    from fractions import Fraction as _F
    enc = payload.partition("|")[2]
    if enc.startswith("BIGINT:"):
        p = enc[7:]
        neg = p.startswith("-")
        p = p.lstrip("-")
        if len(p) > _BIG_HEX:
            STATIC_TOPBITS_USED["n"] += 1
            bits = (len(p) - 1) * 4 + int(p[0], 16).bit_length()
            top = int(p[:128], 16)           # leading 512 bits
            return _canon_shifted(-1 if neg else 1, _F(top),
                                  bits - top.bit_length())
    return IR.rust_canon(payload)


def _selfcheck_static_bigint():
    global _BIG_HEX
    vals = [(1 << 12007) - 12345, -(1 << 9001) + 7,
            10 ** 3000, -(10 ** 2500 + 999)]
    keep = _BIG_HEX
    for v in vals:
        hx = format(abs(v), "x")
        pay = "bigint|BIGINT:%s%s" % ("-" if v < 0 else "", hx)
        exact = IR.rust_canon(pay)
        _BIG_HEX = 10                        # force the shifted path
        fast = fast_static_canon(pay)
        _BIG_HEX = keep
        assert fast == exact, (len(hx), fast, exact)
    STATIC_TOPBITS_USED["n"] = 0


_selfcheck_static_bigint()


# RAISE tokens are few and recur millions of times; sharing one string
# object per kind is a pure memory change (log_064 fold, twelve languages
# on a smaller fold host), the same argument `_CANON` already records.
_RAISE = {}


def raise_tok(payload):
    t = _RAISE.get(payload)
    if t is None:
        t = _RAISE[payload] = "RAISE:" + v2.norm_kind(payload)
    return t


def read_rust_multi(names):
    """the rust line shape over SEVERAL files -- a sharded compiled
    family (`ct_cpp_l2_s*.txt`) or a route-C family that emits the rust
    shape with worker part files (php).  Later files overwrite earlier
    ones, so a combined file first and worker parts after it reads the
    same probes the daemon merged."""
    out, summaries, timings, paths = {}, [], [], []
    if not names:
        raise SystemExit("no lane output found for this family")
    for name in names:
        got = read_rust(name)
        out.update(got[0])
        if got[1]:
            summaries.append(got[1])
        if got[2]:
            timings.append(got[2])
        paths.append(got[3])
    return out, summaries, timings, paths


def _selfcheck_float_bits():
    """THE LOG_057 INSTRUMENT, kept pointed at the two new languages.

    log_057's lesson was not "fix ruby" but "keep the check that would
    have caught it".  python and go both emit binary floats as BITS, so
    the fault cannot arise -- and this proves that rather than asserting
    it, by recomputing each canon INDEPENDENTLY from the double the bits
    name and comparing by STRING at the canon's own 31-digit precision.
    A double-precision round-trip would be vacuous here for the same
    reason it was vacuous there: the buggy and the correct mantissa for
    -DBL_MAX parse back to the identical double.

    Fails loudly -- AssertionError at import -- never a warning."""
    import struct as _s
    import random as _r
    from fractions import Fraction as _F

    def expect(d):
        if d != d:
            return "nan"
        if d == float("inf"):
            return "[1, inf]"
        if d == float("-inf"):
            return "[-1, inf]"
        if d == 0.0:
            return ("[-1, 0.0, 0]" if _s.pack(">d", d)[0] & 0x80
                    else "[1, 0.0, 0]")
        return v2.canon_num(_F(d))

    pts = list(CV.X_FRAC) + [float("inf"), float("-inf"), 0.0, -0.0]
    rng = _r.Random(20260822)
    for _ in range(2000):
        b = rng.getrandbits(64)
        d = _s.unpack(">d", b.to_bytes(8, "big"))[0]
        if d == d:                       # nan compares unequal; skipped
            pts.append(d)
    for d in pts:
        hx = _s.pack(">d", d).hex()
        got_py = fast_python_canon("FLOAT:64:" + hx)
        got_go = go_canon("float64|FLOAT:64:" + hx)
        exp = expect(d)
        assert got_py == exp, ("python float bits canon", d, got_py, exp)
        assert got_go == exp, ("go float bits canon", d, got_go, exp)
    # binary32, the narrower holder both static languages carry
    for x in (1.5, -1.5, 1.0, -1.0, 0.0, -0.0, float(1 << 53)):
        f32 = _s.unpack(">f", _s.pack(">f", x))[0]
        hx = _s.pack(">f", x).hex()
        assert go_canon("float32|FLOAT:32:" + hx) == expect(f32), x
    # and the fault itself, stated as a fact rather than a memory: the
    # TEXT reading of -DBL_MAX's printed digits is NOT the double's canon
    assert (v2.canon_num(_F(repr(-1.7976931348623157e308)))
            != expect(-1.7976931348623157e308))


_selfcheck_float_bits()


def shard_lane_files(prefix, nshard):
    """every product of a SHARDED lane family: `<prefix>_s<k>.txt` and the
    per-worker part files beside it.  Kept separate from `lane_files` on
    purpose -- `lane_files` must keep matching only what it always
    matched, because `raw/` still holds `ct_ruby_l2_s*.txt` from an
    abandoned sharding attempt whose cell partition is NOT the one the
    run of record used, and widening the ruby glob would silently pull
    those back in."""
    out = []
    for k in range(nshard):
        pre = "%s_s%d" % (prefix, k)
        for d in (LANE_OUT, RAW, AIRLOCK_OUT):
            if not os.path.isdir(d):
                continue
            for fn in sorted(os.listdir(d)):
                if (fn == pre + ".txt" or fn.startswith(pre + ".w")) \
                        and fn.endswith(".txt"):
                    p = os.path.join(d, fn)
                    if p not in out:
                        out.append(p)
    return out


def read_python(names):
    """python's lane output.  Same line shape as ruby's -- `<pid>|<kind>|
    <payload>` -- read through python's own payload vocabulary."""
    out, summaries, timings, paths = {}, [], [], []
    if not names:
        raise SystemExit("no lane output found for this family")
    for name in names:
        p = name if os.path.isabs(name) else find_lane(name)
        if p is None:
            raise SystemExit("lane output not found: %s" % name)
        paths.append(p)
        for line in open(p):
            line = line.rstrip("\n")
            if line.startswith("__SUMMARY__"):
                summaries.append(line)
                continue
            if line.startswith("__TIMING__"):
                timings.append(line)
                continue
            parts = line.split("|", 2)
            if len(parts) < 3:
                continue
            pid, kind, payload = parts
            if kind == "ANSWER":
                out[pid] = canon_cached(fast_python_canon, payload)
            elif kind == "RAISE":
                out[pid] = raise_tok(payload)
            elif kind == "REFUSE":
                out[pid] = "REFUSE"
            elif kind == "ABORT":
                out[pid] = "ABORT"
            else:
                out[pid] = "ABORT"       # MISSING: never answered
    return out, summaries, timings, paths


def lane_files(prefix):
    """every lane product whose name starts with `prefix` -- the combined
    file a finished run writes AND the per-worker part files a worker
    writes as it goes.  Reading both means a run the daemon stopped at its
    ceiling still contributes everything it measured, and a probe that no
    file mentions stays visibly uncovered rather than quietly becoming an
    ABORT."""
    seen, out = set(), []
    for d in (LANE_OUT, RAW, AIRLOCK_OUT):
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if (fn == prefix + ".txt"
                    or fn.startswith(prefix + ".w")) and fn.endswith(".txt") \
                    and fn not in seen:
                seen.add(fn)
                out.append(os.path.join(d, fn))
    return out


def read_ruby(names):
    out, summaries, timings, paths = {}, [], [], []
    if not names:
        raise SystemExit("no lane output found for this family")
    for name in names:
        p = name if os.path.isabs(name) else find_lane(name)
        if p is None:
            raise SystemExit("lane output not found: %s" % name)
        paths.append(p)
        for line in open(p):
            line = line.rstrip("\n")
            if line.startswith("__SUMMARY__"):
                summaries.append(line)
                continue
            if line.startswith("__TIMING__"):
                timings.append(line)
                continue
            parts = line.split("|", 2)
            if len(parts) < 3:
                continue
            pid, kind, payload = parts
            if kind == "ANSWER":
                out[pid] = canon_cached(fast_ruby_canon, payload)
            elif kind == "RAISE":
                out[pid] = raise_tok(payload)
            elif kind == "REFUSE":
                out[pid] = "REFUSE"
            elif kind == "ABORT":
                out[pid] = "ABORT"
            else:
                out[pid] = "ABORT"       # MISSING: never answered
    return out, summaries, timings, paths


# ------------------------------------------------------------------
# lane families that are NOT languages
# ------------------------------------------------------------------
#
# log_067, 2026-08-23.  log_066 folded swift's `&+`/`&-`/`&*` under a
# language tag `swift_wrap`.  That tag is RETIRED: `&+` is Swift's own
# infix operator and Swift is the language, so a thirteenth language
# was invented that does not exist.  What log_066 wanted the tag to
# carry -- that the ACCEPTANCE set for those three operators is
# hand-DERIVED rather than measured by the census's swiftc -typecheck
# pass -- is recorded as an index FIELD (`acceptance`) on the operator
# entries instead.
#
# `SWIFT_WRAPOPS` is therefore a LANE FAMILY key, never a language: it
# selects an op list and a cell set, and every name that reaches disk
# (file name, index key, `used_by`, `language`) uses `out_lang()`.
SWIFT_WRAPOPS = "swift.wrapops"

# lane family -> the language tag written to disk
OUT_LANG = {SWIFT_WRAPOPS: "swift"}
# lane family -> the language whose holder table it borrows
BASE_LANG = {SWIFT_WRAPOPS: "swift", "rust_release": "rust"}
# lane families whose ACCEPT set was derived, not measured
DERIVED_ACCEPTANCE = {
    SWIFT_WRAPOPS: ("derived -- hand-derived same-type ACCEPT set "
                    "(FixedWidthInteger), not the census's swiftc "
                    "-typecheck measurement; log_066 section 1")}


def out_lang(lang):
    """the language tag that reaches disk for this lane family."""
    return OUT_LANG.get(lang, lang)


def base_lang(lang):
    """the language whose holder table this lane family borrows."""
    return BASE_LANG.get(lang, lang)


# ------------------------------------------------------------------
# the operand sets, recorded once and in full
# ------------------------------------------------------------------

def record_sets(lang, level, tab, sets):
    cvlang = "rust" if lang == "rust_release" else base_lang(lang)
    lang = out_lang(lang)
    for t in tab:
        sid = t["set_id"]
        if sid in sets:
            u = "%s.%s.L%d" % (lang, t["holder"], level)
            # one family can be folded by TWO lanes (swift's own six
            # operators and swift's wrap-ops lane) -- the same holder
            # must then be named once, not twice
            if u not in sets[sid]["used_by"]:
                sets[sid]["used_by"].append(u)
            continue
        keep, absent = CV.points(cvlang, t["form"], t["holder"], level)
        sets[sid] = dict(
            form=t["form"], level=level, n=len(keep),
            spellings=[s for s, _ in keep],
            canon=[CV.canon_point(cvlang, t["form"], t["holder"], v,
                                  v2.canon_num) for _, v in keep],
            absent_spellings=absent, n_absent=len(absent),
            used_by=["%s.%s.L%d" % (lang, t["holder"], level)])
    return sets


# ------------------------------------------------------------------
# row assembly
# ------------------------------------------------------------------

def build(lang, level, results):
    # `rust_release` is the SAME cells, holders and probe construction as
    # rust -- only the compile flags differ (log_057 Job B) -- so its rows
    # are built from rust's own table; the DISTINCT language tag lives in
    # the file name and index key, never merged with rust's.
    #
    # `swift.wrapops` is log_066's hand-added `&+`/`&-`/`&*` family: a
    # separate LANE (its own op list and cell set, `G.SWIFT_WRAP_OPS` /
    # `G.swift_wrap_cells_l1/l2`, because those three operators have no
    # entry in `acceptance_swift_A2.json` and no probe id issued by the
    # already-run `ct_swift_l1/l2.txt` lanes) over the SAME language.
    # It is NOT a language tag -- log_067 retired `swift_wrap`; the rows
    # land under `swift` and their derived acceptance is recorded as an
    # index field.
    base = base_lang(lang)
    tab = G.table(base, level)
    hold = {t["i"]: t for t in tab}
    if lang == SWIFT_WRAPOPS:
        op_list = G.SWIFT_WRAP_OPS
        cells = (G.swift_wrap_cells_l1() if level == 1
                 else G.swift_wrap_cells_l2()[0])
    else:
        op_list = G.ops(base)
        if base == "rust":
            cells = G.rust_cells_l1() if level == 1 else G.rust_cells_l2()[0]
        elif lang == "go":
            cells = G.go_cells_l1() if level == 1 else G.go_cells_l2()[0]
        elif lang == "python":
            cells = G.python_cells(level)
        elif lang == "php":
            cells = G.php_cells(level)
        elif lang in G.STATIC8:
            cells = (G.static_cells_l1(lang) if level == 1
                     else G.static_cells_l2(lang)[0])
        else:
            cells = G.ruby_cells(level)
    tag = "A" if level == 1 else "B"

    per = collections.OrderedDict()
    coverage = collections.Counter()
    absent_by_family = collections.Counter()
    absent_rows = collections.Counter()
    for (op, i, j) in cells:
        k = op_list.index(op)
        ha, hb = hold[i], hold[j]
        na, nb = ha["n"], hb["n"]
        n = na * nb if level == 1 else (na * nb) ** 2
        ovec = []
        for p in range(n):
            # pop, not get: each probe is read exactly once, and freeing
            # the entry as it is consumed keeps the largest family
            # (python level 2, 12.85M probes) inside a small fold host's
            # memory.  A duplicate line across worker part files was
            # already merged at read time, so nothing is lost.
            c = results.pop("%s%d_%d_%d_%d" % (tag, k, i, j, p), None)
            if c is None:
                # no lane file mentions this probe.  It is recorded as an
                # ABORT -- the honest reading, since nothing came back --
                # and COUNTED, so an incomplete run is visible.
                coverage["not_measured"] += 1
                c = "ABORT"
            else:
                coverage["measured"] += 1
            ovec.append(c)
        nd = sum(1 for c in ovec if is_decline(c))
        per.setdefault(op, []).append({
            "probe_id": "%s%d_%d_%d" % (tag, k, i, j),
            "level": level,
            "form_pair": "%s|%s" % (ha["form"], hb["form"]),
            "lhs_holder": ha["holder"], "rhs_holder": hb["holder"],
            "x_set_a": ha["set_id"], "x_set_b": hb["set_id"],
            "n_probes": n,
            "output_canon_vector": SEP.join(ovec),
            "n_values": n - nd, "n_declines": nd})
        fam = "%s.%s.L%d" % (out_lang(lang), ha["form"], level)
        if ha["absent"]:
            absent_by_family[fam] += len(ha["absent"])
            absent_rows[fam] += 1
        fam = "%s.%s.L%d" % (out_lang(lang), hb["form"], level)
        if hb["absent"]:
            absent_by_family[fam] += len(hb["absent"])
            absent_rows[fam] += 1
    return per, tab, absent_by_family, absent_rows, coverage


# ------------------------------------------------------------------
# format verification
# ------------------------------------------------------------------

def verify(d):
    print("FORMAT VERIFICATION -- %s" % os.path.basename(d))
    files = sorted(f for f in os.listdir(d) if f.endswith(".csv"))
    ncols_bad = veclen_bad = empty_slot = dirty = rows = probes = 0
    tokens = 0
    for fn in files:
        p = os.path.join(d, fn)
        for line in csv.reader(open(p)):
            if len(line) != len(COLUMNS):
                ncols_bad += 1
        for r in csv.DictReader(open(p)):
            rows += 1
            n = int(r["n_probes"])
            probes += n
            v = r["output_canon_vector"].split(SEP)
            if len(v) != n:
                veclen_bad += 1
            for cell in v:
                if cell == "":
                    empty_slot += 1
                    continue
                if cell.startswith("[") and ("/" in cell or "~" in cell):
                    dirty += 1
                if cell in ("negzero", "inf", "-inf"):
                    dirty += 1
                if "−" in cell:                # unicode minus
                    dirty += 1
                if is_decline(cell):
                    tokens += 1
    print("  files                        %d" % len(files))
    print("  rows                         %d" % rows)
    print("  probes inside those rows     %d" % probes)
    print("  non-rectangular lines        %d  (column count %d elsewhere)"
          % (ncols_bad, len(COLUMNS)))
    print("  rows with a wrong vector len %d" % veclen_bad)
    print("  empty vector slots           %d  (padding NOTHING)" % empty_slot)
    print("  dirty canon cells            %d" % dirty)
    print("  outcome tokens in vectors    %d  (REFUSE / RAISE:* / ABORT)"
          % tokens)
    return dict(files=len(files), rows=rows, probes=probes,
                non_rectangular=ncols_bad, wrong_vector_len=veclen_bad,
                empty_slots=empty_slot, dirty_cells=dirty,
                outcome_tokens=tokens)


# ------------------------------------------------------------------

def main():
    print("CARTESIAN matrices -- fold the lane probes into ONE row per "
          "(level, operator, lhs holder, rhs holder)")
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    index, sets, lane_timing = {}, {}, {}
    absent_report, absent_rows_report, coverage_report = {}, {}, {}

    plan = [("rust", 1, lambda: read_rust("ct_rust_l1.txt")),
            ("rust", 2, lambda: read_rust("ct_rust_l2.txt")),
            ("ruby", 1, lambda: read_ruby(["ct_ruby_l1.txt"])),
            ("ruby", 2, lambda: read_ruby(lane_files("ct_ruby_l2"))),
            # log_061, 2026-08-22.  go reads through the SAME bit-grain
            # reader rust uses -- `read_rust` is named for the shape it
            # reads, not for one language.
            ("go", 1, lambda: read_rust("ct_go_l1.txt")),
            ("go", 2, lambda: read_rust("ct_go_l2.txt")),
            ("python", 1, lambda: read_python(lane_files("ct_python_l1"))),
            ("python", 2,
             lambda: read_python(lane_files("ct_python_l2")
                                 + shard_lane_files("ct_python_l2",
                                                    G.PYTHON_L2_SHARDS))),
            # log_064, 2026-08-23: the remaining eight (log_062/063 lanes)
            # plus rust_release (log_057 Job B).  EVERY one of the eight
            # emits the RUST line shape, so they read through `read_rust`
            # with no new payload branch; php's worker part files ride in
            # through `read_rust_multi` exactly as ruby's do through
            # `read_ruby`.
            ("rust_release", 1,
             lambda: read_rust("ct_rust_release_l1.txt")),
            ("rust_release", 2,
             lambda: read_rust("ct_rust_release_l2.txt")),
            ("php", 1, lambda: read_rust_multi(lane_files("ct_php_l1"))),
            ("php", 2, lambda: read_rust_multi(lane_files("ct_php_l2"))),
            ("typescript", 1, lambda: read_rust("ct_typescript_l1.txt")),
            ("typescript", 2, lambda: read_rust("ct_typescript_l2.txt")),
            ("java", 1, lambda: read_rust("ct_java_l1.txt")),
            ("java", 2, lambda: read_rust("ct_java_l2.txt")),
            ("kotlin", 1, lambda: read_rust("ct_kotlin_l1.txt")),
            ("kotlin", 2,
             lambda: read_rust_multi(shard_lane_files("ct_kotlin_l2", 2))),
            ("cpp", 1, lambda: read_rust("ct_cpp_l1.txt")),
            ("cpp", 2,
             lambda: read_rust_multi(shard_lane_files("ct_cpp_l2", 2))),
            ("swift", 1, lambda: read_rust("ct_swift_l1.txt")),
            ("swift", 2, lambda: read_rust("ct_swift_l2.txt")),
            # log_066, 2026-08-23: the hand-added `&+`/`&-`/`&*` family
            # (log_065's diagnosed operator-spelling gap).  A separate
            # LANE FAMILY over the SAME language -- log_067 retired the
            # `swift_wrap` language tag; these rows land under `swift`
            # and carry `acceptance: derived` in the index instead.
            (SWIFT_WRAPOPS, 1, lambda: read_rust("ct_swift_wrap_l1.txt")),
            (SWIFT_WRAPOPS, 2, lambda: read_rust("ct_swift_wrap_l2.txt")),
            ("dart", 1, lambda: read_rust("ct_dart_l1.txt")),
            ("dart", 2, lambda: read_rust("ct_dart_l2.txt")),
            ("csharp", 1, lambda: read_rust("ct_csharp_l1.txt")),
            ("csharp", 2, lambda: read_rust("ct_csharp_l2.txt"))]

    # `--only=lang1,lang2` folds a subset of families, one process per
    # family if wanted -- the twelve-language fold is larger than one
    # process on a small host should hold at once.  It REQUIRES
    # `--merge`: a subset fold must never write an index that names only
    # itself, or a partial build could be mistaken for a complete one.
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = set(a[len("--only="):].split(","))
    merge = "--merge" in sys.argv
    if only is not None:
        if not merge:
            raise SystemExit("--only requires --merge")
        # an entry is either a language ("php") or one family of it
        # ("python.L2"), so the largest family can run in its own process
        plan = [e for e in plan
                if e[0] in only or "%s.L%d" % (e[0], e[1]) in only]

    # `--skip-missing` is a DRY-RUN switch for shaking the pipeline out
    # before every lane has landed.  It never runs silently: the skipped
    # family is named on stdout and recorded in index.json, so a partial
    # build can never be mistaken for a complete one.
    skip_missing = "--skip-missing" in sys.argv
    skipped_families = []

    for lang, level, reader in plan:
        try:
            got = reader()
        except SystemExit as exc:
            if not skip_missing:
                raise
            print("  !! SKIPPING %s level %d -- %s" % (lang, level, exc))
            skipped_families.append("%s.L%d" % (lang, level))
            continue
        results = got[0]
        print("  %s level %d: %d probe results" % (lang, level, len(results)))
        for s in (got[1] if isinstance(got[1], list) else [got[1]]):
            if s:
                print("      lane summary: %s" % s)
        tl = got[2] if isinstance(got[2], list) else [got[2]]
        lane_timing["%s.L%d" % (lang, level)] = [x for x in tl if x]
        for x in tl:
            if x:
                print("      lane timing:  %s" % x)

        per, tab, absent, absent_rows, cov = build(lang, level, results)
        coverage_report["%s.L%d" % (lang, level)] = dict(cov)
        if cov["not_measured"]:
            print("      !! %d of %d probes were NOT MEASURED by any lane "
                  "file and are recorded ABORT"
                  % (cov["not_measured"], cov["measured"] + cov["not_measured"]))
        else:
            print("      coverage: all %d probes measured" % cov["measured"])
        record_sets(lang, level, tab, sets)
        absent_report["%s.L%d" % (lang, level)] = dict(absent)
        absent_rows_report["%s.L%d" % (lang, level)] = dict(absent_rows)
        nrow = npro = 0
        for op, rws in per.items():
            fn = "%s.%s.L%d.csv" % (out_lang(lang), m.op_filename(op), level)
            with open(os.path.join(OUT_DIR, fn), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=COLUMNS)
                w.writeheader()
                for r in rws:
                    w.writerow(r)
            nrow += len(rws)
            npro += sum(r["n_probes"] for r in rws)
            entry = dict(
                file=fn, language=out_lang(lang), operator=op, level=level,
                rows=len(rws), probes=sum(r["n_probes"] for r in rws),
                holders=sorted({r["lhs_holder"] for r in rws}
                               | {r["rhs_holder"] for r in rws}),
                x_sets=sorted({r["x_set_a"] for r in rws}
                              | {r["x_set_b"] for r in rws}),
                n_values=sum(r["n_values"] for r in rws),
                n_declines=sum(r["n_declines"] for r in rws))
            # log_067: provenance of the ACCEPT set is a FIELD, never a
            # language tag -- the lane family says which entry gets it
            if lang in DERIVED_ACCEPTANCE:
                entry["acceptance"] = DERIVED_ACCEPTANCE[lang]
            index["%s.%s.L%d" % (out_lang(lang), op, level)] = entry
        print("      %d operator matrices, %d rows, %d probes (%.1f s)"
              % (len(per), nrow, npro, time.time() - t0))

    # `--no-verify` exists for CHUNKED subset folds on a wall-clock-capped
    # host: the intermediate merges skip the whole-directory format pass
    # and the LAST run (or a standalone `verify(OUT_DIR)`) performs it
    # over everything.  index.json records when the pass was skipped, so
    # a never-verified generation cannot pass silently.
    if "--no-verify" in sys.argv:
        stats = dict(skipped="format verification deferred by --no-verify; "
                             "run verify(OUT_DIR) over the finished "
                             "directory")
    else:
        stats = verify(OUT_DIR)
    print("VALUES ABSENT BECAUSE A HOLDER CANNOT REPRESENT THEM")
    for fam in sorted(absent_report):
        if not absent_report[fam]:
            print("  %-12s none" % fam)
            continue
        for k in sorted(absent_report[fam]):
            print("  %-14s %5d absences over %d row sides"
                  % (k, absent_report[fam][k],
                     absent_rows_report[fam].get(k, 0)))

    if merge:
        # fold INTO an existing generation: everything already recorded
        # for a family this run did not touch is kept verbatim, and the
        # new families are added beside it.  Used-by lists on a shared
        # x_set union rather than overwrite.
        old = json.load(open(os.path.join(OUT_DIR, "index.json")))
        for sid, v in sets.items():
            if sid in old["x_sets"]:
                ub = old["x_sets"][sid]["used_by"]
                for u in v["used_by"]:
                    if u not in ub:
                        ub.append(u)
            else:
                old["x_sets"][sid] = v
        sets = old["x_sets"]
        for fld, new in (("lane_timing", lane_timing),
                         ("absent_values_per_row_family", absent_report),
                         ("absent_row_sides_per_row_family",
                          absent_rows_report),
                         ("probe_coverage", coverage_report),
                         ("matrices", index)):
            merged = dict(old.get(fld, {}))
            merged.update(new)
            if fld == "lane_timing":
                lane_timing = merged
            elif fld == "absent_values_per_row_family":
                absent_report = merged
            elif fld == "absent_row_sides_per_row_family":
                absent_rows_report = merged
            elif fld == "probe_coverage":
                coverage_report = merged
            else:
                index = merged

    json.dump(dict(
        status="CARTESIAN MATRICES -- the settled probe design of "
               "2026-08-21.  LEVEL 1 y = op(x0,x1) over ALL ordered pairs "
               "of a shared set X; LEVEL 2 z = op(op(x0,x1), op(x2,x3)) "
               "over a subset X'.  The level-2 intermediates are never "
               "enumerated, deduped, capped or unioned -- they exist "
               "inside the expression.",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope="twelve languages, both levels (log_064, 2026-08-23): "
              "rust (debug) + rust_release + go + the seven STATIC8 "
              "compiled families (typescript, java, kotlin, cpp, swift, "
              "dart, csharp), and ruby + python + php (route C, worker "
              "processes).  Extended from rust+ruby (log_052) via "
              "log_057 (rust_release lanes), log_061 (python, go) and "
              "log_062/063 (the remaining eight).",
        float_path_per_language=dict(
            rust="BITS -- `f64::to_bits()` / `f32::to_bits()` as "
                 "`FLOAT:<w>:<hex>`",
            go="BITS -- `math.Float64bits` / `math.Float32bits` as "
               "`FLOAT:<w>:<hex>`",
            python="BITS -- `struct.pack('>d', r).hex()` as "
                   "`FLOAT:64:<hex>`; `Decimal` and `Fraction` keep the "
                   "printed grain, where the text already IS the exact "
                   "value",
            ruby="TEXT -- `Float#inspect`, converted by the READER "
                 "through the double (`Fraction(float(text))`), the "
                 "log_057 fix",
            rust_release="BITS -- identical instrument to rust, only "
                         "the compile flags differ (log_057 Job B)",
            php="BITS -- `bin2hex(pack('E', $v))` as `FLOAT:64:<hex>` "
                "(log_062)",
            typescript="BITS -- `DataView.setFloat64` (log_062)",
            java="BITS -- `Double.doubleToRawLongBits` / "
                 "`Float.floatToRawIntBits` (log_062)",
            kotlin="BITS -- the same two JDK calls (log_062)",
            cpp="BITS -- `memcpy` of the object bytes (log_062)",
            swift="BITS -- `Double.bitPattern` / `Float.bitPattern` "
                  "(log_062)",
            dart="BITS -- `ByteData.setFloat64` (log_062)",
            csharp="BITS -- `BitConverter.GetBytes(double)` (log_062)"),
        columns=COLUMNS, vector_separator=SEP,
        probe_index_rule=dict(
            level1="p = i0 * |Xb| + i1",
            level2="p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3"),
        comparability="two rows compare position by position if and only "
                      "if their (x_set_a, x_set_b) pair matches; both "
                      "languages evaluate identical expressions on "
                      "identical inputs, so there is no alignment step",
        absence_rule="a value a holder cannot represent is ABSENT from "
                     "that holder's set -- the row is shorter and carries "
                     "a different x_set id.  Nothing is coerced, wrapped "
                     "or rounded.",
        ruby_operator_menu_extension=G.EXTRA_RUBY_OPS,
        ruby_stall_budget_s=G.RUBY_STALL_S,
        ruby_stall_budget_note="RECORDED CHANGE 2026-08-21: 2 s, was 10 s. "
                               "The previous run spent 550 s of 557 s "
                               "waiting on `**` with BigDecimal.  A stall "
                               "is recorded as ABORT and an ABORT is "
                               "excluded from scoring in the numerator and "
                               "the denominator both, so the shorter "
                               "budget loses no measurement -- only wall "
                               "clock.",
        x_sets=sets,
        lane_timing=lane_timing,
        absent_values_per_row_family=absent_report,
        absent_row_sides_per_row_family=absent_rows_report,
        oversized_ruby_cells_reconstructed_from_leading_bits=(
            IR.TOPBITS_USED["n"]),
        oversized_static_bigints_reconstructed_from_leading_bits=(
            STATIC_TOPBITS_USED["n"]),
        verification=stats,
        incomplete_families_skipped=skipped_families,
        probe_coverage=coverage_report,
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        matrices=index),
        open(os.path.join(OUT_DIR, "index.json"), "w"), indent=1)

    with open(os.path.join(OUT_DIR, "README.md"), "w") as f:
        f.write("# cartesian matrices\n\nThe settled probe design of "
                "2026-08-21.\n\n"
                "- **level 1** `y = op(x0, x1)` for ALL ordered pairs from "
                "a shared set `X`.\n"
                "- **level 2** `z = op(op(x0,x1), op(x2,x3))` with all four "
                "operands from a subset `X'`.  The two intermediates are "
                "never enumerated, deduped, capped or unioned -- they "
                "exist inside the expression.\n\n"
                "One CSV per `language.operator.L<level>`.  One row per "
                "(level, operator, lhs holder, rhs holder); the probe axis "
                "lives inside the row as `output_canon_vector`.  Operand "
                "sets are named by `x_set_a` / `x_set_b` and recorded in "
                "full in `index.json`, with the probe-index rule, so every "
                "position is reconstructible exactly.\n\n"
                "A value a holder cannot represent is ABSENT from that "
                "holder's set -- never coerced.  A slot with no value "
                "carries `REFUSE`, `RAISE:<kind>` or `ABORT`; nothing is "
                "padded and no slot is ever empty.\n")
    print("  wrote %s (%d matrices, %.1f s)"
          % (OUT_DIR, len(index), time.time() - t0))


if __name__ == "__main__":
    main()
