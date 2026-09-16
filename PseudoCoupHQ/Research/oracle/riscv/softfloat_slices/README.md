# softfloat_slices — RISC-V float arch-opcodes as integer-only machine code

Made 2026-09-16. Recorded in `DevComms/log_293_below_sail_gmp_softfloat_and_the_float_gap_sized.md`.

## What is here

Berkeley SoftFloat, vendored in the Sail model's own tree at
`SOURCES/sail-riscv/dependencies/softfloat/berkeley-softfloat-3/`,
implements every RISC-V float instruction in pure integer C. It is what
the Sail C simulator links, and it is the only complete definition of
those instructions anywhere in the line: Sail declares them external
with no body in any backend, so the Lean, Rocq, Isabelle and SMT
outputs all have the same hole.

Each of the 67 float operations the model declares was compiled for
riscv64, linked with its transitive helpers, internalised so only that
operation survives, then inlined and dead-code eliminated. The result
is ONE function per operation, in RISC-V base plus M instructions, with
no floating-point instruction in it.

| folder | what |
|---|---|
| `generic/` | one slice per operation, cut without the caller's context |
| `specialised/` | one slice per (operation, rounding mode), cut inside the context Sail fixes |
| `measurements/` | the per-operation numbers, and the Sail primitive inventory |
| `scripts/` | the slicers and the measurement code |

## The context that matters

Sail does not call these generically. `c_emulator/riscv_softfloat.cpp`
fixes the state first:

```c
void softfloat_init(uint64_t rm) {
  softfloat_exceptionFlags = 0;
  softfloat_roundingMode = uint8_of_rm(rm);
}
```

and the twelve float-to-integer conversions pass a literal `true` for
`exact`. Slicing inside that context is what `specialised/` holds, and
it is 15% smaller than generic: 8,160 instructions against 9,648.

## What the slices are

| | |
|---|---|
| operations | 67 |
| total, best rounding mode each | 8,160 instructions |
| total, keeping all five modes | 38,762 |
| largest | `f64_mulAdd` |
| natural loops | **zero**, dominator-checked over 650 builds |
| indirect jumps | **zero** in every specialised slice |
| calls remaining | only the six add/sub, and none at rounding mode 1 |

Zero loops is the load-bearing fact: it means every float instruction is
a fixed expression, so nothing here needs an induction proof.

## Reproducing

`scripts/slice_specialised.py`. The toolchain is clang 21 and the LLVM
tools at `/usr/lib/llvm-21/bin`. Two traps are recorded in the script:
linking SoftFloat's unmodified `softfloat_state.c` silently folds its
`near_even` initialiser and turns a "generic" slice into the mode-0
slice; and `f64_sqrt` needs `instcombine<no-verify-fixpoint>` because
this LLVM build asserts that pass converges in one iteration.

## What these are NOT

They are not proofs and nothing here has been checked against Sail's own
definition of the instruction. They are the emulation, in machine code,
taken from the implementation the simulator already trusts. Proving one
equal to its Sail definition is a separate step and none has been done.
