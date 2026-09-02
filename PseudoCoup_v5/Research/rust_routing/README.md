# Rust Routing Insertion

Transpile rustc's ROUTING LOGIC into Python, so Python produces
Rust's IR opcodes and arch opcodes by running Rust's own code.
Design: [../../DevComms/dev_plan_log.md](../../DevComms/dev_plan_log.md)
(entry 2026-07-25).

## Components

| Component | File | Status |
|---|---|---|
| RustI64 cell | rust_cell.py | **done** — 8-byte aligned cell, border rules enforced |
| output ring (mount + call) | output_ring.py | **done** — mmap/mprotect/ctypes |
| output ring proof | test_output_ring.py | **ALL PASS** (see below) |
| slice 1: MIR routing | slice_mir_routing.py | **done** — cut from num.rs codegen_int_binop |
| slice 1 proof | test_slice_routing.py | **ALL PASS** — 14 routing cases + 4 refusals |
| slice 2: encoding | slice_encoder.py | **done** — cut from cranelift-assembler-x64 generated Rust |
| END TO END | test_end_to_end.py | **ALL PASS** — hub expr -> rust logic -> machine code -> executed |
| slice 1.5: ISLE lowering | slice_lowering.py | **done** — Sdiv/Srem/arith arms |
| input ring (Ledger as TyCtxt) | ledger.py | **done** |
| backend (assembles slices) | pc_backend.py | **done** — cached per (binop, type) |
| invocation ring (import hook) | pc_import.py + pc_runtime.py | **done** — .pc modules |
| hub module proof | test_hub_module.py + demo.pc | **ALL PASS** |
| subsequence check vs native compilers | test_subsequence.py | **ALL PASS** — 3 EXACT, 2 EQUIV |

## What the output-ring proof establishes

Run: `python3 test_output_ring.py`

- machine code written into a page at run-time and CALLED from
  stock CPython — the delivery mechanism for anything the
  transpiled encoder later produces
- Rust's TRUNCATING division observed through the real `idiv`
  instruction: `-7 / 2 = -3`, where Python's `//` gives `-4`.
  The class-1 divergence resolved by executing Rust's arch op,
  not by emulating it
- i64 wrap at max+1 — proof the value lives in a genuine 64-bit
  cell, not Python bigint
- border refusal: `RustI64 + 1` raises; crossings must be explicit
  (`int(x)`) — the class-1 lattice verdict, executable

Corollary: from here, correctness of the whole PoC reduces to
producing the right BYTES. Mounting is no longer a risk.

## Note on the stand-in bytes

test_output_ring.py hand-assembles `add` and `idiv` sequences.
These stand in for transpiled-encoder output ONLY to prove
mounting. No hand-written encoding survives into the real PoC —
the acceptance test is that Cranelift's own logic (transpiled)
produces these bytes.

## Slice 1 result

`codegen_int_binop` (num.rs:134) transpiled with three stand-ins
(CValue/Layout, InstBuilder-as-accumulator, FunctionCx). Verified
against rustc's own match arms: 14 routing cases correct, including
the sign-dependent flips (Div i64 -> sdiv, u64 -> udiv) — and it
refuses exactly what rustc refuses (compare binops, checked binops,
Offset, mismatched operand types).

The recorded accumulator output IS the "Dict that no compiler
stores": the mapping now exists as data because Rust's own routing
logic generated it, in Python.

## Chain confirmed from source

```
MIR BinOp::Div (signed)
  -> b.sdiv()                    num.rs:164
  -> CLIF Opcode::Sdiv           isle_x64.rs:16597
  -> repeat_sign_bit (cqo) + x64_idiv
  -> constructor_x64_idiv I64 -> idivq_m    isle_x64.rs:14222
  -> emit.rs -> bytes
```

which is the very `48 99 / 48 F7 FE` (cqo; idiv) sequence the output
ring already executes.

## END TO END RESULT (2026-07-25)

`python3 test_end_to_end.py`

