# log 068 — dominant `+` over whole numbers, the first worked example

2026-08-23. **PRELIMINARY — a result to be reviewed, not a settled
artifact.** Nothing structural is decided here; everything is flagged
and measured. Built from `Research/kind_fuzz_clustering/matrices_full_v2/`
by `Research/kind_fuzz_clustering/log067_dominant_plus.py` (written for
this log, product `log067_dominant_plus.json`), following the alignment
recorded in `DevComms/log_067_three_relations_alignment.md`.

Read first: `PseudoCoupHQ/CLAUDE.md`, `log_067`,
`Research/dominant_intentions/census_integer.md`,
`Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/SUPPORT_ontology.md`,
`DevComms/STANDING_RULINGS_AWAITING_DEE.md` §1.

Vocabulary held throughout: super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.

Scope, stated so it is not mistaken for more: **`whole|whole`, level 1
only.** Level 2 exists in the same directory and was not partitioned
here.

---

## 1 — ACCUMULATE by intention

**The set is licensed by SHARED INTENTION, not by measured overlap.**
Every profile below carries the same minimum-set object — *add two
whole numbers* — and that is the whole license. The measurement that
follows says HOW they fracture, never WHETHER they belong together.
Said plainly because it is the step that would otherwise be skipped:
no edge was counted before this set was assembled, and no edge could
have changed its membership.

98 profiles, 12 language tags:

| language tag | spelling | profiles | note |
| --- | --- | --- | --- |
| cpp | `+` | 16 | |
| csharp | `+` | 10 | |
| go | `+` | 4 | |
| java | `+` | 25 | |
| kotlin | `+` | 4 | |
| php | `+` | 1 | |
| python | `+` | 16 | |
| ruby | `+` | 9 | |
| rust | `+` | 4 | debug build — panics on overflow |
| rust_release | `+` | 4 | release build — wraps |
| swift | `&+` | 4 | swift declares no plain `+` row at L1; `&+` is its own wrapping add (log_066, merged into `swift` by log_067) |
| typescript | `+` | 1 | `bigint bigint` only |
| **total** | | **98** | |

**dart contributes nothing.** dart carries no `plus` row at L1 at all
(log_064 §2, standing rulings §2.1 — cause never investigated). The
dominant `+` below is built on eleven languages and one build variant,
not twelve languages.

---

## 2 — PARTITION by behaviour, ALL-CELLS reading

Full-vector equality over the 289-cell grid. This is a **true
partition**: every profile is in exactly one part.

**30 parts, 13 of them cross-language, 16 of them parts of one.**

| part | n | languages | value cells | NAME |
| --- | --- | --- | --- | --- |
| 0 | 18 | cpp, python, ruby, rust, rust_release, typescript | 289/289 | **growing** |
| 1 | 12 | cpp, csharp, go, java, kotlin, rust_release, swift | 256/289 | **wrapping** (64, signed) |
| 2 | 10 | cpp, csharp, go, java, kotlin, rust_release, swift | 81/289 | **wrapping** (32, signed) |
| 3 | 7 | cpp, csharp, java, kotlin | 144/289 | **wrapping** (64, signed) — narrow-left widening |
| 4 | 7 | cpp, csharp, java, kotlin | 144/289 | **wrapping** (64, signed) — narrow-right widening |
| 5 | 4 | cpp, python | 272/289 | **growing** |
| 6 | 4 | cpp, python | 272/289 | **growing** |
| 7 | 4 | csharp, go, rust_release, swift | 121/289 | **wrapping** (64, unsigned) |
| 8 | 3 | csharp, java | 63/289 | **wrapping** (32, signed) |
| 9 | 3 | csharp, java | 112/289 | **wrapping** (64, signed) |
| 10 | 3 | csharp, java | 63/289 | **wrapping** (32, signed) |
| 11 | 3 | csharp, java | 112/289 | **wrapping** (64, signed) |
| 12 | 2 | csharp, java | 49/289 | **NON-DISCRIMINATING** — consistent with all three adds at once (§5) |
| 13 | 2 | python | 0/289 | **NON-DISCRIMINATING, vacuously** — 289 declines, no value cell at all |
| 14–29 | 1 each | — | — | the residue, §6 |

