---
id: pcv6.tools.t1_tree_sitter_base.progress
status: living
---

# PROGRESS — T1 tree_sitter_base

- build — **done** 2026-07-28:
  `<WORKSPACE_DIR>/PseudoCoup_v6/Tools/tree_sitter_base/` (parser
  factory, census recorder, pins, fixtures, frozen censuses).
- acceptance — **done**: 12/12 in-session (frozen-census
  byte-equality, determinism, clean-parse, partition laws).
- deviation on record: pip-pinned packages instead of
  vendored-grammar repos (see the tool's `pins/MANIFEST.md`);
  full vendoring addable per grammar if needed.
- open: add grammars beyond python/rust/cpp as ingestors demand.
