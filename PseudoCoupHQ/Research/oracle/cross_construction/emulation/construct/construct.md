# construct.md -- the second tier, per target and by schema

Written by `construct/construct_report.py` off the pass's own run store and the bank; nothing here is typed in.

## 1. Refused by nature BEFORE, constructed AFTER

| target | width-or-kind refusals the bank held | distinct cells | places the tier constructed | of them proved end to end |
|---|---|---|---|---|
| c | 4 | 2 | 0 | 0 |
| cpp | 5 | 3 | 0 | 0 |
| rust | 34 | 32 | 0 | 0 |
| go | 51 | 47 | 12 | 7 |
| swift | 55 | 51 | 12 | 7 |
| **all five** | **149** | **51** | **24** | **14** |

## 2. By schema

| the schemas the lowering used | places | proved end to end |
|---|---|---|
| add / sub with carry and flags, widening / narrowing / sign spread | 10 | 10 |
| unsigned / signed divide and remainder, widening / narrowing / sign spread | 8 | 0 |
| shifts, rotates, widening / narrowing / sign spread | 4 | 4 |
| multiply (low and high halves), widening / narrowing / sign spread | 2 | 0 |

## 3. The three proof forms

| form | places |
|---|---|
| `canonical` | 0 |
| `lemma+gate` | 14 |
| `sat` | 0 |

## 4. The collapse column

| the compiler's landing | places |
|---|---|
| NOT_COLLAPSED | 14 |

## 5. Every constructed place, one row each

| target | `mnem` | shape | `key_width` | place | schemas | word | gate | equality | proof | instructions | landing |
|---|---|---|---|---|---|---|---|---|---|---|---|
| go | `adc` | gpr_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 7 | NOT_COLLAPSED |
| go | `adc` | imm_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 7 | NOT_COLLAPSED |
| go | `div` | gpr_one | 64 | reg_rax | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| go | `div` | gpr_one | 64 | reg_rdx | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| go | `idiv` | gpr_one | 64 | reg_rax | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| go | `idiv` | gpr_one | 64 | reg_rdx | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| go | `mul` | gpr_one | 64 | reg_rdx | multiply (low and high halves), widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | UNDECIDED | None | 27 | NOT_COLLAPSED |
| go | `sbb` | gpr_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 8 | NOT_COLLAPSED |
| go | `sbb` | gpr_same | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 6 | NOT_COLLAPSED |
| go | `sbb` | imm_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 8 | NOT_COLLAPSED |
| go | `shld` | cl_gpr_gpr | 64 | reg_rdi | shifts, rotates, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 17 | NOT_COLLAPSED |
| go | `shrd` | cl_gpr_gpr | 64 | reg_rdi | shifts, rotates, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 15 | NOT_COLLAPSED |
| swift | `adc` | gpr_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 4 | NOT_COLLAPSED |
| swift | `adc` | imm_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 4 | NOT_COLLAPSED |
| swift | `div` | gpr_one | 64 | reg_rax | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| swift | `div` | gpr_one | 64 | reg_rdx | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| swift | `idiv` | gpr_one | 64 | reg_rax | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| swift | `idiv` | gpr_one | 64 | reg_rdx | unsigned / signed divide and remainder, widening / narrowing / sign spread | 64 | the constructed term is larger than the  | None | None | None | None |
| swift | `mul` | gpr_one | 64 | reg_rdx | multiply (low and high halves), widening / narrowing / sign spread | 64 | UNDECIDED | UNDECIDED | None | 1 | LANDED_ELSEWHERE |
| swift | `sbb` | gpr_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 4 | NOT_COLLAPSED |
| swift | `sbb` | gpr_same | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 4 | NOT_COLLAPSED |
| swift | `sbb` | imm_gpr | 64 | reg_rdi | add / sub with carry and flags, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 4 | NOT_COLLAPSED |
| swift | `shld` | cl_gpr_gpr | 64 | reg_rdi | shifts, rotates, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 10 | NOT_COLLAPSED |
| swift | `shrd` | cl_gpr_gpr | 64 | reg_rdi | shifts, rotates, widening / narrowing / sign spread | 64 | PROVED_ON_SHIP | PROVED | lemma+gate | 10 | NOT_COLLAPSED |

