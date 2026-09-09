# log 050 — the two-tier row graph, 2026-08-21

Assembly only. No probe ran; nothing was re-measured. This log builds a
NEW graph over the interval pilot data already on disk
(`matrices_interval/`, 39 CSVs, 908 rows, rust + ruby).

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

## 1 — what changed, and why the old builder is not it

`l3_agreement_graph_interval.py` (log 049 §5) took an interval row and
**split it into 32 per-sample input pairs**, then scored `lang.op`
against `lang.op` in that pair space. That builder still exists and its
products are untouched, but it is not what the owner asked for next.

the owner's design, settled 2026-08-21, his words:

> "each row is its own node with a central node that connects all rows
>  to its respective node. meaning that `+` is a central node that `+`
>  rows connect to. so two types of connectors, internal and external"

So the ROW is the node and the ROW is the matching unit. It is never
split. A row's 32 samples travel together as one ladder-aligned vector
and are matched **position by position inside a shared ladder**.

`l3_row_graph.py` emits `row_graph.json` and
`row_graph_explorer.html`. Neither reads `matrices/`: this graph is
interval rows only, numeric forms only. Text and containers are
excluded by construction and stay excluded.

## 2 — the two kinds of node

| kind | count | id | attributes |
|---|---|---|---|
| ROW | **908** (rust 116, ruby 792) | `rust.+ / V0_4_4 / i64 + i64 / IV32:w_s64\|w_s64` | language, operator, lhs_holder, rhs_holder, interval_id, probe_id, n_samples, n_values, n_declines, input_key |
| CENTRAL | **39** | `rust.+` | language, operator, n_rows |

947 nodes total.

The row id carries the probe id because `(lang.op, lhs_holder,
rhs_holder, interval_id)` is **not** unique on the ruby side — ruby
spells some holder pairs more than once (e.g. `Rational,Rational`
appears 4 times per operator), and each spelling is its own row and its
own node.

`input_key` is a sha1 digest of `lhs_canon_vector` + `rhs_canon_vector`.
It is not a rename of `interval_id`: `w_s128` and `w_big128` are
different ladder ids that produce **byte-identical vectors**, and that
identity is the only reason rust `i128` rows can reach ruby whole-holder
rows at all.

## 3 — the two kinds of connector

**INTERNAL — 908, exactly one per row node.** Row node to its own
`lang.op` central node. These are STRUCTURE, not similarity: they exist
regardless of any threshold and the threshold slider never touches
them. They carry a weight for display only — the mean pairwise
output-vector agreement between this row and the other rows of the same
operator that share its input vectors. 138 rows have no co-row on their
own inputs; those carry weight 1.0 by convention and the flag
`no_comparison: true`. Mean internal weight 0.8288; 595 of the 908 sit
at exactly 1.0.

**EXTERNAL — 50,386.** Row node to row node, across DIFFERENT operators
only (agreement inside one operator is what the internal connectors
already carry). An external connector exists **only** when both rows
carry identical input vectors — same `lhs_canon_vector` AND same
`rhs_canon_vector`, i.e. the same ladder pair. Different ladders are
not comparable, so there is **no connector at all**, not a low-weight
one. Weight = the fraction of the 32 sample positions at which the two
`output_canon_vector` entries are byte-identical. Every external
connector records `n_samples`, `n_matched`, `weight` and
`cross_language`.

Only `lhs_canon_vector`, `rhs_canon_vector` and `output_canon_vector`
contribute to scoring. Nothing else in the row does.

## 4 — sanity, printed by the builder

```
nodes by kind: 908 row, 39 central, 947 total
edges by kind: 908 internal, 50386 external, 51294 total
comparable universe (row pairs with identical input ladders,
                     any operator):                       52146
  of which SAME operator (carried by internal connectors):  1760
  of which CROSS operator (the external connectors):       50386
distinct input ladder pairs: 25
```

External connectors by threshold:

| threshold | external | same-language | cross-language | external-only components | largest | mixes operators | components with internal on |
|---|---|---|---|---|---|---|---|
| 1.00 | **3,861** | 3,500 | 361 | 469 (58 multi-node) | 39 | **yes** | 13 |
| 0.95 | **4,104** | 3,687 | 417 | 442 (63 multi-node) | 39 | **yes** | 10 |
| 0.85 | **4,156** | 3,724 | 432 | 409 (81 multi-node) | 39 | **yes** | 9 |
| 0.70 | **4,172** | 3,740 | 432 | 397 (83 multi-node) | 39 | **yes** | 9 |

