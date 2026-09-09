# log 020 — the full census run (WP2, phase 1 complete)

2026-08-14. The main event of phase 1: the four heavy census pages — integer,
string, list, dict — executed against real compilers and interpreters, using
the harness the boolean/float calibration run built and calibrated (log 019).
Design constraints from log 018 §2 were settled and were not re-opened.

## §1 — plain-words walkthrough

The cold words first, one line each, because this log leans on all of them:

- **census page** — a hand-written page in `Research/dominant_intentions/`,
  one per data structure, saying what that structure does in each of the
  target languages. Every line on it was written from knowledge and marked
  UNVERIFIED by design.
- **fact** — one such line. `F-i2` is the census's name for "what happens when
  an integer overflows".
- **owner** — each fact belongs to *structure* (what values the thing holds),
  *operation* (what you can do to it) or *border* (this thing meeting some
  other machinery). Border facts are billed elsewhere and are out of scope.
- **universal** — a fact the census believes all languages agree on.
- **fracture** — a fact the census believes the languages split on, with named
  camps.
- **guarantee** — a promise a language makes and keeps. the owner's standing ruling
  is that the Hub models each fracture as the SET of guarantees on offer, and
  ingress records which one a source language made.
- **vector** — a fact turned into something executable: an identifier, a tiny
  piece of code per language, and the answer each language is supposed to give.
- **probe** — one such tiny piece of code. A fact has several, so a fact fails
  in a nameable place rather than as a shrug.
- **mode column** — one language run twice because it behaves differently
  depending on how it is built. Two exist: rust in debug and in release, and
  dart compiled to native code versus compiled to JavaScript for the web.
- **the lane** — the SandboxDesign agent lane. This session cannot run
  containers itself; it writes a shell script into a watched directory, a
  daemon runs it inside the sandbox one script at a time, and the products
  come back where this session can read them.
- **record-not-check** — new this run. Where a census page names no camp for
  some language, that cell RECORDS what the language did instead of grading
  it, because grading a claim nobody made would be grading nothing. Every such
  answer is carried into §3 as a proposed census addition.

What happened, in order:

1. **dart was installed.** `allow.sh sync` put `.googleapis.com` into the
   proxy allowlist, so the SDK finally came down (238 MB, dart 3.13.0). Both
   modes work: `dart run` for native and `dart compile js` plus node for the
   web. That closes the one toolchain gap log 019 left open, and it means the
   census's dart-native-versus-dart-web claim could actually be tested rather
   than assumed. c# remains blocked-deliberate (no toolchain, not pursued).
   Swift was NOT run on these four pages: it is a bonus language outside the
   census's eleven targets, its cells would be informational only, and the
   instruction was to keep the run proportionate.
2. **Four vectors files were written** — `vectors_integer.json`,
   `vectors_string.json`, `vectors_list.json`, `vectors_dict.json` — covering
   every structure and operation fact on the four pages, universals included,
   with the border facts those pages file away left out. 41 facts, 79 probe
   definitions.
3. **The harness grew four things** it did not need for boolean/float, all of
   them foreseen in log 019 §5: per-language probe TEXT (there is no single
   expression that means "add one to the largest integer" in eleven
   languages); a build step separated from a run step, so a program the
   compiler REFUSED can be told apart from a program that built and then died;
   per-program preamble files, because one compiler refuses a source text
   merely for containing a literal it cannot represent; and two new
   expectation spellings, `<any>` and `<raise:*>`, which carry the owner's rulings
   rather than values.
4. **Four lane scripts ran**, one per page, serial as the lane requires.
   715 probe results came back. Total execution time across all four:
   **70 seconds.**
5. **compare.py graded every cell** and wrote `verified_integer.json`,
   `verified_string.json`, `verified_list.json` and `verified_dict.json` into
   `Research/dominant_intentions/verified/`.

**The headline: 467 CONFIRMED, 7 REFUTED, 100 SKIPPED**, across 574
fact-by-language cells (41 facts × 14 columns). All 7 refutations sit in the
dart columns and one php cell. Nothing else in four pages of hand-written
claims had to be withdrawn.

The single most interesting thing the run produced is not a refutation at all.
It is that **rust's debug build and rust's release build genuinely disagree**
about what integer overflow does — debug panics, release wraps silently, the
same source text, the same machine, forty milliseconds apart — which is
exactly what the census predicted and exactly why the owner's record-both-modes
ruling exists. §4 shows it.

The census pages have NOT been edited. Every correction is proposed in §3 as a
numbered list for the owner.

## §2 — the verified tables

`OK` = CONFIRMED, `XX` = REFUTED, `--` = SKIPPED (the language is absent, or
the probe does not exist there).

### integer — 102 CONFIRMED / 6 REFUTED / 18 SKIPPED

