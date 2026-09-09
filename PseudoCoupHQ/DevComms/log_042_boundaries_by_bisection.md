# log 042 — the boundaries, found by halving

Date: 2026-08-20. Node:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

Log 042 was free when this was written; 041 and 043 exist and neither
is touched.

the owner ruled on 2026-08-20: *"i do want things like the boundaries"*.
The value classes this node has measured for nineteen logs are POINT
SAMPLES on an ordered numeric axis. Where two neighbouring samples of
one operation answer differently, the place where the answer changed
is a number, and nobody had ever asked for it. This log asks for it,
by halving the gap between the two samples until one value is left.

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Decision** means a judgment call, numbered and overturnable.
**Unverified** means nobody has checked it.

**One lane ran, once. 96,474 probes, 8.8 seconds of container time,
eleven languages, one compile each.**

---

## words used in this log

Each word is defined once, with an example taken from this log.

```
axis
    the whole-number value classes of the
    value matrix, put in numeric order.
    example tied to context:
        0, 42, 2^53+1, 2^63-1, 2^63,
        2^64-1 -- six points, five gaps.

answer class
    outcome, plus the result type, plus
    fidelity.  two answers are in the same
    class when all three agree.
    example tied to context:
        php answers `integer' at 42+42 and
        `double' at i64max+42, so those two
        are different classes.

fidelity
    whether an answer equals the exact
    mathematical result, worked out over
    the rationals.
    example tied to context:
        go's int64 42+42 is exact; its
        i64max+42 is inexact, and both are
        answers of type int64.

target
    one operation, one holder pair, one
    fixed operand, and two ADJACENT samples
    of the varying operand that answered in
    different classes.
    example tied to context:
        go `+' on int64 with 42 fixed, over
        the gap from 2^53+1 to 2^63-1.

boundary
    the least value of the varying operand
    at which the answer leaves the low
    class.
    example tied to context:
        9223372036854775766 for that target.

wall
    the boundary read in RESULT space rather
    than operand space.
    example tied to context:
        adding 42 to that boundary gives
        exactly 2^63.  the wall is 2^63.

holder ran out
    a boundary that is not the operation
    changing its mind but the holder ceasing
    to hold the axis value.
    example tied to context:
        c++'s int32_t stops carrying the
        axis at 2^31, and 472 c++ boundaries
        are that and not arithmetic.

no move
    a target whose two ends answered in the
    SAME class when re-measured, so the
    stored disagreement did not survive.
    example tied to context:
        60 of 2,798, all in kotlin and php.
```

---

## §1 walkthrough

This section is the whole log in order, in plain sentences.

I read `answers_<lang>.json` for the nine checked languages and
`behavior_<lang>_C.json` for python, ruby and php — the stored answers
at the value grain, from logs 032 to 035 — and I did not re-run any of
them. I put the six whole-number value classes in numeric order, which
they had never been put in, and asked one question of every cell: do
two NEIGHBOURING samples of this operation answer in different
classes. Answer class is defined in `l3_boundary_targets.py` as
outcome plus result type plus fidelity, and that definition is
decision B1, overturnable.

The scan found **8,067 neighbouring pairs that disagree** *(measured)*.
**1,623 of them need no run at all**, because their two samples are
adjacent integers — `2^63-1` and `2^63` sit next to each other on the
axis, so a disagreement between them IS the boundary and the stored
answers already carry it. The other **6,444 have a gap to search**.

I then had to decide how to probe a value that is not a value class.
The stored answers were made by compiling a literal into a program,
one probe per compile. Bisecting a 2^64 span needs about sixty probes
per target, and sixty compiles per target over six thousand targets is
not a run anyone would wait for. So the varying operand became a RUN
TIME variable of the holder's own type — decision B3 — which puts a
whole language's worth of targets into ONE compiled program. The cost
is stated rather than hidden: a boundary that only a compiler's
constant folding would create is invisible this way, and the two
endpoints are therefore RE-MEASURED at run time so that any
disagreement with the stored answer prints as `no move` instead of
being quietly averaged in.

Phase A — decision B4 — is the targets whose fixed operand is also a
whole holder, so both operands are integers and the reference
arithmetic needs nothing but big integers. That is **2,798 targets**
after two operation families are held out for cost — `**`, and the
shifts where a holder has no width, since one probe of
`42 ** 9007199254740993` is a hang and not a measurement (decision
B5). The first python run proved that point by being killed for
memory before the rule existed.

`l3_boundary_gen.py` writes one source file per language — python,
ruby, php, typescript, dart, java, kotlin, c-sharp, go, c++ and rust —
each carrying its own big-integer reference arithmetic, its own way of
naming the type of an answer, and its own way of catching a refusal.
The build commands are lifted verbatim from log 032's execution lanes,
so the instruments are the ones that made the answers being explained.
The smoke run was six targets per language, twice, and it caught the
one thing that mattered: **this php has neither ext-gmp nor
ext-bcmath**, so the php reference arithmetic is decimal strings
written out by hand in the harness.

The lane ran once and finished in 8.8 seconds, every language exit 0,
every language printing its own DONE line with its own probe count.
**2,738 boundaries located, 60 no-move, 96,474 probes, never more than
65 probes for any one target** *(measured)*. `l3_boundary_fold.py`
joins each printed line back to its target, works out the wall in
result space, and marks the rows where the holder ran out of room.
`boundaries.md` is the readable cross-language table.

What this adds is in §5. What surprised me is in §4, and two of the
six surprises there are about this node's own instruments rather than
about the twelve languages.

---

## §2 how the targets were derived

The derivation is host-side and reads nothing but artifacts already on
disk. `python3 l3_boundary_targets.py` finishes in 7.4 seconds and
writes `boundary_targets.json`.

The rule, stated so it can be argued with:

```
same class  <=>  same outcome
             and same result type
             and same fidelity
