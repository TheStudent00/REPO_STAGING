---
id: hq.research.compiler_graph.probes
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (module), rule
node:
    name: probes
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_0_probes/CORE_0_3_1_0_probes.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: operator_inventory
      designation: code (attribute)
      realize: false
    - name: type_inventory
      path: node_0_3_1_0_1_type_inventory/CORE_0_3_1_0_1_type_inventory.md
    - name: legality
      path: node_0_3_1_0_2_legality/CORE_0_3_1_0_2_legality.md
    - name: emit
      path: node_0_3_1_0_3_emit/CORE_0_3_1_0_3_emit.md
    - name: compile
      path: node_0_3_1_0_4_compile/CORE_0_3_1_0_4_compile.md
    - name: manifest
      designation: code (attribute)
      realize: false
---

# CORE 0_3_1_0 — probes

## metadata

- **id:** hq.research.compiler_graph.probes
- **level:** 3
- **status:** draft
- **designation:** code (module), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- operator_inventory — code (attribute) *(realize: false)*
- [type_inventory](node_0_3_1_0_1_type_inventory/CORE_0_3_1_0_1_type_inventory.md) — Per language, the list of every type this target actually accepts in a declaration — one of the two axes the probe grid is built from.
- [legality](node_0_3_1_0_2_legality/CORE_0_3_1_0_2_legality.md) — The reader of a compiler's OWN legality rules — the conditions under which that compiler refuses an operator on a pair of operand types — recorded with the file and line of the compiler source each rule was read from.
- [emit](node_0_3_1_0_3_emit/CORE_0_3_1_0_3_emit.md) — The writer that turns one (operator, operand types) pair into the source text of a one-function probe in one language.
- [compile](node_0_3_1_0_4_compile/CORE_0_3_1_0_4_compile.md) — The step that hands one probe source to the real compiler inside an Airlock instance — Airlock being the sandbox container this research compiles in — and keeps what comes back.
- manifest — code (attribute) *(realize: false)*

## definition

The module that turns a language's operator vocabulary into compiled
machine code, one probe per (operator × operand types), with no hand
written probe anywhere. Its output is the population every later node
works on: for each accepted probe, an ANCHOR build (optimizer off), a
SHIP build (optimized), and the compiler's own DWARF facts; for each
refused probe, the compiler's refusal text as testimony.

## design

```
module probes
	attributes:
		operator_inventory
			"""
			per language: every grammar operator
			with its arity. Data, never typed by
			hand. Source:
			Research/kind_fuzz_clustering/
			operator_arity.json
			"""
		type_inventory
			"""
			per language: every type the target
			ACCEPTS as a declaration (sub-node;
			extracted, then witnessed by a
			one-line compile per type)
			"""
		manifest
			"""
			per language: one row per probe —
			operator label, operand types, source
			text, accept/refuse, refusal text,
			paths of the two builds and the DWARF
			record. probe_manifest_<lang>.json
			"""
	methods:
		legality
			"""
			sub-node: reads the compiler's own
			rules to predict refusal before
			compiling; a cost saver and a second
			witness, never the oracle
			"""
		emit
			"""
			sub-node: operator × types -> source
			text of a one-function probe, per
			language emitter
			"""
		compile
			"""
			sub-node: source -> anchor build,
			ship build, DWARF; runs in an Airlock
			instance; compile-or-refuse is the
			oracle
			"""
```

Call flow:

```
probes.emit(operator_inventory, type_inventory)
    --> probes.compile(source)
    --> probes.manifest (one row per probe)
```

## settled rules

- **Probes are generated, never hand-written.** The inventories are
  data; the emitter is per-language code; no per-operator hand work.
  Decision: `../CORE_0_3_1_operator_equivalence.md` standing rules (the owner,
  2026-08-24).
- **Compile-or-refuse is the acceptance oracle.** The compiler's own
  type checker decides what is a probe; the legality reader only
  predicts. Decision: `../CORE_0_3_1_operator_equivalence.md` ratified
  pipeline step 1.
- **Every accepted probe compiles twice**, anchor and ship, with the
  ruled switches (clang -O0 / rustc opt-level=0 / go -N -l / swiftc
  -Onone). Decision: ratified pipeline step 2.
- **Type inventories are extracted, never hand-written**, and carry a
  second witness: declarable on this target with this toolchain.
  Decision: AgentMemory, round 9 (log_137: 85 of 208 types demoted).
- **A probe whose answer is produced by a `call` into the compiler's
  own runtime is IN SCOPE.** `__divti3` and its family are the
  compiler's lowering of 128-bit division, shipped with the compiler
  and built by it; they are not library calls. The callee's body is
  extracted and followed (see
  [arch_unit](../node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md)).
  Decision: the owner, 2026-09-03 (conversation; supersedes the 2026-09-03
  "out of scope" note in `Research/op_pipeline/out_of_scope_library_calls.json`).
- **The spelling ban applies to the manifest**: the operator label is
  a display column, never a key. See
  [guard](../node_0_3_1_8_guard/CORE_0_3_1_8_guard.md).

## realization (what exists on disk, 2026-09-03)

Home: `PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| emit | `probe_gen.py` (original), `probe_gen2.py` (regeneration), `probe_gen3.py` (swift `@_cdecl` fix, log_143) | three files import one another; the plan names ONE `emit` |
| legality | `legality_rules.py`, `legality_rules.json` | done (log_137) |
| type_inventory | `type_inventory3.json` (extracted ∧ declarable) | done (log_137) |
| compile | the trickle drivers `trickle2.py` and the lane scripts; stores `trickle_store/` | done for the regenerated corpus (29,288 accepted of 129,553) |
| manifest | `probe_manifest_<lang>.json` | done; the guard reads its operator inventory from these |

Populations on disk: original 1,779 (c 610, cpp 770, go 107, rust
125, swift 167); regenerated 29,288; interpreter/JIT 11 (not from this
module — see [arch_unit](../node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md)).
The banked swift population predates `probe_gen3.py`; a swift
re-run would change 1,407 sources (log_143 §5).
