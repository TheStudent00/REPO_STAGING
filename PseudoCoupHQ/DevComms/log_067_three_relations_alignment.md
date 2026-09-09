# log 067 — three relations were wearing one word: the dominance alignment

2026-08-23. Records a design alignment reached with the owner in conversation
today, and applies two rulings that came out of it. **This is settled
content, recorded — not re-derived here.** Read first:
`PseudoCoupHQ/CLAUDE.md`,
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_ontology.md`,
`Research/dominant_intentions/census_integer.md`,
`DevComms/log_064_twelve_language_fold_and_lattice.md`,
`DevComms/log_065_spelling_gaps_and_reading_comparison.md`,
`DevComms/log_066_swift_wrapping_operators.md`,
`DevComms/STANDING_RULINGS_AWAITING_DEE.md`.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

The worked example this alignment unblocks is
`DevComms/log_068_dominant_plus_worked_example.md`.

---

## 1 — the alignment

**Three distinct relations had been conflated under the word
"dominance".** Each has its own license and its own properties, and
carrying one relation's vocabulary into another is what cost the last
several logs their footing.

| relation | the question it answers | what it is | what decides it |
| --- | --- | --- | --- |
| CONTAINMENT | does an existing operator already contain this one? | a directed, transitive order | value agreement at every key where the narrower one answers a value |
| ACCUMULATION | may opA, opB, opC be combined into a dominant opD that may not exist in any language? | a UNION | SHARED INTENTION — never measured overlap |
| FRACTURE | is x0 a mode of x1, or a different behaviour? | a similarity judgement | the graded scoring plus the guarantees rule |

### relation 1 — CONTAINMENT (discovery)

> A dominates B when at every key where B answers a VALUE, A answers
> that identical value.

**It is transitive, and the proof matters because it retires a worry.**

> A dominates B, B dominates C. Take any key where C answers a value
> `v`. B must answer `v`. Since B answers a value there, A must answer
> `v`. So A dominates C.

Nothing is inferred about a never-compared pair — it *follows*.
**Therefore the CHAINING HAZARD that `SUPPORT_ontology.md` rules
against for GROUP does NOT apply to containment.** The 7,212 triples
measured in log_053 are a fact about a SIMILARITY relation; they say
nothing about this one.

### relation 2 — ACCUMULATION (construction)

> May opA, opB, opC be combined into a dominant opD that may not exist
> in any language?

This is a UNION, not containment. the owner's worked examples show that
connectivity is the WRONG criterion **in both directions**:

- **Overlap is NOT SUFFICIENT.** dart `??` and kotlin `?:` share an
  edge in the measured data but are unrelated operations. They matched
  only because neither language declared a nullable holder, so both
  degenerated to "return lhs" — log_065's one confirmed coincidental
  pair. Same shape as `and`/`mul` agreeing on `{0,1}`.
- **Overlap is NOT NECESSARY.** Three operators with entirely disjoint
  behaviour profiles, all spelled `+` in three languages, still justify
  one dominant `+` — maximally fractured, but one operator. Requiring a
  shared edge would refuse to build the operator most needed.

**The license is SHARED INTENTION, not measured overlap.** Two
operators accumulate into one dominant operator when they carry the
same intention — the same minimum-set object. The measurement then says
HOW they fracture, not WHETHER they belong together.

This is the line's existing shape — intention first, behaviour as the
fracture map — and it explains the dart/kotlin pair cleanly: no
intention binds them, so no edge count could license merging them.

### relation 3 — FRACTURE (mode accommodation)

> Is x0 a mode of x1, or a different behaviour?

Neither containment nor equality — a similarity judgement, decided with
the graded scoring plus the guarantees rule. **This is where the
clustering machinery — group, clique, connectedness, the two readings —
legitimately belongs.**

the owner's own instinct was right that a GROUP may hold objects that were
compared and did NOT match: that was a clustering-era decision where
"connected" meant "similar". Under containment "connected" means
"contains", a different relation with different properties.

### the correction, recorded honestly

**The clustering ontology was built for a symmetric similarity
question, and its vocabulary was carried into a directed containment
problem without checking whether it transferred.** Each ontology rule
needs to say WHICH RELATION it governs. That change is made in
`SUPPORT_ontology.md` by this log — added, never rewritten.

---

## 2 — applied: php's third guaranteed add is named `approximating`

**Ruled by the owner, 2026-08-23: "approximating is fine."**

`census_integer.md` carried the php third-add block with `NAME
UNPICKED` marked in place. That marker is replaced with the name and
the approval. The block now reads:

```
  - the intention is KEEP RUNNING WITH AN APPROXIMATE ANSWER -- the
    same contract a float carries, arrived at from the integer side.
  - **NAMED `approximating`** (the owner, ruled 2026-08-23, on Claude's
    suggestion: "approximating is fine"). It names what happens to the
    answer rather than the mechanism that produced it. **The three
    guaranteed adds are now `wrapping`, `growing`, `approximating`.**
