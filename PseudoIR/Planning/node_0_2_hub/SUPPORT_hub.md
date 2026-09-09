---
id: pir.hub.support.hub
status: projected
---

# SUPPORT — hub

projected 2026-07-30 from the previous plan, now archived at
`PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_2_hub/CORE_0_2_hub.md  (258 words)
verdict: clean
changed: nothing

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
  `PseudoIR/Tools/intentions/pc_intentions.json`
  (the `canon` field per primitive/operator). Sub-node
  `node_0_2_0` (previous plan).
- **Borders** — typed cells and crossing rules: how values enter
  and leave sliced-semantics regions, what a cell refuses, the
  border-lattice verdicts (already data: `border_lattice`, 11
  entries). Sub-node
  `node_0_2_1` (previous plan).
- **Surface spelling** — how hub source spells qualified
  semantics (`a r./ b`): the parser-level fork. (The interim
  import-hook rewrite named here was dropped 2026-07-31 by the owner;
  see SUPPORT_surface.md.) Sub-node
  `node_0_2_2` (previous plan).

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

## where those sub-nodes went

the three surfaces are now nodes under `assembly`, not bullets.

- intention objects — `PseudoIR/Planning/node_0_2_hub/node_0_2_1_assembly/node_0_2_1_0_intention_objects/`
- borders — `PseudoIR/Planning/node_0_2_hub/node_0_2_1_assembly/node_0_2_1_1_borders/`
- surface — `PseudoIR/Planning/node_0_2_hub/node_0_2_1_assembly/node_0_2_1_2_surface/`
