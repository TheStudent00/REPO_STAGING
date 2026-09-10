# log 038 — the constructs at the value grain

Date: 2026-08-19. Node:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

Written in the readable register of logs 034 through 037. Every word
this node invented is defined before it is used. Every claim carries
its level.

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
        constructs. `+` is an operator, and
        logs 024 to 035 measured those.

holder
    one way a language can hold a value: a
    declared type plus the statement that
    declares it.
    example tied to context:
        java holds a list of whole numbers as
        `List.of(...)`, and that is one of
        java's thirty-two holders.

value class
    one named value a holder can be given.
    example tied to context:
        java's whole-number holder has value
        classes named `base`, `zero`, `neg`,
        `i64max` and more.

holder grain
    every holder at ONE value, its base.
    log 037 measured the nine checked
    languages this way.
    example tied to context:
        `Kflow.if_2` is a holder-grain probe
        id: holder 2, value unstated.

value grain
    every holder at EVERY value class.
    this log measures the nine that way.
    example tied to context:
        `Kflow.if_2_true` and `Kflow.if_2_false`
        are the two value-grain probes that
        holder-grain probe stood for.

the nine checked languages
    go, rust, c++, swift, dart, c-sharp,
    kotlin, java and typescript. each has a
    checker that scores a probe legal or not
    without running it.
    example tied to context:
        the nine are what this log raises to
        the value grain.

the three open languages
    python, ruby and php. they have no
    separate checker, so running a probe is
    the only evidence that it was legal.
    example tied to context:
        the three were already at the value
        grain and cannot move.

shard
    a contiguous slice of one language's
    probes, run as one job. a shard is a unit
    of SCHEDULING and never of measurement.
    example tied to context:
        java's 89,698 probes ran as fifteen
        shards of about six thousand.

completeness gate (also: gate)
    a check run after a lane finishes. it
    compares the rows written with the probes
    planned and prints COMPLETE only on a
    match.
    example tied to context:
        the gate reads a language's shards
        added together, never one at a time.

message check
    a check that sits BESIDE the gate and
    reads the refusal messages. a refusal
    that names the instrument rather than the
    language is not a measurement.
    example tied to context:
        1,031 go rows said "no space left"
        and the gate could not see it.

harness refusal
    a refusal whose message names the
    RECORDER rather than the construct. it is
    the measuring instrument refusing, not
    the language.
    example tied to context:
        rust refused two probes because its
        encoder had no impl for a type the
        probe itself declared.

trace
    what a flow construct gives back instead
    of an answer: the sequence of values at
    each joint, in the same bits encoding as
    an answer.
    example tied to context:
        a for loop over an empty list records
        TRACE:0 and over a three-item list
        records TRACE:3.

movement
    the difference between a construct's
    holder-grain verdict and its value-grain
    verdicts. if they disagree, the verdict
    MOVED.
    example tied to context:
        c-sharp's slice role read `raise` at
        the holder grain and reads answer,
        raise AND refuse at the value grain.

key space
    the shape of the keys a signature's
    domain is written in. an operator's keys
    are ordered form PAIRS.
    example tied to context:
        a one-slot construct has one-form
        keys, so it cannot meet an operator's
        keys at all.
