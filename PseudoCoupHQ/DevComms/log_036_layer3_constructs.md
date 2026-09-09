# log 036 — layer 3 extended to constructs: access, flow, binding

Date: 2026-08-19. Node:
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PseudoCoupHQ/Research/kind_fuzz_clustering/`.

**Written in the readable register of the rewritten logs 034 and 035.**
Glossary first. Every leaned-on fact restated rather than pointed at.
Every lane name carried with words. Every claim levelled. One idea per
sentence.

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Decision** means a judgment call, and it is numbered. **Unverified**
means nobody has checked it.

---

## words used in this log

Every short word this log uses for one of its own parts is defined here,
with an example taken from this log's own content. Nothing below this
block uses a word that is not either ordinary English or defined here.

```
construct
    the thing a compiler can do to a value
    that is not an operation on it: reach
    into it, choose on it, repeat over it,
    or bind it to a name.
    example tied to context:
        `if` is a construct.  `+` is not; it
        is an operation, and the operator
        pass of logs 024 through 035 already
        measured 238 of those.

family
    one of the three groupings the owner blessed
    on 2026-08-19.  access, flow, binding.
    example tied to context:
        `break` is in the flow family.

role
    what a construct is FOR, named
    independently of how any one language
    spells it.
    example tied to context:
        the index-access role is spelled
        `subscript` in python's grammar and
        `index_expression` in go's.  One
        role, two spellings.

catalogue
    the file that resolves each role, in
    each language, to that grammar's own
    kind name -- or records it ABSENT.
    example tied to context:
        `construct_catalogue.json` resolved
        130 of 144 role slots.

scaffold
    the inert code that makes a construct
    legal without contributing behaviour of
    its own.  the owner's words: code "used to
    connect logical operations of interest".
    example tied to context:
        `break` needs a loop around it.  The
        loop is the scaffold.

slot
    an open position in a construct that a
    value goes into.
    example tied to context:
        `if` has one slot, its condition.
        Index access has two, the container
        and the index.

trace
    the sequence of values at each joint of
    a flow construct, written in the same
    encoding as an answer.
    example tied to context:
        a `for` over 1, 2, 3 has the trace
        `TRACE:3[IT=...1,IT=...2,IT=...3]`.

joint
    one point in a trace where something was
    observed.  Which arm ran, one loop
    iteration, where a break stopped, what
    a name got bound to.
    example tied to context:
        `BR=then` is a joint.  So is
        `STOP=2`.

holder
    the typed slot a value is put into
    before anything is done to it.
    example tied to context:
        python's `list` and its `tuple` are
        two holders of one form.

value class
    a named family of test values, chosen so
    the awkward cases are covered.
    example tied to context:
        `base` is the value class whose
        sequence is 1, 2, 3.

form
    one of the eight layer-1 contents.
    nothing, truth, whole, fractional, text,
    sequence, keyed, nesting.
    example tied to context:
        the truthiness table has one row per
        form, so eight rows.

lane
    one batch job.  It runs a planned set of
    probes and writes its output to one raw
    text file.  A lane has a short name.
    example tied to context:
        `kc_python.sh` is the lane that ran
        python's 59,797 construct probes and
        wrote `raw/kc_python.txt`.

completeness gate (also: gate)
    a check run after a lane finishes.  It
    counts the rows the lane actually wrote
    and compares that with the plan the lane
    printed before it started.
    example tied to context:
        the gate scores python COMPLETE and
        php twenty probes short.

grain
    what one row is a measurement OF.
    example tied to context:
        go's rows are at HOLDER grain,
        python's at VALUE grain.

truthiness
    what a language does when a value that
    is not a boolean is put in an
    if-condition.
    example tied to context:
        ruby answers `then` for every form
        except nothing and false.  go
        refuses every form except truth.

route
    where a piece of evidence came from.
    Route A is the compiler's own checking
    code running.  Route B is the
    compiler's literal data lifted.  Route C
    is execution.
    example tied to context:
        python, ruby and php are route C,
        because execution is the only
        acceptance evidence those three
        have.
