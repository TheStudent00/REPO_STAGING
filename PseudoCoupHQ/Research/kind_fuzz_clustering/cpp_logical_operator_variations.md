# cpp `&&` and `||` — every variation

Measured 2026-08-24 from `arch_units_cpp.json`. One row per arch-unit:
`(operator, lhs type, rhs type)` plus the machine code it compiles to.
`spelling` distinguishes the two C-array forms (`ref` keeps the array
type, `decayed` is the pointer an ordinary call would pass).

## `&&` — 132 variations

| # | lhs | rhs | spelling | canonical machine code |
| --- | --- | --- | --- | --- |
| 1 | `T[N] (C array)` | `__int128` | decayed | `test %rdi,%rdi; setne %cl; or %rdx,%rsi; setne %al; and %cl,%al; ret` |
| 2 | `T[N] (C array)` | `__int128` | ref | `or %rdx,%rsi; setne %al; ret` |
| 3 | `T[N] (C array)` | `bool` | decayed | `test %rdi,%rdi; setne %al; and %sil,%al; ret` |
| 4 | `T[N] (C array)` | `bool` | ref | `mov %esi,%eax; ret` |
| 5 | `T[N] (C array)` | `const char*` | decayed | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 6 | `T[N] (C array)` | `const char*` | ref | `test %rsi,%rsi; setne %al; ret` |
| 7 | `T[N] (C array)` | `double` | decayed | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 8 | `T[N] (C array)` | `double` | ref | `xorpd %xmm1,%xmm1; cmpneqsd %xmm0,%xmm1; movq %xmm1,%rax; and $0x1,%eax; ret` |
| 9 | `T[N] (C array)` | `float` | decayed | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 10 | `T[N] (C array)` | `float` | ref | `xorps %xmm1,%xmm1; cmpneqss %xmm0,%xmm1; movd %xmm1,%eax; and $0x1,%eax; ret` |
| 11 | `T[N] (C array)` | `int32_t` | decayed | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; and %cl,%al; ret` |
| 12 | `T[N] (C array)` | `int32_t` | ref | `test %esi,%esi; setne %al; ret` |
| 13 | `T[N] (C array)` | `int64_t` | decayed | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 14 | `T[N] (C array)` | `int64_t` | ref | `test %rsi,%rsi; setne %al; ret` |
| 15 | `T[N] (C array)` | `std::nullptr_t` | decayed | `xor %eax,%eax; ret` |
| 16 | `T[N] (C array)` | `std::nullptr_t` | ref | `xor %eax,%eax; ret` |
| 17 | `T[N] (C array)` | `std::optional<int64_t>` | decayed | `test %rdi,%rdi; setne %al; and %dl,%al; ret` |
| 18 | `T[N] (C array)` | `std::optional<int64_t>` | ref | `mov %edx,%eax; and $0x1,%al; ret` |
| 19 | `T[N] (C array)` | `uint64_t` | decayed | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 20 | `T[N] (C array)` | `uint64_t` | ref | `test %rsi,%rsi; setne %al; ret` |
| 21 | `__int128` | `T[N] (C array)` | decayed | `or %rsi,%rdi; setne %cl; test %rdx,%rdx; setne %al; and %cl,%al; ret` |
| 22 | `__int128` | `T[N] (C array)` | ref | `or %rsi,%rdi; setne %al; ret` |
| 23 | `__int128` | `__int128` | plain | `or %rsi,%rdi; setne %sil; or %rcx,%rdx; setne %al; and %sil,%al; ret` |
| 24 | `__int128` | `bool` | plain | `or %rsi,%rdi; setne %al; and %dl,%al; ret` |
| 25 | `__int128` | `const char*` | plain | `or %rsi,%rdi; setne %cl; test %rdx,%rdx; setne %al; and %cl,%al; ret` |
| 26 | `__int128` | `double` | plain | `or %rsi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 27 | `__int128` | `float` | plain | `or %rsi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 28 | `__int128` | `int32_t` | plain | `or %rsi,%rdi; setne %cl; test %edx,%edx; setne %al; and %cl,%al; ret` |
| 29 | `__int128` | `int64_t` | plain | `or %rsi,%rdi; setne %cl; test %rdx,%rdx; setne %al; and %cl,%al; ret` |
| 30 | `__int128` | `std::nullptr_t` | plain | `xor %eax,%eax; ret` |
| 31 | `__int128` | `std::optional<int64_t>` | plain | `or %rsi,%rdi; setne %al; and %cl,%al; ret` |
| 32 | `__int128` | `uint64_t` | plain | `or %rsi,%rdi; setne %cl; test %rdx,%rdx; setne %al; and %cl,%al; ret` |
| 33 | `bool` | `T[N] (C array)` | decayed | `test %rsi,%rsi; setne %al; and %dil,%al; ret` |
| 34 | `bool` | `T[N] (C array)` | ref | `mov %edi,%eax; ret` |
| 35 | `bool` | `__int128` | plain | `or %rdx,%rsi; setne %al; and %dil,%al; ret` |
| 36 | `bool` | `bool` | plain | `mov %edi,%eax; and %esi,%eax; ret` |
| 37 | `bool` | `const char*` | plain | `test %rsi,%rsi; setne %al; and %dil,%al; ret` |
| 38 | `bool` | `double` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %dil,%al; ret` |
| 39 | `bool` | `float` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %dil,%al; ret` |
| 40 | `bool` | `int32_t` | plain | `test %esi,%esi; setne %al; and %dil,%al; ret` |
| 41 | `bool` | `int64_t` | plain | `test %rsi,%rsi; setne %al; and %dil,%al; ret` |
| 42 | `bool` | `uint64_t` | plain | `test %rsi,%rsi; setne %al; and %dil,%al; ret` |
| 43 | `const char*` | `T[N] (C array)` | decayed | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 44 | `const char*` | `T[N] (C array)` | ref | `test %rdi,%rdi; setne %al; ret` |
| 45 | `const char*` | `__int128` | plain | `test %rdi,%rdi; setne %cl; or %rdx,%rsi; setne %al; and %cl,%al; ret` |
| 46 | `const char*` | `bool` | plain | `test %rdi,%rdi; setne %al; and %sil,%al; ret` |
| 47 | `const char*` | `const char*` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 48 | `const char*` | `double` | plain | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 49 | `const char*` | `float` | plain | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 50 | `const char*` | `int32_t` | plain | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; and %cl,%al; ret` |
| 51 | `const char*` | `int64_t` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 52 | `const char*` | `std::nullptr_t` | plain | `xor %eax,%eax; ret` |
| 53 | `const char*` | `std::optional<int64_t>` | plain | `test %rdi,%rdi; setne %al; and %dl,%al; ret` |
| 54 | `const char*` | `uint64_t` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 55 | `double` | `T[N] (C array)` | decayed | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 56 | `double` | `T[N] (C array)` | ref | `xorpd %xmm1,%xmm1; cmpneqsd %xmm0,%xmm1; movq %xmm1,%rax; and $0x1,%eax; ret` |
| 57 | `double` | `__int128` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; or %rsi,%rdi; setne %al; and %cl,%al; ret` |
| 58 | `double` | `bool` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %dil,%al; ret` |
| 59 | `double` | `const char*` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 60 | `double` | `double` | plain | `xorpd %xmm2,%xmm2; cmpneqsd %xmm2,%xmm1; cmpneqsd %xmm2,%xmm0; andpd %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%al; ret` |
| 61 | `double` | `float` | plain | `xorpd %xmm2,%xmm2; ucomisd %xmm2,%xmm0; setp %al; setne %cl; or %al,%cl; xorpd %xmm0,%xmm0; ucomiss %xmm0,%xmm1; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 62 | `double` | `int32_t` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %edi,%edi; setne %al; and %cl,%al; ret` |
| 63 | `double` | `int64_t` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 64 | `double` | `std::nullptr_t` | plain | `xor %eax,%eax; ret` |
| 65 | `double` | `std::optional<int64_t>` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %sil,%al; ret` |
| 66 | `double` | `uint64_t` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 67 | `float` | `T[N] (C array)` | decayed | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 68 | `float` | `T[N] (C array)` | ref | `xorps %xmm1,%xmm1; cmpneqss %xmm0,%xmm1; movd %xmm1,%eax; and $0x1,%eax; ret` |
| 69 | `float` | `__int128` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; or %rsi,%rdi; setne %al; and %cl,%al; ret` |
| 70 | `float` | `bool` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %dil,%al; ret` |
| 71 | `float` | `const char*` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 72 | `float` | `double` | plain | `xorps %xmm2,%xmm2; ucomiss %xmm2,%xmm0; setp %al; setne %cl; or %al,%cl; xorps %xmm0,%xmm0; ucomisd %xmm0,%xmm1; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 73 | `float` | `float` | plain | `xorps %xmm2,%xmm2; cmpneqss %xmm2,%xmm1; cmpneqss %xmm2,%xmm0; andps %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%al; ret` |
| 74 | `float` | `int32_t` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %edi,%edi; setne %al; and %cl,%al; ret` |
| 75 | `float` | `int64_t` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 76 | `float` | `std::nullptr_t` | plain | `xor %eax,%eax; ret` |
| 77 | `float` | `std::optional<int64_t>` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %sil,%al; ret` |
| 78 | `float` | `uint64_t` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; and %cl,%al; ret` |
| 79 | `int32_t` | `T[N] (C array)` | decayed | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 80 | `int32_t` | `T[N] (C array)` | ref | `test %edi,%edi; setne %al; ret` |
| 81 | `int32_t` | `__int128` | plain | `test %edi,%edi; setne %cl; or %rdx,%rsi; setne %al; and %cl,%al; ret` |
| 82 | `int32_t` | `bool` | plain | `test %edi,%edi; setne %al; and %sil,%al; ret` |
| 83 | `int32_t` | `const char*` | plain | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 84 | `int32_t` | `double` | plain | `test %edi,%edi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 85 | `int32_t` | `float` | plain | `test %edi,%edi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 86 | `int32_t` | `int32_t` | plain | `test %edi,%edi; setne %cl; test %esi,%esi; setne %al; and %cl,%al; ret` |
| 87 | `int32_t` | `int64_t` | plain | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 88 | `int32_t` | `std::nullptr_t` | plain | `xor %eax,%eax; ret` |
| 89 | `int32_t` | `std::optional<int64_t>` | plain | `test %edi,%edi; setne %al; and %dl,%al; ret` |
| 90 | `int32_t` | `uint64_t` | plain | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 91 | `int64_t` | `T[N] (C array)` | decayed | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 92 | `int64_t` | `T[N] (C array)` | ref | `test %rdi,%rdi; setne %al; ret` |
| 93 | `int64_t` | `__int128` | plain | `test %rdi,%rdi; setne %cl; or %rdx,%rsi; setne %al; and %cl,%al; ret` |
| 94 | `int64_t` | `bool` | plain | `test %rdi,%rdi; setne %al; and %sil,%al; ret` |
| 95 | `int64_t` | `const char*` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 96 | `int64_t` | `double` | plain | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 97 | `int64_t` | `float` | plain | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 98 | `int64_t` | `int32_t` | plain | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; and %cl,%al; ret` |
| 99 | `int64_t` | `int64_t` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 100 | `int64_t` | `std::nullptr_t` | plain | `xor %eax,%eax; ret` |
| 101 | `int64_t` | `std::optional<int64_t>` | plain | `test %rdi,%rdi; setne %al; and %dl,%al; ret` |
| 102 | `int64_t` | `uint64_t` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 103 | `std::nullptr_t` | `T[N] (C array)` | decayed | `xor %eax,%eax; ret` |
| 104 | `std::nullptr_t` | `T[N] (C array)` | ref | `xor %eax,%eax; ret` |
| 105 | `std::nullptr_t` | `__int128` | plain | `xor %eax,%eax; ret` |
| 106 | `std::nullptr_t` | `const char*` | plain | `xor %eax,%eax; ret` |
| 107 | `std::nullptr_t` | `double` | plain | `xor %eax,%eax; ret` |
| 108 | `std::nullptr_t` | `float` | plain | `xor %eax,%eax; ret` |
| 109 | `std::nullptr_t` | `int32_t` | plain | `xor %eax,%eax; ret` |
| 110 | `std::nullptr_t` | `int64_t` | plain | `xor %eax,%eax; ret` |
| 111 | `std::nullptr_t` | `uint64_t` | plain | `xor %eax,%eax; ret` |
| 112 | `std::optional<int64_t>` | `T[N] (C array)` | decayed | `test %rdx,%rdx; setne %al; and %sil,%al; ret` |
| 113 | `std::optional<int64_t>` | `T[N] (C array)` | ref | `mov %esi,%eax; and $0x1,%al; ret` |
| 114 | `std::optional<int64_t>` | `__int128` | plain | `or %rcx,%rdx; setne %al; and %sil,%al; ret` |
| 115 | `std::optional<int64_t>` | `const char*` | plain | `test %rdx,%rdx; setne %al; and %sil,%al; ret` |
| 116 | `std::optional<int64_t>` | `double` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %sil,%al; ret` |
| 117 | `std::optional<int64_t>` | `float` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; and %sil,%al; ret` |
| 118 | `std::optional<int64_t>` | `int32_t` | plain | `test %edx,%edx; setne %al; and %sil,%al; ret` |
| 119 | `std::optional<int64_t>` | `int64_t` | plain | `test %rdx,%rdx; setne %al; and %sil,%al; ret` |
| 120 | `std::optional<int64_t>` | `uint64_t` | plain | `test %rdx,%rdx; setne %al; and %sil,%al; ret` |
| 121 | `uint64_t` | `T[N] (C array)` | decayed | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 122 | `uint64_t` | `T[N] (C array)` | ref | `test %rdi,%rdi; setne %al; ret` |
| 123 | `uint64_t` | `__int128` | plain | `test %rdi,%rdi; setne %cl; or %rdx,%rsi; setne %al; and %cl,%al; ret` |
| 124 | `uint64_t` | `bool` | plain | `test %rdi,%rdi; setne %al; and %sil,%al; ret` |
| 125 | `uint64_t` | `const char*` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 126 | `uint64_t` | `double` | plain | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 127 | `uint64_t` | `float` | plain | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; and %cl,%al; ret` |
| 128 | `uint64_t` | `int32_t` | plain | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; and %cl,%al; ret` |
| 129 | `uint64_t` | `int64_t` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |
| 130 | `uint64_t` | `std::nullptr_t` | plain | `xor %eax,%eax; ret` |
| 131 | `uint64_t` | `std::optional<int64_t>` | plain | `test %rdi,%rdi; setne %al; and %dl,%al; ret` |
| 132 | `uint64_t` | `uint64_t` | plain | `test %rdi,%rdi; setne %cl; test %rsi,%rsi; setne %al; and %cl,%al; ret` |

