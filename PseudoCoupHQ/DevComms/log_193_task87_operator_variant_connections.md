# log 193 — task 87: the third connection kind, the connections that are part of each operator traced variant

Date: 2026-09-04. Instance `t87`, brought down at the end of this log.
Brief: round 16, priority 2. Precedent followed: task 81's clang lap
(log_190) and task 75's miner (log_177). Plan node:
`hq.research.compiler_graph.graph`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/CORE_0_3_5_9_graph.md`).

Every rendering in this log is labelled per the protocol's §5.1a:
**LITERAL** is the object itself quoted from a file or a lane log,
**GLOSS** is a plain-words reading sitting beside a literal, and
**ANALOGY** is something that resembles the thing and is not it. No
gloss appears without its literal.

---

# 1. What was done, in plain words

## 1.1 The one-line account

Every diaried probe of both instrumented compilers was placed in an
**operator traced variant** by machine-form evidence alone; each
visited-next transition in the diaries was attributed to the variants
that walk it; and the nodes and transitions **exclusive to one variant**
were named — the connections the union over all probes cannot tell apart
from ubiquity.

## 1.2 The five numbers that matter, each with its population

- **590 of 590** go probes placed in **294** operator traced variants;
  **1,380 of 1,380** original c and cpp probes in **512**; **3,980 of
  3,980** extended c and cpp probes in **1,361**.
- **`probes_without_a_machine_form` is 0** on every one of the five
  measured populations.
- **48 of 2,044** visited-next transitions in the c-and-cpp population
  are walked by **exactly one** of the 512 variants; **674** are walked
  by every variant. The union holds no transitions at all.
- **133 of the 512** c-and-cpp variants carry **more than one distinct
  display label** among their members, and **all 36** distinct labels
  appear in more than one variant — the spelling ban proved on the
  output, in both directions.
- Peak resident **172.4 MB** (go) and **1,051.9 MB** (c and cpp) against
  a **6,144 MB** ceiling that refuses by name; the 416 MB coverage join
  was read one line at a time at **12.7 MB**.

## 1.3 What is NOT claimed

- **Not** that most variants own a connection. Only **6 of 512**
  c-and-cpp variants and **15 of 1,361** extended ones own an exclusive
  transition at all. §7.3 says why and does not dress it up.
- **Not** that an exclusive transition is a proof of causation. It is a
  measurement: two compiler bodies entered one after the other in this
  variant's diaries and in no other variant's.
- **Not** that rust or swift moved. Both are written down as
  `UNMEASURED_BY_ABSENCE_OF_DIARIES` and are not approximated.
- **Not** that the graph is finished. §9 lists the remainder.

---

# 2. The third connection kind, defined

## 2.1 What the owner asked for, quoted

**LITERAL**, the owner, 2026-09-04, quoted in this node's CORE and in the
dashboard node's:

> connections that are structural, dynamic, and are part of each
> operator traced variant

and

> once its completed, then we can see it through time. until it exists,
> theres nothing to fucking see.

## 2.2 What the graph held before today, and what it did not

| kind | what holds it | what it is |
|---|---|---|
| structural | `graph_go.json` 10,393 / 63,797; `graph_cpp.json` 112,364 / 386,065; `graph_rust.json` 13,446 / 60,382; `graph_swift.json` 71,106 / 192,655 | tree-sitter CST nodes and the contains / calls / reads / writes edges between them |
| dynamic | `diaries/go` 590, `diaries/c` 610, `diaries/cpp` 770, `diaries/regen` 2,600 | per probe, the ordered list of compiler bodies its compilation entered |
| **per operator traced variant** | **nothing, until today** | per variant, the connections that variant's own traces contribute |

**GLOSS.** `Graph.coverage` is the union: per node, which probes entered
it. It has no notion of a variant, it holds **no edges at all**, and it
cannot tell a body that one variant reaches from a body every variant
reaches. That is the gap the third kind fills.

## 2.3 The definition as the code states it

**LITERAL**, `Research/compiler_graph/graph.py`,
`VARIANT_CONNECTIONS_ARE`, printed by lane 6 §[2/5] from the module
itself:

```
the THIRD connection kind of this graph: per OPERATOR TRACED VARIANT,
the compiler-source nodes that variant's own traces enter and the
visited-next edges between them, each marked shared or exclusive to
that variant. It is not the union over probes -- the union
(Graph.coverage) holds no edges and has no notion of a variant, so it
cannot tell a connection one variant walks apart from one every variant
walks
```

## 2.4 What a variant IS, and the one thing it may never be

**LITERAL**, `graph.py`, `VARIANT_IDENTITY_STATED`, printed by lane 6
§[2/5]:

```
a digest over four MACHINE-FORM facts read off the unit's own ship
code, in this order: the emitted body bytes, the same body as read, the
entry contract, and the ledger's block / size / type / produced-by
shape. NO OPERATOR TOKEN ENTERS IT. The token is written onto each
member afterwards as a display label on a typed unit object and is read
back by nothing
```

**LITERAL**, the four fields `machine_form()` reads, printed by lane 6
from the function's own source with `inspect.getsource`:

```
     for row in (unit.get("ledger") or []):
     produced_by = row.get("produced_by") or {}
     ledger_shape.append([row.get("block"), row.get("size"),
     row.get("type"), produced_by.get("kind")])
     "bytes": unit.get("body_bytes"),
     "text": unit.get("body_text"),
     "entry_contract": unit.get("entry_contract"),