```

---

## facts leaned on, restated

Four things this log rests on. Each is restated here in full, so that no
reader has to go and fetch it.

- **The three layers.** Layer 1 is the DATA, with no language attached:
  nothing, truth, whole number, fractional number, text, sequence, keyed
  grouping, nesting. Layer 2 is the per-language HOLDERS of that data —
  python's `int`, its `Decimal`, its `Fraction` are three holders of one
  form. Layer 3, which this log reports on, is what the compiler can DO
  to a loaded holder.
- **The operator pass is finished and this is the other half.** Logs 024
  through 035 measured what 238 OPERATIONS do to holders across twelve
  languages. An operation takes values and gives back a value. A
  construct is the rest of what a compiler can do, and it often gives
  back nothing at all.
- **The answer encoding.** An answer is recorded as the type name the
  language gives its own result, plus the content as bits — integers in
  two's complement, floats as their IEEE bit pattern, text as bytes and
  both length notions. No canonical printing happens at run time. The
  rule lives in `answers_encoding.md` and this log does not change it.
- **The evidence routes were ruled once, on 2026-08-18, and all of them
  run.** Acceptance comes from the compiler's own logic running or its
  literal data matching, never from an agent reading compiler source and
  writing a rule down. Execution supplies the answers everywhere, and it
  is the only acceptance evidence that exists for python, ruby and php.

---

## §1 — walkthrough, in plain words

the owner blessed three construct families on 2026-08-19: **access**, **flow**
and **binding**. Access is reaching into a value. Flow is choosing,
repeating, or leaving. Binding is attaching a value to a name. Twelve
construct roles fall under the three of them.

What was done, in order.

First, the design was written down before anything was generated. It is
`Research/kind_fuzz_clustering/construct_design.md` and it is the same
posture `probe_design.md` took for the operator pass: a design that can
be argued with, rather than one reverse-engineered afterwards from
output. Sixteen numbered decisions sit in it and every one of them can be
overturned. §2 below is that list.

Second, the construct list per language was DERIVED rather than
hand-written. A role says what a construct is for. A candidate set says
which kind names the twelve grammars are known to use for that job. Then
each grammar's own kinds file — phase 0's measurement of what that
grammar declares — was asked which of those names it actually declares.
**130 of the 144 role slots resolved and 14 came back ABSENT.** Absence
is a finding and it is written down as one. Two different absences sit in
that fourteen and they are kept apart: go really has no `while` and no
`try`, while kotlin really does have `break` and its grammar simply does
not name it.

Third, the scaffold principle was fixed. the owner's words for it are the whole
rule: inert code "used to connect logical operations of interest". Each
construct gets one scaffold per language. It is minimal, it contributes
no behaviour, and it is byte-identical across every probe of that
construct. What that buys is the property the whole pass rests on:
anything observed is the construct's doing, because the only thing that
varied between two probes was what went into the slots.

Fourth, the observation standard for flow was settled. An operation's
observation is its answer. A flow construct often has no answer, so what
it has instead is a **trace** — the sequence of values at each joint.
the owner's standard was that a trace is written in the same bits and type
encoding as an answer, so traces compare across languages exactly as
`+`'s bits did. A trace row reuses the answer row's three-field shape, so
a reader that can split one can split the other. Nothing in the answer
encoding was changed and no new encoding was invented.

Fifth, the size was derived and printed before anything ran, as this
node's plan of record demands of every phase. **647,190 probes** across
the twelve. Against the operator pass's 5.79 million, that is about a
ninth of the load, and it buys the other half of what a compiler can do
to a value.

Sixth, the proof pass ran. Python is the executed proof language and go
is the checked one, because go is the cheapest of the nine statically
checked instruments. Both came back complete and both are folded. Ruby
and php were then run on the same pattern, which brings the executed
three to a finish.

Seventh, the fold. The completeness gate reads every lane's raw output
and compares the rows it actually wrote with the plan that lane printed
before it started, because exit 0 is not evidence a lane finished. Then
the construct signatures were written beside the operator signatures, the
truthiness table was written as its own readable artifact, and the first
cross-language trace comparisons were written as another.

Four languages are measured. Eight are not, and §6 says exactly how to
pick them up.

---

## §2 — the design decisions, numbered, for the owner

Verbatim from `construct_design.md` §i. Any of these can be overturned
and the affected lane re-run; the cost of overturning each is stated
beside it.

```
 1 the construct list is DERIVED from each
   grammar's own kinds file, never
   hand-listed
     cost to overturn: none, it is the rule
 2 a role that resolves to nothing is
   ABSENT, and absence is a finding
     cost: none
 3 "the language lacks it" and "the grammar
   is silent about it" are kept apart, and
   neither is inferred from the other
     cost: none
 4 one fixed minimal inert scaffold per
   construct per language
     cost: a re-run of that language
 5 the trace recorder is harness machinery,
   never a probed construct
     cost: none
 6 slice bounds are drawn from the canonical
   whole-number holder, capped at six value
   classes
     cost: a re-run of one construct
 7 member reach uses one fixed name, `f`
     cost: a re-run of one construct
 8 break and continue open no operand slot
     cost: a re-run of two constructs
 9 augmented assignment probes three
   operations, `+=`, `-=` and `*=`
     cost: linear in operations added
