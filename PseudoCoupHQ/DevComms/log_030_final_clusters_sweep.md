# log 030 — layer 3 phase 4: the promoted clustering and the threshold sweep

Date: 2026-08-18 (later the same day than logs 027, 028 and 029). Node:
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
    language one question.
    example tied to context:
        this pass folded 2,221,643 probes
        across nine languages; each declares
        values in typed slots and applies one
        operation to them.

lane
    one batch job. it runs a planned set of
    probes and writes its output to one raw
    text file. a lane has a short name.
    example tied to context:
        `ld_go_00` is the go load-check lane,
        and `vm_dartfix_01` is one of the
        dart value-matrix lanes re-run after
        the severity fix.

shard, and the `__SUMMARY__` line
    one output chunk of a lane, ending in a
    line that states how many probes that
    piece did.
    example tied to context:
        c++'s six shards all landed with
        `__SUMMARY__` lines and matching
        counts.

completeness gate (also: gate)
    a check run after a lane finishes. it
    adds up the probe counts across the
    shards and compares the total with what
    the plan said. it prints COMPLETE only
    if they match.
    example tied to context:
        all nine value matrices pass the gate
        on their own `complete` field; §2.4
        is about a fault the gate cannot see.

ENOSPC, and scratch
    scratch is the disk the lanes write their
    probe sources to; here it is `/work`, a
    4 GB memory-backed filesystem. ENOSPC is
    the operating system's "no space left on
    device" error.
    example tied to context:
        one lane log carries 44,268 `OSError:
        [Errno 28] No space left on device`
        lines, and that lane is void.

holder
    the typed slot a value is put into before
    an operation is applied to it.
    example tied to context:
        go's holders are named `whole`,
        `truth`, `text` and so on; a load
        check asks whether a value fits its
        holder at all.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        the dart map holder's `empty` and
        `flat` are two value classes, and
        §2.4 starts from a cell that accepted
        one and refused the other.

cell (also: pair cell)
    one combination of operand kinds that an
    operation was asked about. a pair cell is
    one combination of two holders, written
    with a bar, as `whole|whole`.
    example tied to context:
        kotlin has 11,492 pair cells; go's
        shift operations accept exactly one
        cell, `whole|whole`.

uniform cell, split cell
    a cell is UNIFORM when every probe in it
    got the same verdict. it is SPLIT when
    some probes in it were accepted and
    others refused, so the verdict depends on
    the value and not only on the two
    holders.
    example tied to context:
        kotlin carries 1,234 split cells of
        11,492, the most of any language
        measured.

load check
    a separate small lane that declares a
    holder with a value in it and nothing
    else. it answers one question: can this
    value be loaded into this holder at all.
    example tied to context:
        the nine `ld_<lang>_00.sh` load-check
        lanes ran 1,046 probes between them.

layer 2, layer 3
    two reasons a split cell can be split.
    LAYER 2 means the value would not load
    into its holder in the first place.
    LAYER 3 means the value loaded and the
    operation itself refused it.
    example tied to context:
        3,267 of the 4,588 split cells are
        layer 2 only, which is 71 percent.

acceptance grid
    the earlier and coarser measurement: one
    probe per pair of holders, using one
    chosen value per holder.
    example tied to context:
        log 029's clustering was built on the
        acceptance grids, and this log
        replaces them.

value matrix
    the finer measurement: every value class
    of the left holder against every value
    class of the right holder, for every pair
    of holders.
    example tied to context:
        dart's value matrix is 217,073
        probes against its acceptance grid's
        10,625.

the promotion
    the act of taking each statically checked
    language's domain from its value matrix
    instead of from its acceptance grid. it
    was held back until all nine matrices
    were finished.
    example tied to context:
        the promotion moved 23 of 233
        operation signatures, and every move
        was a widening.

signature
    everything recorded about one operation of
    one language: which cells it accepts, and
    the shape of that acceptance.
    example tied to context:
        `kotlin.in` is a signature; the
        promotion took it from 4 cells to 18.

domain
    the set of cells an operation actually
    accepted. cells the language refused are
    not in the domain.
    example tied to context:
        `rust.<<` has a domain of one cell,
        `whole|whole`.

leaf
    one operation of one language, once it has
    a domain to cluster with. leaves are the
    things the clustering arranges.
    example tied to context:
        this pass has 229 leaves and 228
        merges over them.

clustering
    the arrangement built from how close the
    leaves are to each other: it repeatedly
    joins the two closest groups until one
    group is left.
    example tied to context:
        the clustering here is run to a single
        root rather than stopped at a chosen
        distance.

average linkage
    the rule used to decide how close two
    GROUPS of leaves are: the average of the
    closenesses between their members. it
    never joins a pair at a closeness higher
    than a pair it already joined.
    example tied to context:
        average linkage is why the cluster
        count can be read off the merge
        history exactly rather than
        approximately.

merge history
    the full ordered record of every join the
    clustering made, each with the similarity
    at which it happened.
    example tied to context:
        228 merges over 229 leaves, stored in
        `clusters_final.json`.

threshold (also: cut)
    a similarity chosen to stop reading the
    clustering at. every threshold gives some
    number of clusters. the clustering itself
    picks no threshold.
    example tied to context:
        log 029 chose 0.70 and got 46
        clusters; this log chooses nothing.

sweep
    computing the cluster count at every
    threshold rather than at one chosen one.
    example tied to context:
        decision 14 is the ruling that
        replaced the chosen cut with the
        sweep.

plateau
    a range of thresholds over which no merge
    fires, so every threshold inside it gives
    not merely the same COUNT of clusters but
    the same CLUSTERING.
    example tied to context:
        [0.137, 0.196) is the widest
        non-degenerate plateau, and it holds
        three clusters.

