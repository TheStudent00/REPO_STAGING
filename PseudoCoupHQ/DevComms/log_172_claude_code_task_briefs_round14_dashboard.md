# log 172 — task briefs for Claude Code, round 14: the dashboard and the compiler graph

Date: 2026-09-03. Point a Claude Code session here. OPUS default.
ONE AIRLOCK INSTANCE PER TASK. All of log_158's binding rules stand
(code carries the node's name; a shape the tree lacks goes into the
tree first; nothing reaches the owner that a CORE or AgentMemory answers;
PROGRESS at the moment of progress; standing requirements incl. the
spelling ban pasted verbatim into every sub-agent brief).


## REORDERED 2026-09-03 (log_173): THE GRAPH IS THE ROUND

the owner: "i specifically asked for the compilers/interpreters to be
analyzed as a graph -- especially wrt to super-op mining but also
other purposes." The super-op detector the owner ruled is the compiler
graph (static structure + dynamic structure, the PCv5 ledgerer's
design); the output-side `super_op_miner.py` was a substitution never
ruled (AgentMemory, corrected; log_173). So this round's order is:

  71 and 72 first, in parallel (the graph and the go diaries);
  75 next (super_ops from the diaries);
  then 68, 69, 70, 73 (the dashboard on top of them);
  74 last.

Read `node_0_3_5_9_graph/CORE_0_3_5_9_graph.md` — its `## design`
names `static_structure`, `dynamic_structure`, `coverage`,
`super_ops` — before touching anything.

## WHAT THIS ROUND IS FOR (the owner, 2026-09-03)

"this project has too many moving pieces and you seem to not be able
to speak in a way that i understand. so we will work to establish an
undeniable means of communication about this project that will
update mechanically." Two new nodes were written for it, both with
provisional names:

- `Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/`
  — the five panes the owner numbered; a draft exists
  (`Research/op_pipeline/viewer_build.py` + `viewer_template.html`
  → `dashboard.html`, shown to the owner).
- `Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/`
  — the compiler's own source as a graph, per compiler, with a
  diary per probe. This is the super-node's founding purpose and
  has only a go lap from August behind it.

Read both COREs before anything. Their realization tables say what
exists; every **planned** row is a task below.

TWO RULINGS FROM DEE THAT SHAPE EVERYTHING HERE:

1. **No server, no terminal.** "i dont want to run a server or use a
   terminal command." The page opens by double-click and reads the
   artifacts itself.
2. **Update mechanically.** Every number on the page is a count over
   a file on disk at the moment the page is opened; nothing is
   hand-maintained.

STATE AT HANDOFF (log_171 bank): canon39 30,432 / 646; terms 26,594
proved / 3,134 undecided / 285 withdrawn / 419 no term (audit65);
pool5 1,831 entries / 490 multi-language; families5 34;
census5 52 producers; render_back 5,909 / 5,873 proved.

---

## TASK 68 — the live loader: the page reads the artifacts, no server (node 0_3_5_10; Opus)

CONTEXT: `viewer_build.py` (the join logic, in Python — port it, do
not reinvent it); `viewer_template.html` (the panes).

WORK:
1. `Research/op_pipeline/dashboard.html` becomes a page that, on
   open, asks ONCE for the `op_pipeline` folder via the File System
   Access API (`window.showDirectoryPicker`), remembers the handle
   (IndexedDB) so the next open needs one click of confirmation,
   and reads `canon39_wrapped_*.json`, `canon39_interp.json`,
   `canon39_regen_store/*.json`, `term65_store/*.json`,
   `the_pool5.json`, `probe_manifest*.json`, `name_census5.json`,
   `the_families5.json`, `audit65.json`, `render_back_store/*`,
   and `../compiler_graph/*` in the browser. All 31,078 units, not a
   sample; read lazily (manifest first, unit bodies on demand) so
   the first paint is under two seconds on this machine — measure
   and paste the timing.
2. Keep `viewer_build.py` as the SNAPSHOT builder (embedded data,
   shareable file) — one join module used by both, not two copies:
   write the join once in JS and have `viewer_build.py` embed the
   same JS with the data pre-read. State in the log which functions
   are shared and prove it by a diff.
3. Firefox has no `showDirectoryPicker`; the page must say so and
   offer the snapshot. State which browsers were tested (Chrome
   and Firefox at least, on this machine).
