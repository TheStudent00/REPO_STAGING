# Slice Notes — what to cut from rustc

## FINDING 2026-07-25: the encoder moved (cranelift 0.134)

Byte encoding is NO LONGER in emit.rs. emit.rs now calls out to a
separate crate:

```
emit.rs:280   asm::inst::idivq_m::new(
                  PairedGpr::from(writable_rax),
                  PairedGpr::from(writable_rdx),
                  *divisor,
                  TrapCode::INTEGER_DIVISION_BY_ZERO,
              ).into()
              ... inst.emit(sink, info, state)
```

`asm` = `cranelift_assembler_x64`, itself GENERATED from a DSL at
build time. So the encoder slice is cut from that crate's generated
Rust — same rule as ISLE: cut from the generated code, never the DSL.

What emit.rs DOES still own (and is worth slicing, it is real
routing): the CheckedDivOrRemSeq sequence — the divisor == -1 check,
the branch, the zero-write, and the choice of idivb/w/l/q by
operand size. That is Rust's own decision logic around the raw
instruction.

Vendor step: rerun ./vendor_encoder.sh (updated) to pull
cranelift-assembler-x64 + its build-generated sources.


Target chain: `a r./ b` on i64 → CLIF ops → x86-64 bytes,
computed by Rust's own routing logic running in Python.

## Where the logic lives

```
rustc_codegen_cranelift/src/num.rs
	codegen_int_binop  — MIR BinOp -> CLIF instruction choice.
	                     the i64 Div arm routes to sdiv.
	                     THIS is the "Dict" that doesn't exist
	                     as a table: a routing function.

cranelift-codegen/src/isa/x64/lower.isle
	lowering rules, DSL. GENERATES rust into
	target/.../lower/isle_x64.rs at build time.
	CUT FROM THE GENERATED RUST, not the DSL.

cranelift-codegen/src/isa/x64/inst/emit.rs
	CLIF/MInst -> bytes. the encoder proper:
	REX prefix computation, ModRM byte, opcode
	selection. plain Rust, transpilable.
```

## Cut procedure (per slice)

1. locate the entry function (e.g. `codegen_int_binop`)
2. follow calls, keeping only what the i64 Div path touches
3. list severed edges — each becomes an input-ring stand-in
4. classify each severed edge:
   - type/layout question  → Ledger answers (input ring)
   - instruction container → local stand-in struct
   - unrelated subsystem   → cut, must not be reachable
5. transpile the kept set (PCv3); operators inside carry RUST
   semantics — Rust `/` becomes trunc_div, never Python `//`
   (class-1 trap inside the extraction itself)

## Expected severed edges (to confirm when cutting)

- `fx: &mut FunctionCx` — carries type info + the builder.
  Split: type queries → Ledger stand-in; builder → a CLIF
  instruction accumulator (a list, in Python)
- `Ty` / layout queries → Ledger
- `Value` / `Inst` handles → small local classes wrapping ints
- diagnostics, spans, error reporting → cut

## Acceptance for the slice work

1. transpiled router, given (i64, i64, Div), emits the same CLIF
   op sequence Cranelift emits for the same MIR (compare against
   `--emit llvm-ir`-style CLIF dump from cranelift's own tools)
2. transpiled encoder, given that CLIF, emits bytes identical to
   the hand-verified `idiv` sequence in test_output_ring.py
3. end-to-end grid vs native rustc — byte-identical results

## Practical first step (host, needs the rust source)

```
git clone --depth 1 https://github.com/rust-lang/rust
# codegen backend:
ls rust/compiler/rustc_codegen_cranelift/src/num.rs
# cranelift is a separate crate (vendored or from crates.io):
cargo new --lib clif_probe && cd clif_probe
cargo add cranelift-codegen
cargo build          # generates isle_x64.rs
find target -name "isle_x64.rs"
```
