# boundaries.md — where each language changes its mind

Written 2026-08-20 with log 042.  Every number here is a value a run printed, or arithmetic over such values.  A **boundary** is the least value of one operand at which an operation stops answering in one class and starts answering in another.  The class is outcome plus result type plus fidelity, where fidelity asks only whether the answer equals the exact mathematical result.

The axis is the whole-number value axis of the value matrix:

```
0  <  42  <  2^53+1  <  2^63-1  <  2^63  <  2^64-1
```

## the run

| language | targets | located | no move | probes | worst probes |
|---|---|---|---|---|---|
| cpp | 1078 | 1078 | 0 | 47442 | 65 |
| csharp | 202 | 202 | 0 | 3206 | 65 |
| dart | 154 | 154 | 0 | 5646 | 65 |
| go | 82 | 82 | 0 | 2346 | 65 |
| java | 280 | 280 | 0 | 7084 | 65 |
| kotlin | 76 | 68 | 8 | 1152 | 65 |
| php | 240 | 188 | 52 | 7316 | 65 |
| python | 270 | 270 | 0 | 5684 | 65 |
| ruby | 184 | 184 | 0 | 7808 | 65 |
| rust | 188 | 188 | 0 | 7366 | 65 |
| typescript | 44 | 44 | 0 | 1424 | 65 |
| ALL | 2798 | 2738 | 60 | 96474 | 65 |

