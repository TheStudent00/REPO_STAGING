---
id: pcv5.tools.ledgerer.ur.progress
status: living
---

# PROGRESS — ur

- 2026-08-07 **done and exercised** (the owner: "definitely drop
  `source_bytes`"): **the no-source-copy ruling.** `Tree` loses
  `source_bytes`; `TsOrigin` gains `text` (content leaves — 14
  kinds, 37.6% of leaf instances, measured) and `variant` (the
  varying token, read at mint, never inferred). `Node.text()` now
  answers from stored content. unparse becomes faithful CONVERGENCE
  (the owner's naming): normalize once, fixed point after. the
  documentation node is PLANNED in `node`'s CORE (comments as data,
  emitted per-target via its comment protocol). applied to
  `PRIVATE/PseudoCoup_v5/Tools/ledgerer/ur.py`, round trip
  re-verified byte-identical with text+variant surviving.

- 2026-08-06 **done** (the owner: "yeah okay i dont think theres any way
  around storing file name... file name is needed"): `TsOrigin`
  gains optional `path` — the source file, set on each file's root
  node by the mapper. raised by the ledger logic pass (merge's
  same-source triage had no flag to raise); the corrected failure
  mode recorded in the node CORE: a double ingestion would merge
  successfully and sit in the ledger twice, unnoticed. applied to
  `PRIVATE/PseudoCoup_v5/Tools/ledgerer/ur.py` the same day.

- 2026-08-06 **done and exercised**: `ur.py` COMPLETE at
  `PRIVATE/PseudoCoup_v5/Tools/ledgerer/ur.py` — the first
  code file of the rebuilt PCv5. written in two passes per
  plan_and_code §2: shape first (all six classes + KINDS, stubs
  refusing loudly), reviewed by the owner ("damn fine code"), then the
  logic pass (the owner: "i feel comfortable with filling out the rest").
  exercised against a hand-built tree: text recovery at three
  depths, None for abstract origins, field-by-role incl. missing,
  walk order = admission order, Id frozen and hashable. the module
  imports neither tree-sitter nor any co-module — the vocabulary is
  parser-free, as designed.

- 2026-08-06 **done** (the owner: "`proof-form` sounds good to me. if we
  are ready for `ur.py`, lets do it"): `proof-form` ruled — the last
  open name. the ur plan is complete by the readiness test
  (descending further adds logic, not structure); code generation
  begins: `PRIVATE/PseudoCoup_v5/Tools/ledgerer/ur.py`,
  written top-down per plan_and_code §2 — shape first, logic last.

- 2026-08-06 **done** (the owner: "yes to your recommendations and
  leanings"): the four ratifications closing the design walk —
  `type-form` and `declarative-form` ruled into the form tier;
  injected-id sub-addressing ruled yes; serialization ruled
  in-memory (ledger is the durable store; `tree` grows no format);
  origin co-class names settled as drafted. ONE name still open:
  the proof-apparatus form bucket, proposed `proof-form` (from
  the owner's recovered ruling's own word: Rust adds "a PROOF"),
  alternatives `borrow-form` or folding into `type-form`.

- 2026-08-06 **done** (the owner: "oh! okay great. i unknowingly answered
  your query"): **the coupled/decoupled question RULED: coupled.**
  the kinds labels follow the minimum set's derivation verdicts; the
  three constructs settle per log_014's recommendations (sum →
  record dual choice; error flow → choice dual function; borrowing →
  no intention-tier bucket). recorded in this CORE's kinds design;
  the decision's full statement and glossary are
  `PRIVATE/PseudoCoup_v5/DevComms/log_015_coupled_or_decoupled.md`.

- 2026-08-05 **done** (the owner: "we are aligned. lets proceed with making
  updates accordingly"): **`id` registered as the module's third
  class**, beside `node` and `connector`; the identity-system design
  (spacetime id, logical two-level clock, frame axis at merge,
  fingerprint-as-attribute, wall-clock provenance) graduated from
  this CORE's design section into `id`'s CORE. the assigner — the
  sequencer — went to the builder's design, per the value/assigner
  placement split.

- 2026-08-05 **done** (the owner: "i agree with it. to confirm, i think i
  like the idea of `node` and `connector`"): **deepened to four
  register entries** — `node` and `connector` as realized sub-nodes
  (the two classes where descending adds design), `tree` and `kinds`
  as `realize: false` entries designed in this CORE's `## components`.
  - names follow the owner's graph vocabulary (node/connector, connector
    reserved for the static object) and the anti-stutter ruling:
    `ur.node` not `ur.ur_node`, and `tree` not `ur_tree` by the same
    logic. both class COREs carry their attributes and methods as
    `realize: false` entries, so the structural overview is
    register-backed.
  - COREs written from log_002 §§3, 6, 7.1, 8.1 and
    SUPPORT_metaprogramming's connector needs; the connector-kind
    vocabulary drafted as an open set (definition↔instance,
    instance→abstract, the two meta-programming connectors, runtime,
    expansion). one drafted-unruled field: `Connector.provenance`.

- 2026-08-02: node folder generated by
  `PRIVATE/PlanPlan/framework/generate_nodes.py` from the
  `nodes` register of `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/CORE_0_0_0_ledgerer.md`. Skeleton only — definition,
  designation, and content pending.
