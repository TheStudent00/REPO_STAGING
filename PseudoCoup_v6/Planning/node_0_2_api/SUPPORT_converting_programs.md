---
id: pcv6.api.support.converting_programs
status: projected
---

# SUPPORT — converting programs

projected 2026-07-30 from the previous plan, now archived at
`PRIVATE/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_4_application_ingress/CORE_0_4_application_ingress.md  (416 words)
source: node_0_4_application_ingress/node_0_4_0_language_ingestors/CORE_0_4_0_language_ingestors.md  (284 words)
verdict: clean
changed: nothing

---

## from CORE_0_4 — Application Ingress (the 12 languages → Hub)

The OTHER half of the project, untouched in PCv6 so far: converting
ordinary application programs — not compiler source — from the 12
languages into hub form without violating their intentions. This is
dashboard capability row 5. It reuses the same foundation as
compiler ingress (T1 parse, T2 ledger, T3 UR-AST) but the target is
different: the hub's intention objects, not sliced compiler
semantics.

### Why it is separate from compiler slicing, in one distinction

- **Compiler ingress** (T3 done, T6 slicing) eats a COMPILER to
  acquire a language's exact low-level semantics.
- **Application ingress** (this node) eats a PROGRAM WRITTEN IN a
  language and re-expresses it in the hub's intention objects,
  which are backed by those acquired semantics.
- They meet at the intention objects: slicing produces the
  semantics; application ingress produces programs that USE them.

### The harvest is substantial and uncomposed

The lineage's whole application-transpiler capability
(AgentMemory/03) targets exactly this and is unused in PCv6:
Kotlin→Dart/Python ingestors (v4/WFL), the coverage gate, the
289-line semantic ledger's application fields (param shapes,
method returns, suspend), v0's behavioral oracle. Composing these
onto the PCv6 T1–T3 spine is the bulk of the work.

### Nodes

- `node_0_4_0_language_ingestors` (previous plan)
  — one ingestor per source language, mapping its constructs to
  intention objects; Rust first (we already parse it), then the
  dominance order.
- `node_0_4_1_intent_capture` (previous plan)
  — recording the program's intentions in the ledger: which
  intention object each construct selects, complexity class
  included.
- `node_0_4_2_behavioral_oracle` (previous plan)
  — the acceptance that matters here: does the hub program BEHAVE
  like the source (v0's oracle discipline, the hardest and most
  valuable harvest).

### Standing constraints

- Ingress is trivial BECAUSE the hub dominates intentions — a
  construct maps to the object whose canon already covers it, no
  semantic distance. Where a construct has no dominating object,
  that is a gap in the intention set, recorded, not patched at
  ingress.
- The uniform-polyfill and border laws apply to ingressed programs
  exactly as to sliced semantics.

### Sequencing note (the owner's call)

This node does NOT block on the Rust/LLVM application or the Hub
node — it needs only T1–T3 (done) plus the harvest. It is the
most direct path to "the Hub can be built from other languages,"
and it is independently startable. Whether to interleave it with
the T6/Hub line or hold it until the compiler-slicing spine is
complete is a sequencing decision recorded for the owner; the current
plan holds the tools order (T6 → Hub) first.

## from CORE_0_4_0 — Language Ingestors

One ingestor per source language: tree-sitter parse (T1) → UR-AST
(T3) → hub program in intention objects. The T3 ingestor contract
already exists (node table + census baseline + no direct-ledger-
writes); an application ingestor is that contract aimed at
intention objects instead of at reproducing compiler vocabulary.

### The mapping each ingestor carries

- construct → intention object: `HashMap<K,V>` → PC.map, a Rust
  `Vec` → PC.list, `Option<T>` → PC.optional, `match` → PC pattern
  form, and so on. The mapping is DATA (a table per language),
  validated against `pc_intentions.json` — a construct that maps
  to no minimum-set object is a recorded gap.
- The census gate makes coverage honest: every node kind in a
  real program is handled, baseline-justified, or leftover (the
  worklist). WFL drove this to zero over 325 files — the same
  discipline, PCv6-side.

### Order (dominance-driven)

1. **Rust** first — we already parse it, it satisfies rows
   A/C/D/G (the most dominant intentions), and its constructs map
   cleanly (Option, Result, match, ownership).
2. Then by satisfier coverage from `pc_intentions.json`'s
   `row_satisfiers` field, not by convenience.
3. The harvest gives Kotlin (v4/WFL) nearly free — a strong
   second once Rust proves the ingestor shape.

### Acceptance (per language, escalating)

- Structural: the census gate green on a real program corpus;
  every construct maps or is a recorded gap.
- Round-trip: hub program → the SAME language → re-ingested →
  identical intention structure (the daisy-chain idea from v1,
  scoped to one language first).
- Behavioral: node_0_4_2's oracle — the real bar.

### Open (the owner)

- The construct→object tables are ontology (naming + mapping
  choices) — the owner's domain per protocol §6. The tool validates
  tables; it does not invent mappings.

## where those nodes went

- language_ingestors — carried in this file, above.
- intent_capture — `PRIVATE/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_recording_intentions.md`
- behavioral_oracle — `PRIVATE/PseudoCoup_v6/Planning/node_0_2_api/node_0_2_0_examples/node_0_2_0_0_on_scripts/SUPPORT_behavioral_oracle.md`
