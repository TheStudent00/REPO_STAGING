# log 037 — the constructs, all twelve languages

Date: 2026-08-19. Node:
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PseudoCoupHQ/Research/kind_fuzz_clustering/`.

Written in the readable register of the rewritten logs 034 and 035.
Every word this node invented is defined before it is used. Every claim
carries its level.

**Measured** means a number a run printed. **Derived** means a number
worked out from measured numbers. **Decision** means a judgment call,
numbered and overturnable. **Unverified** means nobody has checked it.

---

## words used in this log

Each word is defined once, with an example taken from this log rather
than from a made-up one.

```
construct
    the other thing a compiler can do to a
    loaded value, beside applying an operator
    to it: reach into it, choose on it,
    repeat over it, or bind it to a name.
    example tied to context:
        `if`, `for`, `break` and `=` are
        constructs. `+` is not; it is an
        operator, and logs 024 to 035
        measured those.

family
    a group of constructs that do one kind of
    job. this pass has three, and the owner named
    them: access, flow, binding.
    example tied to context:
        `flow` holds if, for, while, break,
        continue and try.

role
    one construct slot in the design, before
    any language spells it.
    example tied to context:
        `access.member` is a role. c-sharp
        spells it `member_access_expression`
        and rust spells it `field_expression`.

scaffold
    the inert code that makes a construct
    legal. a `break` needs a loop around it;
    the loop is the scaffold.
    example tied to context:
        c-sharp's `flow.if` scaffold is four
        lines and its only moving part is
        what fills the condition.

slot
    a hole in a scaffold that a value goes
    into.
    example tied to context:
        `if ((a))` has one slot. `(a)[(b)]`
        has two.

holder
    one way a language can hold a value:
    a declared type plus the statement that
    declares it.
    example tied to context:
        java holds a whole number as `short`
        and as `int`, so java has two whole
        holders among its 32.

form
    the layer-1 name for a kind of value.
    there are eight: nothing, truth, whole,
    fractional, text, sequence, keyed,
    nesting.
    example tied to context:
        `[1, 2, 3]` is of form sequence in
        every one of the twelve.

trace
    what a flow construct gives back instead
    of an answer: the sequence of values at
    each joint, written in the same bits
    encoding as an answer.
    example tied to context:
        java's for over 1, 2, 3 records
        TRACE:3 with three IT steps.

joint
    one step of a trace. a branch taken, an
    iteration run, a jump reached, or a name
    bound.
    example tied to context:
        `BR=then` is a branch joint and
        `STOP=4` is a jump joint.

lane
    one batch job. it runs a planned set of
    probes and writes its output to one raw
    text file. a lane has a short name.
    example tied to context:
        the lane named `kx_kotlin` ran
        kotlin's 2,912 construct probes and
        wrote `raw/kx_kotlin.txt`.

acceptance stage (also: stage A)
    the half of a lane that asks the
    language's own checker whether the probe
    is legal at all. no code is run.
    example tied to context:
        rust's stage A ran `rustc
        --emit=metadata` once per probe.

execution stage (also: stage B)
    the half of a lane that runs the probes
    stage A scored ACCEPT, in chunks.
    example tied to context:
        c++'s stage B built two chunks of
        200 probes and ran each binary.

chunk
    many probes compiled into one program.
    the program takes a START INDEX, so a
    death that the language cannot catch
    costs exactly one probe.
    example tied to context:
        c++'s chunk died 22 times and the
        lane restarted it past each corpse.

completeness gate (also: gate)
    a check run after a lane finishes. it
    compares the rows the lane wrote with
    the probe count the lane's own opening
    line planned, and prints COMPLETE only
    if they match.
    example tied to context:
        the gate prints COMPLETE for all
        twelve languages in this log.

harness refusal
    a refusal whose message names the
    RECORDER rather than the construct. it
    is the measuring instrument refusing,
    not the language.
    example tied to context:
        rust refused 4 probes because its
        encoder has no impl for that type.

plateau
    a run of threshold over which the number
    of clusters does not change. a wide
    plateau is a stable reading.
    example tied to context:
        the construct sweep sits at 42
        clusters from 0.81 to 0.87.

fatal (php)
    php's uncatchable error. no `catch`
    reaches it and the process dies.
    example tied to context:
        php's construct lane hit 20 of them
        and lost one probe to each.
```

---

## what came before this log, restated

