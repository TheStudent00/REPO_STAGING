# log 033 — layer 3 phase 4: the answer grain, all twelve languages

Date: 2026-08-19. Node:
`PRIVATE/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

**Rewritten 2026-08-19 for readability at the owner's instruction. The content
is identical — same facts, same numbers, same findings, same section
numbers. Only the prose was rebuilt.**

Every claim carries its level. **Measured** means a number a run
printed. **Derived** means a number worked out from measured numbers.
**Estimate** means a guess with a reason. **Unverified** means nobody
has checked it.

Log 033 was free when this was written. It closes CHECK item **4i**.

This pass runs nothing. It reads log 031's three print-grain route-C
tables and log 032's nine bit-grain execution tables and joins them.

---

## words used in this log

This node has built up a set of short words for its own parts. Every
one of them is defined here, with an example taken from this log rather
than a made-up one. Nothing below this block uses a word that is not
either ordinary English or defined here.

```
probe
    one small generated program that asks one
    language one question: apply one
    operation to one pair of values, and say
    what happens.
    example tied to context:
        swift's old accepted set held 2,618
        probes, and 1,066 of them produce no
        answer at all.

lane
    one batch job. it runs a planned set of
    probes and writes its output to one raw
    text file.
    example tied to context:
        §7's two reproduction commands read
        files that lanes already wrote; this
        pass starts no lane.

route A, route C
    two ways a language is measured. a
    route-A language is compiled, so a probe
    first gets an accept-or-refuse verdict
    and needs a second run to get an answer.
    a route-C language is run directly, so
    acceptance and answer arrive together.
    example tied to context:
        python, ruby and php are route C, and
        their answers are the printed strings
        log 031 read. the other nine are
        route A, and log 032 executed them.

manifest
    a frozen file listing what was probed for
    one language: its holders, its value
    classes, its operation list. it records a
    past run and is not edited afterwards.
    example tied to context:
        §6 notes that only the route-C
        manifests for python, ruby and php
        enumerate holders that could carry
        indexing or calling.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        c++'s `unsigned` is a holder. on
        `i64max + 42` it answers `whole:41`
        where c++'s signed 64-bit holder
        answers `whole:-9223372036854775767`.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        `i64max` is a value class: the largest
        signed 64-bit integer. `base_42` is
        another: the plain number 42.

form
    the coarse kind an operand is presented
    as, above the holder. the forms are the
    axes of the 64-cell grid.
    example tied to context:
        `whole`, `fractional`, `text`,
        `truth`, `sequence`, `nothing` are
        forms. go has no `nesting` form.

cell (also: input cell)
    one combination of operand kinds an
    operation was asked about. a cell is the
    unit an answer is recorded against.
    example tied to context:
        `cpp.<=>` and `php.<=>` share 211
        input cells and disagree on all 211.

domain
    the set of cells an operation actually
    accepted. cells the language refused are
    not in the domain.
    example tied to context:
        go's `+` accepts three form pairs and
        java's accepts thirty-two, which is
        why their edge is far apart even
        though they never disagree.

answer class
    the kind and value an operation returned
    on a cell, written as kind:value.
    example tied to context:
        `whole:0` is an answer class — a whole
        number, zero. `ord:eq` is another — a
        comparison category reading "equal".

canonical token
    the single agreed spelling of an answer
    class, after the bridge has run. two
    languages agree on a cell when their
    canonical tokens match.
    example tied to context:
        `whole:-9223372036854775767` is the
        canonical token five languages reach
        on `i64max + 42`.

the print grain, the bit grain
    the two ways an answer arrived. the print
    grain is the string a route-C language
    printed. the bit grain is the string
    `<TYPE>|<ENCODING>:<PAYLOAD>` log 032
    recorded by executing a route-A language.
    example tied to context:
        python's printed
        `9223372036854775849` is print grain.
        go's `INT:64:8000000000000029` is bit
        grain. the bridge maps both onto
        canonical tokens.

the bridge
    the set of rules, numbered 31 to 42, that
    turns a print-grain answer and a bit-grain
    answer into one canonical token so the
    twelve languages can be compared at all.
    example tied to context:
        §2 is the bridge. 457 canonical tokens
        are reached from both a printed
        pre-form and a bit pre-form.

the shadow (a 14-digit shadow)
    a second, shortened spelling of a float
    answer: the value printed to 14 digits.
    it is used instead of the exact bits
    whenever one side of a comparison is a
    print-grain language, because a printed
    float carries no more than that.
    example tied to context:
        13,179 of 25,425 edges fall back to
        the shadow.

raise
    an answer class for a language refusing
    an input at run time by throwing. written
    `raise:<name>`.
    example tied to context:
        `raise:ZeroDivisionError` is python's
        answer on `42 / 0`.

death
    an answer class for the process being
    killed rather than throwing. written
    `death:rc-<n>`.
    example tied to context:
        `death:rc-8` is c++'s answer on
        `42 / 0`; it is `SIGFPE` and cannot
        be caught.

CODEGEN_REFUSE (a codegen refusal)
    the compiler accepted a probe when
    checking types but refused it when
    generating machine code. the probe
    produces no answer.
    example tied to context:
        1,066 of swift's 2,618 accepted probes
        are codegen refusals, and decision 40
        removes them with their count.

VOID
    a mark put on a measurement that was
    taken wrongly, so that it is kept on the
    record but not used. a VOID row is not a
    leaf.
    example tied to context:
        php's `and`, `or` and `xor` are VOID
        under decision 30, so three php rows
        are missing from the 226.

leaf
    one operation of one language, once it
    has answers to cluster with. leaves are
    the things the clustering arranges.
    example tied to context:
        `cpp.<=>` is a leaf. this pass has 226
        of them.

signature
    everything recorded about one leaf: its
    64-cell form-pair vector, its full
    input-cell map, its answer classes.
    example tied to context:
        230 signatures were built and 226
        survive as leaves.

edge
    the measured closeness between two
    leaves. every pair of leaves that shares
    at least one cell has an edge.
    example tied to context:
        this pass has 25,425 edges.

Jaccard (J), agreement (A), similarity
    three numbers on an edge. Jaccard is how
    much the two domains overlap. agreement
    is the share of shared cells where the
    two leaves gave the same canonical token.
    similarity is the two multiplied, which
    is decision 27's product.
    example tied to context:
        `go.+` against `java.+` is J 0.094,
        A 1.000, similarity 0.094.

domain_only (an edge marked domain_only)
    an edge whose two domains meet but whose
    two leaves share no input cell, so there
    is no agreement number to compute.
    example tied to context:
        1,255 of 25,425 edges are
        domain_only.

