# log 198 — task 93: the compiler graphs moved, made small, and DRAWN

Round 17. Nodes `hq.research.compiler_graph.graph` (0_3_5_9) and
`hq.research.compiler_graph.dashboard` (0_3_5_10).
Instance `t93`, six lanes, all exit 0. Instance taken down at the end.

---

## the two lists

### decided, recorded for audit

1. **A moment reaches the second repository by ITS OWN timestamp.** The
   graphs now live in `PseudoCoupGraphs`, a different repository from the
   one the page sits in, so "as of moment M" for an artifact over there
   is the graph folder's own commit at or before M's committer timestamp
   — `git rev-list -1 --before=<M's %cI> HEAD`. That is version control
   answering, unfiltered and unread: no message is consulted, no commit
   is promoted. Where the graph folder's history does not reach back that
   far, the figure DRAWS ITS REFUSAL and names the file. `GraphFolder` in
   `dashboard_ouro.py`.
2. **The string table's entries are rows, not bare elements.** The first
   cut wrote each distinct string as a bare list element and the
   UNMODIFIED guard refused both graphs, 7 places each — `new`, `and`,
   `not`, `delete`, `in`, `as`, `or`, `with`, `is`, `xor` are source
   identifiers in the compiler AND members of the 91-token operator
   inventory. Every entry is now `{"text": "..."}`. No exemption was
   added; this is the shape the CORE already ratified for the four x86
   mnemonics that are homographs, and the shape the ORIGINAL graph has,
   where the same identifier sits at `"detail": "new"`.
3. **The `entered` flag was read off a capped slice, and is not any
   more.** `coverage_files_build.py` decided whether a probe had entered
   a file from `file_runs`, which is the summary's first 600 runs of that
   probe's path. A file reached only after run 600 was written down as
   never entered. The cap belongs to what the summary CARRIES, not to
   what it COUNTS. Measured effect on go: **none** — 15 files never
   entered before and after, the same 15 names. It would have mattered
   for clang, whose summary is built for the first time in this task.
4. **`coverage_files_build.py` serves two compilers now.** It was written
   for go with the three paths as literals. They are a table
   (`SOURCES`), the body is unchanged, and `coverage_cpp_files.json` is
   built from `coverage_c_and_cpp.json` and the clang injector's own
   `instrumented_ids`.
5. **Which artifacts moved, and which did not, is a named list, never a
   wildcard.** Lane 5 prints the tracked status and the byte count of
   every candidate before touching one. The four earlier go laps
   (`graph_go2/go3/go4/go_lapone.json`, 533,590,808 bytes), the two
   earlier cpp laps (`graph_cpp2/cpp3.json`) and the superseded
   `coverage_go.json` **STAY where they are**, in this repository,
   untracked, as records of what was.
6. **Nothing was deleted before it was proved rebuildable.** For each
   graph, in one lane and in this order: compact into the companion
   folder → expand back → `cmp` against the original → only then remove
   the original.

### awaiting the owner

1. **7.3 GB in the companion folder is not in its git history, and
   repo-daemon refuses it by its own stated cap.** Its message, verbatim:
   `PseudoCoupGraphs: NOT committing -- 9938 files totalling 8504 MB
   exceeds max_commit_mb (1500 MB). NEEDS A LOOK: commit it by hand once
   you have decided what belongs in history.` The four compact graphs
   (72 MB) and the seven variant-connection files (6.2 MB) ARE committed
   — the latter by hand, because they were tracked in PseudoCoupHQ before
   the move and the move must not quietly untrack a finding. The coverage
   joins, the super-op candidates and the 4.48 GB of diaries are not.
   Two settled things point opposite ways and only the owner can say which
   governs: the folder's README says the diaries live here and local git
   tracks them every thirty seconds; the standing rule on what belongs in
   a repository gates by PROVENANCE and calls regenerable output out, and
   the joins and diaries are regenerable output. Until it is settled the
   daemon logs a refusal every thirty seconds.

---

## 1. PART A — the move

`PseudoCoupGraphs`, no remote, and **no origin was added**.