```

---

## what came before this log, restated

Nothing below assumes the reader remembers the earlier logs.

The node measures what twelve programming languages do with values.
Logs 024 and 027 through 035 did that for **operators** — 238 of them,
over 5.79 million probes. Logs 036 and 037 did the first half of the
**constructs**, in the owner's three blessed families of access, flow and
binding, designed in `construct_design.md` and its twenty numbered
decisions.

Log 037 finished all twelve languages and closed with two admissions,
which the node's CHECK carries as items 5t and 5u.

Item 5t said the nine checked languages had been measured at the
HOLDER grain only. Every holder was handed one value, its base. That
is 21,342 probes against the design's derived 624,166 for the full
value matrix. Whether a construct's domain MOVES when the value varies
was left unverified.

Item 5u said rust had four refusals whose messages named the recorder
rather than the construct, and that nobody had repaired them.

This log closes both.

---

## §1 walkthrough

This section is the whole log in order, in plain sentences.

I read the design first, then log 037, then the two open CHECK items.
`construct_design.md` §h derives 624,166 answer probes across twelve
languages, and I re-ran `construct_space.py` rather than trusting the
number in the document. The script printed 624,166 again, so the
design's arithmetic reproduces.

I then asked what that number actually counts, because a derived
number can be right and still be the wrong number. It counts the full
value matrix for all twelve. The nine checked languages' share of it is
482,301. Taking out `break` and `continue`, which open no operand slot
and therefore have no value grain at all, and taking out the two roles
the catalogue marks NOT APPLICABLE, leaves **481,978**, and that is
what I generated. The difference is 323 probes and every one of them is
accounted for by a rule already written down.

I found the reason the holder grain was not merely coarse but wrong.
`construct_space.py` states in words that "in a statically checked
language the verdict is a function of the holder pair and not of the
value". That reading is false. A holder's declaration text is not fixed
across its value classes: java's `List.of(...)` holder declares
`List<Long>`, `List<String>` and `List<Object>` at three different
value classes, and those are three different types. I measured how
widespread that is before generating anything: **79 of the 226 holders
of the nine change their declared type with the value class**. A
verdict measured at one value was therefore never a verdict for the
holder, and 5t was a larger hole than log 037 thought.

I wrote `l3_construct_value.py`. It reuses the scaffolds, the
recorders, the encoders and the lane machinery of log 037 without
touching them, because reusing a measured instrument keeps new code off
the evidence path. The only thing it changes is what fills a slot:
where log 037 wrote the base value, it writes every value class, and
the probe id carries the value class exactly as decision 14 specifies.

I cut each language into shards small enough that no shard could
approach the daemon's one-hour kill, and froze a manifest beside every
one of them. Sixty-eight shards, sixty-eight manifests.

I smoke-tested all nine lanes at about sixty probes each before paying
for the full runs. Every lane produced acceptance rows and answer rows,
and none refused everything. That is the log 037 lesson applied.

I ran the sixty-eight shards on the serial lane in cost order, kotlin
last through the warm-JVM route.

Four harness faults surfaced, and each one is written up where it was
found rather than smoothed over. Two of them are 5u itself and are
described below. The third is a duplicated import in rust, which a
verification lane caught only because I built one to prove the second
repair. The fourth is the one that matters most: go's driver kept every
probe's compiled binary, filled the four-gigabyte scratch disk part way
through the run, and from that point `go build` failed for a reason
that had nothing to do with the probe. The driver recorded those
failures as REFUSALS. **The completeness gate read COMPLETE over them,
because the rows were there.** I added a message check beside the gate,
fixed the driver to delete each binary as soon as it had read the
result, and re-ran go from the beginning.

The scratch guard itself worked exactly as written. When the disk fell
below the four-hundred-megabyte floor, later lanes REFUSED to start
rather than producing garbage, and one dart shard stopped its execution
stage part way and recorded the untouched probes as MISSING rather than
as answers. Both were re-run.

I repaired 5u by reading the four messages instead of guessing at them,
and found they were two different things rather than one. Two named the
recorder's own method and were genuine harness refusals; they are
repaired and now answer. Two named rust's `Borrow` trait, which is
rust's and not the recorder's; they were rust findings that log 037's
classifier had swept up by matching a token that was too wide. The
classifier is narrowed and those two now read as what they are.

I folded eight languages through the gate and the message check — go,
rust, c++, swift, dart, c-sharp, java and typescript — wrote the
truthiness table and the trace comparison over again at the value
grain, and re-folded the clustering with what was measured at the time
I wrote.
Two lanes were still owed when I closed the log: one dart shard and
kotlin's nine. Swift's three landed while I was writing and are folded
into every artifact and every count below. The log says in every place
it counts them which languages are in and which are owed, rather than
reporting a total it does not have.

I found the completeness gate's own blind spot while checking dart. The
gate compares rows written against probes PLANNED, and it takes the
planned number from each shard's closing summary line. A shard that
produced an EMPTY file therefore contributes zero planned and zero
rows, and the gate reads COMPLETE over a language that is one shard
short. The frozen manifests are the fix and were already on disk: the
manifests say 481,978 probes and the gate said 409,196, and the
difference is exactly the lanes still owed. Every count below is
stated against the manifests.

I found a second thing of the same kind in the lane machinery, not in
the arithmetic. Ten shard scripts were sitting in the drop directory
unrun, and they were not queued: the daemon fires on a file EVENT, and
those files' events had already been spent on an earlier run that
refused for want of scratch. A script that is present is not a script
that is queued. Re-writing each file in place made the event fire again
and the queue took them.

I revisited decision 17, which had kept the constructs out of the
operator tree. Its stated reason was a difference of grain, and this
log removes that difference, so the reason is gone. A second reason
stands and was never about grain: an operator opens two operand
positions and a one-slot construct opens one, so their keys cannot
meet. I therefore put the two-slot constructs into one tree with the
operators and left the one-slot constructs in a tree of their own. The
division is now by key space, which is measured, rather than by grain,
which has dissolved.

---

## §2 the counts, and the runs

### the derived counts, printed before anything ran

The design's column is `construct_design.md` §h. The generated column
is what `l3_construct_value.py` printed.

```
language     generated   design §h
typescript      40,700      40,710
csharp          85,587      85,597
java            89,698      89,857
dart            51,867      51,877
rust            47,736      47,746
go              39,104      39,208
cpp             49,170      49,180
swift           13,334      13,344
kotlin          64,782      64,782

