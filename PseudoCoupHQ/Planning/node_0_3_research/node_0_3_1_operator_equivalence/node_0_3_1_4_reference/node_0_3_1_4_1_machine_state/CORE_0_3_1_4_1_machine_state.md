---
id: hq.research.compiler_graph.reference.machine_state
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: machine_state
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_4_reference/node_0_3_1_4_1_machine_state/CORE_0_3_1_4_1_machine_state.md
super_node:
    name: reference
    path: ../CORE_0_3_1_4_reference.md
sub_nodes:
    - name: registers
      designation: code (attribute)
      realize: false
    - name: flags
      designation: code (attribute)
      realize: false
    - name: memory
      designation: code (attribute)
      realize: false
    - name: stack
      designation: code (attribute)
      realize: false
    - name: x87
      designation: code (attribute)
      realize: false
---

# CORE 0_3_1_4_1 — machine_state

## metadata

- **id:** hq.research.compiler_graph.reference.machine_state
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [reference](../CORE_0_3_1_4_reference.md)

## sub_nodes

- registers — code (attribute) *(realize: false)*
- flags — code (attribute) *(realize: false)*
- memory — code (attribute) *(realize: false)*
- stack — code (attribute) *(realize: false)*
- x87 — code (attribute) *(realize: false)*

## definition

The symbolic machine the reference walks a body over: registers, the
condition flags, memory, the machine stack and the x87 stack, each
holding a z3 term rather than a number. Registers start as free symbols
named `seed_<family>`, so a proof is about every possible input value
at once. Flags are held as a triple — the flag-setting opcode and its
two operand terms — rather than as separate bits, because a condition
is then rebuilt exactly from what set it. Memory is a z3 array with the
unit's rip-relative constants as `ripconst_<n>` symbols. The machine
stack and the x87 stack are NOT modelled today, and their absence is
why 5,602 units are undecided.

## design

```
class MachineState
	attributes:
		registers
			"""
			register family -> term; seeded as
			seed_<family> free symbols so the
			proof covers every input
			"""
		flags
			"""
			the (setter opcode, L, R) triple the
			last flag-setting instruction left
			"""
		memory
			"""
			a z3 array; the unit's rip-relative
			constants enter as ripconst_<n>
			symbols
			"""
		stack
			"""
			the machine stack as (rsp term ->
			array), so a push and its pop round
			trip. PLANNED
			"""
		x87
			"""
			eight positions and a top index,
			each holding an 80-bit extended
			float term (z3 FPSort(15, 64)),
			a load keyed
			x87_<mangled memory operand>.
			CORRECTED 2026-09-03. PLANNED
			"""
```

## settled rules

- **The machine stack and the x87 stack are modelled**, in the same
  shape as the ledger's STACK and X87 blocks. Decision: AgentMemory
  "ROUND 10 RULINGS" (2) applied here; today's absence is why 5,602
  units are undecided (log_153 §4.3).
- **An x87 position holds an `FPSort(15, 64)` term, not a bit
  vector.** An x87 register holds the 80-bit extended form: 15
  exponent bits and a 64-bit significand. A load from memory is the
  symbol `x87_<mangled memory operand text>` (`fldt 0x18(%rsp)` gives
  `x87_0x18_rsp_`). CORRECTION to this CORE's own earlier wording
  ("each holding a bit-vector term"), 2026-09-03. Provenance
  (PROTOCOL §2): `layer4c.py` section 1, `X87_SORT = z3.FPSort(15,
  64)` and `x87_symbol`; the printed terms of log_153 §4.3, which
  read `x87_0x18_rsp_`. Reason the earlier wording is wrong: the
  ledger route already builds x87 values at that sort, and z3 cannot
  compare a bit vector with a float, so a bit-vector reference could
  never be gated against the ledger's term — the two routes would be
  incomparable by construction.
- **The flag model is a triple** (setter, L, R), resolved through
  `condition_table.py`. Decision: log_081 route (a); "ROUND 10
  RULINGS" (3).
- **L and R are the two values the CONDITION reads, which are not
  always the setter's two operands.** A comparison-shaped setter
  (`cmp`, `sub`, `sbb`, `neg`, and every float or x87 compare) leaves
  its own two sides. A setter whose zero and sign bits come from its
  RESULT — the logic family and the shifts — leaves `(result, 0)`,
  which is the shape this node already used for `test`
  (`("test", L & R, 0)`). Reason the silence was wrong: with the
  operands recorded instead, a condition after `or %rsi,%rdi` reads
  `seed_rdi != seed_rsi` where the machine reads
  `(seed_rdi | seed_rsi) != 0` — measured on 1,338 units of the
  30,436 on which the gate's route one disproved a term route two
  proved, which the gate CORE's "two routes never contradict" names as
  a defect to be found. The carry and the overflow are still rebuilt
  from the setter's name, and are False for that family, so nothing
  else moves. Decision: this CORE, 2026-09-03, on the evidence of
  log_160 §3 (task 58).
