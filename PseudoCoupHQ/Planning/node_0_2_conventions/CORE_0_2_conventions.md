---
id: hq.conventions
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: rule, grouping
sub_nodes: []
super_node:
    name: hq
    path: ../CORE_0.md
node:
    name: conventions
    path: Planning/node_0_2_conventions/CORE_0_2_conventions.md
---

# CORE 0_2 — conventions

## metadata

- **id:** hq.conventions
- **level:** 1
- **status:** draft
- **designation:** rule, grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [hq](../CORE_0.md)

## sub_nodes

*(none yet)*

## definition

the rules the work is done under, and where each one lives. this
node does not restate them — it says what exists and what governs
what, so a fresh reader loads the right documents in the right
order.

## which hat — read this before editing outside HQ

the owner, 2026-07-31. Not a red-tape approval system; there is no request
form. It is about which repo a change is being made ON BEHALF OF.

**Two hats, worn at the same time, and they answer to different
things.**

- **Wearing the HQ hat**, we are DEVS of this repo and only USERS of
  `PRIVATE/PlanPlan`. From here we can only REQUEST a
  framework change. HQ does not dictate specifics to PlanPlan.
- **Wearing the PlanPlan hat**, we are devs of that repo. A
  request arriving from HQ gets made **if it is abstract enough that
  it makes sense for every project using PlanPlan** — and not if
  it only makes sense for this one.

So the question before editing PlanPlan is not "did the owner ask" and
not "does HQ need it". It is:

> **would this change be right for a project that has nothing to do
> with PseudoCoup?**

Yes means make it, and PlanPlan is new and evolving so this
happens often. No means it belongs in HQ instead.

Worked example, both directions. The CORE format rule — sub-node
listing first — is about how any planning tree reads, so it went into
PlanPlan. `plan_and_code.md` is about how THIS line maps plans to
code, so it belongs here; it had been written into
`PRIVATE/DevComms` and was moved to
`PRIVATE/PseudoCoupHQ/plan_and_code.md` 2026-07-31.

### `PRIVATE/DevComms` is a third thing again

Not the line's, not the framework's. Very high level decision-making
affecting most of the owner's work with LLMs, and **light on purpose**.
Line-specific content does not go there — that was the
`plan_and_code.md` error. It governs how anything is written and
answers to nothing here.

## the documents

- **communication protocol** —
  `PRIVATE/DevComms/LLM_communication_protocol.md`. how the owner is
  written to. the one authority: each repo's
  `DevComms/LLM_communication_protocol.md` is a SYMLINK to it
  (`../../DevComms/...`), not a copy. so drift between them is not
  possible — but see the fragility recorded in this node's PROGRESS,
  because a symlink pointing outside the repo behaves differently
  from a file inside it.
- **working logs** — `<repo>/DevComms/log_<nnn>_<topic>.md`. long
  explanations, analyses and post-mortems go in a log; the chat
  response stays short and points at it. protocol §18a, added
  2026-07-31 at the owner's request. numbering restarts per repo.
- **plan and code** — `PRIVATE/PseudoCoupHQ/plan_and_code.md`. plan
  names ARE code names; code is written top down with logic last;
  every node carries a `designation`. settled 2026-07-31.
- **the planning framework** —
  `PRIVATE/PlanPlan/framework/PROTOCOL.md`. the
  CORE/PROGRESS/SUPPORT/node grammar every tree in the line conforms
  to, and the frontmatter schema.

## the one script

`PRIVATE/PseudoCoupHQ/hq.sh` is where bash logic for the line
lives. it holds sequencing only — every step is a call into the
framework tools or into a repo's own commit script.

**the whole normal usage is `bash PRIVATE/PseudoCoupHQ/hq.sh`**
with no arguments. that regenerates the dashboards, checks every
planning tree, and commits and pushes every repo. `--force` pushes
despite failing checks.

the narrower commands exist for one part on its own: `check` (no
writes), `dashboard`, `list`, `help`.

**a failed check REFUSES the commit** (the owner, 2026-07-31). the reason
is on the record: a stale PROGRESS entry claiming work was undone
that was done sat in the repo for a day, and a warning printed above
a successful push is a warning nobody reads.

## the commit workflow

a session stages a message in each repo's
`DevComms/next_commit_message.txt`; the owner runs the script on the host,
because the sandbox cannot push.

- one repo alone: that repo's own `git_commit_push.sh`.
- the whole line: `hq.sh commit`, which calls
  `PRIVATE/PseudoCoupHQ/git_commit_push_all.sh`, which calls
  each repo's own script rather than doing git work itself. every
  repo therefore stays able to commit standalone.
- each repo uses its own staged message. there is deliberately no
  global message option — one message labelling four unrelated
  commits is what the staged-message convention exists to avoid.

## the framework tools

in `PRIVATE/PlanPlan/framework/`, all standard library
only:

- `render_plan.py` — one planning tree as an HTML page.
- `check_plans.py` — consistency ACROSS trees: dangling
  `...` references, prose duplicated between trees, id
  collisions, references to archived material, missing
  `designation`. reports by cause with sightings beneath, not one
  item per sighting.
- `generate_dashboards.py` — writes `DASHBOARD.md` into every node
  folder, rolling up that node's sub-tree. generated, never hand
  edited, and deterministic: two runs are byte identical, so a
  dashboard never churns the diff.
- `generate_nodes.py` — realizes the frontmatter `nodes` register:
  diffs each CORE's register against the folders on disk and creates
  the missing node folders with skeleton CORE, PROGRESS and CHECK.
  dry run by default, `--apply` to write; rebuilds the touched CORE's
  `## nodes` projection, and `--projections` refreshes every
  projection tree-wide (run it after writing a definition a skeleton
  was generated without). `--adopt` is the one-off for a tree that
  predates the register: it writes each register FROM the folders on
  disk, then projects — the only place anything runs backwards from
  the markdown, and it never overwrites a register that exists. it
  never invents a `designation` (that
  judgement stays a person's, surfaced by the missing-designation
  warning). run dashboards after it, or plain `hq.sh` does.

### the `(historical)` marker

a line naming a path that deliberately no longer exists carries
`(historical)`, and `check_plans.py` skips it. this exists because
the standing rule is to ANNOTATE what has gone rather than delete it
— a fallen position keeps its record. without the marker, writing
"it used to live at X" is indistinguishable from a stale pointer at
X, and the check would push writers into erasing the history it is
meant to preserve. it is the mechanical form of the
`PCv5-archived-research` annotation in
`PRIVATE/PseudoCoup_v6/AgentMemory/01_vocabulary.md`.

a marker used to silence a REAL stale pointer turns the check off
exactly where it was working.

## conformance of the trees

this HQ tree carries `designation` on every node from birth.
PseudoCoup_v6's and PseudoIR's trees predate the field and do NOT
conform yet; bringing them into conformance is a job of its own,
described in `PRIVATE/PseudoCoupHQ/plan_and_code.md` §4.

the framework's renderer does not yet require `designation` — the
check lands with the trees' update, not before, or it would report
every node in both project trees as defective.
