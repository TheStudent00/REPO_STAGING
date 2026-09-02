# the dominant-operator table -- with directional bridges

This is `dominant_table2.md` with one addition and no subtraction.  THE CLASSES ARE UNCHANGED: the result-type split stands, and a bridge merges nothing.  Every class row now also carries `bridges_out` and `bridges_in`.

A bridge says: **X dominates Y on projection P**.  At every reading Y's callers may perform -- P being the bits the dominated side's own result type promises -- X answers identically, and X answers readings Y cannot.  The row carries the projection, the proof scope, and the adapter an emitter inserts to put the dominated form where the dominant one is expected.

## the projection derivation table

| result type of the dominated side | projection | result register |
| --- | --- | --- |
| `bool` | 8 bits -- the low 8 bits, holding the value 0 or 1 -- what the ABI promises a bool return is | `%rax` |
| `f32` | 32 bits -- the low 32 bits of the result register -- one IEEE single | `%ymm0` |
| `f64` | 64 bits -- the low 64 bits of the result register -- one IEEE double | `%ymm0` |
| `i32` | 32 bits -- the low 32 bits, all of them valid | `%rax` |
| `i64` | 64 bits -- all 64 bits | `%rax` |
| `partial_ordering` | 8 bits -- the low 8 bits of the result register, holding one of the measured encoding values | `%rax` |
| `strong_ordering` | 8 bits -- the low 8 bits of the result register, holding one of the measured encoding values | `%rax` |
| `u32` | 32 bits -- the low 32 bits, all of them valid | `%rax` |
| `u64` | 64 bits -- all 64 bits | `%rax` |
| `weak_ordering` | 8 bits -- the low 8 bits of the result register, holding one of the measured encoding values | `%rax` |
| a result type this table does not name | none derived | -- |
| one side leaves extra live results | the ABI result register only | as above |

## the adapter derivation table

| dominated | dominant | adapter |
| --- | --- | --- |
| `bool` | `i32` | `movzbl %al, %eax` |
| `bool` | `i64` | `movzbl %al, %eax   -- writing %eax zeroes the upper 32 bits of %rax, so no second instruction is needed` |
| `bool` | `u64` | `movzbl %al, %eax   -- writing %eax zeroes the upper 32 bits of %rax, so no second instruction is needed` |
| `u32` | `u64` | `movl %eax, %eax` |
| extra live results | -- | read only %rax; the extra live register is not the answer |
| extra live results | -- | read only %xmm0; the extra live register is not the answer |
| anything else | | none derived -- recorded, not guessed |

## the counts

- bridges: **322**
- class pairs looked at and not bridged: **2110**

| projection kind | bridges |
| --- | --- |
| low-8 | 321 |
| result-register-only | 1 |

| direction | bridges |
| --- | --- |
| c dominates cpp | 281 |
| c dominates cpp,rust,swift | 17 |
| c dominates cpp,rust | 10 |
| c dominates cpp,go,rust,swift | 8 |
| c,cpp dominates cpp,go,rust,swift | 2 |
| c dominates c,cpp,rust,swift | 1 |
| c,cpp dominates cpp,rust,swift | 1 |
| c,cpp dominates c | 1 |
| c,cpp dominates swift | 1 |

## the different-live-results residue

- distinct pairs the solver left with that reason: **759**
- resolved by dominance (a direction proven): **3**
- still standing on the solver's own reason: **756**