4. Every pane shows its population line ("N units read from M
   files, opened at HH:MM") — the mechanical-update rule made
   visible.

## TASK 69 — pane 1 completed: context, rendered-back, verdicts (nodes 0_3_5_10, 0_3_5_1_6 context; Opus)

WORK:
1. **Context mode.** Today a body names a constant by relocation
   (`!!reloc=R_X86_64_PC32:.LCPI0_0-0x4`) and the constant's BYTES
   are stored nowhere per unit. Add them: for every unit whose body
   carries a rip-relative reference, read the bytes from the ship
   object's `.rodata` (the probe builds are in `trickle_store/` and
   the original lanes' outputs — find them, name the path in the
   log) and record `context: [{symbol, bytes, width}]` on the
   canon39 record as a NEW sidecar file `canon39_context.json` (no
   edit to canon39_*). Population: count the units that reference a
   constant; report how many got their bytes and every one that did
   not, with the cause. This is `arch_unit.context`'s owed data;
   update that node's PROGRESS.
2. **Rendered-back mode** from `render_back_store/` (5,909 units).
3. **Verdicts mode**: the wrapped-text verdict, both term routes,
   the reason strings, the counterexample when there is one.
4. **Interpreter units**: show the handler's C source where the
   interp record carries it; say "no source recorded" where it does
   not.

## TASK 70 — panes 2 and 3 hardened over the full population (node 0_3_5_10; Opus; after 68)

WORK: the selector and the opcode index over all 31,078 units (not
the 2,456 sample). The opcode index groups by `lang.operator.
signature` where the signature is the probe's declared types with
the result read off the OUT row's width when the compiler stated it.
The spelling-ban test is RUN, not asserted: a build flag replaces
every operator label with a glyph and a script clicks through every
pane and confirms nothing breaks — paste the transcript. Random
sampler is seeded and the seed is in the URL hash.

## TASK 71 — the compiler graph, four compilers (node 0_3_5_9 graph; Opus; the round's centerpiece; its own Airlock instance)

CONTEXT: `Research/compiler_graph/build_graph3.py` (go; the
language-agnostic claim); `Sources/{llvm-project,
rust, swift-6.0.3-RELEASE, golang_src}`; the super-node's standing
rules (graph never prose; DIARY never tally; frontier honesty).

WORK:
1. `Research/compiler_graph/graph.py` — the class the CORE names,
   with `build`, `query_path`, `diary`, `coverage`; `build_graph3.py`
   becomes a superseded record.
