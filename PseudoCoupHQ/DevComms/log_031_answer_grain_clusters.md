# log 031 — layer 3 phase 4: the answer-grain clusters

Date: 2026-08-19. Node:
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PseudoCoupHQ/Research/kind_fuzz_clustering/`.

**Rewritten 2026-08-19 for readability at the owner's instruction. The content
is identical — same facts, same numbers, same findings, same section
numbers. Only the prose was rebuilt.**

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

Log 031 was free when this was written.

the owner's instruction for this pass, verbatim: *"i want to see it cluster
the actual computed values."*

---

## words used in this log

This node has built up a set of short words for its own parts. Every
one of them is defined here, with an example taken from this log rather
than a made-up one. Nothing below this block uses a word that is not
either ordinary English or defined here.

```
probe
    one small generated program that asks one
    language one question: apply one operation
    to one pair of loaded values.
    example tied to context:
        this pass reads 818,913 route-C
        probes across python, ruby and php.

lane
    one batch job. it runs a planned set of
    probes and writes its output to one raw
    text file.
    example tied to context:
        the two commands in §7 that reproduce
        this pass touch no lane at all; they
        only re-read output already on disk.

route C
    the way the three directly-run languages
    are measured. a route-C language is run
    rather than compiled, so whether it
    accepts a probe and what it answers
    arrive together in one go.
    example tied to context:
        python, ruby and php are the three
        route-C languages, and they are the
        only three that have answers for this
        pass to cluster.

form
    one of the eight kinds of content every
    language in this node carries: nothing,
    truth, whole number, fractional number,
    text, sequence, keyed grouping, and
    identity marks.
    example tied to context:
        `text` and `sequence` are two forms;
        §5.4 compares `+` on one against `+`
        on the other.

holder
    the typed slot a value is put into before
    an operation is applied to it. one form
    usually has several holders.
    example tied to context:
        python's `Decimal`, python's
        `Fraction` and python's `ctypes.c_int64`
        are three holders; §5.1 turns on the
        third one answering differently from
        the others.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        `i64max`, `negzero`, `nan` and
        `eacute` are value classes, and the
        three languages spell them
        identically.

input cell (also: cell)
    the tuple (operation, form on the left,
    value class on the left, form on the
    right, value class on the right). it
    means the same input in every language
    that has it. this is decision 18.
    example tied to context:
        `+ whole|i64max | whole|base_42` is
        one input cell, and §5.1 shows the
        three languages' answers to it.

answer class
    the kind and value an operation returned
    on a cell, written as kind:value.
    example tied to context:
        `whole:9223372036854775849` is an
        answer class: a whole number with that
        printed value. `truth:false` is
        another.

canonical token
    the single written form an answer class is
    reduced to, so that two languages printing
    the same result in different ways can be
    told to be the same result.
    example tied to context:
        php prints false as the empty string
        and python prints it as `False`; both
        become the canonical token
        `truth:false`.

canonicalization
    the act of reducing a raw printed answer
    to its canonical token, under the numbered
    rules of §2.2. the raw string is kept
    beside the token and never replaced by it.
    example tied to context:
        617 canonical tokens in this pass have
        more than one pre-canonical spelling.

the answer alphabet (`answer_alphabet`)
    the stored table listing every canonical
    token beside every raw string that was
    folded into it.
    example tied to context:
        because the alphabet is stored, any
        canonicalization rule in §2.2 can be
        overturned by re-reading the alphabet
        rather than by re-running the probes.

the answer-grain signature (also: signature)
    everything recorded about one operation of
    one language: which form pairs it accepts,
    and, for each accepted cell, its answer
    classes.
    example tied to context:
        there are 73 signatures in this pass,
        and 69 of them survive to be
        clustered.

domain
    the set of cells an operation actually
    accepted. cells it refused are not in its
    domain.
    example tied to context:
        `python.@` has an empty domain, so
        decision 4 excludes it from the
        clustering.

leaf
    one operation of one language, once it has
    answers to cluster with. leaves are the
    things the clustering arranges.
    example tied to context:
        `php.&&` and `ruby.&&` are two leaves,
        and §5.2 is about how far apart they
        turned out to be.

Jaccard (J), agreement (A), similarity
    three numbers on the closeness between two
    leaves. Jaccard is how much their two
    domains overlap. agreement is the share of
    the cells they both accept on which their
    answers meet. similarity combines the two.
    example tied to context:
        the median agreement across the edges
        of this pass is 0.0337.

the distance rule
    the chosen way of turning Jaccard and
    agreement into one closeness number. here
    it is the product, and it is decision 27.
    example tied to context:
        the sum form and the min form are the
        two rivals to it, and both are
        computable from the stored J and A.

