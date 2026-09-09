# log 053 — the row graph rebuilt: INPUT-KEY ALIGNMENT, CONTRACT, GROUP, 2026-08-21

Assembly only. **No probe was run for this log.** Everything here is
recomputed from `matrices_cart/` — the 85 CSVs, 2,601 rows and
10,042,779 probes of the Cartesian run of log 052 — under three rulings
the owner made after reading that log.

`l3_row_graph_v3.py`, `row_graph_v3.json`, `row_graph_explorer_v3.html`
and `verify_row_graph_v3.js` are **left on disk unchanged**, and so are
`l3_row_graph.py` (log 050) and `l3_row_graph_v2.py` (log 051). This is
a v4, not an edit: the alignment rule changed, so the old products stay
readable for the audit.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

## 1 — change 1: align on INPUT PAIRS, not on identical vectors

**The defect.** v3 compared two rows only when their ENTIRE input
vectors were byte-identical — same level AND both operand-set ids equal.
Holders represent different subsets of `X` (rust `i32` cannot hold
`2^53+1`, `u64` cannot hold `-1`, ruby `Integer` holds everything), so
rows that ran dozens of the SAME input pairs were declared incomparable.
v3's 68,725 "no comparable positions" row pairs are largely that
artifact.

**The rule now.** The comparable set of two rows is the **INTERSECTION
of their INPUT KEYS**.

- a level-1 key is the operand pair `(x0, x1)`;
- a level-2 key is the operand quad `(x0, x1, x2, x3)`;
- an operand is identified by its **spelling**, which is globally unique
  across every recorded set and carries exactly one canonical string —
  checked at load, 37 spellings, 37 distinct spelling→canon maps;
- outputs are compared **at each shared key**, found through the
  probe-index rule of `matrices_cart/index.json`, which is applied
  verbatim. Level 2 needs no extra machinery, because
  `((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3 == q01*(|Xa|*|Xb|) + q23` — the
  level-2 key index is the OUTER PRODUCT of the level-1 one with itself;
- a shared key where **either side declines** (`REFUSE` / `RAISE:*` /
  `ABORT`) leaves the numerator AND the denominator, both scorings
  alike. Ruling B, unchanged;
- **zero comparable keys after exclusion → NO CONNECTOR.** That is a
  genuine absence of evidence, not a zero-weight connector;
- **level 1 is never mixed with level 2** in one connector. Their key
  spaces are disjoint by construction and the builder refuses the pair
  outright as well. Every connector records its `level`.

### before / after, counted on RAW ROW PAIRS

Counted on raw rows so the numbers sit directly beside log 052's.

| | comparable row pairs | carry a connector | ZERO comparable |
|---|---|---|---|
| **v3** (entire input vector byte-identical) | 143,895 | 75,170 | **68,725** |
| **v4** (INTERSECTION of input keys) | **447,074** | **247,357** | 199,717 |

**172,187 row pairs GAIN a connector (+229.1 %)**, and all 172,187 of
them were **outside the v3 comparable universe altogether** — v3 could
not see them at all. Inside the v3 universe the two rules agree exactly,
row pair for row pair, which is the consistency check on the change: two
rows with the same operand sets have the whole vector as their
intersection, so nothing there can move.

The 199,717 that still have no connector are the honest ones: the pair
really shares keys, and at every shared key at least one side declines.

### the n_comparable distribution

Over the 247,357 raw row pairs that carry a connector:

| | min | p25 | median | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|
| n_comparable | 1 | 32 | 238 | 324 | 8,100 | 10,000 | 1,403.05 |

| shared keys | 1 | 2–4 | 5–16 | 17–64 | 65–256 | 257–1,024 | 1,025–4,096 | 4,097+ |
|---|---|---|---|---|---|---|---|---|
| row pairs | 13 | 13,350 | 12,212 | 66,405 | 59,742 | 53,378 | 7,771 | 34,486 |

