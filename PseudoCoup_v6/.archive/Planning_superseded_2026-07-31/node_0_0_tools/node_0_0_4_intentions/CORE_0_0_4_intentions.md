---
id: pcv6.tools.t5_intentions
level: 2
status: settled
settled_by: the owner
supersedes: null
---

# CORE 0_0_4 — T5: Intentions Tooling

Dominance as validated, machine-consumable data — the slicer's
steering input. R1 verified the PCv5 data clean (byte-identical
regeneration, 108/108 agreement with probe ground truth); the work
here is ADDITIVE, closing R1's four prose-only gaps:

1. **Row satisfiers as data** — which language satisfies which
   intent row (Rust: A/C/D/G; B/E/J in-hub). The fact that selects
   which compiler to slice; entry point for T6's schema.
2. **Structured `canon` field per verdict** — today the canon
   language is inside English prose ("Rust canon", "Kotlin
   split").
3. **Minimum-intention-set membership** (the 11 objects) in the
   JSON.
4. **Machine links to cited policies** (`PCv7_policy_decisions`).

- Keep: the existing generators and their refuse-if-incomplete
  behavior; regeneration determinism. Builder validation extends
  to refuse if the new fields are incomplete.
- Sources (provenance: PCv5 `Designing/`): `pc_verdicts.json`,
  `build_verdicts.py`, `intention_tables_gen.py`, the
  intention/basis markdowns. Evidence:
  [R1 report](../../../Research/r1_intentions_validation/REPORT.md).
- Acceptance: regeneration byte-identical; schema check that every
  field T6's steering needs is present (defined jointly with T6).
- Depends on: R1 (done). Feeds: T6.

## Nodes (depth layer, 2026-07-28)

- [node_0_0_4_0_schema_extension](node_0_0_4_0_schema_extension/CORE_0_0_4_0_schema_extension.md)
  — the four additive fields closing R1's prose-only gaps.
- [node_0_0_4_1_seam_declarations](node_0_0_4_1_seam_declarations/CORE_0_0_4_1_seam_declarations.md)
  — where a human declares a compiler entry seam, so everything
  downstream can be mechanical (the R5 automation boundary).