| fact | owner | kind | python | ts | java | csharp | go | rust | rust-rel | ruby | php | kotlin | cpp | dart | dart-web | swift |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| int-U1 + - * agree in range | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| int-U2 comparison agrees | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| int-U3 decimal printing agrees | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-i1 what values it holds | structure | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | **XX** | -- |
| F-i2 overflow | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | **XX** | -- |
| F-i3 what division answers | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-i4 the sign of modulo | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | **XX** | **XX** | -- |
| F-i5 division by zero | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | **XX** | -- |
| F-i6 bit ops and their width | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | **XX** | -- |

Fracture evidence, since `OK` on a fracture means "the split is where the
census said it was", never "everybody agreed":

**F-i1 — what values an integer holds.** The probe is 2^53+1, the first whole
number a 64-bit float cannot hold, and then the 64-bit maximum.

| probe | python | ruby | php | typescript | go / cpp / java / rust / kotlin | dart | dart-web |
|---|---|---|---|---|---|---|---|
| a `9007199254740993` | 9007199254740993 | 9007199254740993 | 9007199254740993 | **9007199254740992** | 9007199254740993 | 9007199254740993 | **&lt;compile-error&gt;** |
| b `9223372036854775807` | exact | exact | exact | **9223372036854776000** | exact | exact | **&lt;compile-error&gt;** |
| c `2**70` (unbounded camp only) | 1180591620717411303424 | same | — | — | — | — | — |
| d 8-bit maximum (declared-width camp only) | — | — | — | — | 127 | — | — |
| e unsigned 8-bit maximum (unsigned camp only) | — | — | — | — | 255 (rust, go, cpp) | — | — |

typescript's answers are the census's "there is no integer" claim, measured:
it does not fail, it silently rounds. The comparison is numeric, not textual,
so `9223372036854776000` and `9223372036854775808` count as the same double —
log 019's never-compare-printed-floats rule doing its job.

**F-i2 — overflow.** Each language's own guaranteed spelling of "largest value
plus one", through opaque runtime values so no compiler can answer it early.

| probe | result |
|---|---|
| a python / ruby | `9223372036854775808` — grew, exactly as censused |
| a java / kotlin / go / dart-native | `-9223372036854775808` — wrapped |
| a **rust (debug)** | `<raise:panic>` |
| a **rust (release)** | `-9223372036854775808` |
| a cpp | `-9223372036854775808`, recorded as evidence only — signed overflow is UNDEFINED, so per the owner's ruling no answer can be wrong |
| a php | `double` — the int became a float, as censused |
| a typescript | `9223372036854775808` — same digits as python, entirely different reason (float rounding, not growth) |
| a dart-web | `<compile-error>` — see §3 |
| b unsigned wrap (rust, go, cpp) | `0` in all three — a real guarantee even in c++ |
| c rust `wrapping_add` | `-9223372036854775808` in **both** build modes |

Probe c is the load-bearing one for the guarantees rule: rust's DEFAULT
arithmetic is mode-dependent and therefore promises nothing portable, but
rust's explicitly-spelled wrapping add is identical in debug and release. A
rust source that says `wrapping_add` has CHOSEN the wrapping guarantee, and
that choice survives translation. A rust source that says `+` has chosen
"panic or wrap, depending how you build me", which is a different thing.

**F-i3 — what `/` answers**, and **F-i4 — the sign of modulo**:

| probe | python | ruby | php | ts | go/cpp/java/rust/kotlin | dart | dart-web |
|---|---|---|---|---|---|---|---|
| F-i3.a `7 / 2` | 3.5 | 3 | 3.5 | 3.5 | 3 | 3.5 | 3.5 |
| F-i3.b `-7 / 2` | -3.5 | **-4** | -3.5 | -3.5 | -3 | -3.5 | -3.5 |
| F-i3.c separate integer division | `//` → -4 | `.div` → -4 | — | — | — | `~/` → **-3** | -3 |
| F-i4.a `-7 % 2` | 1 | 1 | -1 | -1 | -1 | **1** | **1** |
| F-i4.b `7 % -2` | -1 | -1 | 1 | 1 | 1 | 1 | 1 |

Three divisions exist and all three were found: float, truncate-toward-zero,
and floor. ruby floors with `/`; python floors with `//`; dart TRUNCATES with
`~/` — so dart's separate integer division belongs to the truncating camp
while dart's `/` belongs to the float camp, which is what the census says.

**F-i5 — integer division by zero**, verbatim from the results:

| language | `7 / 0` (integer) | `7 % 0` |
|---|---|---|
| python | `<raise:ZeroDivisionError>` | same |
| ruby | `<raise:ZeroDivisionError>` | same |
| php | `<raise:DivisionByZeroError>` | same |
| java / kotlin | `<raise:ArithmeticException>` | same |
| go | `<raise:runtime error: integer divide by zero>` | same |
| rust (both modes) | `<raise:panic>` | same |
| dart-native | `<raise:IntegerDivisionByZeroException>` | same |
| dart-web | `<raise:UnsupportedError>` | **`NaN`** |
| cpp | `<aborted>` — the process died on a signal; UNDEFINED, recorded not graded |
| typescript | `Infinity` | `NaN` |

