---
id: pcv6.application.rust_llvm
level: 1
status: draft
settled_by: the owner
supersedes: pcv6.planning.plan_llvm_rust_flat
---

# CORE 0_3 — Application: Rust (LLVM)

The intermediate goal as a campaign: Rust transpiling and slicing
via the compiler Rust actually uses. Re-derived on the component
frame; the PCv5-era chain plan
(`<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/plan_llvm_rust_2026-07-27.md`)
is superseded reference. Work happens in
`<WORKSPACE_DIR>/PseudoCoup_v6/Application/` and graduates general
machinery into Tools.

## Where the campaign already stands (from the tools wave)

- The LLVM x86-64 ENCODER is ingested: T3 increment 2 reproduces
  PCv5's `llvm_encoder_gen.py` byte-identically, and PCv5's
  exhaustive agreement suite (modRM 256/256, REX 131,072/131,072,
  SIB 256/256 vs an independently-derived reference encoder)
  re-verified.
- **SUPERSEDED (2026-07-30):** this campaign was built using a
  retired reference backend's routing/lowering/encoding chain as its
  frozen cross-check ORACLE, with LLVM stages replacing it one at a
  time checked against it. That work and its framing were removed as
  mis-aimed — the backend was meant only as a one-time verification
  reference, never a forward path, and building the campaign's
  ordering around it was the drift the owner ordered corrected. The
  settled direction is LLVM/rustc-LLVM checked directly against real
  rustc/LLVM ground truth (compiled and executed output, or
  `rustc --emit=llvm-ir`), not against any retired backend.

## Nodes

- [node_0_3_0_front_half](node_0_3_0_front_half/CORE_0_3_0_front_half.md)
  — MIR→LLVM-IR: rvalue.rs BinOp routing as a slicing request
  form + extraction.
- [node_0_3_1_isel_gap](node_0_3_1_isel_gap/CORE_0_3_1_isel_gap.md)
  — the instruction-selection gap: price the three options with
  evidence, then decide (the owner).
- [node_0_3_2_all_llvm_chain](node_0_3_2_all_llvm_chain/CORE_0_3_2_all_llvm_chain.md)
  — swap the executing chain to all-LLVM stages, oracle-checked.
- [node_0_3_3_architectures](node_0_3_3_architectures/CORE_0_3_3_architectures.md)
  — aarch64 and beyond, only after the x86-64 chain stands.

## Standing constraints

- x86-64 first (the LLVM encoder's independently-derived
  cross-check is x86-64-only; disagreement is detectable there).
  aarch64 has NO such cross-check — native rustc is its only ground
  truth.
- Every LLVM-derived stage is checked directly against real
  rustc/LLVM ground truth, not against any retired backend.
- Upstream sources vendored and pinned; the open point of moving
  them out of the archived PCv5 tree into PCv6 belongs to this
  campaign's first increment.
