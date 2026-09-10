# log 028 — layer 3 phase 3: close-out, certification, and the value matrix

Date: 2026-08-18 (later the same day than log 027). Node:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`.
This log closes the five items log 027 §6.1 left open.

**Rewritten 2026-08-19 for readability at the owner's instruction. The content
is identical — same facts, same numbers, same findings, same section
numbers. Only the prose was rebuilt.**

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

---

## words used in this log

This node has built up a set of short words for its own parts. Every
one of them is defined here, with an example taken from this log rather
than a made-up one. Nothing below this block uses a word that is not
either ordinary English or defined here.

```
layer 1, layer 2, layer 3
    the three levels this node works on.
    layer 1 is the DATA with no language
    attached.  layer 2 is the HOLDERS, the
    per-language slots that hold that data.
    layer 3 is the OPERATIONS the compiler
    can apply to a loaded holder.
    example tied to context:
        `short a = 9223372036854775807;`
        failing is layer 2 leaking into a
        layer-3 verdict, which is the whole
        subject of the load check in §6.5.

probe
    one small generated program that asks one
    language one question.
    example tied to context:
        java's acceptance run below is 20,480
        probes; each declares two holders and
        applies one operation to them.

lane
    one batch job.  it runs a planned set of
    probes and writes its output to one raw
    text file.  a lane has a short name.
    example tied to context:
        the dart value-matrix lane
        `vm_dart_00` ran 108,537 probes and
        wrote `/out/vm_dart_00.txt`.

shard, and the `__SUMMARY__` line
    one output chunk of a lane, ending in a
    line that states how many probes that
    piece did.  a language too big for one
    lane is cut into several shards.
    example tied to context:
        the value matrix runs as 26 shard
        lanes; kotlin and c++ take six each.

completeness gate (also: gate)
    a check run after a lane finishes.  it
    adds up the probe counts across the
    shards and compares the total with what
    the plan said.  it prints COMPLETE only
    if they match, TRUNCATED if the lane is
    short, and a loud `!!` line either way.
    example tied to context:
        typescript's matrix reads COMPLETE
        below; java's, csharp's, dart's and
        rust's read TRUNCATED.

ENOSPC, and the scratch disk
    the scratch disk is the 4 GB memory-backed
    working area the lanes write their probe
    files into.  ENOSPC is the operating
    system's "no space left on device" error,
    which is how a lane on that disk most
    often dies without saying so.
    example tied to context:
        §6.4 measures 230,000 probe files at
        912 MB and fixes the sweep before an
        ENOSPC could happen.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        `int`, `long` and `String` are three
        java holders; the certification grid
        in §4.3 places seven of them.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        `i64max` is one value class, and
        `short a = 9223372036854775807;` is
        that class refusing to load into a
        `short` holder.

cell (also: pair cell)
    one combination of operand kinds that an
    operation was asked about, held against
    one operation.
    example tied to context:
        typescript's matrix folds 230,000
        probes into 12,167 cells.

uniform cell, split cell
    a cell is UNIFORM when every value pair
    inside it gave the same verdict.  it is
    SPLIT when different values of the same
    two holders gave different verdicts.
    example tied to context:
        876 of typescript's 12,167 cells are
        split, and that is finding 0.

route A1
    the compiler's own checking module is
    imported and CALLED in our own process.
    no separate program is launched per
    probe.
    example tied to context:
        java's `javax.tools` harness and
        typescript's shipped checker, the two
        harnesses §2 builds, are both A1.

route A2
    the real compiler is launched as a
    separate program per probe, with codegen
    and linking skipped by a flag.
    example tied to context:
        `rustc --emit=metadata` and
        `g++ -fsyntax-only` are the A2 routes
        in the cost table of §2.3.

route B, and the lift
    route B reads acceptance rules out of the
    compiler's own source or shipped data,
    where they exist there as literal data.
    a LIFT is one such extraction, and it is
    a mechanical copy rather than a reading.
    example tied to context:
        the rust lift of §3 is 407 rows
        expanded from `core::ops`'s own macro
        templates and argument lists.

route C
    the probe is EXECUTED, so the answer it
    returns is recorded rather than only the
    verdict.
    example tied to context:
        route C is not built for the nine
        checked languages, which is why the
        value matrix of §6 produces verdicts
        and no answers.

certification, and the certification gate
    a lifted rule is a DRAFT until its
    verdicts are diffed cell by cell against
    a route-A or route-C run on the same
    pairs.  agreement CERTIFIES the cell.
    disagreement is recorded as a finding and
    is never reconciled.
    example tied to context:
        rust passes the gate on 490 of 490
        cells; java records 146
        disagreements.

placed, and unmapped holders
    a holder is PLACED on the compared grid
    only when the lift's own vocabulary
    contains that holder's own spelling.  a
    holder that would need a promotion or an
    unboxing rule to place is left UNMAPPED
    and is named in the result file.
    example tied to context:
        java's grid places 7 holders, which
        with 19 operations gives 931 cells.

the value matrix
    the run that takes every ordered holder
    pair of a language, for every operation,
    times the FULL cross product of value
    classes.  it exists to test whether a
    checked language's verdict moves with
    the value.
    example tied to context:
        2,221,643 probes across the nine
        checked languages, in 26 shard lanes.

load check (the `--loadcheck` probe)
    one probe per (holder, value class)
    carrying the DECLARATION ALONE — no
    second operand and no operation.  its
    verdict says whether the value could be
    loaded at all.
    example tied to context:
        1,046 such probes, in nine
        `ld_<lang>_00.sh` lanes, classify
        every split cell into the two kinds.

expander
    the small program that turns a lifted
    macro template plus its lifted argument
    list into the rows the template stands
    for.
    example tied to context:
        the first rust expander put the
        argument list into the wrong half of
        the shift template and produced 294
        rows instead of 407.

`javax.tools`
    java's own shipped compiler API.  it
    hands back the real javac as a callable
    object, so a probe can be checked without
    launching a program.
    example tied to context:
        `ToolProvider.getSystemJavaCompiler()`
        plus `JavacTask.analyze()` is the
        whole of java's route-A1 harness.

