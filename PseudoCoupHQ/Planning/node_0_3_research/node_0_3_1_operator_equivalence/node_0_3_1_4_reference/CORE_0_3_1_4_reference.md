---
id: hq.research.compiler_graph.reference
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: reference
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_4_reference/CORE_0_3_1_4_reference.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: opcode_table
      path: node_0_3_1_4_0_opcode_table/CORE_0_3_1_4_0_opcode_table.md
    - name: machine_state
      path: node_0_3_1_4_1_machine_state/CORE_0_3_1_4_1_machine_state.md
    - name: simulate
      designation: code (method)
      realize: false
    - name: answer_of
      designation: code (method)
      realize: false
---

# CORE 0_3_1_4 — reference

## metadata

- **id:** hq.research.compiler_graph.reference
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- [opcode_table](node_0_3_1_4_0_opcode_table/CORE_0_3_1_4_0_opcode_table.md) — THE one table from mnemonic to meaning: for each arch opcode the corpus actually spells, which places it reads, which places it writes, and the builder that turns its operands into a z3 term.
- [machine_state](node_0_3_1_4_1_machine_state/CORE_0_3_1_4_1_machine_state.md) — The symbolic machine the reference walks a body over: registers, the condition flags, memory, the machine stack and the x87 stack, each holding a z3 term rather than a number.
- simulate — code (method) *(realize: false)*
- answer_of — code (method) *(realize: false)*

## definition

THE one symbolic simulator of the machine that every proof in this
research is made against. It walks a unit's own ship body instruction
by instruction over symbolic registers, flags, memory, the machine
stack and the x87 stack, and returns the z3 term the body leaves in
its answer home. There is exactly one of it; a gate route that proves
"against ship" proves against this object. It exists as its own node
because the pipeline has so far carried three (`canon9`, `canon10`,
`canon12` behaviour checkers) plus a fourth inside `gate48.py`, and
the 415-unit remainder withdrawal of log 153 was two of them
disagreeing.

## design

```
class Reference
	attributes:
		opcode_table
			"""
			sub-node: mnemonic -> (reads, writes,
			term builder). One entry per arch
			opcode the corpus spells; the same
			table Term.transcribe uses, so the
			two routes share meanings and
			nothing else
			"""
	methods:
		simulate
			"""
			(body_text, arrival_contract) ->
			MachineState after the body
			"""
		answer_of
			"""
			MachineState + answer_home -> z3 term
			"""
		blocks_of
			"""
			body lines -> the body's own
			control-flow graph: blocks cut at the
			positional labels and after every
			transfer, with the condition on each
			edge and the out-of-unit edges marked
			"""
		walk_body
			"""
			(MachineState, body lines, callees)
			-> the state after the whole graph,
			visited in reverse postorder, joins
			entered on the merge. The one entry
			point every caller uses -- `simulate`,
			the gate's wrapped route, and
			`term.runtime_row`'s step into an
			attached callee
			"""
		merge
			"""
			(condition, taken state, not-taken
			state) -> one state, If per cell; the
			flag triple only when both setters
			carry one name; refuses by name on a
			stack-depth or x87-depth disagreement
			"""
		guard_rows
			"""
			the conditions under which a side
			transferred OUT of the unit, one row
			each, left on the state the walk
			returns
			"""


class MachineState
	attributes:
		registers
			"""
			family -> term; seeded as
			seed_<family> symbols
			"""
		flags
			"""
			the (setter opcode, L, R) triple the
			last flag-setting instruction left
			"""
		memory
			"""
			z3 array; rip-relative constants as
			ripconst_<n> symbols
			"""
		stack
			"""
			the machine stack as (rsp term ->
			array) so push/pop round-trip
			"""
		x87
			"""
			eight positions, top index; each a
			80-bit extended float term
			(z3 FPSort(15, 64)), keyed
			x87_<mangled memory operand>
			-- CORRECTED 2026-09-03, see
			machine_state's settled rules
			"""
```

## settled rules

- **One reference.** Every "proved against ship" verdict names this
  object; no gate may carry its own simulator. Decision: this CORE,
  2026-09-03 (the finding of log_157 §3.1).
- **Integer division: quotient is `SDiv`/`UDiv`, remainder is
  `SRem`/`URem`** (sign follows the dividend), never z3's `%`
  (`bvsmod`, sign follows the divisor). Decision: log_153 §5, with
  the counterexample `7 % -3`; reproduced log_157 §3.1.
