---
id: hq.research.compiler_graph.dashboard
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (module), rule
node:
    name: dashboard
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_10_dashboard/CORE_0_3_1_10_dashboard.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: unit_viewer
      designation: code (function)
      realize: false
    - name: selector
      designation: code (function)
      realize: false
    - name: opcode_index
      designation: code (function)
      realize: false
    - name: coverage_view
      designation: code (function)
      realize: false
    - name: stats
      designation: code (function)
      realize: false
    - name: loader
      designation: code (function)
      realize: false
    - name: chronology
      designation: code (function)
      realize: false
---

# CORE 0_3_1_10 — dashboard

## metadata

- **id:** hq.research.compiler_graph.dashboard
- **level:** 3
- **status:** draft
- **designation:** code (module), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- unit_viewer — code (function) *(realize: false)*
- selector — code (function) *(realize: false)*
- opcode_index — code (function) *(realize: false)*
- coverage_view — code (function) *(realize: false)*
- stats — code (function) *(realize: false)*
- loader — code (function) *(realize: false)*
- chronology — code (function) *(realize: false)*

## definition

The interactive page that reads the current artifacts and shows the
research as it stands, so that the state of the line is inspected
rather than reported. the owner, 2026-09-03: "we will work to establish an
undeniable means of communication about this project that will
update mechanically." Five panes, numbered as the owner numbered them:
(1) an arch-unit viewer with selectable representations; (2) a
selector — random, and language → operator → type signature;
(3) an index from every arch opcode to the operators and signatures
it appears in; (4) per-language compiler graph with probe coverage;
and (5) stats. It is opened by double-click, runs no server, and
reads the artifacts live.

