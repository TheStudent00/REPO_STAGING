---
id: pcv6.application.rust_llvm.architectures
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_3_3 — Architectures (aarch64 and beyond)

Repeat the encoder stage per architecture; the front half and the
selector-front are shared across architectures (the IR is
target-independent until ISel). Only encoder + arch-specific ISel
are per-architecture.

## Ordering and the oracle problem

- x86-64 FIRST and DONE FIRST because the LLVM encoder's
  independently-derived reference gives an x86-64 cross-check —
  disagreement is byte-detectable there.
- **aarch64 has no such cross-check.** Native `rustc --target
  aarch64-unknown-linux-gnu` is the ONLY ground truth. This
  changes the acceptance shape: no independent second extraction
  to cross-check, so the native-rustc grid must be broader and
  the census/stub discipline stricter (a wrong stub can only be
  caught by native execution, not by a cross-check diff).

## Work items (per architecture)

1. Survey the encoder's grammar FIRST (do not assume it matches
   x86's shape — the CORE for the rust ingestor already warns
   this).
2. Slicing request form for `<Arch>MCCodeEmitter.cpp`.
3. Extract via T6 (C++ ingestor path, already proven on x86).
4. Acceptance: native-rustc grid for that target.

## Open (the owner)

- WHICH architectures matter, and in what order after aarch64.
  This is a product-scope call, not a technical one — recorded
  for when the x86-64 chain is complete.
