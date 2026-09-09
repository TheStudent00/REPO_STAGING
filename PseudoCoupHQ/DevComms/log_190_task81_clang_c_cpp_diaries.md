# log 190 — task 81: clang instrumented, the c and cpp diaries, the cpp coverage and super_ops

Date: 2026-09-04. Instance `t81`, brought down at the end of this log.
Brief: log_183 §"TASK 81". Precedent followed: task 72's go lap
(log_175) and task 75's miner (log_177).

Every rendering in this log is labelled per the protocol's §5.1a:
**LITERAL** is the object itself quoted from a file or a lane log,
**GLOSS** is a plain-words reading sitting beside a literal, and
**ANALOGY** is something that resembles the thing and is not it. No
gloss appears without its literal.

---

# 1. What was done, in plain words

## 1.1 The one-line account

clang was instrumented at `llvmorg-21.1.8` so that every function body
of its code-generation region writes its own graph coordinate as it is
entered; all 1,380 c and cpp units of the original corpus were
recompiled through it, one ordered diary each; those diaries were
joined to `graph_cpp.json` and mined for recurring sub-paths; and the
result was compared both ways against the output-side miner's cpp
candidates.

## 1.2 The five numbers that matter, each with its population

- **1,380 of 1,380** original probes diaried, 0 failed — 610 c units
  recounted from `canon39_wrapped_c.json` and 770 cpp units from
  `canon39_wrapped_cpp.json`.
- **1,331 of 8,871** instrumented compiler bodies visited by at least
  one of those 1,380 probes. **7,540 visited by none**, spread over
  **180 files**.
- **13,783** closed super-op candidates over the **770** cpp diaries,
  with the go lap's own parameters.
- **347 of 347** output-side records naming cpp units have a loose
  graph counterpart; **207** have a strict one; **0** have none.
- **151** further compiler bodies are reached when 2,600 regenerated
  probes are added (3,980 probes in all), and every one of the top ten
  files in that gain is in the X86 backend.

## 1.3 What is NOT claimed

- **Not** that the corpus exercises the compiler. 7,540 of 8,871
  instrumented bodies are never entered; the finding is the shape of
  what is missed, not a score.
- **Not** that a super-op candidate is a super-op. A candidate is a
  contiguous run of compiler coordinates that recurs across probes.
  What it means is a later question.
- **Not** that the whole regenerated population was diaried. 2,600 of
  27,080 were. §6 says exactly why the number is 2,600 and not 27,080.
- **Not** that rust or swift moved. Their rows stay **planned**; the
  cost page in log_175 §6.3–6.4 already says why.

---

# 2. The instrument, with values moving through it

## 2.1 What one hook is

A hook is one C++ statement placed immediately after the opening brace
of a function body in clang's `lib/CodeGen` or llvm's
`lib/Target/X86`. It writes that body's own node id from
`graph_cpp.json`.

**LITERAL**, `/persist/llvmsrc/clang/lib/CodeGen/CGExprScalar.cpp`
lines 132–136, printed by lane 17:

```
132-                             BinaryOperator::Opcode Opcode, bool Signed,
133-                             llvm::APInt &Result) {
134:  t81diary::note("clang/lib/CodeGen/CGExprScalar.cpp#71#def#0|mayHaveIntegerOverflow|clang/lib/CodeGen/CGExprScalar.cpp:71");
135-
136-  // Assume overflow is possible, unless we can prove otherwise.
```

**GLOSS.** The string has three pipe-fields: the node id as
`graph.py` mints it (`file#line#kind#ordinal`), the compiler function's
own name as a display label, and the declaration coordinate
`file:line`, which is the field the join actually uses.

## 2.2 What the subject column is, and why it exists

One diary interleaves the compiler's own start-up work with the
compilation of the probe. The subject column separates them: it is set
once, at the point clang has an LLVM function in hand and is about to
emit its body.

**LITERAL**, `/persist/llvmsrc/clang/lib/CodeGen/CodeGenFunction.cpp`
line 1614:

```
1614:  t81diary::enter("GenerateCode", Fn->getName().data(), (int)Fn->getName().size());
1615-
1616-  t81diary::note("clang/lib/CodeGen/CodeGenFunction.cpp#1466#def#0|CodeGenFunction::GenerateCode|clang/lib/CodeGen/CodeGenFunction.cpp:1466");
```

**GLOSS.** `Fn->getName()` is a `StringRef`, which is not
null-terminated, so the length rides beside the data. From that call
onward the second column of the diary carries the probe's own function
name instead of `-`.

## 2.3 One probe's values, moving

Take `cpp/op_0`. Its source is one function named `op_0` and nothing
else, compiled `clang++ -std=c++20 -O1 -c unit.cpp` — the SHIP tool
line, quoted from `op_pipeline/trickle_lanes/regen_c_c0023.sh` in
lane 4's log.

**LITERAL**, `diaries/cpp/op_0.txt`, lines 6117–6120, printed by
lane 17:

