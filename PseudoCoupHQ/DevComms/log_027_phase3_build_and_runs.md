# log 027 — layer 3 phase 3: the builds, proven, and the runs, launched

Date: 2026-08-18. Node:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`.
Phase 3 of that node's plan of record, under the layer-3 design the owner
ruled 2026-08-18.

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
    layer 1 is the DATA: fixed content with
    no language attached.  layer 2 is the
    HOLDERS: per language, the ways a running
    program can hold that content.  layer 3
    is the OPERATIONS: what the compiler can
    do to a loaded holder.
    example tied to context:
        this log serves layer 3, so every
        run in it asks a compiler about an
        operation applied to layer-2 holders.

form
    one of the layer-1 kinds of content:
    nothing, truth, whole number, fractional
    number, text, sequence, keyed grouping,
    nesting, identity mark.
    example tied to context:
        `int`, `Decimal` and `Fraction` are
        three holders of one form.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        go has 20 holders, so go's enumerated
        space is 400 ordered holder pairs.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        the `i64max` value class is what
        broke python's first route-C run: a
        sequence holder asked for a list of
        9.2e18 elements.

probe
    one small generated program that asks one
    language one question.
    example tied to context:
        the seven acceptance runs together
        sent 71,313 probes.

cell
    one combination of operand kinds that an
    operation was asked about.  a pair cell
    is one combination of two holders.
    example tied to context:
        go's `+` cell is the one thing this
        log certifies.

ordered pair
    two holders in a stated left-and-right
    order, kept in both orders and never
    folded together.
    example tied to context:
        `int32 << int64` and
        `int64 << int32` are two ordered
        pairs, and both were measured.

menu (a language's operation menu)
    the list of operations measured for one
    language.  it is taken mechanically from
    that language's own tree-sitter grammar
    rather than typed by hand.
    example tied to context:
        swift's menu comes out at 6
        operations where the other languages
        give 17 to 20.

generator
    the program that reads the layer-2 holder
    files and a grammar's token list and
    writes out every probe to be run.
    example tied to context:
        `l3_accept.py` is the acceptance
        generator; `l3_routec.py` is the
        route-C one.

lane
    one batch job.  it runs a planned set of
    probes and writes its output to one raw
    text file.  a lane has a short name.
    example tied to context:
        the go acceptance lane `ac_go.sh` ran
        7,600 probes in 132.6 seconds.

lane daemon
    the runner that takes dropped lane
    scripts and executes them one after
    another, serially.
    example tied to context:
        the launch order in §3.4 is the order
        the lane daemon worked through,
        kotlin last by design.

instrument
    the tool used to get a verdict or an
    answer for a probe.
    example tied to context:
        `progress.py` is this session's other
        sense of instrument: the shared
        progress printer every lane uses.

route A1, route A2, route B, route C
    the four ways of getting layer-3 evidence
    out of a language.  route A1 calls the
    compiler's own checker in-process as a
    library.  route A2 runs the compiler as a
    command with a check-only flag.  route B
    lifts the rule out of the compiler's own
    source or bytecode.  route C runs the
    program and watches what happens.
    example tied to context:
        csharp moved from route A2 to route
        A1 when the `-refonly` flag proved
        weak and the Roslyn library proved
        fast.

ACCEPT, REFUSE
    the two verdicts a checking run gives a
    probe.
    example tied to context:
        go's `+` accepts 7 ordered pairs of
        the 400 enumerated and refuses the
        rest.

the lift (a lifted rule, a lifted table)
    the route-B product: a rule or table read
    out of a compiler's own material rather
    than measured from its behaviour.
    example tied to context:
        go's lifted rule is
        `Identical(a,b) AND (a.info &
        (IsNumeric or IsString)) != 0`.

certification (a certified cell)
    diffing two routes' verdicts on the same
    cells.  a cell is certified when they
    agree everywhere; a disagreement is
    recorded as a finding and never
    reconciled quietly.
    example tied to context:
        go's `+` cell is certified; go's `<<`
        cell is a recorded disagreement.

the value matrix
    the full crossing of every operation with
    every ordered holder pair AND every value
    class, rather than one value class per
    holder.
    example tied to context:
        ruby's full value matrix is 261,382
        probes and ran in 2.8 seconds.

statically checked language,
open-dispatch language
    the two kinds this node splits on.  a
    statically checked language decides the
    verdict before running.  an open-dispatch
    language decides everything at run time,
    so nothing is refused before running.
    example tied to context:
        python, ruby and php are the three
        open-dispatch languages, and they are
        the three on route C.

bisect batching
    putting many probes in one file, and on a
    refusal splitting the file in half to
    find which probe refused.
    example tied to context:
        bisect batching took 796 compiles to
        settle 400 go probes.

per-file parallel
    the plain alternative to batching: one
    probe per file, many files compiled at
    once.
    example tied to context:
        per-file parallel settled the same
        400 go probes in 7.76 seconds and won
        the race.

shard, and the `__SUMMARY__` line
    one output chunk of a lane, ending in a
    line the driver prints that states how
    many probes that piece did.
    example tied to context:
        the completeness gate refuses to
        trust a result file whose
        `__SUMMARY__` line is missing.

completeness gate (also: gate)
    a check run when a lane's output is read.
    it compares the folded row count against
    holders squared times the operation menu,
    and requires the driver's own
    `__SUMMARY__` line.
    example tied to context:
        the gate is what caught 11,881 lost
        ruby rows in finding 11.

harvest, fold
    harvesting is collecting finished lanes
    off disk.  folding is reading that raw
    output and building the result files from
    it.
    example tied to context:
        `l3_read.py` is the folder, and
        `HARVEST.md` carries the collection
        commands.

QUARANTINED (a quarantined raw file)
    a raw file renamed so a reader cannot
    pick it up, kept as evidence of a failure
    rather than as a measurement.
    example tied to context:
        `raw/VOID_ac_rust_ebusy.txt` is
        quarantined.

EBUSY
    the operating system's "device or
    resource busy" error, number 16.
    example tied to context:
        `rustc --emit=metadata -o /dev/null`
        answers EBUSY on every accepting
        probe, because rustc writes metadata
        by rename.

SIGKILL, the out-of-memory killer
    the operating system's unstoppable stop
    signal, and the part of the system that
    sends it when memory runs out.  a program
    cannot catch it.
    example tied to context:
        python's first route-C run was
        SIGKILLed at 19,829 probes of
        342,225.

ruling <n>, finding <n>
    a ruling is a numbered instruction this
    node works under.  a finding is a
    numbered thing learned, kept so it can be
    cited by number.
    example tied to context:
        ruling 6 forbids interpretation;
        finding 11 is the delimiter fault in
        the result format.
```