| folder | before | after |
|---|---:|---:|
| `PseudoCoupHQ/Research/compiler_graph` | 8,576,760,358 | 652,798,509 |
| `PseudoCoupGraphs` (including its `.git`) | 1,337 | 7,409,237,029 |

Moved, each verified by size and md5 before the original was removed
(lane `t93_l5_move.sh`, step 3):

| artifact | bytes | md5 |
|---|---:|---|
| `coverage_go2.json` | 515,160,866 | `80695d04aba1855f9efc94cafa1d1083` |
| `coverage_c.json` | 97,699,170 | `a3497d628b9e06003abc1a820aaa6951` |
| `coverage_cpp.json` | 316,493,701 | `7e99cafb55a254a33303f4f66c5f7cb5` |
| `coverage_c_and_cpp.json` | 416,754,589 | `6f6f7ecdee7b59c44b80f5a0b7f48e84` |
| `coverage_extended.json` | 1,270,743,838 | `55187e9ca57599a9d8fa989e95caaf67` |
| `super_ops_go.json` | 103,597,545 | `c49f2c07edb37bc680d017222dc2686f` |
| `super_ops_cpp.json` | 112,107,882 | `0f78b6c004dbf65047dcba65d32421bc` |
| `variant_connections_go.json` | 645,490 | `60a6c1990ebf8f34e1cd574fd52a46c9` |
| `variant_connections_c.json` | 626,325 | `07e33da65ff1f17c6a5744dfd65cf598` |
| `variant_connections_cpp.json` | 701,788 | `01c2ec7a71c20505a90f2204a640527c` |
| `variant_connections_c_and_cpp.json` | 1,056,833 | `e4409d96441bae7492955062316477d2` |
| `variant_connections_extended.json` | 3,169,862 | `36bf3f9d6f1db357a39a5b21186e353c` |
| `variant_connections_rust.json` | 2,085 | `ee97a2c388c2c5255d23623e694ab68e` |
| `variant_connections_swift.json` | 2,226 | `3d31d887e5fad531913ad80e3037c72d` |

`diaries/` moved through `tar` so its HARDLINKS survive: 4,484,020,997
bytes on both sides, and the six folders carry the same counts —
c 610, c_and_cpp 1,380, cpp 770, extended 3,980, go 590, regen 2,600 —
with `op_0.txt` compared byte for byte across the two sides.

**NOT moved, and it is deliberate.** `graph_go2.json` (122,505,637),
`graph_go3.json` (142,459,784), `graph_go4.json` (142,321,364),
`graph_go_lapone.json` (126,304,023), `graph_cpp2.json` (19,097,469),
`graph_cpp3.json` (26,501,104), `coverage_go.json` (27,608,025). They
are earlier laps and stay where they are as records.

**Where the graphs live is answered in ONE place**, so no reader carries
a path: `Research/compiler_graph/graphs_home.py` — the environment
variable `PSEUDOCOUP_GRAPHS`, then the Airlock mount
`PseudoCoupGraphs`, then a sibling of the repository, then
`PseudoCoupGraphs`.

### the readers, updated and PROVED by running

The proof is not that the code was edited. It is that
`graph_files_build.py` was run again over the MOVED, COMPACT graphs and
its output is **byte-identical to the eight summaries already tracked in
this repository** (lane `t93_l6`, step 2):

```
go     graph_go_files.json IDENTICAL      graph_go_defs.json IDENTICAL
cpp    graph_cpp_files.json IDENTICAL     graph_cpp_defs.json IDENTICAL
rust   graph_rust_files.json IDENTICAL    graph_rust_defs.json IDENTICAL
swift  graph_swift_files.json IDENTICAL   graph_swift_defs.json IDENTICAL
peak resident for the whole run: 52 MB (ceiling 6,144 MB)
```

And `Graph.load` over the compact graph in the companion folder:

```
   Graph.load over the COMPACT graph_go.json in the companion folder
     region            go
     nodes             10,393
     edges             63,797
     frontier          77,530
     0.1 s, peak resident 91.9 MB
     one node read back: {'id': 'src/cmd/compile/internal/abi/abiutils.go#657#def#0',
       'kind': 'def', 'language': 'go', 'file': '...abiutils.go',
       'label': 'ComputePadding', 'start_line': 657, 'end_line': 681}
```

