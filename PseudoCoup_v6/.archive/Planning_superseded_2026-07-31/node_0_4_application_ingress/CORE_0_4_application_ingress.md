---
id: pcv6.application.ingress
level: 1
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_4 — Application Ingress (the 12 languages → Hub)

The OTHER half of the project, untouched in PCv6 so far: converting
ordinary application programs — not compiler source — from the 12
languages into hub form without violating their intentions. This is
dashboard capability row 5. It reuses the same foundation as
compiler ingress (T1 parse, T2 ledger, T3 UR-AST) but the target is
different: the hub's intention objects, not sliced compiler
semantics.

## Why it is separate from compiler slicing, in one distinction

- **Compiler ingress** (T3 done, T6 slicing) eats a COMPILER to
  acquire a language's exact low-level semantics.
- **Application ingress** (this node) eats a PROGRAM WRITTEN IN a
  language and re-expresses it in the hub's intention objects,
  which are backed by those acquired semantics.
- They meet at the intention objects: slicing produces the
  semantics; application ingress produces programs that USE them.

## The harvest is substantial and uncomposed

The lineage's whole application-transpiler capability
(AgentMemory/03) targets exactly this and is unused in PCv6:
Kotlin→Dart/Python ingestors (v4/WFL), the coverage gate, the
289-line semantic ledger's application fields (param shapes,
method returns, suspend), v0's behavioral oracle. Composing these
onto the PCv6 T1–T3 spine is the bulk of the work.

## Nodes

- [node_0_4_0_language_ingestors](node_0_4_0_language_ingestors/CORE_0_4_0_language_ingestors.md)
  — one ingestor per source language, mapping its constructs to
  intention objects; Rust first (we already parse it), then the
  dominance order.
- [node_0_4_1_intent_capture](node_0_4_1_intent_capture/CORE_0_4_1_intent_capture.md)
  — recording the program's intentions in the ledger: which
  intention object each construct selects, complexity class
  included.
- [node_0_4_2_behavioral_oracle](node_0_4_2_behavioral_oracle/CORE_0_4_2_behavioral_oracle.md)
  — the acceptance that matters here: does the hub program BEHAVE
  like the source (v0's oracle discipline, the hardest and most
  valuable harvest).

## Standing constraints

- Ingress is trivial BECAUSE the hub dominates intentions — a
  construct maps to the object whose canon already covers it, no
  semantic distance. Where a construct has no dominating object,
  that is a gap in the intention set, recorded, not patched at
  ingress.
- The uniform-polyfill and border laws apply to ingressed programs
  exactly as to sliced semantics.

## Sequencing note (the owner's call)

This node does NOT block on the Rust/LLVM application or the Hub
node — it needs only T1–T3 (done) plus the harvest. It is the
most direct path to "the Hub can be built from other languages,"
and it is independently startable. Whether to interleave it with
the T6/Hub line or hold it until the compiler-slicing spine is
complete is a sequencing decision recorded for the owner; the current
plan holds the tools order (T6 → Hub) first.
