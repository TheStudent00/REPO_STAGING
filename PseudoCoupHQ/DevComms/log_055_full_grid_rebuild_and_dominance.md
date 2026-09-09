# log 055 — full grids, the compatibility gate, and the dominance lattice

2026-08-22. Open items 1 and 2 of
`~/Programming/PseudoCoupHQ/DevComms/log_054_handoff_fuzz_clustering_state.md`,
built to the owner's rulings of 2026-08-21. No new probes were run: this is a
re-fold of the 10,042,779 measured probes in
`~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/matrices_cart/`,
which is unchanged on disk for audit.

Everything below was re-derived from the raw CSVs by
`verify_row_graph_v5.js` (headless, `node`), which reports ALL CHECKS
PASSED. Where a number appears here it is that verifier's number, not
the builder's own.

---

## 1. the headline — the spurious connections are now impossible, not merely absent

- **Zero external connectors cross a form pair or a level**, out of
  38,939. Measured directly on `row_graph_v5.json`, and independently
  by the verifier over all 18 gate blocks.
  - The v4 offender was `ruby.*` (whole) grouped with `ruby.&` (truth)
    on the 4 keys drawn from {0,1} — the only ground a whole profile
    and a truth profile share. That pair is now unbuildable: the gate
    is `(form_pair, level)`, and a truth profile is never compatible
    with a whole profile whatever cells they coincidentally share.
  - This is structural, not a threshold effect. No cut value can
    reintroduce it.
- **GROUP is retired, as ruled.** With full grids every profile inside
  a gate block carries the SAME key set, so the partial-overlap case
  has no instance left to name. The verifier confirms one grid size
  per `(form_pair, level)` across all 18 blocks, and that no `groups`
  array exists anywhere in the data or the page.
- **CONTRACT is unchanged in meaning and unchanged in outcome**:
  1,041 identity sets over the full grids, re-derived from scratch by
  the verifier and identical to the JSON — and identical to the count
  the v4 rule produced, so inflating the grids merged nothing new and
  split nothing apart.

## 2. what was built

| file (all under `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`) | what it is |
| --- | --- |
| `l3_cart_full.py` | the re-fold: inflates every profile to the full X set of its form and level |
| `matrices_full/` | 85 CSVs + `index.json` + `README.md` — the full-grid data |
| `l3_row_graph_v5.py` | the graph builder: gate, contract, two scorings, dominance |
| `row_graph_v5.json` | 1,041 contracted nodes + 43 operator nodes, 38,939 external connectors |
| `row_graph_explorer_v5.html` | the graph page, single file, data embedded, no CDN |
| `dominance_v5.json` | the directed relation: 3,038 nest connectors, 2,277 after transitive reduction |
| `dominance_explorer_v5.html` | the lattice page, same explorer rules |
| `verify_row_graph_v5.js` | headless re-derivation of every claim above |

### the full grid, mechanically

`matrices_cart/index.json`'s `absence_rule` said a value a holder
cannot represent is simply ABSENT from that holder's set, so the row
was shorter and carried a different `x_set` id. That absence is what
made key sets differ, which is what made GROUP necessary.

The re-fold replaces absence with a stated outcome. Every profile now
carries one cell per key of the full X set of its form and level; a
key whose operand the holder cannot represent holds the token
`UNREPRESENTABLE`. It is known statically, so it cost zero probes.

- 2,601 profiles, **11,119,924 cells** after inflation.
- Of those: 5,536,819 value cells, 4,505,960 declines,
  **1,077,145 `UNREPRESENTABLE` fills**.
- The verifier re-inflated 327 profiles (every 9th matrix) from
  `matrices_cart/` through the probe-index rule and got results
  byte-identical to `matrices_full/`, fills included.

### the two scorings, both riding on every connector

Which one is THE weight is **not decided here** — that ruling is
the owner's, and the explorer toggles between them.

- **`weight_value`** — agreement over VALUE cells only. A cell where
  either side is `UNREPRESENTABLE`, `REFUSE`, `RAISE:*` or `ABORT`
  leaves both numerator and denominator. Zero comparable cells gives
  `null`, never zero (3,496 pairs land there).
- **`weight_all`** — agreement over ALL cells, with the outcome tokens
  treated as answers: byte-identical token counts as agreement, and
  the denominator is the whole grid.