(The external-only component count includes the 39 central nodes, which
carry no external connector and so stand alone in that view.)

The weight distribution is the headline: of the 50,386 external
connectors, **39,381 sit at exactly 0.0** and 3,861 at exactly 1.0;
6,063 fall in `(0, 0.5)` and 1,081 in `[0.5, 1)`. Two rows of different
operators, handed the same 32 inputs, usually agree on nothing at all.
That is the sweep doing its job at the row grain, and it is why the
threshold sweep from 1.00 to 0.70 barely moves the count — there is
almost nothing in between to cut.

The largest component is the same at every threshold: **39 ruby row
nodes on the `w_big128|w_big128` ladder spanning 6 lang.op —
`ruby.&`, `ruby.<<`, `ruby.=~`, `ruby.>>`, `ruby.^`, `ruby.|`**. It
mixes operators, and it is single-language. It is the decline-dominated
family: at 128-bit magnitudes those six operations refuse or raise on
every sample, so their output vectors are byte-identical for the
uninteresting reason. `ruby.=~` (`n_values 0`, `n_declines 1152`) is in
it because it declines everywhere.

With the internal connectors switched on the picture is 9 components at
t=0.85, sizes `436, 301, 44, 44, 37, 37, 34, 7, 7`.

### 4.1 rust.+ vs ruby.+ — do any share identical input ladders?

**Yes: 13 row pairs.** Weight max 0.9062, mean 0.7428, min 0.1875.

| weight | matched | ruby row | rust row | ladder |
|---|---|---|---|---|
| 0.9062 | 29/32 | `Integer + Integer` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `Integer + Rational` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `Integer + BigDecimal` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `Rational + Integer` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `Rational + Rational` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `Rational + BigDecimal` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `BigDecimal + Integer` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `BigDecimal + Rational` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `BigDecimal + BigDecimal` | `i128 + i128` | `w_big128\|w_big128` |
| 0.9062 | 29/32 | `Rational + Rational` | `f64 + f64` | `f_b64\|f_b64` |
| 0.2188 | 7/32 | `Float + Float` | `f64 + f64` | `f_b64\|f_b64` |
| 0.1875 | 6/32 | `Float + Rational` | `f64 + f64` | `f_b64\|f_b64` |
| 0.1875 | 6/32 | `Rational + Float` | `f64 + f64` | `f_b64\|f_b64` |

**The three positions where the 29/32 pairs disagree are exactly the
three overflow points**, and nothing else:

| position | ruby | rust |
|---|---|---|
| 0 | `[-1, 1.0, 128]` | `RAISE:panic` |
| 1 | `[-1, 2.0, 127]` | `RAISE:panic` |
| 5 | `[1, 2.0, 127]` | `RAISE:panic` |

An unbounded `Integer` keeps going where `i128` panics. That is the
whole difference between the two additions on this ladder, isolated to
three sample positions out of thirty-two. The row grain says it plainly
in a way the pooled pair space of log 049 could not.

### 4.2 rust.+ vs rust.- — the sweep separating two operators on the same ladders

**6 row pairs share identical input ladders — every rust holder — and
every one of them scores 0.0312, i.e. 1 matched position out of 32.**

```
0.0312  (1/32)  rust.+ / V0_3_3 / i32  + i32  ~  rust.- / V1_3_3 / i32  - i32
0.0312  (1/32)  rust.+ / V0_4_4 / i64  + i64  ~  rust.- / V1_4_4 / i64  - i64
0.0312  (1/32)  rust.+ / V0_6_6 / i128 + i128 ~  rust.- / V1_6_6 / i128 - i128
0.0312  (1/32)  rust.+ / V0_7_7 / f64  + f64  ~  rust.- / V1_7_7 / f64  - f64
0.0312  (1/32)  rust.+ / V0_8_8 / f32  + f32  ~  rust.- / V1_8_8 / f32  - f32
0.0312  (1/32)  rust.+ / V0_5_5 / u64  + u64  ~  rust.- / V1_5_5 / u64  - u64
```

Against log 049, where `rust.+ ~ rust.^` and `rust.-  ~ rust.<<` read
0.83 and 0.85 on the edge values alone, this is the separation the
pilot was built to produce, now at the grain where it is legible: two
different operators handed the same 32 inputs agree on one position.

