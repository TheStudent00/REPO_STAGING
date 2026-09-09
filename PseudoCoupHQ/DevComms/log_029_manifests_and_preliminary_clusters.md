# log 029 — layer 3 phase 4: frozen manifests and a preliminary clustering

Date: 2026-08-18 (later the same day than logs 027 and 028). Node:
`PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `PseudoCoupHQ/Research/kind_fuzz_clustering/`.

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
    language one question about one operation
    applied to two operands.
    example tied to context:
        `manifest_typescript.json` lists
        230,000 probes, and the worked line
        `P7_10_1_3_2` names one of them.

lane
    one batch job. it runs a planned set of
    probes and writes its output to raw text
    files. a lane has a short name.
    example tied to context:
        `vm_dart_01` is dart's second
        value-matrix lane; it exists as a
        script and was never queued.

shard, and the `__SUMMARY__` line
    one output chunk of a lane. a shard has
    landed only when it has printed a
    `__SUMMARY__` line stating how many
    probes that piece did.
    example tied to context:
        twenty-three of the twenty-six
        value-matrix shards have landed; the
        kotlin value-matrix lane's sixth
        shard landed during this session.

completeness gate (also: the gate)
    a check that decides whether a product is
    allowed to be read at all. here it reads
    a value matrix's own `complete` field and
    admits the matrix only if that field is
    true.
    example tied to context:
        seven matrices pass the gate;
        `valuematrix_dart` and
        `valuematrix_cpp` are REFUSED by it.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        in `manifest_typescript.json` holder
        7 is spelled `string` and holder 10
        is spelled `array`.

layer-1 form (also: form)
    the coarse kind a holder belongs to,
    shared across all twelve languages.
    there are eight of them.
    example tied to context:
        holder 7's form is `text` and holder
        10's form is `sequence`.

value class
    a named family of test values put into a
    holder, chosen so awkward cases are
    covered. a manifest records each one's
    literal declaration text.
    example tied to context:
        holder 7's value class 1 is
        `base_hello`; holder 10's value class
        3 is `mixed`.

cell (also: pair cell, form-pair cell)
    one combination of two operand kinds that
    an operation was asked about. a pair cell
    is a pair of holders. a form-pair cell is
    a pair of forms.
    example tied to context:
        typescript has 12,167 pair cells, and
        the shared form space is 64 ordered
        form-pair cells for every language.

split cell
    a pair cell where the verdict moved with
    the VALUE rather than with the pair of
    holders.
    example tied to context:
        kotlin has 1,234 split cells of
        11,492, the most of any language
        measured here.

route A, route C
    two ways a language is measured. a
    route-A language is compiled, so a probe
    gets an ACCEPT or REFUSE verdict. a
    route-C language is run directly, so the
    only evidence is what execution did.
    example tied to context:
        nine languages here are route A;
        python, ruby and php are route C.

ANSWER, RAISE, REFUSE, BUDGET
    the four things a route-C probe can do:
    return a value, throw, be rejected, or
    run out of its allowance.
    example tied to context:
        decision 3 counts only ANSWER as
        acceptance for python, ruby and php.

acceptance grid
    the per-language table of which pair
    cells the language accepted, probed with
    ONE value per holder.
    example tied to context:
        go's acceptance grid is exactly right
        on all 7,600 of its pair cells.

value matrix
    the per-language table taken over the
    FULL cross product of value classes, not
    one value per holder.
    example tied to context:
        typescript's value matrix disagrees
        with typescript's acceptance grid on
        704 cells.

manifest
    a frozen file listing what was probed for
    one language under one plan: its
    operation menu, its holders, its value
    classes, its shard plan and every row in
    enumeration order. it is written once and
    not edited afterwards.
    example tied to context:
        the twelve `manifest_<lang>.json`
        files, which let `P7_10_1_3_2` decode
        without the generator module.

open-dispatch language
    a language whose acceptance is decided at
    run time rather than by a checker, so it
    has no acceptance verdict separate from
    execution.
    example tied to context:
        python, ruby and php are the three
        open-dispatch languages, and they
        have no value matrix by design.

form projection (also: the projection)
    replacing every holder by its layer-1
    form, so that two languages which share
    no holders can be compared.
    example tied to context:
        decision 1 is the projection, and it
        is what makes the shared space the
        same 64 ordered form pairs for every
        language pair.

domain
    the set of form-pair cells an operation
    actually accepted. cells the language
    refused are not in the domain.
    example tied to context:
        `go.+` has a domain of 3 cells and
        `dart.==` has a domain of 64.

density
    the same cell counted under the stricter
    readings — every holder pair accepting,
    or a majority of them — stored beside the
    existential reading.
    example tied to context:
        decision 2 stores density so that
        overturning the existential rule
        costs a re-read and not a re-run.

signature (also: operation signature)
    one operation of one language, together
    with everything recorded about it: its
    domain, its density, and for route C its
    answer classes.
    example tied to context:
        this pass has 233 operation
        signatures, of which 229 have a
        non-empty domain.

Jaccard
    a closeness number for two domains: the
    count of cells in both, divided by the
    count of cells in either.
    example tied to context:
        `cpp.+` against `go.+` scores 0.167.

similarity
    the Jaccard number read as closeness, so
    that 1.0 is identical domains and 0.0 is
    disjoint ones.
    example tied to context:
        the relation edges are restricted to
        pairs that share a spelling or score
        at least 0.5 similarity.

average linkage
    a way of measuring how far apart two
    groups are: the mean distance over every
    pair with one member from each group.
    example tied to context:
        decision 5 clusters by average
        linkage over 1 minus Jaccard.

clustering
    the arrangement built from those
    distances: it repeatedly joins the two
    closest groups until one group is left.
    example tied to context:
        the clustering here is PRELIMINARY,
        and every artifact it writes says so
        in its first field.

threshold (also: the cut)
    a similarity chosen to stop reading the
    clustering at. every cut gives some
    number of clusters. nothing in the data
    picks one.
    example tied to context:
        the 0.70 cut gives 46 clusters and
        the 0.85 cut gives 58.

relation, and its four names
    a measured statement about two
    signatures' domains over the shared
    space. EQUALS is identical domains. NESTS
    is one domain strictly containing the
    other, with the contained one non-empty.
    NESTED_BY is the same edge read from the
    other side. OVERLAPS is domains that
    intersect with neither containing the
    other. CONTRADICTS is reserved for the
    SAME SPELLED operation in two languages
    whose domains are disjoint while both are
    non-empty.
    example tied to context:
        `cpp.+` NESTS `go.+`; `dart.||`
        CONTRADICTS `go.||`.

the mixed-holder statistic
    among accepted probes whose two operands
    carry the SAME layer-1 form, the fraction
    whose HOLDERS differ. it is measured at
    holder grain, by code that names no
    operation and no language.
    example tied to context:
        go's `<<` scores 0.75, 12 of 16, and
        go's `+` scores 0.00, 0 of 7.

the shift exemption
    the observation that in several
    statically checked languages a shift may
    take two operands of DIFFERENT integer
    holders where arithmetic may not.
    example tied to context:
        this log rediscovers it from the
        mixed-holder statistic and then finds
        it is sharp in only two of the five
        languages it had been claimed for.

overlay
    the value matrix read as a separate
    second reading laid beside the acceptance
    grid, and reported as a difference,
    rather than being used as the domain
    itself.
    example tied to context:
        decision 9 keeps the matrices as an
        overlay so that no similarity moves
        because of WHICH LANE FINISHED.

declaration-alone lane
    a lane that declares a value in a holder
    and applies no operation, so it can tell
    apart a holder that could not hold the
    value from an operation that moved.
    example tied to context:
        the nine `ld_<lang>_00.sh` lanes,
        1,046 probes, about 21 seconds total,
        still queued behind the matrix.

decision <n>
    a numbered ruling this node has made,
    kept so it can be overturned by number.
    this log makes eleven of them.
    example tied to context:
        decision 8 is the completeness gate;
        decision 6 is the relation rule.
```

