# log 175 — task 72: the go diaries for the current corpus, and the coverage they measure

Date: 2026-09-03. Node: `hq.research.compiler_graph.graph`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/CORE_0_3_5_9_graph.md`),
sub-nodes `dynamic_structure` and `coverage`. Round 14 as reordered by
log_173.

---

# 1. What was done, in plain words

## 1.1 The one-line account

Every go probe of the current corpus was recompiled through a go
compiler that writes down which of its own functions it enters, in
order; those 590 ordered records were joined to the region graph; and
the join says that **818 of the 1,549 function bodies of go's lowering
region are never entered by any probe we have**.

## 1.2 The walk, without figures

- The go compiler's source was copied out of the read-only tree and
  edited so that **every function body in the lowering region**
  announces its own graph-node id as it is entered. The region is the
  four packages the CORE names: `ssagen`, `abi`, `amd64`, `ssa`.
- That compiler was rebuilt, and each of the corpus's go probes was
  compiled by it, one at a time, each writing its own file. One file
  per probe, one line per entry, in the order the entries happened.
  That is a DIARY and not a tally: nothing is counted, the sequence is
  kept.
- The diaries were joined back to the region graph. For each graph node
  the join says which probes entered it; for each probe it says which
  nodes it walked, in first-entry order.
- The never-entered list is the finding. It is not noise: it is whole
  files — the SIMD instruction emitters, the magic-number division
  helpers, the conditional-branch merger, the compiler's HTML debug
  writer. Our probes are scalar two-operand expressions, so the parts of
  the compiler that exist for other shapes of program are never reached,
  and now that is measured rather than assumed.
- For clang, rustc and swiftc no diaries were made this round; what was
  made instead is a **cost page** (§6), every number on it measured on
  this machine in this session. Two of the three turned out to be
  blocked by facts about what is on this disk, not by build time, and
  measuring found that where reading about it would not have.

## 1.3 What is NOT claimed

- Nothing about the other four languages' units. Only go was diaried.
- "Never visited" is said **only** about the 1,549 bodies an edit was
  actually placed in. The region graph has 174,159 nodes; the other
  172,610 are refs, calls, parameters and locals — positions inside a
  body, not places a statement can be inserted. They were not observed,
  and an unobserved node is a named frontier, never a never-visited one.
  That distinction is now a settled rule in the CORE.
- The join is against the AUGUST region graph (`graph_go4.json`), not
  task 71's `graph_go.json`, because the latter did not exist when
  targets had to be selected. The re-join is one command and needs no
  recompile; §5.3 gives it.

---

# 2. The instrument, with values moving through it

## 2.1 What one hook is

A go function of the region, before the edit — LITERAL, from
`/sources/golang_src/src/cmd/compile/internal/abi/abiutils.go:353`:

```go
func (config *ABIConfig) ABIAnalyzeFuncType(ft *types.Type) *ABIParamResultInfo {
	setup()
```

After the edit, exactly one statement is inserted after the brace that
opens the body:

```go
func (config *ABIConfig) ABIAnalyzeFuncType(ft *types.Type) *ABIParamResultInfo {
	diary.Note("src/cmd/compile/internal/abi/abiutils.go:12127-13356:method|ABIAnalyzeFuncType|src/cmd/compile/internal/abi/abiutils.go:353")
	setup()
```

GLOSS of the string: it is the node's id in the region graph
(`<file>:<start byte>-<end byte>:<kind>`), then the function's name,
then its original file and line. The id is written into the source at
injection time, so a diary line joins to a graph node by string
equality — no line matching, no interpretation step.

## 2.2 What one diary line is

LITERAL — the first four lines of
`Research/compiler_graph/diaries/go/op_0.txt`:

```
1	-	src/cmd/compile/internal/ssa/rewrite.go:22841-22896:func|StringToAux|src/cmd/compile/internal/ssa/rewrite.go:815
2	-	src/cmd/compile/internal/ssa/rewrite.go:22841-22896:func|StringToAux|src/cmd/compile/internal/ssa/rewrite.go:815
3	-	src/cmd/compile/internal/ssa/rewrite.go:22841-22896:func|StringToAux|src/cmd/compile/internal/ssa/rewrite.go:815
4	-	src/cmd/compile/internal/ssa/addressingmodes.go:3140-3212:func|init|src/cmd/compile/internal/ssa/addressingmodes.go:107
```

GLOSS, column by column:

| column | separator | what it is |
|---|---|---|
| `1` | tab | the sequence number — the order, which is the whole point |
| `-` | tab | the SUBJECT: the name of the function the compiler had in hand. `-` means no subject was open (compiler set-up, before any function is dequeued) |
| `src/...rewrite.go:22841-22896:func` | pipe | the region-graph node id |
| `StringToAux` | pipe | the function's name |
| `src/...rewrite.go:815` | end | its original file and line |

The first three lines are the same node three times. That is correct
and is what a diary is for: a tally would say "StringToAux: 3" and lose
where in the run those three sat.

## 2.3 Two compiles interleaving, and the subject separating them

LITERAL — `Research/compiler_graph/diaries/go/regen_400.txt`, events
2525-2536, unedited:

```
2525	main	src/cmd/compile/internal/abi/abiutils.go:13858-14278:method|ABIAnalyze|src/cmd/compile/internal/abi/abiutils.go:397
2526	op_400	src/cmd/compile/internal/ssa/numberlines.go:2142-2320:func|notStmtBoundary|src/cmd/compile/internal/ssa/numberlines.go:63
2527	main	src/cmd/compile/internal/abi/abiutils.go:12127-13356:method|ABIAnalyzeFuncType|src/cmd/compile/internal/abi/abiutils.go:353
2528	op_400	src/cmd/compile/internal/ssagen/ssa.go:51964-52087:method|entryNewValue0|src/cmd/compile/internal/ssagen/ssa.go:1364
2529	main	src/cmd/compile/internal/abi/abiutils.go:19681-20459:func|setup|src/cmd/compile/internal/abi/abiutils.go:573
2530	op_400	src/cmd/compile/internal/ssagen/ssa.go:51498-51889:method|entryBlock|src/cmd/compile/internal/ssagen/ssa.go:1351
2531	main	src/cmd/compile/internal/abi/abiutils.go:17389-17489:func|alignTo|src/cmd/compile/internal/abi/abiutils.go:497
2532	op_400	src/cmd/compile/internal/ssa/func.go:14563-14723:method|NewValue0|src/cmd/compile/internal/ssa/func.go:459
2533	main	src/cmd/compile/internal/abi/abiutils.go:17389-17489:func|alignTo|src/cmd/compile/internal/abi/abiutils.go:497
2534	op_400	src/cmd/compile/internal/ssa/func.go:10280-10769:method|newValue|src/cmd/compile/internal/ssa/func.go:282
2535	main	src/cmd/compile/internal/ssa/op.go:11960-12325:func|OwnAuxCall|src/cmd/compile/internal/ssa/op.go:343
2536	main	src/cmd/compile/internal/abi/abiutils.go:1455-1535:method|InRegistersUsed|src/cmd/compile/internal/abi/abiutils.go:51
```

GLOSS, values in motion. The compiler runs with `-c=6`, so it compiles
this probe's two functions at the same time on two goroutines. Read
column 2 down the block and the two runs separate cleanly:

- `main`'s run, events 2525 → 2527 → 2529 → 2531 → 2533 → 2535 → 2536:
  `ABIAnalyze` calls `ABIAnalyzeFuncType`, which calls `setup`, which
  calls `alignTo` twice, and the argument area is then described by
  `OwnAuxCall` and `InRegistersUsed`. That is a named parameter being
  turned into a stack offset and a register, step by step.
- `op_400`'s run, events 2526 → 2528 → 2530 → 2532 → 2534: the probe's
  own function is being built into SSA — `entryBlock`, `entryNewValue0`,
  `NewValue0`, `newValue`.

The two chains are *perfectly interleaved in the sequence numbers* and
have nothing to do with each other. Order alone would read this as one
chain; the subject column is what makes it two. This is the same effect
the August lap recorded at its events 42-46, now visible over the whole
region rather than at 56 spots.

---

# 3. What was built, and the two defects the building found

## 3.1 The chain of files

| file | what it does | new? |
|---|---|---|
| `Research/compiler_graph/coverage.py` | `class Graph(graph.Graph)`: `diary_targets` (selection), `diary` (the reader), `coverage` (the join) | new |
| `Research/compiler_graph/t72/inject_diary_region.py` | the edit half: places one entry hook at each selected byte coordinate | new |
| `Research/compiler_graph/lanes_t72/t72_l1..l7` | the lanes: toolchain, inject+build, smoke, the 590 compiles, two cost-page passes | new |
| `Research/compiler_graph/inject_diary.py` | the August ancestor | **untouched** |
| `Research/compiler_graph/graph.py` | task 71's file | **untouched** — see §3.2 |

## 3.2 Why `coverage.py` is a subclass and not an edit to `graph.py`

The binding rule says to extend task 71's `graph.py` if it exists. It
does (mtime 2026-09-03 18:26) and it already implements `build`,
`query_path`, a one-column diary reader and a coverage join. But task 71
was still running in parallel, and editing a file another task may be
writing is how a round loses work. So the additions are
`class Graph(graph.Graph)` in `coverage.py`: every method of task 71's
class is inherited unchanged, three are added, two are overridden with
wider readers that still accept the old input. The file's header states
the fold-in: move `diary_targets`, `diary` and `coverage` into
`class Graph` verbatim when task 71's file settles, and delete
`coverage.py`. Nothing else references it.

## 3.3 Defect one: byte offsets read as character offsets

The region graph records `start_byte` and `end_byte`. The first version
of the injector indexed a decoded Python string with them. In files
containing non-ASCII — `ssa/magic.go`'s comments use the mathematical
ceiling brackets, three bytes each — every offset after the first such
character lands in the wrong place.

How it surfaced: a dry run reported **75 targets skipped, cause
"no body brace in own bytes"**, and every one of them was a correctly
formed one-line body:

```
src/cmd/compile/internal/ssa/magic.go 101 umagicOK8 func
```

LITERAL, `/sources/golang_src/src/cmd/compile/internal/ssa/magic.go:101`:

```go
func umagicOK8(c int8) bool   { return c&(c-1) != 0 }
```

The skip was the *safe* symptom. The unsafe one was silent: a target
whose window had shifted but still contained some `{` would have been
injected into a NEIGHBOURING function, and the diary would then have
attributed one function's entries to another with nothing to show it.
The injector now works on bytes throughout — read `rb`, scan bytes,
write `wb`. After the fix: **1,549 targets read, 1,549 instrumented, 0
skipped.**

## 3.4 Defect two: the join read the wrong record shape and reported zero

The first join returned `bodies_visited_by_at_least_one_probe = 0` over
590 diaries. The reader had been written from `diary_meta.md`'s prose
("tab separated: seq, subject, map_node_id, spot_name, file:line") and
expected five tab fields. The hook actually writes **three tab fields**,
the third being three PIPE fields — which is the August format, byte for
byte. The reader now takes its shape from the file (§2.2), not from
prose about the file. That is the §5.1a lesson applied to our own
records: the literal is the authority.

Both defects are recorded here rather than quietly fixed because a
coverage number produced by either of them would have looked exactly as
plausible as the right one.

---

# 4. The lap, measured

## 4.1 The corpus, counted from the manifests

| population | count | read from |
|---|---|---|
| original go units | 107 | `canon39_wrapped_go.json` → `units` |
| regenerated go units | 483 | `canon39_regen_store/op_units2_go_c0000.json` (330) + `...c0001.json` (153) |
| **go units of the corpus** | **590** | the two above |
| their probe sources | 590 of 590 found | `probe_manifest_go.json` (744 probes) and `probe_manifest2_go.json` (553 probes) |

The manifests hold more probes than the corpus holds units — 1,297
against 590 — because not every generated probe became a unit. The
mapping is `go/op_<n>` → `probe_manifest_go.json` key `<n>`, and
`go/regen_<n>` → `probe_manifest2_go.json` key `<n>`; **0 of 590 units
failed to resolve.** Every probe is `package main` with no imports, so
one `importcfg` serves all 590.

## 4.2 The instrumented population

| | count |
|---|---|
| region graph nodes, all kinds (`graph_go4.json`) | 174,159 |
| of those, function bodies (`func` + `method`) | 1,549 |
| bodies an edit was placed in | **1,549** |
| bodies skipped | 0 |
| files touched | 84 (+3 subject-spot files) |
| subject spots (the per-goroutine subject stack) | 3 |

August's lap instrumented 56 spots in 5 files, chosen by three call hops
out of one seed file. This lap instruments the region.

## 4.3 The run

| | measured |
|---|---|
| toolchain build (`make.bash`) in this instance | 124 s |
| instrumented `cmd/compile` rebuild | 20 s |
| probes compiled | 590 of 590 |
| probes failed | 0 |
| wall clock for all 590 | 111 s (5.3 probes/s) |
| diary events, total | 10,015,022 |
| events per probe: min / median / max | 14,582 / 16,629 / 19,232 |
| events, original units (107) | 1,787,275 |
| events, regenerated units (483) | 8,227,747 |
| diaries on disk | 1.2 GB |

Pin, quoted from the toolchain, not typed:

```
go version go1.28-devel-pseudocoup linux/amd64
```

Tree: `/sources/golang_src`, commit `9f1012d9a1aa0831ff44ac9c767e96f9943d13fe`
(2026-07-15), `internal/goversion` `const Version = 28`.

---

# 5. The coverage join, and the finding

## 5.1 The four populations

Every number below carries the population it is over, because the same
count means different things over different ones.

| population | count | what it is |
|---|---|---|
| `population_region_nodes` | 174,159 | every node of the go region graph, all kinds |
| `population_body_nodes` | 1,549 | of those, the function bodies — the only kind an entry hook can sit in |
| `population_instrumented` | 1,549 | the bodies an edit was actually placed in |
| `population_probes` | 590 | diaries read |
| **bodies visited by at least one probe** | **731** | of 1,549 instrumented |
| **bodies visited by no probe** | **818** | of 1,549 instrumented |
| visited ids not found in the graph | 0 | the join is total: every id a diary emitted is a node of the graph |

The 172,610 non-body nodes are a NAMED FRONTIER, not a never-visited
set. They are refs, calls, parameters, locals and constants — positions
inside a body. This instrument cannot observe them, and saying no probe
visited them would be a claim the evidence does not carry.

## 5.2 One real coverage row

LITERAL, from `coverage_go.json`, `per_node_visitors`:

```
"src/cmd/compile/internal/abi/abiutils.go:12127-13356:method":
    ["op_0", "op_1", "op_10", "op_103", "op_110", "op_117", ... ]      590 probes
```

GLOSS: that node is `ABIAnalyzeFuncType`, and **all 590 probes enter
it**. It is the function the August acceptance path starts from, so the
whole corpus walking through it is the expected shape, now shown rather
than assumed.

At the other end, LITERAL:

```
"src/cmd/compile/internal/ssa/rewrite.go:21410-21486:func":  ["op_10", "regen_14"]
"src/cmd/compile/internal/ssa/branchelim.go:12059-12588:func": ["op_707", "regen_551"]
"src/cmd/compile/internal/ssa/rewrite.go:21324-21409:func":  ["op_9", "regen_13"]
```

GLOSS, and worth task 75's attention: each of these compiler-source
nodes is entered by exactly **two** probes, and in each case one comes
from the original population and one from the regenerated one. That is a
recurrence of a compiler-source path across probes, which is precisely
what `Graph.super_ops` is defined to rank — and it arrived from machine
evidence, with no token anywhere in the grouping.

And per probe, its path, LITERAL, the first five entries of
`per_probe_path["op_0"]` (first-visit order):

```
src/cmd/compile/internal/ssa/rewrite.go:22841-22896:func
src/cmd/compile/internal/ssa/addressingmodes.go:3140-3212:func
src/cmd/compile/internal/ssa/compile.go:19952-20324:func
src/cmd/compile/internal/ssagen/ssa.go:43760-43860:func
src/cmd/compile/internal/amd64/galign.go:266-603:func
```

Path lengths over the 590 probes: min 558, mean 591.8, max 643 distinct
nodes. `coverage_go.json` carries the FIRST-VISIT ORDER, not the
unabridged stream; the unabridged stream is the diary file itself, and
copying 10 million lines into the join's output would duplicate a
gigabyte and abridge nothing.

## 5.3 The re-join to task 71's graph, one command

Task 71's `graph.py` spells a node `<file>:<line>:<name>` with kind
`def`; `build_graph3.py` spells it `<file>:<start>-<end>:<kind>`. Each
diary line carries both keys, so no recompile is needed:

```sh
cd PseudoCoupHQ/Research/compiler_graph
/tmp/reconnect_venv/bin/python3 coverage.py join \
    --graph graph_go.json --graph-form task71 \
    --diaries diaries/go --out coverage_go.json
```

Target SELECTION stays on the August graph either way: an edit is placed
at a byte coordinate, and task 71's graph records only lines.

## 5.4 The finding — the compiler logic our probes never exercise

**818 bodies of 1,549, across 58 of the 84 instrumented files.** By
file, the largest:

| never visited | of total in file | file |
|---|---|---|
| 193 | 239 | `src/cmd/compile/internal/ssa/rewrite.go` |
| 84 | 199 | `src/cmd/compile/internal/ssagen/ssa.go` |
| 53 | 65 | `src/cmd/compile/internal/amd64/ssa.go` |
| 42 | 51 | `src/cmd/compile/internal/ssagen/intrinsics.go` |
| 40 | 40 | `src/cmd/compile/internal/ssa/magic.go` |
| 30 | 77 | `src/cmd/compile/internal/ssa/func.go` |
| 30 | 30 | `src/cmd/compile/internal/ssa/merge_conditional_branches.go` |
| 29 | 31 | `src/cmd/compile/internal/ssa/html.go` |
| 24 | 44 | `src/cmd/compile/internal/ssa/op.go` |
| 24 | 45 | `src/cmd/compile/internal/ssa/value.go` |

**Fourteen files are never entered at all** — every body in them, zero
probes:

```
40/40  ssa/magic.go                       the magic-number division helpers
30/30  ssa/merge_conditional_branches.go  branch merging
13/13  ssa/print.go                       SSA printing
 7/7   ssa/loopreschedchecks.go           loop preemption checks
 6/6   ssagen/nowb.go                     the no-write-barrier checker
 4/4   ssa/check.go                       the SSA self-checker
 3/3   ssa/cpufeatures.go                 CPU feature lowering
 3/3   ssa/uses.go                        use counting
 2/2   ssa/rewritetern.go                 ternary rewriting
 1/1   amd64/simdssa.go                   SIMD instruction emission
 1/1   ssa/downward_counting_loop.go      downward loop recognition
 1/1   ssagen/simdAMD64intrinsics.go      amd64 SIMD intrinsics
 1/1   ssagen/simdARM64intrinsics.go      arm64 SIMD intrinsics
 1/1   ssagen/simdWasmintrinsics.go       wasm SIMD intrinsics
```

The first 30 rows of the ordered never-visited list, `file:line  name`,
LITERAL from `coverage_go.json`:

```
src/cmd/compile/internal/abi/abiutils.go:71    SpillAreaSize       (method)
src/cmd/compile/internal/abi/abiutils.go:108   Offset              (method)
src/cmd/compile/internal/abi/abiutils.go:303   NumParamRegs        (method)
src/cmd/compile/internal/abi/abiutils.go:438   regString           (method)
src/cmd/compile/internal/abi/abiutils.go:449   ToString            (method)
src/cmd/compile/internal/abi/abiutils.go:469   String              (method)
src/cmd/compile/internal/abi/abiutils.go:657   ComputePadding      (method)
src/cmd/compile/internal/amd64/simdssa.go:12   ssaGenSIMDValue     (func)
src/cmd/compile/internal/amd64/ssa.go:58       isLowFPReg          (func)
src/cmd/compile/internal/amd64/ssa.go:199      getgFromTLS         (func)
src/cmd/compile/internal/amd64/ssa.go:1911     zeroX15             (func)
src/cmd/compile/internal/amd64/ssa.go:1916     simdV11             (func)
src/cmd/compile/internal/amd64/ssa.go:1926     simdV21             (func)
src/cmd/compile/internal/amd64/ssa.go:1941     simdVfpv            (func)
src/cmd/compile/internal/amd64/ssa.go:1954     simdV2k             (func)
src/cmd/compile/internal/amd64/ssa.go:1965     simdV2kv            (func)
src/cmd/compile/internal/amd64/ssa.go:1982     simdV2kvResultInArg0 (func)
src/cmd/compile/internal/amd64/ssa.go:2000     simdVfpkv           (func)
src/cmd/compile/internal/amd64/ssa.go:2012     simdV2kk            (func)
src/cmd/compile/internal/amd64/ssa.go:2024     simdVkv             (func)
src/cmd/compile/internal/amd64/ssa.go:2035     simdV11Imm8         (func)
src/cmd/compile/internal/amd64/ssa.go:2046     simdVkvImm8         (func)
src/cmd/compile/internal/amd64/ssa.go:2058     simdV21Imm8         (func)
src/cmd/compile/internal/amd64/ssa.go:2070     simdVgpvImm8        (func)
src/cmd/compile/internal/amd64/ssa.go:2080     simdVgpvImm         (func)
src/cmd/compile/internal/amd64/ssa.go:2091     simdV2kImm8         (func)
src/cmd/compile/internal/amd64/ssa.go:2103     simdV2kkImm8        (func)
src/cmd/compile/internal/amd64/ssa.go:2115     simdV2kvImm8        (func)
src/cmd/compile/internal/amd64/ssa.go:2128     simdV31ResultInArg0 (func)
src/cmd/compile/internal/amd64/ssa.go:2138     simdV31ResultInArg0Imm8 (func)
```

GLOSS, what the list says about the corpus rather than about the
compiler: our probes are scalar two-operand expressions on six to
sixteen holder types. So **SIMD emission is untouched** (53 of the 65
never-visited amd64 bodies are the `simdV*` emitters), **the
magic-number path is untouched** (40 of 40 — no probe divides by a
constant the compiler would turn into a multiply-and-shift), **branch
merging is untouched** (30 of 30 — no probe has the control flow for
it), and the compiler's own printers and self-checks are untouched
because they run only under flags we do not pass.

Read the other way, this is the shape of what a NEXT probe generation
would have to contain to reach the rest of the region — and that is the
first time this line has been able to say that from measurement.

## 5.4a The finding checked WITHOUT the join code

A coverage number produced by the same program that reports it proves
little, so both ends were checked by `grep` straight over the 590 diary
files — LITERAL transcript:

```
$ ID=src/cmd/compile/internal/ssa/magic.go:3892-3945:func      # umagicOK8, reported NEVER visited
$ grep -l -F "$ID" diaries/go/*.txt | wc -l
0

$ ID2=src/cmd/compile/internal/abi/abiutils.go:12127-13356:method   # ABIAnalyzeFuncType, reported visited by all
$ grep -l -F "$ID2" diaries/go/*.txt | wc -l
590
```

0 and 590 — exactly what §5.2 and §5.4 report, obtained without running
`coverage.py`.

## 5.5 The four packages, visited of instrumented

| package | visited | instrumented |
|---|---|---|
| `abi` | 29 | 36 |
| `amd64` | 15 | 69 |
| `ssagen` | 140 | 292 |
| `ssa` | 547 | 1,152 |

---

# 6. THE COST PAGE — clang, rustc, swiftc, measured on this machine

Round 15 schedules against this. Every row was measured in lanes
`t72_l5`, `t72_l6` and `t72_l7` in the `t72` instance today; nothing
here is estimated from reputation.

## 6.0 The machine and the toolchain, quoted

```
6 cores granted to the instance;  30 GB RAM;  /persist 41-43 GB free
cmake version 4.2.3
ninja 1.13.2
Ubuntu clang version 21.1.8 (6ubuntu1)
gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0
rustc 1.96.1 (31fca3adb 2026-06-26)
swiftc  NOT INSTALLED
```

## 6.1 The go lap, for comparison — what "cheap" looks like

| step | measured |
|---|---|
| source on disk | 236 MB |
| region files (non-test `.go`) | 154 |
| toolchain build (`make.bash`) | 124 s |
| **instrumented `cmd/compile` rebuild** | **20 s** |
| one probe compile | 0.19 s |
| all 590 probes | 111 s |
| disk after the lap | 316 MB tree + 286 MB cache + 36 MB binary |

The number that matters is the 20 s rebuild: go's whole compiler is one
`go build`, so widening or narrowing the instrumented set costs 20
seconds each time. That is why the region could be instrumented
wholesale rather than sampled.

## 6.2 clang — MEASURED END TO END, and the cheapest of the three

**The blocking fact, found by measuring:** `/sources/llvm-project` has a
**sparse working tree** — seven cone paths, no `clang/` and no `cmake/`
directory on disk at all. The first configure attempt therefore exited
in **0 seconds** with `CMake Error at CMakeLists.txt:77 (project):
VERSION ".." format invalid`, which reads like a version problem and is
actually an absent-directory problem. The object store is **complete**,
so a full tree needs no network.

| step | measured |
|---|---|
| source on disk (sparse working tree) | 3.9 GB, of which `.git` 3.9 GB |
| shared clone to `/persist` (`git clone --shared --no-checkout`) | **0 s** |
| `sparse-checkout disable` + `checkout llvmorg-21.1.8` | **10 s** |
| full working tree at the pin | **2.2 GB** (objects shared, 19 MB of new `.git`) |
| region files on disk after that (`clang/lib/CodeGen` + `llvm/lib/Target/X86`) | 330 |
| cmake configure (clang only, X86 only, Release, Ninja) | **11 s** |
| ninja edges for a full clang+llvm(X86) build | 4,120 |
| objects that build would compile | 3,350 |
| **one region object with all prerequisites** (`CGExpr.cpp.o`; ninja builds `llvm-tblgen` and 457 generated `.inc` headers first) | **73 s, 458 edges** |
| the same object again, prerequisites in place — the marginal cost | **9 s** |
| build tree at that point | 82 MB |

**The emission hook, proved rather than described.** A file-scope helper
plus one entry statement was written into `clang/lib/CodeGen/CGExpr.cpp`
and the object rebuilt. LITERAL, the hook as injected:

```cpp
#include <cstdio>
#include <cstdlib>
namespace {
void t72_diary_note(const char *record) {
  static FILE *out = nullptr;
  static bool tried = false;
  if (!tried) {
    tried = true;
    const char *path = std::getenv("COMPILER_DIARY");
    if (path) out = std::fopen(path, "a");
  }
  if (out) { std::fputs(record, out); std::fputc('\n', out); }
}
} // namespace
```

and one statement in a real body of the region:

```cpp
RValue CodeGenFunction::EmitAnyExpr(const Expr *E, ...) {
  t72_diary_note("clang/lib/CodeGen/CGExpr.cpp|EmitAnyExpr");
```

**Instrumented one-file build: exit 0, 10 seconds.** So the C++ shape of
the go hook compiles in-tree with no build-file change. The one design
difference from go: go's hook is a generated package that every touched
file imports; C++ has no import, so either the helper is repeated per
translation unit as above, or one `.cpp` is added to a library the
region already links. The measured 10 s is for the repeated-helper form,
which needs no build-file edit at all.

**The full build, timed.** Round 15 needs a denominator, so the whole
thing was built rather than extrapolated:

| step | measured |
|---|---|
| `ninja -j6 clang` from the configured tree | **1,316 s (21 min 56 s), exit 0** |
| ninja edges executed | 2,651 of the 4,120 in the graph (the rest belong to targets `clang` does not pull in) |
| build tree after | **784 MB** |
| `bin/clang-21` | 124.7 MB |

The pin, QUOTED from the binary that was just built, not typed:

```
clang version 21.1.8 (/sources/llvm-project 2078da43e25a4623cab2d0d60decddf709aaea28)
Target: x86_64-unknown-linux-gnu
```

(`llvmorg-21.1.8` is an annotated tag, object `42befb84...`, whose
commit is `2078da43...`; the two agree.)

So the honest schedule for a clang diary lap is: **10 s to make the
tree, 11 s to configure, 22 minutes for the first full build, and 9
seconds per touched file after that** — plus one full relink each time
the instrumented set changes. The go lap's equivalent relink is 20
seconds, so widening the instrumented region is roughly sixty times more
expensive in clang than in go, and that is the number that should shape
how clang's region is chosen: go could be instrumented wholesale, clang
probably should not be on the first pass.

## 6.3 rustc — BLOCKED on this machine, and the block is not build time

| fact | measured |
|---|---|
| the compiler that compiled the corpus, quoted | `rustc 1.96.1 (31fca3adb 2026-06-26)`, commit `31fca3adb283cc9dfd56b49cdee9a96eb9c96ffd` — **installed in the container as a binary** |
| is that commit in the source checkout? | **ABSENT** — `git cat-file -e 31fca3adb` → `Not a valid object name` |
| the checkout's own head | `7c329d6c76e11ca40c5673818ab0439c1be8962c`, 2026-08-03 |
| source on disk | 24 MB |
| sparse cone | `rustc_codegen_cranelift`, `rustc_codegen_llvm`, `rustc_codegen_ssa` — `rustc_middle/src/mir` **absent from the working tree** (objects present) |
| region files reachable on disk | 111 |
| `x.py --help` | exit 1 in 0 s — `ModuleNotFoundError: No module named 'bootstrap'` (`src/bootstrap` is not in the cone) |
| making a full tree by shared clone | **exit 128** — LITERAL: `remote: warning: lazy fetching disabled; some objects may not be available` / `remote: fatal: could not fetch 1d270e78949f81b262f05bec8af211e727848b98 from promisor remote` |

GLOSS: `/sources/rust` is a **partial (promisor) clone**. Its objects are
fetched lazily from the network, and this instance is configured
`proxy = no` — no route out at all. So the tree cannot even be
materialized here, let alone built, and no build time is the honest
figure to report. Two separate things are needed before rustc can be
diaried, and both are decisions rather than compute:

1. a complete rust checkout (network, and roughly 1-2 GB of source plus
   the `src/llvm-project` submodule, which is a second LLVM tree);
2. a decision about the PIN. Task 71's `graph.py` already records this
   frontier: the corpus was compiled by 1.96.1 / `31fca3adb`, and that
   commit is not on this machine. A diary joined to a graph built from
   a *nearby* rustc source is bounded by that gap, and the gap has to be
   either closed (fetch the exact commit) or stated on every claim.

## 6.4 swiftc — CANNOT BE STARTED HERE, and that is the measurement

| fact | measured |
|---|---|
| `swiftc` in the container | **NOT INSTALLED** |
| source on disk | 291 MB, tag `swift-6.0.3-RELEASE` (`6a862d2eb7128ff1f317b07e8ad1a6da939775f3`) |
| region files (`lib/SILGen` + `lib/IRGen`) | 230 |
| `cmark` beside the swift tree | **ABSENT** |
| `swift-syntax` | **ABSENT** |
| `swift-corelibs-libdispatch` | **ABSENT** |
| `llvm-project` | present, but **upstream**, not Apple's swift fork — `git branch -a` shows only `main` and `release/1.0.x`, `release/1.1.x` |
| direct cmake configure attempt | exit 1 in 1 s — LITERAL: `Could not find a package configuration file provided by "cmark-gfm"` |

GLOSS: a swift compiler build wants five repositories checked out
side by side at matching tags, one of which is Apple's LLVM fork rather
than upstream. Three of them are not on this disk and the instance has
no route out, so the configure step cannot be reached — not slowly,
at all. The cost of swiftc is therefore a FETCH decision first
(roughly 10-15 GB of additional source across the swift ecosystem) and
a build second; nothing about build time can honestly be reported until
the fetch is ruled.

## 6.5 The page in one table — what round 15 is scheduling

| | go (done) | clang | rustc | swiftc |
|---|---|---|---|---|
| source usable on this disk today | yes | **yes, after a 10 s local checkout** | **no** (promisor clone, no network) | **no** (3 repos absent) |
| configure / prepare | 124 s | 11 s | — | — |
| one region object, cold | — | 73 s | — | — |
| one region object, warm | — | 9 s | — | — |
| **instrumented one-file build proved** | yes (20 s, whole compiler) | **yes (10 s)** | no | no |
| full compiler build | 124 s | **1,316 s** | — | — |
| disk for the source tree | 236 MB | 2.2 GB | needs fetch | needs fetch |
| disk for the build tree | 286 MB cache | 784 MB | — | — |
| what blocks a diary lap | nothing | nothing | a complete checkout AND a pin ruling | a multi-repo fetch |

The scheduling consequence, stated plainly: **clang is ready to be
diaried and is the only other compiler that is.** rustc and swiftc are
blocked on fetch and pin decisions, not on compute, so putting them in
round 15 as build tasks would schedule work that cannot start.

---

# 7. The spelling ban — the mechanical guard, transcript

The guard is `Research/op_pipeline/check_no_spelling_keys.py`,
**unmodified** — last commit `fdff0b2`, 2026-08-26, and
`git status --porcelain` on it prints nothing. One process, four
artifacts:

```
$ /tmp/reconnect_venv/bin/python3 Research/op_pipeline/check_no_spelling_keys.py \
    Research/compiler_graph/coverage_go.json \
    Research/compiler_graph/t72/diary_targets_all.json \
    Research/compiler_graph/t72/inject_report.json \
    Research/compiler_graph/t72/probes_go.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS coverage_go.json -- no operator token in any key, grouping, pairing or row structure
PASS diary_targets_all.json -- no operator token in any key, grouping, pairing or row structure
PASS inject_report.json -- no operator token in any key, grouping, pairing or row structure
PASS probes_go.json -- no operator token in any key, grouping, pairing or row structure
GUARD EXIT=0

$ grep -c exempt <that transcript>
0
```

Nothing in this lap groups or pairs by a token. Probes are keyed by unit
id (`op_0`, `regen_400`); graph nodes by source coordinate; the join is
node id against node id. The one place a token could appear —
`probes_go.json`'s `source` field, which is the probe's own go text — is
a per-unit body, and the manifest's own `operator` field was
deliberately **not carried** into that file.

---

# 8. Resume state

Everything is resumable and nothing needs a rerun to be re-derived.

## 8.1 The state files

| file | what it holds |
|---|---|
| `Research/compiler_graph/t72/diary_state.json` | `done` (590 unit ids), `failed` (empty), `events` (per-unit event count). The lane skips a unit whose diary exists and is non-empty, so re-submitting continues where it stopped |
| `Research/compiler_graph/t72/inject_report.json` | 1,549 targets read / 1,549 instrumented / 0 skipped, with every instrumented id |
| `Research/compiler_graph/t72/diary_targets_all.json` | the 1,549 selected targets with their byte coordinates |
| `Research/compiler_graph/t72/probes_go.json` | the 590 probe sources with their manifest provenance |
| `/persist/probecfg/{toolline.parts,importcfg}` (in `t72-persist`) | the exact compile command line and importcfg the replay uses |

## 8.2 To redo the lap from nothing

```sh
bash Airlock/up.sh --instance t72
cd Airlock
./airlock --instance t72 submit <repo>/Research/compiler_graph/lanes_t72/t72_l1_build.sh       --no-batch
./airlock --instance t72 submit <repo>/Research/compiler_graph/lanes_t72/t72_l2_inject_build.sh --no-batch
./airlock --instance t72 submit <repo>/Research/compiler_graph/lanes_t72/t72_l4b_diaries.sh     --batch t72 --weight 60
cd <repo>/Research/compiler_graph
/tmp/reconnect_venv/bin/python3 coverage.py targets --graph graph_go4.json --out t72/diary_targets_all.json
/tmp/reconnect_venv/bin/python3 coverage.py join --graph graph_go4.json --graph-form august \
    --diaries diaries/go --instrumented t72/diary_targets_all.json --out coverage_go.json
```

Airlock refuses a lane name that has already run, so a re-run needs a
new lane name — that is why the diary lane on disk is `t72_l4b`.

## 8.3 The one command owed to task 71

Given in §5.3. It re-keys the join to `graph_go.json` with no recompile
and no new diaries.

## 8.4 The instance

`t72` was brought DOWN at the end of this task. Its settings live in
`Airlock/instances/t72.conf` — gitignored per-machine
caller config, Airlock's own source untouched. It takes its OWN
`t72-persist` volume read-write rather than `trickle`'s read-only view
of `sandbox-persist`, because this lap had to re-inject and rebuild the
compiler (a write) while task 71 was running in parallel. `/persist/gosrc`
on `sandbox-persist` was checked and is intact — path check in §9.1 —
and was not touched.

---

# 9. Evidence

## 9.1 The path check, from inside a lane

LITERAL, lane `t72_l0_pathcheck.sh` (run in the default instance, which
mounts `sandbox-persist`):

(The user name in the one host path below is replaced by `<user>`; that
is the ONLY edit to this literal, made because no machine path belongs
in a tracked artifact. The lane now uses a glob so the question does not
arise again.)

```
hostname: <container-id>
-- a host-only path must NOT exist in here:
ls: cannot access '/home/<user>/Programming': No such file or directory
  ABSENT (as expected inside the container)
-- container-only paths that must exist:
  /persist                     present
  /sources                     present
  PseudoCoupHQ       present
=== /persist/gosrc ===
/persist/gosrc
PRESENT
-- go binary version, QUOTED from the toolchain:
go version go1.28-devel-pseudocoup linux/amd64
-- instrumented binaries left by the August lap:
-rwxr-xr-x 1 root root 36597564 Aug 24 23:06 /persist/compile_diary
-rwxr-xr-x 1 root root 36602645 Aug 24 23:19 /persist/compile_diary2
-- du:
316M	/persist/gosrc
860M	/persist/gocache
```

## 9.2 Complete file inventory

**New files, this task:**

| path | what |
|---|---|
| `Research/compiler_graph/coverage.py` | `class Graph(graph.Graph)`: `diary_targets`, `diary`, `coverage`; folds into `graph.py` |
| `Research/compiler_graph/coverage_go.json` | the join. 27.6 MB, tracked — it is the finding |
| `Research/compiler_graph/t72/inject_diary_region.py` | the widened injector, bytes-correct, stdlib only |
| `Research/compiler_graph/t72/diary_targets_all.json` | 1,549 targets |
| `Research/compiler_graph/t72/inject_report.json` | 1,549 / 1,549 / 0 skipped |
| `Research/compiler_graph/t72/probes_go.json` | the 590 probe sources with provenance |
| `Research/compiler_graph/t72/diary_state.json` | the resume state |
| `Research/compiler_graph/t72/smoke.diary` | the single-probe smoke record |
| `Research/compiler_graph/t72/toolline_raw.txt` | the captured tool command line |
| `Research/compiler_graph/diaries/go/*.txt` | 590 diaries, 1.2 GB, **gitignored** (regenerable output; the rule was added with its regeneration command, following the file's own precedent for `graph_go*.json`) |
| `Research/compiler_graph/lanes_t72/t72_l0_pathcheck.sh` | the path check |
| `Research/compiler_graph/lanes_t72/t72_l1_build.sh` | the toolchain build |
| `Research/compiler_graph/lanes_t72/t72_l2_inject_build.sh` | inject + rebuild + capture the tool line |
| `Research/compiler_graph/lanes_t72/t72_l3_smoke.sh` | one-probe smoke |
| `Research/compiler_graph/lanes_t72/t72_l4_diaries.sh` | the 590 compiles (first attempt; kept as the record) |
| `Research/compiler_graph/lanes_t72/t72_l4b_diaries.sh` | the 590 compiles, the run of record |
| `Research/compiler_graph/lanes_t72/t72_l5_costpage.sh` | cost page, first pass |
| `Research/compiler_graph/lanes_t72/t72_l6_costpage2.sh` | cost page, second pass |
| `Research/compiler_graph/lanes_t72/t72_l7_clang_hook.sh` | clang emission hook + full build timing |
| `Airlock/instances/t72.conf` | the instance's settings; gitignored caller config, Airlock source untouched |

**Files edited, this task:**

| path | change |
|---|---|
| `PseudoCoupHQ/.gitignore` | one rule for `Research/compiler_graph/diaries/`, with the reason and the regeneration command |
| `Planning/.../node_0_3_5_9_graph/CORE_0_3_5_9_graph.md` | realization table rows for `diary (go)` and `coverage over the corpus`; one new settled rule (an uninstrumented node is a frontier, never a never-visited node) |
| `Planning/.../node_0_3_5_9_graph/PROGRESS.md` | four entries, at the moment of progress |

**PROGRESS files touched:** exactly one —
`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/PROGRESS.md`.

**Files deliberately NOT touched:** `Research/compiler_graph/graph.py`
(task 71's, running in parallel), `Research/compiler_graph/inject_diary.py`
and every August artifact beside it, `Research/op_pipeline/check_no_spelling_keys.py`,
and anything under `Airlock` except the gitignored
`instances/t72.conf`.

## 9.3 Lane record

All lanes ran in the `t72` instance except `t72_l0_pathcheck.sh`, which
ran in the default instance because that is where `sandbox-persist` is
mounted. Logs: `<runs>/t72/agent/logs/`, and
`Airlock/agent/logs/` for lane 0.

| lane | exit | wall clock |
|---|---|---|
| `t72_l0_pathcheck.sh` | 0 | 0.3 s |
| `t72_l1_build.sh` | 0 | 124 s |
| `t72_l2_inject_build.sh` | 4 (the `$WORK` literal, fixed in l3) | 21.9 s |
| `t72_l3_smoke.sh` | 0 | 0.4 s |
| `t72_l4_diaries.sh` | 1 (cross-device rename, fixed) | 0.3 s |
| `t72_l4b_diaries.sh` | 0 | 110.9 s |
| `t72_l5_costpage.sh` | 0 | 2.1 s |
| `t72_l6_costpage2.sh` | 0 | 104.6 s |
| `t72_l7_clang_hook.sh` | 0 | 1326.6 s |

---

# 10. What is owed after this

1. **Task 75 can run.** `Graph.super_ops` needs diaries and now has 590
   of them, 10 million events, with recurrence across probes already
   visible (§5.2's two-probe nodes).
2. **Task 73's coverage pane** has `coverage_go.json` for go, and for
   clang/rustc/swiftc must show the static structure and say the dynamic
   structure is not measured.
3. **The re-join** to task 71's `graph_go.json` (§5.3) — one command.
4. **Round 15's schedule** should take clang and leave rustc and swiftc
   as fetch-and-pin decisions (§6.5).
5. **`coverage.py` folds into `graph.py`** once task 71's file settles.
