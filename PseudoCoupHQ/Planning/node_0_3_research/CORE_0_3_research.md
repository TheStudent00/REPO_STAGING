---
id: hq.research
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: research
    path: Planning/node_0_3_research/CORE_0_3_research.md
super_node:
    name: hq
    path: ../CORE_0.md
sub_nodes:
    - name: intentions
      path: node_0_3_0_intentions/CORE_0_3_0_intentions.md
    - name: operator_equivalence
      path: node_0_3_1_operator_equivalence/CORE_0_3_1_operator_equivalence.md
    - name: arch_unit_oracle
      path: node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md
---

# CORE 0_3 — research

## metadata

- **id:** hq.research
- **level:** 1
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [hq](../CORE_0.md)

## sub_nodes

- [intentions](node_0_3_0_intentions/CORE_0_3_0_intentions.md) — The research project that establishes what developers MEAN by a language's features, measured from the language side: what data is, how each language holds it, and what each compiler's operators do to it when run.
- [operator_equivalence](node_0_3_1_operator_equivalence/CORE_0_3_1_operator_equivalence.md) — The research project that proves which operators of which languages are the same computation at the machine level: every operator of every language, on every operand-type pair its compiler accepts, carved from the compiler's own emission as an ARCH-UNIT, rendered into one canonical form, proved against a reference simulator, and merged into ONE POOL in which units proved equivalent are one entry.
- [arch_unit_oracle](node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md) — A parallel research line, forked 2026-09-05 from the operator equivalence line ([operator_equivalence](../node_0_3_1_operator_equivalence/CORE_0_3_1_operator_equivalence.md)), that turns the arch-unit machinery on itself in three ways and uses each as an ORACLE — an independent answer that the main line's answers can be checked against.

## definition

The master plan of PCHQ's research: the one node that states the
objective every research project serves, assigns each project its
contribution to that objective, orders the work between them, and
holds the rulings all of them share. It describes no experiment
itself; each project sub-node does that.