```

`DevComms/STANDING_RULINGS_AWAITING_DEE.md` §1.2 is closed and moved
out, per that file's own "how to use this file" rule; the item now
lives in `census_integer.md` with its reasoning attached.

**The three guaranteed adds are `wrapping`, `growing`,
`approximating`.** Nothing else was renamed; `unspecified` (rust's bare
`+`, log_020/census) is untouched and is not a fourth add — it is the
record that no add guarantee was chosen.

---

## 3 — applied: the `swift_wrap` language tag is merged into `swift`

**Ruled by Claude with the owner's assent, mechanical.** log_066 folded
swift's `&+`/`&-`/`&*` under a language tag `swift_wrap`, reasoning by
analogy with `rust_release`. The analogy does not hold: `rust_release`
is a different BUILD of the same source, while `&+` is Swift's own
infix operator and Swift is the language. **A thirteenth language was
invented that does not exist.**

What log_066 wanted the tag to carry is real and is kept — that the
ACCEPT set for those three operators is hand-DERIVED (from the
`FixedWidthInteger` same-type declaration, extending the MEASURED
same-type ACCEPT pattern of `*` in `acceptance_swift_A2.json`) rather
than measured by the census's own swiftc `-typecheck` pass. **It is now
a recorded FIELD, not a language tag.**

### what was done, exactly

**Renamed, not re-folded.** A full-grid cell is a pure function of the
cart cell and the x_set ids; the language tag appears only in the file
NAME and the index. So the twelve files were renamed and the two
indexes transformed, and byte-identity was then verified rather than
assumed.

| # | change | where |
| --- | --- | --- |
| 1 | 6 CSVs renamed `swift_wrap.{ampplus,ampminus,ampstar}.L{1,2}.csv` → `swift.{...}.csv` | `Research/kind_fuzz_clustering/matrices_cart_v2/` |
| 2 | the same 6 renamed | `Research/kind_fuzz_clustering/matrices_full_v2/` |
| 3 | 6 index keys `swift_wrap.&+.L1` → `swift.&+.L1` (and `&-`, `&*`, both levels), `"language": "swift_wrap"` → `"swift"`, `"file"` updated | both `index.json` |
| 4 | new field `"acceptance"` on those 6 entries: `derived -- hand-derived same-type ACCEPT set (FixedWidthInteger), not the census's swiftc -typecheck measurement; log_066 section 1` | both `index.json` |
| 5 | new field `"acceptance": "measured -- acceptance_swift_A2.json"` on swift's other 9 operator entries, so the distinction reads off the file rather than off a log | both `index.json` |
| 6 | 14 `x_sets[*].used_by` entries `swift_wrap.Int.L1` → `swift.Int.L1` etc., **deduplicated** where swift's own lane had already named the same holder | both `index.json` |
| 7 | 8 lane-family diagnostic keys `swift_wrap.L1/L2` → `swift.wrapops.L1/L2` in `lane_timing`, `absent_values_per_row_family`, `absent_row_sides_per_row_family`, `probe_coverage` — these name a LANE, not a language, and are kept distinct from `swift.L1/L2` because they are a different lane | `matrices_cart_v2/index.json` |
| 8 | new top-level key `swift_wrap_tag_retired` stating all of the above in place | both `index.json` |
| 9 | `swift_wrap` retired from the fold code: `SWIFT_WRAPOPS = "swift.wrapops"` (a lane-family key), `OUT_LANG`, `BASE_LANG`, `DERIVED_ACCEPTANCE`, `out_lang()`, `base_lang()`; `build()`, `record_sets()`, the file name, the index key and the index `language` all pass through `out_lang()`; `record_sets()` now refuses to name the same holder twice | `Research/kind_fuzz_clustering/l3_cart_read.py` |

**Not changed, deliberately:** `l3_cart_gen.py` (its `SWIFT_WRAP_*`
section already sets `lang = "swift"` inside the lane and its names are
LANE names, not language tags), the lane scripts
`lanes/ct_swift_wrap_l{1,2}.sh`, and the raw lane products — a lane
keeps the name it ran under.

### verification

**Byte-identity, SHA-256 over every CSV in both directories, before
against after, with the six renames mapped:**

