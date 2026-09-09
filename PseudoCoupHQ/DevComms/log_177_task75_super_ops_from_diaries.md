# log 177 — task 75: super-ops mined from the diaries, and what the substitution cost

Date: 2026-09-03. Node: `hq.research.compiler_graph.graph`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/CORE_0_3_5_9_graph.md`),
sub-node `super_ops`. Round 14 as reordered by log_173.

---

# 1. What was done, in plain words

## 1.1 The one-line account

The 590 go diaries were mined for **paths through the compiler's own
source that recur across probes** — 9,809 of them — each carrying the
compiler source it consists of, the probes it recurs in, and the
arch-units those probes produced; and the superseded output-side miner
was joined against them both ways, which shows that on go it produced
**59 records over 17 of the 590 units, with no compiler function
attached to any of them.**

## 1.2 The walk, without figures

- log_175 §5.3's re-join command was run first, verbatim. It returned
  zeros. The cause is an id-scheme mismatch, named in §2, not a
  coverage collapse; the honest join is on the declaration coordinate,
  and after it **no node changed status.**
- `coverage.py`'s additions were folded into `graph.py`, which is what
  the CORE names and where the code belongs. `coverage.py` keeps its
  text and gains a header saying it is a superseded record.
- `Graph.super_ops` was written, run, **abandoned mid-round after it
  took the machine's memory**, redesigned to a streaming bounded shape,
  proved on a 20-diary sample, and run over all 590.
- The top candidates were printed with the compiler's own code at each
  span, quoted from the pinned tree with `git show`.
- The output-side miner was joined against them, both directions, with
  two tests rather than one, because one of them would have flattered
  the result.

## 1.3 What is NOT claimed

- Nothing about cpp, rust or swift. Only go has diaries.
- A candidate is a RECURRING PATH, which is a candidate and not a
  ruling. Nothing here says any of the 9,809 IS a super-op; that is
  the owner's.
- Recurring paths **longer than 12 compiler-source nodes exist and were
  not mined this lap.** `max_length` is 12 and the frequent-run count
  was still rising at 12. That is a stated cap, not a bottom.
- The comparison is over the output-side records' own SAMPLE unit ids.
  Those records carry samples, not full member lists, so a subset test
  is over the sample and says so in the artifact.

---

# 2. Step 0 — the re-join, and the command that returned zeros

## 2.1 log_175 §5.3, run verbatim — LITERAL transcript

```
$ /tmp/reconnect_venv/bin/python3 coverage.py join \
    --graph graph_go.json --graph-form task71 \
    --diaries diaries/go --out <scratch>/coverage_53_verbatim.json
population_region_nodes                    10393
population_body_nodes                      0
population_instrumented                    0
population_probes                          590
bodies_visited_by_at_least_one_probe       0
never_visited_count                        0
```

(The output went to a scratch path, so nothing of task 72's was
overwritten by a command that was about to be found wrong.)

GLOSS — two mismatches, either one fatal:

| | `coverage.py --graph-form task71` expects | task 71's `graph_go.json` actually has |
|---|---|---|
| node id | `<file>:<line>:<name>` | `<file>#<line>#<kind>#<ordinal>` |
| body kind | `func` / `method` (the August words) | `def` |

`population_body_nodes 0` is the second mismatch showing: no node of
that graph carries the kind the reader filters on, so the instrumented
population is empty before any diary is read. Read without checking,
`bodies_visited 0` would have looked like the corpus reaching none of
the compiler.

## 2.2 The join that is sound, and why

Task 71's `graph.py` already joins on the DECLARATION COORDINATE
`<file>:<line>` — the one coordinate both id schemes carry, and the
third pipe-field every diary line writes. The re-join command is
therefore:

```
$ /tmp/reconnect_venv/bin/python3 graph.py join \
    --graph graph_go.json --diaries diaries/go \
    --instrumented t72/diary_targets_all.json --out coverage_go2.json
population_region_nodes                          10393
population_defs                                  1859
population_instrumented                          1534
population_probes                                590
defs_visited_by_at_least_one_probe               724
instrumented_visited_by_at_least_one_probe       724
uninstrumented_defs_a_named_frontier             325
never_visited_count                              810
visited_keys_outside_the_region                  7
wrote coverage_go2.json
```

