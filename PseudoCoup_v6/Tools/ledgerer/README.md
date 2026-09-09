# ledger (T2, phase 1)

The per-program record, one entry per NAMED source node, everything
keyed by positional-path ids. Plan node:
`PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/`
(id `pcv6.tools.t2_ledger`).

- `generate_ids.py` — the id generator, transplanted from
  `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/idgen.py`:
  segment `"<childIndex>:<nodeKind>"` recorded unconditionally at
  every node; files are positioned nodes; anchors are metadata,
  never keys.
- `build_ledger.py` — phase-1 record
  (id/file/node_kind/span/anchor + `semantic.type`), deterministic
  serialization, and the consumer gate `require_type` (halts on
  `unresolvable` — refusal at consumption, settled).
- `check_ledger.py` — integrity: ids unique, entry count equals an
  independent recount of the pinned corpus, nothing
  missing/extra, every declaration typed or explicitly
  `unresolvable` (count reported first-class).
- `test_ledger.py` — acceptance (this tool's oracle): 7/7 at
  graduation (2026-07-28, sandbox), pinned corpus = four of the
  five R2-censused compiler files.

Run acceptance:

```bash
python3 -m pytest PseudoCoup_v6/Tools/ledgerer/ -q
```

## Phase-1 adaptations on record (each intentional, each revisitable)

1. **Named nodes only get records**; anonymous nodes (punctuation,
   keywords) still consume index positions, so ids stay faithful
   positional paths. The v0 source scoped records even tighter
   (containment kinds only) while counting everything — same
   principle, wider net here.
2. **The generated `assembler.rs` (1.27M nodes) is excluded from
   the ACCEPTANCE corpus** for size; the id scheme handles it, but
   materializing ~600k records wants a storage decision (sharding
   / named-subset / lazy build) — open point on the plan node's
   PROGRESS.
3. **`DECLARATION_KINDS` is a deliberately small phase-1 list**
   per grammar; it grows with the ingestors, and growth follows
   the growth gate (writer + check + consumer rule together).
