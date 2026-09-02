---
id: pcv6.tools.t1_tree_sitter_base
level: 2
status: settled
settled_by: the owner
supersedes: null
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
