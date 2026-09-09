# log_077 — briefing for the returning session (2026-08-29)

Written for the session that ran the research of 2026-08-12 to 2026-08-14
and has not been present since. Two weeks happened. Logs 021 through 076
were written, the sandbox moved house, and the planning tree grew three
new sub_nodes. This log gets that session current and gathers the exact,
executed facts a `toolchain` skill rewrite needs.

**Vocabulary.** Structural relationships in this log are said with
**super-node**, **sub-node**, **co-node**, **sub-tree**. The banned
spellings are not used. The outcome where the operating system stops a
probe's process is **ABORT**, never the older word.

**Cold terms, reintroduced in one line each** (they were warm on
2026-08-14 and are cold now):

- **lane** — one shell script dropped into the sandbox's watched folder; a
  file write is a run.
- **holder** — the concrete typed thing a value sits in inside a language
  (`int`, `ctypes.c_int64`, `BigDecimal`), as against the abstract form.
- **form** — the layer-1 data shape (whole number, fractional number, text,
  sequence, keyed grouping, truth, nothing, identity mark).
- **route A1 / A2 / B / C** — the four evidence routes for whether a
  compiler accepts a probe: A1 an in-process compiler API, A2 a batched
  compile, B a rule lifted literally out of compiler data, C execution.
- **profile** — one operator's answers over a full grid of inputs at one
  form pair and one level.
- **containment / dominance** — directed: A dominates B when A answers
  identically everywhere B answers, and may answer more.
- **ANCHOR / SHIP** — the un-optimized build and the optimized build of the
  same source; identity is established at the anchor and carried to the ship
  by the diff.
- **canonical form** — the normalized, runnable arch-instruction rendering of
  a compiled unit; as of 2026-08-26 it is the HOME representation.

---

## §1 — the two weeks, in plain words

Two weeks ago the line had one research sub_node doing signature
clustering, one doing dominant intentions, and a census whose facts had
just been verified by execution for the first time. It now has six
research sub_nodes, and the centre of gravity has moved twice.

**What the shape of the work was.** The first week ran a very large
measurement campaign called layer 3: take every operator every grammar
declares, cross it with every holder that can hold each form, and
actually run the result in twelve languages. That campaign started small
(python alone, 20,024 probes) and ended enormous (2.2 million probes in
one value matrix, then 10 million in the Cartesian rebuild, then 46
million grid cells in the twelve-language fold). Along the way the grain
of measurement was corrected four separate times — each correction the owner's,
each one making the previous reading not merely coarser but wrong. The
biggest of those: a signature row was being built as one accept-or-refuse
bit when it should have carried the whole answer.

**What the campaigns were, in order.**

The **probe-space and vocabulary groundwork** (logs 021, 022, 023) sized
the space from the grammars themselves — 3,556 probes under the base
counting rule — unioned twelve languages' own closed type enumerations
into 59 entries, and audited the layer-2 representations, finding no gap
anywhere and so leaving the layer-1 ruling standing.

The **layer-3 campaign proper** (logs 024 through 040) built the harness,
proved it on python, then ran all twelve. Its findings are the ones a
returning session most needs: that a statically checked language's verdict
genuinely does move with the value; that the wrap camp agrees bit for bit
across five languages; that answers recorded as printed text lose
information the same answers recorded as bits keep; that constructs
(access, flow, binding) behave differently from operators and the
symmetry against signature clustering holds for one and fails for the
other, for a measured reason. The campaign closed the research node's
oldest open item, CHECK 4j, on 2026-08-20.

The **dominance and canonical-reading campaign** (logs 041 through 048)
was mostly the owner correcting the instrument. The product distance was found
to carry a bias it could not report; boundaries and walls became measured
objects located by bisection; the extended matrix and its conversion
spec were settled; the canonical-form rulings landed and then landed
again in final form, retiring the indicator columns and putting outcome
tokens inside `output_canon`; and set-identity aggregation was vetoed in
favour of a row-grain agreement graph.

The **Cartesian rebuild** (logs 049 through 059) replaced the ladder
sampling with exhaustive ordered pairs, full grids with an
`UNREPRESENTABLE` fill, and a hard compatibility gate on profiles. It also
produced the line's most careful moment of refusal: the ten-language
launch was held twice, once because three independent files recorded the
gate as open, and once again because the postscript claiming it lifted
was not independently verifiable. The correction that followed confirmed
the gate was lifted and that the real blocker was different — only two
emitters existed.

The **emitters** (logs 061 through 063) wrote the other ten, proved the
interpreted and compiled shapes first as the owner staged it, and fixed a
throughput fault in the shared static driver that had let the c++ lane
hang with no read timeout at all.

The **twelve-language fold** (logs 064 through 071) put all twelve into
one picture: 11,053 profiles, 46,108,297 grid cells, verified by two
independent re-derivations at zero mismatches. It found the one genuine
operator-spelling gap in the whole estate (swift's wrapping `&+`, `&-`,
`&*`, invisible because swift lexes them as a catch-all custom operator),
closed it under a clearly labelled hand-added namespace, and then
dissolved the long-running "which scoring is the weight" question by
replacing "how much do these disagree" with "what KIND of disagreement is
it" — window, value, or mixed, with no threshold anywhere.

The **compiler graph** campaign (logs 072, 073) founded a new sub_node on
2026-08-24. Its claim is that the connection from a high-level named
variable to a low-level operand is a PATH through the compiler's own
source, found by a machine. Five laps in, Go's compiler is 174,159 nodes
and 335,547 edges, and the register index has been traced forward, no
reversal, twenty-five waypointed hops, to the exact line where the ABI
index selects the physical register. The same campaign found the
optimizer's off switch is the identity anchor.

The **canonical form audit** (logs 074, 075) was forensic and read-only,
and it found the ratified canonical form was decorating rather than
driving: 75.1 percent of same-class decisions were being made on raw
pre-canonical bytes and only 1.8 percent on the canonical runnable form.
It caught a concrete regression — swift's division and modulo merged, and
pulled C's in with them. the owner's clarification that followed made the
canonical form the HOME representation and retired the pseudo-step
notation to comments.

The **update drill** (log 076, today) pointed the whole pipeline at rust
twice, 1.96.1 and 1.98.0, and counted the difference. The conclusion is
worth carrying: the expensive part of a language update is NOTICING. Zero
shape-layer checks can see a release by construction, because all three
read pinned or transcribed data. The toolchain cost 86 seconds and one
command. The harness absorbed a genuinely new kind of language behaviour
in 193 lines with zero tool edits.

**What moved underneath all of it.** On 2026-08-22 the sandbox of record
moved from `~/Programming/SandboxDesign` to `~/Programming/Airlock`. This
is a derivation, not a rename: the file protocol is byte-identical, only
the repository directory and the command name changed. As of today
Airlock is the only lane that answers — verified below by execution, not
by reading.

---

## §2 — every ruling the owner made in the window

Date | ruling | log

