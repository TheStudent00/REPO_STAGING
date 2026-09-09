# log 035 — the re-fold: swift's real answers and the word-spelled leaves

Date: 2026-08-19. Node:
`~/Programming/PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/CORE_0_3_2_kind_fuzz_clustering.md`.
Artifacts: `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

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
        the `xw_cpp_00` run below sent 8,526
        probes; each is a small c++ program
        that applies one operation to one
        pair of values and prints the result.

lane
    one batch job. it runs a planned set of
    probes and writes its output to one raw
    text file. a lane has a short name.
    example tied to context:
        `xw_cpp_00` is the lane that ran
        c++'s six word-spelled operations and
        wrote `raw/xw_cpp_00.txt`.

shard
    one output chunk of a lane. a lane that
    runs in five pieces writes five shards,
    each ending in a `__SUMMARY__` line that
    states how many probes that piece did.
    example tied to context:
        `xw_cpp_00` ran in 5 chunks, so it
        wrote 5 `__SUMMARY__` lines.

completeness gate (also: gate)
    a check run after a lane finishes. it
    reads every shard, adds up the probe
    counts, and compares the total with what
    the plan said the lane would run. it
    prints COMPLETE only if they match and
    no shard is missing.
    example tied to context:
        `l3_swiftfull_read.py` re-run on
        swift's landed shards prints
        `gate: COMPLETE`.

ENOSPC
    the operating system's "no space left on
    device" error. these runs write to a
    memory-backed scratch disk, so running
    out of room is the way a lane most often
    dies without saying so.
    example tied to context:
        every harvested lane log was searched
        for this word before anything was
        folded; none contained it.

holder
    the typed slot a value is put into before
    an operation is applied to it. in c++
    that is a declared variable of a stated
    type.
    example tied to context:
        `UInt64` and `Int64` are two swift
        holders; a probe puts a number in
        each and then applies `>=`.

value class
    a named family of test values, chosen so
    that awkward cases are covered.
    example tied to context:
        `i64max_plus1` is a value class: one
        more than the largest signed 64-bit
        integer.

cell (also: input cell)
    one combination of operand kinds that an
    operation was asked about. a cell is the
    unit an answer is recorded against.
    example tied to context:
        `truth|truth` is a cell: a boolean on
        the left and a boolean on the right.
        `cpp.xor` and `php.xor` share 64 such
        cells.

domain
    the set of cells an operation actually
    accepted. cells the language refused are
    not in the domain.
    example tied to context:
        `swift.<` has a domain of 7 cells,
        both before and after the swift redo.

answer class
    the kind and value an operation returned
    on a cell, written as kind:value.
    example tied to context:
        `whole:0` is an answer class — a
        whole number, zero. `truth:false` is
        another — a boolean, false.

VOID
    a mark put on a measurement that was
    taken wrongly, so that it is kept on the
    record but not used. a VOID row is not a
    leaf.
    example tied to context:
        php's `and`, `or` and `xor` were
        marked VOID in an earlier pass
        because the probe recorded the left
        operand instead of the result.

manifest
    a frozen file listing what was probed for
    one language under one plan: its holders,
    its value classes, its operation list. it
    is a record of a past run and is not
    edited afterwards.
    example tied to context:
        `manifest_ruby.json` was frozen
        before ruby's `and` and `or` were
        admitted, which is what caused the
        fault in §3.2.

leaf
    one operation of one language, once it
    has answers to cluster with. leaves are
    the things the clustering arranges.
    example tied to context:
        `cpp.and` is a leaf. this pass has
        238 leaves; the previous pass had
        226.

edge
    the measured closeness between two
    leaves. every pair of leaves that shares
    at least one cell has an edge.
    example tied to context:
        1,335 edges touch a swift leaf, and
        every one of them is unchanged by
        this pass.

similarity, Jaccard, agreement
    three numbers on an edge. agreement is
    the share of shared cells where the two
    leaves gave the same answer class.
    Jaccard is how much their domains
    overlap. similarity combines them.
    1.0000 is identical.
    example tied to context:
        `cpp.and` against `cpp.&&` scores
        1.0000 on all three.

harvest
    the act of collecting finished lanes off
    disk and checking each one before using
    it.
    example tied to context:
        §2 is the harvest: nine lanes listed,
        each checked for its gate and for
        ENOSPC.

fold (also: re-fold)
    the act of reading the raw lane output
    and building the answer files and the
    clustering from it. a re-fold is doing
    that again over a changed set of lanes.
    example tied to context:
        `l3_refold.py` carries three folds:
        swift's answers, c++'s answers, and
        the two route-C languages.

clustering
    the arrangement built from the edges: it
    repeatedly joins the two closest groups
    of leaves until one group is left. the
    result is `clusters_all12.json` and the
    picture of it is `dendrogram_all12.html`.
    example tied to context:
        the re-folded clustering has 238
        leaves and 475 nodes.

cut (also: reading)
    a distance chosen to stop reading the
    clustering at. every cut gives some
    number of clusters. the clustering itself
    picks no cut.
    example tied to context:
        the cut at 0.155 gives 21 clusters in
        this pass and gave 22 in the previous
        one.

plateau
    a run of cuts over which the number of
    clusters does not change. a wide plateau
    means that reading is stable.
    example tied to context:
        [0.155, 0.185) is a plateau: every
        cut in that range gives 21 clusters.

total contradiction
    a pair of leaves that share cells and
    disagree on every single one.

partial contradiction
    a pair of leaves that share cells and
    disagree on some of them.
    example tied to context:
        `cpp.xor` against `php.xor` is a
        total contradiction: 64 shared cells,
        64 disagreements.

positive control
    a pair whose answer is known before the
    machinery runs, used to test the
    machinery rather than the languages. if
    the known answer does not come back, the
    machinery is wrong.
    example tied to context:
        c++'s `and` is defined by the c++
        standard as another spelling of
        `&&`, so it must score 1.0000
        against `&&`. it does.

codegen refusal (in the runs: CODEGEN_REFUSE)
    the compiler accepted a probe when
    checking types but refused it when
    generating code. the probe produces no
    answer.
    example tied to context:
        swift's old accepted set carried
        1,066 of these; its new one carries
        zero.

route A, route C
    two ways a language is measured. a
    route-A language is compiled, so a probe
    first gets an ACCEPT or REFUSE verdict
    and needs a second run to get an answer.
    a route-C language is run directly, so
    acceptance and answer arrive together.
    example tied to context:
        c++ is route A, which is why its six
        word operations needed the extra
        `xw_cpp_00` execution lane. ruby and
        php are route C, which is why theirs
        came free.

leg G, leg R
    the two tests a word-spelled operation
    must pass to count as part of the
    language rather than part of a library.
    leg G asks whether the grammar declares
    the word in the operator slot of a
    two-sided expression. leg R asks whether
    the language's own checker refuses an
    ordinary variable named with that word.
    example tied to context:
        kotlin's `shl` fails both, so it is
        library and is not in the fold.

decision <n>
    a numbered ruling this node has made,
    kept so it can be overturned by number.
    they run 1 to 44; 44 is made in §7.
    example tied to context:
        decision 43 is the leg G plus leg R
        criterion above; decision 44 lifts an
        earlier voiding of three php rows.

stub (a stubbed lane)
    a lane that has been generated and
    written to disk but deliberately not run.
    example tied to context:
        the four kotlin aside lanes are
        stubbed: generated, sized, not run,
        and not to be folded in.

SUPERSEDED_
    a filename prefix. a product this pass
    replaced is renamed with it rather than
    deleted, so the older logs stay readable
    against the files they were written from.
    example tied to context:
        `SUPERSEDED_clusters_all12_log033.json`
        is the previous 226-leaf clustering,
        kept for the comparisons in §6.

provenance
    the record of how a number was arrived
    at: which instrument, which set of
    probes, which rows were thrown away.
    example tied to context:
        swift's answers did not change in
        this pass. what changed is that they
        no longer rest on throwing 1,066 rows
        away, which is a change of provenance
        and not of measurement.

bridge (a leaf bridges two clusters)
    a leaf that is close to members of two
    separate groups, so adding it makes the
    two groups join into one.
    example tied to context:
        `ruby.and` is close to `python.and`
        in one old group and to `ruby.or` in
        the other, so it bridged them.

signature
    everything recorded about one leaf: its
    domain, its answer classes, its tokens,
    its shape.
    example tied to context:
        all six swift signatures are
        byte-identical to the previous pass's.
```

