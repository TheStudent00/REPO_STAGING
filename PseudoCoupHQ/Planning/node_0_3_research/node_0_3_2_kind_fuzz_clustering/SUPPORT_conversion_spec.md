---
id: hq.research.kind_fuzz_clustering.support.conversion_spec
status: settled
settled_by: the owner
---

# SUPPORT — conversion spec

Ruled by the owner 2026-08-20 in conversation; recorded here as SETTLED, not
proposed. Implemented the same day by
`Research/kind_fuzz_clustering/l3_matrix_extended.py`, which emits
`matrix_extended_base.csv` and `matrix_extended.json` by assembly over
the layer-3 answer data already on disk — no probe runs. Report:
`DevComms/log_044_extended_matrix_and_conversion_spec.md`.

## the governing rule (the owner's design, quoted)

> never compare raw answers, compare their decompositions, and let
> WHICH coordinate disagrees be the feature.

## the base matrix

- **Rows**: the 64 `form|form` pairs over the eight forms — nothing,
  truth, whole, fractional, text, sequence, keyed, nesting.
- **Columns**: every `lang.op` signature the answer-grain artifact
  carries. (The design conversation said 233, which is the log-030-era
  count; after logs 034/035 admitted the word-spelled operations the
  artifact holds **239**, and the matrix follows the data.)
- **Cell**: the SET of answer forms that came back, with `refuse`,
  `raise` and (in the extension layers) `not-applicable` as first-class
  distinct cell elements. `abort` occurs in the data (c++ `SIGFPE`,
  segfault) and is carried as a first-class element too.
- **Rectangular, never sparse**: a cell with nothing behind it reads
  `REFUSE`, whether the pair was never probed for that signature or was
  probed and declined; nothing is omitted.
- **Spelling-blind**: only form names survive into the base cell —
  `whole:-2` and `whole:84` are both `whole`.

## extension layers

Each layer is an ADDED coordinate set. Nothing is replaced; the base
matrix stands unchanged underneath.

### 1 — numeric decomposition

Every numeric answer becomes `[sign | mantissa | exponent | special]`.

- `special` carries `inf`, `nan`, `negzero`, which do **not**
  decompose further.
- The cast is unbounded EXACT — python `int` / `fractions.Fraction` —
  never floating, so precision is not destroyed by the conversion
  itself. A print-grain decimal token is cast exactly AS PRINTED; what
  the printer already destroyed stays destroyed.
- For a non-zero value v: `sign` is ±1; `|v| = mantissa × 2^exponent`
  with mantissa an exact rational in [1, 2); the exact absolute value
  is carried beside them. **Absolute value AND sign are kept as
  separate derived coordinates** (the owner: both matter).
- **Wrap relations become features**: when two columns' unbounded
  values in the same input cell differ by exactly `2^w`, the
  congruence is recorded (e.g. `≡ mod 2^64`) instead of a mismatch.
  The same rule applies within one column when two holders of one
  cell disagree by a power of two. Mechanical floor: `w ≥ 8`, so a
  difference of 2 or 4 reads as arithmetic rather than wrapping;
  overturnable.

### 2 — container canonicalization

Cast to dict-list; cell = `[sorted values | key format | order flag]`.

- A sequence becomes a dict keyed 0..n−1; sorting the values makes
  integer-keyed and text-keyed containers comparable.
- `key format` (`integer` / `text` / `mixed`) and `order flag`
  (`as-sorted` / `reordered` / `unordered` / `not-applicable`)
  preserve exactly what the sort destroys.
- The numeric cast of layer 1 applies **recursively** to keys and
  values.

### 3 — text decomposition

`[utf-8 bytes | codepoint length | grapheme length | NFC-normalized
form]`. The existing `STR:<byte-len>:<codepoint-len>` encoding of
`answers_encoding.md` already carries two of these layers. Grapheme
length uses a documented fallback extended-grapheme-cluster
approximation (combining marks, ZWJ joins and regional-indicator pairs
do not start a new cluster); exact for the probe alphabet in use.

## the applicability rule

An extension coordinate that does not apply to a cell reads
`not-applicable` — a truth answer has no mantissa, a raise has no
container. **`not-applicable` is DISTINCT from refuse**: refuse says
the language declined the question; not-applicable says the coordinate
asks no question of this answer at all.

## worked examples (real cells)

### int64 wrap, `≡ mod 2^64`

Input cell `whole|i64max|whole|base_42`, column `go.+`:
`whole:-9223372036854775767` (int64 holders) beside
`whole:9223372036854775849` (uint64 holders). `python.+` answers
`whole:9223372036854775849`. Raw comparison says mismatch three ways;
the decomposition says: same residue, and

```
go.+ ~ python.+ : whole:-9223372036854775767 vs
                  whole:9223372036854775849   ≡ mod 2^64
go.+ ~ go.+     : the same pair WITHIN the column, int64 against
                  uint64 holders               ≡ mod 2^64
```

— 9 such pairs on that one input cell (also cpp, csharp, kotlin,
ruby), and the coordinate that disagrees (sign, exponent) is the
feature while the congruence certifies the shared arithmetic.

### ruby Set against python list

Input cell `sequence|empty|sequence|strs`: `ruby.<<` (a Set holder)
answers `keyed:{#<Set:{'a','b'}>}`; `python.+` answers
`sequence:['a','b']`. Canonicalized:

```
ruby Set  → sorted_values ['text:61','text:62'], key_format integer,
            order_flag unordered
python    → sorted_values ['text:61','text:62'], key_format integer,
            order_flag as-sorted
```

