# log 006 — the `kinds` vocabulary: five claims, walked one at a time

2026-08-05, at the owner's request ("save your comment in a log and i want
to go through one at a time so we dont miss anything"). The five
claims below are the chat response of 2026-08-05 on how the neutral
`ur_kind` vocabulary should be built, split into separately
judgeable items. Each carries a status; the walk-through updates
them in place.

Context: `ur`'s CORE registers `kinds` as a `realize: false`
`code (variable)` — the destination vocabulary, append-only in
spirit, checked for totality against `node-types.json`. What was
never settled is the initial CONTENT and its organizing principle.

---

## item 1 — who has `node-types.json`

**Claim:** every tree-sitter grammar repository generates its own
`src/node-types.json` — per-grammar, maintained by that grammar's
owner, no central registry. The same information is on the compiled
`Language` object at runtime (`supertypes`, `subtypes`, kind
enumeration), so the pinned vendored grammars answer without
trusting anything beyond the pin.

**Status: factual, confirmed in discussion 2026-08-05.**

## item 2 — scope: per-language as ingested, not union-of-12 up front

**Claim:** the 12 pinned grammars are v2's breadth; PCv5's target is
rust (plus c/cpp for the compiler slice). Building a 12-language
union up front means guessing at eleven languages' semantics with no
corpus in hand — against the WFL discipline of measuring coverage
against actual ingest. The append-only rule makes incremental growth
safe.

**Status: proposed, not yet walked.**

## item 3 — what `ur_kind` classifies (originally "intent vs form")

**Claim as first stated:** `ur_kind` should classify FORM (what a
node is: function definition, call, binary operation), not intent
(what a consumer does with it: definition site vs reference, ingress
vs egress role) — intents already flow through `tags.scm`
categories, connectors, and `semantic`.

**Status: UNDER DISCUSSION — and the claim's vocabulary collided
with the project's.** the owner, 2026-08-05: the word "intention" is a
term of art here, from the original research — "the capability and
constraints of an object determine what intentions can flow through
it. the ultimate intention of an object is the greatest amount of
intent that object can hold... the dominant intentions cover all the
intentions of all other objects... the intent-dominant object can
essentially hot-swap with zero loss of functionality — since unused
intentions are inert." The intentions artifact exists as validated
data (`pc_verdicts.json` — intent_categories, t1_realizations,
108/108 probe agreement; now at
`PRIVATE/PseudoIR/Tools/intentions/`), and the owner figured `ur`
would be based on it. The claim as first stated used "intent" in
the everyday consumer-role sense, which is a THIRD thing. The
walk-through of this item is untangling the three senses; the
resolution updates here when the owner rules.

## item 4 — union quotiented by verified 1:1 merges

**Claim:** each ingested language contributes its kind set; two
kinds merge into one neutral kind when their correspondence is
verified 1:1 — judged on grammar facts (`node-types.json` fields
and permitted sub-node kinds) plus meaning, never on name
resemblance. Partial correspondences (rust `self_parameter` with no
python twin) stay language-specific and unmerged, which is safe
because the substrate carries what the neutral layer does not
claim.

**Status: proposed, not yet walked. the owner's framing that prompted it:
"if nodes have essentially a perfect 1:1 correspondence, than they
can merge?"**

## item 5 — the mechanical seed at language one

**Claim:** with one language ingested the union IS rust's set, so
the initial `kinds` is derivable from the pinned grammar: 163 named
kinds plus the five supertype families as the coarse layer.
`ur_kind = ts_kind` is a legitimate identity map at language one;
normalization becomes non-trivial only when language two arrives
and the first evidence-backed merges are proposed.

**Status: proposed, not yet walked. Interacts with item 3: if the
coarse layer is intention categories rather than grammar
supertypes, the seed changes shape.**
