---
id: pir.intentions.support.intentions_data_shape
status: projected
---

# SUPPORT — intentions data shape

projected 2026-07-30 from the previous plan, now archived at
`~/Programming/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_4_intentions/CORE_0_0_4_intentions.md  (203 words)
source: node_0_0_tools/node_0_0_4_intentions/node_0_0_4_0_schema_extension/CORE_0_0_4_0_schema_extension.md  (408 words)
verdict: clean
changed: nothing

---

## from CORE_0_0_4 — T5: Intentions Tooling

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
  `R1 report` (`~/Programming/PseudoCoup_v6/Research/r1_intentions_validation/REPORT.md`).
- Acceptance: regeneration byte-identical; schema check that every
  field T6's steering needs is present (defined jointly with T6).
- Depends on: R1 (done). Feeds: T6.

### Nodes (depth layer, 2026-07-28)

- `node_0_0_4_0_schema_extension` (previous plan)
  — the four additive fields closing R1's prose-only gaps.
- `node_0_0_4_1_seam_declarations` (previous plan)
  — where a human declares a compiler entry seam, so everything
  downstream can be mechanical (the R5 automation boundary).

## from CORE_0_0_4_0 — Intentions Schema Extension

Add the four structured fields R1 found missing, so the data can
STEER the slicer instead of being read by a human. Additive only:
R1 verified the existing artifact clean (byte-identical
regeneration, 108/108 agreement with probe ground truth), so
nothing existing is rewritten.

### Subject artifacts

*(These were in `~/Programming/PseudoCoup_v5/Designing/` (historical),
which was deleted in the 2026-07-31 gutting — recoverable from that
repo's git history. `pc_verdicts.json` itself was copied forward and
now lives in `~/Programming/PseudoIR/Tools/intentions/`; the
generators that built it did not come with it.)*

- `pc_verdicts.json` — the built artifact (fields today: meta,
  languages, intent_categories, t1_realizations, t2_compatibility,
  t2_diagonal, primitives, operators, basis_audit, border_lattice).
- `build_verdicts.py` — the builder; refuses to emit on incomplete
  data. Extension keeps that behavior and widens it.
- `intention_tables_gen.py` — imported by the builder as the data
  source for categories/realizations/primitives/operators.

### The four fields (names are the owner's to settle)

| working name | carries | lifted from |
|---|---|---|
| `row_satisfiers` | per intent category (A–J): which of the 12 languages satisfies it natively, and which are solved in-hub | `intention_row_satisfiers.md`, `BEJ_expansion.md` |
| `canon` | per primitive/operator verdict: the language whose semantics the hub adopts, as a field rather than inside English prose ("Rust canon", "Kotlin split") | the existing `pc_verdict` strings |
| `minimum_set` | membership of the 11-object minimum intention set | `minimum_intention_set.md` |
| `policy_refs` | machine links from a verdict to the policy entries it cites ("policy 6", "policy 7") | `PCv7_policy_decisions.md` |

### Work items

1. Extend the generator data with the four fields, keeping every
   existing field byte-stable.
2. Extend the builder's completeness refusal to cover them: a
   missing satisfier row, an unparsed canon, an unlisted set
   member, or a dangling policy reference must REFUSE to emit —
   same posture as today, wider surface.
3. Keep regeneration deterministic (no timestamps).

### Acceptance (delegation-ready)

- Rebuild produces a JSON that (a) contains all four new fields,
  (b) is byte-identical on a second rebuild, and (c) leaves every
  pre-existing field byte-identical to the R1-verified artifact —
  compare field-by-field, not whole-file.
- Deliberately removing one satisfier row / one canon / one set
  member / one policy link each cause the builder to REFUSE (four
  separate negative tests).
- A schema check asserts every intent category has a satisfier
  entry and every verdict has a canon.

### Open (the owner)

- **Field names** — naming is the owner's domain; the table above is a
  working proposal.
- Whether the extended artifact is written back into
  `~/Programming/PseudoCoup_v5/Designing/` (historical) or copied
  forward and maintained in a live tools folder. RESOLVED by events,
  twice over — that folder no longer exists. it was
  copied forward, and the intentions tool then moved to
  `~/Programming/PseudoIR/Tools/intentions/` (2026-07-31), which is
  where `pc_intentions.json` is maintained now. Note the original
  reasoning — "PCv6 tools should not write into an archived repo" —
  no longer applies as stated: PCv5 is being gutted and rebuilt as
  the Frankenstein precursor rather than left archived.

## where those nodes went

- schema_extension — carried in this file, above.
- seam_declarations — NOT carried. it was written in the retired
  backend's vocabulary. the record of why is
  `~/Programming/PseudoIR/Planning/node_0_1_research/node_0_1_0_intentions/SUPPORT_retired_seam_declarations.md`
