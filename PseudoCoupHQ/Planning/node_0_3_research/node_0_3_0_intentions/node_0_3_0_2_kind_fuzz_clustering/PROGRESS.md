---
id: hq.research.kind_fuzz_clustering.progress
status: living
---

# PROGRESS — kind_fuzz_clustering

- 2026-08-21 (log 053): **THE ROW GRAPH REBUILT — INPUT-KEY ALIGNMENT,
  CONTRACT, GROUP.** Assembly only, no probe run; `matrices_cart/` is
  untouched and the v3 products stay on disk for the audit.
  **CHANGE 1, a real defect fixed.** v3 compared two rows only when
  their ENTIRE input vectors were byte-identical, so rows that ran
  dozens of the same input pairs on different holders were declared
  incomparable. The comparable set is now the **INTERSECTION of the two
  rows' INPUT KEYS** — level 1 keyed by `(x0,x1)`, level 2 by
  `(x0,x1,x2,x3)`, operands identified by their globally unique
  spelling, positions found through the probe-index rule of
  `index.json`. Declines still leave numerator and denominator both;
  **zero comparable keys still means NO connector**; **level 1 is never
  mixed with level 2** and every connector records its level. Counted on
  raw row pairs: v3 saw **143,895** comparable of which **75,170** had a
  connector and **68,725** had none; v4 sees **447,074** comparable,
  **247,357** with a connector, **199,717** with none. **172,187 row
  pairs gain a connector (+229.1 %), every one of them outside the v3
  universe altogether**; inside the v3 universe the two rules agree
  exactly. n_comparable over the pairs that carry one: min 1, median
  238, p90 8,100, max 10,000, mean 1,403.
  **CHANGE 2, two kinds of collapse kept distinct.** **CASE 1 CONTRACT**
  is identity — same input key set, byte-identical outputs at every key
  — an equivalence relation, so transitive and needing **no clique
  test**: **2,601 raw rows → 1,041 contracted nodes**, 400 carrying more
  than one row. Both of the owner's expectations hold: `ruby.&&`+`ruby.and`
  land in ONE node **32 times** and `ruby.||`+`ruby.or` **32 times**,
  and **165 contracted nodes span three or more of ruby's four numeric
  holder spellings**. `C0975` contracts ruby's nine `==` rows, nine
  `===` rows and rust's `i64 == i64` and `i128 == i128` into one node
  across the languages. **CASE 2 GROUP** is a **MAXIMAL CLIQUE** of
  mutual exact-1.0 over PARTIAL overlaps — complete linkage, **never a
  connected component** — and it is a **CONTAINER, NOT A MERGE**:
  **2,041 exact-1.0 node pairs → 449 groups**, sizes 21 down to 2, 843
  nodes in a group and 210 in more than one, minimum overlap median 30.
  `G170`–`G173` group rust `f32` with ruby `Float` and `Rational` for
  `+ - * /` at level 2 on a 144-key floor — **the finding the alignment
  fix bought, since v3 could compare `f32` with nothing at all.**
  **The TRANSITIVITY HAZARD is measured, not assumed: 7,212 triples
  with A~B = 1.0 and B~C = 1.0 but A~C not 1.0** (6,714 below 1.0 on
  shared keys, 498 with no comparable key). None is merged and none is
  grouped. Graph: **1,084 nodes** (1,041 contracted + 43 central),
  **59,599 connectors** (1,376 internal, 58,223 external); components
  EXTERNAL-ONLY, expanded view exact 643 / 586 / 480 and graded 597 /
  497 / 371 at 0.95 / 0.85 / 0.70, collapsed view 365 / 353 / 301 and
  347 / 303 / 243. `row_graph_explorer_v4.html` draws groups as
  **enclosing hulls** that collapse and expand on click, labels
  contracted nodes with their member count, and preserves every earlier
  fix (exact/graded checkbox, sigmoid sliders, threshold cutting
  external connectors only, near-zero internal springs, autofit once and
  never again, fit view). `verify_row_graph_v4.js` **ALL CHECKS
  PASSED** — the contraction and the alignment both re-derived
  independently in JavaScript from `matrices_cart/` (36,338 level-1
  connectors exhaustively), every group proved a true maximal clique,
  the transitivity count recounted, and the live counters checked
  against a union-find in both scorings AND both view modes. NOT
  decided: whether a floor on `n_comparable` should exist (4,279
  external connectors and 145 groups rest on 4 or fewer shared keys,
  mostly through the `0`/`1` spellings shared by the whole set and
  ruby's six-point truth set — recorded on every connector so a floor
  can be applied later without rebuilding), and, unchanged from log 052,
  which of the two scorings is THE weight.

- 2026-08-21 (log 052): **THE CARTESIAN PROBE DESIGN, RUN** — rust and
  ruby only; the other ten wait. `SUPPORT_conversion_spec.md`'s section
  "the probe design settled 2026-08-21" is now marked RUN and carries
  the sets used. **Level 1** `y = op(x0, x1)` over ALL ordered pairs of
  a shared `X` (whole 17 spellings, fractional 16, truth 6 — truth is
  new, and its non-boolean members `0`, `1`, `""`, `nil` are the point).
  **Level 2** `z = op(op(x0,x1), op(x2,x3))` over `X'` (10, 10, 6),
  **the intermediates never enumerated, deduped, capped or unioned**.
  A value a holder cannot represent is ABSENT, never coerced — 2,202
  absences recorded per row family. `and` and `or` joined the ruby menu
  (24 operations) because the design's own sanity check needs them.
  **10,042,779 probes: rust L1 20,531 / L2 626,128 (432 chunk files,
  432 compile invocations, 159.1 s compiling against 1.9 s executing,
  0 build failures, 0 ABORTs); ruby L1 259,584 / L2 9,136,536 (0 files
  compiled, 5 workers, 1,645 processes, 2,347 s wall of which 3,280 s
  of worker-time is the 2 s stall budget — cut from 10 s, a recorded
  change that loses no measurement because a stall is an ABORT and an
  ABORT is never scored — and 1,640 ABORTs, all `**` stalls).** All
  10,042,779 probes measured; coverage checked, not assumed. Products:
  `matrices_cart/` (85 CSVs, 2,601 rows, 0 dirty cells) and the v3
  graph — **2,644 nodes (2,601 row + 43 central), 74,860 connectors
  (2,601 internal, 72,259 external)**, 59 comparable groups, 68,725 row
  pairs with NO connector because nothing comparable survives the
  decline rule. **BOTH scorings ride on every connector and neither is
  chosen**: exact-match rate and the ruling-A graded similarity;
  components EXTERNAL-ONLY — exact 1,873 / 1,774 / 1,678 and graded
  1,857 / 1,699 / 1,573 at 0.95 / 0.85 / 0.70. Sanity: **ruby.&& ~
  ruby.and and ruby.|| ~ ruby.or hold at 1.0000 at BOTH levels** (the
  positive control), **ruby.&& ~ ruby.|| separates** (exact 0.0345 mean
  at L1, 0.0601 at L2), and the projection is visible in the data —
  `&&` answers the RIGHT operand at 26 of 36 truth positions, `||` the
  LEFT at 26 of 36, with `0` truthy so `0 && true` answers `true` and
  `0 || true` answers `0`. `row_graph_explorer_v3.html` is
  self-contained with an exact/graded checkbox, sigmoid midpoint and
  steepness sliders (steepness 0 IS the raw graded score), the
  external-only threshold, near-zero internal springs and once-only
  autofit; `verify_row_graph_v3.js` passes every check, re-deriving
  both weights independently in JavaScript. **Awaiting the owner: which
  scoring is THE weight and at what cut, the sigmoid defaults, and the
  boolean-composition denominator (measured 1/6 at L1 and 1/18 at L2
  over the six-point truth set against the 2/16 predicted for the
  two-point boolean one; restricted to the boolean sub-square it is the
  predicted 2 of 4).**
- 2026-08-21 (log 051): **ELEMENT SIMILARITY, DECLINES OUT OF SCORING,
  AND THE DIAGONAL BROKEN** — the owner's rulings A–E, settled and recorded in
  `SUPPORT_conversion_spec.md`. Similarity is now PER ELEMENT and
  NUMERIC over `[sign, mant, expo]` (sign distance /2, mant distance
  already bounded by 1, expo through a `1/(1+d)` decay, combined
  EUCLIDEAN — every knob a single constant in the new `l3_row_sim.py`),
  behind a total FORM CLASSIFIER rather than cast-and-catch. **Declines
  are not scored at all**: a position where either row is `REFUSE` /
  `RAISE:*` / `ABORT` leaves the numerator AND the denominator, and
  **63,467 cross-operator row pairs that share an input ladder now have
  no connector at all** because nothing comparable is left. Two probe
  runs broke the diagonal: **C1 shifted** (`x_k OP x_{(k+1) mod 32}`)
  and **C2 one-level composition** (`op(op(x,x'), op(x,x'))`), emitted
  as additional rows in `matrices_interval_c/` — 1,810 rows, the
  diagonal rows untouched. **rust: 7,232 probes, 5 chunk files, 5
  compile invocations, 1.821 s compiling against 0.018 s executing,
  1.853 s wall, 0 build failures. ruby: 50,688 probes in one process,
  0 files compiled, 556.80 s wall of which 550.00 s is the 10 s
  inactivity budget on 55 `**` stalls and 6.80 s is actual
  evaluation.** The graph is rebuilt: **2,757 nodes (2,718 row + 39
  central; diagonal 908 / shift 908 / comp1 902), 73,080 connectors
  (2,718 internal, 70,362 external)**, 224 distinct input ladder pairs,
  components counted EXTERNAL-ONLY — 1,867 at t=0.95, 1,824 at t=0.85,
  1,684 at t=0.70. **The all-decline ruby cluster is gone** (0
  connectors among `&`,`|`,`^`,`<<`,`>>`,`=~` on
  Float/Rational/BigDecimal against 11,805 comparable pairs before;
  `ruby.=~` now has no connector anywhere), and the largest component at
  t=0.85 is 86 value-carrying nodes over 12 cross-language `lang.op`.
  `row_graph_v2.json` + `row_graph_explorer_v2.html` (self-contained,
  internal springs 0.0008 against external 0.0060, carrying 3.44 % of
  the spring impulse); `verify_row_graph_v2.js` re-implements ruling A
  in JavaScript and re-derives all 70,362 weights, worst disagreement
  5e-7. Four questions await the owner — chiefly that ruling A and ruling C
  pull against each other (`rust.+ ~ rust.-` rose from 0.0312 to 0.17
  diagonal and 0.52 shifted, because `a+b` and `a-b` are numerically
  close), and that the ruby `**` stall budget is now 98.8 % of the ruby
  wall clock.

