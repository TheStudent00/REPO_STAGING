# log 070 — the dominant-operator construction over EVERY probed operator

2026-08-23. **PRELIMINARY — a measurement to be reviewed, not a settled
artifact.** Nothing structural is decided here; everything is flagged
and measured. No probe was run, no lane was submitted;
`matrices_full_v2/` is read-only to this log.

Read first: `PseudoCoupHQ/CLAUDE.md`,
`DevComms/log_067_three_relations_alignment.md`,
`DevComms/log_068_dominant_plus_worked_example.md` (the worked example
this generalises), `DevComms/log_069_disagreement_kind_classifier.md`
(the classifier applied throughout),
`Research/dominant_intentions/census_integer.md`,
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_ontology.md`.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

Products, both written for this log:

| product | what it is |
| --- | --- |
| `Research/kind_fuzz_clustering/log070_dominant_operators.py` | the whole pipeline, one pass, 82 s under `nice -n 15` |
| `Research/kind_fuzz_clustering/dominant_operators_v1.json` | 6.1 MB, queryable — every family with its members, windows, output form signature, name, fits and nearest census guarantee; every block's pair counts; the relaxation both ways; the spelling check; the gap map |

Scope: **every probed operator, all twelve language tags plus
`rust_release`, both levels, all form pairs.** 42 distinct operator
spellings, 479 matrices, 11,077 profiles, 46,231,765 cells.

---

## 0 — FIRST: the ruby `Rational`/`BigDecimal` anomaly is REAL ruby

**Verdict: real ruby behaviour, NOT a canon-path artefact. Nothing to
fix, and therefore no re-fold.** This gates trust in every fractional
result below, so it was settled before anything else.

log_068 §6a found `ruby.+ Rational x BigDecimal` and its mirror matching
none of the three guaranteed adds, differing from the exact sum at 94 of
289 cells and from each other at 188 — cause unverified, and the same
SHAPE as the ruby Float canon fault of log_057, which was our own
conversion bug.

### the raw lane payload, beside the canon

Source: `SandboxDesign/agent/out/ct_ruby_l1.txt`, the
cartesian level-1 lane as it ran. Probe `A0_3_4` is
`Rational x BigDecimal`, `A0_4_3` is `BigDecimal x Rational`.

| key | `Rational x BigDecimal` raw payload | `BigDecimal x Rational` raw payload | exact sum |
| --- | --- | --- | --- |
| `(-2^63, -42)` | `BigDecimal:-0.9223372040000000042e19` | `BigDecimal:-0.922337203685477585e19` | `-9223372036854775850` |
| `(-2^63, -1)` | `BigDecimal:-0.9223372040000000001e19` | `BigDecimal:-0.9223372036854775809e19` | `-9223372036854775809` |
| `(-2^63, -2^31)` | `BigDecimal:-0.9223372039002259458e19` | `BigDecimal:-0.9223372039002259456e19` | `-9223372039002259456` |
| `(2^63-1, 42)` | `BigDecimal:0.9223372040000000042e19` | `BigDecimal:0.9223372036854775849e19` | `9223372036854775849` |
| `(2^63-1, 2^63-1)` | `BigDecimal:0.18446744073709551614e20` | `BigDecimal:0.18446744073709551614e20` | `18446744073709551614` |

**The error is in the payload ruby handed back.** It is not introduced
anywhere downstream.

### the canon path, verified rather than assumed

Every answered cell of all nine ruby `+ whole|whole` profiles was
re-canonised **from the raw payload** and compared to the CSV:

| answered cells re-canonised from the raw lane payload | canon mismatches |
| --- | --- |
| **2,601** | **0** |

| key | csv canon, `Rational x BigDecimal` | canon recomputed from the raw payload |
| --- | --- | --- |
| `(-2^63, -42)` | `[-1, 1.0000000003410058947456856559555, 63]` | `[-1, 1.0000000003410058947456856559555, 63]` |
| `(2^63-1, 42)` | `[1, 1.0000000003410058947456856559555, 63]` | `[1, 1.0000000003410058947456856559555, 63]` |
| `(2^53-1, 2^53-1)` | `[1, 1.9999999999999997779553950749687, 53]` | `[1, 1.9999999999999997779553950749687, 53]` |

**Unlike log_057, no float bits are on the path at all** — these are
decimal payloads read as decimal.

### the mechanism, and it predicts every cell

Hypothesis tested: **`BigDecimal` converts the `Rational` operand using
the BIGDECIMAL operand's OWN precision**, and `BigDecimal` carries its
precision in limbs of 9 decimal digits — so an integer of `d` digits
occupies `ceil(d/9)` limbs and therefore `9*ceil(d/9)` significant
digits.

| profile | cells predicted correctly |
| --- | --- |
| `ruby.+ Rational x BigDecimal` | **289 / 289** |
| `ruby.+ BigDecimal x Rational` | **289 / 289** |

Worked, from the table above:

- `(-2^63, -42)`: the right operand `-42` has 2 digits → 1 limb → **9
  significant digits**. `9223372036854775808` to 9 significant digits is
  `9.22337204e18`; add `-42` → `-9223372040000000042`. Matches.
- `(-2^63, -2^31)`: the right operand `-2147483648` has 10 digits → 2
  limbs → **18 significant digits**. `9223372036854775808` to 18
  significant digits is `9.22337203685477581e18`; add `-2147483648` →
  `-9223372039002259458`. Matches, and it is the cell that looks
  arbitrary until the limb rule is applied.

**This is why argument order changes the answer.** In
`BigDecimal + Rational` the `BigDecimal` is the wide operand and its
precision is ample, so the small `Rational` converts exactly; in
`Rational + BigDecimal` the huge `Rational` is converted at the tiny
`BigDecimal`'s precision. Nine of ruby's whole-form add profiles, and
only these two, differ from the exact sum:

| profile | cells differing from the exact sum |
| --- | --- |
| `Integer x Integer`, `Integer x Rational`, `Integer x BigDecimal`, `Rational x Integer`, `Rational x Rational`, `BigDecimal x Integer`, `BigDecimal x BigDecimal` | **0** each |
| `Rational x BigDecimal` | **94** |
| `BigDecimal x Rational` | **94** |
| the two orders against each other | **188** |

log_068 §6a's counts reproduce exactly.

**Recorded, not fixed** — there is nothing to fix. What remains open is
the owner's: whether ruby *guarantees* this precision-budget rule (making it a
mode, and his to name) or merely does it. The MECHANISM is now verified
where log_068 could only say UNVERIFIED.

---

## 1 — GATE

**Same `(form_pair, level)`.** Under the full grids of
`matrices_full_v2/` this ALSO fixes profile cardinality, so "same
cardinality" is implied rather than an extra rule. **Verified, not
assumed:** every one of the 11,077 profiles carries an `n_probes` equal
to its block's `grid_sizes` entry — **0 violations**. The index's own
`comparability` key says the same thing; this log checked it.

**Same INPUT FORM, never holder** (the owner's ruling). `form_pair` already IS
the input-form pair, so the gate needs nothing added: `cpp int32_t` and
`ruby Integer` sit in the same block because both are the form `whole`,
which is what makes cross-language accumulation possible at all.

**Same OUTPUT FORM SIGNATURE — measured both ways, §12.** A profile's
output is a SET of forms. Computed per profile over its answered cells:

```
number      `[sign, mant, expo]` and `nan`
truth       `true`, `false`
nothing     `null`
text        `t|<hex>|...`
container   `c|...`
opaque      `opaque:...`
```

**A LIMIT, stated not hidden: the canon does not carry the OUTPUT
holder**, so `whole` and `fractional` are one `number` at this grain.
The signature is therefore coarser than the census's form vocabulary and
this is a property of the recorded data, not a choice.

The ontology's own five-shapes example is preserved separately as
`output_shape_signature`, which keeps the distinct decline tokens
alongside the forms — `ruby.& TrueFalse x TrueFalse` really does carry
five shapes. Gating uses the FORM signature: a decline is not a form,
and gating on shapes would make the window/value distinction moot.

| gate block | cells | profiles | identity families | WINDOW-only pairs | VALUE-only | MIXED | DECLINE-KIND |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fractional\|fractional/L1 | 256 | 791 | 270 | 2,529 | 5,432 | 28,320 | 34 |
| fractional\|fractional/L2 | 10,000 | 717 | 241 | 2,704 | 3,879 | 22,295 | 42 |
| fractional\|truth/L1 | 96 | 206 | 134 | 1,491 | 787 | 6,626 | 7 |
| fractional\|truth/L2 | 3,600 | 202 | 127 | 1,492 | 647 | 5,840 | 22 |
| fractional\|whole/L1 | 272 | 935 | 305 | 2,685 | 3,018 | 40,641 | 16 |
| fractional\|whole/L2 | 10,000 | 833 | 198 | 1,424 | 1,821 | 16,247 | 11 |
| truth\|fractional/L1 | 96 | 206 | 146 | 1,698 | 766 | 8,120 | 1 |
| truth\|fractional/L2 | 3,600 | 202 | 139 | 1,769 | 688 | 7,124 | 10 |
| truth\|truth/L1 | 36 | 186 | 85 | 624 | 412 | 2,534 | 0 |
| truth\|truth/L2 | 1,296 | 183 | 78 | 678 | 361 | 1,954 | 10 |
| truth\|whole/L1 | 102 | 281 | 182 | 2,251 | 946 | 13,273 | 1 |
| truth\|whole/L2 | 3,600 | 276 | 140 | 1,657 | 771 | 7,295 | 7 |
| whole\|fractional/L1 | 272 | 935 | 314 | 2,737 | 3,137 | 43,251 | 16 |
| whole\|fractional/L2 | 10,000 | 833 | 209 | 2,482 | 1,878 | 17,347 | 29 |
| whole\|truth/L1 | 102 | 281 | 174 | 2,418 | 1,069 | 11,558 | 6 |
| whole\|truth/L2 | 3,600 | 276 | 138 | 2,236 | 837 | 6,335 | 45 |
| whole\|whole/L1 | 289 | 2,001 | 712 | 10,011 | 5,302 | 237,682 | 121 |
| whole\|whole/L2 | 10,000 | 1,733 | 485 | 6,965 | 3,343 | 106,958 | 104 |
| **total** | | **11,077** | **4,077** | **47,851** | **35,094** | **583,400** | **482** |

666,827 pairs classified in all.

---

## 2 — EDGE ON IDENTITY FIRST: the definite families

Identical full-grid vectors CONTRACT — the settled rule. **Equality is
transitive, so components and cliques coincide and there is no chaining
hazard.** 11,077 profiles contract to **4,077 definite families**.

These are what the naming step names, and every count in §7 onward is a
count of these. They stand independently of the two open relaxation
questions.

---

## 3 — THEN RELAX: the disagreement-kind classifier, everywhere

Every non-identical pair inside a gate block was classified by the rule
the owner ruled today (log_069). Across all eighteen blocks:

| kind | pairs | share |
| --- | --- | --- |
| MIXED | 583,400 | 87.5% |
| WINDOW-only | 47,851 | 7.2% |
| VALUE-only | 35,094 | 5.3% |
| DECLINE-KIND only | 482 | 0.07% |

**MIXED dominates by a long way**, which is the load-bearing fact for
the region test: the classifier's cheap verdicts cover under 13% of
pairs, and the rest turn on whether their disagreement has a boundary.

---

## 4 — the one kind the ruled classifier has no bucket for

482 pairs disagree ONLY in WHICH decline they gave — token against a
different token, never value against value, never decline against
answer. The cleanest witness:

| pair | disagreements | value clashes | window | token-vs-token | comparable cells |
| --- | --- | --- | --- | --- | --- |
| `cpp.% int32_t x int32_t` vs `csharp.% int x int` | 10 | 0 | 0 | 10 | 71 |
| `python.& Decimal x bool` vs `python.& Fraction x bool` | 6 | 0 | 0 | 6 | 0 |

The first pair agrees at every one of the 71 keys where both answer and
differs only in how it declined the other 10 — a decline-VOCABULARY
difference, not a behaviour difference. **Flagged, not decided**
(standing rulings §1.5).

---

## 5 — what WINDOW-only admission merges, and what it costs

"WINDOW-only → SAME family" is a PAIRWISE verdict. Closing it into
families needs an operationalisation, and the two available ones
disagree hard. **Both measured, neither chosen.**

**The settled decline rule binds first.** "Zero comparable keys means NO
connector, not a zero-weight one" (`CLAUDE.md`). Without it a profile
that declines at every cell is WINDOW-only-compatible with EVERY profile
in its block, and every gate block collapses to one family — measured,
that is exactly what happens: 18 blocks, 18 families. With the rule
applied, **31,479 of the 47,851 WINDOW-only pairs are refused as edges**
and 16,372 remain.

| block | identity families | WINDOW-only edges | edges refused by the decline rule | components | largest | components that are NOT cliques | maximal cliques |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fractional\|fractional/L1 | 270 | 433 | 2,096 | 110 | 15 | 12 | 155 |
| fractional\|fractional/L2 | 241 | 434 | 2,270 | 72 | 31 | 12 | 133 |
| fractional\|truth/L1 | 134 | 217 | 1,274 | 47 | 29 | 8 | 79 |
| fractional\|truth/L2 | 127 | 112 | 1,380 | 61 | 13 | 4 | 81 |
| fractional\|whole/L1 | 305 | 891 | 1,794 | 79 | 19 | 12 | 108 |
| fractional\|whole/L2 | 198 | 454 | 970 | 64 | 16 | 9 | 94 |
| truth\|fractional/L1 | 146 | 184 | 1,514 | 54 | 13 | 12 | 78 |
| truth\|fractional/L2 | 139 | 155 | 1,614 | 59 | 12 | 5 | 80 |
| truth\|truth/L1 | 85 | 160 | 464 | 13 | 41 | 6 | 61 |
| truth\|truth/L2 | 78 | 116 | 562 | 19 | 34 | 6 | 57 |
| truth\|whole/L1 | 182 | 380 | 1,871 | 36 | 25 | 11 | 78 |
| truth\|whole/L2 | 140 | 182 | 1,475 | 54 | 14 | 10 | 77 |
| whole\|fractional/L1 | 314 | 889 | 1,848 | 87 | 19 | 11 | 116 |
| whole\|fractional/L2 | 209 | 467 | 2,015 | 72 | 16 | 9 | 102 |
| whole\|truth/L1 | 174 | 579 | 1,839 | 24 | 36 | 13 | 101 |
| whole\|truth/L2 | 138 | 130 | 2,106 | 65 | 12 | 11 | 85 |
| whole\|whole/L1 | 712 | 6,476 | 3,535 | **61** | **72** | 22 | **42,324** |
| whole\|whole/L2 | 485 | 4,113 | 2,852 | **42** | **234** | 14 | **28,779** |
| **total** | **4,077** | **16,372** | **31,479** | **1,019** | | **187** | **72,588** |

### the counterexample: WINDOW-only merging is not transitive

**On `whole|whole` L1, taking components merges `add wrapping`,
`add growing` and `add approximating` into ONE group of 96 profiles.**
Two hops suffice:

| step | profile | value cells | edge: window disagreements / comparable cells |
| --- | --- | --- | --- |
| 0 | `php.+ int x int` — approximating | 256 | |
| 1 | `csharp.+ short x short` — reaches no fracture | 49 | 207 / 49 |
| 2 | `cpp.+ int64_t x int64_t` — wrapping 64 signed | 256 | 207 / 49 |

Compared DIRECTLY, the two ends clash at **35 value cells** — the
classifier calls that pair VALUE-only, DIFFERENT modes. The chain runs
through `csharp.+ short x short`, whose declared holder never reaches
its own fracture inside the X set. **This is log_068 §5's finding
arriving as a mechanism**: the profiles that never reach their fracture
are exactly the vector by which transitive closure destroys the mode
partition.

The same happens for `-`, `*`, `/` and `%`:

| block | group size (families) | profiles | census names swallowed into one group | spellings |
| --- | --- | --- | --- | --- |
| whole\|whole/L1 | 29 | 96 | add wrapping, add growing, add approximating | `+`, `&+` |
| whole\|whole/L1 | 29 | 96 | sub wrapping, sub growing, sub approximating | `-`, `&-` |
| whole\|whole/L1 | 36 | 100 | mul wrapping, mul growing, mul approximating | `*`, `&*` |
| whole\|whole/L1 | 55 | 88 | div truncating, div flooring | `/`, `//`, `~/` |
| whole\|whole/L1 | 57 | 96 | mod dividend-sign, mod divisor-sign, mod Euclidean | `%` |
| whole\|whole/L2 | 234 | 514 | div truncating, div flooring, all three mods, mul growing, mul wrapping | `%`, `*`, `&*`, `/`, `//`, `<<`, `>>`, `>>>`, `~/` |

