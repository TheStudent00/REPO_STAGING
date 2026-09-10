# log 040 — the cross-check: declared signatures against measured behavior

Date: 2026-08-20. Node:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`
and `PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/`.

This log closes CHECK item 4j, which was the last open item in the
`kind_fuzz_clustering` node and the oldest unstarted one. It is the
cross-check the node's own opening section promised: the clusters
built from what grammars DECLARE, set against the clusters built from
what compilers and runtimes DO.

**This log will be read cold more often than any other in the node,
because it closes the node.** Nothing below depends on having read
logs 021 to 039. Every term is defined before it is used, and every
number carries where it came from.

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

No probe ran for this log. Nothing was executed and nothing was
compiled. Every number below is read off artifacts that already
existed, or computed from them by two new scripts.

---

## words used in this log

Every short word this log leans on is defined here, with an example
taken from this log's own content rather than a made-up one.

```
the signature source
    the clusters of the
    kind_signature_clustering node.  it reads
    each grammar's node-types.json and builds
    a feature vector per KIND from arity,
    slot types and supertypes.  nothing runs.
    example tied to context:
        the signature source says cpp's `!=`
        and cpp's `+` are one thing, because
        both are the kind
        `binary_expression`.

the behavior source
    the clusters of this node.  it generates
    small programs, runs or checks them, and
    builds a signature per OPERATION from the
    set of inputs accepted and the answer
    returned in each.
    example tied to context:
        the behavior source says cpp's `!=`
        and cpp's `+` disagree on all 232
        input cells they share.

leaf
    one row of a clustering, the thing that
    gets grouped.
    example tied to context:
        `go.+` is a behavior leaf;
        `binary_expression` in go's grammar is
        a signature leaf.

host kind
    the named grammar kind whose declared
    operator slot lists a given operator
    token.  it is how an operator token gets
    a declared signature at all.
    example tied to context:
        the host kind of `rust.+` is rust's
        `binary_expression`.

mapped leaf
    a behavior leaf for which a host kind was
    found, so both sources can see it.
    example tied to context:
        212 of this node's 238 operator leaves
        are mapped.

blind pair
    two mapped leaves whose declared feature
    vectors are IDENTICAL, so the signature
    source cannot tell them apart at all.
    example tied to context:
        `cpp.!=` and `cpp.+` are a blind pair.

matched granularity
    comparing the two trees when each has
    been cut into the SAME number of groups.
    comparing one tree's 21 groups against
    another's 44 would measure the cut and
    not the agreement.
    example tied to context:
        the headline row is both trees cut to
        21 groups.

agreement rate
    over all pairs of mapped leaves, the
    fraction where both sources say the same
    thing: together-and-together, or
    apart-and-apart.
    example tied to context:
        0.8795 for the operators at 21
        groups.

ARI
    the same comparison corrected for the
    agreement two unrelated groupings get by
    luck.  0 means no better than chance, 1
    means identical.  it is quoted BESIDE the
    agreement rate because the agreement rate
    alone rises toward 1 as the cut gets
    finer, for a reason that has nothing to
    do with either source being right.
    example tied to context:
        agreement 0.9856 at 120 groups sits
        with an ARI of 0.0633.

permutation null
    the ARI the same two trees give when one
    side's labels are shuffled at random,
    over 2,000 draws.  it is what "no
    relationship at all" looks like in these
    exact numbers.
    example tied to context:
        the operators' null tops out at
        0.0343 and the measured value is
        0.1193.

type A disagreement
    the signature source says together and
    the behavior source says apart.  the
    LOOKS-alike, BEHAVES-different case.
    example tied to context:
        `cpp.!=` with `cpp.+`.

type B disagreement
    the behavior source says together and the
    signature source says apart.  the
    different-declaration, same-measured-
    intention case.
    example tied to context:
        `php.===` with `python.is`.
