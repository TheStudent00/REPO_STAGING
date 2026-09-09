# log 034 — the swift redo and the word-spelled operations

Date: 2026-08-19. Node:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

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
probe
    one small generated program that asks one
    language one question.
    example tied to context:
        the swift matrix retaken below is
        76,614 probes; each declares a value
        in a typed slot and applies one
        operation to it.

lane
    one batch job. it runs a planned set of
    probes and writes its output to one raw
    text file. a lane has a short name.
    example tied to context:
        `vs_swift_00` and `vs_swift_01` are
        the two lanes that split swift's
        re-measurement in half.

shard, and the `__SUMMARY__` line
    one output chunk of a lane, ending in a
    line that states how many probes that
    piece did.
    example tied to context:
        both swift lanes wrote their
        `__SUMMARY__` line and both recorded
        `complete: true`.

completeness gate (also: gate)
    a check run after a lane finishes. it
    adds up the probe counts across the
    shards and compares the total with what
    the plan said. it prints COMPLETE only
    if they match.
    example tied to context:
        the swift redo's gate reads COMPLETE
        over 76,614 probes.

ENOSPC
    the operating system's "no space left on
    device" error.  these runs write to a
    memory-backed scratch disk, so running
    out of room is the way a lane most often
    dies without saying so.
    example tied to context:
        zero `ENOSPC` lines in either swift
        lane log.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        `UInt64` and `Int64` are two swift
        holders; the worked cell in §2.2
        compares one against the other.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        `i64max_plus1` is one more than the
        largest signed 64-bit integer, and it
        is one of the two value classes that
        swift's real compiler refuses.

cell
    one combination of operand kinds that an
    operation was asked about.  a pair cell
    is one combination of two holders.
    example tied to context:
        swift has 3,456 pair cells; 49 of
        them moved under the new instrument.

instrument
    the tool used to get a verdict on a
    probe.  two tools that disagree are two
    instruments, not one measurement.
    example tied to context:
        `swiftc -typecheck` and the full
        `swiftc -c` are two instruments, and
        this log is largely about the
        difference.

ACCEPT, REFUSE
    the two verdicts a checking run gives a
    probe.  a pair cell is UNIFORM when every
    probe in it got the same verdict, and
    SPLIT when they did not.

CODEGEN_REFUSE (a codegen refusal)
    the compiler accepted a probe when
    checking types but refused it when
    generating machine code.  the probe
    produces no answer.
    example tied to context:
        1,066 of swift's 2,618 old accepted
        probes are codegen refusals.

leaf
    one operation of one language, once it
    has answers to cluster with.  leaves are
    the things the clustering arranges.
    example tied to context:
        swift has six leaves: `*`, `<`, `>`,
        `>=`, `&&`, `||`.