**None of these groups is a clique.** Under maximal cliques instead, the
same block gives 42,324 groups — a COVER, not a partition, exactly the
shape log_068 §3 measured for the VALUE reading.

**Reported, not resolved** (standing rulings §1.6). The IDENTITY
families of §2 are unaffected by this question and are what §7 names.

---

## 6 — the region test, applied to every MIXED pair

Two tests, neither a threshold. `ground` is the set of keys where the
question could be asked at all.

- **named region** — the disagreeing set equals a catalogue region
  intersected with `ground`. Catalogue: one/both/left/right operand
  negative, exactly one negative, left/right/either operand zero, an
  operand at or past 2^31 / 2^32 / 2^53 / 2^63 in magnitude, and *the
  exact `op` result outside signed/unsigned w* for each of `+ - * / %`
  and each w in 8, 16, 32, 64, 128.
- **product region** — the set equals the product of its own
  per-operand-axis projections. General, so it applies to every form
  pair and both levels.

Run on the **value-clash cells** — the fracture itself, which is what
becomes the mode boundary — and separately on the whole disagreement
set:

| verdict on the value-clash set | pairs |
| --- | --- |
| every key where the question could be asked (a total disagreement, no boundary) | 298,494 |
| **UNDESCRIBABLE — flagged for the owner** | 249,034 |
| a product region over operand subsets | 32,559 |
| a NAMED region from the catalogue | **3,313** |