Same sorted values — the containers agree on WHAT they hold — and the
order flag alone carries the disagreement, which is exactly the
feature.

### php `+` left-operand values

Input cell `whole|i64max|whole|base_42`, column `php.+`:
`fractional:9.2233720368548e+18` beside `raise:Error`. The numeric
decomposition of the fractional token is sign +1, exact value
9223372036854800000 — NOT congruent to the others mod any `2^w`,
because php promoted to double and the print destroyed the low digits
before this spec ever saw them. The exact cast preserves precision; it
does not invent precision the printer discarded, and the coordinate
that disagrees (mantissa, at exponent 63) is the finding. (Log 031's
separate left-operand fault in php's word logicals — `and`/`or`/`xor`
recording the LEFT OPERAND — is decision 30/44 territory and arrives
in this matrix through the de-VOIDed rows as ordinary cells.)

## products

- `Research/kind_fuzz_clustering/l3_matrix_extended.py` — assembler,
  reusing `l3_answers12.py`'s `load_three`/`load_nine` so the token
  space is the one the clusters stand on.
- `Research/kind_fuzz_clustering/matrix_extended_base.csv` — 64 × 239.
- `Research/kind_fuzz_clustering/matrix_extended.json` — interned
  `token_decompositions` (6,155 tokens), per-column per-input-cell
  token lists at the value-pair grain, and 63,111 recorded
  congruences.

## 2026-08-20 — the per-operator matrices (settled, settled_by the owner)

Ruled by the owner 2026-08-20 in conversation, over several corrections;
recorded as SETTLED. Implemented the same day by
`Research/kind_fuzz_clustering/l3_per_op_matrices.py`, which emits one
CSV per `lang.op` into `Research/kind_fuzz_clustering/matrices/`
(plus `index.json` and a `README.md` carrying the filename escaping
and its reverse map). Assembly over the answer data on disk; no probe
runs. Report: `DevComms/log_046_per_operator_matrices.md`.

- **Own matrix per `language.operator`.** No shared cross-language row
  space, no padding rows for holders a language lacks. **One PROBE per
  row.** Columns identical on every row of every matrix: `lhs_holder`,
  `lhs_bytes` (as the language holds them), `lhs_canonical`; the same
  three for `rhs`; `output_literal` (the language's own result
  spelling/payload, EMPTY if no value), `output_canonical` (EMPTY if
  no value); indicator columns `REFUSE`, `RAISE`, `ABORT` (0/1) and
  `raise_kind` (empty otherwise). The implementation adds uniform
  bookkeeping columns (`probe_id`, the value-class names,
  `output_type`, and the `*_canonical_exact` machine columns); every
  matrix is rectangular at 19 columns.
- **Inputs are filled on EVERY row** — lhs/rhs bytes and canonical are
  known from the value class and the rep's read-rule, independent of
  outcome. A rep's read-rule applies: `ctypes.c_int64` holding bytes
  `8000000000000000` canonicalizes as `[-1, 1, 63]` (the rep flips the
  reading) while an unbounded int reads `[1, 1, 63]`.
- **Numeric canonical is `[sign, mant, expo]`** with sign ∈ {−1,0,1},
  **mant ∈ [1,2) — floating-point normalization**. The earlier
  integer-mant reading was a misunderstanding and was **rejected
  because the decomposition is not unique** (any mant can be doubled
  while the exponent drops; the [1,2) window makes it single-valued).
  Zero = `[0, 0, empty]`. Specials stay words: `inf`, `nan`,
  `negzero` (and `-inf` for negative infinity in outputs). Full
  precision is kept in a machine column (`*_canonical_exact`, the mant
  as an exact rational) beside the readable decimal mant, which is
  marked with `~` when the decimal is rounded (18 fractional digits).
- **Text canonical** is `[NFC utf-8 hex, byte_len, codepoint_len,
  grapheme_len]` (grapheme fallback as documented in
  `l3_matrix_extended.py`); **container canonical** is
  `[sorted values | key_format | order_flag]` per the layers above.
- **REFUSE rows live here too**: the static languages' compile
  refusals from `acceptance_<lang>_A2/A1.json` appear as rows with
  inputs filled (at the acceptance stage's representative value class,
  `BASE_ORDER` of `l3_accept.py`), outputs empty, `REFUSE=1` — the
  answers files hold only the accepted subset and cannot supply them.
  `codegen_refuse` rows inside the answers files join them with their
  own value classes. `ABORT` is the stopped-by-OS outcome; its rows
  carry inputs, empty outputs, `ABORT=1`.

## 2026-08-20 — FINAL canonical-form rulings (settled, settled_by the owner)

Ruled by the owner 2026-08-20, settled; these OVERRODE the earlier forms of
the section above after repeated miscommunication. One line of
history: integer mants were rejected (the decomposition is not
unique), then the rational-mant reading with `~` rounding markers and
`*_canonical_exact` columns was ALSO rejected — fractions and
rationals are banished from every visible column, and the exact
rationals moved to a side file. Implemented the same day by
`Research/kind_fuzz_clustering/l3_per_op_matrices_v2.py`
(re-emitting `Research/kind_fuzz_clustering/matrices/`); the v1
generator stays on disk for the audit trail. Recorded verbatim:

1. Canonical numeric form: `[sign, mant, expo]` where sign ∈ {−1, 1}
   (0 not used; see zero rule), mant is a DECIMAL floating-point
   string in [1,2) with 31 significant fractional digits (a knob;
   never fewer), expo integer. Intended look:
   `[-1, 1.0324876324798, 23]`. NO fractions/rationals in any visible
   column. NO `~` markers. NO arrows or annotations inside cells.
   Exact rationals go to a SIDE file (`matrices/exact_sidecar.json`),
   never the CSVs.
2. Zero: `+0.0` = `[1, 0.0, 0]`, `-0.0` = `[-1, 0.0, 0]` — the word
   negzero is retired. Infinities: `[1, inf]` / `[-1, inf]`. `nan` is
   the only special word kept. Use ascii `-` everywhere.
3. Bytes columns: exactly as the language holds them (fixed-width
   holders keep leading zeros: c_int64 42 = `000000000000002a`;
   unbounded minimal: `2a`). Never annotate or transform.
4. Columns per matrix (one CSV per lang.op, one probe per row):
   `probe_id, lhs_holder, lhs_value_class, lhs_bytes, lhs_canon,
   rhs_holder, rhs_value_class, rhs_bytes, rhs_canon, output_bytes,
   output_canon`. The old indicator columns
   (REFUSE/RAISE/ABORT/raise_kind) are RETIRED: outcome tokens go IN
   `output_canon` as `REFUSE`, `RAISE:<kind>`, `ABORT` (universal
   vocabulary only, never language message text). `output_bytes`
   empty when no value.
5. lhs/rhs_canon include the rep read-rule (c_int64 holding bytes
   `8000000000000000` canonicalizes `[-1, 1.0, 63]`).
6. Text canon: `t|<NFC utf-8 hex>|byte_len|codepoint_len|grapheme_len`.
   Container canon: `c|<sorted member canons>|key_format|order_flag`.
7. REFUSE rows from the acceptance files stay as rows (inputs filled,
   `output_canon` = REFUSE).

Implementation notes (decided, on record, overturnable): the readable
mant strips trailing zeros to a one-fractional-digit minimum
(`[-1, 1.0, 63]`), the 31-digit knob bounding the rounding; RAISE
kinds are the recorded kind tokens with package prefixes stripped
(`java.lang.X`→`X`, `System.X`→`X`, `_TypeError`→`TypeError`,
`Encoding::CompatibilityError`→`CompatibilityError`) and go's
message-text raise spelled `IntegerDivideByZero`; the exact sidecar is
keyed by the canon string it was rounded into.

Verification against the owner's approved example (python.+, base_42 +
i64max_plus1, 16 rows): int+int, int+c_int64 (with rhs_canon
`[-1, 1.0, 63]`) and the Decimal↔Fraction `RAISE:TypeError` rows all
match byte-for-byte. The c_int64+c_int64 row does NOT: the recorded
answer (`behavior_python_C.json` cell `P5_5_base_42_i64max_plus1_+`)
is `int:-9223372036854775766`, which canonicalizes
`[-1, 1.9999999999999999908927017511218, 62]`, not the example's
`[-1, 1.0, 1]` (= −2). Reported to the owner, not papered over.

### string clustering over the final canonical strings (same ruling)

Similarity between two `lang.op` matrices = row-match rate on the
canonical strings: align rows by the (lhs_canon, rhs_canon) input
pair; where both matrices carry the pair, score 1 iff the
`output_canon` strings are byte-identical, else 0; similarity = mean;
pairs present in only one matrix are excluded (no padding); columns
with no shared input pairs score 0 and stay as leaves. UPGMA average
linkage as in `l3_dendro_extended.py`. Decided detail (overturnable):
a pair carried by several holder rows compares as the sorted SET of
distinct output_canon strings (a multiset would make holder COUNT a
disagreement). Products:
`Research/kind_fuzz_clustering/l3_dendro_strings.py`,
`dendro_strings.json`, `dendrogram_strings.html`. Report:
`DevComms/log_047_final_canon_and_string_clustering.md`.

### the agreement GRAPH replaces the set-identity clustering (2026-08-21, the owner's design settled 2026-08-20)

The set-identity aggregation used by `l3_dendro_strings.py` (compare
the sorted SET of distinct output_canon strings per input pair) is
REJECTED by the owner: it zeroed cross-language pairs (go.+ ~ python.+ =
0.0000) even though individual rows match byte-identically. The
settled comparison is the ROW-grain best-match GRAPH: each of the 242
`lang.op` matrices is a node; edge weight = matched shared input
pairs / shared input pairs, where a pair matches iff ANY row of A and
ANY row of B for that (lhs_canon, rhs_canon) have byte-identical
output_canon; pairs in only one matrix are excluded; no shared or no
matched pairs → no edge (never a 0-weight edge); each edge also
carries n_shared, n_matched, and the VALUE-only rate
(REFUSE/RAISE:*/ABORT rows excluded from both sides) so decline- and
value-agreement stay separable; the threshold is a spectrum (explorer
slider). Under this rule go.+ ~ python.+ = 0.3432 and go.+ ~ rust.+ =
0.9471. Products: `Research/kind_fuzz_clustering/l3_agreement_graph.py`,
`agreement_graph.json`, `graph_explorer.html`. Report:
`DevComms/log_048_operator_agreement_graph.md`.

### interval sampling — the tensor extension (2026-08-21, the owner's design settled 2026-08-20/21)

