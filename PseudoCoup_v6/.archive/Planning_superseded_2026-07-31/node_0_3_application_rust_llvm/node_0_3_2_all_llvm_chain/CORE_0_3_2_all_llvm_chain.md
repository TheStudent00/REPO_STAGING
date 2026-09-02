---
id: pcv6.application.rust_llvm.all_llvm_chain
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_3_2 — The All-LLVM Chain

Build the executing chain so every stage is LLVM-derived: front
half (node_0_3_0) → ISel (node_0_3_1) → the already-ingested LLVM
x86-64 encoder. A retired reference backend was previously kept on
this campaign as a cross-check oracle for the chain; that backend
and its role here were removed as mis-aimed (2026-07-30) — it never
was, and is not now, part of the running path or a standing
cross-check. Native rustc/LLVM output is the ground truth.

## What "done" means

A hub expression (`a r./ b`) executes end to end with every stage
sliced from LLVM/rustc, producing bytes that run in stock CPython
(via the insertion mechanism) and match native `rustc -O` on the
arithmetic grid — the PCv5 cornerstone result, now LLVM-native and
all-PCv6.

## Depends on

- T6 insertion (the execution mechanism) closed all-PCv6.
- node_0_3_0 front half extracted and rustc-verified.
- node_0_3_1 ISel gap decided and built.
- The LLVM encoder increment (done) as the final stage.

## Acceptance

- The grid matches native `rustc -O` (host ground truth).
- `test_all_llvm.py`-style guard: no import of any retired
  reference backend on the running path.

## Consequence when done

The intermediate goal is met: Rust integer arithmetic transpiled
and sliced via LLVM, executing in the hub, checked against native
rustc and the byte-level ISA agreement of the LLVM encoder stage.
The campaign then proceeds to node_0_3_3 (architectures) and the
Hub node's PC.int64 surface.
