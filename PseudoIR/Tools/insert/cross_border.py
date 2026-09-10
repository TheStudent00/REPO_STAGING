"""Wrap a mounted result in a typed cell that refuses unqualified operators; cross out with int(x).

PROVENANCE (harvested, not invented):
  The refusing-border discipline is ported from
  PRIVATE/PseudoCoup_v5/Research/rust_routing/rust_cell.py (61
  lines, read-and-verified): `int(x)` is the explicit outbound crossing;
  every unqualified Python operator (+, -, *, /, //, %, ...) is REFUSED
  so a qualified operand never silently re-enters Python arithmetic; an
  out-of-range literal raises OverflowError ("trap canon").

POLYFILL RECONCILIATION (decision, flagged for the owner):
  PRIVATE/PseudoCoup_v6/Tools/polyfill/wrap_fixed_width.py already
  has a FixedWidthInt/I64 wrapper, but its border policy is the OPPOSITE
  of what insertion needs: there the operator IS the routing
  (`a + b` on two I64 runs Rust-matching add), so it deliberately does
  NOT refuse bare operators (its own docstring records that deviation
  from rust_cell.py). Insertion's border must REFUSE bare operators —
  the mounted machine code is the only sanctioned arithmetic path, and a
  bare `cell + 1` must not silently fall back to Python.
  DECISION: DISTINGUISH the operator policy (this cell refuses; keep
  rust_cell's design) but REUSE polyfill's width math for the range
  check (import I64, do not copy `_wrap`) so the i64 range definition
  lives in exactly one place. This is reuse-of-arithmetic +
  distinct-border, not duplication.
"""

import os
import sys

# Import (do not copy) the T4 width math for the canonical i64 range.
# The polyfill lives in the OTHER project. PseudoIR borrows PseudoCoup's
# toolchain; this is one of the borrow points. Same env-var pattern the
# ledger and intentions suites used before their fixtures were vendored.
_PSEUDOCOUP = os.environ.get(
    "PSEUDOCOUP_ROOT", os.path.expanduser("PRIVATE/PseudoCoup_v6"))
_POLYFILL = os.path.join(_PSEUDOCOUP, "Tools", "polyfill")
if not os.path.isdir(_POLYFILL):
    raise RuntimeError(
        f"cannot find PseudoCoup's polyfill at {_POLYFILL}. "
        "Set PSEUDOCOUP_ROOT to PseudoCoup's repo root.")
if _POLYFILL not in sys.path:
    sys.path.insert(0, _POLYFILL)
from wrap_fixed_width import I64          # noqa: E402  (T4 reuse: range only)


class BorderCell:
    """A qualified i64 result: refuses unqualified Python operators; int(x) crosses outward."""

    __slots__ = ("_value",)

    def __init__(self, value: int):
        v = int(value)
        # Range check delegated to the T4 i64 definition (reuse, not copy).
        if not (I64.MIN <= v <= I64.MAX):
            raise OverflowError(
                f"BorderCell: {v} outside i64 [{I64.MIN}, {I64.MAX}] "
                f"(trap canon; the mounted stub returns i64)")
        self._value = v

    # --- outbound crossing: explicit, allowed (rust_cell.py precedent) ---
    def __int__(self) -> int:
        return self._value

    def __index__(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"BorderCell({self._value})"

    def __eq__(self, other) -> bool:
        if isinstance(other, BorderCell):
            return self._value == other._value
        return NotImplemented

    def __hash__(self):
        return hash(self._value)

    # --- refused crossings: unqualified Python operators ---
    def _refuse(self, *_):
        raise TypeError(
            "BorderCell: unqualified operator refused (class-1 border). "
            "The mounted machine code is the only sanctioned arithmetic "
            "path; cross out explicitly with int(x).")

    __add__ = __radd__ = __sub__ = __rsub__ = _refuse
    __mul__ = __rmul__ = __truediv__ = __rtruediv__ = _refuse
    __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = _refuse
    __and__ = __or__ = __xor__ = __lshift__ = __rshift__ = _refuse
    __neg__ = __invert__ = _refuse


def cell(value: int) -> BorderCell:
    """Wrap a plain int returned by mounted code as a qualified border cell."""
    return BorderCell(value)
