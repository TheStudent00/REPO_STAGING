---
id: pcv6.application.rust_llvm.front_half
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_3_0 — MIR → LLVM IR (the front half)

The language-level half of the Rust/LLVM chain: how a Rust source
construct becomes an LLVM IR opcode. All Rust source, small,
located, and the grammar (Rust) is one the T3 ingestor already
handles.

## The seam and its stand-ins

- **Seam**: `rvalue.rs`'s BinOp routing (rustc_codegen_ssa) plus
  the `math_builder_methods!` macro expansion in
  rustc_codegen_llvm's `builder.rs` (macro-generated:
  `sdiv => LLVMBuildSDiv`). This is a slicing request form to
  write and validate, exactly like the four proven ones.
- **Stand-ins**: the LLVM IR builder (the `LLVMBuild*` FFI names)
  is the boundary — the slice emits IR opcode NAMES, and a hub-
  side accumulator stands in for the real builder (the same
  stand-in shape used for a retired reference backend's own
  instruction-builder accumulator).
- **The FFI wall** (`rustc_codegen_llvm/src/llvm/ffi.rs`) is where
  the chain leaves Rust for C++; the front-half slice stops at
  the IR-opcode name and hands off. Nothing transpilable lives in
  ffi.rs — it is `extern "C"` declarations only.

## Acceptance

For each hub operator, the LLVM IR opcode the extracted routing
selects equals what `rustc --emit=llvm-ir` produces for the same
construct (native rustc on the host is the ground truth; this is
a real diff, not an oracle re-use).

## Work items

1. Write and validate the front-half slicing request form (seam,
   scope filter i64/u64, stand-ins).
2. Extract via T6, following calls as the extractor already does.
3. Host-side `rustc --emit=llvm-ir` comparison harness (staged
   script, like R1/R3).

## Open (the owner)

- macro-expansion handling: `math_builder_methods!` is a Rust
  macro; the T3 ingestor sees the CALL, not the expansion.
  Whether to slice the macro definition or treat the expanded
  names as a small hand-declared table is a design call —
  recorded, priced when reached.