Files changed for the move: `graphs_home.py` (new), `graph_compact.py`
(new), `graph_files_build.py` (`graph_path`, `stream_any`),
`graph.py` (`Graph.load` takes either form), `report_graph.py`
(`artifact`, `graph_document`), `coverage_files_build.py` (`SOURCES`,
`use`), `viewer_build.py` (`read_coverage`), `dashboard_ouro.py`
(`GraphFolder`, `graph_folder`, `coverage_at`).

---

## 2. PART B — made small, and NOTHING LOST

### the sizes, before and after, every graph

| graph | before | after | share | factor |
|---|---:|---:|---:|---:|
| `graph_go.json` | 49,278,033 | 4,839,116 | 9.8% | 10.2× |
| `graph_rust.json` | 61,987,708 | 6,297,219 | 10.2% | 9.8× |
| `graph_swift.json` | 165,106,660 | 21,263,773 | 12.9% | 7.8× |
| `graph_cpp.json` | 331,704,231 | 39,788,093 | 12.0% | 8.3× |
| **all four** | **608,076,632** | **72,188,201** | **11.9%** | **8.4×** |

### what changed, and it is only HOW the graph is stored

The two causes the brief named, both of them repetition:

* the frontier's `reason` sentence, 150–200 characters, repeated on
  77,530 go records — there are exactly **4 distinct sentences** in the
  whole go frontier;
* every edge writing two full source paths, both of which are already in
  the node table.

So: ONE STRING TABLE per document, ordered by how often each string
occurs (machine-form evidence), every record an array whose first
element is its schema, and each schema DISCOVERED from the file rather
than declared. `Research/compiler_graph/graph_compact.py`.

`pins` and `counts` stay at the front of the document, so every existing
256 KB head read keeps working unchanged — checked on all four:

```
go     counts carved: True nodes 10393  edges 63797   frontier 77530   files 81
rust   counts carved: True nodes 13446  edges 60382   frontier 101095  files 134
swift  counts carved: True nodes 71106  edges 192655  frontier 278245  files 230
cpp    counts carved: True nodes 112364 edges 386065  frontier 523694  files 269
```

### THE ROUND-TRIP DIFF, byte for byte, pasted

`graph_compact.py expand` rebuilds the old file; `cmp` and `diff -q`
compare it with the original. Lane `t93_l4_compact_all_four.sh`, and
again inside lane `t93_l5_move.sh` immediately before each original was
removed:

```
   --- go ---
     THE ROUND-TRIP DIFF: cmp graph_go.json <rebuilt> -> IDENTICAL, 0 differing bytes
     SIZE graph_go.json  before       49278033  after       4839116  (9.8%, 10.2x smaller)
   --- rust ---
     THE ROUND-TRIP DIFF: cmp graph_rust.json <rebuilt> -> IDENTICAL, 0 differing bytes
     SIZE graph_rust.json  before       61987708  after       6297219  (10.2%, 9.8x smaller)
   --- swift ---
     THE ROUND-TRIP DIFF: cmp graph_swift.json <rebuilt> -> IDENTICAL, 0 differing bytes
     SIZE graph_swift.json  before      165106660  after      21263773  (12.9%, 7.8x smaller)
   --- cpp ---
     THE ROUND-TRIP DIFF: cmp graph_cpp.json <rebuilt> -> IDENTICAL, 0 differing bytes
     SIZE graph_cpp.json  before      331704231  after      39788093  (12.0%, 8.3x smaller)
```

with md5 against md5 on every one, for example go:

```
   rebuilt /work/t93/rebuilt_go.json: 49278033 bytes, md5 71405afd56f3f5de41539c5c2c17c4b5
   expected                           49278033 bytes, md5 71405afd56f3f5de41539c5c2c17c4b5
   BYTE FOR BYTE IDENTICAL: True
```

Each compact document carries the original's byte count and md5 in its
own `provenance`, so the proof is re-runnable by anyone:

```
python3 graph_compact.py expand --compact <graph> --out <path> --verify
```

