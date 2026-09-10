---
id: hq.research.compiler_graph.graph
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class), rule
node:
    name: graph
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/CORE_0_3_1_9_graph.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: static_structure
      designation: code (attribute)
      realize: false
    - name: dynamic_structure
      designation: code (attribute)
      realize: false
    - name: frontier
      designation: code (attribute)
      realize: false
    - name: build
      designation: code (method)
      realize: false
    - name: diary
      designation: code (method)
      realize: false
    - name: query_path
      designation: code (method)
      realize: false
    - name: coverage
      designation: code (method)
      realize: false
    - name: super_ops
      designation: code (method)
      realize: false
    - name: variant_structure
      designation: code (attribute)
      realize: false
    - name: variant_connections
      designation: code (method)
      realize: false
---

# CORE 0_3_1_9 — graph

## metadata

- **id:** hq.research.compiler_graph.graph
- **level:** 3
- **status:** draft
- **designation:** code (class), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- static_structure — code (attribute) *(realize: false)*
- dynamic_structure — code (attribute) *(realize: false)*
- frontier — code (attribute) *(realize: false)*
- build — code (method) *(realize: false)*
- diary — code (method) *(realize: false)*
- query_path — code (method) *(realize: false)*
- coverage — code (method) *(realize: false)*
- super_ops — code (method) *(realize: false)*
- variant_structure — code (attribute) *(realize: false)*
- variant_connections — code (method) *(realize: false)*

## definition

Each compiler and interpreter analyzed AS A GRAPH: its own source
parsed into a static structure (tree-sitter CST nodes and the
call / read / write edges between them), joined to a dynamic
structure (the diary — which of those nodes each probe's compilation
visited, in order), and joined a THIRD way: to each operator's traced
variant, so that the graph carries the connections belonging to that
variant and not only the union over all probes. the owner, 2026-09-04,
naming all three: a completed compiler graph "with connections that
are structural, dynamic, and are part of each operator traced
variant". The third is the one this node has never held; the
definition carried only the first two until today. This is the
super-node's founding object; the
nine co-nodes above work on the compiler's OUTPUT, this one on the
compiler ITSELF. It is the design of the PCv5 ledgerer — structural
connections plus dynamic connections — applied to the compiler with
less detail, because this graph does not have to produce runnable
code. Super-op mining is a METHOD OF THIS GRAPH: a super-op is a path
through compiler source that recurs across probes. Name provisional
(2026-09-03); the owner's to change.

## design

```
class Graph
	attributes:
		static_structure
			"""
			nodes: tree-sitter CST nodes of the
			compiler's source region, one id per
			node, per implementation-language
			grammar (.go, .cpp, .rs, .swift, .c;
			.td/.rules/.ad as data-table nodes)
			edges: contains / calls / reads /
			writes / dot-resolved binding
			"""
		dynamic_structure
			"""
			per probe: the ordered list of node
			ids its compilation visited (the
			diary); as edges: visited-next
			"""
		variant_structure
			"""
			per OPERATOR TRACED VARIANT: the
			nodes its own traces enter and the
			visited-next edges between them,
			with each marked shared or
			exclusive to that variant. A
			variant is a set of units grouped
			by MACHINE-FORM EVIDENCE ONLY --
			the emitted body bytes, the same
			body as read, the entry contract,
			and the ledger's produced-by shape.
			Never by the operator's token
			"""
		frontier
			"""
			where the walk could not follow, by
			kind, with candidate sets
			"""
	methods:
		build
			"""
			(source tree, region rule) ->
			static_structure. Exists for go;
			the same code over the other
			compilers is the language-agnostic
			claim, proved by running it
			"""
		diary
			"""
			inject id-emission at node
			coordinates (the v0 inject_emitid
			pattern), rebuild the compiler in
			Airlock, compile a probe, collect
			the ordered id stream ->
			dynamic_structure
			"""
		query_path
			"""
			(node a, node b) -> path through
			static_structure, or a named
			frontier; the identity proof
			"parameter a becomes register X"
			"""
		coverage
			"""
			static_structure x dynamic_structure
			over a probe set -> per node: which
			probes visited it; per probe: its
			path; the never-visited set
			"""
		super_ops
			"""
			recurring sub-paths of
			dynamic_structure across probes,
			ranked by recurrence, each joined to
			the arch-units those probes produced
			-> super-op candidates. THE detector
			(the owner). Replaces super_op_miner.py,
			which read arch-unit bodies and
			never touched compiler source
			"""
		variant_connections
			"""
			(diaries, unit records) ->
			variant_structure. Groups the
			diaried probes into operator traced
			variants by machine-form evidence,
			attributes each visited-next edge
			to the variants that walk it, and
			names the edges and nodes EXCLUSIVE
			to one variant -- the connections
			the union over all probes cannot
			tell apart from ubiquity. THE THIRD
			CONNECTION KIND
			"""
```

