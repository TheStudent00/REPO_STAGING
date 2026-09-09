---
id: hq.research.compiler_graph.ledger.producer
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: producer
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_3_ledger/node_0_3_1_3_2_producer/CORE_0_3_1_3_2_producer.md
super_node:
    name: ledger
    path: ../CORE_0_3_1_3_ledger.md
sub_nodes:
    - name: kind
      designation: code (attribute)
      realize: false
    - name: mnem
      designation: code (attribute)
      realize: false
---

# CORE 0_3_1_3_2 — producer

## metadata

- **id:** hq.research.compiler_graph.ledger.producer
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledger](../CORE_0_3_1_3_ledger.md)

## sub_nodes

- kind — code (attribute) *(realize: false)*
- mnem — code (attribute) *(realize: false)*

## definition

What made a row's value, written as a typed object with a `kind` and a
second field naming the thing that kind points at — `mnem` for the
three kinds that name an instruction, `callee` for the one that names
a routine — and never as a bare string. `kind` says which sort
of thing produced the value: `arch_opcode` for a single instruction,
`flag_pair` for the pair of a flag-setting instruction and the
instruction that read those flags, `non_opcode_phrase` for a value no
instruction in the body wrote, and `runtime_callee` for a
value produced by a routine of the compiler's own runtime. Writing it
as an object is what lets the spelling guard read `{"kind":
"arch_opcode", "mnem": "xor"}` as machine form rather than as an
operator token.

## design

```
class Producer
	attributes:
		kind
			"""
			arch_opcode / flag_pair /
			non_opcode_phrase /
			runtime_callee
			"""
		mnem
			"""
			the machine mnemonic, or for a
			flag_pair the two mnemonics of
			setter and reader; absent on the
			kinds that name no mnemonic
			"""
		callee
			"""
			the runtime routine's name, on the
			runtime_callee kind only, which
			names a ROUTINE and not a mnemonic
			"""
```

**The third field, added 2026-09-03.** `runtime_callee` carries
`callee` where the other kinds carry `mnem`, because what produced the
value is a routine of the compiler's own runtime and not an
instruction. Written into this CORE ahead of the code, under round
12's binding rule 2. Provenance: log_158 TASK 59 (b), which states the
shape `{"kind": "runtime_callee", "callee": "__divti3"}`. The field is
machine form in the same sense `mnem` is, and the unmodified guard
already carries `callee` beside `mnem` and `bytes`.

The four kinds, each anchored:

1. **arch_opcode** — one instruction of the body wrote this row.
2. **flag_pair** — the row is flag-derived: the pair is (the opcode
   that set the flags, the opcode that read them). A lifter's helper
   name such as `amd64g_calculate_condition` never appears here.
3. **non_opcode_phrase** — no opcode in the body wrote this row; the
   phrase says why in plain words.
4. **runtime_callee** — a routine of the compiler's own runtime
   produced the value; its second field is `callee`. The routine's
   body is extracted from the archive on this machine and attached as
   a further arch unit the caller references. See
   [runtime_callee](../../node_0_3_1_1_arch_unit/node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md).

## settled rules

- **A producer is a typed object `{kind, mnem}`, never a bare
  string**, so the unmodified guard reads it as machine form.
  Decision: AgentMemory "ROUND 10 RULINGS" (5); log_147 §13.3.
- **Irregular lifter names are never producers.** A flag-derived row
  is produced by the PAIR of arch opcodes. Decision: log_142
  addendum (the owner, 2026-09-02); carried in [ledger](../CORE_0_3_1_3_ledger.md).
- **The shape change is the answer to a spelling collision, not an
  exemption.** An artifact whose mnemonic is spelled like an operator
  token changes its SHAPE rather than quieting the guard. Decision:
  log_147 §13.7; log_150 §3.
- **`runtime_callee` was not invented ahead of its ruling, and the
  ruling has now come.** the owner, 2026-09-03: "if its within the compiler,
  its not a library call." Decision: log_158 TASK 59; the earlier
  statement (log_153 §3.4, log_152 §9.2 — the kind stays planned until
  ruled) is answered rather than dropped.

## realization (what exists on disk, 2026-09-03)

Home: `PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| producer_object | `ledger48.py` (`producer_object`) | done |
| typed everywhere, guard-checked | `canon38_guard.py`, `canon38_guard.json`, `canon38_guard_transcript.txt` | done (log_152 §6.1) |
| `runtime_callee` kind | `ledger.py` (`Producer.runtime_callee`, `PRODUCER_KINDS`) and `runtime_callee.py` | done 2026-09-03 (task 59); 104 `runtime_callee` rows over the 241-unit computed sample of `ledger_sample_walk_printed.txt`; 304 of the 308 recorded callers attached (`runtime_callee_attachments.json`) |
| `Producer` as a class, under the node's own name | `ledger.py` (`class Producer`), importing nothing from `ledger47`/`ledger48` | done (task 59) |
| superseded | `ledger47.py`'s bare-string producers | superseded record |
