"""wrap_fixed_width — the T4 wrapper layer: fixed-width integer types that
route arithmetic, bitwise, shift, and comparison operators through
Rust-matching semantics.

Governing law (CORE_0_0_3, settled): UNIFORM WRAPPING, NO EXEMPTIONS —
every operator on a polyfilled type routes through the wrapper, or none
do. Mixed depth is forbidden because an unwrapped node becomes ambiguous
between "proven safe" and "tool missed it".

PROVENANCE (ported, not invented — see README.md for the full map):

  u8() / u32() masking and the "wrap after every operator" style
      <- fixed-width masking, generalized: mask-then-return on every
         operator result (u8(x) -> x & 0xFF; u32(x) -> x & 0xFFFFFFFF),
         applied uniformly with no exemptions.

  i8() mask-then-sign-extend
      <- the same masking style, extended with a sign-extend step for
         signed widths.

  the generalized mask+sign-extend for ARBITRARY bit width (_wrap)
      <- StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/
         runtime/numbers.py:25-29 (`_wrap(v, bits)`), the exact source
         the T4 plan node cites as "v0 runtime/numbers.py (fixed-width
         at literals)". u8()/i8() above are the bits=8 special cases of
         this function; u32() is the bits=32, signed=False case.
         DEVIATION: v0's `_wrap` always sign-extends (Kotlin has no
         unsigned int type in that file — its docstring literally
         marks "unsigned (UInt/ULong) and `ushr`" as an unimplemented
         refinement). This module adds the `signed` parameter so the
         same formula covers both u* and i* — a generalization, not a
         semantic change, at every bit width the source exercises.

  signed truncating division / remainder (toward zero, dividend's sign)
      <- StressBot/.../runtime/numbers.py:32-40 (`_tdiv`/`_tmod`), and
         byte-identical formula in
         PseudoCoup_v5/Research/divergence_suite/class_1_value_model.py:21-23
         (`trunc_div`). Rust's `/` and `%` on signed integers use this
         same truncate-toward-zero rule.

  arithmetic vs. logical right shift chosen by signedness
      <- doctrine: PseudoIR/DevComms/compiler_transpilation_experiment.md
         section 3's divergence table (`0xFF00000000000000 >> 60` is
         15 logical / -1 arithmetic) and section 5's Map/Wrap/Fail
         rule ("Wrap only `>>` (as `>>>`/masked shift)... Map `~ & | ^
         + - *` directly — bit-identical at matched width"). NOT
         present in any harvested PCv5/v0 source: v0's `numbers.py`
         only ever implements arithmetic shift (Kotlin ints are always
         signed); no harvested masking-style source shifts anything but
         small non-negative register-encoding ints, so it never
         exercises the signed/unsigned divergence either. Implemented
         directly from the doctrine + Rust reference semantics, and
         checked against the doctrine's own worked example in
         test_polyfill.py.

  border discipline (explicit outbound crossing via __int__; refuse
  silent cross-width mixing)
      <- PseudoCoup_v5/Research/rust_routing/rust_cell.py (`RustI64`):
         "int(x) outbound: explicit, allowed"; out-of-range literals
         raise OverflowError ("trap canon, policy 8"). DEVIATION: this
         module does NOT refuse bare Python operators the way
         `RustI64` does (`__add__ = _refuse`, forcing a qualified
         `r.+` call). Here the operator IS the routing: `U8.__add__`
         etc. are the wrapper, so `a + b` on two `U8` instances already
         "routes through the wrapper" per CORE_0_0_3's own definition.
         `check_uniformity.py` exists for the case rust_cell.py's
         design prevents structurally: a value that carries polyfilled
         provenance but has been unwrapped (or was never wrapped) back
         into bare Python-int space.

  MIN / -1 and MIN % -1 signed div/rem overflow: TRAP -- raise
  OverflowError (RULED by the owner 2026-07-28, recorded in
  PseudoCoup_v6/AgentMemory/02_decisions.md). Real Rust
  panics unconditionally on both, even in release builds; the true
  quotient +2^(BITS-1) does not fit the type. An earlier build of
  this module silently wrapped (the uniform mask-the-result policy
  applied blindly); that was the recorded deviation, now closed.
  NOTE: a retired reference backend returned 0 for srem(MIN,-1) via a
  MACHINE-level checked-divide guard sequence; this module models Rust
  SURFACE semantics, which panic on the remainder too.

Source: a retired reference backend's assembler crate (fixed-width
masking style, since removed as mis-aimed — see AgentMemory for the
decision); rustc compiler sources (via rust_cell.py); PseudoCoup_v0
pseudokotlin runtime.
"""