TOTAL          481,978     482,301
```

The 323-probe difference is fully accounted for. Ten probes per
language are `break` and `continue`, which open no operand slot and
have no value grain; kotlin's grammar declares neither, so kotlin
contributes none of those. That is 80. The remaining 243 are go's and
java's unpack roles, which are recorded NOT APPLICABLE with a reason by
log 036's decision 16 and log 037's decision 19.

**The design's 624,166 is arithmetically correct and reproduces**
*(measured)*. What this log adds is what it counts.

### the lanes, as run

A shard is a unit of SCHEDULING and never of measurement, so this
table is here to say what the machine did and not what the pass found.
Elapsed is the daemon's own number, added over that language's shards.

```
language     shards   elapsed   state
typescript        6     114 s   all landed
csharp           11     445 s   all landed
java             15     677 s   all landed
dart              7     182 s   six landed, one owed
rust              4     711 s   all landed
go                4     717 s   all landed, RE-RUN whole
cpp               9   3,218 s   all landed
swift             3     855 s   all landed
kotlin            9         -   nine owed, first
                                shard RUNNING

landed so far           6,919 s   = 1 h 55 m
```

go's line says RE-RUN because its first value run is void and is not
counted anywhere in this log. The reason is written up in §1: the
driver kept every probe's binary, the scratch disk filled, and from
that point the failures were the disk's and not go's.

### the completeness gate

The gate reads a language's shards ADDED TOGETHER. It prints COMPLETE
only when rows written equal probes planned. Beside it sits the message
check, which reads the refusal TEXT and counts any row whose message
names the instrument rather than the language.

```
language     planned      rows   missing  suspect  gate
typescript    40,700    40,700         0        0  COMPLETE
csharp        85,587    85,587         0        0  COMPLETE
java          89,698    89,698         0        0  COMPLETE
rust          47,736    47,736         0        0  COMPLETE
go            39,104    39,104         0        0  COMPLETE
cpp           49,170    49,170         0        0  COMPLETE
swift         13,334    13,334         0        0  COMPLETE
dart          51,867    43,867     8,000        0  ONE SHARD OWED
kotlin        64,782         0    64,782        -  RUNNING

