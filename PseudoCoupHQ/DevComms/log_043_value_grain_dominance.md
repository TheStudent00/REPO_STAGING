# log 043 — the value-grain reformulation, and the one order

Date: 2026-08-20. Node:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

Log 043 was free when this was written. Log 042 is the boundary work,
running beside this one and owned by another agent; nothing here writes
into it and §5 says where the two meet.

the owner ruled on 2026-08-20 that the signature was built at the wrong
grain. His words:

> each row isnt a row element. its a vector

> that way something like php.== cant appear to have obtained
> god-operator status.

This log rebuilds every signature at the VALUE GRAIN with
ANSWER-VALUED elements, reruns the dominance paradigm on the ONE order
that leaves standing, and hands the Hub the union candidates that come
out of it. It does those four things and nothing else.

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

**No probe ran for this log. No lane ran. Nothing was compiled and
nothing was executed.** Every number below is read off artifacts that
were already on disk, or computed from them by four scripts that
finish in under six seconds each.

---

## words used in this log

Every short word this log leans on is defined here. Each definition
carries an example taken from this log's own content rather than a
made-up one.

```
leaf
    one operation in one language.
    example tied to context:
        `go.+' is a leaf.  there are 239.

element
    one question and its answer: a left
    holder at a value class against a right
    holder at a value class, and the answer
    token that came back.
    example tied to context:
        `whole|base_42|whole|base_42' is an
        element.  the merged grid holds 1,156.

answer token
    the canonical form of what came back.  a
    raise, a death and a backend refusal are
    tokens like any other.
    example tied to context:
        `whole:84', `raise:TypeError' and
        `refuse:codegen' are all tokens.

element value
    what a leaf carries AT an element: the set
    of tokens its holders gave there.  a set,
    because several holder pairs of one form
    pair reach one element.
    example tied to context:
        `java.==' carries the two-token value
        `truth:false, truth:true' at
        `fractional|base_1_5|fractional|base_1_5'.

speaks, silent
    a leaf SPEAKS at an element when a run
    recorded something there.  it is SILENT
    when it was never asked -- the compiler
    would not take the holder pair.
    example tied to context:
        `php.==' speaks on all 1,156.
        `go.&&' speaks on 4.

the merged order
    X sits below Y when Y carries the SAME
    element value as X on EVERY element X
    speaks on, and speaks somewhere X does
    not.  there is only this one order now.
    example tied to context:
        `cpp.!=' and `cpp.not_eq' carry the
        same value on all 282 elements either
        speaks on, so neither is below the
        other -- they are one vector class.

vector class
    the leaves whose signatures are identical
    element for element, answers included.
    example tied to context:
        `csharp.&&', `go.&&', `java.&&',
        `kotlin.&&', `rust.&&' and `swift.&&'
        are one vector class.

maximal
    nothing sits above it.
    example tied to context:
        209 of the 239 leaves are maximal.

union candidate
    two maximal leaves that never carry
    different values on an element both speak
    on.  one operation could carry both.
    example tied to context:
        `cpp.&&' with `dart.&&'.

blocked
    two maximal leaves that DO carry different
    values somewhere.  the element where they
    part is the blocking element.
    example tied to context:
        `php.%' with `python.%', blocked at
        `fractional|base_1_5|fractional|base_1_5'.

assembly
    a group of maximal leaves, any size, no
    two of which block.  the union of their
    vectors is still one answer per element.
    example tied to context:
        `php.&&' with `php.and', covering all
        1,156 elements.
