---
id: hq.research.compiler_graph.pool.representative
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), rule
node:
    name: representative
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/node_0_3_1_7_4_representative/CORE_0_3_1_7_4_representative.md
super_node:
    name: pool
    path: ../CORE_0_3_1_7_pool.md
sub_nodes: []
---

# CORE 0_3_1_7_4 — representative

## metadata

- **id:** hq.research.compiler_graph.pool.representative
- **level:** 4
- **status:** draft
- **designation:** code (method), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [pool](../CORE_0_3_1_7_pool.md)

## sub_nodes

*(none yet)*

## definition

The rule that picks one member to stand for an entry: the simplest
member, meaning the one whose canonical text assembles to the fewest
bytes of machine code, with ties broken by first-in-list order. The
bytes are MEASURED, not estimated — each distinct text is assembled
with `as --64` and its bytes counted from `objdump -d`. Only entries
carrying more than one distinct text need the measurement: 394 of the
2,247, between them 1,144 texts. Where a text will not assemble, its
character length stands in and the substitution is written on the entry
rather than hidden.

## design

```
Pool.representative
	methods:
		distinct_texts
			"""
			entry -> its distinct wrapped texts;
			an entry with one text needs no
			measurement
			"""
		measure
			"""
			text -> assembled byte count, via
			`as --64` then `objdump -d`
			"""
		choose
			"""
			entry -> the member with the fewest
			bytes; ties by first-in-list order
			"""
```

The measurement as it ran, from `the_pool3_run.log`:

| quantity | value |
|---|---|
| entries carrying more than one wrapped text | 394 |
| distinct texts to assemble | 1,144 |
| texts newly assembled | 1,144 |
| texts that would not assemble | 8 |
| entries falling back to character length | 2 |

The 8 that would not assemble all carry an inline constant-pool
relocation note the stored text keeps, e.g.
`addsd 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4`, which is
not assembler syntax.

## settled rules

- **Fewest bytes of assembled machine code, ties by first-in-list.**
  Decision: AgentMemory "REPRESENTATIVE RULE" (the owner, 2026-08-29: "the
  most simple arch-unit … fewest bytes"); carried in [pool](../CORE_0_3_1_7_pool.md).
- **The bytes are measured, not estimated.** Decision: log_148 §2.3;
  log_154 §2.4.
- **A substitution is stated on the entry**, in
  `representative_size_measured_as`. Decision: log_154 §2.4.
- **The representative is a display choice, not an identity.** The
  entry is the computation; the representative only stands for it.
  Decision: [pool](../CORE_0_3_1_7_pool.md) design.

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| choose, measure | `build_the_pool3.py` (rule from `build_the_pool2.py`, unedited) | done |
| measured bytes, pool2 | `the_pool2_bytes.json` | done (log_148 §2.3) |
| measured bytes, pool3 | `the_pool3_bytes.json` — the 1,144 texts | done (log_154 §2.4) |
| instance | `go/op_319` at 35 bytes, representative of `E00029` | done |
| earlier representative builders | `build_representatives.py` … `build_representatives5.py` | superseded records |
| measured bytes, pool5 | `the_pool5_bytes.json` — 527 entries with more than one text, 1,689 texts, 288 newly assembled, 120 would not assemble | done (task 65, log_169) |