```

**GLOSS.** `unit.get("operator")` does not appear, because it is never
read for a grouping. The variant id is a sha256 digest of those four
facts, truncated to 16 hex characters — a digest and not the form
itself, because the id is used as a dict key and the ban is absolute
about what may sit in a key.

---

# 3. What was built

## 3.1 The chain of files

| file | what it is |
|---|---|
| `Research/compiler_graph/graph.py` | EDITED this lap: `variant_structure` added as an attribute of `class Graph`; `variant_connections` and `_variant_sets` added as methods beside `build` / `query_path` / `diary` / `coverage` / `super_ops`; the module-level helpers `machine_form`, `machine_form_identity`, `probe_unit_id`, `expand_unit_sources` and the two stated strings above; the `variant-connections` sub-command and `command_variant_connections` |
| `Research/compiler_graph/lanes_t87/t87_l1_survey.sh` … `t87_l11_report_literals.sh` | the eleven lanes |
| `Research/compiler_graph/t81/run_with_peak.py` | task 81's file, UNCHANGED, used to print each pass's peak resident set |
| `Research/op_pipeline/check_no_spelling_keys.py` | the guard, UNMODIFIED (md5 `1d6aba67cbcdb021c3bdfd7f40fd2020`; git reports no change) |

## 3.2 The tree before the code, per the standing rule

The shape went into the CORE first with its provenance, then into
PROGRESS, then into code. `CORE_0_3_5_9_graph.md` now carries
`variant_structure` and `variant_connections` in its frontmatter
`sub_nodes`, in its rendered sub-node list, in its `## design` block and
in its call flow, plus two settled rules — **a variant's identity is
machine form, never a token**, and **the third kind speaks only about
probes that have a machine form on disk**, every other diary being the
named frontier `probe_without_a_machine_form`.

## 3.3 One defect the building found, and its correction

Lane 4 scanned `Research/op_pipeline` for the id shape `go/op_` and read
go's arch-unit population as **107 of 590**, which would have made go's
third kind a thin slice of its diaries. It is wrong, and this node's own
PROGRESS entry for task 72 says why: the 590 go diaries are 107
ORIGINAL units plus **483 REGENERATED** ones, whose ids are
`go/regen_<n>` and whose records live in
`canon39_regen_store/op_units2_go_c000{0,1}.json`.

**LITERAL**, lane 5 §[2/3]:

```
   go unit ids with a record anywhere: 590
   diary stems joining by go/<stem> : 590 of 590
   first five that do not join       : []
   of the joins, carrying body_bytes : 590
```

**GLOSS.** Both lanes are kept on disk. Lane 4 is the record of a search
that read a population short; lane 5 is the correction, and the CORE
carries the corrected number rather than the first one.

---

# 4. The memory bound, stated and then held

## 4.1 The bound, stated before any full pass

**LITERAL**, the block above `Graph.variant_connections` in `graph.py`:

```
    #   * the graph in memory is the FIXED cost and it is measured, not
    #     guessed: 163.6 MB for graph_go.json, 1,043.1 MB for
    #     graph_cpp.json (lane t87_l1);
    #   * unit records are read ONE FILE AT A TIME and only a digest and
    #     a small member record survive each file, so the corpus's
    #     bodies are never all live;
    #   * diaries are streamed by `encode_diaries`, one file at a time,
    #     into an int32 file on disk -- the same streamer the miner uses;
    #   * the live tables are then O(distinct coordinates) and
    #     O(distinct transitions), plus ONE variant's own two sets;
    #     nothing enumerates sub-paths, which is the shape that reached
    #     13.2 GB on 2026-09-03;
    #   * `max_transitions` caps the transition table and
    #     `memory_ceiling_mb` is checked with `check_memory` at every
    #     phase and every 25 probes. Both refuse BY NAME
    #     (`MemoryCeilingReached`). A stop by the operating system is not
    #     a measurement.
```

## 4.2 The sample first, then the fit, then the full pass

**LITERAL**, lane 6 §[3/5], the 50-diary go sample:

```
PEAK RESIDENT 172.7 MB   wall 0.6 s   exit 0
```

**LITERAL**, lane 7 §[2/5], the two-point fit before the c-and-cpp
passes were allowed to run:

```
   peak at 100 probes     : 1051.9 MB
   peak at 400 probes     : 1052.0 MB
   fitted fixed cost      : 1051.9 MB (the graph in memory)
   fitted per-probe cost  : 0.0003 MB
   PROJECTION for 1,380   : 1052 MB
   PROJECTION for 3,980   : 1053 MB
   probes the 6,144 MB ceiling allows at this rate : 15276400
   MEMORY GATE: under the ceiling; the full passes may run.
```

**GLOSS, and it is the correction task 81 §3.4 asked for.** One
measurement cannot separate a fixed cost from a per-probe cost, and
multiplying a fixed cost by the probe count is what made task 81's lane
10 refuse a pass that fitted comfortably. Two points are taken and the
two terms fitted. Here the fixed term is the graph itself and the
per-probe term is 0.3 KB, because the live tables are sized by the
compiler's own alphabet, not by the corpus.

## 4.3 Every full pass, with its peak

**LITERAL**, lane 10 §[1/5]:

```
wrote variant_connections_go.json
PEAK RESIDENT 172.4 MB   wall 3.7 s   exit 0
wrote variant_connections_c.json
PEAK RESIDENT 1052.0 MB   wall 2.0 s   exit 0
wrote variant_connections_cpp.json
PEAK RESIDENT 1051.9 MB   wall 3.2 s   exit 0
wrote variant_connections_c_and_cpp.json
PEAK RESIDENT 1051.9 MB   wall 4.3 s   exit 0
wrote variant_connections_extended.json
PEAK RESIDENT 1051.8 MB   wall 12.0 s   exit 0
```

**LITERAL**, lane 11 §[4/6], the 416,754,589-byte coverage join read for
the comparison in §6:

```
   coverage_c_and_cpp.json: 1188788 lines, PEAK RESIDENT 12.7 MB, wall 0.2 s
```

**GLOSS.** The stated ceiling was never approached and nothing aborted,
so `MemoryCeilingReached` did not fire this lap. It is wired into the
path that ran — `check_memory` is called after every unit-source file,
after the grouping, every 25 variants during attribution, after the
static index and every 25 variants while the rows are built — which is
the gap task 81 flagged in `Graph.coverage`. **That flag is not touched
here:** whether `coverage` gets the same call is a shape question this
CORE has open, and task 87 did not answer it.

---

# 5. The lap, measured

## 5.1 The five measured populations

**LITERAL**, lane 11 §[1/6], read out of the artifacts themselves:

| population | probes | variants | nodes entered | transitions | transitions walked by exactly one variant | transitions walked by every variant |
|---|---|---|---|---|---|---|
| go | 590 | 294 | 626 | 1598 | 14 | 677 |
| c | 610 | 331 | 1134 | 1945 | 44 | 681 |
| cpp | 770 | 353 | 1172 | 2024 | 50 | 678 |
| c and cpp | 1380 | 512 | 1175 | 2044 | 48 | 674 |
| c and cpp + regen | 3980 | 1361 | 1319 | 2474 | 66 | 661 |

```
   probes_without_a_machine_form on every one of the five: 0
```

**GLOSS.** Every diaried probe of both compilers is in a variant. The
named frontier `probe_without_a_machine_form` exists in the code and its
population is measured at zero, which is a different statement from not
having looked.

## 5.2 The census, and how to read it

**LITERAL**, lane 11 §[6/6], `variant_connections_c_and_cpp.json`:

```
   the first four bands PARTITION the population; `walked_by_every_variant` is the tail of the last band named separately and OVERLAPS it. Do not add the five numbers
      nodes: {"walked_by_exactly_one_variant": 18, "walked_by_2_to_10_variants": 85, "walked_by_11_to_100_variants": 310, "walked_by_more_than_100_variants": 762, "walked_by_every_variant": 576}
      transitions: {"walked_by_exactly_one_variant": 48, "walked_by_2_to_10_variants": 266, "walked_by_11_to_100_variants": 712, "walked_by_more_than_100_variants": 1018, "walked_by_every_variant": 674}
      static_backing: {"static_call_edges_between_defs": 22343, "transitions_backed_by_a_static_call_edge": 364, "transitions_with_no_static_call_edge": 1680}
```

**GLOSS.** Of the 1,175 compiler bodies these 1,380 probes actually
enter, **576 are entered by every one of the 512 variants** — clang's
common spine — and **18 by exactly one**. Of the 2,044 visited-next
transitions, **674 belong to every variant and 48 to one**. 364 of the
2,044 have a resolved `calls` edge behind them in the static structure;
the other 1,680 do not, which is either the region rule's own edge (the
caller sits outside `clang/lib/CodeGen` and `llvm/lib/Target/X86`) or an
unresolved call already sitting in this graph's frontier. That number is
a frontier reading, not a defect claim.

---

# 6. THE POINT: what the third kind shows that the union does not

## 6.1 One variant, with its values moving

The variant below was chosen by a NUMBER — its exclusive transition
count, the highest in the population — and by nothing else.

**LITERAL**, lane 11 §[3/6], read out of
`variant_connections_c_and_cpp.json`:

```
   variant_id : var_ac7b8914b059a2c0
   members 4   probes with a diary 4   languages ['c', 'cpp']   populations ['original']
   THE MACHINE FORM IT IS IDENTIFIED BY, and nothing else:
      bytes          0f 57 05 00 00 00 00 c3
      text           xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret
      entry_contract {"a": null, "b": null, ... "result": "xmm0"}
      ledger_shape   [["TEMP", 16, "16-byte vector value", "arch_opcode"], ["OUT", 8, "8-byte vector-held value", "arch_opcode"]]
   THE MEMBERS, typed unit objects, each carrying its display label:
      c/op_15        language c    label "-"    population original    outcome WRAPPED_TEXT_PROVED
      c/op_16        language c    label "-"    population original    outcome WRAPPED_TEXT_PROVED
      cpp/op_15      language cpp  label "-"    population original    outcome WRAPPED_TEXT_PROVED
      cpp/op_16      language cpp  label "-"    population original    outcome WRAPPED_TEXT_PROVED
   ITS OWN CONNECTIONS: nodes 737 (exclusive 13), transitions 925 (exclusive 30, static-backed 155)
```

**GLOSS, step by step.**

- The grouping ran first, on four machine-form facts. `0f 57 05 …` is
  `xorps` against a relocated constant: a floating-point sign flip, and
  `xmm0` is where the answer goes. Four units emit exactly that.
- Only afterwards is the display label written onto each member. All
  four happen to read `-`, and two are c while two are cpp — **one
  traced variant spanning two source languages of one compiler**, which
  a grouping keyed on a language or a token could not produce.
- 737 compiler bodies are entered by these four probes and 925
  transitions run between them. Thirteen of the bodies and thirty of the
  transitions are walked by this variant and by no other of the 512.

**LITERAL**, the exclusive transitions, same lane, to the stated cap of
eight:

```
      llvm/lib/Target/X86/X86ISelLowering.cpp:60487 X86TargetLowering::PerformDAGCombine
        -> llvm/lib/Target/X86/X86ISelLowering.cpp:54660 combineFneg   (static call edge: True)
      llvm/lib/Target/X86/X86ISelLowering.cpp:60487 X86TargetLowering::PerformDAGCombine
        -> llvm/lib/Target/X86/X86ISelLowering.cpp:55110 combineFOr   (static call edge: True)
      llvm/lib/Target/X86/X86ISelLowering.cpp:35474 X86TargetLowering::isCommutativeBinOp
        -> llvm/lib/Target/X86/X86ISelLowering.cpp:3440 X86TargetLowering::isLoadBitCastBeneficial   (static call edge: False)
      llvm/lib/Target/X86/X86ISelLowering.cpp:55026 isNullFPScalarOrVectorConst
        -> llvm/lib/Target/X86/X86ISelLowering.cpp:54660 combineFneg   (static call edge: False)
      llvm/lib/Target/X86/X86ISelLowering.cpp:33573 X86TargetLowering::LowerOperation
        -> llvm/lib/Target/X86/X86ISelLowering.cpp:22566 LowerFABSorFNEG   (static call edge: True)
      llvm/lib/Target/X86/X86ISelLowering.cpp:33573 X86TargetLowering::LowerOperation
        -> llvm/lib/Target/X86/X86ISelLowering.cpp:9171 X86TargetLowering::LowerBUILD_VECTOR   (static call edge: True)
      llvm/lib/Target/X86/X86ISelDAGToDAG.cpp:375 shouldAvoidImmediateInstFormsForSize
        -> llvm/lib/Target/X86/X86ISelDAGToDAG.cpp:678 X86DAGToDAGISel::IsProfitableToFold   (static call edge: False)
      llvm/lib/Target/X86/X86ISelDAGToDAG.cpp:3308 X86DAGToDAGISel::isSExtAbsoluteSymbolRef
        -> llvm/lib/Target/X86/X86ISelDAGToDAG.cpp:678 X86DAGToDAGISel::IsProfitableToFold   (static call edge: False)
```

**GLOSS.** This is clang's floating-point negate path, named in the
compiler's own source coordinates: the DAG combiner reaching `combineFneg`,
the lowering step reaching `LowerFABSorFNEG`, the constant-pool vector
being built. Four of the eight have a static `calls` edge behind them, so
the walk and the structure agree; four do not, and each of those four
sits on a boundary the static walk had already recorded as a frontier.

## 6.2 The union, asked about the same bodies

**LITERAL**, lane 11 §[4/6]. The left column is
`coverage_c_and_cpp.json`'s own `per_node_visitors`, streamed one line
at a time; the right column is the third kind:

| compiler body | the UNION: probes of 1,380 that entered it | the THIRD KIND: variants of 512 whose traces walk the transition |
|---|---|---|
| X86TargetLowering::PerformDAGCombine | 1380 | 1 |
| combineFneg | 82 | 1 |
| combineFOr | 4 | 1 |
| X86TargetLowering::isCommutativeBinOp | 1380 | 1 |
| X86TargetLowering::isLoadBitCastBeneficial | 4 | 1 |
| isNullFPScalarOrVectorConst | 700 | 1 |
| X86TargetLowering::LowerOperation | 878 | 1 |
| LowerFABSorFNEG | 4 | 1 |
| X86TargetLowering::LowerBUILD_VECTOR | 4 | 1 |
| shouldAvoidImmediateInstFormsForSize | 806 | 1 |
| X86DAGToDAGISel::IsProfitableToFold | 56 | 1 |
| X86DAGToDAGISel::isSExtAbsoluteSymbolRef | 806 | 1 |

**GLOSS, and this is the answer to "what does it show that the union
does not".** `X86TargetLowering::PerformDAGCombine` is entered by
**1,380 of 1,380** probes. In the union it is indistinguishable from
start-up: a body everything touches, carrying no information about any
operator. In the third kind the **connection** `PerformDAGCombine →
combineFneg` belongs to **one variant of 512** — the four units whose
emitted body is a floating-point sign flip. The union cannot say this at
all, for two separate reasons: it has no edges, and it has no variants.
The same holds for `isCommutativeBinOp`, also 1,380 of 1,380, whose step
to `isLoadBitCastBeneficial` is likewise walked by that one variant.

## 6.3 The same instrument on the other compiler

**LITERAL**, lane 11 §[5/6], `variant_connections_go.json`:

```
   variant_id var_53d50fbe9bd4c8a2   members 9   probes 9   populations ['original', 'regenerated']
   machine form bytes : 21 d8 c3
   machine form text  : and %ebx,%eax; ret
   members and their display labels:
      go/op_240        label "&"    population original
      go/op_707        label "&&"   population original
      go/regen_402     label "&"    population regenerated
      go/regen_403     label "&"    population regenerated
      go/regen_405     label "&"    population regenerated
      go/regen_407     label "&"    population regenerated
      go/regen_408     label "&"    population regenerated
      go/regen_410     label "&"    population regenerated
      go/regen_551     label "&&"   population regenerated
   nodes 457 (exclusive 1), transitions 992 (exclusive 4, static-backed 235)
      src/cmd/compile/internal/ssa/func.go:806 invalidateCFG
        -> src/cmd/compile/internal/ssa/deadcode.go:311 removeEdge   (static call edge: False)
      src/cmd/compile/internal/ssa/dom.go:176 compressOrig
        -> src/cmd/compile/internal/ssa/dom.go:195 linkOrig   (static call edge: False)
      src/cmd/compile/internal/ssa/branchelim.go:290 isLeafPlain
        -> src/cmd/compile/internal/ssa/branchelim.go:433 canSpeculativelyExecute   (static call edge: False)
      src/cmd/compile/internal/ssa/branchelim.go:433 canSpeculativelyExecute
        -> src/cmd/compile/internal/ssa/branchelim.go:290 isLeafPlain   (static call edge: False)
```

**GLOSS.** Nine go units emit the same three bytes, and the machine form
put them together — two of them display `&&` and seven display `&`. The
connections exclusive to that variant are go's branch-elimination pass
walking back and forth between `isLeafPlain` and
`canSpeculativelyExecute`, and the control-flow graph being invalidated
and rebuilt: which is what a compiler does when a short-circuit form
collapses into a straight-line one. The instrument found that from the
diaries; no one told it what `&&` means.

---

# 7. The honest shape of the result

## 7.1 Most variants own nothing exclusively

**LITERAL**, lane 9 §[2/5]:

```
   variant_connections_c_and_cpp.json       512 variants,    6 own at least one exclusive transition,  506 own none
   variant_connections_extended.json       1361 variants,   15 own at least one exclusive transition, 1346 own none
   variant_connections_go.json              294 variants,    6 own at least one exclusive transition,  288 own none
```

**GLOSS.** Exclusivity is a hard test and this is what it costs: a
transition is exclusive only when **none** of the other 511 variants
walks it. Most operator traced variants walk the same compiler path as
some other variant, which is a finding about compilers rather than a
defect in the instrument — and it is why the census in §5.2 reports the
whole distribution and not only the exclusive band. The census's middle
bands are where the graded answer lives: 266 c-and-cpp transitions are
walked by **2 to 10** variants of 512.

## 7.2 The top of each population

**LITERAL**, lane 9 §[2/5], c and cpp:

```
          var_ac7b8914b059a2c0  members   4  probes    4  nodes  737  edges  925  exclusive edges  30  exclusive nodes  13
          var_66844d7456f6a1fe  members   1  probes    1  nodes  805  edges 1074  exclusive edges   9  exclusive nodes   4
          var_08f130de879e7f67  members   1  probes    1  nodes  692  edges  884  exclusive edges   5  exclusive nodes   1
          var_5b485545010bda60  members   2  probes    2  nodes  675  edges  855  exclusive edges   2  exclusive nodes   0
          var_90afb7a6a9d31c06  members  14  probes   14  nodes  625  edges  778  exclusive edges   1  exclusive nodes   0
```

