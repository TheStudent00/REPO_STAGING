# Tools

This version's tools. HIGH change threshold — no litter.

Empty at founding (2026-07-31). The three tools this version is for —
ledgerer, transpiler, polyfill — are planned at
`PRIVATE/PseudoCoup_v5/Planning/node_0_0_tools/` and not yet
composed.

## Rules, carried from PseudoCoup_v6

- One tool, one folder, self-contained: the tool, its acceptance test,
  and its oracle assets live together. A tool without a falsifiable
  acceptance test does not enter this folder.
- Generalize what overlaps across languages; specialize only where a
  language genuinely demands it.
- Old versions go into this folder's `.archive/` (created on first
  use), never left beside the live file. Truly dead material is
  deleted — VCS remembers.
- Nothing enters from an idea. It arrives via Research (proven) or a
  worked example (proven in use).

## What this version's tools are made of

Composed from best-in-class parts across the lineage — "mine, don't
resurrect". Every transplanted component carries a provenance header
and its own acceptance test.

The test that separates a legitimate transplant from a banned
dependency: **after the harvest, could the source repo be deleted
without anything breaking?** Yes means transplant. No means
dependency, which is not allowed.

Parts list:
`PRIVATE/PseudoCoupHQ/DevComms/log_003_harvest_reminder.md`,
with line-cited evidence in the two 2026-07-27 surveys under
`PRIVATE/PseudoCoup_v5/DevComms/`.
