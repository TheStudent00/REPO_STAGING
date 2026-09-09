---
id: hq.research.compiler_graph.pool
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: pool
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/CORE_0_3_1_7_pool.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: entries
      designation: code (attribute)
      realize: false
    - name: entry
      path: node_0_3_1_7_1_entry/CORE_0_3_1_7_1_entry.md
    - name: merge_grounds
      path: node_0_3_1_7_2_merge_grounds/CORE_0_3_1_7_2_merge_grounds.md
    - name: merge
      designation: code (method)
      realize: false
    - name: representative
      path: node_0_3_1_7_4_representative/CORE_0_3_1_7_4_representative.md
    - name: families
      path: node_0_3_1_7_5_families/CORE_0_3_1_7_5_families.md
    - name: exception_families
      path: node_0_3_1_7_6_exception_families/CORE_0_3_1_7_6_exception_families.md
    - name: compare
      designation: code (method)
      realize: false
---

# CORE 0_3_1_7 — pool

## metadata

- **id:** hq.research.compiler_graph.pool
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- entries — code (attribute) *(realize: false)*
- [entry](node_0_3_1_7_1_entry/CORE_0_3_1_7_1_entry.md) — One distinct computation in the pool, and the units of every language that were proved to compute it.
- [merge_grounds](node_0_3_1_7_2_merge_grounds/CORE_0_3_1_7_2_merge_grounds.md) — The three and only three grounds on which two units may be put into one pool entry, plus the closure rule that applies them.
- merge — code (method) *(realize: false)*
- [representative](node_0_3_1_7_4_representative/CORE_0_3_1_7_4_representative.md) — The rule that picks one member to stand for an entry: the simplest member, meaning the one whose canonical text assembles to the fewest bytes of machine code, with ties broken by first-in-list order.
- [families](node_0_3_1_7_5_families/CORE_0_3_1_7_5_families.md) — The dominant-operator rule applied over the pool's entries, producing groups of language-operators that behave as one operation across languages.
- [exception_families](node_0_3_1_7_6_exception_families/CORE_0_3_1_7_6_exception_families.md) — The same family idea applied to GUARDS rather than to computations.
- compare — code (method) *(realize: false)*

## definition

ONE pool of every canonicalized arch-unit of every language, in
which units proved equivalent collapse into one entry. An entry is one
distinct computation; its members carry language, arrival population
and arrival annotation as columns. There is no compiled table and no
interpreter table; anyone needing one filters the pool. The families
are the dom_op rule applied over the pool's entries; the exception
families are the same idea over guards. This is the research's
deliverable: the dominant-operator table feeding `ur_kind` and the
Hub.

## design

```
class Pool
	attributes:
		entries
	methods:
		merge
			"""
			units -> entries, closed under
			transitivity, on merge_grounds only
			"""
		compare
			"""
			(pool_a, pool_b) -> every split and
			every merge with its COMPUTED cause,
			joined on member sets
			"""
		representative
			"""
			sub-node: per entry, the member with
			the fewest assembled bytes
			"""
		families
			"""
			sub-node: dom_op rule over entries
			"""
		exception_families
			"""
			sub-node: guard condition+response
			identity over entries
			"""


class Entry
	attributes:
		entry_id
		members
			"""
			each: unit, lang, population,
			arrival_annotation,
			layer5_normalized_text,
			layer5_merge_eligible (+ reason),
			operator (display only)
			"""
		representative
		representative_size
		languages
		layer5_normalized_texts
		distinct_wrapped_text_count
		type_key
			"""
			arrival register families | answer
			width — the machine-form stand-in
			for the operand-type key
			"""
		grounds
			"""
			which merge ground joined which pair
			"""
```

## settled rules

- **The merged pool** (the owner, verbatim): "there is a pool of all the
  arch-units we canonicalized and merged them when they are
  equivalent. not an accounting of every languages contribution to
  the number of units." Decision: AgentMemory (round 9, log_134).
- **Three merge grounds**: layer-5 text identity (proved terms only),
  a proved edge, layer-3 wrapped-text identity (identical text is
  identical bytes — equivalence by construction). The two-ground count
  is recorded on the artifact, never used. Decision: "ROUND 10
  RULINGS" (1), the owner 2026-09-03 "agreed".
- **The representative rule**: fewest bytes of assembled machine
  code, ties by first-in-list. Decision: AgentMemory "REPRESENTATIVE
  RULE" (the owner: "the most simple arch-unit … fewest bytes").
- **Accumulate, don't replace**: pools are numbered; a superseded
  pool stays on disk and the next is compared against it with
  computed causes. Decision: AgentMemory (the owner: "we are accumulating
  information").
- **Spelling never keys anything here**; `operator` on a member and
  `label` on a family node are display fields read by nothing.
  Decision: THE SPELLING BAN.
- **The population is the units the gate proved**, minus none; units
  with no proved term are members that cannot merge on layer 5.
  Decision: log_148 §1.3, log_154 §3.

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| merge, Entry, representative | `build_the_pool3.py` (imports `build_the_pool2.py` unedited); `the_pool3.json` (2,247 entries / 30,436 members / 632 multi-language / 3 compiled+interpreted; brief-strict 8,394) | done (log_154) |
| compare | `compare_pool1_pool2.py`, `pool2_pool3_delta*.json` (60 splits, 719 merges, every cause computed) | done |
| families | `build_the_families3.py` (imports `build_the_families2.py`, which imports `dom_ops.py`, both unchanged); `the_families3.json`: 36 families / 197 nodes | done |
| exception_families | `exception_families2.json` (round 5) — not rebuilt since; EF0039 `growing` family | stale against pool3 |
| superseded | `the_pool1.json`, `the_pool2.json`, `dominant_table9…25`, `dom_ops5…23`, `union_table*`, `interp_table*` | superseded records |
| round-13 pool | `pool65_run.py`, `the_pool5.json` (1,831 entries / 30,432 members / 490 multi-language / 3 compiled+interpreted; brief-strict 5,095) | done (task 65, log_169) |
| round-13 compare | `pool4_pool5_delta.json` (35 splits, 89 merges, every cause computed), `pool_delta65.py`, `pool_delta65.json`, `pool_delta65_printed.txt` | done (task 65, log_169) |
| round-13 families | `the_families5.json` — 34 families / 197 nodes | done (task 65, log_169) |
| round-13 exception families | `exception_families5.json` — 40 families over pool5 | done (task 65, log_169) |

Integer addition is `E00029`: 158 members across c/cpp/go/rust/php/
ruby/cpython, one layer-5 text `v0 + v1`, representative `go/op_319`
at 35 bytes.