2026-08-14 | Single-language type entries stay in the union rather than being pruned as noise — "if they truly dont have equivalents in other languages, not a problem. in fact, its those gaps the Hub is trying to fill" | log_022
2026-08-14 | Compile-or-refuse is a first-class camp answer beside a value and a raise | (standing; cited in log_076)
2026-08-15 | Layer 1 — the data forms: nothing, truth, whole number, fractional number, text, sequence, keyed grouping, nesting, identity marks — ruled and frozen as one shared file `data_layer1.json` | log_023, log_024
~2026-08-15 | Standing CORE rule: builtins are OUT of scope until the owner opens them; this is what blocks the dict gap in java/c-sharp/rust/cpp/kotlin and the boolean gap in kotlin | log_021
~2026-08-17 | R2 adopted over R1: the operator menu multiplies — one signature per operator per grammar menu, so `+` and `*` are two signatures, not one host | log_021, log_024
2026-08-18 | The layer-3 design ruled: full enumeration of ordered operand pairs over layer-2 holders, the full value matrix, progress print-outs everywhere, all four evidence routes pursued together | log_027, log_032, log_036
2026-08-18 | The anti-interpretation rule (CORE 6): an acceptance verdict comes from the compiler's own logic running or from data lifted literally; hand re-assembly is forbidden, and a lifted rule is a DRAFT until diffed against route A or C on the same cells. Agreement alone is not evidence | log_027, log_028, log_036
~2026-08-18 | CORE 3: the full value matrix is CARRIED, not pruned — every value of every holder, everywhere, at the grain of form/holder/value class | log_027, log_028
~2026-08-18 | CORE 7: kotlin's cost requires a MEASURED mitigation, not an assumed one | log_027
~2026-08-18 | CORE 1: the form projection is lossy in a stated place — `Decimal(42) + Fraction(42)` raises though both operands hold one layer-1 form | log_029
~2026-08-18 | CORE 5: route C has no separate acceptance verdict — for python, ruby and php, execution is the only evidence | log_029
~2026-08-18 | Route A2 recorded UNVERIFIED for kotlin, swift, dart and csharp, and forbidden to be assigned to any of them before it is proven | log_027
2026-08-18 | The execution pass authorised: since the value matrices say cell by cell which probes compile, accepted probes are emitted into one file each, compiled once and run once — no compile failure possible by construction, nothing to bisect | log_032
2026-08-18 | Answers are recorded as BITS and type info, never printed text — "why wouldn't we get all their bits, and the type info?" Integers as two's-complement bytes, floats as their IEEE pattern, text as byte length plus UTF-8 bytes plus the language's own length notion, containers recursively. Nothing canonicalised at probe time | log_032, log_036
2026-08-18 | NO CHOSEN CUT: the full merge history is computed and the cluster count at any threshold follows from it | log_030
2026-08-18 | Kotlin's and swift's shifts are BUILTINS and out of scope by the CORE's own rule | log_030, log_033
2026-08-19 | Logs 027 through 033 to be rewritten into the readable register — same facts, same numbers, same section numbers, prose only | log_039
2026-08-19 | "i want to see it cluster the actual computed values" — authorises the answer-grain clustering pass | log_031
2026-08-19 | Job A: redo swift with the REAL compiler, not the type checker alone | log_034
2026-08-19 | Job B: "i dont care if it is symbol or word-spelled. if we can detect whether its library to filter and keep the word-spelled as first class objects, just as much as symbols" — built as a two-leg mechanical library-versus-language test | log_034
2026-08-19 | The three construct families blessed: ACCESS, FLOW, BINDING | log_036, log_037
2026-08-19 | Scaffold is inert code "used to connect logical operations of interest" — one fixed minimal scaffold per construct per language, byte-identical across every probe of that construct | log_036
2026-08-19 | A flow TRACE is written in the same bits-and-type encoding as an answer, reusing the answer row's three-field shape. No new encoding invented | log_036
2026-08-20 | The product metric carries a BIAS: a product of two factors cannot say which factor moved. Standing case: `go.+` and `java.+` never disagree over 88 shared cells, yet the product places them at 0.094 | log_041
2026-08-20 | Every alternative reading of the metric is to be BUILT rather than argued about, and each gets its own visual | log_041
2026-08-20 | "i do want things like the boundaries" — boundaries and walls become first-class measured objects, located by bisection | log_042
2026-08-20 | THE GRAIN RULING: "each row isnt a row element. its a vector" / "that way something like php.== cant appear to have obtained god-operator status." Elements become (left holder at a value class × right holder at a value class × answer token), element value the SET of tokens given there | log_043
2026-08-20 | Extended-matrix design SETTLED: 64 form-pair rows × `lang.op` columns, spelling-blind, cell = sorted set of answer forms; refuse / raise / not-applicable are FIRST-CLASS cell elements, not blanks. Three extension layers — numeric, container, text. Wrap congruences recorded as FEATURES, not mismatches | log_044
2026-08-20 | The governing comparison rule: "never compare raw answers, compare their decompositions, and let WHICH coordinate disagrees be the feature" | log_044
2026-08-20 | WORDING BAN: the word `death` is banned; the cell element is ABORT — the operating system stopped the probe's process with no language-level error. Third-party internal tokens stay, quoted as theirs | log_044, log_045
2026-08-20 | REFUSE must be split from UNPROBED: refusal evidence loads from the acceptance files, since answers files hold only the accepted subset. REFUSE = probed and declined (needs polyfill); UNPROBED = never asked (no claim) | log_044
2026-08-20 | CORRECTION on wrap detection: comparing raw signed values violates the governing rule; wrap detection moves into the [sign, mant, expo] coordinates with two labelled spellings | log_044
2026-08-20 | Extended-dendrogram design SETTLED: one merge tree per COORDINATE FAMILY, a shared threshold slider, congruences drawn as typed cross-links | log_045
2026-08-20 | VOCABULARY RULING enforced node-wide: super-node / sub-node / co-node / sub-tree only | log_045
2026-08-20 | Per-operator-matrix design SETTLED: one CSV per `lang.op`, inputs filled on EVERY row including refusal rows, outputs empty on non-value rows | log_046
2026-08-20 | THE MANT RULING: integer mants REJECTED — the decomposition is not unique (42 = 42×2^0 = 21×2^1). Settled canon is floating-point normalization with mant in [1,2) | log_046
2026-08-20 | FINAL canonical-form rulings, overriding log_046: rationals, `~` inexact markers and the exact columns are all REJECTED; fractions are banished from every visible column | log_047
2026-08-20 | Settled canon: 11 columns everywhere; outcome tokens travel INSIDE `output_canon` (REFUSE, RAISE:`<kind>`, ABORT); the separate indicator columns are RETIRED. Numeric canon [sign, mant, expo] with sign in {-1,1}, mant in [1,2) at 31 significant fractional digits; `nan` is the only word kept. Exact rational mants live only in `matrices/exact_sidecar.json` | log_047
2026-08-20 | VETO: set-identity aggregation REJECTED — it zeroed cross-language pairs (`go.+ ~ python.+` = 0.0000) even though 26 individual rows match byte-identically for one holder pairing alone | log_048
2026-08-20 | Agreement-graph design settled, his words: each operator-matrix is a NODE, its connections are the PERCENTAGE OF AGREEMENT, and the threshold is the cutoff for connection | log_048
2026-08-21 | Scope for the interval pilot is rust and ruby ONLY; the other ten follow if the pilot verifies | log_049
2026-08-21 | Each ROW is its own node, with a CENTRAL node per operator that all its rows connect to: "so two types of connectors, internal and external" | log_050
2026-08-21 | Ruling A: similarity is PER ELEMENT and NUMERIC over [sign, mant, expo], never byte comparison; combined euclidean from the perfect point, normalised by √3. A sign flip costs real distance | log_051
2026-08-21 | Ruling B: declines are NOT SCORED AT ALL — "lets only do matching on similarity of actual objects now. lets avoid things like REFUSE/RAISE/whatever-else." Excluded from numerator AND denominator; zero comparable positions means NO connector | log_051
2026-08-21 | Ruling C: break the diagonal with two new lane families — shifted pairing and one-level composition; the existing interval matrices are read-only | log_051
2026-08-21 | The Cartesian probe design: level 1 `y = op(x0,x1)` over ALL ordered pairs of a shared set X; level 2 `z = op(op(x0,x1), op(x2,x3))`. Intermediates are never enumerated, deduped, capped or unioned | log_052
2026-08-21 | SUPERSEDED and not to be re-emitted: the geometric ladder, the constant-offset shifted pairing, and one-level composition with equal operands | log_052
2026-08-21 | ABSENCE, not coercion: a value a holder cannot exactly represent is ABSENT from that row, never rounded into range | log_052
2026-08-21 | Comparability is the INTERSECTION of two rows' INPUT KEYS, not byte-identity of the whole vector; level 1 is never mixed with level 2 in one connector | log_053
2026-08-21 | CONTRACT (identical key set and byte-identical outputs at every key) and GROUP (partial-overlap clique) are kept distinct | log_053
2026-08-21 | Full grids by construction: probe every holder against the FULL X set of its form; a value the holder cannot represent fills its cell with UNREPRESENTABLE | log_054
2026-08-21 | Profile compatibility is a HARD GATE: "the key-to-key/cell-to-cell attraction is never without the context of the profile-to-profile attraction. if the profiles arent compatible, there is no attraction." A truth profile and a whole profile are NEVER compatible | log_054
2026-08-21 | No key-to-key clustering, ever | log_054
2026-08-21 | With full grids, GROUP retires; CONTRACT keeps its meaning | log_054
2026-08-21 | The research question is DOMINANCE, and it is DIRECTED: A dominates B when everywhere B answers, A answers identically. Read as nests / overlaps / contradicts, rendered as a lattice | log_054
2026-08-21 | Scoring carries TWO numbers: agreement over VALUE cells, and agreement over ALL cells with the decline tokens treated as answers | log_054
2026-08-22 | Dominance is an OPERATOR relation, one level above the profile relation: "operator A dominates operator B if A contains all the same profiles as B and more" | log_056
2026-08-22 | The ten-language gate LIFTED, in conversation: "im gonna fall asleep soon. if you want to initialize those other runs for the remaining languages, we can review the results when im back on the laptop." COVERED: generating and running the lanes unattended. NOT COVERED: folding results into any matrices, drawing conclusions, or ruling which scoring is THE weight | log_058 postscript, log_059 correction
2026-08-22 | "if you can migrate from SandboxDesign to Airlock for PCHQ — and the Claude skill if needed — yes please." The sandbox of record for this line is `~/Programming/Airlock` as of 2026-08-22 | log_060
2026-08-22 | SandboxDesign is NOT retired, NOT modified and NOT moved by the migration; it still works | log_060
2026-08-22 | The sandbox CPU default is FULL (6) and the user throttles as they see fit | Airlock MIGRATING.md §2
2026-08-22 | Staging ruling: extend the Cartesian run from rust+ruby to exactly TWO more first — python for the interpreted shape, go for the compiled shape — and prove both before eight more emitters are written | log_061
2026-08-23 | Greenlit running swift's `&+` / `&-` / `&*` at both levels | log_066
2026-08-23 | Three relations separated after wearing one word: CONTAINMENT (directed, transitive, decided by value agreement at every key where the narrower answers), ACCUMULATION (a union, decided by SHARED INTENTION), FRACTURE (a similarity judgement) | log_067
2026-08-23 | ACCUMULATION's licence is SHARED INTENTION, never measured overlap — overlap is neither sufficient nor necessary | log_067
2026-08-23 | php's third guaranteed add is NAMED `approximating` — "approximating is fine." The three guaranteed adds are `wrapping`, `growing`, `approximating`; `unspecified` is not a fourth add, it is the record that no add guarantee was chosen | log_067
2026-08-23 | The disagreement-kind classifier RULED — "looks good! lets do it": WINDOW-only means SAME family, record the window as the profile's RANGE, never as a mode; VALUE-only means DIFFERENT modes, the disagreeing cells define the boundary; MIXED applies the region test; UNDESCRIBABLE flags for the owner. No threshold anywhere | log_069
2026-08-23 | Input gating is by FORM, never by holder | log_070
2026-08-24 | The proof must be the actual graph AS DATA with the proof a mechanical path query over it — no interpretation in the loop; a query either follows edges to an answer or names the exact node where the path dies | log_072
2026-08-24 | The graph is over what the compiler is WRITTEN IN, never over what it DOES | log_072
2026-08-24 | Vocabulary settled: TRACE is the weak form (machinery walked and cited); SLICE is the strong form (logic extracted into the hub as usable parts) | log_072
2026-08-24 | Challenge sustained on indirect calls: statics nearly always names the CANDIDATE SET, so the edge is one-to-many and still built by edge-following; it degrades to a true frontier only when the set is uncomputable | log_072
2026-08-24 | The static-runtime join: run the compiler on OUR authored probe and observe which nodes execute; each one-to-many edge that ran collapses to the member that ran | log_072
2026-08-24 | RULED IN: the machinery is LANGUAGE-AGNOSTIC — dispatch on file extension to the matching grammar, one multi-language graph; probes automate from `operator_arity.json`, never hand-written | log_072
2026-08-24 | Go first for the first compiler-graph build | log_072
2026-08-24 | The runtime record is a DIARY, never a tally — order preserved; the coverage tally is a stopgap and its output must never be presented as a trace | CORE_0_3_5
2026-08-24 | Never key on spelling; two operators are the same only by machine-form equivalence. The spelling-keyed matrix of that day was a defect, ruled then | CORE_0_3_5
2026-08-24 | Coding discipline: no complex statements — if a statement can be split into multiple lines, split it | CORE_0_3_5
2026-08-24 | The anchor/ship/diff layering RULED IN — "weve found our solution": ANCHOR is the un-optimized build where identity is observable by contract, SHIP is the optimized build, DIFF measures exactly what the optimizer changed | log_073
2026-08-26 | CPython ruled first for the interpreter track | SUPPORT_scaling_design.md
2026-08-26 | An erased unit RE-RENDERED AS INSTRUCTIONS is canonical form; the erasure of moves was never the problem — the pseudo-step notation was, and it is retired to comments with no role in matching, analysis or presentation | log_075
2026-08-26 | Transformation is allowed; DISAPPEARANCE is not. A valid simplified expression must be rendered BACK into canonical runnable instructions — "a result that cannot return to canonical form is not a result, it is an intermediate" | log_075
2026-08-26 | The canonical form is the HOME REPRESENTATION: the default material for matching, analysis and presentation. Other representations are kept but are derived views | log_075
2026-08-26 | Statement of the canonical form, his words: normalized arch opcodes; standardized designated registers for traced variables and all others; each call on its own line; canonical form of arch-units runnable with their standardized and normalized context | log_075