---

## what came before this log, restated

Every fact this log borrows from an earlier log or from the CORE is
stated here in full, so no sentence below depends on opening another
file.

- **Log 027 built and ran phase 3.** It produced the nine route-A lane
  scripts, each of which embeds a gzipped `table.json` written at
  generation time and never touched since.
- **Log 028 closed the phase-3 work and recorded four facts this log
  uses.**
  - Typescript narrows each variable to its literal type, so a
    typescript verdict genuinely moves with the value rather than only
    with the pair of holders.
  - Typescript's 876 split cells are all layer-3 movement — the
    operation moving — rather than layer-2 leakage, where the holder
    could not hold the value *(measured, log 028)*.
  - Java's certification pass produced 146 findings, every one of them
    javac accepting where the lifted table is silent, and every one of
    them binary numeric promotion.
  - Dart's `dynamic` holders switch dart's checker off, and HARVEST
    already warns that 388 of dart's 1,170 accepts involve one.
  - The tree-sitter grammar parses swift's `+` through a catch-all
    `custom_operator` node, so swift's operator menu is six operations
    rather than nineteen.
- **The CORE's ruling 1 says the form projection is lossy in a stated
  place.** `Decimal(42) + Fraction(42)` raises even though both operands
  hold one layer-1 form.
- **The CORE's ruling 5 says route C has no separate acceptance
  verdict.** For python, ruby and php, execution is the only evidence.
- **The CORE defines `contradicts` at answer grain** — the same input
  giving a different answer — and asks for dominance between operations
  to be DISCOVERED rather than assumed, with three possible outcomes:
  one dominates, the other dominates, or neither does and the split is
  justified by measurement.
- **The CORE's phase-4 pair is {domain accepted, answer per input}**,
  and its own rule excludes builtins from the operator vocabulary.
- **The standing rule on disagreements** is that a finding is recorded
  and never reconciled silently.

This log does the two jobs phase 4 opens with — freeze the manifests,
then cluster what is already complete. The clustering is
**PRELIMINARY** and every artifact it writes says so in its first
field.

---

## §1 — walkthrough, in plain words

A raw result line from this node looks like `P7_10_1_3_2|ACCEPT|OK`.
That is all it looks like.

- The identifier is **positional**. It says "holder 7 on the left,
  holder 10 on the right, that holder's value class number 1, this
  one's number 3, operation number 2".
