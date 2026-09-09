---
id: hq.research.type_vocabulary.progress
status: living
---

# PROGRESS — type_vocabulary

- 2026-08-14: node founded at the owner's instruction, from his question
  "what will it take to get a complete set of these data structures
  and verify them all?" Method ruled in the CORE: derive the set
  from each compiler's own type enumeration and take the union —
  never hand-list. Scope: all 12 targets where the toolchain allows
  (swift now runs in the sandbox); single-language types stay in
  (the owner: "its those gaps the Hub is trying to fill").
- 2026-08-16: step A done. All 12 languages extracted — 9 from a
  closed compiler enumeration (rustc TyKind, go reflect.Kind, javac
  TypeKind, ts TypeFlags, CLR CorElementType, libstdc++ type
  categories, kotlin PrimitiveType/StandardNames, swift
  Mirror.DisplayStyle, php gettype), 3 from the core type table
  (CPython builtins, ruby core classes, dart:core). The union is 59
  entries: 47 data, 12 compiler machinery; 6 already verified
  instruments, 53 new; 15 single-language. Two findings that change
  the picture — `dict` sits in only 6 of 12 compilers and `list` in 7
  (elsewhere both are library types), and `decimal` produced no row
  at all, refuting the CORE's first-pass expectation. Artifacts:
  `Research/type_vocabulary/{raw/,union.py,type_union.json,
  type_union.md}`. Report: `DevComms/log_022_type_vocabulary_union.md`.
- next: step B — the owner rules the set. The six rulings are listed in
  log 022 §6; the 13 normalization decisions he may overturn are in
  §4, and `Research/type_vocabulary/union.py` is the one file to edit.
