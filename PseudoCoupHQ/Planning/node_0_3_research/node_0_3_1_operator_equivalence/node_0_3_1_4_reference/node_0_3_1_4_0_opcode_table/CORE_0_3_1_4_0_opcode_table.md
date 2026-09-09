---
id: hq.research.compiler_graph.reference.opcode_table
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (attribute)
node:
    name: opcode_table
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_4_reference/node_0_3_1_4_0_opcode_table/CORE_0_3_1_4_0_opcode_table.md
super_node:
    name: reference
    path: ../CORE_0_3_1_4_reference.md
sub_nodes: []
---

# CORE 0_3_1_4_0 — opcode_table

## metadata

- **id:** hq.research.compiler_graph.reference.opcode_table
- **level:** 4
- **status:** draft
- **designation:** code (attribute)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [reference](../CORE_0_3_1_4_reference.md)

## sub_nodes

*(none yet)*

## definition

THE one table from mnemonic to meaning: for each arch opcode the
corpus actually spells, which places it reads, which places it writes,
and the builder that turns its operands into a z3 term. It is shared:
the reference's simulator and
[transcribe](../../node_0_3_1_6_term/node_0_3_1_6_2_transcribe/CORE_0_3_1_6_2_transcribe.md)
read the SAME table, which is what makes the two gate routes
independent evidence — one tests meanings, the other tests the ledger's
wiring, and they cannot drift apart on what an opcode means. Today the
table is split across three files, which is the debt this node names.

## design

```
Reference.opcode_table
	attributes:
		entries
			"""
			mnemonic (one size suffix stripped)
			-> reads, writes, term builder. One
			entry per arch opcode the corpus
			spells; no entry invented for an
			opcode no body contains
			"""
	methods:
		builder_for
			"""
			producer -> the term builder, or
			nothing when the opcode has no
			model; 'nothing' is what the census
			counts
			"""
```

The families the entries cover:

1. **Integer arithmetic and logic.** Division is the careful case:
   quotient is `SDiv` or `UDiv` and remainder is `SRem` or `URem`,
   whose sign follows the dividend — never z3's `%` (`bvsmod`), whose
   sign follows the divisor.
2. **Conditions.** A flag-derived value is built from the (setter, L,
   R) triple through `condition_table.py`'s `SUFFIX_TO_COND` and
   `cond_to_z3`.
3. **Floating point.** Real IEEE terms: `fpAdd` under
   round-to-nearest-even, lane 0 written, the upper lanes kept — not
   uninterpreted functions standing in for arithmetic.
4. **Vector lanes.** The per-lane names in `vex_names.py`, e.g.
   `Add32F0x4` built by `build_lane_arith`.

## settled rules

- **One table, shared with `term.transcribe`**, so route one tests
  meaning and route two tests wiring. Decision: [reference](../CORE_0_3_1_4_reference.md) settled
  rules, 2026-09-03; [term](../../node_0_3_1_6_term/CORE_0_3_1_6_term.md).
- **Remainder is `SRem`/`URem`, never z3's `%`.** Decision: log_153
  §5, with the counterexample `7 % -3`; reproduced log_157 §3.1.
- **Float opcodes are real IEEE terms**, not uninterpreted functions;
  a reference that leaves them uninterpreted returns UNDECIDED.
  Decision: round 4 (`vex_names.build_lane_arith`); log_147 §6.1.
- **An opcode with no builder is a census row, not a silent gap.**
  Decision: [census](../../node_0_3_1_6_term/node_0_3_1_6_4_census/CORE_0_3_1_6_4_census.md);
  log_147 §3.3.
- **THE CORPUS THE TABLE IS BUILT OVER INCLUDES THE ATTACHED CALLEE
  BODIES.** An arch unit extracted from a toolchain's own builtins
  archive is an arch unit; the opcodes its body spells — `endbr64`,
  `bsr`, `cmovle`, … — are entries in THIS table, with reads, writes
  and a builder, and not a second table beside it. The "no entry for
  an opcode no body contains" rule is unchanged: the inventory simply
  now counts the attached bodies too. Decision:
  [runtime_callee](../../../node_0_3_1_1_arch_unit/node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md)
  settled rules, 2026-09-03 (task 63); evidence
  `Research/op_pipeline/canon39_callee_opcodes.json`.

- **A CONDITIONAL TRANSFER IS AN ENTRY WITH A CONDITION BUILDER, NOT A
  CENSUS ROW.** `j<cc>` was carried as an entry with NO builder and
  the cause "a transfer or trap, and this reference walks a body in
  text order" — 499 units stopped there (log_160 §1.7). It now carries
  the same condition builder `set<cc>` and `cmov<cc>` carry, through
  `condition_table.py`'s `SUFFIX_TO_COND` / `cond_to_z3`; what the
  walk DOES with the resulting condition term is the reference's
  control-flow rule, not the table's. `jmp` stays an entry with no
  builder because it reads nothing; `ud2` and `call` likewise. The
  "no entry invented for an opcode no body contains" rule is
  untouched. Decision: this CORE, 2026-09-03 (task 64), following
  [reference](../CORE_0_3_1_4_reference.md)'s branch-following rules.

- **8- AND 16-BIT DIVISION AND WIDENING MULTIPLY ARE ENTRIES LIKE ANY
  OTHER, AND THEIR DESTINATION IS A PAIR OF BYTES OR WORDS INSIDE ONE
  REGISTER.** At width 32 and 64 the pair is two register families
  (accumulator and data register); at width 16 it is `%ax` and `%dx`,
  and at width 8 it is `%al` and `%ah` — two halves of ONE family.
  The builder composes the family's new value from its old one, which
  is why the machine_state CORE's upper-bits rule sits beside this
  one. Decision: this CORE, 2026-09-03 (task 64); the 20 units of
  log_160 §1.7; the table rows are in
  [destination_rules](../../node_0_3_1_3_ledger/node_0_3_1_3_3_destination_rules/CORE_0_3_1_3_3_destination_rules.md).

## realization (what exists on disk, 2026-09-05)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| lane and float builders | `vex_names.py`, folded into the one table | done |
| condition builders | `condition_table.py`, folded into the one table | done |
| producer -> builder table | `layer4.py`, folded into the one table | done |
| ONE shared table | `reference.py`'s `OpcodeTable`, one `Entry` per arch mnemonic, `builder_for` returning nothing for a census row; `term.py` line 362 sets `self.opcode_table = reference.opcode_table`, so the transcription reads THE SAME OBJECT | **done** |
| the wrong remainder in the simulator route | `reference.py`'s `build_division` and `build_narrow_division`: `z3.SRem` / `z3.URem` for the remainder, `z3.SDiv` / `z3.UDiv` for the quotient; the z3 operator appears nowhere in either | **done**. Measured on the CORE's own counterexample: `SRem(7, -3) = 1` where the z3 operator gives `-2` (`t91_reference_evidence.json` B1). All **415** of log 153's withdrawn disproofs prove under it (`t91_audit_printed.txt`) |
| what route two uses, deliberately not this table | `gate.prove_term_against_text` walks the body with `layer4`'s producer table | done, and it stays that way: if route two read this table it would be route one again, and the two routes would share a code path (`gate.py`'s own header) |