- **`sbb` and `adc` set flags from their own arithmetic.** Decision:
  same; carried in [reference](../CORE_0_3_1_4_reference.md) settled rules.
- **Registers are seeded as free symbols**, so a verdict is about
  every value of every input row rather than one sample. Decision:
  [gate](../../node_0_3_1_5_gate/CORE_0_3_1_5_gate.md) definition.
- **There is exactly ONE machine state, the reference's.** No gate
  carries its own. Decision: [reference](../CORE_0_3_1_4_reference.md) settled rules, 2026-09-03 (the
  finding of log_157 §3.1).

- **A STATE IS MERGEABLE WITH ANOTHER STATE, AND THE MERGE REFUSES
  RATHER THAN GUESSES.** Registers, memory cells, machine-stack cells
  and x87 positions merge as `If(cond, a, b)` per cell — a family or
  cell one side never touched reads its own seed, so the merge covers
  every place either side wrote. The FLAG TRIPLE merges only when both
  sides' SETTER carries one name (L and R then merge as `If` terms);
  differing setters leave the triple `("merged", ...)`, and a later
  condition read is REFUSED by name. The machine stack's depth and the
  x87 stack's depth must agree across the sides; a disagreement is
  REFUSED by name. Decision: this CORE, 2026-09-03 (task 64), carried
  from [reference](../CORE_0_3_1_4_reference.md)'s settled rules,
  where the shape is stated in full with its provenance.

- **A RIP-RELATIVE ADDRESS COMPUTATION READS THE SAME COUNTER AS A
  RIP-RELATIVE LOAD.** This CORE already says memory carries "the
  unit's rip-relative constants as `ripconst_<n>` symbols"; it was
  silent on `lea 0x2e57(%rip),%rax`, which computes an ADDRESS the
  artifact does not hold rather than reading a value it does not hold.
  Both are the body's next `ripconst_<k>`, off the one positional
  counter, so the reference and the ledger transcription name one
  constant. 32 units stopped on the silence (log_160 §1.7). Decision:
  this CORE, 2026-09-03 (task 64); provenance
  `MachineState.rip_constant` and `layer4.memory_load_term`'s own
  positional keying.

- **A SUB-32-BIT WRITE INTO THE ACCUMULATOR PAIR PRESERVES THE
  REGISTER'S UPPER BITS.** `MachineState`'s ordinary register write is
  `full64` — a sub-64-bit value zero-extends — which is the machine's
  rule for a 32-bit destination and NOT its rule for an 8- or 16-bit
  one (`mov $1,%al` leaves the upper 56 bits of `%rax` alone). The
  8- and 16-bit division and widening-multiply forms write `%al`/`%ah`
  and `%ax`/`%dx`, so they compose the family's new value from the old
  one rather than going through the ordinary write. `full64` is
  UNCHANGED for every other opcode; nothing outside those forms moves.
  Decision: this CORE, 2026-09-03 (task 64). Provenance: `layer4.
  full64`, which this file reproduces, and Intel SDM vol. 1 §3.4.1.1's
  statement of the three destination-width rules (evidence class:
  human interpretation of stated design, cross-checked by the 20 units
  themselves proving under it).

## realization (what exists on disk, 2026-09-05)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| registers, flags, memory | `reference.py`, class `MachineState` | **done** — `canon9`/`canon10` are records carrying a superseded header line |
| conditions | `condition_table.py`, reached through `reference.py`'s `predicate_of` | done |
| stack | `reference.py`, `MachineState.stack` = `{"pointer": seed_rsp, "offset": 0, "cells": {}}`, written by `push_value` and read by `pop_value`, keyed by the byte offset from the rsp the unit was entered with, so a push and its pop round trip; a pop at an offset this body never wrote is REFUSED by name | **done** |
| x87 | `reference.py`, `MachineState.x87` = `{"slots": [None] * 8, "top": 0, "depth": 0}`, each position an `FPSort(15, 64)` term, a load keyed `x87_<mangled memory operand>`; `x87_push` refuses a ninth value by name, `x87_at` refuses a read of a position this body never loaded | **done** |
| x87 control word | nothing | **not required, and the census is why**: of the 62,156 bodies canon38 and canon40 hold, 2,810 spell an x87 arch opcode and 0 spell any opcode that reads or writes the control word (`t91_reference_evidence.json` B3). The rule "no entry invented for an opcode no body contains" leaves it out |
| what the gaps cost, re-measured | of log 153's 5,602 undecided units, **2,356 now prove**, 2,969 disprove and 277 stay undecided | **measured** — task 91, `t91_audit_printed.txt` |