| pairs | why it still stands |
| --- | --- |
| 248 | the two result types are answered in different registers (ymm0 and rax), so the result register is not one projection |
| 147 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [else -> fp.to_ieee_bv(Va |
| 105 | not equal on the projection: z3 counterexample on the projection (low 8 bits): MACHINE_sseround_64 = 1, fp.to_ieee_bv =  |
| 73 | not equal on the projection: z3 counterexample on the projection (low 8 bits): MACHINE_sseround_64 = 0, fp.to_ieee_bv =  |
| 50 | not equal on the projection: z3 counterexample on the projection (low 8 bits): MACHINE_sseround_64 = 2, fp.to_ieee_bv =  |
| 42 | not equal on the projection: z3 counterexample on the projection (low 8 bits):  |
| 16 | not equal on the projection: z3 counterexample on the projection (low 8 bits): MACHINE_sseround_64 = 3, fp.to_ieee_bv =  |
| 6 | not equal on the projection: z3 counterexample on the projection (low 8 bits): in0_64 = 0, in1_64 = 0 |
| 2 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 18442240474082181 |
| 2 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92188684372274053 |
| 2 | not equal on the projection: z3 counterexample on the projection (low 32 bits): in0_64 = 0, in1_64 = 0 |
| 2 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92233720368547758 |
| 2 | not equal on the projection: z3 counterexample on the projection (low 32 bits): in0_64 = 65535, in1_64 = 48 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92210036653444936 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 18445838076617436 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92189036215994941 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92188684372274708 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92228932815390363 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92219760172796883 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92201869504686904 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92233206318750491 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92211202402526085 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 18442371114079354 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 18444117658346035 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92212863592613225 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92230035604766681 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92198220011526289 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 92192268886319633 |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): in0_256 = 14186358635956797952, in1_256 = |
| 1 | not equal on the projection: z3 counterexample on the projection (low 8 bits): fp.to_ieee_bv = [NaN -> 18442353758845010 |

## every bridge

| dominant class | dominated class | operand types | dominant result | dominated result | projection | adapter |
| --- | --- | --- | --- | --- | --- | --- |
| K0006 | K0019 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0039 | K0020 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0491 | K0035 | bool,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0040 | K0036 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0654 | K0054 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0661 | K0055 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0546 | K0056 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0553 | K0057 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0618 | K0058 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0625 | K0059 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0582 | K0060 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0589 | K0061 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0489 | K0062 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0497 | K0063 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0504 | K0064 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0511 | K0065 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0518 | K0066 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0249 | K0067 | bool,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0633 | K0124 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0640 | K0125 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0647 | K0126 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0561 | K0127 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0568 | K0128 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0575 | K0129 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0453 | K0130 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0460 | K0131 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0467 | K0132 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0474 | K0133 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0481 | K0134 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0488 | K0135 | bool,bool | `i32` | `bool` | result-register-only (8 bits) | read only %rax; the extra live register is not the answer |
| K0377 | K0258 | i32,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0264 | K1103 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0378 | K0268 | i64,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0380 | K0308 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0381 | K0309 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0383 | K0310 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0384 | K0311 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0385 | K0312 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0386 | K0313 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0387 | K0314 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0389 | K0315 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0390 | K0316 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0391 | K0317 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0399 | K0318 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0400 | K0319 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0402 | K0320 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0403 | K0321 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0404 | K0322 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0405 | K0323 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0406 | K0324 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0408 | K0325 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0409 | K0326 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0410 | K0327 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0411 | K0328 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0412 | K0329 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0416 | K0330 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0417 | K0331 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0419 | K0332 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0420 | K0333 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0421 | K0334 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0422 | K0335 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0423 | K0336 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0425 | K0337 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0426 | K0338 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0427 | K0339 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0434 | K0340 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0435 | K0341 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0437 | K0342 | f32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0438 | K0343 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0439 | K0344 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0440 | K0345 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0441 | K0346 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0443 | K0347 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0444 | K0348 | f64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0445 | K0349 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0446 | K0350 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0447 | K0351 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0490 | K0352 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0496 | K0353 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0501 | K0354 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0520 | K0355 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0521 | K0356 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0668 | K0357 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0597 | K0358 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0604 | K0359 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0611 | K0360 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0632 | K0361 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0525 | K0362 | i32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0532 | K0363 | i64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0539 | K0364 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0560 | K0365 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0596 | K0366 | bool,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0379 | K0670 | u64,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0379 | K0671 | u64,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0382 | K0674 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0382 | K0899 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0388 | K0675 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0388 | K0900 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0392 | K0676 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0392 | K0901 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0393 | K0677 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0393 | K0902 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0394 | K0678 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0394 | K0903 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0395 | K0679 | u64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0395 | K0904 | u64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0396 | K0680 | u64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0396 | K0905 | u64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0397 | K0681 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0397 | K0906 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0398 | K0672 | f32,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0398 | K0682 | f32,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0401 | K0683 | f32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0401 | K0907 | f32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0407 | K0684 | f64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0407 | K0908 | f64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0413 | K0685 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0413 | K0909 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0414 | K0686 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0414 | K0910 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0415 | K0687 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0415 | K0911 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0418 | K0688 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0418 | K0912 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0424 | K0689 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0424 | K0913 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0428 | K0690 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0428 | K0914 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0429 | K0691 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0429 | K0915 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0430 | K0692 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0430 | K0916 | u64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0431 | K0693 | u64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0431 | K0917 | u64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0432 | K0694 | u64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0432 | K0918 | u64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0433 | K0695 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0433 | K0919 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0436 | K0696 | f32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0436 | K0920 | f32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0442 | K0697 | f64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0442 | K0921 | f64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0448 | K0698 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0448 | K0922 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0449 | K0699 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0449 | K0923 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0450 | K0700 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0450 | K0924 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0451 | K0673 | f64,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0451 | K0701 | f64,None | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0454 | K0702 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0455 | K0703 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0456 | K0704 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0457 | K0705 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0458 | K0706 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0459 | K0707 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0461 | K0708 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0462 | K0709 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0463 | K0710 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0464 | K0711 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0465 | K0712 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0466 | K0713 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0470 | K0716 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0471 | K0717 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0472 | K0718 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0475 | K0720 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0476 | K0721 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0477 | K0722 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0478 | K0723 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0480 | K0725 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0482 | K0726 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0483 | K0727 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0484 | K0728 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0485 | K0729 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0486 | K0730 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0487 | K0731 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0492 | K0732 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0492 | K0925 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0493 | K0733 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0493 | K0926 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0494 | K0734 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0494 | K0927 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0495 | K0735 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0495 | K0928 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0498 | K0736 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0498 | K0929 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0499 | K0737 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0499 | K0930 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0500 | K0738 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0500 | K0931 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0502 | K0739 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0502 | K0932 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0503 | K0740 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0503 | K0933 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0507 | K0743 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0507 | K0936 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0508 | K0744 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0508 | K0937 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0509 | K0745 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0509 | K0938 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0512 | K0747 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0512 | K0940 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0513 | K0748 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0513 | K0941 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0514 | K0749 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0514 | K0942 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0515 | K0750 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0515 | K0943 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0517 | K0752 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0517 | K0945 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0519 | K0753 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0519 | K0946 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0522 | K0754 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0522 | K0947 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0523 | K0755 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0523 | K0948 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0524 | K0669 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0524 | K0756 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0526 | K0757 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0527 | K0758 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0528 | K0759 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0529 | K0760 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0530 | K0761 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0531 | K0762 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0533 | K0763 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0534 | K0764 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0535 | K0765 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0536 | K0766 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0537 | K0767 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0538 | K0768 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0542 | K0771 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0543 | K0772 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0544 | K0773 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0547 | K0775 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0548 | K0776 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0549 | K0777 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0550 | K0778 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0552 | K0780 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0554 | K0781 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0555 | K0782 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0556 | K0783 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0557 | K0784 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0558 | K0785 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0559 | K0786 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0562 | K0787 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0563 | K0788 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0564 | K0789 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0565 | K0790 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0566 | K0791 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0567 | K0792 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0569 | K0793 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0570 | K0794 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0571 | K0795 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0572 | K0796 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0573 | K0797 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0574 | K0798 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0578 | K0801 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0579 | K0802 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0580 | K0803 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0583 | K0805 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0584 | K0806 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0585 | K0807 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0586 | K0808 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0588 | K0810 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0590 | K0811 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0591 | K0812 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0592 | K0813 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0593 | K0814 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0594 | K0815 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0595 | K0816 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0598 | K0817 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0599 | K0818 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0600 | K0819 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0601 | K0820 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0602 | K0821 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0603 | K0822 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0605 | K0823 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0606 | K0824 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0607 | K0825 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0608 | K0826 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0609 | K0827 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0610 | K0828 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0614 | K0831 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0615 | K0832 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0616 | K0833 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0619 | K0835 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0620 | K0836 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0621 | K0837 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0622 | K0838 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0624 | K0840 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0626 | K0841 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0627 | K0842 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0628 | K0843 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0629 | K0844 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0630 | K0845 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0631 | K0846 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0634 | K0847 | i32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0635 | K0848 | i32,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0636 | K0849 | i32,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0637 | K0850 | i32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0638 | K0851 | i32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0639 | K0852 | i64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0641 | K0853 | i64,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0642 | K0854 | i64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0643 | K0855 | i64,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0644 | K0856 | i64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0645 | K0857 | u64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0646 | K0858 | u64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0650 | K0861 | u64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0651 | K0862 | f32,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0652 | K0863 | f32,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0655 | K0865 | f32,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0656 | K0866 | f32,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0657 | K0867 | f64,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0658 | K0868 | f64,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0660 | K0870 | f64,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0662 | K0871 | f64,bool | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0663 | K0872 | bool,i32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0664 | K0873 | bool,i64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0665 | K0874 | bool,u64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0666 | K0875 | bool,f32 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
| K0667 | K0876 | bool,f64 | `i32` | `bool` | low-8 (8 bits) | movzbl %al, %eax |