edge
    the measured closeness between two leaves.
    example tied to context:
        this pass has 2,346 edges, of which
        2,290 carry an agreement value.

clustering
    the arrangement built from the edges: it
    repeatedly joins the two closest groups of
    leaves until one group is left. the
    joining rule here is average linkage,
    which measures two groups by the average
    closeness across all pairs between them.
    example tied to context:
        the clustering is run to a single
        root and no cut is chosen; the
        clusters at any threshold are read
        off the recorded merge history.

threshold sweep (also: sweep), plateau
    the sweep is the cluster count read at
    every threshold from 0 to 1. a plateau is
    a run of thresholds over which that count
    does not change, and a wide plateau means
    the reading is stable.
    example tied to context:
        [0.601, 0.700) is the widest
        non-degenerate plateau of this pass
        and it holds 45 clusters.

the domain-only control
    the same 69 leaves clustered again on
    Jaccard alone, with the answers left out,
    so that what the answers contributed can
    be shown rather than asserted.
    example tied to context:
        the control gives 25 distinct classes
        at threshold 1.000 where the answers
        give 68.

uniform, split (decision 26's split marker)
    a cell's answer is the SET of tokens its
    several holders produced. the set is
    marked `uniform` when it has one element
    and `split` when it has more.
    example tied to context:
        `+ whole|u64max | whole|base_42` is
        split in python, because its fixed
        width holder answers 41 where its
        ordinary integer answers a bignum.

opaque token
    the token given to a raw answer the rules
    cannot read. it equals only a byte
    identical raw.
    example tied to context:
        1,730 of 255,715 answers are opaque,
        which is 0.68 percent.

`#trunc`
    the mark on an answer that hit the
    harness's 120-character printing cap.
    it never compares equal to an untruncated
    token.
    example tied to context:
        633 answers in this pass carry it.

VOID
    a mark put on a measurement that was taken
    wrongly, so that it is kept on the record
    but not used. a VOID row is not a leaf.
    example tied to context:
        php's `and`, `or` and `xor` are VOID
        here under decision 30, because the
        probe line recorded the left operand
        instead of the result.

contradicts
    the third arm of the CORE's trichotomy of
    relations between two operations: same
    input, different answer. the other two
    arms are `nests` and `overlaps`.
    example tied to context:
        this is the first pass that can test
        it, because it is the first pass that
        holds answers rather than only
        acceptance verdicts.

decision <n>
    a numbered ruling this node has made, kept
    so it can be overturned by number.
    example tied to context:
        decisions 1 to 17 were made in earlier
        logs; this log makes 18 to 30.
```

---

## what came before this log, restated

Each fact this log borrows from an earlier log is stated here in full,
so no sentence below depends on opening another file.

- **Log 024 measured python alone, and its §5.1 recorded a
  contradiction inside one language.** `Decimal(42) + Fraction(42)`
  raises a TypeError, although both holders hold exactly 42, both add
  to a plain 42, and the two compare EQUAL to each other. Two holders
  of one form can be arithmetically incompatible.
- **Log 024 §5.5 measured `python.@` as a token with nothing behind
  it.** Matrix multiplication is on python's operator menu and 0 of its
  327 probes answered, so its domain is empty.
- **Log 029 froze the twelve manifests and published a preliminary
  clustering on domains alone.** A manifest is the frozen list of what
  was probed for one language: its holders, its value classes, its
  operation list. The three route-C manifests count 342,225 python
  probes, 261,382 ruby and 215,306 php.
- **Log 029's decision 1 is the holder-to-form projection.** Two
  languages do not share holders, so each holder is replaced by its
  form, and a domain becomes a set of ordered FORM pairs. All twelve
  languages carry all eight forms, so the shared space is the same 64
  ordered pairs for every language pair.
- **Log 029's decision 3 is the route-C domain rule.** For python, ruby
  and php, acceptance is not a separate verdict, so a cell counts as
  accepted only if at least one probe returned an ANSWER.
- **Log 029's decision 4 sets the domain-grain similarity and excludes
  empty domains.** Similarity there is Jaccard over the 64 accept
  cells, and an operation with an empty domain is excluded from the
  clustering entirely rather than scored 0 against everything.
- **Log 030 closed the acceptance-grain arc over all twelve
  languages.** It ran 233 operation signatures, of which 229 had a
  non-empty domain.
- **Log 030's decision 12 was an instrument fault, found and
  repaired.** The dart lane marked a probe REFUSED whenever its
  filename appeared anywhere in `dart analyze` output at any severity,
  so a `dead_code` WARNING on `true || b` was recorded as a
  language-level refusal. Restricting to severity ERROR moved 50,381 of
  217,073 dart probes from REFUSE to ACCEPT and moved zero the other
  way.
- **Log 030's decision 14 set the clustering machinery.** Average
  linkage is run to a single root, the full merge history is recorded,
  the cluster count at any threshold is read exactly off that history,
  and **no cut is chosen**. Its own curve was smooth with no elbow.
- **Log 030's §5 measured `contradicts` as zero and said the zero meant
  nothing.** Its relation counts were nested_by 937, equals 718, nests
  693, overlaps 582 and contradicts 0. It then recorded that the CORE
  defines `contradicts` at the ANSWER grain — same input, different
  answer — so an acceptance-grain zero says nothing about the CORE's
  definition, because two languages can both accept `1 + true` and then
  compute different things.
- **An `equals` edge in log 030 meant identical accept sets over the 64
  form-pair cells.** `php.&&` and `ruby.&&` were `equals` there,
  because both languages accept everything.
- **Log 030's shift finding was that shifts do not cluster on their
  own.** The largest cluster made of shift spellings alone, at any
  threshold, is two — `csharp.<<` with `csharp.>>`. What looked like
  shift cohesion in log 029 was the bitwise operations carrying them.
- **Log 030 left decisions 1 to 17 standing.** This log adds 18 to 30
  and changes none of the earlier ones.

---

## §1 — walkthrough, in plain words

Logs 029 and 030 clustered operations on their **domains** — which
ordered pairs of forms an operation will accept. Log 030's own §5
recorded what that could not reach. The CORE defines `contradicts` at
the **answer** grain, meaning same input and different answer. An
acceptance verdict cannot see that, because two languages can both
accept `1 + true` and then compute different things. Log 030 measured
**zero** contradictions, and said plainly that a zero at acceptance
grain says nothing about the CORE's definition.

This pass reads the computed values instead. Three languages have them
— python, ruby and php, **818,913 route-C probes carrying 255,715
answers** *(measured)*.

**The headline is that the answers take three languages that acceptance
could not tell apart and split them into forty-five.** The two readings
of the same 69 leaves stand against each other like this.

- **Domains alone, the control.** The 69 operations collapse into one
  cluster of 68 with `ruby.=~` alone beside it, over the widest stable
  band [0.095, 0.194) *(measured)*.
- **Domains and answers together.** The same leaves give **45 clusters
  over the widest band [0.601, 0.700)**, and **68 distinct classes at
  threshold 1.000 against the domains' 25** *(measured)*.

That is not a defect of the earlier method. It is what open dispatch
looks like from the acceptance side, where almost everything typechecks
because nothing is checked until it runs. Level **derived** for the
reading: the acceptance grain was not weakly separating these three
languages, it was barely separating them at all, and the answers carry
essentially the whole signal.

**The second finding is what the answers re-sort the logical operators
into, and it cuts across the spellings.** At the 45-cluster reading the
two groups are these.

- **The operators that return an OPERAND.** `python.and` sits with
  `ruby.&&`, and `python.or` sits with `ruby.||` *(measured)*.
- **The operators that return a BOOLEAN.** `php.&&` and `php.||` sit in
  a cluster of nine with `php.!=`, `php.<`, `php.<=`, `python.!=`,
  `python.is not` and `ruby.!=` *(measured)*.

Spelling put `php.&&` with `ruby.&&`. The answers put it with the
comparisons instead. Level **derived** for the naming, measured for the
memberships.

**And the third arm of the CORE's trichotomy is now tested, and it
answers with a rate rather than a yes.** The scan is restricted, as log
030's relations were, to the same operation spelled in two languages.
There are **55 such language pairs sharing 19,090 input cells**
*(measured)*. **Not one of them disagrees on every shared cell —
`contradicts_total` is zero. Forty-four of the fifty-five disagree on
SOME cell** *(measured)*. `php.||` against `ruby.||` disagrees on
**1,118 of 1,156 shared cells, 96.7 percent**, and `php.+` against
`python.+` on **190 of 365, 52.0 percent** *(measured)*. So
`contradicts` as the CORE spells it — a boolean — does not fit what the
measurement found. What the measurement found is a **disagreement rate
per cell**, and eleven same-spelling pairs sit at rate zero, meaning
perfect agreement everywhere both accept.

**One instrument fault fell out of the pass without being looked for,
and it is the same shape as log 030's dart lint.** php's `and`, `or`
and `xor` bind LOOSER than assignment, so the harness's
`$__r = ($a) $op ($b);` parses as `($__r = ($a)) and ($b)` and every
recorded answer is the LEFT OPERAND — **6,241 answer cells, the left
operand in all of them** *(measured)*. The acceptance passes could not
have seen it, because a wrong answer is still an ACCEPT. Those three
signatures are VOID (decision 30), excluded from the clustering, and
kept in the artifact with the diagnosis. The contrast with php's symbol
spellings matters and is the reason the §5.2 finding stands.

- **php's word-spelled logicals `and`, `or` and `xor`.** They bind
  looser than `=`, so their recorded answers are worthless and the rows
  are VOID.
- **php's symbol-spelled logicals `&&` and `||`.** They bind tighter
  than `=` and are unaffected, so their disagreement with ruby in §5.2
  is real.

The known fractures, read from the answer side, mostly did NOT
fracture. `2^53+1`, `-0.0`, NaN and the e-acute all come back in
agreement once the three printers are canonicalised. **The one that
does fracture is integer overflow: php answers `9.2233720368548E+18`
where python and ruby both answer `9223372036854775849`** *(measured)*.
That is one language leaving the integers and two staying in them, on
the same input. It is the cleanest answer-grain contradiction in the
pass.

---

## §2 — building the answer classes, and every canonicalization

Each route-C cell is the string `TYPE:VALUE` — the language's own type
name and the language's own printing. Nothing is normalised at read
time. The canonical token is stored BESIDE the raw string, never in
place of it, so every rule below is overturned by a re-read of
`answer_alphabet` and not by a re-run.

### 2.1 what makes "the same input" a measurable thing

- the three route-C manifests use **ONE value-class vocabulary** —
  `base_42`, `i64max`, `p53_plus1`, `negzero`, `nan`, `eacute` and the
  rest are spelled identically in all three, and the pass CHECKS this
  rather than assuming it: `value_class_vocabulary_identical` is
  **true** *(measured)*.
- so an **input cell** is the tuple
  `(operation, form_a, value_class_a, form_b, value_class_b)`, and it
  means the same input in every language that has it. Decision 18.
- **42,881 input cells carry at least one answer** — python 11,444,
  ruby 11,102, php 20,335 *(measured)*.

### 2.2 the canonicalization decisions, numbered

Decisions 1 to 17 stand where log 030 left them. These are 18 to 30 and
are carried verbatim in `clusters_answers.json`. Three of them MERGE
answers across languages — 20, 21 and 24 — and those are the ones to
read first, because a merge is where a difference can be smoothed away
silently and none of these is silent.

| n | rule | what it merges | reversible by |
|---|---|---|---|
| 18 | input cell = (op, form, value class, form, value class) | nothing | — |
| 19 | the result is (runtime type, printed value), both kept raw | nothing | — |
| 20 | booleans canonicalised | `boolean:` / `bool:False` / `FalseClass:false` | `answer_alphabet` |
| 21 | exactness wrappers unwrapped, kind taken from the value | `Decimal(42)` / `Fraction(42, 1)` / `(42/1)` / `42` | `answer_alphabet` |
| 22 | floats compared at 14 significant digits | php's lossy echo against python's repr | `answer_alphabet` |
| 23 | signed zero, NaN, infinity preserved | nothing — it SPLITS | — |
| 24 | text canonicalised to its bytes | `'é'` / `b'\xc3\xa9'` / `"\xC3\xA9"` | `answer_alphabet` |
| 25 | containers on printed body, whitespace and quotes normalised | `[1, 2]` with `[1,2]` | `answer_alphabet` |
| 26 | holder-to-form answer projection, existential + split marker | holders of one form | `input_cells_split` |
| 27 | distance = Jaccard × agreement rate | nothing | stored J and A |
| 28 | the harness truncates at 120 characters | nothing — it SPLITS | — |
| 29 | three serialisers, ruby object addresses rewritten | `0x00007ee8…` to `0xADDR` | `answer_alphabet` |
| 30 | php `and` / `or` / `xor` are VOID | nothing — it REMOVES | `void_signatures` |

- **decision 20 is the most load-bearing one and php forces it.** php's
  harness printed booleans through echo, so php false is the EMPTY
  STRING and php true is `1`. Without the merge the three languages
  would disagree on every comparison operator in the pass. It is also
  the merge with the least doubt attached: no other value in php prints
  as the empty string with type `boolean` *(measured, from the
  alphabet)*.
- **decision 21 refuses the loose reading in the other direction.** The
  two directions are these.
    - **What it merges.** `Decimal(42)` and `42` merge, because the
      wrapper is a HOLDER fact.
    - **What it refuses to merge.** `whole:42` and `fractional:42.0` do
      NOT merge, because an operation that answers 42 and one that
      answers 42.0 made different decisions. And `text:3834` — the
      string `"84"` — never equals `whole:84`. The kind is part of the
      answer.
- **decision 22 is a recorded LOSS, not a finding.** php echoed
  `9.2233720368548E+18` where python's repr gives
  `9.223372036854776e+18`. php's default `precision` is 14, so php's
  float answers carry 14 significant digits and no more. Comparing at
  17 would report the INSTRUMENT as a disagreement — exactly log 030
  decision 12's dart fault in a new costume, where a tool's own
  reporting was read as a language's verdict. The cost: **any genuine
  php-versus-python float difference below the 15th digit is invisible
  to this pass.**
- **decision 26 is PROPOSED AND FLAGGED FOR DEE.** A form has several
  holders and they can answer differently, so a cell's answer is the
  SET of tokens over holder pairs, marked `uniform` at one element and
  `split` above. Two languages agree when their sets INTERSECT. The
  rate the rule is hiding is reported rather than buried: **python
  splits on 2,475 of 11,444 input cells (21.6 percent), ruby 2,773 of
  11,102 (25.0), php 6,121 of 20,335 (30.1)** *(measured, derived
  percentages)*. The universal alternative — agree only if the sets are
  EQUAL — is computable from the same stored sets.

### 2.3 what the canonicalization actually did

- **617 canonical tokens have more than one pre-canonical spelling**
  *(measured)*, and the artifact lists each with its pre-canonical
  forms, its languages and its probe count. The four biggest merges,
  verbatim from `canon_merges`:

| canonical token | pre-canonical spellings | probes | languages |
|---|---|---|---|
| `truth:false` | 3 | 79,350 | py, rb, php |
| `truth:true` | 3 | 76,954 | py, rb, php |
| `nothing:null` | 3 | 7,779 | py, rb, php |
| `whole:0` | 7 | 5,971 | py, rb, php |

- **what stayed unparsable is small and is kept as itself.** Anything
  the rules cannot read becomes `opaque:<raw>`, which equals only an
  identical raw: **python 1,276 answers, ruby 434, php 20 — 1,730 of
  255,715, 0.68 percent** *(measured, derived percentage)*.
- **633 answers were at the 120-character cap** — python 175, ruby 438,
  php 20 *(measured)* — and carry `#trunc`, which never compares equal
  to an untruncated token.

---

## §3 — the answer-grain signature, and the distance rule

The 64-cell form-pair vector of decision 1 is kept, and each accepted
cell now carries its answer class beside its accept bit.

- per accepted form-pair cell the signature records the **token count**,
  the **shape** (`uniform` or `split`), the **answer kinds** present
  ordered by frequency, and the **top four canonical tokens**.
- underneath the 64 cells the signature keeps the full input-cell map.
  That map is where the comparisons are actually made. Form-pair grain
  is for reading; input-cell grain is for measuring.
- **69 leaves**: 73 signatures, less `python.@` whose domain is empty
  and which decision 4 excludes, less the three php rows voided by
  decision 30 *(measured)*.

**DECISION 27, the distance, stated once and flagged for the owner:**

```
similarity(a,b) = J x A
  J = Jaccard over the 64 form-pair cells
  A = fraction of input cells accepted by BOTH
      on which the two answer sets intersect
```

- the **product** is chosen so neither factor can be ignored. It rules
  out two kinds of false closeness at once.
    - **Same domain, different values.** Two operations that accept the
      same forms but compute different values are far apart.
    - **Perfect agreement, tiny overlap.** Two operations that always
      agree where they overlap are still far apart if they overlap on
      little.
- where the domains intersect but no input cell is shared, A is null and
  similarity falls back to J alone, flagged `domain_only` on the edge —
  **56 of 2,346 edges** *(measured)*.
- the rivals are the sum form `wJ + (1-w)A` and the min form, and both
  are computable from the stored J and A **without a re-run**.
- **A is small nearly everywhere, which is the point.** Median edge
  agreement is **0.0337**. **955 of 2,290 edges with an agreement value
  have A exactly zero, and 13 have A exactly one** *(measured)*.

---

## §4 — the clusters, the sweep and the plateaus

Same machinery as log 030 decision 14: average linkage run to a single
root, the full merge history recorded, the cluster count at any
threshold read exactly off it, and **no chosen cut**.

### 4.1 the curve, against the domain-only control

| threshold | 0.10 | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 | 0.70 | 0.80 | 0.90 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|
| answer grain | 11 | 20 | 27 | 34 | 42 | 44 | 45 | 51 | 57 | 68 |
| domain only | 2 | 3 | 7 | 11 | 13 | 17 | 19 | 21 | 23 | 25 |

- the control is the **same 69 leaves, same linkage, J alone**, and it
  exists so that this pass shows what the ANSWERS contributed rather
  than asserting it *(measured)*.
- **at threshold 1.000 the answers give 68 distinct classes against the
  domains' 25** *(measured)*. Only one pair of operations has both an
  identical domain and total answer agreement.
- the answer-grain curve is **smooth with no elbow**, as log 030's was
  *(measured)*, which is again the honest reason to publish a sweep.

### 4.2 the plateaus

| threshold range | width | clusters |
|---|---|---|
| [0.601, 0.700) | 0.099 | **45** |
| [0.881, 0.931) | 0.050 | 57 |
| [0.798, 0.840) | 0.042 | 51 |
| [0.562, 0.601) | 0.039 | 44 |
| [0.840, 0.876) | 0.036 | 52 |
| [0.945, 0.979) | 0.034 | 61 |
| [0.700, 0.734) | 0.034 | 46 |
| [0.528, 0.562) | 0.034 | 43 |
| [0.495, 0.528) | 0.033 | 42 |
| [0.284, 0.315) | 0.031 | **27** |

- **the widest non-degenerate plateau is [0.601, 0.700) and it holds 45
  clusters** *(measured)*. Its two large groups are the split described
  in §1, and they are worth quoting whole:

```
9  php.!= php.!== php.&& php.< php.<= php.||
   python.!= python.is not ruby.!=
8  php.== php.=== php.> php.>= python.==
   python.is ruby.== ruby.===
```

- read plainly: the coarsest STRONG structure the answers give is
  **what an operation returns**. There is a false-ish boolean group and
  a true-ish boolean group, with everything that returns a computed
  value scattered into small clusters around them. Level **derived**
  for the reading; the memberships are measured.
- the pairs at that plateau are the interesting small ones:
  `python.and` with `ruby.&&`, `python.or` with `ruby.||`, `php./`
  with `python./`, `php.<<` with `php.>>` *(measured)*.
- **the coarse reading at [0.110, 0.139) is 14 clusters** *(measured)*,
  and the arithmetic finally groups there:
    - **27 signatures over all three** — the comparisons and both kinds
      of logical, `!= !== && < <= == === > >= in is is not not in ||`.
    - **10 over all three** — `% * ** / //`, the operators that answer a
      number and coerce little.
    - **6 over all three** — `+` and `-` together, which is the first
      threshold at which php's `+` will sit with anybody's.
    - **6 php-only** and **5 python-only** bitwise-and-shift groups, and
      ruby's `& ^ | << >>` in four singletons. The bitwise operators do
      not form a cross-language group at ANY threshold in this pass
      *(measured)*. That is the answer-grain counterpart of log 030's
      shift finding, which was that the largest cluster made of shift
      spellings alone is two, and it points the other way: log 030's
      shifts held together only because the bitwise operations carried
      them, whereas here the bitwise operations do not hold together at
      all.

### 4.3 same-spelling agreement, per operation

The fraction of shared input cells on which two languages' answer sets
intersect. Blank means the spelling is not shared.

| operation | python vs ruby | php vs python | php vs ruby |
|---|---|---|---|
| `<` `>` | 1.000 | 0.969 | 1.000 |
| `<=` `>=` | 1.000 | 0.963 | 1.000 |
| `==` `!=` | 0.997 | 0.948 | 0.945 |
| `/` | 1.000 | 0.987 | 0.800 |
| `%` | 0.996 | 0.563 | 0.429 |
| `-` | 0.970 | 0.857 | 0.861 |
| `*` | 0.948 | 0.908 | 0.819 |
| `<<` | 1.000 | 0.825 | 0.600 |
| `>>` | 1.000 | 0.938 | 0.800 |
| `**` | 0.879 | 0.859 | 0.938 |
| `&` | 0.805 | 0.891 | 0.274 |
| `+` | 0.785 | 0.480 | 0.417 |
| `^` | 0.623 | 0.750 | 0.247 |
| `<=>` | — | — | 0.215 |
| `&&` | — | — | 0.082 |
| `\|\|` | — | — | 0.033 |

- **eleven of the fifty-five language pairs agree on every shared cell**
  *(measured)*: `/`, `<<` and `>>` python-with-ruby, and all four
  relational spellings both python-with-ruby and php-with-ruby.
- the two ends of the table are worth naming against each other. Level
  **derived** for both readings.
    - **The agreement floor is the relational operators.** They are the
      operations the three languages agree on most.
    - **The ceiling of disagreement is the logicals.** `&&` and `||`
      php-against-ruby sit at 0.082 and 0.033.
    - `+` and the bitwise operators sit in between.

---

## §5 — the contradicts findings, with the actual answers

Restricted to the same operation spelled in two languages, as log 030's
relations were. **Zero pairs disagree on every shared cell; 44 of 55
disagree on some cell** *(measured)*. Every quotation below is a
canonical token; the pre-canonical raws are in `answer_alphabet`.

### 5.1 integer overflow — the clean one

```
+  whole|i64max | whole|base_42
python  whole:9223372036854775849
ruby    whole:9223372036854775849
php     fractional:9.2233720368548e+18
```

- php's `int` overflows to `float` and the two bignum languages do not
  *(measured)*. At `u64max + 42` the same split shows and python adds a
  second answer of its own:

```
+  whole|u64max | whole|base_42
python  whole:18446744073709551657
        whole:41
ruby    whole:18446744073709551657
php     fractional:1.844674407371e+19
```

- **python's `whole:41` is its `ctypes.c_int64` holder** — the same
  value class loaded into a fixed-width holder wraps to −1 and −1 + 42
  is 41 *(measured)*. Decision 26's split marker is what keeps that
  visible instead of averaging it away. It is a within-language
  contradiction of exactly the kind log 024 §5 was written about, where
  `Decimal(42) + Fraction(42)` raised although both holders held 42 and
  compared equal.
- consequence, at the cell level: `+` on `whole|whole` agrees **1.000
  python-with-ruby and 0.306 for php against either** *(measured)*.

### 5.2 `&&` and `||` — the largest disagreement in the pass

```
&&  fractional|base_1_5 | fractional|inf
php   truth:true
ruby  fractional:inf
```

```
||  fractional|base_1_5 | fractional|base_1_5
php   truth:true
ruby  fractional:1.5
      fractional:3/2
```

- the two languages answer different KINDS of thing, and that is the
  whole finding *(measured)*.
    - **php's logicals answer a boolean.** `truth:true` on both cells
      above.
    - **ruby's logicals answer an operand.** `fractional:inf` and
      `fractional:1.5` — one of the two things it was given.
- **1,118 of 1,156 shared cells disagree for `||` and 1,061 of 1,156
  for `&&`** *(measured)*. Both operations were `equals` at acceptance
  grain in log 030, meaning they had identical accept sets over the 64
  form-pair cells, because both accept everything.
- ruby's two tokens on the second cell are its `Float` and its
  `Rational` holder answering the same input differently, which
  decision 26 marks `split` rather than resolving.

### 5.3 `true == 42` and `true & 42` — coercion, and its absence

```
==  truth|true | whole|base_42
python  truth:false
ruby    truth:false
php     truth:true
```

```
&   truth|true | whole|base_42
python  whole:0
ruby    truth:true
php     whole:0
```

- three languages, one input, and the majority flips between the two
  lines *(measured)*. The odd one out changes identity between them.
    - **On `==`, php is the odd one out.** Its loose `==` coerces the
      boolean.
    - **On `&`, ruby is the odd one out.** Its `&` is a boolean
      operator where the other two are bitwise.
- note that `true + 42` is **whole:43 in both python and php** and ruby
  refuses it entirely *(measured)*.

### 5.4 `+` on sequences and on text

```
+  sequence|base | sequence|strs
python  sequence:[1,2,3,'a','b']
ruby    sequence:[1,2,3,'a','b']
php     sequence:[1,2,3]
```

- php's `+` on arrays is a union by KEY, so the right operand's entries
  are discarded where the keys collide, and the answer is the left
  operand *(measured)*. python and ruby concatenate instead. ruby's
  second token is its `Set` holder.
- on text the picture is different again, and the two halves are worth
  separating.
    - **python against ruby.** They agree **perfectly** once decision 24
      has decoded both printers — `text|text` under `+` is **1.000
      python against ruby** *(measured)*.
    - **php.** It has no `+` on strings at all, and spells
      concatenation `.`.

### 5.5 `<=>` — a disagreement about what "incomparable" answers

```
<=>  fractional|base_1_5 | keyed|empty
ruby  nothing:null
php   whole:-1
      whole:1
```

- the two languages take opposite positions on operands that do not
  order *(measured)*.
    - **ruby answers nil.** It declines to order them.
    - **php answers a number anyway.** WHICH number depends on the
      holder, which is why two tokens are recorded.
- **907 of 1,156 shared cells disagree** *(measured)*.

### 5.6 the known fractures that did NOT fracture

| fracture | input cell | verdict |
|---|---|---|
| 2^53+1 | `+ whole\|p53_plus1 \| whole\|base_42` | all three agree, `whole:9007199254741035` |
| −0.0 | `+ fractional\|negzero \| fractional\|negzero` | agree — php `fractional:-0.0`, python and ruby carry `-0.0` and `0.0` |
| NaN arithmetic | `+ fractional\|nan \| fractional\|nan` | agree, `fractional:nan` |
| NaN equality | `== fractional\|nan \| fractional\|nan` | agree, `truth:false` |
| inf against NaN | `< fractional\|inf \| fractional\|nan` | agree, `truth:false` |
| e-acute equality | `== text\|eacute \| text\|eacute` | agree, both tokens present in all three |
| e-acute concatenation | `+ text\|eacute \| text\|base_hello` | **disagrees** — see below |

- the e-acute concatenation disagreement is a HOLDER story, not a text
  one:

```
+  text|eacute | text|base_hello
python  text:c3a968656c6c6f
ruby    text:c3a968656c6c6f
        sequence:[233,104,101,108,108,111]
php     sequence:[195,169,108,108,111]
```

- the string holders and the codepoint-array holders behave
  differently, and that is where the whole disagreement sits
  *(measured)*.
    - **The string holders agree exactly.** python and ruby produce the
      same bytes, `text:c3a968656c6c6f`.
    - **The codepoint-array holders disagree.** ruby's array carries the
      codepoint 233 while php's carries the utf-8 bytes 195 and 169.
- php also drops a byte, because `+` on php arrays is the key union of
  §5.4 rather than a concatenation.
- **−0.0 survives only because decision 23 reads php's `-0` back by its
  SIGN CHARACTER.** Parsing it as a number first would have produced
  `whole:0` and reported a fracture that was the reader's *(measured
  during the build; the pre-fix run is what showed it)*.