```

Fidelity is `na` wherever the exact result would need this node to
take a position it has no business taking — division, remainder, the
shifts, and any operand that is not a number. A pair that differs ONLY
in an `na` is not a target. A pair that differs in outcome or in
result type is a target whatever fidelity says. That is why the count
below is a floor and not a total.

| language | to bisect | already exact |
|---|---|---|
| cpp | 1462 | 518 |
| python | 1870 | 576 |
| ruby | 775 | 161 |
| typescript | 532 | 60 |
| java | 400 | 8 |
| php | 379 | 216 |
| csharp | 354 | 20 |
| dart | 222 | 46 |
| rust | 188 | 4 |
| kotlin | 180 | 10 |
| go | 82 | 4 |
| swift | 0 | 0 |
| ALL | 6444 | 1623 |

**Swift has no targets at all** *(measured)*. Swift's stored answers
are 1,552 rows against 1,066 codegen refusals, and the refusals take
out the large literals; what is left never has two neighbouring
samples that disagree. Swift is absent from every table in this log
for that reason and not because anything was skipped.

Of the 6,444, phase A ran 2,798. The remainder is written down with
its reason rather than rounded off:

| reason | targets |
|---|---|
| fixed operand is not a whole holder | 3445 |
| unbounded operation (`**`) | 127 |
| shift on a holder with no width | 74 |

---

## §3 the boundary table

The full tables are in
`Research/kind_fuzz_clustering/boundaries.md`. The cross-language
reading is this.

### the walls

Counted only where exactly one power of two lies in the closed span
and the holder still had room for the value.

| language | holder | wall | boundaries |
|---|---|---|---|
| go | `int64`, `int` | 2^63 | 24 |
| go | `uint64` | 2^64, and 0 | 26 |
| java | `int`, `Integer`, `long`, `Long`, `short` | 2^63 | 88 |
| csharp | `int`, `long`, `short` | 2^63 | 28 |
| csharp | `ulong` | 2^64, and 0 | 26 |
| kotlin | `Int`, `Long` | 2^63 | 20 |
| dart | `int` | 2^63 | 6 |
| php | `int`, BCMath | 2^63 | 50 |
| rust | `i64` | 2^63 | 12 |
| rust | `u64` | 2^64, and 0 | 26 |
| rust | `i128` | 2^127 | 2 |
| cpp | `int32_t` | 2^31, 2^63, 2^64, and 0 | 24 |
| cpp | `int64_t` | 2^63, 2^64, and 0 | 35 |
| cpp | `uint64_t` | 2^64, 2^127, and 0 | 68 |
| cpp | `__int128` | 2^127 | 4 |

That is **447 pinned walls**; the per-wall split is in
`boundaries.md`.

**Ten of the eleven languages share the 2^63 wall.** Python and ruby
appear nowhere in that table, and their absence is the finding: their
integers have no wall to find, so the only boundaries their `+`, `-`
and `*` produce are at the value 1 and in the float holders beside
them. **Zero is a wall too** — go, c-sharp, rust and c++ all have
unsigned holders whose boundary is the unsigned floor rather than a
power of two, and rust reaches it by panicking where c++ reaches it by
wrapping.

### the erosion at 2^53

A boundary at 2^53 + 1 on the operand axis is the double mantissa
running out.

| language | where it appears |
|---|---|
| cpp | 47 boundaries, `<` `<=` `>` `>=` `==` `!=` against `double` and `float` |
| ruby | 20, comparisons against `Rational` and `BigDecimal` |
| dart | 12, `==` against `BigInt` and `double` |
| java | 8, `==` and `!=` on `Long` |
| php | 8, `/` and comparisons |
| typescript | 4, `<` against `bigint` |
| go, csharp, rust | 1 each |

### the worked examples

```
go, int64 + int64, 42 fixed
  last exact  9223372036854775765
  boundary    9223372036854775766
  below       answer|int64|exact
  at          answer|int64|inexact
  result at the boundary  2^63 exactly

go, int64 * int64, 42 fixed
  boundary    219604096115589901
  which is    ceil(2^63 / 42)
  same wall, different operand value

php, int + int, 42 fixed
  boundary    9223372036854775766
  below       answer|integer|exact
  at          answer|double|inexact
  the same wall answered by a TYPE
  change rather than by a wrap

rust, u64 - u64, 42 fixed
  boundary    42
  below       raise|panic|na
  at          answer|u64|exact
  the wall is 0, the unsigned floor,
  and rust meets it by panicking

