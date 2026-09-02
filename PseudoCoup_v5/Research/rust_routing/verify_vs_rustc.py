"""Same grid as ground_truth.rs, computed entirely by the transpiled
pipeline. Compare with:

    rustc -O ground_truth.rs -o /tmp/gt && /tmp/gt > /tmp/rs.txt
    python3 verify_vs_rustc.py > /tmp/py.txt
    diff /tmp/rs.txt /tmp/py.txt && echo IDENTICAL
"""
from pc_backend import call_binop

I64, U64 = "i64", "u64"
VALS = [-7, -3, -2, -1, 0, 1, 2, 3, 7]
MIN = -(1 << 63)

for a in VALS:
    for b in VALS:
        add = call_binop("Add", I64, a, b)
        sub = call_binop("Sub", I64, a, b)
        mul = call_binop("Mul", I64, a, b)
        parts = [str(a), str(b), str(add), str(sub), str(mul)]
        can_div = b != 0 and not (a == MIN and b == -1)
        parts.append(str(call_binop("Div", I64, a, b)) if can_div else "-")
        parts.append(str(call_binop("Rem", I64, a, b)) if b != 0 else "-")
        print(" ".join(parts))

UVALS = [1, 2, 3, 7, 1 << 63, (1 << 64) - 2, (1 << 64) - 1]
for a in UVALS:
    for b in UVALS:
        print("u", a, b,
              call_binop("Div", U64, a, b),
              call_binop("Rem", U64, a, b))