Today's value classes are EDGE values only, six per form. Six points
per side let coincidental agreement survive: two operators can match on
every shared input pair and still be different functions. The extension
adds INTERVAL sampling — N samples per side spanning each holder's own
representable range — **in addition to** the edge classes, never
replacing them. Pilot: **N = 32 per side, NUMERIC forms only (whole,
fractional), two languages only (rust, static; ruby, open dispatch /
route C)**. Text and containers keep their edge sets untouched;
an interval is meaningless there. Acceptance is NOT re-run: every
interval sample lives inside its own holder's range, so the recorded
verdicts still hold.

**The ladder is deterministic and closed-form** — no random draw, no
seed, no per-run variation. Every magnitude is an exact integer root of
a power of two computed in integer arithmetic, so a re-run reproduces
the same 32 values bit for bit.

Whole holder, signed, width `W` bits (range `-2^(W-1) .. 2^(W-1)-1`):

- 6 near-boundary anchors `[min, min+1, -1, 0, 1, max]`
- 13 log-spaced magnitudes `m_k = floor(2^(k*(W-1)/14))`, `k = 1..13`,
  as the exact integer 14th root of `2^(k*(W-1))`
- the same 13 magnitudes NEGATED — both signs, the holder is signed
- 6 + 13 + 13 = 32

Whole holder, unsigned, width `W` bits (range `0 .. 2^W-1`):

- 4 near-boundary anchors `[0, 1, max-1, max]`
- 28 log-spaced magnitudes `m_k = floor(2^(k*W/29))`, `k = 1..28`
- 4 + 28 = 32, one sign only

Unbounded whole holders (ruby `Integer`, `Rational`, `BigDecimal`) have
no representable bound, so the ladder uses a NOMINAL 128-bit magnitude
window and the signed rule. The window is a recorded choice, not a
measurement: it matches the widest bounded whole holder in the pilot
(rust `i128`) so the two languages' ladders overlap where they can.

Fractional holder, binary floating, normal exponent range
`[emin, emax]`:

- 10 anchors: `+0.0`, `-0.0`, `+minsubnormal`, `-minsubnormal`,
  `minnormal`, `1.0`, `nextafter(1,2)`, `nextafter(1,0)`,
  `+maxfinite`, `-maxfinite`
- 11 log-spaced magnitudes `1.5 * 2^e_k`,
  `e_k = emin + round(k*(emax-emin)/12)`, `k = 1..11`
- the same 11 magnitudes NEGATED
- 10 + 11 + 11 = 32

The interval ladder carries FINITE values only. `inf` and `nan` stay in
the edge classes, where they already are — a ladder that spans a range
has no business inventing points outside it.

Ladder ids, one per distinct range: `w_s32`, `w_s64`, `w_u64`,
`w_s128`, `w_big128`, `f_b64`, `f_b32`.