- It says nothing about which holders those are.
- The lists it counts against live in a python module that is going to
  keep changing.

So the first job was to write the lists down — once, in full, beside
the data. That is what the twelve `manifest_<lang>.json` files are.

- They are a **replay of the generator's enumeration with no probes
  run**. The generator is deterministic, so walking its loops again
  reproduces the exact identifier order without invoking a single
  compiler.
- Every identifier now decodes to the literal declaration text of both
  operands, forever, without the module that made it.

The manifests verify, and they verify two ways that do not share a code
path.

- **First way, against the raw files.** **All twelve line counts match**
  the raw files that have landed, and **520 of 520 spot-checked
  identifiers resolve to a probe that is actually present in its raw
  file** *(measured)*.
- **Second way, against each lane's own frozen table.** Each phase-3
  lane script carries its own gzipped copy of the holder table, frozen
  at generation time, and **all nine route-A manifests agree with their
  lane's embedded table on operations, holders and value classes — zero
  mismatches** *(measured)*. This way trusts the replay not at all.

Then the second job. Since log 028 was written the value-matrix lanes
kept running, and the picture has moved a long way.

- **Twenty-three of the twenty-six shards have landed**, and **seven
  languages' value matrices are now COMPLETE** — typescript, csharp,
  java, rust, go, swift and kotlin *(measured)*.
- Two are not, and the two are not the same case.
  - **C++ had not started.** That is a wait.
  - **Dart's second shard was never queued at all.** That is a gap, not
    a delay, and it is the one thing in this log that needs an action
    rather than a wait.
- Nothing was disturbed to find any of this out. The running lane was
  left strictly alone and only shards whose own status file said `done`
  were copied.
- Kotlin's sixth and last shard finished partway through this session
  and was folded in on a second pass. That is why kotlin appears as
  admitted here and would have appeared as refused an hour earlier. The
  completeness gate is doing exactly its job.

**The headline is that the machinery rediscovered the shift exemption,
and then corrected the way we had been stating it.**

- The shift exemption is the observation that in several statically
  checked languages a shift may take two operands of DIFFERENT integer
  holders where arithmetic may not.
- It is a claim about holders, and the cross-language form projection
  deliberately destroys holders.
- So it was measured separately, by the mixed-holder statistic, which
  names no operation and no language: among accepted probes whose two
  operands carry the same layer-1 form, what fraction have DIFFERENT
  holders.
- Ranked, the shifts come out on top — `>>>` at 0.80, `<<` and `>>` at
  0.619 mean, against `+` at 0.482, `-` at 0.384 and `*` at 0.325
  *(measured)*. So it falls out.

But the per-language table underneath that ranking says something the
old phrasing did not. The five languages we had been naming together
are two different phenomena.

- **In go and rust the exemption is total.** Shifts run 0.75 mixed
  while `+`, `-` and `*` run **0.00, 0.00 and 0.00** in go and **0.14,
  0.00, 0.00** in rust *(measured)*.
- **In c++, c-sharp and java it is barely there.** Java's shifts are
  0.80 and java's `+` is 0.78 *(measured)*. Those languages promote
  numeric operands implicitly, so their arithmetic is already mixed and
  there is nothing for a shift to be exempt from.

That is a finding about the claim, produced by the method rather than
fed to it.

The other thing worth saying up front is what the machinery caught by
accident.

- Seven of the relation edges are **contradicts** — the same spelled
  operation in two languages with completely disjoint domains — and
  **all seven involve dart's `||`** *(measured)*.
- Chased down, dart accepts `bool && bool` and **refuses `bool ||
  bool`, with an empty error detail** *(measured)*.
- That is not a fact about dart. It is a probable fault in dart's own
  probe harness.
- The relation machinery found it by noticing that one language
  disagreed with all eight others about the most boring operation in
  the set.

---

## §2 — the manifests, frozen

`l3_manifest.py` writes them. It runs as an **ordinary process, not as
a lane**.

- Nothing is written into the sandbox agent's drop directory, so
  nothing queued behind the value matrix.
- The running shard was not perturbed.
- That is the answer to the earlier question of "host-side or a tiny
  lane queued last": neither was needed, because the job runs no probes.

- **what a manifest contains.**
    - the operation menu, in generator order
    - the holder table: index, layer-1 form, holder spelling, any
      preamble, and every value class with its **literal declaration
      text**
    - the identifier grammar and a prose decode rule
    - the shard plan, replaying the phase-3 sharding arithmetic, so a
      raw file's name maps to its row range
    - every row, in enumeration order
- **the two identifier grammars.** Route A is
  `P{i}_{j}_{x}_{y}_{k}`, all five fields numeric. Route C is
  `P{i}_{j}_{vca}_{vcb}_{op}`, where the last three are NAMES, not
  indices. Value-class names and operation spellings both contain
  underscores, so the manifest states in writing that a route-C
  identifier is decoded by matching against the enumeration and
  **never by splitting the string on underscores**.

