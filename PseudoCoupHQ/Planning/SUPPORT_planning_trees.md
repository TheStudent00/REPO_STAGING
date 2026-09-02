---
id: hq.support.planning_trees
status: draft
---

# SUPPORT — planning_trees

Why there are several planning trees, how they relate, and which repo
has one. Written 2026-07-31 because the set of trees was being listed
without ever being explained.

---

## The trees that exist

Four, all conforming to the same framework
(`<WORKSPACE_DIR>/PlanPlan/framework/PROTOCOL.md`):

- `<WORKSPACE_DIR>/PseudoCoupHQ/Planning` — this one. the frame.
- `<WORKSPACE_DIR>/PseudoCoup_v5/Planning` — the Frankenstein rebuild;
  the turn of the cycle where the hub is still empty. founded
  2026-07-31 (the section below records the gap it closed).
- `<WORKSPACE_DIR>/PseudoCoup_v6/Planning` — the transpiler into the
  hub.
- `<WORKSPACE_DIR>/PseudoIR/Planning` — the system the hub is
  constructed with.

## Why more than one

Because a planning tree lives in a repo, and the repos are separate
for a reason that has nothing to do with planning: each project is a
deliverable someone could work on without the other. PseudoCoup can
be worked on knowing only the hub's surface. PseudoIR can be worked
on knowing only that a transpiler arrives.

One tree spanning both would put PseudoIR's internals in front of
someone working on PseudoCoup, which is the coupling the two-artifact
rule exists to prevent. So: one tree per repo, and a frame above them
for what is true across.

## What HQ's tree is for, and what it is not

**It is for what no single project can own.** The exchange between
the projects belongs to neither of them — each knows only its own
half — so it is settled here, in
[node_0_1_exchange](node_0_1_exchange/CORE_0_1_exchange.md), and the
project trees state it as dependents.

**It is not a super-plan.** HQ does not contain the projects' plans
at a coarser depth, and reading HQ does not tell you what PseudoIR is
building this month. HQ is deliberately shallow: three level-1 nodes
and no ambition to grow deeper. Depth belongs in the project trees,
because that is where the work is.

The test for whether something belongs here: **could either project
own this alone?** If yes, it goes there. If it would have to be
written twice, it goes here.

## How governance flows

The framework's rule is that a sub-document may refine its
super-document and never contradict it, and that corrections go
high-first. Across trees that reads as:

- HQ settles the exchange and the cycle. The project trees may
  restate them; a project copy that disagrees with HQ's is the
  project copy that is wrong.
- HQ does NOT govern anything inside a project's own subject. HQ has
  no opinion on how the ledgerer is structured.
- `<WORKSPACE_DIR>/DevComms/` governs all of them and is under none of
  them. It is its own thing (the owner, 2026-07-31), holding the
  communication protocol and `plan_and_code.md` — rules about how
  work is done, not about what is being built. HQ points at it and
  does not own it.

So there are three kinds of authority in play, and they are not
nested inside one another: DevComms rules how anything is written,
HQ settles what is true between the projects, and each project
settles its own subject.

## PseudoCoup_v5 had no planning tree — a gap, closed 2026-07-31

**CLOSED.** The tree now exists at
`<WORKSPACE_DIR>/PseudoCoup_v5/Planning/` (verified 2026-08-01: CORE_0
with a definition line confirmed by the owner, PROGRESS, CHECK, DASHBOARD,
and three nodes — tools, research, api — all carrying `designation`),
and it is in `hq.sh`'s ROOTS. The item is closed in this node's
PROGRESS. The record of the gap is kept below, per the standing
annotate-don't-delete rule.

It was absent from every list of planning trees in this repo and in
the tools' configuration. The reason was only that
`<WORKSPACE_DIR>/PseudoCoup_v5/` contained no `Planning/` folder —
checked 2026-07-31, its top level was `Designing/`, `DevComms/`,
`Research/`, `README.md` and `git_commit_push.sh`.

That made sense while PCv5 was archived research: nothing was being
planned there. **It stopped making sense on 2026-07-31**, when PCv5
became live for new work — gutted and rebuilt as the Frankenstein
transpiler and ledgerer, which is the precursor PseudoIR then uses.
A repo taking new work with no plan is exactly the "few folders with
a few files is not planning" failure.

The PCv5 decision itself was never what was missing — it is written
down in the gutting and annotate-don't-delete rule in
`<WORKSPACE_DIR>/PseudoCoup_v6/AgentMemory/02_decisions.md` under
Direction, the `Frankenstein` and `PCv5-archived-research` glossary
entries in that repo's `01_vocabulary.md`, and the roster entry in
[node_0_0_projects](node_0_0_projects/CORE_0_0_projects.md). What was
missing was a tree for the work the decision authorises, and that is
what founding the tree supplied.
