---
id: hq.research.compiler_graph
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: compiler_graph
    path: Planning/node_0_3_research/node_0_3_5_compiler_graph/CORE_0_3_5_compiler_graph.md
super_node:
    name: research
    path: ../CORE_0_3_research.md
sub_nodes: []
---

# CORE 0_3_5 — compiler_graph

## metadata

- **id:** hq.research.compiler_graph
- **level:** 2
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [research](../CORE_0_3_research.md)

## sub_nodes

*(none yet)*

## definition

A completely transparent, provable, logical trace connecting a high
level variable to its low level form, built by turning the
COMPILER'S OWN SOURCE into a graph and walking it. The compiler is a
program; while it runs it transforms objects; its source is
parseable; therefore the connection "parameter `a` becomes register
X" is a PATH through that source, found by a machine, not asserted
by a person.

Founded 2026-08-24 (the owner: "make a research node please. im super done
saying the same things over and over") after the conversation
recorded in
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_072_compiler_graph_tracing.md`.
This CORE exists so the standing rules below never again live only
in conversation.

## the goal, and its minimality rule (the owner, 2026-08-24, at the
diary's start)

The ultimate goal: use the flow graphs to map a HIGH LEVEL NAMED
VARIABLE to its LOW LEVEL OPERAND. That target sets the scope:
not everything needs to be modelled. Model what is easy; beyond
that, build ONLY enough to prove which low-level operands are
which high-level named variables. Completeness of the compiler
model is not the objective; sufficiency of the identity proof is.

## the standing rules (each one was repeated in conversation until
it hurt; none is re-litigable without the owner)

- **The proof is a graph, never prose.** Nodes and edges as data;
  the claim "X connects to Y" is answered by a path query; the
  query's output is the deliverable. A human quoting source lines is
  a TRACE (weak form, interpretation still in the loop) and is only
  scaffolding. Extraction of the logic for use is a SLICE (strong
  form); tracing is not slicing.
- **The runtime record is a DIARY, never a tally.** A diary writes
  each spot down AS IT IS ENTERED — order preserved. A tally
  (coverage counters) records only how many times — order lost —
  and order-lost is opaque, which defeats the entire point. The
  diary machinery ALREADY EXISTS in the line: v0's `inject_emitid`
  stamped ids into code at tree coordinates and the code printed
  its ids as it ran; the ledger attached those events to static
  ids (PCv5 harvest, survey part 2.7). Apply that pattern to the
  compiler's source. The lap-one use of Go coverage was the wrong
  instrument, chosen for cheapness against the project's own
  design; it stands only as a stopgap and its output must never be
  presented as a trace.
- **Language-agnostic by construction.** The machine ingests file
  extensions and dispatches each file to the tool for the language
  it is DEFINED in (tree-sitter grammar per language; assembly
  grammar for .s; data-table readers for .rules/.td/.ad; the pyvex
  lift for bare machine code). One multi-language graph. "Defined
  in" versus "does": a lowering function about arch opcodes that is
  itself written in Go sits in the Go region.
- **Probes are generated, never hand-written.** The operator
  inventory with arity per language is already data
  (`<WORKSPACE_DIR>/PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.json`).
  arity -> wrapper shape -> feed to the instrumented compiler ->
  the diary records the visited path. No per-operator hand work.
- **Never key on spelling.** Two operators are the same only by
  machine-form equivalence. Spelling is a label carried on the
  data, never a comparison key. (The spelling-keyed matrix of
  2026-08-24 was a defect; ruled then.)
- **Evidence classes, stated on every claim** (AgentMemory, the
  evidence doctrine): forced-by-construction > the tool's own
  testimony > human interpretation of stated design. An observed
  diary path is fact FOR THE OBSERVED RUN; the static graph bounds
  ALL runs; every claim says which it is.
- **Frontier honesty.** Where the graph cannot follow, it says so
  by kind, with the candidate set where computable
  (log_072 §4). A named dead-end is a valid result; a guess never
  is.
- **Coding discipline (the owner, 2026-08-24): no complex statements.**
  If a statement can be split into multiple lines, split it.
  Compound one-liners hide information; that is an anti-pattern in
  every artifact of this node.
- **Communication:** every session on this node re-reads
  [LLM_communication_protocol](../../../DevComms/LLM_communication_protocol.md) and
  `<WORKSPACE_DIR>/PseudoCoupHQ/AgentMemory.md` before any work.

## the ratified pipeline (the owner, 2026-08-24: "we are well aligned")

The road from operator vocabulary to the dominant-operator table.
Steps 1-3 build the material, 4-5 make it comparable, 6-7 decide,
8 is the destination.

1. **probes generated, never hand-written**: grammar operator
   vocabulary (operator_arity.json) × holder types, gated by
   COMPILE-OR-REFUSE — the compiler's own type checker is the
   acceptance oracle (that is where overload resolution lives);
   refusal text recorded as testimony.
2. **every probe compiles twice**: ANCHOR (optimizer off: clang
   -O0 / rustc opt-level=0 / go -N -l / swiftc -Onone) and SHIP
   (optimized). Identity is established at the anchor; matching
   happens on ship; the anchor/ship diff carries identity across.
3. **arch-unit extraction**: objdump, one notation, both builds.
4. **argument identity**: DWARF at the anchor + the forced probe
   (a-b vs b-a) + the route detour — three independent grounds.
5. **normalization**: canon column + lifted sem with anchored
   operand identities (closes the in0/in1 guessing defect).
6. **matching**: byte identity, then sem identity. Spelling is a
   label, never a key.
7. **three verdicts**: MATCHED; DIFFERS-BY-DESIGN (guards, traps,
   checked vs wrapping — the mismatch IS the finding: the
   divergence condition, extractable from the guard code);
   UNMATCHED -> solver (z3 over lifted forms), probe-refutation
   where the solver cannot decide, and an honest UNDECIDED bin.
8. **deliverable**: the dominant-operator table — per operator
   intention, the equivalence classes with their divergence
   conditions — feeding ur_kind and the ledger. Compiled
   languages only (ruled).

## support

- [SUPPORT_scaling_design.md](SUPPORT_scaling_design.md) — the road
  to the remaining eight languages and the deferred operator
  buckets: JIT warm-up track (dump switches, deopt as a mode),
  interpreter track (the handler slice — the interpreter plays the
  compiler's role, the map+diary+tally toolkit transfers), the
  milestone accounting (51 dom_ops, 142/142 measured nodes),
  compound assignment as owed work. CPython ruled first (the owner,
  2026-08-26).

## artifacts (in <WORKSPACE_DIR>/PseudoCoupHQ/Research/compiler_graph/)

- `build_graph.py` — parses a region of a compiler's source into
  `graph_go.json` (nodes, typed edges, frontier records). Lap one:
  86 files of Go's cmd/compile; 182,935 nodes; 234,312 edges; 0
  parse errors. Pins: tree-sitter 0.26.0, tree-sitter-go 0.25.0,
  Go tree commit 9f1012d9 (1.28-dev; provenance UNVERIFIED — the
  tree carries unrecognized internal packages).
- `query_path.py` — the path query over the graph.
- `coverage_go.txt` + `coverage_meta.md` — the lap-one TALLY
  (stopgap; see the diary rule). Instrumented toolchain persisted
  at Airlock `/persist/gosrc`.
- `graph_walk.html` — visualization: the subgraph around the
  8-step path, run-counts overlaid, arrows directional,
  drag/zoom/fit; carries the printed caveat that a tally has no
  order.
- `acceptance_query.{txt,json}` — the lap-one result: 8-step path
  from the parameter loop to register allocation inside
  `abi/abiutils.go`, every step confirmed executed by the tally
  (loop x18, chain x10).

## open, in order

1. **The diary** — id-emission instrumentation of the compiler's
   own source (the inject_emitid pattern), giving visit ORDER;
   supersedes the tally.
2. **Follow the dot** — resolution of `x.field` references by
   finding which declaration `x` is an instance of and landing the
   edge on the slot inside it. Measured cost of not having it:
   20,216 unresolved selector references; the register leg of the
   acceptance path stops on exactly this.
3. **Second language** — apply unchanged machinery to a second
   compiler (rustc front, or clang) to prove language-agnosticism
   by construction rather than intent.