| language | route | manifest probes | shards landed | line counts match |
|---|---|---|---|---|
| typescript | A | 230,000 | 2 of 2 | yes |
| dart | A | 217,073 | 1 of 2 | yes |
| csharp | A | 397,620 | 4 of 4 | yes |
| java | A | 444,020 | 4 of 4 | yes |
| rust | A | 205,504 | 2 of 2 | yes |
| go | A | 167,884 | 2 of 2 | yes |
| swift | A | 76,614 | 2 of 2 | yes |
| kotlin | A | 253,028 | 6 of 6 | yes |
| cpp | A | 229,900 | 0 of 6 | n/a, in flight |
| python | C | 342,225 | — | yes |
| ruby | C | 261,382 | — | yes |
| php | C | 215,306 | — | yes |

- **verification, first way — replay against raw.** For every landed
  shard the manifest's row count for that shard is compared with the
  raw file's line count. A shard counts as landed **only if it printed
  its `__SUMMARY__` line**; a raw file without one is a lane still
  writing, and its short count is progress, not a manifest fault. All
  landed shards match *(measured)*.
- **verification, second way — spot decode.** Twenty random rows per
  landed shard are expanded to full probe records and looked up in the
  raw file. **520 of 520 present** *(measured)*. Where the language
  also has an acceptance grid the decoded verdict is compared against
  it: **460 of the 520 are grid-comparable, and 449 of those 460
  agree** *(measured)*. The eleven that differ are **not** manifest
  faults: **all eleven were checked cell by cell against the value
  matrix and every one lands on a cell the matrix independently
  classified as `split`** *(measured, 11 of 11)*. The verdict moved
  with the VALUE rather than the holder pair, so the grid and the
  matrix are both right about different values of one cell. Nothing
  in the manifests is implicated.
- **verification, third way — against the lane's own frozen table.**
  This one is the important one, because the first two both run
  through the same enumeration code the manifest is a replay of, so a
  shared fault would pass both. Each phase-3 lane script embeds a
  gzipped `table.json` written at generation time and never touched
  since. Decoding it out of the shell script and comparing gives
  **nine of nine languages agreeing on the operation menu, on every
  holder's form and spelling, and on every value class in order — zero
  mismatches** *(measured)*.
- **in-flight runs get manifests too.** C++ has landed nothing and has
  a complete manifest. Kotlin had five of six shards when its manifest
  was first written and six by the time it was verified again, and the
  manifest did not change — because it never depended on a result
  existing. That is the point of freezing now rather than at harvest.

A raw line decodes like this, and this is the whole
of what a reader needs:

```
P7_10_1_3_2  ->  manifest_typescript.json
  operations[2]           = "*"
  holders[7].form         = "text"
  holders[7].holder       = "string"
  holders[7].vc[1]        = base_hello
  holders[10].form        = "sequence"
  holders[10].holder      = "array"
  holders[10].vc[3]       = mixed
```

---

## §3 — the method, stated fully

Eleven numbered decisions. **Every one is overturnable** and they are
numbered so the owner can overturn them one at a time rather than having to
reject the pass whole. They are reproduced verbatim in
`clusters_preliminary.json` and `clusters_preliminary.md`.

1. **HOLDER-TO-FORM PROJECTION.** A language's acceptance grid is at
   holder grain, and two languages do not share holders, so nothing
   can be compared until both are projected onto the layer-1 forms
   they DO share. Every holder is replaced by its form and a domain
   becomes a set of ordered FORM pairs. All twelve languages carry all
   eight forms, so the shared space is the same 64 ordered pairs for
   every language pair — no pair-specific restriction is needed.
   Overturnable: the projection is lossy exactly where CORE ruling 1
   said it would be (`Decimal(42) + Fraction(42)` raises though both
   hold one form), so a holder-grain comparison remains available for
   language pairs that have a holder correspondence.
2. **EXISTENTIAL PROJECTION RULE.** A projected form-pair cell counts
   as ACCEPTED if AT LEAST ONE holder pair with those forms was
   accepted. Rationale: the question a domain answers is "can this
   operation take these forms at all", which is existential. The
   alternatives — universal (all holder pairs accept) and majority —
   are computed and stored alongside as `density` so overturning this
   costs a re-read and not a re-run.
3. **ROUTE-C DOMAIN RULE.** For python, ruby and php acceptance does
   not exist as a separate verdict; execution is the only evidence
   (CORE ruling 5, route C). A cell counts as ACCEPTED there if at
   least one probe returned ANSWER. RAISE, REFUSE and BUDGET all count
   as not-accepted. Overturnable: RAISE is arguably "accepted then
   failed", which would widen these three domains.
4. **SIMILARITY MEASURE.** Jaccard on the ACCEPT sets over the 64
   shared form pairs: intersection over union. Chosen because it
   ignores the enormous agreed-REFUSE background that would make every
   pair of operations look about 90 percent alike under plain
   agreement. An operation with an EMPTY domain is excluded from
   clustering entirely rather than being scored 0 against everything.
5. **CLUSTER CUT.** Average-linkage agglomerative over 1 minus
   Jaccard, cut at similarity 0.70. The 0.85 cut is computed too and
   reported beside it, because the honest thing to show is how much
   the picture moves with the threshold. Nothing in the data picks
   0.70; it is a reading choice.
6. **RELATIONS.** Over the shared space: NESTS if one accept set
   strictly contains the other and the contained one is non-empty;
   OVERLAPS if they intersect and neither contains the other;
   CONTRADICTS is reserved for the SAME SPELLED operation in two
   languages whose accept sets are disjoint while both are non-empty.
   Overturnable: "contradicts" in the CORE is defined at the answer
   grain (same input, different answer) and only three languages have
   answers, so this is the acceptance-grain reading of it and is
   labelled as such.
