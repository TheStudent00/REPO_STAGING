---
id: hq.research.operator_equivalence
level: 2
status: draft
settled_by: the owner
supersedes: hq.research.compiler_graph
designation: grouping
node:
    name: operator_equivalence
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/CORE_0_3_1_operator_equivalence.md
super_node:
    name: research
    path: ../CORE_0_3_research.md
sub_nodes:
    - name: probes
      path: node_0_3_1_0_probes/CORE_0_3_1_0_probes.md
    - name: arch_unit
      path: node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md
    - name: canonical_form
      path: node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md
    - name: ledger
      path: node_0_3_1_3_ledger/CORE_0_3_1_3_ledger.md
    - name: reference
      path: node_0_3_1_4_reference/CORE_0_3_1_4_reference.md
    - name: gate
      path: node_0_3_1_5_gate/CORE_0_3_1_5_gate.md
    - name: term
      path: node_0_3_1_6_term/CORE_0_3_1_6_term.md
    - name: pool
      path: node_0_3_1_7_pool/CORE_0_3_1_7_pool.md
    - name: guard
      path: node_0_3_1_8_guard/CORE_0_3_1_8_guard.md
    - name: graph
      path: node_0_3_1_9_graph/CORE_0_3_1_9_graph.md
    - name: dashboard
      path: node_0_3_1_10_dashboard/CORE_0_3_1_10_dashboard.md
    - name: interp_feeder
      path: node_0_3_1_11_interp_feeder/CORE_0_3_1_11_interp_feeder.md
    - name: remaining_languages
      path: node_0_3_1_12_remaining_languages/CORE_0_3_1_12_remaining_languages.md
---

# CORE 0_3_1 — operator_equivalence

## metadata

- **id:** hq.research.operator_equivalence
- **level:** 2
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** hq.research.compiler_graph

## super_node

- [research](../CORE_0_3_research.md)

## sub_nodes

