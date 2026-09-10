# log 006 — the ur-node research campaign: a historical record

2026-08-05 (compiled 2026-08-06). Written at the owner's request ("a historical
record of useful information") to consolidate the ur-node research
campaign that ran inside `PseudoCoup_v5` (logs 002, 006–013) into one
place, held here in `PseudoCoupHQ`'s DevComms because HQ holds what is
true across the line. Verbosity is deliberate; completeness is the goal
over brevity. A reader a month from now should be able to reconstruct
what was learned, where each finding lives, and what remained open
without re-reading the whole campaign.

**Numbering note.** This record shares the name `log_006` with
`PRIVATE/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md`
because it consolidates that log and its downstream logs 007–013; the two
are different files in different repositories and neither supersedes the
other.

---

## 1. What the campaign was

The campaign was a deepening pass on `pcv5.tools.ledgerer.ur` — the
vocabulary module of `PseudoCoup_v5`'s ledgerer tool — begun 2026-08-02
at the owner's request, "before deepening `pcv5.tools.ledgerer.ur`." `ur` is
the abstraction of the FORM of a parsed source (as `ledger` is the
abstraction of the stored data structure): node forms, edge forms,
registration forms. It has three settled sub-vocabularies — `node`
(the UR node shape), `connector` (the typed graph edge), `id` (the
identity value) — plus two `realize: false` register entries with no
folder of their own: `tree` (the per-file container) and `kinds` (the
neutral `ur_kind` vocabulary).

The campaign had two threads that ran together:

- **Deepening `ur` generally** — working out what tree-sitter actually
  provides (log 002: the worked example, the macro problem, the API
  survey, the open questions), which produced the settled `node`,
  `connector`, and `id` designs (§2 below).
- **Settling `kinds`'s organizing principle** — the register commits to
  `kinds` as data, checked for totality against `node-types.json`, but
  never settled what the INITIAL content should be or what it should
  classify. log 006 (`PRIVATE/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md`)
  opened this as five separately-judgeable claims; logs 007–013 are the
  evidence-gathering that followed, one measurement or history pass per
  open question.

All source logs live in
`PRIVATE/PseudoCoup_v5/DevComms/`: `log_002_ur_brainstorm.md`,
`log_006_ur_kinds_vocabulary.md`, `log_007_rust_kind_census.md`,
`log_008_kinds_coarse_tagging_draft.md`,
`log_009_invisible_intentions_census.md`,
`log_010_token_tree_reparse_coverage.md`,
`log_011_uncertain_families_evidence.md`,
`log_012_discipline_history.md`, `log_013_intentions_gap_history.md`.

---

## 2. The settled design

Everything in this section is SETTLED (`status: draft` at the register
level, but each design point below carries an explicit the owner ruling
quoted in its source CORE). Full COREs are not restated; each point
below is 2–4 sentences with its path.

