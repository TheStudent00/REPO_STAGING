---
id: pcv6.tools.t2_ledger.schema
level: 3
status: settled
settled_by: the owner
supersedes: null
---

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