7. **THE MIXED-HOLDER STATISTIC IS COMPUTED, NEVER ASSERTED.** The
   shift exemption is a claim about HOLDERS, which the form projection
   destroys, so a second statistic is measured at holder grain: among
   accepted probes whose two holders share one form, the fraction
   whose holders DIFFER. No operation and no language is named in the
   code that computes it. Whether the shifts separate out is then an
   observation about the data, not a restatement of the input.
8. **PRELIMINARY SCOPE, AND THE COMPLETENESS GATE.** Only completed
   artifacts are read. The nine acceptance grids and the three route-C
   behavior tables are complete and are read in full. A value matrix
   is read ONLY if its own `complete` field is true — the gate, not
   the file's existence, decides. Reading a part-finished lane would
   produce a domain that shrinks for a reason that is not a fact about
   the language, which is the error this gate exists to prevent. At
   this pass SEVEN matrices pass the gate (typescript, csharp, java,
   rust, go, swift, kotlin — kotlin's sixth and last shard landed
   during this session) and two do not: cpp, which had not started,
   and dart, whose second shard was never queued at all, a gap rather
   than a wait.
9. **THE VALUE MATRIX IS AN OVERLAY, NOT THE PRIMARY DOMAIN.** The
   clustering proper runs on the acceptance grids for ALL TWELVE
   languages. It would be a measurement artifact to widen six
   languages' domains with value-matrix evidence and not the other
   six: every cross-language similarity involving a gated language
   would then move for a reason about WHICH LANE FINISHED rather than
   about the languages. So the matrices are read as a separate overlay
   and reported as a delta. Overturnable when all nine matrices land,
   at which point the overlay should simply BECOME the primary domain
   for the nine statically checked languages.
10. **OVERLAY RULE, EXISTENTIAL OVER VALUES.** In an admitted matrix a
    (operation, lhs holder, rhs holder) cell counts as accepted if AT
    LEAST ONE value combination accepted — the same existential
    posture as decision 2, one layer down. A `split` cell (verdict
    moved with the VALUE, not the holder pair) therefore counts as
    accepted. This is the widest reading and it is chosen
    deliberately, because the overlay's job here is to BOUND how wrong
    the one-value-per-holder acceptance grid could be, and a bound
    wants the extreme.
11. **THE OVERLAY MEASURES THE GRID'S ERROR.** For each admitted
    language the count of cells where the grid and the existential
    overlay disagree is reported. That number is the honest error bar
    on every domain in this pass, including the domains of the six
    languages that have no matrix yet — there is no reason to think
    their grids are better behaved than the measured ones.

The overlay, run under that gate:

| language | gate | pair cells | split cells | grid disagrees | operations widened |
|---|---|---|---|---|---|
| typescript | admitted | 12,167 | 876 | 704 | 8 |
| csharp | admitted | 18,000 | 718 | 18 | 3 |
| java | admitted | 20,480 | 759 | 30 | 0 |
| rust | admitted | 9,196 | 136 | 14 | 7 |
| go | admitted | 7,600 | 103 | 0 | 0 |
| swift | admitted | 3,456 | 9 | 6 | 3 |
| kotlin | admitted | 11,492 | 1,234 | 150 | 2 |
| dart | REFUSED | — | — | — | — |
| cpp | REFUSED | — | — | — | — |

- **read that table as the error bar on this whole pass.**
    - **Go's grid is exactly right** — 7,600 of 7,600 cells agree with
      the full value cross product *(measured)*.
    - **Typescript's grid is the worst measured** — wrong on **704 of
      12,167 cells, 5.8 percent** *(measured, derived percentage)*. The
      reason is the one log 028 established and which is restated
      above: typescript narrows each variable to its literal type, so
      the verdict genuinely moves with the value.
    - Kotlin is next at **150 of 11,492, 1.3 percent**, and the rest sit
      between 0 and 0.15 percent.
- **kotlin has the most value-dependent cells of any language
  measured** — **1,234 splits of 11,492 cells, 10.7 percent**
  *(measured, derived percentage)*, half again typescript's 7.2
  percent.
    - The two numbers are not the same statistic. A cell can split
      without the grid being WRONG about it.
    - That is why kotlin splits more than typescript and errs ten times
      less often. Level **derived** on the distinction.
- level **derived**, and worth stating as a limit: c++ and dart have
  **no error bar at all** here, and neither do the three open-dispatch
  languages, which have no matrix by design.

---

## §4 — clusters, with worked examples

**46 clusters at the 0.70 cut, 58 at 0.85** *(measured)*, over **233
operation signatures**, of which **229 have a non-empty domain** and 4
are empty and excluded — `csharp.is`, `java.instanceof`, `kotlin.&`
and `python.@` *(measured)*.

### the `+` story

`+` does **not** cluster together. It splits three ways, and the split
is by how much implicit conversion the language does, not by
anything about `+`.

