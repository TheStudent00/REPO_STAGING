---
id: pp.progress
status: living
---

# PROGRESS — node_0

- 2026-08-02 **done** (the owner's instruction): the repo was renamed from
  `PlanningPlan` to `PlanPlan`, folder and git remote together.
  - Measured before the edit: 176 sites across 6 repos. 52 of them
    were in generated `DASHBOARD.md` files and were NOT hand-edited —
    they were regenerated, per the standing contract that a hand edit
    to a dashboard is lost the next time the tool runs. 6 more sit
    inside `.archive/` folders and were left alone, since an archive
    is the record of what was. The remaining 122 in 39 files were
    edited.
  - The substring hazard §6c warns about was checked before anything
    ran: neither name contains the other, so the doubled-suffix
    failure that bulk rename produced on 2026-07-31 cannot occur here.
  - **Quoted speech carries the new name too, on the owner's ruling.**
    Eight lines quote his own words and originally said
    `PlanningPlan`. They were restored to the old name by hand, then
    changed back when he ruled "its fine. refactor them" — so the
    repo has ONE name everywhere, in quotations as well as in prose.
    The sites are in
    `PlanPlan/DevComms/log_001_readiness_and_tree.md`,
    `PlanPlan/Planning/CORE_0.md`,
    `PlanPlan/framework/generate_nodes.py`,
    `PseudoCoupHQ/DevComms/log_005_session_state_2026_08_01.md`
    and
    `DevComms/proposal_2026-08-01_communication_protocol.md`.
    The only two places the old name survives are this bullet and the
    matching one in
    `PseudoCoupHQ/Planning/node_0_2_conventions/PROGRESS.md`,
    which record the rename itself.
  - Verified after: `check_plans.py` gives 0 errors over the four line
    trees and 0 errors over this one, `hq.sh check` runs end to end,
    and all four framework Python files parse.
  - **Still the owner's, and not done here: the GitHub side.** The local
    remote now points at `https://github.com/<owner>/PlanPlan.git`;
    the repo itself has not been renamed on GitHub.
- 2026-08-01: tree founded, at the owner's instruction, after he asked why
  the framework's own repo did not use the framework. no exemption
  was ever recorded; see this node's CORE for the search that
  established that.
- 2026-08-01: the three level-1 nodes are this repo's own three areas
  quoted from `README.md` — framework, analysis, instances. two of
  the three have no folder on disk yet.
- 2026-08-01: the tree was founded THROUGH the framework's own tools,
  deliberately, so the founding doubles as a test of them. `CORE_0.md`
  was written by hand with its `nodes` register; the three node
  folders, their skeleton COREs, PROGRESS and CHECK files were
  created by
  `python3 PlanPlan/framework/generate_nodes.py PlanPlan/Planning --apply`.
- **open, the owner's to settle**: the level-0 definition line, the three
  node names, and the count. all are currently drawn from the README
  rather than settled, and are marked as such in the CORE.
- **open, the owner's to settle**: `designation` on the three level-1
  nodes. the generator does not write the field, per his ruling that
  the judgement is made by hand when a node's definition is written.
  the missing-designation warning names them until then.
- **open**: readiness items for the framework itself, recorded with
  evidence in
  `PlanPlan/DevComms/log_001_readiness_and_tree.md`.
- 2026-08-01 **done** (the owner: "if its not already in an archive, put it
  there"): `install_silverbullet.sh` moved to
  `framework/.archive/install_silverbullet_superseded_2026-07-31/`.
- 2026-08-01 **done** (the owner confirmed §3b: "seems like a good check
  policy to have"): PROTOCOL §1's CHECK bullet now says exactly-one
  and enforced; its stale "zero-or-one, not yet enforced" wording is
  gone. log_001 item 2b closed.
- 2026-08-01 **ruled by the owner, restructure pending**: "nothing should
  be depending on the visualization." `check_plans.py` imports its
  grammar checks from `render_plan.py`, so the checker depends on the
  viewer — backwards under the ruling. Proposal in this session's
  reply awaits his yes; the direction itself is settled.
- **future development note** (the owner, 2026-08-01, on stale projection
  DESCRIPTIONS passing check_projection clean): "we can add a future
  development note to catch this kind of stuff using VCS analysis.
  but right now, im concerned with the fucking basics." Belongs to
  node_0_1_analysis when that node is planned.
- **backseat** (the owner, 2026-08-01): the HTML viewer's fold UI — cards
  that fold, not sideways/down arrows. Recorded in PROTOCOL §7;
  explicitly not load-bearing.
- 2026-08-15 **done**: new tool `framework/rename_node.py` — renames a
  node in one pass (folder, CORE/CHECK filenames, the node's own
  frontmatter, the super-node's register entry and projection link,
  every direct sub-node's `super_node` edge, and every other document
  in the tree that still names the old folder/CORE/id), plus an
  optional `--also-artifacts` to rename a research/artifact directory
  outside the planning tree and sweep references to it across a given
  set of scan roots. Dry run by default; refuses and writes nothing on
  a name collision or an unclean tree. Records the framework tension
  between PROTOCOL §3 ("renames keep the id") and `checks.py`'s
  `node-self-name` check (id tail must equal the new folder name) by
  changing the id to match — same tool's docstring has the `## rename
  provenance` note — and prints the old id plus appends it, dated, to
  the node's PROGRESS.md. First real use: the
  `Research/kind_clustering` -> `Research/kind_signature_clustering`
  artifact-directory finish of PseudoCoupHQ's 2026-08-14 node rename
  (see that node's PROGRESS at
  `PseudoCoupHQ/Planning/node_0_3_research/node_0_3_0_kind_signature_clustering/PROGRESS.md`),
  25 files rewritten across PseudoCoupHQ and PseudoCoup_v5, `hq.sh
  check` still 0 errors afterward.