elbow
    a threshold at which the cluster count
    jumps sharply, which would be a place the
    data itself picks to stop at.
    example tied to context:
        the curve in §4.1 has no elbow, which
        is the reason there is a sweep at all.

Jaccard, similarity
    how much two domains overlap: the count of
    cells in both, divided by the count of
    cells in either. 1.0 is identical
    domains, 0.0 is no shared cell.
    example tied to context:
        `cpp.+` and `go.+` score 0.167.

equals, nests, nested_by, overlaps,
contradicts
    the five names for how one operation's
    domain sits against another's. EQUALS is
    the same set of cells. NESTS is strictly
    containing the other. NESTED_BY is
    strictly contained by it. OVERLAPS is
    sharing cells with neither containing the
    other. CONTRADICTS is sharing no cell at
    all.
    example tied to context:
        this pass has 718 equals edges and
        zero contradicts edges.

story
    a named group of leaves picked out by
    hand, so the sweep can be asked where that
    group forms and where it falls apart.
    example tied to context:
        "shifts and bitwise", 52 members, is
        one story in §4.3.

the mixed-holder statistic
    for one operation of one language, the
    share of the cells it accepts whose two
    holders are of different kinds. a high
    number means the operation freely mixes
    kinds; a low one means it insists on two
    of the same.
    example tied to context:
        go's `<<` scores 0.75 and go's `+`
        scores 0.00.

the shift exemption
    the claim that a language constrains its
    shift operations more tightly than its
    arithmetic, seen as a high mixed-holder
    number on the shifts against a low one on
    `+`, `-` and `*`.
    example tied to context:
        the exemption is total in go and rust
        only, and barely measurable in java.

decision <n>
    a numbered ruling this node has made, kept
    so it can be overturned by number.
    example tied to context:
        this log makes decisions 12 to 17;
        decision 14 is the ruling that there
        is no chosen cut.

item <n><letter>
    a numbered item in the node's CHECK file,
    which is where later logs point when they
    cite a finding of this one.
    example tied to context:
        `CHECK_0_3_2_kind_fuzz_clustering.md`
        carries items 4g through 4p against
        this log's findings.

route C
    the way the three directly-run languages
    are measured: they are run rather than
    compiled, so acceptance and answer arrive
    together and no value matrix exists.
    example tied to context:
        python, ruby and php stay on route-C
        behaviour under decision 3 and take no
        part in the promotion.

density
    the stored alternative readings of a split
    cell: what the domain would be if every
    value combination had to be accepted, and
    what it would be if most had to be.
    example tied to context:
        density is why overturning decision 10
        costs a re-read rather than a re-run.

VOID, SUPERSEDED
    two filename marks. VOID marks a
    measurement taken wrongly, kept on the
    record and not used. SUPERSEDED marks a
    measurement a later run replaced, also
    kept.
    example tied to context:
        `raw/VOID_vm_dart_01_enospc.txt` and
        `raw/SUPERSEDED_*_lintbug.txt`.

form projection
    decision 1's rule: a cell records the
    KINDS of its two operands and not which
    holder they came from.
    example tied to context:
        §6 raises the possibility that the
        three-family reading is an artefact of
        form projection destroying holders.