---

## §6 — what extends to the nine, and what does not

- **the machinery extends unchanged.** Nothing in `l3_answers.py` names
  a language. The moment a route-C run for the nine statically checked
  languages lands as `behavior_<lang>_C.json` with a `complete` field, a
  name added to `LANGS` gives the nine their answer signatures, and the
  distance rule, the sweep and the contradicts scan follow.
- **the input-cell identity extends only if the manifests keep one value
  class vocabulary.** Decision 18 is checked at run time and the check
  is what makes cross-language answer comparison meaningful. A route-C
  build for the nine that invents new value-class names would silently
  reduce every cross-language shared-cell count to zero. That is the one
  thing to hold fixed in the next generator.
- **the canonicalization tables will need nine more rows and they are
  the risky part.** Decisions 20, 21, 24 and 25 are per-language type
  tables. The nine bring fixed-width integers, which means overflow is
  the RULE rather than php's exception, and the §5.1 finding will
  probably invert — python and ruby becoming the odd pair out. Level
  **estimate**.
- **decision 22's float loss gets worse before it gets better.** Nine
  more printers, nine more precisions. The right fix is a harness that
  prints float answers as bits or as a `%.17g` round trip, and it is
  cheaper to fix in the route-C build for the nine than to canonicalise
  around afterwards.