the shipped checker (typescript)
    the type checker that ships inside
    typescript's own `typescript.js` and can
    be `require`d and called directly.
    example tied to context:
        one `ts.Program` per 500 probe files,
        at 0.34 ms per probe, the cheapest
        checker of the eleven measured.

`javap -c`
    java's own shipped disassembler.  it
    prints the contents of a compiled class,
    which is how the `Operators` table is
    read out as data.
    example tied to context:
        java's route-B lift is the
        `Operators` table read through
        `javap -c`.

open-dispatch language
    a language where the accepting set is not
    fixed when the compiler is built, because
    the operation resolves at run time.
    example tied to context:
        python, ruby and php are the three,
        and their value matrices were run in
        log 027 for seconds of cost.

ruling 3
    the node's standing ruling that every
    value of every holder is probed
    everywhere, rather than a sample.
    example tied to context:
        §6 exists because ruling 3 was
        counted for the nine checked
        languages and not yet built.

ruling 6 (the anti-interpretation rule)
    an acceptance verdict must come from the
    compiler's own logic running, or from
    data lifted literally.  hand
    re-assembly of a table is forbidden.
    example tied to context:
        java's `instanceof` accepting nothing
        is recorded rather than patched,
        because patching it by hand is what
        ruling 6 forbids.

log 024 decision 3
    the open question of whether a holder
    that only partly succeeded in loading its
    values gets probed on the values it DID
    load.
    example tied to context:
        java's and csharp's split cells look
        like that question arriving as a
        measurement rather than as a
        question.
