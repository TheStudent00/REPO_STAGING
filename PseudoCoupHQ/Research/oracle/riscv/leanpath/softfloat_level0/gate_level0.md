# level 0: the Lean bodies against Sail's softfloat

| operations | points | agree | disagree | misaligned lines | unknown lines |
|---|---|---|---|---|---|
| 27 | 16875 | 16833 | 42 | 0 | 0 |

| operation | width | points (edge, random) | agree | result differs | flags differ | both differ | modes with a disagreement |
|---|---|---|---|---|---|---|---|
| riscv_f16Add | 16 | 1125 (1125, 0) | 1125 | 0 | 0 | 0 | none |
| riscv_f16Div | 16 | 1125 (1125, 0) | 1115 | 0 | 10 | 0 | RNE 2, RTZ 2, RDN 2, RUP 2, RMM 2 |
| riscv_f16Eq | 16 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f16Le | 16 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f16Le_quiet | 16 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f16Lt | 16 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f16Lt_quiet | 16 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f16Mul | 16 | 1125 (1125, 0) | 1121 | 0 | 4 | 0 | RNE 2, RMM 2 |
| riscv_f16Sub | 16 | 1125 (1125, 0) | 1125 | 0 | 0 | 0 | none |
| riscv_f32Add | 32 | 1125 (1125, 0) | 1125 | 0 | 0 | 0 | none |
| riscv_f32Div | 32 | 1125 (1125, 0) | 1115 | 0 | 10 | 0 | RNE 2, RTZ 2, RDN 2, RUP 2, RMM 2 |
| riscv_f32Eq | 32 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f32Le | 32 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f32Le_quiet | 32 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f32Lt | 32 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f32Lt_quiet | 32 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f32Mul | 32 | 1125 (1125, 0) | 1121 | 0 | 4 | 0 | RNE 2, RMM 2 |
| riscv_f32Sub | 32 | 1125 (1125, 0) | 1125 | 0 | 0 | 0 | none |
| riscv_f64Add | 64 | 1125 (1125, 0) | 1125 | 0 | 0 | 0 | none |
| riscv_f64Div | 64 | 1125 (1125, 0) | 1115 | 0 | 10 | 0 | RNE 2, RTZ 2, RDN 2, RUP 2, RMM 2 |
| riscv_f64Eq | 64 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f64Le | 64 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f64Le_quiet | 64 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f64Lt | 64 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f64Lt_quiet | 64 | 225 (225, 0) | 225 | 0 | 0 | 0 | none |
| riscv_f64Mul | 64 | 1125 (1125, 0) | 1121 | 0 | 4 | 0 | RNE 2, RMM 2 |
| riscv_f64Sub | 64 | 1125 (1125, 0) | 1125 | 0 | 0 | 0 | none |

## disagreements by class

| operation | mode | a | b | part | flag bits differing | count |
|---|---|---|---|---|---|---|
| riscv_f64Mul | RMM | pos_normal | pos_normal | flags | UF | 2 |
| riscv_f64Mul | RNE | pos_normal | pos_normal | flags | UF | 2 |
| riscv_f16Div | RDN | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f16Div | RDN | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f16Div | RMM | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f16Div | RMM | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f16Div | RNE | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f16Div | RNE | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f16Div | RTZ | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f16Div | RTZ | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f16Div | RUP | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f16Div | RUP | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f16Mul | RMM | pos_normal | pos_subnormal | flags | UF | 1 |
| riscv_f16Mul | RMM | pos_subnormal | pos_normal | flags | UF | 1 |
| riscv_f16Mul | RNE | pos_normal | pos_subnormal | flags | UF | 1 |
| riscv_f16Mul | RNE | pos_subnormal | pos_normal | flags | UF | 1 |
| riscv_f32Div | RDN | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f32Div | RDN | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f32Div | RMM | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f32Div | RMM | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f32Div | RNE | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f32Div | RNE | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f32Div | RTZ | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f32Div | RTZ | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f32Div | RUP | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f32Div | RUP | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f32Mul | RMM | pos_normal | pos_subnormal | flags | UF | 1 |
| riscv_f32Mul | RMM | pos_subnormal | pos_normal | flags | UF | 1 |
| riscv_f32Mul | RNE | pos_normal | pos_subnormal | flags | UF | 1 |
| riscv_f32Mul | RNE | pos_subnormal | pos_normal | flags | UF | 1 |
| riscv_f64Div | RDN | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f64Div | RDN | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f64Div | RMM | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f64Div | RMM | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f64Div | RNE | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f64Div | RNE | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f64Div | RTZ | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f64Div | RTZ | pos_inf | pos_zero | flags | DZ | 1 |
| riscv_f64Div | RUP | pos_inf | neg_zero | flags | DZ | 1 |
| riscv_f64Div | RUP | pos_inf | pos_zero | flags | DZ | 1 |

## examples (first per operation)