## 7.3 The shape of the partition, recounted

**LITERAL**, lane 12 §[2/3]:

```
   variant_connections_go.json              variants   294  largest   19  singletons   208  members total   590
   variant_connections_c_and_cpp.json       variants   512  largest   18  singletons   190  members total  1380
   variant_connections_extended.json        variants  1361  largest   73  singletons   798  members total  3980
```

**LITERAL**, lane 12 §[1/3], the variants that span both source
languages of the one compiler:

```
   variant_connections_c_and_cpp.json         512 variants,  172 span more than one language
   variant_connections_extended.json         1361 variants,  209 span more than one language
```

**GLOSS.** 190 of the 512 c-and-cpp variants have a single member and
the largest has 18. **172 of the 512 hold both c and cpp units** — a
third of the partition is agreement between two source languages that
nothing in the grouping knows about, because the grouping reads only
what clang emitted.

## 7.4 What the regenerated population added

Going from 1,380 probes to 3,980 raises the variant count from 512 to
1,361, the nodes entered from 1,175 to 1,319, the transitions from 2,044
to 2,474, and the exclusive transitions from 48 to 66 — while the count
walked by every variant falls from 674 to 661, because a wider variant
population makes "every variant" a stronger condition. Every one of
those numbers is in `variant_connections_extended.json`.

---

# 8. The spelling ban — proved twice, mechanically and on the output

## 8.1 The mechanical guard, UNMODIFIED, in ONE process

**LITERAL**, lane 10 §[4/5]:

```
1d6aba67cbcdb021c3bdfd7f40fd2020  PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
   (git reports no change to the guard)
   guard exit=0
```

**LITERAL**, the whole of `Research/compiler_graph/guard_task87.txt`:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS variant_connections_go.json -- no operator token in any key, grouping, pairing or row structure
PASS variant_connections_c.json -- no operator token in any key, grouping, pairing or row structure
PASS variant_connections_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS variant_connections_c_and_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS variant_connections_extended.json -- no operator token in any key, grouping, pairing or row structure
PASS variant_connections_rust.json -- no operator token in any key, grouping, pairing or row structure
PASS variant_connections_swift.json -- no operator token in any key, grouping, pairing or row structure
```

**LITERAL**, the same lane:

```
   grep -c exempt over the transcript:
0
```

**GLOSS.** Seven artifacts, one process, exit 0, no file bought its way
past the guard with the provenance exemption. Two shapes in the output
were written as **typed unit objects** so a machine-form value could ride
without a role key or a field whitelist, which is the remedy task 81 had
ruled: every member row carries `id` + `language` beside its `operator`
label, and every transition endpoint carries `id` + `language` beside its
`label` — because a compiler function's own name can be one of the 91
tokens.

## 8.2 The ban proved ON THE OUTPUT, in both directions

A grouping that secretly used the token would put same-label units
together and never mix labels. Both directions were counted.

**LITERAL**, lane 10 §[2/5]:

```
   --- variant_connections_c_and_cpp.json
      variants                                       512
      variants whose members carry >1 display label   133
      distinct display labels in the population        36
      labels spread over more than one variant         36
      labels confined to exactly one variant            0
        MIXED var_90afb7a6a9d31c06 carries ['+', '++', '--', '__extension__']
        MIXED var_a42c93068b0aa1ba carries ['+', '++', '--', '/', '__extension__']
        MIXED var_55ac9f9fae5f4653 carries ['&', '&&', '*', 'and', 'bitand']
        MIXED var_e70aa2a291f94410 carries ['+', '++', '--', '/', '__extension__']
        SPREAD label ">="     appears in 58 distinct variants
        SPREAD label "<="     appears in 58 distinct variants
        SPREAD label ">"      appears in 58 distinct variants
        SPREAD label "<"      appears in 58 distinct variants
```

**GLOSS.** 133 of 512 variants hold members with different display
labels — one holds four different ones, because those four emit the same
machine code. And not one of the 36 labels is confined to a single
variant: `<` alone is spread over 58 of them. Neither number can occur if
the token is the key. The go population reads the same way: 2 mixed
variants of 294, `>>` spread over 93.

## 8.3 Zero regressions, PROVED against the pre-task-87 file

`graph.py` is shared: task 71 built it, task 75 folded `coverage.py`
into it, task 81 edited it, task 87 added the third connection kind. So
the two methods that were already there were run from the baseline
version out of git (commit `e2cba0db`, 2026-09-04 15:16) and from the
current one, over the same 30-diary go sample, and diffed.

**LITERAL**, lane 13 §[2/4] and §[3/4]:

```
  1822 /work/baseline/graph.py
  2397 Research/compiler_graph/graph.py
   baseline has 0 mentions of variant_connections (as expected)
   coverage: IDENTICAL
   super_ops parameters   identical: True
   super_ops populations  identical: True
   super_ops candidates   identical: True
   (the `cost` block carries wall time and a cache path and is expected to differ)