**Tally over all 30 parts:** 23 name exactly one add; **5 are
NON-DISCRIMINATING** (consistent with several — parts 12 and 13 above,
plus the three `rust` debug singletons of §6); **2 are UNCLASSIFIED**,
matching none — `ruby.+ Rational x BigDecimal` and `ruby.+ BigDecimal x
Rational` (§6a).

Naming rule used, stated so it can be overturned: a part is named
against the census's three guaranteed adds — `wrapping`, `growing`,
`approximating` — by checking every value cell against a
hand-reimplemented prediction (exact sum; two's-complement wrap at 8,
16, 32, 64 bits signed and unsigned; php's rule of *exact while it fits
the signed 64-bit range, the nearest binary64 once it does not*). **The
comparison is canon STRING against canon STRING** — the canon mantissa
is a decimal rounded at 31 digits, so decoding it back and comparing
numbers would be wrong, and the X-set operands are parsed from their
SPELLINGS (`-2^63+1`, `2^53-1`) rather than read back out of canon for
the same reason. A part that matches none of the three is UNCLASSIFIED,
never forced.

### the members, part by part, for the parts that carry a name

**part 0 — `growing`** (289/289 value cells, the exact-arithmetic camp):

| member |
| --- |
| `cpp.+ __int128 x __int128` |
| `python.+ Decimal x Decimal` |
| `python.+ Decimal x int` |
| `python.+ Fraction x Fraction` |
| `python.+ Fraction x int` |
| `python.+ int x Decimal` |
| `python.+ int x Fraction` |
| `python.+ int x int` |
| `ruby.+ BigDecimal x BigDecimal` |
| `ruby.+ BigDecimal x Integer` |
| `ruby.+ Integer x BigDecimal` |
| `ruby.+ Integer x Integer` |
| `ruby.+ Integer x Rational` |
| `ruby.+ Rational x Integer` |
| `ruby.+ Rational x Rational` |
| `rust.+ i128 x i128` |
| `rust_release.+ i128 x i128` |
| `typescript.+ bigint x bigint` |

**part 1 — `wrapping` (64, signed)** (256/289):

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

**part 2 — `wrapping` (32, signed)** (81/289):

| member |
| --- |
| `cpp.+ int32_t x int32_t` |
| `csharp.+ int x int` |
| `go.+ int32 x int32` |
| `java.+ Integer x Integer` |
| `java.+ Integer x int` |
| `java.+ int x Integer` |
| `java.+ int x int` |
| `kotlin.+ Int x Int` |
| `rust_release.+ i32 x i32` |
| `swift.&+ Int32 x Int32` |

**part 7 — `wrapping` (64, unsigned)** (121/289):

| member |
| --- |
| `csharp.+ ulong x ulong` |
| `go.+ uint64 x uint64` |
| `rust_release.+ u64 x u64` |
| `swift.&+ UInt64 x UInt64` |

**parts 3 and 4 — `wrapping` (64, signed), split by argument order
only.** Same guarantee, same width, two parts because the declared
holder pair differs and the narrower side is promoted:

| part 3 (`narrow x wide`) | part 4 (`wide x narrow`) |
| --- | --- |
| `cpp.+ int32_t x int64_t` | `cpp.+ int64_t x int32_t` |
| `csharp.+ int x long` | `csharp.+ long x int` |
| `java.+ Integer x Long` | `java.+ Long x Integer` |
| `java.+ Integer x long` | `java.+ Long x int` |
| `java.+ int x Long` | `java.+ long x Integer` |
| `java.+ int x long` | `java.+ long x int` |
| `kotlin.+ Int x Long` | `kotlin.+ Long x Int` |

