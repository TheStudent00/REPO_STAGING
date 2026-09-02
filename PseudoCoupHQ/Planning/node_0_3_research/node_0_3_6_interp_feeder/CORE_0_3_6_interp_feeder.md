---
id: hq.research.interp_feeder
level: 2
status: draft
settled_by: the owner
designation: task
node:
    name: interp_feeder
    path: Planning/node_0_3_research/node_0_3_6_interp_feeder/CORE_0_3_6_interp_feeder.md
super_node:
    name: research
    path: ../CORE_0_3_research.md
sub_nodes:
    - name: feeder_config
      path: node_0_3_6_0_feeder_config/CORE_0_3_6_0_feeder_config.md
    - name: parse_interp
      path: node_0_3_6_1_parse_interp/CORE_0_3_6_1_parse_interp.md
    - name: format_canon
      path: node_0_3_6_2_format_canon/CORE_0_3_6_2_format_canon.md
    - name: invoke_normalizer
      path: node_0_3_6_3_invoke_normalizer/CORE_0_3_6_3_invoke_normalizer.md
    - name: run_pipeline
      path: node_0_3_6_4_run_pipeline/CORE_0_3_6_4_run_pipeline.md
    - name: run_jvm
      path: node_0_3_6_5_run_jvm/CORE_0_3_6_5_run_jvm.md
    - name: target
      path: node_0_3_6_6_target/CORE_0_3_6_6_target.md
    - name: output
      path: node_0_3_6_7_output/CORE_0_3_6_7_output.md

---

# CORE 0_3_6 — interp_feeder

## metadata

- **id:** hq.research.interp_feeder
- **level:** 2
- **status:** draft
- **designation:** task
- **settled_by:** the owner

## super_node

- [research](../CORE_0_3_research.md)

## sub_nodes

- [feeder_config](node_0_3_6_0_feeder_config/CORE_0_3_6_0_feeder_config.md) — Config object for interp feeder.
- [parse_interp](node_0_3_6_1_parse_interp/CORE_0_3_6_1_parse_interp.md) — Parsing logic.
- [format_canon](node_0_3_6_2_format_canon/CORE_0_3_6_2_format_canon.md) — Formatting logic.
- [invoke_normalizer](node_0_3_6_3_invoke_normalizer/CORE_0_3_6_3_invoke_normalizer.md) — Normalizer bridging.
- [run_pipeline](node_0_3_6_4_run_pipeline/CORE_0_3_6_4_run_pipeline.md) — Execution logic.
- [run_jvm](node_0_3_6_5_run_jvm/CORE_0_3_6_5_run_jvm.md) — JVM execution step.
- [target](node_0_3_6_6_target/CORE_0_3_6_6_target.md) — Target compilation.
- [output](node_0_3_6_7_output/CORE_0_3_6_7_output.md) — Output handling.

## definition

Retrofitting the interpreter language tracks into the semantic pipeline.
