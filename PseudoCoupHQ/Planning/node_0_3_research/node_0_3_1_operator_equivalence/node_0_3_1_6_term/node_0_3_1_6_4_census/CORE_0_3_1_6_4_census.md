---
id: hq.research.compiler_graph.term.census
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), finding
node:
    name: census
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/node_0_3_1_6_4_census/CORE_0_3_1_6_4_census.md
super_node:
    name: term
    path: ../CORE_0_3_1_6_term.md
sub_nodes: []
---

# CORE 0_3_1_6_4 — census

## metadata

- **id:** hq.research.compiler_graph.term.census
- **level:** 4
- **status:** draft
- **designation:** code (method), finding
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [term](../CORE_0_3_1_6_term.md)

## sub_nodes

*(none yet)*

## definition

The filter over ledgers that lists every row whose producer has no
term builder — that is, the list of what the pipeline cannot yet model.
It is a FILTER and not a survey: it reports only rows that actually
blocked a real unit, keyed by the arch opcode of that unit's own body,
never by a lifter's helper name and never by an operator token. Each
entry carries a written reason sentence, and it is that sentence, not
a producer's spelling, that groups entries when two rounds are
compared. The current census is 54 producers, 1,719 rows, 1,668
units.

## design

```
Term.census
	methods:
		filter
			"""
			a population of ledgers -> the rows
			whose producer has no builder
			"""
		group
			"""
			rows -> entries, one per producer,
			carrying rows blocked, units,
			languages and the written reason
			"""
		delta
			"""
			(census_before, census_after) -> what
			closed and what appeared, matched on
			the recorded REASON SENTENCE
			"""
```

The five causes of log_147 §4.1, and what closed:

1. **The machine stack has no block** — `push`, `pop`, 4,298 rows.
   CLOSED by the STACK block (log_153 §3.2).
2. **The implicit destination** — `idiv`, `div`, `mul`, one-operand
   `imul`, 1,558 rows. CLOSED by the destination table.
3. **The x87 stack has no rows** — `fucomip`/`fucomi` pairs, 1,072
   rows. CLOSED by the X87 block.
4. **An unconditional transfer is not a flag reader** — `jmp` pairs,
   324 rows. CLOSED by the flag rule.
5. **The flags the setter left are not in the ledger** — 792 rows.
   CLOSED by carrying the comparison row as the reader's operand.

What the closures revealed behind them: 400 rows of x87 ARITHMETIC
(`fadds`, `faddp`, `fmulp`, `fidivl`), and the `sbb`/`adc` flag pairs,
neither of which the earlier walk could reach at all.

## settled rules

- **The census is a filter, never a survey**, and its keys are arch
  opcodes of the blocked unit's own body. Decision: AgentMemory "THE
  MEMORY-WRAPPED FORM"; log_147 §3.3.
- **Every entry carries a written reason sentence**, and comparisons
  between rounds are grouped on that sentence. Decision: log_153
  §3.3.
- **An unruled gap is a census row, not a blocker and not an invented
  rule.** `call` is the instance: 300 units reported with their
  callee names, no destination rule invented. Decision: log_153 §3.4.
- **Irregular lifter names never key the census.** Decision: log_142
  addendum; the lifter-keyed `name_census.json` is superseded.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| current census | `name_census4.py`, `name_census4.json`, `name_census4_printed.txt` — 54 producers, 1,719 rows, 1,668 units | done |
| previous census | `name_census3.py`, `name_census3.json` — 8,044 rows | superseded record |
| delta by cause | `audit53.py`, `audit53_printed.txt` | done (log_153 §3.3) |
| lifter-keyed and bare-producer censuses | `name_census.json`, `name_census2.json` | superseded records |
| round-12 census | `name_census5.py`, `name_census5.json` — 52 producers, 1,877 rows | superseded record |
| round-13 census | `name_census6.py`, `name_census6.json`, `name_census6_printed.txt` — 49 producers, 1,637 rows, delta vs census5 by reason sentence: 27 closed / 11 appeared / 1 moved | done (task 65, log_169) |
