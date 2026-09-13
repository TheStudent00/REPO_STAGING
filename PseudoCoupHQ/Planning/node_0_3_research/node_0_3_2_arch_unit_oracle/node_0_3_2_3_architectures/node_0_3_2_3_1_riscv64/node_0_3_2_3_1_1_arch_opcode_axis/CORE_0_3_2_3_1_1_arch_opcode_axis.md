---
id: hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: arch_opcode_axis
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_1_arch_opcode_axis/CORE_0_3_2_3_1_1_arch_opcode_axis.md
super_node:
    name: riscv64
    path: ../CORE_0_3_2_3_1_riscv64.md
sub_nodes: []
---

# CORE 0_3_2_3_1_1 — arch_opcode_axis

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.arch_opcode_axis
- **level:** 5
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [riscv64](../CORE_0_3_2_3_1_riscv64.md)

## sub_nodes

*(none yet)*

## definition

Every RISC-V arch-opcode reached, under the owner's rule of 2026-09-13:
the method may know only what every arch-opcode gives it, its
definition from Sail and the language's primitive operators; nothing
is written because someone knows a cell is a multiply or a divide.
The two allowed routes are the language's own operator (native) and
z3's own circuit (bit-blast).

`the population`
- today: the 255 cells the riscv64-compiled corpus attests, of which
  251 are proved on at least one of c, c++, rust, go and 235 on all
  four (logs 265, 267, 268); the four left are `mulh` and `mulhsu` at
  64 bits, two operand forms each.
- next: every instruction the Sail model defines, once
  [lifter_from_sail](../node_0_3_2_3_1_0_lifter_from_sail/CORE_0_3_2_3_1_0_lifter_from_sail.md)
  makes their definitions available without a person; the model table
  swept over all of them, not only the attested ones.

`the two routes on the four`
- native: c and rust hold a 128-bit product, so the operator exists;
  the undecided verdict has a cause not yet named (a text the
  normalizer does not close, or a library routine the standing rule
  attaches); measured from the literal objects.
- bit-blast with structure preserved: compile z3's circuit with less
  rewriting so the check compares like with like; three optimization
  settings measured; rv4's optimization-off regression named from a
  pasted body.

```
for cell in riscv_cells:                    # 255 now; all of Sail's next
    for lang in (c, cpp, go, rust):
        native    = check(compile(render(cell.term, lang)))
        bitblast  = check(compile(render_gates(blast(cell.term), lang)))
        row(cell, lang, native, bitblast)   # "of 255" on every row
```

The brief: `Research/briefs/task_rv9_brief.md`.
