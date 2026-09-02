# Differential test suite: Rust `cranelift-assembler-x64` vs transpiled `pc_vocab`

Everything in this directory is self-contained; nothing outside
`Research/vocab_transpiler/differential/` was modified to build it.

## What this is

Two independent generators build "the same instruction" from the same field
values and compare the emitted machine code byte-for-byte:

- **Rust side**: a generated Cargo project (`harness/`) that links the real
  `cranelift-assembler-x64 = "0.134.2"` crate from crates.io and calls its
  actual `encode()` — this is ground truth, not a re-implementation.
- **Python side**: `pc_vocab`, the mechanically transpiled vocabulary, driven
  through `vocab_support.py`.

`common_operands.py` parses `assembler.rs` once and is imported by both
`gen_rust_harness.py` and `run_python_side.py`, so the two sides are
guaranteed to pick identical register/immediate values for every
`(instruction, operand key)` pair. There are two operand keys per
instruction: `low` (RAX/RSI/RDX/... register choices, no REX.B needed) and
`r14` (R14/R15/... register choices, forces REX.B/.R/.X on every
register-carrying field).

## Files

- `common_operands.py` — parses `assembler.rs`, classifies each instruction's
  constructor fields, and builds the two operand-key value assignments.
  Imported by both generators below.
- `gen_rust_harness.py` — writes `harness/src/main.rs` + `harness/Cargo.toml`.
  Also writes `SKIPPED_RUST.txt` (instructions it could not construct) and
  prints a coverage report to stdout.
- `run_python_side.py` — drives `pc_vocab` with the same instructions/keys,
  prints `NAME|key|hexbytes`, `NAME|key|CUT|reason`, or
  `NAME|key|ERROR|reason` per line, one per `(instruction, key)` attempted.
- `compare.py` — matches `harness_out.txt` (Rust) against `python_out.txt`
  (Python) by `(name, key)` and writes `report.txt`. Exits nonzero only on an
  actual byte mismatch (SKIP/CUT/ERROR/one-sided presence are coverage gaps,
  not failures).
- `run.sh` — orchestrates the above. See "How to run it" below.
- `harness/` — the generated Rust project (`src/main.rs`, `Cargo.toml`).
- `SKIPPED_RUST.txt` — instructions `gen_rust_harness.py` could not build a
  Rust constructor for, with reasons.
- `python_out.txt` — the actual output of `run_python_side.py`, generated and
  committed in this sandbox (see results below).
- `report.txt` — the actual output of `compare.py` against that
  `python_out.txt` (no `harness_out.txt` exists yet in this sandbox — see
  "Status of the Rust side" below).

## How to run it

### Python-only mode (what was actually run in this sandbox — no `cargo` here)

```sh
cd Research/vocab_transpiler/differential
./run.sh --python-only
```

This regenerates `harness/` (harmless, cargo not invoked), regenerates
`python_out.txt`, and runs `compare.py` against whatever `harness_out.txt`
currently exists (none, in this sandbox, so the report shows 0 Rust lines
and reports every Python line as "Python-only").

### Full mode (needs a Rust toolchain — has NOT been done here)

```sh
cd Research/vocab_transpiler/differential
./run.sh
```

This additionally requires `cargo` on `PATH`. If it's missing, `run.sh`
prints a loud error and exits nonzero instead of silently skipping the Rust
side. Full mode:
1. `gen_rust_harness.py` → `harness/src/main.rs`, `harness/Cargo.toml`,
   `SKIPPED_RUST.txt`
2. `cd harness && cargo run --release > ../harness_out.txt`
3. `run_python_side.py > python_out.txt`
4. `compare.py` → `report.txt` (nonzero exit iff there's a byte mismatch)

## IMPORTANT — status of the Rust side: NOT YET VERIFIED

**The Rust harness (`harness/src/main.rs`) has been generated but has NOT
been compiled or run in this sandbox — there is no `cargo` / Rust toolchain
available here.** It has therefore not been checked for compile errors,
correct crate API usage, or correct output. `harness_out.txt` does not exist
in this checkout; `report.txt` here only reflects the Python side's internal
coverage (CUT/ERROR breakdown), not an actual Rust-vs-Python byte comparison.

**Someone with a Rust toolchain — per team convention, "the owner" — needs to run
`./run.sh` (full mode) to actually execute the differential comparison.**
Until that happens, "PASS (no byte mismatches)" in `report.txt` is true only
in the vacuous sense that zero pairs were compared, not evidence that the
transpiler is correct.

Things the owner should sanity-check on first run:
- Does `inst::NAME::<Regs>::new(...)` / `inst::NAME::new(...)` compile as
  generated? The call shape was confirmed against the doc-example in the
  vendored crate's `lib.rs` (`inst::andb_i::new(Fixed(rax), Imm8::new(...))`)
  and against the vendored source of `Gpr`, `GprMem`, `Xmm`, `XmmMem`,
  `Fixed`, `Imm8/16/32/64`, `Simm8/32` (all of which implement `From<u8>` /
  `From<iN>` so a bare integer literal satisfies each `impl Into<...>`
  constructor parameter) — but it was never fed through `rustc`.
  `Vec<u8>` implements `CodeSink` directly in the vendored crate
  (`api.rs`), so `harness/src/main.rs` uses that instead of a hand-rolled
  sink.
- `TrapCode(core::num::NonZeroU8::new(1).unwrap())` — used for the 8
  `div*_m`/`idiv*_m` instructions that take an explicit `trap` field; this
  value is never read on the register-only path we exercise (no `Amode`
  operands are ever constructed), so its exact value shouldn't matter, but
  worth eyeballing.

## Results actually observed in this sandbox (Python side only)

From `gen_rust_harness.py`'s coverage report (field-classification only —
no Rust was compiled):