Over the 61,219 CONTRACTED-NODE connectors (the graph's own pairs):

| | min | p25 | median | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|
| n_comparable | 1 | 30 | 144 | 272 | 5,217 | 10,000 | 1,069.74 |

| shared keys | 1 | 2–4 | 5–16 | 17–64 | 65–256 | 257–1,024 | 1,025–4,096 | 4,097+ |
|---|---|---|---|---|---|---|---|---|
| node pairs | 11 | 4,385 | 4,201 | 17,326 | 19,353 | 6,995 | 2,258 | 6,690 |

### one consequence of the rule, stated plainly

The spellings `0` and `1` belong to the whole set **and** to ruby's
six-point truth set, and they carry the same canonical value in both
(`[1, 0.0, 0]` and `[1, 1.0, 0]`). So a truth-form row and a whole-form
row really do share those two keys, and the intersection rule really
does compare them — on 4 keys at level 1 and 16 at level 2. **4,279 of
the 58,223 external connectors rest on 4 or fewer comparable keys**, and
145 of the 449 groups have such a pair as their weakest link. This is
REPORTED, not suppressed: the rule asks for the intersection and this is
what the intersection gives. `min_overlap` on every group and
`n_comparable` on every connector are exactly there so the thinness is
visible rather than averaged away. **Whether a floor on `n_comparable`
should exist, and where, is a number for the owner to rule on — nothing here
picks one.**

## 2 — change 2: two kinds of collapse, kept distinct

### CASE 1 — CONTRACT (identity)

Rows whose **input key set is IDENTICAL** and whose outputs are
**byte-identical at every key** are the same function on the same
domain. They are contracted into ONE node. This is plain identity: an
equivalence relation, therefore transitive, therefore **no clique test
is needed and none is used**. The contracted node carries its member row
ids, its member count, its languages and its operators.

**2,601 raw rows → 1,041 contracted nodes.** 400 of them carry more than
one row.

| member rows | 1 | 2 | 3–4 | 5–8 | 9–16 | 17–32 | 33–64 | 65+ |
|---|---|---|---|---|---|---|---|---|
| contracted nodes | 641 | 204 | 94 | 55 | 28 | 13 | 5 | 1 |

**the owner's two expectations, both met.**

- `ruby.&&` and `ruby.and` land in the SAME contracted node **32 times**
  (196 rows; 16 nodes at L1, 16 at L2). `ruby.||` and `ruby.or` likewise
  **32 times** (196 rows; 16 and 16). Under v3 these were 225 separate
  connectors per level, each at 1.0000; they are now one node, which is
  the stronger statement.
- **165 contracted nodes span three or more of ruby's four numeric
  holder spellings** (`Integer`, `Rational`, `BigDecimal`, `Float`).

The four largest contracted nodes that carry at least one value:

| node | rows | level | input keys | keys with a value | operators |
|---|---|---|---|---|---|
| `C0975` | 20 | L2 | 10,000 | 10,000 | `ruby.==`, `ruby.===`, `rust.==` |
| `C0537` | 19 | L1 | 289 | 289 | `ruby.==`, `ruby.===`, `rust.==` |
| `C0511` | 18 | L1 | 289 | 289 | `ruby.&&`, `ruby.and` |
| `C0542` | 18 | L1 | 289 | 289 | `ruby.\|\|`, `ruby.or` |
| `C0951` | 18 | L2 | 10,000 | 10,000 | `ruby.&&`, `ruby.and` |
| `C0978` | 18 | L2 | 10,000 | 10,000 | `ruby.or`, `ruby.\|\|` |

`C0511`'s eighteen members are every `{Integer, Rational, BigDecimal}`
holder pair under `&&` and the same nine under `and` — the alias and the
holder spellings collapsing together, which is what the owner predicted.
`C0975` is the same shape for `==` / `===` and reaches ACROSS THE
LANGUAGES: `rust.== / i64 == i64` and `rust.== / i128 == i128` sit in
one identity node with ruby's nine `==` rows and nine `===` rows.

**The largest contracted nodes overall are all-decline nodes**, and they
are reported separately for that reason. `C0954` is 75 rows — every
`{Rational, BigDecimal}` × `{Integer, Rational, BigDecimal}` pair under
ten ruby operators (`&`, `<`, `<<`, `<=`, `=~`, `>`, `>=`, `>>`, `^`,
`|`) at level 2, all 10,000 keys refusing identically. That is a true
identity set and it is contracted correctly, but **38 of the 1,041
contracted nodes (663 rows) have zero keys carrying a value**, so they
agree with nothing, are compared with nothing, and carry no connector.
Both lists — largest overall and largest with a value — are printed and
stored.

### CASE 2 — GROUP (agreement over a partial overlap)

Contracted nodes that are mutually exact-1.0 on their OVERLAPS but whose
input key sets DIFFER are **not** contracted. They are **GROUPED**.

A group is a set in which **every pair is mutually exact-1.0 with
n_comparable ≥ 1** — a **MAXIMAL CLIQUE**, complete-linkage logic. It is
**never a connected component**: chaining through pairs that were never
compared is exactly what this avoids. The group is a **CONTAINER, NOT A
MERGE** — members stay distinct nodes — and it carries every pair's
overlap size plus the **MINIMUM overlap** as its weakest evidence.

**2,041 mutually exact-1.0 contracted-node pairs; 843 nodes have at
least one such co-node; largest degree 46. 449 maximal cliques of size
≥ 2, found in 1,420 Bron–Kerbosch calls.** 843 contracted nodes sit in a
group and **210 of them sit in more than one** — a maximal clique is not
a partition, and the overlap is real rather than an error.

Group sizes: 21, 13, 11, 10, 10, 9, 9, 9, 9, 8×8, 7×27, 6×25, 5×53,
4×69, 3×70, 2×172.

Minimum overlap across the 449 groups: min 1, p25 3, median 30, p75 144,
p90 324, max 8,100, mean 195.1.

| min overlap | 1 | 2 | 3–4 | 5–16 | 17–64 | 65–256 | 257–1,024 | 1,025+ |
|---|---|---|---|---|---|---|---|---|
| groups | 3 | 107 | 35 | 47 | 123 | 75 | 51 | 8 |

**The largest group, `G000`**, is 21 contracted nodes (25 rows) at level
1, operators `ruby.%`, `ruby.>>`, `rust.>>`, **minimum overlap 2 keys**,
maximum 68 — it is held together at its weakest by the `0`/`1`
truth∩whole overlap described in §1. Members: `C0305 TrueFalse %
TrueFalse`, `C0321 TrueFalse >> TrueFalse`, `C0348 TrueFalse >> Integer
(×3)`, `C0368 u64 >> u64`, `C0372 u64 >> i64`, `C0374 u64 >> i128`,
`C0376 u64 >> i32`, `C0378 i64 >> u64`, `C0393 i64 >> i64`, `C0397 i64
>> i128`, `C0399 i64 >> i32`, `C0499 Integer >> TrueFalse`, `C0504 i128
>> u64`, `C0506 i128 >> i64`, `C0540 Integer >> Integer (×3)`, `C0549
i128 >> i128`, `C0551 i128 >> i32`, `C0553 i32 >> u64`, `C0555 i32 >>
i64`, `C0557 i32 >> i128`, `C0572 i32 >> i32`.

**The groups that rest on real evidence at their weakest pair** are more
interesting, and they are reported separately:

| group | size | level | min overlap | max | operators | members |
|---|---|---|---|---|---|---|
| `G115` | 5 | L2 | **81** | 8,100 | `ruby.!=`, `rust.!=` | `C0575 Float != Float (×3)`, `C0620 Float != Rational`, `C0692 f32 != f32`, `C0703 Rational != Float`, `C0724 Rational != Rational` |
| `G116` | 5 | L2 | **81** | 8,100 | `ruby.==`, `ruby.===`, `rust.==` | `C0607 Float == Float (×5)`, `C0638 Float == Rational (×2)`, `C0700 f32 == f32`, `C0721 Rational == Float (×2)`, `C0734 Rational == Rational (×2)` |
| `G170` | 4 | L2 | **144** | 8,100 | `ruby.*`, `rust.*` | `C0588 Float * Float`, `C0628 Float * Rational`, `C0694 f32 * f32`, `C0711 Rational * Float` |
| `G171` | 4 | L2 | **144** | 8,100 | `ruby.+`, `rust.+` | `C0592 Float + Float`, `C0630 Float + Rational`, `C0695 f32 + f32`, `C0713 Rational + Float` |
| `G172` | 4 | L2 | **144** | 8,100 | `ruby.-`, `rust.-` | `C0596 Float - Float`, `C0632 Float - Rational`, `C0696 f32 - f32`, `C0715 Rational - Float` |
| `G173` | 4 | L2 | **144** | 8,100 | `ruby./`, `rust./` | `C0600 Float / Float`, `C0634 Float / Rational`, `C0697 f32 / f32`, `C0717 Rational / Float` |

`G170`–`G173` are the four arithmetic operators, each grouping rust's
`f32` with ruby's `Float` and `Rational` at level 2 on a 144-key floor
and an 8,100-key ceiling. **This is the finding the alignment fix
bought: v3 could not compare `f32` with anything, because `f32` holds 4
of the 10 level-2 fractional points and nothing else has that set.**

### the TRANSITIVITY HAZARD, measured

**7,212 triples (A,B,C) with A~B = 1.0 and B~C = 1.0 while A~C is NOT
1.0** — **6,714** because A~C is below 1.0 on keys they do share, and
**498** because A and C have **no comparable key at all**.

**None of them is merged and none is grouped.** That is what the clique
test is for, and the number is the size of the mistake a connected
component would have made.

## 3 — the graph

**1,084 nodes** — 1,041 contracted (L1 575, L2 466) + 43 `lang.op`
central. **59,599 connectors** — 1,376 internal, 58,223 external.

- 69,589 contracted-node pairs share at least one input key;
- 58,223 of them become EXTERNAL connectors (the two nodes share no
  `lang.op`);
- 2,996 share a `lang.op` and feed the INTERNAL connectors instead;
- 8,370 have zero comparable keys and get **NO connector**;
- 1,376 internal connectors — one per contracted node per `lang.op` it
  carries, because a contracted node may carry several (`C0511` carries
  `ruby.&&` and `ruby.and`); 250 of them carry `no_comparison`.

Components are counted on **EXTERNAL connectors ONLY**, at every
threshold, in both views and both scorings.

### expanded view (groups drawn as containers, members distinct)

| cut | external | same-lang | cross-lang | L1 | L2 | components | multi-node | largest |
|---|---|---|---|---|---|---|---|---|
| exact 0.95 | 1,016 | 335 | 681 | 646 | 370 | 643 | 28 | 123 |
| exact 0.85 | 1,417 | 579 | 838 | 961 | 456 | 586 | 35 | 146 |
| exact 0.70 | 2,502 | 1,062 | 1,440 | 1,703 | 799 | 480 | 30 | 186 |
| graded 0.95 | 1,124 | 370 | 754 | 712 | 412 | 597 | 31 | 125 |
| graded 0.85 | 2,259 | 921 | 1,338 | 1,589 | 670 | 497 | 33 | 180 |
| graded 0.70 | 5,210 | 2,311 | 2,899 | 3,633 | 1,577 | 371 | 31 | 190 |

### collapsed view (every group collapsed to one node)

| cut | external | components | multi-node | largest |
|---|---|---|---|---|
| exact 0.95 | 1,016 | 365 | 138 | 136 |
| exact 0.85 | 1,417 | 353 | 129 | 158 |
| exact 0.70 | 2,502 | 301 | 111 | 192 |
| graded 0.95 | 1,124 | 347 | 134 | 136 |
| graded 0.85 | 2,259 | 303 | 111 | 188 |
| graded 0.70 | 5,210 | 243 | 86 | 192 |

The connector counts are identical in both views, as they must be —
collapsing a group is a VIEW over distinct nodes and changes no
measurement. Only the component count moves, and it moves because a
collapsed group is one node.

## 4 — the named pairs, under the new alignment

Expanded to ROW pairs so the numbers sit beside log 052's. A row pair
that ends up inside ONE contracted node is reported as CONTRACTED —
identical outputs on an identical key set, a stronger statement than a
1.0 connector.

| | row pairs | of which CONTRACTED | on a connector | v3 saw | exact max/mean/min | graded max/mean/min | n_comparable min/median/max |
|---|---|---|---|---|---|---|---|
| `ruby.&&` ~ `ruby.\|\|`, L1 | 625 | 0 | 625 | 225 | 0.5000 / 0.0715 / 0.0110 | 0.7113 / 0.3135 / 0.0889 | 4 / 225 / 289 |
| `ruby.&&` ~ `ruby.\|\|`, L2 | 625 | 0 | 625 | 225 | 0.5000 / 0.0986 / 0.0222 | 0.7113 / 0.3360 / 0.0660 | 16 / 6,561 / 10,000 |
| `ruby.&&` ~ `ruby.and`, L1 | 625 | **225** | 400 | 225 | 1.0000 / 0.9053 / 0.4000 | 1.0000 / 0.9999 / 0.9995 | 4 / 225 / 289 |
| `ruby.&&` ~ `ruby.and`, L2 | 625 | **225** | 400 | 225 | 1.0000 / 0.8957 / 0.3333 | 1.0000 / 0.9999 / 0.9992 | 16 / 6,561 / 10,000 |
| `ruby.\|\|` ~ `ruby.or`, L1 | 625 | **225** | 400 | 225 | 1.0000 / 0.9027 / 0.4000 | 1.0000 / 0.9999 / 0.9995 | 4 / 225 / 289 |
| `ruby.\|\|` ~ `ruby.or`, L2 | 625 | **225** | 400 | 225 | 1.0000 / 0.8919 / 0.3333 | 1.0000 / 0.9999 / 0.9992 | 16 / 6,561 / 10,000 |
| `rust.+` ~ `ruby.+`, L1 | 82 | 7 | 75 | 13 | 1.0000 / 0.8834 / 0.2208 | 1.0000 / 0.9808 / 0.8924 | 4 / 67 / 289 |
| `rust.+` ~ `ruby.+`, L2 | 82 | 7 | 75 | 22 | 1.0000 / 0.8725 / 0.0549 | 1.0000 / 0.9794 / 0.7931 | 16 / 400 / 10,000 |
| `rust.+` ~ `rust.-`, L1 | 20 | 0 | 20 | 6 | 0.3750 / 0.1742 / 0.0588 | 0.7379 / 0.4855 / 0.3335 | 16 / 67 / 289 |
| `rust.+` ~ `rust.-`, L2 | 20 | 0 | 20 | 8 | 0.3594 / 0.1302 / 0.0115 | 0.5845 / 0.4357 / 0.3087 | 25 / 499 / 10,000 |

Three readings, offered as readings and not as rulings.

1. **The alias control now reads two ways at once and both are honest.**
   The 225 same-holder-pair row pairs at each level are CONTRACTED — the
   alias is exact on the whole domain. The 400 that remain are
   DIFFERENT holder pairs (`Integer && Integer` against `Float and
   Float`, say), compared only on the keys they share, and they are NOT
   1.0: the exact-match rate falls to a mean of 0.9053 and a minimum of
   0.4000. That is not the alias failing; it is `&&` on one holder pair
   against `and` on another, which is a different question and now
   visible as a different number. **Graded stays at a 0.9999 mean and a
   0.9992 minimum throughout**, so the two scorings say different things
   here and neither is chosen.
2. **`rust.+ ~ ruby.+` reaches 1.0000 and gets 7 contractions.** v3 saw
   13 row pairs at L1 and 22 at L2; v4 sees 82 at each, of which 7 are
   full identity.
3. **`rust.+ ~ rust.-` stays separated** — exact 0.13–0.17 mean, graded
   0.44–0.49 mean, with the same wide disagreement between the two
   scorings that log 052 recorded. More evidence, same answer.

## 5 — the explorer

`row_graph_explorer_v4.html`, self-contained, data embedded, **no CDN**,
15.6 MB. Every earlier fix preserved:

- **GROUPS DRAW AS ENCLOSING CONTAINERS** — a rounded convex hull around
  the member nodes, taken over each member's own 16 px pad ring so every
  member is provably inside its own hull, labelled with the group id,
  size and minimum overlap. **Not collapsed to a point.** Clicking a
  hull collapses the group to a single node carrying its size; clicking
  that node expands it again. `collapse ALL groups` and `expand all
  groups` do it wholesale;
- **contracted nodes are labelled with their member count** (`x18`),
  drawn with a radius that grows with it and a light rim, and hovering
  shows the full member row list, the languages, the operators, the
  holder pairs, both operand-set ids, the input-key count, the count of
  keys carrying a value, and every group the node sits in;
- a **checkbox** switches the cut and the weight between exact-match and
  graded similarity;
- **sigmoid midpoint and steepness sliders** for graded mode.
  `w(g) = (s(g)-s(0))/(s(1)-s(0))`, `s(x) = 1/(1+exp(-k(x-m)))`.
  **Steepness 0 IS the raw graded score, exactly**; large steepness
  becomes a step at the midpoint. A DISPLAY rule: no stored number is
  rewritten;
- the **threshold cuts EXTERNAL connectors only**;
- **internal springs stay near zero** (0.0008 against 0.0060 external).
  One addition, stated rather than hidden: a **group cohesion spring
  (0.0040)** holds a group's members near each other so the hull is
  drawable. It is not a connector, carries no weight and is never cut;
- **autofit runs ONCE and never again**; any wheel or mousedown disables
  it permanently; a **fit view** button exists;
- **live counts** — nodes drawn, contracted nodes and the raw rows
  behind them, central nodes, groups and how many are collapsed,
  external connectors and how many are cross-language, internal
  connectors, components and multi-node components — plus search over
  node id, label, operators and member row ids, a level filter, five
  colourings (including by member count), a draw cap, and hover on any
  connector showing both weights, the active weight after the sigmoid,
  the level, **n_comparable**, n_shared_keys, n_excluded_declines,
  n_matched_exact, and whether the two key sets are identical or only
  partially overlap.

## 6 — headless verification

`node verify_row_graph_v4.js` — **ALL CHECKS PASSED**. It re-derives,
independently of the python, from `matrices_cart/`:

- the page's one inline script runs with no throw; the embed is
  identical to the standalone JSON (1,084 nodes, 59,599 connectors, 449
  groups);
- **the CONTRACTION re-derived from scratch is EXACTLY the one in the
  JSON** — 1,041 identity sets, same members every time. Nothing was
  merged that is not identical on an identical key set, and nothing
  identical was left apart; the 2,601 member rows partition the raw rows;
- **the ALIGNMENT re-implemented in JavaScript** — shared spellings,
  the probe-index rule, the intersection, the decline exclusion and both
  scorings: **36,338 level-1 connectors re-derived EXHAUSTIVELY** and
  103 level-2 connectors on a deterministic 1-in-211 sample; the
  shared-key count, the decline exclusion and both weights agree to
  1e-6;
- the complete pair table (69,589 pairs) carries every external
  connector with the same numbers, and 207 of its entries — **24 of them
  with ZERO comparable keys and correctly no connector** — are
  re-derived from the matrices on a 1-in-337 sample;
- **every one of the 449 groups is a TRUE MAXIMAL CLIQUE**: every pair
  inside was actually compared, has n_comparable ≥ 1 and an exact-match
  rate of exactly 1.0; the recorded minimum and maximum overlaps are the
  real ones; and no contracted node outside a group is 1.0 with all of
  its members. A connected component would fail this check;
- **the transitivity hazard recounted here is 7,212 (6,714 + 498)**, the
  builder's number exactly;
- external rule: no shared `lang.op`, same level, level 1 never mixed
  with level 2, n_comparable > 0, n_comparable + n_excluded_declines ==
  n_shared_keys, n_shared_keys never above either side's own key count;
  exactly one internal connector per contracted node per `lang.op`;
- **live counters against an independent union-find at eight settings ×
  TWO VIEW MODES**, in both scoring modes and at both documented sigmoid
  limits — the page agrees on the connector count, the component count,
  the group count and the collapsed-group count every time;
- steepness 0 reproduces the raw graded score exactly; steepness 600
  maps 0.49 → 0.0025 and 0.51 → 0.9975;
- component count identical with internal connectors drawn (497) and
  hidden (497);
- internal springs carry 5.2 % of the external impulse;
- the layout settles — 60 further steps move the busiest node 0.000 px;
- **449 group containers drawn, 259 of them with three or more members
  and a real polygon; every member lies inside its own hull**; a click
  inside `G000`'s hull collapsed its 21 member nodes to ONE node and a
  second click expanded it again;
- autofit ran once and never again; a wheel or mousedown disables it
  permanently even after the once-only flag is cleared; the fit view and
  expand-all buttons work;
- self-contained: data embedded, placeholder gone, no external script,
  no CDN, no network reference.

The python side also asserts, before anything is written, that the
vectorised ruling-A similarity agrees with `l3_row_sim.sample_sim` one
pair at a time on a deterministic 37,680-pair sample forcing every form;
worst absolute difference **3.331e-16**.

## 7 — products

- `Research/kind_fuzz_clustering/l3_row_graph_v4.py` — the builder.
  Assembly only; 10.3 s end to end.
- `row_graph_v4.json` (15.5 MB) — nodes, groups, connectors, the
  complete 69,589-row contracted-node pair table, and every sanity
  number in this log.
- `row_graph_explorer_v4.html` (15.6 MB) — self-contained, no CDN.
- `verify_row_graph_v4.js` — the headless verifier.

`l3_row_sim.py` is **not modified**; the graded scoring is the same
ruling-A module log 051 settled, and the builder only evaluates it on
whole arrays instead of one pair at a time.

## 8 — what is NOT decided here

- whether the exact-match rate or the graded similarity is THE weight,
  and at what threshold. Both ride on every connector; nothing picks
  one. This is unchanged from log 052.
- **whether a floor on `n_comparable` should exist.** 13 raw row pairs
  and 11 contracted-node connectors rest on a SINGLE shared key; 4,279
  external connectors and 145 groups rest on 4 or fewer. Every one of
  them is a true statement about a real overlap, and every one of them
  is thin. The number is recorded on every connector and every group so
  a floor can be applied later without rebuilding — but no floor is
  applied here.
- whether the `0`/`1` overlap between the whole set and ruby's six-point
  truth set should count as a shared input key. It is the same value
  with the same canonical string, so the rule as written says yes and
  the builder says yes. §1 states the consequence.
- the sigmoid's default midpoint and steepness. They ship at 0.50 and
  **0** — the raw graded score, changing nothing until the owner moves them.
- the other ten languages.
