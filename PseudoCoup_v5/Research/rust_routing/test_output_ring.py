"""Proves the output ring works with hand-assembled x86-64.

These byte strings stand in for what the transpiled Cranelift
encoder will produce. Proving the MOUNTING path here means the
later work only has to produce correct bytes — the delivery
mechanism is already verified.

Machine code used (System V: args RDI, RSI; return RAX):
  add:  48 89 F8      mov  rax, rdi
        48 01 F0      add  rax, rsi
        C3            ret
  idiv: 48 89 F8      mov  rax, rdi
        48 99         cqo                (sign-extend RAX into RDX)
        48 F7 FE      idiv rsi           (truncating division)
        C3            ret
"""

from output_ring import mount
from rust_cell import RustI64

ADD_I64 = bytes([0x48, 0x89, 0xF8, 0x48, 0x01, 0xF0, 0xC3])
DIV_I64 = bytes([0x48, 0x89, 0xF8, 0x48, 0x99, 0x48, 0xF7, 0xFE, 0xC3])

add = mount(ADD_I64)
div = mount(DIV_I64)
print("mounted:", add, "|", div)

ok = True


def check(label, got, want):
    global ok
    flag = "PASS" if got == want else "FAIL"
    if got != want:
        ok = False
    print(f"{flag}  {label}: got {got}, want {want}")


# 1. arithmetic through mounted code
check("5 + 37", add.call(5, 37), 42)
check("-7 + 2", add.call(-7, 2), -5)

# 2. Rust TRUNCATING division (Python would floor to -4)
check("-7 / 2 (rust trunc)", div.call(-7, 2), -3)
check("7 / -2 (rust trunc)", div.call(7, -2), -3)
check("-7 / -2 (rust trunc)", div.call(-7, -2), 3)
print("      (Python -7 // 2 =", -7 // 2, "— the class-1 divergence,",
      "resolved in OUR favor by using rust's arch op)")

# 3. i64 wrap-around: proves we are on a real 64-bit cell,
#    not Python bigint
MAX = 9223372036854775807
check("i64 max + 1 wraps", add.call(MAX, 1), -9223372036854775808)

# 4. cells: values crossing the border once, then staying Rust-side
a, b = RustI64(-7), RustI64(2)
result = RustI64(div.call(int(a), int(b)))
check("cell chain -7 r./ 2", int(result), -3)
print("      cell repr:", result, "| addr aligned:", result.addr % 8 == 0)

# 5. border refusal
try:
    _ = a + 1
    print("FAIL  border refusal: unqualified + was allowed")
    ok = False
except TypeError as e:
    print("PASS  border refusal:", str(e).split("(")[0].strip())

print("\nOUTPUT RING:", "ALL PASS" if ok else "FAILURES PRESENT")
