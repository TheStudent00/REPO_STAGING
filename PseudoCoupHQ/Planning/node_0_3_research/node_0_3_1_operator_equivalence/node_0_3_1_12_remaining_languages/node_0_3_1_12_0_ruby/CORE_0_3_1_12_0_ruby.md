---
id: hq.research.remaining_languages.ruby
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: work
node:
    name: ruby
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages/node_0_3_1_12_0_ruby/CORE_0_3_1_12_0_ruby.md
super_node:
    name: remaining_languages
    path: ../CORE_0_3_1_12_remaining_languages.md
sub_nodes: []
---

# CORE 0_3_1_12_0 — ruby

## metadata

- **id:** hq.research.remaining_languages.ruby
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [remaining_languages](../CORE_0_3_1_12_remaining_languages.md)

## sub_nodes

*(none yet)*

## definition

Ruby's route into the corpus: the interpreter shape. The operator's
machine code is a handler in the ruby 3.3.0 binary (`rb_fix_plus`,
`rb_int_plus` for `+`; `rb_big_plus` and `vm_opt_plus` have no ship
body and are refused by name), carved at the function body. Four
units exist, from the handler-slice work of logs 095 and 113
(`build_op_units_ruby.py`, `canon_interp_units_ruby_php.json`). What
is not done: the operator SET — probes generated from
`operator_arity.json` over ruby's holders, with the handler each
reaches located by the diary over ruby's source rather than by hand.
