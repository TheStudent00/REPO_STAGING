# log 001 — is PlanPlan ready for use, and its own tree

2026-08-01. Written because the owner asked two things:

> what we need is a concrete/consistent/functional PlanPlan. is
> PlanPlan good?

and, later:

> and why doesnt PlanPlan use its own framework?

This log holds the answer to the first and the record of what was
done about the second. Everything below was measured on the day, by
running the tools; nothing is from memory.

Scope: this is about PlanPlan's own design — the framework and
its tools. It is not about how any project uses the framework.

---

## 0. Status, end of 2026-08-01

**Every item in section 2 is CLOSED.** The section is kept as written
because it is the record of what was wrong and why; each item now
carries its closing note. Read section 0 for the state; read section
2 for the history.

- 2a `render_plan.py` blind to the register — closed by the
  restructure. `planning_model.py` and `checks.py` exist,
  `check_plans.py` is a thin entry point, and no file imports
  `render_plan.py`.
- 2b PROTOCOL §1 vs §3b — closed. §1 now says exactly-one and
  enforced.
- 2c staleness undetected — closed for the flow that matters:
  `bash PRIVATE/PseudoCoupHQ/hq.sh` now rebuilds BOTH generated
  artifacts (projections and dashboards) before checking. A bare
  `check_plans.py` run still does not detect a stale projection
  description; that remains true by design and is noted below.
- 2d §6 named the wrong trees — closed. It now lists all five trees
  with where each stands.
- 2e three cosmetics — two closed (the duplicated §3b bullet, the
  misleading "nothing to generate" message). The third was NOT a
  defect: `check_plans.py` exits 1 on a nonexistent root, as its
  docstring says. The audit's claim of exit 0 came from a shell test
  that read the exit code of `tail` through a pipe rather than of
  Python.
- 2f uncommitted — messages staged in every affected repo.

Also done that day, after this log was first written:

- All five trees are mechanically conformant: registers, `## nodes`
  in first position, CHECK and DASHBOARD everywhere. PseudoCoup_v6
  and PseudoIR were brought in with `--adopt`.
- The strict CORE shape landed: nothing between the title and
  `## nodes`, definition in `## definition` below it.
- PlanPlan's own 12 nodes carry a `designation`.

What is left is the owner's, not mechanical: no node in any tree is
`status: settled`, and `designation` is unfilled on 28 nodes across
PseudoCoup_v6 and PseudoIR. Both fill in as branches are deepened.

---

## 1. The verdict as of the audit: functional, not yet consistent

Nothing is broken. Four tools were run against four real trees,
individually and combined: no crashes, no tracebacks. Roughly 28
defects were planted one at a time into a synthetic conforming tree,
and every claim `PROTOCOL.md` makes about tool behaviour was
reproduced with the documented message.

The remaining problems share one cause: **the register work of
2026-08-01 landed in `PROTOCOL.md` and `check_plans.py`, and not
everywhere else it touches.**

The `nodes` register is the frontmatter field that lists a node's
sub-nodes, added that day. It replaced reading the markdown for that
information.

---

## 2. Six items, as found (all now closed — see section 0)

### 2a. `render_plan.py` does not know the register exists — CLOSED 2026-08-01

`render_plan.py` still finds sub-nodes by scanning the CORE body for
`node_.../` links and comparing them to the folders on disk. That is
reading markdown for truth, which is the mechanism the register
replaced.

Verified: the only occurrence of the string `nodes` in that file is

> SKIP_SECTIONS = {"nodes"}

which hides the `## nodes` section from the rendered detail view and
has nothing to do with the register.

Two defects were planted and both drew **0 grammar problems** from
`render_plan.py`, while `check_plans.py` reported each as an ERROR:

- a folder present on disk but absent from the register
- a folder whose index disagrees with its position in the register

It does not report conforming trees as broken. It is a subset
validator, not a wrong one. But two tools in one repo now hold
different definitions of "conforming", which is the drift this
framework exists to prevent.

**Needs the owner**, because it is a question about what a tool IS.
`render_plan.py` currently holds `scan_node`, the function that
performs the grammar checks, and `check_plans.py` imports it. So
some checking lives in the renderer today. The two directions:

- move the register checks into the shared function, so both tools
  see them; or
- move all checking out of `render_plan.py` into `check_plans.py`,
  leaving the renderer to render.

### 2b. `PROTOCOL.md` contradicts itself on CHECK enforcement — CLOSED 2026-08-01