```

---

## the restatement

Before anything is added, here is what was already true.

Log 041 built two orders and kept them apart. The CONTAINMENT order
asked only which form pairs an operation ACCEPTED — a signature was a
vector over 64 form pairs, an entry was non-zero when the operation
accepted, and no answer entered the entry at all. The DOMINANCE order
was that plus an agreement rate of exactly 1.000 on the shared cells.

The containment order had exactly one top: a class of all 64 form
pairs carried by 35 leaves, mostly php and ruby. Log 041 said in as
many words that the top cost nothing, because a domain that accepts
everything contains everything without earning it.

the owner's ruling says the trouble is a grain and not a caveat. A row of
that vector was a single bit, accept or not. It should have been the
whole answer. Put the answer in the element and the two orders collapse
into one, because a wider leaf sits above a narrower one only where it
REPEATS it, and accepting a question is worth nothing on its own.

---

## 1 — the walkthrough

Start with `python.@`, because the whole rebuild is visible in it.

`python.@` is matrix multiplication. It was asked 1,156 questions and
it raised on every single one — 1,156 `raise:TypeError`, with
`raise:ValueError` and `raise:OverflowError` appearing beside it on
some *(measured)*. Under log 041's reading its DOMAIN was empty, so it
was not a leaf at all: `l3_alt_readings.leaf_keys` filters out an empty
domain and the population was 238.

At the value grain it is a leaf again, and a maximal one. It speaks on
every element in the grid. What it says is "no" every time, and "no" is
an answer. **That is why this log has 239 leaves and log 041 had 238**
*(measured)*, and it is the smallest complete statement of what the
ruling changed.

Now the grid. Log 041's grid was 64 form pairs. This one is **1,156
elements** — the same input cells decisions 18 and 33 already used to
compute the agreement rate, which is worth saying plainly: **the
agreement rate was already being measured at the value grain, and only
the ORDER was being built at the form grain.** The rebuild does not
need new data. It needs the data already in hand to be read at the
grain it was taken at.

Over the 239 leaves, the elements spoken sum to **121,100**, carrying
**6,155 distinct answer tokens** and **6,005 distinct element values**
*(all measured)*. **64,331 of the 121,100 — 53.1 percent — are
elements where a leaf's own holders do not agree with one another**
*(measured)*, and that number is why the choice of grain in §2 is a
choice and not a formality.

Then the order, and there is only one of it:

    X <= Y   when Y carries the SAME element value
             as X on EVERY element X speaks on

X sits strictly below Y when that holds and Y also speaks somewhere X
is silent. Three things follow and none is assumed:

- **It is an order.** Speaking sets nest and values match, so a
  super-chain of two closes. Checked over every such chain the run
  finds: **15 chains, no failure** *(measured, and the run asserts it)*.
- **Containment-without-faithfulness has no referent.** There is no
  second order to sit beside it. A pair either nests faithfully or it
  is not related at all.
- **God status is impossible by construction.** A leaf gets above
  another only by repeating it.

### the php.== verification

`php.==` is the case the owner named, so it is checked directly rather than
left to be inferred.

`php.==` speaks on **1,156 of 1,156 elements** *(measured)*. It is one
of **79 leaves that do — php 27, python 25, ruby 24 and typescript 3**
*(measured)*, the open-dispatch languages that refuse almost no input.
Under log 041's containment order that put it in the single top class,
against which nothing could be higher.

Under the merged order:

| quantity | value |
|---|---|
| elements `php.==` speaks on | 1,156 of 1,156 |
| leaves whose questions all sit inside its own | 160 |
| of those, the ones it CONTRADICTS somewhere | 160 |
| leaves it therefore sits above | **0** |

All measured. **`php.==` sits above nothing.** Every one of the 160
leaves whose questions it could have answered, it answers differently
somewhere. It is maximal — nothing is above it either — but so are 208
other leaves, and being maximal is now worth what it should be worth,
which is "nobody repeats it", not "it contains everybody".

Here are the elements that deny it, printed by the run, its own family
first and then the widest sub-node:

```
dart.==     fractional|base_1_5|text|base_empty
  dart.==    truth:false
  php.==     raise:Error,truth:false

kotlin.!=   fractional|base_1_5|fractional|base_1_5
  kotlin.!=  truth:false
  php.==     truth:true

kotlin.==   fractional|base_1_5|fractional|inf
  kotlin.==  raise:java.lang.NumberFormat...
  php.==     truth:false