Call flow, one probe:

```
Graph.build(source)                 --> static_structure
Graph.diary(probe)                  --> dynamic_structure[probe]
Graph.coverage(static, dynamic)     --> per-node visit sets
Graph.super_ops(dynamic, arch_units)--> candidates
Graph.query_path(param a, reg X)    --> the identity path
Graph.variant_connections(diaries,
        unit records)               --> variant_structure
```

## settled rules

- **The compiler is analyzed as a graph, static + dynamic**, for
  super-op mining and for every other purpose the line has (identity
  proof, coverage). Decision: the owner, 2026-08-24 (log_072; the
  super-node's definition and standing rules) and 2026-09-03 ("i
  specifically asked for the compilers/interpreters to be analyzed
  as a graph — especially wrt to super-op mining but also other
  purposes").
- **The super-op detector is this graph.** the owner, 2026-08-29 (log_081
  §5): "the compiler-graph instrument can measure the path." The
  output-side stand-in (`super_op_miner.py`, "the component miner's
  recurrence counts") was introduced by the coordinator in the same
  log without a ruling and carried into AgentMemory as if ratified;
  corrected 2026-09-03 (AgentMemory, log_173). It is superseded and
  its results are not super-ops.
- **The interpreters are in scope** the same way: the handler's C
  source (cpython, php, ruby) or the JIT's source (java) is the
  compiler here. Decision: SUPPORT_scaling_design.md, interpreter
  track.
- All standing rules of the super-node apply: the proof is a graph
  never prose; the runtime record is a DIARY never a tally;
  language-agnostic by construction; frontier honesty.
- **EVERY READER OF THIS GRAPH RUNS IN BOUNDED MEMORY, not only the miner.**
  A `graph_<lang>.json` is 49 to 331 MB and the coverage join is 515 MB, so
  anything that reads one streams it a record or a line at a time, states
  its peak resident set from `resource.getrusage`, and refuses BY NAME
  (`MemoryCeilingReached`) at a stated ceiling. What a page or a later stage
  reads is a SUMMARY built once by such a streamer, plus a RANGED READ into
  the large file at byte offsets the summary carries. Recorded 2026-09-03
  from task 73, which built `graph_files_build.py` and
  `coverage_files_build.py` under this rule (peak 17-39 MB and 82 MB) after
  task 75's incident made the bound a settled rule for the miner alone.
- **THE MINER RUNS IN BOUNDED MEMORY, and its parameters are stated
  on the artifact.** `super_ops` reads diaries ONE FILE AT A TIME into
  a compact integer stream on disk, counts recurring contiguous runs
  Apriori-style with at most TWO length levels live, and refuses by
  name (`MemoryCeilingReached`) when a stated ceiling is reached. Every
  bound -- `min_length`, `min_support`, `max_length`,
  `max_runs_per_level`, `memory_ceiling_mb` -- is an argument and is
  written into the output. Recorded 2026-09-03 from an incident in task
  75: the first shape held all 10,015,022 diary events as strings and a
  run dictionary for every length at once, both O(events) with no cap;
  it reached 13.2 GB resident, exhausted the machine's 4 GB of swap and
  had to be stopped from outside. The rebuilt shape does the same
  measurement over the same 590 diaries in 21 seconds at 487 MB peak.
  A stop by the operating system is not a measurement; a refusal by
  name is.
- **An uninstrumented node is a frontier, never a never-visited node.**
  An entry hook can only sit in a FUNCTION BODY, so the population
  `coverage` may speak about is the bodies an edit was placed in, and
  no other node kind. Of go's 174,159 region nodes, 1,549 are bodies;
  the remaining 172,610 (refs, calls, params, locals, constants) are
  positions inside bodies and are not observable by this instrument.
  `Graph.coverage` therefore returns four populations, and its
  `never_visited` set is over the instrumented one only. Recorded
  2026-09-03 from task 72 (log_175); the shape was not in the tree
  before that lap needed it.

- **A VARIANT'S IDENTITY IS MACHINE FORM, NEVER A TOKEN, and never
  intention.** The third connection kind groups diaried probes into
  operator traced variants. The grouping key is a digest over four
  machine-form facts read off the unit's OWN ship code -- `body_bytes`
  (what the compiler emitted), `body_text` (the same body as read),
  `entry_contract` (where its arguments arrive and where its answer
  goes) and the ledger's block / size / type / produced-by shape. The
  operator token is written onto each MEMBER as a display label after
  the grouping is finished and is read back by nothing. This is the
  task where the spelling ban is easiest to break, so the rule is
  written before the code: if a grouping cannot be derived without a
  spelling, the lap STOPS and says so. Recorded 2026-09-04, task 87,
  from the owner's naming of the third kind the same day.
- **THE THIRD KIND SPEAKS ONLY ABOUT PROBES THAT HAVE A MACHINE FORM
  ON DISK.** A diary whose probe has no arch-unit record cannot be
  placed in a variant, because the only permitted identity is machine
  form. Such a probe is a NAMED FRONTIER
  (`probe_without_a_machine_form`), never a variant of its own and
  never grouped by anything else. Recorded 2026-09-04, task 87. The
  frontier's population is measured, not assumed: it is **0** on every
  population this lap speaks about — go 590 of 590 (107 in
  `canon39_wrapped_go.json` and 483 in
  `canon39_regen_store/op_units2_go_c000{0,1}.json`), c and cpp 1,380
  of 1,380, and the 2,600 regenerated c and cpp probes 2,600 of 2,600.
  A search lane (`t87_l4_go_unit_id_scan.sh`) first read go as 107 of
  590 by scanning for the id shape `go/op_` alone; `t87_l5_go_regen_
  units.sh` corrected it against this node's own task-72 PROGRESS
  entry. Both lanes are kept as the record.

## the arch-opcode-node — a shape this node lacks, added 2026-09-05

A node in a compiler's graph is an ARCH-OPCODE-NODE when the
compiler's own source shows it producing a machine instruction. It is
detected STATICALLY, from source, with no run of the compiler.

the owner, 2026-09-05: "is there a way to know which parts of the compiler
produces arch-opcodes (arch-units)? perhaps that would shrink the
graph size to only the relevant parts to opcode production... i mean
just by analyzing the compiler source code. like if the compiler
produces an arch opcode, its an arch-opcode-node."

THE MECHANISM. Each compiler emits every machine instruction through a
narrow point, and that point is already inside this node's region.
MEASURED in go's region 2026-09-05: `ssagen/ssa.go:6742 func (s
*State) Prog(as obj.As)` is the emitter; 206 call sites; 50 pass a
CONSTANT opcode (24 distinct, `x86.AMOVQ`, `x86.AADDQ`, `x86.AJNE`
and so on); 118 pass a computed one (`op`, `v.Op.Asm()`, `as`).
clang's equivalent is `llvm/lib/Target/X86/X86MCInstLower.cpp` plus
`BuildMI(..., TII->get(X86::...), ...)` call sites, and the region
already keeps `.td`, which enumerates the instructions.

THREE GRADES, and the third is a category rather than a failure:
  1. NAMES ITS OPCODE -- the call site passes a constant. Provable
     from source; the node is an arch-opcode-node for those opcodes.
  2. RESOLVABLE BY ONE STATIC HOP -- `v.Op.Asm()` reads go's generated
     op table, which maps each SSA operation to its assembler opcode;
     LLVM's `.td` is the same kind of table.
  3. EMITS, OPCODE GENUINELY DYNAMIC -- marked as an emitter whose
     opcode cannot be named statically. Never guessed.
Everything else in the region emits nothing, and that set is what may
be dropped without losing opcode-production information.

WHY IT MATTERS BEYOND SIZE. It needs only source. rust is blocked on
this machine and swift cannot be started here, so neither can be
instrumented -- but both graphs are built, so both get
arch-opcode-nodes from this pass. It reaches compilers the machine
limits block.

NOT FOR INTERPRETERS. An interpreter emits no machine instructions; it
dispatches. Its equivalent already exists and is not this: the unit IS
the handler, bounded by the handler's own function (arch_unit CORE,
"the unit's boundary", ruled 2026-09-05).

## what "completed" means — settled 2026-09-04, and NOT an open question

The graph is complete when it is an actual implementation of the
object this CORE's definition specifies: each compiler and interpreter
in scope, carrying all three connection kinds — structural, dynamic,
and per operator traced variant. Nine compilers and interpreters are
in scope. Two carry all three kinds today (go, and clang serving c and
cpp). The graph is therefore NOT complete, and the remainder is the
work, not a definition to be renegotiated.

THE QUESTION THAT WAS WRONGLY ASKED, recorded so it is not asked
again: the round-16 coordinator forwarded "whether 'completed' means
all nine compilers or the three kinds over the two this machine can
instrument" as a decision for the owner. It is not a decision. It offered a
reduced deliverable as a legitimate reading of the requirement, which
is the substitution failure log_173 already records once for this same
node. the owner, 2026-09-04: "completed compiler graph? when theres an
actual graph that is an implementation of what ive asked."

A machine limit is a measured obstacle to report, never a redefinition
of what was asked. Where a compiler cannot be instrumented here (rust
blocked, swift unstartable — log_175 §6.3-6.4), the row says so with
its cause and stays **planned**.

## realization (what exists on disk, 2026-09-03, after task 71)

Home of the PROGRAMS and the small summaries:
`PRIVATE/PseudoCoupHQ/Research/compiler_graph/`. Home of the
ARTIFACTS since 2026-09-04 (task 93): `PseudoCoupGraphs`,
a companion folder with NO REMOTE by design, holding
`graph_<lang>.json`, `coverage_<lang>*.json`, `super_ops_<lang>.json`,
`variant_connections_*.json` and `diaries/`. One place answers where
they are, `graphs_home.py`, and no reader carries a path. THE GRAPHS ARE
STORED IN THE COMPACT FORM (`graph_compact.py`): one string table per
document, every record an array of references into it, 608,076,632 bytes
of graph in 72,188,201, and `graph_compact.py expand` rebuilds the old
file BYTE FOR BYTE — proved by `cmp` on all four, md5 against md5, with
each compact document carrying the original's own md5 so the proof is
re-runnable. The byte counts below are the EXPANDED form each graph was
measured in. Sources on disk: `Sources/{golang_src,
llvm-project, rust, swift-6.0.3-RELEASE, jdk}`. THE CLASS NOW EXISTS UNDER THE NODE'S OWN
NAME: `graph.py`, `class Graph`, with `build`, `query_path`, `diary`,
`coverage`, `super_ops`. `build_graph.py`, `build_graph2.py` and
`build_graph3.py` are superseded records, each carrying one header
line that says so.

| part | current file | status |
|---|---|---|
| the class | `graph.py` — `Graph(static_structure, dynamic_structure, frontier)` | done, task 71 |
| build (go) | `graph.py go` → `graph_go.json`: 10,393 nodes / 63,797 edges / 77,530 frontier / 0 parse errors, 81 files | done, task 71 |
| build (cpp, serving c and cpp) | `graph.py cpp` → `graph_cpp.json`: 112,364 / 386,065 / 523,694 / 2,082 named parse errors, 269 files incl. 61 data tables | done, task 71 |
| build (rust) | `graph.py rust` → `graph_rust.json`: 13,446 / 60,382 / 101,095 / 49 named parse errors, 134 files | done, task 71 — with a PIN FRONTIER (the corpus's rustc source commit is absent from the checkout) |
| build (swift) | `graph.py swift` → `graph_swift.json`: 71,106 / 192,655 / 278,245 / 311 named parse errors, 230 files | done, task 71 |
| the per-operator-traced-variant connections (go) | `graph.py` `Graph.variant_connections` → `variant_connections_go.json`: **590 of 590 diaried probes, 0 without a machine form, 294 operator traced variants**, 626 nodes entered and 1,598 visited-next transitions; 14 transitions walked by exactly one variant, 677 by every variant; 344 of 1,598 backed by a static `calls` edge. 3.5 s, 172.4 MB peak against a 6,144 MB ceiling | done, task 87 |
| the per-operator-traced-variant connections (c and cpp) | `graph.py` `Graph.variant_connections` → `variant_connections_c.json` (610 probes, 331 variants), `variant_connections_cpp.json` (770, 353), `variant_connections_c_and_cpp.json`: **1,380 of 1,380 probes, 0 without a machine form, 512 variants**, 1,175 nodes and 2,044 transitions, 48 transitions walked by exactly one variant and 674 by every variant, 364 static-backed; and `variant_connections_extended.json` over the 3,980 extended probes: **1,361 variants**, 1,319 nodes, 2,474 transitions, 66 walked by exactly one variant. 3.4 s / 11.0 s, 1,051.9 MB peak, fitted from two measured points before the pass (fixed 1,051.9 MB, 0.0003 MB per probe) | done, task 87 |
| the per-operator-traced-variant connections (rust, swift) | `variant_connections_rust.json`, `variant_connections_swift.json` — each `state: UNMEASURED_BY_ABSENCE_OF_DIARIES`, 0 variants, carrying the cost page's own reason | **planned** — UNMEASURED BY ABSENCE OF DIARIES, written down rather than approximated; the cost page in log_175 §6.3–6.4 gives the reason (rust BLOCKED on this machine: a promisor clone with no route out and an absent pin; swift cannot be started here: three of the five repositories a build needs are not on this disk) |
| build (java, cpython, php, ruby) | nothing | **planned** |
| query_path | `graph.py`, `report_graph.py` | done — go reproduces the August answer; cpp / rust / swift stop at NAMED frontiers |
| diary (reader) | `graph.py` `Graph.diary` | done, task 71 |
| diary (producer, go) | task 72's injector → `diaries/go/*.txt`, 590 probes | done, task 72 |
| diary (producer, c and cpp) | task 81's injector `t81/inject_diary_clang.py` → `diaries/c` (610) and `diaries/cpp` (770), the whole ORIGINAL corpus, plus `diaries/regen` (2,600 of the 27,080 regenerated units, every 10th by unit id). Instrumented clang at `llvmorg-21.1.8` / `2078da43e25a`, 8,871 entry hooks placed of 9,108 targets, 237 skipped each with a named cause. 1,380 of 1,380 and 2,600 of 2,600 compiled, 0 failed | done, task 81 |
| diary (rust, swift, java, cpython, php, ruby) | nothing; cost page in log_175 §6 (rust BLOCKED on this machine, swift cannot be started here) | **planned** |
| coverage (go) | `graph.py` `Graph.coverage` → 724 of 1,859 defs visited by at least one of 590 probes | done, task 71 |
| coverage (cpp, serving c and cpp) | `graph.py join` → `coverage_c.json` / `coverage_cpp.json` / `coverage_c_and_cpp.json` / `coverage_extended.json`. **1,331 of 8,871 instrumented bodies visited by at least one of the 1,380 original probes; 7,540 by none, over 180 files**; 1,918 defs a NAMED FRONTIER (a body in a header file, or one with no declared name); 0 visited keys outside the region. c alone 1,251 of 8,871 over 610 probes, cpp alone 1,328 over 770. With 2,600 regenerated probes added (3,980 in all) the visited set is 1,482 and 151 bodies are reached that no original probe reaches, almost all in the X86 backend | done, task 81 |
| coverage (rust, swift) | 0 probes — never-visited BY ABSENCE OF MEASUREMENT | **planned** |
| super_ops | `graph.py` `Graph.super_ops` -> `super_ops_go.json`: **9,809 closed candidates** over the 590 go diaries, parameters min_length 3 / min_support 2 / subject `probe_own` / collapse_repeats true / max_length 12; 21 s, 487 MB peak | done, task 75 — with a STATED CAP: frequent runs were still growing at length 12 (9,358 of them), so recurring paths LONGER than 12 nodes exist and were not mined this lap |
| super_ops (cpp) | `graph.py super-ops` -> `super_ops_cpp.json`: **13,783 closed candidates** over the 770 cpp diaries, THE SAME PARAMETERS the go lap used and quoted from its own artifact — min_length 3 / min_support 2 / subject `probe_own` / collapse_repeats true / max_length 12 / max_runs_per_level 2,000,000 / memory_ceiling_mb 6,144; 10.3 s, 1,118 MB peak, 1,172 distinct coordinates over 1,185,628 stream events | done, task 81 — with the SAME STATED CAP as go: frequent runs were still growing at length 12 (12,773 of them), so recurring paths longer than 12 nodes exist and were not mined this lap |
| super_ops (rust, swift) | 0 diaries | **planned** |
| the both-ways comparison against the superseded output-side miner | `report_super_ops.py compare` -> `super_ops_comparison_go.json` (task 75) and `super_ops_comparison_cpp.json` (task 81: of 494 output-side records, 347 name cpp units; **347 have a loose counterpart, 207 a STRICT one** — a sub-path confined to the units the record names, where go had 0 — and 0 have none; 6,020 of the 13,783 graph candidates have an output-side counterpart, 7,763 have none). `--language` is now an argument, defaulting to `go`, and the go artifact re-runs byte-identical | done, tasks 75 and 81 |
| the file-level summary of each graph | `graph_files_build.py` -> `graph_<lang>_files.json` (83 / 330 / 134 / 230 file rows for go / cpp / rust / swift) and `graph_<lang>_defs.json` (1,859 / 10,789 / 3,313 / 10,088 definitions). Streaming, no node table; peak resident 17 / 39 / 20 / 31 MB | done, task 73 |
| the file-level summary of the coverage join | `coverage_files_build.py` -> `coverage_go_files.json` (2,597,323 bytes): populations, per-file rows, the 810 never-visited bodies with labels, per-definition visitor counts, and per probe its file-level path plus the BYTE RANGE of its full path inside `coverage_go2.json`. Peak resident 82 MB over a 515 MB input | done, task 73 |
| the spelling ban, PROVED ON THE OUTPUT (task 87) | of the 512 c-and-cpp variants, **133 carry more than one distinct display label** among their members (one holds `+`, `++`, `--`, `__extension__`), and **all 36 distinct labels appear in more than one variant** (`<` in 58). Both directions are impossible if the token were the key. Transcript: lane `t87_l10_rebuild_and_ban_proof.sh` | done, task 87 |
| the guard | `check_no_spelling_keys.py` over all four graphs, one process, exit 0; and over all nine artifacts task 73 emits, one process, exit 0, with both builders refusing their own output on failure | done, tasks 71 and 73 |
| the arch-opcode-node (all four regions) | `graph.py` `Graph.arch_opcode_nodes` → `arch_opcode_nodes_<lang>.json` in `PseudoCoupGraphs`, plus a small `arch_opcode_nodes_<lang>_summary.json` in the repo. FOUR STATES, from SOURCE ALONE, and they partition each definition population: **go 13 / 39 / 5 / 1,802 of 1,859**; **cpp 174 / 8 / 69 / 10,538 of 10,789**; **rust 0 / 0 / 1 / 3,312 of 3,313**; **swift 1 / 0 / 1 / 10,086 of 10,088**. Emitters LOCATED per region, never carried over from go: go's three functions TAKING `obj.As` (`(*State).Prog` 206 sites, `(*State).Br` 9, `opregreg` 23) against its four RETURNING it (the hop targets, including `Op.Asm()` → `ssa/opGen.go`); clang's `BuildMI` 724 / `setDesc` 57 / `MCInstBuilder` 53 / `setOpcode` 36; rust NONE — 0 files of the whole checkout name any instruction-building construct, so the emitter is LLVM, which is the cpp region; swift the inline-assembly constructor, 5 sites, of which one spells `nop`. Inverse index: go 578 arch opcodes, cpp 400, swift 1. The coordinator's go count reproduces exactly — 50 `Prog` sites pass an x86 constant, 24 distinct. Restricted to emitters and their callers each graph keeps **3.6% (go), 3.3% (cpp), 0.2% (rust), 0.0% (swift)** of its definitions. 0.3–3.1 s, peak 117–567 MB against a 6,144 MB ceiling | done, task 95 |
| the arch-opcode-node vs what running the compiler showed | ENTERING IS NOT EMITTING, kept apart in both directions. go: 57 static emitters, 724 entered, **12 in both**; 712 of the 724 entered emit nothing; 45 of the 57 emitters were instrumented and entered by no probe, **39 of them the `simd*` helpers of `amd64/ssa.go` the 590 scalar probes never reach**; 0 emitters outside the instrumented population. cpp: 251 emitters, 1,331 entered, **45 in both**; 1,286 of the entered emit nothing; 203 instrumented and entered by none; 3 never instrumented — a NAMED FRONTIER, never a never-entered node | done, task 95 |
| the guard (task 95) | `check_no_spelling_keys.py` UNMODIFIED (md5 `1d6aba67cbcdb021c3bdfd7f40fd2020`), ONE process, over all 8 artifacts: **8 PASS, exit 0, `grep -c exempt` = 0**. It first REFUSED go's artifact at `$.call_sites[223].argument` — go's emitter is `func (s *State) Prog(as obj.As)` and `s.Prog(as)` puts the operator token `as` in a row-structure position. Fixed at the cause with the ratified typed shape `{"text": "..."}`, no exemption and no rename; and `Graph.arch_opcode_nodes` now runs the guard over its own output and raises `SpellingKeyRefused` rather than returning. Transcript: `Research/compiler_graph/guard_task95.txt` | done, task 95 |
| the guard (task 87) | `check_no_spelling_keys.py` UNMODIFIED (md5 `1d6aba67cbcdb021c3bdfd7f40fd2020`, git reports no change), ONE process, over all seven `variant_connections_*.json`: **7 PASS, exit 0, `grep -c exempt` = 0**. Transcript: `Research/compiler_graph/guard_task87.txt` | done, task 87 |