2. `build` over the LOWERING REGION of each compiler — the region
   rule stated per compiler in the log, chosen by the same
   minimality rule the CORE states ("model what is easy; build only
   enough to prove which low-level operands are which high-level
   variables"): go `cmd/compile/internal/{ssagen,abi,amd64,ssa}`
   (exists); clang `lib/CodeGen` + `lib/Target/X86` (+ the
   TableGen `.td` tables as data-table nodes); rustc
   `compiler/rustc_codegen_ssa`, `rustc_codegen_llvm`,
   `rustc_middle/src/mir`; swift `lib/SILGen`, `lib/IRGen`. One
   graph file per compiler: `graph_<lang>.json`; nodes / edges /
   frontier counts per file, 0 parse errors or every error named.
3. Report, per compiler: nodes, edges, frontier by kind, and ONE
   path query answered — the parameter-to-register question the go
   lap answered — or a named frontier where it cannot yet be
   answered. Frontier honesty is the deliverable where the answer
   is not.

## TASK 72 — the diary for the current corpus, go first (node 0_3_5_9 graph; Opus; after 71; its own instance)

CONTEXT: `inject_diary.py`; the persisted instrumented go tree at
Airlock `/persist/gosrc` (check it is still there; rebuild if not);
the 590 go units of the corpus (107 original + 483 regenerated);
their probe sources in `probe_manifest_go.json` /
`probe_manifest2_go.json`.

WORK:
1. Recompile every go probe of the corpus through the instrumented
   compiler, collecting one ordered diary per probe:
   `diaries/go/<unit>.txt`. Chunked, resumable, in the `trickle`
   instance or a fresh one — state which.
2. `Graph.coverage` joins the diaries to `graph_go.json`: per graph
   node, which probes visited it (and in what order); per probe,
   its path. Output `coverage_go.json`. Report: nodes visited by at
   least one probe / total nodes in the region; the nodes NO probe
   visits, by file (that list is the finding — compiler logic our
   probes never exercise).
3. Only go is diaried this round. For clang / rustc / swiftc, the
   COST PAGE is mandatory output: build time, disk, and the emission
   hook for each, measured on this machine (a one-file instrumented
   build of each is cheap enough to time — do it). Round 15 builds
   them; this page is what it schedules against.

## TASK 73 — pane 4: the coverage view (node 0_3_5_10; Opus; after 71 and 72)

WORK: per language: (a) the static structure — the region graph
drawn as a wiring diagram (files as boxes, functions as nodes,
call/read/write edges; a force layout is acceptable, a file-grouped
layout is better); (b) the dynamic structure — pick a probe, its
diary path lights up in order; (c) coverage — the union over the
corpus shades every node by how many probes visited it, and the
never-visited set is listed. Where a language has a graph but no
diaries (clang, rustc, swiftc after task 71), the pane shows (a)
and says (b)/(c) are not measured. Rendering must stay usable at
174,159 nodes: collapse to file level by default, expand on click.


## TASK 75 — super_ops from the diaries (node 0_3_5_9 graph; Opus; after 72)

CONTEXT: `Graph.super_ops` in the CORE; the go diaries of task 72;
`super_op_candidates.json` / `super_ops3.json` (the superseded
output-side miner's candidates — read for COMPARISON only).

WORK:
1. Over the 590 go diaries: recurring sub-paths of the dynamic
   structure (sequences of visited compiler-source nodes) across
   probes, ranked by recurrence; minimum length and support stated
   as parameters on the artifact, never hidden. Each candidate
   carries: the compiler-source nodes (file:line spans), the probes
   it recurs in, and the arch-units those probes produced.
   `super_ops_go.json`.
2. Print the top 20 with values: the source span, an excerpt of the
   compiler's own code at that span, the probe count, and two of the
   arch-units — so the claim "this idiom is the compiler's logic" is
   read off the compiler's source rather than inferred from bytes.
3. COMPARE against the output-side miner: for every candidate of
   `super_ops3.json` whose units are go units, does a diary sub-path
   coincide with it? Report the join both ways (graph candidates
   with no output-side counterpart; output-side candidates with no
   graph counterpart), each named. This is the measurement of what
   the substitution cost.
4. Guard: the spelling ban applies — candidates are keyed by source
   node ids, never by operator label. Unmodified guard, one process.

## TASK 76 — pane 6: the chronology (node 0_3_5_10; Opus; after 68)

CONTEXT: the owner, 2026-09-03: "i would like the dashboard to also have a
chronology based on vcs so i can step through the history to see
progress." The repo has 972 commits since 2026-07-31 (the daemon
commits every 30 s) and 13 banking commits, one per round
(`git log --grep=banked -i`). The stat artifacts are TRACKED from
round 10 on (`the_pool5.json`, `audit65.json`, `name_census5.json`,
`canon39_wrapped_*.json` all answer `git ls-files`); `the_pool1.json`
(18 MB) was not, so round 9 cannot be recomputed.

WORK:
1. `Research/op_pipeline/chronology_build.py`: walk the banking
   commits (and, on a finer scale, one commit per day); at each,
   `git show <commit>:<path>` the stat artifacts of THAT round
   (the round's bank log names them) and recompute the stats pane's
   numbers — never copy a number from a log. Where an artifact is
   absent at that commit, parse the bank message's count line and
   mark the step `testimony`. Output `chronology.json` (tracked;
   small), one record per step: commit, date, round, numbers, the
   round's log paths, the bank message, and a `source` field
   (`recomputed` | `testimony`) per number.
2. The pane: a slider (rounds) with a fine-scale strip (days); at
   each step the stats table as it stood, the delta from the previous
   step, and the links to that round's logs. The population line
   states the commit hash and date.
3. `chronology_build.py` runs as a step of every bank task from now
   on, so the record grows mechanically.
4. Print the chronology in the log as a table: round, date, commit,
   extracted / distinct / dominant / proved terms, source. This is
   the first time the line's progress is stated from the vcs rather
   than from memory; paste it whole.

## TASK 74 — pane 5 and the bank (smaller model acceptable)

WORK: stats pane over the full population with the four term
states and the census's top causes; `check_plans.py` pasted;
dashboards regenerated; PROGRESS on `dashboard` and `graph` off
`planned` for everything delivered; posterity message with `wc -c`.

---

Order (reordered 2026-09-03, log_173): 71 and 72 first, in
parallel, each in its own instance; 75 after 72; 68 after 71; 69, 70
and 76 after 68; 73 after 75; 74 last (74 runs chronology_build.py
as its own final step). The graph work does not wait on
the dashboard; the dashboard waits on the graph.

NOT IN THIS ROUND: diaries for clang / rustc / swiftc (task 72
prices them); the interpreters' graphs (cpython, php, ruby, java) —
same machinery, later round.

DEE'S QUESTION, ANSWERED IN THE TREE (graph CORE, settled rules):
the super-op miner never produced any of this. It read arch-unit
BODIES for recurring instruction idioms and lifter names; it never
read compiler source, never built a graph, and is superseded by the
ledger census. The compiler graph is `node_0_3_5_9` and has one go
lap behind it — that is the whole of what exists.