java.!=     fractional|base_1_5|fractional|base_1_5
  java.!=    truth:false,truth:true
  php.==     truth:true
```

Read the first one. `dart.==` is asked to compare 1.5 against the
empty string. Dart answers `truth:false` and only that. Php answers
`truth:false` on some of its holder pairs and **raises** on others.
That is a difference of element value, and one is enough: dart.== does
not sit below php.==, and php.== is therefore not above dart.==.

The fourth is the holder grain earning its keep. `java.!=` carries TWO
tokens at one element — `truth:false` on some holder pairs and
`truth:true` on others *(measured)*. Which of java's holders split that
way is not read here, so the usual boxed-against-unboxed explanation is
**unverified** and is named as a guess rather than carried as a
finding. Php answers one thing there. Under a grain that
tolerated the split those two would have matched. Under this one they
do not, and the reason is a measured disagreement inside java rather
than anything about php.

The last thing to say about `php.==` is what did NOT happen to it. It
was not demoted by a rule aimed at it. Nothing in the machinery knows
which leaf it is. It fell out of the top the moment the element carried
an answer, which is what the owner's ruling said it would.

---

## 2 — the numbered decisions

Three, continuing from log 041's decision 57. Log 042 owns the `B'
series and this log does not touch it. Each decision is stated with
what it costs to overturn.

### decision 58 — what an element is

**A signature's element is (lhs holder + value class, rhs holder +
value class) -> answer token, and the element KEY is the input cell
`form_a|vc_a|form_b|vc_b`.**

Why the key is not the holder. Holders are language-private. Go's
`int64` and rust's `i64` are two strings that were never meant to be
one, and no bridge between them was ever measured. A key carrying a
holder would make every cross-language element distinct, and the order
would then say that no operation in any language relates to any
operation in any other — a result produced by the key rather than by
the data. The shared layer-1 value classes ARE bridged: decision 41
measured that every language's value vocabulary is contained in
python's, and that containment is what lets an element cross a
language boundary at all.

The holder is not thrown away. It moves into the element's VALUE,
which is decision 61.

Cost to overturn: change `cell_key` in `l3_valuegrain.py`.

### decision 61 — the grain, HOLDER-PAIR, and it is FLAGGED

**An element's value is the WHOLE SET of tokens the leaf carried over
its holder pairs there, and two leaves match at an element only when
those sets are EQUAL.**

That is the holder-pair grain, and it is the literal reading of "each
row isnt a row element, its a vector": no holder's row is averaged
away, and a leaf whose holders answer two different things at one
element is a different object from a leaf that answers one thing there.

The alternative is the form-pair grain, which is decision 27's standing
rule: two leaves match when their token sets INTERSECT, so a holder
split does not count against them.

**FLAGGED, OVERTURNABLE. the owner has not chosen between the two and this
log does not choose for him.** The holder-pair grain is taken as the
DEFAULT for three reasons, in order of weight:

1. It is the literal reading of his sentence.
2. It is the stricter of the two, so nothing it certifies would be
   uncertified by the other. A union candidate found here is a union
   candidate under either grain; the reverse does not hold.
3. Intersection carries no guarantee of being an order. X can match Y
   on `{a}` against `{a,b}`, Y match Z on `{a,b}` against `{b}`, and X
   and Z share nothing. **On this data it happens not to fail — 0
   transitivity failures, measured** — so this is a reason and not a
   refutation, and it is stated as one.

What the choice costs, measured on every run:

| grain | nesting pairs | faithful | maximal leaves |
|---|---|---|---|
| holder-pair (default) | 18,479 | 202 | 209 |
| form-pair | 18,479 | 349 | 172 |

**The two grains differ by 147 faithful edges and 37 maximal leaves.**
That is the size of the ruling the owner has not yet made, and it is not
small. It is also not decisive: neither grain gives a family a single
top, so the headline of §3 is the same under both.

Cost to overturn: set `GRAIN` in `l3_valuegrain.py` to `"form"`.