- 2026-08-21 (log 050): **THE TWO-TIER ROW GRAPH IS BUILT AND
  VERIFIED** — the owner's design, assembly only, no probe run. The ROW is
  now the node and the matching unit; it is never split into per-sample
  input pairs. **947 nodes: 908 row nodes** (rust 116, ruby 792) **+ 39
  `lang.op` central nodes**. **51,294 connectors of two kinds: 908
  INTERNAL** (exactly one per row node, to its own central node,
  structure and never cut by the threshold, weight = mean output
  agreement with the co-rows sharing its inputs, 138 flagged
  `no_comparison`) **and 50,386 EXTERNAL** (row to row, different
  operators only, existing ONLY where both rows carry byte-identical
  `lhs_canon_vector` and `rhs_canon_vector` — the same ladder pair —
  weight = matched sample positions / 32). Comparable universe: 52,146
  row pairs share an identical input ladder, 1,760 of them inside one
  operator. External connectors clearing 1.00 / 0.95 / 0.85 / 0.70:
  **3,861 / 4,104 / 4,156 / 4,172**, and **39,381 of the 50,386 sit at
  exactly 0.0** — two rows of different operators handed the same 32
  inputs usually agree on nothing, which is the separation the sweep was
  for. `rust.+` and `ruby.+` DO share ladders (13 row pairs, max 0.9062)
  and the three disagreeing positions on the 29/32 pairs are exactly the
  three `i128` overflow points where ruby's unbounded `Integer` keeps
  going. `rust.+` vs `rust.-` share all six rust ladders and **every
  pair scores 1/32**. The largest component at every threshold is the
  same 39 ruby row nodes spanning six decline-dominated operators, so it
  mixes operators but not languages. `l3_row_graph.py`,
  `row_graph.json`, `row_graph_explorer.html` (self-contained, threshold
  cuts external only, internal toggle, language/operator colour modes,
  documented 10,000-connector draw cap), `verify_row_graph.js` — the
  headless verify passes 36 threshold x toggle x cap settings against an
  independent union-find, proves the identical-ladder rule by regrouping
  the row nodes itself, and shows the layout settles to 0.000 px of
  drift.
- next: three questions for the owner before this graph is widened — the
  DIAGONAL (same-ladder rows sweep `v OP v` only, which is why
  `ruby.<=> ~ rust.-` reads 1.0), whether external weight should also be
  offered with declines excluded (the top of the scale is currently
  decline-dominated), and whether ruby's nominal ladder window should
  gain 32/64-bit entries so the two languages meet on more than the two
  ranges they currently share.
- 2026-08-21 (log 049): **THE INTERVAL-SAMPLING PILOT RAN AND
  VERIFIED, on rust and ruby only.** N = 32 deterministic, closed-form
  samples per side spanning each holder's own representable range,
  numeric forms only, IN ADDITION to the edge classes. Two lanes:
  rust 3,712 probes in **0.85 s** (116 accepted numeric cells,
  acceptance REUSED not re-run, 2,716 answers / 996 `RAISE:panic` /
  0 ABORT), ruby 25,344 probes, **191.93 s** wall of which 190 s is the
  19 x 10 s inactivity budget, so ~2 s of actual evaluation
  (18,562 answers / 6,763 raises / 19 ABORT, all 19 the same
  `ruby ** BigDecimal` shape). The tensor —
  `matrices_interval/`, 39 files, 908 rows, 29,056 samples, one row per
  (operator, lhs holder, rhs holder, interval spec) with the sample
  axis inside the row — verifies clean: 0 non-rectangular lines, 0
  wrong vector lengths, **0 empty slots**, 0 dirty canon cells, 7,778
  outcome tokens all in the universal vocabulary. The graph
  (`agreement_graph_interval_pilot.json`,
  `graph_explorer_interval_pilot.html`, 43 rust/ruby nodes, 714 edges,
  567 passing the owner's input-overlap criterion) shows what the pilot was
  for: **at threshold 0.85, 103 of the 164 edges that the edge values
  alone would have drawn are COINCIDENTAL and vanish under the sweep**
  (75 of 127 at 0.95; 109 of 329 at 0.70); 496 node pairs lost weight;
  the sweep manufactured 77,145 disagreeing input pairs against 12,716
  agreeing. `rust.<` ~ `rust.<=` falls 0.8626 -> 0.4777. The positive
  control holds: all six node pairs at weight 1.0000 on the edge values
  — the genuine aliases — are still 1.0000 after the sweep.
  `rust.+ ~ ruby.+` 0.4024 -> 0.5439 but FAILS the criterion
  (overlap 0.1413). Headless verify passes, including the page's own
  live counters against an independent union-find at 10 threshold x
  criterion settings.
- next: two questions for the owner before the other ten follow — the 10 s
  inactivity budget that costs the ruby lane 190 of its 192 seconds
  (all of it `ruby **` on BigDecimal), and whether the input-overlap
  criterion is meant to cut cross-language edges as hard as it does
  (101 of 267 fail, `rust.+ ~ ruby.+` among them).

- 2026-08-21 (log 048): **THE OPERATOR AGREEMENT GRAPH IS BUILT —
  242 nodes (one per `lang.op` matrix), 22,488 edges at the ROW
  grain (best-match: an input pair scores 1 if ANY row of A and ANY
  row of B share byte-identical output_canon), replacing the
  set-identity rule the owner REJECTED.** Each edge carries weight,
  n_shared, n_matched, and the VALUE-only rate (REFUSE/RAISE:*/ABORT
  rows excluded) so decline- and value-agreement stay separable; no
  0-weight edges; threshold is a spectrum (slider in the explorer).
  Products: `Research/kind_fuzz_clustering/l3_agreement_graph.py`,
  `agreement_graph.json`, `graph_explorer.html` (self-contained, no
  CDN, per the dendrogram precedent). Sanity: go.+ ~ python.+
  **0.3432** (was 0.0000 under the rejected rule; the python int+int
  / go uint64+uint64 byte-identical rows exist — 26 of them); go.+ ~
  rust.+ **0.9471**; components 35 / 11 / 4 at t = 0.95 / 0.85 /
  0.70; mixed arithmetic+comparison components exist at all three
  thresholds (best-match bridges them); highest-degree node
  `dart.??` (236, dart). Headless verify clean. **No probe ran** —
  assembly only. Report:
  `DevComms/log_048_operator_agreement_graph.md`.
- 2026-08-20 (log 047): **THE FINAL CANONICAL FORMS ARE IN — the 242
  per-operator matrices re-emitted (v2: 11 columns, outcome tokens in
  `output_canon`, decimal mants at 31 fractional digits, exact
  rationals exiled to `matrices/exact_sidecar.json`) and the STRING
  CLUSTERING over the new canonical strings is built.** the owner's rulings
  recorded verbatim in the new dated section of
  `SUPPORT_conversion_spec.md` (integer mants and rational/`~` forms
  both rejected; fractions banished from visible columns). Products:
  `Research/kind_fuzz_clustering/l3_per_op_matrices_v2.py`,
  `l3_dendro_strings.py`, `dendro_strings.json`,
  `dendrogram_strings.html`. Approved python.+ slice: 4 of 5 expected
  strings match byte-for-byte; the c_int64+c_int64 row mismatches
  because the recorded cell holds `int:-9223372036854775766`, not −2
  — **awaiting the owner**. Sanity: go.+ ~ rust.+ 0.9206; go.+ ~ python.+
  0.0000 (real: python's heterogeneous holders break set
  byte-identity); arithmetic clusters form free of comparison columns
  at 0.95/0.85/0.70. Headless verify clean (242 leaves, monotone
  merges, 0 band-walk disagreements). **No probe ran** — assembly
  only. Report:
  `DevComms/log_047_final_canon_and_string_clustering.md`.
- 2026-08-20 (log 046): **THE SETTLED PER-OPERATOR MATRICES ARE
  BUILT — 242 CSVs, one per `lang.op`, one probe per row, inputs
  filled on every row, mant ∈ [1,2) canon.** the owner ruled the design
  today (settled, recorded in the dated section of
  `SUPPORT_conversion_spec.md`, including the plain rejection of
  integer mants: the decomposition is not unique). Products:
  `Research/kind_fuzz_clustering/l3_per_op_matrices.py`,
  `Research/kind_fuzz_clustering/matrices/` (242 CSVs + `index.json`
  + `README.md` with the filename escaping and reverse map). All five
  sanity checks pass, verified against `behavior_python_C.json`
  directly; the probe set spells e-acute only as NFC, stated rather
  than invented. **No probe ran** — assembly over the answer data on
  disk. Report: `DevComms/log_046_per_operator_matrices.md`.
- 2026-08-20 (log 045): **THE THRESHOLD SPECTRUM IS BUILT — ONE MERGE
  TREE PER COORDINATE FAMILY OVER THE EXTENDED MATRIX, AND THE
  CONGRUENCES ARE DRAWN AS TYPED CROSS-LINKS, NOT DISTANCES.** the owner ruled
  the design today (recorded as SETTLED): one dendrogram per coordinate
  family, a shared threshold slider, a family toggle, and the wrap
  congruences overlaid as arcs on whichever tree shows. Report:
  `PseudoCoupHQ/DevComms/log_045_extended_dendro_spectrum.md`.
  Products: `Research/kind_fuzz_clustering/l3_dendro_extended.py`,
  `dendro_extended.json`, `dendrogram_extended.html` (self-contained,
  data inlined the way `dendrogram_answers.html` embeds its tree),
  `verify_dendro_extended.js`. **No probe ran and no lane ran** —
  assembly over log 044's `matrix_extended.json`.
- **Five families, leaf counts recorded: form 239, sign 129, mant 129,
  container 31, text 32.** A column with no cell of a family is ABSENT,
  not forced in at distance 1 — 110 columns carry no numeric cell, 208 no
  container cell, 207 no text cell. Average linkage (UPGMA), no cut
  chosen, the sweep is the result.
- **The two named checks PASS.** `go.+`/`rust.+` land at form similarity
  **0.9922** (log 033's 0.907 at the answer grain; closer still on form
  alone, because the coordinate that separates them is not the form), and
  the `go.+ ~ python.+` **mant cross-link reads `sign flip, mant sum =
  2^64 (=== mod 2^64)`, w = 64, over 27 input cells** — the int64 wrap as
  a sign-flip edge.
- **Sign is far more agreeable than mant, and that asymmetry is the whole
  reason to split the two coordinates**: the sign tree's root joins at
  0.4765 and its widest plateau is ONE cluster across [0.00, 0.47]; the
  mant tree's root joins at **0.1747** — columns agree about direction
  long after they stop agreeing about magnitude, which a single numeric
  distance would have averaged away. **The congruence-as-height lift is
  confined to the mant tree by construction** (a match with a note); a
  sign flip stays a genuine sign disagreement, so the lift is kept OUT of
  sign.
- **Text: the concatenation columns cohere as a sub-tree.** The text
  tree's root splits at 0.0935 into the STRING PRODUCERS (all nine `.+`
  columns plus php `.` and ruby `<<`) against the TEXT-BY-SELECTION
  operators (`||`, `??`, `?:`, `and`, `%`). The coherence is topological,
  not metric — pairwise text similarity among the `.+` columns is median
  0.369 — because they disagree on the byte/codepoint/grapheme layers.
- **Two container columns (`kotlin…`, `python.**`) join the root at
  height 0.000** — no shared container cell with the rest, the tree's
  honest "not comparable in this family" rather than an invented height,
  the same standing log 037 gave the one-slot constructs.
- **Verified headlessly** (DOM-less, no jsdom present): the band-walk and
  merge-history cluster counts agree at all 101 thresholds for every
  family, leaf counts agree three ways, merge heights monotone, every
  cross-link endpoint a real leaf. All checks pass; real-browser
  interaction unverified as before.
- 2026-08-20 (log 044): **THE EXTENDED CLUSTERING MATRIX IS ASSEMBLED
  AND ITS CONVERSION SPEC IS RECORDED AS SETTLED** — the owner ruled the
  design today; the governing rule: *never compare raw answers,
  compare their decompositions, and let WHICH coordinate disagrees be
  the feature.* Report:
  `PseudoCoupHQ/DevComms/log_044_extended_matrix_and_conversion_spec.md`.
  Products: `SUPPORT_conversion_spec.md` (this node),
  `Research/kind_fuzz_clustering/l3_matrix_extended.py`,
  `matrix_extended_base.csv`, `matrix_extended.json`. **No probe ran
  and no lane ran** — assembly over the layer-3 answers through
  `l3_answers12.py`'s own loaders.