---

## the earlier logs, restated so this one stands alone

Four earlier logs are needed to read this one. Each fact this log uses
from them is stated here in full, so no sentence below depends on
opening another file.

- **Log 033 published the clustering this pass replaces.** It covered
  twelve languages, had 226 leaves, and carried a footnote saying
  swift's numbers were taken with the wrong tool.
- **Log 034 did two jobs and left the clustering alone on purpose.**
  Job A re-measured swift with the real compiler instead of with
  `swiftc -typecheck`, which stops after type checking and therefore
  accepts programs the compiler later refuses. Job B built decision 43,
  the two-leg test described in the word list above, which admits
  word-spelled operations such as c++'s `and` and ruby's `or` on the
  same footing as `&&` and `||`.
- **Log 032 executed the accepted probe sets and produced the answers.**
  It is where swift's 1,066 codegen refusals were first counted.
- **Log 031 and log 030 are the earlier clustering and sweep passes.**
  Several of their numbered open items are answered or carried forward
  below, and each is restated where it comes up.
- **`HARVEST.md`** — full path
  `~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/HARVEST.md`
  — is the checklist written before this pass saying which lanes to
  collect, in what order, and what still had to be built. It was the
  authority for this pass.

Log 035 was free when this was written. It closes CHECK item 4ff, the
item that asked for exactly this collect-and-rebuild pass.

---

## §1 — walkthrough, in plain words

This pass has one job: collect the finished probe runs off disk and
rebuild the clustering from them. The previous published clustering,
`clusters_all12.json` and its picture `dendrogram_all12.html`, was
built before two corrections were made — swift's re-measurement with
the real compiler, and the admission of word-spelled operations like
c++'s `and`. Rebuilding it is what this log records.

**The collection itself was uneventful, and that is worth saying
plainly.**

- Every lane that the previous log listed as running or queued had
  finished by the time this pass started.
- All of them passed the completeness gate. All of them had zero
  `ENOSPC` lines. The scratch disk was left exactly where it started, at
  2,566 MB *(measured)*.
- Nothing had to be re-run for having died quietly. That is the first
  time in this node that has been true of a whole queue.

**Finding one: both positive controls pass, and they pass exactly.**

- The first control is c++'s six word-spelled operations. The c++
  standard defines `and`, `bitand`, `bitor`, `not_eq`, `or` and `xor`
  as alternative spellings of `&&`, `&`, `|`, `!=`, `||` and `^`. Each
  must therefore land at distance exactly zero from its symbol twin.
- The second control is ruby's `and`. It is the same operation as ruby's
  `&&`, at a different precedence, so it must land on `ruby.&&`.
- All seven predictions come back at similarity **1.000**, Jaccard
  1.000, agreement 1.000 *(measured)*. A machine with a systematic fault
  in how it turns answers into distances would not do that seven times
  in a row.

**Finding two: the picture moved more than the previous log predicted,
by three more leaves than it counted.**

- The previous log worked out 235 leaves. The actual number is **238**
  *(measured)*.
- The gap is bookkeeping, not surprise. Php's `and`, `or` and `xor`
  were counted as "not new" because they were already in php's
  operation menu. But they were marked VOID, and a VOID row is not a
  leaf. Lifting that voiding therefore adds three leaves where the
  prediction added none.