```
6117	op_0	-|subject_enter:GenerateCode|-
6118	op_0	clang/lib/CodeGen/CodeGenFunction.cpp#1466#def#0|CodeGenFunction::GenerateCode|clang/lib/CodeGen/CodeGenFunction.cpp:1466
6119	op_0	clang/lib/CodeGen/CodeGenFunction.cpp#1423#def#0|CodeGenFunction::BuildFunctionArgList|clang/lib/CodeGen/CodeGenFunction.cpp:1423
6120	op_0	clang/lib/CodeGen/CodeGenModule.cpp#329#def#0|&CodeGenModule::getTargetCodeGenInfo()|clang/lib/CodeGen/CodeGenModule.cpp:329
```

**GLOSS, step by step.**

- The compilation has already written 6,116 lines before this point.
  Every one of them carries `-` in the subject column: they are
  clang's own start-up — target registration, the assembler backend,
  the object writer — happening before any of the user's code is seen.
- Line 6117 is the marker. From here the subject column reads `op_0`:
  clang now has the LLVM function for the probe in hand.
- Line 6118 is `GenerateCode` itself, the body the marker was placed
  in, entering.
- Line 6119 is the argument list being built — the probe's parameters
  becoming LLVM arguments.
- Line 6120 asks the target for its ABI information, which is where a
  named parameter starts becoming a physical register.

The whole diary is 7,895 lines; **1,779 of them** carry `op_0` as the
subject. The miner reads only those 1,779 — that is what
`subject = "probe_own"` means, and it is the same setting go used.

---

# 3. What was built, and the four defects the building found

## 3.1 The chain of files

| file | what it is |
|---|---|
| `Research/compiler_graph/t81/diary_inputs_build.py` | writes `probes_cpp.json` (the 1,380 probe sources) and `diary_targets_cpp.json` (the 9,108 instrumentable bodies). EDITED this lap — see §3.5 |
| `Research/compiler_graph/t81/inject_diary_clang.py` | the injector: places the hooks in the checked-out llvm tree |
| `Research/compiler_graph/t81/run_with_peak.py` | NEW. Runs one of these programs in-process and prints the kernel's `ru_maxrss` |
| `Research/compiler_graph/graph.py` | `Graph.diary`, `Graph.coverage`, `Graph.super_ops` — task 71/75's file. EDITED this lap — see §3.5 |
| `Research/compiler_graph/report_super_ops.py` | the both-ways comparison. EDITED this lap — see §3.4 |
| `Research/compiler_graph/lanes_t81/t81_l3 … t81_l17` | the lanes |

## 3.2 Defect one — a label with a newline ran the string literal on

Lane 2 (2026-09-04 03:56, exit 2 in 68 s) failed to compile CGExpr.cpp
with `use of undeclared identifier 'E'` twenty times over. The cause:
202 of the 9,108 target labels carry a newline, because a declarator
wraps when the signature wraps; one of them ended the injected string
literal mid-function and the compiler read the rest of the function as
string text. `flatten_label` collapses the label's whitespace, which
loses nothing — nothing joins on a label. **Lane 3 then reported
`injected call lines : 8872`, `malformed : 0`** and CGExpr.cpp compiled
in 9 s.

## 3.3 Defect two — the instance was running a stale image

Lane 6 stopped at `ModuleNotFoundError: No module named 'tree_sitter'`.
Lane 9 tried every interpreter on the filesystem and found the module
on none of them.

**LITERAL**, host `podman inspect`:

```
t81-runner        localhost/sandbox-runner:latest eb3774c9ac56…  (built 40 hours ago)
sandbox-runner:latest                             178941132a3c…  (built 2 hours ago)
```

**GLOSS, and it is an Airlock behaviour rather than a task defect.**
`airlock up` reuses a container that already exists — its own output
says `t81-runner already existed; started`. The t81 container had been
created fifteen hours before the image was rebuilt, so the rebuild
never reached it. Removing the container and bringing the instance up
again fixed it; the named volume `t81-persist`, and so the built
clang, are untouched by that. **FLAGGED for Airlock**, not fixed here:
a rebuilt image does not reach an already-created instance, and
nothing warns.

## 3.4 Defect three — a memory gate that multiplied a fixed cost

Lane 10's gate measured one 50-probe sample at 1,050.5 MB and
projected 28,997 MB for 1,380 probes, refusing a pass that fits
comfortably. The error is that 1,049.6 MB of that sample is the GRAPH
in memory, which does not grow with the probes.

**LITERAL**, lane 11's replacement gate:

```
   peak at 50 probes : 1050.5 MB
   peak at 400 probes : 1445.5 MB
   fitted fixed cost      : 994.1 MB (the graph in memory)
   fitted per-probe cost  : 1.129 MB
   PROJECTION for the joint join : 2552 MB
   probes the 6,144 MB ceiling allows at this rate : 4563
   MEMORY GATE: under the ceiling; the full joins may run.
```

**GLOSS.** Cost is `fixed + per-probe × probes`; one measurement
cannot separate the two terms, so lane 11 takes two and fits them.
Lane 10 is kept on disk as the record — it refused safely, which is
what the rule asks for.

## 3.5 Defect four — the guard was right, and the fix is the ruled one

Lane 15 ran the unmodified `check_no_spelling_keys.py` over sixteen
artifacts in one process. Five FAILED, all for one cause.

