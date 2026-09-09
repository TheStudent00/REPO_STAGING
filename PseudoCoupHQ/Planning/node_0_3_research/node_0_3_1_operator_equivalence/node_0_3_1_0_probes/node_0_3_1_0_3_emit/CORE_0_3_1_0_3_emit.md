---
id: hq.research.compiler_graph.probes.emit
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: emit
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_0_probes/node_0_3_1_0_3_emit/CORE_0_3_1_0_3_emit.md
super_node:
    name: probes
    path: ../CORE_0_3_1_0_probes.md
sub_nodes: []
---

# CORE 0_3_1_0_3 — emit

## metadata

- **id:** hq.research.compiler_graph.probes.emit
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [probes](../CORE_0_3_1_0_probes.md)

## sub_nodes

*(none yet)*

## definition

The writer that turns one (operator, operand types) pair into the
source text of a one-function probe in one language. There is one
emitter per language, because only the spelling and the function
wrapper differ; the operator and the types arrive as data from the
two inventories. Every probe is generated here, so no probe source is
written by hand anywhere in the pipeline. Its output is the source
[compile](../node_0_3_1_0_4_compile/CORE_0_3_1_0_4_compile.md) hands
to the compiler.

## design

```
probes.emit
	attributes:
		emitters
			"""
			one source writer per language: c,
			cpp, go, rust, swift. Each knows the
			language's function wrapper and how
			the operator is spelled there
			"""
	methods:
		emit_one
			"""
			(operator, operand_types, language)
			-> the source text of a probe whose
			whole body is the operator applied
			to its arguments
			"""
		emit_grid
			"""
			the two inventories -> one source
			per surviving cell of the grid,
			plus a manifest row per cell
			"""
```

## settled rules

- **Probes are generated, never hand-written.** The inventories are
  data; the emitter is per-language code. Decision:
  [probes](../CORE_0_3_1_0_probes.md) settled rules (the owner,
  2026-08-24).
- **The operator label the emitter writes is a display column on the
  manifest, never a key.** Decision:
  [guard](../../node_0_3_1_8_guard/CORE_0_3_1_8_guard.md), THE
  SPELLING BAN.
- **The plan names ONE emit.** Three files carry it today and import
  one another; unifying them is owed work, not a second design.
  Decision: [probes](../CORE_0_3_1_0_probes.md) realization table,
  2026-09-03.

## realization (what exists on disk, 2026-09-03)

Home: `PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| emit (original) | `probe_gen.py` | done |
| emit (regeneration) | `probe_gen2.py` | done |
| emit (swift `@_cdecl` fix) | `probe_gen3.py` | done (log_143) |
| emit (interpreter/JIT probes) | `probe_gen_jit.py` | done |
| one module named `emit` | nothing | **planned** — three files stand where the plan names one |

The banked swift population predates `probe_gen3.py`; a swift re-run
would change 1,407 sources (log_143 §5).
