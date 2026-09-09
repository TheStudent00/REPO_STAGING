---
id: pcv6.transpiler.support.ingress
status: projected
---

# SUPPORT — ingress

projected 2026-07-30 from the previous plan, now archived at
`PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_2_transpiler/CORE_0_0_2_transpiler.md  (128 words)
source: node_0_0_tools/node_0_0_2_transpiler/node_0_0_2_0_ingress_framework/CORE_0_0_2_0_ingress_framework.md  (211 words)
verdict: clean
changed: nothing

---

## from node_0_0_2_transpiler

# CORE 0_0_2 — T3: Transpiler

The generalized ingress framework (tree-sitter tree → UR-AST +
ledger population) with per-language ingestors as thin
specializations; emission framework later. Settled (the owner-aligned
2026-07-28): **fresh spine in PCv6 mining the lineage** (no
wholesale port; every transplant carries provenance + its
acceptance test); coverage gate and gate-before-emit are framework
features; ledger writes id-keyed from the start; **first milestone
is ingress only** (Rust→hub).

Harvest map: [transpiler survey](../../../../PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md).
Lowering logic enters the hub by TRANSPILING THE COMPILER AND
SLICING, never by table mining (closed decision).

## Nodes

- `node_0_0_2_0_ingress_framework` (previous plan)
  — the general pipeline and the ingestor contract.
- `node_0_0_2_1_rust_ingestor` (previous plan)
  — first milestone: the compiler-source ingress rebuilt on
  tree-sitter, verified against PCv5's own artifacts.
- `node_0_0_2_2_emission` (previous plan)
  — deferred: the emission framework's settled constraints, held
  until ingress stands.

## from node_0_0_2_0_ingress_framework

# CORE 0_0_2_0 — Ingress Framework

The general pipeline every language rides; an ingestor specializes
only the marked stages.

- **Pipeline** (each stage names its harvest source):
  1. **parse** — T1's parser factory; the ingestor names its
     grammar, nothing more.
  2. **census/coverage gate** — T1's recorder partitions every
     node kind into handled / baseline-justified / leftover;
     leftover IS the worklist and a nonzero leftover fails the
     gate (WFL recorder + v0 total-partition strictness).
  3. **UR-AST build** — general walker maps tree-sitter nodes to
     UR-AST via the ingestor's node table; unknown kinds cannot
     pass silently (they're leftover by construction).
  4. **ledger population** — id-keyed writes per T2's keying spec;
     types/shapes recorded or marked `unresolvable`, never
     guessed.
- **The ingestor contract** (the specialized edge): a node table
  (tree-sitter kind → UR-AST build rule), a grammar id, a census
  baseline with per-entry justification — and nothing else. No
  ingestor constructs parsers, invents keys, or writes the ledger
  directly outside the framework's population API (the v4
  Dart-ingress bare-name violation becomes structurally
  impossible).
- **Generalize/specialize test**: any logic appearing in a second
  ingestor moves up into the framework (the owner's overlap principle
  made mechanical).
- **Framework acceptance**: a toy grammar fixture exercising all
  four stages; census determinism (byte-identical reruns); a
  deliberate-unknown-kind fixture that MUST fail the gate.

## where those nodes went

- ingress_framework — carried in this file, above.
- emission — `PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_1_transpiler/SUPPORT_egress.md`
- rust_ingestor — moved to the other project with the work it
  describes: `PseudoIR/Planning/node_0_2_hub/node_0_2_0_construction/node_0_2_0_0_rust_llvm/node_0_2_0_0_0_transpile/SUPPORT_rust_ingestor.md`