The named ones, which are the useful ones, by name — top of the list:

| named region | pairs |
| --- | --- |
| the exact `-` result outside unsigned 64 | 823 |
| one operand negative | 501 |
| the exact `-` result outside unsigned 32 | 479 |
| the exact `-` result outside unsigned 16 | 179 |
| the exact `*` result outside unsigned 64 | 118 |
| the exact `*` result outside signed 16 | 116 |
| the exact `+` result outside signed 32 | 111 |
| the exact `/` result outside signed 32 | 75 |
| the exact `/` result outside unsigned 64 | 74 |
| the left operand zero / the right operand zero | 69 / 69 |
| the exact `*` result outside signed 32 | 64 |
| the exact `+` result outside signed 64 | 56 |

**Honest reading.** Only 3,313 of 583,400 MIXED pairs have a fracture
that the catalogue can name outright, and 249,034 are UNDESCRIBABLE by
both tests. That is not a failure of the test — most MIXED pairs are
pairs of unrelated operators that happen to sit in one gate block
(`cpp.&&` against `cpp.>=`), and their disagreement is not a fracture at
all. It IS a warning that the region test as ruled cannot be the whole
of the MIXED path at this scale: **at 249,034 flags, "then human eyes"
is not reachable by hand.** Flagged as the load-bearing practical
problem, not solved here.

