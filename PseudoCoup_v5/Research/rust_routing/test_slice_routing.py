"""Verifies slice 1: the transpiled routing produces the CLIF ops
rustc's own num.rs selects.

Expected values read directly from
sources/rust/compiler/rustc_codegen_cranelift/src/num.rs (lines
159-197) — the match arms of codegen_int_binop.
"""

from slice_mir_routing import route, I64, U64

CASES = [
    # (binop, type, expected CLIF op)   -- signed
    ("Add", I64, "iadd"), ("Sub", I64, "isub"), ("Mul", I64, "imul"),
    ("Div", I64, "sdiv"), ("Rem", I64, "srem"),
    ("BitXor", I64, "bxor"), ("BitAnd", I64, "band"),
    ("BitOr", I64, "bor"),
    ("Shl", I64, "ishl"), ("Shr", I64, "sshr"),
    # unsigned: the sign-dependent arms flip
    ("Div", U64, "udiv"), ("Rem", U64, "urem"), ("Shr", U64, "ushr"),
    ("Add", U64, "iadd"),          # sign-independent arms do not
]

ok = True
for binop, ty, want in CASES:
    res, clif = route(binop, ty)
    got = clif[0][0]
    flag = "PASS" if got == want else "FAIL"
    if got != want:
        ok = False
    print(f"{flag}  {binop:6} {ty:3} -> {got:5} (want {want})")

# the routing REFUSES what rustc refuses
for binop, ty, why in [
    ("Eq", I64, "compare binops handled elsewhere"),
    ("AddWithOverflow", I64, "checked binops handled elsewhere"),
    ("Offset", I64, "not an integer operation"),
]:
    try:
        route(binop, ty)
        print(f"FAIL  {binop} was allowed ({why})")
        ok = False
    except AssertionError:
        print(f"PASS  {binop:16} refused ({why})")

# type mismatch guard
try:
    from slice_mir_routing import codegen_int_binop, FunctionCx, CValue, Layout
    codegen_int_binop(FunctionCx(), "Add",
                      CValue("a", Layout(I64)), CValue("b", Layout(U64)))
    print("FAIL  mismatched types allowed")
    ok = False
except AssertionError:
    print("PASS  mismatched operand types refused")

print("\nTHE GENERATED MAPPING (what no compiler stores as a table):")
for binop in ("Add", "Div", "Rem", "Shr"):
    for ty in (I64, U64):
        _, clif = route(binop, ty)
        print(f"   ({binop:4}, {ty}) -> {clif[0][0]}")

print("\nSLICE 1 ROUTING:", "ALL PASS" if ok else "FAILURES PRESENT")