- **The base matrix is 64 form pairs × 239 lang.op columns,
  rectangular and spelling-blind** — 6,863 filled cells, 8,433 REFUSE
  *(measured)*; the design conversation's 233 was the log-030-era
  count and the word-spelled operations of logs 034/035 make it 239.
- **63,111 wrap congruences recorded as FEATURES instead of
  mismatches**, dominated by w = 63 (33,552), w = 64 (16,219) and
  w = 53 (8,337) — the two's-complement walls and the double-mantissa
  wall surfacing from the decomposition alone. The named check
  passes: `go.+` on (i64max, base_42) reads `≡ mod 2^64` within its
  own column (int64 against uint64 holders) AND against python's
  `whole:9223372036854775849`, 9 pairs on that one cell.
- **`not-applicable` is a first-class cell element DISTINCT from
  refuse**, and `death` had to join it — the data carries c++'s
  `SIGFPE` rows and the design named only refuse and raise. 938 of
  2,188 container tokens (ruby Struct/data inspect forms, opaque
  payloads) resist the literal parse and are counted as unparsed
  rather than papered over.
- 2026-08-20 (log 042): **THE BOUNDARIES ARE MEASURED NUMBERS NOW, NOT
  GAPS BETWEEN SAMPLES.** Report:
  `PseudoCoupHQ/DevComms/log_042_boundaries_by_bisection.md`.
  Products: `l3_boundary_targets.py`, `boundary_targets.json`,
  `l3_boundary_gen.py`, `bnd/` (eleven harnesses),
  `l3_boundary_lane.py`, `lanes/bs_all.sh`, `raw/bnd_<lang>.out`,
  `l3_boundary_fold.py`, `boundaries_<lang>.json`,
  `boundaries_index.json`, `l3_boundary_report.py`, `boundaries.md`.
  On the owner's ruling: *"i do want things like the boundaries"*.
- **8,067 adjacent sample pairs disagree on the whole-number axis;
  1,623 of them are ALREADY EXACT** because their two samples are
  adjacent integers, and 6,444 have a gap to search *(measured)*.
- **ONE LANE, 8.8 SECONDS, eleven languages, one compile each, 96,474
  probes, 2,738 boundaries located and never more than 65 probes for
  any one of them** *(measured)*. The varying operand is a RUN TIME
  variable of the holder's own type (decision B3), which is what turns
  sixty compiles per target into one compile per language.
- **Ten of eleven languages share the 2^63 wall and they fail at it in
  four different ways** — go wraps, rust panics, php changes the
  answer's TYPE to double, python and ruby have no wall at all. Zero
  is a wall too, for every unsigned holder.
- **A wall in result space is not a boundary in operand space.**
  `go.+` on int64 against 42 breaks at `2^63 - 43`; `go.*` on the same
  holders against the same 42 breaks at `ceil(2^63 / 42)` =
  219604096115589901. Only 447 of 2,738 boundaries pin a power of two
  at all.
- **Rust's shift boundary follows the LEFT holder and ignores the
  holder of the shift amount** — `i32 << i128` at 32, `i64 << i32` at
  64 *(measured, 56 cells)*.
- **The axis has no negative values, so asymmetry is UNMEASURED** and
  no Hub sentence may read "±2^63" on this node's evidence.
- **Swift has zero targets**, because its codegen refusals remove the
  large literals before any pair can disagree.

- 2026-08-20 (log 043): **THE SIGNATURES ARE REBUILT AT THE VALUE GRAIN
  WITH ANSWER-VALUED ELEMENTS, AND THE TWO ORDERS ARE NOW ONE.**
  Report:
  `PseudoCoupHQ/DevComms/log_043_value_grain_dominance.md`.
  Products: `l3_valuegrain.py`, `signatures_valuegrain.json`,
  `l3_dominance_vg.py`, `dominance_valuegrain.json`,
  `make_dominance_lattice_vg.py`, `dominance_lattice_vg.html`,
  `make_union_candidates.py`, `union_candidates.md`. **No probe ran and
  no lane ran.** Log 041's products are untouched and the new ones sit
  beside them. On the owner's ruling: *"each row isnt a row element. its a
  vector"* and *"that way something like php.== cant appear to have
  obtained god-operator status."*
- **`php.==` sits above NOTHING.** It speaks on all 1,156 elements, 160
  leaves ask only questions it also answers, and it CONTRADICTS all 160
  *(measured)*. The first denial is `dart.==` at
  `fractional|base_1_5|text|base_empty`, where dart answers
  `truth:false` and php answers `truth:false` on some holder pairs and
  `raise:Error` on others. Nothing in the machinery knows which leaf it
  is; it fell out of the top the moment the element carried an answer.
- **The grid went from 64 form pairs to 1,156 elements, and the
  agreement rate was ALREADY being measured there** — only the order
  was being built at the form grain. 239 leaves rather than 238:
  `python.@` raises on all 1,156 and a raise is a token, so an
  all-refusal vector is a vector.
- **THE MERGED ORDER: 209 of 239 leaves are MAXIMAL, on 202 faithful
  edges of 18,479 nesting pairs — 1.09 percent** *(derived)*, against
  log 041's 184 of 238 and 189 of 13,831. **Containment without
  faithfulness has no referent any more.** Per family, no dominant
  vector anywhere; **arithmetic collapsed to 59 maximal of 60 on 2
  faithful edges**, and **logical reversed** from log 041's 36-of-36 to
  24 of 36 on 108 faithful edges, because decision 55's support bar is
  gone and a four-element short-circuit pair can now be read.
- **218 distinct vectors over 239 leaves, and thirteen exact
  identities**, headed by **`csharp.&&` = `go.&&` = `java.&&` =
  `kotlin.&&` = `rust.&&` = `swift.&&`** and the same six for `||`
  *(measured)* — an identity and not a similarity score, resting on
  **four elements each**, which travels with it.
- **THE HUB-FACING ANSWER: 14 within-family union candidates against
  5,092 blocked**, down from log 041's 31, with **ten of the fourteen
  in the logical family** and **arithmetic offering none at all** —
  1,711 pairs, every one blocked. **Log 041's headline candidate does
  not survive**: `dart.==` with `php.===` share 1,089 elements and
  differ on 660.
- **DECISIONS 58, 59, 60, 61**, two of them FLAGGED for the owner with their
  cost measured. **61, the grain**: holder-pair is the default and the
  form-pair alternative is worth **147 faithful edges and 37 maximal
  leaves** (349/172 against 202/209). **59, refusal against raise**:
  silence is free because absence of a claim cannot contradict a claim,
  a raise is not because it was measured; reading a raise as silence
  would give 455 faithful edges and 205 maximal *(all measured)*.
- **The 202 faithful edges are an UPPER bound and the 209 maximal
  leaves a LOWER bound under log 042's boundary work** *(derived from
  the order's definition)* — a finer grid can only remove edges, never
  add one. `boundary_targets.json` names 6,444 targets, 1,623 already
  exact, and admitting them needs no change to `l3_valuegrain.py`.
- next: **the owner's ruling on decision 61, the grain**, which is the one
  thing this log declined to decide for him. Then log 042's boundary
  results folded in, which is one re-run of
  `make_union_candidates.py`. Still not carried, and said rather than
  dropped: the constructs, whose answers sit in
  `construct_answers_<lang>.json`.
- 2026-08-20 (log 041): **THE PRODUCT METRIC'S ALTERNATIVE READINGS ARE
  BUILT, ALL THREE, AND DEE'S DOMINANCE PARADIGM IS BUILT BESIDE
  THEM.** Report:
  `PseudoCoupHQ/DevComms/log_041_alternative_readings_and_dominance.md`.
  Products: `l3_alt_readings.py`, `clusters_agreement.json`,
  `clusters_containment.json`, `clusters_domain.json`,
  `two_tree_disagreement.json`, `make_dendrogram_alt.py`,
  `dendrogram_agreement.html`, `dendrogram_containment.html`,
  `dendrogram_domain.html`, `l3_dominance.py`,
  `dominance_lattice.json`, `make_dominance_lattice.py`,
  `dominance_lattice.html`. **No probe ran and no lane ran**; every
  number is a re-read of `clusters_all12.json`. `domstub.js` gained an
  optional id list and is unchanged with no argument.
- **The bias the owner named is real and it is the DOMAIN factor, not the
  answers.** Cut to 21 groups each, the domain-only tree sorts leaves
  by language MORE strongly than the product tree does (0.246 against
  0.223) and by operator family much LESS (0.418 against 0.674). The
  agreement tree, cut as coarse as it can go, puts **214 of 238 leaves
  in one group** and leaves 24 singletons, sixteen of which are a
  short-circuit `&&` or `||` starved of shared cells. **The answers
  alone do not separate these operations at the coarse end at all.**
- **`go.+` against `java.+` moves from 0.094 to 1.000** under both
  readings that stop punishing a narrow domain, while `java.+` against
  `cpp.+` moves only from 0.129 to 0.293 — the control that keeps the
  readings honest, since that pair is a genuine partial overlap with
  genuine disagreement inside it.
- **DECISION 55, the support threshold: 32 shared input cells.** 5,633
  of 28,203 pairs (20.0 percent) fall below it and are left OUT of
  every average rather than scored zero, because zero is a claim that
  was not measured. Its cost is stated rather than hidden: `go.&&`
  against `java.&&` has agreement exactly 1.000 over **four** shared
  cells, and the agreement tree declines to read it.
- **DEE'S QUESTION ANSWERED: the containment order flattens and the
  dominance order does not.** By domains alone there is **exactly one
  maximal element** — a class of all 64 cells carried by 35 leaves,
  fifteen php, eight ruby, six python, and six of the twelve languages
  putting nothing in it. Put the answers back and **184 of 238 leaves
  are maximal**, where a dominant vector would leave one. Of 13,831
  supported strict containments, **189 never disagree once — 1.4
  percent**. **No family flattens**, and the logical family has 36
  leaves and 36 maximal leaves.
- **The union vector is the whole grid, 64 of 64 cells, and that is
  not news** — 35 leaves already carry it alone. What is news is the
  short list beneath it: **31 within-family union candidates against
  179 forks**, headed by **`dart.==` with `php.===`, agreeing on all
  64 cells** of the grid, and the forks headed by every pairing of a
  three-way `<=>` against an equality at agreement 0.000 — log 033's
  and log 035's contradictions re-derived from a direction that was
  told nothing about them.
- **The two-tree reading gives 13,204 measured containment cases**,
  headed by `csharp.==` inside `python.==` at agreement 1.000 over 322
  shared input cells with a product of 0.406. `cpp.not_eq` appears
  beside `cpp.!=` on that list, which is log 034's positive control
  turning up unasked.
- Flagged for the owner and NOT taken: whether the union candidates or log
  040's near-neighbour short list is the right unification input;
  whether the alternative readings should be extended to the joint
  construct tree, which today carries no agreement rate; and whether
  decision 55's bar should move.
- 2026-08-20 (log 040): **THE CROSS-CHECK IS DONE AND 4j IS CLOSED —
  the node has no open measurement item left.** Report:
  `PseudoCoupHQ/DevComms/log_040_signature_versus_behavior_crosscheck.md`.
  Products: `xcheck_signature.py`, `xcheck_mapping.json`,
  `xcheck_compare.py`, `xcheck_signature.json`,
  `xcheck_sigdist_operators.json`, `xcheck_sigdist_constructs.json`.
  No probe ran; nothing in either node's existing artifacts was
  modified.
- **The symmetry the CORE opens with HOLDS for the operators and is
  ABSENT for the constructs.** Operators at 21 groups each: agreement
  **0.8795**, ARI **+0.1193**, against a 2,000-draw permutation null
  whose largest draw was 0.0343 — **real and weak**. Constructs at 12
  groups each: agreement 0.6365, ARI −0.0057, **p 0.552**, and
  unstable near zero.
