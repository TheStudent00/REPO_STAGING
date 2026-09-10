---
id: hq.research.compiler_graph.probes.compile
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: compile
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_0_probes/node_0_3_1_0_4_compile/CORE_0_3_1_0_4_compile.md
super_node:
    name: probes
    path: ../CORE_0_3_1_0_probes.md
sub_nodes: []
---

# CORE 0_3_1_0_4 — compile

## metadata

- **id:** hq.research.compiler_graph.probes.compile
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

The step that hands one probe source to the real compiler inside an
Airlock instance — Airlock being the sandbox container this research
compiles in — and keeps what comes back. For an accepted probe it
keeps three things: an ANCHOR build with the optimizer off, a SHIP
build with the optimizer on, and the compiler's own DWARF records. For
a refused probe it keeps the compiler's refusal text as testimony.
Whether the compiler accepts or refuses IS the acceptance oracle; no
predictor overrides it. The work is driven in small batches by the
trickle drivers so a long run can stop and resume.

## design

```
probes.compile
	attributes:
		switches
			"""
			the ruled per-language switches:
			clang -O0, rustc opt-level=0,
			go -N -l, swiftc -Onone for the
			anchor; the language's default
			optimized build for the ship
			"""
		store
			"""
			on-disk record per probe: the two
			builds, the DWARF record, and the
			refusal text when refused
			"""
	methods:
		build_anchor
			"""
			source -> unoptimized object; the
			build argument identity is read from
			"""
		build_ship
			"""
			source -> optimized object; the
			build arch-units are extracted from
			"""
		read_dwarf
			"""
			object -> per-operand encoding and
			width, the machine facts that stand
			in for a type name
			"""
		trickle
			"""
			drive the grid in resumable batches,
			banking state after each lane so a
			stopped run resumes where it stood
			"""
```

## settled rules

- **Compile-or-refuse is the acceptance oracle.** The compiler's own
  type checker decides what is a probe. Decision:
  [probes](../CORE_0_3_1_0_probes.md), ratified pipeline step 1.
- **Every accepted probe compiles twice**, anchor and ship, with the
  ruled switches. Decision: [probes](../CORE_0_3_1_0_probes.md),
  ratified pipeline step 2.
- **Arch-units are extracted from the SHIP build; argument identity
  comes from the ANCHOR build.** Decision:
  [arch_unit](../../node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md)
  settled rules, steps 2–4.
- **A refusal is kept, not discarded.** The compiler's refusal text is
  testimony about the language and is banked on the manifest row.
  Decision: [probes](../CORE_0_3_1_0_probes.md) definition.

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| trickle drivers | `trickle.py`, `trickle2.py`, `trickle_up.sh`, `trickle_down.sh`, `trickle_doctor.sh` | done |
| store | `trickle_store/`, `trickle_raw/`, `trickle_lanes/`, `trickle2_outbox/` | done |
| resume state | `trickle_state.json`, `trickle2_state.json` | done |
| tallies | `trickle_tallies.json`, `trickle_tallies.md`, `trickle_report.py` | done |
| read_dwarf | `dwarf_typed_key.py`, `dwarf_typed_key.json` | done |
| superseded record | `TRICKLE_SUPERSEDED.md` | superseded |

Accepted 29,288 of 129,553 offered on the regenerated corpus.
