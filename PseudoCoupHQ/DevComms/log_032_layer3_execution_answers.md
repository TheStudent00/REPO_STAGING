# log 032 — layer 3, EXECUTION: what the accepted operations return

Date: 2026-08-19. Node:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

Log number: **032**. Log 031 was taken by the agent working the
answer-grain clustering for python, ruby and php the same day; this log
takes the next free number after it and does not touch its files.

**Rewritten 2026-08-19 for readability at the owner's instruction. The content
is identical — same facts, same numbers, same findings, same section
numbers. Only the prose was rebuilt.**

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

This log closes CHECK item **3k** for all nine statically checked
languages and gives phase 4's item **4i** its first material outside
python, ruby and php.

---

## words used in this log

This node has built up a set of short words for its own parts. Every
one of them is defined here, with an example taken from this log rather
than a made-up one. Nothing below this block uses a word that is not
either ordinary English or defined here.

```
probe
    one small generated program that asks one
    language one question: what does this
    operation do to these two values.
    example tied to context:
        this pass ran 170,419 probes across
        nine languages.

lane
    one batch job. it runs a planned set of
    probes and writes its output to one raw
    text file. a lane has a short name.
    example tied to context:
        `ex_kotlin_r1.sh` is the lane whose
        output became `answers_kotlin.json`.

chunk
    one generated source file inside a lane,
    holding a run of probes, compiled once
    and run once.
    example tied to context:
        c++ ran 14 chunks of 2000 probes;
        swift ran 7 chunks of 400.

dispatch table
    the code inside a chunk that turns a
    probe number into the probe's own body.
    example tied to context:
        go uses an array of `func()`; java,
        kotlin and c-sharp use a two-level
        switch, because those three cap a
        method at 64 KB.

value matrix
    the earlier product of this node: for one
    language, every operation crossed with
    every pair of holders and every pair of
    values, each carrying a verdict.
    example tied to context:
        the 170,419 accepted probes this pass
        ran were read out of the nine value
        matrices, cell by cell.

manifest
    a frozen file listing what was probed for
    one language: its holders, its value
    classes, its operation list. it decodes a
    probe id back into an operation and two
    operands.
    example tied to context:
        the manifests are what let an
        accepted probe be re-emitted without
        re-deriving anything.

the accepted set
    the probes of one language that the value
    matrix already recorded as ACCEPT. this
    pass runs exactly those and no others.
    example tied to context:
        swift's accepted set is 2,618 probes;
        c++'s is 27,385.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        `int32` in go and `int32_t` in c++
        are two holders; §5's first surprise
        puts `42 << 42` on both.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        `i64max` is a value class: the
        largest signed 64-bit integer. §5's
        second surprise uses it.

cell
    one combination of operand kinds that an
    operation was asked about.
    example tied to context:
        `int64_t + const char*` is one c++
        cell, and §5's sixth surprise is
        about it.

ACCEPT, REFUSE
    the two verdicts a checking run gives a
    probe. ACCEPT means the compiler took the
    expression; REFUSE means it did not.
    example tied to context:
        every verdict-grain pass in this node
        calls §5's first surprise a single
        uniform ACCEPT cell, for all seven
        languages that spell it.

verdict grain, answer grain
    two depths of measurement. the verdict
    grain records only whether the compiler
    accepted a probe. the answer grain
    records what the accepted probe returned.
    example tied to context:
        two and a quarter million verdicts
        existed before this log; this log is
        the node's first answer-grain
        material outside python, ruby and
        php.

route A, route C
    two ways a language is measured. route A
    is check-only: a probe gets a verdict and
    needs a second run to get an answer.
    route C is compile-and-run: acceptance
    and answer arrive together.
    example tied to context:
        route C is what log 028 left unbuilt
        for the nine statically checked
        languages, and it is what this log
        builds.

raise
    the language throwing something the probe
    can catch in-language, so the probe still
    yields a line.
    example tied to context:
        rust's `panic` on `i64max + 42` is a
        raise; there were 471 of them in
        rust.

death
    the process ending on the spot, with
    nothing catchable. the runner records the
    probe that died and restarts.
    example tied to context:
        c++'s `SIGFPE` on integer division
        by zero is a death; c++ had 480.

CODEGEN_REFUSE
    the compiler accepted a probe when
    checking types but refused it when
    generating machine code. the probe
    produces no answer.
    example tied to context:
        1,066 of swift's 2,618 accepted
        probes are codegen refusals.

the start index
    the one argument every chunk binary
    takes: the probe number to begin at. it
    is what makes a death cost one probe
    instead of a whole chunk.
    example tied to context:
        c++'s worst chunk was restarted 108
        times and finished.

the stall watchdog
    a timer that treats ninety seconds of
    silence from a chunk as a death of the
    probe that was next, so the runner can
    resume past it.
    example tied to context:
        it exists because kotlin's `..` can
        hand back a range over every 64-bit
        number, and a recorder that walks it
        never comes back.

the `// __PROBE__` marker
    a comment written above each probe
    function, carrying that probe's id.
    example tied to context:
        it is how a line number the compiler
        complains about is mapped back to the
        probe that owns the line.

