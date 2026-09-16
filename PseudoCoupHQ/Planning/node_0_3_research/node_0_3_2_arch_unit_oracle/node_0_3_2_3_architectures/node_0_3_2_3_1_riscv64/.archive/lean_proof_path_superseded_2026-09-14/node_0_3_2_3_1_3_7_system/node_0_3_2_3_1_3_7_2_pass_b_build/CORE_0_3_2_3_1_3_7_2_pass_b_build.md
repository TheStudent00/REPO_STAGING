---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system.pass_b_build
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: pass_b_build
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_7_system/node_0_3_2_3_1_3_7_2_pass_b_build/CORE_0_3_2_3_1_3_7_2_pass_b_build.md
super_node:
    name: system
    path: ../CORE_0_3_2_3_1_3_7_system.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_7_2 — pass_b_build

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.system.pass_b_build
- **level:** 7
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [system](../CORE_0_3_2_3_1_3_7_system.md)

## sub_nodes

*(none yet)*

## definition

`pass_b_build(defs, langs, dictionary)`

Input: the same, after pass A. Output: entries for every (language, definition) pass A left empty.

Steps, in order:

1. for every definition, for every language with no entry: `source = render(definition)`; `unit = compile(source)`; `unit.lean = meaning(unit, defs)`
2. if `equals(definition, unit.lean)` proves, add an `Emulation` marked built
3. else record the row with the stage: render refused, compile failed, walk refused, differ, undecided