| settlement | summary | path |
| --- | --- | --- |
| `ur` is the whole tree, richer by annotation, not replacement | The UR is the tree-sitter tree kept whole plus layers it never had: substrate (ts_kind, span, bytes, fields, children), identity (id), normalization (ur_kind), annotation (semantic, connections). The prior UR-AST failed by REPLACING the tree with ~30 neutral classes; the fix makes normalization an annotation on the tree, not a substitute for it. | `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/CORE_0_0_0_0_ur.md` |
| `tree` — the per-file container | `code (class)`, `realize: false`. Holds retained source bytes, `language`, grammar `semantic_version`, and the root `node`. Exists because losslessness is substrate PLUS bytes (a node alone cannot answer `text()`), and the grammar version on it is what makes pinning checkable at runtime. Graduates to its own folder only if serialization is ever ruled yes. | same CORE, `## design` |
| `kinds` — the destination vocabulary | `code (variable)`, `realize: false`. DATA, derived from the target grammars, not inherited from the old thirty neutral classes. Checked for totality against `node-types.json` by the census. Append-only in spirit: a kind that vanished would orphan `ur_kind` tags in existing ledgers, so kinds are superseded by addition, never removed. The per-language ts_kind→ur_kind maps live in `ts_to_ur`, not here. | same CORE, `## design` |
| `node` — origin is an attachment, not baked-in fields | Settled 2026-08-05. `Node` carries only what is true of every node — `id`, `ur_kind`, `sub_nodes`, `semantic`, `connectors`, `origin` — and `origin` is an instance of one origin class per producer (`TsOrigin` for parsed nodes carrying `ts_kind`/`named`/`fields`/`span`/`language`; co-shapes for generated/abstract nodes). This scopes "strictly richer than tree-sitter" correctly: for parsed nodes everything tree-sitter knows lives in `TsOrigin`, nothing lost; for macro-generated or abstract (to-be-wrapper) nodes there is honestly no tree-sitter origin to be richer than. | `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_0_node/CORE_0_0_0_0_0_node.md` |
| `node` — the opacity form | A `token_tree` (or any grammar-declared-opaque region) becomes ONE node marked opaque — never silently empty, so a consumer halts or skips knowingly. Re-parsed content (via `injections.scm`) hangs beneath the opaque node, marked injected, so direct and recovered structure are never confusable. | same CORE, `## rules` |
| `connector` — the static graph object | Joins two nodes by id; every writer that extends a ledger after its build writes connectors against existing ids, making late arrival uniform. The kind vocabulary is an open set by design (new kinds are data, not schema); kinds already named: definition↔instance, instance→abstract, invocation→macro-definition, produced→producer, runtime, expansion. | `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_1_connector/CORE_0_0_0_0_1_connector.md` |
| `id` — the spacetime id | Settled 2026-08-05. Uniqueness by exclusion principle: no two admissions occupy the same cell, so the id is unique by EVENT, not by description — the connector circularity vanishes because the id derives from the admission, not the graph. Coordinates are LOGICAL (a Lamport-clock shape, not wall clock): a two-level clock `id = (batch, ordinal)` within one ledger, both assigned by one sequencer; a FRAME id joins the tuple only at merge across independent sequencers. | `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md` |
| `id` — what sits beside the id, deliberately outside it | The node+connector fingerprint is an attribute, never the key (content-derived identity was rejected as a key on recorded evidence — identical co-nodes collide). One wall-clock stamp per file admission is kept as provenance metadata, not as a coordinate (clocks can tie; the frame coordinate is what actually excludes ties). Re-ingesting a file gets a new id correctly, as a different admission event; the fingerprint triages redundant re-admission versus an updated file. | same CORE, `## design` |
| the assigner | The sequencer — the counter handing out coordinates at admission — is the builder's held state, not part of the `id` class itself; the `id` class is the value the sequencer produces. | same CORE, `## design` |

---

## 3. The findings — logs 007 through 013

Each subsection: what was measured/found, the headline numbers, the
one-sentence significance, and the full path.

### 3.1 log 007 — rust named-kind census, codegen crates

**What:** A live census of every named tree-sitter-rust kind occurring
across the two codegen crates targeted by this project line
(`rustc_codegen_ssa`, `rustc_codegen_llvm`; `rustc_codegen_cranelift`
excluded, prohibited backend), 111 `.rs` files, 544,137 total nodes
walked.

**Headline numbers:** 355 total kinds (named + anonymous); **164 named
kinds** in the grammar's full kind table; **153 of 164 named kinds
occur** in this corpus (11 in a zero set — `async_block`,
`await_expression`, `extern_crate_declaration`, `gen_block`,
`generic_pattern`, `higher_ranked_trait_bound`, `shebang`, `union_item`,
`use_bounds`, `variadic_parameter`, `yield_expression`). 106 of 111
files clean, 5 files carry a `has_error` tree (71 `ERROR` occurrences,
concentrated entirely in those 5 files). Five grammar-declared
supertypes: `_expression` (39 sub-kinds, 50.27% of named nodes),
`_pattern` (18, 32.36%), `_type` (17, 8.25%), `_literal_pattern` (7,
1.95%), `_literal` (6, 1.95%) — fractions overlap and do not sum to
100% because sub-kind membership is a static grammar fact, not a
per-occurrence classification.

**Significance:** established the concrete, checkable vocabulary
surface (153/164 named kinds occurring) that log 008's coarse-tagging
draft was built against, and gave a real "totality" baseline for the
census the `kinds` CORE commits to.

**Path:** `PRIVATE/PseudoCoup_v5/DevComms/log_007_rust_kind_census.md`