**Finding three: swift's position in the clustering did not move by a
single edge, and that is the right outcome rather than a
disappointment.**

- All 1,335 edges that touch a swift leaf have the same similarity they
  had in the previous clustering. All six swift signatures have
  byte-identical domains and answer classes *(measured)*.
- What changed is what the numbers rest on.
  - The previous pass's swift row was 1,552 answers with **1,066 rows
    thrown away** as codegen refusals, under decision 40.
  - This pass's swift row is the same 1,552 answers with **zero rows
    thrown away**, because the accepted set was taken with the compiler
    that would have done the refusing.
- So the answers were always the right answers. The record around them
  was wrong, and now it is not.

**Finding four: admitting ruby's word-spelled logicals merged two
coarse clusters.**

- This is the one place where the new leaves changed the structure
  rather than just joining it.
- At the stable [0.155, 0.185) reading, the previous pass had a
  four-member cluster and an eight-member cluster. This pass has one
  cluster of twelve *(measured)*.
- `ruby.and` and `ruby.or` are what bridged them: each is close to
  members of both old groups.
- The cluster count at that cut goes from 22 to 21. Twelve leaves were
  added and there is one fewer cluster.

**Finding five: there is a fourth total contradiction, and it is two
languages using the same spelling for two different operations.**

- `cpp.xor` and `php.xor` share 64 input cells and disagree on all 64
  *(measured)*.
- They are spelled the same and they are not the same operation. C++'s
  `xor` is the bitwise `^` and answers `whole:0`. Php's is a logical
  exclusive-or and answers `truth:false`.
- The three total contradictions found in the previous pass all stand
  unchanged.

**Finding six: this pass found two faults in its own new code, and a
check found both of them rather than a failure.**

- One fault made a lane compile the wrong operation entirely.
- The other silently dropped three leaves out of the rebuild.
- Neither raised an error. Both are written up in §3, because they are
  the interesting part of this pass.

---

## §2 — the harvest

Below is the queue of lanes that `HARVEST.md` asked for, checked
against what was actually on disk. Each row names what the lane is,
not only its short name.

| lane | what it ran | probes | state | gate |
|---|---|---|---|---|
| `vs_swift_00/01` | the two swift acceptance lanes, re-measuring swift's whole value matrix with the real compiler | 76,614 | done, 2,955 s | COMPLETE |
| `lr_words1..5` | the five reservation-probe passes, which ask each language's checker whether a word may be an ordinary variable name | 91 | done | controls ACCEPT |
| `rc_ruby2` | ruby re-run whole with the repaired driver | 285,144 | done, 2.6 s | COMPLETE |
| `rc_php2` | php re-run whole with the repaired driver | 223,587 | done, 0.7 s | COMPLETE |
| `vw_typescript_00` | typescript's acceptance run for its newly admitted word operation | 10,000 | done, 2.9 s | COMPLETE |
| `vw_cpp_00..02` | the three c++ acceptance lanes for its six word-spelled operations | 72,600 | done, 3,835 s | COMPLETE |
| `xr_swift_00` | swift's execution re-run over the new accepted set | 1,552 | done, 2.9 s | COMPLETE |
| `xw_cpp_00` | the c++ word-operation execution lane, built during this pass | 8,526 | **new this pass**, 4.6 s | COMPLETE |
| `ka_kotlin_00..03` | the four kotlin aside lanes, showing where kotlin's excluded library shifts would have landed | 89,304 | still deferred, stubbed | — |

- **Zero `ENOSPC` lines across every harvested lane log** *(measured)*.
  This was checked before anything was folded. Log 030 item 4m is the
  standing instruction to do so: it recorded that a lane which runs out
  of scratch space dies without reporting a failure.
- Every shard's `__SUMMARY__` line is present, and every probe count
  equals the count its plan stated *(measured)*. Re-running the swift
  gate reader `l3_swiftfull_read.py` on the landed shards prints
  `gate: COMPLETE`.
- **The last reservation pass, `lr_words5`, landed and closed the two
  unread cells the previous log left open.** Those two cells were
  python's `is not` and `not in`; a multi-word spelling counts as
  reserved only if every word in it is reserved, and `not` had not been
  probed. The result: python's `not` is reserved on leg R, but the
  python grammar does not declare `not` as a two-sided operator, so
  **`not` is LIBRARY while `is not` and `not in` are ADMITTED**
  *(measured)*. That answer keeps python's standing menu intact and
  costs nothing.

### 2.1 the one lane the previous log did not know it needed

`HARVEST.md` item 2 under "what still has to be built" asked for the
execution of the newly admitted operations — that is, actually running
them to get answers, rather than only finding out which ones compile.

- Ruby's and php's came free, as `HARVEST.md` said they would, because
  both are route-C languages: they are run directly, so acceptance and
  answer arrive together.
- C++'s did not come free. C++ is a route-A language: it is compiled, so
  the acceptance lanes `vw_cpp_*` gave its six words only an
  ACCEPT-or-REFUSE domain and no answers at all.
- Without answers there is nothing to score the positive control
  against, so a new execution lane had to be built.

`l3_wordexec.py` emits that lane the same way `l3_swiftexec.py` emits
swift's. The run: **8,526 accepted probes, 5 chunks, 4.6 s, 8,526
answers, zero raises, zero deaths, zero codegen refusals**
*(measured)*.

- **Typescript's `instanceof` needed no lane at all, and the reason is
  itself a finding.** The typescript acceptance lane
  `vw_typescript_00` accepted **0 of 10,000 probes** *(measured)*.
  - Decision 43 admits `typescript.instanceof` as a real operation of
    the language.
  - The probe space then gives it an empty domain, because every holder
    at this layer is a value, and `x instanceof 5` is a type error for
    every one of them.
  - Admitted-with-an-empty-domain is not the same thing as excluded,
    and `refold_index.json` records it as the former. It contributes no
    leaf.
  - Level **measured** for the count of zero; **derived** for reading
    it as an empty domain rather than a failure.