`no move' means the two ends of the span answered in the SAME class at run time, so the stored disagreement did not survive re-measurement.  Those are named in §the disagreements.

## the walls, in result space

For `+', `-' and `*' the boundary in operand space is dull and the boundary in RESULT space is the wall.  A wall is counted here only where exactly one power of two lies in the span the bisection closed on, and only where the holder itself had room for the value.

| language | varying holder | wall | boundaries |
|---|---|---|---|
| cpp | `__int128` | 2^127 | 4 |
| cpp | `int32_t` | 0 (the unsigned floor) | 3 |
| cpp | `int32_t` | 2^31 | 4 |
| cpp | `int32_t` | 2^63 | 7 |
| cpp | `int32_t` | 2^64 | 10 |
| cpp | `int64_t` | 0 (the unsigned floor) | 6 |
| cpp | `int64_t` | 2^63 | 17 |
| cpp | `int64_t` | 2^64 | 12 |
| cpp | `uint64_t` | 0 (the unsigned floor) | 20 |
| cpp | `uint64_t` | 2^127 | 2 |
| cpp | `uint64_t` | 2^64 | 46 |
| csharp | `int` | 2^63 | 4 |
| csharp | `long` | 2^63 | 20 |
| csharp | `short` | 2^63 | 4 |
| csharp | `ulong` | 0 (the unsigned floor) | 8 |
| csharp | `ulong` | 2^64 | 18 |
| dart | `int` | 2^63 | 6 |
| go | `int` | 2^63 | 12 |
| go | `int64` | 2^63 | 12 |
| go | `uint64` | 0 (the unsigned floor) | 8 |
| go | `uint64` | 2^64 | 18 |
| java | `Integer` | 2^63 | 8 |
| java | `Long` | 2^63 | 36 |
| java | `int` | 2^63 | 8 |
| java | `long` | 2^63 | 36 |
| java | `short` | 2^63 | 8 |
| kotlin | `Int` | 2^63 | 4 |
| kotlin | `Long` | 2^63 | 16 |
| php | `BCMath string-carried number (ext-bcmath)` | 0 (the unsigned floor) | 2 |
| php | `BCMath string-carried number (ext-bcmath)` | 2^63 | 24 |
| php | `int` | 2^63 | 24 |
| rust | `i128` | 2^127 | 2 |
| rust | `i64` | 2^63 | 12 |
| rust | `u64` | 0 (the unsigned floor) | 8 |
| rust | `u64` | 2^64 | 18 |

## the erosion at 2^53

A boundary that sits at 2^53 + 1 on the operand axis is a float-mantissa boundary: the value stops being representable and the answer stops agreeing with exact arithmetic.

| language | operation | varying holder | other holder | boundaries |
|---|---|---|---|---|
| cpp | `!=` | `__int128` | `int32_t` | 2 |
| cpp | `!=` | `int32_t` | `__int128` | 2 |
| cpp | `!=` | `int32_t` | `int64_t` | 2 |
| cpp | `!=` | `int32_t` | `uint64_t` | 2 |
| cpp | `!=` | `int64_t` | `int32_t` | 2 |
| cpp | `!=` | `uint64_t` | `int32_t` | 2 |
| cpp | `-` | `int64_t` | `uint64_t` | 1 |
| cpp | `-` | `uint64_t` | `int64_t` | 1 |
| cpp | `-` | `uint64_t` | `uint64_t` | 1 |
| cpp | `<` | `__int128` | `int32_t` | 1 |
| cpp | `<` | `int32_t` | `__int128` | 1 |
| cpp | `<` | `int32_t` | `int64_t` | 1 |
| cpp | `<` | `int64_t` | `int32_t` | 1 |
| cpp | `<` | `uint64_t` | `int32_t` | 1 |
| cpp | `<=` | `__int128` | `int32_t` | 1 |
| cpp | `<=` | `int32_t` | `__int128` | 1 |
| cpp | `<=` | `int32_t` | `int64_t` | 1 |
| cpp | `<=` | `int64_t` | `int32_t` | 1 |
| cpp | `<=` | `uint64_t` | `int32_t` | 1 |
| cpp | `==` | `__int128` | `int32_t` | 2 |
| cpp | `==` | `int32_t` | `__int128` | 2 |
| cpp | `==` | `int32_t` | `int64_t` | 2 |
| cpp | `==` | `int32_t` | `uint64_t` | 2 |
| cpp | `==` | `int64_t` | `int32_t` | 2 |
| cpp | `==` | `uint64_t` | `int32_t` | 2 |
| cpp | `>` | `__int128` | `int32_t` | 1 |
| cpp | `>` | `int32_t` | `__int128` | 1 |
| cpp | `>` | `int32_t` | `int64_t` | 1 |
| cpp | `>` | `int64_t` | `int32_t` | 1 |
| cpp | `>` | `uint64_t` | `int32_t` | 1 |
| cpp | `>=` | `__int128` | `int32_t` | 1 |
| cpp | `>=` | `int32_t` | `__int128` | 1 |
| cpp | `>=` | `int32_t` | `int64_t` | 1 |
| cpp | `>=` | `int64_t` | `int32_t` | 1 |
| cpp | `>=` | `uint64_t` | `int32_t` | 1 |
| csharp | `-` | `ulong` | `ulong` | 1 |
| dart | `*` | `double (whole number)` | `double (whole number)` | 2 |
| dart | `*` | `int` | `double (whole number)` | 2 |
| dart | `==` | `BigInt` | `double (whole number)` | 2 |
| dart | `==` | `BigInt` | `int` | 2 |
| dart | `==` | `double (whole number)` | `BigInt` | 2 |
| dart | `==` | `int` | `BigInt` | 2 |
| go | `-` | `uint64` | `uint64` | 1 |
| java | `!=` | `BigInteger` | `BigInteger` | 2 |
| java | `!=` | `Long` | `Long` | 2 |
| java | `==` | `BigInteger` | `BigInteger` | 2 |
| java | `==` | `Long` | `Long` | 2 |
| php | `/` | `BCMath string-carried number (ext-bcmath)` | `BCMath string-carried number (ext-bcmath)` | 2 |
| php | `/` | `BCMath string-carried number (ext-bcmath)` | `int` | 2 |
| php | `/` | `int` | `BCMath string-carried number (ext-bcmath)` | 2 |
| php | `/` | `int` | `int` | 2 |
| ruby | `!=` | `Integer` | `Integer` | 2 |
| ruby | `!=` | `Rational` | `Integer` | 2 |
| ruby | `<` | `Integer` | `Integer` | 1 |
| ruby | `<` | `Rational` | `Integer` | 1 |
| ruby | `<=` | `Integer` | `Integer` | 1 |
| ruby | `<=` | `Rational` | `Integer` | 1 |
| ruby | `==` | `Integer` | `Integer` | 2 |
| ruby | `==` | `Rational` | `Integer` | 2 |
| ruby | `===` | `Integer` | `Integer` | 2 |
| ruby | `===` | `Rational` | `Integer` | 2 |
| ruby | `>` | `Integer` | `Integer` | 1 |
| ruby | `>` | `Rational` | `Integer` | 1 |
| ruby | `>=` | `Integer` | `Integer` | 1 |
| ruby | `>=` | `Rational` | `Integer` | 1 |
| rust | `-` | `u64` | `u64` | 1 |
| typescript | `<` | `number` | `bigint` | 1 |
| typescript | `<=` | `number` | `bigint` | 1 |
| typescript | `>` | `number` | `bigint` | 1 |
| typescript | `>=` | `number` | `bigint` | 1 |

## the shift boundaries

| language | operation | varying holder | other holder | boundary | becomes | cells |
|---|---|---|---|---|---|---|
| rust | `<<` | `i128` | `i128` | 128 | raise | 6 |
| rust | `<<` | `i128` | `i32` | 32 | raise | 2 |
| rust | `<<` | `i128` | `i64` | 64 | raise | 4 |
| rust | `<<` | `i128` | `u64` | 64 | raise | 6 |
| rust | `<<` | `i32` | `i32` | 32 | raise | 2 |
| rust | `<<` | `i64` | `i128` | 128 | raise | 6 |
| rust | `<<` | `i64` | `i32` | 32 | raise | 2 |
| rust | `<<` | `i64` | `i64` | 64 | raise | 4 |
| rust | `<<` | `i64` | `u64` | 64 | raise | 6 |
| rust | `<<` | `u64` | `i128` | 128 | raise | 6 |
| rust | `<<` | `u64` | `i32` | 32 | raise | 2 |
| rust | `<<` | `u64` | `i64` | 64 | raise | 4 |
| rust | `<<` | `u64` | `u64` | 64 | raise | 6 |
| rust | `>>` | `i128` | `i128` | 128 | raise | 6 |
| rust | `>>` | `i128` | `i32` | 32 | raise | 2 |
| rust | `>>` | `i128` | `i64` | 64 | raise | 4 |
| rust | `>>` | `i128` | `u64` | 64 | raise | 6 |
| rust | `>>` | `i32` | `i32` | 32 | raise | 2 |
| rust | `>>` | `i64` | `i128` | 128 | raise | 6 |
| rust | `>>` | `i64` | `i32` | 32 | raise | 2 |
| rust | `>>` | `i64` | `i64` | 64 | raise | 4 |
| rust | `>>` | `i64` | `u64` | 64 | raise | 6 |
| rust | `>>` | `u64` | `i128` | 128 | raise | 6 |
| rust | `>>` | `u64` | `i32` | 32 | raise | 2 |
| rust | `>>` | `u64` | `i64` | 64 | raise | 4 |
| rust | `>>` | `u64` | `u64` | 64 | raise | 6 |

## the boundary at one

Two hundred and more boundaries sit at the value 1.  They are not walls.  They are the divisor leaving zero, and the truthiness of zero.

| language | operation | cells |
|---|---|---|
| cpp | `!=` | 8 |
| cpp | `%` | 96 |
| cpp | `*` | 40 |
| cpp | `+` | 14 |
| cpp | `-` | 7 |
| cpp | `/` | 96 |
| cpp | `<` | 8 |
| cpp | `<=` | 8 |
| cpp | `==` | 8 |
| cpp | `>` | 8 |
| cpp | `>=` | 8 |
| csharp | `%` | 74 |
| csharp | `+` | 8 |
| csharp | `-` | 1 |
| csharp | `/` | 74 |
| dart | `%` | 10 |
| dart | `*` | 16 |
| dart | `==` | 8 |
| dart | `~/` | 26 |
| go | `%` | 16 |
| go | `+` | 6 |
| go | `-` | 1 |
| go | `/` | 16 |
| java | `!=` | 2 |
| java | `%` | 70 |
| java | `+` | 20 |
| java | `/` | 70 |
| java | `==` | 2 |
| kotlin | `%` | 24 |
| kotlin | `+` | 4 |
| kotlin | `/` | 24 |
| php | `%` | 24 |
| php | `*` | 8 |
| php | `+` | 8 |
| php | `/` | 32 |
| python | `%` | 48 |
| python | `*` | 8 |
| python | `/` | 50 |
| python | `//` | 50 |
| python | `and` | 24 |
| python | `or` | 24 |
| ruby | `!=` | 4 |
| ruby | `%` | 12 |
| ruby | `/` | 12 |
| ruby | `<` | 2 |
| ruby | `<=` | 2 |
| ruby | `==` | 4 |
| ruby | `===` | 4 |
| ruby | `>` | 2 |
| ruby | `>=` | 2 |
| rust | `%` | 18 |
| rust | `+` | 4 |
| rust | `-` | 1 |
| rust | `/` | 18 |
| typescript | `%` | 6 |
| typescript | `&&` | 6 |
| typescript | `/` | 6 |
| typescript | `||` | 6 |