```

**GLOSS.** 575 lines added, nothing removed or rewritten, and both
pre-existing methods reproduce byte for byte.

**LITERAL**, lane 13 §[4/4], `check_plans.py` over the whole planning
tree:

```
summary: 196 error(s), 3 warning(s)
   check_plans exit=0
```

**GLOSS, stated rather than smoothed.** Those 196 are the tree's
standing conformance gaps — 14 of 69 COREs with no `nodes` register and
no edge fields, and the "first section is `## metadata`" style finding
that this node's CORE shares with most of the tree. None of them is new
this lap and none is fixed this lap; the protocol says the edge fields
are brought in chain by chain, not by a sweep.

---

# 9. Rust and swift — UNMEASURED, by name

**LITERAL**, lane 11 §[2/6], `variant_connections_rust.json` quoted
whole in its state and reason:

```
   state  : UNMEASURED_BY_ABSENCE_OF_DIARIES
   reason : rust is BLOCKED on this machine and the block is not build time: /sources/rust is a partial (promisor) clone whose objects are fetched lazily from the network, this instance is configured proxy = no, and the corpus's own rustc commit 31fca3adb283cc9dfd56b49cdee9a96eb9c96ffd is ABSENT from the checkout. Measured in log_175 section 6.3, lanes t72_l5..l7. Two decisions come before any compute: a complete checkout, and a ruling on the pin.
   populations: {"diaries_on_disk": 0, "probes_with_a_machine_form": 0, "operator_traced_variants": 0, "distinct_nodes_entered": 0, "distinct_transitions": 0}
```

and `variant_connections_swift.json`:

```
   state  : UNMEASURED_BY_ABSENCE_OF_DIARIES
   reason : swiftc CANNOT BE STARTED HERE and that is the measurement: swiftc is not installed in the container, and a swift compiler build wants five repositories side by side at matching tags of which three (cmark-gfm, swift-syntax, swift-corelibs-libdispatch) are absent from this disk and the fifth is Apple's LLVM fork rather than the upstream tree that is present. The direct cmake configure exits in 1 s on 'Could not find a package configuration file provided by cmark-gfm'. Measured in log_175 section 6.4. The cost is a FETCH decision first, roughly 10-15 GB, and a build second.
   populations: {"diaries_on_disk": 0, "probes_with_a_machine_form": 0, "operator_traced_variants": 0, "distinct_nodes_entered": 0, "distinct_transitions": 0}
```

**GLOSS.** Both artifacts exist and both say zero. Nothing was inferred
from the static structure, nothing was carried over from a nearby
language, and no number was written that a measurement did not produce.

---

# 10. What "completed" now means for this graph, and what is still missing

**The three connection kinds the owner named now all exist as data**, for the
two compilers this machine can instrument:

| kind | go | c and cpp | rust | swift | java, cpython, php, ruby |
|---|---|---|---|---|---|
| structural | done | done | done | done | **planned** (no build) |
| dynamic | 590 diaries | 1,380 + 2,600 diaries | **planned** | **planned** | **planned** |
| **per operator traced variant** | **590 probes, 294 variants** | **1,380 → 512; 3,980 → 1,361** | **UNMEASURED** | **UNMEASURED** | **planned** |

**The honest remainder, stated plainly:**

