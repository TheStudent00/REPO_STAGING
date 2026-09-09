# log 181 — task 73: pane 4, the coverage view

Node: `hq.research.compiler_graph.dashboard`, the `coverage_view` method
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md`),
with two builders under `hq.research.compiler_graph.graph`.
Brief: log_172 task 73. Date: 2026-09-03.

---

# 1. What pane 4 is now

Open `Research/op_pipeline/dashboard.html`, grant the folder, and the sixth
nav button — **compiler graph & coverage — pane 4** — draws the compiler's
own source, per compiler, in the three parts the brief names.

## 1.1 The three parts, and which compilers have them

| part | go | cpp | rust | swift |
|---|---|---|---|---|
| (a) static structure — the region as a wiring diagram | drawn | drawn | drawn | drawn |
| (b) dynamic structure — a probe's diary path lit in order | drawn, 590 probes | NOT MEASURED | NOT MEASURED | NOT MEASURED |
| (c) coverage — the union over the corpus, never-visited listed | drawn, 810 listed | NOT MEASURED | NOT MEASURED | NOT MEASURED |

- Where (b) and (c) are not measured the pane says so in its own card, in
  the population line, and in the legend, and names task 72's cost page —
  `DevComms/log_175_task72_go_diaries_coverage.md` — as the thing that
  prices the measurement. Screenshot: `screens/log_181/pane4_cpp.png`.
- The shading for "not measured" (`#2b3444`, flat slate) and the shading
  for coverage (a warm scale) are deliberately unlike each other, so an
  unmeasured compiler cannot be misread as a measured one.

## 1.2 Every view carries its population line

The line above the canvas is a count over files on disk at open time. For
go it reads, verbatim off the page:

```
10,393 graph nodes, 63,797 edges and 77,530 frontier records over 81 files,
read as 83 file rows from graph_go_files.json — 590 probes with a diary;
1,534 instrumented bodies of 1,859 definitions (325 uninstrumented — a
named frontier); 724 visited, 810 never — opened at 19:54:19
```

- **LITERAL:** that is the text of `#g4-pop` in
  `screens/log_181/pane4_go_never_visited.png`.
- **GLOSS:** 83 file rows against 81 files in `counts` is not a discrepancy
  hidden — two rows (`ssa/flags_amd64_test.s`, `ssa/flags_arm64_test.s`)
  carry zero nodes and only frontier records, because task 71's region rule
  lists `.s` files and then records them as the frontier
  `no_reader_dispatched`. The pane draws only rows with nodes, so 81 boxes
  are drawn.

For cpp the same line reads `112,364 graph nodes, 386,065 edges and 523,694
frontier records over 269 files, read as 330 file rows from
graph_cpp_files.json — 0 probes: the dynamic structure and the coverage are
NOT MEASURED for this compiler`.

---

# 2. The memory problem, with the values moving

The brief's binding rule is that the page must never load a whole graph.
This section walks one number through the machinery so the rule is visible
rather than asserted.

## 2.1 What is on disk, and why it cannot be opened

| file | bytes |
|---|---|
| `coverage_go2.json` | 515,160,866 |
| `graph_cpp.json` | 331,704,231 |
| `graph_swift.json` | 165,106,660 |
| `super_ops_go.json` | 103,597,545 |
| `graph_rust.json` | 61,987,708 |
| `graph_go.json` | 49,278,033 |

A page opened by double-click that parsed `graph_cpp.json` would hold the
parsed form of 331 MB of json — several times that in javascript objects.
A round-15 miner reached 13.2 GB on the same class of data and the desktop
swapped (graph CORE, settled rule, from task 75).

## 2.2 The shape: summarise once in python, slice on demand in the page

Two builders were written under the graph node. Both stream, both state
their peak resident set, both refuse by name above a stated ceiling.

### 2.2.1 `graph_files_build.py`, one record at a time

The graphs are written with `json.dump(indent=1)`, so a top-level array
element opens on a line of exactly two spaces and a brace. The builder
reads line by line, accumulates one record, parses it, folds it into
aggregates, and drops it.

It builds **no node table at all**. Task 71's id scheme (log_174) is
`file#line#kind#ordinal`, so both the file and the kind are read off the id
by string surgery. Watch one edge of `graph_go.json` move through:

```
line read:  {"src": "src/cmd/compile/internal/abi/abiutils.go#657#def#0",
             "dst": "src/cmd/compile/internal/abi/abiutils.go#674#local#0",
             "rel": "contains"}
file_of(src) -> "src/cmd/compile/internal/abi/abiutils.go"
file_of(dst) -> "src/cmd/compile/internal/abi/abiutils.go"
same file    -> not an inter-file edge, nothing recorded
kind_of(dst) -> "local", not a def -> not a definition-to-definition edge
record dropped; resident set unchanged
```

and one that is kept:

```
file_edges[("…/ssagen/ssa.go", "…/ssa/rewrite.go", "calls")] += 1
```

At the end the 331 distinct (file, file, relation) triples of go become 331
rows of `[srcIndex, dstIndex, relation, count]` — the wires the page draws.

### 2.2.2 `coverage_files_build.py`, one line at a time, keeping byte offsets

`coverage_go2.json` is read in BINARY, and the builder tracks the byte
offset of every line so it can hand the page a range. Watch probe `op_103`:

```
byte 5,520,276   section per_probe_path opens
…
line '  "op_103": ['      at byte 5,520,307 -> probe_start = 5,520,307
line '   "src/cmd/compile/internal/ssa/rewrite.go:815",'
        events 1; file run [slot(rewrite.go), 1]
line '   "src/cmd/compile/internal/ssa/rewrite.go:815",'
        events 2; the run becomes [slot(rewrite.go), 2]
…
line '  ],'                 at byte 6,266,224 -> byte_end = 6,266,225
record written: {"probe":"op_103","events":18270,"file_runs":<first 600>,
                 "file_runs_total":10008,"file_runs_carried":600,
                 "byte_start":5520307,"byte_end":6266225}
```

- `FILE_RUN_CAP = 600` is the one bound of the artifact, stated on the
  artifact: 590 probes with a median 7,953 file-level runs each will not fit
  in a summary the page reads whole, so the summary carries the first 600
  and every row prints `file_runs_carried` beside `file_runs_total`.
- The whole path is never lost. It is one ranged read away, which is 2.3.

## 2.3 The ranged read, measured in the browser

Choosing probe `op_103` in the pane produced, on the page:

```
probe op_103: 18,270 diary events read in 8 ms by ONE ranged read of
929,634 bytes; 10,008 file-level steps. The summary carried the first 600
of 10,008 for the preview; this is the whole path.
```

- **LITERAL:** the text of `#g4-tip` in
  `screens/log_181/pane4_go_diary_path.png`; the 8 ms is a
  `performance.now()` difference the page took itself.
- **GLOSS:** 929,634 bytes of 515,160,866 — 0.18 % of the file — bought the
  complete ordered path of one probe. The page never opens the other 99.82 %.

## 2.4 The peak resident sets, pasted

Run smallest graph first, as the brief directs. `resource.getrusage(RUSAGE_SELF).ru_maxrss`, ceiling 6,144 MB, `MemoryCeilingReached` raised by name above it (never reached).

```
$ /tmp/reconnect_venv/bin/python3 graph_files_build.py go rust swift cpp
PASS graph_go_files.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_go_defs.json -- no operator token in any key, grouping, pairing or row structure
go     151,720 records -> 83 files, 331 inter-file pairs, 1,859 defs, 6,870 def-to-def edges
       wrote graph_go_files.json (40,966 bytes) and graph_go_defs.json (567,447 bytes) in 0.5 s; PEAK RESIDENT 17 MB (ceiling 6144 MB)
PASS graph_rust_files.json …
rust   174,923 records -> 134 files, 1,022 inter-file pairs, 3,313 defs, 8,711 def-to-def edges
       wrote graph_rust_files.json (84,629 bytes) and graph_rust_defs.json (913,267 bytes) in 0.5 s; PEAK RESIDENT 20 MB (ceiling 6144 MB)
PASS graph_swift_files.json …
swift  542,006 records -> 230 files, 1,909 inter-file pairs, 10,088 defs, 17,708 def-to-def edges
       wrote graph_swift_files.json (147,669 bytes) and graph_swift_defs.json (2,392,393 bytes) in 1.5 s; PEAK RESIDENT 31 MB (ceiling 6144 MB)
PASS graph_cpp_files.json …
cpp    1,022,123 records -> 330 files, 2,095 inter-file pairs, 10,789 defs, 35,773 def-to-def edges
       wrote graph_cpp_files.json (183,876 bytes) and graph_cpp_defs.json (3,345,141 bytes) in 2.8 s; PEAK RESIDENT 39 MB (ceiling 6144 MB)
```