10 break and continue run at k = 1 to 5
     cost: a re-run of two constructs
11 the trace line reuses the answer line's
   three-field shape
     cost: a re-read, not a re-run
12 a trace is capped at 8 steps
     cost: a re-run of the flow family
13 the type field is `-` where a trace's
   joints do not share one type
     cost: a re-read
14 probe ids are positional and every run
   freezes a manifest beside itself
     cost: none; it is the fix for the
     log 029 fault
15 constructs reuse the operator pass's lane
   machinery unchanged
     cost: none
16 where a language's unpack construct
   destructures a call's returns rather than
   a value, the cell is recorded
   NOT_APPLICABLE with its reason rather
   than faked
     cost: none; faking it would have
     measured the harness
```

Decision 16 is the one that came up during the build rather than before
it. go's `expression_list` unpack takes a call's multiple return values.
It never takes a value apart. There is therefore no honest go probe for
the unpack role, and writing `_x, _y := a, a` would have measured the
harness rather than go. The cell says NOT_APPLICABLE and says why.

---

## §3 — the proof pass

Two languages end to end, one executed and one checked, before anything
generalised. That is the order this node's plan of record has used since
phase 1 and it caught three faults again this time.

**python — lane `kc_python.sh`.** Route C, so execution is both the
acceptance evidence and the answer evidence. All twelve construct roles
are present in python's grammar. Measured: **59,797 probes in 16.9
seconds**, 1,538 answers, 6,502 traces, 51,757 raises, no refusals, no
budget exhaustions. The gate scores it COMPLETE — 59,797 rows against a
plan of 59,797. That the raises outnumber everything else is not a
fault and it is the same shape log 024 reported for the operator pass:
most of the probe space is deliberately made of constructs applied where
they do not belong, because the boundary of what a construct accepts is
half of what this node compares constructs on.

**go — lane `kg_go.sh`.** Route A2, which means the real compiler front
end runs and its exit status is the verdict. One file per probe, `go
build` on each, eight at a time. Measured: **1,710 acceptance probes in
26.8 seconds**, 104 accepted and 1,606 refused. The gate scores it
COMPLETE.

**The trace encoding round-trips.** This was the thing to verify before
anything else was worth doing, and it does. go's break-at-k traces and
python's break-at-k traces are byte-identical, and the two were produced
by different encoders written in different languages against the same
written specification.

**Three faults were found and fixed in the proof pass, which is what a
proof pass is for.**

- go puts imports at the file head and never in a function body. A
  holder's setup line is an import in go, and the first go run put it in
  the body. Two of 1,710 probes scored REFUSE with a syntax error, which
  was the harness refusing rather than go refusing the construct. Fixed
  by lifting the setup line into the import block. A second run then
  found the follow-on: an import already in the block is a duplicate and
  a duplicate import is also a refusal, which cost twenty more probes
  until the block was made a set.
- ruby evaluates `#{...}` inside a double-quoted string when the string
  is parsed. The scaffolds were written as double-quoted ruby strings,
  so ruby tried to evaluate the probes' own interpolations while it was
  still reading the driver. The lane died in 0.1 seconds having run
  nothing. Fixed by escaping.
- php refuses a class declared twice in one process and two php holders
  carry a class declaration in their setup text. Every evaluation
  redeclared it, and a php fatal is not catchable. This is the same fault
  log 027 recorded in §5.1 for the operator pass, met again in a new
  place. Fixed the same way java's was: the declared name is suffixed per
  probe, mechanically, over the literal text. Before the fix the lane
  exhausted 400 restarts and got half way. After it, twenty restarts.

---

## §4 — what ran, and what has not

**Ran, gated, folded.** Four lanes. Each is named and each is carried
with words.

