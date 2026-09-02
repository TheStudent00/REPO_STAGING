"""Class 1 — value-model.

Naive divergence:
  -7 // 2        Python -4 (floor)  vs  C/Go/Java/C#/Dart -3 (truncate)
  -7 % 2         Python  1          vs  C-family -1 (sign follows dividend)
  int64 max + 1  Python grows       vs  Go/Java wrap, Swift traps, C++ UB
  -8 >> 1        same here          vs  logical shift on unsigned types

Policy fix (policy 4, 8): named operator family (floor_div/trunc_div),
declared-width ints with trap-on-overflow canon; wrapping only by
explicit spelling.
"""

INT64_MAX = 9223372036854775807


def floor_div(a: int, b: int) -> int:
    return a // b                      # canonical: Python floor


def trunc_div(a: int, b: int) -> int:  # the j.// / c.// borrow
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


def wrapping_add64(a: int, b: int) -> int:   # explicit go.+ borrow
    r = (a + b) & 0xFFFFFFFFFFFFFFFF
    return r - (1 << 64) if r >= (1 << 63) else r


print("floor_div(-7, 2)      =", floor_div(-7, 2))      # -4
print("trunc_div(-7, 2)      =", trunc_div(-7, 2))      # -3
print("wrapping_add64(max,1) =", wrapping_add64(INT64_MAX, 1))
# trap canon: unqualified (INT64_MAX + 1) at declared int64 is a
# dev-time/run-time ERROR, not a value. bigint spelling grows instead:
print("bigint max + 1        =", INT64_MAX + 1)