```
$ /tmp/reconnect_venv/bin/python3 coverage_files_build.py
   ... entering per_node_visitors at byte 190,833, peak 12 MB
   ... entering per_probe_path at byte 5,520,276, peak 12 MB
   ... entering provenance at byte 515,160,618, peak 42 MB
PASS coverage_go_files.json -- no operator token in any key, grouping, pairing or row structure
go coverage -> 84 files, 590 probes, 810 never-visited rows, 724 visited definitions, 15 files never entered
       wrote coverage_go_files.json (2,597,323 bytes) in 8.3 s; PEAK RESIDENT 82 MB (ceiling 6144 MB)
```

- **LITERAL:** every "PEAK RESIDENT" figure above is `ru_maxrss / 1024`
  printed by the builder at the end of its own run.
- **GLOSS:** the largest peak of the whole task is **82 MB**, over a
  515 MB input. Nothing came near the 6,144 MB ceiling and nothing was
  stopped from outside. The first shape of `coverage_files_build.py` wrote
  a 142,709,717-byte summary because it carried every file run of every
  probe; that was the reason `FILE_RUN_CAP` exists, and it is stated on the
  artifact rather than hidden (§2.2.2).

---

# 3. Paint timings, per language

## 3.1 The measurement and its honest caveat

Two harnesses exist and only one of them can time anything.

- **Interactive Chrome pane**, real timers, a visible page: the numbers
  below. Each is `performance.now()` around the canvas draw, logged by the
  page itself as `[pane4] <lang> PAINT …`.
- **Headless Chrome with `--virtual-time-budget`**, which is how the PNG
  files were produced: it virtualises the clock, so every headless run
  prints `PAINT 0.0 ms`. Those runs are used for IMAGES ONLY and none of
  their timings is quoted as a measurement.

## 3.2 The numbers

| compiler | graph behind the drawing | boxes | wires drawn / inter-file pairs | paint, first draw | paint, redraw |
|---|---|---|---|---|---|
| go | 10,393 nodes, 63,797 edges, 81 files | 81 | 331 / 331 | 5.9–13.8 ms | 0.6–1.3 ms |
| rust | 13,446 nodes, 60,382 edges, 134 files | 134 | 1,022 / 1,022 | 2.9–3.8 ms | 1.1–1.6 ms |
| swift | 71,106 nodes, 192,655 edges, 230 files | 230 | 1,500 / 1,909 | 3.5 ms | 2.1 ms |
| cpp | 112,364 nodes, 386,065 edges, 269 files | 330 | 1,500 / 2,095 | 2.8–3.5 ms | 1.1–2.2 ms |
| go, one file expanded (`amd64/ssa.go`) | same graph | 69 definitions | intra-file def edges | 3.2 ms | — |

- **LITERAL:** these are the `[pane4] … PAINT …` console lines read out of
  the interactive pane; the full transcript of one sweep is in §3.3.
- **GLOSS:** the collapse-to-file-level rule is what makes this usable. The
  cpp drawing costs 2 ms because it is **330 boxes**, not 112,364 nodes; the
  graph behind it is never in the page at all. `MAX_EDGES_DRAWN = 1500`
  caps the wires and the page prints "1,500 wires drawn of 2,095 inter-file
  edge pairs" so the cap is read, not assumed.

## 3.3 The transcript

