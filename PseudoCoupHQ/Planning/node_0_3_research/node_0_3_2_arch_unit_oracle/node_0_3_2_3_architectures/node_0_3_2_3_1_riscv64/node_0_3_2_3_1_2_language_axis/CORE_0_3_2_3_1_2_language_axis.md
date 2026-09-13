---
id: hq.research.arch_unit_oracle.architectures.riscv64.language_axis
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: language_axis
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_2_language_axis/CORE_0_3_2_3_1_2_language_axis.md
super_node:
    name: riscv64
    path: ../CORE_0_3_2_3_1_riscv64.md
sub_nodes: []
---

# CORE 0_3_2_3_1_2 — language_axis

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.language_axis
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

Every language PCHQ covers, against the RISC-V definitions.

`the compiled languages`
- c, c++, rust, go: in the table today ("of 255" per language, logs
  265–268).
- swift: the compiler in the image knows the riscv64 target and names
  a runtime directory that does not exist; whether a Swift SDK or a
  community toolchain for riscv64 Linux can be installed is measured
  with the network on, commands and outputs pasted; a swift column
  "of 255" if one installs, a flag if none does.

`the interpreted seven`
- cpython, php, ruby, java, javascript, dart, csharp: no machine body
  exists, so the route is AGREEMENT at points, edge values first, at
  most 20,000 points, recorded `agreed` and never proved; each
  emulation rendered by the same general render into the interpreted
  language and run beside the definition. "of 255" per interpreter
  and on all seven, beside x86's 162–166 of 253.

```
for cell in riscv_cells:
    for lang in compiled:      proved[cell][lang] = check(compile(render(cell.term, lang)))
    for lang in interpreted:   agreed[cell][lang] = run_at_points(render(cell.term, lang), cell.term)
```

The brief: `Research/briefs/task_lx1_brief.md`.