```
total instructions in assembler.rs : 1071
handled (Rust constructor emitted) : 973  (90.8%)
skipped                            : 98   (9.2%)
operand-key lines emitted          : 1946 (973 instrs x 2 keys)
```

From actually running `run_python_side.py` against the real `pc_vocab`
(`python_out.txt`, 1946 lines, one per attempted `(instruction, key)` pair):

```
instructions attempted    : 973 (of 1071 total; 98 skipped, Amode-only, identically on both sides)
lines printed             : 1946
clean encodes             : 1328
CUT (NotImplementedError) : 618
ERROR (other exception)   : 0
missing from pc_vocab     : 0
```

`run_python_side.py` exits 0 and produced exactly one line per attempted
pair — it did not crash.

All 618 CUTs are the same message:

```
VEX/EVEX prefix encoding not cut (SIMD path). Invariant 'no AVX instruction is reached' has been violated.
```

i.e. every `v*` (AVX/VEX) instruction plus a handful of legacy instructions
that happen to route through the same VEX/EVEX prefix code path
(`vocab_support.py`'s `_CutPrefix`). This is an intentional, documented cut
in the transpiler support layer, not a bug: the docstring in
`vocab_support.py` states outright that VEX/EVEX is unreached by the current
GPR-integer vocabulary and raises loudly instead of guessing. 0 instructions
produced an unexpected `ERROR`.

Because `harness_out.txt` doesn't exist here, `compare.py`'s `report.txt`
currently shows 0 pairs actually compared for byte-equality; all 1328 clean
Python encodes show up as "Python-only" and all 618 CUTs are reported as
Python-side CUTs. This is expected and will resolve once the owner runs the full
pipeline with `cargo`.

## Suspected transpiler bugs

None found. Every non-AVX, non-Amode instruction that `pc_vocab` was asked
to build encoded without raising, and the VEX/EVEX cut is a documented,
intentional invariant rather than a bug. (We were not able to verify these
bytes are *correct* — only that they were produced — since the Rust side has
not been run; see above.) If the owner's `cargo run` turns up byte mismatches,
please record them here rather than editing `pc_vocab/` or
`vocab_support.py` — this file's job is only to observe.

## Known limitations / uncovered instruction classes

1. **98 pure-memory-operand ("Amode-only") instructions are skipped
   entirely, on both sides.** These are the `lock_*` read-modify-write
   forms (e.g. `lock_addb_mi`, `lock_xaddq_mr`, `lock_cmpxchg16b_m`) whose
   `new()` constructor takes a bare `Amode<R>` field (`m8`/`m16`/`m32`/
   `m64`/`m128`) with no register-operand fallback (unlike `GprMem`/
   `XmmMem`, which can always be built as a register). Building a
   real `Amode` (base register + displacement + optional index/scale, or a
   RIP-relative target) is possible in the Rust crate but `vocab_support.py`
   explicitly treats the `Mem`/`GprMem::Mem` path as an un-transpiled cut
   ("REACHABILITY INVARIANT: ... unreachable while every caller constructs
   register operands"), so generating a Rust-only Amode encoding would only
   ever produce a one-sided (Rust-only) test with no way to compare bytes.
   These 98 are listed with reasons in `SKIPPED_RUST.txt`.
2. **VEX/EVEX (`v*`) instructions all CUT on the Python side** (618 of the
   1946 attempted pairs) because `vocab_support.py`'s VEX/EVEX prefix
   builders are intentional stubs that raise `NotImplementedError`. The Rust
   harness *can* build and encode these (they're ordinary `Xmm`/`XmmMem`/
   `Imm8` constructors, no `Amode` involved), so once the owner runs the full
   pipeline, `harness_out.txt` will have real bytes for these while
   `python_out.txt` will show `CUT` — `compare.py` correctly reports these
   as coverage gaps, not mismatches.
3. **No genuine memory-addressing coverage.** Even for instructions whose
   `rm`/`xmm_m` operand is a `GprMem`/`XmmMem` (i.e. *could* be a real
   memory reference), this harness always picks the register arm. Testing
   the actual `Amode` encoding paths (ModRM+SIB+displacement, RIP-relative)
   is out of scope here, consistent with `vocab_support.py`'s own
   reachability invariant.
4. **Only two operand keys per instruction** (`low`, `r14`); this is enough
   to exercise the REX-prefix computation (REX.B/.R/.X) on every
   register-carrying field but does not attempt to independently vary each
   field, alias registers together, or sweep the full 0..15 encoding space
   per field, nor try boundary/negative immediates (e.g. negative `Simm8`,
   `Simm32`, sign-extension edge cases) or the "special" 8-bit registers
   (AH/BH/CH/DH — encodings 4-7 without REX, which the crate's
   `is_special_if_8bit` logic treats specially — this differential harness
   never separately drives an 8-bit-operand instruction with encodings 4-7
   *without* a REX prefix already forced by another field, so that
   particular interaction is not directly exercised here).
5. **8 `div*_m`/`idiv*_m` instructions carry an explicit `TrapCode` field**;
   its value doesn't affect the encoded bytes on the register-only path we
   exercise (it's only read for `Amode`/memory operands, which we never
   build), so a fixed placeholder value is used on both sides. This is a
   deliberate simplification, not a gap in coverage of the encoding itself.
6. **9 `nop_Nb` + `nop_zo` custom-encoded instructions** are included and
   *do* work (they have trivial `new()` with 0 fields, handled fine by
   `common_operands.py`) — this is not a limitation, noted here only because
   they looked unusual during parsing (they call
   `crate::custom::encode::nop_Nb` internally instead of the generated
   REX/ModRM machinery).

## Team convention

Per team convention, the person running the Rust-toolchain-dependent parts
of this suite is referred to as **the owner**.
