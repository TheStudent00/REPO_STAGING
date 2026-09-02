#!/usr/bin/env python3
"""l3_interval_values.py -- the INTERVAL SAMPLING LADDER.

the owner's design, settled 2026-08-20/21: today's value classes are EDGE
values only (6 per form), which lets coincidental matches happen.  The
extension adds INTERVAL sampling -- N samples per side spanning each
holder's OWN representable range -- IN ADDITION to the edge classes,
never replacing them.  Pilot: N = 32 per side, NUMERIC forms only
(whole, fractional).  Text and containers keep their edge sets
untouched; intervals are meaningless there.

The ladder is DETERMINISTIC and CLOSED-FORM -- no random draw, no
seed, no per-run variation.  Every magnitude is an exact integer
root of a power of two, computed with integer arithmetic, so a re-run
on any machine reproduces the same 32 values bit for bit.

-------------------------------------------------------------------
WHOLE ladder, 32 samples
-------------------------------------------------------------------
signed bounded, width W bits (range -2^(W-1) .. 2^(W-1)-1):
  6 near-boundary anchors  [min, min+1, -1, 0, 1, max]
  13 log-spaced magnitudes m_k = floor( 2 ^ (k*(W-1)/14) ), k=1..13
     (computed as the exact integer 14th root of 2^(k*(W-1)))
  the same 13 magnitudes NEGATED  -- both signs, the holder is signed
  total 6 + 13 + 13 = 32

unsigned bounded, width W bits (range 0 .. 2^W-1):
  4 near-boundary anchors  [0, 1, max-1, max]
  28 log-spaced magnitudes m_k = floor( 2 ^ (k*W/29) ), k=1..28
     (exact integer 29th root of 2^(k*W))
  total 4 + 28 = 32     -- one sign only, the holder is unsigned

unbounded whole holders (ruby Integer / Rational / BigDecimal) have no
representable bound, so the ladder uses a NOMINAL magnitude window of
128 bits and the signed rule.  That window is a recorded choice, not a
measurement: it matches the widest bounded whole holder in the pilot
(rust i128) so the two languages' ladders overlap where they can.

-------------------------------------------------------------------
FRACTIONAL ladder, 32 samples
-------------------------------------------------------------------
binary floating holder with normal exponent range [emin, emax]:
  10 anchors:  +0.0, -0.0, +minsubnormal, -minsubnormal, minnormal,
               1.0, nextafter(1,2), nextafter(1,0), +maxfinite,
               -maxfinite
  11 log-spaced magnitudes  1.5 * 2^e_k,
               e_k = emin + round(k*(emax-emin)/12), k=1..11
  the same 11 magnitudes NEGATED
  total 10 + 11 + 11 = 32

The interval ladder carries FINITE values only.  inf and nan stay in
the edge classes, where they already are -- an interval that spans a
range has no business inventing points outside it.

Every sample is inside its own holder's range by construction, so the
acceptance verdicts measured on the edge values still hold and no
acceptance run is repeated.

Canonical forms are the v2 rulings unchanged: numeric
`[sign, mant, expo]`, zero `[1, 0.0, 0]` / `[-1, 0.0, 0]`, ascii minus,
no fractions and no `~` in any visible cell.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import decimal
import math
import struct
from fractions import Fraction

N_SAMPLES = 32
UNBOUNDED_NOMINAL_BITS = 128      # recorded choice, see the docstring


# ------------------------------------------------------------------
# exact integer n-th root -- no float pow anywhere in the ladder
# ------------------------------------------------------------------

def iroot(x, n):
    """floor(x ** (1/n)) for x >= 0, exact integer arithmetic."""
    if x < 0:
        raise ValueError("iroot of a negative")
    if x == 0:
        return 0
    hi = 1 << ((x.bit_length() + n - 1) // n + 1)
    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** n <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def pow2_root(num, den):
    """floor( 2 ** (num/den) ), exact."""
    return iroot(1 << num, den)


# ------------------------------------------------------------------
# the ladders
# ------------------------------------------------------------------

def whole_ladder(signed, bits):
    """32 exact integers spanning the holder's whole-number range."""
    if signed:
        lo, hi = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
        anchors = [lo, lo + 1, -1, 0, 1, hi]
        mags = [pow2_root(k * (bits - 1), 14) for k in range(1, 14)]
        out = anchors + mags + [-m for m in mags]
    else:
        hi = (1 << bits) - 1
        anchors = [0, 1, hi - 1, hi]
        mags = [pow2_root(k * bits, 29) for k in range(1, 29)]
        out = anchors + mags
    assert len(out) == N_SAMPLES, len(out)
    assert len(set(out)) == N_SAMPLES, "ladder collided at %d bits" % bits
    return out


def _as_f32(x):
    return struct.unpack(">f", struct.pack(">f", x))[0]