menu (a language's standing menu)
    the list of operations this node measures
    for one language.  it was drawn by hand
    before this log.
    example tied to context:
        python's `and` is in the standing
        menu; c++'s `and` was not, until
        decision 43.

clustering
    the arrangement built from how close the
    leaves are to each other: it repeatedly
    joins the two closest groups until one
    group is left.
    example tied to context:
        the clustering this log does NOT
        rebuild is the 226-leaf one published
        in log 033.

route A, route C
    two ways a language is measured.  a
    route-A language is compiled, so a probe
    first gets an ACCEPT or REFUSE verdict
    and needs a second run to get an answer.
    a route-C language is run directly, so
    acceptance and answer arrive together.
    example tied to context:
        ruby and php are route C, which is
        why the driver line that broke them
        is shared between them.

leg G, leg R
    the two tests decision 43 applies to a
    word-spelled operation.  leg G asks
    whether the grammar declares the word in
    the operator slot of a two-sided
    expression.  leg R asks whether the
    language's own checker refuses an
    ordinary variable named with that word.
    example tied to context:
        kotlin's `shl' fails both.

control word
    a word fed through the same probe harness
    whose answer is known in advance, so a
    broken harness can be told apart from a
    real result.
    example tied to context:
        `zzfoo' is the control word: it is an
        ordinary name in every language, so a
        pass that REFUSES it is broken and
        its verdicts are dropped.

VOID
    a mark put on a measurement that was
    taken wrongly, so that it is kept on the
    record but not used.
    example tied to context:
        php's `and', `or' and `xor' were
        marked VOID in log 033 because the
        probe recorded the left operand.

decision <n>
    a numbered ruling this node has made,
    kept so it can be overturned by number.
    example tied to context:
        this log makes decision 43, the
        library-versus-language criterion.

stub (a stubbed lane)
    a lane that has been generated and
    written to disk but deliberately not run.
    example tied to context:
        the four kotlin aside lanes are
        stubbed and deferred.

SUPERSEDED (kept, not deleted)
    a product this pass replaced is kept on
    disk with the reason recorded, rather
    than being removed.
    example tied to context:
        `valuematrix_swift.json`, taken with
        the wrong instrument, is kept beside
        the new one.

harvest, fold (also: re-fold)
    harvesting is collecting finished lanes
    off disk and checking each one.  folding
    is reading that raw output and building
    the answer files and the clustering from
    it.
    example tied to context:
        this log does neither; both are the
        job of log 035.
```

---

## the earlier logs, restated so this one stands alone

Each fact this log borrows from an earlier log is stated here in full,
so no sentence below depends on opening another file.

- **Log 033 published the current clustering.** Twelve languages, 226
  leaves. Its item 4u recorded php's `and`, `or` and `xor` as VOID.
- **Log 032 executed each language's accepted probe set to get
  answers.** It is where swift's 1,066 codegen refusals were counted,
  and where zero codegen refusals were recorded for the other eight
  languages.
- **Log 031 was the earlier answer-grain clustering pass.** Its
  decision 30 voided php's three word-spelled logicals; its decision 31
  changed a published quantity, so its numbers and log 033's are not
  comparable.
- **Log 030 was the cluster sweep.** Its item 4k left the
  "shift exemption" open — whether a language's shift operators behave
  sharply or bluntly — naming kotlin and swift as the two languages
  that could settle it. Its item 4l went looking for cases where a
  statically checked language's verdict depends on the *value* rather
  than only on the pair of holders.
- **Log 028 closed the phase-3 work.** It recorded that the tree-sitter
  grammar parses swift's `+` through a catch-all `custom_operator`
  node, so swift's operator menu is only six operations.
- **Log 027 built and ran phase 3.** Its finding 11 was that the
  character `|` is the field separator in the raw files, so an
  operation named `||` breaks any reader that splits a line from the
  left.

Log 034 was free when this was written. It answers two rulings the owner gave
on 2026-08-19:

- **Job A** — redo swift with the real compiler.
- **Job B** — let word-spelled operations into the vocabulary, if a
  mechanical test can tell a language-level one from a library one.

---

## §1 — walkthrough, in plain words

Two things were wrong with the picture log 033 published, and the owner named
both of them.

**The first is that swift was measured with the wrong tool.**

- Every swift verdict in this node — the acceptance run, the value
  matrix, the leaves in the clustering — was taken with
  `swiftc -typecheck`, which stops after the type checker.
- Log 032 then executed swift's accepted probe set with the full
  compiler, and found that the compiler refuses **1,066 of the 2,618
  accepted probes, 40.7 percent**. Almost all of them are integer
  literals too large for the typed slot they are being stored into.
- Swift reports those at a later stage of compilation than the type
  checker, so the type checker never sees the problem.
- So swift's whole matrix was a measurement of a question nobody had
  asked. Job A retakes it.

**The second is that the list of operations to measure was drawn by
hand.**

- The generator takes each grammar's own token list and keeps whatever
  also appears in a candidate list of binary operations. That candidate
  list is a python literal somebody typed.
- Python's `and`, `or`, `is` and `in` are in it. Kotlin's `shl` and
  `shr` are not. C++'s `and` and `xor` are not.
- the owner's ruling was blunt: *"i dont care if it is symbol or word-spelled.
  if we can detect whether its library to filter and keep the
  word-spelled as first class objects, just as much as symbols."*
- Job B builds that detector out of evidence the node already trusts,
  and applies it to all twelve languages rather than to kotlin alone.

**The first headline is that the swift redo cost nothing and should
have been done at the start.**

- `swiftc -c` runs the later compilation stages as well as the type
  checker, so it is the real instrument. It was measured at **155
  milliseconds per probe, against `swiftc -typecheck`'s 154**
  *(measured)*.
- Full compilation is not more expensive than type checking here.
- So the whole 76,614-probe matrix was retaken, rather than only the
  probes the old tool accepted. That way the redo rests on no
  assumption about what the type checker refuses.

**The second headline is that the new test works, that it re-derives
almost the whole hand-drawn list on its own, and that it rules kotlin's
`shl` a library function on two independent legs.**

- Decision 43 asks two mechanical questions about a word-spelled
  operation. Does the grammar declare that word in the operator slot of
  a two-sided expression? And does the language's own checker refuse an
  ordinary variable named with that word? Both are cheap to run, and
  the test is both together.
- It admits **c++'s `and`, `bitand`, `bitor`, `not_eq`, `or` and `xor`,
  ruby's `and` and `or`, typescript's `instanceof` and php's
  `instanceof`** *(measured)*.
- It re-derives, without being told, python's six, kotlin's `in`,
  typescript's `in`, and php's `and`, `or` and `xor` — all of which
  were already in the hand-drawn list.
- And it refuses kotlin's `shl`, `shr`, `ushr`, `and`, `or` and `xor`.
  The kotlin grammar does **not** declare them: its two-sided
  expression node carries an ordinary identifier where an operator
  token would be. And `val shl: Int = 1` compiles *(measured, both
  legs)*.

**So the owner's premise was checkable and it does not hold.**

- The ruling said to check whether kotlin's grammar declares `shl`,
  `shr` and `ushr` as infix operators.
- It was checked. It does not.
- Kotlin's shifts are standard-library functions carrying an `infix`
  modifier. They are resolved by name and can be shadowed by name. The
  test the owner asked for is exactly the machine that says so.

**The third headline is therefore that the shift-exemption question
settles by ruling a language OUT rather than by letting one IN, and
that it stops being an open tie at all.**

- Log 030 item 4k left the count at two sharp languages, go and rust,
  against four blunt ones, cpp, csharp, java and dart — with kotlin and
  swift named as the two that could move it.
- Kotlin cannot move it: it has no language-level shift at all,
  measured on two legs. Log 030's ruling that kotlin's shifts are
  builtins is confirmed rather than bent.
- Swift can move it, and the redo is what makes swift readable at all.
- The finished tally is in §4.4 with the run behind it.

**The fourth headline is a fault that the word-spelled operations
dragged into the light in a second language.**

- Log 033 item 4u recorded php's `and`, `or` and `xor` as VOID. The
  probe line `$__r = ($a) and ($b);` binds as `($__r = $a) and $b`,
  because php's word-spelled logicals sit below assignment in
  precedence. So all 6,241 answer cells recorded the left operand
  instead of the result.
- Ruby's driver has the identical line and the identical fault. It was
  invisible because ruby had no word-spelled operation in its list
  until this pass admitted one.
- Both are repaired, and both directly-run languages are re-run whole
  rather than patched.

**The fifth headline is about how the test was measured, rather than
about what it says.**

- The reservation leg is a probe harness, and a probe harness needs a
  control: a word whose answer is known in advance, so that a broken
  harness can be told apart from a real result.
- The first pass carried a control word for seven of the twelve
  languages. **Two of the five without one were measuring their own
  broken harness.** C-sharp's compiler was refusing every probe,
  including the control, for want of an entry point. The typescript
  path search found no checker at all. Both failures looked exactly
  like real measurements.
- `wordop_criterion.py` now drops any verdict from a pass that did not
  also ACCEPT the control word. That cost four re-run passes, and it is
  the reason the table in §3.1 can be read at all.

---

## §2 — job A, swift retaken with the real compiler

The instrument comes first, because it decided the shape of the redo.

| instrument | milliseconds per probe | what it actually runs |
|---|---|---|
| `swiftc -typecheck` | 154 | the type checker, then stops |
| `swiftc -c` | 155 | the type checker, then the later stages that generate code, then writes an object file |
| `swiftc -c`, run 8 at a time on 6 cores | 34 effective | the same work, in parallel |

- **Full compilation is not more expensive than type checking here**
  *(measured 2026-08-19, 40 runs of each)*.
  - That is why the whole 76,614-probe matrix was retaken, and not only
    the 2,618 probes the old tool accepted.
  - A redo covering only the old accepts would have rested on an
    assumption: that the full compiler refuses everything the type
    checker refuses.
  - That assumption turns out to be true, and it is now measured rather
    than assumed. The measurement is the direction of the moved cells,
    below.
- The smoke probe that decided it, in one place:

```
let x: Int8 = 200
swiftc -typecheck  ACCEPT
swiftc -c          REFUSE
  error: integer literal '200'
  overflows when stored into 'Int8'
```

The redo ran as two lanes, `vs_swift_00` and `vs_swift_01`, 38,307
probes each. They took **1,477.6 s and 1,477.1 s** *(measured)*, which
is 38.6 and 38.4 milliseconds per probe against the 34 millisecond
projection. Zero `ENOSPC` lines in either lane log. Both `__SUMMARY__`
lines present, both reading `complete: true`.

### 2.1 the matrix, old instrument against new

| measure | taken with `swiftc -typecheck` | taken with the full `swiftc -c` |
|---|---|---|
| probes run | 76,614 | 76,614 |
| probes ACCEPTED | 2,618 | **1,552** |
| pair cells where every probe was accepted | 77 | **28** |
| pair cells with one verdict throughout | 3,447 | 3,398 |
| pair cells with mixed verdicts | 9 | **58** |
| pair cells that changed at all | — | 49 of 3,456 |

- **The accepted set falls by exactly 1,066** *(measured)*, and 1,066 is
  exactly the codegen-refusal count that log 032's execution pass
  recorded.
  - These are two independent runs: one a per-probe acceptance sweep,
    one a chunked execution with a repair loop.
  - They agree to the single probe. Level **measured** for both counts;
    **derived** for reading the agreement as a cross-check.
- **And 1,552 is exactly the number of answers log 032 recorded for
  swift** *(measured)*. The set the full compiler accepts and the set
  swift actually answered on are the same set. That is the strongest
  available statement that the redo measured the right thing.
- **All 49 changed pair cells changed the same way**, from
  every-probe-accepted to mixed. **None changed from refused to
  accepted, and none changed from mixed to uniform** *(measured)*.
  - So the type checker was uniformly more permissive than the full
    compiler, never differently permissive.
  - That is exactly the property an accepts-only redo would have had to
    assume.

### 2.2 what the redo does to the value-independence assumption

This is the part of the redo that is not simply a smaller swift.

| operation | pair cells where every probe was accepted, before | after | cells changed |
|---|---|---|---|
| `<` | 23 | 8 | 15 |
| `>` | 23 | 8 | 15 |
| `>=` | 23 | 8 | 15 |
| `*` | 6 | 2 | 4 |
| `&&` | 1 | 1 | 0 |
| `\|\|` | 1 | 1 | 0 |

- **Swift's mixed-verdict cells go from 9 to 58, and all 49 new ones
  are the same phenomenon: a literal too big for its slot**
  *(measured)*. The worked cell is `>=` with a `UInt64` slot on the
  left and an `Int64` slot on the right:

```
>=  UInt64 v Int64
base_42  x base_42        ACCEPT
base_42  x base_zero      ACCEPT
base_42  x i64max         ACCEPT
base_42  x i64max_plus1   REFUSE
base_42  x p53_plus1      ACCEPT
base_42  x u64max         REFUSE
```

- The whole acceptance grain of this node rests on one claim: for a
  statically checked language, whether a probe is accepted depends on
  the pair of typed slots and not on the value put in them.
  - Log 030 measured that claim false for typescript on 876 cells, and
    nearly true for swift on 9.
  - **Under the right instrument swift's number is 58, and every one of
    the 49 new ones is a value that does not fit its slot**
    *(measured)*.
  - So the `-typecheck` instrument was hiding exactly the kind of
    value-dependence that log 030 item 4l went looking for.
- Level **derived** for calling all 49 the same phenomenon. Level
  measured for the counts, and for the two refusing value classes being
  `i64max_plus1` and `u64max` in every one of them.

### 2.3 what is superseded, and what is still owed

`valuematrix_swift.json`, the matrix taken with the wrong instrument,
is **kept**. The new `valuematrix_swift_full.json` records a
`supersedes` field pointing at it, with the instrument named in both
files. A wrong instrument that produced a published number belongs on
the record.

**Still running at the time of writing**: `xr_swift_00`, the execution
redo over the new 1,552-probe accepted set.

- It is generated by `l3_swiftexec.py` and queued behind the three c++
  word-matrix lanes.
- Its own run time is under a minute; there is about 50 minutes of
  queue ahead of it.
- **It carries a check that is better than any number the matrix redo
  prints about itself: the execution driver's codegen-repair loop
  should fire ZERO times**, because the accepted set was itself taken
  with the compiler that would do the refusing. A non-zero count there
  would mean the redo did not do its job.

---

## §3 — job B, the test, written as a numbered ruling that can be overturned

Decisions are the numbered rulings this node has made, kept so that any
one of them can be overturned by number. Decisions 1 to 17 stand where
log 030 left them, 18 to 30 where log 031 left them, and 31 to 42 where
log 033 left them. This is **43**, and it is stored in
`wordop_criterion.json` beside its evidence, so that overturning it is
a one-line instruction.

```
DECISION 43 -- the library-versus-language
criterion for a word-spelled operation.

A word-spelled binary operation is admitted
as FIRST CLASS, on the same footing as a
symbol-spelled one, if and only if BOTH of
the following hold.

 leg G, GRAMMAR DECLARATION.  The grammar
 declares the word among the anonymous
 tokens reachable from the OPERATOR slot of
 a node whose field shape is a binary one:
 either (left, operator, right) with the
 right slot admitting an expression; or a
 single repeated `operators' field over a
 run of expression sub-nodes; or a node
 named `<word>_expression' with fields
 (left, right) whose right slot admits an
 expression and whose `<word>' is itself an
 anonymous token of that grammar.  Nodes
 whose operator slot admits the bare token
 `=', or whose operator tokens all end in
 `=', are the assignment family and are
 excluded.

 leg R, RESERVATION.  The language's own
 checker REFUSES a probe that declares an
 ordinary variable named with that word, in
 the probe's own scope, with nothing else
 changed.

A word that fails either leg is LIBRARY and
is excluded, with the failing leg named.
Symbol-spelled operations are untouched: leg
R is vacuous for a spelling that cannot be
an identifier, and leg G already governed
them.

Decision 43 is ADDITIVE.  It admits; it
never removes an entry from the standing
menu.  Where it fails to re-derive one, that
is recorded as a finding against leg G and
not as a deletion.
```

**Why two legs and not one.**

- Leg G on its own would admit a library function that happens to be
  infix, if the grammar happened to tokenise it. It is also blind in a
  way log 028 already recorded: swift's grammar parses `+` through a
  catch-all `custom_operator` node and declares no operator slot at
  all, and dart's grammar spells its operators as named nodes.
- Leg R on its own would admit every keyword in the language, `if` and
  `class` among them.
- The two together are what make this a criterion rather than a
  preference.

**Why "is this word reserved" is the right question to ask a checker.**

- It is the one question whose answer separates a token the language
  has reserved from a name the language looks up.
- Swift is the case that proves the point. **Every** swift operator,
  `+` included, is declared in swift's standard library as a function
  with an `infix operator` declaration. So a test phrased as "is this
  symbol a library symbol" would strip swift of its entire menu.
- "Is this spelling available to the programmer as a variable name"
  does not have that failure.

Two notes on how the reservation probes were run.

- **Three passes of leg R were dropped rather than read**, because
  their own control word `zzfoo` came back REFUSE or was missing
  entirely — 26 verdicts over 7 languages *(measured)*. The re-runs are
  the reservation passes `lr_words3`, `lr_words4` and `lr_words5`, and
  every verdict in the table below comes from a pass whose control was
  ACCEPTED.
- **C-sharp's first two passes are worth naming**, because the failure
  was informative before it was repaired. The words `and` and `or` drew
  only error `CS5001`, a complaint about a missing entry point, while
  `is` and `as` drew `CS1001 Identifier expected` **at the declaration
  column** *(measured)*. The error codes separated the two classes
  before the harness was fixed, and the repaired pass agrees with them.

### 3.1 the twelve-language survey

Each row is one language. The first two columns list the words that
passed each leg. The last two columns are the verdict.

| language | grammar declares it as an operator (leg G) | the checker reserves the word (leg R) | ADMITTED as first class | LIBRARY, excluded |
|---|---|---|---|---|
| go | — | — | — | and, or, shl, xor |
| rust | — | — | — | and, or, shl |
| cpp | and, bitand, bitor, not_eq, or, xor | and, bitand, bitor, not_eq, or, xor | **and, bitand, bitor, not_eq, or, xor** | — |
| swift | — | — | — | and, shl |
| dart | — | — | — | and, or |
| csharp | — | as, is | — | and, as, is, not, or |
| kotlin | in | in | in | **and, or, shl, shr, ushr, xor** |
| java | — | instanceof | — | and, instanceof |
| typescript | in, instanceof | in, instanceof | **in, instanceof** | and |
| python | and, in, is, is not, not in, or | and, in, is, or | **and, in, is, or** | — |
| ruby | and, or | and, or | **and, or** | — |
| php | and, instanceof, or, xor | and, instanceof, or, xor | **and, instanceof, or, xor** | — |

- The leg-G and leg-R columns list only the words that were actually
  probed. That set is every word leg G declares anywhere, plus the six
  kotlin infix functions, plus a spread of control words. An empty
  leg-R cell means every probed word in that language was an ordinary
  identifier there.
- **Two cells are unread and are marked so**: python's `is not` and
  `not in`.
  - A multi-word spelling counts as reserved only if every word in it
    is reserved, and `not` had not been probed when this was written.
  - The reservation pass `lr_words5` is queued and will close them.
  - Both spellings are already in the standing menu, so the gap costs
    nothing but honesty. Level **unverified** for those two cells and
    measured for the other 46 rows.

Read the table with three things in mind.

- **The LIBRARY column is not a list of things the language cannot
  do.**
  - `rust.and`, `swift.shl`, `dart.and`, `java.and` and `kotlin.and`
    are in that column because the word is an ordinary identifier
    there — you may name a variable `and` — and in most of those cases
    the language has no such operation at all.
  - `kotlin.shl` is the one entry where the operation genuinely exists
    and is genuinely a library function *(measured, both legs)*.
- **The test re-derives, without being told, every word already in the
  hand-drawn menu except three.**
  - Python's six, kotlin's `in`, typescript's `in` and php's three all
    come back ADMITTED.
  - The three it does not re-derive are `java.instanceof` and
    `csharp.is`. Both are reserved on leg R, and both fail leg G, for
    the same reason: their grammar node puts a **type** in the
    right-hand slot, not an expression, so leg G reads them as type
    tests rather than as two-sided value operations.
  - That is arguably the right answer, and it is certainly a finding,
    since this layer has no type operands to probe with.
  - Decision 43 only adds, so both stay in the menu and the
    disagreement is recorded here rather than acted on. `csharp.as` is
    the same shape and was never in the menu. Level **derived** for the
    reading; measured for both legs.
- **What is newly admitted is nine leaves across four languages**: six
  from c++, two from ruby, one from typescript, one from php
  *(measured)*.
  - Php's `and`, `or` and `xor` are not new admissions — they were
    already in the menu and marked VOID — but they are new
    measurements, for the reason in §3.2.

### 3.2 the parenthesis fault, now found in a second language

Log 033 item 4u diagnosed this in php. The probe line
`$__r = ($a) $op ($b);` binds as `($__r = $a) and $b`, because php's
word-spelled logicals sit *below* assignment in precedence while its
symbol-spelled ones sit above it. So the assignment happens first, the
recorded answer is the left operand, and every acceptance pass scores
the probe ACCEPT.

Ruby's driver carries the same line, `__r = (a) #{op} (b)`, and ruby's
`and` and `or` have the same precedence relation to `=`.

- **The fault was in ruby all along and could not be seen**, because
  ruby's menu had no word-spelled operation until decision 43 admitted
  one *(derived)*. That is the shape of thing a hand-written vocabulary
  hides: the harness fault and the missing operation were the same
  blind spot.
- Both drivers are repaired with the parentheses. **Both directly-run
  languages are re-run whole rather than patched**, so that the
  symbol-spelled cells can be compared against the pre-repair product
  and confirmed unchanged, rather than assumed unchanged.
- Python needed no repair: python's `and` and `or` bind *above*
  assignment, so `__r = (a) and (b)` was always right *(measured, and
  it is why python's word-spelled logicals produced usable answers in
  log 031 while php's did not)*.

### 3.3 what the c++ six are, and why they make a control

C++'s `and`, `bitand`, `bitor`, `not_eq`, `or` and `xor` are the
standard's alternative token spellings of `&&`, `&`, `|`, `!=`, `||`
and `^`.

- They are not library macros in a hosted C++20 compilation:
  `g++ -std=c++20 -fsyntax-only` refuses `int and = 1;` with no header
  included *(measured)*.
- And the grammar declares them in its `binary_expression` node beside
  the symbols *(measured)*.

So they carry a **prediction the clustering can be scored against**.

- Each of the six should land at distance exactly zero from its symbol
  twin: identical set of accepted cells, identical answer on every one.
- Nothing else in this node has that property.
- A rebuild that does *not* put `cpp.and` on top of `cpp.&&` would be
  evidence against the machinery rather than against c++. This is the
  first control of this kind the clustering has had. Level **derived**
  for the prediction; the run that scores it is in §4.

---

## §4 — the new results

### 4.1 the route-C repair, measured on both sides

Ruby and php are the two directly-run languages. Both were re-run whole
with the repaired driver, so that the symbol-spelled cells could be
compared rather than assumed unchanged.

| language | probes | answers | raises | wall time |
|---|---|---|---|---|
| ruby, repaired, with `and` and `or` added | 285,144 | 76,270 | 208,874 | 2.5 s |
| php, repaired, with `instanceof` added | 223,587 | 98,245 | 125,342 | 0.6 s |

- **18,468 of php's 24,843 word-spelled logical cells changed**, 74.3
  percent *(measured)*.
  - Decision 30 voided 6,241 of them.
  - The true count of cells the fault corrupted is three times that,
    because the re-run covers the whole value matrix and not only the
    cells log 031 had.
- **And php's `&&` and `||` cells changed on 0 of 8,281** *(measured)*.
  The repair touched only what it was meant to touch, and that is
  confirmed rather than assumed. Confirming it is the reason for
  re-running whole.
- The worked cell, php `null and null`:

```
before  NULL:            the LEFT OPERAND
after   boolean: (false) the operation
```

### 4.2 ruby's `and` is a second control, and it passes

Ruby's `and` and `&&` are the same operation written at different
precedence, so the two must give the same answers. The clustering has
never had a pair like that to score itself against.

- **`ruby.and` agrees with `ruby.&&` on all 11,881 shared cells**
  *(measured)*, once 1,218 cells are set aside. Those 1,218 are set
  aside for a reason that is itself a finding, in §4.3 below.
- `ruby.or` against `ruby.||` could not be read in this pass's quick
  check.
  - The operation name `||` contains the character the raw files use to
    separate fields, and the quick check split each line from the left.
  - The folding reader splits from the right and does not have the
    fault.
  - This is log 027 finding 11 turning up for a third time, this time
    in a throwaway script rather than in a product.
  - Level **unverified** for that one pair until the fold.

### 4.3 a third instance of the same recorder fault

Comparing ruby's pre-repair and post-repair runs found **2,492 of
249,501 common cells differing** *(measured)* — and **all 2,492 of them
carry a hexadecimal memory address**:

```
OLD  #<Class:0x00007ee82bbab2c8>:#<struct >
NEW  #<Class:0x000072fb0e4ebf48>:#<struct >
```

- Ruby's anonymous struct and data classes print their memory address
  when inspected, so **0.9 percent of ruby's recorded answers are not
  reproducible between two runs of the same probe** *(measured)*. Every
  one of the 1,218 `and`-against-`&&` differences in §4.2 is one of
  these.
- This is the third instance of the same class of fault. Log 032 found
  it in kotlin's java arrays, recorded through `toString`. Log 032 §6
  found it again. Here it is in ruby's route-C recorder, where it has
  been in every ruby product since log 027.
- It is a fault in how answers are recorded, not a fact about the
  language, and the fix is the one log 032 applied to kotlin: record
  the class name and the structure, never the default inspection text
  of an anonymous class.
- **It was found by re-running a lane nobody suspected**, which is the
  argument for re-running whole rather than patching.

### 4.4 the shift tally, settled

Log 030 item 4k left this open, naming kotlin and swift as the two
languages that could move it. Both are now answered. "Sharp" and
"blunt" describe how tightly a language constrains its shift
operations relative to its arithmetic.

| language | shifts | arithmetic `+` | reading |
|---|---|---|---|
| go | 0.75 | 0.00 | sharp |
| rust | 0.75 | 0.14 | sharp |
| cpp | 0.71 | 0.64 | blunt |
| csharp | 0.73 | 0.70 | blunt |
| java | 0.80 | 0.78 | blunt |
| dart | 0.75 | — | blunt |
| typescript | 0.00 | 0.50 | inverted |
| kotlin | **none, and now for a measured reason** | 0.62 | out |
| swift | **none in its grammar** | — | out |

```
THE SHIFT-EXEMPTION TIE, RESOLVED.

It breaks by ruling a language OUT, not by
letting one IN.

Kotlin has no language-level shift.  Leg G
finds no shl/shr/ushr token in the grammar:
its two-sided expression node carries an
ordinary identifier where an operator token
would be.  Leg R finds that `val shl: Int
= 1' compiles, so the word is an ordinary
name.  Both legs fail, on two independent
instruments.  Log 030 item 4k's ruling that
kotlin's shifts are builtins is CONFIRMED,
not bent.

So the tally stays TWO SHARP (go, rust)
against FOUR BLUNT (cpp, csharp, java,
dart), with typescript inverted -- and it is
no longer a tie awaiting two more rows.  It
is a finished count over the languages that
HAVE the operation.  Kotlin cannot move it
because kotlin does not have it.  Swift's
row depends on the redo of section 2 and on
swift's grammar, which declares no shift
token either.

Settling it further needs more LANGUAGES,
which is what log 030 said, and the two
candidates it named are now measured out.
```

- Level **measured** for both legs of the kotlin exclusion, and for the
  rows carried forward from log 030. Level **derived** for calling the
  count finished.
- The kotlin aside — `shl`, `shr`, `ushr`, `and`, `or` and `xor`
  measured anyway as library leaves, so a reader can see where they
  would have landed — is generated as the four lanes
  `ka_kotlin_00..03`, 89,304 probes, 77 minutes projected, and is
  deferred off the critical path. **It must never be folded into the
  default clustering.** Level **estimate** on its cost.

### 4.5 what has landed, what is running

| lane | what it is | state | numbers |
|---|---|---|---|
| `vs_swift_00/01` | the two swift acceptance lanes, retaking the value matrix with the real compiler | DONE, gate COMPLETE | 76,614 probes, 1,552 accepted |
| `lr_words1..4` | four of the five reservation-probe passes | DONE | 50 + 14 + 13 + 11 reservation probes |
| `rc_ruby2` | ruby re-run whole with the repaired driver | DONE | 285,144 probes, 2.5 s |
| `rc_php2` | php re-run whole with the repaired driver | DONE | 223,587 probes, 0.6 s |
| `vw_typescript_00` | typescript's acceptance run for its newly admitted word operation | DONE | 10,000 probes, 3.1 s |
| `vw_cpp_00..02` | the three c++ acceptance lanes for its six word-spelled operations | RUNNING | 72,600 probes, 45.1 ms each, about 55 min |
| `xr_swift_00` | swift's execution re-run over the new accepted set | QUEUED | 1,552 probes, 4 chunks |
| `lr_words5` | the last reservation pass, probing python's `not` | QUEUED | 3 probes |
| `ka_kotlin_00..03` | the four kotlin aside lanes, for the excluded library shifts | DEFERRED, stubbed | 89,304 probes |

- The first c++ lane `vw_cpp_00` was measured at **45.1 milliseconds
  per probe**, against the 60.9 the plan projected from log 027
  *(measured)*, so the c++ word-operation matrix will land under its
  projection.
- The instructions for collecting all of this and rebuilding the
  clustering are in
  `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/HARVEST.md`,
  written before this log and kept current.

---

## §5 — the rebuilt picture, which this log does not have

**The rebuild has NOT been run, and this section says so rather than
guessing.** It is blocked on two lanes, both queued and both sized:
`xr_swift_00`, the execution re-run that gives swift its real answers;
and `vw_cpp_00..02`, the acceptance lanes that give c++'s six word
spellings the set of cells they work on. `HARVEST.md` carries the exact
commands.

Here is what can be said now, each with its level.

- **Swift will not grow from six leaves to a normal number, and the
  redo makes that plainer rather than fixing it.**
  - Swift's six leaves are `*`, `<`, `>`, `>=`, `&&` and `||`, and that
    number is set by its grammar rather than by its compiler. The
    tree-sitter grammar parses swift's `+` through a catch-all
    `custom_operator` node, so `+`, `-`, `/`, `%`, `==`, `!=` and the
    bitwise and shift spellings have never been in swift's menu at all.
    Log 028 recorded this as "swift's operator menu — 6 operations". It
    is a fact about the instrument.
  - The redo changes the set of cells swift works on, not its leaf
    count: its input cells fall from 400 towards the 1,552-answer set,
    and its every-probe-accepted pair cells from 77 to 28 *(measured)*.
  - **Swift gets more honest, not bigger.** Level **derived** for the
    leaf count staying at six; measured for the cell counts.
- **Swift's row in the twelve-by-twelve comparison stops carrying a
  footnote.**
  - Log 033 §5 said swift's row was "near 1.000 everywhere and means
    almost nothing", because decision 40 — the ruling that throws away
    rows the compiler refused at code-generation time — had removed
    40.7 percent of swift's accepted set.
  - After the redo, decision 40 removes nothing. There is no
    codegen-refusal class left, because the accepted set is defined by
    the compiler that would have done the refusing.
  - That is the change to expect in the rebuild: swift's row stops
    carrying an exclusion footnote and starts being a measurement over
    1,552 answers. Level **derived**.
- **Kotlin's `shl` will not land in the shift cluster, because it will
  not be in the rebuild at all.**
  - Decision 43 rules it a library function on both legs.
  - The shift group of log 033 §3.2 — `dart.<<`, `dart.>>`, `go.&^`,
    `go.<<`, `go.>>`, `java.<<`, `java.>>`, `java.>>>`, `ruby.>>`,
    `rust.<<`, `rust.>>` — should therefore come back with the same
    eleven members and no twelfth. Level **derived**.
  - If the kotlin aside is ever folded in as a labelled extra, it will
    say where `kotlin.shl` *would* have gone, which is a different
    question and is worth asking.
- **The nine new leaves carry two predictions the rebuild can score
  itself against.**
  - Each of c++'s six must land at distance exactly zero from its
    symbol twin (§3.3).
  - `ruby.and` must land on `ruby.&&`, which is already measured true
    on all 11,881 reproducible shared cells before any clustering runs
    (§4.2).
  - **These are the first controls of this kind the clustering has
    had.** A rebuild that fails them is evidence against the machinery.
- **The leaf count moves from 226 to 235** — 226 plus nine, with php's
  three VOID leaves becoming live rather than counting as new. Level
  **derived**.
- **And one number will move for a reason unrelated to either job.**
  Php's word-spelled logical answers change on 18,468 cells (§4.1), so
  every measured closeness involving `php.and`, `php.or` or `php.xor`
  is a different measurement from log 031's and log 033's. Those two
  logs' php word-logical numbers must not be read against the
  rebuild's — for the same reason decision 31 made log 031's and log
  033's A factors incomparable.

---

## §6 — honest remainders

Each item below is something this pass did not settle. Each says what
the state of it is.

- **The partially-loaded-holders default is ratified by silence.** That
  default is: a typed slot that loaded only some of its value classes
  is probed with the values that did load. the owner left it standing on
  2026-08-19. It is recorded in the CORE's open items as ratified by
  silence, and it is still overturnable. Level **measured** that it was
  left standing; nothing in this pass tests it.
- **Decision 43's leg G can only see what tree-sitter's grammars
  declare, and it says so.**
  - Three grammars spell their operators in a way it cannot read:
    swift's catch-all `custom_operator` node, dart's named operator
    nodes, and any grammar that gives an operation its own node with a
    type in the right-hand slot.
  - For those, leg G is silent rather than negative, and a silent leg
    makes the two-leg test fail.
  - **No word was admitted on leg R alone, and none should be.** A
    reader who thinks swift or dart is being short-changed should
    overturn decision 43 by adding a third leg, not by hand-adding a
    word.
- **The test has been applied to the operator vocabulary only.** The
  CORE's kind space also has indexing, calling, member access and
  iteration. Word-spelled forms of those — python's `in` as a container
  test against `in` as loop syntax, for instance — are not separated by
  anything here. Level **unverified** that the test generalises past
  two-sided operations.
- **Kotlin's shifts are excluded and measured anyway**, as a labelled
  aside, so the tally can be read both ways. The aside must never be
  folded into the default clustering. Its lanes are `ka_kotlin_00..03`
  and they are deferred off the critical path in `HARVEST.md`.
- **The swift redo does not touch the other eight languages.** Log 032
  recorded zero codegen refusals for them, which is evidence that their
  checking tools and their compilers agree — but it is evidence over
  the accepted set only. Nothing here re-checks whether, say, javac's
  analysis phase accepts something the full compile refuses. Level
  **unverified**.
- **Decision 31 still changed a published quantity, and the older logs
  are still not re-run.** Log 031's A factors and log 033's are
  different measurements and must not be read against each other.
- **Decision 37's container bridge is still weak and still counted
  rather than fixed** — 134 container tokens matched across languages,
  with every container answer holding a boolean or a null failing to
  meet its counterpart.
- **Decision 26 and decision 27 remain open for the owner.**
- **The cross-check against `kind_signature_clustering` is still not
  started** — CHECK item 4j, the mutual-checkability symmetry the CORE
  opens with. It is now the oldest unstarted item in the node.
- **Rust's panic is still a debug-build fact.** One release build, about
  a second of work, would settle whether `rust.+` joins the wrapping
  five.

---

## §7 — artifacts

All paths are inside
`~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

| file | what it is |
|---|---|
| `wordop_survey.py` | leg G, the grammar test — reads node types and kinds, writes `wordop_survey.json` |
| `wordop_criterion.py` | joins leg G and leg R and writes `wordop_criterion.json`; drops any pass whose control word was not accepted |
| `l3_wordops.py` | builds the lanes for the newly admitted operations, and applies the parenthesis repair to the two directly-run languages |
| `l3_swiftfull.py` | builds `vs_swift_00/01`, the matrix redo using the full `swiftc -c` |
| `l3_swiftfull_read.py` | folds the redo, runs its completeness gate, and compares it against the superseded matrix |
| `valuematrix_swift_full.json` | swift's value matrix, taken with the real compiler |
| `valuematrix_swift.json` | swift's value matrix taken with `swiftc -typecheck` — superseded, kept with the reason recorded |
| `swiftfull_diff.json` | what changed between the two instruments |
| `swiftfull_accepts.json` | the new accepted probe set, which is the input to the execution redo |
| `raw/lr_words*.txt` | the raw output of the five reservation-probe passes, control words included |
| `HARVEST.md` | what is running, how to collect it, and what is still to be built |