Two further items were ratified by silence rather than said, and both
remain overturnable: the partially-loaded-holders default (a typed slot
that loaded only some of its value classes is probed with the values that
did load), and the congruence floor at `w >= 8`.

---

## §3 — what is open and awaiting the owner

Grouped by what a decision would unblock. Every line names its log.

**Structural, blocking construction**

- A fourth disagreement KIND, or a ruling that a decline-vocabulary difference is not a disagreement — 482 pairs disagree only in which decline they gave and under the classifier as ruled have no kind | log_069, log_070, log_071
- Is WINDOW-only merging transitive? By component it merges the three named adds into one group of 96 profiles; by maximal clique the same block gives 42,324 groups — a cover, not a partition | log_070, log_071
- Whether `wrapping` at 32 and at 64 bits is ONE mode — the all-cells reading splits it into 6 parts by width, signedness and argument order | log_068
- Whether `rust_release` becomes its own operator node, and how it interacts with the compatibility gate, containment and the mode partition | log_057, log_068
- Whether `swift_wrap` stays a separate language tag or is merged into `ops("swift")` proper | log_066
- Which relation each remaining ontology rule governs — the graded weight, the input-overlap criterion and the decline rule are still untagged | log_067
- Whether a floor on `n_comparable` should exist, and where — 4,279 of 58,223 external connectors rest on four or fewer comparable keys | log_051, log_053

