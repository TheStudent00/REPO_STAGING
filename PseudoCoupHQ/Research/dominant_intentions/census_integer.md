# feature census — integer (the hard costume case)

2026-08-13, hand-drafted in the owner format ruled the same day
(structure / operation / border; border facts billed to the other
party). Fresh work, no old-project artifacts. EVERY FACT
UNVERIFIED — this page is the harness's work order, and integer is
where verification matters most.

The prediction being tested: bool and float kept their structure
layers universal. Integer is where the costume goes all the way
down — the structure itself should fracture. It does.

RULINGS ABSORBED (the owner, 2026-08-13, post-draft discussion):
- **mode-dependent facts record BOTH behaviors** (rust
  debug/release, dart native/web) — defer-the-decision applied.
- **the guarantees rule**: the Hub models every fracture as the
  set of GUARANTEES the languages make (three divisions, wrapping
  add, growing add...); ingress reads which guarantee the source
  language makes (statically — declared types are the context,
  the owner's observation) and stores THAT operation; the transpiler may
  make a guarantee explicit but never guesses past one. cpp
  signed overflow, having no guarantee, constrains nothing.
- least-modes: the mode set is the set of EXISTING guarantees,
  never a Hub-invented addition (division: floor / truncate /
  float — three, because three exist).
- **overflow CLOSED** (the owner confirmed 2026-08-13): wrap and grow
  are two guaranteed adds, both modeled; the ledger's
  origin+intent determines which a source meant. No contradiction
  remains.
- **php's float promotion is a THIRD guaranteed add** (the owner, ruled
  2026-08-23, on the twelve-language cartesian measurement): on
  `(2^63-1) + 42`, php answers exactly `2^63` where the true sum is
  `2^63 + 41` — the low bits are gone and nothing is raised. It is
  neither wrap nor grow, and php specifies it, so by the guarantees
  rule it is a guarantee and by least-modes it is a mode.
  the owner's reason, which names the intention rather than the mechanism:
  "i mean safety as in the system can still run and is correct for
  some amount of digits the way a floating point number is. so still
  potentially useful but also potentially catastrophic if full
  precision is expected... but preventing a system crash could be an
  intention. so yeah i think its a mode."
  - the intention is KEEP RUNNING WITH AN APPROXIMATE ANSWER — the
    same contract a float carries, arrived at from the integer side.
  - **NAMED `approximating`** (the owner, ruled 2026-08-23, on Claude's
    suggestion: "approximating is fine"). It names what happens to the
    answer rather than the mechanism that produced it. **The three
    guaranteed adds are now `wrapping`, `growing`, `approximating`.**
  - egress selects it only where the source meant it. Under the
    discipline assumption a developer does not rely on silent
    precision loss, so it is carried for ingress fidelity and
    rarely chosen — modelled, not preferred.
  - measured evidence: `~/Programming/PseudoCoupHQ/DevComms/log_064_twelve_language_fold_and_lattice.md`;
    the cell is in `matrices_full_v2/php.plus.L1.csv`.
- **cpp undefined signed overflow, ruled** (the owner, 2026-08-13):
  cpp integer safety is developer discipline, so — if a cpp
  source EXPLICITLY manages overflow, that logic transpiles with
  it and the intent is preserved; if it does not, transpilation
  may safely impose managed overflow (there is no guaranteed
  behavior to betray); a developer purposefully exploiting UB
  overflow modifies manually — surprising if ever needed.
  Flag-if-unhandled (an ingress warning naming the arithmetic
  that COULD overflow unmanaged) noted as a nice-to-have
  diagnostic, feasibility unverified.
- **compile-time refusal is a first-class camp answer** (the owner,
  2026-08-14, ruling on log 020 §3 correction 10): beside
  value-answers and raises, "refuses at build time" is now a
  named third result category. 34 measured instances back this,
  and in six places the refusal IS the language's stated
  guarantee (rust's move, rust's borrow-during-edit, rust's string
  indexing, go's slice `==`, go's constant negative index, every
  declared-element-type violation). Census pages may say "refuses
  at build time" as a first-class camp answer alongside answering
  a value or raising. (measured, log_020 run 2026-08-14; ruled by
  the owner 2026-08-14)
- **mode annotations apply PER-FACT, not per-language** (the owner,
  2026-08-14, ruling on log 020 §3 correction 11): dart's two
  modes (native/web) diverge on F-i2, F-i5 and F-i6, not on every
  fact; rust's two modes (debug/release) diverge on F-i2 only. The
  mode annotation belongs on the individual fact it affects, not
  as a blanket per-language note. (measured, log_020 run
  2026-08-14; ruled by the owner 2026-08-14)