Nothing below assumes the reader remembers the earlier logs.

The node measures what twelve programming languages do with values. Log
024 and logs 027 through 035 did that for **operators** — 238 of them,
over 5.79 million probes. Log 036 opened the second half: the
**constructs**, in the owner's three blessed families of access, flow and
binding, designed in `construct_design.md` and its sixteen numbered
decisions.

Log 036 measured four languages and left eight. The four were python,
ruby, php and go. The eight were typescript, c-sharp, rust, c++, dart,
java, swift and kotlin. Log 036 also left php twenty probes short,
because php died twenty times on an error php cannot catch.

This log runs the eight, recovers php's twenty, folds all twelve
together, and clusters the result.

---

## §1 walkthrough

This section is the whole log in order, in plain sentences.

I read the design first. `construct_design.md` states sixteen numbered
decisions and `HARVEST_constructs.md` states which two parts of the
worked example change per language. The two parts are the value encoder
with its trace recorder, and the scaffold table. Everything else was to
be reused unchanged.

I did not rewrite the value encoders. The operator pass already has one
per language, in `l3_exec.py`, and logs 032 and 033 ran every one of
them over the whole value matrix. Reusing a measured encoder keeps new
code off the evidence path. What I added to each was three lines of
trace recorder — a buffer, an append, a dump — which decision 5 already
calls harness machinery.

I wrote the scaffold table for each of the eight languages. A scaffold
is fixed, minimal and inert, which is decision 4, so the only thing that
differs between two probes of one construct is what goes into its slots.

I generated the probes and printed the derived counts before anything
ran. The eight lanes came to 21,342 acceptance probes.

I smoke-tested all eight lanes at about sixty probes each before paying
for the full runs. That caught one fault, and it was mine: typescript's
acceptance route loads no node type declarations, so the recorder's use
of `process` was a type error in every file, and 64 of 64 probes scored
REFUSE. One line of declaration fixed it and the same subset then scored
38 ACCEPT. Had I skipped the smoke run I would have published a
language that refuses everything.

The smoke run caught a second thing, and it is a counting rule rather
than a fault. A flow construct that records no joint wrote no row at
all, so a probe could pass acceptance and leave nothing behind. I made
the trace dump fire even when the trace is empty, because "the construct
ran and recorded nothing" is a measurement and a missing row is not.

I then ran the eight full lanes, one after another, on the serial lane.
Every lane checks its own scratch space before it starts and refuses to
run below 400 MB free, because a memory-backed scratch disk that fills
silently has already voided one run in this node (log 030).

I recovered php's twenty fatals. I read the fatal messages instead of
guessing at them, diagnosed the cause, fixed it, and re-ran only the
twenty, one php process each.

I folded all twelve languages through the completeness gate. All twelve
print COMPLETE. php is now 33,680 of 33,680.

I extended the truthiness table to twelve languages and the trace
comparison to twelve languages.

I pointed the existing clustering machinery at the construct
signatures, swept the cut rather than choosing one, and built the
visual under the same conventions as the three dendrograms before it.

---

## §2 per-language build notes

What the two changing parts required, language by language, and what is
worth keeping.

### typescript

The scaffolds are the plainest of the eight because typescript refuses
almost nothing at the syntax level and a great deal at the type level.

The one thing worth keeping is the recorder fault described in §1. The
acceptance route builds a typescript Program with `types: []`, so the
recorder's `process.stdout.write` had no declaration to lean on. The
repair is `declare var process: any;`, which transpilation erases, so
the execution stage is untouched by it *(measured: the same 64-probe
subset went from 0 ACCEPT to 38 ACCEPT with that one line)*.

### c-sharp

C-sharp's index-range access is spelled `(a)[(b)..(c)]`, which the
catalogue resolved to `range_expression`. That is the same kind rust and
kotlin resolved their slice role to, so the three are spelled alike on
purpose and compare directly.

C-sharp needed no other special handling. Its Roslyn checker runs in
process and scored 3,850 probes in 25.5 seconds *(measured)*.

### rust

Rust is the only one of the eight whose encoder is a TRAIT rather than a
function over a dynamic value. A holder whose type the encoder has no
impl for cannot be recorded at all, and the compiler says so by naming
the recorder's own method.

Those refusals are counted apart as harness refusals and never read as
findings about rust. There are **4 of them** *(measured)*, which is
0.2 percent of rust's 2,122 probes, so the effect on rust's picture is
small but it is stated rather than buried.