**F-i6 — bit operations and their width.** Probe a shifts inside a 32-bit
declared type, probe b inside a 64-bit one; together they are what "on the
declared width" MEANS.

| probe | python/ruby/php | ts | go/cpp/java/rust/kotlin | dart | dart-web |
|---|---|---|---|---|---|
| a `1 << 31` | 2147483648 | -2147483648 | -2147483648 | 2147483648 | 2147483648 |
| b `1 << 32` | 4294967296 | **1** | 4294967296 | 4294967296 | **0** |

typescript answering `1` to `1 << 32` is the famous 32-bit coercion, censused
and confirmed. dart-web answering `0` is new — §3.

### string — 107 CONFIRMED / 1 REFUTED / 18 SKIPPED

| fact | owner | kind | python | ts | java | csharp | go | rust | rust-rel | ruby | php | kotlin | cpp | dart | dart-web | swift |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| str-U1 concatenation joins | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| str-U2 a content comparison exists | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| str-U3 substring by its own unit | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| str-U4 named-encoding round trip exact | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-s1 what one position holds | structure | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-s2 can it change in place | structure | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | **XX** | OK | OK | OK | OK | -- |
| F-s3 what length counts | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-s4 what `s[i]` answers | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-s5 what `==` does | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |

The two reference texts are "é" (U+00E9: 1 codepoint / 1 utf16 unit / 2 utf8
bytes) and the musical G-clef "𝄞" (1 / 2 / 4). The unit fracture, measured:

| probe | python | ruby | java / kotlin / ts / dart | go / rust / php / cpp |
|---|---|---|---|---|
| F-s1.a first unit of "é", numerically | 233 | 233 | 233 | **195** |
| F-s1.b first unit of "𝄞", numerically | **119070** | 119070 | **55348** (a high surrogate) | **240** |
| F-s3.a length of "é" | 1 | 1 | 1 | 2 |
| F-s3.b length of "𝄞" | 1 | 1 | **2** | **4** |
| F-s3.c length of "é𝄞" | 2 | 2 | 3 | 6 |

Three lengths for one text, exactly as censused, and the G-clef is what
separates the codepoint camp from the utf16 camp — for "é" alone those two
camps agree, which is why one reference character would not have been enough.

**F-s4 — indexing** answers a one-character string in python, ruby, php, java,
kotlin and typescript; a unit NUMBER (97) in go, cpp and dart; and in rust it
does not compile at all — `<compile-error>` — while a byte-range slice landing
off a character boundary gives `<raise:panic>`. Both of rust's answers are
guarantees, and the second explains the first.

**F-s2 — mutability**, the fact the census flags as the residue:

| probe | python / java / kotlin / go / dart / ts / php | ruby | cpp | rust |
|---|---|---|---|---|
| a edit through one name, read through the other | `abc` (unchanged) | **`abcd`** | **`abcd`** | **`<compile-error>`** |
| b assign into a position | refused (`<compile-error>`; python `<raise:TypeError>`) | `zbc` | `zbc` | `<compile-error>` |

rust's cell on probe a is the finding worth keeping: the borrow checker
refuses to let a string be edited while a second name is reading it, so rust
does not answer the shared-mutation question at run time — it deletes the
question at build time. php's cell on probe b is the one refutation, §3.

**F-s5 — what `==` does.** Every language answered `true` comparing two
separately-built equal strings, except **java**, which answered `false`.
Comparing a string with itself, java answers `true`. java's `==` is identity,
its `.equals` is content, and both are guarantees — the `.java_equals`
origin-naming ruling has its evidence.

### list — 146 CONFIRMED / 0 REFUTED / 36 SKIPPED

| fact | owner | kind | python | ts | java | csharp | go | rust | rust-rel | ruby | php | kotlin | cpp | dart | dart-web | swift |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| list-U1 append preserves order | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| list-U2 indexed read answers | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| list-U3 iteration in index order | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| list-U4 length counts elements | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l1 what elements may be | structure | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l2 what the container IS | structure | **fracture** | -- | OK | -- | -- | -- | -- | -- | -- | OK | -- | -- | -- | -- | -- |
| F-l3 all growable | structure | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l4 reading past the end | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l5 negative indexing | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l6 what slicing answers | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l7 what `==` does | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l8 sort order and in-place | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-l9 what `b = a` means | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |

F-l2's row is mostly `--` because its two probes exist in one language each by
construction: the sparse hole is a javascript-family fact and the ordered-hash
key exposure is a php fact. Both confirmed: typescript's `[1, , 3]` has length
3 with position 1 ABSENT (`3/false`), and php's array, after deleting the
middle element, reports its keys as `0,2` — a hash, not a renumbered buffer,
the impostor caught in the act.