---

## what came before this log, restated

Each fact this log borrows from an earlier log or from the node's plan
of record is stated here in full, so no sentence below depends on
opening another file.

- **Log 025 priced the whole node at about 435 hours of serial compiler
  time**, and put **206 of those 435 hours on kotlin alone**, over
  **302,796 kotlin probes**, at a cold cost of **2,397 ms per probe**.
- **Log 025 §4 projected 6.2 hours for the node if the probes were
  batched**, against the 435 serial, and called batching the settlement
  of the expensive tail.
- **Log 025 measured its batching amortisation of 33x to 103x on
  batches selected in advance to compile**, and said so plainly at the
  time.
- **Log 025 §5 named phase 0's swift probe count of 128 as the estimate
  to trust least.**
- **Log 025's design figure for the whole node was about 5.79 million
  probes.**
- **Log 025 estimated that adding the full value matrix costs under 1
  percent**, and ruling 3 was argued on that estimate.
- **Log 026 §2.1 recorded go's lifted rule** as `Identical(a,b) AND
  (a.info & (IsNumeric or IsString)) != 0`, read out of go's own
  `binaryOpPredicates` map, its predicates and its `BasicInfo` masks.
- **Log 026 §2.1 offered the go cross-check as an instructive
  counter-example**: a hand-re-assembled rule that AGREED with go, where
  the agreement did not make the transcription evidence.
- **Log 026 §2 recorded java's `Operators` table as 23 rows**, reported
  without a re-runnable extraction attached.
- **Log 026 finding 2 said that in an open-dispatch language the
  accepting set is decided entirely at run time.**
- **Log 026 finding 4 named go, typescript and java as the three
  compilers that ship a callable in-process checker.**
- **Ruling 3 is the ruling that the full value matrix is to be carried
  rather than pruned**, at the grain of form, holder and value class.
- **Ruling 6 forbids interpretation**: a hand-read rule is a draft until
  something else answers the same cells, and agreement alone is not
  evidence.
- **Ruling 7 demanded a measured mitigation for kotlin's cost**, rather
  than an assumed one.
- **The node's CORE recorded route A2 as UNVERIFIED for kotlin, swift,
  dart and csharp**, and forbade assigning it to any of them before
  proof.
- **The CORE's engineering crux says to batch the probes and bisect on
  refusal**, and this session was told to settle that question by
  measurement.
- **Go's own source carries the same-type requirement at `expr.go:809`,
  as `if !Identical(x.typ, y.typ)`**, and its `binaryOpPredicates` map
  has rows for `+ - * / % & | ^ &^ && ||` and none for `==` or `!=`.

---

## §1 — walkthrough, in plain words

**What this session was for.**

- The ruled layer-3 design asks for four things at once: full
  enumeration of ordered operand pairs over layer-2 holders, the full
  value matrix, progress print-outs everywhere, and all four evidence
  routes pursued together.
- Four things had to be BUILT and PROVEN before any of that could be
  paid for.
- The instruction was explicit that the expensive runs must not start
  until they were.
- So the session went in that order: build, prove, then run.

**The instrument.**

- A shared progress module now exists in two faces: a python class, and
  its POSIX-shell twin.
- Every generator, every lane and every reader in this node now prints
  `[done/total]`, elapsed time, and an ETA taken from the running mean.
- It flushes on every tick, so a half-finished lane log can be read
  while the lane is still working. That was the point.

**Route A2, verified per language.**

Proof here meant three things at once: a known-accepting probe gets an
ACCEPT, a known-refusing probe gets a REFUSE, and code generation is
demonstrably skipped — checked by artifact absence and by the clock
against the full-codegen baseline. Three of the four candidates came
back proven. One came back refuted, which is the more useful result.

- **swift, proven.** `swiftc -typecheck` is real. Correct verdicts both
  ways, **no artifact written at all**, 177 ms accepting against the
  full compile's 255 ms *(measured)*.
- **dart, proven, and it was the session's biggest single saving.**
  `dart analyze` does not stop at the first refusal. A whole DIRECTORY
  analyses in one invocation and every file gets its own diagnostic
  line: 100 probes in **131 ms**, which is **1.3 ms per probe** against
  `dart run`'s 138 ms — a **105-fold** drop, with all 50 refusing files
  named and all 50 accepting files silent *(measured)*.
- **csharp, proven, but on a different route than expected.** The
  check-only FLAG is a dud: `-refonly` saves 23 percent and no more. The
  compiler ships its own checker as a callable library instead, so
  csharp moves up from route A2 to route A1. An in-process Roslyn driver
  settled **200 probes in 288 ms — 1.44 ms each — with all 200 verdicts
  correct**, against `csc`'s 344 ms per probe. That is **239-fold**
  *(measured)*.
- **kotlin, refuted.** **There is no check-only route, and that is now
  measured rather than assumed.** The compiler's own extended help
  offers nothing that skips JVM code generation while keeping the type
  check. Route A2 is REFUTED for kotlin. What works instead is holding
  one JVM open and calling the compiler in-process: **123 ms per probe
  against 2,463 ms cold, a 20-fold drop** *(measured)*. Kotlin's
  206-hour worst case was the single largest line in log 025's bill, and
  this is the measured mitigation ruling 7 demanded.

**The batching question, raced — and log 025's prediction lost.**

The CORE's engineering crux says to batch the probes and bisect on
refusal. Three arms were run over the same 400 go probes and their
verdicts compared.

- **Per-file serial:** 22.4 s *(measured)*.
- **Per-file parallel:** 7.8 s *(measured)*.
- **Batched 100 with bisect:** **42.2 s** *(measured)*.

Batching is **5.4 times slower than per-file parallel and 1.9 times
slower than plain serial**. The cause is measured and it is structural.

- Under full enumeration **375 of the 400 probes refuse**.
- A bisect over a mostly-refusing batch does not converge. It took
  **796 compiles to settle 400 probes**, which is worse than one compile
  each.
- Log 025 measured its 33x-to-103x amortisation on batches selected in
  advance to compile. This is what happens when that selection is
  removed.
- All three arms agreed on all 400 verdicts. So the batcher is correct,
  and it is simply not worth using.
- The runs were built on per-file parallel instead. The one exception is
  a check-only route that batches natively without bisecting at all,
  which is exactly what dart does.

**The generators.**

- The probe space is now enumerated from the layer-2 holder files and
  the grammars' own operator menus.
- It is enumerated at the grain the ruling demands: every row carries
  form, holder and value class.
- Ordered pairs are kept in both orders and nothing is pruned.
- The sizes were printed before anything ran, which is the order the
  node asks for.

**The headline numbers.**

- Seven acceptance lanes and three route-C lanes were generated and
  launched in cost order, kotlin last.
- **All seven acceptance runs are now complete: 71,313 probes, 5,842
  accepted, 65,471 refused, 1,644 seconds of wall time in total**
  *(measured)*.
- Two of the three route-C runs are complete as well: ruby's full value
  matrix, 261,382 probes in 2.8 seconds, and php's, 215,306 in 0.8
  *(measured)*.
- Python's route-C run is re-running after an out-of-memory kill,
  roughly a quarter of an hour from done.
- Counting what has landed, this phase has measured **558,001 probes**
  across nine of the twelve languages.

**Three lanes died silently and all three exited zero.**

- **Rust.** Its first run answered EBUSY on every accepting probe and
  reported 0 accepts of 9,196.
- **Php.** Its driver hit an uncatchable `Cannot redeclare class` fatal
  and stopped at 2,001 of 215,306.
- **Python.** Its run was SIGKILLed by the out-of-memory killer at
  19,829 of 342,225. A probe pairing a sequence holder with the
  `i64max` value class asks for a list of 9.2e18 elements, and the
  two-second signal budget cannot interrupt an allocation.
- All three were found, fixed and re-run *(measured)*.
- The lesson is now BUILT IN rather than written down: the reader
  carries a completeness gate, and every result file states whether it
  is complete.
- **A lane's exit code is not evidence that it finished.** That is the
  single most transferable thing this session learned.

**The cost picture inverted.**

- Kotlin has been the villain of this node's budget since log 025 put
  206 of 435 hours on it.
- At full scale kotlin measured 52.1 ms per probe. That is better than
  the 123 ms the build step predicted, because a held-open JVM keeps
  warming.
- **C++, at 60.9 ms, is now the most expensive compiler per probe of the
  seven** *(measured)*.
- Dart came in at 0.98 ms and csharp at 1.51.

**And the certification gate earned its keep on its first use.**

- **The agreeing cell.** Go's `+` acceptance set measured 7 pairs, every
  one of them same-holder and numeric-or-string. That is precisely what
  the lifted go map predicts, so that cell is certified.
- **The disagreeing cells.** Go's `<<` accepted **16** pairs, of which
  only 4 are same-holder. Go's `==` accepted **36**, of which 24 pair a
  value against a bare `nil`. The lifted rule as recorded in log 026
  cannot produce either set.
- The lift is not wrong. It is INCOMPLETE, and only diffing it against
  the compiler's own verdicts revealed that.
- This is ruling 6's counter-example argument confirmed from the other
  side. Agreement on `+` did not make the transcription evidence.
  Disagreement on `<<` is what a transcription's silence looks like.

---

## §2 — build results

### §2.1 the instrument

`Research/kind_fuzz_clustering/progress.py` holds two faces of one
thing.

- **The python face** is a `Progress` class, used host-side.
- **The shell face** is `SH_PROGRESS`, a POSIX-shell twin meant for
  pasting into a lane script. A lane cannot import the file, because the
  runner cannot see the repo.

Both print `[done/total]`, elapsed, and an ETA from the running mean,
and both flush every tick. They are used by `l3_accept.py`,
`l3_read.py`, every `ac_*.sh` acceptance lane, every `rc_*.sh` route-C
lane, the route-A2 verification lane `a2_verify.sh`, and the batch race
lane `bisect_race.sh`. Verified by reading progress lines out of a lane
log **while the lane was still running** *(measured)*.

### §2.2 route A2, verified per language

All timings are means over 3 repetitions inside the container, with the
two `date` forks subtracted. Kotlin is 1 repetition because it is slow.
All **measured**.

| language | candidate route | accepting probe | refusing probe | cost accepting (ms) | cost refusing (ms) | full-codegen baseline (ms) | codegen skipped | verdict |
|---|---|---|---|---|---|---|---|---|
| swift | `swiftc -typecheck` | correct, rc 0 | correct, rc 1 | 177 | 144 | 255 | yes — no artifact written | **A2 PROVEN** |
| dart | `dart analyze` | correct, rc 0 | correct, rc 3 | 185 | 67 | 138 (`dart run`) | yes — analyser only | **A2 PROVEN** |
| dart | `dart analyze <dir>`, 100 files | 50 of 50 silent | 50 of 50 named | 1.3 per probe | 1.3 per probe | 138 | yes | **A2 PROVEN, and it batches** |
| csharp | `csc -refonly` | correct | — | 264 | — | 344 | partly — writes a reference assembly | weak, not taken |
| csharp | Roslyn in-process `GetDiagnostics` | 100 of 100 correct | 100 of 100 correct | 1.44 per probe | 1.44 per probe | 344 | yes — nothing emitted | **A1 PROVEN** |
| kotlin | any `-X` check-only flag | — | — | — | — | 2,463 | n/a | **A2 REFUTED — no such flag** |
| kotlin | `K2JVMCompiler.exec` in-process, warm JVM | correct, `OK` | correct, `COMPILATION_ERROR` | 123 per probe | 123 per probe | 2,463 | no — still emits | **mitigation PROVEN, 20x** |
| rust | `rustc --emit=metadata` | correct | correct | 15 | 25 | 54 | yes — metadata only | already assigned; confirmed |
| cpp | `g++ -fsyntax-only` | correct | correct | 12 | 10 | 33 | yes — no artifact | already assigned; confirmed |

Three things worth saying in words.

- **Kotlin's refutation is the useful half.** The CORE told us to verify
  before assigning. Verifying found there is nothing to assign. What
  replaced the flag is not another flag but a posture: one JVM, held
  open, called in-process. It is measured at 123 ms per probe. Applying
  that to log 025's 302,796 kotlin probes gives **10.4 hours against
  206** *(derived)*.
- **Csharp and kotlin both ended up on route A1, not route A2.** In both
  cases the compiler ships its checker as a callable library, and the
  in-process call beats every flag by two orders of magnitude. That is
  log 026 finding 4 generalising further than it was stated.
- **Dart is the only one that batches natively.** The distinction that
  matters is not check-only against full-build. It is whether the tool
  ABORTS at the first refusal.
  - **A tool that reports every file:** `dart analyze` names every
    refusing file, so a directory is one invocation and no bisect is
    needed.
  - **A tool that stops early:** `swiftc -typecheck` over 20 files
    reported only 1 of the 10 refusing files *(measured)*, so swift gets
    no batching benefit and runs per-file.

### §2.3 the batch race

Arms run over the SAME 400 go probes, in one container, serially, with
verdicts compared across arms. All **measured**.

| arm | wall time (s) | per probe (ms) | compiles invoked | disagreements with arm 1 |
|---|---|---|---|---|
| 1 — per-file, serial | 22.44 | 56.1 | 400 | — |
| 2 — per-file, parallel (12 workers, 6 cpus) | 7.76 | 19.4 | 400 | 0 of 400 |
| 3 — batched 100 per file, split-on-refusal bisect | 42.15 | 105.4 | **796** | 0 of 400 |

Verdict distribution over the 400: **25 accept, 375 refuse**
*(measured)*.

Speed ratios *(derived)*: parallel is **2.9x** serial; batching is
**0.5x** serial and **0.2x** parallel. **Winner: per-file parallel.**

The mechanism, stated plainly.

- A bisect pays `log2(batch)` compiles to isolate ONE refusal.
- **When refusals are rare** that is a bargain, and log 025 measured the
  bargain.
- **When refusals are 94 percent of the batch** the bisect degenerates
  into a full binary walk of the batch, and a full binary walk costs
  about `2n` compiles rather than `n`. 796 for 400 is that factor of
  two, measured.
- Full enumeration guarantees the refusing majority. That is the whole
  point of enumerating rather than selecting.
- So batching and full enumeration are, on this evidence, in tension.
- The CORE's engineering crux is answered: bisect batching is BUILT, it
  is CORRECT, and it is not the thing to use.

### §2.4 the generators and the enumerated space

The acceptance generator `l3_accept.py` does three things in order.

- It reads the layer-2 holder files and each grammar's own positioned
  anonymous tokens.
- It intersects that token list with a candidate layer-3
  binary-operation vocabulary. The intersection is mechanical: nothing
  that a grammar does not declare survives it.
- It enumerates every ORDERED holder pair against every operation.

Counts printed before any run *(all derived from measured artifacts)*:

| language | holders | operations | ordered pairs | acceptance probes | full value-matrix answer probes |
|---|---|---|---|---|---|
| go | 20 | 19 | 400 | 7,600 | 167,884 |
| rust | 22 | 19 | 484 | 9,196 | 205,504 |
| cpp | 24 | 19 | 576 | 10,944 | 229,900 |
| swift | 24 | 6 | 576 | 3,456 | 76,614 |
| dart | 25 | 17 | 625 | 10,625 | 217,073 |
| csharp | 30 | 20 | 900 | 18,000 | 397,620 |
| kotlin | 26 | 17 | 676 | 11,492 | 253,028 |
| python (route C) | 24 | 25 | 576 | — | full matrix, run in one process |
| ruby (route C) | 22 | 22 | 484 | — | full matrix, run in one process |
| php (route C) | 19 | 26 | 361 | — | full matrix, run in one process |

Two notes on the shape of this table.

- **The acceptance grain and the answer grain are different, and the
  split is not a quiet pruning of ruling 3.**
  - In a statically checked language the VERDICT is a function of the
    holder pair and the operation. The value class changes the ANSWER,
    not the verdict.
  - So the acceptance runs enumerate pairs fully and carry one value
    class per holder.
  - The full value matrix is what route C multiplies. The right-hand
    column of the table above is that multiplication, counted, not
    estimated away.
  - For the three open-dispatch languages the two grains coincide,
    because there the verdict IS produced at run time. Those three run
    the full matrix.
- **Swift's operation menu is 6, not 19, and that is a grammar fact,
  not a bug in the generator** *(measured)*.
  - Swift's tree-sitter grammar does not declare `+`, `-`, `*` and the
    rest as anonymous tokens. It parses them through a `custom_operator`
    rule instead.
  - So the mechanical intersection with the grammar's own token list
    returns almost nothing.
  - It is recorded as a finding in §5, not patched by hand. Patching it
    by hand is exactly the interpretation ruling 6 forbids.

---

## §3 — what ran, what is running, what is pending

**Amended 2026-08-18, later the same day.** The lanes §3.2 listed as
running have since finished and been harvested. Three of them had to be
re-run after silent failures (§5). What follows is the harvested state,
not the launch state. The launch-state table is kept below as §3.4,
because the ETAs in it are what the later measurements are checked
against.

### §3.1 acceptance runs — ALL SEVEN COMPLETE

Every row **measured**. "per probe" is wall time divided by probes and
includes the lane's own setup.

| language | route | probes | accept | refuse | wall time | per probe |
|---|---|---|---|---|---|---|
| go | A2 `go build`, per-file parallel | 7,600 | 179 | 7,421 | 132.6 s | 17.4 ms |
| rust | A2 `rustc --emit=metadata`, parallel | 9,196 | 236 | 8,960 | 62.7 s | 6.8 ms |
| cpp | A2 `g++ -fsyntax-only`, parallel | 10,944 | 1,102 | 9,842 | 666.3 s | 60.9 ms |
| swift | A2 `swiftc -typecheck`, parallel | 3,456 | 80 | 3,376 | 146.7 s | 42.5 ms |
| dart | A2 `dart analyze <dir>` | 10,625 | 1,170 | 9,455 | 10.4 s | 0.98 ms |
| csharp | A1 Roslyn in-process | 18,000 | 1,127 | 16,873 | 27.2 s | 1.51 ms |
| kotlin | A1 in-process, warm JVM | 11,492 | 1,948 | 9,544 | 598.5 s | 52.1 ms |
| **total** | — | **71,313** | **5,842** | **65,471** | **1,644 s** | — |

Every one of the seven passes the completeness gate. Probes folded
equals holders squared times the operation menu, and each lane wrote its
summary line.

Two of the build step's predictions are now checked against the real
runs *(derived)*:

| language | §2.2 predicted per probe | measured at full scale | outcome |
|---|---|---|---|
| dart | 1.3 ms | 0.98 ms | beat it by 25 percent |
| csharp | 1.44 ms | 1.51 ms | held, within 5 percent |
| kotlin | 123 ms | 52.1 ms | beat it by 2.4x |

Kotlin is the one worth saying in words.

- The build step measured 123 ms per probe on a warm JVM over a short
  run.
- Across 11,492 probes the same posture measured **52.1 ms**, because
  the JIT keeps warming and the class loading is paid once.
- Against log 025's 2,397 ms cold figure that is a **46-fold** drop, and
  kotlin's 206-hour worst case becomes **4.4 hours** *(derived)*.
- Kotlin was not the long pole in the end. C++ was.

### §3.2 route C runs

**ALL THREE COMPLETE.** Every row **measured**.

| language | route | probes | answers | raises | refusals | budget | wall time |
|---|---|---|---|---|---|---|---|
| python | C, full value matrix | 342,225 | 100,597 | 241,450 | 0 | 178 | 381.8 s |
| ruby | C, full value matrix | 261,382 | 60,428 | 200,954 | 0 | — | 2.8 s |
| php | C, full value matrix | 215,306 | 94,690 | 120,616 | 0 | — | 0.8 s |
| **total** | — | **818,913** | **255,715** | **563,020** | **0** | **178** | **385.4 s** |

Each of the three folds EXACTLY to the count its own driver printed —
342,225, 261,382 and 215,306. That is the completeness gate of §5.1
finding 6 doing its job on the first data it was pointed at.

The two open-dispatch languages that finished in seconds, set against
the one that did not:

- **Ruby and php.** Each ran the FULL value matrix in one process in
  under three seconds. That is the ruling-3 cost question answered from
  the other end: the full matrix for the two of them together is 476,688
  probes and **3.6 seconds** *(measured)*.
- **Python.** It is slower by two orders of magnitude — 381.8 s, 1.1 ms
  per probe. The reason is in its answers. Python is the only one of the
  three that has to be stopped, 178 times, by the two-second budget.

Counting acceptance and execution together, this phase measured
**890,226 probes** across all twelve languages' worth of lanes that
exist *(derived)*. Log 025's design figure was about 5.79 million for
the whole node. The difference is the full value matrix in the nine
statically checked languages, which is counted but unbuilt (§3.5).

Note the refusal column. It reads zero, and that is the expected shape
rather than a gap.

- In an open-dispatch language nothing is refused at compile time.
- So every probe either answers or raises.
- Route C is the only acceptance evidence these languages have, and it
  says the accepting set is decided entirely at run time. That is log
  026 finding 2, measured.

### §3.3 route B lift

| lift | rows extracted | status | wall time |
|---|---|---|---|
| go `binaryOpPredicates` + predicates + BasicInfo masks | the literal map, 12 token rows | DRAFT, then certified/disagreed per §4 | 0.3 s |
| java `Operators` table via `javap -c` | **86** rows | DRAFT — no java route-A run exists to diff against | (same lane) |
| rust `Add` impl lists via `rust-src` | **0 — did not run** | rust-src is ABSENT in the container | (same lane) |

### §3.4 the launch-state table, kept for the record

The lane daemon is serial, so these ran one after another in the order
listed. ETAs were **derived** from the measured per-probe costs in §2.2,
except where a live progress line gave a better figure. Compare against
§3.1 for how the estimates held.

| language | route | probes | state at launch | ETA from launch |
|---|---|---|---|---|
| cpp | A2 `g++ -fsyntax-only`, parallel | 10,944 | RUNNING, 25 percent at 2m07s, 46.8 ms/probe measured live | ~8.5 min |
| swift | A2 `swiftc -typecheck`, parallel | 3,456 | queued | ~1.7 min |
| dart | A2 `dart analyze <dir>`, 500 per invocation | 10,625 | queued | ~1 min |
| csharp | A1 Roslyn in-process | 18,000 | queued | ~1 min |
| kotlin | A1 in-process, warm JVM | 11,492 | queued, LAST by design | ~24 min |
| — | B lift (go, java, rust) | — | queued | ~1 min |
| python | C, full value matrix | 576 ordered pairs x matrix | queued | ~20 min, estimate |
| ruby | C, full value matrix | 484 ordered pairs x matrix | queued | ~25 min, estimate |
| php | C, full value matrix | 361 ordered pairs x matrix | queued | ~15 min, estimate |
| rust | A2 `rustc --emit=metadata` | 9,196 | re-launched after harness fix | ~1 min |

### §3.5 pending — not built

| item | why | what it needs |
|---|---|---|
| java, route A1 (`javax.tools`) | not written | an in-memory `JavaFileObject` driver plus a `LANG` entry in the generator; ESTIMATE single-digit ms per probe by analogy with the measured Roslyn figure |
| typescript, route A1 (shipped checker) | not written | a node driver over `typescript.js`'s `Program`/`getSemanticDiagnostics`; same generator change |
| rust route-B lift | `rust-src` is absent in the container *(measured)* | `rustup component add rust-src`, then re-drop `lift_b.sh` |
| full value matrix for the nine checked languages | route C is not built for them | counts already derived per language; see `space_summary.json` |

`Research/kind_fuzz_clustering/HARVEST.md` carries the exact collection
commands and the state of every lane.

---

## §4 — route overlap: what got certified, what disagreed

Only one overlap could be evaluated inside the session. It is go, where
route A2 finished and route B's rule is already recorded in log 026
§2.1. Both are reported below. The route-B lift lane for java and rust
was still queued.

### §4.1 certified — go, the `+` cell

Route A2 measured go's `+` accepting exactly **7** ordered holder pairs
of the 400 enumerated, and every one of the 7 is same-holder
*(measured)*:

| operation | accepting pairs |
|---|---|
| `+` | int32+int32, int64+int64, uint64+uint64, int+int, float64+float64, float32+float32, string+string |

The lifted rule recorded in log 026 §2.1 is `Identical(a,b) AND
(a.info & (IsNumeric or IsString)) != 0`. Applied to this holder
vocabulary it yields the same seven and no others *(derived)*. **The
cell is CERTIFIED**: the lift and the compiler's own verdicts agree on
every one of the 400 pairs for this operation.

### §4.2 disagreement one — the shifts

| operation | pairs accepted, measured | of which same-holder | what the recorded lift predicts |
|---|---|---|---|
| `<<` | 16 | 4 | 4 |
| `>>` | 16 | 4 | 4 |

The twelve extra, worked *(measured)*, given as left holder, operation,
right holder:

| left holder | operation | right holder |
|---|---|---|
| int32 | `<<` | int64 |
| int32 | `<<` | uint64 |
| int32 | `<<` | int |
| uint64 | `<<` | int32 |
| uint64 | `<<` | int64 |
| uint64 | `<<` | int |
| int64 | `<<` | int32 |
| int64 | `<<` | uint64 |
| int64 | `<<` | int |
| int | `<<` | int32 |
| int | `<<` | int64 |
| int | `<<` | uint64 |

**Finding.**

- The recorded lift carries the same-type requirement — go's own
  `expr.go:809`, `if !Identical(x.typ, y.typ)` — as an unconditional
  part of the rule.
- The measurement says shifts are exempt from it. A shift's two operands
  may be different whole-number holders.
- So the lift is INCOMPLETE, not wrong. There is a branch upstream of
  the identity check that log 026's reading did not carry out with the
  map.
- It is recorded as a finding. Nothing is reconciled.
- The route-B go table stands as a **draft** for `<<` and `>>`, and as
  **certified** for `+`.

### §4.3 disagreement two — equality has no row at all

| operation | pairs accepted, measured | of which same-holder | what the recorded lift predicts |
|---|---|---|---|
| `==` | 36 | 12 | nothing — the map has no entry for this token |
| `!=` | 36 | 12 | nothing |

The twenty-four cross-holder accepts all pair a value against a bare
`nil` held in an empty interface, in both orders *(measured)*. Six
examples, given as left holder, operation, right holder:

| left holder | operation | right holder |
|---|---|---|
| bool | `==` | nil (interface{}) |
| int64 | `==` | nil (interface{}) |
| string | `==` | nil (interface{}) |
| struct | `==` | nil (interface{}) |
| container/list.List | `==` | nil (interface{}) |
| nil (interface{}) | `==` | *int64 (typed nil pointer) |

**Finding.**

- `binaryOpPredicates` has rows for `+ - * / % & | ^ &^ && ||` and none
  for `==` or `!=`.
- Equality in go is decided by a comparability rule on a different path
  entirely.
- A lifter that stops at that map therefore produces NO verdict for the
  two operations that accept the most pairs of any in the language — 36
  each, against `+`'s 7.
- This is the sharpest form of the certification gate's value. The
  lift's failure here is not a wrong answer. It is a SILENCE, and a
  silence is invisible until something else answers.

### §4.4 corroboration — java's lifted table confirms the go shift finding

This one is the most useful thing in §4, because it is two independent
routes, in two different languages, agreeing on a structural fact that
neither was looking for.

§4.2 found by MEASUREMENT that go exempts shifts from its same-type
requirement. The java route-B lift was extracted MECHANICALLY from
`javap -c` output, with no reading of java source at all. It contains
these rows *(measured)*:

```
java.row|SL|INT|INT|INT
java.row|SL|INT|LONG|INT
java.row|SL|LONG|INT|LONG
java.row|SL|LONG|LONG|LONG
java.row|SR|INT|INT|INT
java.row|SR|INT|LONG|INT
java.row|SR|LONG|INT|LONG
java.row|SR|LONG|LONG|LONG
```

Two kinds of tag in that table, set against each other:

- **The other arithmetic tags** — MINUS, MUL, DIV, MOD, LT, GT, EQ —
  carry ONLY same-type rows.
- **The shift tags** — SL and SR — are the sole exception, and they
  carry the mixed rows explicitly.

So java's own literal data says what go's own compiler said: **a shift's
two operands need not be the same whole-number holder, while every other
arithmetic operation's must be.**

The measured acceptance runs make it four languages *(measured, from
§3.1's per-operation breakdown)*:

| language | `<<` accepts | of which same-holder | route |
|---|---|---|---|
| go | 16 | 4 | A2, measured |
| rust | 16 | 4 | A2, measured |
| csharp | 18 | 3 | A1, measured |
| cpp | 25 | 5 | A2, measured |
| java | — | — | B lift only: mixed rows present |

**Finding.**

- The shift exemption is not a go quirk.
- It is a shared shape across five of the languages measured.
- It is the first cross-language behavioral regularity this node has
  produced from layer-3 evidence, and it is exactly the kind of cell
  phase 4 clusters on.
- It is recorded as a finding, at level measured for the four with
  acceptance runs, and DRAFT for java, which has no route-A run to
  certify its lift against.

### §4.5 disagreement three — java's table is 86 rows, not 23

Two counts of the same table, side by side:

- **Log 026 §2 recorded java's `Operators` table as 23 rows.** It was
  reported without a re-runnable extraction attached.
- **This session's `lift_b.sh` returned 86 rows** *(measured,
  `java.row_count=86`)*, over 19 distinct operation tags.

**Finding.**

- The two numbers come from the same table in the same JDK, and only one
  of them can be right.
- Nothing here reconciles them. The discrepancy is recorded.
- The 86-row extraction is the one carried forward, because it is the
  one produced mechanically and re-runnable. `raw/lift_b.txt` holds
  every row.
- Both are DRAFT until a java route-A1 run exists to diff against, which
  is precisely the harness §3.5 says is not built.

### §4.6 certified by accident — the rust EBUSY count

- The void rust run of §5 reported 0 accepts of 9,196, because every
  ACCEPTING probe died with `Device or resource busy (os error 16)`.
- That error was counted before the re-run: **236** *(measured)*.
- The fixed re-run then measured **236 accepts** of the same 9,196
  *(measured)*.

The two numbers match exactly. That is a small certification of its own,
and it is worth writing down for a reason beyond tidiness.

- It proves the void run's failure was a pure ACCEPT-MASK. It converted
  every accept into a refusal and touched nothing else.
- A failure mode that is total and uniform is recoverable.
- A failure mode that is partial would not have been.

### §4.7 what this does to ruling 6

Log 026 §2.1 offered the go cross-check as the instructive
counter-example: a hand-re-assembled rule that AGREED with go, where the
agreement did not make it evidence. §4.1 to §4.3 are the same argument
completed.

- The re-assembled rule agreed on the operation it was read for.
- The re-assembled rule was silent or wrong on two operations it was not
  read for.

Ruling 6 holds. The certification gate is not a formality: on its first
use it caught two gaps in a lift that had already been reported as
correct.

---

## §5 — surprises

Five, in the sense the line uses: things the earlier logs did not
already contain.

1. **Batching lost the race it was predicted to win.** Log 025 §4
   projected 6.2 hours batched against 435 serial, and called batching
   the settlement of the expensive tail. Measured against full
   enumeration on go, batching is **1.9x SLOWER than plain serial and
   5.4x slower than per-file parallel**. The cause is that the refusing
   majority full enumeration guarantees turns a bisect into a full
   binary walk — 796 compiles for 400 probes *(measured)*. The two
   rulings sit in tension with each other: enumerate fully, and batching
   stops paying. Log 025 flagged the assumption honestly; this is the
   assumption failing.
2. **Two compilers moved UP a route, from A2 to A1.** Csharp and kotlin
   were both listed as route-A2 candidates awaiting a flag. Neither has
   a usable flag. Both ship a callable checker instead. Csharp went from
   344 ms per probe to **1.44**, and kotlin from 2,463 to **123**
   *(measured)*. Log 026 finding 4 named go, typescript and java as the
   in-process three; it is at least five.
3. **The batching lever that DID work is not batching, it is a tool
   that refuses to abort.** `dart analyze` over a directory settles 100
   probes in 131 ms with per-file diagnostics, because it reports every
   file instead of dying on the first. `swiftc -typecheck` over 20 files
   reported 1 of 10 refusals *(measured)*. The useful property is
   error-recovery, not batch size, and no one predicted that.
4. **Go's most permissive operations are the ones the lifted table does
   not mention.** `==` and `!=` accept 36 ordered pairs each. `+`
   accepts 7 *(measured)*. The acceptance data most worth having is
   precisely the part route B is silent on.
5. **A grammar can fail to declare its own operators.** Swift's
   tree-sitter grammar yields 6 operations to the mechanical
   intersection, where the other languages yield 17 to 20. The cause is
   that swift parses `+` through a `custom_operator` rule rather than as
   an anonymous token *(measured)*. Phase 0's swift probe count of 128 —
   which log 025 §5 already named as the estimate to trust least — has
   the same cause. Swift's layer-3 menu cannot be taken off its grammar
   the way the other eleven can. That is a fact about the instrument,
   recorded rather than patched.

One smaller one, recorded because it cost a run.

- `rustc --emit=metadata -o /dev/null` fails with EBUSY on every
  ACCEPTING probe, because rustc writes metadata by rename.
- The failure is silent in the sense that matters: it looks exactly like
  a refusal.
- The lane reported 0 accepts of 9,196 without erroring *(measured)*.
- A route that can only report refusals will always agree with a
  refusing majority. That is a general hazard of this phase, and it is
  why every lane's accept count should be read before its verdicts are.

### §5.1 — the harvest surprises, added later the same day

Six more, from the completed runs.

6. **The silent-truncation failure is a PATTERN, not an incident.**
   The rust EBUSY above was written up as a one-off. It was not. Three
   lanes died mid-run and **all three exited 0** *(all measured)*:

   | lane | how it died | probes done | probes wanted | share |
   |---|---|---|---|---|
   | rust A2 | `-o /dev/null` EBUSY on every accept | 9,196 "refusals" | 9,196 | accepts masked |
   | php C | `Cannot redeclare class R0` FATAL | 2,001 | 215,306 | 0.9 percent |
   | python C | SIGKILL, out of memory | 19,829 | 342,225 | 5.8 percent |

   Three different causes, one shared shape: a partial result that
   looks like a complete one. Two of the three would have entered the
   tables as measurements. The mitigation is now BUILT rather than
   remembered. The reader `l3_read.py` carries a **completeness gate**:
   it compares folded rows against holders-squared-times-operations,
   requires the driver's own final summary line, writes `complete` and
   `completeness` into every result file, and prints a loud `!!` line.
   All ten current result files pass or are labelled. The general rule
   this phase earns: **a lane's exit code is not evidence that it
   finished.**

7. **C++ was the long pole, not kotlin.** The whole cost design of this
   node has pointed at kotlin since log 025 put 206 of the 435 hours on
   it. Measured at full scale, kotlin ran 11,492 probes in **598 s** and
   c++ ran 10,944 in **666 s** *(measured)*. C++ is now the most
   expensive compiler per probe of the seven, at 60.9 ms against
   kotlin's 52.1. The in-process posture moved kotlin from worst to
   middling, and nobody re-checked which language then held the title.

8. **The spread on `&&` is 112-fold, and it is the widest spread
   measured anywhere in this run.** Accepting ordered pairs for logical
   and *(measured)*: cpp **112**, dart 4, go 1, rust 1, csharp 1,
   kotlin 1, swift 1. The two sides of that spread:
   - **C++ converts almost any holder to `bool` implicitly**, so
     `std::map && std::vector` type-checks.
   - **The other six demand an actual truth holder on both sides.**

   One operation, same probe design, and the acceptance sets differ by
   two orders of magnitude. This is the sharpest single cell for phase
   4's contradicts relation that the run produced.

9. **Dart's `==` accepts 576 of its 625 ordered pairs, and 388 of
   dart's 1,170 total accepts involve a `dynamic` operand** — including
   `dynamic null * dynamic null`, which ACCEPTS *(measured)*. Dart's
   static route reports acceptance for operations whose real verdict is
   deferred to run time, because `dynamic` switches the checker off.
   **This matters for comparison**: dart's A2 numbers are not the same
   kind of measurement as go's, and putting them in one table without
   this note would overstate dart's permissiveness. It is recorded here
   so phase 4 does not read it flat. The honest reading is that dart
   needs a route-C run to say what it actually does, and it does not
   have one.

10. **Kotlin's elvis `?:` accepts 673 of 676 ordered pairs — the most
    permissive single operation measured in any language** *(measured)*,
    ahead of dart's `==` at 576 and csharp's `??` at 77. Null-handling
    operations cluster at the permissive end everywhere they exist,
    which is a shape worth carrying into phase 4.

11. **The result format delimits with the same character that is one
    of the operations it records.** Probe ids end with the operation,
    and most menus contain a bare `|`, so a left split on `|` tears the
    id of every `|` and `||` probe apart. It cost exactly one
    operation's rows per language before it was caught — **11,881 in
    ruby and 8,281 in php**, found only because the driver's own printed
    total disagreed with the folded count *(measured)*. It is fixed in
    `l3_read.py` by locating the verdict word rather than counting
    delimiters, and all three route-C files now fold to their driver's
    exact total. It is worth recording as its own item for two reasons.
    It is the fourth silent-loss failure of the session. And it is the
    only one on the READING side rather than the running side — the lane
    was perfectly healthy and the data was still being dropped.

12. **Ruby and php ran the full value matrix in 3.6 seconds together**
    — 476,688 probes *(measured)*. Ruling 3 was argued on log 025's
    estimate that the full matrix adds under 1 percent. For these two
    the full matrix is not a cost at all. The languages where the value
    matrix is genuinely expensive are the nine checked ones, and those
    are exactly the ones where it is not yet built.

---

## §6 — what remains, and how to harvest

### §6.1 remaining

**Amended after the harvest. EVERY LANE IS DONE.** Nothing is running
in the container. What is left is build work, not harvest work:

1. **java and typescript route-A1 harnesses, NOT built** (§3.5). These
   are the two remaining languages of the twelve with no layer-3
   acceptance evidence at all. Java is the more valuable of the two,
   because its route-B lift already exists and cannot be certified
   without it (§4.5).
2. **the rust route-B lift did not run** — `rust-src` is ABSENT in the
   container *(measured)*, which contradicts the working assumption that
   it was installed. The fix is `rustup component add rust-src`, then
   re-drop the lift lane `lift_b.sh`. Rust's acceptance side is complete
   and waiting, so this is one command away from a second certified
   language.
3. **the route-B certification diffs for java and rust**, blocked on
   items 1 and 2 respectively.
4. **the full value matrix for the nine statically checked languages**,
   whose counts are derived and printed in `space_summary.json`, but
   which needs route-C execution built for them. Ruby and php show the
   full matrix costs seconds in an open-dispatch language. In the nine
   it is a genuine cost, and it is unbudgeted.
5. **the java 23-versus-86 row discrepancy** (§4.5), recorded and not
   reconciled.

### §6.1a the state of every lane, at a glance

| lane | route | probes | state | product |
|---|---|---|---|---|
| the go acceptance lane `ac_go.sh` | A2 | 7,600 | DONE 132.6 s | `acceptance_go_A2.json` |
| the rust acceptance lane `ac_rust.sh` | A2 | 9,196 | DONE 62.7 s (2nd run) | `acceptance_rust_A2.json` |
| the c++ acceptance lane `ac_cpp.sh` | A2 | 10,944 | DONE 666.3 s | `acceptance_cpp_A2.json` |
| the swift acceptance lane `ac_swift.sh` | A2 | 3,456 | DONE 146.7 s | `acceptance_swift_A2.json` |
| the dart acceptance lane `ac_dart.sh` | A2 | 10,625 | DONE 10.4 s | `acceptance_dart_A2.json` |
| the csharp acceptance lane `ac_csharp.sh` | A1 | 18,000 | DONE 27.2 s | `acceptance_csharp_A1.json` |
| the kotlin acceptance lane `ac_kotlin.sh` | A1 | 11,492 | DONE 598.5 s | `acceptance_kotlin_A1.json` |
| the route-B lift lane `lift_b.sh` | B | — | DONE 0.3 s, rust part absent | `raw/lift_b.txt` |
| the ruby route-C lane `rc_ruby.sh` | C | 261,382 | DONE 2.8 s | `behavior_ruby_C.json` |
| the php route-C lane `rc_php.sh` | C | 215,306 | DONE 0.8 s (2nd run) | `behavior_php_C.json` |
| the python route-C lane `rc_python.sh` | C | 342,225 | DONE 381.8 s (2nd run) | `behavior_python_C.json` |
| java A1 | A1 | — | NOT BUILT | — |
| typescript A1 | A1 | — | NOT BUILT | — |

Three raw files are QUARANTINED and must never be folded:
`raw/VOID_ac_rust_ebusy.txt`, `raw/PARTIAL_rc_php_fatal.txt`,
`raw/PARTIAL_rc_python_oomkill.txt`. They are kept because they are the
evidence for §5.1 finding 6, not because they measure anything.

### §6.2 harvest instructions, exactly

**The harvest is DONE — every lane listed below has been collected and
folded, and all ten result files are on disk and marked complete.** The
procedure is kept for two reasons. It is the procedure for the lanes
still to be built: java, typescript, and the rust lift. And a later
agent should know how the existing files were made.

1. Poll the lane. Each script's state is at
   `SandboxDesign/agent/status/<name>.sh.status`. The
   names are `ac_cpp.sh`, `ac_swift.sh`, `ac_dart.sh`, `ac_csharp.sh`,
   `ac_kotlin.sh`, `ac_rust.sh`, `lift_b.sh`, `rc_python.sh`,
   `rc_ruby.sh`, `rc_php.sh`. `state=done` plus `exit=0` is the signal.
2. Read a running lane's progress out of the log named in that status
   file's `log=` field, under `agent/logs/`. Every lane prints
   `[done/total]`, elapsed and ETA as it works.
3. Collect and fold:

   ```
   cp SandboxDesign/agent/out/ac_*.txt \
      SandboxDesign/agent/out/rc_*.txt \
      SandboxDesign/agent/out/lift_b.txt \
      PRIVATE/PseudoCoupHQ/Research/\
