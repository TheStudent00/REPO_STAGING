---
id: pcv5.progress
status: living
---

# PROGRESS — node_0

- 2026-08-02: the three conformed nodes here — `pcv5`, `pcv5.tools`,
  `pcv5.tools.ledgerer` — follow the same day's field changes: entry
  key `name`, a `node` field on each, and no `nodes` register left.
  This tree's root now states its OWN repo (`PseudoCoup_v5` and its
  remote), which is what the owner noticed was missing while its
  `super_node` already named HQ's.
- 2026-08-02 **done**: `pcv5`, `pcv5.tools` and `pcv5.tools.ledgerer`
  brought to the 2026-08-02 rules — `super_node`, `sub_nodes`, and
  CHECK frontmatter carrying `id: <node id>.check`. The HQ half of the
  same pass is in `PRIVATE/PseudoCoupHQ/Planning/PROGRESS.md`.
  - This tree's root now states what it hangs under:
    `hq.projects`, by absolute path, with `repo: PseudoCoupHQ` and its
    remote — the first cross-repo edge written under the new rules.
  - `research`, `api`, `transpiler`, `polyfill` and `tracer` each
    gained a `super_node` and nothing else, because the nodes above
    them name them in `sub_nodes` and an edge is not allowed to be
    stated at one end. Their own `sub_nodes` wait for their turn.
  - Verified: 0 errors across all five trees, and the cross-repo edge
    was broken on purpose and caught before being restored.
- 2026-08-02 **correction**: the bullet below saying "no CHECK files
  yet" was already false when it was written down as an open item —
  every one of this tree's 8 node folders holds one, and
  `check_plans.py` reports a missing CHECK as an ERROR, so the tree
  could not have passed a check without them. What was true is the
  part about their CONTENT: only the completeness question is
  specified, and §3b still says the fuller shape of a by-hand check is
  unsettled.
- 2026-07-31: tree founded. shallow clone of PseudoCoup_v6's shape,
  level 0 and level 1 only, per the owner. deliberately NO AgentMemory
  folder, also per the owner — the line-wide material would otherwise exist
  once per version and drift.
- 2026-07-31: every node carries `designation` from birth. this and
  PseudoCoupHQ's are the only two trees in the line that do.
- no CHECK files yet. their location is settled
  (`CHECK_<indexpath>_<description>.<ext>`, beside the CORE) but what
  a by-hand check contains is not, so none are written rather than
  writing ones that would have to be redone.
- **the gutting has NOT happened.** `Designing/` and `Research/` still
  hold the pre-gutting research, untouched. this tree was added
  alongside them, not in place of them. deleting is a separate act
  and needs its own go-ahead — the recorded lesson is that the last
  purge over-deleted by about 1,900 lines because the scope was
  accepted without being measured.
- next, and all the owner's: confirm or replace the definition line in
  CORE_0, then the three level-1 COREs.