the repair step
    what the driver does when a chunk fails
    to compile: map the named lines to
    probes through their markers, drop
    exactly those probes as CODEGEN_REFUSE,
    and rebuild.
    example tied to context:
        it attributed swift's 1,066 codegen
        refusals one by one instead of losing
        seven chunks.

completeness gate
    a check run after a lane is folded. it
    compares the row count against the
    accepted count the value matrix recorded,
    and requires every accepted id present
    exactly once.
    example tied to context:
        all nine languages pass it, with zero
        missing and zero build failures.

the answers encoding
    the rule for writing down what a probe
    returned: the language's own type name,
    then the result's raw content as bits.
    it lives in one file, and §3 summarises
    it.
    example tied to context:
        `INT:64:8000000000000029` is one
        encoded answer: a 64-bit integer,
        written as eight two's complement
        bytes.

quarantine
    a lane that ran but is not the product,
    kept on disk with the reason recorded.
    example tied to context:
        kotlin ran three times and the first
        two runs are quarantined.

`HARVEST.md`
    the file in
        `~/Programming/PseudoCoupHQ/Research/
        kind_fuzz_clustering/`
    that carries what has run, what is
    running, and what is still to be built.
    example tied to context:
        it is where the state and the two
        kotlin quarantines are recorded.

CHECK item (item 3k, item 4i)
    a numbered piece of work the node's
    planning files track by number.
    example tied to context:
        item 3k is the execution evidence
        this log closes; item 4i is the
        answer-grain clustering it feeds.