### decision 59 — silence is free, a claim is not

**The order asks Y to match X only where X SPEAKS. A raise, a death and
a backend refusal are claims and must be matched. Being silent is not
a claim and need not be matched.**

The reasoning, shown because the owner asked for it shown.

A leaf is silent at an element when nobody ever ran it there — the
compiler would not take the holder pair, so no measurement exists.
Requiring Y to be silent too would make the order say something about a
run that never happened. **Absence of a claim cannot contradict a
claim.** So Y may speak on a thousand elements X is silent on and still
sit above it. That is WIDENING and it is permitted, which is the whole
content of "a wider operation" once the answers are in.

A raise is different in kind. `python.+` answering `raise:TypeError` at
`text|base_abc|whole|base_42` was measured, and it is a claim about
that element: this cannot be added. A leaf answering `text:abc42` there
contradicts it flatly. Decision 31 already made a raise a token; this
decision declines to carve an exception back out.

The same holds for a death, and for `refuse:codegen` — a row that says
CODEGEN_REFUSE was asked and declined, where an absent row was never
asked. That distinction is the whole load-bearing part of this
decision and it is where an attack should land.

**FLAGGED, with its cost measured.** Someone could read a raise as a
DECLINE, which is closer to silence than to an answer. That reading is
computed on every run:

| reading | nesting pairs | faithful | maximal leaves |
|---|---|---|---|
| a raise is a claim (decision 59) | 18,479 | 202 | 209 |
| a raise is silence | 15,641 | 455 | 205 |

All measured. **Reading a raise as silence more than doubles the
faithful edges, 202 to 455, and moves the maximal count by four.** So
the decision is worth a great deal to the edges and almost nothing to
the headline. Only 53 of the 6,005 element values are wholly a claim of
refusal *(measured)*, which is why: the raises are spread thin across
many leaves rather than concentrated in a few.

Cost to overturn: `CLAIM_PREFIXES` in `l3_dominance_vg.py`.

### decision 60 — a backend refusal is a token

**A `codegen_refuse` row becomes the token `refuse:codegen`.** Decision
40 dropped those rows from the answer tables because they carried no
value to canonicalise; at the value grain what they carry is the
refusal itself. Folded into decision 59's flag and counted with it.

### one thing that is NOT a decision

The support threshold. Decision 55 exists because an agreement RATE
over three cells is not a rate. The merged order computes no rate — it
asks whether every element matches, and one element is enough to say
no. So decision 55 does not apply here and is not silently reused. What
takes its place is honesty about width: every table in the products
carries the number of elements a leaf speaks on beside its verdict, so
a leaf certified over four elements is visibly certified over four
elements.

---

## 3 — the dominance rerun, against log 041

The same question, asked of the merged order.

| quantity | log 041, form grain | log 043, value grain |
|---|---|---|
| leaves | 238 | **239** |
| grid | 64 form pairs | **1,156 elements** |
| orders | two, kept apart | **one** |
| a single top by containment alone | **yes**, 64 cells, 35 leaves | **the question has no referent** |
| pairs that nest and are readable | 13,831 | **18,479** |
| of those, faithful | 189 (1.4 percent) | **202 (1.09 percent)** |
| maximal | 184 of 238 (77.3 percent) | **209 of 239 (87.4 percent)** |
| a dominant vector | NO | **NO** |

All measured except the two percentages, which are derived.

Read the rows in order, because each one moved for its own reason.

**The nesting count rose, 13,831 to 18,479.** That is not a finer
measurement of the same thing. Log 041 counted pairs whose DOMAINS
nested and which shared 32 input cells; this counts pairs whose
SPEAKING SETS nest, and speaking sets are finer, so pairs that were
tied at the form grain now separate into a strict nesting. The support
bar is also gone, which adds thin pairs back.

**The faithful count barely moved, 189 to 202, and the RATE fell.** The
finer grid gives more chances to disagree, and 98.9 percent of nesting
pairs take one. Log 041's headline was 1.4 percent; the honest version
is 1.09.