kind_fuzz_clustering/raw/
   cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering
   python3 l3_read.py
   ```

   The reader `l3_read.py` tolerates partial output. It folds whatever
   lines are present and reports the count, so it can be run against a
   lane that is still working. It also carries a **completeness gate**:
   it compares folded rows against holders-squared-times-operations,
   requires the driver's own final `__SUMMARY__` line, writes `complete`
   and `completeness` into every result file, and prints a loud `!!`
   line for anything short. **Read `complete` before reading
   verdicts** — three lanes have already exited 0 without finishing.
4. It writes `acceptance_<lang>_<route>.json` (verdict per operation
   and ordered holder pair, every row carrying form, holder and value
   class), `behavior_<lang>_C.json` (answer per operation, form, holder
   and value class) and `phase3_index.json`, and prints the per-language
   table.
5. **Three raw files are QUARANTINED and must never be folded** —
   `raw/VOID_ac_rust_ebusy.txt`, `raw/PARTIAL_rc_php_fatal.txt`,
   `raw/PARTIAL_rc_python_oomkill.txt`. They are the three silent
   failures of §5.1 finding 6, renamed so the reader cannot pick them
   up. They are kept as evidence, not as measurements.
6. Every route-B row in `lift_b.txt` is a DRAFT until diffed against
   route A or route C on the same pairs. Where two routes answer one
   cell, keep BOTH verdicts. A disagreement is a finding and is recorded
   as one, never reconciled silently.

`Research/kind_fuzz_clustering/HARVEST.md` holds the same procedure
alongside a per-lane state table and the exact build instructions for
the two unbuilt harnesses.

---

## record

Everything is in
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`:

- `progress.py` — the shared instrument, python face and shell twin.
- `l3_accept.py` -> `space_<lang>.json`, `space_summary.json`,
  `probes_ac_<lang>.jsonl` — the enumerated acceptance space.
- `l3_lanes.py` -> `lanes/ac_<lang>.sh` — the seven acceptance lanes,
  each carrying its probe payload and its driver inside itself.
- `l3_routec.py` -> `lanes/rc_<lang>.sh` — the three route-C lanes.
- `l3_read.py` -> `acceptance_<lang>_<route>.json`,
  `behavior_<lang>_C.json`, `phase3_index.json`.
- `raw/a2_verify.txt`, `raw/bisect_race.txt` — the two build-step
  measurements this log's §2 reports.
- `raw/ac_<lang>.txt`, `raw/rc_<lang>.txt`, `raw/lift_b.txt` — the run
  output, one line per probe.
- `HARVEST.md` — the state of every lane and how to collect it.

The two build-step lane scripts live at
`SandboxDesign/agent/drop/.done/a2_verify.sh` and
`.done/bisect_race.sh`.
