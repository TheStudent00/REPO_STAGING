# Tools

The project's current tools. HIGH change threshold — no litter.

- One tool, one folder, self-contained: the tool, its acceptance
  test, and its oracle assets live together. A tool without a
  falsifiable acceptance test does not enter this folder.
- Generalize what overlaps (tree-sitter handling, ledger, common
  transpiler machinery); specialize only where a language genuinely
  demands it.
- Old versions of anything go into this folder's `.archive/`
  (created on first use), never left beside the live file. Truly
  dead material is deleted — VCS remembers.
- Nothing enters Tools directly from an idea. It arrives via
  Research (proven) or a worked example (proven in use). The former
  `Application/` folder was retired 2026-07-31 with the plan node of
  the same name; its churn-then-graduate policy is this rule.