## where the holder ran out first

Some boundaries are not the operation changing its mind but the holder ceasing to hold the axis value.  They are counted apart so they cannot be read as arithmetic.

| language | holder | boundary shape | cells |
|---|---|---|---|
| cpp | `int32_t` | - | 231 |
| cpp | `int32_t` | 2^31 | 97 |
| cpp | `int32_t` | 2^31 + 1 | 1 |
| cpp | `int32_t` | 2^32 | 8 |
| cpp | `int32_t` | 2^53 + 1 | 20 |
| cpp | `int32_t` | 2^63 + 1 | 86 |
| cpp | `int32_t` | 2^63 - 1 | 20 |
| cpp | `int32_t` | 2^64 - 1 | 9 |
| cpp | `int64_t` | - | 10 |
| cpp | `int64_t` | 2^63 + 1 | 27 |
| cpp | `int64_t` | 2^64 - 1 | 20 |
| dart | `double (whole number)` | - | 20 |
| dart | `double (whole number)` | 2^53 + 1 | 4 |
| dart | `double (whole number)` | 2^63 + 1 | 8 |
| dart | `double (whole number)` | 2^63 - 1 | 2 |
| dart | `double (whole number)` | 2^64 - 1 | 2 |
| php | `int` | 2^63 + 1 | 4 |
| python | `ctypes.c_int64` | 2^63 + 1 | 10 |
| python | `ctypes.c_int64` | 2^64 - 1 | 8 |
| typescript | `number` | - | 16 |
| typescript | `number` | 2^53 + 1 | 4 |