```

---

## 1 — the walkthrough, and the verdict

### 1.1 what was set against what

Two clusterings of the same population were built by two nodes that
never shared an input.

`kind_signature_clustering` read 411 grammars' shipped
`node-types.json` files and built one feature vector per kind from
declared arity, declared slot types and declared supertypes — 31,212
kinds, no program ever run *(measured, log 010 and log 014)*.

`kind_fuzz_clustering` — this node — generated programs, ran or
checked them on twelve languages, and built one signature per
operation from the set of input pairs accepted plus the answer
returned in each. Its products are `clusters_all12.json` with **238
operator leaves**, `clusters_constructs.json` with **123 construct
leaves**, and `clusters_joint.json` with **284 leaves** *(measured,
CHECK items 4ff, 5x)*.

### 1.2 the walk, step by step

1. **The two populations were aligned.** The signature source names
   grammar KINDS; the behavior source names `language.operation`. An
   operator token was carried to its host kind by reading the
   grammar's own declaration — this node's phase-0 product
   `legal_pairs_<lang>.json`, which flattens `node-types.json` into
   (host, slot, filler) triples. A construct leaf was carried by its
   role through `construct_catalogue.json`, which resolved role to
   declared kind back in log 036 and was not touched here. The
   decisions are §2, numbered and overturnable.
2. **What could not be carried was counted and named, not dropped.**
   26 of 238 operator leaves and 1 of 123 construct leaves have no
   host kind. They are listed by name in §5.2.
3. **A signature tree was built over exactly the mapped leaves**, not
   cut out of the 31,212-kind tree. Cutting the big tree would have
   given groups shaped by the other 399 grammars.
4. **The two trees were compared at every matched granularity** from 2
   groups to 211, not at one chosen cut. The headline is quoted at the
   behavior tree's OWN widest stability plateau, which is 21 groups
   for the operators and 12 for the constructs *(measured, recorded
   in the artifacts as `stability_plateaus` and `plateaus`)*.
5. **A permutation null was run** so that a weak number can be told
   apart from no number.

### 1.3 the verdict

**The symmetry holds for the operators and fails for the constructs,
and the reason is measured rather than guessed.** Level: measured for
every quantity, derived for the reading placed on them.

- **Operators.** At 21 groups each, the two sources agree on
  **0.8795** of the 22,366 leaf pairs, ARI **+0.1193**. The
  permutation null over 2,000 shuffles has mean 0.0002 and never once
  reached 0.0343. **So the relationship is real and it is weak.** Zero
  of 2,000 draws matched it; the ARI peaks at **+0.1638 at 14 groups**
  and falls away on both sides.
- **Constructs.** At 12 groups each, agreement is **0.6365** and ARI
  is **−0.0057**, against a null whose 95th percentile is 0.0565 and
  whose largest draw was 0.1592. **The p-value is 0.552.** On this
  population the two sources are not distinguishable from unrelated.
- **The cause of the weakness is a resolution gap, and it is
  one-sided.** Over the 212 mapped operator leaves the signature
  source holds exactly **12 distinct feature vectors**, and **not one
  pair of leaves from two different languages has the same one**
  *(measured)*. There are twelve target languages. The signature
  source's whole vocabulary about operators is, in effect, one word
  per language. The behavior source resolves the same 212 leaves into
  **183 distinct signatures** *(measured)*.
- **So the signature source cannot in principle confirm or refute any
  grouping of operators WITHIN a language, and every statement it
  makes ACROSS languages is a statement about how that grammar was
  written.** This is not a defect found in the co-node's work; it is
  what a declared operator slot contains. A grammar declares that
  `binary_expression` has a left, an operator and a right. It does not
  declare that `+` adds.
- **Every single one of the 861 type-A operator disagreements is a
  blindness rather than a contrary claim** *(measured)*: all 861 sit
  at declared distance exactly 0.000000, and all 861 are within one
  language. The signature source never once said "these two are the
  same" about a pair the behavior source split — it said "I cannot see
  a difference".
- **The reverse direction carries real content.** Of the 1,833 type-B
  disagreements, **1,578 cross a language** *(measured)*. These are
  groupings the behavior source found and the declaration cannot
  express.
- **The constructs invert the resolution gap and still do not agree.**
  There the signature source is the FINER of the two: 89 distinct
  declared vectors over 122 mapped leaves against the behavior
  source's 48 *(measured)*. Fine resolution on both sides did not
  produce agreement. That rules out "the signature source is simply
  too coarse" as the whole story and leaves the honest reading: on
  constructs the two sources are measuring different things.
- **Where both sources have resolution and both speak, they agree
  exactly.** The clearest instance is this node's own positive
  control: `cpp.and` and `cpp.&&` sit at declared distance 0.000000
  and at behavior similarity 1.000 over 562 shared cells *(measured,
  CHECK 4gg)*. Agreement, where it can happen, is total.

**Neither source won and neither was wasted.** The signature source
sees 1,728 kinds inside these twelve grammars that no behavior leaf
touches. The behavior source sees 26 operator leaves that these twelve
grammars do not name at all. §5 is that accounting.

---

## 2 — the mapping, as numbered overturnable decisions

Each decision below is a choice that could have gone another way.
Each is stated so that overturning it is a known move rather than a
rediscovery. Continuing this node's numbering, which reached 44.

**Decision 45 — the twelve grammars are named explicitly.** The
signature population is 411 grammars; the behavior population is
twelve languages. The restriction is by an explicit table, not by a
prefix match, because three of the twelve carry a compound grammar
identifier. Overturning it means editing one dictionary.

```
go -> go            rust -> rust
cpp -> cpp          java -> java
kotlin -> kotlin    swift -> swift
dart -> dart        python -> python
ruby -> ruby        csharp -> c-sharp
typescript -> typescript__typescript
php -> php__php
```

Two of these are a CHOICE and not a lookup. `typescript__typescript`
was taken over `typescript__tsx`, and `php__php` over
`php__php_only`, in both cases because it is the grammar for the
ordinary source file the probes were written as. Level: measured that
both variants exist; the choice is a decision.

**Decision 46 — an operator token maps to the kind whose declared
operator slot lists it.** Read off `legal_pairs_<lang>.json`, this
node's own phase-0 product, keeping triples whose slot is named
`operator` or `operators` and whose filler is anonymous. Nothing is
guessed and no kind name is pattern-matched. Overturnable by widening
the accepted slot names.

**Decision 47 — a token declared by more than one host keeps the
whole host set, and the distance between two leaves is the SMALLEST
distance over their host sets.** 58 of the 212 mapped operator leaves
have two or three hosts; `go.+` has `binary_expression` and
`unary_expression`, `cpp.+` has `binary_expression` and
`fold_expression` *(measured)*. The smallest-distance reading matches
the signature node's own published instrument, which is a per-kind
top-counterpart list. Taking the average instead would make a leaf
look less like everything, including itself.

**Decision 48 — a construct leaf maps through the catalogue, never
through its name.** `construct_catalogue.json` already resolved role
to declared kind in log 036 by asking each grammar's own kinds file;
this log reuses that resolution untouched. The only added step is
stripping the operator suffix from an augmented-assignment role, so
that `Kbinding.augassign+=` and `Kbinding.augassign*=` both resolve
through the role `augassign`. Level: measured that both resolve to one
kind in every language that has them; that they SHOULD is the
decision.

**Decision 49 — the signature tree is rebuilt over the mapped leaves
alone.** It is not a cut taken from the 411-grammar tree. Reason: at
any cut of the big tree the groups are shaped by 399 grammars that
have nothing to do with this comparison, so agreement measured against
it would be a measurement of those grammars. The distance function is
the signature node's own weighted-Jaccard, and the linkage is average
linkage, both copied rather than re-invented.

**Decision 50 — the comparison is made at MATCHED cluster counts,
swept, with no cut chosen.** For every k from 2 to 211 both trees are
cut to exactly k groups and compared. The one row promoted to a
headline is the behavior tree's own widest stability plateau, which
was chosen by log 030's sweep and not by this log. This carries the
node's standing no-elbow discipline into the cross-check.

**Decision 51 — the agreement rate is never quoted without the ARI
beside it.** The agreement rate rises toward 1.000 as k rises, because
almost every pair is apart in both trees and both-apart counts as
agreement. §3 shows the two columns diverging, which is the reason for
the rule.

**Decision 52 — a pair the signature source cannot resolve is
recorded as BLIND and not as agreement.** A declared distance of
exactly 0.000000 means the two leaves have byte-identical feature
vectors. §4 keeps those apart from pairs that are merely near.

**Decision 53 — unmappable leaves are named, never dropped
silently.** Both directions: behavior leaves with no host kind (§5.2)
and grammar kinds no behavior leaf reaches (§5.1).

**Decision 54 — the leaf ordering of the behavior artifacts was
verified before it was used, not assumed.** `clusters_all12.json`
records leaf ids in its merge history and member NAMES on each merge.
Rebuilding every merge from the sorted signature order and comparing
against the recorded member lists gives **237 of 237 exact matches,
zero mismatches** *(measured)*. `clusters_constructs.json` records no
member lists, so its ordering rests on its builder's own
`sorted(...)` line and is **unverified by an independent route**. It
is stated as such rather than rounded off.

### 2.1 what the mapping could not carry — the honest count

| direction | population | carried | not carried |
|---|---|---|---|
| behavior to signature | operator leaves | 212 | 26 |
| behavior to signature | construct leaves | 122 | 1 |
| signature to behavior | kinds in the 12 grammars | 120 | 1,728 |

*(measured)*. The 1,728 figure is the count of named kinds in the
twelve grammars that no behavior leaf in this node reaches, and it is
the single largest number in this log.

---

## 3 — the agreement rates

### 3.1 the matched-granularity sweep

Both trees cut to the same number of groups. Operators, 212 mapped
leaves, 22,366 pairs.

| groups | agreement | ARI |
|---|---|---|
| 2 | 0.9011 | −0.0083 |
| 3 | 0.7474 | −0.0082 |
| 5 | 0.5144 | +0.0234 |
| 8 | 0.6487 | +0.0423 |
| 12 | 0.7771 | +0.1150 |
| **14** | **0.8417** | **+0.1638** |
| 20 | 0.8717 | +0.1148 |
| **21** | **0.8795** | **+0.1193** |
| 30 | 0.9239 | +0.1337 |
| 45 | 0.9497 | +0.1268 |
| 60 | 0.9635 | +0.1037 |
| 80 | 0.9722 | +0.0699 |
| 100 | 0.9810 | +0.0706 |
| 120 | 0.9856 | +0.0633 |

*(measured)*. The two bolded rows are the ARI peak and the behavior
tree's widest plateau. **The agreement column and the ARI column point
in opposite directions above 30 groups**, which is decision 51's
reason stated as data: at 120 groups the sources agree on 98.6 percent
of pairs and are less related than they were at 30.

### 3.2 the headline table, by family

Both trees cut to 21 groups for the operators and to 12 for the
constructs — each population at its own behavior-side widest plateau.
**A** counts pairs the signature source puts together and the behavior
source splits. **B** counts the reverse.

| family | leaves | pairs | both together | both apart | A | B | agreement | ARI |
|---|---|---|---|---|---|---|---|---|
| arithmetic | 55 | 1,485 | 52 | 1,144 | 39 | 250 | 0.8054 | +0.1882 |
| comparison | 74 | 2,701 | 81 | 1,796 | 72 | 752 | 0.6949 | +0.0758 |
| logical | 31 | 465 | 22 | 321 | 8 | 114 | 0.7376 | +0.1782 |
| bitwise | 30 | 435 | 28 | 356 | 3 | 48 | 0.8828 | +0.4697 |
| shift | 19 | 171 | 3 | 134 | 0 | 34 | 0.8012 | +0.1215 |
| other | 3 | 3 | 0 | 3 | 0 | 0 | 1.0000 | degenerate |
| **all operators** | **212** | **22,366** | **292** | **19,380** | **861** | **1,833** | **0.8795** | **+0.1193** |
| access | 17 | 136 | 14 | 36 | 77 | 9 | 0.3676 | −0.0334 |
| binding | 54 | 1,431 | 126 | 696 | 448 | 161 | 0.5744 | +0.0345 |
| flow | 51 | 1,275 | 184 | 540 | 99 | 452 | 0.5678 | +0.1346 |
| **all constructs** | **122** | **7,381** | **404** | **4,294** | **1,434** | **1,249** | **0.6365** | −0.0057 |

*(measured)*. Four readings, each stated at its level.

- **Bitwise is the strongest family in the node, ARI +0.4697**
  *(measured)*. Derived cause: the six c++ word spellings and their
  symbol twins are bitwise leaves, they are blind pairs on the
  signature side and identical on the behavior side, so both sources
  put them together for unrelated reasons and both are right.
- **Comparison is the weakest operator family, ARI +0.0758 over the
  largest leaf count** *(measured)*. Derived cause: 752 of its 2,701
  pairs are type B — comparison is where the behavior source found the
  most cross-language grouping, and a declaration has no way to say
  it.
- **Shift has ZERO type-A pairs** *(measured)*. Nothing the signature
  source grouped was split by behavior. It also has only 3
  both-together pairs of 171, so this is a family the signature source
  is nearly silent about rather than one it gets right.
- **Access is the only row where the agreement rate falls below
  one-half, at 0.3676 with a NEGATIVE ARI** *(measured)*. 77 of its
  136 pairs are type A. Access is `subscript`, `member` and `slice`,
  and the grammars declare those three very similarly while the
  measurements separate them hard.

The `other` row is three leaves — `php..`, `python.not in` and
`ruby.=~` — and its ARI of exactly 1.0000 over three pairs is
arithmetic on a degenerate set, not a finding. It is printed rather
than hidden.

### 3.3 the permutation null

| population | measured ARI | null mean | null 95th | null largest of 2,000 | p |
|---|---|---|---|---|---|
| operators, 21 groups | +0.1193 | +0.0002 | 0.0127 | 0.0343 | < 0.0005 |
| constructs, 12 groups | −0.0057 | −0.0003 | 0.0565 | 0.1592 | 0.552 |

*(measured, 2,000 shuffles per population, seed 7)*. Read plainly:
**the operators' agreement is small and certainly there; the
constructs' agreement is absent.**

One instrument note, recorded because it bears on how much weight the
constructs row can carry. Recomputing the constructs comparison from
the distances ROUNDED to six decimal places moves its ARI from −0.0057
to +0.0079 *(measured)*. Average linkage breaks ties by input order,
and the construct distances carry many ties. The operators' figure is
not sensitive in this way. **So the constructs' number should be read
as "zero, and unstable near zero", never as a negative value with a
meaning.**

---

## 4 — the disagreements, chased

Three classes, kept apart. Type A and type B are findings. The third
class is the mapping's own fault and is counted separately so that it
never inflates either.

### 4.1 type A — looks alike, behaves differently

**861 pairs at the headline cut, and all 861 are blind pairs**
*(measured)*: declared distance exactly 0.000000, both leaves in one
language. There is not a single type-A pair in the operator population
where the signature source made a positive claim of sameness about two
things it could tell apart.

#### worked example — `cpp.!=` against `cpp.+`

What the signature source holds. Both tokens are declared in the
operator slot of two c++ kinds, `binary_expression` and
`fold_expression`. Both leaves therefore carry the same host set and
the same feature vector, whose opening entries are

```
in:left:pos:left            1.0
in:left:sup:expression      1.0
in:operator:tok             1.0
in:right:sup:expression     1.0
```

Declared distance **0.000000** *(measured)*. The grammar says: a left
expression, an operator token, a right expression. It says the same
thing about both, because it is the same sentence.

What the behavior source holds. The two leaves share **232 input
cells**. Similarity **0.0000**, domain Jaccard 0.357143, and answer
agreement **0.0000** — they disagree on every single shared cell
*(measured, `clusters_all12.json` edge `cpp.!= :: cpp.+`)*. Four of
the ten shared domain cells, with the answer classes each returned:

```
fractional|fractional
  !=  truth:true, truth:false
  +   fractional:nan, fractional:inf,
      fractional:4.641592653589793
