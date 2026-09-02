"""RustI64 — an aligned 8-byte cell in Rust's i64 layout, behind a
Python handle. PoC mounting (ctypes buffer); the fork mounting is a
lean C type with the same cell.

Border rules (class-1 lattice entry, now executable):
    int(x)          outbound: explicit, allowed
    x + 1           REFUSED: unqualified Python operator on a
                    qualified operand — no silent crossing
"""

import ctypes


class RustI64:
    __slots__ = ("_cell",)

    def __init__(self, value: int = 0):
        if not -(1 << 63) <= value < (1 << 63):
            raise OverflowError(
                "RustI64: literal outside i64 (trap canon, policy 8)")
        self._cell = ctypes.c_int64(value)

    # --- the cell itself: what compiled code receives ---
    @property
    def ptr(self):
        """Pointer to the 8-byte cell. Compiled code reads/writes here."""
        return ctypes.byref(self._cell)

    @property
    def addr(self) -> int:
        return ctypes.addressof(self._cell)

    # --- borders ---
    def __int__(self) -> int:
        return self._cell.value          # outbound crossing: explicit

    def __repr__(self) -> str:
        return f"RustI64({self._cell.value})"

    def __eq__(self, other) -> bool:
        if isinstance(other, RustI64):
            return self._cell.value == other._cell.value
        return NotImplemented

    def __hash__(self):
        return hash(self._cell.value)

    # --- refused crossings: unqualified Python operators ---
    def _refuse(self, *_):
        raise TypeError(
            "RustI64: unqualified operator refused (class-1 border). "
            "Use a qualified operator (r./ etc) or cross explicitly "
            "with int(x).")

    __add__ = __radd__ = __sub__ = __rsub__ = _refuse
    __mul__ = __rmul__ = __truediv__ = __rtruediv__ = _refuse
    __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = _refuse


def cells(*values):
    return tuple(RustI64(v) for v in values)
