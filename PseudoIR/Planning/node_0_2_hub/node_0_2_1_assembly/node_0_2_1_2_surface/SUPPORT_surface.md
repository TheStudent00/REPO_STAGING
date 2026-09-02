---
id: pir.surface.support.surface
status: projected
---

# SUPPORT — surface

projected 2026-07-30 from the previous plan, now archived at
`<WORKSPACE_DIR>/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_2_hub/node_0_2_2_surface/CORE_0_2_2_surface.md  (259 words)
verdict: clean
changed: nothing

---

# CORE 0_2_2 — Surface Spelling

How hub source spells qualified semantics: `a r./ b` meaning
"divide with Rust's exact semantics".

## The mechanism

- **Parser-level fork**: `r./` as a real token with real
  precedence in a forked CPython. This is the mechanism. The
  fork's cost is a forked interpreter rebuilt per Python
  release.

## [DROPPED 2026-07-31, the owner] the import-hook rewrite

The previous plan carried a second, interim mechanism: a
meta-path finder intercepting `.pc` modules and rewriting
qualified spellings into method calls before Python parsed them
(PCv5's `pc_import.py`). It is dropped, not deferred.

Its three recorded costs were wrong precedence (the `|`-trick
binds low), error messages pointing at rewritten text, and
qualifiers restricted to positions where the infix trick parses.

The second of those is the debugger problem: after rewriting,
line and column numbers no longer match the file on disk, so
breakpoints and tracebacks land on text the author never wrote.
A stepping stone that cannot be stepped through is not a
stepping stone.

The fork was always the recorded end state and the rest of the
chain is already proven, so the interim mechanism buys nothing
and costs a debugger.

## Work items

1. [DROPPED 2026-07-31, the owner] transplanting the import-hook
   mechanism. The insertion stage's demo relied on it for its
   surface half; that demo now needs either the fork or a
   direct-call surface with no qualifier spelling at all.
   Recorded as a consequence, not yet decided.
2. Qualifier grammar as data: which spellings exist (`r./`,
   `r.%`, future `go.<op>`, …) derives from the intentions
   artifact (language × operator), not from hand-kept lists.
3. The fork, when the owner schedules it: its own depth node; the ABI
   and maintenance analysis from the PCv5 record carries forward
   as its starting material.

## Acceptance shape

A `.pc` module using every spelling the grammar-data declares
runs end to end; a spelling NOT declared is refused at import
with the missing declaration named (the T5 refusal posture at
the surface).
