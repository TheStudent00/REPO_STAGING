---
id: hq.research.compiler_graph.arch_unit.extract
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: extract
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_7_extract/CORE_0_3_1_1_7_extract.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_1_1_arch_unit.md
sub_nodes: []
---

# CORE 0_3_1_1_7 — extract

## metadata

- **id:** hq.research.compiler_graph.arch_unit.extract
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit](../CORE_0_3_1_1_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

The step that turns a probe's two builds into an arch-unit: it cuts
the probe function's own bytes out of the ship object, disassembles
them into one notation with objdump, and reads the compiler's DWARF
records for the operands' encoding and width. What comes out is the
object of record — bytes, text, machine-fact operand types — for every
accepted probe of every language. It writes one file per language for
the original corpus and a resumable store for the regenerated one.

## design

```
ArchUnit.extract
	methods:
		cut_body
			"""
			ship object + probe symbol ->
			body_bytes, the function's own bytes
			and nothing else
			"""
		disassemble
			"""
			body_bytes -> body_text, one
			notation for every language, so two
			compilers' output is comparable as
			text
			"""
		read_operand_types
			"""
			anchor object's DWARF -> per operand
			an encoding and a width; never a
			declared type name
			"""
		bank
			"""
			write one ArchUnit record per probe:
			language, operator label (display),
			operand_types, body_bytes, body_text
			"""
```

## settled rules

- **Arch-units are extracted from the SHIP build; identity comes from
  the ANCHOR build.** Decision: [arch_unit](../CORE_0_3_1_1_arch_unit.md) settled rules,
  `../../CORE_0_3_1_operator_equivalence.md` steps 2-4.
- **Typing is by machine fact**, DWARF encoding and width, never a
  declared type name. Decision: [arch_unit](../CORE_0_3_1_1_arch_unit.md) settled rules (AgentMemory,
  log_074 audit).
- **One notation for every language.** The disassembly is normalized
  to a single notation so that two compilers' bodies are comparable
  as text. Decision: [arch_unit](../CORE_0_3_1_1_arch_unit.md) design (`body_text` docstring).
- **The operator label rides along as display only.** Decision:
  [guard](../../node_0_3_1_8_guard/CORE_0_3_1_8_guard.md), THE
  SPELLING BAN.

## realization (what exists on disk, 2026-09-03)

Home: `PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| units, original corpus | `op_units_c.json`, `op_units_cpp.json`, `op_units_go.json`, `op_units_rust.json`, `op_units_swift.json` | done |
| units, regenerated corpus | `trickle_store/` | done |
| units, interpreter corpus | `op_units_cpython.json`, `op_units_java.json`, `op_units_php.json`, `op_units_ruby.json` | done |
| operand types from DWARF | `dwarf_typed_key.json`, `dwarf_typed_key_t27.json` | done |
| assignment-form units | `op_units_asg_<lang>.json` | done |