### the frontier is COMPLETE, counted both ways

```
   go     old form {"ambiguous_call": 2094, "no_reader_dispatched": 2, "unresolved_call": 6374, "unresolved_reference": 69060}
   go     compact  {"ambiguous_call": 2094, "no_reader_dispatched": 2, "unresolved_call": 6374, "unresolved_reference": 69060}
   go     identical: True   total 77530 frontier records
   rust   identical: True   total 101095 frontier records
   swift  identical: True   total 278245 frontier records
   cpp    identical: True   total 523694 frontier records
```

and record for record, every section, old form against compact:

```
     nodes     old   112364  compact   112364  every record equal: True
     edges     old   386065  compact   386065  every record equal: True
     frontier  old   523694  compact   523694  every record equal: True
```

### memory

Stated bound **6,144 MB**, abort named `MemoryCeilingReached`. Sampled
first (lane `t93_l1`): `json.load` + `json.dumps(indent=1)` of
`graph_go.json` peaked at **258.9 MB**, which is why the compactor
STREAMS instead. Measured peaks: compacting cpp **786.8 MB** at its
heaviest step, the whole four-graph pass under 800 MB, the summary
rebuild **52 MB**, the coverage joins **84 MB** (go) and **185 MB**
(clang), the whole pane-4 render pass **114.1 MB** against the page's own
1,500 MB cap. **No limit was hit and nothing was reduced to fit.**

---

## 3. PART C — pane 4, DRAWN

`Research/op_pipeline/dashboard_graph_draw.py` (new) draws;
`pane_coverage` in `dashboard_ouro.py` chooses the compiler, reads the
summaries at the moment, and hands them over. `dashboard_ouro.html`
gains the drawing's CSS and ONE click function, `ouro_cov`.

**No JavaScript.** Measured on what the pane emits (lane `t93_l6`,
step 6):

```
   NO JAVASCRIPT IN WHAT THIS PANE EMITS:
     <script                  0
     javascript:              0
     onload=                  0
     onerror=                 0
     onclick="python:       336
```

and read back off the live page in Ourobrowser, the whole document
carries `script_tags_in_the_page: 2` — the engine's own QWebChannel
handshake and the page's one `text/python` block, exactly as before.

### the three figures, in the owner's three words

1. **basic structure — the compiler's own organisation.** A band is a
   directory of the compiler's source, in path order. A box is one file,
   in path order inside its directory, shaded by how many definitions it
   holds. **A box's place is a function of its path** — there is no
   physics and no randomness, so the picture is the compiler's shape and
   is the same at every moment and in every figure. The inter-file
   `calls` connections are drawn as directed arcs; the heaviest 100 of
   them, with the population and the ceiling printed. Clicking a file
   draws THAT FILE'S connections alone (go's `addressingmodes.go`: 3 of
   331).
2. **dynamic connections — which parts our probes entered.** The SAME
   boxes in the SAME places, each filled in proportion to the share of
   its instrumented bodies at least one probe entered, and carrying
   `visited/instrumented`. A file no probe entered is drawn HOLLOW and
   dashed; a file with no instrumented body is HATCHED and named a frontier
   of the join, never a never-visited file.
3. **the traced directional connections made by our probes.** The same
   boxes again, and three ways to read them:
   * **in aggregate** — every ordered file-to-file step some probe's
     compilation took, weighted by how many probes take it, heaviest 80
     of the population, ceiling printed;
   * **one probe's own walk** — its ordered path with the step number on
     each box it first entered (`op_0`: 599 steps drawn);
   * **one operator traced variant** — the transitions that variant walks
     and NO OTHER variant walks, the third connection kind
     (`var_53d50fbe9bd4c8a2`: 4 arrows). The menu is ranked by how many
     transitions belong to a variant alone, which is machine-form
     evidence; the operator tokens appear once, as display labels on the
     member list, and are read back by nothing.

### what is drawn, per compiler, measured off the rendered page