**The output is `coverage_go2.json`, not `coverage_go.json`, and that
is deliberate.** `coverage_go.json` is task 72's join against the
August graph; it is a different measurement over a different node
population and overwriting it would destroy the only record of the lap
this one is checked against.

## 2.3 Which nodes changed status: NONE

Compared body by body on the declaration coordinate, over the 1,534
instrumented bodies both graphs contain:

```
instrumented coords compared: 1534
visited in August join, not visited in re-join: 0
visited in re-join, not in August join: 0
old visited coords (instrumented): 724   new: 724
```

The two remaining differences from log_175's 731 / 818 are **named, not
absorbed**: 15 of task 72's 1,549 injection targets have no def at that
coordinate in task 71's graph, because the stated region rule excludes
generated files. LITERAL, the 15:

```
src/cmd/compile/internal/amd64/simdssa.go 12          ssaGenSIMDValue      func
src/cmd/compile/internal/ssa/opGen.go 332             String               method
src/cmd/compile/internal/ssa/opGen.go 333             AuxIntType           method
src/cmd/compile/internal/ssa/opGen.go 115435..115443  Asm, Scale, String, SymEffect,
                                                      IsCall, IsTailCall, HasSideEffects,
                                                      UnsafePoint, ResultInArg0   (methods)
src/cmd/compile/internal/ssagen/simdAMD64intrinsics.go 11  simdAMD64Intrinsics  func
src/cmd/compile/internal/ssagen/simdARM64intrinsics.go 11  simdARM64Intrinsics  func
src/cmd/compile/internal/ssagen/simdWasmintrinsics.go 12   initWasmSIMD         func
```

Of those 15, **7 were visited** (the `opGen.go` accessors, which is
exactly the `visited_keys_outside_the_region 7` line above) and **8
were never visited**. 731 − 7 = 724 and 818 − 8 = 810. The two joins
agree exactly, and the difference is the region rule, stated.

---

# 3. THE INCIDENT — the miner took the machine, and the bound that now
prevents it

Recorded here rather than quietly fixed, because a result produced this
way would have looked exactly as plausible as one produced properly.

**What happened.** The first shape of `Graph.super_ops` read all 590
diaries into `dynamic_structure` — 10,015,022 event strings — and then
held, for every run length at once, a dictionary of every run of that
length together with the list of probes it occurred in. Both parts are
O(events); the level dictionaries are O(events) PER LENGTH; and nothing
capped the length. The process reached **13.2 GB resident, exhausted
this machine's 4 GB of swap, and was spilling the whole desktop.** It
was stopped from outside (SIGTERM, then SIGKILL) after about 12
minutes. the owner saw it happen. Nothing about the intended measurement was
wrong; the shape was.

**The bound now, and it is a settled rule of the CORE, not a habit:**

1. Diaries are read **one file at a time** and encoded to a compact
   array of 4-byte integers in a cache file on disk. Live cost of this
   phase is one diary plus the coordinate alphabet (626 strings).
2. The Apriori passes read that cache one probe at a time. **At most
   two length levels are live**, and each holds integer counts, not
   probe lists; the probes of a candidate are collected in one final
   pass, for the surviving candidates only.
3. `max_length` caps the number of passes, `max_runs_per_level` caps
   the width of one pass, and `memory_ceiling_mb` is checked with
   `resource.getrusage` after every pass and every 25 probes. The
   miner **aborts by name** (`MemoryCeilingReached`) rather than
   letting the operating system stop it. A stop by the operating
   system is not a measurement; a refusal by name is.

**Proved on a sample before the full run, as instructed.** 20 diaries:

```
"wall_seconds": 0.7, "peak_resident_mb": 170.8
Maximum resident set size (kbytes): 224388
Elapsed (wall clock) time: 0:01.12
```

**The full 590, run under `ulimit -v 7000000` as well as the stated
ceiling** — LITERAL, `/usr/bin/time -v`:

```
Elapsed (wall clock) time (h:mm:ss or m:ss): 0:21.06
Maximum resident set size (kbytes): 498968
Swaps: 0
Exit status: 0
```

**21 seconds and 487 MB, against 12 minutes and 13.2 GB.** Same
diaries, same measurement.

