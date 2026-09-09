---
id: hq.research.remaining_languages.php
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: work
node:
    name: php
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages/node_0_3_1_12_1_php/CORE_0_3_1_12_1_php.md
super_node:
    name: remaining_languages
    path: ../CORE_0_3_1_12_remaining_languages.md
sub_nodes: []
---

# CORE 0_3_1_12_1 — php

## metadata

- **id:** hq.research.remaining_languages.php
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

PHP's route into the corpus: the interpreter shape. The operator's
machine code is a Zend handler (`ZEND_ADD_LONG_NO_OVERFLOW_SPEC_…`,
`ZEND_ADD_LONG_SPEC_…`, `ZEND_ADD_SPEC_…`, `add_function`) in the
instrumented php 8.3.0 build, carved at the function body. Four
units exist (logs 095, 113; `build_op_units_php.py`,
`interp_php.md`). PHP's handler frame is the case that forced the
seventh block kind: the handler works through `%r15` as a bytecode
pointer into an arriving area (log_201). Not done: the operator set
by generated probes and diary-located handlers, as for ruby.