**F-l4 / F-l5 — reading past the end, and reading backwards:**

| language | `a[10]` | `a[-1]` |
|---|---|---|
| python | `<raise:IndexError>` | `3` (counts from the end) |
| ruby | `nil` | `3` (counts from the end) |
| php | `null` | `null` |
| typescript | `undefined` | `undefined` |
| go | `<raise:runtime error: index out of range [10] with length 3>` | **`<compile-error>`** |
| rust (both) | `<raise:panic>`; `.get(10)` answers `None` | **`<compile-error>`** |
| java / kotlin | `<raise:IndexOutOfBoundsException>` | same |
| dart | `<raise:RangeError>` | same |
| dart-web | `<raise:IndexError>` | same |
| cpp | `0` via `[]` — UNDEFINED, recorded not graded; `.at(10)` throws `<raise:vector::_M_range_check…>` | `0`, undefined |

The census said of negative indexing that everyone outside python and ruby
"refuses or misbehaves". The run separates the refusals into two kinds worth
distinguishing: go and rust refuse at BUILD time (go rejects a constant
negative index; rust indexes by an unsigned type, so a negative index cannot
be written), while java, kotlin and dart refuse at run time and typescript and
php answer their nothing-value. A build-time refusal costs nothing and is
visible to ingress; a run-time refusal is a behaviour that must be preserved.

**F-l6 — slicing**, the sharing question:

| language | edit through the slice, then read the original |
|---|---|
| python / ruby / typescript / kotlin / dart / php / cpp | `1` — the slice was a COPY |
| **go** | `99` — the slice is a WINDOW on shared storage |
| **rust** | `99` — a supervised borrow, same storage |
| **java** | `99` — `subList` is a VIEW; the census does not place java here (§3) |

**F-l7 — `==` between lists:** content in python, ruby, kotlin, rust, php and
cpp; identity (`false`) in java, typescript and dart; and in go a
`<compile-error>` — slices are not comparable at all, which is the census's
third camp confirmed as a build-time fact.

**F-l8 — sort:** every language sorted `[10, 9, 1]` to `1,9,10` except
**typescript**, which produced **`1,10,9`** — the lexicographic default, the
census's "single most surprising guarantee", confirmed. python's `sorted()`
and ruby's `.sort` left the original at `10,9,1`, so the record-both half
holds too: both languages genuinely ship two spellings.

**F-l9 — what `b = a` means:** `99` (shared) in python, ruby, java, kotlin,
dart, typescript and go; `1` (copied) in php and in cpp; and in rust
`<compile-error>` — the move. The rust probe EXPECTED a compile error and got
one, and that is not a failed probe, it is the guarantee: `let b = a` ends
a's usability and the compiler says so.

### dict — 112 CONFIRMED / 0 REFUTED / 28 SKIPPED

| fact | owner | kind | python | ts | java | csharp | go | rust | rust-rel | ruby | php | kotlin | cpp | dart | dart-web | swift |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dict-U1 read by existing key | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| dict-U2 last write wins | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| dict-U3 delete then membership | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| dict-U4 length counts entries | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-d1 what a key may be | structure | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-d2 is iteration order promised | structure | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-d3 reading a missing key | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-d4 deleting while iterating | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |
| F-d5 key-equality fine print | operation | **fracture** | OK | OK | OK | -- | -- | -- | -- | OK | -- | -- | -- | -- | -- | -- |
| F-l9-dict what `b = a` means | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | OK | OK | -- |

**F-d1 — keys.** Setting position `1` and then position `"1"`, and reading
back the integer key: python and ruby answer `int` (two different keys), while
**php** and the **javascript plain object** answer `str` — the string
overwrote the integer, because both coerce. javascript's **Map** answers `int`,
so the split personality the census describes is real and lives inside one
language.

**F-d2 — iteration order.** The insertion-order camp (python, ruby, php,
kotlin, dart both modes, js Map) all answered `z,a,m`. The not-promised camp
answered whatever it liked, and this is where the mode columns pay off a
second time:

| language | order of three keys inserted z, a, m |
|---|---|
| java HashMap | `a,z,m` |
| cpp unordered_map | `a,m,z` |
| **rust (debug)** | `m,a,z` |
| **rust (release)** | `a,m,z` |

Three different orders from three implementations that all promise nothing —
and rust's two build modes disagreeing with each other, in a run forty
milliseconds apart, is the cleanest possible demonstration that "not promised"
means exactly what it says.

**go was probed differently, on purpose.** Its order is not merely unpromised,
it is deliberately randomised, which is an ANTI-guarantee: a promise OF
unpredictability. There is no order to assert, so the probe builds a ten-key
map, iterates it three times INSIDE ONE PROCESS, and asserts that the three
orders DIFFER. go answered **`unstable`**. The census's first anti-guarantee is
verified by the only test that could verify it.