# ---------------------------------------------------------------------------
# Core mask + sign-extend, generalized from v0 runtime/numbers.py's _wrap(v,
# bits) [always-signed] to also cover the unsigned masking style used
# elsewhere in this project's harvested sources. bits=8, signed=False here
# reproduces that plain byte-mask u8() byte-for-byte; bits=8, signed=True
# reproduces the mask-then-sign-extend i8() byte-for-byte.
# ---------------------------------------------------------------------------

def _wrap(value: int, bits: int, signed: bool) -> int:
    v = value & ((1 << bits) - 1)
    if signed and (v >> (bits - 1)):
        v -= 1 << bits
    return v


# ---------------------------------------------------------------------------
# Functional wrappers, matching the calling convention of the harvested
# masking-style sources. u8/u32 reproduce that plain byte/dword mask; i8
# reproduces the mask-then-sign-extend form; the rest are the same formula
# at the widths the doctrine's wrapper-set growth rule (CORE_0_0_3: "the
# wrapper SET grows per source-grammar need") calls for next (u16/u64/
# i16/i32/i64 -- byte, word, dword, qword).
# ---------------------------------------------------------------------------

def u8(x: int) -> int:
    return x & 0xFF


def u16(x: int) -> int:
    return _wrap(x, 16, signed=False)


def u32(x: int) -> int:
    return x & 0xFFFFFFFF


def u64(x: int) -> int:
    return _wrap(x, 64, signed=False)


def i8(x: int) -> int:
    x &= 0xFF
    return x - 256 if x >= 128 else x


def i16(x: int) -> int:
    return _wrap(x, 16, signed=True)


def i32(x: int) -> int:
    return _wrap(x, 32, signed=True)


def i64(x: int) -> int:
    return _wrap(x, 64, signed=True)


FUNCS = {
    "u8": u8, "u16": u16, "u32": u32, "u64": u64,
    "i8": i8, "i16": i16, "i32": i32, "i64": i64,
}


# ---------------------------------------------------------------------------
# Class-based wrapper types. Every arithmetic/bitwise/shift/comparison
# operator is a dunder method on this class -- Python's own operator dispatch
# is the routing mechanism CORE_0_0_3 requires ("routes through the
# wrapper"). Internal storage (`self.value`) is always the CANONICAL Python
# int for the type: masked-and-non-negative for u*, masked-and-sign-extended
# for i*. Keeping that invariant is what makes native Python comparison and
# right-shift automatically match Rust's unsigned/signed semantics (see the
# `__rshift__`/comparison notes below) without extra branching per call.
# ---------------------------------------------------------------------------