---

## §3 — the two faults this pass found in its own work

Both faults were caught by a number that had a predicted value. Neither
was caught by a crash: both lanes and both readers exited 0 and
reported success.

### 3.1 the operator list that did not reach the compiler

`l3_wordops.with_ops` is the patch that forces a language's operation
list to the word-spelled one. Every `vw_*` acceptance lane was
generated under it. It rebinds the name `ops` on three modules:
`l3_accept`, `l3_matrix` and `l3_routec`.

The execution path has a fourth module, and `l3_exec.py` line 51 reads

```
from l3_accept import LANG, holders, ops
```

That line binds `l3_exec`'s own module-level name to the function
object as it stands at import time. Rebinding `l3_accept.ops`
afterwards never reaches it.

- **So the first run of `xw_cpp_00` used c++'s standing menu instead of
  its word-spelled one.**
  - A probe id `Pi_j_x_y_k` carries `k` as a position in the operation
    list the probe was generated against.
  - In the word-spelled list, position 3 is `not_eq`. In c++'s standing
    menu, position 3 is `/`.
  - The lane dutifully compiled division.
- **2,466 of 8,526 probes came back `CODEGEN_REFUSE` and 426 came back
  DEATH** *(measured)*. The error text names the fault outright:

```
P0_0_0_0_3 CODEGEN_REFUSE
 error: no match for 'operator/'
 (operand types are 'std::monostate'
  and 'std::monostate')
```

- **The lane exited 0 and wrote a complete `__SUMMARY__` reporting its
  full 8,526 probes.** The completeness gate passed it.
  - What did not pass was a different expectation: a probe set that the
    compiler already accepted should produce zero codegen refusals.
  - That is the same check `l3_swiftexec.py` carries for swift, applied
    here for the same reason.
- The bad output is quarantined as `raw/VOID_xw_cpp_00_wrongops.txt`
  rather than deleted.
- The repaired run has **zero refusals and zero deaths** *(measured)*.
  `l3_wordexec.py` now asserts `E.table(lang)["ops"] == oplist` before
  it emits anything, so this fault cannot happen again without saying
  so.
- This is the sixth lane in this node to report success while having
  failed. It is the first to do so by reporting a full, gate-passing
  measurement of the wrong question. Level **measured** throughout.

### 3.2 the frozen manifest that dropped three leaves

`l3_answers12.load_three` walks the `operations` list inside each
language's manifest file, `manifest_<lang>.json`. Those manifests are
frozen records of a past run, and they were frozen in log 029 — long
before decision 43 admitted any word-spelled operation.

- **So the first re-fold produced 235 leaves and looked exactly
  right**, because 235 was the number the previous log had predicted.
  - It was right for the wrong reason. C++'s six had been folded in.
    Php's three VOID leaves had come back live.
  - But **`ruby.and`, `ruby.or` and `php.instanceof` were silently
    absent** *(measured)* — three leaves whose cells were sitting
    unread in `behavior_ruby_C.json` and `behavior_php_C.json`.
- It was caught by listing what the fold had added, rather than by
  counting what it produced. A count that matches a prediction is the
  weakest evidence available in this node, and this is the reason why.
- The repair appends the admitted operations to the frozen list at read
  time. It does not rebuild the manifests.
  - **A manifest is a frozen record of what was probed under a given
    plan. Re-freezing one to fix a reader destroys the thing the
    manifest exists to preserve.**
  - Holders and value classes do not depend on the operation list, so
    appending to the list at read time cannot change anything else.
    Level **derived**.

---

## §4 — the folds

`l3_refold.py` carries all three folds. Each one runs the standing
completeness gate. Each one keeps the file it replaces under a
`SUPERSEDED_` name rather than editing in place. The whole script is
safe to run twice: each fold reads the kept copy as its starting point,
so a second run gives the same file rather than folding the same
material in twice.

### 4.1 swift's execution redo, and the check it carries

| accepted set | probes in the set | answers produced | codegen refusals |
|---|---|---|---|
| the retired set, accepted by `swiftc -typecheck`, which stops after type checking | 2,618 | 1,552 | 1,066 |
| the new set, accepted by the full `swiftc`, which also generates code | 1,552 | 1,552 | **0** |

- **The check the previous log named passes** *(measured)*. That check
  was: the execution driver's codegen-repair loop should fire zero
  times, because the accepted set was taken with the compiler that
  would have done the refusing. It fired zero times. Under the old
  accepted set it fired 1,066 times, and never once for any other
  language.
- **And the two sets are the same set.** The full compiler's accepted
  count, the old run's answer count, and the new run's answer count are
  all 1,552. Three numbers from three different runs agree to the
  single probe. Level **measured** for all three counts; **derived**
  for reading their agreement as a cross-check.

### 4.2 c++'s six, folded in on top of what was there

| c++ operation set | probes | answers | deaths | codegen refusals |
|---|---|---|---|---|
| the symbol-spelled operations, already standing | 27,385 | 26,905 | 480 | 0 |
| the six word-spelled ones admitted by decision 43 | 8,526 | 8,526 | 0 | 0 |
| the two merged into one c++ answer file | 35,911 | 35,431 | 480 | 0 |

- The merge only adds; it replaces nothing. That was checked rather
  than assumed: no probe-id-and-operation key collides between the two
  sets, and no word-spelled operation was already in c++'s standing
  menu *(both asserted in the code, both hold)*.

### 4.3 route C re-read from the repaired runs

Ruby and php are the two route-C languages: they are run directly, so
each probe's acceptance and its answer arrive together. Both were
re-run whole with a repaired driver before this pass.

| language | probes | answers | raises | lane it came from | gate |
|---|---|---|---|---|---|
| ruby | 285,144 | 76,270 | 208,874 | `rc_ruby2` | COMPLETE |
| php | 223,587 | 98,245 | 125,342 | `rc_php2` | COMPLETE |