The javascript plain object's weird cousin also confirmed: keys inserted
`b`, `2`, `a`, `1` iterate as **`1,2,b,a`** — integer-like keys first, in
numeric order, then the rest in insertion order.

**F-d3 — reading a missing key**, all four camps:

| camp | language | result |
|---|---|---|
| throw | python | `<raise:KeyError>` |
| throw | rust (indexing) | `<raise:panic>` |
| nothing-value | ruby / typescript / java / kotlin / dart / php | `nil` / `undefined` / `null` / `null` / `null` / `null` |
| zero value plus an ok flag | go | `""/false` |
| **INSERT a default and answer it** | cpp `operator[]` | `""/2` — the map had ONE entry, and reading a key that was not there made it TWO |
| the other spelling | cpp `.at()` | `<raise:map::at>` |
| the other spelling | rust `.get()` | `None` |

cpp's insert-on-read is the strangest guarantee in the census and it is real:
the size is the evidence.

**F-d4 — deleting while iterating:** `<raise:RuntimeError>` in python,
`<raise:ConcurrentModificationException>` in java and kotlin,
`<raise:ConcurrentModificationError>` in dart both modes, `ok` in go, ruby,
php and js Map, `<aborted>` in cpp (the process died — undefined, recorded not
graded), and in **rust a `<compile-error>`**: the borrow rules forbid it before
the program exists.

**F-d5 — key equality:** two objects of equal content are TWO keys in a js Map
(`2`) and ONE key in python, ruby and java (`1`). A NaN key is retrievable in
a js Map (`yes`) and unreachable in python (`<raise:KeyError>`) — stored, but
never findable again.

**F-l9-dict:** the census claims dict inherits list's assignment camps
wholesale. It does, cell for cell: shared in eight languages, copied in php
and cpp, and `<compile-error>` in rust.

## §3 — every refuted cell, diagnosed

Seven cells. Six are dart, one is php. Each is classed as **census wrong**,
**harness wrong**, or **instructive** (the census is right at the level it
meant, and the probe found a different animal).

**(1) F-i4 / dart-native — the sign of modulo.** Expected `-1` (the census
puts dart in the dividend-sign camp); got **`1`**. Probe F-i4.b, `7 % -2`,
answered `1` as censused; only the negative DIVIDEND diverges.
Verdict: **census wrong.** dart's `%` is a Euclidean modulo — the result is
never negative — which is a THIRD camp, not either of the two the census
names. dart's truncating remainder is spelled `.remainder()`, so dart ships
both operations under different names, exactly like division. This is a
guarantee, cheap to honour, and it strengthens rather than threatens the
guarantees rule.

**(2) F-i4 / dart-web.** Same value, same cause. Not a separate finding; the
web mode agrees with native here.

**(3) F-i1 / dart-web — what values an integer holds.** Expected the eroded
float answers (`9007199254740992`, `9223372036854775808`); got
**`<compile-error>`**, twice. The compiler said, verbatim:
`Error: The integer literal 9007199254740993 can't be represented exactly in
JavaScript.`
Verdict: **instructive.** The census says dart-web "behaves as floats", and
the assumption inside that phrase is that it behaves as floats *at run time*.
It does not get that far: dart's web compiler REFUSES a source text merely for
containing an integer literal JavaScript cannot represent. That is a better
guarantee than the census predicted — a silent erosion turned into a loud
refusal — and it is a third example of log 019's compile-time-refusal
category.

**(4) F-i2 / dart-web — overflow.** Expected `9223372036854775808` (float
behaviour); got `<compile-error>`, same cause as (3): the probe has to write
the 64-bit maximum in order to add one to it.
Verdict: **instructive**, same finding as (3). What dart-web overflow does to
a value that is expressible on both sides remains unprobed, and is the one
gap this run leaves — noted in §6.

**(5) F-i5 / dart-web — modulo by zero.** Integer division by zero threw as
censused (`<raise:UnsupportedError>`); `7 % 0` answered **`NaN`**.
Verdict: **census wrong, narrowly.** The census's F-i5 says dart throws, and
dart-native does throw for both. On the web the modulo falls through to the
JavaScript `%`, which answers NaN rather than refusing. So dart's two modes
disagree about modulo-by-zero and agree about division-by-zero — a fine
distinction, and precisely the kind of thing the record-both-modes ruling
exists to catch.

**(6) F-i6 / dart-web — bit ops.** Expected `4294967296` for `1 << 32`; got
**`0`**.
Verdict: **census wrong.** F-i6 places dart(native) on the declared width and
says nothing about dart-web. Measured, dart-web's shift is the JavaScript
32-bit shift: `1 << 31` gives 2147483648 (so it is not simply typescript's
answer either), and `1 << 32` gives 0. dart-web therefore belongs in its own
row of F-i6, agreeing with neither the declared-width camp nor typescript.

