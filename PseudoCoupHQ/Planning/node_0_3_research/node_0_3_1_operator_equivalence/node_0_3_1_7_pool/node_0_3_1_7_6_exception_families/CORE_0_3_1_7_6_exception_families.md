---
id: hq.research.compiler_graph.pool.exception_families
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), finding
node:
    name: exception_families
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/node_0_3_1_7_6_exception_families/CORE_0_3_1_7_6_exception_families.md
super_node:
    name: pool
    path: ../CORE_0_3_1_7_pool.md
sub_nodes: []
---

# CORE 0_3_1_7_6 — exception_families

## metadata

- **id:** hq.research.compiler_graph.pool.exception_families
- **level:** 4
- **status:** draft
- **designation:** code (method), finding
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [pool](../CORE_0_3_1_7_pool.md)

## sub_nodes

*(none yet)*

## definition

The same family idea applied to GUARDS rather than to computations. A
guard is the check a compiler emits around an operation together with
what it does when the check fires — a division checking for a zero
divisor and transferring to a panic routine, for instance. Two guards
are the same when both halves match: the condition tested and the
response taken. Grouping guards that way across languages gives the
exception families. The current file is from round 5 and has not been
rebuilt since; it is STALE against `the_pool3.json`, and the rebuild is
planned.

## design

```
Pool.exception_families
	methods:
		collect_guards
			"""
			pool entries -> the guard rows their
			members carry: the condition tested
			and the response taken
			"""
		identity
			"""
			two guards are the same when both
			the condition and the response match
			"""
		group
			"""
			guards -> families across languages,
			the same component rule the
			computation families use
			"""
```

Instance: `EF0039`, the `growing` family, from
`exception_families2.json` (round 5).

## settled rules

- **Guard identity is condition AND response together**, not the
  condition alone. Decision: [pool](../CORE_0_3_1_7_pool.md) design
  (`exception_families` docstring).
- **Guard outcomes have their own ledger block and their own rows**,
  so a guard is a value with provenance like any other. Decision:
  AgentMemory "REFINEMENT — NO DESIGNATED REGISTERS" + "ROUND 10
  RULINGS" (2).
- **Spelling never keys a guard family.** Decision: THE SPELLING BAN.
- **THE REBUILD TAKES THE NEXT NUMBER, NOT A TAKEN ONE** (correction,
  2026-09-03, task 61). Task 61's brief named `exception_families3.json`
  for the rebuild. That name is already on disk: the round-5 line's own
  later build over `guards5.json` wrote `exception_families3.py` /
  `exception_families3.json` on 2026-09-01, and this CORE's own
  realization table already recorded them. A superseded record is never
  edited, and numbered artifacts accumulate, so the rebuild is
  `exception_families4.json`. Decision: log_075's accumulate ruling +
  this CORE's realization table; recorded in PROGRESS the same day.
- **A stale artifact is labelled stale, not quietly reused.**
  Decision: this CORE, 2026-09-03, applying log_075's accumulate
  ruling; the staleness is recorded in [pool](../CORE_0_3_1_7_pool.md)'s realization table.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| round-5 build | `exception_families2.py`, `exception_families2.json`; `EF0039` the `growing` family | **stale** against `the_pool3.json` |
| earlier build | `exception_families.py`, `exception_families.json` | superseded record |
| later build | `exception_families3.py`, `exception_families3.json` | on disk, not read against pool3 |
| rebuild over the current pool | `pool.py` `Pool.exception_families`, `exception_families4.json` | done (task 61) |
| guard rows in the ledger | GUARD block in `ledger48.py` | done |
| rebuild over pool5 | `pool65_run.py`, `exception_families5.json` — 40 families, 128 rows considered, 186 excluded | done (task 65, log_169) |