---

# 4. The instrument, with values moving through it

## 4.1 One stream

A diary interleaves several compiler entry points, because the compiler
runs concurrently (log_175 §2.3 shows two chains alternating event by
event). Order alone would read them as one chain, and a sub-path mined
out of that mixture would be an artefact of the scheduler. So the
miner's `subject` parameter selects a stream:

| setting | what it keeps |
|---|---|
| `probe_own` | events whose subject is neither `-` nor `main` — the compilation of the probe's own expression. **Used.** |
| `main` | the events of the probe file's own `main` |
| `all` | every event, subject ignored — kept only so the mixture can be measured, never as a default |

`collapse_repeats` folds a run of the same coordinate entered back to
back into one occurrence, so recurrence measures the SHAPE of a path
and not how many times a loop turned.

Counted with `awk` straight over the diaries, not by the miner:

```
$ awk -F'\t' '$2!="-" && $2!="main"{n++} END{print n}' diaries/go/*.txt
2263885
$ awk -F'\t' 'END{print NR}' diaries/go/*.txt
10015022
```

2,263,885 probe-own events of 10,015,022; after collapse, **1,998,333
stream events over 626 distinct compiler-source coordinates.**

## 4.2 THE PARAMETERS, stated on the artifact, with why

LITERAL, the `parameters` object of `super_ops_go.json`:

```json
{
 "min_length": 3, "min_support": 2, "subject": "probe_own",
 "collapse_repeats": true, "max_length": 12,
 "max_runs_per_level": 2000000, "memory_ceiling_mb": 6144,
 "support_is_counted_in": "distinct probes",
 "closure": "closed contiguous runs only"
}
```

| parameter | value | why this value |
|---|---|---|
| `min_length` | 3 | two nodes is a call edge the static structure already carries; three is the shortest run that says something the static graph does not |
| `min_support` | 2 probes | "recurs across probes" has a floor of two. Support is counted in **distinct probes, never occurrences**: a path one probe walks a thousand times has recurred across one probe |
| `subject` | `probe_own` | §4.1 |
| `collapse_repeats` | true | §4.1 |
| `max_length` | 12 | a **cap, and therefore a frontier** — see §4.3 |
| `max_runs_per_level` | 2,000,000 | the width bound of one pass; the miner refuses rather than growing past it |
| `memory_ceiling_mb` | 6,144 | §3 |

Closure: a run is dropped when a one-step extension of it has exactly
the same probe support, because the shorter run then carries no
evidence the longer one does not. That test is exact for contiguous
runs.

## 4.3 The cap is a frontier, and it is still rising

LITERAL, `frequent_runs_by_length` from the artifact:

| length | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| frequent runs | 2,495 | 3,360 | 4,211 | 4,998 | 5,748 | 6,485 | 7,221 | 7,934 | 8,645 | 9,358 |

The count rises monotonically to the cap. **Recurring compiler-source
paths longer than 12 nodes exist and were not mined this lap.** Raising
the cap is one parameter and 21 seconds; it was not raised without a
ruling on what a longer path would mean.

## 4.4 The populations

| population | count |
|---|---|
| probes (diaries) | 590 |
| distinct compiler-source coordinates in the streams | 626 |
| stream length per probe, min / max | 1,945 / 5,182 |
| stream events, total | 1,998,333 |
| **closed candidates** | **9,809** |
| of those, walked by all 590 probes | 669 |
| of those, walked by 30 probes or fewer | 4,330 |

---

# 5. The top 20 by recurrence, with the compiler's own code

Full print with every span's excerpt: `super_ops_go_top20.txt` (2,121
lines). Every excerpt below is taken from the PINNED tree, not the
working tree:

```
$ git -C ~/Programming/Sources/golang_src log -1 --format=%H
9f1012d9a1aa0831ff44ac9c767e96f9943d13fe
```

## 5.1 The table

Ranked by probe support, then length. Labels are the compiler's own
function names, carried once per node for reading — the candidates are
keyed by source node ids, never by a name.

