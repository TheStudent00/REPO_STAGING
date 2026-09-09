---
id: hq.research.remaining_languages.kotlin
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: work
node:
    name: kotlin
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages/node_0_3_1_12_4_kotlin/CORE_0_3_1_12_4_kotlin.md
super_node:
    name: remaining_languages
    path: ../CORE_0_3_1_12_remaining_languages.md
sub_nodes: []
---

# CORE 0_3_1_12_4 — kotlin

## metadata

- **id:** hq.research.remaining_languages.kotlin
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

Kotlin's route into the corpus: the JIT shape by way of the JVM.
`kotlinc` (in the persist volume, `/persist/kotlinc`) compiles the
generated probe to bytecode; from there the route is java's
([interp_feeder / run_jvm](../../node_0_3_1_11_interp_feeder/node_0_3_1_11_5_run_jvm/CORE_0_3_1_11_5_run_jvm.md)):
warm until C2 compiles, dump, carve at the method body. Kotlin's
operator inventory is in `operator_arity.json`; its holders are in
the fuzz census (log_062). Not started; blocked on nothing but the
java route's own open item (the `AREA_SPAN` ruling).
