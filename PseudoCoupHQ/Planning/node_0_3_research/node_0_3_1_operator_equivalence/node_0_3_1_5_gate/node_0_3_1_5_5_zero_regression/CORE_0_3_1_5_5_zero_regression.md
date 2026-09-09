---
id: hq.research.compiler_graph.gate.zero_regression
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), rule
node:
    name: zero_regression
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_5_zero_regression/CORE_0_3_1_5_5_zero_regression.md
super_node:
    name: gate
    path: ../CORE_0_3_1_5_gate.md
sub_nodes: []
---

# CORE 0_3_1_5_5 — zero_regression

## metadata

- **id:** hq.research.compiler_graph.gate.zero_regression
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

The before-and-after check run over a whole population after any
change: every unit that was PROVED before must still be PROVED, or its
loss must carry a named cause that was checked mechanically rather than
asserted. A text that changed while the verdict stayed PROVED is not a
regression — the rule is about proofs, not about characters. It is what
makes "accumulate, don't replace" enforceable: a new round may not
quietly lose ground, and where it does lose ground the reason is on the
page with the units it applies to.

## design

```
Gate.zero_regression
	methods:
		compare
			"""
			(verdicts_before, verdicts_after) ->
			per unit, kept / lost / gained,
			joined on unit name
			"""
		explain_losses
			"""
			each lost proof -> a cause, checked
			over that unit's own artifact, not
			asserted
			"""
		report
			"""
			the counts plus every cause with the
			units under it
			"""
```

The rule, as numbered statements:

1. No unit proved in the previous round loses PROVED without a named
   cause.
2. The cause is CHECKED over the unit's own artifact, mechanically.
3. A change of text with the verdict unchanged is not a regression.
4. The report is by cause with its sightings, never a list of every
   sighting.

The named causes so far, with their counts:

- **Cause A — the unreachable store**, 392 units (log_146 §9.1).
- **Cause B — the vacuous answer home**, 214 units (log_146 §9.2).
- **The flag link**, 699 units whose old proofs were wrong: the
  reader had been answered from a stale earlier comparison's flags
  (log_153 §4.2).
- **The alternative stretches added together**, 245 units whose old
  proofs were wrong: the text-order walk ran BOTH sides of a
  conditional transfer and added the two answers, and the ledger's
  term did the same, so the two agreed. All 245 carry a positional
  label and a conditional transfer; all 245 were proved by route two
  alone; route two now refuses each by name. Decision: log_168 §6
  found and fixed it, task 91 measured it over log 153's own
  population (log_196 §5).

## settled rules

- **Zero regressions in the ruled sense**: no unit loses PROVED
  without a named, proved cause; text change is not regression.
  Decision: log_129 header (round 8); carried in [gate](../CORE_0_3_1_5_gate.md) settled
  rules.
- **Causes are computed, not asserted.** Decision: log_152 §1.2.
- **Accumulate, don't replace.** A superseded artifact stays on disk
  and the next is compared against it. Decision: AgentMemory (the owner:
  "we are accumulating information").
- **A withdrawn proof that was WRONG is a correction, not a loss to
  be avoided.** The 699 flag-link withdrawals are the instance.
  Decision: log_153 §4.2.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| round-9 to round-10 check | `canon37_zero_regression.py`, `canon37_zero_regression.json` | done |
| round-10 to round-11 check | `canon38_zero_regression.py`, `canon38_zero_regression.json`, `canon38_zero_regression.txt` | done (log_152 §1.2) |
| term-route checks | `zero_regression48.py`, `zero_regression49.py`, `zero_regression53.py` with their printed transcripts | done per round |
| one module named `zero_regression` | nothing | **planned** — one per round stands today |
