---
id: pcv6.hub
level: 1
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_2 — The Hub

The artifact everything else exists to assemble: the disciplined-
Python center that all 12 languages convert into without violating
the intentions of their source scripts, and that computes every
target's exact semantics via inserted compiler slices. The tools
(node_0_0) build it; the applications (node_0_3) exercise it; this
node plans the Hub itself as a deliverable.

## What the Hub consists of (the three surfaces)

- **Intention objects** — the 11-object minimum intention set
  realized as PC objects (PC.bool, PC.int64, PC.list, PC.map, …),
  each carrying the canon semantics now recorded AS DATA in
  `~/Programming/PseudoCoup_v6/Tools/intentions/pc_intentions.json`
  (the `canon` field per primitive/operator). Sub-node
  [node_0_2_0](node_0_2_0_intention_objects/CORE_0_2_0_intention_objects.md).
- **Borders** — typed cells and crossing rules: how values enter
  and leave sliced-semantics regions, what a cell refuses, the
  border-lattice verdicts (already data: `border_lattice`, 11
  entries). Sub-node
  [node_0_2_1](node_0_2_1_borders/CORE_0_2_1_borders.md).
- **Surface spelling** — how hub source spells qualified
  semantics (`a r./ b`): the import-hook rewrite today, the
  parser-level fork as the recorded end state. Sub-node
  [node_0_2_2](node_0_2_2_surface/CORE_0_2_2_surface.md).

## Standing constraints (all settled elsewhere, restated)

- The hub DOMINATES intentions; target-language shortfalls are
  recorded, never designed around.
- Lowering semantics enter by transpile+slice+insert, never by
  reimplementation — a PC object's arithmetic is backed by an
  inserted slice wherever exactness matters.
- The ledger is the hub's type context (the TyCtxt stand-in
  pattern, now id-keyed).

## Sequencing

The Hub assembles from proven parts; it does not start until T6
insertion closes the all-PCv6 end-to-end loop. First increment
after that: PC.int64 backed by the inserted integer-arithmetic
chain — the PCv5 demo reborn as a product surface.