§1, in the CHECK file bullet:

> Zero-or-one for now rather than exactly-one; §3b records that every
> node is meant to carry one and why the tools do not yet enforce it.

§3b, under "Existence is enforced":

> Settled 2026-07-31. `check_plans.py` reports as an ERROR any node
> folder missing a CHECK file or a DASHBOARD.md.

Same document, same date, opposite claims. The code sides with §3b —
deleting either file produces `[ERROR] missing-check` or
`[ERROR] missing-dashboard`. §1's sentence was left behind when that
rule shipped and should be deleted.

### 2c. A clean `check_plans.py` run does not mean the tree agrees with itself — CLOSED 2026-08-01 for the hq.sh flow

Two files in each node are generated rather than written: that node's
`DASHBOARD.md`, and the `## nodes` section of its CORE.

Each has a tool that detects staleness. `check_plans.py` calls
neither:

- `generate_dashboards.py --check` reports stale dashboards.
- `generate_nodes.py --projections` in dry run reports projections
  that no longer match their register.

Measured that day: `check_plans.py` reported 0 errors on PseudoCoup_v6
and PseudoIR while 24 of their dashboards were stale. The dashboards
were regenerated afterwards and all 44 are current now, so the state
is fine and the CHECK is the gap.

Also unchecked: `check_projection()` compares only the bracketed
titles in `## nodes`, never the descriptions after them. A stale
description passes clean.

### 2d. §6 names the wrong trees as conforming — CLOSED 2026-08-01

> Conforming projects: PseudoCoup_v6
> (`PRIVATE/PseudoCoup_v6/Planning/`) and PseudoIR
> (`PRIVATE/PseudoIR/Planning/`), which were one tree until
> 2026-07-31.

Those two are the trees with no register at all — 10 of 10 COREs and
18 of 18 COREs respectively. PseudoCoupHQ and PseudoCoup_v5 are at
100% and are not named. The sentence should say which tree conforms
to what, and when.

### 2e. Three cosmetic defects — two CLOSED 2026-08-01, one was not a defect

- §3b carries two near-duplicate bullets about how a node's CHECK
  composes with the rule that every tool ships its own acceptance
  test.
- `check_plans.py`'s docstring says exit code 2 for a nonexistent
  root; the code returns 1.
- `generate_nodes.py` prints "nothing to generate" after refusing a
  bad register entry, when the refusal is the real reason.

### 2f. The register feature was uncommitted — CLOSED by staging

Everything describing the register — `PROTOCOL.md`'s 2026-08-01
bullets, `check_nodes_register`, `check_projection`, the conformance
banner, `--adopt`, `--projections` — existed only in the working tree
when the audit ran. A commit message is staged in
`DevComms/next_commit_message.txt`.

---

## 3. The tree, founded 2026-08-01

### Why it was missing

No exemption was ever recorded. `PROTOCOL.md` and `README.md` were
both searched for one and neither says the framework does not apply
to this repo.

The closest thing to a cause is §6's wording:

> The framework is a template, not a dependency: conforming
> projects copy the conventions; PlanPlan later EXTRACTS
> instances from their VCS histories for the ontology-evolution
> dataset.

That puts PlanPlan on one side and "conforming projects" on the
other. It never says PlanPlan is exempt; it just never counts it
as a candidate. Offered as a reading, not a finding.

### What was founded

`PRIVATE/PlanPlan/Planning/`, with three level-1 nodes
taken from this repo's own README: framework, analysis, instances.

Two of the three have no folder on disk. There is no `analysis/` and
no `instances/`. That is the point — unbuilt work with no plan was
sitting in the framework's own repo.

### The founding was done through the tools, on purpose

`CORE_0.md` was written by hand with its register. Everything below
it came from

    python3 PRIVATE/PlanPlan/framework/generate_nodes.py \
        PRIVATE/PlanPlan/Planning --apply

so the founding doubles as a live test of the generator. It produced
three node folders with skeleton CORE, PROGRESS and CHECK files, then
rebuilt the root's projection.

One behaviour worth recording: the skeletons carry no definition
line, so the first projection listed them as bare links. The
definitions were then written by hand and `--projections --apply`
re-run to pick them up. That is the known one-run lag, working as
described.

### What is the owner's

- The level-0 definition line, the three node names, and the count.
  All are currently drawn from the README rather than settled.
- `designation` on the three level-1 nodes. The generator does not
  write the field, per his ruling that the judgement is made by hand
  when a node's definition is settled.