```

---

## what came before this log, restated

Every fact this log borrows from an earlier log or from the node's CORE
is stated here in full, so no sentence below depends on opening another
file.

- **Log 027 §6.1 left five items open, and this log closes all five.**
  They were: java's and typescript's route-A1 harnesses, not built; the
  rust route-B lift, which could not run; the certification diffs for
  java and rust, blocked on those two; the full value matrix for the
  nine checked languages, counted but not built; and the java
  23-versus-86 row discrepancy, recorded and not reconciled.
- **Log 027 §2.4 stated the value-independence assumption honestly, and
  never measured it.** Its words were that in a statically checked
  language the VERDICT is a function of the holder pair and the
  operation, and that the value class changes the ANSWER rather than the
  verdict. That is why every acceptance run in the node carried one
  value class per holder.
- **Log 027 §2.4 also recorded swift's six-operation menu as a grammar
  fact.** Swift's tree-sitter grammar parses `+` through a
  `custom_operator` rule instead of declaring it as an anonymous token,
  so the mechanical intersection with the grammar's token list returns
  six operations where other languages return 17 to 20.
- **Log 027 §5 item 5 recorded that same swift fact as a finding about
  the instrument**, not about the language, and refused to patch it by
  hand.
- **Log 027 §3.1 measured seven acceptance runs**: 71,313 probes, 5,842
  accepted, 65,471 refused, 1,644 seconds of wall time. Its per-probe
  cost table is the first nine rows of §2.3 below.
- **Log 027 §3.5 estimated java's unbuilt route-A1 harness** at
  single-digit milliseconds per probe, by analogy with the measured
  Roslyn figure of 1.51 ms for csharp.
- **Log 027 §4.1 certified go's `+` cell.** Go's `+` accepted 7 ordered
  pairs, every one same-holder and numeric-or-string, which is what the
  lifted `binaryOpPredicates` map predicts.
- **Log 027 §4.2 and §4.3 recorded go's two disagreements.** Go's `<<`
  accepted 16 pairs of which 4 are same-holder, and `==` accepted 36 of
  which 24 pair a value against a bare `nil`. The lifted map has no row
  for either operation, so the lift is incomplete rather than wrong.
- **Log 027 §4.4 called java's lifted shift evidence DRAFT**, for want
  of a route-A run to diff it against. Its lifted rows carry the mixed
  `INT|LONG` and `LONG|INT` combinations explicitly.
- **Log 027 §4.5 raised the java row-count discrepancy**: the
  `Operators` table had been read as 23 rows in log 026 §2 and as 86 in
  this session's extraction.
- **Log 027 §5.1 finding 6 opened the silent-truncation family.** Three
  lanes died mid-run and all three exited 0 — rust on EBUSY, php on a
  fatal redeclaration, python on an out-of-memory kill. The rule it
  earned is that a lane's exit code is not evidence that it finished,
  and the mitigation is the completeness gate.
- **Log 027 §5.1 finding 8 measured the `&&` spread at 112-fold**, with
  c++ at 112 accepting ordered pairs and dart at 4, and go, rust,
  csharp, kotlin and swift at 1 each.
- **Log 027 §5.1 finding 10 recorded kotlin's elvis `?:` at 673 of 676
  accepting ordered pairs**, the most permissive single operation
  measured anywhere, and predicted that null-handling operations sit at
  the permissive end wherever they exist.
- **Log 027 §2.3 raced the batching question and batching lost.** Over
  400 go probes, batched-with-bisect took 42.2 s against per-file
  parallel's 7.8 s, because a mostly-refusing batch does not converge.
  The one case the batching argument survives is a set of probes already
  known to compile.
- **Log 026 §2 read java's `Operators` table as 23 rows.** Log 026
  finding 4 named go, typescript and java as the three languages whose
  checkers can be called in process.
- **Log 024 decision 3 is open**: whether a holder that partially
  refused loading gets probed on the values it DID load. Log 024 §6 is
  the owner's review of phase 1, also still outstanding.
- **The CORE's ruling 3 says every value of every holder, everywhere**,
  rather than a sampled placement.
- **The CORE's ruling 6 forbids interpretation**: a verdict comes from
  the compiler's own logic running, or from data lifted literally, and
  hand re-assembly is not allowed. Its certification gate says a lifted
  rule is a draft until diffed against route A or route C on the same
  pairs.
- **The lane daemon kills any script at 3600 seconds**, measured from
  the log header of every run, and it runs the lanes it is given
  serially in the order they were dropped.

---

## §1 — walkthrough, in plain words

Log 027 left five things open and this session did all five.

- Two languages had no layer-3 acceptance evidence at all. Both now have
  it, from their own compilers' own checkers.
- One lift could not run for want of a source component. It ran.
- Two lifts were drafts with nothing to diff against. Both were diffed,
  and the gate returned one certified language and one language's worth
  of findings.
- One number contradicted another number. The contradiction is resolved,
  mechanically, and the resolution is dull in the best way.
- And the full value matrix — the ruling this node has been carrying as
  counted-but-unbuilt since the design was settled — is built, sized,
  sharded and running.

**The two new harnesses.**

- **Java goes in process through `javax.tools`.** The verdict comes from
  `JavacTask.analyze()`, which runs parse, enter, attribute and flow and
  stops before code generation. One JVM serves the whole run: **20,480
  probes, 981 accepts, 3.4 ms per probe** *(measured)*.
- **Typescript loads the checker that ships inside `typescript.js`.** It
  reads each file's own diagnostics out of a shared `Program`: **12,167
  probes, 2,318 accepts, 0.34 ms per probe** *(measured)*. That is the
  cheapest checker of the eleven now measured — forty times cheaper than
  the next-cheapest compiled route, and a hundred and eighty times
  cheaper than c++.
- Both harnesses were spot-checked in both directions before their
  numbers were believed.

**The certification gate, on its second and third uses.**

- **Rust is CERTIFIED.** 490 cells compared, 490 agreements, **zero
  disagreements** *(measured)*. That is this node's first fully
  certified language, and it is worth saying what it cost: one command
  (`rustup component add rust-src`), a mechanical expander, and a diff.
- **Java is not certified.** 931 cells compared, 785 agreements, **146
  disagreements** *(measured)*. Every single one of the 146 has the same
  shape — javac ACCEPTS where the lifted table says nothing. Not one
  disagreement runs the other way.
- The cause is one step in the wrong place. The lifted table is a table
  of exact operand types. Javac widens the operands before it consults
  the table. The widening is not in the table. So the lift is INCOMPLETE
  in exactly the way go's was, for a different reason, found the same
  way.

**The 23-versus-86 question is answered and the answer is boring.**

- The java `Operators` table has **86 rows** and **23 distinct ordered
  operand pairs** *(measured, both counted from the same extraction)*.
- The two numbers were never in conflict. They count different things.
- The A1 evidence settles which one governs acceptance. On the placed
  grid, java's twenty operations produce **seven different accepting
  pair sets** *(measured)*, so a verdict is not a function of the
  operand pair alone, and a 23-entry pair vocabulary cannot express the
  table. 86 is the row count and it is the one that matters.

**The value matrix is running.**

- Ruling 3 says every value of every holder, everywhere.
- The acceptance runs carried one value class per holder, on the
  argument that a statically checked language's verdict does not depend
  on the value. That was an assumption. It was stated honestly in log
  027 §2.4 and never measured.
- It is being measured now: the same checkers, the same ordered holder
  pairs, times the full value cross product. **2,221,643 probes across
  the nine, 10.32 hours projected from measured per-probe costs, in 26
  shard lanes** *(derived)*.
- Six shards have landed already, all at or under projection.

**And the assumption did not survive the first fold.**

- Typescript's matrix is complete, and **876 of its 12,167 cells SPLIT —
  7.2 percent of them give different verdicts for different values of
  the same two holders** *(measured)*.
- The cleanest case is four lines long. `false == false` type-checks and
  `false == true` does not, because typescript narrows each variable to
  its literal type and then refuses a comparison it can see has no
  overlap. The acceptance run recorded that cell as a flat ACCEPT.
- So the value class does move a checked language's verdict, in at least
  one language. The phrase *a static language's verdict is a function of
  the holder pair* is now known to be false as a general statement,
  rather than assumed to be true.
- Java, csharp, dart and rust show splits too on their part-finished
  shards. Theirs look like a different animal — the value failing to
  LOAD into the holder, rather than the operation refusing it — and a
  control probe that settles which is which is built and queued.

**Two smaller things the session learned, both the hard way.**

- **A shard's probe SOURCE COUNT is a cost, because a tmpfs charges a
  whole block per file.** 230,000 probe files measured **912 MB** of the
  4 GB scratch *(measured)*. A serial queue of twenty shards that each
  wiped only their own directory on entry would have filled it. Lanes
  now sweep up after themselves.
- **The first rust expander produced same-type shift rows**, because it
  put a macro's argument list into the wrong half of the macro's own
  template. That is an expander fault which would have hidden the very
  finding the diff was run to test. It was caught by reading the output
  before trusting it, which is the only way these are ever caught.

---

## §2 — the two harnesses that did not exist

### §2.1 java, route A1 — `javax.tools`

- **what it is.** `ToolProvider.getSystemJavaCompiler()`, an in-memory
  `JavaFileObject` per probe, a file manager whose output goes to a
  discarded byte array, and `com.sun.source.util.JavacTask.analyze()`
  as the call. `analyze()` stops before code generation, so nothing is
  emitted and nothing is linked.
- **why it is route A1 and not a reading.** The verdict is the
  `DiagnosticCollector`'s own error list. No source of javac's is read
  by anyone; javac's own checker runs and answers.
- **the run** *(all measured)*:

| language | probes | accept | refuse | wall time | per probe | gate |
|---|---|---|---|---|---|---|
| java | 20,480 | 981 | 19,499 | 69.9 s | 3.41 ms | COMPLETE |

- **checked in both directions before it was believed** *(measured)*:

```
String a=null; String b=null; a + b   ACCEPT
String a=null; String b=null; a - b   REFUSE
int << long                           ACCEPT
boolean && Boolean                    ACCEPT
```

- **the estimate held.** Log 027 §3.5 put java at *single-digit
  milliseconds per probe, by analogy with the measured Roslyn figure of
  1.51 ms*. Measured: **3.41 ms** *(measured)*. That is slower than
  Roslyn by 2.3x, and inside the range that was claimed.

### §2.2 typescript, route A1 — the shipped checker

- **what it is.** `require` of
  `/persist/tv/ts5/node_modules/typescript/lib/typescript.js`, one
  `ts.Program` per 500 probe files, and each file's own
  `getSyntacticDiagnostics` plus `getSemanticDiagnostics`. The
  `lib.*.d.ts` files are parsed once and held, which is where the speed
  comes from.
- **one generator change, stated because it touches the probe text.**
  Every probe file ends `export {};`, which makes it a module and keeps
  its holder types file-scoped. Without it the class declarations that
  three typescript holders carry would collide across the files of one
  `Program`. It changes no operand and no operation.
- **the run** *(all measured)*:

| language | probes | accept | refuse | wall time | per probe | gate |
|---|---|---|---|---|---|---|
| typescript | 12,167 | 2,318 | 9,849 | 4.1 s | 0.34 ms | COMPLETE |

- **checked in both directions before it was believed** *(measured)*:

```
number + number    ACCEPT     null + null      REFUSE
string + string    ACCEPT     number - string  REFUSE
string + number    ACCEPT     bigint + number  REFUSE
boolean && boolean ACCEPT     array + array    REFUSE
```

- `bigint + number` refusing while `string + number` accepts is the
  four-line proof that the checker is really running. Those two differ
  only in typescript's own rules.

### §2.3 the cost table, all eleven checked languages

Per-probe cost, cheapest first. Rows other than the last two are log
027 §3.1's; the last two are this session's. All **measured**.

| language | route | per probe | cost against c++ |
|---|---|---|---|
| typescript | A1 shipped checker | 0.34 ms | 179x cheaper |
| dart | A2 `dart analyze <dir>` | 0.98 ms | 62x |
| csharp | A1 Roslyn in process | 1.51 ms | 40x |
| java | A1 `javax.tools` | 3.41 ms | 18x |
| rust | A2 `rustc --emit=metadata` | 6.8 ms | 9x |
| go | A2 `go build` | 17.4 ms | 3.5x |
| swift | A2 `swiftc -typecheck` | 42.5 ms | 1.4x |
| kotlin | A1 in process, warm JVM | 52.1 ms | 1.2x |
| cpp | A2 `g++ -fsyntax-only` | 60.9 ms | — |

- **the pattern is now unmistakable, and it is not about the language.**
  The split is between two groups, and the line between them is how the
  checker is reached rather than what it checks.
  - **The four cheapest are the four whose checker can be CALLED** —
    three in process, and one that analyses a directory without
    aborting.
  - **The five dearest all pay a process launch per probe**, as opposed
    to the four above, which pay none.
- Log 026 finding 4 named three in-process candidates. The count is
  five, and the two added this session are the two cheapest of the lot
  *(derived)*.

---

## §3 — the rust lift, run at last

- **the blocker was one command.** `rustup component add rust-src`
  installed into `/opt/rustup/toolchains/1.96.1-x86_64-unknown-linux-gnu`
  in seconds *(measured)*. Note for a later agent: that path is NOT
  `/persist`, so a container rebuild loses it and the command must be
  re-run.
- **what was lifted, and what makes it data rather than a reading.**
  Two literal things per operation family: the macro's own template
  line (`impl Add for $t`, `impl Shl<$f> for $t`) and the macro's own
  argument list (`add_impl! { usize u8 ... f128 }`). The rows are the
  mechanical expansion of the one by the other. Where a macro forwards
  to an inner macro with a second literal operand list — which is
  exactly what `shl_impl_all` does — that inner list is read from the
  forwarding body, literally.
- **the result** *(measured, `raw/lift_b_rust.txt`)*:

| trait | rows | shape |
|---|---|---|
| Add, Sub, Mul, Div, Rem | 16 each | same holder only |
| BitAnd, BitOr, BitXor | 13 each | same holder only, `bool` included |
| Shl, Shr | 144 each | 12 by 12, every ordered pair |
| **total** | **407** | — |

- **the first expander was wrong, and the wrong version is kept.**
  - **Run 1 emitted 294 rows**: same-type shifts only, and no `bool`.
  - **Run 2, the one above, emitted 407 rows**, as opposed to run 1's
    294.
  - Two faults separate them, both in the expander and neither in the
    source. The shift template's second operand hole was filled with the
    first operand's list. The type filter was numeric-only.
  - `raw/VOID_lift_b_rust_run1.txt` is kept, because a wrong expansion
    that would have CONFIRMED the assumption under test is worth having
    on the record.
- **level.** The 407 rows are **measured** as an extraction and
  **DRAFT** as a rule until §4 diffs them. §4 diffs them.

---

## §4 — CERTIFICATION RESULTS

The gate is stated once more here, so the numbers below are read right.
A route-B lift is a DRAFT until its verdicts are diffed cell by cell
against a route-A run on the same pairs. Agreement CERTIFIES the cell.
Disagreement is a FINDING and is recorded as one, never reconciled.
The diff is `cert_diff.py`; its products are
`certification_rust.json`, `certification_java.json` and
`certification_go.json`.

A holder enters the compared grid only when the lift's own vocabulary
contains that holder's own spelling. Holders that would need a
promotion or an unboxing rule to place are NOT placed — placing them is
the hand-re-assembly ruling 6 forbids — and they are counted and named
as unmapped in the result file instead.

### §4.1 the headline

| language | route A | route B | cells compared | agreements | disagreements | verdict |
|---|---|---|---|---|---|---|
| rust | A2 `rustc --emit=metadata` | core::ops macro data | 490 | 490 | 0 | **CERTIFIED** |
| java | A1 `javax.tools` | `Operators` via `javap -c` | 931 | 785 | 146 | **DISAGREEMENTS RECORDED** |
| go | A2 `go build` | `binaryOpPredicates` map | — | see §4.4 | see §4.4 | part certified, part silent |

### §4.2 rust — CERTIFIED, and what that sentence is worth

- **the grid.** 7 holders placed (`bool`, `i32`, `i64`, `u64`, `i128`,
  `f64`, `f32`), 10 operations the lift speaks to (`+ - * / % & | ^ <<
  >>`), 490 cells *(measured)*.
- **the result.** Every one of the 490 agrees *(measured)*. Worked
  examples of both verdicts agreeing:

```
i32  +  i32   lift ACCEPT   rustc ACCEPT
i32  +  i64   lift REFUSE   rustc REFUSE
bool &  bool  lift ACCEPT   rustc ACCEPT
bool +  bool  lift REFUSE   rustc REFUSE
i32  << i64   lift ACCEPT   rustc ACCEPT
f64  << f64   lift REFUSE   rustc REFUSE
```

- **why the shift rows are the interesting half.** The two families
  differ in shape, and the compiler agrees with both shapes.
  - **`Shl` has 144 rows in the lift** — every ordered pair of the
    twelve whole-number types.
  - **`Add` has 16**, as opposed to `Shl`'s 144: same-type only.
  - rustc agrees on all of them. So rust's shift exemption is now
    attested TWICE, by its own source data and by its own compiler, and
    the two were produced independently *(measured)*.
- **what the lift is silent on.** `== != < <= > >= && || ..` — nine
  operations of rust's nineteen. Those live in `cmp.rs` and in the
  language rules, not in `core::ops`'s arithmetic macros. The silence
  is recorded in `certification_rust.json` as
  `operations_lift_is_silent_on`; it is not a disagreement and it is
  not a certification either.

### §4.3 java — 146 disagreements, all of one shape

- **the grid.** 7 holders placed (`boolean`, `int`, `long`, `float`,
  `double`, `String`, and the null-reference holder, whose declared
  type is also `String`), 19 operations the table has a tag for, 931
  cells *(measured)*.
- **the shape.** All 146 disagreements are javac ACCEPT against lift
  REFUSE *(measured)*. **Zero run the other way.** A lift that never
  says ACCEPT where the compiler says REFUSE is incomplete, not wrong,
  and the distinction matters for what may be done with it.
- **by operation** *(measured)*:

| operation | disagreements | operation | disagreements |
|---|---|---|---|
| `==` | 16 | `<` `<=` `>` `>=` | 12 each |
| `!=` | 16 | `&` `\|` `^` | 2 each |
| `+` `-` `*` `/` `%` | 12 each | `<<` `>>` `>>>` | **0** |
| — | — | `&&` `\|\|` | **0** |

- **worked, the twelve on `+`** *(measured)*:

```
int    + long     int    + double   int   + float
long   + int      long   + double   long  + float
float  + int      float  + long     float + double
double + int      double + long     double+ float
```

- **the finding, stated plainly.** Java's `Operators` table is indexed
  by EXACT operand types. Javac applies binary numeric promotion to the
  operands BEFORE consulting it, so `int + double` reaches the table as
  `DOUBLE + DOUBLE` and finds its row. A lifter that stops at the table
  therefore reports a refusal for every mixed numeric pair the language
  accepts. The lift is not wrong about any row it has; it is missing
  the step upstream of itself. **Recorded as a finding. Nothing is
  reconciled.** The java route-B table stands as CERTIFIED for the
  shift and logical tags and as DRAFT for the arithmetic, relational
  and equality tags.
- **the shifts certify, and that is the corroboration log 027 §4.4
  wanted.** `<<`, `>>` and `>>>` have zero disagreements over 147 cells
  *(derived: 3 operations by 49 placed pairs)*. The lifted rows for
  those tags carry the mixed `INT|LONG` and `LONG|INT` combinations
  explicitly, and javac accepts exactly those. Log 027 §4.4 called
  java's shift evidence DRAFT for want of a route-A run; the route-A
  run exists now and it agrees.
- **the free consistency check passed.** Two holders map to the table's
  `STRING` — the `String` holder and the null-reference holder, whose
  declaration is `String v = null;`. They agree on all 19 operations
  *(measured)*, which is the harness checking itself.

### §4.4 go — re-diffed, and log 027 §4's numbers re-counted

- `certification_go.json` re-counts from the artifact rather than
  quoting the log. The map's own token list, lifted literally, covers
  **eleven** operations *(measured)*:

```
+  -  *  /  %  &  |  ^  &^  &&  ||
```

- and is SILENT on **eight** *(measured)*:

```
==  !=  <  <=  >  >=  <<  >>
```

- so log 027 §4.2 and §4.3 stand exactly as recorded. Go's `+` is
  certified. Go's shifts and equalities disagree, because the map has no
  row for them at all.
- The eight silent operations include the two most permissive in the
  language: `==` and `!=` accept 36 pairs each, against `+`'s 7
  *(measured)*.

### §4.5 what the three languages say together

- **three lifts, three different outcomes, one gate.**
  - **Rust's lift is complete for what it covers, and certifies whole.**
  - **Java's is complete per row and incomplete per language**, because
    a step upstream of the table is not in the table.
  - **Go's is silent on the operations that matter most.**
  - **No lift was WRONG about a row it carried** — all three failures
    are omissions *(measured, across 1,421 compared cells and the go
    operation census)*.
- **that is a usable rule for phase 4**, and it is stated as a
  hypothesis, level **derived**: a lifted acceptance table under-states
  and does not over-state. If it holds up, a lift is safe to read as a
  LOWER BOUND on acceptance and never as an upper one. It rests on
  three languages and it should be tested against a fourth before it is
  leaned on.

---

## §5 — the java 23-versus-86 row count, RESOLVED

**Verdict: both numbers are right, they count different things, and
the count that governs acceptance is 86.**

- **the two counts, from one mechanical extraction of one table in one
  JDK** *(both measured, `raw/lift_b.txt`, `cert_diff.py`)*:

| what is counted | number |
|---|---|
| rows `(tag, lhs, rhs, result)` | **86** |
| distinct ordered operand pairs `(lhs, rhs)` | **23** |
| distinct operation tags | 19 |

- 23 is exactly the size of the pair vocabulary the 86 rows draw on —
  `BOOLEAN BOOLEAN`, `BOOLEAN STRING`, `BOT STRING`, `DOUBLE DOUBLE`,
  and so on to `STRING STRING`. Log 026 §2's "23-row" reading counted
  the vocabulary; this session's extraction counted the rows. Nothing
  is in conflict and no JDK changed underneath anyone.
- **which number the compiler's own behavior supports.** If a verdict
  were a function of the operand pair alone, all twenty operations
  would share one accepting pair set and 23 entries would say
  everything. Java's own checker, run over the placed grid, produces
  **seven distinct accepting pair sets across the twenty operations**
  *(measured)*:

| operation | accepting pairs on the placed grid |
|---|---|
| `+` | 27 |
| `==` `!=` | 18 |
| `-` `*` `/` `%` `<` `<=` `>` `>=` | 16 |
| `&` `\|` `^` | 5 |
| `<<` `>>` `>>>` | 4 |
| `&&` `\|\|` | 1 |
| `instanceof` | 0 |

- so the table cannot be indexed by pair; it is indexed by
  `(tag, lhs, rhs)`. **86 is the count that governs acceptance and it
  is the one carried forward** *(derived from measured material)*.
- **and the honest remainder.** This resolves the arithmetic. It does
  not make either extraction a verdict: §4.3 has just shown that all 86
  rows together still miss every mixed numeric pair javac accepts. The
  right reading of the table is 86 rows AND incomplete.

---

## §6 — the full value matrix for the nine checked languages

### §6.1 what is being measured, and why this shape

- **ruling 3 says every value of every holder, everywhere.** In the
  three open-dispatch languages that was done in log 027 and cost
  seconds. In the nine checked ones it was counted and not built. The
  reason given for the acceptance runs carrying one value class per
  holder was that *a static language's verdict is a function of the
  holder pair and not of the value* (log 027 §2.4).
- **that reason is an assumption and it has never been measured.** This
  run measures it, with the same instrument that produced the
  acceptance verdicts: same checkers, same ordered holder pairs, times
  the FULL value cross product. A cell whose verdict is the same across
  every value pair is `uniform`; a cell that is not is `split`, and
  every differing value-class pair in a split is listed in full.
- **a split would be the most consequential single finding in this
  node**, because the acceptance runs, the certification diffs and the
  §2.3 cost table all rest on the assumption it would break.
- **what this run is NOT.** It produces no ANSWERS. Answers come from
  execution, which is route C, which is not built for these nine. That
  remains open and is named as such in §7.

### §6.2 the plan, sized before it ran

`matrix_plan.json`; per-probe costs are the measured ones of §2.3, so
the projections are **derived** and the probe counts **measured**.

| language | holders | ops | value-matrix probes | ms/probe | projected | shards |
|---|---|---|---|---|---|---|
| typescript | 23 | 23 | 230,000 | 0.34 | 1.3 min | 2 |
| dart | 25 | 17 | 217,073 | 0.98 | 3.5 min | 2 |
| csharp | 30 | 20 | 397,620 | 1.51 | 10.0 min | 4 |
| java | 32 | 20 | 444,020 | 3.41 | 25.2 min | 4 |
| rust | 22 | 19 | 205,504 | 6.80 | 23.3 min | 2 |
| go | 20 | 19 | 167,884 | 17.40 | 48.7 min | 2 |
| swift | 24 | 6 | 76,614 | 42.50 | 54.3 min | 2 |
| kotlin | 26 | 17 | 253,028 | 52.10 | 219.7 min | 6 |
| cpp | 24 | 19 | 229,900 | 60.90 | 233.3 min | 6 |
| **total** | — | — | **2,221,643** | — | **10.32 h** | **26** |

- **why 26 shards and not 9 lanes.** Each shard is capped twice, and the
  two caps come from two different facts.
  - **The time cap is 40 minutes of projected time.** It exists because
    the lane daemon kills a script at 3600 s *(measured, from the log
    header of every run)*. Kotlin and c++ need six pieces each on this
    cap.
  - **The file cap is 120,000 probe files.** It exists because a tmpfs
    charges a block per file, as opposed to charging by content. Java
    and csharp need four pieces each on this cap.
- **launch order is cost order**, cheapest first, so that a fault in
  the shared assembly step is found for the price of a minute rather
  than of four hours. The first five shards were watched before the
  remaining twenty-one were queued.

### §6.3 what has landed so far

All **measured**. Projections are from the table above.

| shard | probes | accept | refuse | wall time | per probe | against projection |
|---|---|---|---|---|---|---|
| typescript 0/2 | 115,000 | 24,232 | 90,768 | 20.2 s | 0.18 ms | 1.9x cheaper |
| typescript 1/2 | 115,000 | 20,318 | 94,682 | 32.9 s | 0.29 ms | held |
| dart 0/2 | 108,537 | 11,872 | 96,665 | 102.2 s | 0.94 ms | held |
| csharp 0/4 | 99,405 | 8,220 | 91,185 | 76.1 s | 0.77 ms | 2.0x cheaper |
| java 0/4 | 111,005 | 5,553 | 105,452 | 309.1 s | 2.78 ms | 1.2x cheaper |
| rust 0/2 | 102,752 | — running — | — | — | — | — |

- **548,947 value-matrix probes measured already** *(derived)*, in five
  lanes. That is more than seven times the whole of log 027's
  acceptance evidence.
- Every settled shard met or beat its projection. So the 10.32-hour
  figure is, on this evidence, an upper bound rather than an estimate
  to be nervous about *(derived)*.

### §6.5 THE FIRST FOLD — and the assumption does not survive it

`l3_matrix_read.py` was run against what had landed. Typescript is the
one language COMPLETE so far. The rest are labelled TRUNCATED by the
gate, and they are shown only because their shape is already visible.

| language | probes folded | pair cells | uniform | **split** | gate |
|---|---|---|---|---|---|
| typescript | 230,000 | 12,167 | 11,291 | **876** | COMPLETE |
| java | 111,005 of 444,020 | 6,500 | 5,952 | 548 | TRUNCATED |
| csharp | 99,405 of 397,620 | 5,500 | 4,998 | 502 | TRUNCATED |
| dart | 108,537 of 217,073 | 5,355 | 5,085 | 270 | TRUNCATED |
| rust | 15,146 of 205,504 | 1,520 | 1,490 | 30 | TRUNCATED |

- **the finding, measured, and it is the one this run was built to
  look for: a statically checked language's verdict is NOT always a
  function of the holder pair. Typescript splits on 876 of its 12,167
  cells — 7.2 percent** *(measured, on a COMPLETE file)*.
- **worked, and it is not an edge case** *(measured)*:

```
let a: boolean = false; let b: boolean = false;
a == b   ACCEPT
let a: boolean = false; let b: boolean = true;
a == b   REFUSE
```

  The holders are identical, the operation is identical, and only the
  VALUE differs. Typescript narrows `a` and `b` to their literal types
  by control flow and then refuses a comparison between `false` and
  `true` as having no overlap. The acceptance run, carrying one value
  class per holder, recorded this cell as a flat ACCEPT.
- **all 876 of typescript's splits are operation-level, none is a
  failure to load** *(measured, derived from the complete file)*: no
  `(holder, value class)` pair is refused in every split cell it
  appears in, which is the signature a value that does not fit its
  holder would leave.
- **the other four are a different story, and the difference matters.**
  Java's and csharp's splits so far look like the OPPOSITE case — the
  value failing to load, as opposed to the operation refusing:

```
short a = 42;                    a + b   ACCEPT
short a = 9223372036854775807;   a + b   REFUSE
```

  That is layer 2 leaking into a layer-3 verdict, not layer 3 moving.
  It is exactly log 024 decision 3 — *whether a holder that partially
  refused loading gets probed on the values it DID load* — arriving as
  a measurement rather than as a question.
- **which is why a control probe is now built and queued.**
  `l3_matrix.py --loadcheck` emits one probe per (holder, value class)
  carrying the DECLARATION ALONE, no second operand and no operation:
  **1,046 probes across the nine, about 21 seconds in total**
  *(derived)*. Its verdicts classify every split into the two kinds,
  mechanically, with no reading of anything. The nine `ld_<lang>_00.sh`
  lanes are queued behind the matrix.
- **level discipline on this section.** Typescript's 876 is
  **measured** and complete. The other four counts are **measured on
  a fraction** and are flagged TRUNCATED by the gate; they say the
  shape exists, not how large it is. The split-versus-load
  classification is **measured for typescript** and **pending** for
  the rest.

### §6.4 the scratch-space fault, measured and fixed

- Every lane wipes its own working directory ON ENTRY, which was
  correct while lanes were rare and enormous. Twenty-six shards in a
  serial queue is a different problem. A finished dart shard was still
  holding **1,121 MB** of probe sources when the next lane started, and
  free space on the 4 GB scratch had fallen from 3,555 MB to 1,096 MB
  after four shards *(all measured)*.
- **cause, measured:** a tmpfs charges a whole block per file, so
  230,000 probe files cost 912 MB regardless of their content.
- **fix, built:** every value-matrix lane now sweeps its own directory
  on EXIT and prints the free space it leaves behind. A one-off
  `vm_sweep.sh` clears what the first five left.
- **why this belongs in the log.** It is the fifth member of the family
  log 027 §5.1 finding 6 opened. An ENOSPC in the middle of a shard
  would have produced a partial result file and, on this phase's
  evidence, an exit code of 0. It was headed off by arithmetic rather
  than caught by the gate, but the gate would have caught it.

---

## §7 — findings

Six, in the line's sense: things the earlier logs did not contain.

0. **A statically checked language's verdict is not always a function
   of the holder pair.** Typescript splits on **876 of 12,167 cells**
   *(measured, complete file)*, all of them at the operation level and
   none of them a failure to load. This is the load-bearing assumption
   under every acceptance run in this node, it was stated honestly as
   an assumption in log 027 §2.4, and the first complete value matrix
   refutes it. It is numbered zero because it changes how the rest of
   this log's numbers should be read: an acceptance-grain verdict is a
   verdict for the value class the acceptance run happened to carry,
   and nothing more, until that language's matrix lands. See §6.5.

1. **The shift exemption has an exception, and it is typescript.**
   Log 027 §4.4 recorded the exemption from the same-type requirement
   as a shape shared by go, rust, csharp and c++, with java's lifted
   table agreeing. Two languages now stand against each other on it.

   - **Java confirms the exemption by measurement.** Its `<<` accepts
     **25** ordered pairs, of which only **5** are same-holder — the
     full 5-by-5 cross product of its whole-number holders.
   - **Typescript does NOT.** Its `<<` accepts **5** pairs and every one
     is same-holder: `number << number` and `bigint << bigint`, with
     `number << bigint` REFUSED *(all measured)*.

| language | `<<` accepts | of which same-holder | route |
|---|---|---|---|
| java | 25 | 5 | A1, measured |
| cpp | 25 | 5 | A2, measured |
| dart | 28 | 2 | A2, measured |
| csharp | 18 | 3 | A1, measured |
| go | 16 | 4 | A2, measured |
| rust | 16 | 4 | A2, measured |
| typescript | **5** | **5** | A1, measured |

   The regularity is real and it is not universal. Six of seven exempt
   their shifts. The seventh is the one language whose whole-number
   holders are two disjoint families rather than a promotion ladder.
   That is a better shaped finding than the unanimity log 027 was
   heading towards, and it is exactly the contradicts relation phase 4
   wants.

2. **Typescript's `??` accepts every ordered pair it has — 529 of
   529** *(measured)*. That takes the most-permissive title from
   kotlin's elvis at 673 of 676. Both are null-handling operations and
   both sit at the ceiling; log 027 §5.1 finding 10 predicted that
   shape and this is a second instance of it, at 100 percent rather
   than 99.6.

3. **`&&` is not a two-camp story, it is a spectrum, and typescript
   sits at the top of it.** Log 027 §5.1 finding 8 recorded a 112-fold
   spread with c++ alone at the permissive end. Typescript accepts
   **506** of 529 *(measured)*, beating c++'s 112 of 576 outright:

| language | `&&` accepts | share of pairs |
|---|---|---|
| typescript | 506 | 96 percent |
| cpp | 112 | 19 percent |
| dart | 4 | 0.6 percent |
| java | 4 | 0.4 percent |
| go, rust, csharp, kotlin, swift | 1 | under 0.3 percent |

   The table has two camps and they are worth naming against each
   other.

   - **Two languages permit almost anything in a truth position**:
     typescript and c++.
   - **Seven demand a truth holder**, as opposed to those two.
   - And the two permissive ones got there by different routes — c++ by
     implicit conversion to `bool`, typescript by truthiness in its own
     type rules. Same measurement, same cell, two mechanisms; that pair
     is worth carrying into phase 4 whole.

4. **A lifted table under-states and never over-states — three for
   three.** Across 1,421 compared cells in rust and java, plus go's
   operation census, **no lift ever said ACCEPT where the compiler said
   REFUSE** *(measured)*. Every failure was an omission: a silent
   operation (go), a missing upstream promotion step (java), or nothing
   at all (rust). Level **derived**, and named as a hypothesis rather
   than a rule because it rests on three languages.

5. **Java's `instanceof` accepts nothing, and that is a fact about the
   probe design rather than about java** *(measured, 0 of 1,024)*. The
   probe form is `(a) instanceof (b)` and `b` is always a VALUE, where
   java requires a TYPE on the right. The operation is in the menu
   because java's grammar declares it as an anonymous token, and the
   mechanical intersection has no way to know that one of its operands
   is not an operand. Recorded, not patched — patching it by hand is
   the interpretation ruling 6 forbids. It is the same class of
   instrument fact as swift's six-operation menu (log 027 §5 item 5).

---

## §8 — state of every lane, and how to harvest

### §8.1 done this session

| lane | route | probes | state | product |
|---|---|---|---|---|
| `ac_java.sh` | A1 `javax.tools` | 20,480 | DONE 69.9 s | `acceptance_java_A1.json` |
| `ac_typescript.sh` | A1 shipped checker | 12,167 | DONE 4.1 s | `acceptance_typescript_A1.json` |
| `lift_b_rust5.sh` | B | 407 rows | DONE 0.1 s | `raw/lift_b_rust.txt` |
| `cert_diff.py` (host) | gate | 1,421 cells | DONE | `certification_{rust,java,go}.json` |
| `vm_typescript_00/01` | A1 matrix | 230,000 | DONE 53.1 s | `/out/vm_typescript_*.txt` |
| `vm_dart_00` | A2 matrix | 108,537 | DONE 102.2 s | `/out/vm_dart_00.txt` |
| `vm_csharp_00` | A1 matrix | 99,405 | DONE 76.1 s | `/out/vm_csharp_00.txt` |

The two acceptance lanes are `ac_java.sh` and `ac_typescript.sh`; the
value-matrix lanes carry the `vm_` prefix, so the dart value-matrix lane
is `vm_dart_00` and the csharp one is `vm_csharp_00`.

### §8.2 RUNNING and QUEUED — the value matrix

Twenty-six shard lanes. The daemon is serial and runs them in the order
dropped, which is cost order. ETAs are **derived** from §6.2.

| lane group | shards | probes | projected remaining |
|---|---|---|---|
| java | shard 0 DONE 309 s, 1–3 queued | 333,015 | ~16 min |
| rust | shard 0 running, 1 queued | 205,504 | ~23 min |
| go | 2 queued | 167,884 | ~49 min |
| swift | 2 queued | 76,614 | ~54 min |
| kotlin | 6 queued | 253,028 | ~3.7 h |
| cpp | 6 queued | 229,900 | ~3.9 h |
| csharp | 3 queued | 298,215 | ~4 min |
| dart | 1 queued | 108,536 | ~2 min |
| load check, 9 lanes | 9 | 1,046 | ~21 s, queued last |
| **remaining total** | **32** | **1,673,742** | **~9.2 h** |

- **the whole matrix should be finished about 9.5 hours after this log
  is written** *(derived, and an upper bound: every settled shard so
  far has beaten its projection)*.

### §8.3 harvest, exactly

- Poll the value-matrix lane's own status file,
  `SandboxDesign/agent/status/vm_<lang>_<nn>.sh.status`.
  `state=done` plus `exit=0` is the signal to look. It is NOT evidence
  the lane finished — read the gate for that.
- Collect and fold:

```
cp SandboxDesign/agent/out/vm_*.txt \
   PRIVATE/PseudoCoupHQ/Research/\
