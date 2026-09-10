---
id: hq.research.compiler_graph.pool.merge_grounds
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: rule
node:
    name: merge_grounds
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/node_0_3_1_7_2_merge_grounds/CORE_0_3_1_7_2_merge_grounds.md
super_node:
    name: pool
    path: ../CORE_0_3_1_7_pool.md
sub_nodes: []
---

# CORE 0_3_1_7_2 — merge_grounds

## metadata

- **id:** hq.research.compiler_graph.pool.merge_grounds
- **level:** 4
- **status:** draft
- **designation:** rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [pool](../CORE_0_3_1_7_pool.md)

## sub_nodes

*(none yet)*

## definition

The three and only three grounds on which two units may be put into
one pool entry, plus the closure rule that applies them. Layer-5
identity: both units printed the same normalized term, and BOTH terms
were proved. A proved edge: an earlier prover established the pair
equal. Layer-3 identity: the two wrapped texts are the same string,
which means the same machine code twice, so equivalence is by
construction. The join is closed under transitivity. A fourth count —
what the pool would be on the first two grounds alone — is RECORDED on
the artifact and used for nothing.

## design

The rule, as numbered statements:

1. **Ground one, layer-3 identity.** Two units whose wrapped texts are
   the same string are the same machine code twice. Equivalence by
   construction; no solver is asked.
2. **Ground two, layer-5 identity.** Two units whose normalized terms
   are the same string merge, and ONLY when both terms were proved
   equal to their own unit's machine code. An unproved term is not a
   weaker key; it is no key.
3. **Ground three, a proved edge.** A pair an earlier prover
   established equal, read from the banked edge files.
4. **The join is closed under transitivity**, so the entry count is
   what survives all three together, never their sum.
5. **The two-ground count is recorded, not used.** It goes on the
   artifact as `entries_under_the_brief_strict_rule`.

The counts each ground contributed over the 30,436 members, from
`the_pool3_run.log`:

| quantity | value |
|---|---|
| distinct layer-3 wrapped texts | 2,997 |
| distinct layer-5 texts among eligible units | 1,104 |
| layer-3 identity merges | 27,439 |
| layer-5 identity merges | 22,028 |
| proved edges applied | 118 |
| entries | 2,247 |

## settled rules

- **Three merge grounds, and the two-ground count is recorded, never
  used.** Decision: AgentMemory "ROUND 10 RULINGS" (1); the owner,
  2026-09-03, "agreed". Carried in [pool](../CORE_0_3_1_7_pool.md) settled rules.
- **Only a PROVED term counts on layer 5.** Decision: log_147 §1.2;
  log_148 §1.4; log_154 §1.4.
- **Layer-3 identity is equivalence by construction**, because
  identical text is identical bytes. Decision: log_154 §2.1.
- **The population is the units the gate proved, minus none.**
  Decision: log_148 §1.3; log_154 §3.
- **Spelling never keys a merge.** Decision: THE SPELLING BAN;
  [guard](../../node_0_3_1_8_guard/CORE_0_3_1_8_guard.md).

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| the three grounds applied | `build_the_pool3.py` | done |
| the per-ground counts | `the_pool3_run.log` | done |
| the two-ground count recorded | `the_pool3.json` `summary.entries_under_the_brief_strict_rule` = 8,394, with `meta.brief_strict_count_note` | done (log_154 §1.4) |
| proved edges read | `proved_edges.json`, `proved_edges2.json`, `proved_edges3.json`, `interp_join3.json`, `interp_fastpath.json` — 118 applied | done |
| round-13 per-ground counts | `pool65_run.log` — layer-3 merges 27,439, layer-5 merges 25,327, proved edges 118, entries 1,831 | done (task 65, log_169) |
| round-13 two-ground count recorded | `the_pool5.json` `summary.entries_under_the_brief_strict_rule` = 5,095, used for nothing | done (task 65, log_169) |