| candidate | len | support | the path, by the compiler's own function names |
|---|---|---|---|
| cand_00000 | 12 | 590/590 | truncateValues → retSparseSet → clear → cap → Log ×4 → nilcheckelim → Sdom → NumValues → num |
| cand_00001 | 12 | 590/590 | regMaskAt → clobber → minus → regspec → AuxInt8 → regMaskAt → advanceUses → dropIfUnused → freeRegs → intersect → empty → union |
| cand_00002 | 12 | 590/590 | retSparseMap → clear → cap → Log ×4 → flagalloc → NumBlocks → num → postorder → ControlValues |
| cand_00003 | 12 | 590/590 | NumBlocks → num → NumValues → num → NumValues → num → NumValues → num → newSparseSet → IsVarWantedForDebug → liveness → NumBlocks |
| cand_00004 | 12 | 590/590 | minus → regspec → AuxInt8 → regMaskAt → advanceUses → dropIfUnused → freeRegs → intersect → empty → union → empty → intersect |
| cand_00005 | 12 | 590/590 | cleanup → retPoset → Log ×4 → divisible → applyRewrite → clear ×3 → NumBlocks |
| cand_00006 | 12 | 590/590 | get → notStmtBoundary → entryNewValue0 → entryBlock → NewValue0 → newValue, twice over |
| cand_00007 | 12 | 590/590 | NumBlocks → num → Postorder → postorder → allocBlock → mergePredecessors → clear → reset → clear → getHome → processValue → empty |
| cand_00008 | 12 | 590/590 | Log ×2 → likelyadjust → NumBlocks → num → NumBlocks → num → postorder → loopnest → Log ×3 |
| cand_00009 | 12 | 590/590 | RegisterTypesAndOffsets → appendParamOffsets → appendParamTypes → FrameOffset → SpillAreaOffset → LocalsOffset → ObjRegForAbiReg → archRegForAbiReg → popLine → genssa → Frontend → NumBlocks |
| cand_00010 | 12 | 590/590 | get → mapFor → get → cap → cap → contains → truncateValues → deleteNamedVals → Log ×4 |
| cand_00011 | 12 | 590/590 | foreachEntry → size → size → truncateValues → retSparseSet → clear → cap → Log ×4 → cse |
| cand_00012 | 12 | 590/590 | newFactsTable → newPoset ×4 → SetUnsigned → NumValues → num → initLimit → noLimit → noLimitForBitsize → initLimit |
| cand_00013 | 12 | 590/590 | Log → likelyadjust → NumBlocks → num → NumBlocks → num → postorder → loopnest → Log ×4 |
| cand_00014 | 12 | 590/590 | Log ×3 → divmod → applyRewrite → clear ×3 → NumBlocks → num → ControlValues → phielimValue |
| cand_00015 | 12 | 590/590 | elimIfElse → retSparseSet → clear → cap → Log ×4 → opt → applyRewrite → clear ×2 |
| cand_00016 | 12 | 590/590 | tighten → NumValues → num → NumBlocks → num → NumBlocks → num → NumValues → num → newSparseSet → memState → MemoryArg |
| cand_00017 | 12 | 590/590 | empty → freeReg → hasReg → removeReg → intersect → empty → dropIfUnused → freeRegs → intersect → empty → union → setHome |
| cand_00018 | 12 | 590/590 | mapFor → contains → cap → cap → contains → isPoorStatementOp → contains → mapFor → contains → cap → cap → contains |
| cand_00019 | 12 | 590/590 | num → postorder → loopnest → Log ×4 → layout → layoutOrder → NumBlocks → num → NumBlocks |

## 5.2 One candidate read off the compiler's source, in full

cand_00009, length 12, support 590 of 590. LITERAL excerpts, each one
`git show 9f1012d9a1aa:<file>` at the node's start line:

```go
// src/cmd/compile/internal/abi/abiutils.go:137  RegisterTypesAndOffsets
func (pa *ABIParamAssignment) RegisterTypesAndOffsets() ([]*types.Type, []int64) {
	l := len(pa.Registers)
	if l == 0 {

// src/cmd/compile/internal/abi/abiutils.go:197  appendParamOffsets
func appendParamOffsets(offsets []int64, at int64, t *types.Type) ([]int64, int64) {
	w := t.Size()
	if w == 0 {

// src/cmd/compile/internal/abi/abiutils.go:148  appendParamTypes
func appendParamTypes(rts []*types.Type, t *types.Type) []*types.Type {
	w := t.Size()
	if w == 0 {

// src/cmd/compile/internal/abi/abiutils.go:249  FrameOffset
func (a *ABIParamAssignment) FrameOffset(i *ABIParamResultInfo) int64 {
	if a.offset == -1 {
		base.Fatalf("function parameter has no ABI-defined frame-pointer offset")
```