**The maximal count rose from 184 to 209, and the share from 77 to 87
percent.** Twenty-five more leaves have nothing above them. This is the
ruling's direct effect: leaves that were dominated at the form grain by
a wider leaf are, at the value grain, dominated by nobody, because the
wider leaf differs from them on some value inside a form pair the two
shared.

**The single top is gone and did not go quietly.** Log 041 could report
"the containment order flattens" as a true statement about a real
object. There is no such object now. There is one order and it has 209
tops.

### per family

| family | leaves | nesting pairs | faithful | maximal | a dominant vector? |
|---|---|---|---|---|---|
| arithmetic | 60 | 1,303 | 2 | 59 | NO |
| comparison | 83 | 2,054 | 14 | 72 | NO |
| logical | 36 | 434 | 108 | 24 | NO |
| bitwise | 33 | 368 | 6 | 27 | NO |
| shift | 21 | 140 | 0 | 21 | NO |
| other | 6 | 10 | 0 | 6 | NO |

All measured. Against log 041's per-family table, three things changed
and are worth naming.

**Arithmetic collapsed. 60 leaves and 59 maximal, on 2 faithful edges
out of 1,303 nesting pairs** *(measured)*. Log 041 gave arithmetic 46
maximal leaves of 59. Nearly every arithmetic containment that survived
the form grain dies at the value grain, which says the arithmetic
family's agreements were agreements about which FORMS were accepted and
not about what was computed.

**Logical reversed.** Log 041's headline was that the logical family
failed as hard as a family can — 36 leaves, 36 maximal, not one
operation dominating another. At the value grain it is **the only
family with real internal structure: 108 faithful edges of 434 nesting
pairs, 24.9 percent, and 24 maximal leaves rather than 36**
*(measured, the percentage derived)*. The reversal has a cause and it
is decision 55, now absent: a short-circuit `&&` in a checked language
speaks on four elements, so under log 041 every one of its pairs fell
below the support bar and could not be read at all. The merged order
reads them, because four matching elements is four matching elements.

**Shift and other flattened to nothing. 0 faithful edges each**
*(measured)*. Every shift operation in these twelve languages is
maximal, and there is no pair among them where one repeats another over
a wider set of questions.

### the vector classes, which are new here

238 leaves carried 59 distinct domains at the form grain. 239 leaves
carry **218 distinct vectors** at the value grain *(measured)* — almost
all singletons, which is expected once an element carries an answer.
The thirteen that are not singletons are worth reading, because they
are exact identities and not near-misses:

```
csharp.&&  go.&&  java.&&  kotlin.&&
  rust.&&  swift.&&
csharp.||  go.||  java.||  kotlin.||
  rust.||  swift.||
cpp.!=  cpp.not_eq      cpp.&  cpp.bitand
cpp.&&  cpp.and         cpp.^  cpp.xor
cpp.bitor  cpp.|        cpp.or  cpp.||
php.&&  php.and         php.or  php.||
ruby.&&  ruby.and       ruby.or  ruby.||
java.>>  java.>>>
```

All measured. **Six statically checked languages carry a
byte-identical `&&` vector, and the same six a byte-identical `||`.**
That is the strongest cross-language sameness this node has produced —
not a similarity score, an identity. It is also thin, and the thinness
must travel with it: those six speak on **four elements each**, because
a short-circuit operator in a checked language admits truth values and
almost nothing else. Six languages agreeing on four questions is six
languages agreeing on four questions.

The c++ pairs are log 034's word spellings turning up unasked, again,
and `java.>>` with `java.>>>` is a genuine finding of its own: over
every element java was asked, the signed and unsigned right shifts are
indistinguishable, because the probe values never made the sign bit
matter. That is a gap in the probe space and it is named here rather
than read as a sameness.

### the union vector, which is still not news