FOLDED       409,196   409,196         0        0  COMPLETE
PLANNED      481,978   409,196    72,782        -  84.9 percent
```

The planned column is the frozen manifests', not the shards'. That
distinction is the gate fault of §1: read from the shards, dart's line
would say 43,867 of 43,867 and print COMPLETE while a shard was
missing. **Sixty-eight manifests exist, one per shard, and they sum to
481,978, which is the generated total §2 opened with** *(measured)*.

Suspect rows are zero in all eight folded languages *(measured)*. go's
void run had 1,031.

---

## §3 truthiness movement at the value grain

### the finding, in one sentence

**Every one of the eight checked languages folded so far reads
always-then for the truth form at the holder grain and SPLITS at the
value grain, so log 037's `T` in that column was an artifact of the
base value and not a fact about any language** *(measured)*.

### restated

The if-condition slot takes one operand. Log 037 handed that slot one
value per holder — the holder's base — and the base value class for a
truth holder is `true`. A slot that is only ever handed `true` can only
ever answer `then`. The table it produced was therefore not wrong so
much as unable to be wrong.

At the value grain the same slot is handed `true` AND `false`, and
every language that admits a truth value into a condition sends one to
each arm. The cell now reads `S`, for splits.

### what moved, cell by cell

`T>S` means the cell read always-then at the holder grain and splits at
the value grain. A dot means the cell did not move.

```
            no tr wh fr tx sq ke ne
go           .  T>S  .   .   .   .   .   .
rust         .  T>S  .   .   .   .   .   .
cpp          .  T>S T>S T>S  .   .   .   .
swift        .  T>S  .   .   .   .   .   .
dart         .  T>S  .   .   .   .   .   .
csharp       .  T>S  .   .   .   .   .   .
java         .  T>S  .   .   .   .   .   .
typescript   .  T>S T>S T>S T>S  .   .   .
```

Two languages moved in more columns than the truth one, and they are
exactly the two checked languages log 037 found to COERCE: c++ moved on
whole and fractional, typescript on whole, fractional and text. That is
the expected shape and it is worth saying why it is expected: a
language that refuses a form in a condition outright cannot split on
it, because there is nothing to split. **The six refusing languages
moved in one column and could not have moved in any other**
*(derived)*.

Kotlin is NOT in this block. Its row in `truthiness_table.md` is log
037's holder-grain letters carried forward, and the table now says so
in its own text. The `T` in that row means accepted at one value and
NOT proved uniform over its values. Swift's row was in that position
while this section was being written and moved out of it when swift's
three shards landed: swift's truth cell now reads `S`, like the other
seven.

### the same question asked of every construct, not just the condition

The condition slot is one construct. The movement check asks the same
question of all of them: group every value-grain probe under the
holder-grain probe it refines, and ask whether the refined verdicts
agree with the coarse one.

```
language     holder keys   split by value   disagrees
typescript          2,277               27          27
csharp              3,840              153         153
java                4,288              167         167
dart                2,375              141         141
rust                2,112               25          26
go                  1,700               70          70
cpp                 2,472               88          88
swift                 696               22          22