- **The repair did reach the clustering, and that is shown here rather
  than asserted.** `php.and` has 64 cells in its domain, and **57 of
  them changed answer class** *(measured)*:

```
php `and', cell fractional|fractional
 before  fractional:1.5, fractional:inf,
         fractional:nan
         -- these are the LEFT OPERAND
 after   truth:true, truth:false
         -- these are the operation's result
```

---

## §5 — the positive controls

A positive control is a pair whose answer is known before the machinery
runs. If the known answer does not come back, the machinery is wrong.
This pass has two that were predicted in advance, and one that fell
out of the repair.

### 5.1 control A — c++'s six words against their symbol twins

The c++ standard defines each of these six words as an alternative
spelling of a symbol operator. Scored first on the answers directly,
before any clustering runs:

| word operation | its symbol twin | cells they share | cells they agree on | cells they disagree on |
|---|---|---|---|---|
| `cpp.and` | `cpp.&&` | 2,380 | 2,380 | **0** |
| `cpp.bitand` | `cpp.&` | 676 | 676 | **0** |
| `cpp.bitor` | `cpp.\|` | 676 | 676 | **0** |
| `cpp.not_eq` | `cpp.!=` | 1,738 | 1,738 | **0** |
| `cpp.or` | `cpp.\|\|` | 2,380 | 2,380 | **0** |
| `cpp.xor` | `cpp.^` | 676 | 676 | **0** |

And then scored inside the clustering, which is where the prediction
was actually made. A similarity of 1.0000 means the two leaves sit at
distance exactly zero from each other.

| pair | similarity | Jaccard | agreement | shared inputs |
|---|---|---|---|---|
| `cpp.and` ~ `cpp.&&` | **1.0000** | 1.0000 | 1.0000 | 562 |
| `cpp.bitand` ~ `cpp.&` | **1.0000** | 1.0000 | 1.0000 | 64 |
| `cpp.bitor` ~ `cpp.\|` | **1.0000** | 1.0000 | 1.0000 | 64 |
| `cpp.not_eq` ~ `cpp.!=` | **1.0000** | 1.0000 | 1.0000 | 282 |
| `cpp.or` ~ `cpp.\|\|` | **1.0000** | 1.0000 | 1.0000 | 562 |
| `cpp.xor` ~ `cpp.^` | **1.0000** | 1.0000 | 1.0000 | 64 |

```
CONTROL A PASSES.  Every c++ word answers
exactly what its symbol twin answers, on
every shared cell, and lands at distance
exactly zero from it.
```

- One cell worked through, `cpp.xor` against `cpp.^` on the cell
  `truth|truth`, showing the answers themselves rather than the score:

```
truth|truth  ^  : whole:0, whole:1
truth|truth  xor: whole:0, whole:1
```

### 5.2 control B — ruby's `and` against ruby's `&&`

Ruby's `and` is the same operation as ruby's `&&`, written at a
different precedence, so the two must give the same answers.

| word operation | its symbol twin | cells they share | cells they agree on | cells they differ on | of those, cells carrying a memory address |
|---|---|---|---|---|---|
| `ruby.and` | `ruby.&&` | 11,881 | 10,663 | 1,218 | **1,218** |
| `ruby.or` | `ruby.\|\|` | 11,881 | 10,607 | 1,274 | **1,274** |

```
CONTROL B PASSES.  Every difference between
the word form and the symbol form carries a
hexadecimal object address, so it is the
known recorder fault and not a real
disagreement.  Similarity in the clustering
is 1.0000 for both pairs.
```

- **This closes the one line the previous log had to leave
  unverified.** That log could not compare `ruby.or` against
  `ruby.||`, because its throwaway checking script split each raw line
  from the left, and the operation name `||` contains the character the
  raw files use to separate fields. That is the same trap recorded as
  log 027 finding 11, turning up for a third time.
  - The control here matches on the end of the probe id instead of the
    start, so it does not have the fault.
  - Result: **11,881 shared cells, 1,274 differing, all 1,274 carrying
    a memory address** *(measured)*. That claim moves from unverified
    to measured.
- The 1,218 and the 1,274 are the same known problem rather than a hole
  in the control. Ruby's anonymous struct and data classes print their
  memory address when inspected, so those cells are not reproducible
  between two runs of the *same* probe either. That recorder fault is
  still unfixed and is carried forward in §8.

### 5.3 a third control, which this pass did not plan — php

This one was not predicted by the previous log. It falls out of the
route-C repair.

| pair | similarity | shared inputs |
|---|---|---|
| `php.and` ~ `php.&&` | **1.0000** | 1,156 |

- Before the repair, `php.and` was marked VOID and had been recording
  the left operand instead of the result.
- After the repair, php's word-spelled logicals sit exactly on php's
  symbol-spelled logicals, which is what php's own manual says they
  are.
- **That is a third independent confirmation that the parenthesis
  repair did what it claimed**, and it needed no new run. Level
  **measured**.

---

## §6 — where the picture moved against the previous clustering

Every comparison below is against log 033's published clustering, the
226-leaf one, kept on disk as
`SUPERSEDED_clusters_all12_log033.json`.

### 6.1 the totals

| measure | log 033 | log 035 |
|---|---|---|
| leaves — one operation of one language | 226 | **238** |
| edges — measured closeness between two leaves | 25,425 | 28,203 |
| input cells — operand-kind combinations asked about | 111,410 | 119,944 |
| value answers recorded | 399,845 | 446,491 |
| raises — probes that threw instead of answering | 549,231 | 567,997 |
| deaths — probes that killed their runner | 480 | 480 |
| rows thrown away as codegen refusals | 1,066 | **0** |
| VOID leaves — rows kept on record but not used | 3 | **0** |
| total contradictions — pairs disagreeing on every shared cell | 3 | **4** |
| partial contradictions — pairs disagreeing on some | 628 | 640 |
| pairs agreeing on every shared cell | 343 | 343 |

- The twelve new leaves are **`cpp.and`, `cpp.bitand`, `cpp.bitor`,
  `cpp.not_eq`, `cpp.or`, `cpp.xor`, `ruby.and`, `ruby.or`,
  `php.instanceof`, `php.and`, `php.or`, `php.xor`** *(measured)*.
  **No leaf was lost.**
- The arithmetic: 226 old leaves, plus c++'s six, plus ruby's two, plus
  php's `instanceof`, plus php's three that stopped being VOID, is 238.
  The previous log predicted 235 by not counting those last three.
  Level **derived** for this reconciliation.

### 6.2 swift — six leaves before, six leaves after

The previous log predicted swift would not gain leaves, and it does
not.

| swift leaf | cells in its domain, log 033 | cells in its domain, log 035 | codegen refusals then | codegen refusals now |
|---|---|---|---|---|
| `swift.*` | 2 | 2 | 106 | **0** |
| `swift.<` | 7 | 7 | 320 | **0** |
| `swift.>` | 7 | 7 | 320 | **0** |
| `swift.>=` | 7 | 7 | 320 | **0** |
| `swift.&&` | 1 | 1 | 0 | 0 |
| `swift.\|\|` | 1 | 1 | 0 | 0 |

- **All 1,335 edges touching a swift leaf have the same similarity they
  had in log 033, to the last digit, and all six swift signatures have
  identical domains and identical answer classes** *(measured)*.
- So the honest statement is the narrow one: **the swift redo changed
  how swift's numbers were arrived at, not where swift sits.**
  - Decision 40 was the ruling that throws away rows the compiler
    refused at code-generation time. It was throwing away 1,066 rows
    that should never have been in the accepted set in the first place.
  - Throwing them away gave the same answers as never admitting them.
  - That the two agree is the strongest available evidence that
    decision 40 was doing the right thing with the wrong input. Level
    **measured** for the equality; **derived** for that reading.
- Swift's leaf count is six, and stays six, because of its grammar
  rather than its compiler. The tree-sitter grammar parses swift's `+`
  through a catch-all `custom_operator` node, so `+`, `-`, `/`, `%`,
  `==` and `!=` have never been in swift's operation menu at all. That
  was established in log 028, it is unchanged here, and it remains the
  single largest known gap in the twelve-language picture.

### 6.3 where the admitted word operations landed

Read at the stable [0.155, 0.185) cut. Every one of the twelve joins a
cluster containing operations from its own language. None is
unattached and none crossed into another language.

| leaf | size of the cluster it joined | its same-language neighbours in that cluster |
|---|---|---|
| `cpp.and` | 46 | `cpp.&&`, `cpp.\|\|`, `cpp.!=`, `cpp.or`, `cpp.not_eq` |
| `cpp.or` | 46 | `cpp.&&`, `cpp.\|\|`, `cpp.!=`, `cpp.and`, `cpp.not_eq` |
| `cpp.not_eq` | 46 | `cpp.&&`, `cpp.\|\|`, `cpp.!=`, `cpp.and`, `cpp.or` |
| `cpp.bitand` | 14 | `cpp.&`, `cpp.\|`, `cpp.^`, `cpp.<<`, `cpp.>>`, `cpp.%` |
| `cpp.bitor` | 14 | `cpp.&`, `cpp.\|`, `cpp.^`, `cpp.<<`, `cpp.>>`, `cpp.%` |
| `cpp.xor` | 14 | `cpp.&`, `cpp.\|`, `cpp.^`, `cpp.<<`, `cpp.>>`, `cpp.%` |
| `ruby.and` | 14 | `ruby.&&`, `ruby.\|\|`, `ruby.or`, `ruby.<=>` |
| `ruby.or` | 14 | `ruby.&&`, `ruby.\|\|`, `ruby.and`, `ruby.<=>` |
| `php.and` | 46 | `php.&&`, `php.==`, `php.!=`, `php.<`, `php.===` |
| `php.or` | 46 | `php.&&`, `php.==`, `php.!=`, `php.<`, `php.===` |
| `php.xor` | 46 | `php.&&`, `php.==`, `php.!=`, `php.<`, `php.===` |
| `php.instanceof` | 46 | `php.&&`, `php.==`, `php.!=`, `php.<`, `php.===` |

- **C++'s six split exactly the way the c++ standard says they should.**
  The three that stand for logical and equality operations went to the
  cluster of operations that return booleans. The three that stand for
  bitwise operations went to the cluster of operations that return
  integers and truth values *(measured)*. Nothing in the machinery was
  told which was which.
- **`php.instanceof` is the one admitted leaf with no twin to check it
  against**, so it has no control.
  - It sits in php's boolean-returning cluster, closest to `php..` at
    0.581, and to `php.>` and `php.===` at 0.518.
  - That is where a boolean-returning php operation belongs. Level
    **measured** for the distances; **derived** for calling that the
    right place.
- **`java.instanceof`, `csharp.is` and `csharp.as` are not leaves at
  all**, and this pass does not change that.
  - They fail leg G, the grammar test: their grammar node puts a *type*
    in the right-hand slot, not an expression.
  - This layer has no type operands to probe them with, so there is
    nothing to measure.
  - `php.instanceof` becomes a leaf because php's grammar puts an
    *expression* in that slot.

### 6.4 the shift group is unchanged, exactly as predicted

The shift group is the set of leaves that perform bit-shifting and
cluster together across languages.

```
log 033: dart.<<  dart.>>  go.&^  go.<<
         go.>>    java.<<  java.>> java.>>>
         ruby.>>  rust.<<  rust.>>   -- 11

