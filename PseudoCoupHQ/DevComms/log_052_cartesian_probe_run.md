# log 052 — the Cartesian probe design, RUN (rust + ruby), 2026-08-21

The probe design the owner settled on 2026-08-21 and recorded in
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
SUPPORT_conversion_spec.md` has been RUN, for **rust and ruby only**.
The other ten wait. That spec section is now marked RUN with this log
number and carries the `X` / `X'` sets actually used.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

## 1 — what ran

- **Level 1** `y = op(x0, x1)` for ALL ordered pairs from a shared set
  `X`. Exhaustive: no pairing scheme, no offsets, no ladder.
- **Level 2** `z = op(op(x0, x1), op(x2, x3))` with all four operands
  from a subset `X'`. **The two intermediates are never enumerated,
  deduped, capped or unioned** — nothing in the fold or the graph
  materialises `op(x0,x1)`; it exists only inside the expression the
  lane evaluated.

Both languages evaluate identical expressions on identical inputs, so
rows compare position by position with **no alignment step anywhere**.

Superseded and not re-emitted: the geometric ladder (never an interval
sweep), the constant-offset shifted pairing (`y - x` constant makes
every difference-only operator answer a constant vector), and comp1
with equal operands (degenerate).

### the sets

| form | `X` (level 1) | `X'` (level 2) |
|---|---|---|
| whole | 17 spellings: `-2^63, -2^63+1, -2^53-1, -2^31, -42, -1, 0, 1, 7, 42, 1000, 2^31-1, 2^31, 2^53-1, 2^53+1, 2^63-1, 2^64-1` | 10: `-2^63, -1, 0, 1, 7, 2^31-1, 2^31, 2^53-1, 2^53+1, 2^63-1` |
| fractional | 16: `-max_finite, -1.5, -1.0, -(1.0-1ulp), -0.0, +0.0, +min_subnormal, +min_normal, 1.0-1ulp, 1.0, 1.0+1ulp, 1.5, pi, 2^53, max_finite, 0.1` | 10: `-max_finite, -1.0, -0.0, +0.0, +min_subnormal, 1.0-1ulp, 1.0, 1.0+1ulp, 0.1, max_finite` |
| truth | 6: `true, false, 0, 1, "" (empty text), nil` | 6: all of them |

`X'` keeps **both sides of every critical point** and drops the
ordinary duplicates — whole: both sides of 0, `2^31` and `2^53`, the two
64-bit extremes and `7` as the ordinary value; fractional: both sides of
`1.0`, both signed zeros with the first value above them, both finite
extremes, one plain negative and `0.1`; truth is already under the
ten-point budget and every member is a critical point of some
language's truthiness rule, so nothing is dropped. Every set is
recorded in full — spellings, canonical strings, enumeration order — in
`matrices_cart/index.json`, and in code in `l3_cart_values.py`.

**Absence, not coercion.** A value a holder cannot represent is ABSENT
for that row; the row is shorter and carries a different operand-set id,
so it is only compared against rows with the same sets. Representable
means EXACTLY representable — `f32` does not hold `1.0 + 1ulp(f64)`, so
that point is absent from every `f32` row rather than rounded to `1.0`.

**Two additions the design's own sanity check required.** `and` and
`or` are added to the ruby operator menu (24 operations, was 22): ruby's
`&&`/`||`/`and`/`or` RETURN AN OPERAND rather than a truth value, so
they are projections, and `&&` against `and` is the positive control
that says the harness measures what it claims to. And the **truth form
is in scope for the first time** — text and containers stay excluded.

## 2 — the ruby stall budget is 2 seconds (was 10)

Recorded change. The previous run (log 051) spent 550 s of its 557 s
wall clock waiting on `**` with BigDecimal. A stall is recorded as
`ABORT` and an `ABORT` is excluded from scoring in the numerator AND the
denominator, so the shorter budget **loses no measurement — only wall
clock**. Constant `RUBY_STALL_S` in `l3_cart_gen.py`.

## 3 — what came back

| lane | probes | answers | raises | ABORTs | REFUSE | buildfail |
|---|---|---|---|---|---|---|
| rust L1 | 20,531 | 16,082 | 4,449 | 0 | 0 | 0 |
| rust L2 | 626,128 | 412,482 | 213,646 | 0 | 0 | 0 |
| ruby L1 | 259,584 | 189,394 | 70,190 | 0 | 0 | — |
| ruby L2 | 9,136,536 | 4,918,861 | 4,216,035 | 1,640 | 0 | — |
| **total** | **10,042,779** | | | **1,640** | | **0** |