**Row shape (the owner's words):** "each set of interval inputs and outputs to
be contained within in their own respective row." So the interval
results are NOT one row per sample. One row = one
`(operator, lhs holder, rhs holder, interval spec)`, carrying the input
sample VECTOR and the output result VECTOR in that row. the owner calls this
a tensor: a per-operator matrix, plus the sample axis inside each row.
They live in their own files, `matrices_interval/<lang>.<op>.csv`, with
columns

    probe_id, lhs_holder, rhs_holder, interval_id, n_samples,
    lhs_canon_vector, rhs_canon_vector, output_canon_vector,
    n_values, n_declines

Vectors are semicolon-separated canonical strings under the same canon
rules as `matrices/`. Every file is rectangular; every vector in a row
has exactly `n_samples` entries; **nothing is padded** — a sample that
produced no value carries its outcome token (`REFUSE`, `RAISE:<kind>`,
`ABORT`) in that slot, never an empty. The existing edge-value matrices
in `matrices/` stay exactly as they are.

**Edge criterion (the owner, settled 2026-08-21).** An edge between two
operator-nodes counts only when

    input_overlap >= output_agreement,
    input_overlap = shared input pairs / union of input pairs

Two nodes that agree on most of what they share, while sharing little of
what they span, are not neighbours — the agreement is an artefact of a
thin intersection. It is applied as a FILTER, not a deletion: every edge
is still emitted, still carries `n_shared`, `n_matched`, `n_union`,
`input_overlap`, `value_weight` and the EDGE-ONLY numbers, and carries a
`criterion_pass` flag, so the filter is inspectable and reversible. The
explorer has a checkbox for it.

Products: `Research/kind_fuzz_clustering/l3_interval_values.py` (the
ladder), `l3_interval_gen.py` + `l3_interval_ruby.py` (the lanes),
`l3_interval_read.py` (the tensor), `matrices_interval/`,
`l3_agreement_graph_interval.py`,
`agreement_graph_interval_pilot.json`,
`graph_explorer_interval_pilot.html`. Report:
`DevComms/log_049_interval_sampling_pilot.md`.

## the two-tier row graph

Ruled by the owner 2026-08-21 in conversation; recorded here as SETTLED, not
proposed. Implemented the same day by
`Research/kind_fuzz_clustering/l3_row_graph.py` by assembly over
`matrices_interval/` — no probe runs. Report:
`DevComms/log_050_two_tier_row_graph.md`.

the owner's design, quoted:

> "each row is its own node with a central node that connects all rows
>  to its respective node. meaning that `+` is a central node that `+`
>  rows connect to. so two types of connectors, internal and external"

**The row is the matching unit.** An interval row is NEVER split into
per-sample input pairs. Its 32 samples travel together as one
ladder-aligned vector and are matched position by position inside a
shared ladder. (This is the point of difference from
`l3_agreement_graph_interval.py`, which pooled per-sample pairs across a
whole operator; that builder and its products stand unchanged, but the
row graph does not use them.)

**Only `lhs_canon_vector`, `rhs_canon_vector` and
`output_canon_vector` contribute to scoring.** No other column of the
interval row enters a weight. `probe_id`, `lhs_holder`, `rhs_holder`,
`interval_id`, `n_values` and `n_declines` are carried on the node as
attributes for reading and searching, and nothing else.

**Two kinds of node.**

- A **ROW node** is one interval row, id
  `<lang>.<op> / <probe_id> / <lhs> <op> <rhs> / <interval_id>`. The
  probe id is part of the id because `(lang.op, lhs_holder, rhs_holder,
  interval_id)` is not unique — ruby spells some holder pairs more than
  once and each spelling is its own row and its own node. Attributes:
  language, operator, lhs_holder, rhs_holder, interval_id, probe_id,
  n_samples, n_values, n_declines, and `input_key` (a sha1 digest of the
  row's two input vectors).
- A **CENTRAL node** is one `lang.op`, id `rust.+`. Attributes:
  language, operator, n_rows.

**Two kinds of connector, kept distinct in the data and visually
distinguishable in the explorer.**

- An **INTERNAL** connector joins a row node to its own `lang.op`
  central node. Exactly one per row node. Internal connectors are
  STRUCTURE, not similarity: they exist regardless of any threshold and
  the threshold never cuts them. They carry a weight for display only —
  the mean pairwise output-vector agreement between this row and the
  other rows of the same operator that share its input vectors. A row
  with no co-row on its own inputs carries weight 1.0 by convention and
  the flag `no_comparison: true`. The explorer can show, hide, and fade
  them by weight.
- An **EXTERNAL** connector joins two row nodes of DIFFERENT operators
  — never two rows of one operator, which is what internal connectors
  are for. **An external connector exists only when the two rows carry
  IDENTICAL input ladders: byte-identical `lhs_canon_vector` AND
  byte-identical `rhs_canon_vector`.** Different ladders are not
  comparable, so there is no connector at all — not a low-weight one.
  Weight = the fraction of the sample positions at which the two
  `output_canon_vector` entries are byte-identical. Every external
  connector records `n_samples`, `n_matched`, `weight`, and whether the
  two rows are same-language or cross-language.

Note that `interval_id` is NOT the comparability test: `w_s128` and
`w_big128` are different ladder ids that produce byte-identical vectors,
and that identity is the only route by which rust `i128` rows reach
ruby's whole-holder rows. The test is on the vectors themselves, and
`input_key` is the digest that makes it checkable outside the builder.

Every external connector is emitted, including those at weight 0.0, so
the comparable universe is in the file rather than inferred; the
explorer, not the builder, does the cutting. The threshold slider cuts
external connectors only. The explorer draws at most 10,000 external
connectors, highest weight first with ties broken by position in the
file, and states that rule on screen whenever it bites.

Scope: interval rows only, numeric forms only. Text and containers are
excluded by construction and stay excluded. Both pilot languages.

Products: `Research/kind_fuzz_clustering/l3_row_graph.py`,
`row_graph.json`, `row_graph_explorer.html` (self-contained, data
embedded, no CDN), `verify_row_graph.js`.

## rulings A–E — element similarity, declines, the broken diagonal, physics

Ruled by the owner 2026-08-21 in conversation, after the two-tier row graph
above; recorded here as SETTLED, not proposed. Implemented the same day
by `Research/kind_fuzz_clustering/l3_row_sim.py` (A, B, E),
`l3_interval_c.py` + `l3_interval_c_read.py` (C, two probe runs) and
`l3_row_graph_v2.py` (the rebuild, D). Report:
`DevComms/log_051_element_similarity_and_broken_diagonal.md`.

The log-050 products — `l3_row_graph.py`, `row_graph.json`,
`row_graph_explorer.html`, `verify_row_graph.js` — and the log-049
`matrices_interval/` are kept UNCHANGED as the byte-identity audit
trail. Everything below is a v2 alongside them, never an edit to them.

### RULING A — similarity is PER ELEMENT and NUMERIC, not byte identity

A canonical numeric answer is `[sign, mant, expo]`. Two of them are
compared element by element, AS NUMBERS:

- **sign** — distance `|sign_0 - sign_1|`, which is 0 or 2. A sign flip
  costs real distance; the owner's call, because across a 32-point interval
  closeness that survives a sign flip is coincidence and the ladder
  makes it vanishingly rare. `sign_sim = 1 - d / 2`.
- **mant** — distance `|mant_0 - mant_1|`. Mants live in `[1,2)`, so
  the distance is already bounded by 1 and needs no scale constant.
  `mant_sim = 1 - d`, **clamped at 0**: zero canonicalizes to mant `0.0`
  and a mant that rounds up at the 31st digit spells `2.0`, so `d` can
  reach 2. Both are real distance and both floor at 0.
- **expo** — distance `|expo_0 - expo_1|`, an unbounded integer, so it
  needs a DECAY to become a similarity. **The decay is a KNOB and is
  flagged as one.** Default `expo_sim = 1 / (1 + d)`.

The three combine into ONE per-sample similarity, the owner's sketch,
**EUCLIDEAN**: the distance from the perfect point `(1,1,1)` in
element-similarity space, normalised by `sqrt(3)`, subtracted from 1.

    var_sim = 1 - sqrt((1-sign_sim)^2 + (1-mant_sim)^2 + (1-expo_sim)^2) / sqrt(3)

Every knob is a **single named constant** in `l3_row_sim.py` —
`EXPO_DECAY`, `EXPO_DECAY_K`, `COMBINE`, `COMBINE_WEIGHTS`,
`SIGN_MAX_DISTANCE` — and all of them are copied into the graph JSON as
`scoring_knobs`, so no number in the artifact is separated from the
settings that produced it. The documented alternative
`COMBINE = "weighted_mean"` is implemented and is one word away.

**FORM CLASSIFIER, not cast-and-catch.** Every `output_canon` declares
its form in its own prefix, so the classifier is TOTAL — every string
lands in exactly one form and nothing raises:

| prefix | form | rule |
|---|---|---|
| `[` | numeric | the element rule above. A NON-FINITE (`[1, inf]`, `[-1, inf]`) carries no mant and no expo to difference, so inside the numeric form it compares by IDENTITY |
| `nan` | numeric | the one special word the canon keeps; identity, same reason |
| `t\|` | text | identical NFC bytes → 1.0, else euclidean over the three length similarities |
| `c\|` | container | identity |
| `true` / `false` | truth | identity |
| `opaque:` | opaque | identity — a value the canon does not decompose (rust `Range`, ruby `Complex`) |
| `REFUSE` / `RAISE:<kind>` / `ABORT` | an outcome token | **not scored at all** — ruling B |

Same form → that form's rule. **Different form → similarity 0.** No
exceptions, no casting, no caught errors.

### RULING B — DECLINES ARE NOT SCORED AT ALL

the owner, quoted: "lets only do matching on similarity of actual objects
now. lets avoid things like REFUSE/RAISE/whatever-else."

- A sample position where EITHER row's output is `REFUSE`, `RAISE:*` or
  `ABORT` is **EXCLUDED from the comparison entirely** — out of the
  numerator AND out of the denominator.
- If two rows share an input ladder but have **zero** comparable
  positions after the exclusion, there is **NO connector between them**
  — not a zero-weight one.
- Every connector records `n_comparable`, `n_excluded_declines` and the
  weight. The old byte-identity weight is kept as a **SECONDARY**
  recorded number (`weight_byte`, `n_matched_byte`, over all
  `n_samples` positions so it stays directly comparable with log 050).
  The **PRIMARY** weight is the ruling-A/B one.

This retires the all-decline clusters — the ruby `&`, `|`, `^`, `<<`,
`>>`, `=~` family on Float/Rational/BigDecimal that scored 1.0 against
each other purely by refusing identically. `ruby.=~` declines on every
sample of every row and therefore now has no connector anywhere in the
graph.

### RULING C — break the diagonal

The log-049 sweep paired sample k with sample k, so every probe on a
same-ladder row was `v OP v`. Two more pairings are added, as
**ADDITIONAL rows with distinct `interval_id` spellings, the same column
schema and the same canon rules**. The diagonal rows are NOT
overwritten.

- **C1 SHIFTED** — `x_k OP x_{(k+1) mod 32}`. 32 more probes per row and
  no new values; the ladder already carries every point, only the
  pairing moved. `interval_id` `IV32:<a>|<b>:shift`.
- **C2 ONE-LEVEL COMPOSITION** — `op(op(x_k, x_k'), op(x_k, x_k'))`,
  each operator's own outputs fed back through itself. The composed
  operands are OUTPUT values, which mostly do not land on ladder points,
  so this is a real probe run AT the composed points. `interval_id`
  `IV32:<a>|<b>:comp1`. A comp1 row's `lhs_canon_vector` and
  `rhs_canon_vector` are BOTH the diagonal row's `output_canon_vector`;
  `lhs_holder`/`rhs_holder` keep naming the SOURCE operand holders so
  the row traces back to the diagonal row it composes.
- **Where an operand of the composition is a decline, the composed
  probe is NOT RUN and the position is excluded** (ruling B). ruby
  reports the operand's own outcome under the kinds `RAISEOP` /
  `REFUSEOP` so the count is visible rather than inferred; rust gets the
  same effect for free, because a panic while computing the operand
  unwinds the whole probe function and is caught as `RAISE:panic`.

The ruling-C rows live in `matrices_interval_c/`, a second directory
with the identical ten-column schema. `matrices_interval/` is opened for
reading only. The graph reads both directories together.

Composition type-validity is decided from data, never guessed: `y`'s
type is read out of the diagonal lane output's recorded
`std::any::type_name`, and `op(y, y)` is emitted only where
`(op, ty, ty)` is an ACCEPT cell in `acceptance_rust_A2.json`.

### RULING D — explorer physics

- **Internal connectors must NOT dominate the layout.** Their spring
  strength goes near zero — they exist to tether a row to its `lang.op`
  central node visually, and for nothing else. Recorded constants:
  internal `0.0008` against external `0.0060`.
- **EXTERNAL connectors carry the layout.**
- **Component counting remains EXTERNAL-ONLY**, whether or not internal
  connectors are drawn, at every threshold. The explorer's rule line
  says so on screen.
- The clamped springs, velocity clamp, gravity to centre, hard boundary,
  grid repulsion and periodic autofit are kept unchanged — that physics
  does not explode and is not to be re-tuned.

### RULING E — the internal connector weight is rescored

The internal connector weight is rescored under rulings A and B like
everything else: the mean ruling-A/B similarity with the co-rows of the
same operator that share this row's input vectors, taken over the
co-rows that have at least one comparable position. No co-row with a
comparable position → weight 1.0 by convention and the flag
`no_comparison: true`.

Products: `Research/kind_fuzz_clustering/l3_row_sim.py`,
`l3_interval_c.py`, `l3_interval_c_read.py`, `lanes/iv_rust_c0.sh`,
`lanes/iv_ruby_c0.sh`, `matrices_interval_c/`, `l3_row_graph_v2.py`,
`row_graph_v2.json`, `row_graph_explorer_v2.html` (self-contained, data
embedded, no CDN), `verify_row_graph_v2.js` (which re-implements ruling
A independently in JavaScript and re-derives every emitted weight).

---

## the probe design settled 2026-08-21 (the owner) — RUN 2026-08-21, log 052

**RUN.** First run 2026-08-21 for rust and ruby only (log 052); the
other ten wait. The sets actually used are recorded at the foot of this
section, and `Research/kind_fuzz_clustering/matrices_cart/index.json`
carries every set in full — spellings, canonical strings, enumeration
order and per-holder absences.

Recorded so it is not lost. This supersedes the ladder-plus-shift
design of logs 049 and 051 for all future runs.

**Level 1.** `y = op(x0, x1)` for ALL combinations of `x0, x1` drawn
from one shared set `X`. `|X|^2` probes per row. Exhaustive, so there
is no pairing scheme to choose: equal operands, both orderings and
every cross-magnitude combination are all included by construction.

**Level 2.** `z = op(op(x0, x1), op(x2, x3))` for all four operands
drawn from the SAME `X`. `|X|^4` probes per row. The two intermediates
are never enumerated, deduped, capped or unioned — they exist inside
the expression. Because both languages evaluate identical expressions
on identical inputs, level-2 rows compare position by position across
languages with no alignment step.

**What X must contain (the owner's minimum).** Around every major critical
point, one point on EACH side, where both exist: so `p-1, p, p+1` for
whole numbers and `p-1ulp, p, p+1ulp` for fractional. Critical points
carried today: 0, +/-1, 2^31, 2^53, 2^63, 2^64, type max and min, and
for fractional +/-0.0, 1.0, the subnormal boundary and max finite.
Plus a couple of ordinary values so normal-condition behaviour is
measured, not only edges.

**Level 2 may use a subset X' of X** (fracture-straddling points kept)
when `|X|^4` is too costly; level 1 always runs the full X.

**Cost, measured rates.** rust ~4,000 probes/s (rustc dominated,
parallel); ruby ~7,500 probes/s of evaluation. Rows: rust 116 numeric
holder pairs, ruby 792.

| \|X\| | level 2 per row | ruby total | ruby wall |
|---|---|---|---|
| 8 | 4,096 | 3.2 M | ~7 min |
| 12 | 20,736 | 16.4 M | ~36 min |
| 16 | 65,536 | 51.9 M | ~2 h |
| 20 | 160,000 | 126.7 M | ~4.7 h |

**Superseded by this entry:** the geometric ladder (boundary anchors
plus `2^(k*63/14)` magnitudes) was never an interval sweep and is not
the design of record; the constant-offset shifted pairing is rejected
because `y - x` constant across a row makes every difference-only
operator answer a constant vector. Also rejected, and not re-emitted:
comp1 with equal operands, as degenerate.

### the sets actually used, run of 2026-08-21 (log 052)

`X` and `X'` are per FORM and shared by every holder of that form.
Recorded in code as `Research/kind_fuzz_clustering/l3_cart_values.py`.

| form | `X` (level 1) | `X'` (level 2) |
|---|---|---|
| whole | 17: `-2^63, -2^63+1, -2^53-1, -2^31, -42, -1, 0, 1, 7, 42, 1000, 2^31-1, 2^31, 2^53-1, 2^53+1, 2^63-1, 2^64-1` | 10: `-2^63, -1, 0, 1, 7, 2^31-1, 2^31, 2^53-1, 2^53+1, 2^63-1` |
| fractional | 16: `-max_finite, -1.5, -1.0, -(1.0-1ulp), -0.0, +0.0, +min_subnormal, +min_normal, 1.0-1ulp, 1.0, 1.0+1ulp, 1.5, pi, 2^53, max_finite, 0.1` | 10: `-max_finite, -1.0, -0.0, +0.0, +min_subnormal, 1.0-1ulp, 1.0, 1.0+1ulp, 0.1, max_finite` |
| truth | 6: `true, false, 0, 1, "" (empty text), nil` | 6: all of them |

`X'` keeps BOTH SIDES of every critical point and drops the ordinary
duplicates. Whole: both sides of 0, of `2^31` and of `2^53`, the two
64-bit extremes, and `7` as the ordinary value; dropped `-2^63+1`,
`-2^53-1`, `-42`, `42`, `1000`, `2^64-1`. Fractional: both sides of
`1.0`, both signed zeros with the first value above them, both finite
extremes, one plain negative, and `0.1` as the ordinary
non-representable decimal; dropped `-1.5`, `-(1.0-1ulp)`,
`+min_normal`, `1.5`, `pi`, `2^53`. Truth is already under the
ten-point budget and every member is a critical point of some
language's truthiness rule, so nothing is dropped.

**Absence, not coercion.** A value a holder cannot represent is ABSENT
for that row — the row is shorter and carries a different operand-set
id, so it is only ever compared against rows with the same sets. Nothing
is coerced, wrapped or rounded. Representable means EXACTLY
representable: `f32` does not hold `1.0 + 1ulp(f64)`, so that point is
absent from every `f32` row rather than quietly rounded to `1.0`.

**Ruby operator menu extension.** `and` and `or` are added to the ruby
menu for this design. They are required by its own sanity check:
ruby's `&&`/`||`/`and`/`or` RETURN AN OPERAND rather than a truth
value, so they are projections, and `&&` against `and` is the positive
control that says the harness measures what it claims to.

**Ruby stall budget: 2 seconds** (was 10). A stall is recorded as
`ABORT` and an `ABORT` is excluded from scoring in the numerator and
the denominator both, so the shorter budget loses no measurement —
only wall clock.

---

## the row-graph rules settled 2026-08-21 (log 053)

Ruled by the owner after reading log 052; recorded here as **SETTLED**, not
proposed. Implemented the same day by
`Research/kind_fuzz_clustering/l3_row_graph_v4.py` by ASSEMBLY over
`matrices_cart/` — **no probe run**. Report:
`DevComms/log_053_input_key_alignment_contract_and_group.md`.

`l3_row_graph_v3.py` and its products are left on disk unchanged. This
is a v4, not an edit.

### THE ALIGNMENT RULE — settled

> The comparable set of two rows is the **INTERSECTION of their INPUT
> KEYS**.

- a **level-1 key** is the operand pair `(x0, x1)`;
- a **level-2 key** is the operand quad `(x0, x1, x2, x3)`;
- an operand is identified by its **SPELLING**. Every spelling is
  globally unique across all recorded operand sets and carries exactly
  one canonical string — 37 spellings, 37 distinct maps, checked at
  load and asserted, not assumed;
- outputs are compared **at each shared key**. The position of a key in
  a row's own probe vector comes from the probe-index rule of
  `matrices_cart/index.json` applied verbatim:
  level 1 `p = i0*|Xb| + i1`, level 2
  `p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3`. Level 2 needs no extra
  machinery because that equals `q01*(|Xa|*|Xb|) + q23` with
  `q = i*|Xb| + j` — the level-2 key index is the OUTER PRODUCT of the
  level-1 one with itself. **Operands stay recorded once per set, never
  per row**;
- a shared key where **EITHER side declines** (`REFUSE`, `RAISE:*`,
  `ABORT`) is excluded from the numerator AND the denominator, both
  scorings alike. Ruling B, unchanged;
- **ZERO comparable keys after the exclusion → NO CONNECTOR.** That is a
  genuine absence of evidence, not a zero-weight connector;
- **LEVEL 1 IS NEVER MIXED WITH LEVEL 2 in one connector.** Their key
  spaces are disjoint by construction and the builder refuses the pair
  outright as well. **Every connector records its level.**

**What this replaces.** v3 compared two rows only when their entire
input vectors were byte-identical — same level AND both operand-set ids
equal. Holders represent different subsets of `X`, so rows that ran
dozens of the same input pairs were declared incomparable; v3's 68,725
"no comparable positions" row pairs were largely that artifact. The
intersection rule is a strict superset of the old one: inside the v3
comparable universe the two agree exactly, row pair for row pair.

**One consequence, recorded because it is real.** The spellings `0` and
`1` belong to the whole set AND to ruby's six-point truth set and carry
the same canonical value in both, so a truth-form row and a whole-form
row genuinely share those keys — 4 at level 1, 16 at level 2. The rule
as written says compare them, and the builder does. `n_comparable` on
every connector and `min_overlap` on every group are exactly there so
the thinness is visible rather than averaged away. **No floor on
`n_comparable` is imposed; that is an open ruling.**

### THE CONTRACT RULE (case 1, identity) — settled

> Rows whose **INPUT KEY SET is IDENTICAL** and whose outputs are
> **BYTE-IDENTICAL AT EVERY KEY** are the same function on the same
> domain. Contract them into **ONE node**.

- this is **plain identity** — an equivalence relation, therefore
  transitive, therefore **it needs no clique test and none is used**;
- the contracted node carries its **member row ids**, its **member
  count**, its **languages** and its **operators**. A contracted node
  may carry several `lang.op` (the aliases collapse together) and may
  cross languages;
- byte-identical means at EVERY key, including the keys where both sides
  declined with the same token. A node whose every key declines is a
  true identity set and is contracted, and it is reported separately
  because it agrees with nothing and is compared with nothing.

### THE GROUP RULE (case 2, agreement over a partial overlap) — settled

> Contracted nodes that are mutually exact-1.0 on their **OVERLAPS** but
> whose **input key sets DIFFER** are **NOT contracted**. They are
> **GROUPED**.

- a group is a set in which **EVERY PAIR is mutually exact-1.0 with
  `n_comparable >= 1`** — a **MAXIMAL CLIQUE**, complete-linkage logic;
- it is **NEVER a connected component.** Chaining through pairs that
  were never compared is exactly what this avoids;
- the group is a **CONTAINER, NOT A MERGE.** Members stay distinct
  nodes. Collapsing a group in the explorer is a VIEW and changes no
  measurement;
- the group carries **every pair's overlap size** plus the **MINIMUM
  overlap** as its weakest evidence;
- **a maximal clique is not a partition.** A node may sit in more than
  one group, and that overlap is real rather than an error.

### THE TRANSITIVITY HAZARD IS MEASURED, NOT ASSUMED — settled

> Count the triples `(A,B,C)` with `A~B = 1.0` and `B~C = 1.0` while
> `A~C` is `< 1.0` **or has no comparable key at all**. Report the
> count. **Never merge and never group those.**

The count is the size of the mistake a connected component would have
made. Under log 053's build it is **7,212** — 6,714 because `A~C` is
below 1.0 on keys they do share, 498 because `A` and `C` share no
comparable key.