**LITERAL**, `guard_task81.txt` as lane 15 wrote it:

```
FAIL coverage_c_and_cpp.json -- 1 spelling-keyed place(s)
     $.never_visited_rows[5407].label
         operator token 'consume' on a object that does not identify one unit -- this is a grouping/row key, not a per-unit label
```

**GLOSS.** A function of the compiler region is named `consume`, and
`consume` is one of the 91 operator tokens the guard reads out of the
probe manifests. The row carrying that name as its `label` had a unit
id but no language field, so the guard could not tell it identified
ONE unit and read the token as a grouping key. It was right to.

**THE FIX IS THE RULED ONE** (log_158): a flagged machine-form value
gets a typed-object SHAPE — not a role key, not a field whitelist, and
not an edit to the guard. `Graph.coverage`'s never-visited row and
`diary_inputs_build.py`'s target row now carry `language` beside their
unit id. Lane 16 proves nothing else changed:

```
   probes_cpp.json against the file before this lane:
      IDENTICAL
   diary_targets_cpp.json, lines only in the NEW file:
9108
   lines only in the OLD file (must be 0):
0
   every added line, by its key (must be one key only):
   9108 language
```

The injector reads `id`, `file`, `start_line`, `end_line` and `label`
and nothing else, so the built clang is still the clang these targets
describe and was not rebuilt.

## 3.6 The one change to `report_super_ops.py`, and its regression proof

`compare` spelled `go/` into the unit prefix in three places. It is now
`--language`, **defaulting to `go`**, and every key is composed from
that value, so `go_units_named` and
`output_side_records_naming_go_units` are what the default still
writes. A language is not an operator token — `go` and `cpp` name
which corpus a unit id belongs to, which is a machine coordinate.

Lane 7's byte-for-byte re-run found ONE character wrong: the
`why_both` sentence, now computed from the artifact in hand, read
`9809` where task 75's file reads `9,809`. That is a regression in
shape, small and real, and it was fixed rather than excused.

**LITERAL**, lane 12 §[3/3]:

```
   IDENTICAL -- zero regressions, proved rather than asserted
   the two sentences, LITERAL:
  "why_both": "669 of the 9,809 graph candidates are walked by all 590 probes, so the loose test on its own would report ubiquity as coincidence",
  "why_both": "532 of the 13,783 graph candidates are walked by all 770 probes, so the loose test on its own would report ubiquity as coincidence",
```

---

# 4. The lap, measured

## 4.1 The population, RECOUNTED inside the sandbox

The brief says 610 + 770 = 1,380. Lane 5 recounted it from the canon
rather than accepting the figure.

**LITERAL**, lane 5:

```
   canon39_wrapped_c.json : 610 units, tally {"WRAPPED_TEXT_PROVED": 610}
   canon39_wrapped_cpp.json : 770 units, tally {"WRAPPED_TEXT_PROVED": 770}
   RECOUNTED TOTAL : 610 + 770 = 1380
   probes_cpp.json  : 1380 probes
   in the canon but not a probe : 0
   a probe but not in the canon : 0
```

Lane 5 also re-ran `diary_inputs_build.py` INSIDE the sandbox, because
the two input files had first been written by a host run on 2026-09-03,
before the 2026-09-04 all-compute-through-Airlock ruling. Both came
back `IDENTICAL to the tracked file`.

## 4.2 The instrumented population, and its named frontiers

**LITERAL**, lane 11 §[1/6]:

```
   entry hooks actually placed       : 8871
   distinct declaration coordinates  : 8871
   skipped, each a NAMED FRONTIER    : 237
   by cause : {"defaulted_or_deleted_body": 40, "lambda_body": 186, "no_body_brace_in_own_lines": 11}
```

Beside those 237, two whole populations were excluded before the
injector ran and are counted in `diary_targets_cpp.json`: **1,664**
bodies declared in a header file (one edit there is carried into every
translation unit that includes it) and **17** with no declared name (a
lambda). Region defs 10,789; targets selected 9,108.

## 4.3 The build, against the cost page

| step | cost page (log_175 §6.2) | measured here |
|---|---|---|
| sparse tree expanded | 10 s | 7 s (lane 1) |
| cmake configure | 11 s | 8 s (lane 1) |
| one CodeGen object, cold | 73 s | 9 s warm, after the injection (lane 3) |
| **full clang build** | **1,316 s / 784 MB** | **1,378 s / 801 MB** (lane 3, exit 0) |

**LITERAL**, the pin quoted from the binary that was built:

```
clang version 21.1.8 (/sources/llvm-project 2078da43e25a4623cab2d0d60decddf709aaea28)
Target: x86_64-unknown-linux-gnu
```

## 4.4 The probe replay

The sample first, as the memory rule requires. **LITERAL**, lane 4:

```
   probes compiled : 40 of 40
   probes failed   : 0 of 40
   probes with an EMPTY diary : 0 of 40
   distinct pid-file counts seen : [1]
   seconds per probe : min 0.01  max 0.05  mean 0.02
   diary lines       : min 2215  max 8707  mean 5320
   PROJECTION for 1,380 probes: 28 s wall, 1.0 GB of diaries
   PEAK RESIDENT, replay driver : 15.1 MB
   PEAK RESIDENT, largest child (the compiler) : 69.1 MB
```

