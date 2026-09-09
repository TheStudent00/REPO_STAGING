---
id: hq.research.arch_unit_oracle.hub_compiler
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: hub_compiler
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_1_hub_compiler/CORE_0_3_2_1_hub_compiler.md
super_node:
    name: arch_unit_oracle
    path: ../CORE_0_3_2_arch_unit_oracle.md
sub_nodes:
    - name: front_end
      path: node_0_3_2_1_0_front_end/CORE_0_3_2_1_0_front_end.md
    - name: dictionary
      path: node_0_3_2_1_1_dictionary/CORE_0_3_2_1_1_dictionary.md
    - name: joiner
      path: node_0_3_2_1_2_joiner/CORE_0_3_2_1_2_joiner.md
    - name: oracle_test
      path: node_0_3_2_1_3_oracle_test/CORE_0_3_2_1_3_oracle_test.md
---

# CORE 0_3_2_1 — hub_compiler

## metadata

- **id:** hq.research.arch_unit_oracle.hub_compiler
- **level:** 3
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit_oracle](../CORE_0_3_2_arch_unit_oracle.md)

## sub_nodes

- [front_end](node_0_3_2_1_0_front_end/CORE_0_3_2_1_0_front_end.md) — The reader of the file to be lowered: tree-sitter parses it; the tree's nesting is the data flow (a sub-node's value is an operand of its super-node); at each operator node the front end must also know the operand TYPES, which the tree does not carry.
- [dictionary](node_0_3_2_1_1_dictionary/CORE_0_3_2_1_1_dictionary.md) — The Hub's lookup: key (language, operator token, operand holder types) → dominant operator entry → representative canonical body.
- [joiner](node_0_3_2_1_2_joiner/CORE_0_3_2_1_2_joiner.md) — The emitter of the row traffic between entries: a post-order walk of the tree in which a sub-node's entry stores its answer into a memory row (the canonical form's epilogue) and the super-node's entry loads that row as an operand (its prelude); one row per tree edge; the prelude and epilogue are the canonical form's own ([canonical_form](../../../node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md)).
- [oracle_test](node_0_3_2_1_3_oracle_test/CORE_0_3_2_1_3_oracle_test.md) — Step 5 of the master order and the sub-node's reason to exist: for one source file, body A = what the language's own compiler emits, carved at the function body; body B = what the dictionary and joiner emit; the gate run over A and B exactly as over two units.

## definition

Our own Hub-like compiler: a lowering that reads a source file
through tree-sitter, types each operator node by the language's own
front end run once as a type oracle (ruled 2026-09-07 on o6's
measurement: go/types typed 79,799 of 103,475 sites at 541 MB and
160 s), resolves each node to its dominant operator, and emits target
SOURCE composed from AutoPoly's proved emulations, one per node, so
that the target's own compiler lowers and optimizes ACROSS the
operators; its output is compared by the gate against what the
original compiler emits for the same file.

Ruled 2026-09-07 (the owner: "make the updates according to our
alignment"). The founding definition of 2026-09-05 — one canonical
BODY per operator node joined through the canonical form's memory
rows — is kept below under its date as the superseded form: it is
still the shape of the oracle test's two bodies, and it is what the
source composition replaces at egress.

## why source composition replaces the memory-row join

- The row join by construction cannot optimize across operators; y's
  compiler can, and does (o7: 82–95% of rendered emulations prove
  equivalent; o8, o11: 91–93% land on the exact primitive).
- The proofs are done once per (dominant operator, target language)
  and reused; the per-file oracle test stays as the check.
- Correction to the founding text's "why it may vectorize": the map
  over operator nodes is now a map over source functions; the
  optimizer's cross-operator work is the thing gained.

## the founding definition, 2026-09-05, superseded 2026-09-07

Our own Hub-like compiler: a lowering that reads a source file
through tree-sitter (and, where it applies, the ledgerer), walks the
tree's nesting, places one pool entry (a proved arch-unit body) per
operator node, joins the entries through the canonical form's memory
rows along the tree's edges, and compares its output by the gate
against what the original compiler emits for the same file.

## why "Hub-like"

The Hub (AgentMemory, the vision, 2026-08-05) is the center of
intention: every language's operator intentions held in one place.
The pool is that center at the machine level — one entry per
distinct computation, members from every language. A compiler that
lowers through the pool lowers through the Hub.

## the lowering, mechanically

- **Front end:** tree-sitter parses the file into its concrete
  syntax tree. Each operator node has operand sub-nodes; the tree's
  nesting IS the data flow: a sub-node's value is an operand of its
  super-node. The ledgerer (PCv5 `ts_to_ur`, `ur_to_ledger`) is the
  existing tool that already reads such trees into operator rows
  with types; whether it is used as-is or only its tree walk is
  taken is decided when the first file is lowered.
- **Dictionary step:** for each operator node, with the operand
  types the tree resolves, look up the pool entry proved for that
  computation and take its canonical body.
- **Join:** walk the tree in post-order. A sub-node's entry stores
  its answer into a memory row (its epilogue); the super-node's
  entry loads that row as an operand (its prelude). One row per
  tree edge. The prelude and epilogue are the canonical form's own.
- **Output:** one body B, in canonical form, for the whole file.

## the oracle test, exactly

- Body A: what the language's own compiler emits for the file,
  carved by the function-body rule.
- Body B: what the lowering above emits.
- Run the gate over A and B as it runs over two units today.
    - PROVED: the pool entries hold in context. The guard-rail.
    - DISPROVED, counterexample: a pool entry wrong in context (a
      main-line defect, located to the entry) or an optimisation
      across operators in the original compiler that the
      node-by-node model lacks. The counterexample says which.
    - NO_TERM / UNDECIDED: outside the walk's reach; cause table.

## why lowering may vectorize (unverified)

Each operator node's lowering is an independent lookup; the join is
the same prelude/epilogue on every edge; so lowering a tree is a map
over its operator nodes with the rows fixed by the edges. Register
allocation across operators, the usual dependence, is absent because
every value crosses between entries through a row. The emitted code
is slower; speed is not this node's objective.

## why it may slice (unverified)

Every value in B is a named row by construction, and the row is a
tree edge. When the gate proves A equivalent to B, the proof says
which register of A holds each edge's value — a slice of the
original compiler's output tied to the source tree, obtained without
walking the compiler.

## artifacts

`PseudoCoupHQ/Research/oracle/hub_compiler/`.