**(7) F-s2 / php — mutability.** The census files php under "immutable value
(value semantics via copy-on-write)". The probe assigned into a position:
`$s[0] = "z"` on `"abc"` gave **`zbc`**.
Verdict: **census wrong on one half.** php is genuinely a copy-on-assign
value type — probe a confirmed it, the alias saw `abc` — but a php string is
mutable IN PLACE through its own name. So php's guarantee is: value semantics
between names, mutation within a name. That is a fourth position on F-s2, and
because it is observable, it belongs on the page.

### proposed corrections, for the owner

None applied. The census pages are untouched.

1. **census_integer.md, F-i4** — add a THIRD camp: **result is never negative
   (Euclidean)**: dart, both modes. Measured: `-7 % 2` is `1`, `7 % -2` is `1`.
   Note beside it that dart's truncating remainder is spelled
   `.remainder()`, so dart ships both operations and the origin-naming rule
   applies unchanged.
2. **census_integer.md, F-i4** — place **php** in the dividend-sign camp,
   where it is currently absent. Measured: `-7 % 2` is `-1`, `7 % -2` is `1`.
3. **census_integer.md, F-i2 and F-i1** — add to the dart-web entries that the
   web compiler REFUSES a source containing an integer literal JavaScript
   cannot represent, rather than eroding it at run time. The census's "behaves
   as floats" is true of arithmetic, not of literals.
4. **census_integer.md, F-i5** — split dart: division by zero throws in BOTH
   modes; modulo by zero throws natively and answers `NaN` on the web.
5. **census_integer.md, F-i6** — give **dart-web** its own row: the JavaScript
   32-bit shift (`1 << 31` is 2147483648, `1 << 32` is 0), which matches
   neither the declared-width camp nor typescript.
6. **census_string.md, F-s2** — move **php** out of the immutable-value camp
   into a fourth position: **value semantics between names, mutable in place
   through one name**. Both halves measured.
7. **census_string.md, F-s1 and F-s3** — place **ruby**, currently unplaced,
   in the CODEPOINT camp with python. Measured: length of "é" is 1, of "𝄞"
   is 1, of the pair is 2; the first unit of "𝄞" is 119070.
8. **census_list.md, F-l6** — place **java**, currently unplaced, in the
   WINDOW camp: `subList` is a view, and editing through it is visible in the
   original (measured `99`). Also place **php** and **cpp** in the COPY camp
   (both measured `1`).
9. **census_list.md, F-l7 and F-l9** — place **cpp**, currently unplaced:
   `==` on vectors compares CONTENT (measured `true`), and `b = a` COPIES
   (measured `1`), which puts cpp beside php on assignment rather than beside
   the sharing camp. The same cpp placement carries to dict's F-l9-dict.
10. **A standing-rules addition, if the owner agrees.** log 019 §3 proposed
    compile-time refusal as a third result category beside "answers" and
    "raises". This run turned that from a curiosity into a workhorse: **34 of the
    results recorded here are build-time refusals**, and in six places the refusal
    IS the census's stated guarantee (rust's move, rust's borrow-during-edit,
    rust's string indexing, go's slice `==`, go's constant negative index, and
    every declared-element-type violation). Recommend the category be named
    and the census pages be allowed to say "refuses at build time" as a
    first-class camp answer.
11. **A scope note, not a correction.** dart-web is now a real column. The
    census pages mention dart's two modes only inside F-i2; on the evidence
    here the modes also diverge on F-i5 and F-i6. Suggest the mode annotation
    the integer page asks for (its own "format finding for the owner") be applied
    per-fact rather than per-language.

## §4 — the mode columns

Two languages ran twice. Both earned it.

**rust debug versus rust release — the headline.** Same source file, two
compiler invocations, and one genuine disagreement:

| fact | probe | rust (debug) | rust (release) |
|---|---|---|---|
| F-i2 | `i64::MAX + 1` | **`<raise:panic>`** | **`-9223372036854775808`** |
| F-i2 | `i64::MAX.wrapping_add(1)` | `-9223372036854775808` | `-9223372036854775808` |
| F-i2 | `u64::MAX + 1` (unsigned) | `0` | `0` |
| F-d2 | iteration order of z, a, m | `m,a,z` | `a,m,z` |
| everything else, 40 facts | — | identical | identical |

This is the record-both-modes ruling justified in one row. rust's `+` on
integers does not make a portable promise: it panics or it wraps, depending
how the program was built, and both behaviours are correct rust. Two
consequences follow directly for the Hub. First, the guarantees rule needs the
DEFAULT rust add to be modelled as its own thing — "checked in debug, wrapping
in release" — rather than being filed under either wrap or grow. Second,
`wrapping_add` is the operation a rust source uses when it MEANS wrapping, and
it is stable across modes, so ingress reading `wrapping_add` learns something
that ingress reading `+` does not. The F-d2 row is a bonus: two build modes
disagreeing about a map's iteration order is what "explicitly not promised"
looks like when you actually check.