| compiler | figures drawn | file boxes | structural arcs | directional arrows |
|---|---:|---:|---:|---:|
| go | 3 | 83 × 3 = 249 | 100 of 331 | 80 of the aggregate |
| c and cpp (clang) | 3 | 330 × 3 = 990 | 100 of 2,095 | 80 of the aggregate |
| rust | 1 | 134 | 100 of 1,022 | none — refused BY NAME |
| swift | 1 | 230 | 100 of 1,909 | none — refused BY NAME |
| java, cpython, php, ruby | none | — | — | drawn as `no graph` chips |

rust and swift draw figure 1 and then say, in figures 2 and 3, that no
probe of this corpus has ever been diaried through them, quoting the cost
page: rust BLOCKED on this machine (a promisor clone with no route out
and an absent pin), swift unstartable here (three of the five
repositories a build needs are not on this disk). **UNMEASURED BY ABSENCE
OF DIARIES, written down rather than approximated.**

### the memory rule, kept

`graph_cpp.json` is read for its **first 256 KB and no more**, for the
head line that names it. Every figure is drawn from
`graph_<lang>_files.json` (41–184 KB), `coverage_<lang>_files.json`
(2.6 MB go, 6.8 MB clang) and `variant_connections_<lang>.json`
(0.6–3.2 MB). `coverage_go2.json` (515 MB) is never opened at all.

### the chronology applies

Screenshots 13 and 14 are the same drawing at commit `51ad534fa0`
(2026-09-04 23:47); at that moment go renders all three figures and
**clang renders only figure 1**, because `coverage_cpp_files.json` did
not exist yet — the pane recomputes from that commit's own blobs rather
than remembering today's number. Screenshot 15 is commit `e3547c87ba`
(2026-09-03 00:01), where the pane refuses entirely and names
`Research/compiler_graph/graph_go_files.json` as what it would need.

### the clang coverage summary, built for the first time

```
cpp coverage -> 187 files, 1,380 probes, 7,540 never-visited rows,
                1,331 visited definitions, 88 files never entered
       wrote coverage_cpp_files.json (6,766,596 bytes) in 6.8 s;
       PEAK RESIDENT 185 MB (ceiling 6144 MB)
{"region_nodes": 112364, "defs": 10789, "instrumented_bodies": 8871,
 "probes": 1380, "visited_by_at_least_one_probe": 1331,
 "never_visited": 7540, "uninstrumented_defs_a_named_frontier": 1918,
 "probes_with_a_path": 1380, "files_with_a_row": 187,
 "files_never_entered": 88, "file_run_cap": 600}
```

go, rebuilt with the `entered` correction, is unchanged in every
population: 84 files with a row, 15 never entered, the same 15 names.

---

## 4. the gates

### the spelling guard, UNMODIFIED, ONE process, over every artifact

`md5 1d6aba67cbcdb021c3bdfd7f40fd2020`, and `git status --porcelain` over
it prints nothing. 21 artifacts, one process, **exit 0**:

```
operator inventory: 91 tokens read from probe_manifest_*.json
PASS graph_go.json / graph_cpp.json / graph_rust.json / graph_swift.json
PASS variant_connections_{go,c,cpp,c_and_cpp,extended,rust,swift}.json
PASS graph_{go,cpp,rust,swift}_files.json
PASS graph_{go,cpp,rust,swift}_defs.json
PASS coverage_go_files.json / coverage_cpp_files.json
   guard exit: 0
   grep -c exempt over the guard's own output: 0
```

Transcript: `Research/compiler_graph/guard_task93.txt`.

The page's own code guard, `check_dashboard_py_no_spelling.py`, over the
four python files this task wrote or touched: **PASS on all four,
exit 0** — `dashboard_ouro.py`, `dashboard_graph_draw.py`,
`graph_compact.py`, `graphs_home.py`. Every mention it lists is a token
appearing as a value or as prose (`/` in a path, `<` and `&` in the html
escape), in no position that keys anything.

**The guard caught a real violation and it was fixed at the cause.** See
"decided, recorded for audit" item 2. Lane 3's refusal, verbatim:

```
FAIL graph_go.compact.json -- 7 spelling-keyed place(s)
     $.strings[1017]  list element is the bare operator token 'delete'
     $.strings[1444]  list element is the bare operator token 'new'
     $.strings[3460]  list element is the bare operator token 'and'
     ...
```