kind_fuzz_clustering/raw/
cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering
python3 l3_matrix_read.py
```

- `l3_matrix_read.py` writes `valuematrix_<lang>.json` and
  `valuematrix_index.json`. It carries the same completeness gate the
  rest of phase 3 carries: expected probes from `matrix_plan.json`, a
  required `__SUMMARY__` line PER SHARD, `complete` and `completeness`
  written into the file, and a loud `!!` line for anything short.
- **Read `uniform_cells` and `split_cells` first.** Every split is a
  place where a statically checked language's verdict moved with the
  VALUE, and every one of them is a finding.
- Then collect the nine load-check lanes, `ld_<lang>_00.sh`, and
  classify the splits:

```
cp SandboxDesign/agent/out/ld_*.txt \
   PRIVATE/PseudoCoupHQ/Research/\
kind_fuzz_clustering/raw/
```

  The classification has two outcomes and they mean opposite things.

  - **A split whose differing value class ALSO refuses on the
    declaration-alone probe is layer 2 leaking in.** The holder could
    not hold that value.
  - **A split whose value class loads fine is layer 3 moving**, as
    opposed to the case above. That one is the finding proper.
  - Typescript's 876 are all the second kind *(measured)*. The other
    eight languages are open.

### §8.4 still open after this session

| item | why it is open | what it needs |
|---|---|---|
| route C for the nine checked languages | never built; the value matrix measures VERDICTS, not answers | compile-and-run over the ACCEPTED cells only, batched — accepted probes are known to compile, which is the one case log 025's batching argument survives (log 027 §2.3) |
| the java arithmetic lift | 146 disagreements recorded, unreconciled by rule | nothing, unless the owner wants the promotion step lifted as data too |
| swift's operator menu | 6 operations, a grammar fact (log 027 §5 item 5) | a menu source that is not the tree-sitter token list |
| `rust-src` persistence | installed to `/opt/rustup`, which a container rebuild loses | re-run `rustup component add rust-src` |
| the owner's review of phase 1 | log 024 §6, still gating nothing in practice | the owner |

---

## record

New this session, all in
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`:

- `l3_accept.py` — java and typescript templates added; a mechanical
  right-side type rename for java's two type-declaring holders.
- `l3_lanes.py` — `javac_inproc` and `ts_inproc` modes, with the two
  drivers carried inside the lane.
- `l3_matrix.py` -> `matrix_plan.json`, `lanes/vm_<lang>_<nn>.sh` — the
  full value matrix, sized, sharded and self-sweeping.
- `l3_matrix_read.py` -> `valuematrix_<lang>.json` — the fold, with the
  completeness gate.
- `cert_diff.py` -> `certification_{rust,java,go}.json` — the gate.
- `acceptance_java_A1.json`, `acceptance_typescript_A1.json`.
- `raw/ac_java.txt`, `raw/ac_typescript.txt`, `raw/lift_b_rust.txt`,
  `raw/VOID_lift_b_rust_run1.txt`.
- `HARVEST.md` — rewritten for the running matrix.
