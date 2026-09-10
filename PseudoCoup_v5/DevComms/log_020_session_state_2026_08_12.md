# log 020 — session state, 2026-08-12: the compiler-as-authority arc, and where the walk stands

At the owner's request ("please make note of the state of our
conversations, especially the research findings"). The record of the
stretch from the token-table brainstorm through the empirical
compiler research. Predecessor state log:
`PRIVATE/PseudoCoupHQ/DevComms/log_006_ur_research_record.md`.

---

## 1. What is settled (rulings, with dates)

- **no source copy** (2026-08-07): `Tree` holds no bytes; content
  leaves carry `TsOrigin.text`; unparse is faithful convergence.
- **`variant`** (2026-08-07): varying tokens read from the tree at
  mint, stored on the node; read by grammar role name where one
  exists (verified: tree-sitter's `child_by_field_name` answers
  anonymous tokens).
- **token tables are grammar-authored** (2026-08-11): the pinned
  `grammar.js` is a closed human-written enumeration, complete by
  construction; the corpus census is frequency/oracle material only.
  This superseded "census-generated, human-reviewed" — the review
  gate fell to the owner's automation push, replaced by a mechanical
  three-way classification (STENCIL / DERIVED / VARIANT,
  `PRIVATE/PseudoCoup_v5/Research/census_stencils.py`) plus
  the convergence oracle as verifier.
- **`ts_to_ur` shape** (2026-08-11): `Mapper` + `LanguagePack`, both
  realize:false, designed in
  `Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md`;
  shape-pass stubs live in `Tools/ledgerer/ts_to_ur.py`. the owner is
  skeptical until tests verify — tests are the settling instrument.
- **mirror tree-sitter's pin** (2026-08-12): the q4 lean — the pin
  follows their releases; `ERROR` from newer syntax is an
  out-of-date-pin signal, not a design flaw. Fork-if-they-lag stays
  available, undecided, for when it bites.
- **`check_pin` + staleness check** (2026-08-12, the owner: "i dont see
  why we wouldnt"): the pack checks its version pin AND whether that
  version is level with the language (the differential alphabet).
- **ordering** (2026-08-12): pin bump first, compiler fallback
  second; the fallback's shape when built is refuse-by-name + warn +
  explicit user override, and such nodes may sit in the ledger with
  honest substrate and unresolved `ur_kind` — ingress without
  egress.

## 2. The research findings (the part the owner flagged as unexpected wins)

- **log_018 — the differential token alphabet.** rustc's post-glue
  token enumeration (`rustc_ast/src/token.rs`) vs the pinned
  grammar's anonymous tokens: 51 of ~55 punctuation agree; all 6
  disagreements explained by purpose (rustc keeps dead tokens for
  diagnostics; the grammar splits string/comment delimiters rustc
  fuses). The keyword extension against the Rust reference
  (`keywords.md`: 58 keywords) explained 17 of 18 apparent gaps and
  found ONE real one: **`safe`** (stabilized 1.82) — a pin gap found
  with no corpus, then confirmed by parse (`safe fn` → ERROR node).
  The compiler is thereby a corpus-free staleness detector.
- **log_019 — empirical stencil recovery.** rustc's pretty-printer
  (`RUSTC_BOOTSTRAP=1 -Zunpretty=normal`) recovers stencils
  mechanically: placeholders in every slot, print, substitute — the
  literal remainder is the stencil, INCLUDING variant tokens
  (`&raw const`, `move`, match guards). Two side findings: rustc's
  printer normalizes output (canonical form out — the same design
  choice as faithful convergence, independently made by the
  compiler team); and the instrument is itself pinned (sandbox 1.75
  refused `safe fn`; the owner's container 1.96.1 parses and prints it —
  verified through the SandboxDesign agent lane).
- **the owner's standing interest, recorded**: "i am very interested in
  this development potential — including other language compilers.
  but that is far beyond us right now." Whether other languages'
  compilers offer an equivalent authority (a post-join token
  enumeration; a canonical pretty-printer) is an open research
  question PER LANGUAGE; nothing in the pack design depends on it.

## 3. The conversational arc worth keeping

the owner pressed three times that the compiler is a knowledge resource;
the initial responses defended the grammar instead of examining the
compiler, and the examination, once done, paid out twice (the
staleness detector; the stencil recovery). The corrected division of
labor: **the grammar authors the tables** (arrangements, complete by
enumeration), **the compiler informs and verifies** (alphabet
diffing, empirical recovery, compile-as-oracle) — in the owner's words,
"the compiler cares about compiling, not creating a user interface
for interpreting/processing tokens in an abstract representation...
but it very much seems that it can inform/verify decisions."

## 4. Where the walk stands (task list state)

- done: CORE for `ts_to_ur` (register + design + open edges by
  log_017 number); shape-pass stubs (`Tools/ledgerer/ts_to_ur.py`,
  imports clean, hq check 0 errors).
- next: logic pass on the stubs (now including `check_pin` and the
  staleness check), then verification tests (round-trip mint /
  admit / convergence on sample files).
- open behind that: q1 kind-map ratification (163 rows; mint_node
  refuses unknown kinds pending it), q3 macro cluster, q4 formally
  (mirror-the-pin is the ruled lean; refuse-vs-opaque for residual
  ERROR nodes still open), q5 one-yes ratification, q6 pack file
  layout.

## 5. Unplaced (raised 2026-08-12, no ruling yet)

- PlanPlan labels for brainstorm/future-plan/archive visibility —
  the owner's proposal that scattered `.archive/` folders and dev
  brainstorms be surfaceable at project top level via special
  labels. PlanPlan-level design, the owner's to shape; discussion open.