---

## 7 — NAME, discovery-first

**The naming step takes no spelling as input.** Every `whole|whole`
family was tested against EVERY census guarantee of EVERY arithmetic
intention — add, subtract, multiply, divide, modulo — 52 candidate
prediction vectors per level, each an independent reimplementation
comparing canon STRING against canon STRING (never decoding the
31-digit mantissa back). A family fits whichever it fits.

**Width and signedness are HOLDER properties, not guarantees** (census
F-i1), so `wrapping/32/signed` and `wrapping/64/unsigned` both report as
`wrapping`. 128 is in the width set because `cpp __int128` and
`rust i128` are declared holders in this run.

| census name | families | profiles | languages | spellings that landed here, POST-HOC |
| --- | --- | --- | --- | --- |
| add wrapping | 28 | 114 | 7 | `+` 106, `&+` 8 |
| sub wrapping | 28 | 114 | 7 | `-` 106, `&-` 8 |
| mul wrapping | 36 | 128 | 8 | `*` 120, `&*` 8 |
| mul growing | 2 | 25 | 4 | `*` 25 |
| add approximating | 2 | 2 | 1 | `+` 2 |
| sub approximating | 2 | 2 | 1 | `-` 2 |
| mul approximating | 1 | 1 | 1 | `*` 1 |
| div truncating (F-i3) | 72 | 120 | 9 | `/` 116, `~/` 4 |
| div flooring (F-i3) | 5 | 20 | 2 | `//` 18, `/` 2 |
| mod dividend-sign (F-i4) | 70 | 118 | 9 | `%` 118 |
| mod divisor-sign (F-i4) | 5 | 32 | 2 | `%` 32 |
| mod Euclidean (F-i4) | 3 | 4 | 1 | `%` 4 |
| **named total** | **254** | | | |
| NON-DISCRIMINATING | 82 | 196 | 10 | `+` 72, `-` 72, `*` 29, `%` 12, `/` 11 |
| UNCLASSIFIED | 861 | | | §11 |
| NO-VOCABULARY (outside `whole\|whole`) | 2,880 | | | §11 tier C |

**`-` and `*` DO share `+`'s three — VERIFIED, not assumed.** Each of
`add`, `sub` and `mul` is found in a `wrapping` family, an
`approximating` family, and (for `mul`, where the X set can reach the
boundary) a `growing` family, discovered independently for each
intention.

### the evidence limit, and where `growing` went

`growing` is named on measured agreement with the exact result, never on
a proof of unboundedness (log_068 §5). Adding the 128-bit holders makes
that limit visible: for `+` and `-` the X set tops out at `2^64-1`, so
`wrapping` at 128 bits is UNREACHABLE and the unbounded camp is
consistent with BOTH. For `*` the X set does reach past 2^128, so the
same profiles ARE discriminated.

| consistent with | families | profiles | spellings |
| --- | --- | --- | --- |
| add growing \| add wrapping | 15 | 64 | `+` |
| sub growing \| sub wrapping | 14 | 63 | `-` |
| mul approximating \| mul growing \| mul wrapping | 12 | 16 | `*` |
| mul growing \| mul wrapping | 9 | 13 | `*` |
| mod Euclidean \| mod dividend-sign \| mod divisor-sign | 8 | 10 | `%` |
| div flooring \| div truncating | 8 | 10 | `/` |
| sub approximating \| sub growing \| sub wrapping | 7 | 9 | `-` |
| add approximating \| add growing \| add wrapping | 6 | 8 | `+` |
| mod Euclidean \| mod dividend-sign | 2 | 2 | `%` |
| div truncating \| mod Euclidean \| mod dividend-sign \| mod divisor-sign | 1 | 1 | `/` |