| directory | files before | files after | byte-identical | changed or missing | unexpected new |
| --- | --- | --- | --- | --- | --- |
| `matrices_cart_v2/` | 479 | 479 | **479** | **0** | **0** |
| `matrices_full_v2/` | 479 | 479 | **479** | **0** | **0** |

**Format verification** (`l3_cart_read.verify`), re-run over both
directories after the rename:

| directory | files | rows | probes | non-rectangular | wrong vector len | empty slots | dirty canon |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `matrices_cart_v2/` | 479 | 11,077 | 33,159,198 | 0 | 0 | 0 | 0 |
| `matrices_full_v2/` | 479 | 11,077 | 46,231,765 | 11,556 * | 0 | 0 | 0 |

\* the 11,556 "non-rectangular" lines are the verifier's own
cart-shaped `COLUMNS` (11) being applied to the full grids' 14 columns
— a property of running the cart verifier over the full directory, not
a fault, and identical in kind before the rename. Every count matches
log_066's own post-fold numbers exactly (479 files, 11,077 rows,
33,159,198 probes in cart).

**Residual occurrences of the string `swift_wrap`** after the change,
by file:

| file | occurrences | what they are |
| --- | --- | --- |
| `matrices_cart_v2/index.json` | 2 | the `swift_wrap_tag_retired` key and its explanatory text |
| `matrices_full_v2/index.json` | 2 | same |
| `l3_cart_read.py` | 8 | comments explaining the retirement, `G.swift_wrap_cells_l1/l2` (function names owned by `l3_cart_gen.py`) and the two `ct_swift_wrap_l<N>.txt` lane-product file names |
| `l3_cart_gen.py` | 15 | `SWIFT_WRAP_*` / `swift_wrap_cells_*` names and `ct_swift_wrap_l<N>` lane names — LANE names, kept |
| `lanes/ct_swift_wrap_l{1,2}.sh` | — | the lanes as they ran, untouched |
| `DevComms/log_066_*.md` | — | the historical record, untouched |

**Downstream effect, checked not assumed.**
`l3_operator_dominance_v2_twelve.py` and `log065_readings.py` both
enumerate `matrices_full_v2/` with `os.listdir` and take the language
from `name[:-4].split(".")`. They therefore now see `&+`/`&-`/`&*` as
`swift`'s own operators with no code change. **`operator_dominance_v2.json`
is now STALE with respect to this** — it was built before log_066's fold
and has never seen these six matrices at all (log_066 awaiting item 2,
still open); it was not re-run here.

---

## decided, recorded for audit

- The three relations, their licenses and their properties are recorded
  as the owner's alignment, not re-derived: containment is transitive (proof
  in §1), accumulation is licensed by shared intention and never by
  measured overlap, fracture is the similarity question the clustering
  machinery was actually built for.
- **The chaining hazard does not apply to containment** — recorded with
  the proof, because it is the worry the alignment retires.
- php's third guaranteed add is **`approximating`** (the owner's ruling,
  2026-08-23). `census_integer.md` updated in place; standing rulings
  §1.2 closed and moved out.
- **`swift_wrap` is retired as a language tag.** 12 CSVs renamed, both
  indexes transformed, the fold code changed so a future fold produces
  the same names, acceptance provenance recorded as a FIELD. Byte
  identity of all 479 CSVs in each directory confirmed by SHA-256
  before and after; format verification re-run.
- Renamed rather than re-folded, and that is stated as the method: a
  full-grid cell is a pure function of the cart cell and the x_set ids,
  neither of which the rename touched.
- `matrices_cart/` and `matrices_full/` (superseded generations) were
  not touched. No probe was run. No lane was submitted.

## awaiting the owner

1. **Which relation each REMAINING ontology rule governs**, for the
   rules this log did not tag. §1's addition to `SUPPORT_ontology.md`
   tags contract, group, clique and the two readings; the graded
   weight, the owner's input-overlap criterion and the decline rule are named
   there as still-untagged and are structural, so they are his.
2. **`operator_dominance_v2.json` is stale** — it predates both the
   swift fold and this rename. Re-running
   `l3_operator_dominance_v2_twelve.py` over the now-correct
   `matrices_full_v2/` would fold swift's `&+` into the lattice for the
   first time. Not run here (out of scope, and it overwrites a product
   log_064 cites).
3. **Standing rulings §1.1 (the two readings) is what actually blocks
   the construction** — measured, in
   `log_068_dominant_plus_worked_example.md` §7. It is not a tie: under
   ALL-CELLS the mode partition is a partition; under VALUE it is a
   COVER, with profiles in up to 11 parts at once.
