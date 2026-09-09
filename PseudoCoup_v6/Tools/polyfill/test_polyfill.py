"""Acceptance for T4 polyfill (this tool's oracle).

Two halves, per the plan node's settled acceptance criterion
("differential -- wrapped arithmetic vs native source-language execution
on a pinned grid, the PCv5 pattern that caught the urem guard bug within
minutes"):

  1. A differential grid: every wrapper type x every operator, checked
     against an oracle re-derived HERE from Python's arbitrary-precision
     ints plus explicit `%`-mask / sign-extend -- never by importing and
     reusing wrap_fixed_width's own `_wrap`/`_trunc_div` helpers as the
     expectation (that would just be testing the implementation against
     itself).
  2. check_uniformity flags a deliberately non-uniform sample (modeled on
     a harvested transpile's real `encode_modrm`, with one nested wrap
     removed) and passes the uniform original.

Run:
    python3 -m pytest ~/Programming/PseudoCoup_v6/Tools/polyfill -q
"""
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_uniformity as cu  # noqa: E402
import wrap_fixed_width as w  # noqa: E402

TYPES = w.TYPES  # {"u8": U8, "u16": U16, ..., "i64": I64}


# ---------------------------------------------------------------------------
# Independent oracle -- arbitrary-precision math + explicit mask/sign-extend,
# written from scratch here (uses `%`, not the implementation's `&` masking
# trick) so it is not merely re-running wrap_fixed_width's own code.
# ---------------------------------------------------------------------------

def oracle_wrap(value: int, bits: int, signed: bool) -> int:
    v = value % (1 << bits)                 # Python's % is always non-negative here
    if signed and v >= (1 << (bits - 1)):
        v -= (1 << bits)
    return v


def oracle_trunc_div(a: int, b: int) -> int:
    q, _ = divmod(abs(a), abs(b))
    return -q if (a < 0) != (b < 0) else q


def oracle_trunc_mod(a: int, b: int) -> int:
    return a - oracle_trunc_div(a, b) * b


def bounds(bits: int, signed: bool):
    lo = -(1 << (bits - 1)) if signed else 0
    hi = (1 << (bits - 1)) - 1 if signed else (1 << bits) - 1
    return lo, hi


def sample_values(bits: int, signed: bool):
    """Required edge cases (type max/min, -1, 0) plus a handful of
    interesting bit patterns (sign-bit-only, all-ones, alternating), kept
    small so the O(n^2) binary-operator grid stays fast across 8 types."""
    lo, hi = bounds(bits, signed)
    vals = {0, 1, -1, lo, hi, lo + 1, hi - 1, 2, 3, 5, 7,
            1 << (bits - 1), (1 << bits) - 1}
    if bits >= 8:
        vals.add(0x55)
        vals.add(0xAA)
    return sorted(v for v in vals if lo <= v <= hi)


ALL_TYPES = sorted(TYPES.items())


# ---------------------------------------------------------------------------
# 1a. Arithmetic: +, -, * wrap silently (two's-complement, mod 2**bits).
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,cls", ALL_TYPES)
def test_arithmetic_wraps_against_oracle(name, cls):
    bits, signed = cls.BITS, cls.SIGNED
    vals = sample_values(bits, signed)
    for a in vals:
        for b in vals:
            assert (cls(a) + cls(b)).value == oracle_wrap(a + b, bits, signed), \
                (name, "add", a, b)
            assert (cls(a) - cls(b)).value == oracle_wrap(a - b, bits, signed), \
                (name, "sub", a, b)
            assert (cls(a) * cls(b)).value == oracle_wrap(a * b, bits, signed), \
                (name, "mul", a, b)


def test_unsigned_wraparound_explicit():
    """Named edge case: unsigned wraparound (doctrine table: uint32_t(0xFFFFFFFF) + 1 -> 0)."""
    assert (w.U32(0xFFFFFFFF) + w.U32(1)).value == 0
    assert (w.U8(0xFF) + w.U8(1)).value == 0
    assert (w.U64(2 ** 64 - 1) + w.U64(1)).value == 0


def test_signed_max_min_boundary():
    """Named edge case: type max/min."""
    for name, cls in ALL_TYPES:
        if not cls.SIGNED:
            continue
        assert (cls(cls.MAX) + cls(1)).value == cls.MIN, name
        assert (cls(cls.MIN) - cls(1)).value == cls.MAX, name


