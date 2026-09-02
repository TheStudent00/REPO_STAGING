# the three verdicts -- tier 1

This is `verdicts.md` with ONE change: the pairs that the first pass left UNDECIDED because its z3 translation did not cover floating point, the flag helper or the 128-bit bitwise operations have been re-asked with a translation that does.  Every other verdict is carried forward unchanged and is still the first pass's.

A re-asked pair carries `tier1`, the verdict it used to have, and the reason it was re-asked.  A pair proved equal on fewer bits than both units define carries `scope_bits`: the width the claim holds at.  A pair re-asked with the ABI's `bool` promise as a precondition carries `abi_precondition`, and that verdict is CONDITIONAL on the promise.

**On a `scope_bits` of 8.**  Nearly every pair re-asked here is a COMPARISON or a BOOLEAN operator, whose answer is one byte: `setcc` writes one byte and leaves the seven above it holding whatever the caller left there, and `and $0x1,%eax` against `and $0x1,%al` differ in exactly those seven bytes and in nothing else.  The 8-bit claim is the whole answer for such an operator and is not the whole answer for any other, which is why the width is written on every verdict and why each row also carries the two sides' own `result_type`.

- pairs re-asked: **170**
- moved to: MATCHED 161, UNMATCHED 9
- bool pairs that moved under the ABI precondition: **15**
- wall seconds: 2

## what tier 1 models

- IEEE FP via z3's FP theory (SSE lane ops, the conversions, the four-value CmpF64/CmpF32)
- amd64g_calculate_rflags_c for SUB, ADD, LOGIC, COPY
- amd64g_calculate_condition for cc_op COPY
- the 128-bit bitwise vector operations

## tally

| verdict | pairs |
| --- | --- |
| MATCHED | 1133 |
| DIFFERS-BY-DESIGN | 60 |
| UNMATCHED | 131 |
| UNDECIDED | 196 |

## every pair re-asked at tier 1