**The naming and vocabulary gaps**

- THE VOCABULARY GAP MAP, in the priority log_070 gives it: (a) the three shift/bit camps have NO NAMES — 244 families, 480 profiles, the largest single gap; (b) the single `float` name covers at least three contracts; (c) the SIGN OF ZERO; (d) mixed-signedness reinterpretation, 16 c++ families; (e) `**` has no census entry at all, 20 families across 4 languages; (f) comparison operators — 316 whole-by-whole families with no guarantee vocabulary anywhere | log_070
- A FOURTH guaranteed arithmetic mode beside `wrapping`/`growing`/`approximating`, for rust's algebraic float methods. Candidate name `rearranging` (what happens to the answer, per the owner's own principle) against rust's own word `algebraic` (the origin-naming rule). Ingress would record it, never `unspecified`; the egress bridge runs ONE WAY | log_076
- Is php's float-fallback overflow a third candidate arithmetic mode, or does it belong under declines and casts? | log_064
- Is the ruby `Rational`/`BigDecimal` precision-budget add a guarantee — and therefore a mode, and therefore his to name — or an implementation detail of BigDecimal's limb arithmetic? Measured as REAL ruby, not a canon artefact, predicting 289/289 cells in both orders | log_068, log_070

**Scope**

- type_vocabulary step B: which of the 59 union entries become instruments. Also whether the twelve MACHINERY entries are out of scope wholesale (would drop the union to 47), and whether the `integer`/`bigint` split stands | log_022
- Whether to open the METHOD/BLOCK scope question — 13 candidates found; "builtins are out of scope until the owner opens it" stands unless he opens it | log_065
- Whether `java.>>` and `java.>>>` forming one vector class needs a negative whole value class added — a probe-space question | log_043
- The dict gap in five languages and the boolean gap in kotlin: record unmeasurable, or open a narrow exception for one constructor per missing dominant | log_021

**Canonical form and the compiler graph**

- Canonical coverage for the 827 compound-assignment member slots; the 941 unmodeled operations blocking return paths; the 80 named canonical refusals | log_075
- Evidence ranking: canonical text primary with assembled bytes as its verification, unless the owner wants them kept as separate grounds | log_075
- The compiler-graph open list: the allocator's choice on the ship build; goroutine id in diary records; a second language on unchanged machinery; 9,923 selector refusals remain, 282 of them naming an out-of-region package | CORE_0_3_5

**Carried forward, unresolved**

- The `ctypes.c_int64 + ctypes.c_int64` expected-string discrepancy: the run gives one triple, the owner's approved example expects another, and the recorded cell yields neither. Either the approved example needs a correction or the recorded cell does. Still the only carried-forward item as of log_048 | log_047, log_048
- Which scoring is THE weight, and at what cut. Log_069's classifier DISSOLVES the question rather than answering it, but nothing has been retired | log_054, log_055, log_056, log_064, log_065, log_068
- Decision 26, the existential holder-to-form answer projection, and decision 27, the product distance — both flagged, both re-readable from stored data without a re-run | logs 031, 033, 034, 035, 041

**Infrastructure, on his hand specifically**

- Is SandboxDesign's daemon meant to be down? | log_076 — and see §5 below, confirmed today
- Whether to bump `Airlock/Containerfile` line 82 from 1.96.1 to 1.98.0. It would REPLACE, not co-install; the image was not rebuilt and the pin was not bumped | log_076
- Whether to repoint the seventeen live `Research/` scripts at Airlock, and if so whether to move the 480 products out of `SandboxDesign/agent/out/` first. Decides where the line's data lives | log_060
- Saving the toolchain skill rewrite — the text is written and ready, see §4.8 | log_060
- Whether typescript's absence from PATH is deliberate | log_076 — refuted in part below, see §5
- Census pages and vectors are the owner's to rule; log_076's proposed fact id F-f2 is not installed and no census page was edited | log_076
- `Research/dominant_intentions` WP3/WP4, or a new census object if he opens one | node_0_3_1 PROGRESS

---

## §4 — infrastructure, organized for the skill rewrite

Everything in this section was produced by running something today,
2026-08-29, except where marked NOT EXECUTED. Two probes were dropped, one
into each lane, and the container answered one of them.

### 4.1 What Airlock is, and what changed

Airlock is a DERIVATION of SandboxDesign, made project-agnostic by
construction and public-ready. It is not a rename and not a replacement.
The derivation is recorded at
`~/Programming/Airlock/DevComms/log_001_airlock_derivation.md`; the
move-across instructions are `~/Programming/Airlock/MIGRATING.md`.

What changed is small and can be said in four lines:

- the repository directory: `~/Programming/SandboxDesign` → `~/Programming/Airlock`
- the command name: `sandbox` → `airlock` (same flags, same refusals, same exit codes)
- the environment variables: `SANDBOX_DESIGN_ROOT` → `AIRLOCK_ROOT`, `SANDBOX_CPUS` → `AIRLOCK_CPUS`; the old spellings are still read, AFTER the new ones
- the CPU default: 3 → 6, the full share, ruled 2026-08-22