GLOSS: that is a named parameter's registers, types and frame offset
being read out one after another and then handed to the amd64 emitter
(`ObjRegForAbiReg` → `archRegForAbiReg` → `genssa`) — the lowering path
this whole line exists to prove, arriving as a recurring diary sub-path
rather than as a hand-followed walk.

and, from the top of the same print, the shape of every other excerpt:

```go
// src/cmd/compile/internal/ssa/func.go:117
func (f *Func) NumValues() int {
	return f.vid.num()
}

// src/cmd/compile/internal/ssa/id.go:26
func (a *idAlloc) num() int {
	return int(a.last + 1)
}

// src/cmd/compile/internal/ssa/sparseset.go:73
func (s *sparseSet) clear() {
	s.dense = s.dense[:0]
}
```

The arch-units the probes of cand_00000 produced, canon39 `body_text`,
LITERAL:

```
go/op_0   ret
go/op_1   ret
```

## 5.3 THE READING, and it is not the flattering one

**The top of the ranking is not a super-op. It is the compiler's own
housekeeping.** Every one of the top 20 is walked by all 590 probes,
and what they consist of is sparse-set allocation and release
(`newSparseSet`, `retSparseSet`, `clear`, `cap`), id counting
(`NumValues`, `NumBlocks`, `num`), the debug-log predicate (`Log`,
which is `return f.fe.Log()` and is called before every pass), and pass
entry points in their fixed order (`nilcheckelim`, `cse`, `dse`,
`flagalloc`, `layout`, `tighten`, `opt`). That is the pass pipeline,
which every compile of every program walks. Ranked by recurrence, this
is the correct answer and it is the honest one.

The arch-units confirm it from the other side: the probes of cand_00000
are all 590 units, whose bodies range from `ret` to full expressions —
one path, every output. **A path that everything walks cannot explain
any particular output.**

So the ranking's top says something real about the instrument rather
than about the corpus: **recurrence alone does not isolate an idiom, it
isolates the pipeline.** The band where a super-op could live is the one
where a path recurs across SOME probes and not others, and that band is
large — 4,330 candidates at support ≤ 30. LITERAL, six of them, all
walked by the same six-probe front:

```
cand_05480  30  ResultReg -> Reg -> SetPos -> ssaGenValue -> Prog -> Reg ->
                DebugFriendlySetPosFrom -> SetPos -> SetPos
cand_05481  30  isLoweredGetClosurePtr -> clear -> needRegister -> add -> size ->
                isLoweredGetClosurePtr -> clear -> needRegister -> add ->
                needRegister -> size -> makeLCArange
cand_05483  30  isHighFPReg -> isFPReg -> isKReg -> CheckArgReg ->
                DebugFriendlySetPosFrom -> SetPos -> ResultReg -> Reg
   probes: op_6, op_7, op_17, op_18, op_19, op_20, ...
```

and the arch-units those probes produced, canon39 `body_text`, LITERAL:

```
go/op_6    neg %eax; ret
go/op_17   xor $0x1,%eax; ret
```

`isHighFPReg`/`isFPReg`/`isKReg` → `CheckArgReg` is the amd64 emitter
deciding which register file an argument lives in — a compiler-source
path that separates part of the corpus from the rest. Whether such a
path is a super-op is the owner's to rule; this instrument's job was to find
them and it does. `super_ops_go_discriminating10.txt` prints the top of
that band in full, with excerpts.

Two nodes of cand_05480 and cand_05483 print as `NOT A NODE OF THE
REGION GRAPH (a named frontier)`: they are the generated `ssa/opGen.go`
accessors of §2.3, which the region rule excludes. They are shown as a
frontier, never dropped.

---

# 6. The both-ways comparison against the output-side miner

## 6.1 What the output-side miner has to say about go, before any join