```

---

## what came before this log, restated

Each fact this log borrows from an earlier log or an earlier decision is
stated here in full, so no sentence below depends on opening another
file.

- **Log 029 published the clustering this log replaces, and it published
  it on the acceptance grids.** One probe per pair of holders, one
  chosen value per holder.
- **Log 029 marked itself PRELIMINARY in its first field**, and named
  three things that would end that state: all nine value matrices
  landing, the dart `||` fault being examined rather than left, and the
  promotion of its decision 9.
- **Log 029's decision 9 said the acceptance grid was a placeholder.**
  The ruling was that once all nine value matrices finished, the matrix
  should simply BECOME the domain, because a grid that asks a language
  about `42 + 42` and calls the answer "what `+` does to two whole
  things" is guessing about every other whole number.
- **Log 029's decision 9 also carried an objection to promoting early.**
  A partial promotion would move measured closenesses for a reason about
  which lane happened to finish first.
- **Log 029 published an error bar on the acceptance grids**: up to 5.8
  percent of cells possibly wrong.
- **Log 029 reported 46 clusters at threshold 0.70 and 58 at 0.85**, and
  conceded that nothing in the data picked either threshold.
- **Log 029 found seven `contradicts` edges and called their cause
  unverified.** Every one of the seven was dart's `||` against another
  language's `||`. Dart recorded `bool && bool` as ACCEPT and
  `bool || bool` as REFUSE, with an empty error detail on every dart
  refusal.
- **Log 029 flagged `vm_dart_01` as a shard that had never been
  queued.**
- **Log 029 measured kotlin as carrying the most value-dependent cells
  of any language**: 1,234 split cells of 11,492.
- **Log 029 said go's acceptance grid was called exactly right.**
- **Log 029 named two clusters this log follows up.** Its cluster 5 has
  twelve members: `go.%`, `go.&`, `go.&^`, `go.<<`, `go.>>`, `go.^`,
  `go.|`, `java.<<`, `java.>>`, `java.>>>`, `rust.<<`, `rust.>>`. Its
  cluster 6 has ten members and is the node's one cross-family cluster,
  cpp with python.
- **Log 029 said "`+` does not cluster together".**
- **Log 029 published the shift exemption as covering "go, rust,
  c-sharp, c++ and java", and then corrected that phrasing itself.**
- **Log 029 published the relation counts this log compares against**:
  nested_by 1,009, equals 687, nests 588, overlaps 618, contradicts 7.
- **Log 029 used `cpp.+` against `go.+` as its worked `nests` example.**
- **Log 029 §6 left the kotlin and swift shift vocabulary question
  open.** Kotlin spells its shifts `shl` and `shr`, and swift's
  tree-sitter grammar parses `+` through a catch-all `custom_operator`
  node, so neither language has a shift row in the mixed-holder table.
- **Log 028 projected the total probe count** that this log's harvest
  had to reach: 2,221,643.
- **Log 028 established that typescript's split cells are literal-type
  narrowing** — typescript's checker gives a literal its own narrow
  type, so the verdict depends on the literal.
- **Log 028 recorded that cpp's and java's value matrices were refused
  by the completeness gate at that time**, which is why those two
  languages carried no error bar in log 029.
- **Log 027 built and ran phase 3, and its HARVEST notes predicted a
  layer-2 leak** of the shape `short v = 9223372036854775807;` — a
  literal that will not fit the holder it is being loaded into.
- **Log 024's decision 3 asked for the classification this log
  performs**: separating a true value-level acceptance split from a
  value that merely failed to load into its holder.
- **Decision 1 is the form projection rule.** A cell records the kinds
  of its two operands, not which holder they came from.
- **Decision 3 keeps python, ruby and php on route-C behaviour.** They
  are run rather than compiled, so no value matrix exists or can exist
  for them.
- **Decision 6 is the acceptance-grain reading of `contradicts`** — two
  operations sharing no accepted cell — as against the CORE's own
  definition.
- **Decision 7 requires the mixed-holder statistic to be computed by
  code that names no operation and no language.**
- **Decision 10 is the existential-over-values rule.** A cell counts as
  accepted if ANY combination of values in it was accepted.
- **The CORE defines `contradicts` at the ANSWER grain** — same input,
  different answer — and it is the third arm of a trichotomy whose other
  two arms are `nests` and `overlaps`. Only three languages have answers
  at all.

This log closes phase 4's first arc. All three of log 029's conditions
are met here, and the owner's ruling of this session replaces the chosen cut
with a sweep.

---

## §1 — walkthrough, in plain words

**All nine value matrices have landed, so the promotion has fired.**

- Log 029 clustered on the acceptance grids, one probe per pair of
  holders and one value per holder.
- Its decision 9 said that arrangement was a placeholder, to be replaced
  the moment all nine value matrices finished.
- All nine have now finished — **2,221,643 probes, all nine matrices
  COMPLETE** *(measured)*.
- So this pass asks the full cross product of value classes instead of
  one chosen value per holder.

**The promotion moved less than expected and the reason is
interesting.**

- Only **23 of 233 operation signatures changed domain at all**, and
  every single change was a WIDENING — 23 gained cells, none lost any
  *(measured)*.
- That is not luck. It follows from decision 10, where one accepting
  value combination is enough for the cell to count as accepted.
- What it means is that the acceptance grid was, for two hundred and ten
  signatures out of two hundred and thirty-three, already telling the
  truth.
- The error bar log 029 published — up to 5.8 percent of cells wrong —
  was real. It concentrated in a few places rather than spreading.

**The dart `||` fault is now verified, and it was an instrument fault of
a kind worth naming.**

- Log 029 found seven `contradicts` edges, all of them dart's `||`, and
  called the cause unverified.
- The dart lane ran `dart analyze <dir>` and marked a probe REFUSED if
  its filename appeared **anywhere** in the output, **at any severity**.
- `dart analyze` reports `dead_code` on the right operand of `true || b`
  and of `false && b`.
- So a short-circuit lint was being read as a type refusal.
- The acceptance grid happened to draw `true` for the truth holder. That
  is the dead-code case for `||` and the live case for `&&`.
- One value, opposite luck, and a language-level contradiction reported.
  Captured verbatim from the container:

```
warning - P3_3_1_1_14.dart:5:16 - Dead code.
WARNING|STATIC_WARNING|DEAD_CODE|...|Dead code.
```

- The fix reads `--format=machine` and counts only severity ERROR.
- That is what the other eight harnesses already measure — g++, javac
  and rustc do not fail on warnings either — so the fix makes dart
  **consistent** rather than special.
- Dart was re-run whole. **All seven `contradicts` edges are gone; the
  final pass has zero** *(measured)*.

**The headline is what the sweep found once there was no chosen cut.**

- Log 029 reported 46 clusters at 0.70 and 58 at 0.85, and conceded that
  nothing in the data picked either.
- Computing the whole merge history instead, the widest threshold band
  over which the picture does not move at all — leaving aside the
  degenerate ends — is **[0.137, 0.196), and across it there are exactly
  THREE clusters** *(measured)*.
- Those three are not three languages and not three operator families.
  They are, in order:
  - **147 wide signatures with a median domain of 18 cells, drawn from
    all twelve languages** *(measured)*.
  - **51 narrow ones with a median domain of 3, drawn mostly from go,
    java, typescript and rust** *(measured)*.
  - **31 whose median domain is 2 and whose spellings are only
    `% & && << >> ^ | ||`** *(measured)*.
- The third one crosses the static-versus-open-dispatch divide that
  every other structure in this node respects — cpp, java, python, rust,
  csharp, dart, go, kotlin and swift together.
- Level **derived** for the reading; the memberships are measured.

**And one thing the machinery caught that nobody asked it to.**

- Chasing an incoherent dart cell — the matrix claimed dart accepted
  `Map<String,int> && String` for some values of the map and not others,
  which is not a rule any type checker could be following — turned up a
  fault that **the completeness gate cannot see**.
- A lane that runs out of scratch cannot write its probe sources.
- A file that was never written draws no diagnostic.
- The harness scores "no diagnostic" as ACCEPT.
- The lane still exited 0 and still printed its `__SUMMARY__` line with
  the full probe count, so the gate passed it.
- Details in §2.

---

## §2 — harvest, the load checks, and the two instrument fixes

### 2.1 the harvest

Everything queued behind the matrix had landed. Copied and folded with
no lane disturbed:

| language | probes folded | pair cells | uniform | split | gate |
|---|---|---|---|---|---|
| typescript | 230,000 | 12,167 | 11,291 | 876 | COMPLETE |
| dart | 217,073 | 10,625 | 9,966 | 659 | COMPLETE |
| csharp | 397,620 | 18,000 | 17,282 | 718 | COMPLETE |
| java | 444,020 | 20,480 | 19,721 | 759 | COMPLETE |
| rust | 205,504 | 9,196 | 9,060 | 136 | COMPLETE |
| go | 167,884 | 7,600 | 7,497 | 103 | COMPLETE |
| swift | 76,614 | 3,456 | 3,447 | 9 | COMPLETE |
| kotlin | 253,028 | 11,492 | 10,258 | 1,234 | COMPLETE |
| cpp | 229,900 | 10,944 | 10,850 | 94 | COMPLETE |

- **All nine pass the completeness gate on their own `complete` field**
  *(measured)*. The total is 2,221,643 probes, which is the number log
  028 projected and log 029 was waiting on.
- The dart value-matrix shard `vm_dart_01`, which log 029 flagged as
  never queued, was queued and ran *(measured)*. C++'s six shards all
  landed with `__SUMMARY__` lines and matching counts *(measured)*.
- Kotlin still carries the most value-dependent cells of any language
  measured — **1,234 split cells of 11,492, 10.7 percent** *(measured,
  derived percentage)*. That is unchanged from log 029 and is now final
  rather than provisional.

### 2.2 the load checks, and the two of nine that were void

The nine load-check lanes `ld_<lang>_00.sh` ran — 1,046 probes between
them, each carrying a holder's declaration alone. Two of them measured
nothing, and reading their refusal details rather than their counts is
what showed it.

- **The go load-check lane `ld_go_00` refused all 94.** The detail says
  why:

```
declared and not used: a
"fmt" imported and not used
```

  Both are hard errors in go. A load check that drops the body leaves
  the variable and the import unused, so the lane was measuring go's
  unused-variable rule, not whether the holder can hold the value
  *(measured)*.
- **The dart load-check lane `ld_dart_00` refused all 113**, with empty
  details. That is the same severity fault as §2.3,
  `unused_local_variable` being an INFO *(measured)*.
- Both were re-run. Go was re-run with a single `_ = fmt.Sprint(a)` that
  consumes the variable and the import together. Dart was re-run under
  the severity fix. **Go now refuses 21 of 94 and dart 12 of 113**
  *(measured)*, and dart's refusals read
  `INTEGER_LITERAL_OUT_OF_RANGE`, which is precisely the layer-2 leak
  HARVEST predicted with `short v = 9223372036854775807;`.
- A load check that refuses everything cannot separate anything, so the
  earlier go and dart classifications were void and are replaced, not
  adjusted. Numbered as decision 13.

The classification, which is the thing log 024 decision 3 asked for,
separates two things that look the same in a split cell:

- **a true value-level acceptance split** — the value loaded into its
  holder, and the operation itself refused it. This is layer 3 moving.
- **a value that merely failed to load into its holder** — the operation
  never got a chance to have an opinion. This is layer 2 only.

| language | ld probes | ld refusals | split cells | layer 3 moving | mixed | layer 2 only |
|---|---|---|---|---|---|---|
| go | 94 | 21 | 103 | 0 | 6 | 97 |
| rust | 104 | 16 | 136 | 38 | 44 | 54 |
| cpp | 110 | 30 | 94 | 7 | 28 | 59 |
| swift | 113 | 9 | 9 | 0 | 9 | 0 |
| dart | 113 | 12 | 659 | 0 | 0 | 659 |
| csharp | 141 | 28 | 718 | 15 | 32 | 671 |
| kotlin | 122 | 14 | 1,234 | 41 | 149 | 1,044 |
| java | 149 | 20 | 759 | 76 | 0 | 683 |
| typescript | 100 | 0 | 876 | 876 | 0 | 0 |
| **all nine** | **1,046** | **150** | **4,588** | **1,053** | **268** | **3,267** |

- **Most splits are layer 2 leaking in, not layer 3 moving** — 3,267 of
  4,588, **71 percent** *(measured, derived percentage)*. That is the
  single most useful number this classification produced. It cuts the
  apparent size of the value-dependence finding by about two thirds.
- The two extremes of the table are worth naming against each other.
  - **Typescript is the pure case and remains so**: 876 split cells,
    **876 of them layer 3 moving, zero layer 2** *(measured)*.
    Typescript is also the one language whose load check refuses nothing
    at all. Its splits are literal-type narrowing, exactly as log 028
    established.
  - **Dart is the pure opposite**: 659 split cells, **all 659 layer 2
    only** *(measured)*. After the severity fix, dart has no value-level
    acceptance split anywhere in its matrix. Level **derived** on the
    reading: dart's value-dependence in log 029 was the lint, and what
    remains is literals that do not fit their holder.
- **Go's grid was called exactly right in log 029 and still is.** Its
  103 split cells are 97 layer 2 and 6 mixed, with no pure layer-3 cell
  *(measured)*.
- Level **derived**, and worth stating as a limit: `unclassified` is
  **zero everywhere** *(measured)*. Every split in all nine languages
  got a verdict from the load check rather than a guess.

### 2.3 the dart harness fault, diagnosed and fixed

Decision 12. Diagnosed by reading the lane, confirmed by running four
files alone in the container, and closed by re-running dart whole.

- **The mechanism.** `dart analyze <dir>` was scraped for any line
  mentioning a probe's filename, at any severity, and the detail field
  was written as the empty string unconditionally. That is why log 029
  saw "REFUSE with an empty error detail" on **every** dart refusal, not
  only on `||`.
- **The confirming run** is `raw/dx_dart_deadcode.txt`: four probes,
  dart 3.13.0. The two that draw a diagnostic are exactly `false && b`
  and `true || b`, both `DEAD_CODE`, both severity **WARNING**
  *(measured)*. No other severity appears.
- **The fix**: `--format=machine`, severity ERROR only, detail restored
  from the diagnostic's own code and message.
- **The regression check, which matters more than the fix.** Of
  **217,073 dart matrix probes, 50,381 moved REFUSE to ACCEPT and ZERO
  moved ACCEPT to REFUSE** *(measured)*. A severity filter can only ever
  loosen, so a single movement the other way would have meant the patch
  was wrong. There were none.
- The acceptance grid was re-run too, because the mixed-holder statistic
  reads off it: **506 of 10,625 probes moved, all in the same one
  direction**, accepts 1,170 to 1,676 *(measured)*.
- The target cell, verbatim, before and after:

```
P3_3_14  old  REFUSE  (empty detail)
P3_3_14  new  ACCEPT
```

- And in the value matrix, `&&|3|3` and `|||3|3` are now **uniform
  ACCEPT**, not split *(measured)*. The disagreement between dart and
  the other eight has no residue.
- The superseded raw files are kept as `raw/SUPERSEDED_*_lintbug.txt`,
  per the standing rule that a wrong measurement stays on the record.

### 2.4 the fault the completeness gate cannot see

Decision 17. Found, not looked for.

- **The symptom.** The first re-run of the dart value-matrix lane
  `vm_dartfix_01` produced 49,827 accepts where the same shard had
  produced 4,675. The matrix then claimed dart accepted
  `Map<String,int> && String` for the map value class `empty` and
  refused it for `flat` *(measured)*. No type checker follows that rule.
- **Two hypotheses were tested and both were cleared.**
  - Batching: 30 identical probes analysed alone, and again inside a
    500-file directory, gave the same 30 errors both ways *(measured,
    `raw/dx_dart_batch.txt`)*.
  - An output cap: 100, 300, 500 and 1,000 all-erroring files returned
    an ERROR for **every** file *(measured, `raw/dx_dart_cap.txt`)*.
- **The actual cause.** `/work`, the scratch filesystem, is a 4 GB tmpfs
  and it was holding 3.7 GB of phase-3 leftovers, so the lane could not
  write its probe sources. Its log carries **44,268
  `OSError: [Errno 28] No space left on device` lines** *(measured)*.
  The harness scores "no diagnostic" as ACCEPT, and a file that was
  never written draws no diagnostic, so ENOSPC reads as universal
  acceptance.
- **The gate passed it.** The lane exited 0, printed its `__SUMMARY__`
  line, and reported its full probe count, because it emitted a verdict
  line per probe — just the wrong verdict. Probe counts, summary lines
  and exit codes are all blind to this.
- **Remediation and control.** `/work` was swept back to 4,096 MB free.
  The shard re-ran clean with **0 ENOSPC and 9,350 accepts**. The other
  dart lane `vm_dartfix_00` was re-run on clean scratch purely as a
  control: it **reproduced its 17,101 accepts exactly** *(measured)*.
- **Scope, which is the reassuring part.** Every value-matrix,
  acceptance and load-check lane log in the node was then scanned for
  ENOSPC: **exactly one file matches, the void run itself**
  *(measured)*. No other measurement in this node is implicated. The
  void file is kept as `raw/VOID_vm_dart_01_enospc.txt`.
- Proposed as a standing rule for the next agent: **grep a lane's log
  for ENOSPC before folding its product**, because nothing in the result
  file can reveal it.

---

## §3 — what the promotion changed, with worked examples

Decision 16. The nine statically checked languages take their domain
from the value matrix under decision 10's existential-over-values rule.
Python, ruby and php stay on route-C behaviour under decision 3, because
no matrix exists or can exist for them. Decision 9's objection — that a
partial promotion would move similarities for a reason about which lane
finished — is spent, because it is now all nine.

**The delta: 23 of 233 signatures moved, all of them widened, none
narrowed, and none disappeared** *(measured)*. Every mover, in full:

| signature | grid | matrix | gained | the cells gained |
|---|---|---|---|---|
| `kotlin.in` | 4 | 18 | +14 | `fractional\|nesting`, `keyed\|sequence`, … |
| `typescript.==` | 28 | 42 | +14 | `keyed\|nesting`, `keyed\|sequence`, … |
| `typescript.!=` | 28 | 42 | +14 | same fourteen |
| `typescript.===` | 28 | 42 | +14 | same fourteen |
| `typescript.!==` | 28 | 42 | +14 | same fourteen |
| `typescript.<` `<=` `>` `>=` | 14 | 24 | +10 each | `keyed\|text`, `keyed\|truth`, … |
| `rust.<` `<=` `>` `>=` `==` `!=` `..` | 8 | 10 | +2 each | `nothing\|sequence`, `sequence\|nothing` |
| `swift.<` `>` `>=` | 5 | 7 | +2 each | `nothing\|sequence`, `sequence\|nothing` |
| `csharp.==` `!=` `??` | 24 / 18 | 26 / 20 | +2 each | `keyed\|nesting`, `nesting\|keyed` |
| `kotlin.+` | 38 | 39 | +1 | `keyed\|nesting` |

- **The worked example that explains the whole shape.** Typescript's
  four equality spellings each gained the same fourteen cells, and all
  fourteen involve `keyed` or `nesting` on one side *(measured)*. The
  acceptance grid probed one object value per keyed holder, and that one
  value's literal type did not compare against the other side. The
  matrix probes all of them and at least one does. This is the same
  literal-type narrowing that produced typescript's 876 split cells,
  seen from the domain side rather than the cell side.
- **The second worked example, and the smallest one.** Rust's seven
  relational spellings each gained exactly `nothing|sequence` and
  `sequence|nothing` *(measured)*. Rust's grid drew one value for its
  nothing holder and one for its sequence holder, and that pair did not
  compare. Some other pair of values does. Two cells out of sixty-four,
  on seven signatures — the promotion's effect on rust is real,
  measurable and tiny.
- **Dart does not appear in the delta at all, and that is the point.**
  Its acceptance grid was re-run under the same severity fix as its
  matrix, so grid and matrix now agree everywhere and there is nothing
  to widen *(measured)*. Before the fix dart would have been the largest
  mover in the table by a wide margin. Fixing the instrument removed a
  delta that was never about the language. Level **derived**.
- **Go, cpp and java did not move one cell** *(measured)*. Go's grid was
  already exact in log 029 and stays exact. Cpp and java, which had no
  error bar at all in log 029 because their matrices were refused by the
  gate, turn out to have needed none.
- **What it costs at the cluster level.** The preliminary pass reported
  46 clusters at 0.70 and 58 at 0.85; this pass has **44 and 58**
  *(measured)*. So the promotion, the dart fix and the load-check
  repairs together move the count at the old cut by two, and not at all
  at the other. Level **derived** as to significance: the domains that
  moved were mostly permissive ones getting slightly more permissive,
  which Jaccard barely notices.

---

## §4 — the sweep

Decision 14, on the owner's ruling this session: no chosen cut. The full merge
history is computed — average linkage run to a single root, every merge
recorded with the similarity at which it happened — and the cluster
count at any threshold follows exactly from it, as the leaf count minus
the number of merges at or above that similarity. Average linkage is
monotone, so there are no inversions and the identity is exact rather
than approximate. **228 merges over 229 leaves** *(measured)*. The
identity was checked against an independent tree walk at all 167
breakpoints and their neighbourhoods: **zero mismatches** *(measured)*.

### 4.1 the curve

| threshold | 0.10 | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 | 0.70 | 0.80 | 0.90 | 1.00 |
|---|---|---|---|---|---|---|---|---|---|---|
| clusters | 2 | 4 | 8 | 17 | 25 | 34 | 44 | 51 | 59 | 61 |

- The curve is **smooth and has no elbow** *(measured)*. There is no
  threshold at which the cluster count jumps. That is the direct reason
  no cut can be picked from the data, and the honest reason to publish
  the sweep instead. Level **derived**.
- **It flattens hard above 0.90**: 59 clusters at 0.90 and 61 at 1.00
  *(measured)*. Sixty-one is the number of **distinct domains** in the
  whole pass — 229 signatures collapse to 61 exact equivalence classes
  on the shared 64-cell space. Level **derived**; the count is measured.

### 4.2 the plateaus — the ranges where the picture does not move

A plateau is a maximal threshold range over which no merge fires, so
every threshold inside it yields not merely the same COUNT but the same
CLUSTERING. The two degenerate ends — one cluster, and all singletons —
are marked and set aside.

| threshold range | width | clusters |
|---|---|---|
| [0.137, 0.196) | 0.058 | **3** |
| [0.900, 0.952) | 0.052 | 60 |
| [0.255, 0.304) | 0.049 | **8** |
| [0.952, 1.000) | 0.048 | 61 |
| [0.095, 0.137) | 0.042 | 2 |
| [0.338, 0.374) | 0.036 | 14 |
| [0.667, 0.700) | 0.033 | **44** |
| [0.842, 0.875) | 0.033 | 58 |
| [0.577, 0.608) | 0.031 | 34 |
| [0.750, 0.778) | 0.028 | 50 |

- **The widest non-degenerate plateau is [0.137, 0.196) and it holds
  three clusters** *(measured)*. This is the natural coarse reading of
  the whole pass, and it is a reading the data picks rather than one a
  cut imposes.
    - **147 signatures over all twelve languages, median domain 18 cells
      of 64** — php 26, python 19, ruby 19, csharp 17, dart 15, cpp 13,
      typescript 13, kotlin 10, rust 7, java 3, swift 3, go 2
      *(measured)*. The permissive end, and every language has something
      in it.
    - **51 signatures over 7 languages, median domain 3** — go 15,
      java 11, typescript 10, rust 7, kotlin 4, ruby 3, swift 1
      *(measured)*. The strict end.
    - **31 signatures over 9 languages, median domain 2**, spelled only
      `% & && << >> ^ | ||` — cpp 6, java 5, python 5, rust 5,
      csharp 2, dart 2, go 2, kotlin 2, swift 2 *(measured)*. Two whole
      things and nothing else, plus the truth-only logicals.
    - Read plainly: the coarsest stable structure is **not by language
      and not by operator**. It is width — permissive, strict, and a
      third family of operations that refuse to coerce anything at all.
      **No language sits wholly inside one family**; go has 15
      signatures in the strict one and 2 in each of the others
      *(measured)*. The third family crosses the static and
      open-dispatch divide. Level **derived** for the naming; the
      memberships are measured.
- **The second reading, at [0.255, 0.304), is eight clusters**
  *(measured)*. It is the first threshold band where the strict family
  has split into recognisable pieces while the integer-only family stays
  whole at 29.
- **[0.667, 0.700) holds 44 clusters**, and log 029's chosen 0.70 sits
  exactly on that plateau's upper edge *(measured)*. So the old cut was
  not a bad reading; it was an unmarked one. Level **derived**.

### 4.3 where the named stories form and dissolve

For each story: PEAK is the largest cluster containing only members of
that story, and the story DISSOLVES below the threshold at which its
members stop forming any pure cluster at all.

| story | members | peak | at threshold | dissolves below |
|---|---|---|---|---|
| log 029's cluster 5 | 12 | **12** | 1.000 | 0.500 |
| log 029's cluster 6 | 10 | **10** | 0.800 | 0.467 |
| `&&` and `\|\|` | 22 | 12 | 1.000 | 0.196 |
| shifts and bitwise | 52 | 6 | 1.000 | 0.255 |
| `==` `!=` `===` `!==` | 26 | 4 | 1.000 | 0.459 |
| comparisons | 50 | 4 | 1.000 | 0.434 |
| `+` | 10 | **2** | 1.000 | 0.507 |
| shift spellings alone | 21 | **2** | 1.000 | 0.800 |
| `==` alone | 11 | **0** | — | never forms |

- **Log 029's cluster 5 survives the promotion intact and is stronger
  than log 029 could say.** Its twelve members — `go.%`, `go.&`,
  `go.&^`, `go.<<`, `go.>>`, `go.^`, `go.|`, `java.<<`, `java.>>`,
  `java.>>>`, `rust.<<`, `rust.>>` — form a pure cluster **at threshold
  1.000**, meaning their projected domains are not merely similar but
  **identical**, and that domain is the single cell `whole|whole`
  *(measured)*. It holds as a pure group all the way down to 0.500.
- **Log 029's cluster 6 also survives**, peaking as all ten at 0.800 and
  dissolving below 0.467 *(measured)*. It remains the node's
  cross-family cluster, cpp with python.
- **The `+` story is confirmed and sharpened.** `+` never forms a pure
  cluster larger than **two** at any threshold in the entire sweep, and
  the pair is `csharp.+` with `java.+` *(measured)*. Two statements sit
  against each other here:
  - log 029 said "`+` does not cluster together", which was a statement
    about one chosen threshold.
  - the sweep says it does not cluster together at ANY reading, which is
    a strictly stronger statement.
- **The shift spellings alone never exceed two either** — `csharp.<<`
  with `csharp.>>` *(measured)*. Shifts do not form a shift cluster.
  They form a **shift-and-bitwise** cluster, and only in the languages
  where those operations share the "two whole things" domain. The
  shifts' apparent cohesion in log 029 was the bitwise operations
  carrying them.
- **`==` never forms a pure cluster at any threshold, at all**
  *(measured)*. Its eleven signatures scatter across all three families
  — rust's at 10 cells of 64 sits with the strict family, and dart's,
  php's, python's and ruby's at 64 sit with the permissive one. `==` is
  the operation on which languages disagree most and agree least, and
  the sweep says so with a zero.
- The twelve logicals that peak together at threshold 1.000 —
  `csharp`, `go`, `java`, `kotlin`, `rust` and `swift`'s `&&` and `||` —
  likewise have **identical domains**, the single cell `truth|truth`
  *(measured)*. Six languages, one operation, one cell, no disagreement:
  this is the cleanest `equals` block in the pass, and the dart fix is
  what let dart out of it and into honest company.

### 4.4 the mixed-holder statistic, restated on the promoted domains

Computed by code that names no operation and no language, per decision
7, and restricted to the nine statically checked languages for
comparability with log 029:

| language | `<<` | `>>` | `+` | `-` | `*` |
|---|---|---|---|---|---|
| go | 0.75 | 0.75 | 0.00 | 0.00 | 0.00 |
| rust | 0.75 | 0.75 | 0.14 | 0.00 | 0.00 |
| cpp | 0.71 | 0.71 | 0.64 | 0.64 | 0.67 |
| csharp | 0.73 | 0.73 | 0.70 | 0.64 | 0.64 |
| java | 0.80 | 0.80 | 0.78 | 0.76 | 0.76 |
| dart | 0.75 | 0.75 | — | — | 0.71 |
| typescript | 0.00 | 0.00 | 0.50 | 0.00 | 0.00 |
| kotlin | — | — | 0.62 | 0.65 | 0.36 |
| swift | — | — | — | — | 0.00 |

- **Log 029's correction stands unchanged.** The exemption is total in
  **go and rust only** — shifts at 0.75 against arithmetic at 0.00 to
  0.14 — and is barely measurable in java, where shifts are 0.80 and
  `+` is 0.78 *(measured)*. The phrasing "the shift exemption in go,
  rust, c-sharp, c++ and java" over-groups, and it still does.
- **Dart's row is new and it lands with the java pattern**, shifts 0.75
  against `*` 0.71 *(measured)*. Two runs of dart sit against each other
  here:
  - under the old harness, dart's row was contaminated by the lint.
  - under the fixed harness, this one is not.

  That makes the tally **two languages sharp (go, rust) against four
  blunt (cpp, csharp, java, dart)**. Level **derived**.
- **Typescript still inverts it** — shifts 0.00, `+` 0.50 *(measured)*.

---

## §5 — relations, updated

**2,930 relation edges** *(measured)*, restricted as before to
cross-language pairs that either share a spelling or score at least 0.5:

| relation | log 029 | this pass | movement |
|---|---|---|---|
| nested_by | 1,009 | 937 | −72 |
| equals | 687 | 718 | +31 |
| nests | 588 | 693 | +105 |
| overlaps | 618 | 582 | −36 |
| **contradicts** | **7** | **0** | **−7** |

- **THE CONTRADICTS EDGES ARE GONE. All seven, and the count is now
  zero** *(measured)*. Every one of the seven was `dart.||` against
  another language's `||`, and every one was the `dead_code` lint. With
  the harness fixed, dart's `||` accepts `truth|truth` like the other
  eight, and there is no disjoint pair of same-spelled operations left
  anywhere in the pass. Level **measured** for the count; level
  **derived** for the reading, which is that **this node has not
  measured a single genuine cross-language contradiction at acceptance
  grain**. Every apparent one was the instrument.
- That is worth stating as a limit as much as a result. Two readings of
  `contradicts` are in play, and only one of them has a zero:
  - **the acceptance-grain reading, decision 6** — two operations share
    no accepted cell. This is what the zero is a zero of.
  - **the CORE's own reading, at the ANSWER grain** — same input,
    different answer. Only three languages have answers, so nothing here
    speaks to it. The trichotomy's third arm remains **untested as the
    CORE means it**.
- **Equals gained 31 edges and nests gained 105** *(measured)*. Both
  follow from the promotion widening 23 domains and never narrowing one:
  a widened domain is more likely to strictly contain another, and more
  likely to coincide with another. Level **derived**.
- **NESTS, verbatim** — dominance discovered rather than assumed, and
  the same example log 029 used, now on the promoted domains:

```
cpp.+ contains go.+, jaccard 0.167
shared   fractional|fractional, text|text,
         whole|whole