TOTAL              19,760              693         694
```

**693 of 19,760 holder keys — 3.5 percent — hide a verdict that
depends on the value** *(measured)*. That is a small fraction and it is
not a small finding, because nothing about the holder grain told anyone
WHICH 3.5 percent, and one of them is the whole truthiness table.

rust's disagrees exceeds its splits by one. That single key agrees with
itself across its values and disagrees with the holder-grain run, which
is the 5u repair showing through: the probe that was a harness refusal
in log 037 now answers.

---

## §4 trace findings at the value grain

### does break-at-k depend on the value?

**No, and the reason it cannot is structural rather than measured:
`break` and `continue` open no operand slot, so they have no value
grain at all** *(derived)*. They are the ten probes per language §2
subtracted. Log 037's finding stands unchanged and unchallenged: break
at k agrees in shape across all eleven languages that have a break, and
differs only in integer width.

What DOES depend on the value is the loop the break sits in, and that
is the question the value grain could reach for the first time.

### the while guard decides whether the loop runs at all

A while probe records `TRACE:<n>` for the number of times it went
round. At the holder grain each while holder had one guard value and so
one trace length. At the value grain the same holder records **either 0
steps or 9** and nothing between, in every language that has a while
and admits more than one value into its guard *(measured)*:

```
language     while keys   keys whose step count varies
rust                  1                              1
cpp                  11                              7
java                  2                              2
csharp                1                              1
typescript           22                              5
dart                  1                              1
```

Swift's lane landed after this table was computed and does not change
its shape; swift declares one while holder and it behaves as dart's
does.

The 0-or-9 shape is the guard being read as a truth value and nothing
else: a guard that reads false never enters, a guard that reads true
runs to the recorder's cap. It is §3's truthiness finding seen from
inside a loop, and the two were measured by different probes.

### the for-iterable's length follows the value, and by how much differs

`trace_compare.md` is rewritten at the value grain and now prints, per
holder, the SET of step counts that holder's value classes produced.
Log 037 could only print one number per holder, because it only had one
value per holder.

```
rust    holder 11 text        steps 0,2,4,5,9
cpp     holder 12 text        steps 0,1,5,9
dart    holder 13 sequence    steps 0,2,3,5
csharp  holder 21 sequence    steps 0,1,2,3,5
python  holder 12 sequence    steps 0,1,2,3,5
```

Two things are visible here that the holder grain hid. The first is
that **a container holder's trace length is the container's length and
the value class is what sets it** — obvious once written down and
unmeasured until now. The second is a disagreement between languages
about the SAME value class: rust's text holder walks a text of 5 as 2
steps where c++'s walks it as 1, because the two languages disagree
about what a text is made of. That is a layer-1 disagreement surfacing
through a layer-3 construct.

Eleven of the twelve languages appear in the rewritten table. Kotlin
does not, because its probe ids carry no value class yet — its lane is
the one still owed.

---

## §5 the re-folded clustering

### what was done

Two trees were re-folded, and the second one is new.

The first is the constructs' own tree, `clusters_constructs.json` and
`dendrogram_constructs.html`, rebuilt on the value-grain signatures:

```
construct signatures                133
  with a non-empty domain           123
  probed and answered nothing        10
families      access 18, binding 54, flow 51
plateaus      0.10..0.17  width 0.07    6 clusters
              0.81..0.87  width 0.06   45 clusters
              0.54..0.59  width 0.05   28 clusters
one-slot leaves                        78
nearest operator, by jaccard   median 0.929
                               lowest 0.053
                              highest 1.000  n 45
of those 45, nearest an operator
of their OWN language                  20
```

Log 030's no-elbow finding holds again at the value grain: **the widest
plateau is 0.07 and it is the degenerate six-cluster one; no
non-degenerate plateau is wider than 0.06** *(measured)*.

### why the constructs can now share a tree with the operators

Decision 17 of log 037 kept the constructs out of the operator tree,
and it gave ONE reason: a measured difference of grain. Nine of the
twelve construct lanes reported at the holder grain, where a form pair
is present or absent and never partly so, while every operator leaf
carried value-matrix density behind it. Pouring the two into one tree
would have joined a construct to an operator whenever both were empty,
and emptiness was what nine languages had most of.

**This log removes that difference for eight of the nine, so the reason
it gave is gone.** A reason that has dissolved should not be left
standing as a rule, so decision 17 is overturned for everything it
covered.

A SECOND objection stands, and it was never about grain. An operator
opens TWO operand positions. A one-slot construct opens ONE. Their
domain keys are written in different spaces, so they cannot be compared
at all, however either was measured.

**DECISION 21.** The division is by KEY SPACE rather than by grain.
The two-slot constructs — index access and augmented assignment — join
the operators in one tree, because they share the operator's ordered
form-pair key space exactly. The one-slot constructs keep a tree of
their own, because there is no one-operand operator signature for them
to sit beside, and saying so is more honest than recording a zero.
Cost to overturn: a probe space that gives an operator a one-operand
form, which nothing of the kind is built.

```
joint tree            284 leaves
  operator leaves     239
  construct leaves     45   (the two-slot ones)
left in their own tree 78   (the one-slot ones)

nearest leaf to each two-slot construct
  an OPERATOR          13
  a CONSTRUCT          32
  of its own language  19 of 45
  jaccard   median 1.000  lowest 0.400

