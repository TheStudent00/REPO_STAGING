---
id: hq.research.compiler_graph.ledger.row
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: row
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_3_ledger/node_0_3_1_3_1_row/CORE_0_3_1_3_1_row.md
super_node:
    name: ledger
    path: ../CORE_0_3_1_3_ledger.md
sub_nodes:
    - name: block
      designation: code (attribute)
      realize: false
    - name: index
      designation: code (attribute)
      realize: false
    - name: offset
      designation: code (attribute)
      realize: false
    - name: size
      designation: code (attribute)
      realize: false
    - name: type
      designation: code (attribute)
      realize: false
    - name: produced_by
      designation: code (attribute)
      realize: false
    - name: operands
      designation: code (attribute)
      realize: false
    - name: written_half
      designation: code (attribute)
      realize: false
    - name: value_at_run
      designation: code (attribute)
      realize: false
---

# CORE 0_3_1_3_1 — row

## metadata

- **id:** hq.research.compiler_graph.ledger.row
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledger](../CORE_0_3_1_3_ledger.md)

## sub_nodes

- block — code (attribute) *(realize: false)*
- index — code (attribute) *(realize: false)*
- offset — code (attribute) *(realize: false)*
- size — code (attribute) *(realize: false)*
- type — code (attribute) *(realize: false)*
- produced_by — code (attribute) *(realize: false)*
- operands — code (attribute) *(realize: false)*
- written_half — code (attribute) *(realize: false)*
- value_at_run — code (attribute) *(realize: false)*

## definition

One value that moves through a unit, written down as one line of the
ledger. A row says which block it belongs to and which position in that
block, where it sits in memory and how many bytes it takes, what kind
of value it is, which arch opcode produced it, and which other rows
that opcode read. Its name is its block plus its index — IN-0, TEMP-3,
OUT-0 — and that name is what every other row and every term refers to
it by. A row exists for every value including temporaries and guard
outcomes, whether or not that value is ever stored to memory.

## design

```
class Row
	attributes:
		block
			"""
			IN, CONST, TEMP, OWN, STACK, X87,
			GUARD or OUT
			"""
		index
			"""
			position within the block; block +
			index is the row's name
			"""
		offset
			"""
			byte offset of the row inside its
			block
			"""
		size
			"""
			bytes; a 16-byte value gets a
			16-byte row
			"""
		type
			"""
			'8-byte general value', '16-byte
			vector value', 'x87 stack value',
			'flags only', 'flag-derived value',
			"the unit's own stack address", ...
			"""
		produced_by
			"""
			a Producer: a typed object, never a
			bare string
			"""
		operands
			"""
			the row names this row's producer
			read, in the arch text's own operand
			order
			"""
		written_half
			"""
			for an opcode writing two places:
			quotient / remainder / low / high /
			'the sign of the accumulator'
			"""
		value_at_run
			"""
			filled only when the unit is
			actually executed
			"""
```

## settled rules

- **Rows carry provenance** — producer and operands — for every value
  including temporaries and guard outcomes. Decision: AgentMemory
  "THE PROVENANCE LEDGER" (the owner, 2026-09-02); carried in [ledger](../CORE_0_3_1_3_ledger.md).
- **A row's name is block plus index**, and that name is what terms
  and other rows refer to. Decision: [ledger](../CORE_0_3_1_3_ledger.md) design.
- **Rows are sized by type**; a 16-byte value gets a 16-byte row.
  Decision: log_141 §8, log_146 §2.5.
- **A comparison's row is typed `flags only`** and does not repoint a
  destination register; it is carried as the first operand of the next
  flag-reading row. Decision: log_152 §2.5 and §9.1 item 2.
- **Storing a row to memory is a separate cheap choice.** The row is
  the information; the store is not what makes it exist. Decision:
  AgentMemory "THE PROVENANCE LEDGER".

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| Row and the block order | `ledger48.py` (`BLOCK_ORDER`) | done |
| rows built | 240,675+ rows over 30,436 units | done (log_152) |
| STACK rows | 3,408 (instance `c/regen_11491`, log_152 §3.2) | done |
| X87 rows | 3,090 (instance `cpp/regen_36796`, log_152 §3.3) | done |
| `flags only` rows | 19,934 | done |
| `value_at_run` | not filled; no unit is executed in this pipeline today | **deferred** |
| superseded | `ledger47.py`'s rows (last-named-operand destination) | superseded record |