**parts 5 and 6 — `growing`**, python's `c_int64` mixed with an
unbounded holder, beside `cpp __int128` mixed with `int64_t`; 272/289
value cells, the 17 `UNREPRESENTABLE` being the `2^64-1` operand.

**parts 8–11** are the csharp/java `short`-involving widenings — same
two guarantees (32-bit and 64-bit signed wrap), split by which side the
`short` sits on.

### the single key that separates the three adds

`(2^63-1, 42)`, position **264** of 289 in the whole/L1 grid. Every
answer that appears there, with its canon string:

| cell | profiles | reading |
| --- | --- | --- |
| `[1, 1.0000000000000000044452289071906, 63]` | 40 | the exact sum `9223372036854775849` — `growing`, and every holder wide enough not to overflow |
| `UNREPRESENTABLE` | 31 | a 32-bit or 16-bit holder cannot hold the operand; nothing was asked |
| `[-1, 1.9999999999999999911095421856189, 62]` | 22 | `-9223372036854775767`, bit pattern `0x8000000000000029` — `wrapping` at 64 signed |
| `[1, 1.0, 63]` | 1 | exactly `2^63` — **`approximating`**, `php.+ int x int` |
| `RAISE:TypeError` | 2 | `python.+ Decimal x Fraction`, `python.+ Fraction x Decimal` |
| `[1, 1.0000000003410058947456856559555, 63]` | 1 | **UNCLASSIFIED** — `ruby.+ Rational x BigDecimal`, §6 |
| `RAISE:panic` | 1 | `rust.+ i64 x i64` (debug) — the `unspecified` case |

The 22 wrapping profiles at that key, in full:

| member |
| --- |
| `cpp.+ int64_t x int32_t` |
| `cpp.+ int64_t x int64_t` |
| `csharp.+ long x int` |
| `csharp.+ long x long` |
| `csharp.+ long x short` |
| `go.+ int x int` |
| `go.+ int64 x int64` |
| `java.+ Long x Integer` |
| `java.+ Long x Long` |
| `java.+ Long x int` |
| `java.+ Long x long` |
| `java.+ Long x short` |
| `java.+ long x Integer` |
| `java.+ long x Long` |
| `java.+ long x int` |
| `java.+ long x long` |
| `java.+ long x short` |
| `kotlin.+ Long x Int` |
| `kotlin.+ Long x Long` |
| `rust_release.+ i64 x i64` |
| `swift.&+ Int x Int` |
| `swift.&+ Int64 x Int64` |

**swift's `&+` is in the wrap part on its own evidence**, through the
merged `swift` tag, for the first time in the partition tooling rather
than by hand (log_066 §5 checked this cell by hand only).

---

## 3 — PARTITION by behaviour, VALUE reading

Compatible = no conflict at any cell where BOTH profiles answer a
value, and at least one such cell exists (log_065's operationalisation,
unchanged).

| quantity | measured |
| --- | --- |
| profiles | 98 |
| compatible pairs | 1,538 of 4,753 possible (density 0.32) |
| connected components | **3** — sizes 96, 1, 1 |
| maximal cliques | **14** — sizes 36, 36, 19, 15, 15, 11, 10, 9, 9, 5, 3, 3, 1, 1 |

**Components are not usable and the reason is measured, not argued.**
The 96-member component is not a clique: it chains through pairs that
conflict. Concrete witness inside it, the same shape log_065 recorded:
`cpp.+ int32_t x int32_t` against `cpp.+ int32_t x int64_t` disagree at
14 of 289 cells — 32-bit wrap against the exact 64-bit sum — yet both
sit in the one component.

**Cliques are a COVER, not a partition.** 39 of the 98 profiles are in
more than one maximal clique. The worst offenders:

| profile | in how many cliques | fits |
| --- | --- | --- |
| `csharp.+ short x short` | **11** | growing, approximating, wrapping 16/32/64 signed |
| `java.+ short x short` | **11** | growing, approximating, wrapping 16/32/64 signed |
| `rust.+ i32 x i32` | **9** | growing, approximating, wrapping 32/64 signed |
| `rust.+ i64 x i64` | **6** | growing, approximating, wrapping 64 signed |
| `rust.+ u64 x u64` | 3 | growing, wrapping 64 unsigned |
| `csharp.+ long x short`, `csharp.+ short x long`, `java.+ Long x short`, `java.+ long x short`, `java.+ short x Long`, `java.+ short x long` | 3 each | wrapping 64 signed |

**7 of the 14 cliques cannot be named at all**, because their members
fit DIFFERENT guaranteed adds and the intersection is empty:

| clique | n | languages | name |
| --- | --- | --- | --- |
| 0 | 36 | cpp, csharp, go, java, kotlin, rust, rust_release, swift | **wrapping** (64, signed) |
| 1 | 36 | cpp, csharp, java, python, ruby, rust, rust_release, typescript | **growing** |
| 2 | 19 | cpp, csharp, go, java, kotlin, rust, rust_release, swift | **wrapping** (32, signed) |
| 3 | 15 | cpp, csharp, java, kotlin, rust | **UNNAMEABLE** — holds `cpp __int128 x int32_t` (growing) beside `csharp int x long` (wrapping 64) |
| 4 | 15 | cpp, csharp, java, kotlin, rust | **UNNAMEABLE** — the mirrored argument order of clique 3 |
| 5 | 11 | cpp, csharp, go, java, python, rust, rust_release, swift | **UNNAMEABLE** — holds `python c_int64 x c_int64` (growing) beside `go uint64 x uint64` (wrapping 64 unsigned) |
| 6 | 10 | cpp, csharp, go, rust, rust_release, swift | **wrapping** (64, unsigned) |
| 7 | 9 | csharp, java, rust | **UNNAMEABLE** |
| 8 | 9 | csharp, java, rust | **UNNAMEABLE** |
| 9 | 5 | csharp, java, php, rust | **approximating** — `php.+ int x int` sits here with `csharp/java short x short` and `rust i32/i64` |
| 10 | 3 | csharp, java, ruby | **UNNAMEABLE** — the ruby anomaly, §6 |
| 11 | 3 | csharp, java, ruby | **UNNAMEABLE** — the same, mirrored |
| 12 | 1 | python | vacuous — `python.+ Decimal x Fraction`, no value cell |
| 13 | 1 | python | vacuous — `python.+ Fraction x Decimal`, no value cell |

---

## 4 — the two readings, side by side

Both computed here, neither chosen (standing rulings §1.1 is open).

| | ALL-CELLS | VALUE (components) | VALUE (maximal cliques) |
| --- | --- | --- | --- |
| parts | **30** | 3 | 14 |
| cross-language parts | 13 | 1 | 12 |
| is it a partition? | **yes** — every profile in exactly one part | yes, but the big one chains through conflicting pairs | **no** — a COVER; 39 profiles are in 2 to 11 parts |
| parts nameable against the three adds | 23 of 30 name exactly one, 5 non-discriminating, **2 UNCLASSIFIED** | 1 of 3 | **7 of 14 UNNAMEABLE** (members fit different adds), 2 more consistent with several |
| where `rust.+ i64 x i64` (debug) lands | its own part | inside the 96-blob | in 6 cliques at once |
| where `php.+ int x int` lands | its own part, `approximating` | inside the 96-blob | one clique, `approximating` |
| where `python.+ Decimal x Fraction` lands | with `Fraction x Decimal`, 2 members | its own component | its own singleton clique |