### 3.2 log 008 — coarse tagging draft: rust named kinds → the 21 intention buckets

**What:** A DRAFT (not adopted) proposing a coarse tag for all 163
named-and-visible kinds of the pinned grammar, drawn from the validated
intentions artifact's 11 minimum-set objects + 10 category
differentiators (21 buckets), plus two PROPOSED new buckets
(`type-form`, `declarative-form`) argued for on the grounds that bare
type syntax and non-executing trivia/modifiers have no home in the 21.

**Headline numbers:** 42 of 163 rows flagged DUAL (carry two buckets),
**37 rows flagged UNCERTAIN** (13 of those carry both flags), 97 rows
unflagged. **Three buckets received zero rows**: B (channels), G
(scoped cleanup), I (operator overloading) — consistent with those
categories' Rust realizations being library code (`std::sync::mpsc`) or
ordinary `impl` blocks indistinguishable in the grammar from any other
impl. H (events) is nearly as empty, appearing only as a flagged dual on
`closure_expression`.

**Significance:** the empty-bucket finding is a real, positive claim —
"a category can be present in a language and invisible to its grammar"
— not an oversight; it is what log 009 goes on to measure directly. The
37 UNCERTAIN rows cluster into five families (import/namespace, sum
types, borrowing, error propagation, structural containers), which log
011 investigates one at a time.

**Path:** `PRIVATE/PseudoCoup_v5/DevComms/log_008_kinds_coarse_tagging_draft.md`

### 3.3 log 009 — the form-invisible intentions (B, G, I): how they manifest in the codegen corpus

**What:** A direct measurement, over the same two-crate corpus, of how
often the three form-invisible categories (B channels, G scoped
cleanup, I operator overloading) actually occur, using `impl_item.trait`
field parsing rather than grep.

**Headline numbers:** B — 1 `use_declaration` (`std::sync::mpsc`), 3
`channel()` calls, 11 `Sender`/`Receiver` type occurrences, all
concentrated in one file
(`rustc_codegen_ssa/src/back/write.rs`). G — **12 `Drop` impls** across
9 files (grep alone finds only 11 — misses one nested-generic case a
non-nesting regex cannot cross), plus 27 explicit `drop()` calls and 4
`*Guard`-suffixed type names. I — **5 `ops` impls** (`IndexMut` ×1,
`Deref` ×2, `DerefMut` ×1, i.e. 4 distinct target types), against 2,756
candidate operator-shaped syntax sites (`binary_expression` +
`index_expression` + `unary_expression`) corpus-wide — no arithmetic
operator traits (`Add`/`Sub`/`Mul`/etc.) are implemented anywhere in
this corpus.

**Significance:** confirms log 008's empty-bucket claim is not merely a
vocabulary gap but a real invisibility — all 17 of the B/G/I-relevant
`impl_item` nodes (12 + 5) are indistinguishable at the kind level from
any of the other 259 ordinary trait impls in the corpus (276 total);
recovering the intention requires reading the `trait` field text, which
is ledger-level work, not `ur_kind` tagging.

**Path:** `PRIVATE/PseudoCoup_v5/DevComms/log_009_invisible_intentions_census.md`

### 3.4 log 010 — token_tree re-parse coverage, measured

**What:** A direct test of log 002 §6.3's "~94% with ~20 shape entries"
estimate for re-parsing macro `token_tree` content via a per-macro shape
table (expression / argument-list / statements / items /
format-first-arg-list / array-literal / opaque), against the real
distribution of macro invocations in the two-crate corpus.

**Headline numbers:** 1,616 total macro invocations, 58 distinct macro
names; top 20 names account for 91.15% of invocations by raw frequency.
**Measured coverage: 82.98% (1,341 / 1,616), against the log 002 §6.3
estimate of ~94% — an 11.0-point overshoot correction.** 18 of the 20
tabled macros hit 100% coverage under their assigned shape. Failure
breakdown of the 275 uncovered: 122 (44.4%) from macros that define
their own grammar via pattern-plus-guard syntax (`matches!`,
`assert_matches!`); 10 (3.6%) from the `tracing` crate's `?ident`
shorthand nested inside otherwise-covered `debug!`/`info!`; 143 (52.0%)
from the 38 macro names outside the 20-entry table entirely.

