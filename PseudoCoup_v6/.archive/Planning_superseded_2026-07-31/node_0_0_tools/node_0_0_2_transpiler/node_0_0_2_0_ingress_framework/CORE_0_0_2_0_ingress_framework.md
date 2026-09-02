---
id: pcv6.tools.t3_transpiler.ingress_framework
level: 3
status: settled
settled_by: the owner
supersedes: null
---

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