**The difference that matters, stated plainly and not resolved.** Under
ALL-CELLS the mode partition IS a partition and 23 of its 30 parts take
exactly one census name. Under VALUE it is a cover, and half its parts hold
profiles that fit different guaranteed adds — so "which part is this
operator in" has no answer under VALUE without a further rule. This is
not the same trade-off log_065 stated (VALUE gets the mode partition
right, ALL-CELLS gets fracture detection right); the naming step is new
evidence, and it points the other way. **Recorded as a measurement for
the owner, not as a recommendation.**

The one thing ALL-CELLS costs, unchanged from log_065 and visible
above: parts 1 and 2 are the same guarantee at two WIDTHS, and widths
are holder properties. `wrapping` appears as 6 separate parts (64
signed ×4 by argument order and holder mix, 32 signed ×3, 64 unsigned
×1) rather than one.

---

## 5 — the profiles that never reach their own fracture

Not residue, but the reason two parts are UNCLASSIFIED and the reason
the VALUE cover is a cover. A profile whose declared holder never
overflows inside the sampled X set is **consistent with every add at
once**, and no reading can tell them apart:

| profile | value cells | consistent with |
| --- | --- | --- |
| `csharp.+ short x short` | 49/289 | growing, approximating, wrapping 16/32/64 signed |
| `java.+ short x short` | 49/289 | growing, approximating, wrapping 16/32/64 signed |
| `python.+ Decimal x Fraction` | 0/289 | everything, vacuously — 289 `RAISE:TypeError` |
| `python.+ Fraction x Decimal` | 0/289 | everything, vacuously |
| `cpp.+ __int128 x __int128` | 289/289 | growing (its 128-bit wrap is unreachable in this X set) |

**`growing` in this log means "agrees with the exact sum at every cell
it answered", never "provably unbounded".** `cpp __int128` is a
fixed-width wrapping holder that the X set cannot push past its
boundary; it is named `growing` on the evidence and that naming is
evidence-limited, not a claim about c++.

This is log_065's awaiting-the owner item 4 (a fourth filter for the vacuous
profile) arriving in a second shape: not "constant function of one
argument" but "narrower than its own fracture".

---

## 6 — the residue

**16 ALL-CELLS parts of one.** Each with why it is alone:

| profile | value cells | declines | why alone |
| --- | --- | --- | --- |
| `rust.+ i64 x i64` | 221 | 35 `RAISE:panic` | **the known case** — rust debug's `unspecified`; it panics where the wrap camp answers, so no co-profile matches its full vector |
| `rust.+ i32 x i32` | 67 | 14 `RAISE:panic` | same cause, 32-bit |
| `rust.+ u64 x u64` | 102 | 19 `RAISE:panic` | same cause, unsigned |
| `php.+ int x int` | 256 | 0 | **`approximating`** — the only profile in the whole set carrying that guarantee. Alone because nothing else approximates, not because anything is wrong |
| `python.+ c_int64 x c_int64` | 256 | 0 | `growing` behaviour, but 33 `UNREPRESENTABLE` where the `2^64-1` operand cannot be constructed; its VECTOR therefore differs from `python int x int` while agreeing at every cell it answers (log_064 §4b, confirmed again here) |
| `ruby.+ Rational x BigDecimal` | 289 | 0 | **UNCLASSIFIED — a fourth behaviour**, §6a |
| `ruby.+ BigDecimal x Rational` | 289 | 0 | **UNCLASSIFIED — a fourth behaviour**, and NOT the same as its mirror: the two differ at 188 of 289 cells |
| `cpp.+ __int128 x int32_t` | 153 | 0 | `growing`; alone by `UNREPRESENTABLE` footprint — no co-language declares a 128-bit holder |
| `cpp.+ int32_t x __int128` | 153 | 0 | same, mirrored |
| `cpp.+ __int128 x uint64_t` | 170 | 17 | same |
| `cpp.+ uint64_t x __int128` | 170 | 17 | same |
| `cpp.+ int32_t x uint64_t` | 90 | 9 | `wrapping` 64 unsigned; alone by holder mix — no co-language mixes a signed 32 with an unsigned 64 |
| `cpp.+ uint64_t x int32_t` | 90 | 9 | same, mirrored |
| `cpp.+ int64_t x uint64_t` | 160 | 16 | same, signed 64 with unsigned 64 |
| `cpp.+ uint64_t x int64_t` | 160 | 16 | same, mirrored |
| `cpp.+ uint64_t x uint64_t` | 100 | 21 | `wrapping` 64 unsigned, but with 21 declines where the co-members (`csharp ulong`, `go uint64`, `rust_release u64`, `swift UInt64`) answer — so it misses part 7 on the decline footprint alone |