clustering
    the arrangement built from the edges: it
    repeatedly joins the two closest groups
    of leaves until one group is left. the
    result is `clusters_all12.json` and the
    picture of it is `dendrogram_all12.html`.
    example tied to context:
        the clustering here has 226 leaves and
        picks no cut of its own.

linkage
    the rule for how far apart two GROUPS of
    leaves are, once single leaves have been
    joined. average linkage is used
    throughout this node.
    example tied to context:
        the domain-only control uses the same
        226 leaves and the same linkage, so
        the only difference is the numbers on
        the edges.

threshold sweep (also: reading, cut)
    a distance chosen to stop reading the
    clustering at. every cut gives some
    number of clusters. the sweep is the
    whole curve of cluster counts, published
    instead of one chosen cut.
    example tied to context:
        the cut at 0.085 gives 15 clusters;
        the cut at 1.000 gives 195.

plateau
    a run of cuts over which the number of
    clusters does not change. a wide plateau
    means that reading is stable.
    example tied to context:
        [0.465, 0.499) is the widest plateau
        in this pass: every cut in it gives 80
        clusters.

elbow
    a place where the cluster-count curve
    bends sharply, which would be a reason in
    the data to pick one cut. a smooth curve
    has none.
    example tied to context:
        the answer-grain curve has no elbow,
        which is why this log publishes a
        sweep and chooses no cut.

singleton
    a cluster holding exactly one leaf.
    example tied to context:
        30 of the 80 clusters at the widest
        plateau are singletons, `cpp.+` among
        them.

the domain-only control
    the same 226 leaves clustered with the
    same linkage but on domain overlap alone,
    with the answers switched off. it exists
    so this pass can SHOW what the answers
    added rather than assert it.
    example tied to context:
        the control gives 58 distinct classes
        at threshold 1.000 where the answers
        give 195.

contradicts (total, partial)
    the CORE's word for two languages giving
    different answers to the same input. a
    total contradiction disagrees on every
    shared cell. a partial one disagrees on
    some.
    example tied to context:
        `cpp.<=>` against `php.<=>` is total:
        211 shared cells, 211 disagreements.

same-spelling pair
    two leaves that are the same operation
    written the same way in two different
    languages. §5's relations are restricted
    to these.
    example tied to context:
        `java.+` and `php.+` are a
        same-spelling pair. there are 974 of
        them.

the static-and-open divide (the static/open
    divide is the same thing)
    the split between the nine languages
    whose compiler checks the operand types
    before the program runs, and the three
    that decide at run time.
    example tied to context:
        c++ is on the static side and php and
        ruby are on the open side, so the two
        total contradictions in §4.4 cross the
        divide.

the numeric tower
    the set of number holders a language
    offers and the rules for moving between
    them.
    example tied to context:
        python's tower has an unbounded
        integer, so `i64max + 42` stays exact.
        go's has a 64-bit one, so it wraps.

decision <n>
    a numbered ruling this node has made,
    kept so it can be overturned by number.
    decisions 1 to 30 were made in earlier
    logs; 31 to 42 are made in §2 here.
    example tied to context:
        decision 39 keeps `ORD`, `RANGE` and
        `ENUM` in kinds of their own, and it
        is what makes §4.4's contradictions
        total.

CHECK item <n><letter>
    a numbered line in the node's CHECK file,
    `CHECK_0_3_2_kind_fuzz_clustering.md`,
    which tracks what phase 4 owes.
    example tied to context:
        this log closes item 4i and leaves
        item 4j unstarted.

the icicle, the DOM stub
    the icicle is the block rendering of the
    clustering used by every visual in this
    node. the DOM stub is a small script that
    pretends to be a browser page so the
    visual's own scripts can be run and
    checked without opening one.
    example tied to context:
        `node domstub.js dendrogram_all12.html`
        runs both scripts with zero throws.
