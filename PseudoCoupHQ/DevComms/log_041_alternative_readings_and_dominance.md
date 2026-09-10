# log 041 — the alternative readings, and the dominance lattice

Date: 2026-08-20. Node:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

Log 041 was free when this was written.

the owner ruled on 2026-08-20 that the product metric carries a bias, that
every alternative reading of it should be built rather than argued
about, that each one gets its own visual, and that a new analysis he
sketched should be built beside them. This log does those five things
and nothing else.

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

**No probe ran for this log. No lane ran. Nothing was compiled and
nothing was executed.** Every number below is read off artifacts that
were already on disk, or computed from them by three new scripts that
finish in under a second each.

---

## words used in this log

Every short word this log leans on is defined here. Each definition
carries an example taken from this log's own content rather than a
made-up one. Nothing below this block uses a word that is not either
ordinary English or defined here.

```
leaf
    one operation in one language, and the
    thing that gets grouped.
    example tied to context:
        `go.+' is a leaf.  there are 238 of
        them.

cell (also: input cell)
    one combination of operand kinds an
    operation was asked about.  the shared
    grid holds 64 of them.
    example tied to context:
        `whole|whole' is a cell.  go's `+'
        accepts three cells and java's
        accepts thirty-two.

domain
    the set of cells an operation actually
    accepted.  a refused cell is not in it.
    example tied to context:
        `go.+' has a domain of 3 cells and
        `java.+' has one of 32.

J, the Jaccard
    shared cells divided by all cells either
    one accepts.  it is 1 when two domains
    are identical and 0 when they never meet.
    example tied to context:
        `go.+' against `java.+' is J 0.094.

A, the agreement rate
    the fraction of the cells BOTH accept on
    which the two return the same answer.
    example tied to context:
        `go.+' against `java.+' is A exactly
        1.000 over 88 shared input cells.

C, the containment rate
    shared cells divided by the size of the
    SMALLER of the two domains.  it is 1
    whenever one domain sits wholly inside
    the other.
    example tied to context:
        `go.+' against `java.+' is C 1.000,
        because every cell go accepts, java
        accepts.

the product reading
    decision 27, from log 031 and carried to
    twelve languages in log 033: similarity
    is J times A.  it is the reading every
    earlier tree in this node was built on.
    example tied to context:
        `go.+' against `java.+' is 0.094
        under it.

supported, unsupported
    a pair is SUPPORTED when it shares enough
    input cells for its agreement rate to be
    a rate at all.  decision 55 sets the bar.
    example tied to context:
        `go.&&' against `java.&&' shares four
        input cells, so it is unsupported and
        its A of 1.000 is not read.

average linkage
    the rule for joining two groups: their
    similarity is the mean over every pair of
    leaves, one from each.
    example tied to context:
        all four trees in this log use it, so
        the linkage is never what differs
        between them.

plateau
    a range of threshold over which the
    grouping does not move at all.  a wide
    plateau is a reading the data offers; a
    narrow one is an accident of where the
    line was put.
    example tied to context:
        the product tree's widest is
        [0.155, 0.185) and it holds 21
        groups.

matched granularity
    comparing two trees when each has been
    cut into the SAME number of groups.
    example tied to context:
        comparing the domain tree's 2 groups
        against the agreement tree's 29 would
        measure the cut and not the trees.

the containment order
    X sits below Y when every cell X accepts,
    Y accepts.  domains only.  answers are
    not consulted.
    example tied to context:
        `go.+' sits below `java.+' in it.

the DOMINANCE order
    X sits below Y when X sits below Y in the
    containment order AND the two never
    disagree on a cell they share.  this is
    the CORE's `nests' arm.
    example tied to context:
        `go.+' is dominated by `java.+',
        because A is 1.000.