text|text
  !=  truth:true, truth:false
  +   text:68656c6c6f,
      sequence:[104,101,108,108,111]
```

**The chase, and the cause.** No harness fault is involved and neither
source is wrong. `!=` returns a truth value and `+` returns a value of
the operand's own kind. c++'s grammar has no slot in which to write
that down, because a return type is not a declared feature of a
tree-sitter node. **This is the LOOKS-alike, BEHAVES-different case in
its purest available form: identical declaration, total behavioral
contradiction, and the declaration is not lying — it is silent.**

Level: measured for both sides' numbers; derived for the cause, which
follows from the answer classes rather than from reading a compiler.

### 4.2 type B — different declaration, same measured intention

**1,833 pairs at the headline cut, 1,578 of them crossing a language**
*(measured)*. **36 of the 1,833 sit at behavior similarity 0.999 or
better** — the behavior source calls them the same thing outright.
These are the Hub's unification candidates.

#### worked example — `php.===` against `python.is`

What the signature source holds. php declares `===` in the operator
slot of `binary_expression`; python declares `is` in the operator slot
of `comparison_operator`. The two kinds are genuinely different
declarations, not two names for one shape: php's vector opens on a
right slot admitting eleven positions, python's on an anonymous
multiple-child spec.

```
php  binary_expression
  in:right:pos:alternative  1.0
  in:right:pos:name         1.0
  in:operator:tok           1.0