```

---

## what came before this log, restated

Each fact this log borrows from an earlier log is stated here in full,
so no sentence below depends on opening another file.

- **Log 025 measured what one probe costs.** Its amortised per-probe
  acceptance rates are cpp 60.9 ms, kotlin 52.1 ms, swift 42.5 ms and
  go 17.4 ms. §4 compares this pass's per-probe cost against those four
  numbers.
- **Log 027 built and ran phase 3**, the per-probe acceptance work that
  the value matrices were later built on top of.
- **Log 028 closed phase 3 and built the value matrix.** It is also the
  log that left route C — compile-and-run — unbuilt, because compiling
  two hundred thousand programs one at a time was judged too expensive.
  This log is the pass that builds it.
- **Log 029 froze the manifests.** A raw result line from this node is
  positional: `P7_10_1_3_2` means holder 7 on the left, holder 10 on
  the right, that holder's value class 1, this one's value class 3,
  operation 2 — and it names none of those things itself. The twelve
  `manifest_<lang>.json` files are the written-down lists that decode
  it. This pass relies on them to turn an accepted probe id back into
  an operation and two operands.
- **Log 030 recorded the dart severity fault**, and §5's fifth surprise
  compares itself to it. The dart lane ran `dart analyze <dir>` and
  marked a probe REFUSED if the probe's filename appeared anywhere in
  the output, at any severity. `dart analyze` reports `dead_code` on
  the right operand of `true || b`, so a short-circuit lint was being
  read as a type refusal. The fix reads `--format=machine` and counts
  only severity ERROR. The shape of the fault is the point: the
  instrument was answering a slightly different question than the one
  being asked.
- **Log 030 also measured value-dependence in the acceptance grain**,
  which is the background to §5's first surprise: a verdict-grain pass
  can call a cell uniform when the language's behaviour inside that
  cell is not uniform at all.
- **Log 031 built the answer-grain clustering machinery for python,
  ruby and php**, the three languages this node runs directly rather
  than compiles. It was written the same day as this log, by a
  different agent, and this log does not touch its files.
- **`HARVEST.md` already flagged dart's `dynamic` operands.** 388 of
  dart's acceptance-grain accepts carry a `dynamic` operand, where
  dart's checker is switched off and the real verdict is deferred to
  run time. §5's seventh surprise is where that deferred verdict
  arrives.
- **the owner's ruling of 2026-08-18 authorised this pass**, by removing the
  cost objection log 028 recorded. §1 states the ruling and what it
  changed.

---

## §1 — walkthrough, in plain words

Everything this node has measured for the nine statically checked
languages has been a **verdict**: does the compiler accept this
expression. Two and a quarter million probes' worth of verdicts, and
not one **answer** — not one record of what an accepted operation
actually returns. Route C, compile-and-run, was the missing half. Log
028 left it unbuilt because running two hundred thousand programs one
at a time is the cost that killed the idea.

the owner's ruling of 2026-08-18 removed the cost. We already know which
probes compile: the value matrices say so, cell by cell, and the
manifests decode every probe id back into its operation and its two
operands. So the accepted probes can be emitted **into one file each**,
compiled once, and run once. No compile failure is possible by
construction, and there is nothing to bisect. That is the whole design.

It worked, and the size of the saving is the first thing worth saying.
There are **170,419 accepted probes across the nine languages**
*(derived from the value matrices)*. All nine ran to completion in this
session: **170,419 probes, 162,853 answers, 297.5 seconds of wall time
in total** *(measured)*. The acceptance runs that produced the verdicts
for those same nine languages cost hours. Collapsing the compile from
one-per-probe to one-per-chunk is worth roughly three orders of
magnitude. It is worth that much precisely because the accepted subset
is small — between 1 and 20 percent of each language's matrix.

The second thing worth saying is that **the answers are recorded as
bits, not as printed text**. the owner's question was "why wouldn't we get
all their bits, and the type info?", and the answer is that there is no
reason not to. Every row carries the language's own name for the result
type and the result's raw content: integers as two's complement bytes,
floats as their IEEE bit pattern, text as its byte length plus its
UTF-8 bytes plus the language's own idea of "length", containers
recursively in the same encoding. Nothing is canonicalised while the
probe runs. Comparison happens later, over the recorded bits, and it is
mechanical. `answers_encoding.md` is the one place that rule lives.

The third thing is a design element that was not planned and turned out
to matter. **A runtime death does not have to cost a chunk.** The two
cases are different and are handled differently.

- **Where the language can catch a raise in-language**, each probe is
  wrapped in the language's own catch and every probe yields a line.
  Go's `recover` in a `defer` is this case.
- **Where the language cannot**, there is nothing to wrap with. C++
  takes `SIGFPE` on integer division by zero and there is no catching
  that. So the chunk binary takes a **start index**, and the runner
  records a death for the probe that died and restarts the binary at
  the next one.

C++ lost **480 probes to death and no chunk at all** *(measured)*; one
chunk restarted 108 times and finished.

The fourth thing was not planned either, and it is a finding rather
than an engineering note. **Swift accepts, at type-check time, code
that swift refuses at compile time.** `swiftc -typecheck` — the
instrument every swift verdict in this node was taken with — accepts
`let b: Int = 9223372036854775808`. Full compilation of the same line
says `integer literal '9223372036854775808' overflows when stored into
'Int'`. **1,066 of swift's 2,618 accepted probes, 40.7 percent, are
refused by the compiler that accepted them** *(measured)*. They are
recorded as `CODEGEN_REFUSE` with the compiler's own message, not
quietly dropped and not counted as answers. No other language showed
this: the other eight recorded zero codegen refusals.

The headline, though, is what the answers say when you line the
languages up on one expression. `42 << 42`, both operands a 32-bit
signed holder, is accepted by seven of the eight languages that spell
it at all, and they return **five different things**: go 0, c++ and
java and c-sharp 43008, typescript 43008 as a float64, dart 43008
shifted inside 64 bits, and rust panics *(measured)*. One expression,
seven acceptances, five answers. Every verdict-grain pass in this node
would have called that a single uniform ACCEPT cell.

---

## §2 — the design as built, per language

The rule was: emit only the known-accepted probes, all of them in one
file per language. Chunk only where a runtime death cannot be caught in
the language, or where the compiler's own habits make one enormous file
a bad bet.

Three things pushed chunk sizes down from "one file per language".

- **Swift's type checker is superlinear in a file's size.** A bigger
  file costs more than proportionally more.
- **Java, kotlin and c-sharp cap a method at 64 KB.** That is why the
  dispatch table in those three is a two-level switch over
  hundred-case helpers, rather than an array of lambdas.
- **Where death is uncatchable, the chunk is the blast radius of one
  restart.** Smaller is cheaper.

| language | catches its own deaths | probes per chunk | chunks | dispatch |
|---|---|---|---|---|
| go | yes, `recover` in a `defer` per probe | 1500 | 2 | array of `func()` |
| rust | yes, `catch_unwind` per probe, panic hook silenced | 1500 | 3 | vec of `fn()` |
| c++ | `catch (...)` only; `SIGFPE` and `SIGSEGV` are not catchable | 2000 | 14 | array of function pointers |
| java | yes, `catch (Throwable)` per probe | 2000 | 7 | two-level switch |
| c-sharp | yes, `catch (Exception)` per probe | 2000 | 8 | two-level switch |
| typescript | yes, `try/catch` per probe | 5000 | 9 | array of closures |
| swift | no — a trap is not catchable, `do/catch` sees thrown errors only | 400 | 7 | array of closures |
| kotlin | yes, `catch (Throwable)` per probe | 2000 | 18 | two-level switch |
| dart | yes, `catch (e)` per probe | 3000 | 9 | list of closures |

Four mechanisms carry the design.

**The start index.** Every chunk binary takes one argument, the probe
number to start at. The runner reads its lines. If the process ends
before the last probe, the runner writes `DEATH` for the next unemitted
probe and runs the binary again from the one after that. A death costs
one probe. The cap is 400 restarts per chunk; c++'s worst chunk used
108 *(measured)*.

**The stall watchdog.** A probe can hang rather than die. Kotlin's `..`
returns a `LongRange`, a `LongRange` **is** an `Iterable`, and a
recorder that walks iterables walks `0..Long.MAX_VALUE` and does not
come back. Ninety seconds of silence is now treated as a death of the
probe that was next, and the runner resumes past it. The recorder was
also fixed to test for ranges **before** iterables and to truncate any
container past a thousand elements *(measured, found by the first
kotlin lane taking 126 s for its first chunk against 8.6 s of
compile)*.

**The `// __PROBE__` marker and the repair step.** Each probe function
is preceded by a `// __PROBE__ <id>` comment. If a chunk fails to
compile, the driver maps every line number the compiler names back to a
probe through those markers, drops exactly those probes, records them
as `CODEGEN_REFUSE` with the message, and rebuilds. That is not a
bisect — the compiler names the line itself. It is what let swift's
1,066 codegen refusals be attributed one by one instead of losing seven
chunks. Sixteen attempts maximum; swift never needed more than one per
chunk *(measured)*.