Then the full pass. **LITERAL**, lane 5:

```
[1380/1380] done=1380 failed=0  43.1 probes/s
FINAL done=1380 failed=0 of 1380
pid files per compile, by count: [(1, 1380)]
PEAK RESIDENT, replay driver : 16.0 MB
PEAK RESIDENT, largest child : 69.9 MB
   diaries/c : 610 files, 232M
   diaries/cpp : 770 files, 792M
   diaries/c_and_cpp : 1380 files, 1023M
   stray pid files left behind (must be 0):
0
```

**GLOSS on `pid files per compile`.** clang's driver forks a `-cc1`
process, so the hook writes `<COMPILER_DIARY>.<pid>` and the lane
merges what it finds. Every one of the 1,380 compiles produced exactly
one file: the driver never enters the region, so it never opens a
diary. `diaries/c_and_cpp` is 1,380 HARD LINKS to the same bytes, not a
second gigabyte.

---

# 5. The coverage join, and the finding

## 5.1 The graph, recounted

**LITERAL**, lane 11 §[2/6]:

```
   load seconds : 0.8
   PEAK RESIDENT after load : 1049.6 MB
   nodes RECOUNTED : 112364   (log_183 records 112,364)
   edges RECOUNTED : 386065   (log_183 records 386,065)
   nodes by kind   : {"data_row": 1196, "def": 10789, "file": 330, "local": 76562, "param": 23487}
   distinct files carried by nodes : 330   (record: 269 files)
```

**GLOSS on 330 against 269.** The two are not in conflict: the CORE's
row reads "269 files incl. 61 data tables", and 269 + 61 = 330. The
`.td` tables have file nodes and are not code files.

## 5.2 The four populations

**LITERAL**, lane 16 §[3/5], the joint join over all 1,380 probes:

```
   population_region_nodes                    112364
   population_defs                            10789
   population_instrumented                    8871
   population_probes                          1380
   instrumented_visited_by_at_least_one_probe 1331
   defs_visited_by_at_least_one_probe         1331
   never_visited_count                        7540
   uninstrumented_defs_a_named_frontier       1918
   visited_keys_outside_the_region            0
   never-visited FILES : 180
   c    : 1251 of 8871 instrumented bodies visited by 610 probes
   cpp  : 1328 of 8871 instrumented bodies visited by 770 probes
```

**GLOSS, population by population.**

- 112,364 region nodes; 10,789 of them are definitions.
- 8,871 of those definitions carry an entry hook. The other 1,918 are
  NAMED FRONTIERS — a header body or an unnamed one — and are never
  counted as never-visited.
- 1,380 probes visited 1,331 of the 8,871.
- **0 visited keys outside the region**: every coordinate any diary
  wrote is a node of this graph. That is the region rule holding.
- c alone reaches 1,251 and cpp alone 1,328, but the two together
  reach only 1,331 — the c path is very nearly a subset of the cpp
  one, which is what "clang serves both languages" means concretely.

## 5.3 The never-visited set, BY FILE

**LITERAL**, lane 17 §[4/6]:

```
   never-visited bodies : 7540 over 180 files, from a population of 8871 instrumented and 1380 probes
         719  llvm/lib/Target/X86/X86ISelLowering.cpp
         434  clang/lib/CodeGen/CGOpenMPRuntime.cpp
         425  clang/lib/CodeGen/CGStmtOpenMP.cpp
         259  clang/lib/CodeGen/CGObjCMac.cpp
         213  clang/lib/CodeGen/CGDebugInfo.cpp
         175  clang/lib/CodeGen/CGObjC.cpp
         170  clang/lib/CodeGen/CGExpr.cpp
         168  clang/lib/CodeGen/CodeGenModule.cpp
         160  clang/lib/CodeGen/MicrosoftCXXABI.cpp
         150  clang/lib/CodeGen/ItaniumCXXABI.cpp
```

The full 180-file table is in `coverage_cpp_summary.json` under
`never_visited_by_file`.

**GLOSS — the finding, by cause rather than by sighting.** The
never-visited mass falls into four groups, and only the first is about
this corpus at all.

1. **Language features the probes do not use.** OpenMP is 859 bodies
   across two files; Objective-C is 434 across two more; the Microsoft
   C++ ABI is 160. A probe is one function with two scalar parameters
   compiled for the Itanium ABI on Linux. None of this code can run.
2. **Debug information**, 213 bodies in `CGDebugInfo.cpp`. The ship
   tool line is `-O1` with no `-g`.
3. **The breadth of one file.** `X86ISelLowering.cpp` alone accounts
   for 719 never-visited bodies — it is the whole x86 lowering surface,
   most of it for vector and mask registers a scalar probe never
   reaches.
4. **The long tail.** 180 files carry never-visited bodies and the
   smallest carry one each — for instance
   `llvm/lib/Target/X86/X86SpeculativeExecutionSideEffectSuppression.cpp`,
   a pass that only runs under a mitigation flag.