```
[pane4] go PAINT 6.3 ms — file level, 81 boxes and 331 wires drawn of 331 inter-file edge pairs; the graph behind them is 10,393 nodes and 63,797 edges in 81 files
[pane4] cpp PAINT 3.2 ms — file level, 330 boxes and 1,500 wires drawn of 2,095 inter-file edge pairs; the graph behind them is 112,364 nodes and 386,065 edges in 269 files
[pane4] cpp PAINT 2.1 ms — file level, 330 boxes and 1,500 wires drawn of 2,095 inter-file edge pairs; the graph behind them is 112,364 nodes and 386,065 edges in 269 files
[pane4] rust PAINT 2.9 ms — file level, 134 boxes and 1,022 wires drawn of 1,022 inter-file edge pairs; the graph behind them is 13,446 nodes and 60,382 edges in 134 files
[pane4] rust PAINT 1.6 ms — file level, 134 boxes and 1,022 wires drawn of 1,022 inter-file edge pairs; the graph behind them is 13,446 nodes and 60,382 edges in 134 files
[pane4] swift PAINT 3.5 ms — file level, 230 boxes and 1,500 wires drawn of 1,909 inter-file edge pairs; the graph behind them is 71,106 nodes and 192,655 edges in 230 files
[pane4] swift PAINT 2.1 ms — file level, 230 boxes and 1,500 wires drawn of 1,909 inter-file edge pairs; the graph behind them is 71,106 nodes and 192,655 edges in 230 files
[pane4] cpp PAINT 1.1 ms — file level, 330 boxes and 1,500 wires drawn of 2,095 inter-file edge pairs; the graph behind them is 112,364 nodes and 386,065 edges in 269 files
[pane4] go PAINT 3.2 ms — one file expanded, 69 boxes and 0 wires drawn; the graph behind them is 10,393 nodes and 63,797 edges in 81 files
```

## 3.4 A number the brief carried that the graph on disk does not

The brief asks the drawing to stay usable at 174,159 go nodes. The go graph
task 71 wrote holds **10,393** nodes (`graph_go.json`, `counts.nodes`); the
174,159 figure is lap one's graph, `graph_go_lapone.json` (126,304,023 bytes,
still on disk), which the graph CORE's settled rule quotes. The largest
graph pane 4 actually draws is therefore **cpp at 112,364 nodes**, and it
paints in 1.1–3.5 ms. This is stated rather than quietly reconciled.

---

# 4. What the pane draws, part by part

## 4.1 (a) The static structure

- One box per source file, side scaled by `sqrt(nodes)`, so `ssa/rewrite.go`
  is a large box and `ssa/cpufeatures.go` a small one.
- **Grouped by directory** (the default, and the layout the brief prefers):
  files are packed into a labelled band per directory —
  `internal/ssa`, `internal/ssagen`, `internal/amd64`, `internal/abi` for
  go. Screenshot `screens/log_181/pane4_go.png`.
- **Force** is offered beside it: 220 iterations of repulsion plus
  attraction along the inter-file edges, then scaled to fit. Screenshot
  `screens/log_181/pane4_go_force.png`.
- Autofit runs ONCE per layout and never again; any wheel or drag sets
  `touched` and the view becomes the person's. This is the rule the fuzz
  explorer settled on (`CLAUDE.md`, explorer requirements), reused here for
  the same reason.
- **Expand on click.** Clicking `src/cmd/compile/internal/ssagen/ssa.go`
  reads `graph_go_defs.json` once and redraws that ONE file as its
  definitions, with the definition-to-definition edges that stay inside it.
  Screenshot `screens/log_181/pane4_go_expanded.png`. "collapse to file
  level" returns.

## 4.2 (b) The dynamic structure

- The probe selector is keyed by unit id and lists every probe that HAS a
  diary — 590 of them — with its event count: `op_103 — 18,270 events,
  10,008 file steps`. A unit id with no diary is refused by name on the
  page rather than silently ignored.
- Choosing one does the ranged read of §2.3, then the file-level path is
  walked by a step slider or the "play the diary path" button (90 ms per
  step). The current file is filled bright with a white ring, the files
  already walked carry a blue ring, and the last 24 steps are drawn as
  lines that brighten toward the present — so ORDER is drawn as direction
  and not only as colour.
- The step readout is `step 181 of 10,008 —
  src/cmd/compile/internal/ssagen/ssa.go`. Screenshot
  `screens/log_181/pane4_go_diary_path.png`.
- Inside an expanded file the same path lights that file's DEFINITIONS in
  order, up to the current step: the events are `file:line` and the
  declaration line is the join key task 72 recorded
  (`coverage_go2.json.provenance.join_key`), so a def whose `start_line` is
  on the path is ringed.

## 4.3 (c) Coverage

- Every file box is shaded by how many of the 590 probes entered it, on a
  pale-to-warm scale; a file with instrumented bodies that no probe entered
  is a distinct dark red; a file with no instrumented body at all is the
  flat "named frontier" slate.