Rust's `try` role resolved to `try_expression`, which is the `?`
operator. The honest scaffold is therefore a closure returning an
option, with `?` applied to the slot inside it. That is decision 18
below.

### c++

C++ has no `finally`, so its try scaffold records a try joint and a
catch joint and no finally joint. That is a fact about c++ and it shows
up directly in the trace shape.

C++ is the only one of the eight whose execution stage died. It died 22
times *(measured)*, and each death cost exactly one probe because the
chunk binary takes a start index and the lane restarts past the corpse.
That is the same posture `answers_encoding.md` already gives a death.

### dart

Dart's acceptance instrument is `dart analyze --format=machine`, and
**only severity ERROR counts as a refusal**. This is the log 030 fix and
it is not optional: at any lower severity a dart lint scores a legal
probe as refused.

Dart accepted 426 probes and 207 of them raised at run time
*(measured)*, which is the highest raise rate of the eight. The reason
is dart's `dynamic` holder: the static checker lets a dynamic value into
any slot and the run time then refuses it. That is worth keeping,
because it means dart's acceptance number and dart's answer number
measure two different things and a reader must not add them.

### java

Java's record pattern destructures inside `instanceof` and inside
`switch`. It never destructures in a binding statement. There is no java
`var (p, q) = a`.

So java's binding.unpack role is recorded NOT APPLICABLE with that
reason, which is the same standing go's unpack role already has from log
036's decision 16. Nothing is faked to fill the cell.

### swift

Swift is measured with the **FULL compiler**, never `-typecheck`. Log
034 measured `-typecheck` accepting 1,066 of 2,618 probes the full
compiler refuses, so `-typecheck` is not swift's checker for this
node's purposes.

Swift's grammar declares only eight of the twelve roles, so swift's
lane is the smallest at 706 probes. Its execution stage died 6 times
*(measured)*, and swift traps are exactly the kind of death the start
index exists for.

### kotlin

Kotlin runs through the warm-JVM in-process route, because a cold
`kotlinc` costs about 2.4 seconds per probe and 2,912 probes would have
been nearly two hours of compiler startup. The warm route measured
**203.6 seconds for 2,912 probes**, which is 70 milliseconds each
*(measured)*.

Kotlin's grammar declares no `break` kind and no `continue` kind, so
kotlin has no probes for those two roles at all. Kotlin has both
keywords; the grammar is silent, not the language. Decision 3 keeps
those two readings apart and this log does not infer one from the other.

---

## §3 results

### the eight lanes, as run

Probes planned, probes accepted, and seconds. All measured.

```
lane         probes  accept   raise  seconds
typescript     2287     174       0      6.5
csharp         3850     269      48     26.2
rust           2122      63       2     31.4
cpp            2482     309       0    149.0
dart           2685     426     207      9.1
java           4298     269      15     28.9
swift           706      55       0     48.1
kotlin         2912     192      11    208.9

total         21342    1757     283    508.1
```

The seconds column is the whole lane, both stages, including compiler
startup and the writing of every probe source.

### the completeness gate, all twelve

```
language      rows  planned  missing
go            1710     1710        0
rust          2122     2122        0
cpp           2482     2482        0
swift          706      706        0
dart          2685     2685        0
csharp        3850     3850        0
kotlin        2912     2912        0
java          4298     4298        0
typescript    2287     2287        0
python       59797    59797        0
ruby         48297    48297        0
php          33680    33680        0

total       164826   164826        0
```

**All twelve print COMPLETE** *(measured)*. php's row is 33,680 of
33,680 rather than log 036's 33,660, which §7 explains.

### deaths and harness refusals

```
cpp        22 deaths
swift       6 deaths
rust        4 harness refusals
everything else   none
```

A death costs one probe and is recorded as a death. A harness refusal is
counted apart and is never read as a finding about the language.

---

## §4 truthiness, the full twelve-language table

The if-condition slot takes one operand. Run over every holder and every
value class, that single slot IS the cross-language truthiness table.
This is the table the owner singled out in the design.

Read the codes like this.

```
T   always then
E   always else
S   splits: some values then,
    some values else
R   refused: the checker would not
    accept a value of that form in
    a condition at all
p   part refused: some holders of
    that form accepted, some not
-   not probed
```

The twelve languages against the eight forms. Column headings are the
first two letters of the form: nothing, truth, whole, fractional, text,
sequence, keyed, nesting.