What did NOT change, and this is the load-bearing part for a session: the
file protocol is byte-identical, path for path. Every tail under `agent/`
is the same. The status file's field names and atomic write are the same.
The batch manifest format is the same — one written by either tool is read
by the other. Every shell script carries the same name, arguments and
behaviour. The container, network, image and volume names are deliberately
unchanged: `sandbox-runner`, `sandbox-proxy`, `sandbox-internal`,
`sandbox-egress`, `sandbox-persist`, `sandbox-runner:latest`,
`sandbox-proxy:latest`. **Do not search-and-replace those.**

Also removed from the repository, deliberately: `agent/templates/`
altogether (a lane belongs to the project that wrote it), and the
one-person host workflow scripts.

**Is SandboxDesign dead?** No, and this distinction matters. the owner ruled it
NOT retired, NOT modified and NOT moved. It still *works* in the sense that
its files and its 480 recorded products are intact. But its DAEMON is not
running, and today's probe confirms that (see §5). The two installs share
container names and only one may ever be up.

### 4.2 The agent lane, as a recipe

Plain words first. Four host directories are bound into the running
container. A session that can write a file but cannot run podman turns a
file write into a sandbox run: write the script, poll the status file,
read the log, collect the products.

The four directories:

| host path | mounts at | direction | who writes |
|---|---|---|---|
| `~/Programming/Airlock/agent/drop/` | `/drop` | in | the session writes `x.sh` |
| `~/Programming/Airlock/agent/status/` | `/status` | out | the daemon writes `x.sh.status` |
| `~/Programming/Airlock/agent/logs/` | `/logs` | out | the daemon writes `<stamp>__x.sh.log` |
| `~/Programming/Airlock/agent/out/` | `/out` | out | the lane script writes products |

Two more paths a session touches:
`~/Programming/Airlock/agent/batch.json` (the manifest) and
`~/Programming/Airlock/agent/drop/.done/` (where a run's script is archived
once finished).

The recipe, five steps:

1. Write `~/Programming/Airlock/agent/drop/<lane>.sh`. A direct write is
   safe and is the truth underneath — the daemon watches `close_write` as
   well as `moved_to`, so it fires when the writer closes the file, never
   mid-write. The documented front door is
   `python3 ~/Programming/Airlock/airlock submit <lane>.sh --batch <label> --weight <n>`,
   a validating wrapper that refuses ten named ways.
2. Poll `~/Programming/Airlock/agent/status/<lane>.sh.status`. This path
   follows from the script name alone; the log's name embeds a run
   timestamp and cannot be predicted, which is exactly why the status file
   exists.
3. Read `state=running`, then `state=done`.
4. Read the log named in the status file's `log=` field, under
   `~/Programming/Airlock/agent/logs/`.
5. Collect anything the lane wrote to `/out`, which is
   `~/Programming/Airlock/agent/out/` on the host. The SESSION places
   products into the real tree — which is why project mounts can stay
   read-only.

The status file, verbatim from today's run:

```
script=d77_inventory.sh
state=done
exit=0
started=2026-08-29T20:32:16+00:00
finished=2026-08-29T20:32:37+00:00
elapsed_s=20.9
log=/logs/20260829T203216Z__d77_inventory.sh.log
work_free_mb_after=3505
work_consumed_mb=45
verdict=exit 0
```

Field names, unchanged from SandboxDesign: `script`, `state`, `exit`,
`started`, `finished`, `elapsed_s`, `log`, `work_free_mb_before`,
`work_free_mb_after`, `work_consumed_mb`, `verdict`.

Facts a session must respect:

- **Execution is SERIAL.** `run_script()` is called synchronously from a
  single event loop; two lanes dropped together run one after the other.
- **The daemon sweeps the drop folder ONCE at startup** and is
  inotify-driven after that. A lane dropped while the daemon is bound
  elsewhere is never picked up; a restart's startup sweep will collect it,
  in sorted-listing order.
- **A bound daemon writes a status file the instant it starts a lane.** An
  empty status folder beside a non-empty drop folder is decisive evidence
  that the running container is not bound to that tree.
- `SCRIPT_TIMEOUT` defaults to 3600 s. Log_063 observed it NOT being
  enforced, roughly 2,800 s past the ceiling. Do not rely on it.
- `/work` is tmpfs, capped (4.0 G measured today, 3.5 G free), wiped on
  restart. `/persist` is a named volume that survives restarts.
- Only the owner can restart the container (`down.sh` then `up.sh`); podman is
  not reachable from a session.

Operator commands, for the owner at a terminal — NOT EXECUTED by this session,
since podman is host-only:

```
python3 ~/Programming/Airlock/airlock status            # all lanes
python3 ~/Programming/Airlock/airlock status <lane>.sh  # one, renders ABORT for timeout
python3 ~/Programming/Airlock/airlock watch
python3 ~/Programming/Airlock/airlock doctor
bash    ~/Programming/Airlock/progress.sh   (-w to refresh)
bash    ~/Programming/Airlock/batch.sh <label> <lane>.sh:<weight>
bash    ~/Programming/Airlock/down.sh && bash ~/Programming/Airlock/up.sh
bash    ~/Programming/Airlock/allow.sh sync
bash    ~/Programming/Airlock/selftest.sh
```

`progress.sh` is NOT deprecated and NOT replaced. It is the only view that
lists live processes inside `sandbox-runner`; every `airlock` view ends by
pointing at it.

### 4.3 Which lane actually runs today — verified by execution

Two probes were dropped, one into each lane, at the same sitting.

| lane | probe dropped at | answered | evidence |
|---|---|---|---|
| Airlock | `~/Programming/Airlock/agent/drop/d77_inventory.sh` | YES, in 20.9 s | status file written, log at `agent/logs/20260829T203216Z__d77_inventory.sh.log`, exit 0 |
| Airlock | `~/Programming/Airlock/agent/drop/d77_ts_and_pins.sh` | YES, in 11.2 s | status file written, exit 0 |
| SandboxDesign | `~/Programming/SandboxDesign/agent/drop/d77_probe_sbx.sh` | NO | no status file after many minutes; the file still sits in `drop/` |

Corroboration: SandboxDesign's `agent/status/` folder was last written
2026-08-22 03:46 and its newest log is `20260822T073459Z`. Its `drop/`
folder additionally holds ten unrun `d76_*.sh` scripts left by today's
earlier drill. Airlock's newest logs before today were `20260829T172243Z`
from that same drill.

**Conclusion: Airlock is the only lane that answers. SandboxDesign's
daemon is down.** Whether that is intended is the owner's to say.

### 4.4 The verified language inventory

Plain words first: of the thirteen toolchains checked, twelve run and one
does not run from PATH. Six live in the image and six live in `/persist`,
the named volume that survives restarts but is not part of the image and
would be lost if the volume were wiped. The `/persist` six are exactly the
ones a rebuild would NOT restore.

Everything below is the output of `d77_inventory.sh` and
`d77_ts_and_pins.sh`, run 2026-08-29 through the Airlock lane. Container
base is Ubuntu 26.04 LTS, kernel 7.0.0-30-generic.

