"""INPUT RING — the Ledger plays TyCtxt.

rustc's routing asks its type context: what type is this operand?
The Ledger already holds that answer for hub code, so the severed
edge re-anchors here rather than on a stand-in with invented data.

Scope for the PoC: types come from (a) the value itself when it is a
RustI64 cell, (b) declared annotations recorded by the import hook.
"""

from rust_cell import RustI64

I64 = "i64"
U64 = "u64"

# qualified type spellings usable in hub source annotations
QUALIFIED = {
    "r.i64": I64,
    "r.u64": U64,
}


class Ledger:
    def __init__(self):
        self._declared = {}          # name -> canonical type

    # --- recording (import hook feeds this from annotations) ---
    def declare(self, name: str, qualified_ty: str):
        if qualified_ty not in QUALIFIED:
            raise TypeError(f"Ledger: unknown qualified type "
                            f"{qualified_ty!r}")
        self._declared[name] = QUALIFIED[qualified_ty]

    def declared(self, name: str):
        return self._declared.get(name)

    # --- the TyCtxt question ---
    def type_of(self, value) -> str:
        """What rustc would ask TyCtxt. Cells carry their own type."""
        if isinstance(value, RustI64):
            return I64
        raise TypeError(
            f"Ledger: {type(value).__name__} is not a qualified value; "
            f"a qualified operator needs qualified operands "
            f"(wrap with r.i64(...))")

    def binop_types(self, lhs, rhs) -> str:
        lt, rt = self.type_of(lhs), self.type_of(rhs)
        if lt != rt:
            raise TypeError(
                f"Ledger: mismatched operand types {lt} vs {rt} "
                f"(rustc's codegen_int_binop asserts the same)")
        return lt


LEDGER = Ledger()