**Two VALUE-reading isolates** — profiles with zero comparable value
cells against every co-profile, so under the settled rule "zero
comparable keys means NO connector" they have no connector at all:
`python.+ Decimal x Fraction` and `python.+ Fraction x Decimal`, 289
`RAISE:TypeError` each. Under ALL-CELLS they are one part of two; under
VALUE they are two singletons. **The same two profiles, two readings,
opposite answers.**

### 6a — the ruby anomaly, an unnamed fourth behaviour

`ruby.+ Rational x BigDecimal` answers a value at all 289 cells and
matches NONE of the three guaranteed adds. It differs from the exact
sum at **94 of 289** cells. The objects:

| key | answered | exact |
| --- | --- | --- |
| `(-2^63, -42)` | `[-1, 1.0000000003410058947456856559555, 63]` | `[-1, 1.0000000000000000045536491244391, 63]` |
| `(-2^63, -1)` | `[-1, 1.0000000003410058903004567487649, 63]` | `[-1, 1.0000000000000000001084202172486, 63]` |
| `(-2^63, -2^31)` | `[-1, 1.0000000002328306438707100634034, 63]` | `[-1, 1.0000000002328306436538696289062, 63]` |
| `(2^63-1, 42)` | `[1, 1.0000000003410058947456856559555, 63]` | `[1, 1.0000000000000000044452289071906, 63]` |

The error appears around the tenth significant digit — the shape of a
limited-precision decimal, consistent with `BigDecimal` carrying a
default significant-digit budget when a `Rational` is coerced into it.
**Cause UNVERIFIED** — not investigated here, and it is not the log_057
float-canon fault shape (these are decimal holders, never read through
float bits).

Its mirror, `ruby.+ BigDecimal x Rational`, also differs from the exact
sum at 94 of 289 cells, but **not the same 94**: the two profiles
disagree with each other at **188 of 289** cells. Argument order
changes the answer.

This is a real fourth arithmetic behaviour in the measured data. It is
marked UNCLASSIFIED and not named, per the brief and per least-modes —
a name would be the owner's, and it is not yet established that ruby
*guarantees* this rather than merely doing it.

---

## 7 — the constructed dominant `+`, as a structural overview

the owner's §2 format. Shape only, no logic. What a dominant operator object
holds: its modes, what selects among them, and what it refuses.

```
DominantPlus
	"""
		one operator, accumulated by intention
		over 98 measured profiles; three named
		modes and one residue
	"""
	attributes:
		intention
		form
		modes
		unclassified
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


PlusMode
	attributes:
		name
		guarantee
		holder_width
		signedness
		member_profiles
		discriminating_keys
		evidence_limit
	methods:
		apply
		agrees_with


ModeSelector
	"""
		what picks a mode: the ledger's
		origin and intent, never the
		measurement
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
		reading
		parts
		cover_overlaps
		non_discriminating_profiles
		unreachable_fractures
	methods:
		...
```

