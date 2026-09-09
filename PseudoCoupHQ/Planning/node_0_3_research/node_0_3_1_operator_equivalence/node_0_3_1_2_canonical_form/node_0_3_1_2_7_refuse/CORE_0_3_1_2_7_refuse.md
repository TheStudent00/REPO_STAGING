---
id: hq.research.compiler_graph.canonical_form.refuse
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), finding
node:
    name: refuse
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/node_0_3_1_2_7_refuse/CORE_0_3_1_2_7_refuse.md
super_node:
    name: canonical_form
    path: ../CORE_0_3_1_2_canonical_form.md
sub_nodes: []
---

# CORE 0_3_1_2_7 — refuse

## metadata

- **id:** hq.research.compiler_graph.canonical_form.refuse
- **level:** 4
- **status:** draft
- **designation:** code (method), finding
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [canonical_form](../CORE_0_3_1_2_canonical_form.md)

## sub_nodes

*(none yet)*

## definition

The named reasons a unit cannot be put into the canonical form at all,
each recorded as a cause with a real unit shown under it rather than a
count. There are three causes and 642 refused units across the three
populations. NEVER RETURNS: the whole body is a transfer into another
routine, so there is no moment in this unit at which the answer exists
to be stored. NO ANSWER HOME: the body names no register the answer is
left in. NO CANONICAL TEXT: the handler has no ship body to wrap. A
refusal is a verdict on the record, not a unit quietly dropped.

## design

```
CanonicalForm.refuse
	attributes:
		causes
			"""
			never_returns / no_answer_home /
			no_canonical_text — each with its
			count per population and one unit
			quoted in full
			"""
	methods:
		classify
			"""
			ArchUnit -> a cause, or nothing when
			the unit can be wrapped
			"""
		record
			"""
			cause + unit -> a refusal row that
			travels with the population, so a
			refused unit is visible rather than
			absent
			"""
```

The three causes and their instances:

1. **never returns** — 16 in the original population, 408 in the
   regenerated one. Instance, the whole body of `swift/op_690`:
   one unconditional jump into another routine. Turning that `jmp`
   into a `call` would change the body, which ruling 1 forbids.
2. **no answer home** — 216 regenerated units. Two shapes, both
   measured: 81 whose answer is on the x87 stack (instance, the whole
   body of `c/regen_137`: `fldt 0x8(%rsp); fchs; ret`), and 135 whose
   entire body is `ret`.
3. **no canonical text** — 2 interpreter units, `ruby/rb_big_plus`
   and `ruby/vm_opt_plus`, which have no ship body at all.

## settled rules

- **The body is never edited to avoid a refusal.** Decision: log_146
  §8.1, ruling 1 ("the compiler's body is verbatim"); [canonical_form](../CORE_0_3_1_2_canonical_form.md).
- **Every refusal is named by cause, with an instance**, never
  reported as a count alone. Decision: log_146 §8.
- **The refusals must be the same refusals across a rebuild.** A
  refusal that changes cause between rounds is a regression to be
  explained. Decision: log_152 §1.3.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| classify, record | `ledger48.py` + the canon38 drivers | done |
| causes, classify, record | `canonical_form.Refuse` | done, 2026-09-03 (log_162) |
| a FOURTH cause, `no runtime callee body` | 4 swift regenerated units (log_161 §4.1.1) | done, named; 646 refusals in all |
| refusals, original population | 16 never returns (log_146 §8.1) | done, named |
| refusals, regenerated population | 408 never returns + 216 no answer home (log_146 §8.3) | done, named |
| refusals, interpreter population | 2 no canonical text, in `interp_canon35.json` (log_146 §8.2) | done, named |
| same-refusals check across the rebuild | `canon38_zero_regression.py` (log_152 §1.3) | done |