plateaus  0.85..0.90  width 0.05   75 clusters
          0.24..0.29  width 0.05   10 clusters
```

The median jaccard of exactly 1.000 says what log 037 already saw from
outside the tree and could not act on: **a two-slot construct's
accepted domain very often coincides EXACTLY with some operator's**
*(measured)*. Now that they sit in one tree, thirty-two of the
forty-five find another construct nearer than any operator, which is
the result that would have been unavailable while the two lived apart.

### the visual

`Research/kind_fuzz_clustering/dendrogram_constructs.html` — 123
leaves, 245 nodes, 0.07 MB, self-contained, opens from `file://`.

Validated under `domstub.js`, the same instrument log 033 built:
**1 script run, 1 ok, 0 threw**; the icicle and the curve each append
their drawing; `#legend` 825 chars, `#plateaus` 309 chars; `#count`
reads 35 at the default 0.700 threshold *(measured)*. The stub also
names three EMPTY PANELS — `smat`, `sops`, `worked` — which belong to
log 033's page and do not exist on this one. That is a checklist
mismatch and not a broken picture, and the stub is left alone because
it is log 033's instrument.

**What is IN the picture: eight languages at the value grain and one —
kotlin — at log 037's holder grain.** It will need one more fold when
kotlin's nine shards land, and §6 says exactly how.

---

## §6 remainders, 5u, and harvest

### 5u, rust's four harness refusals — CLOSED

The four messages were READ rather than guessed at, and they turned out
to be two different things.

Two named the recorder's own method: `the method 'db' exists for
reference '&R3', but its trait bounds were not satisfied`, and the same
for `&Node`. `db` is the recorder's encoder. A holder whose type the
encoder has no impl for cannot be recorded, so the probe never reached
a verdict about the construct at all. Those two are genuine harness
refusals and they are repaired: at the value grain
`Kbinding.assign_19` and `Kbinding.assign_21` record BIND traces across
their value classes *(measured)*.

Two named rust's `Borrow` trait: `the trait bound 'String:
Borrow<[i64]>' is not satisfied`, which rust says when IT refuses to
index a string-keyed map with a slice of whole numbers. `Borrow` is
rust's own trait and not the recorder's. Those two were never harness
refusals; log 037's classifier matched the bare token "trait bound",
which is too wide, and swept them up. The classifier is narrowed to the
recorder's method name, and at the value grain **44 rows carry the
`Borrow` message and every one of them is read as what it is, a rust
refusal** *(measured)*.

**rust's value-grain lane records ZERO harness refusals** *(measured)*.
The two that remain in `raw/kb_rust.txt` are log 037's holder-grain
file, which is left exactly as it was written.

### what is still running

Two lanes, 72,782 probes, 15.1 percent of the pass.

```
lane            probes    state at close of log
kv_kotlin_00..08 64,782   shard 00 RUNNING, eight
                          queued behind it
kv_dart_04.sh    8,000    queued
kv_swift_00..02  13,334   LANDED and folded, 855 s
```

Swift is done and its numbers are in every table above. Its three
shards cost 855 s at **64 ms a probe** *(measured)*, which is what full
compilation costs and is why log 034 made swift last.

Kotlin's running shard prints **87 ms a probe** *(measured)*, close to
the 70 ms its holder-grain lane measured through the same warm-JVM
route. Nine shards of 8,000 acceptance probes at that rate is about
**105 minutes** before the execution stages, so the honest estimate for
the whole tail is **about two hours from the close of this log**
*(derived)*. Dart's remaining shard is thirty seconds and is queued
behind kotlin only because kotlin's event reached the daemon first.

Swift is the expensive one and it is expensive for a reason log 034
established: `swiftc -typecheck` is not the swift compiler and accepts
lines the full compiler refuses, so swift's lane pays for full
compilation. Kotlin goes through the warm-JVM route at about 70 ms a
probe, which its holder-grain lane measured. On those two numbers the
tail is **hours and not days**, and no estimate finer than that is
honest, because neither language's value-grain lane has produced a
progress line yet.

### how to harvest them

Nothing needs writing. Every step below is a script already on disk and
already run once in this session.