```
routing   (Div, i64)          -> sdiv            slice 1
lowering  sdiv                -> cqto_zo, idivq_m   ISLE arm
encoding  cqto_zo             -> 48 99          slice 2
          idivq_m rsi         -> 48 f7 fe       slice 2
          idivq_m r14         -> 49 f7 fe       (REX.B path)
stub      48 89 f8 48 99 48 f7 fe c3
exec      -7 r./ 2 = -3   (Python's -7 // 2 = -4)
```

**The acceptance criterion is met**: the bytes the transpiled
encoder produced (`48 99`, `48 f7 fe`) are byte-identical to the
hand-verified sequence in test_output_ring.py — but nothing was
hand-written this time. Rust's own `encode()` logic, running in
Python, emitted them.

Full i64 grid passes including both extremes (i64::MAX, i64::MIN).

### What this establishes

A high-level hub expression was routed to Rust IR opcodes by Rust's
own routing logic, lowered to Rust's machine instructions, encoded
to x86-64 bytes by Rust's own encoder, mounted, and executed inside
a stock CPython process — with the result landing in a RustI64 cell.
No approximation at any step. The "Dict that no compiler stores"
now exists, generated on demand by the transpiled generator.

## THE HUB MODULE WORKS (2026-07-25)

`demo.pc` — real qualified spelling, stock CPython, no fork:

```python
a = r.i64(-7)
b = r.i64(2)
quotient  = a r./ b          # -3   (Python's -7 // 2 = -4)
remainder = a r.% b          # -1
chained   = (a r.* b) r./ b  # -7   stays Rust-side throughout
```

What the transpiled pipeline produced for it:

```
Div/i64   clif=sdiv  cqto_zo+idivq_m  48 89 f8 48 99 48 f7 fe c3
Rem/i64   clif=srem  cqto_zo+idivq_m  48 89 f8 48 99 48 f7 fe 48 89 d0 c3
Mul/i64   clif=imul  imulq_rm         48 89 f8 48 0f af c6 c3
```

Note Rem reuses the same instruction sequence as Div and differs
only by `mov rax, rdx` — because ISLE's Srem arm takes
`value_regs_get(.., 1)` (the remainder) where Sdiv takes 0. That
distinction came from Rust's lowering table, not from us.

### The rings, resolved

- **input ring**: `ledger.py` answers the TyCtxt question. Cells
  carry their own type; mismatched operands are refused with the
  same assertion rustc's codegen_int_binop makes.
- **invocation ring**: `pc_import.py` is a meta-path finder for
  `.pc` modules. It rewrites qualified spellings between file and
  compile (`a r./ b` -> `a |_r_div| b`), so surface syntax is real
  with ZERO parser surgery. Parser-level qualifiers remain the
  PCv6 question.
- **backend**: `pc_backend.py` caches per (binop, type) — routing
  and encoding run once, then it is a direct call into mounted code.

### Honesty markers — BOTH NOW CUT (2026-07-25, Phase 1.3)

`CheckedDivOrRemSeq` (emit.rs:215) is CUT. srem now emits the real
guard with computed displacements (two-pass label resolution, as a
MachBuffer does — no hand-written offset constants):

```
Rem/i64  48 89 f8  48 83 fe ff  75 04  33 d2  eb 05  48 99 48 f7 fe  48 89 d0  c3
         mov       cmp rsi,-1   jne+4  xor    jmp+5  cqto; idiv rsi   mov rax,rdx
```

`udiv`/`urem` are CUT, using `divq_m` taken from the MACHINE-
TRANSPILED `pc_vocab` (the 1328/1328-verified source) rather than
the hand slice.

```
Div/u64  48 89 f8 31 d2 48 f7 f6 c3           xor edx,edx; div rsi
Rem/u64  48 89 f8 31 d2 48 f7 f6 48 89 d0 c3
```

The guard applies to **signed** rem ONLY. An early version applied it
to urem too, which returned 0 for `urem(a, u64::MAX)` — because that
bit pattern reads as -1 when signed. The extended ground-truth grid
caught it immediately. Only `sdiv` still refuses an input:
`i64::MIN / -1`, which is a genuine overflow trap, not a guarded case.

