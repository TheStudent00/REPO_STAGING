"""Full stack: a .pc hub module using qualified operators, executed
by transpiled Rust logic, in stock CPython.

    demo.pc  --hook-->  rewritten  --Ledger-->  slice 1 routing
             --> slice 1.5 lowering --> slice 2 encoding
             --> mmap --> executed
"""

import pc_import
from pc_backend import cache_report
from rust_cell import RustI64

pc_import.install()
import demo                                    # loads demo.pc

ok = True


def check(label, got, want):
    global ok
    if got != want:
        ok = False
    print(f"{'PASS' if got == want else 'FAIL'}  {label}: {got}"
          f"{'' if got == want else f' (want {want})'}")


print("--- hub module values ---")
check("a", repr(demo.a), "RustI64(-7)")
check("b", repr(demo.b), "RustI64(2)")
check("a r./ b   (rust trunc)", int(demo.quotient), -3)
check("a r.% b", int(demo.remainder), -1)
check("(a r.* b) r./ b  chained", int(demo.chained), -7)
check("python -7 // 2 (contrast)", demo.python_floor, -4)
check("results are cells", isinstance(demo.quotient, RustI64), True)

print("\n--- what the transpiled pipeline produced ---")
for key, entry in sorted(cache_report().items()):
    print(f"  {key:10} clif={entry['clif']:5} "
          f"minsts={'+'.join(entry['minsts']):20} "
          f"bytes={entry['bytes']}")

print("\n--- border enforcement ---")
try:
    demo.quotient + 1
    check("unqualified + refused", "allowed", "refused")
except TypeError:
    check("unqualified + refused", "refused", "refused")

try:
    from pc_runtime import _r_div
    _ = 7 | _r_div | 2                    # plain ints, not cells
    check("unqualified operands refused", "allowed", "refused")
except TypeError:
    check("unqualified operands refused", "refused", "refused")

print("\nHUB MODULE:", "ALL PASS" if ok else "FAILURES PRESENT")