### the JavaScript route and Ourobrowser, untouched

```
$ cd PseudoCoupHQ
$ git diff -- Research/op_pipeline/dashboard.html \
      'Research/op_pipeline/dashboard_pane*.js' | wc -l
0
$ cd Ourobrowser && git diff | wc -l
0
```

### the screenshots

`DevComms/screens/log_198/`, 16 of them, two compilers and two moments as
the gate requires and four compilers in all:

| file | what it shows |
|---|---|
| `01_pane4_go_now_figure1_structure.png` | go, figure 1 |
| `02_pane4_go_now_figure2_dynamic.png` | go, figure 2 |
| `03_pane4_go_now_figure3_direction.png` | go, figure 3 in aggregate |
| `04_pane4_go_one_file_held_figure1.png` | one file held, 3 of 331 arcs |
| `05_pane4_go_one_file_held_figure2.png` | the same file marked in figure 2 |
| `06_pane4_go_one_probe_walk.png` | `op_0`'s own ordered walk |
| `07_pane4_go_one_variant.png` | `var_53d50fbe9bd4c8a2`, 4 exclusive transitions |
| `08..10_pane4_cpp_now_figure{1,2,3}.png` | clang, the three figures |
| `11,12_pane4_rust_*.png` | rust: a graph, and the two refusals named |
| `13,14_pane4_{go,cpp}_at_an_earlier_commit.png` | the same drawings at `51ad534fa0` |
| `15_pane4_at_a_moment_it_cannot_be_recomputed.png` | the refusal at `e3547c87ba` |
| `16_pane4_back_at_now.png` | back at the present moment |

Rig: `Research/op_pipeline/t93_ouro_shots.py`, on the host, importing the
engine and not editing it. Peak resident of the python side **465 MB**.

---

## 5. every artifact this task names

**New programs**
`Research/compiler_graph/graphs_home.py`,
`Research/compiler_graph/graph_compact.py`,
`Research/op_pipeline/dashboard_graph_draw.py`,
`Research/op_pipeline/t93_ouro_shots.py`.

**Programs changed**
`Research/compiler_graph/graph.py`,
`Research/compiler_graph/graph_files_build.py`,
`Research/compiler_graph/coverage_files_build.py`,
`Research/compiler_graph/report_graph.py`,
`Research/op_pipeline/viewer_build.py`,
`Research/op_pipeline/dashboard_ouro.py`,
`Research/op_pipeline/dashboard_ouro.html`,
`Airlock/mounts.conf` (the companion folder, read-write).

**Lanes** — `Research/compiler_graph/lanes_t93/`:
`t93_l1_sample.sh`, `t93_l2_compact_go_rust.sh` (ABORTED, kept as the
record), `t93_l3_compact_go_rust.sh`, `t93_l4_compact_all_four.sh`,
`t93_l5_move.sh`, `t93_l6_readers_and_summaries.sh`.
Logs: `<runs>/t93/agent/logs/`.

**Artifacts written or rebuilt in PseudoCoupHQ**
`Research/compiler_graph/guard_task93.txt`,
`coverage_cpp_files.json` (new, 6,766,596 bytes),
`coverage_go_files.json` (rebuilt, 2,597,339 bytes),
`graph_{go,cpp,rust,swift}_files.json` and
`graph_{go,cpp,rust,swift}_defs.json` (rebuilt, byte-identical),
`DevComms/screens/log_198/01..16*.png`,
this log.

**Artifacts now in PseudoCoupGraphs**
`graph_{go,cpp,rust,swift}.json` (compact),
`coverage_{go2,c,cpp,c_and_cpp,extended}.json`,
`super_ops_{go,cpp}.json`,
`variant_connections_{go,c,cpp,c_and_cpp,extended,rust,swift}.json`,
`diaries/{c,c_and_cpp,cpp,extended,go,regen}`.

**Artifacts deliberately left where they are, as records**
`Research/compiler_graph/graph_go2.json`, `graph_go3.json`,
`graph_go4.json`, `graph_go_lapone.json`, `graph_cpp2.json`,
`graph_cpp3.json`, `coverage_go.json`.
