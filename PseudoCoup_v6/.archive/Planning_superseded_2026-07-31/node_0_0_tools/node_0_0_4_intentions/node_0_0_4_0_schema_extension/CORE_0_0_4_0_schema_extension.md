---
id: pcv6.tools.t5_intentions.schema_extension
level: 3
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_0_4_0 — Intentions Schema Extension

Add the four structured fields R1 found missing, so the data can
STEER the slicer instead of being read by a human. Additive only:
R1 verified the existing artifact clean (byte-identical
regeneration, 108/108 agreement with probe ground truth), so
nothing existing is rewritten.

## Subject artifacts (all in `<WORKSPACE_DIR>/PseudoCoup_v5/Designing/`)

- `pc_verdicts.json` — the built artifact (fields today: meta,
  languages, intent_categories, t1_realizations, t2_compatibility,
  t2_diagonal, primitives, operators, basis_audit, border_lattice).
- `build_verdicts.py` — the builder; refuses to emit on incomplete
  data. Extension keeps that behavior and widens it.
- `intention_tables_gen.py` — imported by the builder as the data
  source for categories/realizations/primitives/operators.

## The four fields (names are the owner's to settle)

| working name | carries | lifted from |
|---|---|---|
| `row_satisfiers` | per intent category (A–J): which of the 12 languages satisfies it natively, and which are solved in-hub | `intention_row_satisfiers.md`, `BEJ_expansion.md` |
| `canon` | per primitive/operator verdict: the language whose semantics the hub adopts, as a field rather than inside English prose ("Rust canon", "Kotlin split") | the existing `pc_verdict` strings |
| `minimum_set` | membership of the 11-object minimum intention set | `minimum_intention_set.md` |
| `policy_refs` | machine links from a verdict to the policy entries it cites ("policy 6", "policy 7") | `PCv7_policy_decisions.md` |

## Work items

1. Extend the generator data with the four fields, keeping every
   existing field byte-stable.
2. Extend the builder's completeness refusal to cover them: a
   missing satisfier row, an unparsed canon, an unlisted set
   member, or a dangling policy reference must REFUSE to emit —
   same posture as today, wider surface.
3. Keep regeneration deterministic (no timestamps).

## Acceptance (delegation-ready)

- Rebuild produces a JSON that (a) contains all four new fields,
  (b) is byte-identical on a second rebuild, and (c) leaves every
  pre-existing field byte-identical to the R1-verified artifact —
  compare field-by-field, not whole-file.
- Deliberately removing one satisfier row / one canon / one set
  member / one policy link each cause the builder to REFUSE (four
  separate negative tests).
- A schema check asserts every intent category has a satisfier
  entry and every verdict has a canon.

## Open (the owner)

- **Field names** — naming is the owner's domain; the table above is a
  working proposal.
- Whether the extended artifact is written back into
  `<WORKSPACE_DIR>/PseudoCoup_v5/Designing/` (PCv5 is archived
  research) or copied forward into
  `<WORKSPACE_DIR>/PseudoCoup_v6/Tools/intentions/` and maintained
  there. Recommendation: copy forward, since PCv6 tools should not
  write into an archived repo.