- **Float opcodes are real IEEE terms** (`fpAdd` under RNE, lane 0
  written, upper lanes kept), not uninterpreted functions. Decision:
  round 4 (vex_names.py `build_lane_arith`); a reference that leaves
  them uninterpreted returns UNDECIDED, which is the current
  route-one limit (log_147 §6.1).
- **The machine stack and the x87 stack are modelled**, in the same
  shape as the ledger's STACK and X87 blocks. Decision: "ROUND 10
  RULINGS" (2) applied here; today's absence is why 5,602 units are
  undecided (log_153 §4.3).
- **The flag model is a triple** (setter, L, R) resolved through
  `condition_table.py`'s `SUFFIX_TO_COND` / `cond_to_z3`; `sbb`/`adc`
  set flags from their own arithmetic. Decision: log_081 route (a);
  "ROUND 10 RULINGS" (3).
- **`simulate` follows intra-unit branches and steps into attached
  runtime callees.** Today it walks in text order and refuses a
  conditional transfer (499 units, log_160 §1.7) and refuses every
  `call` (3,419 units). The shape: at a `j<cc>` the walk forks on the
  condition term and the two states merge at the join label as
  `If(cond, a, b)` per register/flag/memory cell; a transfer OUT of
  the unit on one side (a panic/trap) makes that side's state
  unreachable and the guard row records it; at a `call` whose callee
  is attached (runtime_callee) the walk enters the callee's body with
  the arrival contract of the callee, and returns to the caller.
  Decision: coordinator, 2026-09-03 (log_165 §3), refining this
  CORE's design — a shape the tree lacked, added before round 13
  codes it.
- **8- and 16-bit division and widening multiply are modelled** (20
  units, log_160 §1.7): the AH/AL and DX:AX destination pairs enter
  `DESTINATION_RULES` and the opcode table. Decision: same.

- **A BODY IS WALKED AS ITS OWN CONTROL-FLOW GRAPH, NOT AS A LINE OF
  TEXT.** The blocks are cut at the body's own positional labels and
  after every transfer; the walk visits them in reverse postorder; a
  block reached from more than one place is entered on the MERGE of
  its incoming states. A body whose control flow has a CYCLE is
  REFUSED by name — no loop invariant is invented. Decision: this
  CORE, 2026-09-03 (task 64), refining the `simulate` rule above,
  which stated the fork and the merge and did not state the order the
  blocks are visited in or what happens to a cycle. Provenance: the
  attached body `clang++/__extendhfsf2` (log_167 §3.3) has five
  transfers over forty instructions and four join points, so a
  two-sided fork/merge with no block order does not describe it.

- **A TRANSFER OUT OF THE UNIT MAKES ITS SIDE UNREACHABLE.** A
  transfer whose target is not a positional label DEFINED IN THIS
  BODY leaves the unit — go's `call x_runtime_panicshift`, rust's
  `call ..._panic_const_div_by_zero`, `ud2`. The side that takes it
  contributes NOTHING to the merge, and its condition is recorded on
  the guard row. When every side of a body transfers out, the body
  leaves no answer and is refused by name. Decision: this CORE,
  2026-09-03 (task 64). Reason it is the sound reading rather than a
  convenience: the ledger's own OUT-0 term is the NORMAL-PATH term
  (AgentMemory, "SEED = the normal-path computation graph"), and the
  guard row is where the condition already lives, so an unreachable
  side is what makes the two routes comparable at all.

- **WHAT A MERGE DOES TO EACH KIND OF STATE, AND WHERE IT REFUSES.**
  Registers, memory cells, machine-stack cells and x87 positions merge
  as `If(cond, taken, not-taken)` per cell. The FLAG TRIPLE is not a
  value and does not merge that way: it merges only when both sides'
  SETTER is the same name, in which case the two sides' L and R merge
  as `If` terms; when the setters differ the merged flags are the
  triple `("merged", ...)` and any later condition read is REFUSED by
  name rather than answered. The machine stack's depth and the x87
  stack's depth must agree across the merged sides; when they differ
  the merge is REFUSED by name. Decision: this CORE, 2026-09-03 (task
  64). Provenance for the flag rule: this CORE's own `flags` shape is
  "(setter, L, R)", and `predicate_of` reads the SETTER's name to
  choose between the integer route, the float route and the carry
  route — two different setters have no single name, so an `If` over
  L and R alone would answer with the wrong rule.