The union of the 209 maximal leaves' speaking sets is **1,156 of 1,156
elements** *(measured)* — the whole grid, exactly as log 041 found at
its own grain, and for the same reason. `php.%` alone speaks on all
1,156. **The union vector is the grid and reaching it is worth
nothing.** What is worth something is §4.

---

## 4 — the union candidates, per family

This is the Hub-facing answer, and the readable form of it is
`Research/kind_fuzz_clustering/union_candidates.md`.

The question. The order has 209 tops rather than one, so no single
operation carries the node. Can several be LAID ON TOP of one another?
Two maximal leaves can when they never carry different values on an
element both speak on — then the combined vector is still one answer
per element and neither leaf gives up a measured answer.

Compatibility is pairwise and that is enough for a group of any size: a
union of vectors fails to be one answer per element exactly when SOME
TWO of them differ somewhere. So the assemblies are the maximal cliques
of the compatibility graph, enumerated exactly.

Two kinds of compatible edge, and the difference is marked rather than
buried:

| edge | meaning | what it is worth |
|---|---|---|
| agreeing | they share elements and agree on every one | measured sameness |
| vacuous | they share no element at all | assembly, not evidence |

The headline, all measured:

| family | leaves | maximal | agreeing | vacuous | blocked | widest assembly | its coverage |
|---|---|---|---|---|---|---|---|
| arithmetic | 60 | 59 | 0 | 0 | 1,711 | none | — |
| comparison | 83 | 72 | 1 | 12 | 2,543 | 2 | 531 of 1,156 |
| logical | 36 | 24 | 10 | 1 | 265 | 2 | 1,156 of 1,156 |
| bitwise | 33 | 27 | 2 | 0 | 349 | 2 | 64 of 1,156 |
| shift | 21 | 21 | 1 | 0 | 209 | 2 | 16 of 1,156 |
| other | 6 | 6 | 0 | 0 | 15 | none | — |

**14 agreeing pairs within a family, against 5,092 blocked.** That is
the Hub-facing answer and it is a hard one. Log 041 offered 31
within-family union candidates at the form grain. At the value grain
fourteen survive, and **ten of the fourteen are in the logical family**.

**The arithmetic family offers nothing.** 59 maximal leaves, 1,711
pairs, every one blocked, no assembly of two exists at all *(measured)*.
There is no pair of arithmetic operations in these twelve languages
that could be one operation without one of them giving up an answer it
was measured giving.

The fourteen, in full:

| left | right | family | shared elements | |
|---|---|---|---|---|
| `cpp.&&` | `dart.&&` | logical | 4 | cross-language |
| `cpp.and` | `dart.&&` | logical | 4 | cross-language |
| `cpp.or` | `dart.\|\|` | logical | 4 | cross-language |
| `cpp.\|\|` | `dart.\|\|` | logical | 4 | cross-language |
| `php.&&` | `php.and` | logical | 1,156 | same language |
| `php.or` | `php.\|\|` | logical | 1,156 | same language |
| `ruby.&&` | `ruby.and` | logical | 1,156 | same language |
| `ruby.or` | `ruby.\|\|` | logical | 1,156 | same language |
| `cpp.&&` | `cpp.and` | logical | 562 | same language |
| `cpp.or` | `cpp.\|\|` | logical | 562 | same language |
| `cpp.!=` | `cpp.not_eq` | comparison | 282 | same language |
| `cpp.&` | `cpp.bitand` | bitwise | 64 | same language |
| `cpp.bitor` | `cpp.\|` | bitwise | 64 | same language |
| `java.>>` | `java.>>>` | shift | 16 | same language |

All measured. **Ten of the fourteen are a same-language spelling pair**
— the c++ word operators, php's and ruby's `and`/`or`. Those are known
positive controls from logs 034 and 035, and their turning up here is
the machinery working rather than news.

**The news is the four cross-language rows, and they are thin.**
`cpp.&&` with `dart.&&` agree on four elements. Four. That is enough to
be a union candidate under this order and it is not enough to build a
kind map on, and both halves of that sentence should travel together.