| operator | type pair | left | right | was | now | scope | detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `!=` | bool,bool | c/op_533 | go/op_527 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `!=` | bool,bool | cpp/op_533 | go/op_527 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `!=` | bool,bool | go/op_527 | rust/op_317 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 8/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `!=` | bool,bool | go/op_527 | swift/op_473 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 8/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `!=` | f32,f32 | c/op_519 | go/op_513 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `!=` | f32,f32 | cpp/op_519 | go/op_513 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `!=` | f32,f32 | go/op_513 | rust/op_303 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `!=` | f32,f32 | go/op_513 | swift/op_459 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `!=` | f64,f64 | c/op_526 | go/op_520 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `!=` | f64,f64 | cpp/op_526 | go/op_520 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `!=` | f64,f64 | go/op_520 | rust/op_310 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `!=` | f64,f64 | go/op_520 | swift/op_466 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `&&` | bool,f32 | c/op_351 | cpp/op_351 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | bool,f64 | c/op_352 | cpp/op_352 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f32,bool | c/op_341 | cpp/op_341 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f32,f32 | c/op_339 | cpp/op_339 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `&&` | f32,f64 | c/op_340 | cpp/op_340 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128, 128/128 bits of these results |
| `&&` | f32,i32 | c/op_336 | cpp/op_336 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f32,i64 | c/op_337 | cpp/op_337 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f32,u64 | c/op_338 | cpp/op_338 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f64,bool | c/op_347 | cpp/op_347 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f64,f32 | c/op_345 | cpp/op_345 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128, 128/128 bits of these results |
| `&&` | f64,f64 | c/op_346 | cpp/op_346 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `&&` | f64,i32 | c/op_342 | cpp/op_342 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f64,i64 | c/op_343 | cpp/op_343 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | f64,u64 | c/op_344 | cpp/op_344 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | i32,f32 | c/op_321 | cpp/op_321 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | i32,f64 | c/op_322 | cpp/op_322 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | i64,f32 | c/op_327 | cpp/op_327 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | i64,f64 | c/op_328 | cpp/op_328 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | u64,f32 | c/op_333 | cpp/op_333 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `&&` | u64,f64 | c/op_334 | cpp/op_334 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `<` | bool,bool | c/op_677 | cpp/op_677 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `<` | bool,bool | c/op_677 | rust/op_353 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `<` | bool,f32 | c/op_675 | cpp/op_675 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | bool,f64 | c/op_676 | cpp/op_676 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,bool | c/op_665 | cpp/op_665 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,f32 | c/op_663 | cpp/op_663 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,f32 | c/op_663 | go/op_549 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,f32 | c/op_663 | rust/op_339 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,f32 | c/op_663 | swift/op_315 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,f64 | c/op_664 | cpp/op_664 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,i32 | c/op_660 | cpp/op_660 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f32,i64 | c/op_661 | cpp/op_661 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,bool | c/op_671 | cpp/op_671 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,f32 | c/op_669 | cpp/op_669 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,f64 | c/op_670 | cpp/op_670 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,f64 | c/op_670 | go/op_556 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,f64 | c/op_670 | rust/op_346 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,f64 | c/op_670 | swift/op_322 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,i32 | c/op_666 | cpp/op_666 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | f64,i64 | c/op_667 | cpp/op_667 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | i32,f32 | c/op_645 | cpp/op_645 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | i32,f64 | c/op_646 | cpp/op_646 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | i64,f32 | c/op_651 | cpp/op_651 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<` | i64,f64 | c/op_652 | cpp/op_652 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<<` | i64,u64 | c/op_686 | go/op_176 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 3, in1_64 = 69 |
| `<<` | i64,u64 | cpp/op_686 | go/op_176 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 251, in1_64 = 64 |
| `<<` | i64,u64 | go/op_176 | rust/op_470 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 255, in1_64 = 64 |
| `<<` | u64,u64 | c/op_692 | go/op_182 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 255, in1_64 = 64 |
| `<<` | u64,u64 | cpp/op_692 | go/op_182 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 11, in1_64 = 68 |
| `<<` | u64,u64 | go/op_182 | rust/op_476 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 15, in1_64 = 68 |
| `<<` | u64,u64 | go/op_182 | swift/op_704 | UNDECIDED | MATCHED | 64 | z3 proved the two lifted forms equal for every input (negation unsat) |
| `<=` | bool,bool | c/op_641 | cpp/op_641 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `<=` | bool,bool | c/op_641 | rust/op_389 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `<=` | bool,f32 | c/op_639 | cpp/op_639 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | bool,f64 | c/op_640 | cpp/op_640 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,bool | c/op_629 | cpp/op_629 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,f32 | c/op_627 | cpp/op_627 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,f32 | c/op_627 | go/op_585 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,f32 | c/op_627 | rust/op_375 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,f32 | c/op_627 | swift/op_387 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,f64 | c/op_628 | cpp/op_628 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,i32 | c/op_624 | cpp/op_624 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f32,i64 | c/op_625 | cpp/op_625 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,bool | c/op_635 | cpp/op_635 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,f32 | c/op_633 | cpp/op_633 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,f64 | c/op_634 | cpp/op_634 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,f64 | c/op_634 | go/op_592 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,f64 | c/op_634 | rust/op_382 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,f64 | c/op_634 | swift/op_394 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,i32 | c/op_630 | cpp/op_630 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | f64,i64 | c/op_631 | cpp/op_631 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | i32,f32 | c/op_609 | cpp/op_609 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | i32,f64 | c/op_610 | cpp/op_610 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | i64,f32 | c/op_615 | cpp/op_615 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `<=` | i64,f64 | c/op_616 | cpp/op_616 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `==` | bool,bool | cpp/op_497 | go/op_491 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `==` | bool,bool | go/op_491 | rust/op_281 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 8/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `==` | bool,bool | go/op_491 | swift/op_545 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 8/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `==` | f32,f32 | c/op_483 | go/op_477 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `==` | f32,f32 | cpp/op_483 | go/op_477 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `==` | f32,f32 | go/op_477 | rust/op_267 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `==` | f32,f32 | go/op_477 | swift/op_531 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `==` | f64,f64 | c/op_490 | go/op_484 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `==` | f64,f64 | cpp/op_490 | go/op_484 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers R_u0_64, R_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `==` | f64,f64 | go/op_484 | rust/op_274 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `==` | f64,f64 | go/op_484 | swift/op_538 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_64, L_u2_64; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `>` | bool,bool | c/op_569 | cpp/op_569 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `>` | bool,bool | c/op_569 | rust/op_425 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `>` | bool,f32 | c/op_567 | cpp/op_567 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | bool,f64 | c/op_568 | cpp/op_568 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,bool | c/op_557 | cpp/op_557 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,f32 | c/op_555 | cpp/op_555 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,f32 | c/op_555 | go/op_621 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,f32 | c/op_555 | rust/op_411 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,f32 | c/op_555 | swift/op_351 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,f64 | c/op_556 | cpp/op_556 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,i32 | c/op_552 | cpp/op_552 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f32,i64 | c/op_553 | cpp/op_553 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,bool | c/op_563 | cpp/op_563 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,f32 | c/op_561 | cpp/op_561 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,f64 | c/op_562 | cpp/op_562 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,f64 | c/op_562 | go/op_628 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,f64 | c/op_562 | rust/op_418 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,f64 | c/op_562 | swift/op_358 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,i32 | c/op_558 | cpp/op_558 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | f64,i64 | c/op_559 | cpp/op_559 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | i32,f32 | c/op_537 | cpp/op_537 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | i32,f64 | c/op_538 | cpp/op_538 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | i64,f32 | c/op_543 | cpp/op_543 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>` | i64,f64 | c/op_544 | cpp/op_544 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | bool,bool | c/op_605 | cpp/op_605 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `>=` | bool,bool | c/op_605 | rust/op_461 | UNMATCHED | MATCHED | 8 (ABI precondition) | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results; under the ABI precondition that each `bool` operand arrives as 0 or 1 in the low byte of its register |
| `>=` | bool,f32 | c/op_603 | cpp/op_603 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | bool,f64 | c/op_604 | cpp/op_604 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,bool | c/op_593 | cpp/op_593 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,f32 | c/op_591 | cpp/op_591 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,f32 | c/op_591 | go/op_657 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,f32 | c/op_591 | rust/op_447 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,f32 | c/op_591 | swift/op_423 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,f64 | c/op_592 | cpp/op_592 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,i32 | c/op_588 | cpp/op_588 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f32,i64 | c/op_589 | cpp/op_589 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,bool | c/op_599 | cpp/op_599 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,f32 | c/op_597 | cpp/op_597 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,f64 | c/op_598 | cpp/op_598 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,f64 | c/op_598 | go/op_664 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,f64 | c/op_598 | rust/op_454 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,f64 | c/op_598 | swift/op_430 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,i32 | c/op_594 | cpp/op_594 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | f64,i64 | c/op_595 | cpp/op_595 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | i32,f32 | c/op_573 | cpp/op_573 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | i32,f64 | c/op_574 | cpp/op_574 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | i64,f32 | c/op_579 | cpp/op_579 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>=` | i64,f64 | c/op_580 | cpp/op_580 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the proof holds for every value of the unanchored scratch registers L_u0_256, R_u0_256; the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8 bits of these results |
| `>>` | u64,u64 | c/op_728 | go/op_218 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 18302628885633695744, in1_64 = 121 |
| `>>` | u64,u64 | cpp/op_728 | go/op_218 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 18158513697557839872, in1_64 = 122 |
| `>>` | u64,u64 | go/op_218 | rust/op_512 | UNDECIDED | UNMATCHED | 8 | z3 counterexample at width 8 (the two units disagree at every width tried: 64, 32, 16, 8): in0_64 = 18230571291595767808, in1_64 = 120 |
| `>>` | u64,u64 | go/op_218 | swift/op_740 | UNDECIDED | MATCHED | 64 | z3 proved the two lifted forms equal for every input (negation unsat) |
| `||` | bool,f32 | c/op_315 | cpp/op_315 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | bool,f64 | c/op_316 | cpp/op_316 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f32,bool | c/op_305 | cpp/op_305 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f32,f32 | c/op_303 | cpp/op_303 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `||` | f32,f64 | c/op_304 | cpp/op_304 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128, 128/128 bits of these results |
| `||` | f32,i32 | c/op_300 | cpp/op_300 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f32,i64 | c/op_301 | cpp/op_301 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f32,u64 | c/op_302 | cpp/op_302 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f64,bool | c/op_311 | cpp/op_311 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f64,f32 | c/op_309 | cpp/op_309 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128, 128/128 bits of these results |
| `||` | f64,f64 | c/op_310 | cpp/op_310 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/64 bits of these results |
| `||` | f64,i32 | c/op_306 | cpp/op_306 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f64,i64 | c/op_307 | cpp/op_307 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | f64,u64 | c/op_308 | cpp/op_308 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | i32,f32 | c/op_285 | cpp/op_285 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | i32,f64 | c/op_286 | cpp/op_286 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | i64,f32 | c/op_291 | cpp/op_291 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | i64,f64 | c/op_292 | cpp/op_292 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | u64,f32 | c/op_297 | cpp/op_297 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |
| `||` | u64,f64 | c/op_298 | cpp/op_298 | UNDECIDED | MATCHED | 8 | z3 proved the two lifted forms equal for every input (negation unsat); the claim is over the low 8 bits -- the widest width at which it holds; the two units define 64/8, 128/128 bits of these results |