```
kc_python.sh   python, route C
    59,797 probes, 16.9 s, COMPLETE
kc_ruby.sh     ruby, route C
    48,297 probes, 0.8 s, COMPLETE
kc_php.sh      php, route C
    33,660 of 33,680 probes, 10.4 s,
    TWENTY SHORT
kg_go.sh       go, route A2
    1,710 probes, 26.8 s, COMPLETE
```

php's twenty short probes are php FATALS. A fatal is not catchable and
kills the process. The lane restarts past the corpse, so a fatal costs
exactly one probe — the standing `answers_encoding.md` already gives a
DEATH. Twenty restarts, twenty lost probes, each recorded in the lane log
with the probe number it died on. Measured, not estimated.

**Has not run.** Eight lanes. None of them is running right now; they are
BUILT-FOR but not BUILT, and calling them "still running" would be
false. What exists for each of them is the derived probe count, the
resolved construct list, and a worked example to copy.

The derived counts, and the time each would take at the operator pass's
own measured per-probe cost for that language:

```
typescript   2,277 accept + 40,710 answers
    ETA 15 min, in-process checker
csharp       3,840 accept + 85,597 answers
    ETA 25 min, in-process checker
kotlin       2,912 accept + 64,782 answers
    ETA 2 h, cold compiler start dominates
rust         2,112 accept + 47,746 answers
    ETA 20 min, check-only invocation
cpp          2,472 accept + 49,180 answers
    ETA 30 min, check-only invocation
dart         2,675 accept + 51,877 answers
    ETA 35 min, lint severity must be
    lowered first
java         4,320 accept + 89,857 answers
    ETA 40 min, in-process checker
swift          696 accept + 13,344 answers
    ETA 45 min, FULL compiler, not
    -typecheck
```

Every one of those ETAs is **derived** from the operator pass's measured
per-probe cost for that language, not measured for constructs. kotlin's
two hours is the same cold-start problem log 025 measured: 2,397
milliseconds per probe against c++'s 173 and rust's 36.

---

## §5 — first findings

Five, and every one is measured.

**Finding 1 — the fourteen absences, and two of them are about the
language rather than the grammar.** go has no `while` construct and no
`try` construct at all; it spells every loop `for` and it returns errors
instead of raising. Seven of the twelve grammars declare no slice kind,
because seven of the languages have no slice syntax and use a library
call for the job. kotlin's `break` and `continue`, and four of swift's
roles, are the other kind of absence: the language has them and the
pinned grammar does not name them. The pinned swift grammar declares 72
named kinds against c++'s 223, which is why four of its twelve roles fall
in its gaps.

**Finding 2 — the truthiness table, and the four languages measured
disagree completely.** This is the excerpt, verbatim from
`truthiness_table.md`.

```
go       (grain: holder, base value only)
nothing     refused
truth       always then
whole       refused
fractional  refused
text        refused
sequence    refused
keyed       refused
nesting     refused

python
nothing     always else
truth       splits 1 then 1 else
whole       splits 20 then 4 else
fractional  splits 13 then 3 else
text        splits 15 then 3 else
sequence    splits 17 then 5 else
keyed       splits 15 then 3 else
nesting     always then

ruby
nothing     always else
truth       splits 1 then 1 else
whole       always then
fractional  always then
text        always then
sequence    always then
keyed       always then
nesting     always then

php
nothing     always else
truth       splits 1 then 1 else
whole       splits 10 then 2 else
fractional  splits 5 then 1 else
text        splits 10 then 2 else
sequence    splits 19 then 1 else
keyed       splits 19 then 1 else
nesting     always then
```

Three whole positions, measured rather than recalled. go admits exactly
one form into a condition and refuses the other seven. ruby admits every
form and answers `then` for all of them except nothing — it is the only
one of the four where an empty text and a zero are both true. python and
php both split on emptiness and on zero, and they split by different
counts because they hold different numbers of values per form.

**Finding 3 — a `for` over 1, 2, 3 does NOT see the same trace in every
language.** This is the comparison the owner asked for by name, verbatim from
`trace_compare.md`.

```
go
    TRACE:3[IT=INT:64:0000000000000000,IT=INT:64:00000
    00000000001,IT=INT:64:0000000000000002]
python
    TRACE:3[IT=INT:64:0000000000000001,IT=INT:64:00000
    00000000002,IT=INT:64:0000000000000003]
ruby
    TRACE:3[IT=INT:64:0000000000000001,IT=INT:64:00000
    00000000002,IT=INT:64:0000000000000003]
php
    TRACE:3[IT=INT:64:0000000000000001,IT=INT:64:00000
    00000000002,IT=INT:64:0000000000000003]
```