log 035: the same eleven.  No twelfth.
```

- Decision 43 rules kotlin's `shl` a library function on both legs — the
  kotlin grammar does not declare it as an operator, and `val shl: Int
  = 1` compiles — so it is not in the fold and could not have joined.
  The prediction was made before the run and the run agrees. Level
  **measured**.

### 6.5 the one structural change — a cluster merge caused by ruby

| reading | log 033 | log 035 |
|---|---|---|
| number of clusters at the [0.155, 0.185) cut | 22 | **21** |

Twelve leaves were added and there is one fewer cluster. The cause is
specific:

```
log 033, two separate clusters:
  python.and  ruby.&&  ruby.<=>
  typescript.&&
and
  python.or   ruby.||  typescript.||
  typescript.??  csharp.??  dart.??
  kotlin.-  kotlin.?:

log 035, ONE cluster of twelve: the union
of those two, bridged by ruby.and and
ruby.or.
```

- **The newly admitted operations did not merely take up residence.
  One pair of them changed the coarse reading** *(measured)*.
  `ruby.and` is close to `python.and` and also close to `ruby.or`, and
  the two old clusters each held only one of those.
- This answers a question raised as log 031 item 4r and carried forward
  as log 033 item 4x: whether the logical operations that return one of
  their operands, rather than a boolean, form a single group across
  languages. With ruby's word spellings in, at this reading, they do.
  Level **measured** for the merge; **derived** for reading it as an
  answer to that item.

### 6.6 the plateau structure

A plateau is a run of cuts over which the number of clusters does not
change. A wide plateau means that reading is stable.

| plateau | log 033 | log 035 |
|---|---|---|
| [0.155, 0.185) | 22 clusters | **21 clusters** |
| [0.465, 0.499) | 80 clusters, the widest | narrows to [0.472, 0.499), 81 clusters |
| [0.697, 0.730) | 115 clusters | narrows to [0.706, 0.730), 116 clusters |
| the widest plateau overall | [0.465, 0.499), width 0.0340 | **[0.155, 0.185), width 0.0302** |

- **The [0.155, 0.185) plateau holds its bounds to six decimal places
  across a change of twelve leaves** *(measured)*.
  - It became the widest plateau not by growing but because the two
    plateaus above it narrowed.
  - That is a stability statement, and it is worth more than the
    "widest" label: the reading that survives adding twelve leaves
    unchanged is the one at 0.155.
- Log 030 item 4n recorded that the curve of cluster count against cut
  distance has no elbow — no natural place to stop. That still holds,
  and no cut is chosen here either.

### 6.7 log 033's three contradictions — do they stand?

**All three stand, unchanged, at the same rates** *(measured)*. The
fourth row is the new one.

| pair | shared cells | cells they disagree on | rate | which side of the static-versus-open divide each is on |
|---|---|---|---|---|
| `cpp.<=>` vs `php.<=>` | 211 | 211 | 1.000 | static\|open |
| `cpp.<=>` vs `ruby.<=>` | 211 | 211 | 1.000 | static\|open |
| `kotlin...` vs `rust...` | 112 | 112 | 1.000 | static\|static |
| **`cpp.xor` vs `php.xor`** | **64** | **64** | **1.000** | static\|open |

The fourth is new, and it is a direct product of both of the previous
log's two jobs. `cpp.xor` exists as a leaf because decision 43 admitted
it. `php.xor` is a leaf again because decision 44, below, lifted the
voiding of it. The worked cells:

```
cell truth|truth
 cpp.xor -> whole:0, whole:1
 php.xor -> truth:false, truth:true
