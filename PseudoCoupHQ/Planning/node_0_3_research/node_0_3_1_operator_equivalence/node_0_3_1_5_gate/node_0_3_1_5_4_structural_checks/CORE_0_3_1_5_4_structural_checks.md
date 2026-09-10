---
id: hq.research.compiler_graph.gate.structural_checks
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), rule
node:
    name: structural_checks
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_4_structural_checks/CORE_0_3_1_5_4_structural_checks.md
super_node:
    name: gate
    path: ../CORE_0_3_1_5_gate.md
sub_nodes: []
---

# CORE 0_3_1_5_4 — structural_checks

## metadata

- **id:** hq.research.compiler_graph.gate.structural_checks
- **level:** 4
- **status:** draft
- **designation:** code (method), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [gate](../CORE_0_3_1_5_gate.md)

## sub_nodes

*(none yet)*

## definition

The six mechanical checks that carry a unit when the solver cannot —
used only where the reference has no model for a mnemonic the body
spells. Because the canonical form applies NO transformation to the
body, the proof obligation reduces to two claims that can be checked by
looking: the compiler's body is present and unchanged, and the added
plumbing cannot disturb it. A unit passing all six is
PROVED_BY_CONSTRUCTION. The checks are C1 through C6, and C6 exists
because the positional label rewrite makes C1's original
character-for-character wording false as written.

## design

The six checks, as numbered statements:

1. **C1** — the body appears in the wrapped text character-for-
   character and in its own order: no register renamed, no immediate
   moved, no stack address rewritten.
2. **C2** — the prelude writes only the registers the arrival
   contract names, one two-step load per input row, plus at most one
   general scratch that is not an arrival family (so the body never
   reads it before writing it).
3. **C3** — every `ret` is immediately preceded by the epilogue.
4. **C4** — no body line names the ledger symbol or any ledger row.
5. **C5** — the epilogue's pointer register is not the result
   register.
6. **C6** — the label rewrite touched only transfer targets: an
   intra-unit target became `L0..` and an out-of-unit transfer lost
   its address and comment; nothing else on any line changed.

```
Gate.structural_checks
	methods:
		check_one .. check_six
			"""
			(wrapped_text, unit) -> pass or the
			line that failed
			"""
		verdict
			"""
			all six pass ->
			PROVED_BY_CONSTRUCTION; any fail ->
			the failing check named
			"""
```

## settled rules

- **The structural route is used only where the solver returns
  UNDECIDED** for want of a model, never as a cheaper first choice.
  Decision: log_146 §5.3.
- **C1, C3, C4 and C5 are forced by construction** over artifacts the
  lap itself built; C2 rests on the arrival contract being read off
  the body's own text. Decision: log_146 §5.3, evidence class.
- **C6 is a new check, not a reuse of canon37's claim.** Ruling 4
  makes the old wording false, and `canon37_gate.py` was not edited.
  Decision: log_152 §9.1 item 3; §4.1.
- **A unit that fails any check is not counted**, whatever its text
  looks like. Decision: AgentMemory "PROVED UNIT IS A COUNTED UNIT".

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| C1-C5 | `canon37_gate.py` | done |
| C1-C6 | `canon38_gate.py` (`check_six`) | done |
| units carried by this route | 11,889 PROVED_BY_CONSTRUCTION | done |
| one module named `gate.py` | nothing | **planned** |