`DominantPlus.modes` holds `PlusMode` instances named `wrapping`,
`growing` and `approximating` — the census's three guaranteed adds and
no others. `DominantPlus.unclassified` holds what matched none of them
(§6a) rather than forcing it into one. `DominantPlus.selector` is a
`ModeSelector`: it reads the ledger's origin and intent, and
`ModeSelector.unspecified_flag` is what carries rust's bare `+`, which
chose no guarantee. `DominantPlus.refusals` holds `Refusal` objects —
rust debug's `RAISE:panic` and python's `RAISE:TypeError` on
`Decimal + Fraction` — the keys where an origin declined, kept as data
rather than dissolved into a mode.

`DominantPlus.fracture_map` is a `FractureMap`, and it is the
measurement — deliberately a sub-object rather than the operator's
identity, because the intention is what made the operator and the
measurement only says how it fractures.

`PlusMode.evidence_limit` exists because of §5: `growing` is named on
289 agreeing cells, not on a proof of unboundedness, and the object
should carry that limit rather than let a later reader mistake it for a
guarantee.

---

## 8 — which open rulings actually BIT, and which did not

**This is the point of the exercise.**

### bit

| ruling | how it bit, measured |
| --- | --- |
| **§1.1 — the two readings** | Hard, and it is the ONLY thing that blocks. ALL-CELLS gives a partition (30 parts, 23 of them naming exactly one add). VALUE gives either 3 untrustworthy components or 14 maximal cliques that are a COVER — 39 profiles in 2 to 11 parts, and 7 of 14 cliques UNNAMEABLE because their members fit different guaranteed adds. The construction cannot proceed on VALUE without a further rule that does not exist. |
| **§1.2 — the name for php's mode** | Would have blocked §2's naming outright: part 23 is php alone and needed a name. **Ruled today** (`approximating`) and used here; had it stayed open, one of the three modes of the first dominant operator would have been nameless. |
| **§1.4 — how `rust_release` sits in the ontology** | Bit, quietly but everywhere. `rust` and `rust_release` contribute 8 of the 98 profiles and land in different parts at every width — `rust_release i64` in the 12-member wrap part, `rust i64` alone with 35 panics. If `rust_release` is a mode annotation rather than its own node, three of the sixteen singletons stop being singletons and rust's `+` becomes one operator with two build modes, which is exactly what `unspecified` already says it is. **3 of 16 residue rows turn on this one ruling.** |
| **§2.1 — swift and dart carry no `plus` at L1** | Bit. dart contributes zero profiles, so the first dominant `+` is built on eleven languages, and swift appears only through `&+` — its wrapping add — so swift's DEFAULT add has no evidence here at all. Flagged as blocking-nothing in the standing file; it turns out to bound what the constructed operator can claim. |
| **log_065 awaiting item 4 — a filter for vacuous profiles** | Bit, in a new shape (§5): not "constant function of one argument" but "holder narrower than its own fracture". `csharp/java short x short` sit in 11 cliques each; `cpp __int128` is named `growing` only because the X set cannot reach 2^127. |
| **the GROUP chaining hazard** (`SUPPORT_ontology.md`) | Bit for the VALUE partition exactly as it always has (the 96-member blob is not a clique; witness `cpp int32_t x int32_t` against `cpp int32_t x int64_t`, 14 conflicting cells). **Did NOT bite for containment** — log_067's transitivity proof retires it there. |

### did not bite

| ruling | why not |
| --- | --- |
| **§1.3 — which scoring is THE weight, and at what cut** | **Never used.** Not one number in this log came from the graded per-element similarity, and no threshold was applied anywhere. Partition by behaviour is exact-match only: cells are equal or they are not. The 0.95/0.85/0.70 cut table in the standing file has no bearing on building a dominant operator. If it matters, it matters to the explorer, not here. |
| **§2.2 — the six unmeasured chunk caps** | Pure data work; no lane was submitted. |
| **§2.3 — python's stall budget** | Same. |
| **§2.4 — where the older run products live** | `matrices_full_v2/` is complete on its own; nothing here read `SandboxDesign/agent/out/`. |
| **§2.5 — whether to retire SandboxDesign** | No probe was run. |
| **§2.6, §2.7 — Airlock repo and co-project names** | Unrelated. |
| **§3 — the PseudoCoup_v5 ledgerer walk** | Unrelated. |
| **the owner's input-overlap criterion** | No overlap percentage was computed; in the full-grid generation every profile of one `(form_pair, level)` carries the SAME key set by construction, so there is no partial overlap to defend against. It was written for a world `matrices_full_v2/` already left. |