# ---------------------------------------------------------------------------
# 1b. Bitwise: &, |, ^, ~ -- signedness-invariant AT MATCHED WIDTH (doctrine
# section 3: these five/six ops are bit-identical whether the pattern is
# read as signed or unsigned). Verified directly, not assumed.
# ---------------------------------------------------------------------------

BITWIDTH_PAIRS = [(TYPES[f"u{b}"], TYPES[f"i{b}"]) for b in (8, 16, 32, 64)]


@pytest.mark.parametrize("ucls,icls", BITWIDTH_PAIRS)
def test_bitwise_signedness_invariant_at_matched_width(ucls, icls):
    bits = ucls.BITS
    patterns = sample_values(bits, signed=False)  # unsigned view covers full bit range
    for pa in patterns:
        for pb in patterns:
            u_and = (ucls(pa) & ucls(pb)).value
            i_and = (icls(pa) & icls(pb)).value & ((1 << bits) - 1)
            assert u_and == i_and, ("and", pa, pb)

            u_or = (ucls(pa) | ucls(pb)).value
            i_or = (icls(pa) | icls(pb)).value & ((1 << bits) - 1)
            assert u_or == i_or, ("or", pa, pb)

            u_xor = (ucls(pa) ^ ucls(pb)).value
            i_xor = (icls(pa) ^ icls(pb)).value & ((1 << bits) - 1)
            assert u_xor == i_xor, ("xor", pa, pb)

        u_not = (~ucls(pa)).value
        i_not = (~icls(pa)).value & ((1 << bits) - 1)
        assert u_not == i_not, ("not", pa)


@pytest.mark.parametrize("name,cls", ALL_TYPES)
def test_bitwise_against_oracle(name, cls):
    bits, signed = cls.BITS, cls.SIGNED
    vals = sample_values(bits, signed)
    mask = (1 << bits) - 1
    for a in vals:
        for b in vals:
            araw, braw = a & mask, b & mask
            assert (cls(a) & cls(b)).value == oracle_wrap(araw & braw, bits, signed)
            assert (cls(a) | cls(b)).value == oracle_wrap(araw | braw, bits, signed)
            assert (cls(a) ^ cls(b)).value == oracle_wrap(araw ^ braw, bits, signed)
        assert (~cls(a)).value == oracle_wrap((~ (a & mask)) & mask, bits, signed)


# ---------------------------------------------------------------------------
# 1c. Shifts: logical (unsigned) vs. arithmetic (signed) right shift; left
# shift signedness-invariant. Includes shift-by-0 and shift-by-(width-1).
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,cls", ALL_TYPES)
def test_shift_by_zero_is_identity(name, cls):
    for v in sample_values(cls.BITS, cls.SIGNED):
        assert (cls(v) << 0).value == v
        assert (cls(v) >> 0).value == v


@pytest.mark.parametrize("name,cls", ALL_TYPES)
def test_shift_by_width_minus_one(name, cls):
    bits = cls.BITS
    lo, hi = bounds(bits, cls.SIGNED)
    for v in (lo, hi, -1 if cls.SIGNED else hi, 1):
        got_left = (cls(v) << (bits - 1)).value
        want_left = oracle_wrap(v * (1 << (bits - 1)), bits, cls.SIGNED)
        assert got_left == want_left, (name, "shl", v)

        if cls.SIGNED:
            # arithmetic: Python's own `>>` on an arbitrary-precision int
            # already floors toward -inf (sign-extends), which IS the
            # definition of arithmetic shift -- used directly as the
            # from-scratch oracle for the signed case (doctrine section 3).
            want_right = v >> (bits - 1)
        else:
            # logical: zero-fill from the top -- oracle via true (floor)
            # division on the non-negative canonical value, a different
            # code path than the implementation's native `>>` but
            # mathematically identical for non-negative operands.
            want_right = v // (1 << (bits - 1))
        got_right = (cls(v) >> (bits - 1)).value
        assert got_right == want_right, (name, "shr", v, got_right, want_right)


def test_doctrine_shift_divergence_worked_example():
    """The exact worked example from
    PseudoIR/DevComms/compiler_transpilation_experiment.md section 3:
    `0xFF00000000000000 >> 60` is 15 under a logical (unsigned) shift and
    -1 under an arithmetic (signed) shift."""
    pattern = 0xFF00000000000000
    assert (w.U64(pattern) >> 60).value == 15
    assert (w.I64(pattern) >> 60).value == -1