```

- **This is a spelling collision, not a disagreement about a shared
  operation.** C++'s `xor` is the alternative token for `^` and returns
  an integer. Php's `xor` is a logical exclusive-or and returns a
  boolean. Two languages spell two different operations with the same
  three letters.
- It is also the first contradiction in this node that decision 39 does
  not explain. Decision 39 explains a contradiction as two operations
  being kept apart because their operand kinds do not match. Here the
  operands are the same, the operation names are the same, and the
  answers are of different kinds because the *operations* are
  different. Level **measured** for the rate and the answers;
  **derived** for the reading.
- One more number is worth naming. The total-contradiction count went
  from 3 to 4 while the count of pairs agreeing on every shared cell
  stayed at exactly 343. The twelve new leaves added 13 same-spelling
  pairs and 12 partial contradictions, and not one new pair that agrees
  everywhere *(measured)*.

---

## §7 — decision 44

Decisions are the numbered rulings this node has made, kept so that any
one of them can be overturned by number. Decisions 1 to 17 stand where
log 030 left them, 18 to 30 where log 031 left them, 31 to 42 where log
033 left them, and 43 where log 034 left it. This is **44**.

```
DECISION 44 -- decision 30's voiding of php's
`and', `or' and `xor' is LIFTED.

Decision 30 voided those three rows because
`$__r = ($a) and ($b);' binds as
`($__r = $a) and $b'.  Php's word-spelled
logicals sit BELOW assignment in precedence,
so the assignment happened first and the
recorded answer was the LEFT OPERAND, on all
6,241 answer cells.

The fault is repaired in `l3_wordops.repair_
routec', php was re-run WHOLE as the lane
`rc_php2', and `l3_refold.refold_routec'
folded that run into `behavior_php_C.json'.
The three rows are measurements again and
are leaves again.

The voiding is KEPT in the code beside the
lifting, not deleted, because decision 30
produced published numbers in logs 031 and
033, and those logs must stay readable
against the reason they excluded three
leaves.

CONSEQUENCE, stated here so it is not
discovered later: logs 031 and 033 report
php `and'/`or'/`xor' numbers taken under the
fault.  They are not comparable with log
035's -- in the same way decision 31 made
log 031's and log 033's A factors
incomparable.
```

Level **measured** that the repair changed 57 of the 64 domain cells.
Level **derived** for the lifting being the right response to that.

---

## §8 — honest remainders

Each item below is something this pass did not settle. Each says what
the state of it is.

- **Ruby's recorder fault is unfixed.** The previous log measured 2,492
  of 249,501 ruby cells carrying a hexadecimal memory address, and
  therefore not reproducible between two runs of the same probe.
  - This pass measured the same fault from a different direction —
    1,218 and 1,274 out of 11,881 in control B, §5.2 — and did not fix
    it.
  - It has been in every ruby product since log 027.
  - The fix is the one log 032 applied to kotlin: record the class name
    and the structure, never the default inspection text of an
    anonymous class.
  - Level **measured** for the counts; **unverified** what the
    corrected answers would be.
