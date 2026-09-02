---
id: pir.rust_llvm_insert.support.whole_chain_from_llvm
status: projected
---

# SUPPORT — whole chain from llvm

projected 2026-07-30 from the previous plan, now archived at
`<WORKSPACE_DIR>/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_3_application_rust_llvm/node_0_3_2_all_llvm_chain/CORE_0_3_2_all_llvm_chain.md  (250 words)
verdict: substitute
changed: nothing lexical — the source already carries its own
2026-07-30 self-correction: the retired backend is unnamed and its
former cross-check-oracle role on this chain is explicitly struck as
mis-aimed, with native rustc/LLVM output stated as the ground truth.
The guard rule ("no import of any retired reference backend on the
running path") is carried as-is, worded without naming the backend.

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