```
            no tr wh fr tx sq ke ne
go           R  T  R  R  R  R  R  R
rust         R  T  R  R  R  R  R  R
cpp          p  T  T  T  p  p  R  R
swift        R  T  R  R  R  R  R  R
dart         p  T  R  R  R  R  R  R
csharp       R  T  R  R  R  R  R  R
kotlin       R  T  R  R  R  R  R  R
java         R  T  R  R  R  R  R  R
typescript   p  T  T  T  T  T  T  T
python       E  S  S  S  S  S  S  T
ruby         E  S  T  T  T  T  T  T
php          E  S  S  S  S  S  S  T
```

Three readings, all measured.

**Which languages refuse a non-boolean condition, and which coerce
one.** Seven refuse everything but truth: go, rust, swift, dart,
c-sharp, kotlin and java. Five coerce: c++, typescript, python, ruby
and php. The line is not the static-against-open line — c++ and
typescript are statically checked and coerce, and the coercing five do
not otherwise group.

**c++ and typescript coerce differently.** C++ admits whole and
fractional and part of text and sequence, and flatly refuses keyed and
nesting: a `std::map` has no conversion to bool. Typescript admits every
form, because every javascript value has a truthiness.

**The open three do not agree with each other.** Python, php and ruby
all send nothing to the else arm — that is the one cell all three share.
They then split: ruby sends every other form to the then arm without
exception, because in ruby only `nil` and `false` are false, while
python and php both split whole, fractional, text, sequence and keyed by
value, because zero and empty are false in both.

The nine statically checked languages are measured at the HOLDER grain.
Their verdict is a function of the holder, so a cell reading **T** there
was accepted, not proved uniform over its values. The three open
languages are measured at the VALUE grain and their **S** cells carry
counts.

---

## §5 trace findings

A trace is the flow family's answer. It is written in the same bits and
type encoding as an operator's answer, which is what makes two
languages' traces comparable at all.

### worked example one: a for over the sequence 1, 2, 3

Every language's canonical sequence holder carries the same three whole
numbers at its `base` value class. Eleven of twelve walk the values.

Java, and it is the shape ten others share:

```
Kflow.for_20|-|TRACE:3[
  IT=INT:64:0000000000000001,
  IT=INT:64:0000000000000002,
  IT=INT:64:0000000000000003]
```

Go, and go alone:

```
Kflow.for_12|-|TRACE:3[
  IT=INT:64:0000000000000000,
  IT=INT:64:0000000000000001,
  IT=INT:64:0000000000000002]
```

**Where the index-against-value split lands across the twelve: at
exactly one language, and it is go** *(measured)*. Go's `for ... range`
over a slice binds the INDEX to a single loop variable, so go's trace
reads 0, 1, 2 where every other language's reads 1, 2, 3. Nothing in the
scaffold differs; the same three lines were written for all twelve.

Typescript agrees on the values and disagrees on the type:

```
Kflow.for_10|-|TRACE:3[
  IT=FLOAT:64:3ff0000000000000,
  IT=FLOAT:64:4000000000000000,
  IT=FLOAT:64:4008000000000000]
```

Those three bit patterns are 1.0, 2.0 and 3.0. A javascript number is a
double, so typescript's loop over three whole numbers is a loop over
three floats, and the encoding says so without anyone having to argue
about it.

### worked example two: a break at k = 2

The loop is the fixed sequence 1 through 5 in every language, so the
only thing that varies is the language.

```
cpp         TRACE:2[IT=INT:32:00000001,STOP=1]
csharp      TRACE:2[IT=INT:32:00000001,STOP=1]
dart        TRACE:2[IT=INT:64:0000000000000001,STOP=1]
go          TRACE:2[IT=INT:64:0000000000000001,STOP=1]
java        TRACE:2[IT=INT:32:00000001,STOP=1]
kotlin      ABSENT: the grammar declares no break kind
php         TRACE:2[IT=INT:64:0000000000000001,STOP=1]
python      TRACE:2[IT=INT:64:0000000000000001,STOP=1]
ruby        TRACE:2[IT=INT:64:0000000000000001,STOP=1]
rust        TRACE:2[IT=INT:32:00000001,STOP=1]
swift       TRACE:2[IT=INT:64:0000000000000001,STOP=1]
typescript  TRACE:2[IT=FLOAT:64:3ff0000000000000,STOP=1]
```

