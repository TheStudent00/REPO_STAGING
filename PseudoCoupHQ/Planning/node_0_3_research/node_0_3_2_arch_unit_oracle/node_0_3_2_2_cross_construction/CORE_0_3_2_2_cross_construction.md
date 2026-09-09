---
id: hq.research.arch_unit_oracle.cross_construction
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: cross_construction
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md
super_node:
    name: arch_unit_oracle
    path: ../CORE_0_3_2_arch_unit_oracle.md
sub_nodes:
    - name: length_one
      path: node_0_3_2_2_0_length_one/CORE_0_3_2_2_0_length_one.md
    - name: length_two
      path: node_0_3_2_2_1_length_two/CORE_0_3_2_2_1_length_two.md
    - name: single_opcode_units
      path: node_0_3_2_2_2_single_opcode_units/CORE_0_3_2_2_2_single_opcode_units.md
    - name: autopoly
      path: node_0_3_2_2_3_autopoly/CORE_0_3_2_2_3_autopoly.md
---

# CORE 0_3_2_2 — cross_construction

## metadata

- **id:** hq.research.arch_unit_oracle.cross_construction
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit_oracle](../CORE_0_3_2_arch_unit_oracle.md)

## sub_nodes

- [length_one](node_0_3_2_2_0_length_one/CORE_0_3_2_2_0_length_one.md) — The length-one construction map: for every ordered pair of languages (x, y), the pool entries with a y member that also have an x member.
- [length_two](node_0_3_2_2_1_length_two/CORE_0_3_2_2_1_length_two.md) — The depth-2 composition search at the term level: y's layer-5 term matched at the root against x's terms with variables as holes, each hole bound to a variable, a literal, or another x term whose holes bind only to variables or literals.
- [single_opcode_units](node_0_3_2_2_2_single_opcode_units/CORE_0_3_2_2_2_single_opcode_units.md) — The two lists the owner asked for on 2026-09-05 as the precondition for construction: per language, the compiler-operators that lower to a single arch opcode (chaff = `ret` and plain register moves), and the distinct arch opcodes across all of the language's arch-units.
- [autopoly](node_0_3_2_2_3_autopoly/CORE_0_3_2_2_3_autopoly.md) — AutoPoly, the automated polyfiller: for one dominant operator (a pool entry) and one target language y, the proved source-level function in y that computes it — rendered from the entry's term by one renderer per target, compiled with y's own compiler at ship flags, carved at the function body, gated against the entry's unit — kept per (entry, y) with its proof as the polyfill library the Hub's egress composes.

## definition

Language x's arch-units as the ONLY building blocks from which every
arch-unit of language y is constructed, each construction proved by
the gate, so that the set of y's operators that x can express is
measured rather than assumed.

## status, ruled 2026-09-07

Term-level composition (length_one, length_two) stays FROZEN: under
3% at depth 2. The node is UNFROZEN on the EMULATION route (the owner,
2026-09-07, "make the updates according to our alignment"): x's
operator rebuilt from y's operations by rendering its term to y
source and letting y's compiler lower it — 76–95% proved per target,
91–93% landing on the exact primitive (o7, o8, o11) — and, as the
second producer, by direct synthesis of y's arch-units. That work is
the sub-node [autopoly](node_0_3_2_2_3_autopoly/CORE_0_3_2_2_3_autopoly.md).

## in relation to the hub compiler

This is the hub compiler's lowering with the pool restricted to one
language: for each arch-unit U of y, find a composition of x's
units whose gate verdict against U is PROVED. The measured result is
a map: which of y's operators x can build, which it cannot, and the
composition for each it can.

## what already exists for it

- Terms: 27,866 of 30,280 units carry a proved z3 term (as of
  2026-09-05). A composition's term is the substitution of its parts'
  terms, so the search runs at the term level first (symbolic,
  fast) and is confirmed at the body level by the gate (authoritative).
- Distinct bodies: 2,744 across 31,067 compiled units, 642 of them
  in more than one language. Those 642 are length-one compositions
  already found: the same body IS both languages' unit.

## why it automates polyfill

A polyfill is code in y supplying an operator y lacks. If the map
says y's operator O decomposes into x's units, and each of those
has a counterpart in y's pool (the 642 shared bodies seed that),
then the composition rewritten in y's counterparts IS the polyfill,
and it arrives proved rather than written.

## the open part

Composition search is synthesis, and synthesis over 2,744 blocks
does not enumerate. The usable structure is the term: y's term is a
tree of z3 operations and x's terms are subtrees; matching subtrees
bottom-up is rewriting, which terminates. Whether that finds
compositions the gate then confirms is the experiment.

## artifacts

`~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/`.