**Two allowed lints in rust, and only two.** `unconditional_panic` and
`arithmetic_overflow` are deny-by-default lints that fire once const
propagation runs, which is after the `--emit=metadata` stage every rust
verdict in this node was taken at. They are allowed in the execution
build. The panic still happens at run time and is still caught and
recorded as a raise — 471 of them *(measured)*.

The probe body itself is the value matrix's own construction rule,
copied unchanged, because these probes were accepted under exactly it:
the same `v`-to-`a`/`b` rename, the same java `_b` suffix on the
right-hand side's declared types, the same per-language filter on which
`pre` lines survive. Only the wrapper changed. Holder `pre` lines are
hoisted to file scope and deduplicated, with import-like lines sorted
ahead of declarations for java, kotlin, c-sharp and dart, and go's
imports merged into one block because go refuses a package imported
twice.

---

## §3 — the encoding, in summary

The full rule is in
`Research/kind_fuzz_clustering/answers_encoding.md`. One line per
probe, in one of four shapes:

```
PROBE_ID|TYPE_NAME|ENCODING:PAYLOAD
PROBE_ID|-|RAISE:<name>
PROBE_ID|-|DEATH:<rc>
PROBE_ID|-|CODEGEN_REFUSE:<message>
```

`PROBE_ID` is the value matrix's own `P<i>_<j>_<x>_<y>_<k>`, so an
answer row joins to its verdict row by id and nothing is re-derived.

