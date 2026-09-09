---
id: hq.research.compiler_graph.canonical_form.epilogue
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: epilogue
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/node_0_3_1_2_3_epilogue/CORE_0_3_1_2_3_epilogue.md
super_node:
    name: canonical_form
    path: ../CORE_0_3_1_2_canonical_form.md
sub_nodes: []
---

# CORE 0_3_1_2_3 — epilogue

## metadata

- **id:** hq.research.compiler_graph.canonical_form.epilogue
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [canonical_form](../CORE_0_3_1_2_canonical_form.md)

## sub_nodes

*(none yet)*

## definition

The standardized lines placed BEFORE every `ret` in the compiler's
body that store the compiler's own result register into OUT-0, the
answer row. It reaches that row the same two-step way the prelude
reaches an input: read the ledger entry for the OUT block to get the
block's base, then store into the row at OUT-0's offset. The register
it uses as the pointer is never the register holding the result, or
the store would overwrite the thing it is storing. The epilogue is
emitted before EVERY `ret`, because a body with two returns has two
places the answer leaves from.

## design

```
CanonicalForm.epilogue
	methods:
		emit
			"""
			answer_home -> the epilogue lines:
			ledger entry -> OUT block base ->
			store the result register into OUT-0
			"""
		pick_pointer
			"""
			result register -> a pointer
			register that is not it and not an
			arrival family still live
			"""
		place
			"""
			body_text -> the same lines inserted
			immediately before every `ret`
			"""
```

## settled rules

- **Every `ret` is immediately preceded by the epilogue** —
  structural check C3. Decision: log_146 §5.3.
- **The epilogue's pointer register is not the result register** —
  structural check C5. Decision: log_146 §5.3.
- **The answer leaves through OUT-0 of the ledger**, reached in two
  steps like every other row; the ledger symbol appears only as a
  relocation. Decision: [canonical_form](../CORE_0_3_1_2_canonical_form.md) design; log_146 §2.4.
- **A unit with no answer home is REFUSED, not patched.** A body whose
  own code names no register the answer is left in cannot have an
  epilogue written for it. Decision: log_146 §8.3; see
  [refuse](../node_0_3_1_2_7_refuse/CORE_0_3_1_2_7_refuse.md).
- **The body is never edited to make the epilogue fit** — a `jmp` is
  not turned into a `call`. Decision: log_146 §8.1, ruling 1.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| emit, place | `ledger48.py`, driven by `canon38_wrapped.py` | done for 30,436 units |
| emit, pick_pointer, place (the node's shape over `ledger.py`'s one text) | `canonical_form.Epilogue` | done for 30,432 units, 2026-09-03 (log_162) |
| C3 and C5 checked per unit | `canon37_gate.py`, `canon38_gate.py` | done |
| relocation read back | `canon38_assemble.py` — 8,946 ledger relocations over 2,728 texts | done |
| units with no answer home | 216 regenerated units refused | done, named (log_146 §8.3) |