**ANALOGY, labelled as such and standing next to the literal above,
not in place of it:** the corpus lights a narrow corridor through a
large building. The unlit rooms are mostly rooms this corpus has no
door to — OpenMP, Objective-C, the Microsoft ABI — rather than rooms
it walked past.

## 5.4 The memory bound, stated and then MISSED

The bound was stated before the pass (§3.4) and enforced with the
kernel's own `ru_maxrss`. Every full join's peak:

| join | probes | peak resident | wall | artifact |
|---|---|---|---|---|
| `diaries/cpp` | 770 | 2,089.0 MB | 21.5 s | 316,493,701 B |
| `diaries/c` | 610 | 1,185.9 MB | 5.6 s | 97,699,170 B |
| `diaries/c_and_cpp` | 1,380 | 2,530.4 MB | 36.7 s | 416,754,589 B |
| `diaries/extended` | 3,980 | **6,253.1 MB** | 279.2 s | 1,270,743,838 B |

**THIS IS A FLAG, and it is stated rather than smoothed.** The last row
is **6,253.1 MB against a stated ceiling of 6,144 MB** — 1.8% over —
and **nothing aborted**. The reason is mechanical: `Graph.super_ops`
calls `check_memory` and raises `MemoryCeilingReached` by name;
`Graph.coverage` has no such call, because the two were written in
different laps. The machine was never at risk (30 GB host, 12 GB
instance cap) and the fitted model under-predicted by 14%, which is
what a two-point fit on a nonlinear allocator does. Whether `coverage`
gains `super_ops`'s check is a shape question for
`CORE_0_3_5_9_graph.md` and is FLAGGED for the owner, not decided here.

---

# 6. The extension past the original corpus, and exactly how far it got

## 6.1 What the measurements allow

- Compiling one probe: **0.023 s**, **690 KB** of diary (lane 5).
- The regenerated c and cpp population: **27,080 units** — c 10,010,
  cpp 17,070 (lane 5, counted from `canon39_regen_store`). At the
  measured rate that is **542 s of compile and 18.7 GB of diary**. The
  COMPILE cost allows the whole thing.
- The coverage join: **994.1 MB fixed plus 1.129 MB a probe**, so the
  6,144 MB ceiling allows **4,563 probes** (lane 11).

**GLOSS.** The binding cost is the JOIN's, not the compiler's. So the
diary was extended to the largest population the join can actually
read: 2,600 more, for 3,980 in all.

## 6.2 Which 2,600, and the two defects choosing them found

Sorted by unit id over the whole regenerated population, then every
10th — arithmetic on unit ids, no token anywhere in the selection. The
slice touches **265 of the store's 308 chunks**.

Lane 13 found two defects of its own and refused rather than inventing
anything:

1. it read `probe_manifest_<lang>.json`, which carries the ORIGINAL
   corpus only (750 c rows, 1,002 cpp rows). A regenerated unit is
   `c/regen_<n>` and its source lives in the second generator's
   manifest, `probe_manifest2_<lang>.json` (51,829 c rows, 70,991 cpp).
   **2,557 of the 2,600 had no probe source and the lane said so.**
2. the 43 that did join by coincidence were written to a diary path
   built from the unit id, which carries a `/`: `c__c/regen_1.txt`
   names a subdirectory that does not exist, so `fopen` failed inside
   the hook and all 43 were recorded as "compiled, but the hook
   produced no diary".

Lane 14 fixed both. **LITERAL**:

```
   regenerated units, total : 27080
   every 10th taken          : 2600
   store chunks represented  : 265
   probe_manifest2_c.json rows keyed by n : 51829
   probe_manifest2_cpp.json rows keyed by n : 70991
   probe source found        : 2600
   probe source absent       : 0
   …
FINAL done=2600 failed=43 of 2600
```

**GLOSS on `failed=43`.** The state file is resumable and carried
lane 13's 43 failures forward as records; lane 14 retried them and they
succeeded, which is why `done` is 2,600 of 2,600. The 43 entries are
lane 13's history, not lane 14's outcome.

## 6.3 What the extra probes bought

**LITERAL**, lane 14 §[5/5] and lane 16 §[3/5]:

```
   population_instrumented                          8871 ->     8871
   population_probes                                1380 ->     3980
   instrumented_visited_by_at_least_one_probe       1331 ->     1482
   never_visited_count                              7540 ->     7389
   visited_keys_outside_the_region                     0 ->        0
   bodies visited by the extra probes and by no original probe : 151
         31  llvm/lib/Target/X86/X86FloatingPoint.cpp
         31  llvm/lib/Target/X86/X86InstrInfo.cpp
         21  llvm/lib/Target/X86/X86ISelLowering.cpp
         19  llvm/lib/Target/X86/X86FrameLowering.cpp
         11  llvm/lib/Target/X86/X86ISelLoweringCall.cpp
          5  llvm/lib/Target/X86/X86FixupVectorConstants.cpp
          4  clang/lib/CodeGen/Targets/X86.cpp
          4  llvm/lib/Target/X86/X86ISelDAGToDAG.cpp
          3  llvm/lib/Target/X86/X86RegisterInfo.cpp
          3  clang/lib/CodeGen/ABIInfoImpl.cpp
```

