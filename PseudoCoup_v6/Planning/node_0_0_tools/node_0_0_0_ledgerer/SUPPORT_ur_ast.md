---
id: pcv6.ledgerer.support.ur_ast
status: projected
---

# SUPPORT — ur_ast

projected 2026-07-30 from the previous plan, now archived at
`<WORKSPACE_DIR>/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_1_ledger/CORE_0_0_1_ledger.md  (183 words)
source: node_0_0_tools/node_0_0_1_ledger/node_0_0_1_0_schema/CORE_0_0_1_0_schema.md  (238 words)
source: node_0_0_tools/node_0_0_1_ledger/node_0_0_1_1_keying/CORE_0_0_1_1_keying.md  (280 words)
verdict: clean
changed: nothing

---

## from node_0_0_1_ledger

# CORE 0_0_1 — T2: Ledger

An independent tool (PseudoCoup is a module of tools; centralized
control comes later when ontology reveals itself). The per-program
record across **three axes** — semantic (drives emission),
structural (verifies shape/wiring), runtime (observations from
executing the output) — one record per source node, everything
joined by one id.

Settled design (the owner-aligned 2026-07-28): ONE record schema, not
joined ledgers; the ledger id is a **runtime-observable signal**
emitted into every transpiled side; ingest records `unresolvable`
honestly, consumers halt on it; minimal core ships first, slots
grow additively. Composition sources and evidence:
[ledger survey](../../../../PseudoCoup_v5/DevComms/ledger_survey_2026-07-27.md),
[R4 runtime survey](../../../Research/r4_runtime_ledger_survey/REPORT.md).

Acceptance (tool-level): `--check` invariants on a pinned corpus;
dump/load byte-fidelity; consumer-halt refusal test; id-emission
test (emitted output carries the ledger id, recoverable by a
runtime probe).

## Nodes

- `node_0_0_1_0_schema` (previous plan)
  — the record: fields, slots, serialization, unresolvable
  markers.
- `node_0_0_1_1_keying` (previous plan)
  — identity: call-site id + instance key, the emission contract,
  secondary indexes.
- `node_0_0_1_2_integrity` (previous plan)
  — the check harness: invariants, refusal semantics, growth
  gates.
- `node_0_0_1_3_growth` (previous plan)
  — the deepening: later slots (semantic/connectivity/ui/
  divergence/runtime) under the growth gate, and the
  assembler-scale storage decision. *(planning added 2026-07-29)*

## from node_0_0_1_0_schema

# CORE 0_0_1_0 — Ledger Record Schema

One record per source node. Draft shape (JSON; sidecar file per
program, `<program>.ledger.json`):

```json
{
  "id": "0:source_file/44:function_declaration/2:call_expression",
  "file": "TodayScreen.kt",
  "node_kind": "call_expression",
  "span": {"start_line": 104, "start_col": 4, "end_line": 108,
           "end_col": 5, "start_byte": 2210, "end_byte": 2391},
  "anchor": "TodayScreen",
  "semantic": {
    "fqdn": "TodayScreen.build",
    "type": "…| \"unresolvable\"",
    "param_shape": [], "method_return": null, "suspend": false,
    "symbol_owners": [], "singleton": false, "enum": false
  },
  "ui": null,
  "connectivity": null,
  "divergence": [
    {"kind": "…", "confidence": "runtime-confirmed",
     "evidence": "…", "registry_op": "…"}
  ],
  "runtime": null
}
```

- **Slots ship in phases** (minimal core first — the owner): phase 1 is
  `id`/`file`/`node_kind`/`span`/`anchor` + `semantic.type`; every
  other slot starts null and is added when its writer exists. The
  builder REFUSES a record claiming a slot its phase doesn't
  define (the R1 refusal pattern).
- **`unresolvable` is a value, never an omission**: a declaration
  the ingestor cannot type gets the explicit marker; integrity
  counts them; consumers halt on them (see integrity node).
- **Serialization**: sets→sorted arrays, tuples→arrays (round-trip
  byte-fidelity); derived overlays (anything recomputed per run,
  e.g. async-required-style egress overlays) are deliberately NOT
  serialized — the 289-line ledger's reasoned rule, kept.
- **Divergence entries** use the merged taxonomy (v0
  classify_methods kinds + exp sidecar reasons) and carry
  registry-style `confidence`/`evidence`, plus `registry_op`
  linking class-level lowering knowledge when it exists.
- Harvest sources: record shape from v0 `ledger_unified.py`;
  semantic fields from `PseudoCoup/pseudocoup/core/ledger.py`
  (re-keyed); `ui`/`connectivity` slot vocabularies from v0
  `ui_ledger.py`/`ledger.py`; `runtime` slot shape from the walker
  suite's per-state records (R4).

## from node_0_0_1_1_keying

# CORE 0_0_1_1 — Ledger Keying: the id as a runtime-observable signal

Spec taken from direction (b) of
`PseudoCoup_v0/DevComms/walk_node_identity_decision.md` (the
written, previously-unmade decision — see
`R4` (previous plan)).

- **Primary key: the call-site id** — idgen positional path over
  T1's tree-sitter tree: `"<childIndex>:<nodeKind>"` segments
  (idgen's own format string, quoted as theirs) joined by `/` from
  the source root — the sub-node index recorded unconditionally at
  EVERY node. Anchors (names, labels, text) are metadata only,
  never keys. Files and directories are themselves positioned
  nodes. Uniqueness is asserted at build (`--check`), not assumed.
- **Instance key at fire time**: a per-instance ordinal appended
  when the same call site executes multiply (`<id>#<rank>` — the
  walk_id form already present in the recorded walk JSONs).
- **The emission contract** (what makes it a signal, not just a
  key): every transpiled side EMITS the id identically into its
  output at the call site (the `inject_emitid.py` precedent), so
  any runtime observation joins the ledger by id equality —
  "never ambiguous: id is unique by construction."
- **Rejected keyings, on recorded evidence**: source coordinates
  (list-valued oracle registry — one Kotlin line hosts three
  composables) and content anchors (identical co-node collisions;
  the 5-shared-states walk diff). Both failures are documented in
  the R4 sources.
- **Secondary index: FQDN** (`scope.identifier`, three tiers per
  the 02_ledger spec — global / class / parameter) for call sites
  that only know a name; always resolves THROUGH the id, never
  around it.
- Address-vs-identity note (mirrors the planning framework):
  positional ids are addresses of the parse tree as vendored —
  re-ingesting changed source changes ids. Cross-version node
  tracking is an analysis problem (diff-based), not a keying
  problem; the ledger never pretends ids are stable across source
  edits.

## where those nodes went

the list above names nodes of the previous plan. they are no longer
nodes; this is where their content sits now.

- schema, keying — carried in this file, above.
- integrity — `<WORKSPACE_DIR>/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_validation.md`
- growth — `<WORKSPACE_DIR>/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_todos.md`
- R4 — `<WORKSPACE_DIR>/PseudoCoup_v6/Research/r4_runtime_ledger_survey/REPORT.md`
