"""END TO END: hub expression -> Rust's routing -> Rust's encoder ->
machine code -> executed in this Python process.

Every step is Rust's own logic, transpiled:
  slice 1  codegen_int_binop  (num.rs)          MIR   -> CLIF
  ISLE     Opcode::Sdiv arm   (isle_x64.rs)     CLIF  -> MInst
  slice 2  cqto_zo/idivq_m    (assembler.rs)    MInst -> bytes
  output ring                                    bytes -> running code
"""

from slice_mir_routing import route, I64, U64
from slice_encoder import CodeSink, GprMem, cqto_zo, idivq_m, emit, \
    RAX, RDX, RSI
from output_ring import mount
from rust_cell import RustI64

ok = True


def check(label, got, want):
    global ok
    if got != want:
        ok = False
    print(f"{'PASS' if got == want else 'FAIL'}  {label}: "
          f"{got if not isinstance(got, bytes) else got.hex(' ')}"
          f"{'' if got == want else f'  (want {want if not isinstance(want, bytes) else want.hex(chr(32))})'}")


# ---- step 1: routing (slice 1) ----
_, clif = route("Div", I64)
clif_op = clif[0][0]
check("routing: (Div, i64) -> CLIF", clif_op, "sdiv")

# ---- step 2: ISLE lowering for Opcode::Sdiv, I64 arm ----
# isle_x64.rs:16611-16620:
#   repeat_sign_bit(ty, lhs)  ->  cqto for I64
#   x64_idiv(ty, lhs, sign, divisor, trap) -> idivq_m for I64
assert clif_op == "sdiv"
from slice_lowering import lower
minsts, _rreg = lower(clif_op, I64, RSI)
check("lowering: sdiv -> MInst sequence",
      [type(m).__name__ for m in minsts], ["cqto_zo", "idivq_m"])

# ---- step 3: encoding (slice 2) — Rust's own encode() ----
code_cqto = emit(cqto_zo())
code_idiv = emit(idivq_m(RAX, RDX, GprMem(RSI)))
check("encode cqto_zo", code_cqto, bytes([0x48, 0x99]))
check("encode idivq_m rsi", code_idiv, bytes([0x48, 0xF7, 0xFE]))

# encoder must also be right for the extended registers (REX.B path)
check("encode idivq_m r14 (REX.B)",
      emit(idivq_m(RAX, RDX, GprMem(14))), bytes([0x49, 0xF7, 0xFE]))

# ---- step 4: assemble the callable stub ----
# System V: arg0 in RDI, arg1 in RSI, return in RAX.
#   mov rax, rdi     48 89 F8   (prologue: get dividend into RAX)
#   <cqto>                       produced by slice 2
#   <idivq rsi>                  produced by slice 2
#   ret              C3
PROLOGUE = bytes([0x48, 0x89, 0xF8])
RET = bytes([0xC3])
stub = PROLOGUE + code_cqto + code_idiv + RET
print("\n  assembled stub:", stub.hex(" "))

# ---- step 5: mount and run ----
fn = mount(stub)
print("  mounted:", fn, "\n")

GRID = [(-7, 2, -3), (7, 2, 3), (-7, -2, 3), (7, -2, -3),
        (-1, 2, 0), (9223372036854775807, 2, 4611686018427387903),
        (-9223372036854775808, 2, -4611686018427387904)]
for a, b, want in GRID:
    check(f"exec {a} r./ {b}", fn.call(a, b), want)

# ---- step 6: through RustI64 cells (border crossings only) ----
x, y = RustI64(-7), RustI64(2)
res = RustI64(fn.call(int(x), int(y)))
check("cells: RustI64(-7) r./ RustI64(2)", int(res), -3)
print(f"      {x!r} r./ {y!r} = {res!r}")
print(f"      Python's -7 // 2 = {-7 // 2}  <- the class-1 divergence")

print("\nEND TO END:", "ALL PASS" if ok else "FAILURES PRESENT")