Three languages agree on three steps and go does not. go's one-variable
`range` hands back the INDEX, so it walks 0, 1, 2 where the other three
walk 1, 2, 3. Same loop length, same construct role, different thing at
the joint. That is precisely the kind of disagreement the trace was
built to make visible, and it would have been invisible to any
observation that only recorded whether the loop finished.

**Finding 4 — break at k agrees in all four languages, exactly.** Same
artifact, verbatim.

```
break at k = 2
go
    TRACE:2[IT=INT:64:0000000000000001,STOP=1]
php
    TRACE:2[IT=INT:64:0000000000000001,STOP=1]
python
    TRACE:2[IT=INT:64:0000000000000001,STOP=1]
ruby
    TRACE:2[IT=INT:64:0000000000000001,STOP=1]
```

Four languages, four different compilers, four independently written
encoders, one byte-identical line. When the loop is the fixed sequence
rather than a holder, the disagreement of finding 3 vanishes — which
locates that disagreement precisely in how a language's loop reads a
container, and nowhere else.

**Finding 5 — go's construct domain is narrow and it is narrow in a
readable pattern.** Of 1,710 acceptance probes, 104 were accepted.
Twenty of go's twenty holders accept a plain assignment. Thirty-three
holder pairs accept index access, eight accept slicing, and nineteen of
the 1,200 augmented-assignment pairs are accepted. Member reach was
accepted zero times, which is honest: decision 7 asks every holder for a
member named `f` and none of go's holders has one. The if-condition
accepted exactly one holder.

---

## §6 — remainders, and how to pick them up

The instruction sheet is
`Research/kind_fuzz_clustering/HARVEST_constructs.md`. It is written for
a session that has none of this in mind and it assumes only
`construct_design.md`.

What is in it.

- The four finished lanes with their measured numbers, so the next
  session does not re-run them.
- The eight remaining languages in **cost order**, cheapest instrument
  first: typescript, csharp, kotlin, then rust and cpp, then dart, then
  java, and swift last because swift needs the full compiler.
- The four parts of a construct lane and which two of them change per
  language. `l3_construct_go.py` is the worked example and it is meant to
  be copied rather than read.
- The nine faults not to repeat, each of which has already cost a run
  once. Scratch fills silently. Exit 0 is not evidence. Dart's dead-code
  lint scores a legal probe as refused. php and ruby word-spelled
  operations need their parentheses. `swiftc -typecheck` is not the swift
  compiler. Positional ids need frozen manifests. Imports live at the
  file head. A class cannot be declared twice. Ruby interpolates inside
  double quotes.
- How to fold what comes back: add the language to one table in
  `l3_construct_read.py`, run it, and the gate, the signatures, the
  truthiness table and the trace comparisons all rebuild themselves.

Three things are open and open is what they are.

- **The eight lanes are unbuilt.** Their scaffolds and their encoders
  have to be written in eight more languages. That is the bulk of the
  remaining work and no part of it is hard; it is eight times the same
  shape.
- **php's twenty fatals are unrecovered.** Re-running them one at a time
  would recover them. Nobody has, and the gate says so rather than
  rounding it off.
- **The construct signatures are not yet clustered.** They are written
  beside the operator signatures in the same shape — domain accepted plus
  answer per cell — so the clustering machinery can take them without
  changes. Nothing has pointed it at them yet.

---

## artifacts written by this log

```
construct_design.md
    the design of record, 16 decisions
construct_catalogue.py / .json
    the derived construct list per language
construct_space.py
    the probe space and its size, printed
    before anything ran
l3_construct.py
    the route-C lanes: python, ruby, php
l3_construct_go.py
    the checked lane: go, and the worked
    example for the other eight
l3_construct_read.py
    the gate and the fold
manifest_construct_<lang>.json
    frozen beside each of the four runs
raw/kc_python.txt, raw/kc_ruby.txt,
raw/kc_php.txt, raw/kg_go.txt
    the raw lane output, with each lane's
    own log beside it
construct_index.json
    the completeness gate
construct_answers_<lang>.json
    the construct signatures
truthiness_table.md
    the truthiness table, twelve languages,
    four filled in
trace_compare.md
    the first cross-language traces
HARVEST_constructs.md
    the instruction sheet for the remaining
    eight
```