## what is still UNDECIDED, in the tool's own words

| pairs | reason |
| --- | --- |
| 18 | both units trap or panic, and their lifted forms differ; this pass classifies only a one-sided guard |
| 7 | the two units leave a different number of live results (2 and 1) |
| 6 | the two units leave a different number of live results (1 and 0) |
| 6 | the two units leave a different number of live results (1 and 2) |
| 4 | swift op_692 is not pure scalar dataflow: jmp $s9unit_ship6op_692ys5Int32VAD_s6UInt64VtF |
| 4 | swift op_698 is not pure scalar dataflow: jmp $s9unit_ship6op_698ys5Int64VAD_s6UInt64VtF |
| 4 | swift op_728 is not pure scalar dataflow: jmp $s9unit_ship6op_728ys5Int32VAD_s6UInt64VtF |
| 4 | swift op_734 is not pure scalar dataflow: jmp $s9unit_ship6op_734ys5Int64VAD_s6UInt64VtF |
| 3 | the two units leave a different number of live results (0 and 1) |
| 3 | swift op_690 is not pure scalar dataflow: jmp $s9unit_ship6op_690ys5Int32VAD_ADtF |
| 3 | swift op_691 is not pure scalar dataflow: jmp $s9unit_ship6op_691ys5Int32VAD_s5Int64VtF |
| 3 | swift op_696 is not pure scalar dataflow: jmp $s9unit_ship6op_696ys5Int64VAD_s5Int32VtF |
| 3 | swift op_697 is not pure scalar dataflow: jmp $s9unit_ship6op_697ys5Int64VAD_ADtF |
| 3 | swift op_702 is not pure scalar dataflow: jmp $s9unit_ship6op_702ys6UInt64VAD_s5Int32VtF |
| 3 | swift op_703 is not straight-line: 7 blocks |
| 3 | swift op_726 is not pure scalar dataflow: jmp $s9unit_ship6op_726ys5Int32VAD_ADtF |
| 3 | swift op_727 is not pure scalar dataflow: jmp $s9unit_ship6op_727ys5Int32VAD_s5Int64VtF |
| 3 | swift op_732 is not pure scalar dataflow: jmp $s9unit_ship6op_732ys5Int64VAD_s5Int32VtF |
| 3 | swift op_733 is not pure scalar dataflow: jmp $s9unit_ship6op_733ys5Int64VAD_ADtF |
| 3 | swift op_738 is not pure scalar dataflow: jmp $s9unit_ship6op_738ys6UInt64VAD_s5Int32VtF |
| 3 | swift op_739 is not straight-line: 7 blocks |
| 2 | core of c op_253 is ['ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64H |
| 2 | core of cpp op_253 is ['ex64@64(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(6 |
| 2 | go op_9 is not pure scalar dataflow: riprel movss |
| 2 | go op_10 is not pure scalar dataflow: riprel movsd |
| 2 | core of c op_217 is ['ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64HL |
| 2 | core of cpp op_217 is ['ex64@0(DivModS128to64(64HLto128(Sar64(in0:64,63:8),in0:64),in1:64))', 'ex64@64(DivModS128to64(64 |
| 2 | core of go op_168 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)),32:64 |
| 2 | core of go op_169 is ['zx64(And32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),ex3 |
| 2 | core of go op_174 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64 |
| 2 | core of go op_175 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64 |
| 2 | core of go op_180 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64 |
| 2 | core of go op_181 is ['And64(Shl64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64 |
| 2 | core of go op_204 is ['zx64(Or32(Not32(Sub32(0:32,And32(1:32,ex32@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@0(in1:64)), |
| 2 | core of go op_205 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,32:64,u0:64)))),in1:64)',  |
| 2 | core of go op_210 is ['Sar64(in0:64,And8(63:8,Or8(Not8(Sub8(0:8,And8(1:8,ex8@0(amd64g_calculate_rflags_c(7:64,zx64(ex32@ |
| 2 | core of go op_211 is ['Or64(Not64(Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64,in1:64,64:64,u0:64)))),in1:64)',  |
| 2 | core of go op_216 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(7:64 |
| 2 | core of go op_217 is ['And64(Shr64(in0:64,And8(63:8,ex8@0(in1:64))),Sub64(0:64,And64(1:64,amd64g_calculate_rflags_c(8:64 |
| 1 | core of c op_246 is ['zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))', |
| 1 | core of cpp op_246 is ['zx64(ex32@32(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64)))) |
| 1 | core of c op_260 is ['ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in |
| 1 | core of cpp op_260 is ['ex64@64(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64, |
| 1 | c op_35 writes memory |
| 1 | cpp op_47 writes memory |
| 1 | c op_33 writes memory |
| 1 | cpp op_45 writes memory |
| 1 | c op_34 writes memory |
| 1 | cpp op_46 writes memory |
| 1 | c op_30 writes memory |
| 1 | cpp op_42 writes memory |
| 1 | c op_31 writes memory |
| 1 | cpp op_43 writes memory |
| 1 | c op_32 writes memory |
| 1 | cpp op_44 writes memory |
| 1 | core of c op_188 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |
| 1 | core of cpp op_188 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |
| 1 | core of go op_74 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |
| 1 | core of rust op_620 is ['Mul64(in0:64,in1:64)']; core of swift op_128 is ['ex64@64(MullU64(in0:64,in1:64))'] |
| 1 | c op_15 is not pure scalar dataflow: riprel xorps |
| 1 | cpp op_15 is not pure scalar dataflow: riprel xorps |
| 1 | c op_16 is not pure scalar dataflow: riprel xorps |
| 1 | cpp op_16 is not pure scalar dataflow: riprel xorps |
| 1 | core of c op_210 is ['zx64(ex32@0(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))',  |
| 1 | core of cpp op_210 is ['zx64(ex32@0(DivModS64to32(32HLto64(Sar32(ex32@0(in0:64),31:8),ex32@0(in0:64)),ex32@0(in1:64))))' |
| 1 | core of c op_224 is ['ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,in0 |
| 1 | core of cpp op_224 is ['ex64@0(DivModU128to64(64HLto128(0:64,in0:64),in1:64))', 'ex64@64(DivModU128to64(64HLto128(0:64,i |
| 1 | c op_662 is not straight-line: 4 blocks |
| 1 | c op_668 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | c op_657 is not straight-line: 4 blocks |
| 1 | c op_658 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | core of c op_678 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_168 is ['zx64( |
| 1 | core of cpp op_678 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_168 is ['zx6 |
| 1 | core of c op_679 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_169 is ['zx64( |
| 1 | core of cpp op_679 is ['zx64(ex32@0(Shl64(zx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_169 is ['zx6 |
| 1 | core of c op_684 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_174 is ['And64(Shl64(in0:64,And8(63:8,ex8@ |
| 1 | core of cpp op_684 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_174 is ['And64(Shl64(in0:64,And8(63:8,ex |
| 1 | core of c op_685 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_175 is ['And64(Shl64(in0:64,And8(63:8,ex8@ |
| 1 | core of cpp op_685 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_175 is ['And64(Shl64(in0:64,And8(63:8,ex |
| 1 | core of c op_690 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_180 is ['And64(Shl64(in0:64,And8(63:8,ex8@ |
| 1 | core of cpp op_690 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_180 is ['And64(Shl64(in0:64,And8(63:8,ex |
| 1 | core of c op_691 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_181 is ['And64(Shl64(in0:64,And8(63:8,ex8@ |
| 1 | core of cpp op_691 is ['Shl64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_181 is ['And64(Shl64(in0:64,And8(63:8,ex |
| 1 | c op_626 is not straight-line: 4 blocks |
| 1 | c op_632 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | c op_621 is not straight-line: 4 blocks |
| 1 | c op_622 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | c op_554 is not straight-line: 4 blocks |
| 1 | c op_560 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | c op_549 is not straight-line: 4 blocks |
| 1 | c op_550 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | c op_590 is not straight-line: 4 blocks |
| 1 | c op_596 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | c op_585 is not straight-line: 4 blocks |
| 1 | c op_586 is not pure scalar dataflow: riprel punpckldq; riprel subpd |
| 1 | core of c op_714 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_204 is ['zx64( |
| 1 | core of cpp op_714 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_204 is ['zx6 |
| 1 | core of c op_715 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_205 is ['Or64( |
| 1 | core of cpp op_715 is ['zx64(ex32@0(Sar64(sx64(ex32@0(in0:64)),And8(31:8,ex8@0(in1:64)))))']; core of go op_205 is ['Or6 |
| 1 | core of c op_720 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_210 is ['Sar64(in0:64,And8(63:8,Or8(Not8(S |
| 1 | core of cpp op_720 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_210 is ['Sar64(in0:64,And8(63:8,Or8(Not8 |
| 1 | core of c op_721 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_211 is ['Or64(Not64(Sub64(0:64,And64(1:64, |
| 1 | core of cpp op_721 is ['Sar64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_211 is ['Or64(Not64(Sub64(0:64,And64(1:6 |
| 1 | core of c op_726 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_216 is ['And64(Shr64(in0:64,And8(63:8,ex8@ |
| 1 | core of cpp op_726 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_216 is ['And64(Shr64(in0:64,And8(63:8,ex |
| 1 | core of c op_727 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_217 is ['And64(Shr64(in0:64,And8(63:8,ex8@ |
| 1 | core of cpp op_727 is ['Shr64(in0:64,And8(63:8,ex8@0(in1:64)))']; core of go op_217 is ['And64(Shr64(in0:64,And8(63:8,ex |