| token | payload |
|---|---|
| `INT:<bits>:<hex>` | two's complement, big-endian, `bits/4` digits |
| `UINT:<bits>:<hex>` | unsigned, big-endian |
| `BIGINT:<hex>` | arbitrary width |
| `FLOAT:<bits>:<hex>` | the IEEE 754 bit pattern, big-endian |
| `DEC128:<hex>` | c-sharp `decimal`, its four words |
| `BOOL:true` or `BOOL:false` | canonical token |
| `CHAR:<hex>` | code unit or scalar value |
| `STR:<own len>:<utf8 bytes>:<hex>` | both length notions, then the bytes |
| `NULL`, `UNDEFINED`, `UNIT` | canonical tokens |
| `SOME(<enc>)`, `REF(<enc>)`, `PTR` | optionals, go references, opaque pointers |
| `LIST:<n>[…]`, `MAP:<n>[…]` | containers, recursive |
| `TUP:<n>[…]`, `STRUCT:<n>[…]` | tuples, fields in declaration order |
| `RANGE[<enc>,<enc>,incl]` | rust and kotlin ranges |
| `ORD:LT\|EQ\|GT\|UN` | c++ `<=>` |
| `OPAQUE:<hex>` | UTF-8 of the language's own `toString`, last resort |

Two recording choices are surfaced rather than buried.

- **Map entries are sorted by their encoded text.** Several of these
  languages' maps have no order of their own. This is the one place the
  recorder imposes an order.
- **`STR` carries two lengths on purpose.** Java, kotlin, c-sharp,
  typescript and dart count UTF-16 code units. Go counts bytes. Rust
  and swift count scalar values. A text answer is not comparable across
  languages without both numbers.

The type name is the language's own, and it is the **static** type
wherever the language will give one: go's `reflect.TypeOf`, rust's
`type_name::<T>`, a c++ template parameter, swift's and dart's and
c-sharp's generic type argument, and for java and kotlin an overload
set over the eight primitives plus `Object`, so that `int` does not
arrive as `Integer`. Typescript is the exception, and it is a fact
about the language: its static types are erased before run time, so
what is recorded is `typeof` and the constructor name.

---

## §4 — results

All nine complete.