- Three tables under the canvas, all counts over the artifact:
  - **15 files no probe ever entered**, with their instrumented-body counts
    — `ssa/magic.go` 40, `ssa/merge_conditional_branches.go` 30,
    `ssa/print.go` 13, `ssa/opGen.go` 11, `ssa/loopreschedchecks.go` 7,
    `ssagen/nowb.go` 6, `ssa/check.go` 4, `ssa/cpufeatures.go` 3,
    `ssa/uses.go` 3, `ssa/rewritetern.go` 2, `amd64/simdssa.go` 1,
    `ssa/downward_counting_loop.go` 1, `ssagen/simdAMD64intrinsics.go` 1,
    `ssagen/simdARM64intrinsics.go` 1, `ssagen/simdWasmintrinsics.go` 1.
  - **Every file, by how much of it the corpus reaches** — instrumented,
    visited, never, probes entering. `ssa/rewrite.go` 239 / 46 / 193;
    `ssagen/ssa.go` 199 / 115 / 84; `amd64/ssa.go` 65 / 12 / 53.
  - **The 810 never-visited bodies, by file**, with names and lines, files
    no probe entered marked ◆ and sorted first. Screenshot
    `screens/log_181/pane4_go_never_visited.png`.
- The pane prints, in the same card, that 325 definitions carry no entry
  hook and are a NAMED FRONTIER, not never-visited nodes — the graph CORE's
  settled rule, on the page rather than only in the tree.

## 4.4 The brief's "14 never-entered files" is 15

The brief names 14. The count over `coverage_go_files.json` is **15**, and
the fifteen are listed in §4.3. The number is computed on the page from the
artifact every time it opens, so if the artifact changes the page changes;
no count on this page is typed in.

---

# 5. The guards, pasted, one process each

## 5.1 The data guard, over the nine artifacts task 73 emits

```
$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
    ../compiler_graph/graph_go_files.json ../compiler_graph/graph_cpp_files.json \
    ../compiler_graph/graph_rust_files.json ../compiler_graph/graph_swift_files.json \
    ../compiler_graph/graph_go_defs.json ../compiler_graph/graph_cpp_defs.json \
    ../compiler_graph/graph_rust_defs.json ../compiler_graph/graph_swift_defs.json \
    ../compiler_graph/coverage_go_files.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS graph_go_files.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_cpp_files.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_rust_files.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_swift_files.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_go_defs.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_cpp_defs.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_rust_defs.json -- no operator token in any key, grouping, pairing or row structure
PASS graph_swift_defs.json -- no operator token in any key, grouping, pairing or row structure
PASS coverage_go_files.json -- no operator token in any key, grouping, pairing or row structure
EXIT=0
```

```
$ /tmp/reconnect_venv/bin/python3 check_dashboard_js_no_spelling.py dashboard_pane4.js > g.txt; grep -c exempt g.txt
0
```

Both builders now run this guard over their own output IN THEIR OWN PROCESS
and DELETE that output on failure (`refuse_on_spelling`), which is the
mechanical guard the ban requires of every stage that groups or pairs.

### 5.1.1 The guard caught a real violation, and the fix was structural

The first cut wrote a definition as a positional list, `[id, label, start,
end]`. The guard refused:

```
FAIL graph_rust_defs.json -- 57 spelling-keyed place(s)
     $.by_file.compiler/rustc_codegen_llvm/src/back/lto.rs[11][1]
         list element is the bare operator token 'new'
FAIL graph_swift_defs.json -- 15 spelling-keyed place(s)
     $.by_file.lib/IRGen/GenEnum.cpp[43][1]
         list element is the bare operator token 'consume'
```

- **LITERAL:** rustc has 57 definitions named `new` and swiftc has
  definitions named `consume` and `as`; `new`, `consume` and `as` are all in
  the 91-token operator inventory.
- **GLOSS:** a bare list element could be a key, so the guard is right to
  refuse it. The fix is the ban's own shape: the record became an OBJECT
  that identifies one unit — `{"id", "language", "label", "start_line",
  "end_line"}` — so the name is a display label on that member and nothing
  else. No exemption was added and the guard was not modified.

## 5.2 The page-code guard