### 4.3 the diagonal, stated plainly

The interval sweep pairs the k-th lhs sample with the k-th rhs sample —
32 pairs, not 32 x 32. When a row's two ladders are the same (and most
rows' are), every sample is therefore `v OP v`, the **diagonal**. Two
consequences, both visible above and neither hidden:

- `rust.+ ~ rust.-` reads 1/32 because `v+v` and `v-v` coincide only
  where `v = 0`, which the ladder visits once.
- 36 cross-language lang.op combinations reach weight 1.0, and some
  read strangely until the diagonal is remembered — `ruby.<=> ~ rust.-`
  is 1.0 on 13 row pairs because `v <=> v` is `0` and `v - v` is `0`.
  Likewise `ruby.== ~ rust.<=` (all true), `ruby.!= ~ rust.<`
  (all false).

So a weight-1.0 external connector on a same-ladder row means
"indistinguishable **on the diagonal**", not "indistinguishable". This
is a property of the log-049 sweep, not of the new graph, and the graph
does not paper over it. Whether to add off-diagonal sample pairings is
a question for the owner (§7).

Same-language weight-1.0 traffic is dominated by the decline-heavy ruby
family — `ruby.== ~ ruby.===` (192 row pairs), then `ruby.&`,
`ruby.<<`, `ruby.>>`, `ruby.^`, `ruby.|`, `ruby.=~` against each other
(126–154 row pairs each).

## 5 — the explorer

`row_graph_explorer.html`, self-contained, data embedded, no CDN, no
`<script src`. 11.6 MB, because it carries the entire comparable
universe rather than a pre-filtered slice.

- **threshold slider** cuts EXTERNAL connectors only, and the page says
  so in a rule line under the toolbar; internal connectors are never
  cut by it (the headless verify asserts the internal count is
  unchanged between t=1.00 and t=0.00);
- **internal connectors on/off**, plus **fade internal by weight**;
- internal connectors draw warm and dashed, external cool and solid, so
  the two kinds are distinguishable without reading a tooltip;
- **central nodes** draw large, white-ringed and always labelled
  `lang.op`; **row nodes** draw small and label with their holder pair
  on hover, on search hit, or when zoomed past 1.1x;
- **colour mode switch**: by language, or by operator;
- **live counts**: `908 row nodes | 39 central nodes | N external | M
  internal | C components`;
- **search** over node id, operator and holder pair;
- **hover tooltip**: a node's full attributes (including its internal
  weight and whether it was `no_comparison`), an external connector's
  `n_samples` / `n_matched` / `weight` / cross-language flag, an
  internal connector's weight and co-row count;
- **draw cap, documented on screen**: at most **10,000** external
  connectors are drawn, highest weight first, ties broken by position
  in the file. The rule line states the cap, how many connectors clear
  the threshold and how many are therefore not drawn. At the default
  t=0.85 only 4,156 clear it, so the default picture is complete; the
  cap bites only below t=0.05 or with the cap set to 1,000/2,000/4,000
  by hand.

Physics copied from `graph_explorer_interval_pilot.html` — clamped
linear springs, velocity clamp, gravity to centre, hard boundary,
periodic autofit — with the one change 947 nodes forces: the O(n^2)
repulsion is put on a uniform 170-px grid with a 300-px cutoff. The
layout is seeded with the central nodes on a wide ring and each row
node beside its own central node, so the sub-trees start where they
belong.

## 6 — headless verify

`node verify_row_graph.js` — same shape as `verify_graph_interval.js`:
a canvas-shaped stub, the page's own script run verbatim, then:

```
  [script] the page's one inline script ran with no throw
  [embed] 947 nodes, 51294 connectors, identical to row_graph.json
  [kinds] 908 row nodes + 39 central nodes; 908 internal + 50386
          external connectors; header counts agree
  [refs] every connector endpoint is a node, every weight in [0,1]
  [internal] exactly one internal connector per row node (908), each to
          its OWN lang.op central node; no_comparison == (n_co_rows ==
          0) and always weight 1.0
  [external] all 50386 join row nodes of DIFFERENT operators with
          IDENTICAL input ladders (25 distinct ladder pairs); weight ==
          n_matched/n_samples; cross_language correct; no duplicate,
          none missing, none invented
  [counters] 36 threshold x internal-toggle x draw-cap settings: the
          page's live row/central/external/internal/component counts
          equal an independent union-find, every one
  [internal toggle wired] t=0.85 with internal connectors: "... 4156
          external | 908 internal | 9 components"; without: "... 4156
          external | 0 internal | 409 components"
  [threshold cuts external only] t=1.00 -> 3861 external, t=0.00 ->
          10000 external, internal unchanged at 908 both times
  [draw cap stated] "50386 external connectors clear 0.00, the top 1000
          BY WEIGHT are drawn, 49386 are not."
  [autofit] the periodic fit ran with no throw
  [physics] after 600 steps every one of 947 nodes is finite and inside
          the hard boundary
  [settle] 60 further steps move the busiest node 0.000 px; the picture
          spans 887 px from centre -- settled, not drifting
  [self-contained] data embedded, placeholder gone, no external script,
          no CDN
HEADLESS VERIFY: all checks pass
```

The completeness check is the one worth naming: the verifier regroups
the 908 row nodes by `input_key` itself, enumerates every
cross-operator pair in every group, and requires that set to equal the
external connector set exactly — so the rule "identical input ladders,
different operators, all of them" is proved from the emitted data
rather than trusted from the builder.

The builder's own python-side verify passes the same ground
independently, plus `[input_key] the 25 digests partition the row nodes
exactly as the raw input vectors do`.

## 7 — decided vs awaiting

### decided, recorded for audit (reversible, each one line)

1. Row id is `lang.op / probe_id / lhs op rhs / interval_id`; the probe
   id is in it because ruby spells some holder pairs more than once and
   each spelling is its own row node.
2. Internal connector weight = mean pairwise output agreement with the
   co-rows of the same operator sharing this row's inputs; no co-row →
   1.0 and `no_comparison: true`.
3. Internal connectors are structure: always present, never cut by the
   threshold, toggleable and fadeable in the explorer only.
4. External connectors require byte-identical `lhs_canon_vector` AND
   `rhs_canon_vector`. Different ladders → no connector, not a
   low-weight one.
5. All 50,386 external connectors are emitted, including the 39,381 at
   weight 0.0, so the comparable universe is in the file rather than
   inferred. The explorer, not the builder, does the cutting.
6. Draw cap 10,000 external connectors, highest weight first, ties by
   position; stated on screen whenever it bites.
7. `input_key` (sha1 of the two input vectors) is carried on every row
   node so the identical-ladder rule is checkable outside python.

### awaiting the owner

1. **The diagonal (§4.3).** Same-ladder rows sweep `v OP v` only, so a
   weight-1.0 external connector means "indistinguishable on the
   diagonal". `ruby.<=> ~ rust.-` at 1.0 is the honest but startling
   case. Add off-diagonal pairings (a k x k grid per row, or a shifted
   diagonal), or accept the diagonal as the pilot's grain and say so?
2. **Declines dominate the top of the scale.** The largest component at
   every threshold is six ruby operators that decline on all 32 samples
   at 128-bit magnitudes. Should external weight be computed on values
   only, with `REFUSE` / `RAISE:*` / `ABORT` positions excluded (the
   `value_weight` the log-048 graph carried), and offered as a second
   weight rather than replacing the first?
3. **Cross-language reach is narrow by construction.** Only 4,422 of
   50,386 external connectors are cross-language, and every one of them
   lives on `w_big128|w_big128` (rust `i128` meeting ruby's nominal
   128-bit window) or `f_b64|f_b64`. rust `i32`, `i64`, `u64` and `f32`
   have no ruby counterpart ladder at all. Widen the ruby nominal
   window set to include 32/64-bit ladders so the two languages meet on
   more than two ranges, or leave the pilot as it stands?

## 8 — products

- `Research/kind_fuzz_clustering/l3_row_graph.py` — the builder,
  with the explorer template embedded.
- `Research/kind_fuzz_clustering/row_graph.json` (11.6 MB).
- `Research/kind_fuzz_clustering/row_graph_explorer.html` (11.6 MB,
  self-contained).
- `Research/kind_fuzz_clustering/verify_row_graph.js` — the headless
  verify.
- Spec: `Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
  SUPPORT_conversion_spec.md`, section "the two-tier row graph",
  recorded as SETTLED.

`l3_agreement_graph_interval.py`,
`agreement_graph_interval_pilot.json` and
`graph_explorer_interval_pilot.html` are untouched and still stand as
log 049 left them.