- **`php.instanceof` has no control.** Every other leaf this pass added
  had a twin whose answer was predictable in advance. It landed
  plausibly, and that is a weaker claim than the six-plus-two above.
- **Typescript's `instanceof` is admitted with an empty domain**, so
  decision 43's typescript admission is not tested by any answer.
  Whether a probe space containing type operands would give it a domain
  is **unverified**. It is the same gap that keeps `java.instanceof` and
  `csharp.is` out.
- **The kotlin aside is still deferred and still unrun.** Those are the
  four lanes `ka_kotlin_00..03`, 89,304 probes, about 78 minutes
  *(estimate)*, which would show where kotlin's excluded library shifts
  would have landed.
  - It must never be folded into the default clustering.
  - It answers a different question from the one decision 43 answers.
- **Decision 43's leg G — the grammar test — can only see what
  tree-sitter's grammars declare**, and swift and dart are still the two
  languages it cannot see, because their grammars spell operators in a
  way the test cannot read. Nothing in this pass tests that.
- **The criterion has been applied to the operator vocabulary only.**
  Indexing, calling, member access and iteration are untouched.
- **The cross-check against `kind_signature_clustering` is still not
  started.** That is CHECK item 4j, still the oldest unstarted item in
  the node, and now the only phase-4 item still open.
- **Rust's panic is still a debug-build fact**, one release build away
  from settled.
- **Decisions 26 and 27 remain open for the owner**, and the
  partially-loaded-holders default — a holder that loaded only some of
  its value classes is probed with the ones that loaded — remains
  ratified by silence.
- **`clusters_all12.json` is not byte-identical between two runs, and
  the difference is confined to two display fields.** Running
  `l3_answers12.py` twice on identical inputs gives two files that
  differ. The difference was chased down rather than shrugged at:

```
 differing top-level keys: built, signatures
 signature fields ever differing:
   answer_classes
   `top'   648 same set, order only
           232 set differs, a truncation tie
   `kinds' 299
 edges          identical
 merge_history  identical
 plateaus       identical
 snapshots      identical
 contradicts    identical
 dendrogram_all12.html  BYTE-IDENTICAL
```

  - The cause: `answer_classes` builds its per-cell counts by walking a
    set, so the order varies between runs. Both `top` (which is cut to
    four entries) and `kinds` are sorted by count, with ties broken by
    that varying order *(measured)*.
  - **The tokens, the shape, every domain, every edge, the whole merge
    history, every plateau, every snapshot and every contradiction are
    identical.** That is why the picture comes out byte-identical:
    nothing load-bearing moves.
  - It is a presentation fault, not a measurement fault. It is recorded
    rather than fixed, because fixing it means changing a sort key in a
    file this pass had no other reason to touch. Level **measured**.
- **`l3_answers.py`, run as a script, no longer reproduces log 031
  exactly**, because it reads `behavior_php_C.json` and
  `behavior_ruby_C.json` and both of those are now the repaired runs.
  Its docstring still claims it does.
  - The pre-repair products are kept as
    `SUPERSEDED_behavior_<lang>_C_preparen.json`, and pointing the
    script at them would restore the claim.
  - That is one line, and it is not done. Level **measured** that the
    inputs changed.

---

## §9 — artifacts

All paths are inside
`~/Programming/PseudoCoupHQ/Research/kind_fuzz_clustering/`.

| file | what it is |
|---|---|
| `l3_wordexec.py` | builds the execution lane for the newly admitted word-spelled operations; carries the operation-list assertion that §3.1's fault cost |
| `l3_refold.py` | the three folds, their completeness gates, and the two positive controls |
| `refold_index.json` | the folds' counts, and both controls' full output |
| `answers_swift.json` | swift's answers over the accepted set taken with the full compiler; nothing thrown away |
| `SUPERSEDED_answers_swift_typecheck.json` | swift's retired answers, the ones with 1,066 codegen refusals, kept on the record |
| `answers_cpp.json` | c++'s answers, symbol-spelled operations and the six word-spelled ones together |
| `SUPERSEDED_answers_cpp_symbolsonly.json` | the symbol-only c++ answers the fold merges into, kept |
| `behavior_ruby_C.json`, `behavior_php_C.json` | the repaired whole re-runs of the two directly-run languages |
| `SUPERSEDED_behavior_*_C_preparen.json` | the same two before the parenthesis repair, kept |
| `raw/xw_cpp_00.txt` | the raw output of c++'s word-operation execution lane, 8,526 probes |
| `raw/VOID_xw_cpp_00_wrongops.txt` | the bad run from §3.1, quarantined rather than deleted |
| `raw/SUPERSEDED_rc_ruby_preparen.txt` | ruby's raw output from before the repair, renamed to this node's convention |
| `clusters_all12.json` | **the rebuilt clustering, 238 leaves** |
| `SUPERSEDED_clusters_all12_log033.json` | the previous 226-leaf clustering, kept for the comparisons in §6 |
| `dendrogram_all12.html` | **the picture of the rebuilt clustering, 238 leaves, 475 nodes** |
| `SUPERSEDED_dendrogram_all12_log033.html` | the previous picture, kept |

The picture is checked by running it under a stand-in for the browser's
document model, the same way the previous one was checked. The command
and its output:

```
node domstub.js dendrogram_all12.html
 scripts: 2 run, 2 ok, 0 threw
 elements written: 5
 #chart 1 appended, #curve 1 appended
 #count reads 115 at the default 0.700
```

- That reported count of 115 is checked against the plateau table
  rather than eyeballed: **0.700 falls inside [0.694444, 0.706118),
  whose cluster count is exactly 115** *(measured)*.