| language | probes | answers | raises | deaths | codegen refuse | complete |
|---|---|---|---|---|---|---|
| go | 2806 | 2774 | 32 | 0 | 0 | yes |
| rust | 4263 | 3792 | 471 | 0 | 0 | yes |
| c++ | 27385 | 26905 | 0 | 480 | 0 | yes |
| java | 12841 | 12349 | 492 | 0 | 0 | yes |
| c-sharp | 14852 | 14636 | 216 | 0 | 0 | yes |
| typescript | 44550 | 43030 | 1520 | 0 | 0 | yes |
| swift | 2618 | 1552 | 0 | 0 | 1066 | yes |
| kotlin | 34653 | 33203 | 1450 | 0 | 0 | yes |
| dart | 26451 | 24612 | 1839 | 0 | 0 | yes |
| **nine** | **170419** | **162853** | **6020** | **480** | **1066** | **9 of 9** |

Every one passes the completeness gate: row count equals the accepted
count the value matrix recorded, every accepted id present exactly
once, `__SUMMARY__` present, zero missing, zero build failures
*(measured)*.

Cost. The lane's own wall time, and the share of it that was
compilation:

| language | wall time s | compile time s | ms per probe |
|---|---|---|---|
| go | 0.8 | 0.8 | 0.29 |
| rust | 1.3 | 1.2 | 0.30 |
| java | 7.7 | 7.1 | 0.60 |
| c-sharp | 11.3 | 10.6 | 0.76 |
| typescript | 10.7 | 9.2 | 0.24 |
| swift | 7.9 | 7.8 | 3.02 |
| dart | 19.1 | 18.7 | 0.72 |
| c++ | 44.7 | 13.7 | 1.63 |
| kotlin | 194.0 | 193.2 | 5.60 |

Compilation is **the** cost in eight of nine. Only c++ spends more time
running than compiling, and that is the 480 deaths and their restarts
*(derived)*. Log 025 measured amortised per-probe acceptance rates of
cpp 60.9 ms, kotlin 52.1, swift 42.5 and go 17.4. Against those, the
execution rate is between 6x and 200x cheaper per probe, on top of
asking a harder question.

What comes back. Distinct result types and the three commonest:

| language | distinct result types | distinct encodings | top three result types |
|---|---|---|---|
| go | 8 | 5 | bool 1322, uint64 504, int64 264 |
| rust | 40 | 15 | bool 2158, i128 371, u64 325 |
| c++ | 14 | 8 | bool 15112, __int128 2408, unsigned long 1856 |
| java | 6 | 4 | boolean 6232, String 1701, long 1512 |
| c-sharp | 43 | 10 | Boolean 6736, BigInteger 1598, String 1582 |
| typescript | 18 | 9 | boolean 11938, Array 5920, Object 5920 |
| swift | 7 | 4 | Bool 1442, Double 36, Float 36 |
| kotlin | 466 | 10 | Boolean 13870, ArrayList 3388, LinkedHashMap 2162 |
| dart | 75 | 9 | bool 12309, Object 8030, double 1444 |

And what is returned instead of an answer:

| language | the three commonest non-answers |
|---|---|
| go | integer divide by zero 32 |
| rust | panic 471 |
| c++ | DEATH rc-8 318, DEATH rc-11 162 |
| java | NullPointerException 200, NumberFormatException 152, ArithmeticException 140 |
| c-sharp | DivideByZeroException 216 |
| typescript | SyntaxError 1468, RangeError 52 |
| swift | codegen overflow 1032, codegen other 34 |
| kotlin | NumberFormatException 1326, NullPointerException 68, ArithmeticException 56 |
| dart | NoSuchMethodError 1313, _TypeError 294, UnsupportedError 192 |

One caveat, stated rather than hidden: **a raise can come from the
declaration and not from the operation**, because both sit inside the
same guarded block. Typescript's 1,468 `SyntaxError` raises are all of
that kind, from a `BigInt64Array` holder's declaration *(measured)*.
Separating declaration raises from operation raises needs a second
guarded block and is not built.

Products, all in `Research/kind_fuzz_clustering/`:
`answers_<lang>.json` per language with self-describing rows,
`answers_index.json`, `answers_encoding.md`, `exec_plan.json`, the raw
lane output in `raw/ex_<lang>_00.txt`, the generators `l3_exec.py`,
`l3_exec_lanes.py` and the reader `l3_exec_read.py`.