**GLOSS, and it is a real finding.** Tripling the probe count moves
the visited set by 151 bodies — 11% — and almost all of the gain is in
the X86 BACKEND, not the front end. `X86FloatingPoint.cpp` is the x87
stack pass, which a scalar `long double` reaches and nothing in the
original corpus does. The front end is saturated by 1,380 probes; the
backend is not.

## 6.4 How far this got, stated plainly

**2,600 of 27,080 regenerated c and cpp units were diaried; 24,480
were not.** The reason is not compile cost — that would have been
542 s — it is that the coverage join's measured cost admits 4,563
probes under the stated 6,144 MB ceiling and 1,380 were already spent.
The full regenerated population is reachable the moment `coverage`
either streams or is given a larger stated bound; both are shape
questions and neither is decided here.

---

# 7. `super_ops` over the cpp diaries

## 7.1 The parameters, quoted from the go artifact and not from notes

**LITERAL**, lane 7 §[1/6], read out of `super_ops_go.json` itself:

```
{
 "min_length": 3,
 "min_support": 2,
 "subject": "probe_own",
 "collapse_repeats": true,
 "max_length": 12,
 "max_runs_per_level": 2000000,
 "memory_ceiling_mb": 6144,
 "support_is_counted_in": "distinct probes",
 "closure": "closed contiguous runs only"
}
```

Those exact values were passed on the command line for the cpp run and
are written onto `super_ops_cpp.json`, where lane 17 read them back
identically.

## 7.2 The two laps side by side

| | go (task 75) | cpp (task 81) |
|---|---|---|
| probes | 590 | 770 |
| distinct coordinates in the streams | 626 | 1,172 |
| stream length, min … max | 1,945 … 5,182 | 918 … 4,200 |
| stream length, total | 1,998,333 | 1,185,628 |
| frequent runs at length 12 | 9,358 | 12,773 |
| **closed candidates** | **9,809** | **13,783** |
| wall | 20.4 s | 9.1 s |
| peak resident | 289.5 MB | 1,050.6 MB in the miner, 1,118.0 MB for the process |

**GLOSS.** cpp's streams are SHORTER than go's but its alphabet is
nearly twice as wide: a clang probe walks fewer events through more
distinct compiler functions. The peak is higher only because
`graph_cpp.json` is 331 MB against `graph_go.json`'s 49 MB — the
mining itself is cheaper.

**The same stated cap as go applies**: frequent runs were still growing
at length 12 (12,773 of them), so recurring paths longer than 12 nodes
exist and were not mined this lap.

## 7.3 One candidate, with its values

**LITERAL**, lane 17 §[5/6], the highest-ranked candidate:

```
   candidate_id cand_00000 length 12 probe_support 770 of 770
      llvm/lib/Target/X86/MCTargetDesc/X86AsmBackend.cpp:138       X86AsmBackend
      llvm/lib/Target/X86/MCTargetDesc/X86AsmBackend.cpp:1064      ELFX86AsmBackend
      llvm/lib/Target/X86/MCTargetDesc/X86AsmBackend.cpp:1108      ELFX86_64AsmBackend
      …
      llvm/lib/Target/X86/X86AsmPrinter.cpp:56                     X86AsmPrinter::X86AsmPrinter
      llvm/lib/Target/X86/X86TileConfig.cpp:60                     getRequiredProperties
```

**GLOSS.** Support 770 of 770 means every probe walks it. This is
clang setting up its ELF object writer — start-up, not the probe's
expression. It ranks first precisely because it is ubiquitous, which is
why the comparison in §8 runs a strict test as well as a loose one.

A discriminating one, **LITERAL**, same lane:

```
   the highest-support candidate NOT walked by every probe:
   cand_00532 length 11 support 769 of 770
      llvm/lib/Target/X86/X86FixupBWInsts.cpp:424    FixupBWInstPass::processBasicBlock
      llvm/lib/Target/X86/X86RegisterInfo.cpp:280    X86RegisterInfo::getCalleeSavedRegs
      llvm/lib/Target/X86/X86ISelLowering.cpp:62074  X86TargetLowering::supportSwiftError
      …
      llvm/lib/Target/X86/X86FixupLEAs.cpp:220       FixupLEAPass::runOnMachineFunction
      llvm/lib/Target/X86/X86FixupLEAs.cpp:215       isLEA
```

**GLOSS.** This is the machine-function fix-up chain: byte/word
instruction widening, then the LEA fix-up pass. One probe of the 770
does not walk it.

---

# 8. The both-ways comparison

## 8.1 The join, and what it is

**LITERAL**, `super_ops_comparison_cpp.json`, read by lane 17:

```
   what_this_join_is : for every candidate of the superseded output-side miner whose named sample units are cpp units, does a diary sub-path recur across exactly those probes? The scope is the output-side record's own unit ids -- machine coordinates, no operator token anywhere in the pairing.
   populations       : {"output_side_candidate_records": 494, "output_side_records_naming_cpp_units": 347, "graph_candidates": 13783, "graph_candidate_probes": 770}
   output_side_with_a_graph_counterpart_loose           347
   output_side_with_a_graph_counterpart_strict          207
   output_side_without_a_graph_counterpart              0
   graph_candidates_with_an_output_side_counterpart     6020
   graph_candidates_without_an_output_side_counterpart  7763
```