Remaining cut: `Amode` (memory operands) and VEX/EVEX SIMD.

### Verification

`./verify_all.sh` runs all four test files and diffs an 81-row
arithmetic grid against native `rustc` output.

**HOST RUN 2026-07-25 — GROUND TRUTH CONFIRMED:**

```
===== test_output_ring.py     OUTPUT RING: ALL PASS
===== test_slice_routing.py   SLICE 1 ROUTING: ALL PASS
===== test_end_to_end.py      END TO END: ALL PASS
===== test_hub_module.py      HUB MODULE: ALL PASS
===== grid vs native rustc    PASS: 81 rows byte-identical to rustc
```

The transpiled pipeline's arithmetic — add, sub, mul, truncating
div, remainder, across all sign combinations and both i64 extremes —
is byte-identical to what `rustc -O` computes. Verified against the
compiler whose logic we extracted, not against our own reasoning.

## Does our code appear inside what a real compiler emits?

`python3 test_subsequence.py` — compiles the equivalent function
natively, disassembles, and searches for our generated stub body as
a contiguous sub-sequence. Result vs `gcc -O2`:

```
EXACT  Div  48 89 f8 48 99 48 f7 fe          verbatim inside gcc's d()
EXACT  Rem  48 89 f8 48 99 48 f7 fe 48 89 d0 verbatim inside gcc's r()
EXACT  Mul  48 89 f8 48 0f af c6             verbatim inside gcc's m()
EQUIV  Add  48 89 f8 48 03 c6                gcc used lea rax,[rdi+rsi]
EQUIV  Sub  48 89 f8 48 2b c6                gcc used 48 29 f0
```

Three are byte-identical sub-sequences; gcc's only additions are the
`endbr64` CET landing pad before and `ret`/padding after. Note the
Rem case includes our `mov rdx,rax` tail — the remainder-register
detail that came out of ISLE's lowering table — appearing verbatim
in gcc's output too.

The two EQUIV cases are encoding choices, not semantic differences:

- **Sub**: ours `48 2b c6` = opcode 2B (SUB r64, r/m64), ModRM
  reg=rax rm=rsi. gcc's `48 29 f0` = opcode 29 (SUB r/m64, r64),
  ModRM reg=rsi rm=rax. **Both decode to `sub rax, rsi`** — two
  legal encodings of one instruction.
- **Add**: gcc peepholed to `lea rax, [rdi+rsi]`, a different
  instruction that computes the same sum without touching flags.

EQUIV is not asserted from inspection: the test MOUNTS the native
compiler's own bytes and runs them against ours on a grid,
including i64::MIN/MAX. Identical results everywhere.

Run on the host to add the `rustc -O` rows (ground truth); the test
picks rustc up automatically when present.

## Does transpilation change the mapping? (2026-07-25)

No. Our bytes ARE Cranelift's mapping; the transpilation is
faithful. The gcc differences are a gcc-vs-Cranelift disagreement,
not drift introduced by transpiling.

Verified rather than assumed, after the question was raised:

```
isle_x64.rs:15570  Opcode::Iadd -> constructor_x64_add
isle_x64.rs:5954   x64_add      -> x64_add_break_deps
isle_x64.rs:5921   break_deps: I8/I16 -> addl_rm;
                   all other types (incl. I64) -> x64_add_raw
                                               -> addq_rm
```

So Cranelift lowers i64 `add` to `addq_rm` (`48 03 /r`) — exactly
what we emit. It does NOT peephole to `lea`; gcc does. Likewise our
`sub` uses the 0x2B form because that is the form Cranelift's
`subq_rm` encoder emits.

Provenance note recorded honestly: the iadd/isub/imul arms in
slice_lowering.py were originally INFERRED from instruction shape
(unlike the Sdiv/Srem arms, which were cut from ISLE directly).
They have since been verified against the generated ISLE at the
lines above, and the file records that.

Consequence for the ground-truth test: comparing against
`rustc -O` compares us to LLVM, which has its own peepholes. The
exact-match baseline for our slices is
`rustc -Zcodegen-backend=cranelift` (nightly).