- **A `call` WITH AN ATTACHED CALLEE IS NOT A TRANSFER.** The walk
  enters the callee's own body — itself a control-flow graph, walked
  by the same rule — with the callee's OWN arrival contract, which is
  the families its text reads before it writes them
  (`canon39_callee_units.json`, `arrival_families`); the caller's own
  registers already hold those values, so nothing about a calling rule
  is assumed. It returns through the callee's ANSWER REGISTER: `xmm0`
  when the callee's body writes `xmm0`, and `rax` otherwise, computed
  off the callee's own body rather than declared. A callee that
  reaches itself is refused by name (cycle guard). A `call` whose
  callee is NOT attached is a transfer out of the unit by the rule
  above. Decision: this CORE, 2026-09-03 (task 64), realizing the
  `simulate` rule's "enters the callee's body with the arrival
  contract of the callee, and returns to the caller" — which did not
  say WHERE the answer is read. Provenance:
  `node_0_3_1_1_8_runtime_callee`'s `arrival_families`, and
  `term.runtime_row`, which already reads a callee's answer at the
  place the CALLER'S LEDGER ROW names; the rule here is the same fact
  computed when no such row exists.

- **A RIP-RELATIVE ADDRESS COMPUTATION IS THE BODY'S NEXT
  `ripconst_<k>`** (32 units, log_160 §1.7). `lea 0x2e57(%rip),%rax`
  computes an address this artifact does not hold, exactly as a
  rip-relative READ returns a value this artifact does not hold, and
  both are keyed by their position in the body — the same counter, so
  the reference and the ledger transcription name one constant.
  Decision: this CORE, 2026-09-03 (task 64), from log_166 TASK 64's
  own wording. Provenance: `MachineState.rip_constant`, already the
  positional keying `layer4.memory_load_term` uses.

## realization (what exists on disk, 2026-09-05)

| part | current file | status |
|---|---|---|
| the ONE simulator | `reference.py` — class `Reference`, class `MachineState`, one `OpcodeTable` | **done** (task 57, extended by tasks 58 and 64) |
| simulate (integer, cmp/test flags) | `reference.py` | done |
| simulate (division family) | `reference.py`, `build_division` / `build_narrow_division` — `SDiv`/`UDiv` and `SRem`/`URem` | **done**; the wrong remainder is gone |
| opcode_table (term builders) | `reference.py`'s `OpcodeTable`, folding in `vex_names.py`, `condition_table.py` and `layer4.py`'s producer table; `term.py` line 362 reads the SAME object | **done** — one table, shared with `term.transcribe` |
| machine_state.stack | `reference.py`, `MachineState.stack` = `{pointer, offset, cells}` with `push_value` / `pop_value` | **done** |
| machine_state.x87 | `reference.py`, `MachineState.x87` = `{slots (eight), top, depth}` at `FPSort(15, 64)`, with `x87_push` / `x87_pop` / `x87_at` / `x87_set` | **done** |
| the four superseded simulators | `canon9_behaviour_check.py`, `canon10_behaviour_check.py`, `canon12_behaviour_check.py`, and `gate48.py`'s route through `canon10` | **records**; each of the three carries one `# SUPERSEDED 2026-09-03 by reference.py` header line and nothing else changed. `gate.py` imports NO behaviour checker (`grep -c "^import canon[0-9]*_behaviour_check" gate.py` = 0) |
| what the one reference is worth, measured | 415 of 415 withdrawn disproofs prove; 2,356 of 5,602 undecided prove; 245 old proofs fall, all of them route-two proofs of the alternative-stretch defect log_168 §6 named | **measured** — task 91, `t91_audit_printed.txt`, `t91_lost_proofs_printed.txt` |

The x87 CONTROL WORD is not modelled, and the census says why: over the
62,156 bodies canon38 and canon40 hold together, 2,810 spell an x87
arch opcode and **not one spells `fldcw`, `fnstcw`, `fstcw`, `fldenv`,
`fnstenv`, `fstenv`, `fnsave`, `frstor`, `finit`, `fninit`, `fnclex` or
`fclex`** — the opcodes that read or write it. The opcode_table rule
"no entry invented for an opcode no body contains" therefore leaves it
out. Evidence: `t91_reference_evidence.json`, section B3.