Container `PATH` as the daemon sets it:
`/opt/cargo/bin:/opt/venv/bin:/usr/lib/go-1.26/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin`

| language | version, as printed | resolved path | image or persist | hello-world |
|---|---|---|---|---|
| python | Python 3.13.14 | `/opt/venv/bin/python3` → `/opt/python/cpython-3.13.14-linux-x86_64-gnu/bin/python3.13` | IMAGE | ran |
| javascript (node) | v22.22.1 | `/usr/bin/node` | IMAGE | ran |
| npm | 11.19.0 | `/usr/local/bin/npm` | IMAGE | n/a |
| typescript | Version 7.0.2 | `/persist/ts/node_modules/.bin/tsc` — **NOT on PATH** | PERSIST | ran, compiled and executed |
| java | javac 25.0.3 / openjdk 25.0.3 | `/usr/bin/javac`, `/usr/bin/java` → `/usr/lib/jvm/java-25-openjdk-amd64/` | IMAGE | ran |
| go | go1.26.0 linux/amd64 | `/usr/lib/go-1.26/bin/go` | IMAGE | ran |
| rust | rustc 1.96.1 (31fca3adb 2026-06-26) | `/opt/cargo/bin/rustc` → rustup shim | IMAGE | ran |
| rust 1.98.0 | rustc 1.98.0 (88d9e12ae 2026-08-18) | `/persist/rustup076/toolchains/1.98.0-x86_64-unknown-linux-gnu/bin/rustc` | PERSIST | ran |
| ruby | ruby 3.3.8 (2025-04-09 revision b200bad6cd) | `/usr/bin/ruby` → `/usr/bin/ruby3.3` | IMAGE | ran |
| php | PHP 8.5.4 (cli) NTS, built Jul 16 2026 | `/usr/bin/php` → `/usr/bin/php8.5` | IMAGE | ran |
| kotlin | kotlinc-jvm 2.3.21 (JRE 25.0.3) | `/persist/kotlinc/bin/kotlinc` — **NOT on PATH** | PERSIST | ran |
| c++ | g++ (Ubuntu 15.2.0-16ubuntu1) 15.2.0 | `/usr/bin/g++` → `x86_64-linux-gnu-g++-15` | IMAGE | ran |
| c++ (clang) | Ubuntu clang version 21.1.8 (6ubuntu1) | `/usr/bin/clang++` → `/usr/lib/llvm-21/bin/clang` | IMAGE | n/a |
| c | gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0 | `/usr/bin/gcc` → `x86_64-linux-gnu-gcc-15` | IMAGE | ran |
| dart | Dart SDK 3.13.0 (stable), 2026-08-05 | `/persist/dart-sdk/bin/dart` — **NOT on PATH** | PERSIST | ran |
| csharp | .NET SDK 10.0.400 | `/persist/dotnet/dotnet` — **NOT on PATH** | PERSIST | ran, `dotnet new console` + `dotnet run` printed Hello, World! |
| swift | Swift version 6.0.3 (swift-6.0.3-RELEASE) | `/persist/swift/usr/bin/swift` — **NOT on PATH** | PERSIST | ran |

**The rule a session must carry: six of the thirteen are `/persist`-only
and none of them is on PATH.** Any lane script that says `kotlinc`,
`swift`, `dart`, `dotnet` or `tsc` bare will fail with command-not-found.
Use the absolute paths above.

