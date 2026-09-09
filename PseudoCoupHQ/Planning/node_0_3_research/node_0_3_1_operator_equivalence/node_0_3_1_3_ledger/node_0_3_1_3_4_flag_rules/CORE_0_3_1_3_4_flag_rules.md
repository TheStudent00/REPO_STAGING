---
id: hq.research.compiler_graph.ledger.flag_rules
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (attribute), rule
node:
    name: flag_rules
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_3_ledger/node_0_3_1_3_4_flag_rules/CORE_0_3_1_3_4_flag_rules.md
super_node:
    name: ledger
    path: ../CORE_0_3_1_3_ledger.md
sub_nodes: []
---

# CORE 0_3_1_3_4 — flag_rules

## metadata

- **id:** hq.research.compiler_graph.ledger.flag_rules
- **level:** 4
- **status:** draft
- **designation:** code (attribute), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledger](../CORE_0_3_1_3_ledger.md)

## sub_nodes

*(none yet)*

## definition

The table of which instructions SET the processor's condition flags
and which READ them, plus the rule that links a reader to the exact row
that set the flags it reads. Setters are recognized by mnemonic stem,
so the table covers comparisons (`cmp`, `test`), x87 and SSE compares
(`fucomip`, `ucomiss`), and arithmetic instructions that set flags as a
side effect. A reader links to the setter's own row, never to a running
"last flags" variable, because a running variable answers from whatever
comparison happened most recently rather than from the one that
actually set these flags. An unconditional `jmp` reads no flags and is
never a reader.

## design

The rules, as numbered statements:

1. A setter is recognized by its mnemonic stem, so size and form
   variants are one entry.
2. The setter families covered: comparisons (`cmp`, `test`), x87
   compares (`fucomip`, `fucomi`), SSE compares (`ucomiss`,
   `ucomisd`), and arithmetic setters for the overflow, no-overflow,
   below and above-or-equal conditions.
3. A comparison's row is typed `flags only` and does not repoint its
   destination register.
4. A flag reader's row links to the ROW that set the flags — carried
   as the reader's first operand — never to a running "last flags"
   variable.
5. An unconditional `jmp` is never a flag reader.
6. A flag-derived row's producer is the PAIR (setter, reader); the
   lifter's helper name never enters the ledger.
7. `sbb` and `adc` are BOTH a flag reader and a flag setter, and each
   one writes TWO rows. They read the carry the previous flag-setting
   opcode left, and they set flags from their own arithmetic. So the
   walk emits, for one such instruction:
   - a VALUE row, typed by the destination operand's own width,
     `written_half` "the difference" for `sbb` and "the sum" for
     `adc`; and
   - a FLAGS row, typed `flags only`, `written_half` "the flags",
     and it is THIS row that a following flag reader links to.

   Both rows read the same operands, and the row that set the flags
   this instruction reads is their FIRST operand — the same shape
   rule 4 already gives a reader. Where no flag-setting opcode
   precedes, the walk records a hole by name; it does not invent a
   carry-in.

   Written into this CORE 2026-09-03, ahead of the code, under round
   12's binding rule 2 ("a shape the tree lacks is added to the tree
   first"). Provenance: log_158 TASK 59 (a); the gap it closes is
   log_153 §4.2. The realization is `ledger.py`
   (`FLAG_RULES["carry_in_setters"]`, `carry_in_stem`).

   What this rule does and does not claim: it fixes the LINEAGE, so
   `reference.py` (node 0_3_5_4) has a flag row with named operands to
   build a term from. Whether a given unit then proves is the gate's
   answer (node 0_3_5_5), not this node's.

8. Whether EVERY arithmetic setter should carry its own `flags only`
   row — not only the two that also read the carry — is not decided
   here and is not invented here. The two carry-in setters are
   separated because their flag row's operands differ from an ordinary
   setter's: they include the carry-in row.

```
Ledger.flag_rules
	attributes:
		setters
			"""
			stem -> the flags it sets
			"""
		comparison_setters
			"""
			stem -> writes a `flags only` row and
			does not repoint its destination
			"""
		carry_in_setters
			"""
			stem -> the value half and the flags
			half it writes, and the carry it
			reads (rule 7)
			"""
		readers
			"""
			stem -> the condition it reads
			"""
```

## settled rules

- **The flag reader links to the row that set the flags**, never to a
  running variable. Decision: log_153 §4.2 — the link cost 699
  wrongly-proved units and is correct.
- **An unconditional `jmp` is never a flag reader.** Decision:
  AgentMemory "ROUND 10 RULINGS" (3); log_152 §2.4; it closes log_147
  §4.1's fourth cause.
- **Irregular lifter names are never producers**; a flag-derived row
  is produced by the pair. Decision: log_142 addendum (the owner,
  2026-09-02).
- **`sbb` and `adc` write two rows: the value and the flags.** They
  are a reader and a setter at once, and a following flag reader links
  to their flags row, not to their value row and not to the earlier
  comparison. Decision: this CORE, `## design` rule 7, 2026-09-03;
  provenance log_158 TASK 59 (a), closing the gap log_153 §4.2 named.
  - Superseded by that rule, and named so the change is visible: the
    earlier statement that "`sbb` and `adc` as setters have no model,
    and that is stated rather than papered over" (log_153 §4.2). The
    statement was true when it was written and is now answered.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| setter table | `ledger47.py` (stem-based) | done |
| reader-to-setter link | `ledger48.py` | done |
| `flags only` rows | 19,934 over 30,436 units | done |
| condition resolution | `condition_table.py` (`SUFFIX_TO_COND`, `cond_to_z3`) | done |
| `sbb` / `adc` as setters (rule 7) | `ledger.py` (`FLAG_RULES["carry_in_setters"]`, `carry_in_stem`, the walk's carry-in branch) | done 2026-09-03 (task 59): 728 units of the 31,067 walked carry a flag pair whose setter is one of the two; `c/regen_34943` and `c/regen_35988` printed in `ledger_sample_walk_printed.txt` |
| the whole table, under the node's own name | `ledger.py` (`FLAG_RULES`), importing nothing from `ledger47`/`ledger48` | done (task 59) |
| superseded | `ledger47.py`'s walk, where `jmp` was a flag reader | superseded record |
