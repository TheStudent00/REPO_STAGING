---
id: hq.progress
status: living
---

# PROGRESS — node_0

- 2026-08-02: `hq` and `hq.projects` follow the field changes the owner
  settled the same day — the edge entry key is `name` rather than
  `description`, both nodes carry a `node` field stating themselves,
  and the superseded `nodes` register is gone from both. `hq`'s
  `node` carries `repo: PseudoCoupHQ` and its remote because it is a
  tree root; `hq.projects` carries neither, since below a root they
  are derivable by walking `super_node` up.
- 2026-08-02 **done**: `hq` and `hq.projects` brought to the
  2026-08-02 rules — `super_node`, `sub_nodes`, and CHECK frontmatter
  carrying `id: <node id>.check`. This is the HQ half of the first
  chain conformance pass; the other half is recorded in
  `PseudoCoup_v5/Planning/PROGRESS.md`.
  - **The HQ-to-PCv5 edge is now stated, and it never was before.**
    `hq.projects` names `PseudoCoup_v5/Planning/CORE_0.md`
    in `sub_nodes` with `repo` and `remote`, and PCv5's root names
    `hq.projects` back in `super_node`. Until today the only thing
    joining the two trees was a sentence, and it pointed two levels
    deep into PCv5 rather than at its root — so a reader descending
    from HQ never passed PCv5's own CORE.
  - `hq.projects` names all three repos, not only PCv5, because it is
    the roster. PCv6's and PseudoIR's roots each gained the matching
    `super_node` so that no edge is left stated at one end.
  - **Conforming a chain reaches one step sideways at each level.**
    `hq` names `exchange` and `conventions` in `sub_nodes`, so both
    needed a `super_node` or the edge would have been half-written.
    They got that field and nothing else; their own `sub_nodes` wait
    for their own turn. This is a property of the both-ends rule worth
    knowing before the next chain: the unit of work is a chain plus
    the co-nodes it touches.
  - Verified: 0 errors across all five trees. The edge was also
    broken ON PURPOSE — PCv5's `super_node` repointed at
    `hq.exchange` — and the checker reported both an
    `edge-disagreement` and an `edge-one-ended`; the file was then
    restored and confirmed byte-identical to its backup.
- 2026-07-31: tree founded. three level-1 nodes drafted (projects,
  exchange, conventions), all `status: draft` pending the owner. node names
  and the count are the first thing to cut or keep.
- 2026-07-31: this tree carries `designation` on every node from
  birth, per `PseudoCoupHQ/plan_and_code.md`. it is the
  first tree in the line that does — PseudoCoup_v6's and PseudoIR's
  predate the field and do not conform yet.
- 2026-07-31: SUPPORT_planning_trees.md written at the owner's request —
  prose for the meta-vision of the several planning trees: why more
  than one, what HQ is and is not, and the three non-nested kinds of
  authority (DevComms rules how anything is written, HQ settles what
  is true between the projects, each project settles its own
  subject).
- raised by the owner 2026-07-31, **closed 2026-08-01** (see the closing
  sub-bullet): `PseudoCoup_v5/` had NO planning tree,
  which is why it was absent from every list of trees here and from
  the tools' configuration. Verified the same
  day: its top level is `Designing/`, `DevComms/`, `Research/`,
  `README.md`, `git_commit_push.sh` — no `Planning/`.
  - That was correct while PCv5 was archived research. It stopped
    being correct on 2026-07-31 when PCv5 became live for new work as
    the Frankenstein rebuild.
  - The DECISION about PCv5 is recorded in three places and is not
    what is missing; what is missing is a tree for the work the
    decision authorises.
  - Founding it is a small mechanical job — `Planning/CORE_0.md` plus
    `PROGRESS.md` conforming to the framework — but its CORE_0 is
    the owner's to settle, and the first question it has to answer is what
    version 5 IS now that it is neither the old research nor PCv6.
  - 2026-07-31: a proposed definition written at the owner's request, in
    `PseudoCoupHQ/DevComms/log_002_what_pcv5_is.md` —
    version 5 as the PseudoCoup that serves PseudoIR (eats compiler
    source, holds the Frankensteins, runs before a hub exists),
    version 6 as the one that serves applications. Derived clause by
    clause from what the owner has said, with the join marked as Claude's.
    Awaiting his yes or no; nothing is built on it.
  - 2026-08-01 **done**: the tree exists. Verified on disk:
    `PseudoCoup_v5/Planning/` holds `CORE_0.md`
    (`id: pcv5`, definition line confirmed by the owner 2026-07-31 and
    marked in the file), `PROGRESS.md`, `CHECK_0.md`, `DASHBOARD.md`,
    and three nodes (tools, research, api), every node carrying
    `designation`. `hq.sh` ROOTS and `git_commit_push_all.sh` REPOS
    both include PCv5, so the tools' configuration is current too.
    `SUPPORT_planning_trees.md` updated the same day from three trees
    to four.
- 2026-07-31 **done** (the owner: "yeah add them"): the project plans' cycle
  text now depends on this tree.
  `PseudoCoup_v6/Planning/CORE_0.md` and
  `PseudoIR/Planning/CORE_0.md` each open "the other
  project" by naming node_0_1_exchange as where it is settled, and
  state that a project copy disagreeing with HQ's is the project copy
  that is wrong. an earlier entry here recorded this as deferred
  pending the owner's ruling on the tree's shape; he ruled the same day.
  - this entry was itself stale for part of the day, which is the
    same defect the checker was built to catch — and it did not catch
    it, because a PROGRESS claim going out of date is prose, not a
    broken reference. worth knowing about the tooling's reach.