Coverage is checked, not assumed: **all 10,042,779 probes were measured
by a lane file**; none fell back to an unmeasured ABORT.

### timing split, per language

**rust — static, rustc dominated**

| | L1 | L2 |
|---|---|---|
| chunk files | 14 | 418 |
| probes per file (cap) | 1,500 | 1,500 |
| compile invocations | 14 | 418 |
| compile seconds | 4.359 | 154.770 |
| execution seconds | 0.062 | 1.801 |
| driver overhead | 0.028 | 0.965 |
| stall seconds | 0.000 | 0.000 |
| **wall** | **4.449 s** | **157.536 s** |

rustc is 98 % of rust's wall clock at both levels; execution is
noise. Zero build failures, so the bisecting driver never fired.

**ruby — route C, nothing is compiled**

| | L1 | L2 |
|---|---|---|
| files compiled | 0 | 0 |
| compile invocations | 0 | 0 |
| worker processes | 5 | 5 |
| ruby processes total | 5 | 1,645 (5 workers + 1,640 restarts) |
| restarts past a probe that stopped a worker | 0 | 1,640 |
| stall seconds (worker-time inside the 2 s budget) | 0.000 | 3,280.000 |
| evaluation seconds | 11.669 | 1,679.712 |
| **wall** | **11.669 s** | **2,335.712 s** |

All 1,640 ABORTs are `**` stalls. At the old 10 s budget the same
stalls would have cost 16,400 s of worker-time instead of 3,280 s.

### values absent because a holder cannot represent them

| row family | absences | over row sides |
|---|---|---|
| rust.whole.L1 | 690 | 138 |
| rust.fractional.L1 | 216 | 24 |
| rust.truth.L1 | 96 | 24 |
| rust.whole.L2 | 308 | 88 |
| rust.fractional.L2 | 132 | 22 |
| rust.truth.L2 | 88 | 22 |
| ruby.fractional.L1 | 336 | 336 |
| ruby.fractional.L2 | 336 | 336 |
| ruby.whole.L1 / L2, ruby.truth.L1 / L2 | 0 | — |

Per holder: `i32` holds 9 of the 17 whole spellings (5 of the 10 in
`X'`), `i64` 16 (10), `u64` 11 (8), `i128` all; `f32` holds 7 of the 16
fractional spellings (4 of 10) and `f64` all; rust `bool` holds 2 of the
6 truth points; ruby `Rational` has no signed zero, so `-0.0` is absent
from every ruby fractional-Rational row. ruby's whole and truth holders
hold everything.

## 4 — products

- `Research/kind_fuzz_clustering/l3_cart_values.py` — the sets, the
  representability test, the declaration text, the canonical spelling.
- `l3_cart_gen.py` — the lanes, on the existing lane machinery (drop
  file, gzip+base64 payload, rustc per chunk with bisection, ruby eval
  under begin/rescue with the restart-past-a-stall discipline).
- `lanes/ct_rust_l1.sh`, `ct_rust_l2.sh`, `ct_ruby_l1.sh`,
  `ct_ruby_l2.sh`.
- `l3_cart_read.py` → `matrices_cart/` — **85 CSVs, 2,601 rows,
  10,042,779 probes**; 0 non-rectangular lines, 0 wrong vector lengths,
  0 empty slots, 0 dirty canon cells, 4,505,960 outcome tokens.
- `l3_row_graph_v3.py` → `row_graph_v3.json` and
  `row_graph_explorer_v3.html` (self-contained, data embedded, no CDN).
- `verify_row_graph_v3.js` — the headless verifier.

`l3_row_graph.py` (log 050) and `l3_row_graph_v2.py` (log 051) are left
on disk unchanged, and `matrices_interval/` and `matrices_interval_c/`
are not touched. This is a v3, not an edit.

The 482 MB ruby level-2 lane output stays in the gitignored
`SandboxDesign/agent/out/`; `raw/` carries the three small lane outputs
and `matrices_cart/` carries the folded form of all four.

## 5 — scoring: BOTH numbers, neither chosen