- **decision 28's 120-character cap should be raised or hashed in the
  same build.** 633 answers hit it here on three languages *(measured)*;
  the nine will hit it harder wherever a container answer is printed.
- **what this pass does NOT settle.** It measures three languages that
  all resolve at run time, so every finding here is inside the
  open-dispatch family. Whether the answer grain separates the STATIC
  languages as sharply is unmeasured, and the control in §4.1 gives a
  reason to think it will separate them LESS, since their domains
  already separate them well.

### open for the owner

- **decision 26, the existential holder-to-form answer projection.** The
  split rate it hides is 21.6 / 25.0 / 30.1 percent, which is not small.
  The universal reading is one comparison away.
- **decision 27, the product distance.** Sum and min are the rivals and
  both are re-readable from the stored J and A.
- **the CORE's `contradicts` is a boolean and the measurement is a
  rate.** 44 of 55 same-spelling pairs disagree somewhere and none
  disagrees everywhere. Either the CORE's third arm needs a threshold,
  or the honest relation is "contradicts on N of M cells" and the
  trichotomy becomes a trichotomy plus a number.
- **php's `and` / `or` / `xor` need a re-run, not a repair.** The fix is
  one pair of parentheses in `l3_routec.py`; the rows are void until it
  runs.

---

## §7 — artifacts

All paths are inside
`PseudoCoupHQ/Research/kind_fuzz_clustering/`.

| file | what it is |
|---|---|
| `clusters_answers.json` | signatures, alphabet, merge history, sweep, contradicts |
| `dendrogram_answers.html` | the visual — self-contained, opens from disk |
| `l3_answers.py` | the answer-grain pass; decisions 18 to 30 |
| `make_dendrogram_answers.py` | writes the visual; reads only |
| `clusters_final.json` | log 030's domain-grain result, unchanged |

Reproduce with two commands, neither of which touches a lane:

```
cd PseudoCoupHQ/Research/kind_fuzz_clustering && python3 l3_answers.py
cd PseudoCoupHQ/Research/kind_fuzz_clustering && python3 make_dendrogram_answers.py
```

The visual keeps every convention of `dendrogram_sweep.html`, the
domain-grain picture published with log 030 — the icicle rendering, the
similarity axis, the draggable threshold line, the live cluster count,
the yellow outline on the current clusters, the search box, the hover
card, the plateau table and the shaded cluster-count curve. It adds two
panels the domain-grain file had no data for: the same-spelling
agreement table of §4.3, coloured by rate, and the known-fracture table
of §5.6.