| language | `+` domain size | `text\|text` | `whole\|whole` | `sequence\|sequence` |
|---|---|---|---|---|
| go | 3 | yes | yes | no |
| rust | 3 | yes | yes | no |
| typescript | 19 | yes | yes | no |
| cpp | 18 | yes | yes | no |
| csharp | 32 | yes | yes | no |
| java | 32 | yes | yes | no |
| kotlin | 38 | yes | yes | yes |
| python | 20 | yes | yes | yes |
| ruby | 14 | yes | yes | yes |
| php | 32 | yes | yes | yes |
| dart | — | — | — | — |
| swift | — | — | — | — |

- **the one thing every `+` agrees on.** Every language that has a `+`
  at all accepts **`whole|whole` and `text|text`** *(measured)*. That
  is the entire agreed core: ten languages out of ten, two cells out
  of sixty-four.
- **string-concat does not land apart from numeric `+`.** This was the
  open question and the answer is clean: **no language in the set has
  a separate concatenation operation whose domain is text-only**. In
  all ten, `text|text` sits inside the same `+` signature as
  `whole|whole`.
    - The place the languages differ is whether `+` will also take
      `text|whole`.
    - **Will coerce across forms:** c++, c-sharp, java and typescript
      *(measured)*.
    - **Will not coerce across forms:** go and rust *(measured)*.
    - So the interesting boundary is not concat-versus-arithmetic. It is
      **whether the language will coerce across forms**, which is a
      property of the language and not of the operator.
- **go and rust's `+` is the narrowest operation in the whole pass**
  at 3 cells, and it **nests inside** every other `+`. Worked
  example, verbatim from the relation edges: `cpp.+` contains `go.+`,
  shared `fractional|fractional`, `text|text`, `whole|whole`;
  only-in-c++ `fractional|truth`, `fractional|whole`,
  `sequence|truth`, `sequence|whole`, `text|truth`, `text|whole`
  *(measured)*. Every one of the six extra cells is c++ converting
  something to a number.
- **`sequence|sequence` is the dividing line between the two families
  of language.**
    - **Accept it, meaning list concatenation:** kotlin, python, ruby
      and php *(measured)*.
    - **Refuse it:** the other six *(measured)*.
    - Kotlin is the only statically checked language on the accepting
      side.

### the shift story

Shifts DO form their own cluster, and they take the bitwise
operations with them.

- **cluster 5 at the 0.70 cut, 12 members over 3 languages**:
  `go.%`, `go.&`, `go.&^`, `go.<<`, `go.>>`, `go.^`, `go.|`,
  `java.<<`, `java.>>`, `java.>>>`, `rust.<<`, `rust.>>`
  *(measured)*. That is a **cross-language shift-and-bitwise
  cluster** and nothing in the input grouped them; they arrive
  together because their domains are all "two whole things and
  nothing else".
- **cluster 6, 10 members over 2 languages**: `cpp.%`, `cpp.&`,
  `cpp.<<`, `cpp.>>`, `cpp.^`, `cpp.|`, `python.&`, `python.<<`,
  `python.>>`, `python.^` *(measured)* — the same shape, and it
  crosses the static/open-dispatch divide, which is the first
  cross-family cluster this node has produced.
- **the mixed-holder statistic, ranked, statically checked languages
  only** *(measured)*:

| operation | mean mixed-holder ratio | signatures |
|---|---|---|
| `>>>` | 0.800 | 1 |
| `<<` | 0.619 | 7 |
| `>>` | 0.619 | 7 |
| `+` | 0.482 | 7 |
| `==` | 0.446 | 8 |
| `!=` | 0.409 | 7 |
| `<` | 0.394 | 9 |
| `-` | 0.384 | 7 |
| `%` | 0.371 | 8 |
| `*` | 0.325 | 9 |
| `&&` | 0.207 | 9 |
| `\|\|` | 0.207 | 9 |

- **the exemption is rediscovered** — the three shift spellings are
  the top three, above every arithmetic and every comparison
  *(measured)*. It was not hard-coded; the code that produced this
  ranking names no operation.
- **and the exemption is not one phenomenon.** Per language
  *(measured)*:

| language | `<<` | `>>` | `+` | `-` | `*` |
|---|---|---|---|---|---|
| go | 0.75 (12/16) | 0.75 (12/16) | 0.00 (0/7) | 0.00 (0/6) | 0.00 (0/6) |
| rust | 0.75 (12/16) | 0.75 (12/16) | 0.14 (1/7) | 0.00 (0/6) | 0.00 (0/6) |
| cpp | 0.71 (12/17) | 0.71 (12/17) | 0.64 (16/25) | 0.64 (14/22) | 0.67 (14/21) |
| csharp | 0.73 (8/11) | 0.73 (8/11) | 0.70 (26/37) | 0.64 (16/25) | 0.64 (16/25) |
| java | 0.80 (20/25) | 0.80 (20/25) | 0.78 (32/41) | 0.76 (22/29) | 0.76 (22/29) |
| dart | 0.60 (3/5) | 0.60 (3/5) | — | — | 0.50 (6/12) |
| typescript | 0.00 (0/3) | 0.00 (0/3) | 0.50 (4/8) | 0.00 (0/3) | 0.00 (0/3) |

Three readings, named against each other.

- **go and rust: the exemption is total.** Shifts 0.75, arithmetic 0.00
  to 0.14. In go a `+` may not cross holders at all, and a shift may,
  in 12 of 16 accepted same-form cases.