## 8.2 What it showed, read against go

| | go (task 75) | cpp (task 81) |
|---|---|---|
| output-side records, total | 494 | 494 |
| …naming units of this language | 59 | **347** |
| with a LOOSE counterpart | 59 | 347 |
| with a STRICT counterpart | **0** | **207** |
| with NO counterpart | 0 | 0 |
| graph candidates with a counterpart | 4,479 of 9,809 | 6,020 of 13,783 |
| graph candidates with none | 5,330 | 7,763 |

**GLOSS, and this is the result of the comparison.** On the go lap the
strict test found NOTHING: every match was a sub-path the whole corpus
walks, so the loose result could not be distinguished from ubiquity.
On the cpp lap **207 of 347 output-side records have a graph candidate
that recurs in exactly the units the record names and in no others**.
That is the first time this join has produced a discriminating answer.

**What it still cannot say**, quoted from the artifact rather than
softened: `the output-side records carry SAMPLE unit ids, not their
full member lists, so a subset test is over the sample`.

## 8.3 One strict match, LITERAL

```
      idiom_id  idiom_0107
      section   resolved
      support   6
      units it names (4): ['cpp/op_513', 'cpp/op_518', 'cpp/op_981', 'cpp/op_986']
      candidates confined to those units (8): ['cand_12345', 'cand_12346', 'cand_12347', 'cand_12348', 'cand_12349', 'cand_12350']
```

**GLOSS.** The output-side miner grouped four cpp units by what their
machine code looks like. Eight diary sub-paths recur across exactly
those four probes and across no other probe of the 770. The two sides
were built from different evidence — one from emitted instructions,
one from the compiler's own control flow — and they agree on the
scope. **The pairing is by unit id throughout: no token enters the
candidate selection, the comparison scope, or any key.**

---

# 9. The spelling ban — the mechanical guard, transcript

The guard ran UNMODIFIED, in ONE process, over every artifact this
task produced.

**LITERAL**, the command, from `lanes_t81/t81_l16_typed_rows_and_guard.sh`:

```
python3 "$PIPELINE/check_no_spelling_keys.py" $ARTIFACTS \
    > "$REPO/guard_task81.txt" 2>&1
```