---

## §5 — surprises

**One. `42 << 42` on a 32-bit signed holder: seven acceptances, five
answers** *(measured)*.

| language | holder | result |
|---|---|---|
| go | int32 | `int32` `INT:32:00000000` — zero |
| rust | i32 | panic |
| c++ | int32_t | `int` `INT:32:0000a800` — 43008 |
| java | int | `int` `INT:32:0000a800` — 43008 |
| c-sharp | int | `System.Int32` `INT:32:0000a800` — 43008 |
| typescript | number | `number` `FLOAT:64:40e5000000000000` — 43008.0 |
| dart | int | `int` `INT:64:0000a80000000000` — 43008 × 2³² |

Three of them mask the shift count to five bits and give 43008. Go does
not mask and gives zero. Typescript masks and then returns a float,
because it has no integer type. Dart shifts inside 64 bits. Rust
refuses to answer at all. The verdict grain records one thing here —
ACCEPT — for all seven.

**Two. Integer overflow: five wraps and one panic** *(measured)*. The
expression is `i64max + 42`, both operands the language's 64-bit signed
holder. The two sides of this are a group of five and a single
language, so they are set out separately.

*The five that wrap, and they agree bit for bit:*

| language | result |
|---|---|
| go int64 | `INT:64:8000000000000029` |
| c++ int64_t | `INT:64:8000000000000029` |
| java long | `INT:64:8000000000000029` |
| c-sharp long | `INT:64:8000000000000029` |
| kotlin Long | `INT:64:8000000000000029` |

*The one that does not wrap:*

| language | result |
|---|---|
| rust i64 | raise, `panic` |

Rust is alone only because this build has debug assertions on, which is
rust's own default for an unoptimised build. The same source built with
`-O` wraps like the rest. That is a property of the build and it is
stated here as one.

**Three. Division by zero splits six ways** *(measured)*. The
expression is `42 / 0` on each language's own integer holder:

| language | what happens |
|---|---|
| go | raise, `runtime error: integer divide by zero` |
| rust | raise, `panic` |
| java | raise, `java.lang.ArithmeticException` |
| c-sharp | raise, `System.DivideByZeroException` |
| kotlin | raise, `java.lang.ArithmeticException` |
| c++ | **death**, `SIGFPE`, uncatchable |
| dart | **an answer**: `double` `FLOAT:64:7ff0000000000000`, positive infinity |
| typescript | raise, `RangeError` (bigint holder) |

Dart is the one that answers. It answers because dart's `/` is not
integer division at all — it returns a `double` whatever its operands
are. The same spelling, a different operation. Dart's `~/` does raise,
`IntegerDivisionByZeroException`. Meanwhile `42 % 0` gives typescript a
`number` `FLOAT:64:7ff8000000000000`, which is NaN, where every other
language raises or dies.

**Four. Float arithmetic agrees perfectly** *(measured)*. `pi + pi` on
the 64-bit float holder returns `FLOAT:64:401921fb54442d18` in go,
rust, c++, java, c-sharp, kotlin and typescript — seven languages, one
bit pattern, no exceptions. Recording bits rather than printed decimals
is what makes that statement possible. Seven different default float
formatters would have produced at least three different strings.

**Five. Swift's type checker and swift's compiler disagree on 40.7
percent of swift's accepted set** *(measured)*. The two instruments are
set against each other here rather than joined in a sentence.

- **`swiftc -typecheck`, the instrument every swift verdict in this
  node was taken with.** It accepted 2,618 of swift's probes.
- **`swiftc` proper, the full compiler.** It refuses 1,066 of those
  2,618 — 1,032 of them for arithmetic or literal overflow.

This does not invalidate the swift verdict rows. It says the verdict
was taken at a stage, and names the stage. It is the same shape of
finding as log 030's dart severity fault, restated above: dart's lane
scraped `dart analyze` output at any severity, so a dead-code warning
was read as a type refusal. In both cases the instrument was answering
a slightly different question than the one being asked.