**The chronology is not a pane. It is the OUTER CONTROLLER** (the owner,
2026-09-04, correcting this CORE): "the chronology is the outer
controller. regardless of what tab im in, i can select a moment in
the chronology (that is always visible at the top), and it shows what
that moment in the chronology looked like in that tab but it also
updates all the tabs for that time." So it is always on screen, above
the panes, in every tab; choosing a moment sets ONE selected moment
for the whole page; and every pane re-reads itself as of that moment,
not the stats pane alone. The count "five panes" in this CORE was
always right — the chronology had been miscounted into the tab bar,
which is the same defect log_188 saw from the other end when the tab
bar carried more entries than the CORE numbers. Its own reason is
unchanged (the owner, 2026-09-03: "a chronology based on vcs so i can step
through the history to see progress").

## design

```
module dashboard
	methods:
		loader
			"""
			reads the artifact folder in the
			browser: the page asks once for the
			folder (File System Access API),
			then reads canon39_*, term65_store,
			the_pool5, probe_manifest*, census,
			families, and the graph/diary files
			directly — no server, no terminal,
			no build step. The JOIN logic of
			viewer_build.py is ported to the
			page. Fallback: the embedded-data
			build (viewer_build.py) for a
			shareable snapshot
			"""
		unit_viewer
			"""
			one unit, modes: high-level source /
			raw extracted / context / canonical /
			ledger / z3 + normalized / rendered
			back / pool entry / verdicts
			"""
		selector
			"""
			random (seeded, in the URL); menus
			language -> operator -> signature;
			free-text by unit id
			"""
		opcode_index
			"""
			mnem -> lang.operator.signature
			groups -> units, from ledger
			producers; every opcode, seed or not
			"""
		coverage_view
			"""
			per language: the graph as a wiring
			diagram (static structure), the
			diary path of a chosen probe
			(dynamic), and the union of visited
			nodes over the corpus (coverage);
			says "not measured" where it is not
			"""
		stats
			"""
			per-language table; totals:
			extracted / distinct / dominant
			operators; pool, census, term states
			"""
		chronology
			"""
			THE OUTER CONTROLLER, not a pane.
			Always visible at the top, in every
			tab. A MOMENT IS A COMMIT. The scale
			is the repository's own history --
			`git log` -- unfiltered and
			ungrouped. No commit is selected as
			more important than another by
			reading its message, and no
			project's vocabulary ("round",
			"banked", "lap") appears in the
			mechanism: a general dashboard
			cannot know those words. Where a
			coarser scale than every commit is
			needed, the marks come from what
			version control itself carries --
			tags, dates, merges -- never from
			text a writer chose. It
			holds ONE selected moment for the
			whole page; every pane renders
			itself as of that moment, and a
			pane's own view of that moment is
			what its tab shows. Choosing a
			moment therefore updates all five
			panes at once, not the stats pane
			alone. At each step a pane is
			recomputed from the artifacts git
			holds at that commit — never from a
			remembered number — alongside that
			round's logs and its bank
			message. Where an artifact was not
			tracked at that commit (pool1,
			18 MB, was not), the pane DRAWS ITS
			REFUSAL there and names the file it
			would need. The fallback to a bank
			message's own count line, labelled
			as testimony, is RETIRED with the
			mechanism it rested on -- a bank
			message is text a writer chose, and
			the settled rule above forbids the
			chronology reading such text.
			Source: `git log` at render time.
			chronology.json and
			chronology_build.py stay on disk as
			superseded records
			"""
```

## settled rules

- **Reads the artifacts, never a hand-written summary.** Every number
  on the page is a count over a file on disk at open time. Decision:
  the owner, 2026-09-03 ("update mechanically").
- **No server, no terminal.** Double-click opens it; the page asks
  for the folder once. Decision: the owner, 2026-09-03 ("i dont want to run
  a server or use a terminal command").
- **Spelling appears as a label on an entry keyed by unit identity**;
  the menus are built from that index and nothing compares by token.
  The test: replace every label with a glyph and every pane still
  works. Decision: THE SPELLING BAN, applied here.
- **A pane with no data says so**, on the page, with the population
  it would need. Decision: this CORE, 2026-09-03 (the coverage pane
  today).
- **A pane may never load a whole artifact into memory.** Where an artifact
  is larger than the page can hold, a SUMMARY is built once in python by a
  streaming builder and the page reads the summary; a detail the summary
  cannot carry is fetched by a RANGED READ into the large file, at byte
  offsets the summary carries. The four compiler graphs total 608 MB and the
  coverage join is 515 MB, so pane 4 reads `graph_<lang>_files.json`,
  `graph_<lang>_defs.json` and `coverage_go_files.json`, and slices one
  probe's path out of `coverage_go2.json`. Decision: this CORE, 2026-09-03,
  from task 73, taking the rule the graph CORE already states for its own
  miner and applying it to the page.
- **PRIORITY ORDER, set by the owner 2026-09-04.** (1) the chronology as the
  outer controller; (2) pane 4 drawn as a visual compiler graph. Nothing
  else in this node outranks them. the owner: "put dashboard chronology as the
  top priority... the dashboard is supposed to have a visual compiler
  graph as ive described several times and yet tab 4 'coverage' remains
  NOT that. thats also the next priority below the chronology. the
  chronology also works on the coverage." The two meet: the coverage
  pane is one of the five the moment applies to, so the graph is drawn
  as it stood at the selected moment.
- **Pane 4 cannot exist before the object it draws does.** The
  compiler graph the owner specified -- structural connections, dynamic
  connections, and the connections belonging to each operator's traced
  variant -- is not complete, and until it is there is nothing for
  this pane to show. the owner, 2026-09-04: "it reads a completed fucking
  compiler graph... once its completed, then we can see it through
  time. until it exists, theres nothing to fucking see." The
  coordinator's suggestion that pane 4 gain a past by banking a small
  per-commit summary is WITHDRAWN: it manufactured something to
  display in place of the missing deliverable. Priority 2 is
  therefore completing the graph (node 0_3_5_9), not rendering a pane;
  the drawing follows, and the moment then applies to it as to any
  other pane.
- **Pane 4 is a DRAWING, not a table of counts.** The requirement is
  unchanged since log_172 task 73 — files as boxes, functions as nodes,
  call/read/write edges, collapsed to file level and expanded on click.
  The defect, named 2026-09-04: `dashboard_ouro.py`'s `pane_coverage`
  emits four tables and a `<pre>` list and draws nothing, while the
  drawing exists only in `dashboard_pane4.js`, the route the owner does not
  use. A pane that reports the graph's node and edge COUNTS does not
  satisfy a requirement to show the graph. Provenance: the owner, 2026-09-04,
  having asked "several times"; the open question was raised in log_184
  and never carried to him, which is the process failure underneath.
  **CLOSED 2026-09-04 by task 93** (log_198): `pane_coverage` now emits
  three inline-SVG figures over one layout that follows the compiler's
  own directories and files — basic structure, dynamic connections, and
  the traced directional connections, which are the owner's own three words.
  The realization row above carries what was measured.
- **The chronology is version control, and nothing curates it.**
  A moment is a commit. Which commits exist as moments is a fact of the
  repository, never a judgement made by whoever wrote the commit
  messages. Decision: the owner, 2026-09-04: "i said vcs chronology. i dont
  want you to have any say in how it updates... because i cant trust
  you." THE DEFECT THIS RETIRES, named exactly: `chronology_build.py`
  line 163 ran `git log --grep=banked -i` and line 155 matched
  `round\s+(\d+)\s+bank`, so the chronology's steps existed because
  the coordinator had written the word "banked" into a commit message.
  The rounds were the mechanism and version control was only its
  substrate. The repository holds 1,309 commits and 0 tags.
- **This dashboard is becoming general-purpose.** the owner, 2026-09-04:
  "plans are now in place to convert this to a general purpose
  PlanPlan dashboard design. so think abstractly." Every mechanism in
  this node is therefore written so that it holds for a project that
  is not this one: the chronology reads version control, a pane reads
  artifacts by path, and nothing consults a research vocabulary.
  Anything that can only work for PseudoCoup is a defect in this node,
  not a feature of it.
- **One moment, held outside the panes, applied to all of them.** The
  chronology is not one pane's control and never a tab. It sits above
  the tab bar, visible in every tab, and the moment it holds is the
  page's, not any pane's. Choosing a moment re-renders every pane as
  of that moment; the tab in view shows that pane's version of it.
  A pane may not carry its own separate time. Decision: the owner,
  2026-09-04 ("the chronology is the outer controller... it shows
  what that moment in the chronology looked like in that tab but it
  also updates all the tabs for that time").
- **A pane that cannot be recomputed at a moment says so at that
  moment**, with what it would need, exactly as an empty pane does
  today. An untracked artifact is exactly such a case, and the pane
  says so rather than standing a remembered number in its place;
  extending the moment to all five panes extends the obligation to
  all five. Decision: this
  CORE, 2026-09-04, following from the rule above.
- **History is recomputed, not remembered.** Each chronology step
  re-derives its numbers from the artifacts at that commit; a step
  that cannot (untracked artifact) draws its refusal and names what it
  would need. AMENDED 2026-09-04: it does NOT stand a commit message's
  own count line in place of the number, which was the 2026-09-03
  form. A message is text a writer chose, and no part of this node may
  rest on that. Decision: this CORE, 2026-09-03, applying "reads the
  artifacts, never a hand-written summary" to the past.
- **Names of the panes and the node are provisional**; the owner's to
  change.
- **A SECOND ROUTE MAY RENDER THE SAME PANES, AND NEITHER ROUTE OWNS THE
  JOIN.** `dashboard.html` reads the folder in an ordinary browser and
  joins in JavaScript; `dashboard_ouro.html` is rendered by python inside
  `~/Programming/Ourobrowser`, whose scripting language is python. The
  two coexist: neither edits or retires the other, and each states which
  it is on its own page. The condition that makes a second route legal
  is that it ADDS NO THIRD JOIN — the python page imports the python
  join `viewer_build.py` already holds rather than restating it.
  Decision: this CORE, 2026-09-03, from the owner's own request quoted in
  log_183 task 77 — "the browser allows python to be run locally
  natively within the browser. id like to see the dashboard written to
  run in it". Evidence: log_184.

## realization (what exists on disk, 2026-09-03, after task 68)

| part | current file | status |
|---|---|---|
| the live page | `Research/op_pipeline/dashboard.html` — opens by double-click, asks once for the folder, reads the artifacts in the browser | **done** (task 68) |
| `loader` | `Research/op_pipeline/dashboard_loader.js` — File System Access API, IndexedDB for the remembered folder, prefix and tail slices for the first paint, unit bodies on demand | **done** (task 68) |
| the one join, and panes 1/2/3/4/5 | `Research/op_pipeline/dashboard_join.js` — loaded by the live page with a script tag and embedded VERBATIM in the snapshot; the two proved byte-identical by diff | **done** (task 68) |
| the snapshot (embedded data, shareable) | `Research/op_pipeline/viewer_build.py` + `viewer_template.html` -> `dashboard_snapshot.html` (19.5 MB; 2,456 unit bodies carried, all 31,078 counted) | **done** (task 68) |
| the guard over what the builder emits | `dashboard_snapshot_data.json`, walked by the unmodified `check_no_spelling_keys.py`; the builder refuses its own output on failure | **done** (task 68) |
| the guard over the page's own code | `Research/op_pipeline/check_dashboard_js_no_spelling.py` — the same operator inventory, over javascript string literals | **done** (task 68) |
| `unit_viewer` mode "context" | `Research/op_pipeline/dashboard_pane1.js` (`contextBody`) reads `canon39_context.json` (task 69's sidecar, 329 units / 524 sites / 300 with bytes) and renders the rip-relative constant bytes per unit | **done** (task 69, log_178) — STALE ROW CORRECTED 2026-09-04 (round-15 bank): task 69 delivered `arch_unit.context`'s data (`canon39_context.json`) and wired it into pane 1 the same round; this row had never been updated off **planned** |
| panes 2 and 3 over the full population | `Research/op_pipeline/dashboard_pane23.js` — the selector and the arch opcode index over all 31,078 units; 31,067 rows carry a type signature and the 11 that do not are the interpreter handlers, which have no probe; 3,390 signatures, 131 operator groups, 9 languages, 162 arch opcodes, 151,279 (language, operator group, signature) groups | **done** (task 70) |
| `coverage_view`, THE PYTHON ROUTE, DRAWN | `Research/op_pipeline/dashboard_graph_draw.py` + `pane_coverage` in `dashboard_ouro.py` — three figures over ONE structure-following layout: (1) basic structure, directory bands and file boxes in path order, a box's place a function of its path; (2) dynamic connections, the same boxes filled by the share of instrumented bodies entered, hollow where no probe entered, hatched where nothing was instrumented; (3) the traced directional connections, in aggregate / for one probe / for one operator traced variant. Inline SVG, NO JavaScript (`<script` 0 in what the pane emits); `graph_cpp.json` read for its first 256 KB and no more, `coverage_go2.json` never opened; 114.1 MB peak over all four compilers against the 1,500 MB cap. rust and swift draw their structure and REFUSE figures 2 and 3 by name; java, cpython, php and ruby are drawn as `no graph`. The moment reaches the graphs' second repository by its own timestamp (`GraphFolder`) | **done** (task 93, log_198) — this closes the defect named below |
| `coverage_view`, the JavaScript route | `Research/op_pipeline/dashboard_pane4.js` — per compiler, the region as a wiring diagram (file boxes, directory-grouped or force, collapsed to file level, one file expanded on click into its definitions), a probe's diary path lit in order with a step slider, and the corpus's coverage shading with the never-visited set listed; says "not measured" for every compiler but go and names task 72's cost page | **done** (task 73). The earlier head-slice row (task 68) stands as the pane's population line |
| what `coverage_view` reads, and what it never opens | `graph_<lang>_files.json` (41 KB–184 KB), `graph_<lang>_defs.json` (0.6–3.3 MB, only on expanding a file), `coverage_go_files.json` (2.6 MB), and for a chosen probe ONE `Blob.slice` of `coverage_go2.json` (929,634 bytes of 515,160,866 for `op_103`). `graph_cpp.json` (331 MB) and `coverage_go2.json` (515 MB) are never opened whole | **done** (task 73) |
| `chronology` | `Research/op_pipeline/chronology_build.py` -> `chronology.json` (tracked, 56,904 bytes, 38 steps) + `Research/op_pipeline/dashboard_pane6.js`, added to the live page by one script tag and to the snapshot by `viewer_build.py` | **superseded** (task 86 — its steps existed because a person wrote "banked" into a commit message; the program carries a SUPERSEDED banner and both it and `chronology.json` stay on disk as records. The JavaScript route still reads `chronology.json`) |
| the chronology's own population | **superseded** by task 86. It was: 12 commits matching `git log --grep=banked -i`, naming 8 distinct rounds, plus the last commit of each of 30 days — a population produced by a coordinator's own commit messages |
| `stats` | `Research/op_pipeline/dashboard_pane5.js`, added to the live page by one script tag and to the snapshot by `viewer_build.py`; the four term states over the full population (proved 26,594 / disproved-withdrawn 3,134 / undecided 285 / no term 419 of 30,432 records, `audit65.json`'s `term65` tally) and the census's top causes read from the HIGHEST-numbered `name_census*.json` present on disk (`name_census6.json`, by number, not a hard-coded name — the fix for the task-76 finding that pane 4/stats read `name_census5.json` while a higher generation existed), against the pool's own population line (1,831 entries / 30,432 members, `the_pool5.json` summary) | **done** (task 74) |
| `stats`, THE PYTHON ROUTE — TWO LABELLED HALVES, AND EVERY ROW EXPLAINED | `Research/op_pipeline/dashboard_stats.py` (new) + `pane_stats`/`stats_stored`/`stats_computed`/`explained_table` in `dashboard_ouro.py`; CSS only in `dashboard_ouro.html`. The pane draws `read from a stored summary` (the pool, the term audit, the census) and `counted at render time` (two bounded walks over the artifacts). Measured off the rendered page at its own half marker: **136 rows, 36 stored / 100 computed, 17 tables, 136 `?` controls, 0 unexplained**. The explanations are DATA — `MEANINGS`, 46 records keyed per row, each carrying what is counted / out of what / which file and whether stored or counted / what it does NOT mean — and a row whose key has no record is drawn as UNEXPLAINED on the page. That marker FIRED and was right: nine rows at two 2026-09-03 commits, where the pool generation is `the_pool3` and spells the same measurements under other names. NO JAVASCRIPT: the `?` is a `<details>` element and `<script` in what the pane emits is 0. Render 1.0–1.3 s / 41.7–44.2 MB; the real Ourobrowser over the comparable pass **599.2 MB** against task 86's 566.4 MB. `git diff` over `dashboard.html`, every `dashboard_pane*.js` and `~/Programming/Ourobrowser` is 0 lines | **done** (task 98, log_203) |
| the python page, all six panes | `Research/op_pipeline/dashboard_ouro.html` — no JavaScript at all; one `<script type="text/python">` block imports the renderer, emits the first paint, and defines the four functions its clicks call | **superseded** (task 77 — the six-tab form; task 85 replaced the tab bar with five and lifted the chronology above it) |
| the chronology AS THE OUTER CONTROLLER | `Research/op_pipeline/dashboard_ouro.py` — `Moment`, `NotAtThisMoment`, `set_moment`, `moment_change`, `chronology_bar`; `dashboard_ouro.html` gains one click function, `ouro_moment`, and the controller's styling. The moment lives in `STATE["moment_key"]`, ABOVE every pane; `frame()` draws `chronology_bar` before `tab_bar`, so no pane can be drawn without it. The tab bar numbers the CORE's FIVE panes. Measured over 5 panes × 40 moments = **200 renders, 0 errors**: the chronology is drawn on 200/200 and is above the tab bar on 200/200, and the tab bar carries 5 entries on 200/200 (closing log_188's finding). Only the JavaScript route keeps `dashboard_pane6.js`; `git diff` over `dashboard.html` and every `dashboard_pane*.js` is 0 lines | **done** (task 85) |
| history RECOMPUTED at a past moment, not remembered | at a moment other than now, every read goes through `git ls-tree -r -l <commit>` (once per moment, cached) and `git cat-file --batch` (one process per moment) — nothing is checked out and no number is taken from `chronology.json`, which is no longer read by this page at all (task 86). Measured: at 2026-09-03 `f6856895` the index rebuilds **31,078 units in 1.8 s** from that commit's own blobs, and pane 5 reads `the_pool4.json` — a DIFFERENT generation from today's `the_pool5.json`, **1,961 entries / 30,432 members** against today's 1,831 / 30,432 | **done** (task 85) |
| THE CHRONOLOGY'S SCALE — version control's own, nothing curating it | `Research/op_pipeline/dashboard_ouro.py` — `history` (one `git log`, no `--grep`, no filter, three fields), `vcs_marks`, `moments`, `set_moment`, `WINDOW_TICKS`/`window_start`/`set_window`, `chronology_bar` as two rows; `dashboard_ouro.html` gains one click function, `ouro_window`. A MOMENT IS A COMMIT and every commit is one: the moment list is proved equal to `git rev-list --reverse HEAD` — **1,324 moments, 1,324 commits, identical order**. A commit's subject is drawn as a LABEL and read by no ordering, grouping, windowing or selection. Measured over 5 panes × 41 moments = **205 renders, 0 errors**; chronology drawn 205/205, above the tab bar 205/205, tab bar of five 205/205; one moment change altered **all five panes**. Evidence: `t86_all_panes2.json` | **done** (task 86) |
| what the scale DEGRADES to, and why | measured, not assumed (`t86_vcs_scale.json`, each figure with its command): **1,311 commits, 0 tags, 0 merge commits, 1 root commit, 2 refs, 31 distinct committer days**, commits per day min 1 / median 3 / **max 521**. With no tags and no merges the scale degrades to the commits and the days their own timestamps fall on, and the page prints those marks at every moment. THE DAY ROW SELECTS NOTHING — it moves the window of the commit row and leaves `STATE["moment_key"]` alone, so no commit stands for its day. The commit row carries a printed ceiling of **60** beside the population it was cut from, with two shift controls so every commit is reachable | **measured** (task 86) |
| ONLY ONE MOMENT'S WORK IS HELD, structurally | `open_at`/`close_open` — the commit's tree listing and its `git cat-file --batch` process live in ONE slot, evicted when any other moment is read, rather than cached on each `Moment`. Found by measuring: with the cache on the moment, a pass drawing the bar at all 1,321 moments peaked at **1,970.2 MB**, over this page's own 1,500 MB cap; with the slot the same pass over 1,325 moments peaks at **30.7 MB**. Full pass **276.4 MB** over 205 renders (task 85: 286.1 MB over 200); the real Ourobrowser **566.4 MB** (task 85: 577.8 MB). `MEMORY_CAP_MB` 1500 and `OURO_MEMORY_ABORT` unchanged | **measured** (task 86) |
| the generation of an artifact, picked by number AT EVERY MOMENT | `highest_generation` + `POOL_GENERATION` / `CENSUS_GENERATION`. Task 74 fixed the census by number; the pool was still the hard-coded `the_pool5.json`. A past moment makes the general form necessary rather than merely correct — at 2026-09-03 `f6856895` the highest pool is `the_pool4.json` — so both families are now picked by number. `viewer_build.read_pool` gained ONE optional argument (the pool document) so that the same implementation serves both moments; with no argument its behaviour is unchanged | **done** (task 85) |
| which panes CAN be recomputed at a past moment, measured | population: 5 panes × 40 moments (39 chronology steps + now). Panes 1, 2 and 3 recompute at **5 of 40** (the corpus entered version control on 2026-09-03); pane 4 at **3 of 40** (only `graph_rust.json`, `coverage_go_summary.json` and `coverage_go_files.json` were ever tracked; the 331 MB and 515 MB files never were); pane 5 at **14 of 40** (the census entered on 2026-08-31, the pool on 2026-09-02). Every other case draws the refusal, naming the files. Evidence: `Research/op_pipeline/t85_all_moments3.json`, `t85_gitfacts.json` | **measured** (task 85) |
| the python page's memory bound, with the moment | `MEMORY_CAP_MB` 1500 unchanged, abort `OURO_MEMORY_ABORT` unchanged; the moment adds a second bound — ONLY ONE MOMENT'S WORK IS HELD, every cache dropped in `set_moment` before the next moment is read, so memory does not grow with the number of moments visited. Measured: 200 renders over 40 moments peak at **286.1 MB** in one process; the real Ourobrowser driven through 12 screenshots and 4 moment changes peaks at **577.8 MB**, against the 402.3 MB of the task-77 page and the stated cap of 1,500 MB | **measured** (task 85) |
| the python renderer | `Research/op_pipeline/dashboard_ouro.py` — reads the artifacts with `open()`; imports `viewer_build.units_of`, `.load`, `.carve`, `.OperatorGroups`, `.read_pool`, `.read_coverage`, `.census_name` and `pane23_manifest_regex_check.PAT`/`.unq`; ports the two rules that exist only in `dashboard_join.js` (`mnemsOf`, `signatureOf`) and marks them as ports | **done** (task 77) |
| the python page's own memory bound | `MEMORY_CAP_MB` 1500, abort named `OURO_MEMORY_ABORT`, caught per pane and rendered as that pane's refusal. Measured peak of the whole Ourobrowser process over all six panes: 402.3 MB. The index over 31,078 units is built shard by shard and the parsed document dropped; `the_pool5.json`'s summary is a TAIL carve | **measured** (task 77) |
| the guard over python page code | `Research/op_pipeline/check_dashboard_py_no_spelling.py` — the same 91-token inventory, read from the unmodified `check_no_spelling_keys.py`, over a python syntax tree: a token fails in a dict key, a subscript, a comparison, a membership test or a `.get`/`.setdefault`/`.pop` lookup | **done** (task 77) |

## measured constraints found while realizing panes 2 and 3 (2026-09-03)

- **The signature of a unit is not in the unit.** It is the probe's
  declared types, which live in the probe manifests, joined to the OUT
  row's own width when the compiler stated no result type. The two
  regenerated manifests are 37 MB and 50 MB because every probe carries
  its source text, so the page reads the ten manifests as TEXT and takes
  three fields per probe with one regular expression — 133,993 probes,
  94.2 MB — rather than parsing them. The shortcut is checked, not
  assumed: `pane23_manifest_regex_check.py` runs the same expression in
  python and compares it with `json.load`, probe for probe, on all ten
  files. Evidence: log_179 section 2.
- **A pane over the whole population needs a stated ceiling.** The arch
  opcode in the most units is in 30,432 of them and in 29,653 (language,
  operator group, signature) groups. The pane draws 200 groups, says
  which number it cut down from, and offers a language and a signature
  menu to narrow them. A ceiling that is not printed with its population
  would be a hidden sample. Evidence: log_179 section 3.
- **Four x86 mnemonics are homographs of operator tokens.** `and`, `or`,
  `xor` and `not` are arch opcodes read out of objdump AND alternative
  operator spellings in C++, so they are in the 91-token inventory. A
  json dict key cannot carry that distinction and the unmodified guard
  is right to refuse one. Any artifact of this node that reports the arch
  opcode index therefore carries the mnemonic as `mnem`, a value on a
  row, keyed by an opaque arch id. Evidence: log_179 section 5.

## measured constraints found while realizing the loader (2026-09-03)

- **A page opened by double-click has no storage of its own.** Measured in
  Chrome on this machine: a `file://` page's origin is `null` (opaque) and
  `indexedDB.open` there fires NO event — not success, not error, not
  blocked. The first cut of the loader waited on it and the page was dead.
  The loader now refuses storage on an opaque origin, wires the folder
  button first and unconditionally, and the gate says plainly that the
  folder has to be chosen each time. Remembering the folder works when the
  page is served from an origin; from a double-clicked file it cannot.
  Evidence: log_176 section 4.
- **Firefox has no `showDirectoryPicker`** (measured, Firefox 154.0.1). The
  page detects this, says so on screen, and points at
  `dashboard_snapshot.html`. Evidence: log_176 section 5.