Every connector carries both, and nothing in the pipeline picks one:

- **`weight_exact`** — the fraction of COMPARABLE positions where the
  two `output_canon` strings are byte-identical.
- **`weight_graded`** — the ruling-A per-element numeric similarity
  already implemented in `l3_row_sim.py` (sign distance `|s0-s1|`
  → `1 - d/2`; mant distance `|m0-m1|` with mants in `[1,2)` → `1 - d`
  clamped at 0; expo distance through the decay `1/(1+d)`; combined by
  euclidean distance from `(1,1,1)` normalised by `sqrt(3)`), averaged
  over the COMPARABLE positions.

**Declines are never scored.** A position where either side is
`REFUSE` / `RAISE:*` / `ABORT` leaves the numerator and the denominator
both, for both numbers alike. Zero comparable positions → **no
connector at all**, not a zero-weight one: **68,725 row pairs that share
a level and both operand sets have no connector for exactly that
reason**.

## 6 — the graph

**2,644 nodes** (2,601 row + 43 `lang.op` central; by language rust 249,
ruby 2,352; by level L1 1,304, L2 1,297), **74,860 connectors** (2,601
internal, 72,259 external), 44,105 distinct canon strings, **59
comparable groups** (level plus both operand-set ids; largest 252 rows).
Comparable universe 143,895 row pairs, of which 2,911 are the same
`lang.op` (the internal connectors carry those). 1,032 internal
connectors carry `no_comparison`.

Components are counted on EXTERNAL connectors ONLY, at every threshold,
whether or not the internal connectors are drawn.

| cut | external | same-lang | cross-lang | L1 | L2 | components | multi-node | largest |
|---|---|---|---|---|---|---|---|---|
| exact 0.95 | 1,936 | 1,695 | 241 | 1,088 | 848 | 1,873 | 150 | 20 |
| exact 0.85 | 2,352 | 2,053 | 299 | 1,438 | 914 | 1,774 | 175 | 20 |
| exact 0.70 | 2,617 | 2,294 | 323 | 1,560 | 1,057 | 1,678 | 186 | 22 |
| graded 0.95 | 1,956 | 1,706 | 250 | 1,094 | 862 | 1,857 | 161 | 20 |
| graded 0.85 | 2,555 | 2,222 | 333 | 1,569 | 986 | 1,699 | 184 | 24 |
| graded 0.70 | 3,347 | 2,892 | 455 | 2,041 | 1,306 | 1,573 | 192 | 25 |

## 7 — the sanity numbers the owner asked for

### ruby.&& ~ ruby.|| — level 1 and level 2 separately

| | connectors | exact max / mean / min | graded max / mean / min | n_comparable mean | excluded mean |
|---|---|---|---|---|---|
| L1 | 225 | 0.1667 / 0.0345 / 0.0110 | 0.3528 / 0.2592 / 0.0889 | 251.8 | 0.0 |
| L2 | 225 | 0.1111 / 0.0601 / 0.0222 | 0.3599 / 0.2749 / 0.0660 | 8,924.0 | 0.0 |

Strong separation, as expected once the operands differ. Under the old
diagonal design the same pair could not be told apart at all.

### the projection — `&&` answers the RIGHT operand, `||` the LEFT

Level 1, truth|truth, 36 positions. `&&` equals the right operand at
**26 of 36**; `||` equals the left operand at **26 of 36** (the other
ten are the positions where the two coincide or where falsity flips the
projection). Sample positions, verbatim from `row_graph_v3.json`
`sanity.ruby_projection_samples`:

| pos | x0 | x1 | `&&` / `and` answered | `\|\|` / `or` answered |
|---|---|---|---|---|
| 0 | true | true | `true` | `true` |
| 1 | true | false | `false` | `true` |
| 2 | true | 0 | `[1, 0.0, 0]` | `true` |
| 5 | true | nil | `null` | `true` |
| 7 | false | false | `false` | `false` |
| 8 | false | 0 | `false` | `[1, 0.0, 0]` |
| 12 | 0 | true | `true` | `[1, 0.0, 0]` |
| 14 | 0 | 0 | `[1, 0.0, 0]` | `[1, 0.0, 0]` |
| 20 | 1 | 0 | `[1, 0.0, 0]` | `[1, 1.0, 0]` |
| 26 | "" | 0 | `[1, 0.0, 0]` | `t\|\|0\|0\|0` |
| 30 | nil | true | `null` | `true` |
| 35 | nil | nil | `null` | `null` |