python  comparison_operator
  anon:mult                 1.0
  in:anon:sup:expression    0.5
  has_subnode_spec          1.0
```

Declared distance **0.669421** *(measured)* — **the largest declared
distance of any pair in the node that the behavior source calls
identical.**

What the behavior source holds. **1,156 shared input cells, domain
Jaccard 1.000, answer agreement 0.999135, similarity 0.999135**
*(measured)*. Both accept every one of the 64 form pairs. Both answer
`truth:false` on `fractional|keyed`, `fractional|nesting` and
`fractional|nothing`. The 0.000865 shortfall is python raising where
php answers, and it is confined to python's own overflow and value
errors, which decision 31 already rules an answer class.

**The chase, and the cause.** Two languages spell identity comparison
differently, put it under differently shaped grammar nodes, and mean
the same operation. **The declaration cannot express the sameness and
the measurement finds it without being told.** This pair is the case
for the behavior source existing at all.

Level: measured throughout. Whether the pair should be UNIFIED in the
Hub's kind map is a ruling and is flagged in §6.4, not taken here.

### 4.3 artifacts of the mapping — named as such, counted apart

These are not findings about either source's clusters. They are places
where the alignment of §2 could not carry a leaf across, and they are
listed so that nobody counts them as disagreement.

- **dart's seventeen operator leaves have no host kind at all.**
  dart's grammar declares an `operator` slot only on
  `assignment_expression` and `assignment_expression_without_cascade`,
  and every filler in it is an assignment spelling *(measured)*.
  dart's `+`, `<`, `==`, `<<` and their kin are not named anywhere in
  `node-types.json`. **Not a gap in this mapping and not a gap in the
  behavior data — a limit of what tree-sitter node types expose**,
  which is the same limit decision 43 already met and recorded from
  the other side in log 034.
- **swift's six operator leaves, likewise.** swift's grammar declares
  **no anonymous filler in any operator slot whatsoever** *(measured)*
  — swift spells operators through `custom_operator`, which log 028
  already recorded as the largest known gap in the behavior picture.
  Here it becomes a gap in the signature picture too, which is worth
  saying plainly: **the one language where both sources are weakest is
  the same language.**
- **`kotlin...`, `kotlin.in` and `rust...`** — three tokens the
  behavior source measured through decision 43's word-operator
  criterion or through a range spelling, and which their grammars do
  not carry in an operator slot.
- **`swift.Kaccess.subscript`** — the catalogue resolves it to the
  kind `subscript`, which is not in the signature source's clusterable
  population. One leaf.

Total: **26 operator leaves and 1 construct leaf**, out of 361. Level:
measured. **None of these 27 appear anywhere in §3 or in the A and B
counts.**

---

## 5 — what each source sees that the other cannot

### 5.1 what only the signature source sees

**1,728 named kinds inside these twelve grammars that no behavior leaf
in this node touches** *(measured)*, against the 120 kinds the mapping
reaches.

| grammar | kinds reached | kinds not reached |
|---|---|---|
| cpp | 13 | 210 |
| dart | 7 | 212 |
| csharp | 10 | 209 |
| typescript | 12 | 164 |
| rust | 9 | 154 |
| php | 12 | 145 |
| java | 8 | 134 |
| ruby | 13 | 121 |
| python | 15 | 107 |
| kotlin | 9 | 105 |
| go | 7 | 100 |
| swift | 5 | 67 |

*(measured)*. These are declarations, type expressions, imports,
literals, parameter lists, class bodies, generics — everything a
program is made of that is not an operator applied to two values or
one of twelve construct roles. **The behavior source has no leaf for
any of them and this node never claimed one.** Beyond that, the
signature source covers 411 grammars against this node's 12, and it
needs no compiler, no runtime and no probe — it read the whole
ecosystem in one pass.

### 5.2 what only the behavior source sees

- **26 operator leaves that these grammars do not name** — dart's 17,
  swift's 6, `kotlin...`, `kotlin.in`, `rust...` *(measured, §4.3)*.
  Every one of them has a measured domain and measured answers.
- **The distinctions inside a kind.** 183 distinct behavior signatures
  against 12 distinct declared vectors, over the same 212 leaves
  *(measured)*. Everything the node found about `+` splitting into
  four families, about the eleven-member shift group, about
  `dart./` sitting on `typescript./` at similarity 1.000 — none of it
  is expressible in the signature source's vocabulary. Not
  contradicted by it. **Not expressible in it.**
- **Answers at all.** A declaration has no field for what an operation
  returns. Every finding in this node that turns on a returned value —
  the integer-overflow fracture, the truthiness table, the
  index-against-value split in go's `for` — lives entirely outside
  what the signature source can hold.
- **Refusal as a result.** Which pairs a compiler REJECTS is measured
  here and declared nowhere.

### 5.3 the one thing both see, and it agrees exactly

Where both sources have resolution on the same pair, they have never
disagreed. The instance on record is this node's positive control:
c++'s six word spellings against their symbol twins, blind pairs on
the signature side and **similarity 1.000, Jaccard 1.000, agreement
1.000, 0 disagreements of 8,526 shared cells** on the behavior side
*(measured, CHECK 4gg)*. Level: measured. **It is one instance, not a
rate, and it is quoted as one.**

---

## 6 — the node's closing statement

### 6.1 what kind_fuzz_clustering set out to do

The CORE's definition, verbatim:

> **Cluster KINDS by measured behavior, using an automated fuzzer.**

and the method the owner stated the same day, verbatim:

> "i was thinking about establishing the basic data structures so
> that we can fuzz the rest of the vocabulary. without having to
> have a corpus. we generate the scripts based on vocab tokens
> (that we know what it wants for input and its output type) in
> order to observe how it processes data structures. and then use
> those changes to cluster across languages."

### 6.2 what it measured

The campaign's own recorded totals, each read off the CHECK item that
booked it. They are listed rather than summed, because the passes
overlap and two of them supersede earlier passes.

| pass | probes | CHECK |
|---|---|---|
| acceptance, routes A1 and A2 | 71,313 | 3e |
| acceptance, route C, three languages | 818,913 | 3e-C |
| java and typescript route A1 | 32,647 | 3f |
| full value matrix, nine languages | 2,221,643 | 3g |
| execution answers, nine languages | 170,419 | 3k |
| swift retaken, full compiler | 76,614 | 4z |
| constructs, holder grain | 21,342 | 5e to 5l |
| constructs, value grain | 481,978 | 5t |

*(measured)*. Twelve languages. Every lane passing a completeness
gate that this node had to build twice, and that caught six lanes
which exited zero while measuring nothing or measuring the wrong
question.

### 6.3 what stands proven

Stated with levels, and only what this log's own work or a closed
CHECK item supports.

1. **The two evidence sources are mutually confirming on operators and
   mutually silent on constructs.** Measured: ARI +0.1193 against a
   null that never reached 0.0343, and ARI −0.0057 at p 0.552.
2. **The declared-signature source carries no operation-grain
   information about operators.** Measured: 12 distinct declared
   vectors over 212 leaves, zero of them shared across two languages.
3. **Every disagreement in which the declaration says "same" is a
   blindness, not a contrary claim.** Measured: 861 of 861 at declared
   distance exactly zero.
4. **The behavior source found 1,578 cross-language groupings the
   declaration has no way to state, 36 of them at similarity 0.999 or
   better.** Measured.
5. **Neither source subsumes the other.** Measured: 1,728 kinds only
   the declaration reaches; 26 operator leaves only the measurement
   reaches.
6. **The CORE's claim that disagreement is itself the finding is
   upheld, and the finding is sharper than the CORE anticipated.** The
   CORE expected "a kind that LOOKS like its counterpart but behaves
   differently". Measured, every such kind in this population is a
   kind the declaration could not look at.

### 6.4 what transfers to the Hub's kind map

Carried forward as material, not as rulings.

- **The behavior source is the operation-grain authority.** It is the
  only one of the two with resolution at that grain.
- **The declared-signature source is a language-shape reading.** Its
  twelve vectors describe twelve grammar-writing styles. That is
  useful and it is not a kind map.
- **The 36 near-identical cross-language pairs are the unification
  short list**, headed by `php.===` with `python.is` and
  `php.!==` with `python.is not`, and including the four
  short-circuit pairs `csharp.&&` with each of `go.&&`, `kotlin.&&`,
  `rust.&&` and `java.&&`, plus the same four for `||`.
- **Two languages are weak on both sources at once, dart and swift**,
  and any kind map should carry that as a stated confidence gap rather
  than discover it later.

### 6.5 flagged for the owner, not taken

1. **Node status.** `CORE_0_3_2` reads `status: draft`. With 4j closed
   the node has no open CHECK item except 4nn, which is a recorded
   presentation fault in two display fields of one artifact and not a
   measurement fault. **Whether the node moves off draft is the owner's
   call.** It has not been changed.
2. **Whether the 36 unification candidates become one intention
   each** in the Hub's vocabulary. This log lists them; it does not
   unify anything.
3. **Whether the constructs' non-result warrants a different
   comparison** — for instance against the signature source's
   supertype structure rather than its feature vectors — or whether it
   is simply the answer.
4. **Whether the signature source should be re-run at operator grain
   at all.** It cannot be, from `node-types.json` alone; it would need
   a different grammar input. Recording the question so it is not
   rediscovered.

---

## 7 — products and reproduction

New in `Research/kind_fuzz_clustering/`:

```
xcheck_signature.py    the mapping, decisions 45-48
xcheck_mapping.json    its product, with the
                       unmapped lists by name
xcheck_compare.py      the trees, the sweep, the
                       null, decisions 49-54
xcheck_signature.json  the whole comparison
xcheck_sigdist_operators.json
xcheck_sigdist_constructs.json
```

Nothing in either node's existing artifacts was modified. Both scripts
run in under two seconds on the host and read only files already on
disk. Reproduction is `python3 xcheck_signature.py` then
`python3 xcheck_compare.py`.

`hq.sh check`: **0 errors** *(measured, before and after this log)*.