**Eleven of eleven agree on the SHAPE and disagree only on the width of
the integer** *(measured)*. Break at k stops after k minus one
iterations in every language that has a break, and the trace records the
same two joints everywhere.

The widths are a language fact and not a disagreement: c++, c-sharp,
java and rust default a small integer literal to 32 bits, and dart, go,
php, python, ruby and swift to 64. Typescript has no integer at all.

Kotlin's line reads ABSENT rather than MISSING, and the difference
matters. Kotlin's grammar declares no break kind, so kotlin was never
probed for it. A reader must not read that gap as a lost probe, and the
generated file now says so in words.

### what a trace shows that an answer cannot

At break k = 5 the trace carries four iteration joints and then STOP=4.
At k = 1 it carries STOP=0 and nothing else, because the break is
reached before the first recorded iteration. An operator's answer has no
way to say either of those things; the trace does, and it says it the
same way in eleven languages.

---

## §6 construct clustering

### the leaf, and why the constructs get their own picture

**Decision 17. The construct signatures get their own dendrogram and are
NOT merged into the operator tree.**

The reason is a measured difference of grain, not a taste. Nine of the
twelve construct lanes report at the holder grain, where a form pair is
present or absent and never partially so. The operator tree's leaves
carry value-matrix density behind every cell. Pouring the two into one
tree would put a construct beside an operator whenever both were empty,
and emptiness is what nine languages have most of.

Cost to overturn: re-running `l3_construct_cluster.py` with `COMBINE`
set to true.

The method is unchanged from logs 030, 031 and 033. The distance is the
jaccard of the domains, the linkage is average, the cut is SWEPT and
never chosen, and the plateaus are read off the sweep.

### the leaves

```
construct signatures    149
non-empty domain        129
empty domain             20

by family
  access                 13
  flow                   67
  binding                49
```

An empty domain means the construct was probed and nothing was answered.
Twenty of the 149 are in that state, and admitted-and-empty is not the
same as excluded — the same standing log 035 gave typescript's
`instanceof`.

### the plateau summary

```
0.81..0.87   width 0.06    42 clusters
0.53..0.59   width 0.06    27 clusters
0.39..0.45   width 0.06    17 clusters
```

**No plateau is wider than 0.06, and there is no elbow** *(measured)*.
That is the same shape log 030 found for the operators and the same
reason no cut is chosen here either. The three readings above are the
only bands at least 0.05 wide in the entire sweep.

The reading at 42 clusters is the most stable one available and it is
not a language reading: constructs of the same role across different
languages join before constructs of different roles inside one language,
wherever the domains are wide enough to overlap at all.

### where constructs land relative to operators

This is measured rather than asserted, and the measurement has a limit
that must be stated first.

**87 of the 129 construct leaves are ONE-SLOT and share no key space
with an operator** *(measured)*. An operator opens two operand
positions and a one-slot construct opens one, so their domain keys
cannot meet. Saying so is more honest than recording a zero.

For the 42 two-slot construct leaves — index access and augmented
assignment — the nearest operator signature by the same jaccard is:

```
median jaccard   1.000
lowest           0.053
highest          1.000
n                   42
of these, nearest an operator of
their own language:  20 of 42
```

**The median is exactly 1.000** *(measured)*. A two-slot construct's
accepted domain very often coincides EXACTLY with some operator's
accepted domain. That is the sharpest single result of this pass:
whatever the compiler is doing when it decides which pairs of holders
`a[b]` will take, it is the same decision it makes for some operator's
operand pair.

That fewer than half sit nearest an operator of their own language is
recorded and **unverified** as to cause.

### the visual

`dendrogram_constructs.html`, 129 leaves, 257 nodes, built by
`make_dendrogram_constructs.py` from the same template as
`dendrogram_sweep.html`, `dendrogram_answers.html` and
`dendrogram_all12.html`. Same icicle rendering, same similarity axis,
same draggable threshold line, same live cluster count, same outline on
the current clusters, same search box, same hover card, same shaded
plateau curve. Self-contained; it opens from `file://`.

**Validated under the DOM stub** *(measured)*: 1 script run, 1 ok, 0
threw; the icicle and the curve each append their drawing; `#count`
reads 34 at the default threshold of 0.700; `#legend` and `#plateaus`
are both filled.

