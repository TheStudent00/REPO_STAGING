---
id: hq.research.lean_proof_path_resistant_to_churn.language.compose_at_width
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: compose_at_width
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_4_language/node_0_3_3_4_4_compose_at_width/CORE_0_3_3_4_4_compose_at_width.md
super_node:
    name: language
    path: ../CORE_0_3_3_4_language.md
sub_nodes: []
---

# CORE 0_3_3_4_4 — compose_at_width

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.language.compose_at_width
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [language](../CORE_0_3_3_4_language.md)

## sub_nodes

*(none yet)*

## definition

`compose_at_width(language, primitive, widths) -> source | None`

When `operator_for` has no unit for the primitive at the definition's
widths (a 128-bit product on a language whose widest word is 64), build
the primitive from entries at narrower widths, under a theorem of
`LeanExpr.once_proved_theorems` that says the composition equals the
primitive at every width.

Steps, in order:

1. find a theorem whose head is this primitive
2. instantiate its right-hand side at the widths asked
3. `render` that right-hand side: every primitive in it is at a width
   `operator_for` holds, or this returns None
4. no theorem: return None

What a person writes: the theorem, once, general in width (written
once). Never a case for an opcode. Where no theorem exists yet, the
definition is refused with the primitive and widths named, and the
refusal row is the ask for that theorem.