## 6. Where the tier declined, by cause

| the cause, LITERAL | places |
|---|---|
| the native route proved this place, so there is nothing the second tier can add | 22 |

## 7. Both routes on one place

places both routes proved: 0

## 8. Every `sat`, with its point

| target | `mnem` | shape | `key_width` | place | schemas | the equality's seconds |
|---|---|---|---|---|---|---|

## 9. The lemmas

| schema | width | word | the shape | the shape's row | limbs |
|---|---|---|---|---|---|
| add / sub with carry and flags | 16 | 8 | `add_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 16 | 8 | `negate_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 16 | 8 | `sub_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 32 | 16 | `add_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 32 | 16 | `negate_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 32 | 16 | `sub_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 64 | 32 | `add_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 64 | 32 | `negate_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 64 | 32 | `sub_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 65 | 64 | `add_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 65 | 64 | `negate_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 65 | 64 | `sub_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 128 | 64 | `add_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 128 | 64 | `negate_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| add / sub with carry and flags | 128 | 64 | `sub_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 16 | 8 | `complement_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 16 | 8 | `differ_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 16 | 8 | `join_bits_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 16 | 8 | `meet_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 16 | 8 | `select_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 32 | 16 | `complement_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 32 | 16 | `differ_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 32 | 16 | `join_bits_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 32 | 16 | `meet_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 32 | 16 | `select_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 64 | 32 | `complement_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 64 | 32 | `differ_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 64 | 32 | `join_bits_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 64 | 32 | `meet_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 64 | 32 | `select_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 65 | 64 | `complement_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 65 | 64 | `differ_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 65 | 64 | `join_bits_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 65 | 64 | `meet_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 65 | 64 | `select_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 128 | 64 | `complement_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 128 | 64 | `differ_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 128 | 64 | `join_bits_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 128 | 64 | `meet_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| bitwise and select over the word | 128 | 64 | `select_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| comparisons and the flag word | 16 | 8 | `below_or_equal_signed_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 16 | 8 | `below_or_equal_unsigned_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 16 | 8 | `below_signed_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 16 | 8 | `below_unsigned_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 16 | 8 | `equal_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 32 | 16 | `below_or_equal_signed_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 32 | 16 | `below_or_equal_unsigned_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 32 | 16 | `below_signed_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 32 | 16 | `below_unsigned_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 32 | 16 | `equal_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 64 | 32 | `below_or_equal_signed_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 64 | 32 | `below_or_equal_unsigned_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 64 | 32 | `below_signed_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 64 | 32 | `below_unsigned_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 64 | 32 | `equal_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 65 | 64 | `below_or_equal_signed_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 65 | 64 | `below_or_equal_unsigned_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 65 | 64 | `below_signed_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 65 | 64 | `below_unsigned_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 65 | 64 | `equal_w65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 128 | 64 | `below_or_equal_signed_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 128 | 64 | `below_or_equal_unsigned_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 128 | 64 | `below_signed_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 128 | 64 | `below_unsigned_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| comparisons and the flag word | 128 | 64 | `equal_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| multiply (low and high halves) | 16 | 8 | `product_w16` | LEAN_REFUSED | 0 PROVED_BY_LEAN; 1 LEAN_REFUSED |
| multiply (low and high halves) | 32 | 16 | `product_w32` | LEAN_REFUSED | 0 PROVED_BY_LEAN; 1 LEAN_REFUSED |
| multiply (low and high halves) | 64 | 32 | `product_w64` | LEAN_REFUSED | 0 PROVED_BY_LEAN; 1 LEAN_REFUSED |
| multiply (low and high halves) | 65 | 64 | `product_w65` | LEAN_REFUSED | 0 PROVED_BY_LEAN; 1 LEAN_REFUSED |
| multiply (low and high halves) | 128 | 64 | `product_w128` | LEAN_REFUSED | 0 PROVED_BY_LEAN; 1 LEAN_REFUSED |
| shifts, rotates | 16 | 8 | `shift_down_arithmetic_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 16 | 8 | `shift_down_logical_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 16 | 8 | `shift_up_w16` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 32 | 16 | `shift_down_arithmetic_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 32 | 16 | `shift_down_logical_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 32 | 16 | `shift_up_w32` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 64 | 32 | `shift_down_arithmetic_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 64 | 32 | `shift_down_logical_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 64 | 32 | `shift_up_w64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 65 | 64 | `shift_down_arithmetic_w65` | REFUSED_BEFORE_LEAN | 0 REFUSED_BEFORE_LEAN; 1 REFUSED_BEFORE_LEAN |
| shifts, rotates | 65 | 64 | `shift_down_logical_w65` | REFUSED_BEFORE_LEAN | 0 REFUSED_BEFORE_LEAN; 1 REFUSED_BEFORE_LEAN |
| shifts, rotates | 65 | 64 | `shift_up_w65` | REFUSED_BEFORE_LEAN | 0 REFUSED_BEFORE_LEAN; 1 REFUSED_BEFORE_LEAN |
| shifts, rotates | 128 | 64 | `shift_down_arithmetic_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 128 | 64 | `shift_down_logical_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| shifts, rotates | 128 | 64 | `shift_up_w128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| unsigned / signed divide and remainder | 16 | 8 | `quotient_signed_w16` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 16 | 8 | `quotient_unsigned_w16` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 16 | 8 | `remainder_signed_w16` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 16 | 8 | `remainder_unsigned_w16` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 32 | 16 | `quotient_signed_w32` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 32 | 16 | `quotient_unsigned_w32` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 32 | 16 | `remainder_signed_w32` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 32 | 16 | `remainder_unsigned_w32` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 64 | 32 | `quotient_signed_w64` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 64 | 32 | `quotient_unsigned_w64` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 64 | 32 | `remainder_signed_w64` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 64 | 32 | `remainder_unsigned_w64` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 65 | 64 | `quotient_signed_w65` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 65 | 64 | `quotient_unsigned_w65` | REFUSED_BEFORE_LEAN | 0 TOO_LARGE_TO_STATE; 1 REFUSED_BEFORE_LEAN |
| unsigned / signed divide and remainder | 65 | 64 | `remainder_signed_w65` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 65 | 64 | `remainder_unsigned_w65` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 128 | 64 | `quotient_signed_w128` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 128 | 64 | `quotient_unsigned_w128` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 128 | 64 | `remainder_signed_w128` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| unsigned / signed divide and remainder | 128 | 64 | `remainder_unsigned_w128` | TOO_LARGE_TO_STATE | 0 TOO_LARGE_TO_STATE; 1 TOO_LARGE_TO_STATE |
| widening / narrowing / sign spread | 8 | 64 | `extend_zero_w8_t128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| widening / narrowing / sign spread | 64 | 64 | `extend_sign_w64_t128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| widening / narrowing / sign spread | 64 | 64 | `extend_zero_w64_t128` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| widening / narrowing / sign spread | 64 | 64 | `extend_zero_w64_t65` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| widening / narrowing / sign spread | 65 | 64 | `extract_w65_h64_l64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| widening / narrowing / sign spread | 128 | 64 | `concat_w128_p64-64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN; 1 PROVED_BY_LEAN |
| widening / narrowing / sign spread | 128 | 64 | `extract_w128_h127_l64` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |
| widening / narrowing / sign spread | 128 | 64 | `extract_w128_h63_l0` | PROVED_BY_LEAN | 0 PROVED_BY_LEAN |

## 10. The certificates the bank now holds on the constructed route

| kind | certificates |
|---|---|
| `proved` | 14 |

peak resident while writing this: 28392 kB