class FixedWidthInt:
    BITS: int = 0
    SIGNED: bool = False
    __slots__ = ("value",)

    def __init__(self, value: int = 0):
        self.value = _wrap(int(value), self.BITS, self.SIGNED)

    # --- borders (rust_cell.py precedent: explicit outbound crossing) ---
    def __int__(self) -> int:
        return self.value

    def __index__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value})"

    def __hash__(self):
        return hash((type(self), self.value))

    def cast(self, cls: "type[FixedWidthInt]") -> "FixedWidthInt":
        """Explicit cross-width/cross-signedness crossing (rust_cell.py's
        'int(x) outbound: explicit, allowed' pattern, generalized to
        cross into another wrapped type instead of only to bare int)."""
        return cls(self.value)

    # --- operand coercion: same wrapped type, or a bare Python int
    # (coerced at THIS type's width/signedness). A different wrapped
    # type is refused -- silent cross-width mixing is exactly the
    # ambiguity CORE_0_0_3 forbids. ---
    def _coerce(self, other):
        if type(other) is type(self):
            return other.value
        if isinstance(other, FixedWidthInt):
            raise TypeError(
                f"{type(self).__name__}: refused mixed-type operand "
                f"{type(other).__name__} (explicit .cast() required)")
        if isinstance(other, int):
            return _wrap(other, self.BITS, self.SIGNED)
        return NotImplemented

    def _make(self, raw: int) -> "FixedWidthInt":
        return type(self)(raw)

    def _check_divrem_overflow(self, dividend: int, divisor: int):
        """RULED (the owner, 2026-07-28): MIN / -1 and MIN % -1 TRAP.
        Real Rust panics unconditionally on both; the true quotient
        +2^(BITS-1) does not fit the type. Raise loudly instead of
        the silent wrap the uniform mask policy would produce."""
        if self.SIGNED and dividend == self.MIN and divisor == -1:
            raise OverflowError(
                f"{type(self).__name__}: {dividend} div/rem -1 overflows "
                f"(Rust panics: attempt to divide with overflow)")

    # --- arithmetic: wraps silently (matches the harvested mask-after-
    # every-op style: u8(u8(a) + u8(b)) collapses to one _wrap call here) ---
    def __add__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self._make(self.value + o)
    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self._make(self.value - o)

    def __rsub__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self._make(o - self.value)

    def __mul__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self._make(self.value * o)
    __rmul__ = __mul__

    def __neg__(self):
        if not self.SIGNED:
            raise TypeError(f"{type(self).__name__}: unary '-' refused on "
                             f"unsigned type (Rust: no Neg impl for u*)")
        return self._make(-self.value)

    def __invert__(self):
        return self._make(~self.value)

    # --- division / remainder: truncating toward zero, dividend's sign
    # (v0 _tdiv/_tmod; class_1_value_model.trunc_div). Unsigned operands
    # are never negative so this degenerates to plain floor division. ---
    def __truediv__(self, other):
        return self.__floordiv__(other)

    def __rtruediv__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        self._check_divrem_overflow(o, self.value)
        return self._make(_trunc_div(o, self.value))

    def __floordiv__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        self._check_divrem_overflow(self.value, o)
        return self._make(_trunc_div(self.value, o))

    def __rfloordiv__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        self._check_divrem_overflow(o, self.value)
        return self._make(_trunc_div(o, self.value))

    def __mod__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        self._check_divrem_overflow(self.value, o)
        return self._make(_trunc_mod(self.value, o))

    def __rmod__(self, other):
        o = self._coerce(other)
        if o is NotImplemented:
            return NotImplemented
        self._check_divrem_overflow(o, self.value)
        return self._make(_trunc_mod(o, self.value))

    # --- bitwise: signedness-invariant at matched width (doctrine
    # section 3) -- mask the raw result the same way regardless of
    # SIGNED; _make()/_wrap() re-applies sign-extension for i*. ---
    def __and__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self._make(self.value & o)
    __rand__ = __and__

    def __or__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self._make(self.value | o)
    __ror__ = __or__

    def __xor__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is NotImplemented else self._make(self.value ^ o)
    __rxor__ = __xor__

    # --- shifts: shift amount is masked to the width (Rust's release-mode
    # wrapping_shl/wrapping_shr rule: `rhs & (BITS - 1)`, BITS a power of
    # two). Left shift is signedness-invariant (drops high bits either
    # way). Right shift is NOT: unsigned must be logical (zero-fill),
    # signed must be arithmetic (sign-extend). Because `self.value` is
    # already the canonical Python int for this type -- non-negative for
    # u*, correctly negative for i* -- Python's native `>>` on that value
    # performs exactly the right kind of shift for free: `>>` on a
    # non-negative Python int is logical (no sign bit to extend), and
    # `>>` on a negative Python int floors toward -inf, i.e. arithmetic
    # (sign-extending). No extra branch on SIGNED is needed here. ---
    def __lshift__(self, amount: int):
        amt = int(amount) & (self.BITS - 1)
        return self._make(self.value << amt)

    def __rshift__(self, amount: int):
        amt = int(amount) & (self.BITS - 1)
        return self._make(self.value >> amt)

    # --- comparisons: because `self.value`/`other.value` are always the
    # canonical signed-or-unsigned Python int for the type, plain Python
    # comparison between two canonical values already reproduces Rust's
    # unsigned vs. signed compare divergence (doctrine section 3:
    # `0xFFFFFFFFFFFFFFFF < 1` is False unsigned / True as -1 signed) --
    # whichever wrapper type performed the comparison already carries the
    # right interpretation in its stored value. ---
    def __eq__(self, other):
        if type(other) is type(self):
            return self.value == other.value
        if isinstance(other, FixedWidthInt):
            return False
        if isinstance(other, int):
            return self.value == _wrap(other, self.BITS, self.SIGNED)
        return NotImplemented

    def _cmp_operand(self, other):
        if type(other) is type(self):
            return other.value
        if isinstance(other, FixedWidthInt):
            raise TypeError(
                f"{type(self).__name__}: refused mixed-type comparison "
                f"with {type(other).__name__} (explicit .cast() required)")
        if isinstance(other, int):
            return _wrap(other, self.BITS, self.SIGNED)
        return NotImplemented

    def __lt__(self, other):
        o = self._cmp_operand(other)
        return NotImplemented if o is NotImplemented else self.value < o

    def __le__(self, other):
        o = self._cmp_operand(other)
        return NotImplemented if o is NotImplemented else self.value <= o

    def __gt__(self, other):
        o = self._cmp_operand(other)
        return NotImplemented if o is NotImplemented else self.value > o

    def __ge__(self, other):
        o = self._cmp_operand(other)
        return NotImplemented if o is NotImplemented else self.value >= o