`/persist` also holds, beyond the toolchains: `cpython`, `cpython_anchor`,
`cpython_ship` (the interpreter track's three builds), `gosrc` and
`gocache` (the instrumented Go toolchain for the compiler-graph campaign),
`compile_cov`, `compile_diary`, `compile_diary2`, the `interp_*` trees,
`/persist/tv/ts5` (a second, older typescript), `/persist/cargo076`, and
`/persist/dotnet-csc-build.sh` + `/persist/dotnet-csc-run.sh` (the
network-free c# compile helpers that bypass NuGet restore).

One image-level fact worth carrying: the swift `libncurses` symlink
(`/usr/lib/x86_64-linux-gnu/libncurses.so.6` →
`libncursesw.so.6.6`) EXISTS right now, dated 2026-08-29 17:21 — it was
reapplied during today's earlier drill. It is not persisted across
container restarts and is not in the image; it must be reapplied per
container lifetime until folded into the image build.

**csharp is not blocked.** The 2026-08-13 census recorded it as
deliberately out; log_062 found .NET present in `/persist` and today's run
compiled and executed a console project with no network. The census's
"csharp deliberately absent" line describes a decision, not the container.

**dart is not blocked either.** The 2026-08-13 PROGRESS entry recording
`storage.googleapis.com` as blocking dart is now stale: googleapis was only
ever needed to INSTALL the SDK. The SDK is installed, at `/persist/dart-sdk`,
and it runs. (googleapis IS still refused through Airlock's proxy — see
§4.5 — but nothing needs it.)

### 4.5 Egress allowlist

Plain words: the proxy denies everything by default and permits only what
a per-machine text file names. That file is instance state, gitignored, and
is NOT the same file in the two repositories — Airlock's copy was never
brought across from SandboxDesign.

- **Live file:** `~/Programming/Airlock/proxy/allowlist.txt`
- **Template:** `~/Programming/Airlock/proxy/allowlist.txt.example`
- **Old file, no longer live:** `~/Programming/SandboxDesign/proxy/allowlist.txt`
- If the live file is missing entirely, `airlock doctor` reports a FAULT
  and the proxy refuses everything.

**How a session adds a host, and where the owner's hand is needed.** A session
may append the entry directly — the allowlist is the session's to manage —
but the RELOAD runs podman and is host-only. So:

1. Append the hostname to `~/Programming/Airlock/proxy/allowlist.txt`, with
   a LEADING DOT so subdomains match (`.example.com` matches
   `files.example.com`).
2. Ask the owner for one command:
   `bash ~/Programming/Airlock/allow.sh sync`.
3. Design probe scripts to report cleanly when the proxy has not yet
   reloaded — the observable is HTTP 000 or 403, not an exception.

`allow.sh add <host>` does both steps at once but is host-only, since it
calls `podman cp` and `squid -k reconfigure`. `allow.sh denied` names what
the proxy has refused; also host-only.

**What is on Airlock's live list today** (verified by reading the file and
by curl from inside the container): the Ubuntu archives
(`.ubuntu.com`, `.archive.ubuntu.com`, `.security.ubuntu.com`,
`.canonical.com`); python (`.pypi.org`, `.pythonhosted.org`, `.astral.sh`);
rust (`.crates.io`, `.static.crates.io`, `.rust-lang.org`); go
(`.proxy.golang.org`, `.sum.golang.org`, `.golang.org`, `.go.dev`); node
(`.registry.npmjs.org`, `.npmjs.org`, `.nodejs.org`); java and kotlin
(`.repo1.maven.org`, `.maven.org`, `.gradle.org`); source hosting
(`.github.com`, `.githubusercontent.com`, `.gitlab.com`, `.swift.org`,
`.download.swift.org`).

Measured from inside the container today:
`static.rust-lang.org` → 200, `registry.npmjs.org` → 200,
`github.com` → 200, `storage.googleapis.com` → 000,
`example.com` → 000. The deny path works.

**A drift worth flagging.** Airlock's live allowlist is byte-for-byte the
`.example` template — 832 bytes, identical size. SandboxDesign's is 1,153
bytes and carries two extra blocks the migration never copied:
`.googleapis.com` (the dart SDK, staged 2026-08-14 and synced) and the six
.NET SDK entries (`.dot.net`, `.microsoft.com`, `.azureedge.net`,
`.dotnetcli.blob.core.windows.net`, `.builds.dotnet.microsoft.com`,
`.download.visualstudio.microsoft.com`, staged 2026-08-17). MIGRATING.md
step 2 says to copy the allowlist across; that step was not done. Nothing
currently needs either block — both SDKs are already installed in
`/persist` — but a session that assumes the old list is live will be wrong.

### 4.6 Version pins a session must respect

Plain words: there is exactly one place rust's version is pinned, and it
is a single line in the container build file. Nothing else in the estate
pins rust at all — searched for and not found: a `rust-toolchain` file, a
`Cargo.toml`, a `rust-version` key, or a rust version string in any
research script under PseudoCoupHQ.

| what is pinned | file | line | value |
|---|---|---|---|
| rust, in the image | `~/Programming/Airlock/Containerfile` | 82 | `--default-toolchain 1.96.1` |
| rust, in the old repo (not live) | `~/Programming/SandboxDesign/Containerfile` | 79 | `--default-toolchain 1.96.1` |
| go, by apt package and PATH | `~/Programming/Airlock/Containerfile` | 32 | `/usr/lib/go-1.26/bin` |
| gcc / g++ / clang / lld / llvm | `~/Programming/Airlock/Containerfile` | 21 | `gcc-15 g++-15 clang-21 lld-21 llvm-21` |
| openjdk | `~/Programming/Airlock/Containerfile` | 26 | `openjdk-25-jdk-headless` |
| npm major | `~/Programming/Airlock/Containerfile` | ~76 | `npm install -g npm@11`, never fatal |
| tree-sitter, grammar pin check | `~/Programming/PseudoCoup_v6/Tools/ledgerer/tree_sitter/test_tree_sitter_base.py` | — | tree-sitter 0.26.0, tree-sitter-rust 0.24.2, tree-sitter-python 0.25.0, tree-sitter-cpp 0.23.4 (12 checks, pass) |
| tree-sitter, compiler graph | `~/Programming/PseudoCoupHQ/Research/compiler_graph/build_graph.py` | 12 | tree-sitter == 0.26.0; also tree-sitter-go 0.25.0, Go tree commit 9f1012d9 (1.28-dev), provenance UNVERIFIED |
| tree-sitter, operator arity | `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.py` | 1127 | cross-check note: `tree-sitter==0.26.0` |
| rustc token alphabet, transcribed | `~/Programming/PseudoCoup_v5/Research/differential_alphabet.py` | — | 53 rustc `TokenKind` punctuation names, fetch-dated 2026-08-12, **no refresh path** |

Bumping line 82 would REPLACE 1.96.1, not co-install beside it. The image
was not rebuilt today and the pin was not bumped. The 1.98.0 toolchain
that exists lives outside the image at `RUSTUP_HOME=/persist/rustup076`,
survives restarts, and would be lost if `/persist` were wiped.

Tuning constants a session must also respect, in
`Research/kind_fuzz_clustering/l3_cart_gen.py`: `RUBY_STALL_S = 2.0`
(reduced from 10.0), `PHP_STALL_S = 2.0`, python's stall budget 0.5 s,
`STATIC8_STARTUP_S = 60.0` and `STATIC8_STALL_S = 15.0` (both chosen, not
measured), the c++ chunk cap at 8,000 (raised from 2,000, measured), and
swift's chunk at 400.

### 4.7 Project entry points that changed since 2026-08-14

`~/Programming/PseudoCoupHQ/Research/` had two folders and now has eight.
One line each, with the main runnable script.

| folder | what it is | main runnable |
|---|---|---|
| `kind_signature_clustering/` | The 2026-08-12 line, renamed from `kind_clustering` on 2026-08-15 to say what it clusters — declaration-derived signatures from `node-types.json`. | `features_all.py` → `cluster.py` → `validate_all.py`; explorer via `make_explorer_all.py` |
| `kind_fuzz_clustering/` | The layer-3 campaign's home and by far the largest — probe generation, acceptance, execution, answers, clustering, boundaries, the Cartesian grids, the family graph. 454 files. | `run_all_languages.sh` (see below); per-stage `l3_*.py`, notably `l3_cart_gen.py`, `l3_cart_read_v2.py`, `l3_dominance.py`, `build_family_graph.py` |
| `type_vocabulary/` | The twelve languages' own closed type enumerations, unioned into 59 entries. Step B has not run. | `python3 .../type_vocabulary/union.py` |
| `data_representation/` | Layer 1 (the shared data forms) and layer 2 (per language, the shapes that can hold each form), plus the 328-cell audit. | `audit_generate.py` then `audit_classify.py` |
| `compiler_graph/` | The compiler's own source turned into a graph, and the path query that proves a variable reaches a register. Five laps on Go. | `build_graph.py`, then `resolve_dots.py` / `resolve_dots2.py` / `fix_bindings.py` / `flow_forward.py`, then `query_path.py`; `inject_diary.py` for the diary |
| `op_pipeline/` | The arch-unit and canonical-form pipeline: probe manifests, arch units, canon generations 1 through 13, dominant tables, behaviour checks. 337 files, the most actively churned folder in the estate. | latest generation `canon13.py` + `canon13_render.py`; `dominant_table12.py`; lanes under `op_pipeline/lanes/` |
| `stage_asg/` | A staged snapshot of the ASG-stage work carried out of `op_pipeline` — canon units, verdicts, semantic anchoring, the z3 extension. 40 files. | `canon.py`, `verdicts3.py`, `sem_anchored.py`, `z3_ext.py` |
| `dominant_intentions/` | Unchanged in shape: the five census pages, the harness that verifies them by execution, and the verified results. | `harness/generate_run.py --vectors vectors_<object>.json` then `harness/compare.py` |

Run-everything scripts, both current:

- `~/Programming/PseudoCoupHQ/hq.sh` — the planning-tree check;
  `bash ~/Programming/PseudoCoupHQ/hq.sh check` reports 0 errors and is the
  gate every housekeeping pass runs before and after.
- `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/run_all_languages.sh`
  — new on 2026-08-22 (log_062). Submits every Cartesian lane for the
  remaining eight languages, in the one order that is safe, through the
  validating CLI, then watches status files. It never starts, stops or
  restarts podman and never runs a probe itself. Its companion document
  `RUN_ALL_LANGUAGES.md` is addressed to the owner alone, at a terminal, with no
  session open.

### 4.8 The skill rewrite is already largely drafted

Two files exist that the rewrite should start from rather than duplicate:

- `~/Programming/Airlock/DevComms/toolchain_skill_airlock_patch.md` — the
  exact replacement text for each affected section, quoted old against new,
  in file order, with a twelve-block table. Written 2026-08-22.
- `~/Programming/Airlock/DevComms/toolchain_SKILL_updated.md` — a complete
  478-line replacement skill, frontmatter included. The frontmatter is
  deliberately UNCHANGED, on the reasoning that the description is the
  trigger text and changing it risks changing when the skill fires for no
  gain.

Both were written because the cached copy a session can see is read-only:
writing to it does not change the saved skill. Applying either needs the
skill-save mechanism, which is why log_060 left it on the owner's list.

**However, the drafted §3 is now materially wrong** against today's
measurement, and the rewrite must correct it:

- it lists Kotlin, Swift, Dart and .NET as "absent, verified against the
  Containerfile" — all four are present in `/persist` and all four ran
  hello-world today;
- it does not mention typescript at all, which is present in `/persist` at
  7.0.2 and works;
- it does not list ruby or php, both of which are in the image and both of
  which ran (this is the present-but-unlisted drift the 2026-08-14 PROGRESS
  entry already flagged and which was never closed);
- the distinction it needs and does not draw is IMAGE versus PERSIST — six
  toolchains would not survive a `/persist` wipe and none of the six is on
  PATH.

---

## §5 — the three drift items log_076 flagged

**Item 1 — SandboxDesign's daemon. CONFIRMED.** A trivial probe,
`d77_probe_sbx.sh`, was written into
`~/Programming/SandboxDesign/agent/drop/` today. No status file appeared.
The same sitting's probe into `~/Programming/Airlock/agent/drop/` was
answered in 20.9 seconds with exit 0. SandboxDesign's status folder was
last written 2026-08-22 03:46 and its newest log is 20260822T073459Z; ten
unrun `d76_*.sh` scripts from today's earlier drill are still sitting in
its drop folder, joined now by mine. The daemon is down. Whether that is
intended is the owner's to say; the probe file was left in place as evidence.

**Item 2 — typescript's disappearance. PARTLY REFUTED, and the correction
matters.** typescript has NOT vanished. `tsc` is not on the container's
PATH, which is what log_076 observed and correctly reported as ABSENT under
the command it ran. But the installation of 2026-08-14 is intact at
`/persist/ts/node_modules/.bin/tsc`, a symlink to
`../typescript/bin/tsc`, dated 2026-08-17 13:34, and
`/persist/ts/node_modules/typescript/package.json` reports
`"version": "7.0.2"` — the exact version the census recorded. Run today by
absolute path it printed `Version 7.0.2`, compiled a typed hello-world with
no diagnostics, and node executed the emitted JavaScript. A second, older
typescript also exists at `/persist/tv/ts5/node_modules/typescript/bin/tsc`.

The real finding is narrower and more useful than "a toolchain vanished":
**the 2026-08-14 install was a global npm install whose PATH entry did not
survive, while the payload did.** `npm root -g` today is
`/usr/local/lib/node_modules` and contains only `npm`. So log_076's
consequence still holds — the census's one REFUTED cell (bool-U4,
typescript, TS2367) could not be re-measured under the command used — but
it is now re-measurable, by pointing at
`/persist/ts/node_modules/.bin/tsc`. That is a one-line PATH change, the
same shape as the rust 1.98.0 fix log_076 itself used.