```
$ /tmp/reconnect_venv/bin/python3 check_dashboard_js_no_spelling.py dashboard_pane4.js
operator inventory: 91 tokens read from probe_manifest_*.json
     dashboard_pane4.js:180  '/' -- the artifacts' own unit-id separator, as in c/op_100
     dashboard_pane4.js:630  '/' -- the artifacts' own unit-id separator, as in c/op_100
     dashboard_pane4.js:630  '/' -- the artifacts' own unit-id separator, as in c/op_100
     dashboard_pane4.js:702  '/' -- the artifacts' own unit-id separator, as in c/op_100
PASS dashboard_pane4.js -- no operator token is written as a literal, so none can be a key (4 named coincidences above)
EXIT=0
```

An earlier draft used `"?"` as the placeholder for a definition with no
label; `?` is an operator token, so the guard failed it. It is now
`"(unnamed)"`.

## 5.3 The spelling-ban test RUN, not asserted

Pane 4 keys nothing by an operator token, so `?labels=glyph` must not change
a single character it draws. Measured, same page, same probe, same step,
flag off then on, with the clock and the paint figure masked:

```
off:  {"len": 45277, "hash": 22110881}
on:   {"len": 45277, "hash": 22110881, "glyphModeOn": true}
```

- **LITERAL:** `document.querySelector('#t-graph4').innerText` with
  `opened at HH:MM:SS`, `PAINT … ms` and `read in … ms` masked, hashed with
  a rolling 31-multiplier; `DashboardJoin.glyphMode()` returned `true` on
  the second run.
- **GLOSS:** character for character identical. Screenshot of the glyph run:
  `screens/log_181/pane4_go_labels_glyph.png`.

---

# 6. The concurrency rule, honoured

Tasks 69, 70 and 76 were editing the dashboard at the same time.

- **All pane-4 code is in one new module**, `dashboard_pane4.js`. It wraps
  `DashboardJoin.mount`, lets every existing pane draw exactly as it did,
  then appends one nav button and one section.
- **`dashboard.html` gained ONE line**, appended after the existing script
  tags, the file re-read immediately before the edit:
  `<script src="dashboard_pane4.js"></script>`.
- **`dashboard_join.js` was not touched at all.** No hook was needed: the
  module reaches the folder through `source.graphDir`, which
  `dashboard_loader.js` already sets.
- **`viewer_build.py` gained an additive block** at the same seam panes 1,
  2 and 3 use, embedding `dashboard_pane4.js` verbatim plus the four
  file-level graph summaries and the go coverage summary (2,873,445 bytes),
  because a snapshot has no folder to read them from.

Proof that both embeddings are verbatim, after the rebuild:

```
dashboard_join.js verbatim in snapshot: True 43902 bytes
dashboard_pane4.js verbatim in snapshot: True 49121 bytes
```

The snapshot build line:

```
PASS dashboard_snapshot_data.json -- no operator token in any key, grouping, pairing or row structure
pane 4: 4 file-level graph summaries and 1 go coverage embedded (2873445 bytes)
wrote …/dashboard_snapshot.html  (22.6 MB, 2456 unit bodies carried, 31078 units counted, 1019 files read)
the join embedded above is dashboard_join.js, verbatim (43902 bytes)
```

The snapshot was then opened from `file://` in headless Chrome and pane 4
drew: `[pane4] go PAINT 14.4 ms — file level, 81 boxes and 331 wires drawn
of 331 inter-file edge pairs`. Screenshot
`screens/log_181/pane4_snapshot_go.png`. In the snapshot the pane draws the
file level and says that expanding a file and reading a probe's full path
need the live page — the per-definition artifacts (7.2 MB) and the 515 MB
join are not carried.

---

# 7. A difference between two of this line's own numbers, named

`t72/inject_report.json` reads `"targets_read": 1549, "instrumented": 1549,
"skipped": 0`, and `t72/diary_targets_all.json` holds 1,549 rows.
`coverage_go2.json` reads `"population_instrumented": 1534`. Fifteen bodies
are instrumented according to the injector and not according to the join.

- The pane prints **1,534**, because that is the population the visited /
  never sets were measured against.
- `coverage_files_build.py` carries the recount beside it as
  `instrumented_bodies_recounted_here: 1549`, so the difference is on the
  artifact rather than lost.
- Which is right is not settled here. It belongs to the graph node's next
  lap and is recorded in that node's PROGRESS as a frontier.

---

# 8. Complete file inventory

## 8.1 New files