def _trunc_div(a: int, b: int) -> int:
    """Ported from v0 runtime/numbers.py's _tdiv / class_1_value_model's
    trunc_div: truncate toward zero, quotient sign = XOR of operand signs.
    b == 0 traps (Rust: integer division by zero always panics); this
    module raises Python's native ZeroDivisionError for it rather than
    v0's Kotlin-flavoured ArithmeticException, matching rust_cell.py's own
    precedent of representing a trap as a raised Python exception."""
    if b == 0:
        raise ZeroDivisionError("division by zero (Rust: integer division traps)")
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def _trunc_mod(a: int, b: int) -> int:
    """Ported from v0's _tmod: remainder takes the dividend's sign."""
    return a - _trunc_div(a, b) * b


def _make_type(name: str, bits: int, signed: bool):
    return type(name, (FixedWidthInt,), {"BITS": bits, "SIGNED": signed,
                                         "__slots__": ()})


U8 = _make_type("U8", 8, False)
U16 = _make_type("U16", 16, False)
U32 = _make_type("U32", 32, False)
U64 = _make_type("U64", 64, False)
I8 = _make_type("I8", 8, True)
I16 = _make_type("I16", 16, True)
I32 = _make_type("I32", 32, True)
I64 = _make_type("I64", 64, True)

TYPES = {
    "u8": U8, "u16": U16, "u32": U32, "u64": U64,
    "i8": I8, "i16": I16, "i32": I32, "i64": I64,
}

for _cls in TYPES.values():
    _bits, _signed = _cls.BITS, _cls.SIGNED
    _cls.MASK = (1 << _bits) - 1
    _cls.MAX = (1 << (_bits - 1)) - 1 if _signed else (1 << _bits) - 1
    _cls.MIN = -(1 << (_bits - 1)) if _signed else 0
del _cls, _bits, _signed
