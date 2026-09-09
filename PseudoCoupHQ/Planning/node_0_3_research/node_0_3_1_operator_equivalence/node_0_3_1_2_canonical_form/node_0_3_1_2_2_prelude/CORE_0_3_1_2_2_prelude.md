---
id: hq.research.compiler_graph.canonical_form.prelude
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), rule
node:
    name: prelude
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/node_0_3_1_2_2_prelude/CORE_0_3_1_2_2_prelude.md
super_node:
    name: canonical_form
    path: ../CORE_0_3_1_2_canonical_form.md
sub_nodes: []
---

# CORE 0_3_1_2_2 — prelude

## metadata

- **id:** hq.research.compiler_graph.canonical_form.prelude
- **level:** 4
- **status:** draft
- **designation:** code (method), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [canonical_form](../CORE_0_3_1_2_canonical_form.md)

## sub_nodes

*(none yet)*

## definition

The standardized lines placed BEFORE the compiler's body that put each
arriving value into the register the compiler's own code expects it in.
Each input is loaded in two steps: the ledger entry for the input block
is read to get that block's base address, then the row at its offset in
that block is read into the destination register. The destination
register doubles as the pointer for its own first step, so the prelude
reserves no register of its own. A row wider than a general register —
a 16-byte vector row — is moved with `movdqu`, which needs one general
scratch register that is not an arrival family. The prelude MUST emit
its loads in arrival_contract order.

## design

The rule, as numbered statements:

1. One IN row per argument, numbered in
   [arrival_contract](../../node_0_3_1_1_arch_unit/node_0_3_1_1_5_arrival_contract/CORE_0_3_1_1_5_arrival_contract.md)
   order: IN-i holds argument i.
2. The load is two steps. Step one reads the ledger entry for the IN
   block, rip-relative from the ledger's absolute address, into the
   destination register. Step two reads the row at IN-i's offset from
   that base, into the same destination register.
3. The destination register is the pointer for its own step one. No
   register is reserved and no register is renamed.
4. A 16-byte vector row is moved with `movdqu` into its vector
   destination, which needs one general scratch register. That
   scratch must not be an arrival family, so the body cannot read it
   before writing it.
5. The prelude emits in arrival_contract order — IN-0 first,
   whichever family that is. Emitting the vector arrivals first is a
   defect, not an alternative order.
6. The prelude writes only the registers the arrival contract names,
   plus that one scratch. This is structural check C2.

```
CanonicalForm.prelude
	methods:
		emit
			"""
			arrival_contract -> the prelude
			lines, in contract order
			"""
		emit_general_row
			"""
			IN-i, general destination -> the two
			step lines
			"""
		emit_vector_row
			"""
			IN-i, vector destination -> movdqu
			through one general scratch
			"""
```

## settled rules

- **The two-step load through the ledger**, so rows need not be
  contiguous and no register is a region base. Decision: log_141 §8.2;
  the lemma is log_146 §2.6.
- **Rows are sized by type**; a 16-byte value gets a 16-byte row.
  Decision: log_141 §8, log_146 §2.5.
- **IN rows are numbered in arrival_contract order, and the prelude
  emits in that same order.** The vector-first ordering is a defect.
  Decision: [canonical_form](../CORE_0_3_1_2_canonical_form.md) settled rules, this CORE's super-node,
  2026-09-03; the disagreement is printed in log_153 §9.
- **The prelude writes only arrival registers plus one non-arrival
  scratch** — structural check C2. Decision: log_146 §5.3.
- **No register is reserved and none is renamed.** Decision:
  AgentMemory "REFINEMENT — NO DESIGNATED REGISTERS"; [canonical_form](../CORE_0_3_1_2_canonical_form.md).

## realization (what exists on disk, 2026-09-03)

Home: `PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| emit | `ledger48.build_prelude` (in `ledger48.py`) | done for 30,436 units |
| drivers | `canon38_wrapped.py`, `canon38_interp.py`, `canon38_regen.py` | done |
| C2 checked per unit | `canon38_gate.py` | done |
| emit, emit_general_row, emit_vector_row, IN CONTRACT ORDER | `canonical_form.Prelude` | done, 2026-09-03 (log_162); 5,818 of 31,078 units were affected, `c/op_105` printed before and after |
| superseded | `ledger47.py`'s prelude, `canon37_wrapped.py` | superseded records |