```
1  check the lanes are done
   SandboxDesign/agent/status/kv_<lang>_<nn>.sh.status
   state=done AND exit=0.  exit 0 is not
   evidence; it is only permission to look.

2  fold and gate
   python3 l3_value_fold.py
   reads agent/out directly.  prints the
   gate and the suspect-row count per
   language.  do not proceed on SHORT or
   CONTAMINATED.

3  check the gate against the MANIFESTS and
   not against itself
   the planned column comes from the shard
   summaries, so an EMPTY shard file reads
   COMPLETE.  sum manifest_value_<lang>_*.json
   and require 481,978 in total, of which
   dart 51,867, kotlin 64,782, swift 13,334.

4  rewrite the signatures and the two tables
   python3 l3_construct_read.py
   python3 l3_value_report.py
   IN THAT ORDER.  the first writes
   truthiness.json at whatever grain its
   LANES table names; the second reads
   truthiness_holder037.json, which is log
   037's frozen baseline, to say what MOVED.
   Reading truthiness.json there would compare
   the run against itself and print no
   movement.  This cost log 038 one wrong
   table.

5  re-fold both trees and the picture
   python3 l3_construct_cluster.py
   python3 l3_joint_cluster.py
   python3 make_dendrogram_constructs.py

6  validate the picture
   node domstub.js dendrogram_constructs.html
   1 script run, 0 threw, and #count non-empty.
   domstub.js is extractable from
   agent/drop/.done/*__vz_domstub.sh.
```

### the faults this log adds to the list

```
a script in drop is not a script queued
    the daemon fires on a file EVENT.  a
    script whose event was spent on an earlier
    refused run sits there forever.  re-write
    the file in place to fire it again.
the gate's planned number is the SHARDS'
    an empty shard file contributes zero
    planned and zero rows, and the gate reads
    COMPLETE one shard short.  check the
    frozen manifests, which is what they are
    for.
a baseline overwritten cannot be a baseline
    truthiness.json is rewritten at whatever
    grain the reader currently names.  the
    holder-grain baseline is frozen separately
    as truthiness_holder037.json.
```

### what remains open after this log

```
5t   PARTIAL.  eight of nine checked
     languages are at the value grain.  kotlin
     is running, dart is one shard short.
5u   CLOSED.  read above.
4j   UNTOUCHED and older: the cross-check
     against kind_signature_clustering's
     signature clusters.
```

---

## POSTSCRIPT — 2026-08-19, the pass is closed

The two lanes this log left running have landed and been harvested by
the six steps written above, in order, with no step skipped and no
number taken on trust. **CHECK 5t is CLOSED.**

### what landed

```
lane              probes   lane time   verdict
kv_kotlin_00..08  64,782     4,931 s   done, exit 0
kv_dart_04.sh      8,000        22 s   done, exit 0
```

Kotlin's nine shards ran at 76 ms a probe, slower per probe than any
other checked language and the reason it was launched first. Dart's
seventh shard took the thirty seconds its six siblings took.

Kotlin's shard 05 was re-dropped after a restart, and the drop
directory holds two `.done` entries for it — one from the run that
refused for want of scratch and wrote nothing, one from the run that
finished. It wrote **one** output file and that file holds 8,000 rows
with 8,000 distinct probe ids. **Measured**: the row count against the
frozen manifest is what says so, not the count of entries in `.done`.

### the totals for the whole value-grain pass

**Measured.** The gate, checked against the sum of the 68 frozen
manifests and not against its own shard summaries:

```
language      shards    planned      rows   suspect
typescript        6      40,700    40,700         0
csharp           11      85,587    85,587         0
java             15      89,698    89,698         0
dart              7      51,867    51,867         0
rust              4      47,736    47,736         0
go                4      39,104    39,104         0
cpp               9      49,170    49,170         0
swift             3      13,334    13,334         0
kotlin            9      64,782    64,782         0
              -----------------------------------
TOTAL            68     481,978   481,978         0
```