- **c++, c-sharp and java: the exemption is barely measurable.** Java's
  shifts are 0.80 and java's `+` is 0.78, a gap of 0.02.
    - The cause is not that shifts are less permissive there.
    - The cause is that arithmetic is MORE permissive, through implicit
      numeric promotion.
    - Level **derived** for the promotion attribution; the ratios
      themselves are measured.
    - Log 028's 146 java certification findings — all of them javac
      accepting where the lifted table is silent, all of them binary
      numeric promotion, as restated above — are independent support
      for the same mechanism.
- **typescript inverts it**: shifts 0.00, `+` 0.50 *(measured)*.

So the phrasing "the shift mixed-holder exemption in go, rust, c-sharp,
c++ and java" **over-groups**. It is sharp in exactly two of the five.
Level **derived**.

### where `==` lands

| language | `==` domain size (of 64) |
|---|---|
| rust | 8 |
| go | 18 |
| cpp | 20 |
| csharp | 24 |
| java | 26 |
| typescript | 28 |
| kotlin | 52 |
| dart | 64 |
| python | 64 |
| ruby | 64 |
| php | 64 |

- `==` is the **widest operation in eight of the twelve languages**
  and it is the cleanest single-number picture of a language's
  strictness this pass produced *(measured)*.
- **four languages accept `==` on all 64 cells** — dart, python, ruby
  and php.
    - Dart is the surprise on that list. It is statically checked and it
      lands with the three open-dispatch languages.
    - Level **derived**, and the cause is the log 028 fact restated
      above: dart's `dynamic` holders switch the checker off, and
      HARVEST already warns that 388 of dart's 1,170 accepts involve
      one.
- **rust's `==` at 8 cells is the strictest equality measured**, level
  with rust's own `<` at 8 *(measured)*. **In nine of the eleven
  languages that have both, `==` is strictly wider than `<`** — go 18
  against 3, java 26 against 4, kotlin 52 against 9, dart 64 against
  14 *(measured)*. The two exceptions are rust, where both are 8, and
  php, where both are 64. Equality is where a language relaxes first,
  and rust is the one language that does not.
- the largest cluster at the 0.70 cut, **34 members over 4
  languages**, is built almost entirely out of comparisons and
  equality — `dart.==`, `kotlin.==`, `kotlin.!=`, `kotlin.?:`,
  `php.==`, `php.===`, `php.!=`, `php.!==`, `php.<`, `php.<=`,
  `php.>`, `php.<=>` and more *(measured)*. The permissive
  comparisons of the permissive languages collapse into one blob,
  which is expected and is mostly a statement that the Jaccard measure
  cannot separate operations that accept everything.

---

## §5 — relations, with examples

**2,909 relation edges** *(measured)*, restricted to cross-language
pairs that either share a spelling or score at least 0.5:

| relation | count |
|---|---|
| nested_by | 1,009 |
| equals | 687 |
| overlaps | 618 |
| nests | 588 |
| contradicts | 7 |

- **NESTS — this is dominance, discovered.** Verbatim:
  `cpp.+` contains `go.+`, jaccard 0.167; shared
  `fractional|fractional`, `text|text`, `whole|whole`; only in c++
  `fractional|truth`, `fractional|whole`, `sequence|truth`,
  `sequence|whole` *(measured)*. The CORE asked for dominance to be
  discovered rather than assumed and this is the shape it arrives in:
  c++'s `+` does everything go's `+` does and six things more, so on
  this evidence c++'s `+` dominates go's.
- **EQUALS — 687 edges, and they are the most useful ones.** An
  `equals` edge between two languages' identically spelled operation
  is the statement "these are one thing in two spellings", which is
  precisely the discovered kind map phase 4 is for. Level **derived**
  as to significance; the edges are measured.
- **OVERLAPS — union candidates.** Verbatim: `cpp.!=` and
  `csharp.!=`, jaccard 0.571; shared `fractional|fractional`,
  `fractional|nothing`, `fractional|whole`, `nothing|fractional`;
  only in c++ `fractional|truth`, `truth|fractional`, `truth|whole`,
  `whole|truth`; only in c-sharp `keyed|keyed`, `keyed|nothing`,
  `nesting|nesting`, `nesting|nothing` *(measured)*. Read plainly, and
  as two statements rather than one:
    - **c++ will compare a truth value against a number, and c-sharp
      will not.**
    - **C-sharp will compare two references, and c++ will not.**
    - Neither dominates, and the split is justified by measurement,
      which is exactly the third arm of the CORE's trichotomy.
- **CONTRADICTS — 7 edges, all one operation, and it is a bug.**
  Verbatim: `dart.||` against `go.||`, jaccard 0.0; only in dart
  `nothing|nothing`, `nothing|truth`; only in go `truth|truth`
  *(measured)*. The same edge exists against c++, c-sharp, java,
  kotlin, rust and swift — **all seven** *(measured)*.
    - chased to the cell: dart's grid records
      `bool && bool` **ACCEPT** and `bool || bool` **REFUSE, with an
      empty error detail** *(measured)*.
    - a refusal with no error text, on the one cell every other
      language in the set accepts, next to `&&`, a co-operation in
      the same menu that does accept it. Level **unverified** as to cause, but the reading is
      that this is dart's probe harness and not dart. It is recorded
      as a finding and NOT reconciled silently, per the standing rule.
    - the point worth keeping: **the relation machinery found a
      probable instrument fault without being asked to look for one**,
      by noticing that one language contradicted eight others about
      the dullest operation in the vocabulary.