- **The cause is measured and it is one-sided: over the 212 mapped
  operator leaves the declared-signature source holds exactly TWELVE
  distinct feature vectors, and not one of the twelve is shared across
  two languages.** The behavior source resolves the same 212 into 183.
  The declaration's whole operator vocabulary is, in effect, one word
  per language.
- **Every one of the 861 type-A disagreements is a BLINDNESS rather
  than a contrary claim** — all 861 at declared distance exactly
  0.000000, all 861 within one language. The declaration never once
  said "these are the same" about a pair it could tell apart.
- **1,578 of the 1,833 type-B disagreements cross a language, and 36
  sit at behavior similarity 0.999 or better** — the Hub's unification
  short list, headed by `php.===` with `python.is` (declared distance
  0.669421, behavior agreement 0.999135 over 1,156 shared cells).
- **Neither source subsumes the other**: 1,728 named kinds inside the
  twelve grammars are reached by no behavior leaf, and 26 operator
  leaves are named by no grammar's node types — dart's 17 and swift's
  6 among them, which makes **dart and swift the two languages weak on
  both sources at once**.
- Mapping stated as **decisions 45 to 54**, all overturnable; leaf
  ordering verified 237 of 237 against the artifact's own member
  lists.
- **FLAGGED FOR DEE, NOT TAKEN:** `CORE_0_3_2` still reads
  `status: draft`, and with 4j closed the only remaining CHECK entry
  is 4nn, a recorded presentation fault in two display fields of one
  artifact. Whether the node moves off draft is the owner's call and was not
  changed.

- 2026-08-19 (log 038 postscript): **THE VALUE-GRAIN PASS IS CLOSED —
  481,978 of 481,978 probes, all nine checked languages COMPLETE
  against the frozen manifests, ZERO suspect rows, and CHECK 5t is
  CLOSED.** The two lanes log 038 left running landed: kotlin's nine
  shards, 64,782 probes in 4,931 s at 76 ms a probe, and kv_dart_04,
  8,000 probes in 22 s, taking dart to its full 51,867. Kotlin's
  re-dropped shard 05 folded **once**: 8,000 rows, 8,000 distinct probe
  ids, checked against its manifest and not against the two `.done`
  entries. Both stages ran in-lane, so no separate execution stage was
  owed. 11,844 s of lane time over the 68 shards. With the three open
  languages the gate now reads COMPLETE for all twelve, **623,752
  rows**.
- **kotlin's truth column moves T>S like the other eight — the
  truthiness table's `T` was an artifact of the base value in every
  checked language WITHOUT EXCEPTION.** Kotlin's other seven columns
  read `R` and could not have moved. Movement over all nine is now
  **1,045 of 22,972 holder keys, 4.5 percent**, up a full point from the
  693 of 19,760 log 038 printed at eight-ninths.
- **kotlin splits more keys than any other checked language, 331, and
  splits them somewhere else**: 159 on `+=` and 124 on `-=`, 283 of 331,
  where every other language's biggest splitter is `subscript` or `+=`
  alone. Derived: `plusAssign`/`minusAssign` are resolved on the
  receiver's declared type and that type changes with the value class.
  No other language in the nine has an appreciable `-=` split.
  **Kotlin has no kotlin-only construct leaves** — elvis, `in` and `..`
  are OPERATORS, measured in the operator pass, and were never in this
  space.
- Re-folded at matched grain for all nine: `construct_answers_*.json`,
  `truthiness.json`, `truthiness_value.json`, `truthiness_table.md`,
  `trace_compare.md`, `value_movement.json`, `clusters_constructs.json`
  (123 leaves), `clusters_joint.json` (284 leaves) and
  `dendrogram_constructs.html` (123 leaves, 245 nodes), validated by DOM
  stub: 1 script run, 0 threw, `#count` = 34.
  `HARVEST_constructs.md` has nothing pending. **4j is now the only open
  item in the node.**