`op_pipeline/super_ops3.json`, all four of its sections read together:

| population | count |
|---|---|
| candidate records in the file | 494 |
| **records naming any go unit** | **59** |
| distinct go units they name, of the corpus's 590 | **17** |
| of those, regenerated units | **0** |
| the 59 records' section | all `frontier_non_ambiguous` |
| **the 59 records carrying an emitting compiler function** | **0** |

LITERAL, one of the 59, its own frontier text:

> "no graph coverage: graph_cpp3.json (Task 11) reads only cpp/tablegen
> sources over the widened 11-file region; these languages have no
> reader in that graph: go (named frontier, reused from Task 1/6,
> unchanged by widening)"

**That is the cost of the substitution, stated by the substitute
itself.** On go the output-side instrument produced no compiler-source
claim at all — not a wrong one, none — and it saw 17 of 590 units.

## 6.2 The join, both ways, with two tests rather than one

Artifact: `super_ops_comparison_go.json`. The comparison scope comes
from the output-side record's OWN machine coordinates — the go unit ids
it names. No token enters the pairing.

```
output_side_with_a_graph_counterpart_loose               59
output_side_with_a_graph_counterpart_strict               0
output_side_without_a_graph_counterpart                   0
graph_candidates_with_an_output_side_counterpart       4479
graph_candidates_without_an_output_side_counterpart    5330
```

| test | what it asks | result |
|---|---|---|
| LOOSE | is there a graph candidate that recurs in **every** go unit this record names? | **59 of 59** |
| STRICT | is there one that recurs in those units **and in no others**? | **0 of 59** |

**Both are reported because the loose test on its own would have
flattered the result.** 669 of the 9,809 graph candidates are walked by
all 590 probes, so any of them satisfies "covers every unit you name"
for every record. The loose 59-of-59 is ubiquity, not agreement. The
strict test is the one that would show correspondence, and it is zero:
**not one diary sub-path is confined to the units any output-side
record groups together.**

What neither test can say, stated in the artifact: the output-side
records carry SAMPLE unit ids, not full member lists (one record of
support 13 lists 8), so the subset test is over the sample.

## 6.3 The other direction, named

**5,330 of the 9,809 graph candidates have no output-side counterpart
at all** — no record of `super_ops3.json` names a go unit set they
cover. That includes the whole discriminating band of §5.3: the
amd64 register-file path (cand_05483), the closure-pointer lowering
path (cand_05481), the position-setting path (cand_05480). The
output-side instrument could not have produced any of them: it read
arch-unit bodies and never opened the compiler's source.

---

# 7. The guard

Unmodified, one process, over this task's three outputs. `git status`
reports no change to it and its md5 is
`1d6aba67cbcdb021c3bdfd7f40fd2020`. LITERAL transcript
(`guard_task75.txt`):

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
    ../compiler_graph/super_ops_go.json \
    ../compiler_graph/coverage_go2.json \
    ../compiler_graph/super_ops_comparison_go.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS super_ops_go.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_go2.json -- no operator token in any key, grouping, pairing or row structure
PASS super_ops_comparison_go.json -- no operator token in any key, grouping, pairing or row structure
EXIT=0

$ grep -c exempt guard_task75.txt
0
```

Candidates are keyed by SOURCE NODE IDS (`<file>#<line>#<kind>#<ordinal>`)
and by declaration coordinates. The compiler's own function names ride
once per node on `label`, which is the one place the ban permits a
token, and several of them (`clear`, `cap`, `size`, `contains`, `num`,
`empty`, `union`, `minus`) are exactly the words the guard refused in an
id in task 71 — which is why they are on `label` and nowhere else.

---

# 8. File inventory

## 8.1 Written this task