**This is not a regression against log_068** — log_068 named those
profiles `growing` under a width set that stopped at 64, and said so.
It is the same fact, made explicit: on THIS X set, `x + y` cannot tell
an unbounded add from a 128-bit wrapping add.

---

## 8 — POST-HOC SPELLING CHECK

**Only now is spelling looked at.** The agreement and the disagreement
between discovered families and naming convention is the headline
result.

### where naming convention AGREES with behaviour

351 of the 4,077 families hold more than one spelling. **73 of those are
VACUOUS** — the shared vector holds no value cell at all, so the
spellings contracted on declines only (`python.& Decimal x Fraction`
beside `python.// Decimal x Fraction`, both 289 `RAISE:TypeError`).
**278 carry real evidence.** Only the latter are quoted:

| spelling pair sharing a family | families | verdict |
| --- | --- | --- |
| `or` + `\|\|` | 68 | ruby/php's own synonyms — the harness's positive control (log_065) |
| `&&` + `and` | 66 | same |
| `==` + `===` | 55 | type-restricted synonym, log_065 §3 |
| `===` + `is` | 18 | same family of fact |
| `!==` + `is not` | 16 | same |
| `==` + `is` | 16 | same |
| `?:` + `??` | 12 | **the KNOWN coincidence** — log_065's one confirmed vacuous match; neither language declares a nullable holder |
| `!=` + `!==` | 11 | type-restricted synonym |
| **`/` + `//`** | **6** | **the headline — see below** |
| `&+` + `+` | 6 | swift's wrapping add is byte-identical to the wrap camp's plain `+` |
| `&-` + `-` | 6 | same |
| `&*` + `*` | 6 | same |
| `&` + `*` | 2 | the `{0,1}` coincidence `CLAUDE.md` already names |
| `!=` + `^` | 2 | XOR equals `!=` on booleans — genuine, domain-restricted |

**`ruby./ Integer x Integer` is byte-identical to `python.// int x int`
across all 289 cells.** The family, named `div flooring (F-i3)` on
behaviour alone with no spelling input:

Family `whole|whole/L1#585`, named `div flooring (F-i3)`, 272 of 289
value cells:

| member |
| --- |
| `python.// Fraction x Fraction` |
| `python.// Fraction x int` |
| `python.// int x Fraction` |
| `python.// int x int` |
| `ruby./ Integer x Integer` |

The same family reappears at level 2 (`whole|whole/L2#397`, 10
profiles, 5,310 value cells). **This is the census's own F-i3 claim —
"python's integer division is spelled `//` and FLOORS, agreeing with
ruby's rounding, not with the truncating camp" — recovered from
measurement, not assumed.** `dart.~/` lands in `div truncating`
alongside nine languages' `/` by the same route.

Swift's three wrapping operators, likewise discovered, not asserted:

Family `whole|whole/L1#260`, named `add wrapping`, 256 of 289 value
cells, 12 profiles:

| member |
| --- |
| `cpp.+ int64_t x int64_t` |
| `csharp.+ long x long` |
| `go.+ int x int` |
| `go.+ int64 x int64` |
| `java.+ Long x Long` |
| `java.+ Long x long` |
| `java.+ long x Long` |
| `java.+ long x long` |
| `kotlin.+ Long x Long` |
| `rust_release.+ i64 x i64` |
| `swift.&+ Int x Int` |
| `swift.&+ Int64 x Int64` |

### where naming convention DISAGREES with behaviour — the fractures

| spelling | census names its families carry |
| --- | --- |
| `+` | add wrapping, add growing, add approximating |
| `-` | sub wrapping, sub growing, sub approximating |
| `*` | mul wrapping, mul growing, mul approximating |
| `/` | **div truncating (F-i3), div flooring (F-i3)** |
| `%` | **mod dividend-sign, mod divisor-sign, Euclidean (all F-i4)** |

| spelling | carries exactly ONE census name |
| --- | --- |
| `&+` | add wrapping |
| `&-` | sub wrapping |
| `&*` | mul wrapping |
| `//` | div flooring (F-i3) |
| `~/` | div truncating (F-i3) |

**Read together: the five spellings everyone shares are the five that
fracture, and the five that are "unusual spellings" are the five that
mean exactly one thing.** A language that gave the guarantee its own
spelling gave it unambiguously; the shared spellings are the ambiguous
ones.

### the case the thesis is built on

**php's `.` is the only operator in the run whose `whole|whole` output
form signature is `text`.** It is a family of ONE in every single one
of the eighteen gate blocks:

| family | output form signature | member |
| --- | --- | --- |
| `whole\|whole/L1#525` | text | `php.. int x int` |
| `whole\|whole/L2#372` | text | `php.. int x int` |
| `fractional\|fractional/L1#66` | text | `php.. float x float` |
| `truth\|truth/L1#24` | text | `php.. bool x bool` |

No other language's `.` is probed at all (it is member access, not a
binary operator on values). **The output-form signature caught this
structurally, before any human read the spelling** — no gate that
compares form signatures could ever place php's concatenation beside
anything arithmetic.

### spellings split across families

40 of the 42 spellings appear in more than one family inside a single
gate block. That is expected and mostly uninformative — different
holders give different windows. The informative version is the table
above: **which spellings carry more than one census NAME.**

---

## 9 — RESIDUE

**2,404 of the 4,077 families hold exactly one profile.**

| language | singleton families |
| --- | --- |
| cpp | 824 |
| python | 497 |
| ruby | 411 |
| php | 280 |
| csharp | 114 |
| dart | 80 |
| rust | 64 |
| typescript | 39 |
| go | 28 |
| kotlin | 25 |
| rust_release | 20 |
| java | 12 |
| swift | 10 |

**The explanation is holder inventory, and it is measurable rather than
mysterious.** cpp declares 4 whole holders including `__int128` and
`uint64_t`, and mixes them freely, so it produces holder pairs no
co-language declares — its profiles are alone by UNREPRESENTABLE
footprint, not by behaviour. Likewise python's `Decimal`/`Fraction`/
`c_int64` and ruby's `Rational`/`BigDecimal`. The three languages with
the fewest holders (java, swift, kotlin) contribute the fewest
singletons.

