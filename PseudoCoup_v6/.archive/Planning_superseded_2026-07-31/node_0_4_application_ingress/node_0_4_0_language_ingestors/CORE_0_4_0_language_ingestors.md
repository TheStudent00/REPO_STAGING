---
id: pcv6.application.ingress.language_ingestors
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_4_0 — Language Ingestors

One ingestor per source language: tree-sitter parse (T1) → UR-AST
(T3) → hub program in intention objects. The T3 ingestor contract
already exists (node table + census baseline + no direct-ledger-
writes); an application ingestor is that contract aimed at
intention objects instead of at reproducing compiler vocabulary.

## The mapping each ingestor carries

- construct → intention object: `HashMap<K,V>` → PC.map, a Rust
  `Vec` → PC.list, `Option<T>` → PC.optional, `match` → PC pattern
  form, and so on. The mapping is DATA (a table per language),
  validated against `pc_intentions.json` — a construct that maps
  to no minimum-set object is a recorded gap.
- The census gate makes coverage honest: every node kind in a
  real program is handled, baseline-justified, or leftover (the
  worklist). WFL drove this to zero over 325 files — the same
  discipline, PCv6-side.

## Order (dominance-driven)

1. **Rust** first — we already parse it, it satisfies rows
   A/C/D/G (the most dominant intentions), and its constructs map
   cleanly (Option, Result, match, ownership).
2. Then by satisfier coverage from `pc_intentions.json`'s
   `row_satisfiers` field, not by convenience.
3. The harvest gives Kotlin (v4/WFL) nearly free — a strong
   second once Rust proves the ingestor shape.

## Acceptance (per language, escalating)

- Structural: the census gate green on a real program corpus;
  every construct maps or is a recorded gap.
- Round-trip: hub program → the SAME language → re-ingested →
  identical intention structure (the daisy-chain idea from v1,
  scoped to one language first).
- Behavioral: node_0_4_2's oracle — the real bar.

## Open (the owner)

- The construct→object tables are ontology (naming + mapping
  choices) — the owner's domain per protocol §6. The tool validates
  tables; it does not invent mappings.