rust, i32 << i32, shift amount varying
  boundary    32
  below       answer|i32|na
  at          raise|panic|na
  and with the LEFT holder i64 the same
  target's boundary is 64
```

---

## §4 what surprised me

**1. A wall in result space is not a boundary in operand space, and
the operand boundary MOVES with the other operand.** `go.+` on int64
against 42 breaks at `2^63 - 43`; `go.*` on the same holders against
the same 42 breaks at `ceil(2^63 / 42) = 219604096115589901`, which is
not a power of two, not near one, and not a number anyone would have
guessed. Every arithmetic boundary in this log is a preimage of a
power of two under the fixed operand. **Of 2,738 located boundaries, 560 have a
power of two anywhere in their closed span and only 447 pin one with
the holder still in range**; the other 2,178 sit at divisibility, at
truthiness, at a shift width, or at a holder's edge.

**2. Rust's shift boundary follows the LEFT holder and ignores the
holder of the shift amount.** `i32 << i128` breaks at 32 and
`i64 << i32` breaks at 64 *(measured, 56 cells)*. The boundary is the
width of the value being shifted, so the same operation with the same
varying operand has three different boundaries in one language
depending on what sits on the other side. That is the clearest case in
this node of a boundary that moves with the holder.

**3. The axis is one-sided, so asymmetry could not be measured.** The
whole-number value classes run 0, 42, 2^53+1, 2^63-1, 2^63, 2^64-1 and
there is not one negative value among them. Whether a language's
negative wall sits at `-2^63` exactly, or one short of it, is
therefore **unverified** and nothing in this log's tables should be
read as evidence either way. It is a gap in the probe design of log
024, found by trying to use it for something it was not built for, and
it is the single cheapest thing left to add.

**4. All sixty no-moves are this node's own instruments and not the
languages, in two kinds.** Kotlin's eight are `BigInteger` subtraction whose
STORED answer decodes as inexact and whose re-measured answer is
exact — the host-side decoder in `l3_boundary_targets.py` reads
kotlin's big-integer payload wrongly, and eight targets exist only
because of that. Php's fifty-two are `int` comparisons at `2^63` and
above, where the stored run compiled a literal that php turned into a
float and the re-measured run assigned an integer that saturates — the
literal-against-variable cost that decision B3 named in advance,
appearing exactly where it was predicted to appear and nowhere else.

**5. Php answers a three-class span.** Forty-four php targets pass
through a THIRD class on the way from the low class to the high one:
`integer|exact`, then `double|exact`, then `double|inexact`. The
promotion to double and the loss of exactness are two different
boundaries, and every other language in the run has one boundary where
php has two. All 44 three-class spans in the whole run are php's.

**6. Six hundred and seven boundaries are a holder running out of
room, and 472 of them are one c++ holder.** C++ accepts
`int32_t v = 9223372036854775807;` with truncation, so the stored
answers for that holder were never answers about the axis value at
all — the value class name says `i64max` and the holder holds `-1`.
Those rows are counted apart in `boundaries.md` so they cannot be read
as arithmetic, and the finding that the value class NAME can lie about
what the holder holds is new to this log.

---

## §5 what this adds to the Hub's guarantee statements

The Hub can already say which languages agree on an answer for a named
value. It could not say WHERE agreement stops, and a guarantee that
holds up to an unnamed number is not a guarantee.

- **A range statement is now writable for ten languages.** "Whole
  arithmetic is exact and agrees across go, java, kotlin, c-sharp,
  dart, php, rust, c++ and the two open languages up to 2^63" is
  measured, per holder, with the exact last value in
  `boundaries_<lang>.json`.
- **The statement's failure mode differs by language and the
  difference is measured.** Above the wall go wraps, rust panics, php
  changes the answer's TYPE, and python and ruby carry on. A guarantee
  that stops at 2^63 stops in four different ways.
- **A guarantee must name the holder and the other operand, not just
  the operation.** `*` against 42 fails at a different value than `+`
  against 42, and rust's `<<` fails at a different value depending on
  what it is shifting.
- **The 2^53 line is a separate guarantee from the 2^63 line** and it
  is reached through comparisons, not through arithmetic: six
  languages have boundaries at 2^53 + 1 and they are `==`, `<` and
  their kin.
- **Nothing here licenses a statement about negative values.** §4 item
  3 says why, and any Hub sentence that reads "±2^63" would be
  asserting something this node has not measured.

---

## products

```
l3_boundary_targets.py    the derivation
boundary_targets.json     8,067 pairs, 6,444
                          to bisect
l3_boundary_gen.py        eleven harnesses
bnd/*.{py,rb,php,ts,dart,
       java,kt,cs,go,cpp,rs}
l3_boundary_lane.py       the lane wrapper
lanes/bs_all.sh           the run that
                          produced this log
raw/bnd_<lang>.out        what the run
                          printed, verbatim
l3_boundary_fold.py       the fold
boundaries_<lang>.json    eleven files
boundaries_index.json     the roll-up
l3_boundary_report.py     the reader
boundaries.md             the table
```