**Significance:** this is the log 002 §6.3 CORRECTION made concrete —
the earlier ~94% estimate is superseded by a measured 82.98% on real
data, and the residue is explained rather than left as noise (own-
grammar macros are a structural category, not sampling error).

**Path:** `PRIVATE/PseudoCoup_v5/DevComms/log_010_token_tree_reparse_coverage.md`

### 3.5 log 011 — the five uncertain families: evidence and recommendations

**What:** For each of log 008's five UNCERTAIN clusters — (1) imports/
namespacing, (2) sum types/enums, (3) borrowing/references/lifetimes,
(4) error propagation, (5) structural containers — evidence quoted from
the validated intentions artifact
(`PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json`), a
cross-language check against 2–3 of the other eleven target languages,
a cost-asymmetry table, and one labelled RECOMMENDATION with an
explicit confidence.

**Headline numbers — the 37 uncertain rows resolve into 5 families**,
plus three gap-questions raised as QUESTIONS (never corrections) to
the owner:

| family | recommendation | confidence |
| --- | --- | --- |
| 1 — imports/namespacing | not `name`; a distinct `namespace-form` bucket | medium |
| 2 — sum types/enums | not `record` alone; a distinct `sum` bucket at minimum-set tier, DUAL with D pattern matching on `enum_item` only | high (negative), medium (positive) |
| 3a — borrowing, type side | keep type-form / F generics DUAL as drafted | medium |
| 3b — borrowing, value side | not `name`; a distinct `borrow` bucket for `reference_expression` | high (negative), medium (positive) |
| 4 — error propagation | not C alone; a distinct `error-flow` bucket, DUAL with C, with the `?`-over-`Option` caveat recorded | medium |
| 5 — structural containers | split: order-bearing containers stay `sequence`; order-free declaration containers get a distinct structural tag. Low priority — cheap either direction | medium |

Three gap-questions (never applied, never claimed as corrections): **G1
sum types** — absent from `minimum_set`/`intent_categories` despite
"sum type" appearing three times in `t1_realizations` and being the
satisfier basis of row C; **G2 error flow** — no category mentions
error/exception/Result, yet at least Java/Python/Swift spell error
propagation with grammar wholly disjoint from their optional grammar;
**G3 aliasing** — absent from the 21 buckets despite being the only
`border_lattice` verdict marked "incompatible" (twice, both aliasing
crossings).

**Significance:** converts log 008's 37 raw uncertain flags into five
argued, sourced, reversible recommendations, and surfaces the three gap
questions that log 013 later resolves as project history rather than
open research.

**Path:** `PRIVATE/PseudoCoup_v5/DevComms/log_011_uncertain_families_evidence.md`

### 3.6 log 012 — discipline history

**What:** Answers the owner's question of whether "discipline" (v3's 8-rule
Oracle Discipline matrix) is the same thing as, or different from, "the
fidelity doctrine" (PCv5's uniform-polyfill rule / PseudoIR's boundary
rule).

**Headline finding — the two-ideas verdict:** the two are readings of
one recurring word applied to two different scopes. v3's discipline
governs the Hub-language SOURCE code the developer writes, upstream of
transpilation, as an 8-item prose checklist keyed to the 12 target
languages (static typing REQUIRED, null safety REQUIRED, multiple
inheritance FORBIDDEN, generators FORBIDDEN, kwargs RESOLVED AT
COMPILE, exceptions RESTRICTED, tuple unpacking RESTRICTED, operator
overloading FORBIDDEN). The fidelity doctrine governs the TRANSPILED
OUTPUT, downstream of a polyfill decision, as a single boundary law:
"every operator on the polyfilled type routes through the simulator, or
none do." No source anywhere in the lineage asserts they are the same
instrument; the transpiler survey's "appears twice independently...
same law, derived from different bugs" claim is about the fidelity
doctrine's two independent sightings (PCv5 and retired-PseudoIR), not
about equivalence with v3's discipline. **Verdict, stated plainly:
these read as two ideas under one recurring word, not one idea with two
names — the owner rules on whether that distinction is worth preserving.**