| path | bytes |
|---|---|
| `Research/op_pipeline/dashboard_pane4.js` | 49,175 |
| `Research/op_pipeline/dashboard_pane4_harness.html` (test rig only) | 3,861 |
| `Research/compiler_graph/graph_files_build.py` | 12,922 |
| `Research/compiler_graph/coverage_files_build.py` | 13,705 |
| `Research/compiler_graph/graph_go_files.json` | 40,966 |
| `Research/compiler_graph/graph_rust_files.json` | 84,629 |
| `Research/compiler_graph/graph_swift_files.json` | 147,669 |
| `Research/compiler_graph/graph_cpp_files.json` | 183,876 |
| `Research/compiler_graph/graph_go_defs.json` | 567,447 |
| `Research/compiler_graph/graph_rust_defs.json` | 913,267 |
| `Research/compiler_graph/graph_swift_defs.json` | 2,392,393 |
| `Research/compiler_graph/graph_cpp_defs.json` | 3,345,141 |
| `Research/compiler_graph/coverage_go_files.json` | 2,597,323 |
| `DevComms/log_181_task73_pane4_coverage_view.md` | this file |

## 8.2 Files changed

| path | change |
|---|---|
| `Research/op_pipeline/dashboard.html` | ONE appended script tag |
| `Research/op_pipeline/viewer_build.py` | one additive embed block + `PANE4` constant |
| `Research/op_pipeline/dashboard_snapshot.html` | rebuilt, 19.5 MB → 22.6 MB |
| `Research/op_pipeline/dashboard_snapshot_data.json` | rebuilt |
| `.gitignore` | eight negation rules so the summaries are TRACKED, with the regeneration commands |
| `…/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md` | `coverage_view` realization rows; one new settled rule (a pane may never load a whole artifact) |
| `…/node_0_3_5_10_dashboard/PROGRESS.md` | three entries |
| `…/node_0_3_5_9_graph/CORE_0_3_5_9_graph.md` | two realization rows; the bounded-memory rule widened from the miner to every reader |
| `…/node_0_3_5_9_graph/PROGRESS.md` | two entries |

## 8.3 Screenshots, `DevComms/screens/log_181/`

| file | what it shows |
|---|---|
| `pane4_go.png` | go, static structure grouped by directory, shaded by coverage |
| `pane4_cpp.png` | cpp, static structure, (b) and (c) NOT MEASURED with the cost page named |
| `pane4_rust.png` | rust, same |
| `pane4_swift.png` | swift, same |
| `pane4_go_force.png` | go, the force layout |
| `pane4_go_diary_path.png` | probe `op_103`, step 181 of 10,008, the path lit in order |
| `pane4_go_expanded.png` | one file expanded into its definitions |
| `pane4_go_never_visited.png` | the coverage tables: 15 never-entered files, every file's reach, the 810 bodies |
| `pane4_go_labels_glyph.png` | the same page with `?labels=glyph` |
| `pane4_snapshot_go.png` | pane 4 inside `dashboard_snapshot.html`, opened from `file://` |

## 8.4 Why the summaries are tracked and the graphs are not

`.gitignore` already ignored `Research/compiler_graph/graph_<lang>*.json`
(608 MB for four) and `coverage_go2.json` (515 MB) as regenerable output
over GitHub's limits. That rule also swallowed the new summaries, and a
clone with no summaries has NO PANE 4 at all — so eight negation rules were
added, with the two regeneration commands written beside them. Every
tracked summary is between 41 KB and 3.3 MB.

---

# 9. Two lists

## 9.1 Decided, recorded for audit

- The file-level summary artifacts and the byte-range read are the shape by
  which the page reads a graph too large to open; recorded as a settled
  rule on both COREs with its provenance (§2).
- `FILE_RUN_CAP = 600` for the summary's preview path, stated on the
  artifact, with the full path one ranged read away (§2.2.2).
- `MAX_EDGES_DRAWN = 1500` for the wiring diagram, printed on the page
  beside the total (§3.2).
- A definition record is an object with `id`, `language` and `label`, not a
  positional list, so the guard can see that a name is a display label
  (§5.1.1).
- The nav button is labelled "compiler graph & coverage — pane 4"; the
  existing panes were not renumbered, since three other tasks were editing
  the same page.

## 9.2 Awaiting the owner

- Nothing. The one open measurement — the 1,534 / 1,549 difference — is a
  frontier on the graph node, not a decision.