**Item 3 — `lane_bf.sh` regenerating 126 lines different. CONFIRMED
EXACTLY.** `generate_run.py` was run against the UNCHANGED
`vectors_boolean_float.json` into a scratch copy, and the output diffed
against the committed `lane_bf.sh`. Result: 126 changed lines, 63 removed
and 63 added — log_076's number to the line. Of the removals, 24 are the
`<compile-error>` verdict refinement the generator no longer emits:

```
<       if [ "$(grep -c "|" run.out)" = 0 ]; then VERDICT="<compile-error>"; else VERDICT="<aborted>"; fi
---
>       VERDICT="<aborted>"
```

The remaining 39 are c++ probe lines whose template shape changed. The
generator is not a fixed point on its own committed lane, and regenerating
right now would silently drop a verdict refinement in 24 places. Log_076's
remediation item 3 stands: make the generator a fixed point, and add a
check that regenerating a committed lane reproduces that lane.

---

## §6 — what could not be verified, and why

- **Any host-side command.** This session can write files under
  `~/Programming` and drive the container through the lane, but cannot run
  podman, systemd or the `airlock` CLI. So the operator commands in §4.2 are
  quoted from `README.md`, `MIGRATING.md` and `agent/README.md`, not run.
  The file protocol underneath them WAS run, twice, and that is what the
  §4.2 recipe rests on.
- **Whether the quadlet units were re-installed after the migration.**
  MIGRATING.md is explicit that the systemd path needs a re-install because
  SandboxDesign's unit hardcoded four volume lines. A container is plainly
  up and bound to Airlock's folders, so something is correct; which of the
  two start paths is live could not be read without host access.
- **Whether SandboxDesign's daemon being down is deliberate.** Confirmed
  down by execution; the intent is not something a probe can measure.
- **The `<compile-error>` refinement's provenance.** The regeneration diff
  proves the drift and its direction. Which change to `generate_run.py`
  removed the refinement, and whether that removal was deliberate, was not
  chased — it is a git-history question on a file last touched 2026-08-14.
- **The 39 c++ template lines in the same diff.** Counted and located, not
  read for meaning.
- **`airlock doctor` and `selftest.sh` output.** Both would sharpen §4.5's
  allowlist finding; both are host-only.
- **Whether typescript's absence from PATH is deliberate.** Refuted as a
  disappearance; the intent behind the missing PATH entry is unknown.
- **The DevComms logs 021-076 were read at §1 only**, as briefed, plus
  logs 060 and 076 in full and a whole-file grep of all of them for
  rulings. A ruling stated only in a later section of an unread log, and
  nowhere near any of the searched words, would have been missed. The
  ruling list in §2 was cross-checked against the sub_node PROGRESS files
  and against `CORE_0_3_5_compiler_graph.md`, which supplied several
  standing rules the logs state only in passing.
- **`Planning/node_0_3_research/PROGRESS.md` itself stops at 2026-08-19.**
  The research node's own PROGRESS has not been written to in ten days even
  though four of its sub_nodes have. Its CHECK still carries one open item,
  the kind_signature_clustering pack generator, whose rulings were done
  2026-08-12. Flagged, not fixed — a super-node's PROGRESS is not this
  session's to write.

---

## artifacts this log left behind

- `~/Programming/Airlock/agent/drop/.done/…d77_inventory.sh` and
  `…d77_ts_and_pins.sh` — the two probes, archived by the daemon.
- `~/Programming/Airlock/agent/logs/20260829T203216Z__d77_inventory.sh.log`
  — the full language inventory, verbatim.
- `~/Programming/Airlock/agent/logs/20260829T203340Z__d77_ts_and_pins.sh.log`
  — the typescript and rust-1.98.0 follow-up.
- `~/Programming/SandboxDesign/agent/drop/d77_probe_sbx.sh` — left in place
  deliberately, as standing evidence that the lane does not answer.

Nothing under `Research/`, `Planning/` or any census page was edited.