Hasse diagram
    the picture of an order with the edges
    that FOLLOW FROM other edges removed.  if
    X is inside Z and Z is inside Y, the edge
    from X straight to Y is not drawn,
    because the two shorter edges already say
    it.  what is left is the covering
    relation, and it is the only version of
    an order a person can read.
    example tied to context:
        the shift family has 7 classes; its
        Hasse diagram is what
        `dominance_lattice.html' draws for
        it.

maximal element
    an element with nothing above it.  in the
    containment order it is a domain no other
    domain contains.
    example tied to context:
        the arithmetic family has 6 maximal
        classes and the comparison family
        has 1.

dominant vector, in the owner's sense
    a single element that sits above ALL the
    others -- one operation whose domain
    contains every other domain and which
    never disagrees with any of them.  it is
    what "does the tree flatten" is asking
    for.  a family has one only when it has
    exactly ONE maximal element under the
    dominance order.
    example tied to context:
        no family in this node has one, and
        the whole population has 184 maximal
        leaves where a dominant vector would
        leave exactly 1.

domain class
    the group of leaves whose domains are
    identical, taken as one node of the
    lattice.
    example tied to context:
        238 leaves carry 59 distinct domains,
        and the widest class holds 35 leaves
        that all accept the whole 64-cell
        grid.

fork
    two maximal elements that overlap and
    disagree on every cell they share.  no
    one operation can carry both.
    example tied to context:
        `php.<=>' against `python.=='.

union candidate
    two maximal elements that overlap and
    never disagree.  one operation could
    carry both domains.
    example tied to context:
        `dart.==' against `php.===', over all
        64 shared cells.
