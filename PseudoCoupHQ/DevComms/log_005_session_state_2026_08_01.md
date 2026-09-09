# log 005 — session state, 2026-08-01

Written at the owner's request, so nothing from this session is lost:

> please generate documents for the state of the conversation so we
> dont lose track of anything.

The session touched four repos. This log is the index. Detail lives
in the repo it belongs to, per the hats rule.

---

## 1. Where the detail is

- **PlanPlan's readiness, and its new tree** —
  `PlanPlan/DevComms/log_001_readiness_and_tree.md`
- **Proposed communication-protocol changes** —
  `DevComms/proposal_2026-08-01_communication_protocol.md`
- **This session's HQ and PCv5 work** — sections 2 and 3 below.

---

## 2. What changed, and where

### PseudoCoupHQ

- Two stale open items closed: PCv5's planning tree exists, and
  `DevComms` is its own pushed repo.
- `SUPPORT_planning_trees.md` now lists four trees, not three. The
  record of the gap is kept in past tense.
- Roster corrections in `node_0_0_projects/CORE_0_0_projects.md`:
  PseudoIR holds three tools (transpile, slice, insert), not "two
  tools: insert, intentions"; `intentions` is a research node, not a
  tool. PCv5's entry points at PCv5's own tools CORE rather than
  naming a count.
- The PlanPlan entry was REMOVED from that roster, on the owner's
  instruction:

  > PseudoCoupHQ is not in charge of the development of PlanPlan
  > -- rather it informs the development of PlanPlan.

- `plan_and_code.md` gained the `object` designation kind, which
  `PROTOCOL.md` §3a had and it did not.
- Stale counts in `node_0_2_conventions/PROGRESS.md` restated: 6
  warnings, designation missing on 28 of 40 nodes.

### PseudoCoup_v5

- `pcv5.tools` deepened to four sub-nodes: ledgerer, transpiler,
  polyfill, tracer. the owner ruled the tracer a SIBLING of the ledgerer.
- Every CORE carries the `nodes` register.
- `node_0_1_research` and `node_0_2_api` had `## nodes` in last
  position; the tool moved it to first.

### PlanPlan

- `code (object)` added as the coarse designation kind, with a
  settle-guard: a node may not reach `status: settled` still carrying
  it.
- The frontmatter `nodes` register added as the sub-node truth, with
  `## nodes` demoted to a projection of it.
- `generate_nodes.py` written: realizes the register into folders,
  `--projections` refreshes projections tree-wide, `--adopt` writes
  registers into trees that predate the rule.
- `check_plans.py` gained the register checks, the projection checks,
  and a CONFORMANCE GAPS banner.
- A planning tree founded for the repo itself.

---

## 3. Open, and who owns each

### the owner's

1. **Whether to run `--adopt` on PseudoCoup_v6 and PseudoIR.** Those
   two trees have no register: 10 of 10 and 18 of 18 COREs. The
   command is
   `python3 PlanPlan/framework/generate_nodes.py <root> --adopt --apply`.
   It was verified on a COPY of PseudoIR's tree — 18 registers
   written, projections rebuilt, 0 errors — and has NOT been run on
   any real tree.
2. **HQ `CORE_0.md`'s `## the repos` section.** It opens

   > three, and these are the whole of it.

   while `node_0_0_projects` is a second list of repos, and neither
   names PseudoCoupHQ itself or DevComms_root, both of which are
   repos.
3. **Where checking lives in PlanPlan.** See log_001 §2a: either
   the register checks move into the shared `scan_node`, or all
   checking moves out of `render_plan.py`.
4. **The five proposed protocol rules.** See the proposal file.
5. **PlanPlan's level-0 definition, node names, and the
   `designation` on its three level-1 nodes.**

### Claude's, mechanical, not yet done

6. `PROTOCOL.md` §1 versus §3b contradiction on CHECK enforcement.
7. `check_plans.py` should call the two staleness checks it currently
   leaves to a person.
8. `PROTOCOL.md` §6 names the wrong trees as conforming.
9. Three cosmetic defects, listed in log_001 §2e.

---

## 4. Two things worth carrying forward

- **`bash PseudoCoupHQ/hq.sh` is the runnable form.**
  There is no `hq.sh` command; it is a file, not on PATH and not
  executable. An alias was offered and not yet added.
- **Running the tools from the sandbox needs `$HOME` mapped**, or
  every `...` reference resolves nowhere and the
  checker reports ~85 false dangling paths. This cost two separate
  agents a wrong first result today.
