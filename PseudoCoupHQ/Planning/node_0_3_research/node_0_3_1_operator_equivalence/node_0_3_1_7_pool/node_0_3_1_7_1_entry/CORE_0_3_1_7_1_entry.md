---
id: hq.research.compiler_graph.pool.entry
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: entry
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/node_0_3_1_7_1_entry/CORE_0_3_1_7_1_entry.md
super_node:
    name: pool
    path: ../CORE_0_3_1_7_pool.md
sub_nodes:
    - name: entry_id
      designation: code (attribute)
      realize: false
    - name: members
      designation: code (attribute)
      realize: false
    - name: representative
      designation: code (attribute)
      realize: false
    - name: representative_size
      designation: code (attribute)
      realize: false
    - name: languages
      designation: code (attribute)
      realize: false
    - name: layer5_normalized_texts
      designation: code (attribute)
      realize: false
    - name: distinct_wrapped_text_count
      designation: code (attribute)
      realize: false
    - name: type_key
      designation: code (attribute)
      realize: false
    - name: grounds
      designation: code (attribute)
      realize: false
---

# CORE 0_3_1_7_1 — entry

## metadata

- **id:** hq.research.compiler_graph.pool.entry
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [pool](../CORE_0_3_1_7_pool.md)

## sub_nodes

- entry_id — code (attribute) *(realize: false)*
- members — code (attribute) *(realize: false)*
- representative — code (attribute) *(realize: false)*
- representative_size — code (attribute) *(realize: false)*
- languages — code (attribute) *(realize: false)*
- layer5_normalized_texts — code (attribute) *(realize: false)*
- distinct_wrapped_text_count — code (attribute) *(realize: false)*
- type_key — code (attribute) *(realize: false)*
- grounds — code (attribute) *(realize: false)*

## definition

One distinct computation in the pool, and the units of every language
that were proved to compute it. An entry is not a language's row and
not an operator's row: its members carry their language, their
population and their arrival annotation as COLUMNS, so a per-language
view is a filter over the entry rather than a table of its own. Each
entry names the member chosen as its representative, the layer-5 texts
its members printed, and which merge ground joined which pair. The
worked instance is `E00029`, integer addition: 158 members across c,
cpp, go, rust, php, ruby and cpython, one layer-5 text `v0 + v1`,
representative `go/op_319` at 35 assembled bytes.

## design

```
class Entry
	attributes:
		entry_id
			"""
			E00029 and the like; stable within
			one numbered pool
			"""
		members
			"""
			each: unit, lang, population,
			arrival_annotation,
			layer5_normalized_text,
			layer5_merge_eligible (+ reason),
			operator (display only)
			"""
		representative
			"""
			the member with the fewest assembled
			bytes
			"""
		representative_size
			"""
			assembled bytes; where a text would
			not assemble, character length with
			the substitution stated on the entry
			"""
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

- **An entry is one distinct computation**, and language is a member
  column, not a table. Decision: AgentMemory (round 9, log_134), the owner
  verbatim in [pool](../CORE_0_3_1_7_pool.md) settled rules.
- **`operator` on a member is display only**, read by nothing.
  Decision: THE SPELLING BAN; [pool](../CORE_0_3_1_7_pool.md).
- **The type key is machine form** — arrival register families and
  answer width — never a declared type name. Decision: [pool](../CORE_0_3_1_7_pool.md)
  design.
- **A member with no proved term is carried and flagged**, not
  dropped; it simply cannot merge on layer 5. Decision: log_148 §1.3,
  log_154 §3.
- **A substitution is stated on the entry, never hidden.** Two of the
  2,247 entries fall back to character length for their
  representative and say so in `representative_size_measured_as`.
  Decision: log_154 §2.4.

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| Entry | `build_the_pool3.py` (importing `build_the_pool2.py` unedited) | done |
| the entries | `the_pool3.json` — 2,247 entries over 30,436 members, 632 multi-language, 3 compiled+interpreted | done (log_154) |
| the worked entry | `the_pool2_entry_E00029.json`; printed verbatim in log_154 §4.2 | done |
| earlier pools | `the_pool1.json`, `the_pool2.json` | superseded records |
| round-13 entries | `the_pool5.json` — 1,831 entries over 30,432 members, 490 multi-language, 3 compiled+interpreted | done (task 65, log_169) |
| the worked entry, round 13 | `the_pool5_entry_E00029_successor_printed.txt` — `E00029`, 166 members across 8 languages, representative `go/op_319` | done (task 65, log_169) |
