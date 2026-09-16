# emulations — every RISC-V float arch-opcode as ordinary integer source

Made 2026-09-16, from `../flattened/`.

## What these are

A float arch-opcode has no definition in Lean, Rocq, Isabelle or SMT: Sail
declares all 67 external with no body. Berkeley SoftFloat, vendored inside the
Sail model's own tree, implements them in pure integer C, and the C simulator
links it. `../flattened/` holds each of those 67, for each rounding mode, cut
down to ONE basic block of pure arithmetic — no branches, no calls, no memory.

This folder is that block turned back into SOURCE, in four languages:

| | |
|---|---|
| operations | 67 |
| rounding mode | 1 (`softfloat_round_minMag`, RISC-V `RTZ`) |
| variant | `value` (the returned bits; the exception flags are a separate slice) |
| languages | `c/` `cpp/` `rust/` `go/` — one file per operation |
| lines of source | 10,617 c · 10,885 c++ · 10,617 rust · 10,550 go |

Each file is a single function of straight-line `const` bindings, one per LLVM
instruction, using nothing but `and or xor add sub mul udiv shl lshr`, the
width casts `sext zext trunc`, `icmp`, and eight helpers. A float arch-opcode
is emulated by ordinary integer operators, in each language, with no floating
point instruction anywhere in it.

```
c/f16_add.c        uint64_t f16_add_rm1(uint64_t, uint64_t)
cpp/f16_add.cpp    sfemul::f16_add_rm1
rust/f16_add.rs    sfemul::f16_add::f16_add_rm1
go/f16_add.go      emul.Emu_f16_add_rm1
```

The helpers live once per language: `c/sfemul.h`, `cpp/sfemul.hpp`,
`rust/helpers.rs`, `go/helpers.go`. `c/sfemul_decls.h`, `cpp/sfemul_decls.hpp`,
`rust/lib.rs` and `go/go.mod` are the generated module wiring.

## These are TESTED, not PROVED

Nothing here is a proof and no prover has seen it. Correctness is established
by differential testing against Berkeley SoftFloat's own C, built here from the
copy at `sail-riscv/dependencies/softfloat/berkeley-softfloat-3`, with the
model's own defines and the `source/RISCV` specialisation, wrapped so each call
sets `softfloat_roundingMode = 1` and passes `exact = true` for the twelve
float-to-integer conversions — exactly what `c_emulator/riscv_softfloat.cpp`
does.

| | |
|---|---|
| inputs per (operation, language) | 302,500 typical, 425,000 for the `mulAdd` family |
| total per language | **20,544,314** |
| total, all four | **82,177,256** |
| **mismatches** | **0** |

Inputs are every edge case per operand — ±0, ±inf, quiet and signalling NaN,
largest and smallest normal, largest and smallest subnormal, ±1, ±2, ±0.5, and
one ulp either side of each — crossed over every operand, plus 200,000 uniform
random bit patterns per operand, plus 100,000 with the exponent banded around
the bias so subnormals, the rounding path and overflow are actually reached.
All four languages draw the identical sequence: the same xorshift64 from the
same seed, in the same order.

c and c++ call the SoftFloat wrapper directly, rust through `extern "C"`, go
through cgo. Every comparison is in-process and bit-exact on the returned
value.

**The test discriminates.** Running the same four binaries against an oracle at
rounding mode 0 instead of 1 produces 115,378 mismatches out of 645,314 in
every language.

## The three don't-cares, and why they cannot be seen

The flattened block speculates: it evaluates both arms of what used to be a
branch and masks the loser away. So it contains shifts whose amount can exceed
the operand width, a `ctlz` whose operand can be zero, and a `udiv` whose
divisor the flattener has already forced non-zero. LLVM calls all three poison
and puts a `freeze` on each — arbitrary but fixed. This emitter pins them:

| | pinned to | why |
|---|---|---|
| shift amount ≥ width | the amount modulo the width | what x86 and RISC-V hardware do, and what rust's `wrapping_shl` does; go is masked explicitly because go's own `>>` yields 0 |
| `llvm.ctlz(0)` | the bit width | the flattener's own `range(i32 0, 33)` annotation already admits 32 |
| `udiv` by zero | zero | never fires — `flattened.json: guarded_instructions` records the forced divisor — but rust and go panic rather than trap |
| `freeze` | a plain copy | it exists only to block poison and has no runtime meaning |

