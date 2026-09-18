# log 300 — template status, 2026-09-17

*notes:*

* denominator is the template's 1038; my own expansion of the 354 `execute_*`
  clauses by their dispatch enums gives 1090, so percentages carry ±5%

### 0. Basic Numbers

Number of RISCV arch-opcodes: 1038

Number of GMP primitives: 23

Number of c arch-units: 610

Number of cpp arch-units: 770

Number of rust arch-units: 125

Number of go arch-units: 107

### 1.1 Sail to Lean

Complete: 34% (353 of 1038 arch_opcodes)

*notes:*

- 353 RISCV arch-opcodes are full-body Lean expressions via Sail model
- 0 RISCV arch-opcodes are body-full Lean expressions via GMP slicing
- 685 RISCV arch-opcodes are body-less Lean expressions

| body-less, by cause | arch-opcodes | reachable? |
|---|---|---|
| vector, dynamic SEW (`get_sew`, `get_start_element`) | 262 | never |
| `match merge_var with` | 218 | yes — splitter built, see below |
| rounding mode read from `fcsr` | 90 | yes |
| not in the strip record | 70 | unmeasured |
| `assert` on xlen/width | 21 | never |
| the body is the retire | 11 | nothing to express |
| scattered singletons (CSR, traps, barriers, memory) | 13 | mixed |

- 308 of the 685 are reachable with machinery that exists
- ceiling without new theory: 661 of 1038 = 64%

### 1.2 GMP Slice Insertion

Complete: 0% (0 of 1038 arch_opcode_leans)

*notes:*

- 15 of 23 GMP slices have body-full Lean expressions
- 15 of 15 walked produced a body; 8 never walked, now running (`lp3_l122`)
- 0 inserted into any arch-opcode
  - the opaque name is `riscv_f32Eq` / `riscv_f64Add`, not `f32_eq` / `f64_add`
  - each returns `(fflags, value)`; the walked slices are value-only
  - the flags variant is flattened and unwalked

| slice | insts | body | also certified |
|---|---|---|---|
| f64_eq | 25 | yes | yes |
| f32_eq | 26 | yes | |
| f64_le | 34 | yes | yes |
| f64_lt | 35 | yes | yes |
| f32_le | 38 | yes | yes |
| f32_lt | 39 | yes | |
| ui32_to_f64 | 43 | yes | |
| i32_to_f64 | 49 | yes | |
| ui32_to_f32 | 84 | yes | |
| i32_to_f32 | 88 | yes | |
| f32_to_f64 | 97 | yes | yes |
| ui64_to_f64 | 98 | yes | |
| i64_to_f64 | 100 | yes | |
| ui64_to_f32 | 102 | yes | |
| i64_to_f32 | 105 | yes | |
| f32_mul, f32_div, f64_mul, f64_div | 283–345 | running | |
| f32_add, f32_sub, f64_add, f64_sub | 644–712 | running | |

- certification failures are `(kernel) deep recursion`, not missing bodies
- `i64_to_f32`'s body is 1,915,374 characters

### 2. compiler-operators lowered to arch-units, in Lean

Complete: partial

| | |
|---|---|
| `lower()` | 1,312 arch-units, riscv64, c/cpp/rust/go |
| `build_unit_lean()` | 164 of 186 integer class representatives certified |
| not reached | 51 classes — the walk refuses a branch or a call |
| float layer | 144 classes — decoder returns ILLEGAL |
| `discover_kinds()` | `leanpath/kinds.py` present |

### 3. the primitives

Complete: 0%

*notes:*

- `pieces_of()` exists as an inventory: 459 primitives, 392 atoms, gate netlists
- `arch_unit_lean_primitives` per language: does not exist

### 4. arch-opcodes emulated in every language

Complete: artifacts yes, the specified proof no

*notes:*

- 34 integer arch-opcodes + 67 float ops emulated in 8 languages, bit-exact
- built without step 3's table
- proof held is `arch_unit ≡ emulation` (542 arch-units), not
  `prove_lean_equivalence(definition, arch_unit.lean)`

### 5. cross-language arch-unit equivalence

Complete: 276 classes / 979 arch-units related; 0 proved

| pair | arch-units |
|---|---|
| c ↔ cpp | 880 |
| cpp ↔ rust | 303 |
| c ↔ rust | 204 |

*notes:*

- relation is identical body + arrival shape, not `prove_lean_equivalence`
- 83 semantic merges owed as lemmas
- go shares no class: its codegen differs

### work done 2026-09-17

`strip.merge_var_arms` — a third arm shape, distinct from UTYPE's:

```
let merge_var := (arg0, arg1, arg2)
match merge_var with
| (rs1, rd, .FCLASS_S) => (do … own write … own retire)
| (rs1, rd, .FMV_X_W)  => (do … own write … own retire)
```

| | |
|---|---|
| clauses split | 15 of 16 (`execute_WRS` is a different shape) |
| arms extracted | 56 |
| arms usable | 0 |

- refusals are no longer "a shape the rule does not know"

| arm refusal | arms |
|---|---|
| `rF_or_X_D` — float register read | 10 |
| `rF_or_X_H` — float register read | 10 |
| `rF_or_X_S` — float register read | 9 |
| `match (← select_instr_or_fcsr_rm rm)` | 6 |
| `assert (xlen ≥b 64)` | 7 |
| `feature_enabled_for_priv` | 2 |
| effect in the written value / pure-wrapped let | 2 |

- 29 of 56 wait on one addition: the rule knows `rX_bits`, not `rF_or_X_*`
- 6 more are the rounding-mode select — same item as the 90 above

*defects hit, recorded:*

- `MERGE_LET` and `TUPLE_LET` already exist in `strip.py` with different
  capture groups; collided with both
- `elements()` takes a list of lines, not a string

### next

1. float register reads (`rF_or_X_S/D/H`) in the rule — 29 arms, one addition
   for all three widths
2. pin the rounding mode — the 90, plus 6 of the arms above
3. rm0 slice insertion — 18 externals left, blocked on kernel recursion depth