**Log 041's headline union candidate does not survive.** `dart.==`
with `php.===` agreed on all 64 form pairs and was called the node's
strongest unification candidate. At the value grain the pair is
BLOCKED, and not narrowly: **the two speak on 1,089 elements in common
and carry different values on 660 of them** *(measured)*. The first is
exactly the element §1 quoted — dart answers `truth:false` comparing
1.5 to the empty string, php answers `truth:false` on some holder pairs
and `raise:Error` on others. **The form grain could not see that,
because
both leaves accepted the form pair `fractional|text` and the domain
vector recorded only that they accepted it.**

The blocked unions with their blocking elements quoted, per family, are
the body of `union_candidates.md`. A sample from arithmetic, which is
the family with nothing to offer:

```
php.% / python.%
  at fractional|base_1_5|fractional|base_1_5
  php.%     whole:0
  python.%  fractional:0.0, raise:TypeError,
            whole:0
```

php's remainder on 1.5 by 1.5 casts to whole and answers 0. Python's
answers 0.0 on floats, 0 on whole numbers, and raises where a holder
pair has no remainder at all. One element, three tokens against one,
and the union is blocked *(measured)*.

---

## 5 — what the boundary runs will add, and where they plug in

Log 042 is running beside this one and this section is written from its
artifacts on disk, not from its results, which do not exist yet.

`boundary_targets.json` names **6,444 boundary targets across the
twelve, of which 1,623 are already exact** *(measured, read off the
artifact)*. A target is a place where two numerically adjacent value
classes of one operation answer in DIFFERENT classes, so a boundary
sits between them at a number nobody has measured. The axis is the six
whole-number value classes from 0 to `u64max`.

What that does to this log's products is precise and worth stating
before the results land, because it is a prediction that can be wrong.

**Every boundary found adds a value class, and every value class added
adds elements to the merged grid.** The grid is 1,156 today. Each new
class on the whole axis multiplies out against every holder pair and
every operation that reaches it.

**Adding elements can only REMOVE order edges, never add one.** The
reason is the shape of the order and not a guess: `X <= Y` asks Y to
match X everywhere X speaks. A new element either leaves both silent,
in which case nothing changes, or makes X speak somewhere new — and
then Y must match there too, which it may fail to do. No new element
can repair a mismatch that already exists. So:

- **the 202 faithful edges are an UPPER BOUND**;
- **the 209 maximal leaves are a LOWER BOUND**;
- **the 14 union candidates are an UPPER BOUND**, by the same argument
  applied to the compatibility graph.

*(All three derived, from the definition of the order rather than from
a run.)* That is the single most useful thing this log can hand log
042: it does not have to re-argue any of these numbers, only report
which of them fell.

Where the results plug in, mechanically:

1. The new value classes enter the answer artifacts in the shape
   `l3_valuegrain.load_nine` and `load_three` already read — a row
   carrying `lhs.value` and `rhs.value`. **No change to
   `l3_valuegrain.py` is needed** to admit them.
2. `python3 l3_valuegrain.py` rebuilds `signatures_valuegrain.json` on
   the wider grid.
3. `python3 make_union_candidates.py` reruns everything downstream,
   because it calls the dominance pass itself.
4. The three bounds above become the check: if a faithful edge count
   rises, something is wrong with the fold and not with the finding.

One thing log 042 will NOT settle. The boundaries are on the numeric
axes. `java.>>` with `java.>>>` being one vector class is a gap in the
SIGN of the probe values, not in their magnitude, and no whole-axis
boundary reaches it. That pair needs a negative whole value class,
which is a probe-space question and belongs with the owner rather than in
either log.

---

## 6 — what this implies for the Hub's kind map

**Flagged for the owner. None of this is a ruling and nothing has been
changed on the strength of it.**

1. **The god-operator opening is closed and it was a grain, not a
   metric.** No leaf sits above another without repeating it. `php.==`
   sits above nothing at all. Any future reading that produces a
   universal operation by taking the widest anything should be checked
   against this one first.