- 2026-08-19 (log 038): **THE NINE CHECKED LANGUAGES ARE MOVING TO THE
  VALUE GRAIN — seven are folded, three lanes are still running, and
  CHECK 5u is CLOSED.** Report:
  `PseudoCoupHQ/DevComms/log_038_constructs_value_grain.md`.
  Products: `l3_construct_value.py` (the value-grain generator, reusing
  log 037's scaffolds, recorders and encoders untouched),
  `l3_value_fold.py` (merge + gate + message check + movement),
  `l3_value_report.py`, `l3_joint_cluster.py`, **68 frozen shard
  manifests**, `truthiness_value.json`, `value_movement.json`,
  `truthiness_holder037.json` (log 037's frozen baseline),
  `clusters_joint.json`, and the re-folded `clusters_constructs.json`
  and `dendrogram_constructs.html`.
- **409,196 of 481,978 probes folded (84.9 percent), every folded
  language COMPLETE and ZERO suspect rows**: typescript 40,700, csharp
  85,587, java 89,698, rust 47,736, go 39,104, cpp 49,170, swift 13,334,
  dart 43,867 of 51,867. 6,919 s of lane time. Still owed: kotlin's nine
  shards (running, 87 ms a probe, about two hours) and dart's seventh
  (30 s) — 72,782 probes, harvest steps in
  `Research/kind_fuzz_clustering/HARVEST_constructs.md`.
- **the truthiness table's `T` was an artifact of the base value.**
  All eight folded checked languages read always-then for the truth
  form at the holder grain and **SPLIT** at the value grain. C++ and
  typescript — the two checked languages that COERCE — moved in more
  columns than that one; the six refusing languages moved in exactly
  one and could not have moved in any other.
- **693 of 19,760 holder keys, 3.5 percent, hide a verdict that depends
  on the value.** Small fraction, not a small finding: nothing at the
  holder grain said WHICH 3.5 percent, and one of them was the whole
  truthiness table.
- **break-at-k does NOT depend on the value, and cannot** — `break` and
  `continue` open no operand slot, so they have no value grain at all.
  What does depend on it is the loop around them: a while guard records
  **either 0 steps or 9 and nothing between**, and a for-iterable's
  trace length is the container's length, which the value class sets.
- **DECISION 21 — the constructs and the operators now share ONE tree,
  divided by KEY SPACE rather than by grain.** Decision 17's stated
  reason was the difference of grain, and this pass removes it. The 45
  two-slot constructs join the 239 operators in `clusters_joint.json`;
  the 79 one-slot ones keep their own tree, because there is no
  one-operand operator signature for them to sit beside. 32 of the 45
  find another construct nearer than any operator.
- **CHECK 5u CLOSED — rust's four harness refusals were TWO different
  things.** Two named the recorder's own `db` method and are genuine;
  they are repaired and now record BIND traces. Two named rust's own
  `Borrow` trait and were never harness refusals — log 037's classifier
  matched the bare token "trait bound", which is too wide. Narrowed:
  44 `Borrow` rows now read as rust refusals and **rust's value-grain
  lane records zero harness refusals**.
- **two instrument faults found, both of the "exit 0 is not evidence"
  family.** The completeness gate takes its planned count from the
  shard summary lines, so an EMPTY shard file reads COMPLETE one shard
  short — the frozen manifests are the check and dart was caught by it.
  And a script sitting in the drop directory is NOT a queued script:
  the daemon fires on a file event, and ten shards sat unrun because
  their events had been spent on an earlier run that refused for want
  of scratch.
- next: harvest kotlin and dart's seventh shard by the six steps
  in `HARVEST_constructs.md`, then re-fold both trees and the picture
  so that all twelve languages stand on the same grain. Also open and
  older: the cross-check against `kind_signature_clustering`'s
  signature clusters (item 4j).

- 2026-08-19 (log 037): **THE CONSTRUCT PASS IS COMPLETE FOR ALL TWELVE
  LANGUAGES, and php's twenty fatals are RECOVERED.** Report:
  `PseudoCoupHQ/DevComms/log_037_constructs_all_twelve.md`.
  Products: `l3_construct_lang.py` (the eight lanes — the trace
  recorders and the scaffold tables, the only two parts
  `HARVEST_constructs.md` said would change), `l3_php_recover.py`,
  `l3_construct_cluster.py`, `make_dendrogram_constructs.py`,
  `clusters_constructs.json`, `dendrogram_constructs.html`, eight
  frozen manifests, sixteen raw lane files, and the rewritten
  `truthiness_table.md`, `trace_compare.md` and `construct_index.json`.
- **21,342 acceptance probes over the eight, 1,757 accepted, 508 s of
  lane time, and every lane COMPLETE.** The gate now reads COMPLETE for
  all twelve languages and 164,826 of 164,826 rows.
- **php's twenty fatals RECOVERED, and the cause read rather than
  guessed.** All twenty said `Cannot redeclare class`; the harness
  suffixed a declared class name per PROBE, and a probe whose two slots
  are the same class-declaring holder redeclared it. The suffix is now
  per SLOT as well. All twenty answer, none died again, and
  `raw/kc_php.txt` is left exactly as the first run wrote it.
- **the twelve-language TRUTHINESS table is the pass's sharpest
  result.** Seven languages refuse every non-boolean condition (go,
  rust, swift, dart, csharp, kotlin, java); five coerce (cpp,
  typescript, python, ruby, php). The line is NOT the static-against-
  open line — c++ and typescript are checked and coerce.
- **the index-against-value split lands at exactly ONE language of
  twelve, and it is go** — go's one-variable `range` hands back the
  index, so go's for-trace reads 0, 1, 2 where the other eleven read
  1, 2, 3. Typescript agrees on the values and disagrees on the type:
  its three are FLOAT:64, because a javascript number is a double.
- **break at k agrees in SHAPE across all eleven languages that have a
  break** and disagrees only on integer width. kotlin has no break kind
  in its grammar, so its line reads ABSENT and not MISSING.
- **the constructs get their own dendrogram (decision 17), and no
  plateau is wider than 0.06.** 129 leaves with a non-empty domain, 20
  admitted-and-empty, plateaus at 42 / 27 / 17 clusters. For the 42
  two-slot construct leaves the nearest operator signature has median
  jaccard **exactly 1.000** — a two-slot construct's accepted domain
  very often coincides exactly with some operator's.
- next: the ANSWER GRAIN for the nine checked languages. This pass
  measured them at the holder grain, 21,342 probes against the design's
  derived 624,166 for the full value matrix, so whether a construct's
  domain moves when the value varies is unverified for the nine — the
  same question decision 9 answered for the operators by measuring it.
  Also open and older: the cross-check against
  `kind_signature_clustering`'s signature clusters (item 4j).

- 2026-08-19 (log 036): **LAYER 3 EXTENDED FROM OPERATIONS TO
  CONSTRUCTS — the owner blessed access / flow / binding, and four of the
  twelve languages are measured.** Report:
  `PseudoCoupHQ/DevComms/log_036_layer3_constructs.md`.
  Products: `construct_design.md` (16 numbered decisions, written
  BEFORE anything was generated), `construct_catalogue.py/.json`,
  `construct_space.py`, `l3_construct.py`, `l3_construct_go.py`,
  `l3_construct_read.py`, four frozen manifests, four raw lane files,
  `construct_index.json`, `construct_answers_<lang>.json`,
  `truthiness_table.md`, `trace_compare.md`, `HARVEST_constructs.md`.
- **the construct list is DERIVED, and 14 of 144 role slots come back
  ABSENT.** Two different absences, kept apart: go really has no
  `while` and no `try`, and seven languages really have no slice
  syntax; kotlin's `break` and four of swift's roles exist in the
  language and are simply unnamed by the pinned grammar.
- **647,190 probes derived and printed before anything ran** — about a
  ninth of the operator pass's 5.79M.
- **the proof pass: python 59,797 probes in 16.9 s COMPLETE, go 1,710
  in 26.8 s COMPLETE.** Then ruby 48,297 in 0.8 s COMPLETE and php
  33,660 of 33,680 in 10.4 s, twenty short on uncatchable fatals.
- **the trace encoding round-trips.** go's break traces and python's
  break traces are byte-identical, produced by different encoders in
  different languages from the same written spec.
- **the TRUTHINESS table exists and the four measured languages
  disagree completely.** go admits ONE form into a condition and
  refuses the other seven. ruby admits every form and answers `then`
  for all but nothing. python and php both split on emptiness and on
  zero.
- **a `for` over 1, 2, 3 does NOT see the same trace in every
  language.** python, ruby and php walk 1, 2, 3; go walks 0, 1, 2,
  because go's one-variable `range` hands back the INDEX. Invisible to
  any observation that only recorded whether the loop finished.
- **break at k agrees in all four, byte for byte.** When the loop is
  the fixed sequence rather than a holder the disagreement vanishes,
  which locates it precisely in how a language's loop reads a
  container.
- **three faults found by the proof pass**, which is what a proof pass
  is for: go imports must sit at the file head and must not repeat
  (two runs); ruby evaluates `#{...}` when the DRIVER is parsed, so the
  first ruby lane died in 0.1 s having run nothing; php refuses a class
  declared twice and a php fatal is not catchable — the log 027 §5.1
  fault met again in a new place.
- **eight languages UNBUILT.** Not running, not queued —
  built-for. `HARVEST_constructs.md` carries the cost order, the four
  parts of a lane and which two change per language, and the nine
  faults not to repeat.
- next: the eight remaining construct lanes in cost order —
  typescript, csharp, kotlin, rust, cpp, dart, java, swift last
  because swift needs the full compiler. Then point the clustering
  machinery at the construct signatures, which are already written in
  the shape it takes. Phase 4 item 4j — the cross-check against
  `kind_signature_clustering` — is still the oldest unstarted item in
  the node and is untouched by this pass.
- 2026-08-19 (log 035): **THE RE-FOLD — 238 leaves, both positive
  controls PASS, and swift's 1,066 exclusions are gone.** Report:
  `PseudoCoupHQ/DevComms/log_035_refold_all_twelve.md`.
  Products: `l3_wordexec.py`, `l3_refold.py`, `refold_index.json`,
  a rebuilt `clusters_all12.json` and `dendrogram_all12.html`, and
  `HARVEST.md` closed to "nothing pending".
- **the harvest was clean.** Every lane log 034 left running or queued
  had finished, every one passed the completeness gate, every one had
  zero `ENOSPC` lines, and scratch was left exactly at 2,566 MB — the
  first whole queue in this node that needed no re-run.
- **both positive controls PASS exactly.** C++'s six word spellings
  each land at similarity **1.000** on their symbol twin, and
  `ruby.and` lands at 1.000 on `ruby.&&`. A third, unplanned one falls
  out of the parenthesis repair: `php.and` on `php.&&` at 1.000.
- **swift did not move by a single edge, and that is the right
  outcome.** All 1,335 edges touching a swift leaf keep their log-033
  similarity to the last digit and all six signatures keep identical
  domains. What changed is the record: 1,552 answers with **1,066 rows
  excluded** by decision 40 become 1,552 answers with **ZERO**. The
  answers were always right; the provenance was not.
- **238 leaves, not log 034's predicted 235** — the prediction did not
  count php's three de-VOIDed rows. Twelve added, none lost.
- **decision 44 lifts decision 30's voiding of php's `and`/`or`/`xor`**;
  57 of 64 domain cells changed answer class, from the LEFT OPERAND to
  the operation.
- **a FOURTH total contradiction**, `cpp.xor` against `php.xor`, 64 of
  64 — a spelling collision, c++'s bitwise `^` against php's logical
  exclusive-or. Log 033's three all stand unchanged.
- **admitting ruby's word logicals MERGED two coarse clusters**, 22 to
  21 at the stable [0.155, 0.185) reading, which holds its bounds to
  six decimals across a twelve-leaf change. The eleven-member shift
  group returns with no twelfth, as predicted.
- **two faults found in this pass's own new code, both by a check and
  not by a failure**: an operator list that did not reach the exec
  module, so a lane compiled `/` where `not_eq` was meant and still
  exited 0 with a full gate-passing summary; and a FROZEN manifest that
  silently dropped three leaves while producing exactly the predicted
  leaf count.
- next: **CHECK item 4j, the cross-check against
  `kind_signature_clustering`** — now the only phase-4 item still open
  and the oldest unstarted item in the node. Behind it: ruby's
  unreproducible-address recorder fault, unfixed since log 027 and
  measured three times; the deferred kotlin aside; and one release
  build to settle rust's panic.
- 2026-08-19 (log 034): **the SWIFT REDO with the real compiler, and
  DECISION 43 — a mechanical library-versus-language criterion that
  lets word-spelled operations into the vocabulary.** Report:
  `PseudoCoupHQ/DevComms/log_034_swift_redo_and_word_operators.md`.
  Products: `wordop_survey.py`, `wordop_criterion.py`, `l3_wordops.py`,
  `l3_swiftfull.py`, `l3_swiftfull_read.py`, `wordop_survey.json`,
  `wordop_criterion.json`, `swiftfull_plan.json`, `raw/lr_words*.txt`,
  and a rewritten `HARVEST.md`.
- **JOB A, swift.** Every swift verdict in this node was taken with
  `swiftc -typecheck`, which log 032 measured accepting 1,066 of 2,618
  probes the full compiler refuses — 40.7 percent, almost all
  overflowing integer literals diagnosed in SILGen. `swiftc -c` was
  measured at **155 ms per probe against `-typecheck`'s 154**, so the
  WHOLE 76,614-probe matrix is retaken rather than only its accepts and
  the redo rests on no assumption. `valuematrix_swift.json` is kept and
  marked superseded-with-reason; the new one is
  `valuematrix_swift_full.json`.
- **JOB B, decision 43.** A word-spelled binary operation is first
  class iff BOTH legs hold: leg G, the grammar declares the word in the
  operator slot of a binary-shaped expression node; leg R, the
  language's own checker REFUSES an ordinary variable named with that
  word. Both mechanical, both run, applied to all twelve. **Admits
  c++'s `and` `bitand` `bitor` `not_eq` `or` `xor`, ruby's `and` and
  `or`, typescript's `instanceof`, php's `instanceof`** and re-derives
  python's six, kotlin's `in`, typescript's `in` and php's three
  without being told.
- **the owner's kotlin premise was checked and does not hold.** The kotlin
  grammar does NOT declare `shl`/`shr`/`ushr` as infix operators — its
  `infix_expression` carries an ordinary `identifier` — and
  `val shl: Int = 1` compiles. Both legs fail, so kotlin's shifts are
  LIBRARY and log 030 item 4k's builtin ruling is confirmed rather than
  bent. The shift tally therefore breaks by EXCLUSION.
- **A precedence fault found in a second language.** Log 033 item 4u's
  php parenthesis fault is the identical fault in ruby's route-C
  driver, invisible until decision 43 gave ruby a word-spelled
  operation. Both repaired, both languages re-run whole so the
  symbol-spelled cells can be diffed rather than assumed unchanged.
- **The reservation leg cost four passes because it started without a
  control.** Two of the five languages with no control word were
  measuring their own broken harness and it looked exactly like a
  measurement. 26 verdicts over 7 languages were DROPPED rather than
  read; every verdict in the published table comes from a pass whose
  control `zzfoo` ACCEPTED.
- **The partially-loaded-holders default is RATIFIED BY SILENCE**
  (the owner, 2026-08-19) — a holder that loaded only some of its value
  classes is probed with the values that loaded. Recorded in the CORE's
  open items, still overturnable.
- 2026-08-19 (log 033): **the ANSWER GRAIN for ALL TWELVE languages —
  domains and computed values in one dendrogram.** Closes CHECK 4i.
  Report:
  `PseudoCoupHQ/DevComms/log_033_answer_grain_all_twelve.md`.
  Products: `clusters_all12.json`, `dendrogram_all12.html`,
  `l3_answers12.py`, `make_dendrogram_all12.py`, `domstub.js`, and the
  bridge added beside decisions 18 to 30 inside `l3_answers.py`.
  **226 leaves, 111,410 input cells, 399,845 value answers, 549,231
  raises, 480 deaths, 1,066 swift refusals excluded with their count.**
- **The two answer encodings are BRIDGED as decisions 31 to 42**, every
  one overturnable by a re-read and none by a re-run. Log 031's three
  languages arrive as printed tokens and log 032's nine as bits; the
  bits are mapped into the same canonical token space, width dropped on
  integers, both lengths dropped on text, floats carrying an exact
  token AND a 14-digit shadow with the shadow used only where a
  print-grain language is in the comparison. **457 canonical tokens are
  reached from both a printed and a bit pre-form** and each is listed
  with both spellings and both counts.
- **The first genuine answer-grain CONTRADICTION in this node, and it
  crosses the static-and-open divide.** `cpp.<=>` against `php.<=>` and
  against `ruby.<=>`, **211 of 211 shared cells**, plus `kotlin...`
  against `rust...` at 112 of 112. Log 030 measured zero at acceptance
  grain and log 031 zero at answer grain over three languages. All
  three are a language answering in a KIND the other does not have, and
  decision 39 is what keeps those kinds apart — stated so a reader who
  overturns it knows what will vanish.
- **`+` still splits by coercion and the answers name the principle.**
  Four families at the 15-cluster reading: the five checked languages
  whose `+` concatenates a string, go-with-rust, php-with-python, and
  ruby alone. **The five languages that return the bit-identical
  wrapped integer on `i64max + 42` never form a cluster at any
  threshold** — go pairs with panicking rust at 0.907 because their
  domains are identical, while go against java is 0.094 with perfect
  answer agreement on all 88 shared cells.
- **dart's answer-anyway `/` and typescript's float-everything land
  together**, similarity 1.000 over 144 shared cells, in a cluster of
  four with `java./` and `kotlin./`; the disagreement is only where the
  divisor is zero. `42 / 0` is an eleven-way reading with two
  `fractional:inf` answers, one `death:rc-8` and eight distinct raises,
  which decision 31 is what makes visible.
- next: **the non-operator kinds**, which are unmeasured for eleven of
  the twelve and which phase 4 is not finished without; the
  `kind_signature_clustering` cross-check (item 4j), still not started;
  a swift route-C build taken with full `swiftc` rather than
  `swiftc -typecheck`, since 1,066 of 2,618 probes are refused and
  swift is measured in name only; the php `and`/`or`/`xor` re-run; and
  one release-build rust run, about a second, to settle whether
  `rust.+` joins the wrapping five.
- 2026-08-19 (log 032): **the EXECUTION pass — what the accepted
  operations RETURN, for all nine statically checked languages.**
  Closes CHECK 3k. Report:
  `PseudoCoupHQ/DevComms/log_032_layer3_execution_answers.md`.
  Recording rule:
  `PseudoCoupHQ/Research/kind_fuzz_clustering/answers_encoding.md`.
  Products: `answers_<lang>.json` for go, rust, cpp, java, csharp,
  typescript, swift, kotlin, dart, plus `answers_index.json`.
  **170,419 accepted probes, 162,853 answers, 6,020 raises, 480
  deaths, 1,066 codegen refusals, 297.5 s of wall time**, every
  language passing the completeness gate.
- **the owner's single-file ruling paid three orders of magnitude.** Only the
  probes the value matrix already scored ACCEPT are emitted, one
  function each, into a handful of chunk files per language — so no
  compile failure is possible by construction and there is nothing to
  bisect. Compilation is the cost in eight of nine languages; go's
  2,806 probes cost 0.8 s in total against log 025's 17.4 ms per probe
  for acceptance.
- **The answers are BITS and TYPE, never printed text.** Two's
  complement bytes, IEEE bit patterns, byte length plus both length
  notions for text, containers recursively, and the language's own
  name for the result type — the STATIC type wherever the language
  will give one, which for java and kotlin meant an overload set over
  the eight primitives so that `int` does not arrive as `Integer`.
- **`42 << 42` on a 32-bit signed holder: seven acceptances, five
  answers.** go 0, c++/java/c-sharp 43008, typescript 43008 as a
  float64, dart 43008 shifted inside 64 bits, rust panics. Every
  verdict-grain pass in this node calls that one uniform ACCEPT cell.
- **`i64max + 42` wraps to the same 64 bits in five languages and
  panics in rust**; `42 / 0` raises in five, dies with `SIGFPE` in
  c++, and ANSWERS positive infinity in dart, whose `/` is not integer
  division at all. `pi + pi` returns the identical bit pattern in all
  seven languages that accept it.
- **swiftc -typecheck accepts what swiftc refuses: 1,066 of swift's
  2,618 accepted probes, 40.7 percent.** Recorded as `CODEGEN_REFUSE`
  with the compiler's own message. The other eight languages recorded
  zero. Same shape as log 030's dart severity fault — the instrument
  was answering a slightly different question than the one asked.
- **c++ segmentation-faults on `i64max + "hello"`**, which the matrix
  records as ACCEPT because it is pointer arithmetic. 162 of c++'s 480
  deaths are that; the other 318 are `SIGFPE`.
- **Three mechanisms are new and are standing rules now.** A chunk
  binary takes a START INDEX so an uncatchable death costs one probe
  and not a chunk; ninety seconds of silence is treated as a death, so
  a hang costs one probe too; and a compiler that refuses a chunk
  NAMES the probes to drop through a `// __PROBE__` marker per probe,
  which is a repair step and not a bisect.
- **Kotlin ran three times and two runs are quarantined**, both faults
  found by diffing runs rather than by inspection: a `LongRange` walked
  as an `Iterable` does not come back, and a java array recorded
  through `toString` embeds an identity hash that differs run to run.
  `raw/SUPERSEDED_ex_kotlin_rangebug.txt` and
  `raw/SUPERSEDED_ex_kotlin_arrayhash.txt` are kept and not folded.
- next: point log 031's clustering machinery at `answers_<lang>.json`
  — CHECK item 4i, the answer half of the CORE's phase-4 pair for the
  other nine languages. The rows are shaped for it already.

- 2026-08-19 (log 031): **the FIRST answer-grain clustering — the
  computed values, not the acceptance verdicts, over the three
  languages that have executed answers.** the owner's instruction: *"i want
  to see it cluster the actual computed values."* Report:
  `PseudoCoupHQ/DevComms/log_031_answer_grain_clusters.md`.
  Visual:
  `PseudoCoupHQ/Research/kind_fuzz_clustering/dendrogram_answers.html`.
    - **the answers carry nearly the whole signal.** Clustered on
      domain overlap alone as a control, the same 69 signatures of
      python, ruby and php collapse into **one cluster of 68 with
      `ruby.=~` beside it** over the widest band [0.095, 0.194); with
      the answers counted the same leaves give **45 clusters** over
      [0.601, 0.700), and **68 distinct classes at threshold 1.000
      against 25 on domains alone**. Open dispatch barely separates at
      acceptance grain because nothing is checked until it runs.
    - **the answers re-sort the logicals by what they RETURN.**
      `python.and` clusters with `ruby.&&` and `python.or` with
      `ruby.||` — the operand-returning ones — while `php.&&` and
      `php.||` sit with `php.!=`, `php.<` and python's and ruby's
      `!=`, the boolean-returning ones. Spelling says otherwise.
    - **the CORE's third arm is tested and it answers with a RATE.**
      Over 55 same-spelling language pairs sharing 19,090 input
      cells: **zero disagree on every shared cell, 44 of 55 disagree
      on some cell**. `php.||` against `ruby.||` disagrees on 1,118 of
      1,156; eleven pairs agree perfectly. `contradicts` as a boolean
      does not fit the measurement.
    - **integer overflow is the one known fracture that fractured.**
      `i64max + 42` answers `whole:9223372036854775849` in python and
      ruby and `fractional:9.2233720368548e+18` in php. 2^53+1, −0.0,
      NaN, inf-against-NaN and e-acute equality all AGREE across the
      three once the printers are canonicalised.
    - **a second harness fault, found not looked for, and the answer
      grain is what caught it.** php's `and`, `or` and `xor` bind
      looser than assignment, so `$__r = ($a) $op ($b);` parses as
      `($__r = ($a)) and ($b)` and every one of 6,241 answer cells
      records the LEFT OPERAND. An acceptance pass cannot see it,
      because a wrong answer is still an ACCEPT. The three signatures
      are VOID (decision 30) and kept with the diagnosis.
    - **thirteen numbered overturnable decisions, 18 to 30**, every
      canonicalization reversible: 617 canonical tokens have more than
      one pre-canonical spelling and all of them are kept beside the
      token. Unparsable residue is 1,730 of 255,715 answers, 0.68
      percent.
    - next: **route C for the nine** (CHECK 3k) is now the single gate
      on everything left. Hold the value-class vocabulary FIXED when
      building it — decision 18's cross-language input identity
      depends on it — raise the harness's 120-character print cap, and
      print floats without loss so decision 22's 14-digit comparison
      can be dropped.

- 2026-08-18 (log 030): **phase 4's first arc is closed — the value
  matrix is promoted to the primary domain, the dart fault is fixed
  rather than flagged, and the chosen cut is replaced by a threshold
  sweep on the owner's ruling.** Report:
  `PseudoCoupHQ/DevComms/log_030_final_clusters_sweep.md`.
  Visual:
  `PseudoCoupHQ/Research/kind_fuzz_clustering/dendrogram_sweep.html`.
    - **all nine value matrices COMPLETE**, 2,221,643 probes folded and
      every one passing its own gate; `vm_dart_01` and cpp's six shards
      landed. All nine load-check lanes folded, **zero unclassified**.
    - **the split classification, which is the number log 024 decision
      3 asked for**: of 4,588 split cells, **3,267 (71 percent) are
      layer 2 leaking in** — the holder could not hold the value —
      against 1,053 layer 3 moving and 268 mixed. That cuts the
      apparent size of the value-dependence finding by about two
      thirds. Typescript is the pure layer-3 case (876 of 876, literal
      type narrowing); dart is the pure layer-2 case (659 of 659).
    - **the dart `||` fault is diagnosed, fixed and confirmed.** The
      lane scraped `dart analyze` at every severity, so `dead_code`
      (a WARNING) on `true || b` and `false && b` was read as a type
      refusal, and the one-value-per-holder grid drew the unlucky
      value. Fixed to severity ERROR only — which makes dart
      consistent with the other eight rather than special. Dart
      re-run whole: 50,381 probes moved REFUSE to ACCEPT and **zero
      moved the other way**. **All seven `contradicts` edges are gone;
      the final pass has zero.**
    - **a fault the completeness gate cannot see, found by accident.**
      A lane that runs out of tmpfs cannot write its probe sources, a
      file that was never written draws no diagnostic, and the harness
      scores "no diagnostic" as ACCEPT — while the lane exits 0, prints
      its `__SUMMARY__` and reports its full probe count. Swept,
      re-run, and a control re-run reproduced its numbers exactly.
      Every other lane log in the node was scanned: **exactly one file
      is implicated, the void run itself.** Proposed standing rule:
      grep a lane's log for ENOSPC before folding its product.
    - **the promotion cost less than expected**: only **23 of 233
      signatures moved domain, every one a widening, none narrowed**.
      Go, cpp and java did not move one cell. Cluster count at the old
      0.70 cut moves 46 to 44.
    - **the sweep.** Full merge history, 228 merges over 229 leaves,
      verified against an independent walk at all 167 breakpoints with
      zero mismatches. **The curve has no elbow**, which is the direct
      reason no cut can be picked from the data. Widest non-degenerate
      plateau **[0.137, 0.196) holds THREE clusters**, and they divide
      by WIDTH rather than by language or by operator: 147 permissive
      (median domain 18 of 64), 51 strict (median 3), and 31
      integer-and-truth-only spelled `% & && << >> ^ | ||` (median 2),
      the last crossing the static and open-dispatch divide. **229
      signatures collapse to 61 exact distinct domains.**
    - **the stories, tracked rather than asserted.** Log 029's cluster
      5 survives and is stronger than log 029 could say — its twelve
      members have IDENTICAL domains, the single cell `whole|whole`.
      **`+` never forms a pure cluster larger than two at any
      threshold, and `==` never forms one at all** — both strictly
      stronger than the preliminary phrasing.
    - **next**: route C for the nine checked languages is still the one
      genuinely unbuilt thing — the matrices give VERDICTS, not
      ANSWERS, and the CORE's phase-4 pair is {domain accepted, answer
      per input}, so a zero `contradicts` count is zero of the
      acceptance-grain reading and says nothing about the CORE's
      definition. The cross-check against
      `kind_signature_clustering`'s signature clusters has still not
      been started. Six questions for the owner in log 030 §6, including the
      kotlin `shl`/`shr` vocabulary question carried from log 029 —
      which matters concretely, because the go-and-rust shift pattern
      against the cpp-and-java one now stands two against four and
      kotlin and swift are the two languages that could move it.

- 2026-08-14: node founded at the owner's instruction ("lets draw up a
  PlanPlan research plan for this"), and NAMED by him the same turn
  ("oh kinds. thats what i was looking for. to cluster kinds using
  an automated fuzzer") — the session's first spelling,
  `vocabulary_probing`, was removed in favour of his word.
- 2026-08-14: the node's spine is four corrections the owner made to the
  session's mis-records, all stated in the CORE: there is NO corpus
  (scripts are GENERATED per kind); comparison is by the
  domain-and-answer RELATION, not a flat signature, because an
  equivalent kind elsewhere may accept a wider domain; what gets
  fuzzed is the grammar's kinds (named + anonymous), builtins being
  library names and out of scope; chains are mostly depth two with a
  short hand-written tail, and the legal-pair table in
  `node-types.json` prunes the probe space long before n^2.
- 2026-08-15: phase 0 measured, nothing executed. 1,776 named kinds
  and 1,422 anonymous tokens across the 11 targets; 8,371 declared
  legal triples (36,236 with the grammar's abstract groupings
  expanded); **probe space = 3,556** under the base rule (one probe per
  host-slot-dominant), 7,140 if each operator on a token menu counts
  separately — 168 to 445 per language, so the CORE's "hundreds per
  language rather than 26,000" holds, at its lower half (rust: 311
  probes against 163^2 = 26,569). Depth: 974 probes need no enclosing
  kind, 1,646 need one, 928 need two or more across a 175-host tail.
  1,150 kinds take no dominant input and are honest exclusions. Two
  findings the plan did not have: node-types.json lists every anonymous
  token but places only 438 of 1,422 in a host slot, and the grammar
  does NOT state the owner's `break`-needs-`for` chains — seven of eleven
  grammars declare break as a legal top-level line, so grammar depth is
  a lower bound. Report:
  `PseudoCoupHQ/DevComms/log_021_fuzz_phase0_probe_space.md`;
  scripts and data:
  `PseudoCoupHQ/Research/kind_fuzz_clustering/`.
- 2026-08-17: phases 1 and 2 done, python only. Phase 1 is a written
  artifact — `Research/kind_fuzz_clustering/probe_design.md` — stating the
  generation rules before anything was generated, with ELEVEN numbered
  judgment calls for the owner to overturn (log 024 §2). Its spine: a probe's
  operand is a layer-2 CELL, not a dominant, so python's 686 R2 probes
  become **20,024** over 62 kinds and 100 signatures (R2: one signature per
  menu token); operands are 117 values from the 26 cells the layer-2 audit
  passed (23 LOADS + 3 PARTIAL minus refused edges), base and edge alike
  baked as literals; 200 operand pairs by four rules rather than the 13,689
  cross product; every literal-spellable probe written TWICE, once opaque
  through a variable and once as the literal in the operator's own slot.
  Phase 2 ran them through the SandboxDesign agent lane in **64.5 s**:
  7,868 answered, 11,736 raised, 388 compile-refused, 32 exhausted the
  two-second budget, NONE lost. Python needed no bisect — its compiler is
  reachable at run time, so each probe compiles alone and a refusal
  isolates exactly; the bisect crux stands unbuilt for the ten. Three
  findings the census did not hold: `Decimal(42) + Fraction(42)` RAISES
  though both equal 42 and each adds to a plain 42 (two holders of one form,
  no shared arithmetic); `list += tuple` answers where `list + tuple`
  raises, so the augmented operator NESTS over the plain one inside one
  language; and `<>`, `print` and `exec` as statements are in the grammar
  and refuse to compile (382 of the 388 refusals), dating the grammar
  against the runtime. Report:
  `PseudoCoupHQ/DevComms/log_024_layer3_python_fuzz.md`;
  artifacts: `PseudoCoupHQ/Research/kind_fuzz_clustering/`
  (`probe_design.md`, `probes_python.json`, `lanes/l3_python.sh`,
  `raw/l3_python.txt`, `behavior_python.json`, `behavior_python.md`).
- 2026-08-18: two measurement logs landed ahead of the design
  ruling. `DevComms/log_025_probe_timing_measurements.md` timed one
  probe per language and priced brute force: ~5.79M probes across
  the twelve (§1), 435 h at one probe per file — **18.1 days** —
  against **6.2 h batched** at 33x-103x measured amortisation, with
  the full value matrix costing **under 1 percent** on top of pair
  enumeration (§4). Kotlin is 206 h of the 435, 47 percent of the
  bill from 5 percent of the probes, all of it 2,397 ms cold
  compiler start. `DevComms/log_026_compiler_acceptance_shape.md`
  traced "which operand pairs does `+` accept" to its literal
  location in five compilers: go, java and rust hold it as literal
  DATA (`binaryOpPredicates`; a 23-row `Operators` table; `add_impl!`
  over 16 primitives), typescript and python do not and cannot — `+`
  is open there — and go, typescript and java all ship their checker
  as a callable library (§3 finding 4).
- 2026-08-18: **the owner ruled the layer-3 design**; the CORE now carries
  it as `## the layer-3 design — RULED 2026-08-18`. Seven rulings:
  the probe operand is a layer-2 HOLDER, not a form ("yeah per
  holder"), every row carrying (form, holder, value class) so
  form-level views stay derivable; FULL ENUMERATION of ordered
  operand pairs, no pruning rules ("full enumeration... its proof vs
  potentially biased rules"); the FULL VALUE MATRIX everywhere ("if
  its within reason, we can just brute force it"); progress
  print-outs — [done/total], elapsed, ETA — as a standing
  requirement on every generation and run phase ("for fuck sakes
  please include runtime print-outs on progress and maybe even time
  estimates"); ALL non-overlapping evidence routes pursued together
  ("i want to pursue all of them as solutions where they dont
  overlap") — A1 in-process checker calls, A2 check-only invocation,
  B lifted literal data behind a certification gate, C execution —
  with overlapping cells run twice so agreement certifies and
  disagreement is a finding; the anti-interpretation rule, that a
  verdict comes from the compiler's own logic running or its literal
  data matching and never from an agent's hand-re-assembled reading;
  and kotlin's cost mitigation chosen at phase-3 build time,
  measured not assumed.
- 2026-08-18: two positions FELL and are superseded in the CORE with
  dated rationale, text kept. The **four-rule pair selection** (log
  024 §2 decisions 1/2/11, python's 13,689 cross product cut to 200
  pairs) fell to ruling 2 — it was a cost compromise made before the
  cost was measured, and a selected pair set cannot prove an absence
  it never probed. The **tier-B sampled placement** policy fell to
  ruling 3 — log_025 §4 priced the full matrix at under one percent,
  which removes the reason for the split; "tier B" survives as the
  name of the per-slot placement probe only. The python phase-2
  results stay valid as measurements of what they covered.
- 2026-08-18: the go cross-check in log_026 §2.1 is recorded in the
  CORE as the **counter-example** to the anti-interpretation rule —
  it reproduced go's acceptance set from a hand-lifted rule without
  invoking the checker's expression path, and it AGREED, which is
  precisely why it is instructive: agreement does not make a
  transcription evidence. Such a step is now a route-B draft
  awaiting certification.
- 2026-08-18: open items recorded as open — bisect/batching for
  compiled-language execution probes still unbuilt (log_025's
  batched figure is a lower bound, not a schedule); route A2
  unverified for kotlin, swift, dart and csharp; and log_024
  decision 3 (holders that partially refused loading get probed on
  the values they did load) standing as the owner-default-yes, not yet
  explicitly ruled.
- 2026-08-18: phase 3 BUILD STEPS done and measured (log 027). The
  shared progress instrument exists (`Research/kind_fuzz_clustering/
  progress.py`, python face + shell twin) and every generator, lane
  and reader in this node now prints [done/total], elapsed and ETA,
  flushed per tick so a running lane is pollable.
- 2026-08-18: route A2 VERIFIED per language, closing that open item.
  swift `swiftc -typecheck` PROVEN (177 ms accepting, no artifact
  written); dart `dart analyze` PROVEN and it batches natively at
  1.3 ms per probe over a directory; csharp has no usable flag but
  its shipped Roslyn checker answers in-process at 1.44 ms per probe,
  so csharp moves to route A1; kotlin route A2 is REFUTED — no
  check-only flag exists — and its measured mitigation is a warm
  in-process compiler at 123 ms per probe against 2,463 cold, a 20x
  drop that takes log 025's 206 h to about 10.4 h (derived).
- 2026-08-18: the bisect/batching crux is BUILT, raced, and answered
  AGAINST batching. Over 400 go probes: per-file serial 22.4 s,
  per-file parallel 7.8 s, batched-100-with-bisect 42.2 s, all three
  agreeing on all 400 verdicts. Batching needs 796 compiles to settle
  400 probes because full enumeration makes refusals the majority
  (375 of 400), which turns a bisect into a full binary walk. log
  025's batched projection rested on batches selected in advance to
  compile and does not survive full enumeration. Runs use per-file
  parallel, except where a check-only tool recovers from errors
  instead of aborting, which is dart alone.
- 2026-08-18: the probe space is enumerated and COUNTED before any
  run — go 7,600 acceptance probes, rust 9,196, cpp 10,944, swift
  3,456, dart 10,625, csharp 18,000, kotlin 11,492, with the full
  value-matrix answer counts printed alongside. Seven acceptance
  lanes and three route-C lanes generated and launched in cost
  order, kotlin last. Go finished inside the session: 7,600 probes,
  179 accept, 7,421 refuse, 132.4 s.
- 2026-08-18: the certification gate earned its keep on first use.
  Go's `+` acceptance set (7 pairs, all same-holder, all
  numeric-or-string) matches the lifted go map exactly and that cell
  is CERTIFIED. Go's `<<` accepts 16 pairs where the recorded lift
  predicts 4, and `==` accepts 36 where the lift has no row at all —
  both recorded as findings, neither reconciled. Ruling 6 holds: the
  lift is incomplete and only the compiler's own verdicts showed it.
- 2026-08-18: one decision surfaced rather than buried — the
  `identity` form's holders are excluded from operand pairs, because
  their layer-2 probes end in a verdict word rather than in an
  operand. Decision, not ruling; cheapest thing in `l3_accept.py` to
  overturn.
- 2026-08-18 (harvest, later the same day): **all seven acceptance
  runs COMPLETE** — 71,313 probes, 5,842 accept, 65,471 refuse, 1,644 s
  wall (log 027 §3.1). Per language: go 179 accepts of 7,600; rust 236
  of 9,196; cpp 1,102 of 10,944; swift 80 of 3,456; dart 1,170 of
  10,625; csharp 1,127 of 18,000; kotlin 1,948 of 11,492. **All three
  route-C runs complete too** — python 342,225 probes / 100,597
  answers / 381.8 s, ruby 261,382 / 60,428 / 2.8 s, php 215,306 /
  94,690 / 0.8 s, and 0 refusals in all three, which is the expected
  shape: open dispatch refuses nothing at compile time. **890,226
  probes measured in total**, and every one of the ten result files
  folds to its own driver's printed count.
- 2026-08-18: **the cost picture inverted.** Kotlin, the villain of
  this node's budget since log 025 put 206 of 435 hours on it, measured
  52.1 ms per probe at full scale — better than the 123 ms the build
  step predicted, because a held-open JVM keeps warming. **C++, at
  60.9 ms, is now the most expensive compiler per probe of the seven.**
  Dart 0.98 ms, csharp 1.51 ms, rust 6.8 ms, go 17.4 ms, swift 42.5 ms.
- 2026-08-18: **three lanes died mid-run and all three exited 0** —
  rust EBUSY on `-o /dev/null` (all 236 accepts masked as refusals),
  php an uncatchable `Cannot redeclare class` fatal (2,001 of 215,306),
  python a SIGKILL out of memory (19,829 of 342,225, a sequence holder
  times the `i64max` value class asking for a list of 9.2e18 elements).
  All three found, fixed and re-run. The mitigation is BUILT, not
  remembered: `l3_read.py` carries a completeness gate and every result
  file states `complete`. **A lane's exit code is not evidence that it
  finished.**
- 2026-08-18: **the first cross-language behavioral regularity this
  node has produced.** The shift exemption from the same-type
  requirement, found by measurement in go, holds in rust (16 accepts,
  4 same-holder), csharp (18/3) and cpp (25/5), and java's route-B
  lift — extracted mechanically, never read — carries the mixed
  `SL|INT|LONG` and `SL|LONG|INT` rows explicitly while every other
  arithmetic tag in that table carries only same-type rows. Two
  independent routes in two languages agreeing on a shape neither was
  looking for. Exactly the kind of cell phase 4 clusters on.
- 2026-08-18: two more route-B findings recorded, neither reconciled.
  Java's `Operators` table extracted mechanically at **86 rows** where
  log 026 §2 recorded 23. And the rust lift DID NOT RUN — `rust-src`
  is absent in the container, contradicting the working assumption that
  it was installed; one `rustup component add rust-src` away from a
  second certified language, since rust's acceptance side is complete.
- 2026-08-18: the widest acceptance spread measured anywhere — logical
  and (`&&`) accepts 112 ordered pairs in cpp against 1 in go, rust,
  csharp, kotlin and swift, because cpp converts almost any holder to
  `bool` implicitly. And a comparison hazard recorded: 388 of dart's
  1,170 accepts involve a `dynamic` operand where the checker is
  switched off (`dynamic null * dynamic null` ACCEPTS), so dart's A2
  numbers are not the same kind of measurement as the other six.
- 2026-08-18: a fourth silent loss, this one on the READING side — the
  result format delimits with `|` and probe ids END with the operation,
  one of which is a bare `|`, so the fold dropped exactly one
  operation's rows per language (11,881 ruby, 8,281 php). Caught only
  because the driver's own printed total disagreed with the folded
  count; fixed by locating the verdict word rather than counting
  delimiters. The lane was healthy and the data was still being lost.
- 2026-08-18 (close-out, log 028): **all twelve languages now have
  layer-3 acceptance evidence.** The two harnesses log 027 left unbuilt
  are built and run — java through `javax.tools`
  (`JavacTask.analyze()`, one JVM, 20,480 probes, 981 accepts, 3.41 ms
  per probe) and typescript through the checker shipped inside
  `typescript.js` (12,167 probes, 2,318 accepts, **0.34 ms per probe**,
  the cheapest checker of the eleven measured). Both were checked in
  both directions before their numbers were believed. The pattern in
  the cost table is now unmistakable: the four cheapest routes are the
  four whose checker can be CALLED rather than launched.
- 2026-08-18: **the certification gate has been run, and rust is this
  node's first CERTIFIED language** — 490 cells compared, 490
  agreements, zero disagreements, after `rustup component add rust-src`
  and a mechanical expansion of `core::ops`'s own macro templates by
  its own argument lists (407 rows). Rust's shift exemption is now
  attested twice, independently: by its source data (`Shl` has 144
  rows, every ordered pair, where `Add` has 16 same-type rows) and by
  rustc itself.
- 2026-08-18: **java is not certified: 931 cells compared, 785 agree,
  146 disagree** — and every one of the 146 is javac ACCEPT against
  lift REFUSE, never the reverse. The cause is measured: javac applies
  binary numeric promotion to the operands BEFORE consulting its
  `Operators` table, so `int + double` reaches the table as
  `DOUBLE + DOUBLE`. The lift is incomplete, not wrong. Java's shift
  and logical tags certify with zero disagreements, which is the
  corroboration log 027 §4.4 asked for.
- 2026-08-18: **across three lifted languages, no lift ever said ACCEPT
  where the compiler said REFUSE.** Every failure was an omission — a
  silent operation (go), a missing upstream step (java), nothing at all
  (rust). Recorded as a hypothesis at level derived: a lifted table
  under-states and does not over-state, so it is safe to read as a
  lower bound on acceptance and never as an upper one.
- 2026-08-18: **the java 23-versus-86 discrepancy is RESOLVED, and the
  resolution is arithmetic.** One table, two counts: 86 rows
  `(tag, lhs, rhs, result)` and 23 distinct ordered operand pairs. The
  A1 evidence settles which governs acceptance — java's twenty
  operations produce SEVEN different accepting pair sets, so a verdict
  is not a function of the operand pair alone and 23 entries cannot
  express the table. 86 is carried forward, and it is still incomplete
  per §4.3 above.
- 2026-08-18: **the shift exemption has an exception and it is
  typescript.** Java's acceptance run confirms the exemption by
  measurement (25 accepts on `<<`, only 5 same-holder, the full 5-by-5
  cross product of its whole-number holders). Typescript refuses it:
  5 accepts, all same-holder, `number << bigint` REFUSED. Six of seven
  languages exempt shifts; the seventh is the one whose whole-number
  holders are two disjoint families rather than a promotion ladder.
- 2026-08-18: two acceptance records changed hands. Typescript's `??`
  accepts **529 of 529** ordered pairs, taking the most-permissive
  title from kotlin's elvis at 673 of 676; and typescript's `&&`
  accepts 506 of 529, beating c++'s 112 of 576, so logical and is a
  spectrum rather than the two-camp story log 027 recorded.
- 2026-08-18: **the FULL VALUE MATRIX for the nine statically checked
  languages is BUILT and RUNNING** — 2,221,643 probes, 26 shard lanes,
  10.32 hours projected from measured per-probe costs, launched in cost
  order. It measures the assumption every acceptance run in this node
  rests on: that a checked language's verdict is a function of the
  holder pair and not of the value. Five shards had landed at
  close-out, all at or under projection; 437,942 probes measured
  already.
- 2026-08-18: **and the first complete matrix REFUTES the assumption it
  was built to test.** Typescript splits on **876 of its 12,167 cells**
  — 7.2 percent give different verdicts for different VALUES of the
  same two holders — and none of the 876 is a failure to load; they are
  all at the operation level *(measured, on a file the gate marks
  complete)*. The four-line case: `false == false` type-checks and
  `false == true` does not, because typescript narrows each variable to
  its literal type and then refuses a comparison it can see has no
  overlap. So *a checked language's verdict is a function of the holder
  pair* is now known to be false as a general statement, and every
  acceptance-grain verdict in this node is a verdict for the value
  class its run happened to carry until that language's matrix lands.
  Java, csharp, dart and rust show splits too on part-finished shards,
  but theirs look like the value failing to LOAD rather than the
  operation refusing — layer 2 leaking into layer 3, which is log 024
  decision 3 arriving as a measurement. A control probe that settles
  which is which (`l3_matrix.py --loadcheck`, 1,046 probes, ~21 s) is
  built and queued.
- 2026-08-18 (log 029): **phase 4 opened — manifests frozen, and a
  PRELIMINARY clustering run.** The twelve `manifest_<lang>.json` files
  make a positional raw line (`P7_10_1_3_2|ACCEPT|OK`) decodable
  forever without the generator: each is a replay of the generator's
  enumeration with **no probes run**, mapping every probe id to its
  operation and both operands' form, holder, value class and literal
  declaration text. They verify three ways — every landed shard's line
  count matches, **520 of 520 spot-checked ids resolve** (449 of the
  460 grid-comparable agreeing, and all 11 differences confirmed to
  sit inside measured `split` cells), and,
  independently of the replay, **all nine route-A manifests agree with
  the frozen table each lane script carries inside itself, zero
  mismatches** *(measured)*. In-flight runs got manifests too, which is
  the point of freezing now.
- 2026-08-18 (log 029): **the value-matrix harvest moved a long way and
  the gate did its job.** 23 of 26 shards landed; **seven matrices are
  COMPLETE** — typescript, csharp, java, rust, go, swift and kotlin,
  whose sixth and last shard landed partway through the session — and
  two are refused by the completeness gate and contribute nothing (cpp
  not started, and **dart's second shard was never queued at all**, a
  gap rather than a wait). Nothing running was disturbed: only shards
  whose own status file said `done` were copied. The grid's error bar
  is now measured where it can be: **go's acceptance grid is exactly
  right, 7,600 of 7,600 cells; kotlin's is wrong on 150 of 11,492;
  typescript's on 704 of 12,167, 5.8 percent** *(measured)*. Kotlin
  also has the most value-dependent cells of any language measured,
  **1,234 splits of 11,492, 10.7 percent** — more splits than
  typescript but ten times fewer grid errors, which are two different
  statistics and are kept apart.
- 2026-08-18 (log 029): **the clustering machinery rediscovered the
  shift exemption and then corrected how we had been stating it.** 233
  operation signatures over twelve languages, projected onto the shared
  64-cell layer-1 form space (the projection is decision 1 and is
  stated as a choice, not defended); 46 clusters at the 0.70 cut, 58 at
  0.85; **2,909 relation edges** across nests / nested_by / overlaps /
  equals / contradicts. The exemption was measured by a statistic that
  names no operation and no language, and the shifts came out on top —
  `>>>` 0.80, `<<`/`>>` 0.619, against `+` 0.482, `-` 0.384, `*` 0.325
  *(measured)*. **But the per-language table says the five languages we
  had been naming together are two phenomena**: in go and rust the
  exemption is total (shifts 0.75, arithmetic 0.00 to 0.14), and in
  java, c++ and c-sharp it is barely measurable (java's shifts 0.80,
  java's `+` 0.78) because implicit numeric promotion already mixes
  their arithmetic holders. It stands two languages against two, and
  **no run still in flight can break the tie** — kotlin and swift have
  no shift spellings in their grammars at all *(measured)*, so
  settling which pattern is the common one needs more languages, not
  more values. Level derived for the promotion
  attribution; log 028's 146 java certification findings are
  independent support. Shifts and bitwise operations do form a
  cross-language cluster (go, java and rust shifts together); `+` does
  **not** cluster, splitting by how much the language coerces, and
  string concatenation never lands apart from numeric `+` in any of the
  ten languages that have one.
- 2026-08-18 (log 029): **the relation machinery found an instrument
  fault without being asked to.** All 7 `contradicts` edges involve
  dart's `||`; chased to the cell, dart records `bool && bool` ACCEPT
  and **`bool || bool` REFUSE with an empty error detail** *(measured)*
  — a refusal, with no error text, on the one cell all eight other
  languages accept, beside a sibling operation that accepts it. Cause
  **unverified**, recorded as a finding and not reconciled silently.
- next: **drop `vm_dart_01.sh`** — it is the only thing standing
  between dart and a complete matrix, and it was never queued. Then
  wait out c++'s six shards, collect the nine
  queued `ld_<lang>_00.sh` load-check lanes that classify every split,
  and **re-run phase 4 as non-preliminary**: decision 9 says the value
  matrix then becomes the primary domain for the nine checked
  languages instead of an overlay. The genuinely unbuilt thing is
  still route C for the nine — the matrices give VERDICTS, not
  ANSWERS, and the CORE's phase-4 pair is {domain accepted, answer per
  input}, so this pass has the answer half for three of twelve
  languages. The cross-check against `kind_signature_clustering`'s
  signature clusters — the mutual-checkability symmetry the CORE opens
  with — has not been started.
- (the earlier 2026-08-18 "next", kept for the record and now answered by log 029) harvest the value matrix — `python3 l3_matrix_read.py` after
  copying `agent/out/vm_*.txt` into `raw/` — and read `split_cells`
  first. Then the one genuinely unbuilt thing left: route C for the
  nine checked languages, which is compile-and-run over the ACCEPTED
  cells only, the one case where batching survives log 027 §2.3's race
  because the accepted probes are known in advance to compile. Phase 4
  (relate + cluster) is unchanged and is now fed by all twelve.
- (the earlier 2026-08-18 "next", kept for the record and now answered by log 028) every lane is DONE and harvested; nothing is running in the
  container. Remaining work is build work — run
  `rustup component add rust-src` and
  re-drop `lift_b.sh` for the rust certification, then build the two
  unbuilt route-A1 harnesses — java via `javax.tools` first, since its
  route-B lift cannot be certified without it, then typescript via the
  shipped checker. The full value matrix for the nine statically
  checked languages remains counted but unbuilt. Phase 4 (relate +
  cluster) is unchanged.
- (the 2026-08-18 morning "next", kept for the record and now answered by the build results above) phase 3 is now the all-twelve run UNDER THIS DESIGN, and its
  first build steps are the bisect, the A2 verification for the four
  unverified languages, and the progress/ETA instrumentation. Phase
  4 (relate + cluster) is unchanged.
- (the 2026-08-17 "next", kept for the record and now answered by the
  2026-08-18 rulings) phase 3 (the other ten) is GATED on the owner's review of the eleven
  design decisions — log 024 §6 names what to review first: the run size
  that decisions 1/2/11 set, the unbuilt bisect (decision 5), whether a
  REFUSES-behavioral cell is an input (decision 3), the five languages whose
  keyed grouping needs a constructor call, and whether the clustering can
  express a NESTS relation inside one language.
- (the 2026-08-15 "next", kept for the record and now answered) phase 1 — probe design, blocked on six rulings listed in log
  021 §6; the first is whether the operator menus multiply (3,556 or
  7,140), the second is the dict gap in java/csharp/rust/cpp/kotlin and
  the boolean gap in kotlin, which can only be closed by opening
  builtins.
