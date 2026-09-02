"""Runtime injected into hub modules by the import hook.

Provides the qualified operators. Each one:
  1. asks the Ledger for the operand type (the TyCtxt question)
  2. runs the transpiled routing/lowering/encoding for that type
  3. calls the mounted machine code
  4. returns a RustI64 cell — values stay Rust-side between borders
"""

from ledger import LEDGER
from pc_backend import call_binop
from rust_cell import RustI64


class _Infix:
    """Carries a qualified operator through Python's `|` so hub source
    can spell it infix. The import hook rewrites `a r./ b` into
    `a |_r_div| b`; this class makes that work."""

    __slots__ = ("bin_op", "_lhs")

    def __init__(self, bin_op, lhs=None):
        self.bin_op = bin_op
        self._lhs = lhs

    def __ror__(self, lhs):
        return _Infix(self.bin_op, lhs)

    def __or__(self, rhs):
        ty = LEDGER.binop_types(self._lhs, rhs)
        result = call_binop(self.bin_op, ty, int(self._lhs), int(rhs))
        return RustI64(result)


_r_div = _Infix("Div")
_r_rem = _Infix("Rem")
_r_add = _Infix("Add")
_r_sub = _Infix("Sub")
_r_mul = _Infix("Mul")


def i64(value: int) -> RustI64:
    """r.i64(...) — the inbound border crossing."""
    return RustI64(value)


NAMESPACE = {
    "_r_div": _r_div, "_r_rem": _r_rem, "_r_add": _r_add,
    "_r_sub": _r_sub, "_r_mul": _r_mul,
    "_pc_i64": i64,
}
