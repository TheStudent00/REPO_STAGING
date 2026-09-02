# construct_design.md — layer 3 extended to the construct families

Written 2026-08-19, BEFORE anything was generated, so that it can be
argued with rather than reverse-engineered from output. It is the same
posture `probe_design.md` took for the operator pass of log 024.

the owner blessed three construct families on 2026-08-19: **access**, **flow**,
**binding**. This file says, per family: which constructs each of the
twelve languages actually has, what encloses each construct so that it
is legal, what fills the construct's open slots, how a flow construct's
behaviour is written down, and how many probes all of that comes to.

Every claim carries its level. **Measured** means a number a program
printed. **Derived** means a number worked out from measured numbers.
**Decision** means a judgment call, numbered, and overturnable.

---

## §a — the three families, and what a construct is here

An **operator** takes values and gives back a value. The operator pass
(logs 024 and 027 through 035) measured 238 of them across twelve
languages.

A **construct** is the other thing a compiler can do to a loaded value:
reach into it, choose on it, repeat over it, or bind it to a name. It
does not always give back a value, and that is exactly why it needs its
own way of being written down.

The three families, in the owner's naming:

```
access    reach into a value
            index access, slice, member reach
flow      choose, repeat, or leave
            if, for, while, break, continue, try
binding   attach a value to a name
            assignment, augmented assignment,
            unpacking
```

Twelve construct roles. Twelve languages. 144 role slots.

---

## §b — which constructs each language HAS (derived, not hand-listed)

**Decision 1. The construct list per language is DERIVED from that
language's own kinds file, never hand-written.** `construct_catalogue.py`
states a ROLE and a set of candidate kind names that the twelve grammars
are known to use for that same job. It then asks `kinds_<lang>.json` —
phase 0's measurement of what each grammar declares — which of those
names the grammar actually declares. The name it resolved to is
recorded, because the spelling differs everywhere: python's index access
is `subscript`, go's and rust's is `index_expression`, c++'s is
`subscript_expression`, ruby's is `element_reference`.

**Decision 2. A role with no declared kind is ABSENT, and absence is a
finding.** Nothing is patched in. Measured: **130 of the 144 role slots
resolved, 14 ABSENT** (`construct_catalogue.json`, 2026-08-19).

The fourteen absences, and what each one is:

```
go        flow.try        go has no exception
                          construct at all; it
                          returns errors instead
go        flow.while      go spells every loop
                          `for`; there is no
                          second loop keyword
kotlin    flow.break      kotlin declares these as
kotlin    flow.continue   plain tokens, not as
                          named kinds; the grammar
                          is silent, the language
                          is not
swift     access.member   the pinned swift grammar
swift     access.slice    declares 72 named kinds
swift     binding.augassign   against c++'s 223; four
swift     flow.try        roles fall in its gaps
cpp       access.slice    seven grammars declare no
dart      access.slice    slice kind, because their
java      access.slice    language has no slice
php       access.slice    syntax -- a library call
ruby      access.slice    does that job instead
typescript access.slice
```

Two different kinds of absence sit in that list and they must not be
read as one thing.

- **The language really lacks it.** go has no `while` and no `try`.
  c++, java, typescript, dart, php and ruby have no slice SYNTAX.
  This is a fact about the language and it is a finding.
- **The grammar is silent about it.** kotlin's `break` exists in kotlin
  and this grammar does not give it a named kind. swift's four gaps are
  the same shape: a thin grammar, not a thin language.

**Decision 3. The two are kept apart in the record and neither is
guessed at from the other.** `construct_catalogue.json` records only
what the grammar declared. This document's reading of WHY is a
judgment and is marked as one.

---

## §c — the SCAFFOLD principle

the owner's words, 2026-08-19, and they are the whole rule:

> inert code "used to connect logical operations of interest"

A construct usually cannot stand alone. `break` needs a loop around it.
An assignment needs a function body around it in nine of the twelve.
The code that makes it legal is the **scaffold**.

**Decision 4. Each construct gets ONE fixed minimal scaffold per
language, and that scaffold is identical across every probe of that
construct.** Three properties are demanded of it and each is there for a
reason:

- **minimal** — the least code that makes the construct legal. Every
  extra line is a second thing that could have caused what was observed.
- **inert** — it contributes no behaviour of its own. It computes
  nothing, it branches on nothing, it holds no state the construct can
  see.
- **fixed** — byte-identical across every probe of that construct in
  that language. Only the slot fillers change.

Together these give the property the whole pass rests on: **anything
observed is the construct's doing**, because the only thing that varied
between two probes was what went into the construct's slots.

The scaffolds, shown as actual code. One per language shape.

Braces with types — go, the proof language:

```
package main
import "fmt"
func main() {
    var c CT = CV
    if c {
        fmt.Print("BR=then")
    } else {
        fmt.Print("BR=else")
    }
}
```

Indentation — python:

```
c = CV
if c:
    T("BR=then")
else:
    T("BR=else")
```

Keyword and end — ruby:

```
c = CV
if c
  t("BR=then")
else
  t("BR=else")
end
```

Tag delimited — php:

```
<?php
$c = CV;
if ($c) { t("BR=then"); }
else { t("BR=else"); }
```

`CV` is the slot. `CT` is the holder's declared type where the language
needs one. `T` and `t` are the trace recorder, which is harness
machinery and never a probed construct — the same standing that
log 024 decision 4 gave to exception catching.

**Decision 5. The trace recorder is harness machinery.** It is a
function that appends one step to a buffer. It is not a construct, it is
never probed, and it is the same three lines in every scaffold of a
language.

---

## §d — the slots, and what fills them

Slot discipline carries over unchanged from the operator pass: every
construct slot is fed the layer-2 **holders** and, through them, the
layer-1 **values**. Ruling 1 of the CORE's 2026-08-18 block already
settled that the operand is a holder, and a construct slot is an
operand position like any other.

The slot count per construct, which is what the probe arithmetic runs
on:

```
one slot
    member reach, if, for, while, try,
    assignment, unpacking
two slots
    index access, augmented assignment
three slots
    slice
no slot
    break, continue
```

What fills each one:

- **the if-condition slot** takes every holder and every value class.
  That single slot, run over all of them, IS the cross-language
  **truthiness table** — and it is a one-operand table, so it is an
  8-form vector per language and not a 64-cell grid. This is the slot
  the owner singled out.
- **the for-iterable slot** takes every holder and every value class.
  A holder that is not iterable refuses or raises, and that refusal
  locates the edge of the construct's domain exactly as a raise did for
  the operators.
- **the index-access slots** take an ordered holder pair, container on
  the left and index on the right, over the full value matrix. Both
  orders are kept; nothing assumes a container cannot be an index.
- **the augmented-assignment slots** take an ordered holder pair over
  three operations.

**Decision 6. Slice bounds are drawn from the canonical whole-number
holder only, capped at six value classes.** A slice opens three slots
and the honest cross product is the value count times the whole-number
value count squared. Capping the two bound slots at one holder keeps
slices affordable while still varying the bounds through their edge
classes. Overturnable, and the cost of overturning it is a re-run of
one construct.

**Decision 7. The member-reach slot uses one fixed name, `f`.** Every
holder is asked for a member called `f`. Most refuse. The point is the
refusal boundary — which holders admit member reach at all — not the
contents of any particular member.

**Decision 8. break and continue open no operand slot.** Their loop is
the fixed sequence 1 through 5 and what varies is WHERE the jump sits,
k = 1 through 5. The measurement wanted from them is the trace, not a
domain.

**Decision 9. Augmented assignment probes three operations, `+=`, `-=`
and `*=`.** The operator pass already measured the plain forms across
the full menu; what is new here is the BINDING, and three operations is
enough to see whether the binding differs from the operation. log 024 §5
found `list += tuple` answering where `list + tuple` raises, which is the
finding this slot exists to generalise.

**Decision 10. break and continue run at k = 1 through 5.** Five is the
loop length. Every stopping point including both ends is covered.

---

## §e — the TRACE, the observation standard for flow

An operator's observation is its answer. A flow construct often has no
answer. What it has instead is a **trace**: the sequence of values at
each joint.

the owner's standard, 2026-08-19: the trace is recorded in the **same bits and
type encoding as `answers_encoding.md`**, so that traces are
cross-language comparable exactly as `+`'s bits were.

**Decision 11. The trace line reuses the answer line's three-field
shape.** A reader that can already split an answer row can split a trace
row.

```
PROBE_ID|TYPE_NAME|TRACE:<n>[<step>,<step>,...]
PROBE_ID|-|RAISE:<name>
PROBE_ID|-|REFUSE:<message>
PROBE_ID|-|DEATH:<rc>
```

`<n>` is the step count. Each `<step>` is one joint, and the joint kinds
are these:

```
BR=<name>
    a branch joint. which arm ran.
    names: then, else, body, skip,
    try, catch, finally
IT=<enc>
    one loop iteration. the loop
    variable's value, written in
    the answers_encoding encoding.
STOP=<k>
    iteration stopped after k steps,
    because break was reached.
SKIP=<k>
    iteration k was skipped, because
    continue was reached.
BIND=<enc>
    a binding joint. the value read
    back out of the name after the
    binding ran.
THROW=<name>
    a raise observed INSIDE the trace,
    at the joint where it happened.
    the language's own class name.
```

`<enc>` is an `answers_encoding.md` payload verbatim — `INT:64:...`,
`STR:5:5:...`, `BOOL:true` and the rest. No new encoding is invented and
none of the old one is changed. That is what makes a trace comparable
across languages: the same value written the same way in all twelve.

**Decision 12. A trace is capped at 8 steps.** A loop over a value that
turns out to be unbounded would otherwise never end. At the cap the
trace closes with `STOP=8` and the probe is recorded as capped rather
than as an answer. Capping is harness machinery, and the cap is stated
here rather than buried in a driver.