only c++ fractional|truth, fractional|whole,
         sequence|truth, sequence|whole,
         text|truth, text|whole, truth|*, whole|*
```

- **OVERLAPS, verbatim** — neither dominates and the split is justified
  by measurement, the third arm of the CORE's trichotomy:

```
cpp.!= and csharp.!=, jaccard 0.533
only c++     fractional|truth, truth|fractional,
             truth|whole, whole|truth
only c-sharp keyed|keyed, keyed|nesting,
             nesting|nesting, nothing|nesting, ...
```

  Read plainly, as two facts rather than one:
  - c++ will compare a truth value against a number, and c-sharp will
    not *(measured)*.
  - c-sharp will compare two references, and c++ will not *(measured)*.
- **EQUALS — 718 edges, and the identical-domain blocks are the useful
  ones.** `cpp.<<` equals `python.<<` on a four-cell domain, and
  `cpp./` equals `python./` on a nine-cell one *(measured)*. An `equals`
  edge between two languages' identically spelled operation is the
  statement "these are one thing in two spellings", which is the
  discovered kind map phase 4 exists to produce. Level **derived** as to
  significance; the edges are measured.

---

## §6 — open questions for the owner

- **The kotlin and swift shift vocabulary question, carried from log 029
  §6 and still open.** Kotlin spells its shifts `shl` and `shr`, and
  swift's tree-sitter grammar parses `+` through `custom_operator`, so
  neither language has a shift row anywhere in §4.4 *(measured, read
  from the manifests)*. The CORE's own rule puts builtins out of scope,
  and `shl` is a builtin infix function rather than an operator token.
  The question is whether that rule should bend for a spelling that is
  an operator in every other sense. It matters concretely: the
  go-and-rust pattern against the cpp-and-java pattern stands **two
  against four**, and kotlin and swift are the two languages that could
  move it. Level **derived** on the consequence.
- **Is a zero `contradicts` count evidence, or is it the acceptance
  grain being too coarse to disagree?** §5 argues the second is at least
  as likely, since acceptance asks "can this typecheck" and two
  languages can both accept `1 + true` while answering differently.
  Settling it needs route C for the nine, which is the one genuinely
  unbuilt thing left in phase 3.
- **Decision 10, existential over values, is the widest possible reading
  and it is now load-bearing rather than a bound.** Its two roles sit
  against each other:
  - **in log 029 it was a bound.** The matrix was an overlay whose job
    was to BOUND the grid's error, so the extreme was the right choice.
  - **here it is a claim.** As the primary domain it says: `+` takes
    these two forms if ANY pair of values works.

  The universal and majority readings are computed and stored as
  `density`, so overturning it costs a re-read and not a re-run. the owner
  should say which he wants, because it is now a statement about
  languages rather than an error bar.
- **Should the load-check classification feed back into the domains?**
  §2.2 shows 71 percent of split cells are layer 2 leaking in. Decision
  10 currently counts a split as accepted regardless of which kind it
  is. A defensible alternative counts only layer-3 splits, which would
  narrow the nine domains by an amount nobody has measured yet.
- **The three-family reading at [0.137, 0.196) is the widest stable
  structure in the data, and this node has no theory for it.** That the
  coarsest honest clustering of 229 operations across 12 languages is
  strict / permissive / integer-only, rather than anything about
  operators, is one of two things. It is either the most interesting
  result of phase 4, or an artefact of the form projection destroying
  holders (decision 1). Level **unverified** as to which.
- **`raw/dx_dart_*.txt` are diagnostic runs, not measurements.** They
  are folded into no table and are kept because they are the evidence
  for decisions 12 and 17. Flagging them so a later agent does not
  mistake them for probe products.

---

## §7 — artifacts

All paths are inside
`PseudoCoupHQ/Research/kind_fuzz_clustering/`.

| file | what it is |
|---|---|
| `clusters_final.json` | signatures, merge history, sweep, relations |
| `dendrogram_sweep.html` | the visual — self-contained, opens from disk |
| `l3_final.py` | the promoted clustering; decisions 12 to 17 |
| `make_dendrogram.py` | writes the visual; reads only |
| `l3_loadcheck.py` | classifies every split against the load checks |
| `loadcheck_classified.json` | the classification, per language |
| `valuematrix_<lang>.json` × 9 | all nine COMPLETE |
| `lanes/vm_dartfix_0*.sh` etc. | the fixed dart and go lanes |
| `raw/SUPERSEDED_*_lintbug.txt` | the pre-fix dart raws, kept |
| `raw/VOID_vm_dart_01_enospc.txt` | the ENOSPC run, kept |
| `raw/dx_dart_*.txt` | the three diagnostic runs |

Reproduce the whole of this log with four commands, none of which
touches a lane:

```
python3 l3_matrix_read.py    # fold all nine
python3 l3_loadcheck.py      # classify the splits
python3 l3_final.py          # promote, then sweep
python3 make_dendrogram.py   # write the visual
```

The visual is the same picture as
`Research/kind_signature_clustering/dendrogram_explorer.html` — same
icicle rendering, same draggable threshold line, same live cluster
count, same yellow outline on the current clusters, same search and
hover card — with three differences the phase demands:

- the axis is similarity rather than merge height.
- all 229 leaves are labelled `language.operation`.
- a second panel carries the cluster-count-versus-threshold curve with
  the plateaus shaded.

Unlike the earlier file it pulls no d3 from a CDN, so it works from
`file://` with no network.
