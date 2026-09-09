---
id: hq.research.compiler_graph.arch_unit
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: arch_unit
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: language
      designation: code (attribute)
      realize: false
    - name: operator_label
      designation: code (attribute)
      realize: false
    - name: operand_types
      designation: code (attribute)
      realize: false
    - name: body_bytes
      designation: code (attribute)
      realize: false
    - name: body_text
      designation: code (attribute)
      realize: false
    - name: arrival_contract
      path: node_0_3_1_1_5_arrival_contract/CORE_0_3_1_1_5_arrival_contract.md
    - name: context
      path: node_0_3_1_1_6_context/CORE_0_3_1_1_6_context.md
    - name: extract
      path: node_0_3_1_1_7_extract/CORE_0_3_1_1_7_extract.md
    - name: runtime_callee
      path: node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md
    - name: interp_unit
      path: node_0_3_1_1_9_interp_unit/CORE_0_3_1_1_9_interp_unit.md
---

# CORE 0_3_1_1 — arch_unit

## metadata

- **id:** hq.research.compiler_graph.arch_unit
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- language — code (attribute) *(realize: false)*
- operator_label — code (attribute) *(realize: false)*
- operand_types — code (attribute) *(realize: false)*
- body_bytes — code (attribute) *(realize: false)*
- body_text — code (attribute) *(realize: false)*
- [arrival_contract](node_0_3_1_1_5_arrival_contract/CORE_0_3_1_1_5_arrival_contract.md) — Per argument of a unit, the register family the body READS before it ever writes that family — a register family being one register and its narrower spellings taken as one thing, so `%rdi`, `%edi` and `%dil` are one family.
- [context](node_0_3_1_1_6_context/CORE_0_3_1_1_6_context.md) — Everything OUTSIDE a unit's body that the body needs in order to run: the constants it reaches rip-relative (addressed as an offset from the instruction pointer), the stack frame it addresses as its own, and the routines it transfers to.
- [extract](node_0_3_1_1_7_extract/CORE_0_3_1_1_7_extract.md) — The step that turns a probe's two builds into an arch-unit: it cuts the probe function's own bytes out of the ship object, disassembles them into one notation with objdump, and reads the compiler's DWARF records for the operands' encoding and width.
- [runtime_callee](node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md) — For a body that `call`s a routine of the compiler's OWN runtime, the step that extracts that routine's body out of the runtime archive on this machine and attaches it as a further arch-unit the caller references.
- [interp_unit](node_0_3_1_1_9_interp_unit/CORE_0_3_1_1_9_interp_unit.md) — The same object as an arch-unit, built for an interpreter or JIT handler instead of a compiled probe: the handler's own machine code, its arrival contract and its answer home.

## definition

One operator, in one language, on one operand-type pair, as the
machine code the compiler emitted for it — plus the facts needed to
run and compare that code: which register each argument arrives in,
which register (or memory) the answer leaves in, and the bytes of any
routine of the compiler's own runtime the body jumps into. An
arch-unit is the object of record; everything downstream is a view of
it and must preserve a return path to it.

## design

```
class ArchUnit
	attributes:
		language
		operator_label
			"""
			display only; never a key
			"""
		operand_types
			"""
			DWARF machine facts: encoding +
			width per operand; never a type name
			"""
		body_bytes
		body_text
			"""
			objdump of body_bytes, one notation
			"""
		arrival_contract
			"""
			sub-node: per argument, the register
			family the body READS before writing;
			read off the body, in the language's
			own register order
			"""
		context
			"""
			sub-node: everything outside the
			body the body needs to run —
			rip-relative constants, own stack
			frame, callees
			"""
	methods:
		extract
			"""
			sub-node: probe builds -> ArchUnit
			(bytes, text, DWARF facts)
			"""
		runtime_callee
			"""
			sub-node: for a body that `call`s a
			routine of the compiler's runtime,
			extract that routine's body from the
			runtime archive and attach it as a
			further ArchUnit the caller references
			"""
		interp_unit
			"""
			sub-node: the same object for an
			interpreter or JIT handler
			"""
```

## settled rules

- **Arch-units are extracted from the SHIP build; identity comes from
  the ANCHOR build.** Argument identity rests on three grounds: DWARF
  at the anchor, the forced probe (a−b vs b−a), the route detour.
  Decision: `../CORE_0_3_1_operator_equivalence.md` steps 2–4.
- **Typing is by machine fact**, DWARF encoding and width, never by a
  declared type name. Decision: AgentMemory (log_074 audit; int32_t
  ruling).
- **The arrival contract is read off the body**, in the language's
  own order (System V for c/cpp/rust/swift; go's `%rax,%rbx,%rcx,…`
  since go 1.17); a register inside a memory operand is a read.
  Decision: log_146 §5.4, fixed at first observation.
