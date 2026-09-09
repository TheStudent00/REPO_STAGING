---
id: hq.research.compiler_graph.guard
level: 3
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (function), rule
node:
    name: guard
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_8_guard/CORE_0_3_1_8_guard.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: check_no_spelling_keys
      designation: code (function)
      realize: false
    - name: machine_form_fields
      designation: code (attribute)
      realize: false
---

# CORE 0_3_1_8 — guard

## metadata

- **id:** hq.research.compiler_graph.guard
- **level:** 3
- **status:** draft
- **designation:** code (function), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- check_no_spelling_keys — code (function) *(realize: false)*
- machine_form_fields — code (attribute) *(realize: false)*

## definition

The mechanical enforcement of the spelling ban: a function that walks
any artifact the pipeline reads or writes and fails on an operator
token in any key, grouping, pairing, row structure or comparison
scope. Every stage that groups or pairs units runs it on its own
output and refuses that output on failure. It is unmodified,
un-exempted, and run as one process over every file; a stage that
quiets it about its own field has failed.

## design

```
function check_no_spelling_keys(paths) -> exit code
	"""
	reads the operator inventory from the
	probe manifests; walks each JSON in full;
	reports every (path, field, token)
	"""

machine_form_fields
	"""
	the fields the guard reads as machine
	form, not spelling: bytes, key, sem_key,
	mnem. Fixed in the guard's own source;
	never extended at run time by a caller
	"""
```

## settled rules

- **THE SPELLING BAN, ABSOLUTE.** No operator token in any key,
  grouping, pairing, row structure, candidate selection or comparison
  scope. The token appears exactly once per unit, as a display label.
  Decision: AgentMemory (the owner, 2026-08-25, after the second violation).
- **No exemption of any kind.** No file that feeds grouping declares
  `role: generator provenance`; no caller adds a field to the guard's
  prose set at run time. An artifact that collides (a mnemonic
  spelled like a token) changes its SHAPE — `{"kind": "arch_opcode",
  "mnem": "xor"}` — so the machine form is machine form on the page.
  Decision: "ROUND 10 RULINGS" (5); log_147 §13.7 (the lesson);
  log_150 §3 (the finding on task 47's files).
- **One process, every file, transcript pasted, `grep -c exempt` =
  0.** Decision: log_151 standing requirements.

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| check_no_spelling_keys | `check_no_spelling_keys.py` | done, unmodified since round 3 |
| conformance of artifacts | canon38 (336 files), layer4b/c, pool3, census4: PASS, 0 exempt | done (log_152 §6, log_154 §8) |
| non-conforming, superseded | canon37 files: 273 of 332 FAIL with the role line removed (579 places in c); `guard48.py` and `canon37_guard.py` added fields at run time | superseded; kept as record |