Each singleton carries its window in `dominant_operators_v1.json`
(`residue[*].window`, the `src_x_set` of each side, which IS the
range the holder could represent). **The ones that are alone for a
BEHAVIOUR reason rather than a holder reason are exactly the tier-A gap
families of §11**; the rest are marked by their window and are
unverified beyond that.

---

## 10 — the shape of a dominant operator

the owner's §2 format. Structure only, no logic. Presented ONCE, generalised
from log_068 §7 — the object is the same for `+`, for `%` and for a
spelling no language has.

```
DominantOperator
	"""
		one operator, accumulated by
		INTENTION over every measured
		profile that carries it; its modes
		are DISCOVERED, and each mode
		carries the output form signature
		egress must satisfy
	"""
	attributes:
		intention
		input_form_pair
		level
		modes
		unclassified
		non_discriminating
		selector
		refusals
		fracture_map
		provenance
	methods:
		apply
		select_mode
		accumulate
		contains
		refuse


Mode
	"""
		one discovered family with a census
		name.  output_form_signature is part
		of the CONTRACT: egress must produce
		it, by polyfill where the target's
		native operator cannot
	"""
	attributes:
		name
		guarantee
		output_form_signature
		members
		discriminating_keys
		evidence_limit
	methods:
		apply
		agrees_with
		satisfies_signature


Member
	"""
		one profile inside a mode, with the
		RANGE its holder could represent --
		never a mode of its own
	"""
	attributes:
		origin_language
		origin_spelling
		lhs_holder
		rhs_holder
		window
		n_value_cells
		n_declines
		n_unrepresentable
	methods:
		...


ModeSelector
	"""
		what picks a mode: the ledger's origin
		and intent, never the measurement
	"""
	attributes:
		origin_language
		origin_spelling
		declared_holder
		build_mode
		unspecified_flag
		default_mode
	methods:
		mode_for_ingress
		mode_for_egress


Refusal
	attributes:
		kind
		keys
		origin_profile
	methods:
		...


FractureMap
	"""
		the measurement, kept as the map of
		HOW the modes differ -- never as the
		license that put them in one operator
	"""
	attributes:
		disagreement_kinds
		window_only_groups
		value_only_boundaries
		mixed_regions
		undescribable_pairs
	methods:
		...
```

**`Mode.output_form_signature` is the new carrier and it is part of the
mode's contract.** `div truncating (F-i3)` has signature `number`;
php's concatenation family has signature `text`; every comparison
family has signature `truth`. Egress into a target whose native
operator produces a different form must polyfill rather than emit the
native operator — that requirement is now readable off the mode object
instead of being rediscovered.

**`Member.window` is a RANGE, never a mode** — the direct consequence of
the WINDOW-only half of the owner's classifier. `java.+ short x short` and
`java.+ int x int` are two Members of one Mode with different windows,
not two modes.

**`Mode.evidence_limit`** carries §7's finding: `growing` is named on
measured agreement, and on this X set `+` cannot distinguish it from a
128-bit wrapping add.

---

## 11 — THE VOCABULARY GAP MAP

**The measurement-generated work order for extending the census's
guarantee vocabulary.** Tiered by OUTPUT FORM SIGNATURE — a structural
property — never by spelling; spelling is quoted post-hoc.

Every family below is in `dominant_operators_v1.json` under
`vocabulary_gap`, each with its members, windows, value-cell counts and
a `nearest_census_guarantee` block naming the closest census guarantee,
how many value cells it misses by, and up to three witness cells with
answered and predicted canon strings.

### TIER A — answers a NUMBER on `whole|whole`, matches no census guarantee

**507 families. A real arithmetic-vocabulary gap.**

| spelling | families | profiles |
| --- | --- | --- |
| `<<` | 115 | 211 |
| `>>` | 105 | 211 |
| `^` | 39 | 144 |
| `\|` | 39 | 144 |
| `&` | 38 | 143 |
| `/` | 38 | 64 |
| `%` | 22 | 28 |
| `**` | 20 | 39 |
| `>>>` | 18 | 50 |
| `*` | 17 | 27 |
| `??` | 10 | 10 |
| `~/` | 6 | 6 |
| `&^` | 6 | 8 |
| `?:` | 4 | 4 |
| `&&` + `and` | 4 | 63 |
| `//` | 4 | 10 |
| `-` | 4 | 4 |
| `+` | 4 | 4 |
| `<=>` | 3 | 20 |
| `and` | 3 | 7 |
| `or` | 3 | 7 |
| `or` + `\|\|` | 2 | 27 |
| three mixed `?:`/`??`/`or`/`\|\|` families | 3 | 44 |

**The headline work order, and it is not close: `<<`, `>>`, `>>>` and
`&^` — 244 families, 480 profiles, with NO guarantee name at all.**
The census DESCRIBES this fracture at F-i6 (three camps: on the
declared width / on an unbounded value / coerced to 32 bits regardless)
but supplies **no NAMES** the way F-i2 supplies `wrapping`/`growing`/
`approximating` and F-i3/F-i4 supply their camps. Naming F-i6's camps
is the single largest vocabulary extension the measurement asks for.

**Five further arithmetic gaps, each with its object.** These are the
ones inside a domain the census DOES name, and each is a genuine
behaviour with no census word:

**(a) "gives a float" is at least three behaviours.** F-i3 has ONE name
for it. All three of the languages that carry it are UNCLASSIFIED
against that one name, each failing at a different number of cells:

| profile | value cells | mismatches against the single `float` name |
| --- | --- | --- |
| `python./ int x int` | 272 | 51 |
| `php./ int x int` | 240 | 10 |
| `dart./ int x int` | 256 | 6 |

The witnesses, each a different cause:

| profile | key | answered | convert-each-operand-to-double-then-divide |
| --- | --- | --- | --- |
| `python./ int x int` | `(-2^63, -2^53-1)` | `[1, 1.9999999999999997779553950749687, 9]` | `[1, 1.0, 10]` |
| `php./ int x int` | `(-2^63+1, -1)` | `[1, 1.9999999999999999997831595655029, 62]` | `[1, 1.0, 63]` |
| `dart./ int x int` | `(0, -2^63)` | `[-1, 0.0, 0]` | `[1, 0.0, 0]` |

python's is a **correctly rounded quotient of the exact rational**,
never a division of two doubles. php's `(-2^63+1) / -1` answers the
EXACT `2^63-1` — php returned an **int, because the division was
exact** — where a float division answers `2^63`. dart's six failures
are all **negative zero**. Same census word, three different contracts,
and the fourth camp — the one that really does convert then divide —
is a fourth.

**(b) mixed signedness silently reinterprets the signed operand.**
cpp's usual arithmetic conversions, with no census word:

| key | `cpp./ int64_t x uint64_t` | truncating | flooring |
| --- | --- | --- | --- |
| `(-1, 42)` | `[1, 1.5238095238095238082021154468748, 58]` | `[1, 0.0, 0]` | `[-1, 1.0, 0]` |
| `(-42, 42)` | `[1, 1.5238095238095238047326684949212, 58]` | `[-1, 1.0, 0]` | `[-1, 1.0, 0]` |

`-1` became `2^64-1` before the division. **16 families**, `/` and `%`
at both levels, cpp alone — the only language in the run that declares
both signed and unsigned holders and lets them mix.

**(c) the answer carries a SIGNED ZERO.** `python.% Decimal x Decimal`
is `dividend-sign` in every respect except that its zero has a sign —
and the match is exact once that is allowed for:

| profile | mismatches against `mod dividend-sign` | of which are `[-1, 0.0, 0]` against `[1, 0.0, 0]` |
| --- | --- | --- |
| `python.% Decimal x Decimal` (and 2 co-holders) | 25 | **25** |

| key | `python.% Decimal x Decimal` | `mod dividend-sign` prediction |
| --- | --- | --- |
| `(-2^63, -1)` | `[-1, 0.0, 0]` | `[1, 0.0, 0]` |
| `(-2^63, -2^31)` | `[-1, 0.0, 0]` | `[1, 0.0, 0]` |

**Every one of the 25 failures is the sign of zero and nothing else.**
4 families for python's `Decimal` remainder, plus dart's `/` above.
F-i3 and F-i4 have no way to say "and the zero keeps its sign" —
`CLAUDE.md` retired the word negzero and put the sign in the canon
precisely so this stays visible, and here it is, unnamed.

**(d) `**` — exponentiation, 20 families over 4 languages, no census
entry of any kind.** Neither F-i2 nor F-i3 nor F-i4 covers it. The
nearest census guarantee to `php.** int x int` misses at 181 of 240
value cells, which is the measurement saying "there is no vocabulary
here", not "it nearly fits".

**(e) the ruby precision-budget behaviour of §0** — mechanism now
verified, still unnamed, and it is not confined to `+`: it appears in
`%` as well, `ruby.% Rational x BigDecimal` and its mirror, at both
levels (4 families). the owner's to name or reject.

### TIER B — `whole|whole`, answers something OTHER than a number

**354 families.** The arithmetic vocabulary was never applicable to
these; they are listed so the gap map is not read as "861 arithmetic
gaps".

| output form signature | families |
| --- | --- |
| truth | 316 |
| opaque | 24 |
| (declines only) | 8 |
| number \| opaque | 4 |
| **text** | **2** |

The two `text` families are php's `.` at both levels (§8). The 24
`opaque` families are `<=>` returning `opaque:ORD:LT`/`GT`/`EQ` (16) and
kotlin's and rust's `..` returning a range object (8) — outputs that
are neither a number nor a truth nor a text, and that the canon can only
carry opaquely. **There is no census vocabulary for a comparison
GUARANTEE at all** — 316 families of truth-answering operators on whole
numbers, and the census's integer page calls comparison a universal
without naming what it guarantees.

### TIER C — outside `whole|whole`

**2,880 families over 613 operator × form-pair regions.** The census's
integer page states no guarantee vocabulary for any of them.
`census_boolean_float.md`, `census_string.md`, `census_list.md` and
`census_dict.md` are the pages that would have to carry it. Full region
list in the JSON.

---

## 12 — output form signature: HARD GATE or SIGNAL

**the owner left this open, so both were measured and neither was chosen.**

The signature cannot affect the IDENTITY families — identical vectors
have identical signatures by construction. It affects only the
WINDOW-only relaxation, by refusing edges between profiles that answer
different forms.

| pair kind | pairs | of those, crossing an output-form-signature boundary |
| --- | --- | --- |
| WINDOW-only | 47,851 | 27,115 (56.7%) |
| VALUE-only | 35,094 | 18,048 (51.4%) |
| MIXED | 583,400 | 289,849 (49.7%) |

| | WINDOW-only groups across all 18 blocks |
| --- | --- |
| signature as a SIGNAL (recorded, not gated) | **1,019** |
| signature as a HARD GATE | **1,120** |

**It changed the answer in 11 of the 18 blocks, and in every one of them
a `truth` operand is involved.** The blocks where it changed nothing are
`fractional|fractional`, `fractional|whole`, `whole|fractional` (both
levels) and `whole|whole` L1.