## the disagreements

Where the stored answer and the re-measured run part company, the parting is written down rather than smoothed.

| language | operation | lhs holder | rhs holder | cells |
|---|---|---|---|---|
| kotlin | `-` | `BigInteger` | `BigInteger` | 8 |
| php | `!=` | `BCMath string-carried number (ext-bcmath)` | `int` | 1 |
| php | `!=` | `int` | `BCMath string-carried number (ext-bcmath)` | 1 |
| php | `!=` | `int` | `int` | 2 |
| php | `%` | `BCMath string-carried number (ext-bcmath)` | `int` | 6 |
| php | `%` | `int` | `int` | 6 |
| php | `*` | `BCMath string-carried number (ext-bcmath)` | `BCMath string-carried number (ext-bcmath)` | 2 |
| php | `*` | `BCMath string-carried number (ext-bcmath)` | `int` | 2 |
| php | `*` | `int` | `BCMath string-carried number (ext-bcmath)` | 2 |
| php | `*` | `int` | `int` | 2 |
| php | `-` | `BCMath string-carried number (ext-bcmath)` | `int` | 1 |
| php | `-` | `int` | `BCMath string-carried number (ext-bcmath)` | 1 |
| php | `-` | `int` | `int` | 2 |
| php | `<` | `BCMath string-carried number (ext-bcmath)` | `int` | 1 |
| php | `<` | `int` | `int` | 1 |
| php | `<<` | `int` | `int` | 6 |
| php | `<=` | `int` | `BCMath string-carried number (ext-bcmath)` | 1 |
| php | `<=` | `int` | `int` | 1 |
| php | `==` | `BCMath string-carried number (ext-bcmath)` | `int` | 1 |
| php | `==` | `int` | `BCMath string-carried number (ext-bcmath)` | 1 |
| php | `==` | `int` | `int` | 2 |
| php | `>` | `int` | `BCMath string-carried number (ext-bcmath)` | 1 |
| php | `>` | `int` | `int` | 1 |
| php | `>=` | `BCMath string-carried number (ext-bcmath)` | `int` | 1 |
| php | `>=` | `int` | `int` | 1 |
| php | `>>` | `int` | `int` | 6 |

## what was not run

| reason | targets |
|---|---|
| fixed operand is not a whole holder | 3445 |
| unbounded operation | 127 |
| shift on a holder with no width | 74 |

Beside those, 1623 target pairs needed no run at all: their two samples are adjacent integers, so the boundary is already exact in the stored answers.