**481,978 of 481,978 probes, 100 percent, every one of the nine
COMPLETE and zero suspect rows.** 11,844 s of lane time across the 68
shards. The plan of this log asked for 481,978 and 481,978 is what
landed; the 323-probe difference from the design's 482,301 is the one
already accounted for above — 80 `break`/`continue` probes, which open
no operand slot and have no value grain, and 243 NOT-APPLICABLE unpack
roles in go and java.

With the three open languages, which were always at the value grain,
the completeness gate now reads COMPLETE for all twelve: **623,752
rows** — the nine above plus python 59,797, ruby 48,297 and php 33,680,
php's twenty fatals recovered and folded.

### what moved, with all nine in

**Measured.** The movement count is now over every checked language:

```
language     holder keys   split by value
typescript         2,277               27
csharp             3,840              153
java               4,288              167
dart               2,675              162
rust               2,112               25
go                 1,700               70
cpp                2,472               88
swift                696               22
kotlin             2,912              331
             ---------------------------
TOTAL             22,972            1,045
```

**1,045 of 22,972 holder keys, 4.5 percent, hide a verdict that depends
on the value.** The figure this log printed at eight-ninths was 693 of
19,760, 3.5 percent; kotlin alone raised it a full point.

### kotlin's truthiness column

**Measured.** Kotlin does what the other eight do and nothing else.
Its truth column reads `T` at the holder grain and **`S`** at the value
grain — the same `T>S` move every one of the nine makes. Its other
seven columns read `R`: kotlin will not take a value of any non-truth
form in an `if` condition, so those columns could not have moved and
did not. Kotlin sits with go, rust, swift, dart, csharp and java in the
refusing group, and apart from cpp and typescript, the two that coerce
and therefore moved in more columns than one.

The finding this log opened with is now complete over all nine: **the
truthiness table's `T` was an artifact of the base value in every
checked language without exception.**

### what kotlin showed that the other eight did not

**Measured.** Kotlin splits more keys than any other checked language —
331, twice java's 167 — and it splits them somewhere else. In every
other language the biggest splitter is `Kaccess.subscript` or, in the
JVM and dotnet pair, `augassign+=`. In kotlin the split is
**compound assignment and almost nothing else: 159 keys on `+=` and 124
on `-=`, 283 of 331, 85 percent**, with subscript contributing 11.

**Derived.** This is kotlin's operator-convention resolution showing
through: `+=` and `-=` are `plusAssign` and `minusAssign` looked up on
the receiver's declared type, and that type changes with the value
class. No other language in the nine has an appreciable `-=` split at
all — the `-=` column is where kotlin stands alone.

**Measured, and against the brief.** The catalogue holds twelve
constructs and they are the twelve shared by all twelve languages.
Kotlin has **no kotlin-only construct leaves** — no elvis `?:`, no
`in`, no range `..`. Those are kotlin OPERATORS and they were measured
as such in the operator pass; they are not constructs and were never in
this space. Anyone looking for them at construct value grain will not
find them, and that is correct rather than missing.

### the artifacts, re-folded at matched grain for all nine

```
construct_answers_<lang>.json   twelve, rewritten
truthiness.json / _value.json   rewritten at value grain
truthiness_table.md             all twelve, movement filled
trace_compare.md                rewritten
value_movement.json             all nine
clusters_constructs.json        123 leaves with a non-empty
                                domain, of 133 signatures
clusters_joint.json             284 leaves: 239 operator,
                                45 two-slot construct
dendrogram_constructs.html      123 leaves, 245 nodes
```

The picture was validated with the DOM stub, not by looking at it:
`node domstub.js dendrogram_constructs.html` reports **1 script run, 1
ok, 0 threw**, `#count` non-empty at 34 and `#legend` and `#plateaus`
written. The three panels it reports empty — `smat`, `sops`, `worked` —
are filled by a click and are empty in a stub by construction.

### what remains open after this postscript

```
5t   CLOSED.  481,978 of 481,978, all nine
     COMPLETE, zero suspect rows.
5u   CLOSED.  read above.
4j   UNTOUCHED and older, and now the only
     open item in the node: the cross-check
     against kind_signature_clustering's
     signature clusters.
```