Founded 2026-08-12 as a flat list of research lines (the owner: "PCHQ and
we will add a research sub_node to PCHQ planning and then a literal
Research folder in PCHQ"). Restructured 2026-09-06 on the owner's ruling
that each research project be its own realized sub-node holding its
own sub-nodes, "which gives the research node a different
responsibility but opens the door for some master planning with
great focus on the PCHQ objectives." The rigor rule from founding
stands: "as thorough as needed but not nearly as rigorous as our
PCv5 deep dive."

## 1. The objective

the owner, 2026-09-06, verbatim: "the objective is to create dominant
operators and types for constructing the Hub."

**The Hub** is a dictionary: key = (operator intention, input types,
output type), value = one canonical arch-unit body, with tree-sitter
supplying the nesting that turns a source tree into a sequence of
lookups joined through memory rows. It is the center of intention of
the twelve languages (AgentMemory, the vision, 2026-08-05): every
language's operator intentions held in one place, at the machine
level.

**A dominant operator** is one distinct computation, proved: the set
of every language's arch-units that compute the same function,
collapsed to one entry with one representative body, carrying its
modes (the guarded variants such as trapping versus wrapping
arithmetic) as related entries with their divergence conditions.

**A dominant type** is one machine-level holder — a class (signed
integer, unsigned integer, float, truth) at a width — with every
language's spellings for it hanging off it, so that a language type
resolves to the holder the machine distinguishes and no further.

### 1.1 How the purpose shifted, and why the plan is now this shape

- The original route was PCv5 → PseudoIR → PCv6: transpile each
  compiler, slice its lowering, insert the slice into the Hub.
- The function-wrapping probes (operator_equivalence, from 2026-08-24)
  made the lowering's OUTPUT available directly: one function body
  per (operator, operand types), read off the compiler's own
  emission. the owner, 2026-09-06: "the function wrapping probes allowed
  us to extract essentially all the arch-units."
- So the value side of the dictionary comes from the corpus, not
  from a slice. What the transpile route was also carrying, and what
  is NOT replaced, is the compiler's type checker: the dictionary's
  key needs the input types at every operator node, and a tree-sitter
  tree carries none. That gap is the largest open question in §5.

## 2. The projects, and what each contributes

- **[intentions](node_0_3_0_intentions/CORE_0_3_0_intentions.md)** —
  the language side: what data IS (layer 1, nine forms), how each
  language HOLDS it (layer 2, representations), and what each
  compiler's operators DO to a representation, measured by execution
  (layer 3, the fuzz census). Delivers the type half of the key and
  the behaviour census that names an operator's modes.
- **[operator_equivalence](node_0_3_1_operator_equivalence/CORE_0_3_1_operator_equivalence.md)**
  — the machine side: the arch-unit corpus, the canonical form, the
  proofs, the pool. Delivers the value half of the dictionary (the
  pool's entries and representatives) and the per-language routing
  table (language, operator token, operand types → entry), which is
  the probe corpus itself, produced by the compilers and never by
  hand. Was named `compiler_graph` until 2026-09-06; the compiler
  graph proper is its sub-node `graph`.
- **[arch_unit_oracle](node_0_3_2_arch_unit_oracle/CORE_0_3_2_arch_unit_oracle.md)**
  — the checks: a second way of producing the same machine code or
  the same proof from a different start, so agreement is evidence
  and disagreement is a located defect. Holds the Hub compiler
  prototype (lowering by lookup and join, gated against the original
  compiler), the operators-a-compiler-uses census, and
  cross_construction, whose term-composition study is frozen and whose
  emulation route — AutoPoly, adopted 2026-09-07 — is the research's
  route to the Hub.

## 3. What exists toward the objective, as of 2026-09-06

| piece | state | where |
|---|---|---|
| arch-unit corpus | 31,078 units, 9 languages (c 10,620 · cpp 17,840 · swift 1,322 · rust 695 · go 590 · php 4 · java 2 · ruby 2 · cpython 1) | operator_equivalence / probes, arch_unit |
| proofs | 27,866 proved · 1,676 disproved · 253 undecided · 485 no term, of 30,280 in the term store | operator_equivalence / gate, term |
| the pool | 1,831 entries over 30,432 members; 490 entries span languages | operator_equivalence / pool (`the_pool5.json`) |
| families | 34 operator families, 40 exception families | operator_equivalence / pool |
| language type inventories | scalar core: c 56 · cpp 56 · go 14 · rust 15 · swift 17 spellings, each with a class | operator_equivalence / probes / type_inventory |
| machine type keys | 88 distinct (register families \| answer width) over the pool | operator_equivalence / pool |
| data forms | layer 1 ruled complete-for-content: nine forms | intentions / data_representation |
| verified data structures | six dominants, executed across 11 languages, zero contradictions | intentions / dominant_intentions |
| fuzz census | layer 3 designed and run for the twelve; relate-and-cluster (phase 4) not run | intentions / kind_fuzz_clustering |
| compiler graphs | structural + dynamic + per-variant for go and clang; rust, swift structural only; interpreters none | operator_equivalence / graph |
| single-opcode operators | per compiled language, 10–26 of 20–32 operators lower to one arch opcode on some operand types; comparisons never | arch_unit_oracle (log_208) |

## 4. Dependencies and the order of work

### 4.1 What the dictionary needs, and which project supplies it

| the Hub needs | supplied by | state |
|---|---|---|
| one entry per distinct computation | operator_equivalence: pool entries proved equal across text differences | open (step 2) |
| one holder per machine type, with language spellings | operator_equivalence type keys joined to the language inventories through task 40's DWARF tables; intentions layer 2 for non-scalar holders | open (step 3) |
| the routing (language, token, types → entry) | operator_equivalence: the probe corpus | exists; coverage unmeasured (step 4) |
| an operator's modes | operator_equivalence exception families; intentions layer-3 fracture lists | data exists; key design is the owner's |
| the tree walk and the join | arch_unit_oracle / hub_compiler | not started (step 5) |
| input types at every tree node | the typing route — the owner's ruling (§5) | open |
| non-scalar operators (text, sequence, keyed, nesting) | operator_equivalence probes over aggregate holders; intentions layer 2 | not started (step 6) |
| the remaining seven languages | operator_equivalence / interp_feeder, remaining_languages | 11 hand-carved units; nothing else |

### 4.2 The order, agreed with the owner 2026-09-06, revised 2026-09-07

Done in the first round (2026-09-06/07): step 1 (o5, log_215); step 2's
first pass (t100, log_224: 226 proved edges, 12 applied, pool6
candidate 1,819 entries, not ratified); step 3 (t101b, log_217: 32
holders); the typing measurement (o6, log_216); the emulation studies
(o7, o8, o11: logs 218, 220, 226); the signature censuses (o9, o10);
the Lean opening (L1, log_227). The route AutoPoly → Hub, et al. was
adopted 2026-09-07 (§2, §5), so the order from here is:

1. **Layer-5 normalization** (t104, running): commutative operand
   order, with the before/after audit and the pool rebuilt over the
   new texts. operator_equivalence / term / normalize.
2. **Dominant operators, second pass**: prove the 214 unapplied edges
   on members whose own-body proof exists; the untouched 61 type-key
   groups; families over the merged entries. operator_equivalence / pool.
3. **The arch-opcode loop and its model** (the owner, 2026-09-07;
   arch_unit_oracle CORE "goal"): the full model of the 162 members of
   `set_of_unique_arch_opcodes` from the reference simulator, keyed by
   (mnemonic, operand form, width) — the ruling of 2026-09-08 in the
   arch_unit_oracle CORE — with the corpus's attestation and the alias/split
   report beside the 162 (task m1, after the `mnem` rename, task mn1; both
   on the tower); then the owner's loop, every opcode × every language,
   with `find_emulation` printers for go, swift and the interpreted
   languages and a check for interpreted targets; the fit study
   (log_234). Runs only after the portable Airlock is on the server.
   Then **AutoPoly**, arch_unit_oracle / cross_construction / autopoly:
   render the MODE (guards) so trapping operators trap; the synthesis
   route as the second producer; size and cycles against native
   units; go and swift renderers after rust.
4. **The proof system**, operator_equivalence / gate / lean: the model
   translator first, then comparisons and connectives, the rust
   expression type, guarded division, the float model.
5. **Hub v1**: the dictionary from the corpus with coverage and holes;
   one explicitly typed go file lowered as SOURCE COMPOSITION of
   AutoPoly emulations, gated against go's own output.
   arch_unit_oracle / hub_compiler.
6. Aggregate forms, then the remaining languages.
   operator_equivalence with intentions.

## support

- [SUPPORT_BRAINSTORM_autopoly.md](SUPPORT_BRAINSTORM_autopoly.md) —
  AutoPoly → Hub, et al.: the automated polyfiller (proved
  source-level emulations of dominant operators per target language)
  as the route in place of PCv5 → PseudoIR → PCv6. Opened 2026-09-06
  from the owner's commentary on task o7 (log_219); ADOPTED 2026-09-07 (§5);
  the proof system beneath it in its §9 (logs 228, 229).

## 5. Open, and the owner's to rule

Ruled 2026-09-07 ("make the updates according to our alignment"),
recorded here so they are not re-asked: the typing route is the
language's own front end run once as a type oracle (o6's measurement);
cross_construction is unfrozen on the emulation route with AutoPoly as
its sub-node; hub_compiler lowers by source composition; the lean node
is the operator-mapping proof system with the model translator first;
the synthesis route opens as a task beside the compiler route.

Still open:

- **Whether the dictionary key carries a mode axis** (wrap / trap /
  checked), or the Hub picks the target language's mode by policy.
  Rendering the mode (order §4.2 item 3) produces the data this
  ruling needs.
- **Ratification of the pool6 candidate** (`pool100_pool6_candidate.json`,
  1,819 entries) into `the_pool6.json`, or waiting for t104's rebuild
  and the second pass.
- **type_vocabulary**: superseded 2026-08-15; whether it moves to
  `.archive/` or stays in place under intentions.

## 6. Rulings shared by every project

Each is recorded in full in `PseudoCoupHQ/AgentMemory.md`;
a project CORE restates only the ones it adds to.

- The unit boundary is a function body, read from the symbol table
  and DWARF (2026-09-04).
- The canonical form keeps the body unchanged; loads and stores only
  at the edges (2026-09-02, corrected reading 2026-09-05).
- The spelling ban: no operator token in any key, grouping, pairing
  or comparison scope; the mechanical guard runs on every artifact
  (2026-08-25).
- The three-layer anchor: every research work package states which
  of data / representation / operation it serves (2026-08-15).
- The evidence doctrine: forced-by-construction > the tool's own
  testimony > interpretation; every claim names its class
  (2026-08-24).
- All compute through Airlock; memory bound stated per task; every
  report's claims re-runnable and attributed to a lane log
  (2026-09-04, 2026-09-05).
- Vocabulary: super / sub / co-node, never the familial words; ABORT,
  never the death words.
- Planning: this tree conforms to `PlanPlan/framework/PROTOCOL.md`;
  level-0 and level-1 COREs change only through the owner; a lower node
  refines, never contradicts, its super-node.

## 7. Where things are recorded

- Artifacts: `PseudoCoupHQ/Research/<project or line>/`
  (`kind_signature_clustering/`, `dominant_intentions/`,
  `kind_fuzz_clustering/`, `data_representation/`, `op_pipeline/`,
  `compiler_graph/`, `oracle/`; graphs in `PseudoCoupGraphs/`).
- The record of what was learned: `PseudoCoupHQ/DevComms/`,
  numbered per repo, shared by every project; a log names its
  project in its first line.
- Standing shape: this tree. Progress: each node's `PROGRESS.md`.

## 8. Address map for readers of logs written before 2026-09-06

| before | now |
|---|---|
| `node_0_3_0_kind_signature_clustering` | `node_0_3_0_intentions/node_0_3_0_0_kind_signature_clustering` |
| `node_0_3_1_dominant_intentions` | `node_0_3_0_intentions/node_0_3_0_1_dominant_intentions` |
| `node_0_3_2_kind_fuzz_clustering` | `node_0_3_0_intentions/node_0_3_0_2_kind_fuzz_clustering` |
| `node_0_3_3_type_vocabulary` | `node_0_3_0_intentions/node_0_3_0_3_type_vocabulary` |
| `node_0_3_4_data_representation` | `node_0_3_0_intentions/node_0_3_0_4_data_representation` |
| `node_0_3_5_compiler_graph` and its `node_0_3_5_<i>_*` | `node_0_3_1_operator_equivalence` and `node_0_3_1_<i>_*` (same i) |
| `node_0_3_6_interp_feeder` | `node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder` |
| `node_0_3_7_remaining_languages` | `node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages` |
| `node_0_3_8_arch_unit_oracle` | `node_0_3_2_arch_unit_oracle` |

Ids did not change, except `hq.research.compiler_graph`, superseded
by `hq.research.operator_equivalence` (the rename rule). DevComms
logs keep their original addresses as written; this table resolves
them.