**Significance:** disentangles a vocabulary collision the owner flagged before
it propagated into `ur` or `ledger` design language; also catalogs
every other distinct sense of "discipline"/"doctrine" found across the
whole `0_Archive` + `StressBot` lineage (13 further senses, tabulated in
the source log) so future readers don't re-derive the ambiguity.

**Path:** `PRIVATE/PseudoCoup_v5/DevComms/log_012_discipline_history.md`

### 3.7 log 013 — history of the three gap-questions: sum types, error flow, aliasing

**What:** Archive research answering the owner's memory-check on log 011's
three gap-questions ("i think error flow was included at one point. i
vaguely remember something about aliasing. i dont recall sum types at
all") by walking the full provenance chain of the intentions artifact
back through deleted git history.

**Headline finding — the copy-forward root cause, one event for all
three questions:** the source document
(`PRIVATE/PseudoCoup_v5/Designing/minimum_intention_set.md`,
byte-identical across all three PCv5 commits that held it) has SIX
sections — "The set", "Why the set stops here", "Derived (not in the
set)", "Relation to the divergence study", "Audit", "Non-object
finding", "Audit verdict", "Open" — and only "The set" was lifted into
`PRIVATE/PseudoIR/Tools/intentions/intentions_data.py`. The exact
git quote fixing the scope of what was taken:

> "# Extension field 3: MINIMUM_SET
> # The 11-object minimum intention set, lifted by reading
> # minimum_intention_set.md ("The set" section, post-audit form)."

**Three gap verdicts, each stated as a reading, the owner to rule:**

- **G1 sum types — "was discussed but never a row," confidence high.**
  The audit section examined optionals by name and passed the
  mechanism as DERIVED ("record with a tag field + choice on the tag"),
  under the document's own rule that derivable things "are listed as
  derived, or left out." "Sum type" was never a candidate object in any
  version; it is still present in `t1_realizations`/`t2_compatibility`
  today, unchanged.
- **G2 error flow — "was present," confidence high.** Present under the
  name `exception`, in the "Derived (not in the set)" section, from the
  document's first git appearance (2026-07-24) through its last
  (2026-07-27): "exception / choice + early return through / call
  layers." It vanished at the 2026-07-28 copy-forward, which lifted
  only "The set."
- **G3 aliasing — "was present," confidence high.** Had its own named
  section, "Non-object finding," with an explicit exclusion ruling: "NOT
  an object at any level ... lives beside the border grammar of PCv7,
  not in this set." It was carried into the audit verdict ("One
  non-object identified") and RELOCATED (not deleted) to
  `border_lattice` class 2, which is in the artifact today as the only
  "incompatible" crossing in the whole lattice — what was lost is the
  RULING, not the concept.

**Significance:** the campaign's answer to its own three open questions
is not "the artifact is missing something" but "the artifact's
copy-forward took a conclusion and left its argument behind" — a
verifiable, sourced history rather than a guess, delivered as readings
for the owner to rule on rather than as corrections.

**Path:** `PRIVATE/PseudoCoup_v5/DevComms/log_013_intentions_gap_history.md`

---

## 4. Corrections the campaign made to its own earlier claims

Per this project line's annotate-don't-erase practice, corrections are
stated plainly here rather than silently folded into the numbers above.