- **Context code is kept.** If the body needs code outside itself to
  run, that code is part of the unit's record. Decision: the owner,
  2026-08-30 ("if the system requires context code to function, that
  context code needs to be kept").
- **The arrival/computation boundary is lineage confluence** — the
  first instruction whose result depends on more than one input
  lineage — never "where the arguments meet". Decision: AgentMemory
  "ARRIVAL/COMPUTATION BOUNDARY IS LINEAGE CONFLUENCE".
- **A `call` into the compiler's own runtime is followed.** The
  callee (`__divti3`, `__udivti3`, `__modti3`, `__umodti3`, and any
  other routine shipped in libgcc / compiler-rt) is extracted from the
  runtime archive on this machine, produced by the same compiler, and
  becomes an ArchUnit the caller references; the caller's answer row
  is produced by that callee. Decision: the owner, 2026-09-03. Supersedes
  the "out of scope" note of the same day.
- **Interpreter and JIT handlers are arch-units too**, with arrival
  annotated plain / typed-pointer / tagged. Decision: AgentMemory
  (round 7, universal form for every unit).

## the unit's boundary — RULED by the owner 2026-09-05

**A unit is a function body: from just after the wrapper-function call
to just before the return.** For a compiled probe the wrapper is the
probe function we wrote. For an interpreter there is no wrapper of
ours, so the interpreter's OWN handler function is the wrapper and the
unit is that function's body.

the owner, 2026-09-05: "everything is wrapped in a function. it should be
just after the wrapper-function call to just before the return
statement. no?"

WHY, and it is a provenance argument rather than a taste one. A
function boundary is READ -- from the symbol table and DWARF. The
lineage carve that chose interpreter boundaries until now is
COMPUTED, by propagating operand taint to a fixpoint, and
`lineage_carve.py`'s own header records that it was wrong once: ruby's
optimised `rb_fix_plus` places its slow coercion path at LOWER
addresses than its fast path, and address-order propagation gave the
wrong region for that unit. A boundary that is read cannot be
disputed; one that is computed can be wrong unnoticed.

WHAT THIS RETIRES. The compiled population already met this rule --
`c/op_0`'s body is `xor %eax,%eax; test %edi,%edi; sete %al; ret`, the
whole probe function. The interpreter population did not: `ruby/
rb_fix_plus` is named as a function, while `cpython/
long_add_fastpath` is four instructions (`mov %rdi,%rax; mov %rsi,%r10;
add %r10,%rax; ret`) carved out of a function that also checks types,
branches on overflow, allocates a PyLongObject and manages reference
counts. The `_fastpath` suffix admits the slice. Those units are
re-carved to their handler function's body; the carved records stay on
disk as the superseded evidence.

WHAT CARRIES THE COST, ruled in the same breath. A whole handler body
writes memory, allocates, and answers with a pointer. the owner: "canonical
form should reduce unnecessary clutter with the reference to a virtual
memory system, and the super-op miner should be able to fill in the
missing stuff for z3." So: the universal canonical form's VIRTUAL
MEMORY (AgentMemory 2026-09-01) carries the memory traffic, and
recurring machinery inside a handler -- a reference-count sequence, an
allocation preamble -- is a RECURRING PATH, which is what the super-op
miner finds and what "modelled once by recurrence rank" already means.
Neither is new machinery; both are existing parts pointed at this.

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| extract | `op_units_<lang>.json` (original), `trickle_store/` + `op_units2_*` chunks (regenerated); DWARF in `dwarf_*.json` | done |
| arrival_contract | recorded per unit in `canon37_wrapped_*.json` / `canon38_*` as `arrival_families`; go's order corrected in log_146 | done; the IN-i ordering disagreement (log_153 §9) is a canonical_form defect, not this node's |
| context | `context record` per unit (round 6) | done |
| runtime_callee | `ledger.py` (`RUNTIME_TRANSFER_RULE`, `answer_registers_of_body`) — one row per register family the attached callee's own body changes, read off the body rather than asserted as the accumulator | **done** (task 78, log_185) — STALE FIGURE CORRECTED 2026-09-04 (round-15 bank): the "308 units" line was round-9's population and pre-dates the round-12 attachment work; the current measured population (task 83, log_189, over canon40's 30,324 proved units) is **3,927 units carrying a runtime-callee row, 49,362 rows over 30 distinct callees** — up from 608 rows before task 78's rule |
| interp_unit | `interp_canon35.json`, 11 units (java 2, cpython 1, ruby 4, php 4); `ruby/rb_big_plus` and `ruby/vm_opt_plus` have no ship body | done for 9; 2 refused by name |
