---
id: pcv6.ledgerer.support.tree_sitter
status: projected
---

# SUPPORT — tree_sitter

projected 2026-07-30 from the previous plan, now archived at
`<WORKSPACE_DIR>/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_0_tree_sitter_base/CORE_0_0_0_tree_sitter_base.md  (111 words)
verdict: clean
changed: nothing

---

# CORE 0_0_0 — T1: tree_sitter_base

One place owning grammars and parsing for every language the
project touches; nothing else constructs a parser. Fully general —
zero per-language logic beyond grammar selection.

- Contents: vendored grammars commit-pinned with a provenance
  manifest (harvest: `PseudoIR/v2/grammars/` pattern, 12 languages;
  ADD rust + c/cpp for compiler-source ingress); parser factory
  (harvest: v1 `core/parser.py`, 49-line dispatch); node
  census/coverage recorder (harvest: WFL `ingress/coverage.py` +
  justified baseline; v0 `classify.py` total-partition
  strictness).
- Acceptance: per grammar, parse a pinned sample and byte-compare
  the serialized census against a frozen expectation
  (deterministic regeneration); coverage recorder self-test —
  partition of a sample tree is total.
- Depends on: nothing. Everything depends on it.