- **rust's bare `+` is `unspecified`** (the owner, 2026-08-14, name
  provisional on his veto): rust's bare `+` on integers maps to
  NEITHER the wrapping-add guarantee nor the growing-add guarantee
  — it panics or wraps depending on build mode, which is not a
  portable choice. Ingress records this as `unspecified` (the term
  is drawn from the C standards literature itself, per the
  origin-naming rule): the developer did not choose an add
  guarantee, the ledger carries the `unspecified` flag, and egress
  may then choose any guaranteed add when translating. (ruled by
  the owner 2026-08-14, name provisional on his veto)

---

## structure facts — FRACTURED (the first structure-level fracture
in the census)

**F-i1 — what values an "integer" can hold.** Three camps:

- **fixed-width**: rust (i8..i128, u8..u128, developer-chosen),
  go (int, int8..64, uint...), java (int/long — NO unsigned),
  csharp (int/long/uint/ulong), kotlin (Int/Long), cpp
  (int/long long/unsigned...), dart (int, 64-bit), php (int,
  64-bit).
- **unbounded**: python, ruby — the value grows as needed
  (level-1 composition: boxed growable buffer of level-0 words).
- **there is no integer**: typescript — `number` is the float;
  integers are exact only to 2^53; BigInt exists as a separate
  opt-in structure.

Sub-fracture: WHO chooses the width. developer-chosen (rust, go,
csharp, cpp, java, kotlin) vs language-fixed (dart, php) vs
nobody/unbounded (python, ruby) vs float (typescript).

Sub-fracture: unsigned integers exist (rust, go, csharp, cpp) /
do not (java, kotlin mostly, python*, ruby, dart, php, ts).
(*python: unbounded makes the question moot.)