```

---

## what came before this log, restated

Six earlier logs are needed to read this one. Each fact this log uses
from them is stated here in full, so no sentence below depends on
opening another file.

- **Log 029 was the first answer-shaped look at `+`.** It found `+`
  scattered rather than grouped, with no principle named for the
  scattering.
- **Log 030 clustered the operations on their domains alone.** Its
  coarse reading was three clusters sorted purely by domain WIDTH: 147
  permissive, 51 strict, and 31 integer-and-truth-only.
- **Log 030 measured zero contradictions at acceptance grain.** It said
  plainly that a zero at acceptance grain says nothing about whether
  the CORE's answer-grain definition of `contradicts` has instances.
- **Log 030 found that `+` never forms a pure cluster larger than two**
  at any threshold in its sweep.
- **Log 030 item 4k ruled kotlin's and swift's shifts out of scope.**
  Kotlin spells them `shl` and `shr` and they are builtins by the
  CORE's own rule; swift has no route-C rows for `<<` and `>>` in this
  material. That ruling has not been revisited.
- **Log 031 was the answer-grain clustering over three languages** —
  python, ruby and php — and it found that the answers carried
  essentially the whole signal, with the domains adding little.
- **Log 031 made decisions 18 to 30**, including decision 25's printed
  container grammar, decision 26's holder split marker, and decision
  27's distance, which is Jaccard on domains multiplied by the
  agreement rate on shared cells.
- **Log 031's decision 30 voided php's `and`, `or` and `xor`** because
  the probe recorded the left operand instead of the result.
- **Log 031 found the bitwise operators forming NO cross-language group
  at any threshold**, which pointed the other way from log 030's shift
  finding.
- **Log 031 found php's float escape on integer overflow** and called
  it the cleanest answer-grain contradiction of that pass. Its §5.1
  recorded python's `ctypes.c_int64` holder wrapping and then adding,
  and its §5.4 diagnosed php's `+` on arrays as a key union rather than
  a concatenation.
- **Log 031's same-spelling relations were 55 pairs, of which 11 agreed
  on every shared cell**, and it reported the CORE's boolean
  `contradicts` as measuring out to a rate strictly between 0 and 1.
- **Decision 31 in THIS log changed a quantity log 031 published.** Log
  031 discarded RAISE cells; this pass records them as answer classes.
  So `php.+` against `python.+` reads 0.480 in log 031 and 0.945 here.
  **The two logs' A factors are not the same measurement and must not
  be read against each other.**
- **Log 032 executed the other nine languages and recorded their
  answers as bits**: integers as two's complement, floats as their IEEE
  pattern, text as its bytes, containers recursively.
- **Log 032 §5 measured swift's 1,066 codegen refusals** out of 2,618
  accepted probes, and said the fix is a route-C build taken with full
  `swiftc` rather than `swiftc -typecheck`. Its §5 also described the
  six-way split on `42 / 0`.
- **Log 032 §6 found kotlin stringifying an array under `+`** rather
  than concatenating, and recorded that rust's panic on overflow is a
  debug-build property that a release build would not show.
- **Decision 24, made before this pass, already chose bytes for text**,
  which is why text needs no bridging work here.

---

## §1 — walkthrough, in plain words

Three passes stand behind this one, and this pass joins the last two.

- Log 030 clustered operations on their **domains** — which ordered
  pairs of forms an operation will accept — and measured zero
  contradictions at that grain.
- Log 031 read the computed values for the three languages that had
  them, and found the answers carried essentially the whole signal.
- Log 032 executed the other nine and recorded what they return as
  **bits**.

That leaves two logs, two encodings, and one question. Do the answers
say the same thing when all twelve languages stand in the same picture?
This pass builds the bridge between the two encodings and answers it.

**The headline is that the first genuine answer-grain contradiction in
this node has been measured, and it lands across the static-and-open
divide.**

- `cpp.<=>` against `php.<=>`, and `cpp.<=>` against `ruby.<=>`,
  disagree on **all 211 shared input cells**, rate 1.000 *(measured)*.
- C++ answers a comparison category — `std::partial_ordering`, the
  canonical token `ord:eq` — where php answers `whole:0` and ruby
  answers `whole:0`.
- One more pair is total inside the nine statically checked languages:
  `kotlin...` against `rust...`, 112 of 112 *(measured)*.
- Log 030 measured zero contradictions at acceptance grain, and log 031
  measured zero at answer grain over its three languages. Twelve
  languages give **three**.
- Every one of the three is a language answering in a KIND the other
  does not have. Level **derived** for that reading, measured for the
  counts.

**The second finding is that the answers do not rearrange the twelve
the way they rearranged the three.** The two sides of that comparison,
named against each other:

- **The domain-only control — the same 226 leaves, answers switched
  off.** It collapses to **one cluster over [0.000, 0.059)** and **two
  over the widest band [0.059, 0.130)** *(measured)*. Acceptance grain
  is nearly blind here, exactly as log 031 found for its three.
- **The answer grain — the same 226 leaves, answers switched on.** It
  gives **80 clusters over the widest band [0.465, 0.499)** and **195
  distinct classes at threshold 1.000 against the domains' 58**
  *(measured)*.

The coarse structure the answers produce is no longer log 031's
principle, and the two principles are worth naming side by side:

- **Log 031's three-language reading**, its principle: what does this
  operation return.
- **This pass's 15-cluster reading**, its principle: what family of
  computation the language belongs to. The languages split along their
  own lines before the operators do.

**The third finding is that `+` still splits by coercion, and now into
four families rather than log 029's scatter.** At the coarse
[0.085, 0.104) reading:

- `cpp.+`, `csharp.+`, `java.+`, `kotlin.+` and `typescript.+` sit
  together with `cpp.-` *(measured)*.
- `go.+` and `rust.+` sit inside the thirty-member arithmetic group
  *(measured)*.
- `php.+` and `python.+` sit inside the thirty-three-member
  open-dispatch group *(measured)*.
- `ruby.+` sits with the rest of ruby *(measured)*.

The five that group are the five that concatenate a string with `+`.
Log 030 could say only that `+` never forms a pure cluster larger than
two. The answers say what the grouping principle is instead.

**And the fourth is a negative result that had to be checked.**

- Five languages return the **bit-identical** wrapped integer on
  `i64max + 42`. Go, c++, java, c-sharp and kotlin all record
  `INT:64:8000000000000029`. Rust panics.
- That bit identity does **not** pull them into a cluster.
- `go.+` pairs with `rust.+` at similarity 0.907, Jaccard 1.000, the
  panic and all *(measured)*.
- `go.+` against `java.+` is 0.094, because their DOMAINS barely
  overlap *(measured)*.
- Answer agreement cannot rescue two operations that accept different
  things. That is what decision 27's product was chosen to do.

The instrument facts belong here, where they can be seen, rather than
in a footnote.

- Swift's 1,066 `CODEGEN_REFUSE` probes are excluded with their count
  under decision 40. That leaves swift **six leaves and 400 input
  cells** *(measured)*, and makes every swift number in this log thin.
- C++'s 480 deaths are answer classes of their own under decision 31.
  `death:rc-8` on `42 / 0` is what lets that cell be measured as the
  six-way split log 032 §5 described, rather than as a blank.

---

## §2 — the bridge, as numbered overturnable decisions

Decisions 1 to 17 stand where log 030 left them, and 18 to 30 where log
031 left them. These are **31 to 42**. They are carried verbatim in
`clusters_all12.json` under `bridge_decisions`, beside the earlier ones
under `decisions`, so overturning any of them is a one-line
instruction.

The rule the whole section obeys: a merge is only ever performed on the
canonical side, and the pre-bridge form is kept in `answer_alphabet` —
the printed string for the three route-C languages, the string
`<TYPE>|<ENCODING>:<PAYLOAD>` for the nine route-A ones.

| n | rule | what it merges | reversible by |
|---|---|---|---|
| 31 | a raise or a death is an answer class | nothing — it ADDS | drop the two token families |
| 32 | the 64-cell domain stays value-answers only | nothing | — |
| 33 | integers bridge by value, width dropped | `INT:32` with `INT:64` with `whole:42` | `answer_alphabet` |
| 34 | floats keep bits AND a 14-digit shadow | shadow used when a print-grain language is in the pair | stored both tokens |
| 35 | `BOOL`/`NULL` join `truth:`/`nothing:null` | three spellings of two values | `answer_alphabet` |
| 36 | `STR` drops both lengths, `CHAR` becomes text | java's `char` with a one-character string | `answer_alphabet` |
| 37 | containers rendered into decision 25's grammar | numeric and text bodies only | `bridge_merges` |
| 38 | `SOME(x)` and `REF(x)` unwrap, `PTR` does not | an optional with its content | one line |
| 39 | `ORD`, `RANGE`, `ENUM` keep their own kind | nothing — it SPLITS | — |
| 40 | swift `CODEGEN_REFUSE` excluded with count | nothing — it REMOVES | `codegen_refuse` per leaf |
| 41 | the value-class check is containment, not equality | nothing | `value_class_vocabulary` |
| 42 | every pre-bridge form kept, bridge counted | nothing | `bridge_merges` |

- **decision 31 is the one that changes a published number, and it is
  said here rather than found later.** Log 031 discarded RAISE cells.
  This pass records them as `raise:<name>` tokens for all twelve, which
  is what makes `42 / 0` measurable at all. The price is that two
  languages that both refuse the same input now AGREE there. `php.+`
  against `python.+` was **0.480 in log 031 and is 0.945 here**
  *(measured)*, and the difference is entirely raises agreeing with
  raises. **The two passes' A factors are not the same quantity and
  must not be read against each other.**
- **decision 33's dropped width is what makes the overflow story
  measurable.** Go's `INT:64:8000000000000029` becomes
  `whole:-9223372036854775767`, and python's answer stays
  `whole:9223372036854775849`. The two are one comparison apart instead
  of two encodings apart.
- **decision 34 records where precision is lost and how much.**
  **13,179 of 25,425 edges fall back to the 14-digit shadow** because a
  print-grain language is on one side *(measured)*. Among the edges
  that do NOT fall back, **37 edges and 1,698 input cells would have
  been merged by the shadow and are not** *(measured)*. That is the
  size of the precision the nine keep and the three cannot offer.
- **decision 37 is the weakest bridge in the pass and is labelled so.**
  A container renders into decision 25's printed grammar, so
  `LIST:3[INT:64:…1,INT:64:…2,STR:1:1:61]` becomes
  `sequence:[1,2,'a']` and meets kotlin's and python's answer for the
  same thing. It does not meet a python container holding a boolean or
  a null, because python prints `True` and `None` where this renders
  `true` and `null`. **134 of 457 bridged tokens are containers**
  *(measured)*, and the honest fix is a re-print, not a
  re-canonicalisation.
- **decision 41 passes.** Every one of the nine uses value-class names
  drawn from the three's vocabulary and none invents one:
  `value_class_vocabulary_contained` is **true** *(measured)*. Go has
  no `nesting` form and no `sequence|bigint` class. That is a smaller
  input space, not a different one, and decision 18's identity holds
  wherever a cell exists in both.

What the bridge actually did, for the five largest canonical tokens:

| canonical token | languages reaching it by printing | languages reaching it by bits | cells |
|---|---|---|---|
| `truth:false` | 3 | 11 | 121,015 |
| `truth:true` | 3 | 11 | 106,822 |
| `whole:0` | 7 | 40 | 10,945 |
| `nothing:null` | 3 | 12 | 8,439 |
| `fractional:nan` | 4 | 31 | 6,202 |

- **457 canonical tokens are reached from BOTH a printed pre-form and a
  bit pre-form** *(measured)*. Each is listed in `bridge_merges` with
  both spellings and both counts. The largest is the boolean, as it was
  in log 031, and it carries twelve languages.

The material, per language, after the bridge:

| language | leaves | input cells | value answers | raises | deaths | refused |
|---|---|---|---|---|---|---|
| python | 24 | 27,744 | 100,597 | 227,761 | 0 | 0 |
| ruby | 22 | 25,432 | 60,428 | 200,954 | 0 | 0 |
| php | 23 | 26,588 | 75,967 | 114,496 | 0 | 0 |
| go | 19 | 1,378 | 2,774 | 32 | 0 | 0 |
| rust | 19 | 1,541 | 3,792 | 471 | 0 | 0 |
| c++ | 19 | 4,407 | 26,905 | 0 | 480 | 0 |
| java | 19 | 2,473 | 12,349 | 492 | 0 | 0 |
| c-sharp | 19 | 2,940 | 14,636 | 216 | 0 | 0 |
| typescript | 23 | 8,918 | 43,030 | 1,520 | 0 | 0 |
| swift | 6 | 400 | 1,552 | 0 | 0 | 1,066 |
| kotlin | 16 | 5,482 | 33,203 | 1,450 | 0 | 0 |
| dart | 17 | 4,107 | 24,612 | 1,839 | 0 | 0 |
| **twelve** | **226** | **111,410** | **399,845** | **549,231** | **480** | **1,066** |

- **226 leaves**: 230 signatures, less `python.@` whose domain is empty
  and which decision 4 excludes, less the three php rows voided by
  decision 30 *(measured)*.

---

## §3 — the signatures, the sweep and the plateaus

The 64-cell form-pair vector of decision 1 is kept, and each accepted
cell carries its answer classes, with decision 26's holder split marked
per cell. Underneath the 64 cells the signature keeps the full
input-cell map, which is where the comparisons are made.

Decision 26's split rate — how often two holders of the same form
answer differently on one cell — is the first thing the wider set
changes. Measured across all twelve:

| language | split rate |
|---|---|
| swift | 0.020 |
| go | 0.042 |
| rust | 0.103 |
| java | 0.198 |
| dart | 0.199 |
| c++ | 0.280 |
| c-sharp | 0.335 |
| kotlin | 0.344 |
| typescript | 0.352 |
| python | 0.437 |
| php | 0.661 |
| ruby | 0.793 |

- Read plainly: **the more holders a form has and the freer they are,
  the more often two holders of one form answer differently**
  *(measured)*. Go and swift barely split. Ruby splits on four cells in
  five. Decision 26 hides more in the open languages than in the
  statically checked ones, which is the opposite of harmless.

### 3.1 the curve, against the domain-only control

| threshold | 0.10 | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 | 0.70 | 0.80 | 0.90 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|
| answer grain | 15 | 27 | 43 | 68 | 81 | 101 | 115 | 131 | 153 | 195 |
| domain only | 2 | 4 | 9 | 17 | 25 | 33 | 42 | 49 | 56 | 58 |

- The control is the **same 226 leaves, same linkage, Jaccard alone**
  *(measured)*. It exists so this pass shows what the answers
  contributed rather than asserting it.
- **At threshold 1.000 the answers give 195 distinct classes against
  the domains' 58** *(measured)*.
- The answer-grain curve is **smooth with no elbow**, as log 030's and
  log 031's were *(measured)*. That is again the honest reason to
  publish a sweep and no cut.
- **A is small nearly everywhere.** Median edge agreement is
  **0.0436**. **10,234 of 24,170 edges with an agreement value have A
  exactly zero, and 481 have A exactly one.** **1,255 of 25,425 edges
  are `domain_only`**, meaning the domains meet but no input cell does
  *(measured)*.

### 3.2 the plateaus

| threshold range | width | clusters |
|---|---|---|
| [0.465, 0.499) | 0.034 | **80** |
| [0.697, 0.730) | 0.033 | 115 |
| [0.155, 0.185) | 0.030 | **22** |
| [0.114, 0.142) | 0.028 | 18 |
| [0.629, 0.656) | 0.027 | 105 |
| [0.607, 0.629) | 0.022 | 103 |
| [0.212, 0.233) | 0.021 | 30 |
| [0.264, 0.284) | 0.020 | 39 |
| [0.085, 0.104) | 0.019 | **15** |
| [0.448, 0.464) | 0.016 | 78 |

- **The widest plateau is [0.465, 0.499) and it holds 80 clusters**
  *(measured)*, 30 of them singletons. Its three largest groups, quoted
  whole:

| size | the leaves in the group |
|---|---|
| 14 | `php.!=` `php.!==` `php.&&` `php.<` `php.<=` `php.>` `php.>=` `php.\|\|` `kotlin.!=` `python.!=` `python.is not` `ruby.!=` `typescript.!=` `typescript.!==` |
| 12 | `csharp.&&` `csharp.\|\|` `go.&&` `go.\|\|` `java.&&` `java.\|\|` `kotlin.&&` `kotlin.\|\|` `rust.&&` `rust.\|\|` `swift.&&` `swift.\|\|` |
| 10 | `dart.==` `kotlin.==` `php.==` `php.===` `python.==` `python.is` `ruby.==` `ruby.===` `typescript.==` `typescript.===` |

- Log 031's finding survives the widening and is now sharper. The
  false-ish boolean group has picked up typescript and kotlin. The
  true-ish boolean group has picked up dart, kotlin and typescript. And
  the **nine statically checked languages' `&&` and `||` form a group
  of their own that php's do not join** *(measured)*.
- The reason php stays out is a domain fact, and the two sides are
  worth naming against each other:
  - **php's `&&` and `||`** answer a boolean, so they sit with the
    comparisons, exactly as log 031 read them.
  - **the nine statically checked languages' `&&` and `||`** answer a
    boolean too, but on a different domain, and the Jaccard factor is
    what keeps them apart.
- **The coarse reading at [0.085, 0.104) is 15 clusters** *(measured)*,
  and it is the one to read against log 030's three-cluster
  domain-width reading. The groups are by language family first:

| size | the group |
|---|---|
| 43 | the equality-and-loose group, 9 languages |
| 34 | the relational group, 8 languages |
| 33 | python and php arithmetic, plus c++ bitwise |
| 30 | the strict arithmetic group, 8 languages |
| 26 | the statically checked languages' bitwise-and-logical |
| 13 | ruby, almost whole |
| 12 | the operand-returning group, 6 languages |
| 11 | the shift group: dart, go, java, ruby, rust |
| 9 | c-sharp arithmetic-and-bitwise |
| 6 | `cpp.+` `cpp.-` `csharp.+` `java.+` `kotlin.+` `typescript.+` |

- The two coarse readings sort by different principles, and this is the
  contrast *(derived)*:
  - **Log 030's acceptance-grain coarse reading** sorted purely by
    domain WIDTH: 147 permissive, 51 strict, 31 integer-and-truth-only.
  - **This pass's answer-grain coarse reading** sorts by what the
    operation computes, and at the coarse end that tracks the
    language's numeric tower more than it tracks the operator.
- Against log 031's three-language picture, the shift finding **flips
  back**, and again the two readings sit side by side:
  - **Log 031 reported** that the bitwise operators form no
    cross-language group at any threshold.
  - **This pass measures** `dart.<<`, `dart.>>`, `go.&^`, `go.<<`,
    `go.>>`, `java.<<`, `java.>>`, `java.>>>`, `ruby.>>`, `rust.<<` and
    `rust.>>` forming an eleven-member group that holds from
    [0.085, 0.104) to [0.212, 0.233), with eight of the eleven
    surviving to the widest plateau *(measured)*.
- Log 030's shift finding was about go, java and rust. The answers add
  dart and ruby to it, and keep c++, c-sharp and typescript out.

---

## §4 — the named stories, with the actual answers

Every quotation below is a canonical token. The pre-bridge raws are in
`answer_alphabet`: the printed string for the three route-C languages,
the type-and-bits string for the nine route-A ones.

### 4.1 does `+` still split by coercion once answers weigh in

Yes, and the answers name the principle log 029 and log 030 could only
observe. At the 15-cluster reading `+` occupies four different
clusters:

| cluster | the `+` leaves in it |
|---|---|
| the concatenating checked six | `cpp.+ csharp.+ java.+ kotlin.+ typescript.+` |
| the strict arithmetic thirty | `go.+ rust.+` |
| the open thirty-three | `php.+ python.+` |
| ruby's own thirteen | `ruby.+` |

- Dart has no `+` leaf at all in this material *(measured)*; dart's
  route-C operation menu does not carry it.
- The five that group are the five whose `+` will take a string, and
  the joining cell is text concatenation.

The worked cell, `+` on the input cell `text|eacute | text|base_hello`:

| language | canonical token |
|---|---|
| python | `text:c3a968656c6c6f` |
| ruby | `text:c3a968656c6c6f` |
| go | `text:c3a968656c6c6f` |
| rust | `text:c3a968656c6c6f` |
| c++ | `text:c3a968656c6c6f` |
| php | `sequence:[195,169,108,108,111]` |

- **Six languages agree on the bytes exactly** *(measured)*, which is
  the first time this fracture has been read outside the three. Php
  still drops a byte, because `+` on php arrays is a key union and not
  a concatenation, as log 031 §5.4 diagnosed.
- Java, c-sharp, kotlin and typescript disagree here, and the reason is
  a holder rather than a text rule. Their array holders stringify
  rather than concatenate, so java answers
  `text:5b4240353931306534343068656c6c6f` — the bytes of
  `[B@5910e440hello`, an identity hash inside a string *(measured)*.
  That is the same shape of fault log 032 §6 found in kotlin, and it is
  a property of what java's `+` does to an array rather than a recorder
  choice.
- The numeric side keeps them apart just as firmly.

The worked cell, `+` on the input cell `whole|i64max | whole|base_42`.
Ten languages give six distinct answers. Where a language shows more
than one token, that is decision 26's split marker: a language with a
`BigInteger` holder answers in the bignum and in the wrapped 64-bit
holder on the same input cell, and both are kept *(measured)*.

| language | canonical tokens |
|---|---|
| python | `whole:9223372036854775849` |
| ruby | `whole:9223372036854775849` |
| php | `fractional:9.2233720368548e+18` |
| go | `whole:-9223372036854775767`, `whole:9223372036854775849` |
| rust | `raise:panic`, `whole:9223372036854775849` |
| java | `whole:-9223372036854775767` |
| c-sharp | `whole:-9223372036854775767`, `whole:9223372036854775849` |
| typescript | `fractional:9.223372036854776e+18`, `whole:-9223372036854775767` |
| kotlin | `whole:-9223372036854775767`, `whole:9223372036854775849` |
| c++ | `whole:-9223372036854775767`, `whole:41`, `whole:9223372036854775849` |

- C++'s `whole:41` is its `unsigned` holder — the same
  wrap-to-minus-one-then-add-42 that log 031 §5.1 found in python's
  `ctypes.c_int64`.
- Php is still the odd one, leaving the integers where python and ruby
  stay in them. It is no longer alone, though, because **typescript's
  `number` holder does the same thing**,
  `fractional:9.223372036854776e+18` *(measured)*.
- Log 031 called php's float escape the cleanest answer-grain
  contradiction of that pass. At twelve languages it is a two-language
  habit, and the majority is the wrap.

### 4.2 do the bit-identical wrap languages cluster against rust-panic

No, and the reason is the point of decision 27's product. The two sides
of the question, named against each other and each shown:

**Side one — the fact that says they should cluster: the bits are
identical.** On `i64max + 42` in each language's 64-bit signed holder,
log 032's bit-grain records read:

| language | log 032's bit-grain record |
|---|---|
| go | `INT:64:8000000000000029` |
| c++ | `INT:64:8000000000000029` |
| java | `INT:64:8000000000000029` |
| c-sharp | `INT:64:8000000000000029` |
| kotlin | `INT:64:8000000000000029` |
| rust | `panic` |

- All five bridge to the single canonical token
  `whole:-9223372036854775767` *(measured)*, and rust bridges to
  `raise:panic`. On that one cell the five agree with each other, and
  none of them agrees with rust.

**Side two — the fact that decides: the domains do not meet.** At the
widest plateau **`go.+` sits with `rust.+` and with nobody else**,
while `java.+` sits with `csharp.+`, and `cpp.+`, `kotlin.+` and
`typescript.+` are singletons *(measured)*. The edges say why:

| pair | J | A | similarity | shared cells |
|---|---|---|---|---|
| `go.+` `rust.+` | 1.000 | 0.907 | 0.907 | 108 |
| `java.+` `csharp.+` | 1.000 | 0.531 | 0.531 | 527 |
| `java.+` `kotlin.+` | 0.522 | 0.860 | 0.449 | 379 |
| `go.+` `java.+` | 0.094 | 1.000 | 0.094 | 88 |
| `go.+` `cpp.+` | 0.167 | 1.000 | 0.167 | 108 |

The two rows that carry the whole answer, set against each other:

- **`go.+` against `rust.+`: perfect domains, imperfect answers, and
  they cluster.** J 1.000, A 0.907, similarity 0.907 over 108 shared
  cells. The wrap-versus-panic difference costs them 0.093 of agreement
  and does not separate them.
- **`go.+` against `java.+`: perfect answers, almost no shared domain,
  and they do not cluster.** J 0.094, A exactly 1.000, similarity
  0.094 over 88 shared cells. They **agree on every one of their 88
  shared cells** and are still the fourth-most-distant pair in the
  table, because go's `+` accepts three form pairs and java's accepts
  thirty-two *(measured)*.

- Bit identity on a shared cell buys nothing when the domains do not
  meet. Level **derived** for the reading; the numbers are measured.
- **The bit-identical five never form a cluster at any threshold in
  this sweep** *(measured)*, which is the answer-grain counterpart of
  log 030's "`+` never forms a pure cluster larger than two".
- One caveat repeated from log 032 §6: rust's panic is a **debug-build
  property**. A release build wraps like the other five and has not
  been run.

### 4.3 where dart's answer-anyway `/` and typescript's float-everything land

Together, and with java and kotlin, which is the surprise.

The worked cell, `42 / 0`, each language in its own integer holder:

| language | canonical tokens |
|---|---|
| go | `raise:runtime error: integer divide by zero` |
| rust | `raise:panic` |
| java | `raise:java.lang.ArithmeticException` |
| kotlin | `raise:java.lang.ArithmeticException` |
| c-sharp | `raise:System.DivideByZeroException` |
| c++ | `death:rc-8` |
| typescript | `fractional:inf`, `raise:RangeError` |
| dart | `fractional:inf` |
| python | `raise:ZeroDivisionError` |
| ruby | `raise:ZeroDivisionError` |
| php | `raise:DivisionByZeroError` |

- **Eleven languages, and `fractional:inf` appears in two of them**
  *(measured)*. Dart's `/` returns a `double` whatever its operands
  are, and typescript has no integer type. Both answer where the other
  nine refuse or die. C++'s `death:rc-8` is `SIGFPE`, uncatchable, and
  it is an answer class here rather than a hole.
- And yet `dart./` and `typescript./` are at **similarity 1.000,
  Jaccard 1.000, agreement 1.000 over 144 shared cells** *(measured)* —
  the same domain and the same answer on every cell they share. At the
  widest plateau they sit in a cluster of four with `java./` and
  `kotlin./`:

| pair | J | A | similarity | shared |
|---|---|---|---|---|
| `dart./` `typescript./` | 1.000 | 1.000 | 1.000 | 144 |
| `java./` `kotlin./` | 1.000 | 1.000 | 1.000 | 100 |
| `dart./` `java./` | 1.000 | 0.840 | 0.840 | 100 |
| `dart./` `go./` | 0.500 | 0.500 | 0.250 | 72 |
| `dart./` `python./` | 0.444 | 0.656 | 0.292 | 189 |

- The four share a domain — `whole|whole`, `whole|fractional`,
  `fractional|whole`, `fractional|fractional` — and disagree only where
  the divisor is zero, which is 16 percent of the cells java and dart
  share *(measured, derived percentage)*.
- The **answer-anyway habit costs dart less distance from java than
  java's own domain costs it from go**, whose `/` accepts only
  `whole|whole` and `fractional|fractional`.
- Typescript's float-everything shows up more strongly on the shifts
  than on the division. `typescript.<<` sits with typescript's own
  bitwise operators and nowhere else at any threshold, and its edge to
  `java.<<` is **J 0.250, A 0.188, similarity 0.047** — the lowest
  same-spelling agreement of any shift pair *(measured)*.

The worked cell, `<<` on the input cell `whole|base_42 | whole|base_42`:

| language | canonical tokens |
|---|---|
| go | `whole:0`, `whole:184717953466368` |
| c++ | `whole:43008`, `whole:184717953466368` |
| java | `whole:43008`, `whole:184717953466368` |
| typescript | `fractional:43008.0`, `whole:-96757023244288` |
| dart | `whole:-96757023244288`, `whole:184717953466368` |
| rust | `raise:panic`, `whole:184717953466368` |
| python | `whole:184717953466368` |

- Decision 21's refusal to merge `whole` with `fractional` is what
  makes typescript's `fractional:43008.0` a different answer from
  java's `whole:43008` *(measured)*. It is the same number and it is
  not the same answer, and this pass exists to see that.

### 4.4 the first answer-grain contradicts, and it crosses the divide

The worked cell, `<=>` on the input cell
`fractional|base_1_5 | fractional|base_1_5`:

| language | canonical token |
|---|---|
| c++ | `ord:eq` |
| php | `whole:0` |
| ruby | `whole:0` |

- `cpp.<=>` disagrees with `php.<=>` on **211 of 211 shared cells**,
  and with `ruby.<=>` on **211 of 211** *(measured)*. Both are
  `contradicts_total` in the CORE's sense — same input, different
  answer, everywhere both accept — and both cross the static-and-open
  divide.
- The honesty this needs: **the totality is guaranteed by decision
  39**, which keeps c++'s comparison category — `std::partial_ordering`
  on this cell, `std::strong_ordering` on the integer ones — in a kind
  of its own rather than reading it as an integer.
- That is a real language difference. C++'s three-way comparison
  returns a comparison category and php's returns an `int`.
- It is also a decision that can be overturned, and the consequence of
  overturning it is stated here rather than left to be found. A reader
  who overturns decision 39 and maps `ord:lt`/`ord:eq`/`ord:gt` onto
  `whole:-1`/`whole:0`/`whole:1` will see these two contradictions
  vanish and a partial rate appear in their place.
- Level **measured** for the counts, **derived** for calling it a
  contradiction rather than a kind mismatch. Both readings are one
  comparison apart from the stored tokens.
- The third total pair, `kotlin...` against `rust...`, 112 of 112, is
  the same shape. Kotlin's `..` hands back a `LongRange` and rust's
  hands back a `Range<T>`. Decision 39 renders both as `range:`, and
  they still never coincide because their endpoint tokens differ
  *(measured)*.

---

## §5 — the answer-grain relations, all twelve

Restricted, as log 030's and log 031's relations were, to the same
operation spelled in two languages. **974 such language pairs**
*(measured)*.

| reading | pairs | disagree somewhere | disagree everywhere | cells | cell rate |
|---|---|---|---|---|---|
| open with open | 55 | 55 | 0 | 63,580 | 0.460 |
| static with static | 501 | 260 | 1 | 47,851 | 0.130 |
| static with open | 418 | 316 | 2 | 76,957 | 0.283 |
| **all** | **974** | **631** | **3** | **188,388** | **0.302** |

- **343 of 974 pairs agree on every shared cell** *(measured)*. Log 031
  found 11 of 55. The wider set finds a great many more, and most of
  them are inside the nine statically checked languages, where two
  languages with the same numeric tower answer the same thing
  everywhere their domains meet.
- **The CORE's `contradicts` is a boolean and the measurement is still
  a rate**, as log 031 said. What has changed is that the rate is no
  longer always strictly between 0 and 1. Three pairs sit at exactly
  1.000 and 343 at exactly 0.000. So the trichotomy's third arm now HAS
  instances, and it has them only where two languages answer in kinds
  that do not meet. Level **derived**.
- The open-with-open rate rose from log 031's reading because decision
  31 admitted raises. The same warning as §2 applies: the two numbers
  are not the same quantity.

The twelve-by-twelve mean same-spelling agreement, pooled over every
operation the pair both spells. Column headings are the languages in
the same order as the rows: python, ruby, php, go, rust, c++, java,
c-sharp, typescript, swift, kotlin, dart.

| | py | rb | php | go | rs | c++ | java | c# | ts | swift | kt | dart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| py | · | .498 | .752 | .941 | .906 | .847 | .763 | .735 | .643 | .977 | .734 | .778 |
| rb | .498 | · | .402 | .943 | .924 | .494 | .769 | .739 | .678 | .978 | .738 | .753 |
| php | .752 | .402 | · | .839 | .787 | .805 | .714 | .666 | .536 | .990 | .677 | .707 |
| go | .941 | .943 | .839 | · | .912 | .973 | .976 | .990 | .802 | 1.00 | .960 | .832 |
| rs | .906 | .924 | .787 | .912 | · | .940 | .932 | .934 | .795 | 1.00 | .895 | .805 |
| c++ | .847 | .494 | .805 | .973 | .940 | · | .912 | .915 | .599 | 1.00 | .884 | .863 |
| java | .763 | .769 | .714 | .976 | .932 | .912 | · | .864 | .860 | 1.00 | .925 | .926 |
| c# | .735 | .739 | .666 | .990 | .934 | .915 | .864 | · | .809 | .996 | .842 | .796 |
| ts | .643 | .678 | .536 | .802 | .795 | .599 | .860 | .809 | · | .962 | .880 | .888 |
| swift | .977 | .978 | .990 | 1.00 | 1.00 | 1.00 | 1.00 | .996 | .962 | · | 1.00 | .964 |
| kt | .734 | .738 | .677 | .960 | .895 | .884 | .925 | .842 | .880 | 1.00 | · | .888 |
| dart | .778 | .753 | .707 | .832 | .805 | .863 | .926 | .796 | .888 | .964 | .888 | · |

- **Swift's row is near 1.000 everywhere and means almost nothing.** It
  rests on six leaves and 400 input cells after decision 40 removed
  40.7 percent of swift's accepted set, and its only operations are
  comparisons and the two logicals *(measured)*. Read it as absent, not
  as agreement.
- **Ruby-against-php at 0.402 is the lowest pair in the table**, and
  ruby-against-python at 0.498 the second *(measured)*. The three
  open-dispatch languages disagree with each other more than any of
  them disagrees with a statically checked language, which is the
  wider-set version of log 031's central finding.
- **Go-against-c-sharp at 0.990 and go-against-java at 0.976** are the
  highest non-swift pairs *(measured)*. Go's `/` refusing what java's
  accepts is a domain fact that A never sees.

Per operation, pooled over every language pair that spells it:

| operation | pairs | shared cells | agreement | lowest pair | highest pair |
|---|---|---|---|---|---|
| `..` | 1 | 112 | 0.000 | kotlin vs rust | — |
| `<=>` | 3 | 1,578 | 0.158 | cpp vs php 0.000 | php vs ruby 0.215 |
| `\|\|` | 55 | 5,365 | 0.322 | php vs ruby 0.033 | swift vs ts 1.000 |
| `&&` | 55 | 5,365 | 0.352 | php vs ts 0.079 | swift vs ts 1.000 |
| `>>` | 45 | 5,077 | 0.394 | php vs ts 0.035 | go vs ruby 1.000 |
| `<<` | 45 | 5,077 | 0.425 | ruby vs ts 0.021 | csharp vs rust 1.000 |
| `^` | 45 | 5,471 | 0.458 | ruby vs ts 0.097 | ruby vs rust 1.000 |
| `+` | 45 | 16,672 | 0.535 | java vs php 0.180 | ruby vs rust 1.000 |
| `**` | 6 | 3,900 | 0.559 | python vs ruby 0.308 | php vs ts 0.951 |
| `%` | 55 | 8,135 | 0.599 | php vs ts 0.076 | java vs kotlin 1.000 |
| `\|` | 45 | 5,471 | 0.618 | ruby vs ts 0.104 | ruby vs rust 1.000 |
| `&` | 45 | 5,471 | 0.622 | ruby vs ts 0.090 | ruby vs rust 1.000 |
| `/` | 55 | 9,419 | 0.668 | php vs ruby 0.280 | java vs kotlin 1.000 |
| `-` | 45 | 9,567 | 0.726 | kotlin vs php 0.194 | ruby vs rust 1.000 |
| `<` `>` `>=` | 66 | 12,314 | 0.745 | php vs ruby 0.233 | swift vs ts 1.000 |
| `*` | 66 | 10,055 | 0.800 | go vs ts 0.500 | rust vs swift 1.000 |
| `!=` | 45 | 16,489 | 0.947 | java vs php 0.872 | python vs ts 1.000 |
| `==` | 55 | 22,513 | 0.951 | java vs php 0.872 | python vs ts 1.000 |
| `===` | 3 | 2,032 | 0.998 | php vs ts 0.995 | php vs ruby 0.998 |

- **The equality spellings are the agreement floor of the pass and the
  logicals and shifts are the ceiling of disagreement** *(measured)*,
  which is log 031's ordering, with `+` and the bitwise operators still
  in between.
- The wider set moves the relational operators DOWN from log 031's
  perfect scores, because php-against-ruby drags them.
- `python vs ruby` on `**` at 0.308 is the lowest pair for that
  operation, and it is a bignum-against-`Rational` difference rather
  than a cross-family one *(measured)*.

---

## §6 — what phase 4 still owes

- **The non-operator kinds are unmeasured for eleven of the twelve.**
  This pass, like every pass in the node, reads binary OPERATORS. The
  CORE's kind space also has indexing, calling, member access and
  iteration, and only the route-C manifests for python, ruby and php
  even enumerate holders that could carry them. Nothing here says
  anything about those, and phase 4 is not finished until it does.
  Level **unverified** that the operator picture generalises.
- **Kotlin's and swift's shifts are still pending the owner.** Kotlin spells
  them `shl` and `shr`. Swift spells them `<<` and `>>` but has no
  route-C rows in this material. Log 030 item 4k ruled them builtins
  and out of scope by the CORE's own rule, so the eleven-member shift
  group of §3.2 has two languages missing that might change it. That
  ruling has not been revisited and this pass does not revisit it.
- **Swift is measured in name only.** Six leaves, 400 input cells,
  1,066 of 2,618 accepted probes refused by the compiler that accepted
  them. Every swift number in §5 should be read as absent. The fix is a
  route-C build taken with full `swiftc` rather than
  `swiftc -typecheck`, which is log 032 §5's finding and is not this
  pass's to make.
- **Decision 31 changed a published quantity and the older logs were
  not re-run.** Log 031's A factors and log 033's are different
  measurements. Re-running `l3_answers.py` with raises admitted would
  make them one quantity and costs one flag. It has not been done, and
  until it is, the two logs' agreement numbers must not be read against
  each other.
- **Decision 37's container bridge is weak and its weakness is counted,
  not fixed.** 134 bridged container tokens *(measured)*. Every
  container answer holding a boolean or a null fails to meet its
  counterpart across the bridge, because the two printers spell those
  differently. A re-print of the three's route-C answers in the bits
  encoding would remove the whole bridge, and that is the right fix
  rather than more canonicalization.
- **Decision 22's float loss is now bounded and still real.** 13,179 of
  25,425 edges compare floats at 14 digits. 37 edges and 1,698 cells
  are known to be affected in the other direction *(measured)*. The
  nine do not need it and pay for the three.
- **Php's `and`, `or` and `xor` are still VOID** and still need a
  re-run rather than a repair — one pair of parentheses in
  `l3_routec.py`. Three leaves are missing from this picture for that
  reason.
- **Decision 26 and decision 27 are still open for the owner**, as log 031
  left them. The split rates in §3 are larger than log 031's, which
  makes decision 26's existential projection a bigger choice than it
  was. The universal reading is one comparison away from the stored
  sets.
- **The cross-check against `kind_signature_clustering` is still not
  started** — CHECK item 4j, the mutual-checkability symmetry the CORE
  opens with.
- **Rust's panic is a debug-build fact.** One release build, about a
  second, would settle whether `rust.+` joins the wrapping five, and
  would move a story in §4.2.

---

## §7 — artifacts

All of these live in
`PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

| file | what it is |
|---|---|
| `clusters_all12.json` | signatures, alphabet, bridge merges, merge history, sweep, contradicts |
| `dendrogram_all12.html` | the visual — self-contained, opens from disk |
| `l3_answers12.py` | the twelve-language driver |
| `l3_answers.py` | decisions 18 to 30 AND the bridge, decisions 31 to 42 |
| `make_dendrogram_all12.py` | writes the visual; reads only |
| `domstub.js` | the DOM stub the visual was validated under |
| `clusters_answers.json` | log 031's three-language result, unchanged |
| `clusters_final.json` | log 030's domain-grain result, unchanged |

Reproduce with two commands, neither of which starts a lane:

```
cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering && python3 l3_answers12.py
cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering && python3 make_dendrogram_all12.py
```

`cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering && python3 l3_answers.py`
still reproduces log 031's result exactly; the bridge is added beside
its decisions and its `main` is untouched.

The visual keeps every convention of `dendrogram_sweep.html` and
`dendrogram_answers.html` — the icicle rendering, the similarity axis,
the draggable threshold line, the live cluster count, the yellow
outline on the current clusters, the search box, the hover card, the
plateau table and the shaded cluster-count curve — with 226 leaves
labelled `language.operation`. The three-column agreement table could
not survive twelve languages, so it becomes the twelve-by-twelve matrix
of §5 with the per-operation roll-up beside it, and the known-fracture
table carries twelve columns.

**Validated under a DOM stub**, as log 030's visual was. Both scripts
run to completion with zero throws. The icicle and the curve each
append their drawing. `#count` reads **115** at the default threshold
0.700, which matches the [0.697, 0.730) plateau exactly. All five
innerHTML panels are written *(measured)*. Run it with
`cd PRIVATE/PseudoCoupHQ/Research/kind_fuzz_clustering && node domstub.js dendrogram_all12.html`.