2. **The unification short list shrank by more than half and moved
   families.** 31 candidates at the form grain, 14 at the value grain,
   and ten of the fourteen in the logical family. A kind map built on
   log 041's list would have carried `dart.==` with `php.===` as its
   worked example, and that pair is blocked here.

3. **The arithmetic family cannot be unified at all on this evidence.**
   Zero agreeing pairs among 59 maximal leaves. That is a finding about
   arithmetic and not about the method: the comparison family, run
   through the same machinery, produced one.

4. **The six-language `&&` identity is the best cross-language object
   in the node and it rests on four elements.** If the Hub wants one
   worked example of an intention crossing a language boundary intact,
   that is it, and widening the probe space for short-circuit operators
   is what would make it worth its weight.

5. **The grain is the owner's to rule and it is worth 147 edges.** Decision
   61 is flagged. Holder-pair against form-pair moves the faithful
   count from 202 to 349 and the maximal count from 209 to 172. Neither
   grain gives any family a single top, so the ruling changes the
   detail and not the headline.

6. **Constructs are still not carried.** Log 041 said the alternative
   readings were operators only; the same holds here for the same
   reason, and `construct_answers_<lang>.json` carries the answers that
   would let it be done in one pass. Said rather than quietly dropped.

---

## 7 — products and reproduction

New in `Research/kind_fuzz_clustering/`:

```
l3_valuegrain.py            decisions 58, 60, 61
signatures_valuegrain.json  the vectors, sparse
l3_dominance_vg.py          decision 59, the order
dominance_valuegrain.json   the whole rerun
make_dominance_lattice_vg.py
dominance_lattice_vg.html   the visual
make_union_candidates.py
union_candidates.md         the Hub-facing read
```

**Nothing else on disk was touched.** `l3_dominance.py`,
`dominance_lattice.json` and `dominance_lattice.html` are exactly as
log 041 left them, and the value-grain products sit beside them rather
than over them, so the two readings can be set against each other.
`domstub.js` is unchanged.

### the format of `signatures_valuegrain.json`

It is sparse, because a dense 239 by 1,156 table of token sets is
tens of megabytes for no gain. Four tables and one vector per leaf:

```
cells[i]   the element key,
           form_a|vc_a|form_b|vc_b
tokens[i]  one answer token
values[i]  one element VALUE: the sorted
           list of token ids a leaf's
           holders carried at one element
leaves[k].vec
           a flat list of [cell id, value
           id], sorted by cell id.  a cell
           id ABSENT from the list is an
           element the leaf is SILENT on.
```

Reading one leaf back is one line:

```
{cells[c]: [tokens[t] for t in values[v]]
 for c, v in leaves[k].vec}
```

The file is 4.7 MB and `dominance_valuegrain.json` is 8.4 MB
*(measured)*.

### reproduction

In order, all on the host, all under six seconds each:

```
python3 l3_valuegrain.py
python3 l3_dominance_vg.py
python3 make_dominance_lattice_vg.py
python3 make_union_candidates.py
```

The last two each call `l3_dominance_vg.main()` themselves, so either
one rebuilds `dominance_valuegrain.json` on the way. Neither rebuilds
`signatures_valuegrain.json` — that is step one and it is the only step
that reads the answer artifacts.

### the visual, validated

```
node domstub.js dominance_lattice_vg.html \
  lattice \
  answer,phpeq,famtable,maxpairs,cands,blocked,legend,fams
```

| visual | scripts | threw | panels filled | drawing |
|---|---|---|---|---|
| `dominance_lattice_vg.html` | 1 | 0 | 8 | lattice appended |

All measured, exit status 0. The page draws a Hasse diagram per family
over the 218 vector classes, and **every line in it is faithful by
construction**, so the red edges of `dominance_lattice.html` are simply
absent rather than recoloured. Each family panel carries the count of
nesting pairs the answers threw out, so a reader is told why the
picture is sparse rather than left to notice it.

`hq.sh check`: **0 errors** *(measured, before and after this log)*.