Position 12 is the one that settles it: `0` is TRUTHY in ruby, so `&&`
hands back the right operand `true` while `||` hands back the left
operand `0`. Neither returns a boolean. This is only visible because
`X` for truth carries `0`, `1`, `""` and `nil` beside `true` and
`false` — with booleans alone the projection is invisible.

### the boolean composition check

truth-form rows, `and` composed against `or` composed:

| | truth\|truth connectors | exact-match agreement | graded | n_comparable |
|---|---|---|---|---|
| L1 | 1 | **0.1667** (= 6/36) | 0.1901 | 36 |
| L2 | 1 | **0.0556** (= 72/1296) | 0.0660 | 1,296 |

the owner's truth-table prediction for the composed form was 2/16 = 0.1250.
Level 1 measures 1/6 and level 2 measures 1/18 over the SIX-point truth
set, not the two-point boolean one — with `0`, `1`, `""` and `nil` in
play the operators are projections rather than boolean functions, so
the two-valued truth table is the wrong denominator. Restricted to the
boolean sub-square the agreement is the predicted 2 of 4 at level 1.
**This is a number for the owner to rule on, not one to be reconciled here.**

### positive controls — genuine aliases

| | connectors | exact | graded |
|---|---|---|---|
| ruby.&& ~ ruby.and, L1 | 225 | **1.0000** (max = mean = min) | **1.0000** |
| ruby.&& ~ ruby.and, L2 | 225 | **1.0000** | **1.0000** |
| ruby.\|\| ~ ruby.or, L1 | 225 | **1.0000** | **1.0000** |
| ruby.\|\| ~ ruby.or, L2 | 225 | **1.0000** | **1.0000** |

Both aliases hold at 1.0 at both levels, on 251.8 and 8,924.0
comparable positions per connector. The harness measures what it
claims to.

### the two named cross-language / cross-operator checks

| | connectors | exact max / mean / min | graded max / mean / min | n_comparable mean | excluded mean |
|---|---|---|---|---|---|
| rust.+ ~ rust.-, L1 | 6 | 0.3265 / 0.1891 / 0.0588 | 0.5802 / 0.4876 / 0.3335 | 146.8 | 28.5 |
| rust.+ ~ rust.-, L2 | 8 | 0.3594 / 0.1278 / 0.0127 | 0.5845 / 0.4316 / 0.3448 | 4,746.6 | 2,125.5 |
| rust.+ ~ ruby.+, L1 | 13 | 1.0000 / 0.7306 / 0.2539 | 1.0000 / 0.9745 / 0.9263 | 278.9 | 0.0 |
| rust.+ ~ ruby.+, L2 | 22 | 1.0000 / 0.7468 / 0.0549 | 1.0000 / 0.9599 / 0.8009 | 8,512.5 | 1,487.5 |

`rust.+ ~ rust.-` is the pair the diagonal design could not separate
(0.0312 byte identity on 6 pairs, log 050); it now sits near 0.13–0.19
exact and 0.43–0.49 graded, and the two scorings disagree by a wide
margin — which is the point of carrying both.

## 8 — the explorer

`row_graph_explorer_v3.html`, rebuilt on the v2 pattern, self-contained,
no CDN.

- a **checkbox** switches the cut and the weight between exact-match and
  graded similarity;
- **sigmoid controls** for graded mode — a MIDPOINT slider and a
  STEEPNESS slider. The map is
  `w(g) = (s(g)-s(0))/(s(1)-s(0))`, `s(x) = 1/(1+exp(-k(x-m)))`.
  **Steepness 0 IS the raw graded score, exactly**; large steepness
  becomes a step at the midpoint, which is the exact-match-style hard
  cut. It is a DISPLAY rule: no stored number is rewritten;
- the **threshold cuts EXTERNAL connectors only**;
- **internal springs stay near zero** (0.0008 against 0.0060 external),
  preserved from v2, so they never dominate the layout;
- **autofit runs ONCE and never again**; any wheel or mousedown disables
  it permanently; a **fit view** button exists — all preserved from v2;