## `||` — 132 variations

| # | lhs | rhs | spelling | canonical machine code |
| --- | --- | --- | --- | --- |
| 1 | `T[N] (C array)` | `__int128` | decayed | `or %rdx,%rsi; or %rdi,%rsi; setne %al; ret` |
| 2 | `T[N] (C array)` | `__int128` | ref | `mov $0x1,%al; ret` |
| 3 | `T[N] (C array)` | `bool` | decayed | `test %rdi,%rdi; setne %al; or %sil,%al; ret` |
| 4 | `T[N] (C array)` | `bool` | ref | `mov $0x1,%al; ret` |
| 5 | `T[N] (C array)` | `const char*` | decayed | `or %rsi,%rdi; setne %al; ret` |
| 6 | `T[N] (C array)` | `const char*` | ref | `mov $0x1,%al; ret` |
| 7 | `T[N] (C array)` | `double` | decayed | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 8 | `T[N] (C array)` | `double` | ref | `mov $0x1,%al; ret` |
| 9 | `T[N] (C array)` | `float` | decayed | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 10 | `T[N] (C array)` | `float` | ref | `mov $0x1,%al; ret` |
| 11 | `T[N] (C array)` | `int32_t` | decayed | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; or %cl,%al; ret` |
| 12 | `T[N] (C array)` | `int32_t` | ref | `mov $0x1,%al; ret` |
| 13 | `T[N] (C array)` | `int64_t` | decayed | `or %rsi,%rdi; setne %al; ret` |
| 14 | `T[N] (C array)` | `int64_t` | ref | `mov $0x1,%al; ret` |
| 15 | `T[N] (C array)` | `std::nullptr_t` | decayed | `test %rdi,%rdi; setne %al; ret` |
| 16 | `T[N] (C array)` | `std::nullptr_t` | ref | `mov $0x1,%al; ret` |
| 17 | `T[N] (C array)` | `std::optional<int64_t>` | decayed | `test %rdi,%rdi; setne %al; or %dl,%al; and $0x1,%al; ret` |
| 18 | `T[N] (C array)` | `std::optional<int64_t>` | ref | `mov $0x1,%al; ret` |
| 19 | `T[N] (C array)` | `uint64_t` | decayed | `or %rsi,%rdi; setne %al; ret` |
| 20 | `T[N] (C array)` | `uint64_t` | ref | `mov $0x1,%al; ret` |
| 21 | `__int128` | `T[N] (C array)` | decayed | `or %rsi,%rdi; or %rdx,%rdi; setne %al; ret` |
| 22 | `__int128` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 23 | `__int128` | `__int128` | plain | `or %rcx,%rsi; or %rdx,%rdi; or %rsi,%rdi; setne %al; ret` |
| 24 | `__int128` | `bool` | plain | `or %rsi,%rdi; setne %al; or %dl,%al; ret` |
| 25 | `__int128` | `const char*` | plain | `or %rsi,%rdi; or %rdx,%rdi; setne %al; ret` |
| 26 | `__int128` | `double` | plain | `or %rsi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 27 | `__int128` | `float` | plain | `or %rsi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 28 | `__int128` | `int32_t` | plain | `or %rsi,%rdi; setne %cl; test %edx,%edx; setne %al; or %cl,%al; ret` |
| 29 | `__int128` | `int64_t` | plain | `or %rsi,%rdi; or %rdx,%rdi; setne %al; ret` |
| 30 | `__int128` | `std::nullptr_t` | plain | `or %rsi,%rdi; setne %al; ret` |
| 31 | `__int128` | `std::optional<int64_t>` | plain | `or %rsi,%rdi; setne %al; or %cl,%al; and $0x1,%al; ret` |
| 32 | `__int128` | `uint64_t` | plain | `or %rsi,%rdi; or %rdx,%rdi; setne %al; ret` |
| 33 | `bool` | `T[N] (C array)` | decayed | `test %rsi,%rsi; setne %al; or %dil,%al; ret` |
| 34 | `bool` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 35 | `bool` | `__int128` | plain | `or %rdx,%rsi; setne %al; or %dil,%al; ret` |
| 36 | `bool` | `bool` | plain | `mov %edi,%eax; or %esi,%eax; ret` |
| 37 | `bool` | `const char*` | plain | `test %rsi,%rsi; setne %al; or %dil,%al; ret` |
| 38 | `bool` | `double` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %dil,%al; ret` |
| 39 | `bool` | `float` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %dil,%al; ret` |
| 40 | `bool` | `int32_t` | plain | `test %esi,%esi; setne %al; or %dil,%al; ret` |
| 41 | `bool` | `int64_t` | plain | `test %rsi,%rsi; setne %al; or %dil,%al; ret` |
| 42 | `bool` | `uint64_t` | plain | `test %rsi,%rsi; setne %al; or %dil,%al; ret` |
| 43 | `const char*` | `T[N] (C array)` | decayed | `or %rsi,%rdi; setne %al; ret` |
| 44 | `const char*` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 45 | `const char*` | `__int128` | plain | `or %rdx,%rsi; or %rdi,%rsi; setne %al; ret` |
| 46 | `const char*` | `bool` | plain | `test %rdi,%rdi; setne %al; or %sil,%al; ret` |
| 47 | `const char*` | `const char*` | plain | `or %rsi,%rdi; setne %al; ret` |
| 48 | `const char*` | `double` | plain | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 49 | `const char*` | `float` | plain | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 50 | `const char*` | `int32_t` | plain | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; or %cl,%al; ret` |
| 51 | `const char*` | `int64_t` | plain | `or %rsi,%rdi; setne %al; ret` |
| 52 | `const char*` | `std::nullptr_t` | plain | `test %rdi,%rdi; setne %al; ret` |
| 53 | `const char*` | `std::optional<int64_t>` | plain | `test %rdi,%rdi; setne %al; or %dl,%al; and $0x1,%al; ret` |
| 54 | `const char*` | `uint64_t` | plain | `or %rsi,%rdi; setne %al; ret` |
| 55 | `double` | `T[N] (C array)` | decayed | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 56 | `double` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 57 | `double` | `__int128` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; or %rsi,%rdi; setne %al; or %cl,%al; ret` |
| 58 | `double` | `bool` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %dil,%al; ret` |
| 59 | `double` | `const char*` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 60 | `double` | `double` | plain | `xorpd %xmm2,%xmm2; cmpneqsd %xmm2,%xmm1; cmpneqsd %xmm2,%xmm0; orpd %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%al; ret` |
| 61 | `double` | `float` | plain | `xorpd %xmm2,%xmm2; ucomisd %xmm2,%xmm0; setp %al; setne %cl; or %al,%cl; xorpd %xmm0,%xmm0; ucomiss %xmm0,%xmm1; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 62 | `double` | `int32_t` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %edi,%edi; setne %al; or %cl,%al; ret` |
| 63 | `double` | `int64_t` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 64 | `double` | `std::nullptr_t` | plain | `xorpd %xmm1,%xmm1; cmpneqsd %xmm0,%xmm1; movq %xmm1,%rax; and $0x1,%eax; ret` |
| 65 | `double` | `std::optional<int64_t>` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %sil,%al; and $0x1,%al; ret` |
| 66 | `double` | `uint64_t` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 67 | `float` | `T[N] (C array)` | decayed | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 68 | `float` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 69 | `float` | `__int128` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; or %rsi,%rdi; setne %al; or %cl,%al; ret` |
| 70 | `float` | `bool` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %dil,%al; ret` |
| 71 | `float` | `const char*` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 72 | `float` | `double` | plain | `xorps %xmm2,%xmm2; ucomiss %xmm2,%xmm0; setp %al; setne %cl; or %al,%cl; xorps %xmm0,%xmm0; ucomisd %xmm0,%xmm1; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 73 | `float` | `float` | plain | `xorps %xmm2,%xmm2; cmpneqss %xmm2,%xmm1; cmpneqss %xmm2,%xmm0; orps %xmm1,%xmm0; movd %xmm0,%eax; and $0x1,%al; ret` |
| 74 | `float` | `int32_t` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %edi,%edi; setne %al; or %cl,%al; ret` |
| 75 | `float` | `int64_t` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 76 | `float` | `std::nullptr_t` | plain | `xorps %xmm1,%xmm1; cmpneqss %xmm0,%xmm1; movd %xmm1,%eax; and $0x1,%eax; ret` |
| 77 | `float` | `std::optional<int64_t>` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %sil,%al; and $0x1,%al; ret` |
| 78 | `float` | `uint64_t` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %al; setne %cl; or %al,%cl; test %rdi,%rdi; setne %al; or %cl,%al; ret` |
| 79 | `int32_t` | `T[N] (C array)` | decayed | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; or %cl,%al; ret` |
| 80 | `int32_t` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 81 | `int32_t` | `__int128` | plain | `test %edi,%edi; setne %cl; or %rdx,%rsi; setne %al; or %cl,%al; ret` |
| 82 | `int32_t` | `bool` | plain | `test %edi,%edi; setne %al; or %sil,%al; ret` |
| 83 | `int32_t` | `const char*` | plain | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; or %cl,%al; ret` |
| 84 | `int32_t` | `double` | plain | `test %edi,%edi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 85 | `int32_t` | `float` | plain | `test %edi,%edi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 86 | `int32_t` | `int32_t` | plain | `or %esi,%edi; setne %al; ret` |
| 87 | `int32_t` | `int64_t` | plain | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; or %cl,%al; ret` |
| 88 | `int32_t` | `std::nullptr_t` | plain | `test %edi,%edi; setne %al; ret` |
| 89 | `int32_t` | `std::optional<int64_t>` | plain | `test %edi,%edi; setne %al; or %dl,%al; and $0x1,%al; ret` |
| 90 | `int32_t` | `uint64_t` | plain | `test %edi,%edi; setne %cl; test %rsi,%rsi; setne %al; or %cl,%al; ret` |
| 91 | `int64_t` | `T[N] (C array)` | decayed | `or %rsi,%rdi; setne %al; ret` |
| 92 | `int64_t` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 93 | `int64_t` | `__int128` | plain | `or %rdx,%rsi; or %rdi,%rsi; setne %al; ret` |
| 94 | `int64_t` | `bool` | plain | `test %rdi,%rdi; setne %al; or %sil,%al; ret` |
| 95 | `int64_t` | `const char*` | plain | `or %rsi,%rdi; setne %al; ret` |
| 96 | `int64_t` | `double` | plain | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 97 | `int64_t` | `float` | plain | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 98 | `int64_t` | `int32_t` | plain | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; or %cl,%al; ret` |
| 99 | `int64_t` | `int64_t` | plain | `or %rsi,%rdi; setne %al; ret` |
| 100 | `int64_t` | `std::nullptr_t` | plain | `test %rdi,%rdi; setne %al; ret` |
| 101 | `int64_t` | `std::optional<int64_t>` | plain | `test %rdi,%rdi; setne %al; or %dl,%al; and $0x1,%al; ret` |
| 102 | `int64_t` | `uint64_t` | plain | `or %rsi,%rdi; setne %al; ret` |
| 103 | `std::nullptr_t` | `T[N] (C array)` | decayed | `test %rsi,%rsi; setne %al; ret` |
| 104 | `std::nullptr_t` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 105 | `std::nullptr_t` | `__int128` | plain | `or %rdx,%rsi; setne %al; ret` |
| 106 | `std::nullptr_t` | `const char*` | plain | `test %rsi,%rsi; setne %al; ret` |
| 107 | `std::nullptr_t` | `double` | plain | `xorpd %xmm1,%xmm1; cmpneqsd %xmm0,%xmm1; movq %xmm1,%rax; and $0x1,%eax; ret` |
| 108 | `std::nullptr_t` | `float` | plain | `xorps %xmm1,%xmm1; cmpneqss %xmm0,%xmm1; movd %xmm1,%eax; and $0x1,%eax; ret` |
| 109 | `std::nullptr_t` | `int32_t` | plain | `test %esi,%esi; setne %al; ret` |
| 110 | `std::nullptr_t` | `int64_t` | plain | `test %rsi,%rsi; setne %al; ret` |
| 111 | `std::nullptr_t` | `uint64_t` | plain | `test %rsi,%rsi; setne %al; ret` |
| 112 | `std::optional<int64_t>` | `T[N] (C array)` | decayed | `test %rdx,%rdx; setne %al; or %sil,%al; and $0x1,%al; ret` |
| 113 | `std::optional<int64_t>` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 114 | `std::optional<int64_t>` | `__int128` | plain | `or %rcx,%rdx; setne %al; or %sil,%al; and $0x1,%al; ret` |
| 115 | `std::optional<int64_t>` | `const char*` | plain | `test %rdx,%rdx; setne %al; or %sil,%al; and $0x1,%al; ret` |
| 116 | `std::optional<int64_t>` | `double` | plain | `xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %sil,%al; and $0x1,%al; ret` |
| 117 | `std::optional<int64_t>` | `float` | plain | `xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %cl; setne %al; or %cl,%al; or %sil,%al; and $0x1,%al; ret` |
| 118 | `std::optional<int64_t>` | `int32_t` | plain | `test %edx,%edx; setne %al; or %sil,%al; and $0x1,%al; ret` |
| 119 | `std::optional<int64_t>` | `int64_t` | plain | `test %rdx,%rdx; setne %al; or %sil,%al; and $0x1,%al; ret` |
| 120 | `std::optional<int64_t>` | `uint64_t` | plain | `test %rdx,%rdx; setne %al; or %sil,%al; and $0x1,%al; ret` |
| 121 | `uint64_t` | `T[N] (C array)` | decayed | `or %rsi,%rdi; setne %al; ret` |
| 122 | `uint64_t` | `T[N] (C array)` | ref | `mov $0x1,%al; ret` |
| 123 | `uint64_t` | `__int128` | plain | `or %rdx,%rsi; or %rdi,%rsi; setne %al; ret` |
| 124 | `uint64_t` | `bool` | plain | `test %rdi,%rdi; setne %al; or %sil,%al; ret` |
| 125 | `uint64_t` | `const char*` | plain | `or %rsi,%rdi; setne %al; ret` |
| 126 | `uint64_t` | `double` | plain | `test %rdi,%rdi; setne %cl; xorpd %xmm1,%xmm1; ucomisd %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 127 | `uint64_t` | `float` | plain | `test %rdi,%rdi; setne %cl; xorps %xmm1,%xmm1; ucomiss %xmm1,%xmm0; setp %dl; setne %al; or %dl,%al; or %cl,%al; ret` |
| 128 | `uint64_t` | `int32_t` | plain | `test %rdi,%rdi; setne %cl; test %esi,%esi; setne %al; or %cl,%al; ret` |
| 129 | `uint64_t` | `int64_t` | plain | `or %rsi,%rdi; setne %al; ret` |
| 130 | `uint64_t` | `std::nullptr_t` | plain | `test %rdi,%rdi; setne %al; ret` |
| 131 | `uint64_t` | `std::optional<int64_t>` | plain | `test %rdi,%rdi; setne %al; or %dl,%al; and $0x1,%al; ret` |
| 132 | `uint64_t` | `uint64_t` | plain | `or %rsi,%rdi; setne %al; ret` |