- **The 94% → 82.98% token_tree coverage correction.** log 002 §6.3
  estimated "~94% with ~20 shape entries" from a single worked example
  generalized. log 010 measured the real figure against 1,616 macro
  invocations in the pinned two-crate corpus and got **82.98%**, an
  11.0-point overshoot. This is not treated as invalidating the ~20-
  shape approach — 18 of the 20 tabled macros hit 100% coverage — but
  the ~94% figure itself is corrected downward and the residue (275
  failures) is explained by cause rather than left unexplained: 44.4%
  is macros that define their own pattern-plus-guard grammar
  (`matches!`-family), 3.6% is a nested own-grammar shorthand inside an
  otherwise-covered macro family (`tracing`'s `?ident`), 52.0% is
  simply names outside the 20-entry table. log 010 leaves open, as an
  explicit unresolved question, whether the ~94% figure should be
  retired from planning documents now that a measured figure exists.

- **The intent-vs-form vocabulary collision, and its resolution.** log
  006 item 3 was first stated as "`ur_kind` should classify FORM ...
  not intent (what a consumer does with it)." the owner flagged that
  "intention" is a term of art in this project's own research — "the
  capability and constraints of an object determine what intentions can
  flow through it" — and that the intentions artifact
  (`pc_intentions.json`, R1-verified, 108/108 probe agreement) was
  expected to be the basis for `ur`'s kinds vocabulary. The claim as
  first stated used "intent" in a third, everyday consumer-role sense,
  colliding with the project's own vocabulary. This was resolved,
  not merely noted: log 008 built the coarse-tagging draft directly on
  the intentions artifact's minimum-set objects and intent categories,
  which is the working resolution of item 3 (the coarse layer of
  `ur_kind` is the intentions vocabulary, not an invented FORM/intent
  split) — though log 006 records the item's status as still "UNDER
  DISCUSSION" at the point the collision was named, and log 008
  explicitly says "nothing here is decided."

- **The discipline/doctrine disentanglement.** log 012 corrects an
  implicit conflation risk rather than an explicit prior claim: nothing
  in the campaign had yet asserted v3's Oracle Discipline and the
  fidelity doctrine were the same instrument, but the shared word
  "discipline"/"doctrine" recurring across 14+ distinct senses in the
  lineage (catalogued in log 012 §4) made the conflation an active risk
  for anyone reading quickly. log 012 states the two-ideas verdict
  plainly and leaves the "worth preserving or worth collapsing" call to
  the owner — this is a disambiguation delivered before an error occurred,
  not a walk-back of one that did.

---

## 5. Open decisions at campaign end — owner the owner

- **The buckets-vs-derivations tension.** log 011 recommends four new
  or split buckets (`namespace-form`, `sum`, `borrow`, `error-flow`,
  plus the low-priority container split) built from first-principles
  cross-language argument. log 013 subsequently discovered that three
  of the underlying concepts (sum types, error flow / `exception`,
  aliasing/borrowing) were already RULED ON once, in
  `minimum_intention_set.md`'s unlifted sections — sum types and
  exceptions ruled DERIVED (excluded because derivable from existing
  objects), aliasing ruled a NON-OBJECT relocated to the border lattice.
  These old rulings, if authoritative, argue directly AGAINST two of
  log 011's four recommended new buckets (`sum` and `error-flow` would
  need to be re-argued against an explicit exclusion ruling rather than
  against silence; the `borrow` recommendation is actually reinforced,
  since the non-object relocation to `border_lattice` is exactly the
  reading log 011 independently guessed at). log 013's open questions 1–3
  ask directly whether E5 answers G2, whether A4 answers G3, and whether
  S1 answers G1 — none of the three is resolved as of this record.

- **The argument-document repair.** log 013 identifies that
  `minimum_intention_set.md` is "not a list of 11 things, it is an
  ARGUMENT that ends in 11 things," and that the 2026-07-28 copy-forward
  took only the conclusion. log 013 open question 4 proposes making the
  derived list and the non-object finding into DATA — a `derived` and a
  `non_objects` field alongside `minimum_set` in
  `PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json` — so the
  argument travels with the conclusion going forward, bringing
  `minimum_intention_set.md`'s six sections forward beside
  `PRIVATE/PseudoIR/Tools/intentions/intentions_data.py` rather
  than leaving them recoverable only via PCv5 git archaeology. Not yet
  decided; also unresolved is whether the 2026-07-28 lift's narrow scope
  was ever an explicit decision or merely a default nobody recorded
  (log 013 open question 5).

- **The two proposed buckets from log 008** — `type-form` (bare type
  syntax, 19 rows) and `declarative-form` (non-executing trivia/
  modifiers, 13 rows) — remain unadopted. Both have an argument-for and
  an argument-against recorded in log 008 §"the PROPOSED new buckets";
  neither has been ruled on.

- **Primary-vs-dual tags.** log 008 open question 1, restated by log 011
  §"one further question"/9: 42 of 163 rows in the coarse-tagging draft
  carry two buckets. Unruled whether `ur_kind` may hold a set of tags or
  must resolve to one primary tag with a tie-break rule — this decision
  changes the totality check's shape and is upstream of adopting any of
  log 011's family recommendations cleanly.