def test_shift_amount_masked_to_width():
    """Rust's release-mode wrapping_shl/wrapping_shr rule: the shift
    amount is masked to the width (rhs & (BITS - 1)), not passed through
    raw (which would either panic in debug Rust or, naively in Python,
    just perform an oversized shift)."""
    assert (w.U8(1) << 8).value == (w.U8(1) << 0).value == 1
    assert (w.U8(0x80) >> 8).value == (w.U8(0x80) >> 0).value == 0x80


# ---------------------------------------------------------------------------
# 1d. Signed division / remainder: truncate toward zero (dividend's sign),
# per class_1_value_model.trunc_div / v0 numbers.py's _tdiv-_tmod.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,cls", ALL_TYPES)
def test_division_remainder_against_oracle(name, cls):
    bits, signed = cls.BITS, cls.SIGNED
    vals = [v for v in sample_values(bits, signed) if v != 0]
    for a in sample_values(bits, signed):
        for b in vals:
            if signed and a == cls.MIN and b == -1:
                # RULED (the owner, 2026-07-28): the one div/rem overflow
                # input TRAPS (Rust panics); asserted separately in
                # test_min_divrem_neg_one_traps.
                with pytest.raises(OverflowError):
                    cls(a) // cls(b)
                with pytest.raises(OverflowError):
                    cls(a) % cls(b)
                continue
            got_div = (cls(a) // cls(b)).value
            want_div = oracle_wrap(oracle_trunc_div(a, b), bits, signed)
            assert got_div == want_div, (name, "div", a, b, got_div, want_div)

            got_mod = (cls(a) % cls(b)).value
            want_mod = oracle_wrap(oracle_trunc_mod(a, b), bits, signed)
            assert got_mod == want_mod, (name, "mod", a, b, got_mod, want_mod)


def test_signed_truncation_named_example():
    """Named edge case: signed division/remainder truncate toward zero.
    Source values: v0 numbers.py's own self-test / class_1_value_model's
    module-level demo both use (-7, 2) -> div -3, mod -1 (Python's // and
    % would give -4 and 1 -- the floor-division answer -- instead)."""
    assert (w.I32(-7) // w.I32(2)).value == -3
    assert (w.I32(-7) % w.I32(2)).value == -1
    assert (-7) // 2 == -4 and (-7) % 2 == 1          # Python floor, for contrast


def test_division_by_zero_traps():
    with pytest.raises(ZeroDivisionError):
        w.I32(1) // w.I32(0)
    with pytest.raises(ZeroDivisionError):
        w.U8(1) % w.U8(0)


def test_min_divrem_neg_one_traps():
    """RULED (the owner, 2026-07-28): MIN / -1 and MIN % -1 TRAP, matching
    real Rust's unconditional panic (even in release). Replaces the
    earlier pinned-wrap deviation test. Neighboring inputs must NOT
    trap: MIN / 1, MIN % 1, (MIN+1) / -1, MAX / -1."""
    for cls in (w.I8, w.I32, w.I64):
        with pytest.raises(OverflowError):
            cls(cls.MIN) // cls(-1)
        with pytest.raises(OverflowError):
            cls(cls.MIN) % cls(-1)
        with pytest.raises(OverflowError):
            cls(cls.MIN) / cls(-1)
        assert (cls(cls.MIN) // cls(1)).value == cls.MIN
        assert (cls(cls.MIN) % cls(1)).value == 0
        assert (cls(cls.MIN + 1) // cls(-1)).value == cls.MAX
        assert (cls(cls.MAX) // cls(-1)).value == -cls.MAX
    # unsigned types have no -1; coercion wraps -1 to MAX, no trap path
    assert (w.U8(w.U8.MIN) // w.U8(255)).value == 0


# ---------------------------------------------------------------------------
# 1e. Comparisons: unsigned vs. signed compare genuinely diverge on the
# same bit pattern (doctrine section 3).
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,cls", ALL_TYPES)
def test_comparisons_against_oracle(name, cls):
    bits, signed = cls.BITS, cls.SIGNED
    vals = sample_values(bits, signed)
    for a in vals:
        for b in vals:
            assert (cls(a) < cls(b)) == (a < b)
            assert (cls(a) <= cls(b)) == (a <= b)
            assert (cls(a) > cls(b)) == (a > b)
            assert (cls(a) >= cls(b)) == (a >= b)
            assert (cls(a) == cls(b)) == (a == b)


def test_doctrine_unsigned_vs_signed_compare_divergence():
    """Named edge case + doctrine worked example: the all-ones 64-bit
    pattern compares as the maximum value unsigned, but as -1 signed --
    `0xFFFFFFFFFFFFFFFF < 1` is False unsigned / True signed."""
    pattern = 0xFFFFFFFFFFFFFFFF
    assert not (w.U64(pattern) < w.U64(1))
    assert (w.I64(pattern) < w.I64(1))


# ---------------------------------------------------------------------------
# 1f. Functional wrappers (u8/u32/i8 etc.) byte-identical to their PCv5
# source formulas, re-derived independently here.
# ---------------------------------------------------------------------------

def test_functional_wrappers_match_pcv5_formula_independently():
    for x in range(-300, 300):
        assert w.u8(x) == oracle_wrap(x, 8, signed=False)
        assert w.i8(x) == oracle_wrap(x, 8, signed=True)
    for x in (0, 1, -1, 0xFFFFFFFF, 0x100000000, -5, 2 ** 32 + 7):
        assert w.u32(x) == oracle_wrap(x, 32, signed=False)
    for name, fn in w.FUNCS.items():
        bits, signed = TYPES[name].BITS, TYPES[name].SIGNED
        for v in sample_values(bits, signed) + [1 << (bits + 3)]:
            assert fn(v) == oracle_wrap(v, bits, signed), (name, v)


# ---------------------------------------------------------------------------
# 1g. Mixed-type / cross-width refusal (uniform-wrapping border discipline).
# ---------------------------------------------------------------------------

def test_mixed_type_operator_refused():
    with pytest.raises(TypeError):
        w.U8(1) + w.U16(1)
    with pytest.raises(TypeError):
        w.I32(1) < w.I64(1)


def test_unsigned_unary_negation_refused():
    """Rust has no `Neg` impl for unsigned integer types -- `-x` on a u32
    is a compile error, unlike signed types where it wraps like any other
    operator here."""
    with pytest.raises(TypeError):
        -w.U32(5)
    assert (-w.I32(w.I32.MIN)).value == w.I32.MIN  # release-mode wrap, not a trap


# ---------------------------------------------------------------------------
# 2. check_uniformity: flags a deliberately non-uniform sample, passes a
# uniform one. Both modeled directly on a harvested transpile's real
# `encode_modrm` (the CORE_0_0_3 worked example).
# ---------------------------------------------------------------------------

UNIFORM_SAMPLE = """
def encode_modrm(m0d: u8, enc_reg_g: u8, rm_e: u8):
    return u8(u8(u8(m0d & 3) << 6) | u8(u8(enc_reg_g & 7) << 3) | u8(rm_e & 7))
"""

# the same expression with exactly one nested wrap removed (the innermost
# `m0d & 3` left bare before being shifted) -- the precise "mixed depth"
# CORE_0_0_3 forbids: this node is now ambiguous between "proven safe" and
# "tool missed it".
NON_UNIFORM_SAMPLE = """
def encode_modrm(m0d: u8, enc_reg_g: u8, rm_e: u8):
    return u8(u8((m0d & 3) << 6) | u8(u8(enc_reg_g & 7) << 3) | u8(rm_e & 7))
"""


def test_check_uniformity_passes_uniform_sample():
    assert cu.check(UNIFORM_SAMPLE) == []
    assert cu.is_uniform(UNIFORM_SAMPLE)


def test_check_uniformity_flags_non_uniform_sample():
    violations = cu.check(NON_UNIFORM_SAMPLE)
    assert violations, "expected the bare `m0d & 3` to be flagged"
    assert not cu.is_uniform(NON_UNIFORM_SAMPLE)
    assert any(v.snippet == "m0d & 3" for v in violations), violations


def test_check_uniformity_accepts_ast_input_too():
    import ast
    tree = ast.parse(UNIFORM_SAMPLE)
    assert cu.check(tree) == []
    tree2 = ast.parse(NON_UNIFORM_SAMPLE)
    assert cu.check(tree2)


def test_check_uniformity_catches_bare_operator_with_no_wrap_at_all():
    """A polyfilled value operated on with NO wrapper call anywhere --
    the simplest possible violation."""
    src = "def f(x: u8, y: u8):\n    return x & y\n"
    violations = cu.check(src)
    assert violations
    assert violations[0].snippet == "x & y"


def test_check_uniformity_ignores_unrelated_code():
    """Ordinary Python arithmetic on values never marked polyfilled must
    not be flagged -- the check is scoped to polyfilled values only."""
    src = "def f(x, y):\n    return x & y\n"
    assert cu.check(src) == []