**dart native versus dart web.** Both modes ran, and they diverge on four of
the nine integer facts:

| fact | probe | dart-native | dart-web |
|---|---|---|---|
| F-i1 | 2^53+1 as a literal | `9007199254740993` | `<compile-error>` |
| F-i1 | 2^63-1 as a literal | `9223372036854775807` | `<compile-error>` |
| F-i2 | largest plus one | `-9223372036854775808` (wraps) | `<compile-error>` |
| F-i5 | `7 % 0` | `<raise:IntegerDivisionByZeroException>` | `NaN` |
| F-i6 | `1 << 32` | `4294967296` | `0` |
| F-i5 | `7 ~/ 0` | `<raise:IntegerDivisionByZeroException>` | `<raise:UnsupportedError>` |
| string, list, dict — all 32 facts | — | identical | identical |

Two readings. The narrow one: dart's integer is a different structure on the
web, and the census was right to flag it, though wrong about the mechanism —
the divergence starts at COMPILE time, not at run time. The broad one, which
matters more for the Hub: **the divergence is confined entirely to the integer
page.** dart's strings, lists and dicts behave identically in both modes, all
32 facts. Mode-dependence is not a property of a language; it is a property of
a language-and-object pair, and so far only one pair has it.

## §5 — harness state after this run

The pipeline is unchanged in shape and is now proven on five pages:
`vectors_<object>.json` → `generate_run.py` → one lane script → `results/` →
`compare.py` → `verified_<object>.json`. What this run added, all of it
reusable:

- **Per-language probe text.** A probe's `expr` may be a mapping from language
  to that language's own code, and where a body needs statements rather than
  an expression it lives in `templates/<lang>.<object>.pre` as a named
  function, with the vector carrying only the call. 40 such preamble files
  exist now, one per language per object, plus 24 small per-PROGRAM ones.
- **Build separated from run.** A program the compiler refused records
  `<compile-error>`; a program that built and then died records `<aborted>`.
  Before this, a c++ probe that killed the process was mislabelled a compile
  error.
- **Per-program preambles.** A preamble is pasted into every program a
  language runs, and dart's web compiler refuses a source text merely for
  CONTAINING an unrepresentable literal — so a body that cannot compile is
  parked in the one program that needs it, keeping the refusal where the
  finding is.
- **Two expectation spellings that carry rulings.** `<any>` means no answer
  can be wrong (c++'s undefined behaviour, and the record-not-check policy for
  cells the census never placed); `<raise:*>` means "must refuse at run time,
  by any name", with the exact exception name preserved in `results/` and
  quoted in this log rather than pinned in the vectors.
- **Mode columns do not inherit.** compare.py now looks up a mode column's
  expectation by its EXACT name and never falls back to the base language.
  This was a real bug caught mid-run: rust-release was inheriting rust's
  panic expectation, which would have erased the headline finding of §4.
- **Two template fixes.** The c++ probe pattern now computes the value BEFORE
  printing the label, so a thrown exception cannot leave a half-written line
  (it did, once, on `vector.at`). The rust probe pattern now catches panics
  with `catch_unwind` and a silenced hook, so a panicking probe records
  `<raise:panic>` instead of taking every later probe in its program down.

**What the next object would cost.** Adding one more object is: one
`vectors_<object>.json`, ten preamble files (one per active source language),
and one lane run. No changes to `generate_run.py`, `compare.py`, the runner
templates or the probe patterns — the four pages here needed none after the
first day's fixes. Budget roughly the writing time for ten short source files;
the machine time is free.

**Machine time is emphatically not a constraint.** The four runs took 15.4,
12.3, 24.4 and 17.9 seconds — **70 seconds** for 715 probe results across 12
language runs each. kotlinc, budgeted at a minute per compile, is invisible in
that total. Disk cost was 103 MB of scratch. The lane's serial discipline was
respected throughout: one script in flight at a time, six scripts total
(two dart installs, four census runs), plus two discarded first attempts whose
failures are themselves recorded above.

**Coverage, honestly stated.** 41 facts across four pages, all structure and
operation facts, no border facts. 12 language runs against 14 census columns:
c# is blocked-deliberate (no toolchain, not pursued) and swift was not run on
these pages (a bonus language outside the census's targets; running it would
have added informational cells and no census evidence). Those two account for
every one of the 100 skipped cells except the ones where a probe genuinely
does not exist in a language — F-l2's two single-language probes and F-d5's
key-equality corner, which are skipped by construction and not by absence.

## §6 — open items for the owner

1. **The eleven proposed corrections in §3.** Nothing has been written to a
   census page. Items 1–9 are camp placements with measured evidence; item 10
   is the standing-rules addition (compile-time refusal as a first-class camp
   answer, now supported by 34 build-time refusals rather than the two log 019
   had); item 11 is the mode-annotation format question the integer page
   itself raised.