| operation | mode | a | b | tag | softfloat flags | softfloat result | Lean flags | Lean result |
|---|---|---|---|---|---|---|---|---|
| riscv_f16Div | RNE | 7c00 | 0 | edge pos_inf pos_zero | none | 7c00 | DZ | 7c00 |
| riscv_f16Div | RNE | 7c00 | 8000 | edge pos_inf neg_zero | none | fc00 | DZ | fc00 |
| riscv_f16Div | RTZ | 7c00 | 0 | edge pos_inf pos_zero | none | 7c00 | DZ | 7c00 |
| riscv_f16Div | RTZ | 7c00 | 8000 | edge pos_inf neg_zero | none | fc00 | DZ | fc00 |
| riscv_f16Div | RDN | 7c00 | 0 | edge pos_inf pos_zero | none | 7c00 | DZ | 7c00 |
| riscv_f16Div | RDN | 7c00 | 8000 | edge pos_inf neg_zero | none | fc00 | DZ | fc00 |
| riscv_f16Div | RUP | 7c00 | 0 | edge pos_inf pos_zero | none | 7c00 | DZ | 7c00 |
| riscv_f16Div | RUP | 7c00 | 8000 | edge pos_inf neg_zero | none | fc00 | DZ | fc00 |
| riscv_f16Mul | RNE | 40c0 | 1af | edge tiny_boundary_a tiny_boundary_b | NX UF | 400 | NX | 400 |
| riscv_f16Mul | RNE | 1af | 40c0 | edge tiny_boundary_b tiny_boundary_a | NX UF | 400 | NX | 400 |
| riscv_f16Mul | RMM | 40c0 | 1af | edge tiny_boundary_a tiny_boundary_b | NX UF | 400 | NX | 400 |
| riscv_f16Mul | RMM | 1af | 40c0 | edge tiny_boundary_b tiny_boundary_a | NX UF | 400 | NX | 400 |
| riscv_f32Div | RNE | 7f800000 | 0 | edge pos_inf pos_zero | none | 7f800000 | DZ | 7f800000 |
| riscv_f32Div | RNE | 7f800000 | 80000000 | edge pos_inf neg_zero | none | ff800000 | DZ | ff800000 |
| riscv_f32Div | RTZ | 7f800000 | 0 | edge pos_inf pos_zero | none | 7f800000 | DZ | 7f800000 |
| riscv_f32Div | RTZ | 7f800000 | 80000000 | edge pos_inf neg_zero | none | ff800000 | DZ | ff800000 |
| riscv_f32Div | RDN | 7f800000 | 0 | edge pos_inf pos_zero | none | 7f800000 | DZ | 7f800000 |
| riscv_f32Div | RDN | 7f800000 | 80000000 | edge pos_inf neg_zero | none | ff800000 | DZ | ff800000 |
| riscv_f32Div | RUP | 7f800000 | 0 | edge pos_inf pos_zero | none | 7f800000 | DZ | 7f800000 |
| riscv_f32Div | RUP | 7f800000 | 80000000 | edge pos_inf neg_zero | none | ff800000 | DZ | ff800000 |
| riscv_f32Mul | RNE | 40940000 | 1bacf9 | edge tiny_boundary_a tiny_boundary_b | NX UF | 800000 | NX | 800000 |
| riscv_f32Mul | RNE | 1bacf9 | 40940000 | edge tiny_boundary_b tiny_boundary_a | NX UF | 800000 | NX | 800000 |
| riscv_f32Mul | RMM | 40940000 | 1bacf9 | edge tiny_boundary_a tiny_boundary_b | NX UF | 800000 | NX | 800000 |
| riscv_f32Mul | RMM | 1bacf9 | 40940000 | edge tiny_boundary_b tiny_boundary_a | NX UF | 800000 | NX | 800000 |
| riscv_f64Div | RNE | 7ff0000000000000 | 0 | edge pos_inf pos_zero | none | 7ff0000000000000 | DZ | 7ff0000000000000 |
| riscv_f64Div | RNE | 7ff0000000000000 | 8000000000000000 | edge pos_inf neg_zero | none | fff0000000000000 | DZ | fff0000000000000 |
| riscv_f64Div | RTZ | 7ff0000000000000 | 0 | edge pos_inf pos_zero | none | 7ff0000000000000 | DZ | 7ff0000000000000 |
| riscv_f64Div | RTZ | 7ff0000000000000 | 8000000000000000 | edge pos_inf neg_zero | none | fff0000000000000 | DZ | fff0000000000000 |
| riscv_f64Div | RDN | 7ff0000000000000 | 0 | edge pos_inf pos_zero | none | 7ff0000000000000 | DZ | 7ff0000000000000 |
| riscv_f64Div | RDN | 7ff0000000000000 | 8000000000000000 | edge pos_inf neg_zero | none | fff0000000000000 | DZ | fff0000000000000 |
| riscv_f64Div | RUP | 7ff0000000000000 | 0 | edge pos_inf pos_zero | none | 7ff0000000000000 | DZ | 7ff0000000000000 |
| riscv_f64Div | RUP | 7ff0000000000000 | 8000000000000000 | edge pos_inf neg_zero | none | fff0000000000000 | DZ | fff0000000000000 |
| riscv_f64Mul | RNE | 3fe4000000000000 | 19999999999999 | edge tiny_boundary_a tiny_boundary_b | NX UF | 10000000000000 | NX | 10000000000000 |
| riscv_f64Mul | RNE | 19999999999999 | 3fe4000000000000 | edge tiny_boundary_b tiny_boundary_a | NX UF | 10000000000000 | NX | 10000000000000 |
| riscv_f64Mul | RMM | 3fe4000000000000 | 19999999999999 | edge tiny_boundary_a tiny_boundary_b | NX UF | 10000000000000 | NX | 10000000000000 |
| riscv_f64Mul | RMM | 19999999999999 | 3fe4000000000000 | edge tiny_boundary_b tiny_boundary_a | NX UF | 10000000000000 | NX | 10000000000000 |