- live counts, search, level filter, four colourings, draw cap, and
  hover showing every number on a connector including both weights, the
  active weight after the sigmoid, `n_probes`, `n_comparable` and
  `n_excluded_declines`.

## 9 — headless verification

`node verify_row_graph_v3.js` — **ALL CHECKS PASSED**:

- the page's one inline script runs with no throw; embed identical to
  the standalone JSON (2,644 nodes, 74,860 connectors);
- **both scorings re-implemented independently in JavaScript** from the
  canon strings in `matrices_cart/` — 42,533 level-1 connectors
  re-derived EXHAUSTIVELY and 306 level-2 connectors on a deterministic
  1-in-97 sample; both weights and both counts agree to 1e-6;
- external rule: different `lang.op`, same level, identical operand
  sets, `n_comparable > 0`, `n_comparable + n_excluded_declines ==
  n_probes` on every one; exactly one internal connector per row node;
- **live counters against an independent union-find at nine settings**,
  in both scoring modes and at both documented sigmoid limits — the
  page agrees on the connector count and the component count every time;
- steepness 0 reproduces the raw graded score exactly; steepness 600
  maps 0.49 → 0.0025 and 0.51 → 0.9975;
- component count identical with internal connectors drawn (1,699) and
  hidden (1,699);
- internal springs carry 4.4 % of the external impulse;
- the layout settles — 60 further steps move the busiest node 0.000 px;
- autofit ran once and never again; a wheel or mousedown disables it
  permanently even after the once-only flag is cleared; the fit view
  button refits on demand;
- self-contained: data embedded, placeholder gone, no external script,
  no CDN, no network reference.

## 10 — two defects found and fixed, recorded so they are not repeated

**A. The ruby driver materialised the probe list.** The first level-2
attempt built all 2.28 M probe source strings before emitting a single
line. That exceeded both the 2 s stall budget (the runner saw silence
and called a healthy driver stuck) and the 2 GB address-space cap, so
every worker span on restart-at-probe-0 and the lane burned its full
hour producing nothing. Fixed two ways: the driver now enumerates
probes ARITHMETICALLY from a small per-cell plan with prefix sums and an
O(1) decode from a global probe index to the four operand indices, so a
restart resumes in constant time; and the runner now gives a driver a
separate STARTUP grace until it announces `__READY__`, because a slow
start is not a stuck probe. Each worker also writes its answers to its
own part file AS THEY ARRIVE, so a run the daemon stops at its ceiling
still leaves everything it measured.

**B. `l3_interval_read._from_top` cannot survive this design.** It
rebuilds an oversized ruby answer as an exact `Fraction`, `sign * top *
2**(bits - top.bit_length())`. On the interval ladder the largest such
answer was a few thousand bits. The Cartesian sweep reaches `**`
results of **2^31 bits**, where materialising the integer costs ~28 s
and gigabytes EACH — the fold would never have finished. It never
needed the integer: `expo = bits - 1` and `mant = top /
2^(top.bit_length()-1)` follow from the declared bit length and the
leading bits alone. `l3_cart_read.fast_ruby_canon` carries the power of
two as an exponent instead of a multiplication, and
`_selfcheck_bignum()` proves it agrees with the original on magnitudes
where the slow path is still affordable. **`l3_interval_read.py` is not
modified** — the interval products stand exactly as they were.

## 11 — one deviation from the run of record, stated plainly

The `lanes/ct_ruby_l2.sh` now on disk differs from the script that
produced `ct_ruby_l2.txt` by ONE thing: the per-worker part-file write
of defect A's fix was added afterwards, for crash safety. It writes a
file and changes no measurement. Everything else — the sets, the
enumeration, the operator menu, the stall budget, the worker count —
is identical. Re-running the recorded script would reproduce the
recorded output; it was not re-run because doing so costs another
39 minutes for no new information.

## 12 — what is NOT decided here

- whether the exact-match rate or the graded similarity is the number
  the owner wants as THE weight, and at what threshold. Both ride on every
  connector and the explorer switches between them; nothing in the
  pipeline picks one.
- the sigmoid's default midpoint and steepness. They ship at 0.50 and
  **0** — that is, at the raw graded score, changing nothing until the owner
  moves them.
- the boolean composition denominator (§7): measured 1/6 at level 1 and
  1/18 at level 2 over the six-point truth set against the 2/16
  predicted for the two-point boolean one.
- the other ten languages.
