---
id: hq.research.arch_unit_oracle.architectures
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: architectures
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/CORE_0_3_2_3_architectures.md
super_node:
    name: arch_unit_oracle
    path: ../CORE_0_3_2_arch_unit_oracle.md
sub_nodes:
    - name: x86_64
      path: node_0_3_2_3_0_x86_64/CORE_0_3_2_3_0_x86_64.md
    - name: riscv64
      path: node_0_3_2_3_1_riscv64/CORE_0_3_2_3_1_riscv64.md
---

# CORE 0_3_2_3 — architectures

## metadata

- **id:** hq.research.arch_unit_oracle.architectures
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit_oracle](../CORE_0_3_2_arch_unit_oracle.md)

## sub_nodes

- [x86_64](node_0_3_2_3_0_x86_64/CORE_0_3_2_3_0_x86_64.md) — The architecture the line was built on.
- [riscv64](node_0_3_2_3_1_riscv64/CORE_0_3_2_3_1_riscv64.md) — The second architecture: an exploration, not a pivot (the owner, 2026-09-10: "not that we need a hard pivot .

## definition

The architectures the oracle runs on, one sub-node each, so that the
part of the line that touches the machine is kept apart from the part
that does not. Created 2026-09-10 on the owner's word ("we could make a
super_node to contain the two nodes that each have their
architecture").

`the part that touches the machine` (per architecture, in its own node)
- the `lifter`: every `arch_opcode` of the architecture as a z3 function
  from input bits to output bits (`reference.py` for x86-64,
  `riscv_reference.py` for RISC-V); this is `level 0` for that
  architecture, and everything above it rests on it.
- the `level 0 check`: the lifter set beside a formal model of the ISA
  written by other people (K-framework for x86-64, Sail for RISC-V).
- the `carve`: cutting a compiled function's body out of a binary at its
  symbol, with that architecture's disassembler.
- the `calling convention`: which registers arrive and which answer,
  and how a narrow argument is extended; stated as a contract, so a
  difference between two architectures is a constraint and never a
  meaning.

`the part that does not touch the machine` (shared, above this node)
- the `term` (the meaning as one formula per output bit), the model
  table's `cells`, `Term.normalize`, the `bank` of certificates, the
  Lean proofs, the renderers. A certificate says "this source computes
  this term"; the term does not know its architecture.

`the claim this node measures`
- for one source unit compiled for two architectures, the two bodies'
  terms are equal. Where they are not, the cause is named and is a
  contract (the ABI, a trap rule), never a meaning.
- the `surface`: the lines that had to be written to run the pipeline
  on the new architecture, per layer. rv1 measured 2,644 lines in five
  files for RISC-V, the lifter 44% of it; everything in the shared part
  moved untouched (`DevComms/log_258`).

```
for arch in architectures:                 # x86_64, riscv64
    lifter[arch]      = level_0(arch)      # checked against the ISA's formal model
    for unit in units_compiled_for(arch):
        body  = carve(unit, arch)
        term  = lifter[arch].walk(body)    # the meaning, architecture-neutral from here on
        claim = gate(term == term_of(unit, x86_64))   # equal / differ by a named contract
```

## the two sub-nodes, in relation to each other

1. [x86_64](node_0_3_2_3_0_x86_64/CORE_0_3_2_3_0_x86_64.md) is where
   the line was built: its lifter is `reference.py` (3,093 lines), its
   level 0 check is the K-framework semantics (ref1, ref2), and every
   certificate in the bank was proved on it.
2. [riscv64](node_0_3_2_3_1_riscv64/CORE_0_3_2_3_1_riscv64.md) is the
   second architecture, an exploration and not a pivot (the owner,
   2026-09-10): its lifter is `riscv_reference.py`, its level 0 check
   is the ratified Sail model run at points, and its question is how
   much of the bank transfers by term identity (rv1 closed, rv2
   running).