```

---

## the restatement

Before anything is added, here is what was already true, in the
smallest number of sentences that keeps it true.

This node measures what twelve languages DO. It generates a small
program per operation per input pair, runs or checks it, and records
two things: which inputs the operation accepted, and what it answered
on each. Log 035 folded all of that into 238 operation signatures over
a shared grid of 64 input cells, and clustered them with a similarity
that multiplies two factors — how much the two domains overlap, and
how often the two agree where they overlap. That product is decision
27. Every tree the node has published rests on it.

the owner's ruling of 2026-08-20 is that a product of two factors cannot say
which factor moved. The standing case is `go.+` against `java.+`: they
never disagree once, over 88 shared input cells, and the product puts
them at 0.094 because go accepts three cells and java accepts
thirty-two. The product spent all of A's evidence on a J that was
small for a reason that had nothing to do with disagreement.

This log builds three readings that separate the factors, gives each
one its own visual, and then builds the analysis the owner sketched, which
asks a different question of the same data: not how far apart two
operations are, but whether one of them contains the rest.

---

## 1 — the walkthrough

Start with one pair, because the whole log is visible in it.

`go.+` accepts three cells. `java.+` accepts thirty-two, and the three
go accepts are among them. On the 88 input cells both accept, the two
languages return the same answer every single time — A is exactly
1.000, and log 033 measured that before this log existed.

Under the product reading those two leaves sit at 0.094. That is very
near the bottom of the scale. Two operations that have never once been
caught disagreeing are placed nearly as far apart as two that always
disagree. Nothing is wrong with the arithmetic: J is 0.094 because
java accepts twenty-nine cells go does not, and 0.094 times 1.000 is
0.094. What is wrong is the reading. The number says "far apart" and
the evidence says "identical wherever comparable, and one is wider".

Those are two different findings and the product cannot tell them
apart. That is the bias, stated exactly.

So the factors are separated, and each separation is a tree of its
own over the same 238 leaves with the same average linkage. Only the
distance changes, which is what makes the four trees comparable at all.

**The agreement-only tree** throws the domain away. Similarity is A.
The question it asks is "where both speak, do they agree", and nothing
else. It needs one new rule, because an agreement rate computed over
three shared cells is not a rate — that is decision 55, below.

**The containment tree** keeps both factors but replaces J with C,
which divides by the smaller domain rather than by the union. A
signature sitting wholly inside another scores C = 1, so nesting costs
nothing, while two domains that genuinely half-overlap still cost.

**The domain-only tree** throws the answers away. Similarity is J.
Log 033 already computed this one as a summary control; here it
becomes a full tree so it can be set against the agreement tree pair
for pair.

What each reading shows that the product hid:

- **Agreement-only** shows that disagreement is *not* what separates
  these 238 leaves. Cut as coarse as it can go, this tree puts 214 of
  238 leaves in one group and leaves 24 singletons *(measured)*. The
  structure the product tree shows is therefore almost entirely the
  domain factor wearing the answers' clothes.
- **Containment** shows which of the product's distances were about
  disagreement and which were about width. `go.+` against `java.+`
  moves from 0.094 to 1.000 — the pair was never about disagreement.
  `java.+` against `cpp.+` moves from 0.129 only to 0.293, because C
  is 0.500 and A is 0.586 there; that pair really is a partial overlap
  with real disagreement inside it.
- **Domain-only** shows what the clustering sees when told only which
  inputs each operation accepts. Set against the agreement tree, every
  pair the two place differently is a nests-or-overlaps case, which is
  §5.

And then the owner's own paradigm, which is not a fourth distance. He asked
whether the picture flattens into a dominant vector. Read against this
data his sketch is exact: an operation IS a vector over 64 cells, a
cell is non-zero when the operation accepts it, "what others have that
non-zero element" is the containment order, and "does that tree
flatten" is asking whether that order has a single top. It has one,
and the answer is still no, and §4 is why.

---

## 2 — the numbered decisions

Three, continuing from log 040's decision 54. Each is stated with what
it costs to overturn, in the node's standing style.

### decision 55 — the support threshold

**A pair needs at least 32 shared input cells before its agreement
rate is read at all.** Below that the pair is UNSUPPORTED.

Why 32. A is a rate. Over 32 shared cells one cell moves it by 0.031,
which is fine enough that the third decimal a tree is cut on means
something. Over 8 shared cells one cell moves it by 0.125 and the rate
is a coin, not a measurement. 32 is the smallest power of two at which
one cell is worth under three points, and it is also half the 64-cell
grid, so it is sayable without arithmetic: a pair must meet on at
least half a grid's worth of cells.

What happens to a pair below it. **It is left out of every average,
not scored zero.** Zero is a claim — it would say the two never agree,
which is exactly what was not measured. When two groups are compared,
only their supported leaf pairs count toward the mean. If two groups
share no supported pair at all, their similarity is 0.0 and the merge
is recorded as unsupported, with a count.

The counts, measured:

| quantity | value |
|---|---|
| leaf pairs in all | 28,203 |
| supported at 32 | 22,570 |
| EXCLUDED as unsupported | 5,633 (20.0 percent) |
| of those, sharing no input cell at all | 1,264 |
| merges made with no supported pair beneath them | 22 of 237 |

Sensitivity, computed on every run so the choice is never invisible:
at 16 shared cells the excluded count would be 3,674 (13.0 percent);
at 64 it would be 10,230 (36.3 percent) *(all measured)*.

Cost to overturn: set `SUPPORT` in `l3_alt_readings.py` to another
number and re-run. It takes under a second.

### decision 56 — what dominance is

**X is dominated by Y when three things hold at once: every cell X
accepts Y accepts and Y accepts at least one more; the pair is
supported under decision 55; and the agreement rate is exactly 1.000.**

Why exactly 1.000 and not a high threshold. Dominance is the CORE's
`nests` arm and the CORE's own wording is "same answers, wider
domain". One disagreeing cell is a measured counter-example to
sameness. A 0.99 bar would let a signature dominate another it
demonstrably contradicts somewhere, which is the distinction the
trichotomy exists to hold.

The looser 0.99 reading is computed anyway and printed beside it, so
the cost of the strictness is a number and not an argument: 184
maximal leaves at 1.000 against 176 at 0.99 *(measured)*.

Cost to overturn: change `CLEAN` in `l3_dominance.py`.

### decision 57 — the lattice is drawn per family, over classes

**The containment lattice is drawn over DOMAIN CLASSES, and drawn one
operator family at a time.**

238 leaves carry only 59 distinct domains, so a leaf-wise drawing
would put 179 nodes exactly on top of other nodes with exactly the
same edges. And 59 classes in one diagram is not readable at any size,
so the drawing is split by the operator families log 040's decision 9
already defined — arithmetic, comparison, logical, bitwise, shift and
a residue of three spellings called other.

**The dominance order is NOT collapsed to classes.** It is computed
over leaves, always, because two leaves with one domain can answer
differently and that difference is the whole of what dominance turns
on.

Nothing is lost by the split: the overall lattice's shape is stated in
the page's own summary panel and its full edge list is in
`dominance_lattice.json`.

Cost to overturn: one grouping call in `make_dominance_lattice.py`.

### one thing that is NOT a new decision

The linkage. All four trees use the same average linkage, the same
tie-breaking, and the same no-chosen-cut rule as every earlier tree in
this node. That is deliberate: if the linkage changed too, no
difference between two of these pictures could be attributed to
anything.

It is checked rather than asserted. **The domain-only reading
reproduces log 033's own `control_domain_only` on all twelve plateaus
it publishes, bound for bound and count for count** *(measured, and
the run asserts it — if it ever stops being true the script stops)*.
That is a positive control on the new machinery, in the same spirit as
log 034's c++ word spellings.

---

## 3 — the four readings compared

Each tree at its own widest non-degenerate plateau — the reading the
data offers rather than one chosen:

| reading | similarity | widest plateau | groups |
|---|---|---|---|
| product (log 035) | J × A | [0.155, 0.185) | 21 |
| agreement only | A | [0.114, 0.189) | 29 |
| containment | C × A | [0.010, 0.077) | 4 |
| domain only | J | [0.060, 0.129) | 2 |

Read on its own that table says little, because the counts are not
comparable. So the readings are also compared at MATCHED GRANULARITY,
which is log 040's decision 51 and is not re-argued here: two trees
are set beside each other cut to the same number of groups. K is 21,
the product tree's own widest plateau, so the comparison stands where
log 035 read the product's headline.

**One tree cannot be cut there.** The agreement tree steps from 25
groups straight to 1 and stands in nothing between *(measured)*. That
is not an inconvenience, it is the first finding of this section: 24
merges in that tree happen at similarity exactly 0.000, so the moment
the threshold drops below the last shred of agreement, everything
falls together at once. The agreement tree is reported at 25.

| reading | groups | same-language rate | same-family rate | one-language groups | largest group | singletons |
|---|---|---|---|---|---|---|
| product | 21 | 0.223 | 0.674 | 9 | 46 | 4 |
| agreement | 25 | 0.090 | 0.256 | 24 | 214 | 24 |
| containment | 21 | 0.128 | 0.703 | 9 | 40 | 5 |
| domain only | 21 | 0.246 | 0.418 | 7 | 46 | 3 |

The same-language rate is, over every pair of leaves a cut puts
together, how often the two are of one language. All measured.

**Does the surprising language-family sorting of the product tree
dissolve under agreement-only? Yes, and it turns out never to have
been the answers' doing.**

The product tree's largest group at 21 is 46 leaves reading php 16,
typescript 8, c++ 6, python 4, ruby 3 — the group log 035 read as a
cross-language equality-and-short-circuit family. Its same-language
rate is 0.223 and its same-family rate is 0.674, so the product tree
sorts strongly by what an operation DOES and moderately by which
language it is in.

The domain-only tree at the same 21 groups sorts by language MORE
strongly than the product does, 0.246 against 0.223, and by family
much less, 0.418 against 0.674 *(measured)*. So the family structure
in the product tree is the answers' contribution and the language
structure is the domains'.

The agreement tree at its own coarsest real cut has a same-language
rate of 0.090 — below both — and a largest group of 214 leaves. **The
answers alone do not separate these operations into language families
or into anything else at the coarse end.** They separate 24 leaves
from the mass and leave the rest together. Every one of those 24 is a
singleton, and they are not a random 24: **sixteen of them are a
short-circuit `&&` or `||`** — java 8, c-sharp 4, rust 3, dart, go,
kotlin and swift 2 each, c++ 1 across the whole set *(measured)*. A
short-circuit operator in a statically checked language accepts truth
values and almost nothing else, so its shared-cell counts fall under
decision 55 against nearly everything, and the agreement tree has too
little to read. They are singletons for want of evidence, not for
disagreeing.

The containment tree is the interesting middle. It keeps the family
sorting at its highest of the four, 0.703, while dropping the language
sorting to 0.128 — the lowest of the three trees that can be cut at 21
*(measured)*. Removing Jaccard's double penalty on a narrow domain
removes most of what was sorting these leaves by language, and what is
left sorts them by what they do. Its groups at 21 are readable in a
way the product's are not: one of 30 spanning c++, c-sharp, dart, go
and java on `^ | || ?? ?: or xor bitor`, one of 12 on `&^ << >> >>>`
across go, java, c++, c-sharp and rust.

**Where do the go.+ / java.+ style pairs land now?** This is the
verbatim table the run prints, and it is the shortest answer to the owner's
ruling:

```
left      right          A      J      C product  cells
go.+      java.+     1.000  0.094  1.000   0.094     88
   product no / agreement yes / containment yes / domain no
