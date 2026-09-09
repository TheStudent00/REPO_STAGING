---
id: hq.research.compiler_graph.ledger
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: ledger
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_3_ledger/CORE_0_3_1_3_ledger.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: rows
      designation: code (attribute)
      realize: false
    - name: row
      path: node_0_3_1_3_1_row/CORE_0_3_1_3_1_row.md
    - name: producer
      path: node_0_3_1_3_2_producer/CORE_0_3_1_3_2_producer.md
    - name: destination_rules
      path: node_0_3_1_3_3_destination_rules/CORE_0_3_1_3_3_destination_rules.md
    - name: flag_rules
      path: node_0_3_1_3_4_flag_rules/CORE_0_3_1_3_4_flag_rules.md
    - name: walk_dataflow
      designation: code (method)
      realize: false
---

# CORE 0_3_1_3 — ledger

## metadata

- **id:** hq.research.compiler_graph.ledger
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- rows — code (attribute) *(realize: false)*
- [row](node_0_3_1_3_1_row/CORE_0_3_1_3_1_row.md) — One value that moves through a unit, written down as one line of the ledger.
- [producer](node_0_3_1_3_2_producer/CORE_0_3_1_3_2_producer.md) — What made a row's value, written as a typed object with a `kind` and a second field naming the thing that kind points at — `mnem` for the three kinds that name an instruction, `callee` for the one that names a routine — and never as a bare string.
- [destination_rules](node_0_3_1_3_3_destination_rules/CORE_0_3_1_3_3_destination_rules.md) — The per-opcode table saying which registers an instruction writes and which it reads WITHOUT naming them in its operands.
- [flag_rules](node_0_3_1_3_4_flag_rules/CORE_0_3_1_3_4_flag_rules.md) — The table of which instructions SET the processor's condition flags and which READ them, plus the rule that links a reader to the exact row that set the flags it reads.
- walk_dataflow — code (method) *(realize: false)*

## definition

The table beside every canonical unit with one row per value that
moves through it — input, constant, temporary, own stack address,
machine-stack slot, x87 slot, guard outcome, answer — each row
carrying its block, its type, the arch opcode (or opcode pair) that
PRODUCED it, and the rows that opcode READ. The ledger is the unit's
dataflow graph written as a table; the z3 term is read off it, and
the census of unmodelled operations is a filter over it.

## design

```
class Ledger
	attributes:
		rows
			"""
			ordered list of Row; block + index
			gives the name (IN-0, TEMP-3, OUT-0)
			"""
	methods:
		walk_dataflow
			"""
			body_text -> rows. One pass in
			program order keeping a
			register-family -> row map; each
			instruction's destination(s) per
			destination_rules; each flag reader
			linked to the row that set the flags
			per flag_rules
			"""


class Row
	attributes:
		block
		index
		offset
		size
		type
			"""
			'8-byte general value',
			'16-byte vector value',
			'x87 stack value', 'flags only',
			'flag-derived value',
			'the unit's own stack address', …
			"""
		produced_by
			"""
			a Producer (sub-node): typed object,
			never a bare string
			"""
		operands
			"""
			row names, in the arch text's own
			operand order
			"""
		written_half
			"""
			for multi-destination opcodes:
			quotient / remainder / low / high /
			'the sign of the accumulator'
			"""
		value_at_run
			"""
			filled only when executed
			"""
```

## settled rules

- **Rows carry provenance** — producer and operands — for every value
  including temporaries and guard outcomes; storing them to memory is
  a separate cheap choice, the rows are the information. Decision:
  AgentMemory "THE PROVENANCE LEDGER" (the owner, 2026-09-02: "the ledger
  should also track the operator that a result might create").
- **A producer is a typed object** — `arch_opcode`, `flag_pair`,
  `non_opcode_phrase` with `{kind, mnem}` or `{kind, phrase}`, and
  `runtime_callee` with `{kind, callee}` — so the unmodified guard
  reads it as machine form. Decision: "ROUND 10 RULINGS" (5); log_147
  §13; the fourth kind's shape, log_158 TASK 59 (b), 2026-09-03.
- **Implicit destinations are per-opcode rules**; an unconditional
  `jmp` is never a flag reader; a comparison's row is `flags only`
  and does not repoint its destination register. Decision: "ROUND 10
  RULINGS" (3); log_152 §2.
- **The flag reader links to the row that set the flags**, never to a
  running "last flags" variable. Decision: log_153 §4.2 (the link
  cost 699 wrongly-proved units and is correct).
- **Irregular lifter names are never producers.** A flag-derived row
  is produced by the PAIR (setter, reader) of arch opcodes; the
  lifter's helper (`amd64g_calculate_condition`) never enters the
  ledger. Decision: log_142 addendum (the owner, 2026-09-02).

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| the module under this node's name | `ledger.py` — `Ledger`, `Row`, `Producer`, `DESTINATION_RULES`, `FLAG_RULES`; imports nothing from `ledger47`/`ledger48`, and every unchanged part is copied with a header line saying so | done 2026-09-03 (task 59). Its unit test walks a computed sample of 241 units (every acceptance unit of logs 152/153 plus 50 random per population over four populations, seed 59): 241 walked, 0 refused, 2,189 rows, 0 producer holes — `ledger_sample_walk.py`, `ledger_sample_walk_printed.txt` |
| walk_dataflow, Row, Producer | `ledger48.py` (`walk_dataflow`, `producer_object`, `DESTINATION_RULES`, `BLOCK_ORDER`) | superseded record (log_152): 240,675+ rows over 30,436 units; 3,807 destination-table rows; 3,408 STACK; 3,090 X87; 19,934 `flags only`. Never edited, never imported |
| destination_rules | `ledger.DESTINATION_RULES`: idiv, div, mul, imul(1-op), cltd, cqto, cwtl, cltq, cbtw, plus `RUNTIME_TRANSFER_RULE` | done, the transfer into the runtime included (task 59; see arch_unit.runtime_callee) |
| flag_rules | `ledger.FLAG_RULES` — the stem-based setter table, the comparison setters, the carry-in setters and the reader link, all in one place | done, `sbb`/`adc` included (task 59): 728 units of the 31,067 walked carry a flag pair whose setter is one of the two |
| superseded | `ledger47.py`'s walk (last-named-operand rule; jmp as flag reader; bare-string producers) | superseded by `ledger48.py` |

Next lap: `canonical_form.py` (node 0_3_5_2, task 60) consumes
`ledger.py` and renders the populations into `canon39_*`. This node
does not re-render them itself.