## 3. the overflow fracture reappears, exactly where it was predicted

log_054 recorded the standing complaint: excluding declines made
`rust.+ i32` and `ruby.+ Integer` score 1.000 while differing at all 14
overflow keys — the real difference between the two operators was the
thing that vanished. Recomputed from the CSVs by the verifier:

| pair | `weight_value` | `weight_all` | value cells | overflow cells |
| --- | --- | --- | --- | --- |
| `rust.+ i32 x i32` ~ `ruby.+ Integer x Integer` | 1.0000 | 0.2318 (67/289) | 67 of 67 matched | 14 |

The 14 cells are rust answering `RAISE:panic` where ruby answers a
value — e.g. key `(-2^31, -2^31)` gives `RAISE:panic` against
`[-1, 1.0, 32]`. Scoring (a) hides the fracture; scoring (b) shows it.
Both readings are now available on the same connector, which is what
the ruling asked for.

## 4. dominance — the directed object

A dominates B when at every key where B answers a VALUE, A answers the
identical value. A may answer at more keys. Computed over compatible
pairs only; 40,966 pairs classified.

| reading | count | note |
| --- | --- | --- |
| contradicts | 36,733 | the two disagree at a shared value key |
| nests | 3,038 | of which 2,547 are trivial — the dominated profile has no value cell at all |
| overlaps | 1,085 | of which 910 have disjoint value sets |
| equal_values | 110 | mutual nesting: identical over every value key |

- **491 nests are substantive** (the dominated profile actually
  answers values somewhere). Reading a few:

| dominator | dominated | dominated value cells |
| --- | --- | --- |
| `Float != Float [L1] x3` | `Float != Rational [L1]` | 240 |
| `Float != Float [L1] x3` | `Rational != Rational [L1]` | 225 |
| `Float != Float [L1] x3` | `f32 != f32 [L1]` | 49 |
| `Float != BigDecimal [L1]` | `f32 != f32 [L1]` | 49 |

- The lattice view draws the **transitive reduction**: 2,277 of the
  3,038 nest connectors survive, and the verifier confirms every
  dropped connector has a two-step dominator route, so nothing is
  lost by the reduction.
- The 2,547 trivial nests are recorded but flagged: a profile that
  answers no value anywhere is dominated by everything in its block,
  which is true and uninformative. They are counted separately rather
  than silently dropped.

## 5. what this does NOT settle

the owner's research question is whether a dominant operator exists — one
that contains every other operator's behaviour, or could be
constructed to. The lattice is the instrument for asking; it does not
answer. The 36,733 contradicts dominate the relation numerically, and
whether that is the real shape or an artefact of scoring declines as
answers is exactly the open question below.

---

## decided, recorded for audit

- `UNREPRESENTABLE` spelled as an outcome token in the same column as
  values, alongside `REFUSE` / `RAISE:*` / `ABORT`, per the settled
  canonical form. No new column.
- The gate is keyed on `(form_pair, level)` rather than on the X-set
  string, because with full grids they are the same partition —
  verified: one grid size per block across all 18.
- `matrices_cart/` left untouched; the re-fold writes a new
  `matrices_full/`, so both generations are on disk.
- Trivial nests (dominated profile has no value cell) counted as
  nests but reported separately rather than excluded.
- Transitive reduction applied to the lattice VIEW only; the full
  3,038 nest connectors stay in `dominance_v5.json`.
- Explorer requirements preserved verbatim from v4 and re-checked
  headlessly: autofit once and never again, wheel or mousedown
  disables it permanently, fit-view button present, internal springs
  near zero, threshold cuts external connectors only, components
  counted on external connectors only.

## awaiting the owner

1. **Which scoring is THE weight, and at what cut.** Both ride on
   every connector; neither was chosen. For orientation, external
   connector counts: `value@0.95` 287, `value@0.85` 522,
   `value@0.70` 780; `all@0.95` 202, `all@0.85` 703, `all@0.70` 1536.
2. **Declines as disagreement rather than exclusion** — `weight_all`
   now offers that reading, but whether it REPLACES the exclusion
   rule or sits beside it is unruled.
3. **Whether the clustering now behaves as expected.** The spurious
   cross-form connections are gone by construction; whether what
   remains groups the way the owner expects is his call to make on the
   explorer, and it gates the other ten languages (log_054 item 5:
   do not run them before that).