| block | signal | hard gate | delta |
| --- | --- | --- | --- |
| truth\|truth/L1 | 13 | 32 | **+19** |
| truth\|truth/L2 | 19 | 41 | **+22** |
| truth\|whole/L1 | 36 | 49 | +13 |
| truth\|fractional/L1 | 54 | 65 | +11 |
| truth\|fractional/L2 | 59 | 67 | +8 |
| truth\|whole/L2 | 54 | 64 | +10 |
| whole\|truth/L1 | 24 | 30 | +6 |
| whole\|truth/L2 | 65 | 70 | +5 |
| fractional\|truth/L1 | 47 | 49 | +2 |
| fractional\|truth/L2 | 61 | 63 | +2 |
| whole\|whole/L2 | 42 | 45 | +3 |
| whole\|whole/L1 | 61 | 61 | **0** |

**The reading.** In a block with a `truth` operand, one profile answers
`truth` where another answers `number` (`csharp.& bool x bool` against
`csharp.& int x int`), and the hard gate keeps them apart where the
signal only notes it. **In `whole|whole` L1 — the block every named
family lives in — the choice makes no difference at all**, because a
WINDOW-only pair there almost never crosses a form boundary. So the
question is real but it is not load-bearing for the naming work; it is
load-bearing for the `truth`-operand blocks, which carry no census
vocabulary yet anyway.

---

## decided, recorded for audit

- **The ruby `Rational`/`BigDecimal` anomaly is REAL ruby behaviour, not
  a canon-path artefact.** The raw lane payload carries the imprecise
  answer; the canon path was verified faithful over 2,601 answered cells
  re-canonised from the payload with 0 mismatches. The mechanism —
  `BigDecimal` converts the `Rational` at the OTHER operand's precision,
  9 decimal digits per limb — predicts 289/289 cells in both argument
  orders. **Not fixed, because there is nothing to fix**; no re-fold is
  implied.
- The gate was verified, not assumed: 0 of 11,077 profiles carry a
  cardinality different from their block's grid size, so "same
  cardinality" is implied by "same `(form_pair, level)`" under full
  grids and is not a separate rule.
- Input gating is by FORM, never holder, per the owner's ruling; the output
  form signature was measured BOTH as a hard gate and as a signal and
  neither was chosen (§12).
- **11,077 profiles contract to 4,077 DEFINITE families** by identity.
  These are what is named, and they do not depend on either open
  relaxation question.
- 666,827 pairs classified by the ruled classifier: 47,851 WINDOW-only,
  35,094 VALUE-only, 583,400 MIXED, 482 DECLINE-KIND-only.
- **Naming took no spelling as input.** 254 families carry exactly one
  census name; 82 are NON-DISCRIMINATING with their consistent-with sets
  recorded; 861 `whole|whole` families and 2,880 outside it are the gap
  map. **No new name was coined anywhere.**
- **`-` and `*` were VERIFIED to share `+`'s three guaranteed adds**,
  each discovered independently rather than assumed by analogy.
- Width and signedness ride under the one name `wrapping`, per census
  F-i1. 128-bit holders were included because cpp and rust declare them;
  the consequence — `+` and `-` can no longer discriminate `growing`
  from a 128-bit `wrapping` on this X set — is recorded as an EVIDENCE
  LIMIT, not hidden (§7).
- The post-hoc spelling check separates the 73 VACUOUS spelling
  co-occurrences (contracted on declines only, zero value cells) from
  the 278 carrying real evidence, and only the latter are quoted.
- The WINDOW-only relaxation is reported as components AND as maximal
  cliques with a measured two-hop counterexample; **neither is chosen**.
- Level 2 was processed on equal terms with level 1 throughout — 5,822
  profiles at L1 and 5,255 at L2 — and the L1 named families reappear at
  L2 (`&+` with `+`, `ruby./` with `python.//`).
- Products: `log070_dominant_operators.py`, `dominant_operators_v1.json`
  (6.1 MB). `log067_dominant_plus.json` and log_068 are left untouched.

## awaiting the owner

1. **Is WINDOW-only merging transitive?** (standing rulings §1.6) By
   component it merges the three named adds into one group of 96
   profiles through `csharp.+ short x short`, a profile that never
   reaches its own fracture; by maximal clique the same block gives
   42,324 groups — a cover, not a partition. Structural, so his.
2. **A fourth disagreement kind, or not** (standing rulings §1.5). 482
   pairs disagree only in WHICH decline they gave. Witness:
   `cpp.% int32_t x int32_t` against `csharp.% int x int`, 10 such
   cells, 71 comparable cells, zero value clashes.
3. **The region test cannot be finished by hand at this scale.**
   249,034 MIXED pairs are UNDESCRIBABLE by both the named catalogue and
   the product test, and the rule says undescribable → human eyes.
   Either the catalogue grows, or the MIXED path needs a prior filter
   that removes the unrelated-operator pairs (most of the 249,034 are
   `cpp.&&` against `cpp.>=`, not a fracture at all).
4. **THE VOCABULARY GAP MAP, in priority order.** (a) **F-i6's three
   shift/bit camps have no NAMES** — 244 families, 480 profiles, the
   largest single gap, and the census already describes the fracture
   without naming its camps. (b) F-i3's single `float` name covers at
   least three contracts (correctly-rounded exact quotient;
   convert-then-divide; "int when the division is exact"), and all three
   languages that carry it are UNCLASSIFIED against it. (c) The SIGN OF
   ZERO — 25 of 25 failures for python's `Decimal` remainder, 6 of 6 for
   dart's `/`. (d) Mixed-signedness reinterpretation, 16 cpp families.
   (e) `**`, no census entry at all, 20 families over 4 languages.
   (f) Comparison operators — 316 `whole|whole` families answering
   `truth` with no guarantee vocabulary anywhere.
5. **Output form signature: hard gate or signal.** Measured both (§12):
   1,019 groups against 1,120, differing in 11 of 18 blocks and **not at
   all in `whole|whole` L1**, where every named family lives.
6. **The ruby precision-budget add**, carried forward from log_068 item
   3 with its mechanism now verified: is it a guarantee (and therefore a
   mode, and therefore the owner's to name), or an implementation detail of
   `BigDecimal`'s limb arithmetic that belongs nowhere near the add
   vocabulary?