- **Standing smaller items, all explicitly left open in their source
  logs:**
  - **injected-id sub-address** — whether re-parsed (injected)
    token_tree content gets ids under the enclosing opaque node's path
    as a sub-address space; leaning yes (byte offsets already stay true
    to the original file under `included_ranges`), unruled. Recorded in
    `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_0_node/CORE_0_0_0_0_0_node.md`.
  - **supersedes connector kind** — a candidate connector kind for
    joining two admissions of an updated file (differing fingerprint,
    same origin file name), named but not yet added to the connector
    kind vocabulary. Recorded in
    `PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md`.
  - **serialization** — whether a UR tree is ever written to a file or
    exists only in memory during a run; if `tree`/`kinds` ever need a
    byte-fidelity round-trip discipline (as the 289-line ledger already
    has), `tree` graduates to its own folder. Recorded in log 002 §8.3
    and echoed in the `ur` CORE's `tree` design note.
  - **origin co-class names** — `TsOrigin`, `GeneratedOrigin`,
    `AbstractOrigin` are explicitly drafts ("names of the origin classes
    are drafts") pending further design.

---

## 6. Method note — the containment pattern used

Worth recording because it worked across the whole campaign and is
worth repeating on future research passes of this shape:

- **Subagents write evidence logs only.** Every measurement log (007,
  009, 010) and every evidence/history log (008, 011, 012, 013) is
  explicit at its own top about what it IS and is NOT: "A working
  record," "A DRAFT FOR DEE'S REVIEW... nothing here is decided,"
  "EVIDENCE FOR DEE'S REVIEW... Nothing here is applied," "ARCHIVE
  RESEARCH FOR DEE'S REVIEW. Nothing here is a decision, a correction,
  or an amendment." No log in the chain rules on anything; every log
  ends in RECOMMENDATIONS, QUESTIONS, or READINGS with explicit
  confidence levels, never a settlement.
- **Planning untouched.** None of logs 002 or 006–013 edits anything
  under `PRIVATE/PseudoCoup_v5/Planning/`. The settled design
  captured in §2 above reached the COREs only through the owner's own rulings,
  quoted verbatim in each CORE with the date and the exact words ("yes
  ... and yes," "we are aligned. lets proceed," "yeah logical space
  makes sense").
- **Flags are not decisions.** log 008's DUAL and UNCERTAIN flags, log
  011's RECOMMENDATION-plus-confidence structure, and log 013's
  "MY READING... confidence high, the owner rules" pattern are all the same
  discipline applied at different depths: findings are surfaced with
  their evidence and their own author's confidence attached, never
  smuggled in as settled fact.
- **Walk-through with the owner one item at a time.** log 006 itself is
  structured as five separately-judgeable claims specifically because
  the owner asked, 2026-08-05: "save your comment in a log and i want to go
  through one at a time so we dont miss anything." Each of the five
  items in that log carries its own status field, updated in place as
  the walk-through proceeds rather than each claim being bundled into
  one take-it-or-leave-it verdict.

This pattern — narrow, self-labelled, sourced evidence logs; zero writes
to Planning; explicit flag-not-decision language; one-item-at-a-time
review — is what let a five-way branching research question (log 006's
five items) fan out into seven downstream logs without any of them
drifting into unauthorized settlement, and it is recorded here as a
transferable practice, not just as this campaign's history.

---

## sources

All source logs are under
`PRIVATE/PseudoCoup_v5/DevComms/`:
`log_002_ur_brainstorm.md`, `log_006_ur_kinds_vocabulary.md`,
`log_007_rust_kind_census.md`, `log_008_kinds_coarse_tagging_draft.md`,
`log_009_invisible_intentions_census.md`,
`log_010_token_tree_reparse_coverage.md`,
`log_011_uncertain_families_evidence.md`,
`log_012_discipline_history.md`, `log_013_intentions_gap_history.md`.

The settled ur design is under
`PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/`:
`CORE_0_0_0_0_ur.md`,
`node_0_0_0_0_0_node/CORE_0_0_0_0_0_node.md`,
`node_0_0_0_0_1_connector/CORE_0_0_0_0_1_connector.md`,
`node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md`.

The intentions artifact is
`PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json` and its
`README.md` in the same directory.