2. **log 019 §3 is still unruled** — whether typescript's refusal to compare
   two bool literals joins boolean's border list. This run found the same
   shape repeatedly, so the answer generalises.
3. **The one gap this run leaves.** dart-web's overflow BEHAVIOUR is unmeasured,
   because the probe cannot be written: expressing "the largest integer" is
   what the web compiler refuses. Measuring it needs a value reachable by
   arithmetic rather than by literal. Worth a small follow-up if the dart-web
   column is to be complete; not worth a run on its own.
4. **rust's default add needs a name.** §4 shows it is neither the wrapping
   guarantee nor the growing one. If the Hub carries wrapping-add and
   growing-add as two operations per the overflow ruling, rust's bare `+` maps
   to neither cleanly, and the honest ingress reading of it is "the developer
   did not choose". the owner's call whether that is a third modelled operation, a
   flag on the ledger entry, or an ingress warning of the flag-if-unhandled
   kind the integer page already floats for c++.
5. **The residue check.** After six objects and 574 verified cells, the
   genuinely-hard residue is still EMPTY. Every fracture measured on these
   four pages is a guarantee, an anti-guarantee (go's randomisation, verified
   as unstable), or a build-time refusal — and each of those is computable
   from a faithful representation. The two hard cases the census named remain
   closed by the owner's rulings, and nothing new joined them. The phase-2
   conclusion the dict page drafted survives contact with execution.

6. **A tiny housekeeping item, incurred not chosen.** `hq.sh check` was
   carrying 2 pre-existing errors when this run began, both against
   `SUPPORT_BRAINSTORM_basis_data_structures.md` in this node's planning
   folder: no frontmatter id, and not listed in the CORE. Both are fixed
   (the file now carries an id, and the CORE has a `## support` section
   naming it), and the check is back to **0 errors, 8 warnings**. The
   framework requires a SUPPORT file's id suffix to match its filename
   exactly, so the id reads
   `hq.research.dominant_intentions.support.BRAINSTORM_basis_data_structures`,
   with an uppercase segment. Renaming the file to
   `SUPPORT_basis_data_structures.md` would read better, but a file name is
   a naming decision and those are the owner's — flagged, not taken.

### artifacts

- `Research/dominant_intentions/harness/vectors_integer.json`,
  `vectors_string.json`, `vectors_list.json`, `vectors_dict.json`
- `Research/dominant_intentions/harness/templates/` — 11 runner templates
  (dart is new), 64 preamble files
- `Research/dominant_intentions/harness/generate_run.py` (extended),
  `compare.py` (extended)
- `Research/dominant_intentions/harness/lane_int.sh`, `lane_str.sh`,
  `lane_lst.sh`, `lane_dct.sh` (generated)
- `Research/dominant_intentions/harness/results/` — 48 raw result files, the
  evidence
- `Research/dominant_intentions/verified/verified_integer.json`,
  `verified_string.json`, `verified_list.json`, `verified_dict.json`
- lane logs in `SandboxDesign/agent/logs/`:
  `…__dart_install.sh.log`, `…__dart_web_check.sh.log`,
  `…__census_int2.sh.log`, `…__census_str.sh.log`, `…__census_lst2.sh.log`,
  `…__census_dct.sh.log`

## postscript, 2026-08-14 — the dart-web overflow follow-up (§6 item 3, closed)

the owner ruled the eleven §3 corrections, the log 019 §3 typescript border fact,
and the name `unspecified` for rust's bare-add non-choice; all applied to the
census pages the same day. That ruling pass also asked for §6 item 3's one
open gap to be closed: dart-web's overflow BEHAVIOUR was unmeasured because
the probe could not be written without a literal the web compiler refuses.

A small lane script, `dartweb_overflow.sh`, reached the 64-bit maximum by
arithmetic instead: `x = 1`, doubled 63 times (`x = x * 2` in a loop, never a
literal), then `maxVal = x - 1`. That value is never written as a literal
anywhere in the source, so the compiler had nothing to refuse.

**Result:** `maxVal` prints as `9223372036854776000`; `maxVal + 1` prints the
identical `9223372036854776000` (the double's own precision gap swallows the
+1); `maxVal + x` (adding another 2^63) prints `18446744073709552000`. No
throw, no wrap, no compile-error — silent float erosion the whole way, exactly
what the census's original "dart-web behaves as floats" claim predicted. The
`<compile-error>` findings this run recorded earlier (§3 items (3) and (4))
were about LITERALS the web compiler cannot represent; they said nothing
about what overflow itself does once a value is safely in hand, and now that
gap is measured too. Recorded on `census_integer.md`'s F-i2 dart-web entry
with provenance; the §6 item 3 gap is closed.