**Six. C++ segmentation-faults on `i64max + "hello"`** *(measured)*.
The value matrix records `int64_t + const char*` as ACCEPT, because it
is: c++ reads it as pointer arithmetic. Executing it produces a pointer
nine quintillion bytes past a string literal, and reading that pointer
kills the process. 162 of c++'s 480 deaths are `SIGSEGV` of this kind,
the other 318 are `SIGFPE`. An acceptance-grain pass calls this cell
uniform ACCEPT and stops.

**Seven. Dart raises on 1,839 of its 26,451 accepted probes, 7.0
percent — more than any other language here** *(measured)*.
Overwhelmingly `NoSuchMethodError`, and the reason is the one
`HARVEST.md` already flagged: 388 of dart's acceptance-grain accepts
carry a `dynamic` operand, where the checker is switched off and the
real verdict is deferred to run time. This pass is where that deferred
verdict finally arrives. `dynamic v = null; null + null` type-checks
and then raises `NoSuchMethodError`. Dart's ACCEPT and go's ACCEPT are
not the same word.

**Eight. Kotlin returns 466 distinct result types, rust 40, c-sharp 43
and dart 75, against java's 6 and swift's 7** *(measured)*. Kotlin's
466 is its elvis `?:`, its `in` and its `..`, which hand back the
operand's own class rather than a primitive. Java's six is the honest
one: java's operators return primitives and `String` and nothing else.
Dart's 75 is mostly the `Object` bucket and the many holder classes
reachable through `??`. This is the raw material for the answer-grain
clustering of item 4i and it is not analysed here.

---

## §6 — what is still running, and what is left

**Nothing is still running.** All nine lanes are done, harvested into
`raw/`, folded, and past the completeness gate. `HARVEST.md` carries
the state and the quarantines.

**Two quarantines, by this node's standing convention.** Kotlin ran
three times and only the third is folded.

| lane | wall s | why it is not the product |
|---|---|---|
| `ex_kotlin_00.sh` | 761.4 | the `LongRange`-as-`Iterable` fault of §2; one chunk spent nine minutes materialising a range |
| `ex_kotlin_r0.sh` | 198.2 | ranges fixed, but java arrays still recorded through `toString` |
| `ex_kotlin_r1.sh` | 194.0 | **the product**; `answers_kotlin.json` is built from this |

The second fault was found by **diffing the two runs**, which is worth
recording as a method. Run 0 and run r0 disagreed on 2,645 of 34,653
rows, and every one of them was a java array recorded as `[C@4b1210ee`.
Kotlin's `toString` for an array embeds an **identity hash**, so the
same probe records a different answer on every run *(measured)*. A
recorder that writes one is recording the heap and not the answer. It
was fixed by reflecting over the array; r0 against r1 moved 2,372 rows
from `OPAQUE` to `LIST` *(measured)*.

**182 rows remain genuinely non-deterministic and they are not a
fault.** They are `String + CharArray`, whose answer IS the string
`null[C@238e0d81` — the identity hash is part of what kotlin returns.
Recorded as it comes back *(measured)*.

Three things this pass does not do and a later agent should not assume
it did.

**Declaration raises are not separated from operation raises.** One
guarded block covers both. Typescript's 1,468 `SyntaxError` rows are
declaration raises *(measured)*. Whether any other language's raises
are is **unverified**. Kotlin's 1,326 `NumberFormatException` rows are
the same shape and are **unverified**.

**The answers are not clustered.** Item 4i wants the answer half of the
CORE's phase-4 pair for all twelve languages. Log 031 built the
clustering machinery for the three open-dispatch languages; pointing it
at `answers_<lang>.json` is the next step and it is not started. The
nine files are shaped for it: every row carries the operation, both
operands as form plus holder plus value class, and the result as type
plus encoding plus payload.

**The rust wrap-versus-panic result is build-dependent** and only the
debug build has been measured. A release build would cost about a
second and would settle whether rust's `i64max + 42` joins the other
five. It has not been run.
