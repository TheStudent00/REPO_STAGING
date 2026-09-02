"""SLICE 1 — transpiled from rustc_codegen_cranelift/src/num.rs,
function `codegen_int_binop` (line 134).

This is the routing logic that generates the mapping which no
compiler stores as a table. Transpiled by hand here (PCv3 automation
is the extraction system's later job); the LOGIC is unaltered —
only severed edges are re-anchored (input ring below).

Severed edges and their re-anchors:
    fx: &mut FunctionCx   -> FunctionCx: type queries answered by
                             the Ledger stand-in; fx.bcx.ins()
                             becomes an instruction accumulator
    CValue / layout().ty  -> CValue + Layout stand-ins carrying
                             only the fields the slice touches
    codegen_i128          -> cut (unreachable for i64; guarded)
    trap-on-overflow FIXME-> preserved as rustc has it (no trap)
"""

# ---------------- input ring: stand-ins ----------------

I8, I16, I32, I64 = "i8", "i16", "i32", "i64"
U8, U16, U32, U64 = "u8", "u16", "u32", "u64"

SIGNED = {I8, I16, I32, I64}


class Layout:
    """Stand-in for rustc's TyAndLayout. The Ledger answers these."""

    def __init__(self, ty: str):
        self.ty = ty


class CValue:
    """Stand-in for CValue: a value plus its layout."""

    def __init__(self, name: str, layout: Layout):
        self.name = name
        self._layout = layout

    def layout(self) -> Layout:
        return self._layout

    def load_scalar(self, fx) -> str:
        return self.name

    @staticmethod
    def by_val(val: str, layout: Layout) -> "CValue":
        return CValue(val, layout)


class InstBuilder:
    """Stand-in for cranelift's InstBuilder (fx.bcx.ins()).

    Records the CLIF ops the routing logic selects — this recording
    IS the generated mapping the project was trying to extract.
    """

    def __init__(self, sink):
        self._sink = sink

    def _emit(self, op, lhs, rhs):
        res = f"v{len(self._sink)}"
        self._sink.append((op, lhs, rhs, res))
        return res

    def iadd(self, a, b): return self._emit("iadd", a, b)
    def isub(self, a, b): return self._emit("isub", a, b)
    def imul(self, a, b): return self._emit("imul", a, b)
    def sdiv(self, a, b): return self._emit("sdiv", a, b)
    def udiv(self, a, b): return self._emit("udiv", a, b)
    def srem(self, a, b): return self._emit("srem", a, b)
    def urem(self, a, b): return self._emit("urem", a, b)
    def bxor(self, a, b): return self._emit("bxor", a, b)
    def band(self, a, b): return self._emit("band", a, b)
    def bor(self, a, b): return self._emit("bor", a, b)
    def ishl(self, a, b): return self._emit("ishl", a, b)
    def sshr(self, a, b): return self._emit("sshr", a, b)
    def ushr(self, a, b): return self._emit("ushr", a, b)


class FunctionCx:
    def __init__(self):
        self.clif = []            # the produced CLIF op sequence

    class _Bcx:
        def __init__(self, outer):
            self._outer = outer

        def ins(self):
            return InstBuilder(self._outer.clif)

    @property
    def bcx(self):
        return FunctionCx._Bcx(self)


def type_sign(ty: str) -> bool:
    """Transpiled from num.rs's type_sign."""
    return ty in SIGNED


# ---------------- the slice proper ----------------

SHIFT_OPS = {"Shl", "ShlUnchecked", "Shr", "ShrUnchecked"}


def codegen_int_binop(fx: FunctionCx, bin_op: str,
                      in_lhs: CValue, in_rhs: CValue) -> CValue:
    if bin_op not in SHIFT_OPS:
        assert in_lhs.layout().ty == in_rhs.layout().ty, \
            "int binop requires lhs and rhs of same type"

    # crate::codegen_i128::maybe_codegen — cut; guard its precondition
    assert in_lhs.layout().ty not in ("i128", "u128"), \
        "i128 path cut from this slice"

    signed = type_sign(in_lhs.layout().ty)

    lhs = in_lhs.load_scalar(fx)
    rhs = in_rhs.load_scalar(fx)

    b = fx.bcx.ins()
    # FIXME trap on overflow for the Unchecked versions  [rustc's own]
    if bin_op in ("Add", "AddUnchecked"):
        val = b.iadd(lhs, rhs)
    elif bin_op in ("Sub", "SubUnchecked"):
        val = b.isub(lhs, rhs)
    elif bin_op in ("Mul", "MulUnchecked"):
        val = b.imul(lhs, rhs)
    elif bin_op == "Div":
        val = b.sdiv(lhs, rhs) if signed else b.udiv(lhs, rhs)
    elif bin_op == "Rem":
        val = b.srem(lhs, rhs) if signed else b.urem(lhs, rhs)
    elif bin_op == "BitXor":
        val = b.bxor(lhs, rhs)
    elif bin_op == "BitAnd":
        val = b.band(lhs, rhs)
    elif bin_op == "BitOr":
        val = b.bor(lhs, rhs)
    elif bin_op in ("Shl", "ShlUnchecked"):
        val = b.ishl(lhs, rhs)
    elif bin_op in ("Shr", "ShrUnchecked"):
        val = b.sshr(lhs, rhs) if signed else b.ushr(lhs, rhs)
    elif bin_op == "Offset":
        raise AssertionError("Offset is not an integer operation")
    elif bin_op in ("AddWithOverflow", "SubWithOverflow",
                    "MulWithOverflow"):
        raise AssertionError(
            "Overflow binops handled by codegen_checked_int_binop")
    elif bin_op in ("Eq", "Ne", "Lt", "Le", "Gt", "Ge", "Cmp"):
        raise AssertionError(
            f"{bin_op}({in_lhs.layout().ty}, {in_rhs.layout().ty})")
    else:
        raise AssertionError(f"unknown binop {bin_op}")

    return CValue.by_val(val, in_lhs.layout())


def route(bin_op: str, ty: str):
    """Convenience: run the routing for one binop on one type,
    return (result_cvalue, clif_sequence)."""
    fx = FunctionCx()
    lhs = CValue("a", Layout(ty))
    rhs = CValue("b", Layout(ty))
    res = codegen_int_binop(fx, bin_op, lhs, rhs)
    return res, fx.clif
