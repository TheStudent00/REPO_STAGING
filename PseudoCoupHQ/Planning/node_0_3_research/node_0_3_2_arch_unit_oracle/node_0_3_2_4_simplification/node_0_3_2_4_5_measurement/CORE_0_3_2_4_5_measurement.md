---
id: hq.research.arch_unit_oracle.simplification.measurement
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: measurement
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_4_simplification/node_0_3_2_4_5_measurement/CORE_0_3_2_4_5_measurement.md
super_node:
    name: simplification
    path: ../CORE_0_3_2_4_simplification.md
sub_nodes:
    - name: benchmark
      path: node_0_3_2_4_5_0_benchmark/CORE_0_3_2_4_5_0_benchmark.md
    - name: report
      path: node_0_3_2_4_5_1_report/CORE_0_3_2_4_5_1_report.md
---

# CORE 0_3_2_4_5 — measurement

## metadata

- **id:** hq.research.arch_unit_oracle.simplification.measurement
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [simplification](../CORE_0_3_2_4_simplification.md)

## sub_nodes

- [benchmark](node_0_3_2_4_5_0_benchmark/CORE_0_3_2_4_5_0_benchmark.md) — `Benchmark` - the fixed body set drawn from `Population`, frozen by code_version, so a later run compares against the same bodies.
- [report](node_0_3_2_4_5_1_report/CORE_0_3_2_4_5_1_report.md) — `report(results) -> table` - rows keyed (lang, cell, method): the metric, the cost line, the guarantee; guard over the json; the collapse-missed count is the headline.

## definition

One benchmark for every path, so the paths are compared on the same
bodies with the same metric.

`benchmark`
- the emulator arch-units the compiler did not collapse (ap6, t2, t4),
  per language, with the cell each emulates.

`metric`, per body and method
- reduced to the one instruction the cell names / shorter than the
  compiler's body / unchanged; the instruction count before and after;
  seconds and z3 calls; and the guarantee the number carries (sub-node 6).