Two instrument facts shape every table above. Both are already on the
record and both are restated because they explain gaps.

- **Swift has 6 operations, not 19.** Its tree-sitter grammar parses
  `+` through `custom_operator`, as log 028 recorded and as restated at
  the top of this log. So swift has no `+` row anywhere in this log.
- **Dart's menu has 17 operations and contains no `+`, no `-` and no
  `!=`** *(measured, read from `manifest_dart.json`)*. Same class of
  fact, newly stated: dart's absence from the `+` table is the
  grammar's doing, not a refusal.

---

## §6 — what this pass can and cannot claim

**Can claim, level measured:**

- the twelve manifests are frozen, and a positional raw line from any
  of the twelve runs decodes without the generator, verified three
  ways including one that does not share the manifest's code path.
- 233 operation signatures over twelve languages, on the shared
  64-cell form space, with domains, densities and — for python, ruby
  and php — answer-class maps per cell.
- 46 clusters at 0.70, 58 at 0.85, with the full membership recorded.
- 2,909 relation edges across the four kinds.
- the shift exemption, rediscovered by a statistic that names no
  operation, and sharply present in go and rust only.
- the acceptance grid's error bar, for seven languages: 0 cells wrong
  in go, 150 of 11,492 in kotlin, 704 of 12,167 in typescript.

**Cannot claim:**

- **that any domain here is final.** Every domain rests on the
  acceptance grid, which probes **one value per holder**, and the
  overlay measures that grid as wrong on up to 5.8 percent of cells
  where it can be checked. C++ and dart cannot be checked at all yet,
  and the three open-dispatch languages never will be by this route.
- **anything about answers outside python, ruby and php.** The value
  matrix produces verdicts, not answers. The CORE's phase-4 pair is
  {domain accepted, **answer per input**} and this pass has the
  answer half for three of twelve languages. The trichotomy's
  `contradicts` arm is therefore evaluated at acceptance grain
  (decision 6) and is NOT the CORE's definition.
- **that the cluster count means anything on its own.** It moves from
  46 to 58 between two defensible thresholds *(measured)*. The
  clusters are readable; the count is not a result.
- **anything about dart's `||`, or about c++ and dart at value
  grain.** The first is a probable harness fault; the other two have
  no admitted matrix.
- **that the projection is safe.** Decision 1 destroys exactly the
  distinction CORE ruling 1 was written to preserve. It is stated as a
  choice, not defended as correct.

**What the full matrices add, when c++ and dart land:**

- the overlay becomes the primary domain for all nine statically
  checked languages (decision 9 says so explicitly), and every
  domain in §4 is recomputed against the full value cross product
  rather than one value per holder. Level **estimate** on the size of
  the movement: go moved 0 cells, typescript moved 704, so the range
  is wide and language-specific.
- the split-cell classification finishes. The nine `ld_<lang>_00.sh`
  declaration-alone lanes — 1,046 probes, about 21 seconds total —
  are still queued behind the matrix. They separate two kinds of
  split, which are named here against each other.
    - **layer 2 leaking in**: the holder could not hold that value.
    - **layer 3 moving**: the operation itself moved, which is the
      finding proper.
    - Typescript's 876 are all the second kind *(measured, log 028)*;
      the other eight languages are open.
- the mixed-holder table does **not** grow much, and this is worth
  saying because it was the obvious hope.
    - C++ already has its row, because the statistic runs off the
      acceptance grid and not off the matrix.
    - **Kotlin and swift have no shift spellings in their grammars at
      all** — kotlin spells them `shl`/`shr`, which are builtins and
      out of scope by the CORE's own rule *(measured, read from the
      manifests)*.
    - So the go-and-rust pattern against the java pattern stands at two
      languages each, and settling which is the common one needs **more
      languages, not more values**.
    - Level **derived**; it is a statement about what the remaining runs
      can and cannot decide.

**The one action item, not a wait:** dart's `vm_dart_01` shard exists
as a lane script and has **no status file and no output** — it was
never queued *(measured)*. Dart's matrix cannot complete until it is
dropped. Everything else in flight is progressing on its own.

---

## §7 — artifacts

| file | what it is |
|---|---|
| `manifest_<lang>.json` × 12 | the frozen enumerations |
| `manifest_verify.json` | the three-way verification report |
| `l3_manifest.py` | writes and verifies them; runs no probes |
| `clusters_preliminary.json` | signatures, clusters, relations, overlay |
| `clusters_preliminary.md` | the readable rendering |
| `l3_cluster.py` | builds the clustering; 11 numbered decisions |
| `l3_cluster_md.py` | renders the markdown; reads only |

Reproduce the whole of this log with three commands, none of which
touches a lane:

```
python3 l3_matrix_read.py     # fold landed shards
python3 l3_manifest.py        # freeze + verify
python3 l3_cluster.py         # cluster, then
python3 l3_cluster_md.py      # render
```