`scripts/pin_probe.sh` re-emits the C with the **opposite** reading of all
three (over-wide shift → 0, `ctlz(0)` → 0, `udiv` by zero → all ones) and runs
the same 20,544,314 inputs: **0 mismatches**. The pins are unobservable, not
lucky.

## The eight intrinsic helpers

A language's built-in is used only where its edge case is LLVM's.

| intrinsic | c | c++ | rust | go |
|---|---|---|---|---|
| `llvm.ctlz.i32/i64` | written out | `std::countl_zero` | `leading_zeros` | `math/bits.LeadingZeros32/64` |
| `llvm.abs.i16/i32/i64` | written out | written out | `wrapping_abs` | written out |
| `llvm.usub.sat.i8/i16` | written out | written out | `saturating_sub` | written out |
| `llvm.fshl.i64` | written out | written out | written out | written out |

- **ctlz** — every built-in used returns the bit width for 0, which is LLVM's
  `ctlz` with `is_zero_poison=false`. C's `__builtin_clz(0)` is undefined, so C
  is written out.
- **abs** — `llvm.abs` wraps at INT_MIN. rust's `wrapping_abs` is exactly that;
  rust's `abs` would panic. C's `abs()` is int-only and undefined at INT_MIN,
  C++'s `std::abs` likewise, and go has no integer abs at all.
- **usub.sat** — rust's unsigned `saturating_sub` is exactly `llvm.usub.sat`.
  C, C++ (before C++26) and go have no saturating subtract.
- **fshl** — no language of the four has a funnel shift; `rotl` / `RotateLeft`
  is only the degenerate `a == b` case.

## i128, and what go does instead

`i128` appears in exactly **two** of the 67 operations at this rounding mode:
**`f64_mul`** and **`f64_mulAdd`**, both for the 64×64 → 128 significand
product. c, c++ and rust use their native 128-bit integer (`unsigned __int128`,
`u128`). Go has none, so `go/helpers.go` carries a `U128 {Hi, Lo uint64}` pair
and the five operations the corpus actually reaches:

| LLVM | go |
|---|---|
| `zext i64 → i128` | `U128{0, x}` |
| `mul i128` | `u128Mul` — `bits.Mul64` for the low product, plus the two cross terms into the high half |
| `lshr i128, 64` | `u128Lshr` — amount masked to 127, three cases (0, <64, ≥64) |
| `trunc i128 → i64` | `u128Lo64` — the `Lo` half |
| `icmp slt i128 x, 0` | `u128Scmp` — signed on `Hi`, unsigned on `Lo` |

`helpers.go` also carries `and or xor add sub shl udiv`, the widening and
narrowing casts, and both comparisons, so a later rounding mode or the `flags`
variant needs no new 128-bit code.

## Re-running the test

```sh
cd Research/oracle/riscv/softfloat_slices

# re-emit all four languages from the flattened IR (rounding mode 1, value)
python3 scripts/emit_emulations.py 1 value

# build SoftFloat, build the four harnesses, run them
python3 scripts/verify_emulations.py 1

# merge the verdict into emulations.json and print the family table
python3 scripts/report_emulations.py

# optional: are the poison pins observable?  (expect 0 mismatches)
bash scripts/pin_probe.sh 1
```

`verify_emulations.py` reads `NRAND` and `NBAND` from the environment for a
quicker pass, and `EMUL_SCRATCH` for where to build. Everything it writes goes
to the scratch directory; `SOURCES` is read-only throughout.

Toolchains this was run on: clang 21.1.8, rustc 1.96.1, go 1.26.0, all on
x86-64. This is emulation testing, not lowering, so nothing is cross-compiled.

## Files

| | |
|---|---|
| `c/` `cpp/` `rust/` `go/` | one source file per operation, plus the helpers and the module wiring |
| `emulations.json` | per (operation, language): lines, LLVM opcodes and intrinsics used, integer widths, inputs tested, mismatches, whether i128 splitting was needed |
| `_emitted.json`, `_index.json` | the emitter's own records, read by the test harness |

## What these are NOT

They are not proofs. Nothing here has been checked against Sail's own
definition of the instruction — only against the SoftFloat implementation the
simulator already links. Proving one equal to its Sail definition is a separate
step and none has been done. The `flags` variant and rounding modes 0, 2, 3 and
4 are emitted by the same script but have not been run.
