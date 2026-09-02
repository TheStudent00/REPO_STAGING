# R4 — Runtime Ledgering / Flow-Graph / Walker Survey

Date: 2026-07-28. Deep search across all of `<WORKSPACE_DIR>`
including archives, prompted by the owner's recall of advanced ledgering
with runtime modeling and flow-graph visualization. Agent survey,
read-based, line-cited. This report is the condensed record; ranked
relevance at the end.

## The find: three generations of runtime state-graph tooling

### Gen 3 (most advanced) — the WALKER suite
`<WORKSPACE_DIR>/StressBot/RelevantProjects/WFL_MixingCenter/render/`

- **`walker.py` (1,403 lines)** — builds a runtime STATE GRAPH from
  a live, driven app. Nodes = app states (content-addressed:
  `state_id = sha256(route + tree_summary)`, where tree_summary is
  a preorder list of `{kind, text, interactive}`; geometry
  deliberately excluded — that's the fidelity gauge's job). Edges =
  one real tap through the engine's own input pipeline. Bounded
  checkpointed BFS; fresh-reboot-per-edge recovery replaying the
  tap-path; pinned clock + text canonicalization for determinism
  (two 60-step runs byte-identical — measured in
  `PseudoCoup_v0/DevComms/walker_slice1.md`); errors and unsettled
  states recorded, never swallowed. Output: `py_walk.json`
  (states+edges), activations log, opt-in per-state screenshot
  bundle.
- **`walk_diff.py` (965)** — diffs the Python-side walk against the
  Kotlin/Robolectric-side walk (`kt_walk.json`). Only permitted
  normalization is a hand-authored, per-entry-justified kind
  vocabulary projection. Real report:
  `walks/walk_diff_report.txt` — "5 shared states / 23 kt-only /
  33 py-only / 203 edge mismatches" — the honest finding.
- **`identity.py` (197) + `oracle_registry.py` (337)** — the
  runtime→source bridge: every live node carries `.origin` = its
  Kotlin source coordinate resolved via the transpiler's
  `.linemap.json` sidecars (approximations marked `~`), checked
  against a static registry that is LIST-VALUED per coordinate —
  the empirical proof that source coordinate is NOT a unique node
  id (one line can host three composables).
- **`mount_diff.py` (1,630)** — cross-engine per-node comparison
  joined on source coordinate, using mounts-per-dump density;
  registry 2,273 entries in the recorded hostrun.
- **`nav_graph.py` (487)** — STATIC screen/edge graph from the nav
  source; `--walk` mode classifies every unreached screen as
  nav-reachable vs app-state-gated — the coverage oracle for a
  walk.
- **`emu_walker.py` (680)** — same state_id byte-for-byte over a
  real device (uiautomator/adb); UNEXECUTED per its own docstring.
- **THE design document:**
  `PseudoCoup_v0/DevComms/walk_node_identity_decision.md` (259) —
  the unmade decision on node identity. Direction (b): **every
  callable emits its own unique id at runtime — a per-call-site
  ledger id + per-instance key, emitted identically by BOTH
  transpiler sides, matched on id alone** ("never ambiguous: id is
  unique by construction"). Source-coordinate-as-id explicitly
  retracted on evidence.

### Gen 2 — dualgraph (static dual-tree aligner with a match ledger)
`WFL_Projects/WFL_PseudoCoup/.archive/tools/dualgraph/` (copy in
the Briefing archive)

- Static UI trees from both sides (tree-sitter Kotlin vs Python
  ast), LCS-aligned by kind+label signature; a RECORDED
  correspondence ledger (`ledger.json`: kind_aliases,
  handler_aliases per screen) consulted before any heuristic.
  Measured: `build/dualgraph/REPORT.md` (911 lines) — "matched 204
  · KOTLIN-only 336 · PC-only 297" across 30 screens.

### Gen 1 — dynamic_mapper / runtime_uimap / StressBot GraphLedger

- `PseudoCoup_v0/_deprecated/dynamic_mapper/`: ADB/Maestro DFS
  spider over BOTH apps simultaneously; `SemanticState` frozen
  dataclass hashed on app-model identity (program/path/vectors,
  not just screen content); `GraphLedger` nodes/edges;
  `utils/visualizer.py` → mermaid + graphviz. Working artifacts in
  `_deprecated/runtime_uimap/` (`wfl_map.mmd` 11 nodes/9 edges) —
  with the recorded failure: every node labeled "unknown" because
  screen identity was never populated.
- `StressBot/StressBot/core/{ledger,visualizer,explorer}.py` — the
  same design live: records transitions, exports mermaid/dot on
  every new edge, counterfactual explorer with snapshot/replay.

## What this adds to the ledger picture (the third axis)

The earlier ledger survey covered two families: semantic
(emission-driving) and structural (verification). This is a THIRD:
**runtime** — per-state/per-node facts observed from execution,
joined back to source identity. And the keying unification already
half-happened: `py_walk.json` action `walk_id`s ARE idgen
positional-path ids, stamped into emitted code by
`inject_emitid.py`.

## Design consequence for T2 (the combined ledger)

- The ledger id must be a RUNTIME-OBSERVABLE SIGNAL, not just a
  record key: emitted into transpiled output on every side (the
  walk_node_identity_decision direction (b)), so runtime
  observations join the ledger by id equality. Coordinate joins
  and anchor joins are both empirically disproven (list-valued
  registry; 5-shared-states diff).
- The unified record gains a `runtime` slot (states reached,
  mounts, walk edges, screenshots) beside `semantic`, `ui`,
  `connectivity`, `divergence`.
- Visualization is a solved pattern to harvest, not to invent:
  mermaid/dot exporters (StressBot/dynamic_mapper), screenshot
  bundles + manifests (walker), static/dynamic reachability
  classification (nav_graph).

## Ranked relevance (top of the agent's list)

1. `render/walker.py` — the runtime half of the target design
   already exists and ran deterministically.
2. `walk_node_identity_decision.md` — the identity design,
   written, unmade; direction (b) is the T2 keying answer.
3. `idgen.py` + `ledger_unified.py` — the identity primary key +
   integrity harness (already in the harvest map).
4. `identity.py` + `oracle_registry.py` — the observation→source
   bridge and the proof of where coordinate keying breaks.
5. `walk_diff.py` + report — the audited cross-engine vocabulary
   projection and the cost of leaving it incomplete.
6. `dualgraph/` — static counterpart with recorded correspondence
   ledger; largest measured dataset.
7. `nav_graph.py` — the coverage oracle (nav-reachable vs
   app-state-gated).
8. StressBot `GraphLedger`/`visualizer`/`explorer` +
   `SemanticState` — simplest complete ledger→graph→viewer loop;
   app-model identity hashing.

Negative results, checked: GameDynamicAnalysis (MCTS, not this),
ModellingResearch (Lean/mathlib), GuiGui (ChronologyTree — same
graph shape applied to editor history; adjacent inspiration only),
PseudoIR v3 visualization (node-only Cytoscape dump).