The stub also reports three EMPTY PANELS named smat, sops and worked.
Those three panels belong to log 033's twelve-language visual and do not
exist in this one, because a construct has no spelling to share with
another language's construct in the way an operator does. The stub's
checklist is hard-coded to the log-033 page; the reading is a checklist
mismatch and not a broken picture, and I left the stub alone because it
is log 033's instrument.

`dendrogram_all12.html` was re-validated at the same time and is
unchanged: 2 scripts run, 0 threw, `#count` reads 115 at 0.700.

---

## §7 remainders

### php's twenty fatals: RECOVERED

Log 036 left php 20 probes short. This log recovers all twenty
*(measured)*.

I read the fatal messages rather than guessing. All twenty say `Cannot
redeclare class R<x>_<n>`. That is the harness's own class-name suffix
failing, and it is not php refusing a construct. The php driver suffixes
a declared class name with the PROBE NUMBER. When one probe's two slots
are filled by two holders whose declaration text declares the SAME class
name, both get the same suffix and the second declaration redeclares the
first.

The fix is one line of the generator: the suffix is made per SLOT as
well as per probe, so the left declaration's classes end `_A` and the
right's end `_B` before the probe number goes on. Nothing else about the
probe changes.

The recovery ran only the twenty indices, one php process each, so a
residual fatal would still have cost one probe. None died again. All
twenty now answer, and all twenty are the same holder paired with
itself:

```
Kaccess.subscript_16_16_flat_flat|-|RAISE:Error
Kbinding.augassign+=_16_16_flat_flat|-|RAISE:TypeError
```

Holder 16 is php's class-declaring holder, which confirms the diagnosis
from the other side: every fatal was a probe that paired that holder
with itself. The recovered rows are folded BESIDE the original file and
`raw/kc_php.txt` is left exactly as the first run wrote it.

### what this pass did not do

**The answer grain for the nine checked languages was not run.** This
pass measured them at the HOLDER grain — every holder at its base value
— which is 21,342 probes against the design's derived 624,166 for the
full value matrix. The design's §h counts are unchanged and still stand
as the cost of the value grain. Whether a construct's domain moves when
the value varies is **unverified** for the nine, and it is exactly the
question log 030's decision 9 answered for the operators by measuring
it.

**Rust's four harness refusals are not repaired.** Repairing them means
adding impls to a measured encoder, and this pass had no other reason to
touch it.

**The one-slot constructs cannot be compared with the operators at
all** under the present key space. A probe space that gave an operator a
one-operand form would close that, and nothing of the kind is built.

**c++ has no finally joint.** Where a try reaches no throw, java,
typescript and dart all record two joints — `BR=try` then `BR=finally` —
and c++ records one, `BR=try` alone *(measured)*. That is a language
fact and not a gap, but a reader comparing try traces across twelve must
know it before reading the shorter trace as a shorter run.

### decisions added by this log

```
17  the construct signatures get their own
    dendrogram; they are not merged into the
    operator tree
      reason: a measured difference of grain
      cost to overturn: one flag and a re-run

18  rust's flow.try role is probed as the `?`
    operator inside a closure returning an
    option, because `try_expression` is the
    kind the catalogue resolved
      cost to overturn: a re-run of one
      construct in one language

19  java's binding.unpack role is NOT
    APPLICABLE: java's record pattern
    destructures inside `instanceof` and
    `switch`, never in a binding statement
      cost to overturn: none; it is a reading
      of the language, and the cell is empty
      rather than faked

20  a flow or binding probe writes its trace
    row even when the trace is empty, so that
    every probe leaves exactly one row
      cost to overturn: a re-read
```

### artifacts

```
l3_construct_lang.py
    the eight lanes: the encoders' trace
    recorders and the scaffold tables
l3_php_recover.py
    the twenty-fatal recovery
l3_construct_read.py
    the fold, now over all twelve
l3_construct_cluster.py
    the construct clustering and the sweep
make_dendrogram_constructs.py
    the visual
clusters_constructs.json
dendrogram_constructs.html
truthiness_table.md
trace_compare.md
construct_index.json
construct_answers_<lang>.json  (twelve)
manifest_construct_<lang>.json (eight, frozen
    before their runs)
manifest_php_recover.json
raw/kx_<lang>.txt   acceptance verdicts
raw/ky_<lang>.txt   answers and traces
raw/kb_<lang>.txt   the two merged, one row
    per probe
raw/kz_php.txt      the twenty recovered rows
```