go.+      rust.+     0.907  1.000  1.000   0.907    108
   product yes / agreement yes / containment yes / domain yes
go.+      cpp.+      1.000  0.167  1.000   0.167    108
   product no / agreement yes / containment yes / domain no
java.+    cpp.+      0.586  0.220  0.500   0.129    232
   product no / agreement yes / containment yes / domain no
java.+    csharp.+   0.531  1.000  1.000   0.531    527
   product yes / agreement yes / containment yes / domain yes
go.&&     java.&&    1.000  1.000  1.000   1.000      4
   product yes / agreement no / containment yes / domain yes
go.==     java.==    0.986  0.222  0.444   0.219    141
   product yes / agreement yes / containment yes / domain no
go.<<     java.<<    0.688  1.000  1.000   0.688     16
   product yes / agreement no / containment yes / domain yes
```

Read it row by row. `go.+` with `java.+` and `go.+` with `cpp.+` are
apart under the product and under domain-only, and together under both
readings that stop punishing a narrow domain — which is the bias,
caught. `java.+` with `cpp.+` is the control that keeps the readings
honest: C is only 0.500 there and A is only 0.586, so it is a genuine
partial overlap with genuine disagreement, and it stays apart under
the product for a reason the product was right about.

The last two rows are decision 55 doing its job and are worth naming
rather than hiding. `go.&&` against `java.&&` has A of exactly 1.000
and shares **four** input cells. `go.<<` against `java.<<` shares
sixteen. Both fall under the support bar, so the agreement tree
declines to read their rates and places them apart — and the product
tree, which reads every rate however thin, puts them together.
**Decision 55 is therefore not free: it costs two pairs that the
product got right by not asking how much evidence it had.** That cost
is stated here rather than discovered later.

---

## 4 — the dominance analysis

This is the owner's paradigm, built as its own reading and its own visual.

His sketch, verbatim: *"the paradigm could be about the dominant
vectors. if an element is non-zero, what others have that non-zero
element. and for each of those others, what are their non-zero
elements and what others share non-zero elements. does that tree
flatten into a dominant vector."*

Read against this data the sketch is exact. Every signature is a
vector over the 64-cell grid. A cell is non-zero when the operation
accepts it. "What others have that non-zero element" is the set of
operations whose domain also contains that cell. Following that
outward, and outward again, is the containment order. "Does that tree
flatten into a dominant vector" is asking whether that order has a
single top.

The order is built twice, and the two are never mixed. The
CONTAINMENT order consults domains only. The DOMINANCE order is
containment plus never disagreeing, under decision 56, and it is the
CORE's `nests` arm — which the CORE already says IS dominance,
discovered rather than assumed.

### the answer, plainly

**The containment order flattens. The dominance order does not.**

Under containment alone, the whole 238-leaf population has **exactly
one maximal element** *(measured)*. It is a single domain class of all
64 cells, carried by 35 leaves: fifteen php spellings, eight ruby,
six python, typescript's `&&`, `??` and `||`, dart's `==` and `??`,
and kotlin's `?:` *(measured)*. Every other domain in the node sits
inside it. Six of the twelve languages put nothing
in it at all — c++, c-sharp, go, java, rust and swift — and the two
that fill most of it are php and ruby, the open-dispatch languages
that refuse almost no input. So by domains alone the answer to the owner's question is
yes, and the dominant vector is the full grid.

That answer is worth exactly as much as it costs, which is nothing.
The top accepts everything, so containing everything is not a
property it earned. The question only becomes a real one when the
answers are put back, and then it reverses.

**Under the dominance order, 184 of 238 leaves are maximal** — nothing
dominates them *(measured)*. A dominant vector would leave exactly
one. Of the 13,831 ordered pairs that are a strict containment AND
carry enough shared cells to be read, **189 never disagree once**.
That is 1.4 percent *(derived)*. The other 98.6 percent are a wider
domain that does not dominate what it contains, because somewhere
inside it, it answers differently.

So: **the tree does not flatten into a dominant vector.** There is no
operation in these twelve languages that accepts what the others
accept and answers as they answer. The containment top exists and is
not it — the 64-cell class contains every other domain and contradicts
most of them.

### per family

Same question asked six more times, once per operator family:

| family | leaves | domain classes | maximal classes under containment | a single top? | union cells | maximal leaves under dominance | a dominant vector? |
|---|---|---|---|---|---|---|---|
| arithmetic | 59 | 24 | 6 | no | 61 | 46 | NO |
| comparison | 83 | 22 | 1 | yes, 64 cells | 64 | 50 | NO |
| logical | 36 | 6 | 1 | yes, 64 cells | 64 | 36 | NO |
| bitwise | 33 | 10 | 4 | no | 40 | 27 | NO |
| shift | 21 | 7 | 2 | no | 40 | 19 | NO |
| other | 6 | 6 | 1 | yes, 64 cells | 64 | 6 | NO |

All measured. Three families flatten by containment and three do not.
**No family flattens under dominance, and one of them fails as badly
as it is possible to fail**: the logical family has 36 leaves and 36
maximal leaves, so not one logical operation in these twelve languages
dominates another.

The families that fail containment fail it in a readable way.
Arithmetic has 6 maximal classes and its union runs to 61 of 64 cells,
while its widest single domain reaches 38 — so no arithmetic operation
in any of the twelve accepts everything arithmetic is asked to accept
anywhere, and three cells of the grid are refused by every arithmetic
operation in every language *(measured)*. Bitwise and shift both stop
at a union of 40 cells, which is the same ceiling from both, and
neither has a top.

### if there is no single top, what next

the owner's ruling asks three follow-on questions and they are answered in
his order.

**How many maximal elements.** 184 overall, and per family the counts
are the last column above. At the looser 0.99 reading it would be 176
overall, so the strictness of decision 56 is worth eight leaves and no
more *(measured)*.

**What would the union vector look like.** The union of the 184
maximal domains is **64 of 64 cells** — the whole grid *(measured)*.
That is a weaker statement than it sounds and the reason is worth
saying: 35 leaves already carry the whole grid on their own, so the
union is reached by any one of them and the other 183 add nothing to
it. **The union vector is not a new object. It is the grid.** What
would be new is an operation that answers consistently across it, and
that is the next question.

**Which maximal elements agree where they overlap, and which
contradict.** Every pair of maximal elements is scored, and the
verdicts are counted twice — over all pairs, and over pairs within one
family. The within-family count is the readable one: a comparison
operator disagreeing with an arithmetic one is a restatement that they
are different operations, not a finding about either.

| verdict | all pairs | within one family |
|---|---|---|
| union candidate — never disagree | 36 | 31 |
| partial — disagree on some cells | 7,716 | 2,623 |
| fork — disagree on every shared cell | 4,799 | 179 |
| thin — too few shared cells to read | 2,995 | 560 |
| disjoint — share no cell | 1,290 | 34 |

All measured.

**31 union candidates within a family, against 179 forks.** The
candidates are the short list of places where two maximal operations
could be one operation. Ranked cross-language first, because a
same-language pair like `php.&&` with `php.and` is a known positive
control from log 035 rather than news:

| left | right | family | shared cells | agreement |
|---|---|---|---|---|
| `dart.==` | `php.===` | comparison | 64 | 1.000 |
| `cpp.<` | `typescript.<` | comparison | 8 | 1.000 |
| `cpp.>` | `typescript.>` | comparison | 8 | 1.000 |
| `csharp.<` | `typescript.<` | comparison | 5 | 1.000 |
| `csharp.<=` | `typescript.<=` | comparison | 5 | 1.000 |
| `csharp.>` | `typescript.>` | comparison | 5 | 1.000 |
| `csharp.>=` | `typescript.>=` | comparison | 5 | 1.000 |
| `cpp.-` | `csharp.-` | arithmetic | 4 | 1.000 |
| `dart./` | `typescript./` | arithmetic | 4 | 1.000 |
| `java.%` | `kotlin.%` | arithmetic | 4 | 1.000 |

The first row is the one to look at. **`dart.==` and `php.===` agree
on all 64 cells of the grid, both accepting the whole of it** — two
languages that share no runtime, no type discipline and no lineage,
giving the same answer to every question this node knows how to ask
*(measured)*.

The forks are the other side and they are concentrated. The widest are
every pairing of a three-way comparison against an equality:
`dart.==` with `php.<=>`, `php.!=` with `ruby.<=>`, `php.<=>` with
`python.==`, and so on — 64 shared cells and agreement 0.000 in each
*(measured)*. That is log 033's `<=>` contradiction and log 035's
fourth one, re-derived here from a completely different direction:
nothing was told to this analysis about `<=>`, and it fell out as the
node's sharpest fork because a three-way comparison returns an
ordering where an equality returns a truth value.

---

## 5 — the nests and overlaps pairs, from the two trees

The two-tree reading the owner asked for is the agreement tree beside the
domain tree. Where they place a pair differently, that pair is a
nests-or-overlaps case: the two operations answer alike wherever both
answer, and they sit apart only because one accepts more, or the
reverse.

Both trees cut to 21 groups, under decision 51:

| quantity | value |
|---|---|
| pairs the two trees place differently | 20,593 |
| of those, a true domain containment | 13,204 |
| together only in the agreement tree | 20,355 |
| together only in the domain tree | 238 |

All measured. The asymmetry is the shape of the finding: the
agreement tree groups far more freely, because agreement does not care
how wide either domain is.

The top such pairs, cross-language, ordered by agreement and then by
how much evidence stands behind it. Every row has A of exactly 1.000
and a strict domain containment, so every row is a `nests` case in the
CORE's sense:

| narrower | wider | A | J | product | shared input cells | domains |
|---|---|---|---|---|---|---|
| `csharp.!=` | `python.!=` | 1.000 | 0.406 | 0.406 | 322 | 26 in 64 |
| `csharp.==` | `python.==` | 1.000 | 0.406 | 0.406 | 322 | 26 in 64 |
| `csharp.!=` | `typescript.!=` | 1.000 | 0.619 | 0.619 | 310 | 26 in 42 |
| `csharp.!=` | `typescript.!==` | 1.000 | 0.619 | 0.619 | 310 | 26 in 42 |
| `csharp.==` | `typescript.==` | 1.000 | 0.619 | 0.619 | 310 | 26 in 42 |
| `csharp.==` | `typescript.===` | 1.000 | 0.619 | 0.619 | 310 | 26 in 42 |
| `csharp.==` | `dart.==` | 1.000 | 0.406 | 0.406 | 305 | 26 in 64 |
| `cpp.!=` | `python.!=` | 1.000 | 0.312 | 0.312 | 282 | 20 in 64 |
| `cpp.==` | `python.==` | 1.000 | 0.312 | 0.312 | 282 | 20 in 64 |
| `cpp.not_eq` | `python.!=` | 1.000 | 0.312 | 0.312 | 282 | 20 in 64 |
| `cpp.*` | `python.*` | 1.000 | 0.360 | 0.360 | 196 | 9 in 25 |
| `go.==` | `dart.==` | 1.000 | 0.281 | 0.281 | 181 | 18 in 64 |
| `go.!=` | `kotlin.!=` | 1.000 | 0.346 | 0.346 | 181 | 18 in 52 |
| `go.!=` | `php.!==` | 1.000 | 0.281 | 0.281 | 181 | 18 in 64 |
| `go.!=` | `python.!=` | 1.000 | 0.281 | 0.281 | 181 | 18 in 64 |
| `go.!=` | `ruby.!=` | 1.000 | 0.281 | 0.281 | 181 | 18 in 64 |
| `go.==` | `kotlin.==` | 1.000 | 0.346 | 0.346 | 181 | 18 in 52 |
| `go.==` | `php.===` | 1.000 | 0.281 | 0.281 | 181 | 18 in 64 |

All measured. `cpp.not_eq` appearing on that list beside `cpp.!=` is
log 034's positive control turning up again unasked.

The full list, all 13,204 containment cases and the 20,593
disagreements they sit inside, is in `two_tree_disagreement.json`.

One caution belongs with this table. **A `nests` relation here is
measured over the cells the narrower operation accepts and says
nothing about the cells it refuses.** `go.==` agrees with `dart.==` on
all 18 cells go accepts; what go would answer on the other 46 was not
measured, because go refuses to be asked.

---

## 6 — what this implies for the Hub's kind map

**Flagged for the owner. None of this is a ruling and nothing has been
changed on the strength of it.**

1. **A universal operation cannot be read off this data by taking the
   widest domain.** The containment order has a single top and that
   top contradicts most of what it contains. Any kind map built by
   "pick the most permissive and let the others be special cases"
   would be picking a leaf that disagrees with 98.6 percent of what
   sits under it.

2. **The unification short list should probably be the union
   candidates, not the near neighbours.** Log 040 produced a short
   list of 36 pairs by behaviour similarity. This log produces 31
   within-family union candidates by a different criterion —
   containment plus never disagreeing — and the two lists are built
   from different arithmetic. Whether they overlap has not been
   computed and would take one pass.

3. **`dart.==` with `php.===` is the strongest single unification
   candidate this node has produced.** 64 shared cells, agreement
   1.000, two unrelated languages. If the Hub wants one worked example
   of an intention that survives crossing a language boundary intact,
   that pair is it.

4. **The `<=>` fork is structural and a kind map will have to say so.**
   Three-way comparison and equality share the whole grid and agree on
   none of it. They are not two dialects of one intention; they return
   different kinds. Decision 39 already keeps them apart and this
   reading agrees from an independent direction.

5. **Decision 55 has a cost and the Hub should know its size.** Two of
   the eight watched pairs are placed apart in the agreement tree only
   because their evidence is thin — four and sixteen shared cells.
   Where a kind map depends on a thin pair, the honest move is to
   widen the probe space for it, not to lower the bar.

6. **The language sorting in the published tree is the domain factor.**
   Anyone reading `dendrogram_all12.html` as evidence that languages
   cluster by family should read `dendrogram_containment.html` beside
   it, where the language sorting drops from 0.223 to 0.128 and the
   family sorting rises from 0.674 to 0.703.

7. **Constructs and the joint tree were not carried into these
   readings.** The three alternative distances need an agreement rate
   on shared input cells, and `clusters_joint.json` is a domain-only
   artifact — it carries J and no A, because decision 21 built it to
   answer a key-space question. So the alternative readings are
   operators only, 238 leaves, and the joint population is stated as
   not attempted rather than quietly dropped. What it would take: the
   construct answers exist in `construct_answers_<lang>.json`, so an
   agreement rate over the two-slot constructs is one pass.

---

## 7 — products and reproduction

New in `Research/kind_fuzz_clustering/`:

```
l3_alt_readings.py        the three distances,
                          decision 55