**The short version.** One ruling blocks (§1.1). One would have blocked
and was ruled today (§1.2). Two bound what the result can claim (§1.4,
§2.1). One filter question recurs in a new shape. **Everything about
weights, cuts and thresholds turned out to be irrelevant to building a
dominant operator** — which is the most useful negative result in this
log.

---

## decided, recorded for audit

- The accumulation set was assembled by INTENTION first — every `+`
  profile on `whole|whole` across every language tag that has one — and
  no edge, overlap or score took part in deciding its membership. Said
  explicitly because it is the step the old machinery would have
  performed differently.
- Partition computed under BOTH readings, both reported, **neither
  chosen** (§4). Under VALUE, both operationalisations (components and
  maximal cliques) are reported, because they disagree 3 against 14.
- Parts are named ONLY against the census's three guaranteed adds
  (`wrapping`, `growing`, `approximating`); anything matching none is
  UNCLASSIFIED. No new name was coined — the ruby anomaly (§6a) is left
  unnamed on purpose.
- The naming check is an independent reimplementation: canon strings
  are regenerated from exact operands parsed out of the X-set
  SPELLINGS, never decoded back out of the canon (the mantissa is
  rounded at 31 digits, and an earlier draft of this check was WRONG
  for exactly that reason — recorded so the trap is not re-entered).
- `growing` is named on measured agreement with the exact sum, never on
  a proof of unboundedness; `PlusMode.evidence_limit` exists in the
  overview to carry that (§5).
- Level 1 only. Level 2 exists in `matrices_full_v2/` and was not
  partitioned; `whole|whole` only, no other form pair.
- Products: `Research/kind_fuzz_clustering/log067_dominant_plus.py` and
  `log067_dominant_plus.json` (every profile with its fit set, the 30
  ALL-CELLS parts, the 3 VALUE components and the 14 VALUE cliques, in
  full). No probe was run; no lane was submitted; `matrices_full_v2/`
  is read-only to this log.

## awaiting the owner

1. **§1.1, the two readings — this is the one that blocks.** New
   evidence beyond log_065: under VALUE the mode partition is a COVER,
   not a partition (39 of 98 profiles in 2 to 11 parts), and 7 of 14
   maximal cliques cannot be named against the three guaranteed adds
   because their members fit different ones. Under ALL-CELLS every
   profile is in exactly one part and 23 of 30 parts take exactly one census name, at
   the known cost that one guarantee appears as several parts because
   holder WIDTH is visible. Measured both ways above; not chosen.
2. **§1.4, `rust_release`** — 3 of the 16 residue singletons and 8 of
   the 98 profiles turn on it. Structural, so his.
3. **The ruby `Rational`/`BigDecimal` behaviour (§6a)** — a fourth
   arithmetic behaviour in the measured data, argument-order-dependent
   (188 of 289 cells differ between the two orders), cause UNVERIFIED.
   Is it a guarantee (and therefore a mode, and therefore the owner's to
   name), or an artefact of `BigDecimal`'s precision budget that
   belongs nowhere near the add vocabulary?
4. **Whether `wrapping` at 32 and at 64 bits is ONE mode.** The census
   says width is a holder property, not a guarantee; the ALL-CELLS
   partition splits `wrapping` into 6 parts by width, signedness and
   argument order. Collapsing them is a structural call.
5. **§2.1, dart's missing `plus`** — the first dominant `+` is built
   without dart, and swift enters only through `&+`. Whether to
   investigate now or accept the operator as eleven-language evidence.