**LITERAL**, its whole output (`Research/compiler_graph/guard_task81.txt`,
also in lane 16's log):

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS probes_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS diary_targets_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS inject_report_cpp2.json -- no operator token in any key, grouping, pairing or row structure
PASS instrumented_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS diary_state_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS diary_state_regen.json -- no operator token in any key, grouping, pairing or row structure
PASS probes_regen_slice.json -- no operator token in any key, grouping, pairing or row structure
PASS sample_probe_cost.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_cpp_summary.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_extended_summary.json -- no operator token in any key, grouping, pairing or row structure
PASS super_ops_comparison_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS super_ops_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_c.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_c_and_cpp.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_extended.json -- no operator token in any key, grouping, pairing or row structure
```

**LITERAL**, the three checks the gate names:

```
   guard exit=0
   grep -c exempt on that output:
0
   (no line above means the guard file is untouched)
1d6aba67cbcdb021c3bdfd7f40fd2020  PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py
```

Sixteen artifacts, one process, exit 0, `grep -c exempt` = 0, the guard
file unmodified with `git status --porcelain` printing nothing for it.

---

# 10. Every artifact this task wrote, INCLUDING the superseded ones

## 10.1 Products

| path | bytes | tracked? |
|---|---|---|
| `Research/compiler_graph/t81/probes_cpp.json` | 437,302 | tracked |
| `Research/compiler_graph/t81/diary_targets_cpp.json` | 1,904,787 → rewritten with `language` | tracked |
| `Research/compiler_graph/t81/inject_report_cpp2.json` | 950,802 | tracked |
| `Research/compiler_graph/t81/instrumented_cpp.json` | 1,222,603 | tracked |
| `Research/compiler_graph/t81/diary_state_cpp.json` | 74,612 | tracked |
| `Research/compiler_graph/t81/diary_state_regen.json` | 125,344 | tracked |
| `Research/compiler_graph/t81/probes_regen_slice.json` | 738,375 | tracked |
| `Research/compiler_graph/t81/sample_probe_cost.json` | 9,965 | tracked |
| `Research/compiler_graph/coverage_cpp_summary.json` | 9,739 | tracked |
| `Research/compiler_graph/coverage_extended_summary.json` | 10,534 | tracked |
| `Research/compiler_graph/super_ops_comparison_cpp.json` | 13,078,736 | tracked |
| `Research/compiler_graph/guard_task81.txt` | — | tracked |
| `Research/compiler_graph/super_ops_cpp.json` | 112,107,882 | ignored, regenerable |
| `Research/compiler_graph/coverage_c.json` | 97,699,170 | ignored, regenerable |
| `Research/compiler_graph/coverage_cpp.json` | 316,493,701 | ignored, regenerable |
| `Research/compiler_graph/coverage_c_and_cpp.json` | 416,754,589 | ignored, regenerable |
| `Research/compiler_graph/coverage_extended.json` | 1,270,743,838 | ignored, regenerable |
| `Research/compiler_graph/diaries/{c,cpp,c_and_cpp,regen,extended}/` | 1,023 MB + 2.1 GB | ignored, regenerable |
| `Research/compiler_graph/t81/sample_one.diary` | — | ignored |

## 10.2 Programs

| path | new or edited |
|---|---|
| `Research/compiler_graph/t81/run_with_peak.py` | NEW |
| `Research/compiler_graph/t81/inject_diary_clang.py` | edited before this session's first build (the `flatten_label` repair, §3.2) |
| `Research/compiler_graph/t81/diary_inputs_build.py` | edited: the target row is a typed unit object (§3.5) |
| `Research/compiler_graph/graph.py` | edited: the never-visited row is a typed unit object (§3.5) |
| `Research/compiler_graph/report_super_ops.py` | edited: `--language`, defaulting to `go` (§3.6) |
| `.gitignore` | extended: the five regenerable artifacts above |

## 10.3 Lanes, including the three that stopped

| lane | outcome | what it was |
|---|---|---|
| `t81_l1_tree_configure.sh` | exit 0, 16.9 s | the tree at the pin, and cmake configure (written before this session) |
| `t81_l2_inject_build.sh` | **exit 2**, 68.3 s | the first injection; the label-newline defect (§3.2) |
| `t81_l3_reset_inject_build.sh` | exit 0, 1,378.0 s | reset, re-inject, both halves, full clang build |
| `t81_l4_sample_probes.sh` | exit 0, 1.0 s | the 40-probe sample |
| `t81_l5_full_probes.sh` | exit 0, 33.6 s | all 1,380 probes |
| `t81_l6_coverage.sh` | **exit 7**, 0.2 s | stopped: stale container image (§3.3) |
| `t81_l9_python_probe.sh` | exit 0, 4.9 s | which interpreter has tree_sitter |
| `t81_l10_coverage.sh` | **exit 9**, 2.7 s | stopped at its own memory gate (§3.4) |
| `t81_l11_coverage.sh` | exit 0, 76.4 s | the two-point gate, and three joins |
| `t81_l7_super_ops.sh` | exit 0, 92.3 s | the miner and the first comparison |
| `t81_l12_comparison_redo.sh` | exit 0, 82.2 s | the comparison after the one-character fix |
| `t81_l13_regen_extension.sh` | exit 0, 39.5 s | the extension's two defects (§6.2) |
| `t81_l14_regen_extension2.sh` | exit 0, 346.9 s | 2,600 regenerated probes, and the extended join |
| `t81_l15_guard.sh` | exit 0, 11.2 s | the guard's refusal (§3.5) |
| `t81_l16_typed_rows_and_guard.sh` | exit 0, 360.0 s | typed rows, four joins rebuilt, guard PASS |
| `t81_l17_report_literals.sh` | exit 0, 0.6 s | the literals this log quotes |

Logs: `<runs>/t81/agent/logs/`, statuses
`<runs>/t81/agent/status/`. Lane scripts:
`Research/compiler_graph/lanes_t81/`. Superseded artifacts are kept as
records, unedited: `t81/inject_report_cpp.json` (the failed first
injection) and lanes `t81_l6`, `t81_l8`, `t81_l10`, `t81_l13`.

---

# 11. Two lists

## 11.1 Decided, recorded for audit

- The instrumented population is `.cpp` bodies only; header bodies
  (1,664) and unnamed bodies (17) are NAMED FRONTIERS, counted, never
  never-visited.
- The extension's slice is every 10th regenerated unit by unit id,
  sized by the coverage join's own measured cost.
- `report_super_ops.py compare` takes `--language`, defaulting to `go`;
  the go artifact re-runs byte-identical.
- The never-visited row and the injection target row carry a
  `language` field, making each a typed unit object — the ruled remedy
  for the guard's refusal.
- `diaries/c_and_cpp` and `diaries/extended` are hard links, not
  copies.

## 11.2 Awaiting the owner — three flags, none decided here

1. **`Graph.coverage` has no memory check.** The extended join peaked
   at 6,253.1 MB against a stated 6,144 MB ceiling and nothing aborted,
   because only `Graph.super_ops` calls `check_memory`. Whether
   `coverage` gains the same call — or is rewritten to stream — is a
   shape question for `CORE_0_3_5_9_graph.md`.
2. **A rebuilt Airlock image does not reach an already-created
   instance.** `airlock up` reuses the container and says so, but
   nothing warns that its image is older than `:latest`. This cost one
   lane and is generic to every caller; it belongs in Airlock, not
   here. (Task 82 is already editing Airlock's status views.)
3. **24,480 of the 27,080 regenerated c and cpp units are still
   undiaried**, and the reason is the join's bound rather than the
   compiler's cost. Whether that bound should be raised for this node
   is the owner's.
