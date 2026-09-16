---
id: hq.research.lean_proof_path_resistant_to_churn.language.render
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: render
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_4_language/node_0_3_3_4_3_render/CORE_0_3_3_4_3_render.md
super_node:
    name: language
    path: ../CORE_0_3_3_4_language.md
sub_nodes: []
---

# CORE 0_3_3_4_3 — render

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.language.render
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [language](../CORE_0_3_3_4_language.md)

## sub_nodes

*(none yet)*

## definition

`render(language, definition) -> source | Refusal`

Input: an arch-opcode's definition as a `LeanExpr`: Sail's own text of
the execute clause with its reads made parameters (`sail_model.strip`),
parsed into a tree (the parser that exists in
`Research/oracle/riscv/leanpath/leanpath/lean_to_z3.py`, kept without
its z3 evaluation; no z3 term is built). Output: source text in this
language whose compiled body computes the definition, built from
`operator_for` and nothing else.

Steps, in order:

1. walk the tree bottom-up; at each node name its primitive and the
   widths of its operands (`LeanExpr.primitives`)
2. look up `operator_for[(primitive, widths)]`; take the first unit
3. copy that unit's source into the output verbatim (its function, byte
   for byte: the proven piece is not re-spelled) and write a call to it
   over the operands' names
4. no entry: `compose_at_width`; still none: return a `Refusal` naming
   the primitive and its widths
5. a conditional in the definition: the unit of the language's own
   conditional operator from `operator_for`, if the probe set carries
   one for the language; else a `Refusal`
6. wrap the whole as one function over the definition's inputs (the
   language's function syntax and its call syntax: plumbing, written
   once per language) and return the source

What it does not do: choose an operator by its spelling, know a
mnemonic, simplify, search, or hold any table of its own. One source,
one candidate, every piece of it proved by pass A.

Home: a new file `Research/oracle/riscv/leanpath/leanpath/render.py`.
Retired (see `the_run.retire_drifted_code`): the route through
`construct.py` and the earlier renderer `render_general.py`, whose table
from term nodes to operators was written by hand.