clusters_agreement.json   tree 1
clusters_containment.json tree 2
clusters_domain.json      tree 3
two_tree_disagreement.json  the nests list and
                          the matched-granularity
                          comparison
make_dendrogram_alt.py    the three visuals
dendrogram_agreement.html
dendrogram_containment.html
dendrogram_domain.html
l3_dominance.py           decisions 56 and 57
dominance_lattice.json    the whole analysis
make_dominance_lattice.py the fourth visual
dominance_lattice.html
```

Modified: `domstub.js` takes an optional list of element ids to check,
so a page that is not a dendrogram can be validated by the same stub.
**With no such argument it behaves exactly as before**, and
`dendrogram_all12.html` re-validates unchanged.

Nothing else on disk was touched. No existing artifact was rewritten.

Reproduction, in order, all on the host and all under a second each:

```
python3 l3_alt_readings.py
python3 make_dendrogram_alt.py
python3 l3_dominance.py
python3 make_dominance_lattice.py
```

All four visuals validated under the DOM stub, zero throws:

| visual | scripts | threw | panels filled | drawing |
|---|---|---|---|---|
| `dendrogram_agreement.html` | 2 | 0 | 5 | icicle and curve both appended |
| `dendrogram_containment.html` | 2 | 0 | 5 | icicle and curve both appended |
| `dendrogram_domain.html` | 2 | 0 | 5 | icicle and curve both appended |
| `dominance_lattice.html` | 1 | 0 | 6 | lattice appended |

All measured. Each dendrogram's own cluster-count self-check — the one
that warns when the tree walk and the merge history disagree — was
silent on all three.

`hq.sh check`: **0 errors** *(measured, before and after this log)*.