- [probes](node_0_3_1_0_probes/CORE_0_3_1_0_probes.md) — The module that turns a language's operator vocabulary into compiled machine code, one probe per (operator × operand types), with no hand written probe anywhere.
- [arch_unit](node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md) — One operator, in one language, on one operand-type pair, as the machine code the compiler emitted for it — plus the facts needed to run and compare that code: which register each argument arrives in, which register (or memory) the answer leaves in, and the bytes of any routine of the compiler's own runtime the body jumps into.
- [canonical_form](node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md) — THE one form every arch-unit is rendered into so that units from different compilers become comparable and stay runnable: the compiler's body kept character-for-character, between a standardized PRELUDE that loads each argument out of a memory row into the register the compiler expects it in, and a standardized EPILOGUE that stores the compiler's result register into the answer's row.
- [ledger](node_0_3_1_3_ledger/CORE_0_3_1_3_ledger.md) — The table beside every canonical unit with one row per value that moves through it — input, constant, temporary, own stack address, machine-stack slot, x87 slot, guard outcome, answer — each row carrying its block, its type, the arch opcode (or opcode pair) that PRODUCED it, and the rows that opcode READ.
- [reference](node_0_3_1_4_reference/CORE_0_3_1_4_reference.md) — THE one symbolic simulator of the machine that every proof in this research is made against.
- [gate](node_0_3_1_5_gate/CORE_0_3_1_5_gate.md) — The proof obligations and the object that discharges them.
- [term](node_0_3_1_6_term/CORE_0_3_1_6_term.md) — A unit's computation as a z3 expression, read off its ledger from OUT-0 downward (layer 4), and that expression printed by one fixed rule so that two units computing the same thing print the same characters (layer 5).
- [pool](node_0_3_1_7_pool/CORE_0_3_1_7_pool.md) — ONE pool of every canonicalized arch-unit of every language, in which units proved equivalent collapse into one entry.
- [guard](node_0_3_1_8_guard/CORE_0_3_1_8_guard.md) — The mechanical enforcement of the spelling ban: a function that walks any artifact the pipeline reads or writes and fails on an operator token in any key, grouping, pairing, row structure or comparison scope.
- [graph](node_0_3_1_9_graph/CORE_0_3_1_9_graph.md) — Each compiler and interpreter analyzed AS A GRAPH: its own source parsed into a static structure (tree-sitter CST nodes and the call / read / write edges between them), joined to a dynamic structure (the diary — which of those nodes each probe's compilation visited, in order), and joined a THIRD way: to each operator's traced variant, so that the graph carries the connections belonging to that variant and not only the union over all probes.
- [dashboard](node_0_3_1_10_dashboard/CORE_0_3_1_10_dashboard.md) — The interactive page that reads the current artifacts and shows the research as it stands, so that the state of the line is inspected rather than reported.
- [interp_feeder](node_0_3_1_11_interp_feeder/CORE_0_3_1_11_interp_feeder.md) — The retrofit that lets an interpreted or JIT-compiled language enter the operator-equivalence pipeline at the arch-unit step: it reads what the interpreter or its JIT itself produced for an operator (a handler function's body, or the JIT's emitted machine code with its own dump of what it did) and writes it in the record shape the compiled probes already have, so everything after [arch_unit](../node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md) runs unchanged.
- [remaining_languages](node_0_3_1_12_remaining_languages/CORE_0_3_1_12_remaining_languages.md) — The per-language route, one sub-node per language, for the target languages that have no arch-unit corpus: how each one's operators become arch-units, given that none of them compiles our wrapper function to a machine-code body the way c, cpp, go, rust and swift do.

## definition

The research project that proves which operators of which languages
are the same computation at the machine level: every operator of
every language, on every operand-type pair its compiler accepts,
carved from the compiler's own emission as an ARCH-UNIT, rendered
into one canonical form, proved against a reference simulator, and
merged into ONE POOL in which units proved equivalent are one entry.
It is the machine-level half of the objective in
[research](../CORE_0_3_research.md) §1: it supplies the dominant
OPERATORS (the pool's entries) and the per-language routing from
(operator token, operand types) to entry, which is the probe corpus
itself; the language-level half is
[intentions](../node_0_3_0_intentions/CORE_0_3_0_intentions.md).

### the name

This node was `compiler_graph` from its founding on 2026-08-24 until
2026-09-06, when the owner's restructure made it the project node and the
name followed the project's content: eleven sub-nodes of which the
compiler graph is one ([graph](node_0_3_1_9_graph/CORE_0_3_1_9_graph.md)).
Per the framework's rename rule the id `hq.research.compiler_graph`
is superseded by `hq.research.operator_equivalence`; every sub-node
keeps its id. The founding definition is kept in §1 because the
standing rules in §3 were written under it.

## 1. The founding definition (2026-08-24), now the graph sub-node's

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
`PseudoCoupHQ/DevComms/log_072_compiler_graph_tracing.md`.

The ultimate goal stated then: use the flow graphs to map a HIGH
LEVEL NAMED VARIABLE to its LOW LEVEL OPERAND. That target sets the
scope: model what is easy; beyond that, build ONLY enough to prove
which low-level operands are which high-level named variables.
Completeness of the compiler model is not the objective;
sufficiency of the identity proof is.

What happened next: the function-wrapping probes (§2, step 1) made
each operator's lowered form available directly from the compiler's
emission, so the pipeline from probe to pool became the project's
body and the graph one instrument beside it. The graph keeps its
own goal and its own open items in its sub-node.

## 2. The pipeline, as sub-nodes, with the state of each

Read top to bottom: each step consumes the one above.

| step | sub-node | one sentence | state 2026-09-06 |
|---|---|---|---|
| 1 | [probes](node_0_3_1_0_probes/CORE_0_3_1_0_probes.md) | operator vocabulary × holder types → one compiled function per pair, accepted or refused by the compiler itself | 1,779 original (6 holders per language) + 29,288 regenerated (the scalar core: c 56 · cpp 56 · go 14 · rust 15 · swift 17) |
| 2 | [arch_unit](node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md) | one probe's machine code, carved at the function body, with its arrival and answer facts and any runtime callee body attached | 31,078 units, 9 languages |
| 3 | [canonical_form](node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md) | the body verbatim between a prelude that loads arguments from memory rows and an epilogue that stores the answer | canon40, current |
| 4 | [ledger](node_0_3_1_3_ledger/CORE_0_3_1_3_ledger.md) | one row per value moving through the unit, with the arch opcode that produced it and the rows it read | canon40 ledgers; 49,362 runtime-callee rows (task 78) |
| 5 | [reference](node_0_3_1_4_reference/CORE_0_3_1_4_reference.md) | the one symbolic simulator of the machine every proof is made against | `reference.py`; machine stack and x87 built (task 91) |
| 6 | [gate](node_0_3_1_5_gate/CORE_0_3_1_5_gate.md) | the proof obligations and the object that discharges them, with a solver ceiling of 3,000 ms wall clock | 27,866 proved · 1,676 disproved · 253 undecided · 485 no term, of 30,280 |
| 7 | [term](node_0_3_1_6_term/CORE_0_3_1_6_term.md) | the unit as a z3 expression read off its ledger, printed by one fixed rule so equal computations print equal text | 30,280 records; 44 proved units whose layer-5 text never converges |
| 8 | [pool](node_0_3_1_7_pool/CORE_0_3_1_7_pool.md) | one entry per distinct computation; families over entries; exception families over guards | `the_pool5.json`: 1,831 entries / 30,432 members; 34 families; 40 exception families; pool6 not built (blocked on the 44) |
| — | [guard](node_0_3_1_8_guard/CORE_0_3_1_8_guard.md) | the mechanical enforcement of the spelling ban over every artifact | runs on every stage's output |
| — | [graph](node_0_3_1_9_graph/CORE_0_3_1_9_graph.md) | each compiler's own source as a graph: static structure, the diary, per-operator-variant connections | go and clang all three kinds; rust, swift structural; interpreters none |
| — | [dashboard](node_0_3_1_10_dashboard/CORE_0_3_1_10_dashboard.md) | the page that reads the artifacts and shows the line as it stands; chronology is raw `git log` | five panes, 136 explained rows |
| 2′ | [interp_feeder](node_0_3_1_11_interp_feeder/CORE_0_3_1_11_interp_feeder.md) | interpreters and JITs entering at step 2: their handler bodies or emitted code turned into unit records | 11 units (java 2, cpython 1, php 4, ruby 4), on the canonical form |
| 1′ | [remaining_languages](node_0_3_1_12_remaining_languages/CORE_0_3_1_12_remaining_languages.md) | the per-language route for the seven languages without a probe corpus | plans; no corpus yet |

## 3. The standing rules (each one was repeated in conversation until it hurt; none is re-litigable without the owner)

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
  (`PseudoCoupHQ/Research/kind_fuzz_clustering/operator_arity.json`).
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
- **The unit boundary is a function body** (2026-09-04), read from
  the symbol table and DWARF, never computed by taint propagation.
- **The canonical form keeps the body unchanged** (2026-09-02, read
  correctly 2026-09-05): loads at the front, the body verbatim, a
  store at the back. `%r15` collisions were an artifact of the
  misreading; never fix them by moving a base register.
- **Library calls are attached, never excluded.** A `call __divti3`
  is a runtime callee whose body is extracted from the toolchain
  archive and attached to the unit (2026-08-31, round 12).
- **Time and memory limits are flags.** Re-run with more room and
  report whether the answer changed; never change what is measured
  to make it fit.

## 4. The ratified pipeline (the owner, 2026-08-24: "we are well aligned")

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

Where the ratified steps live now: 1 → probes; 2–3 → arch_unit;
4 → arch_unit / arrival_contract and ledger; 5 → canonical_form,
ledger, term; 6–7 → gate and pool / merge_grounds; 8 → pool /
families. The "sem" of step 5 became the term.

## 5. What this project delivers to the Hub, and what stands between

From [research](../CORE_0_3_research.md) §4:

- **Delivered:** the value side (pool entries, each with a
  representative body of fewest bytes) and the routing (each
  probe's language, token and holder types → its entry).
- **Step 2 of the master order, dominant operators:** the pool
  merges on identical layer-5 text; equal computations with
  different texts stay separate (5,095 entries under text identity
  alone against 1,831 merged). The dominant operator is the union
  of entries the solver proves equal, term against term, inside
  each machine type key (88 keys). Owner: pool.
- **Step 3, dominant types:** join the language inventories
  (spellings with a class) to the pool's machine keys (register
  family | width) through task 40's DWARF parameter tables. Owner:
  probes / type_inventory.
- **Step 4, the Hub v1 dictionary** with per-language coverage over
  operator × core type. Owner: pool; read by
  [arch_unit_oracle / hub_compiler](../node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/CORE_0_3_2_1_hub_compiler.md).
- **Step 6, aggregate holders and the remaining languages:** probes
  over text, sequence, keyed and nesting holders; the interpreted
  languages through interp_feeder and remaining_languages.

## 6. Open, in order (the graph's own items, kept from the founding)

1. **The diary** — id-emission instrumentation of the compiler's
   own source (the inject_emitid pattern), giving visit ORDER;
   supersedes the tally. Done for go and clang (tasks 81, 87);
   rust blocked on fetch, swift unstartable here — flagged, not
   redefined.
2. **Follow the dot** — resolution of `x.field` references by
   finding which declaration `x` is an instance of and landing the
   edge on the slot inside it. Measured cost of not having it:
   20,216 unresolved selector references.
3. **All nine compilers and interpreters** — the owner's ruling
   2026-09-05: "completed" means all nine, three connection kinds;
   a machine limit is a measured obstacle, never a redefinition.

And the pool's: the 44 units whose layer-5 text never converges
(the owner's, handoff log_204 §4.2); the solver ceiling (3,000 ms, ditto
§4.3); `AREA_SPAN` 0x100 against two java units needing 0x538.

## support

- [SUPPORT_scaling_design.md](SUPPORT_scaling_design.md) — the road
  to the remaining eight languages and the deferred operator
  buckets: JIT warm-up track (dump switches, deopt as a mode),
  interpreter track (the handler slice — the interpreter plays the
  compiler's role, the map+diary+tally toolkit transfers), the
  milestone accounting (51 dom_ops, 142/142 measured nodes),
  compound assignment as owed work. CPython ruled first (the owner,
  2026-08-26).

## artifacts

- The pipeline: `PseudoCoupHQ/Research/op_pipeline/`
  (canon40 stores, `term66_store/`, `the_pool5.json`,
  `the_families5.json`, `exception_families5.json`, `reference.py`,
  `gate.py`, `canonical_form.py`, `check_no_spelling_keys.py`,
  `check_conventions_log_claims.py`, `dashboard_ouro.py`).
- The graph: `PseudoCoupHQ/Research/compiler_graph/`
  (`build_graph.py`, `query_path.py`, `graph_walk.html`) and the
  graphs themselves in `PseudoCoupGraphs/` (no remote,
  by design; compact form 72 MB).
- The record: PCHQ DevComms logs 072 to 204, with the round-by-round
  state in each sub-node's PROGRESS.