| file | what it is |
|---|---|
| `Research/compiler_graph/super_ops_go.json` | 9,809 closed candidates, with parameters, populations and cost on the artifact. 103.6 MB |
| `Research/compiler_graph/super_ops_go_top20.txt` | the top 20 printed with each span's compiler source, `git show` from the pin, and the arch-units. 2,121 lines |
| `Research/compiler_graph/super_ops_go_discriminating10.txt` | the same print filtered to probe support ≤ 589 — the band where a super-op could live |
| `Research/compiler_graph/super_ops_comparison_go.json` | the both-ways join against the output-side miner, with both tests |
| `Research/compiler_graph/coverage_go2.json` | the re-join against task 71's `graph_go.json` (`coverage_go.json` NOT overwritten) |
| `Research/compiler_graph/report_super_ops.py` | the print-only reader: `top20`, `compare` |
| `Research/compiler_graph/guard_task75.txt` | the guard transcript |
| `DevComms/log_177_task75_super_ops_from_diaries.md` | this log |

## 8.2 Edited (the round's two live modules only)

| file | what changed |
|---|---|
| `Research/compiler_graph/graph.py` | `Graph.super_ops` implemented (streaming, bounded, closed contiguous runs) with `encode_diaries`, `check_memory`, `read_stream`; `MemoryCeilingReached`; `load_august` and `diary_targets` folded in from `coverage.py`; `diary` keeps the subject column; `coverage` gains the four populations and the instrumented list; CLI gains `join` and `super-ops` (the `graph.py <region>` form is unchanged) |
| `Research/compiler_graph/coverage.py` | **header only** — marked a superseded record, folded into `graph.py`, with the id-scheme mismatch of §2.1 named. Body unedited |

## 8.3 Plan tree

| file | what changed |
|---|---|
| `Planning/.../node_0_3_5_9_graph/PROGRESS.md` | five entries: the re-join and its zero status changes; `super_ops` with its parameters and its cap; the memory incident and the bound; the both-ways comparison; the fold-in and the guard |
| `Planning/.../node_0_3_5_9_graph/CORE_0_3_5_9_graph.md` | new settled rule **"the miner runs in bounded memory, and its parameters are stated on the artifact"** with the incident as its provenance; realization table rows for `super_ops`, `coverage` (re-joined), the comparison, the fold-in, and `super_ops` for cpp/rust/swift as planned |

## 8.3a One repo hazard found and closed

`super_ops_go.json` (104 MB) and `coverage_go2.json` (515 MB) are over
GitHub's per-file limit, and `graph_swift.json` (165 MB) and
`graph_rust.json` (62 MB) from task 71 were untracked and unignored —
the daemon would have committed a file that can never be pushed. All
four are regenerable output, not findings, so `.gitignore` now names
them WITH the command that re-derives them (about half a minute for
both of task 75's). The findings stay tracked: the two printed tables,
the comparison json, the guard transcript and this log.

## 8.4 Read only, unchanged

`op_pipeline/check_no_spelling_keys.py` (the guard, unmodified),
`op_pipeline/super_ops3.json`, `op_pipeline/super_op_candidates.json`,
`op_pipeline/canon39_wrapped_go.json`,
`op_pipeline/canon39_regen_store/op_units2_go_c000{0,1}.json`,
`diaries/go/*.txt` (590), `t72/diary_targets_all.json`,
`graph_go.json`, `coverage_go.json`, `coverage_go_summary.json`.

---

# 9. Two lists

## 9.1 Decided, recorded for audit

- The re-join output is `coverage_go2.json`, not `coverage_go.json`:
  the two are joins against different graphs over different node
  populations and neither replaces the other.
- The join key is the declaration coordinate, because it is the only
  coordinate both id schemes carry.
- `subject = probe_own`: the miner reads the probe's own compilation,
  not the scheduler's interleaving of two.
- Support is counted in distinct probes, never occurrences.
- Only closed runs are reported.
- `max_length = 12` this lap, and it is written down as a cap that the
  data was still growing against.
- Both the loose and the strict comparison test are reported, and the
  strict one is the one that would show correspondence.
- `coverage.py` is folded in and marked superseded, not deleted.

## 9.2 Awaiting the owner

- **Which band of candidates is a super-op.** The instrument ranks by
  recurrence and the top of that ranking is the compiler's pass
  pipeline, which every probe walks. The candidates that separate part
  of the corpus from the rest sit lower (4,330 at support ≤ 30). A
  ruling on what makes a recurring path a super-op — support band,
  region, or something else — is what turns 9,809 candidates into a
  finding.
- **Whether to raise `max_length` past 12.** One parameter, 21 seconds,
  and the frequent-run count was still rising at the cap.