**Decision 13. `TYPE_NAME` on a trace row is the joint's type where the
joints share one, and `-` where they do not.** A loop over a list of
whole numbers has one joint type and it is recorded. A loop over a keyed
grouping does not, and `-` is honest.

An example, and it is the one the owner asked for — a `for` over the sequence
1, 2, 3:

```
Kfor_9_base|int64|TRACE:3[IT=INT:64:0000000000000001,
IT=INT:64:0000000000000002,IT=INT:64:0000000000000003]
```

And the same loop with a break at k = 2:

```
Kbreak_2|int64|TRACE:3[IT=INT:64:0000000000000001,
IT=INT:64:0000000000000002,STOP=2]
```

Those two lines are what a cross-language comparison reads. If twelve
languages give the same three `IT` steps for the first, the `for`
construct agrees across twelve languages at that grain, and it is
MEASURED to agree rather than assumed to.

---

## §f — probe identifiers, and the manifest that makes them readable

**Decision 14. A construct probe id is `K<construct>_<slots>`, and every
run freezes a manifest beside it.** The operator pass learned this the
hard way (log 029): positional ids are unreadable without the frozen
list of what each position meant.

```
one slot    K<construct>_<i>_<x>
two slots   K<construct>_<i>_<j>_<x>_<y>
three slots K<construct>_<i>_<x>_<b1>_<b2>
no slot     K<construct>_<k>
```

`i` and `j` are holder positions, `x` and `y` are value classes, `b1`
and `b2` are slice bounds, `k` is the jump position. The manifest —
`manifest_construct_<lang>.json` — carries the holder list in position
order, the value classes per holder, the construct list, and the
scaffold text per construct. It is frozen before the run and is not
edited afterwards.

---

## §g — the routes, unchanged

The evidence routes carry over from CORE ruling 5 with no change, which
is the point of having ruled them once.

- **acceptance** through each language's own proven instrument: the
  in-process checkers for go, typescript, java, csharp and kotlin; the
  check-only invocations for rust and c++; the FULL swift compiler, not
  `-typecheck`, per log 034; and route-C execution for python, ruby and
  php, where no other acceptance evidence exists.
- **answers and traces** through single-file execution of probes already
  known to be legal.

**Decision 15. Constructs reuse the operator pass's lane machinery
without rebuilding it.** The same chunked lanes, the same completeness
gate, the same scratch check before a run. The faults logged 027 through
035 are not to be repeated: the memory-backed scratch disk fills
silently, dead-code lint severity has to be lowered or a legal probe
scores as refused, php and ruby word-spelled operations need their
parentheses, and `-typecheck` is not the swift compiler.

---

## §h — the probe count, derived, per language

Printed by `construct_space.py` before anything runs. The arithmetic:
`H` is the holder count, `V` the value count, `M` the full value matrix
summed over ordered holder pairs.

```
language      H     V        M    accept    answers
go           20    94     8836      1720      39208
rust         22   104    10816      2112      47746
cpp          24   110    12100      2472      49180
swift        24   113    12769       696      13344
dart         25   113    12769      2675      51877
csharp       30   141    19881      3840      85597
kotlin       26   122    14884      2912      64782
java         32   149    22201      4320      89857
typescript   23   100    10000      2277      40710
python       24   117    13689         0      59797
ruby         22   109    11881         0      48297
php          19    91     8281         0      33771

TOTAL                            23024     624166
grand total                             647190
```

The three route-C languages have a zero acceptance column because
execution is their only acceptance evidence; their answer column carries
the whole load. Swift's numbers are small because four of its twelve
roles are ABSENT from its grammar.

**647,190 probes.** Derived. Against the operator pass's measured 5.79M,
this is about a ninth of the load, and it buys the other half of what a
compiler can do to a value.

---

## §i — the decision list, gathered

For the owner, in one place. Any of these can be overturned; the cost of
overturning each is stated.

```
 1 construct list DERIVED from the grammar
     cost to overturn: none, it is the rule
 2 an unresolved role is ABSENT, a finding
     cost: none
 3 language-lacks and grammar-silent kept
   apart, and neither inferred from the other
     cost: none
 4 one fixed minimal inert scaffold per
   construct per language
     cost: a re-run of that language
 5 the trace recorder is harness machinery
     cost: none
 6 slice bounds from the canonical whole
   holder, capped at six classes
     cost: a re-run of one construct
 7 member reach uses one fixed name, `f`
     cost: a re-run of one construct
 8 break and continue open no operand slot
     cost: a re-run of two constructs
 9 augmented assignment probes three
   operations
     cost: linear in operations added
10 break and continue run at k = 1..5
     cost: a re-run of two constructs
11 the trace line reuses the answer line's
   three-field shape
     cost: a re-read, not a re-run
12 a trace is capped at 8 steps
     cost: a re-run of the flow family
13 TYPE_NAME is `-` where joints disagree
     cost: a re-read
14 probe ids are positional and every run
   freezes a manifest
     cost: none, it is the fix for a past
     fault
15 constructs reuse the operator lane
   machinery unchanged
     cost: none
```