1. **rust and swift diaries.** The graphs exist; the diaries do not, and
   the third kind over them is UNMEASURED rather than approximated. rust
   is BLOCKED on this machine (a promisor clone with no route out, and
   the corpus's own compiler commit absent) and swift CANNOT BE STARTED
   here (three of five repositories absent). Both are FETCH and PIN
   decisions before any compute — log_175 §§6.3–6.4.
2. **java, cpython, php and ruby builds.** No graph at all yet; the
   CORE's realization table has carried these as **planned** since task
   71 and they have not moved.
3. **The recurring-path cap** stays where task 75 and task 81 left it:
   frequent runs were still growing at length 12 in both `super_ops`
   laps, so paths longer than 12 nodes exist and were not mined.
4. **The 15-body recount** between `t72/inject_report.json` (1,549) and
   `coverage_go2.json` (1,534) is still a frontier on this node.
5. **`Graph.coverage` still has no in-process memory check** — task 81's
   flag, deliberately untouched here.

Within that remainder, **pane 4 of the dashboard node is no longer
blocked on a missing object**: the graph it reads now carries all three
connection kinds for go and for c and cpp, in seven artifacts named
below.

---

# 11. Every artifact this task wrote

## 11.1 Products, with sizes as lane 10 §[5/5] printed them

| artifact | bytes | what it holds |
|---|---|---|
| `Research/compiler_graph/variant_connections_go.json` | 645,490 | 590 probes, 294 variants |
| `Research/compiler_graph/variant_connections_c.json` | 626,325 | 610 probes, 331 variants |
| `Research/compiler_graph/variant_connections_cpp.json` | 701,788 | 770 probes, 353 variants |
| `Research/compiler_graph/variant_connections_c_and_cpp.json` | 1,056,833 | 1,380 probes, 512 variants |
| `Research/compiler_graph/variant_connections_extended.json` | 3,169,862 | 3,980 probes, 1,361 variants |
| `Research/compiler_graph/variant_connections_rust.json` | 2,085 | UNMEASURED, with its reason |
| `Research/compiler_graph/variant_connections_swift.json` | 2,226 | UNMEASURED, with its reason |
| `Research/compiler_graph/guard_task87.txt` | 787 | the guard transcript, 7 PASS, exit 0 |

## 11.2 Programs

| file | change |
|---|---|
| `Research/compiler_graph/graph.py` | EDITED: `variant_structure`, `variant_connections`, `_variant_sets`, `machine_form`, `machine_form_identity`, `probe_unit_id`, `expand_unit_sources`, `VARIANT_CONNECTIONS_ARE`, `VARIANT_IDENTITY_STATED`, the `variant-connections` sub-command, and the module header's stub statement extended. Nothing already in the file was removed or rewritten |
| `Research/op_pipeline/check_no_spelling_keys.py` | UNCHANGED — md5 `1d6aba67cbcdb021c3bdfd7f40fd2020`, git reports no change |
| `Research/compiler_graph/t81/run_with_peak.py` | UNCHANGED, used as the peak-resident harness |

## 11.3 Lanes, all eleven, all exit 0

`Research/compiler_graph/lanes_t87/`:
`t87_l1_survey.sh`, `t87_l2_unit_sources.sh`,
`t87_l3_go_machine_form_hunt.sh`, `t87_l4_go_unit_id_scan.sh`,
`t87_l5_go_regen_units.sh`, `t87_l6_go_variant_connections.sh`,
`t87_l7_c_and_cpp_variant_connections.sh`,
`t87_l8_extended_and_unmeasured.sh`, `t87_l9_worked_example.sh`,
`t87_l10_rebuild_and_ban_proof.sh`, `t87_l11_report_literals.sh`,
`t87_l12_verify_report_claims.sh`,
`t87_l13_zero_regression_and_plan_check.sh`. Thirteen lanes, all exit 0.
Logs: `<runs>/t87/agent/logs/20260904T*__t87_l*.log`.
Instance config: `Airlock/instances/t87.conf`.

## 11.4 Tree

- `Planning/.../node_0_3_5_9_graph/CORE_0_3_5_9_graph.md` — two sub-nodes,
  the `## design` block, the call flow, two settled rules, five
  realization rows.
- `Planning/.../node_0_3_5_9_graph/PROGRESS.md` — two dated entries, the
  shape one written before the code and the measured one after.

---

# 12. Two lists

## 12.1 Decided, recorded for audit

1. **The variant's identity is a digest over four machine-form facts** —
   emitted body bytes, the same body as read, the entry contract, and
   the ledger's block / size / type / produced-by shape. Composite
   rather than any one of them, because it is the union of the
   machine-form evidence a unit carries; strictly finer than each. The
   counts under five candidate identities were measured first (lane 1
   §[5/7]) and the choice was made against them.
2. **A variant may span source languages.** c and cpp are one compiler
   and one graph, so two units with the same emitted form are one traced
   variant whichever of the two they were written in. 172 of the 512
   c-and-cpp variants span both.
3. **Exclusivity is measured against all other variants of the same
   population**, not against all other probes. A transition walked by
   nine probes of one variant is exclusive; the same transition walked
   by one probe of another variant is not.
4. **The census bands are reported whole**, with a note on the artifact
   saying the fifth number overlaps the fourth and the five must not be
   added.
5. **Every transition is joined to the static structure** and marked
   backed or not by a resolved `calls` edge, with the unbacked case
   explained on the artifact as a region-rule edge or an existing
   frontier — never as a defect.
6. **Lane 4's wrong reading of go's population is kept on disk** beside
   lane 5's correction, rather than being deleted.
7. **Zero regressions were proved, not asserted.** The baseline
   `graph.py` was taken out of git and both pre-existing methods were
   run side by side over the same sample; `coverage` is byte-identical
   and `super_ops` matches on parameters, populations and candidates.
8. **`Graph.coverage` was not touched.** Task 81 flagged that it carries
   no in-process memory check and left the shape question open for this
   CORE; task 87 wired the check into its own method and left the flag
   exactly where it was.

## 12.2 Awaiting the owner

1. **Is the graph "completed" in the sense you meant?** All three
   connection kinds now exist as data for go and for c and cpp. rust and
   swift carry the third kind as UNMEASURED with the cost page's reason,
   and java / cpython / php / ruby have no graph at all. If "completed"
   means all nine, the remainder in §10 is the schedule; if it means the
   three kinds over the compilers this machine can instrument, it is
   done and pane 4 can be built.