def frac_ladder(bits):
    """32 FINITE doubles (f32 ladder pre-rounded to f32) spanning the
    holder's exponent range."""
    if bits == 64:
        emin, emax = -1022, 1023
        minsub = 5e-324
        maxfin = 1.7976931348623157e308
        near_up = math.nextafter(1.0, 2.0)
        near_dn = math.nextafter(1.0, 0.0)
        rnd = float
    else:
        emin, emax = -126, 127
        minsub = _as_f32(2.0 ** -149)
        maxfin = _as_f32(3.4028234663852886e38)
        near_up = _as_f32(1.0 + 2.0 ** -23)
        near_dn = _as_f32(1.0 - 2.0 ** -24)
        rnd = _as_f32
    minnorm = rnd(2.0 ** emin)
    anchors = [0.0, -0.0, minsub, -minsub, minnorm,
               1.0, near_up, near_dn, maxfin, -maxfin]
    span = emax - emin
    es = [emin + int(round(k * span / 12.0)) for k in range(1, 12)]
    mags = [rnd(math.ldexp(1.5, e)) for e in es]
    out = anchors + mags + [-m for m in mags]
    assert len(out) == N_SAMPLES, len(out)
    # +0.0 and -0.0 compare equal but are DISTINCT samples; check the
    # rest for collisions with their bit patterns
    keys = [struct.pack(">d", v).hex() for v in out]
    assert len(set(keys)) == N_SAMPLES, "fractional ladder collided"
    return out


# ------------------------------------------------------------------
# the pilot's numeric holders -> (ladder id, ladder, read-rule)
#   read-rule spellings follow l3_per_op_matrices.REP_RULES
# ------------------------------------------------------------------

LADDER_ID = {}


def _reg(lid, ladder):
    LADDER_ID[lid] = ladder
    return lid


W_S32 = _reg("w_s32", whole_ladder(True, 32))
W_S64 = _reg("w_s64", whole_ladder(True, 64))
W_U64 = _reg("w_u64", whole_ladder(False, 64))
W_S128 = _reg("w_s128", whole_ladder(True, 128))
W_BIG = _reg("w_big128", whole_ladder(True, UNBOUNDED_NOMINAL_BITS))
F_B64 = _reg("f_b64", frac_ladder(64))
F_B32 = _reg("f_b32", frac_ladder(32))


# (language, form, holder) -> (ladder id, read rule)
NUMERIC_HOLDERS = {
    ("rust", "whole", "i32"): (W_S32, ("s", 32)),
    ("rust", "whole", "i64"): (W_S64, ("s", 64)),
    ("rust", "whole", "u64"): (W_U64, ("u", 64)),
    ("rust", "whole", "i128"): (W_S128, ("s", 128)),
    ("rust", "fractional", "f64"): (F_B64, ("f64",)),
    ("rust", "fractional", "f32"): (F_B32, ("f32",)),

    ("ruby", "whole", "Integer"): (W_BIG, ("big",)),
    ("ruby", "whole", "Rational"): (W_BIG, ("big",)),
    ("ruby", "whole", "BigDecimal"): (W_BIG, ("dec",)),
    ("ruby", "fractional", "Float"): (F_B64, ("f64",)),
    ("ruby", "fractional", "Rational"): (F_B64, ("binfrac",)),
    ("ruby", "fractional", "BigDecimal"): (F_B64, ("dec",)),
}


def samples_for(lang, form, holder):
    lid, rule = NUMERIC_HOLDERS[(lang, form, holder)]
    return lid, rule, LADDER_ID[lid]


# ------------------------------------------------------------------
# declaration text -- the SAME shapes the layer-2 tables already use,
# with the ladder value substituted for the value class spelling
# ------------------------------------------------------------------

def _rs_int_lit(ty, v, ladder):
    if v == ladder[0] and v < 0:
        return "%s::MIN" % ty          # avoid the overflowing-literal lint
    if v == max(ladder):
        return "%s::MAX" % ty
    return str(v)


def _f_lit(x):
    """python repr round-trips and is a legal float literal in both
    rust and ruby (`5e-324`, `1.7976931348623157e+308`, `-0.0`)."""
    return repr(x)


def decl(lang, form, holder, name, v, ladder):
    if lang == "rust":
        if form == "whole":
            return "let %s: %s = %s;" % (name, holder,
                                         _rs_int_lit(holder, v, ladder))
        return "let %s: %s = %s;" % (name, holder, _f_lit(v))
    # ruby
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
# canonical form of a SAMPLE, under the holder's read-rule
# ------------------------------------------------------------------

def _signbit(x):
    return struct.pack(">d", x)[0] & 0x80


def canon_sample(rule, v, canon_num):
    """canon_num is l3_per_op_matrices_v2.canon_num (v2 rulings)."""
    if isinstance(v, int):
        # every whole sample is inside its own holder's range by
        # construction, so no rep read-rule wrap can fire
        return canon_num(Fraction(v))
    if v == 0.0:
        return "[-1, 0.0, 0]" if _signbit(v) else "[1, 0.0, 0]"
    if rule[0] == "dec":
        return canon_num(Fraction(decimal.Decimal(repr(v))))
    return canon_num(Fraction(v))