dart-web addendum: dart's web compiler REFUSES a source text
merely for containing an integer literal JavaScript cannot
represent exactly (`<compile-error>`, verbatim: "The integer
literal 9007199254740993 can't be represented exactly in
JavaScript"), for both 2^53+1 and 2^63-1. This is a build-time
refusal, not the run-time float erosion the "behaves as floats"
phrasing implies — arithmetic still erodes silently, but literals
are refused outright. (measured, log_020 run 2026-08-14; ruled by
the owner 2026-08-14)

## operation facts

Universal candidates (believed 11/11, within representable range):

- + - * agree exactly while no limit is hit.
- comparison (< <= == etc.) agrees exactly.
- decimal printing of an in-range integer agrees.

Fractures (integer's own operations — these stay):

- **F-i2 — overflow: what happens when + - * exceed the width.**
  The deepest fracture in the census so far; FIVE behaviors:
  - wrap silently: java, kotlin, csharp (default unchecked), go,
    cpp UNSIGNED, php-adjacent (see below), dart (native).
  - undefined behavior: cpp SIGNED overflow — no behavior at all
    to preserve; the worst case for dominance.
  - mode-dependent: rust — debug builds PANIC, release builds
    wrap. dart — native wraps at 64 bits; web-compiled REFUSES at
    build time for any literal the web's underlying float cannot
    represent exactly (`<compile-error>`, verbatim: "The integer
    literal ... can't be represented exactly in JavaScript") rather
    than eroding to float behavior at run time — the census's
    "behaves as floats" is true of arithmetic, not of literals.
    (measured, log_020 run 2026-08-14; ruled by the owner 2026-08-14)
    dart-web overflow BEHAVIOUR, follow-up measured: with the 64-bit
    max reached by arithmetic (`x = 1`, doubled 63 times, minus 1)
    rather than written as a literal, the compiler does not refuse.
    `maxVal` prints as `9223372036854776000`, `maxVal + 1` prints
    the SAME `9223372036854776000` (the float's precision gap
    swallows the +1), and `maxVal + x` (adding another 2^63) prints
    `18446744073709552000` — no throw, no wrap, no compile-error,
    silent float erosion throughout. This CONFIRMS the census's
    original "behaves as floats" claim for arithmetic overflow
    itself; the `<compile-error>` findings above are about literals
    only, never about overflow behaviour. (measured,
    dartweb_overflow.sh lane run 2026-08-14; ruled by the owner
    2026-08-14)
    NEW FACT TYPE: behavior varies WITHIN a language
    by build mode; the census format needs a mode annotation
    (format finding for the owner).
  - become a float: php — an overflowing int quietly converts to
    float, losing exactness.
  - grow: python, ruby — no overflow exists.
  - (typescript: no overflow because no integer; exactness just
    erodes past 2^53, silently.)
- **F-i3 — what division answers.**
  - `/` gives a float: python, typescript, php, dart, ruby-NO
    (see next), kotlin-NO.
  - `/` gives a truncated integer (toward zero): rust, go, java,
    csharp, kotlin, cpp; dart spells it `~/`.
  - `/` gives a FLOORED integer: ruby (7/2 is 3, -7/2 is -4).
  - python's integer division is spelled `//` and FLOORS
    (-7//2 is -4) — agreeing with ruby's rounding, not with the
    truncating camp.
- **F-i4 — the sign of modulo.** THREE camps:
  - result takes the DIVISOR's sign (floor-mod): python, ruby.
  - result takes the DIVIDEND's sign (truncating remainder):
    rust, go, java, csharp, kotlin, cpp, typescript, and **php**
    (measured: `-7 % 2` is `-1`, `7 % -2` is `1`). (measured,
    log_020 run 2026-08-14; ruled by the owner 2026-08-14)
  - result is NEVER negative (Euclidean modulo): **dart, both
    modes** (measured: `-7 % 2` is `1`, `7 % -2` is `1`). dart's
    truncating remainder is spelled `.remainder()`, so dart ships
    both operations under different names and the origin-naming
    rule applies unchanged. (measured, log_020 run 2026-08-14;
    ruled by the owner 2026-08-14)
  - (-7 mod 2: python answers 1, java answers -1.)
- **F-i5 — integer division by zero.**
  - raise/throw/panic: python, ruby, java, csharp, kotlin, go
    (runtime panic), rust (panic), dart-native (throws, both `/`
    and `%`), php 8 (throws).
  - undefined behavior: cpp.
  - Infinity/NaN: typescript (it was never an integer).
  - **dart-web splits from dart-native**: integer division by zero
    throws (`<raise:UnsupportedError>`) same as native, but modulo
    by zero answers **`NaN`** (falls through to JavaScript's `%`)
    instead of throwing. dart's two modes agree on division-by-zero
    and disagree on modulo-by-zero. (measured, log_020 run
    2026-08-14; ruled by the owner 2026-08-14)
- **F-i6 — bit operations and their width.**
  - on the declared width: rust, go, java, csharp, kotlin, cpp,
    dart(native).
  - on an unbounded value (defined as if infinite two's
    complement): python, ruby.
  - coerced to 32 BITS regardless: typescript — `1 << 31` is
    negative; the famous surprise.
  - **dart-web, its own row**: the JavaScript 32-bit shift, but not
    typescript's — measured `1 << 31` is `2147483648` (positive,
    unlike typescript) and `1 << 32` is `0` (unlike dart-native's
    `4294967296`). dart-web agrees with neither the declared-width
    camp nor typescript. (measured, log_020 run 2026-08-14; ruled
    by the owner 2026-08-14)

## border facts — filed away, for the record

- **→ (integer, float) under equality and promotion** — already
  on float's page (F-f2).
- **→ (integer, bool)** — already on bool's page (True == 1).
- **→ (integer, text)**: parsing conventions (leading zeros,
  underscores in literals, radix prefixes) — billed to the
  conversion machinery; decimal PRINTING of in-range values is
  universal enough to sit in the operations universals above.

## reading — the dominance crux, stated plainly

- **Containment is easy; behavior is not.** The unbounded camp's
  integer CONTAINS every fixed-width integer's values — as a set
  of values, python's costume is the union, and the dominant
  integer holds values without contradiction.
- **The contradiction candidate is F-i2, exactly as predicted.**
  A program that RELIES on wrapping (hash functions, checksums,
  ring arithmetic) breaks under grow; a program relying on grow
  breaks under wrap. No single behavior satisfies both — unless
  the dominant carries BOTH as distinct operations (wrapping add
  vs growing add) and the mapping records which one a source
  program meant. That is the owner's split-when-dominance-fails ruling
  arriving on schedule: the split may be per-OPERATION (two adds)
  rather than per-STRUCTURE (two integers) — open, the owner's call,
  and the first ruling the runtime results must inform.
- cpp signed overflow being UNDEFINED is strangely good news for
  ingress: there is no behavior to preserve, so any dominant
  choice is faithful to a correct cpp program.
- F-i3/F-i4 (division and modulo) are NOT contradictions — every
  camp's answer is computable from every other's — they are
  polyfill table entries, cheap.
- two format findings for the owner: (a) MODE-dependent behavior
  (rust debug/release, dart native/web) needs a census
  annotation; (b) structure-level fractures exist (F-i1), so the
  "structure facts" section is not always a universals list.

---

## layer-3 findings, folded back 2026-08-19

Everything above was hand-drafted 2026-08-13 and marked UNVERIFIED:
the page was the harness's work order. The layer-3 campaign has since
run — logs 024 through 037 in
`~/Programming/PseudoCoupHQ/DevComms/`. This section carries what
those runs PROVED that the sections above do not already say. Nothing
stated above is repeated here.

Each item names the log and section it comes from, and its level.
**Measured** means a number a run printed. **Derived** means a number
worked out from measured numbers.

### the words this section uses

```
probe
    one small generated program that asks one
    language one question.
    example tied to context:
        `42 << 42` declared in a 32-bit signed
        slot, in seven languages, is seven
        probes.

holder
    the typed slot a value is put into before
    an operation is applied to it.  one census
    camp can hold several holders.
    example tied to context:
        go's `int32` and c++'s `int32_t` are
        two holders of the fixed-width camp of
        F-i1.

value class
    a named family of test values, chosen so
    the awkward cases are covered.
    example tied to context:
        `i64max` is a value class: the largest
        signed 64-bit integer.

cell
    one combination of operand kinds an
    operation was asked about.
    example tied to context:
        `whole|whole` is the cell where both
        operands are whole numbers.

answer grain
    measuring what an operation RETURNS, as
    against measuring only whether the
    language accepts it.
    example tied to context:
        every language below accepts
        `i64max + 42`; the answer grain is
        what separates the wrappers from the
        panicker.

mixed-holder ratio
    the share of a language's accepted cells
    for one operation where the two operands
    sit in DIFFERENT holders.  a high ratio
    means the operation is relaxed about
    mixing widths.
    example tied to context:
        go's `<<` is 0.75 and go's `+` is
        0.00 — go lets you shift an int64 by
        an int32 and will not add them.
```

### F-i2 (overflow) — the wrap camp agrees BIT FOR BIT

- On `i64max + 42`, with both operands in the language's own 64-bit
  signed holder, five languages return the identical bit pattern
  `INT:64:8000000000000029` — go `int64`, c++ `int64_t`, java `long`,
  c-sharp `long`, kotlin `Long`. *(measured, log_032 §5 surprise two)*
- The page above put those five in one camp on the strength of language
  knowledge. The measurement is stronger than the camp: it is not that
  they all wrap, it is that they wrap to the same bits.
- Rust is alone in that set, and the log states WHY as a property of the
  build rather than of the language: this build has debug assertions on,
  which is rust's own default for an unoptimised build, and the same
  source built with `-O` wraps like the other five. *(measured,
  log_032 §5 surprise two)* That is the page's record-both-modes ruling
  arriving with a measurement behind it.

### F-i2 (overflow) — php's fall to float, with the actual tokens

The page says php's overflowing int quietly converts to float. Here is
the run saying it, against the two growing languages:

- `i64max + 42` answers `whole:9223372036854775849` in python and in
  ruby, and `fractional:9.2233720368548e+18` in php. *(measured,
  log_031 §5.1)*
- At the cell level this makes `+` on `whole|whole` agree **1.000
  python-with-ruby and 0.306 for php against either**. *(measured,
  log_031 §5.1)* Two camps predicted; two camps measured, with a number
  on the gap.

### F-i2 — a language contradicts ITSELF, inside python

- The same run found python answering `u64max + 42` two ways at once:
  `whole:18446744073709551657` from its ordinary integer, and
  `whole:41` from its `ctypes.c_int64` holder — that value class loaded
  into a fixed-width holder wraps to −1, and −1 + 42 is 41. *(measured,
  log_031 §5.1)*
- This matters to F-i1's "unbounded" camp, which the page treats as one
  thing. Python's unboundedness is a property of one holder, not of the
  language: python can be made to wrap, on purpose, by choosing a
  different holder.

### F-i2 at the answer grain — wrapping alike does NOT make languages alike

Two facts point opposite ways, and the second is the one that decides.

- **The fact that says the wrap camp should group:** the five languages
  above return identical bits on the overflow cell. *(measured,
  log_032 §5 surprise two)*
- **The fact that decides:** when the whole answer signature is
  compared, `go.+` sits nearest `rust.+` at similarity **0.907** — the
  language that PANICS — while `go.+` against `java.+` is **0.094**,
  and that is with the two agreeing on every shared cell, agreement
  exactly 1.000. *(measured, log_033 §4.2)*
- The cause is the domains, not the answers: `go.+` and `java.+` barely
  accept the same cells, so agreeing on the few they share buys them
  nothing. **`+` splits into four families at the answer grain, and
  overflow behaviour is not what draws the lines.** *(measured,
  log_033 §4.1)*
- Read against this page's "reading" section: F-i2 remains the
  contradiction candidate for DOMINANCE, and it is not the axis the
  languages actually cluster on. Those are two different questions and
  the page only asked the first.

### F-i5 (division by zero) — c++ does not merely have undefined behavior, it DIES

- `42 / 0` on each language's own integer holder splits six ways, and
  two rows are sharper than the page's F-i5:
  - **c++ is a death, not a raise**: `SIGFPE`, uncatchable — the
    process is gone, so there is no behaviour for a program to observe
    or recover from. *(measured, log_032 §5 surprise three)*
  - **dart ANSWERS**: `FLOAT:64:7ff0000000000000`, positive infinity,
    because dart's `/` is not integer division at all and returns a
    `double` whatever its operands are. Dart's `~/` does raise,
    `IntegerDivisionByZeroException`. *(measured, log_032 §5 surprise
    three)* The page files dart-native under "throws, both `/` and
    `%`"; the run says `/` is a different operation wearing the same
    spelling.
- `42 % 0` gives typescript `FLOAT:64:7ff8000000000000`, which is NaN,
  where every other language raises or dies. *(measured, log_032 §5
  surprise three)*

### F-i6 (bit operations) — the shift mixed-holder exemption, and where it is real

The page records what width a shift operates ON. The runs measured a
different thing: which holder PAIRS a shift will accept at all.

- Ranked by the mixed-holder ratio, restricted to the nine statically
  checked languages *(measured, log_030 §4.4)*:

| language | `<<` | `>>` | `+` | `-` | `*` |
|---|---|---|---|---|---|
| go | 0.75 | 0.75 | 0.00 | 0.00 | 0.00 |
| rust | 0.75 | 0.75 | 0.14 | 0.00 | 0.00 |
| cpp | 0.71 | 0.71 | 0.64 | 0.64 | 0.67 |
| csharp | 0.73 | 0.73 | 0.70 | 0.64 | 0.64 |
| java | 0.80 | 0.80 | 0.78 | 0.76 | 0.76 |
| dart | 0.75 | 0.75 | — | — | 0.71 |
| typescript | 0.00 | 0.00 | 0.50 | 0.00 | 0.00 |
| kotlin | — | — | 0.62 | 0.65 | 0.36 |
| swift | — | — | — | — | 0.00 |

- **The exemption is total in go and rust only** — shifts at 0.75
  against arithmetic at 0.00 to 0.14. *(measured, log_030 §4.4)*
- **It is barely measurable in java** — shifts 0.80 against `+` 0.78 —
  and c++, c-sharp and dart sit with java. *(measured, log_030 §4.4)*
  Where implicit numeric promotion already mixes arithmetic holders,
  the shift has nothing to be exempt from.
- **Typescript inverts it**: shifts 0.00, `+` 0.50. *(measured,
  log_030 §4.4)*
- The tally is **two sharp against four blunt**. Level **derived**,
  from the rows above.
- The question is CLOSED, and it closed by ruling a language out rather
  than letting one in. Kotlin cannot move the tally: its grammar does
  not declare `shl`, `shr` or `ushr` as operators — the two-sided
  expression node carries an ordinary identifier where an operator
  token would be — and `val shl: Int = 1` compiles, so the name is an
  ordinary name. Kotlin's shifts are library functions. *(measured on
  both tests, log_034 §1)* The re-fold confirmed the consequence: the
  eleven-member shift group returned with no twelfth. *(measured,
  log_035 §6.4)*

### F-i6 (bit operations) — `42 << 42` gives seven acceptances and five answers

Every one of these is an ACCEPT, so an acceptance-grain pass records
one thing here and stops. On a 32-bit signed holder *(measured,
log_032 §5 surprise one)*:

| language | holder | result |
|---|---|---|
| go | int32 | `INT:32:00000000` — zero |
| rust | i32 | panic |
| c++ | int32_t | `INT:32:0000a800` — 43008 |
| java | int | `INT:32:0000a800` — 43008 |
| c-sharp | int | `INT:32:0000a800` — 43008 |
| typescript | number | `FLOAT:64:40e5000000000000` — 43008.0 |
| dart | int | `INT:64:0000a80000000000` — 43008 × 2³² |

- Three mask the shift count to five bits and answer 43008. Go does not
  mask and answers zero. Typescript masks and then hands back a float,
  because it has no integer. Dart shifts inside 64 bits. Rust refuses to
  answer.
- This adds a camp the page's F-i6 has no row for: **whether the shift
  COUNT is masked**, which is a separate question from what width the
  shift operates on. Go and the maskers agree on width and disagree on
  the answer.
