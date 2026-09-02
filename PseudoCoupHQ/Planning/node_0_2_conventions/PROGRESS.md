---
id: hq.conventions.progress
status: living
---

# PROGRESS — conventions

- 2026-08-02 **standing prohibition, the owner**: a Rust code generation
  backend is BANNED from every repo in the line, with the consequence
  the owner stated — permanent firing of Anthropic from any of his work.
  `<WORKSPACE_DIR>/PseudoCoupHQ/CRANELIFT_IS_BANNED.md` is the authority
  and the only file that names it. It OVERRIDES every older document
  in any repo that endorses it: those are historical record under the
  annotate-don't-delete rule, and a citation to one is not
  authorization. This belongs in HQ because it holds across the line
  and no single project can own it.

- 2026-08-02 **done** (the owner's instruction): the framework repo is now
  `<WORKSPACE_DIR>/PlanPlan`, renamed from `PlanningPlan`. Every path in
  this node's CORE, in `<WORKSPACE_DIR>/PseudoCoupHQ/hq.sh` and in
  `<WORKSPACE_DIR>/PseudoCoupHQ/plan_and_code.md` was updated with it.
  The full account of the rename, including what was deliberately not
  edited, is in `<WORKSPACE_DIR>/PlanPlan/Planning/PROGRESS.md`.
  - The hats rule in this node's CORE is unaffected in substance: HQ
    is still only a USER of that repo and can only request framework
    changes of it. Only the name changed.
- 2026-08-01 **done and exercised**: `generate_nodes.py` built in
  `<WORKSPACE_DIR>/PlanPlan/framework/` — the register realizer the
  `nodes` field was designed for. exercised on a synthetic tree:
  dry-run listed without writing; `--apply` created two level-1 nodes
  and then a level-2 node under one of them (correct chain, id, and
  level); re-run reported nothing to generate; an invalid register
  title was refused by name; a `##` heading inside a fenced code
  block did not fool the projection rewrite; `check_plans.py` on the
  result: 0 errors. on the four real trees: nothing to generate,
  which is correct — every registered sub-node is realized.

- 2026-07-31: written as a pointer node — what exists and what
  governs what, not a restatement of any of it.
- 2026-07-31: **no arguments now means do everything** (the owner: "i just
  want to run the script ... i want to simplify this"). Bare
  `bash <WORKSPACE_DIR>/PseudoCoupHQ/hq.sh` regenerates dashboards,
  checks, and pushes; `--force` works with or without the word
  `commit`. The previous behaviour — no arguments printed usage —
  made the common case the one you had to read instructions for.
  Re-tested all three paths after the change.
- 2026-07-31 **done and exercised**: `<WORKSPACE_DIR>/PseudoCoupHQ/hq.sh`
  built with check / dashboard / commit / list, checks blocking
  commits per the owner's ruling.
  - `check`, `dashboard`, `list`, no-args usage and unknown-subcommand
    all run through hq.sh itself, correct exit codes. dashboards
    byte-identical across two runs driven through hq.sh.
  - the `commit` GATE was tested by copying hq.sh with only the final
    `git_commit_push_all.sh` call stubbed to an echo, leaving the gate
    logic untouched, and running all three paths: checks pass reaches
    git (exit 0); checks fail without `--force` prints REFUSING TO
    COMMIT, exits 1, and does NOT reach git; checks fail with
    `--force` prints the override warning and proceeds. the failure
    was induced with a real planted dangling path, then removed.
  - NOT exercised: the live git half. The sandbox cannot push, so
    `git_commit_push_all.sh` calling four real `git_commit_push.sh`
    scripts has never run end to end. That is the one part of the
    chain whose first real run will be the owner's. `check_plans.py` and `generate_dashboards.py` built
  in `<WORKSPACE_DIR>/PlanPlan/framework/`; `render_plan.py` and
  PROTOCOL.md §1 updated so `DASHBOARD.md` is grammar, not a stray.
- 2026-07-31: the checker paid for itself on first run — six dangling
  cross-repo references in PseudoIR's SUPPORT files, all left by the
  2026-07-31 renames, all pre-existing. fixed by cause (three causes:
  the PCv6 internal renames, the tool move to PseudoIR, and material
  removed in the purge). now 0 errors.
- 2026-07-31: the `(historical)` marker added to `check_plans.py`
  after the first fix pass produced two NEW errors from prose
  deliberately naming dead paths in the past tense. verified the
  exemption does not blind the check: a genuinely stale path added as
  a test was still caught, and the test line was removed.
- open: warnings stand, all expected. **counts restated 2026-08-01**
  — the earlier form of this bullet said "5 warnings, designation
  missing on 28 of 32 nodes" and both numbers had gone stale, which
  is the same defect this file exists to catch.
  - measured 2026-08-01: **6 warnings**. `designation` missing on
    **28 of 40** nodes — the numerator is unchanged (PCv6 and
    PseudoIR), the denominator grew because PCv5's 8 nodes were
    founded since, all of them carrying the field.
  - the sixth warning is new that day and expected: PCv6's and
    PseudoIR's COREs have no `nodes` register, added to the framework
    the same day. it clears branch by branch as those trees conform.
  - four are duplicated prose, three of which are the exchange/cycle
    text the two project trees carry as declared dependents of HQ —
    the check surfacing them is correct behaviour, not a defect to
    silence.
- open, carried from `<WORKSPACE_DIR>/PseudoCoupHQ/plan_and_code.md` §6:
  the renderer does not yet require `designation`. one line to add;
  waits for the project trees' conformance pass so it does not report
  every existing node as defective.
- raised 2026-07-31 as "open, and sharper than first recorded",
  **closed 2026-08-01** (see the closing sub-bullet):
  `<WORKSPACE_DIR>/DevComms/` was not a git repo, so
  `LLM_communication_protocol.md` and `plan_and_code.md` were not
  version controlled anywhere.
  - first stated 2026-07-31 as "the authority is the only
    uncontrolled copy, the three in-repo copies are controlled".
    **that was wrong.** measured the same day: each repo's
    `DevComms/LLM_communication_protocol.md` is a SYMLINK to
    `../../DevComms/LLM_communication_protocol.md`, confirmed with
    `ls -li` (three distinct inodes, each a `l`-mode entry) and
    `readlink`. git tracks the symlink, so what is version
    controlled in each repo is a POINTER, and the pointed-at content
    is controlled nowhere.
  - consequence: cloning any one repo on its own yields a dangling
    symlink, because the target resolves outside the repo. the
    protocol is only readable on a machine where the whole
    `<WORKSPACE_DIR>` layout is present.
  - upside, and the reason not to just replace them with copies:
    symlinks cannot drift. four real copies could, and keeping them
    in step would be a new job.
  - `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/LLM_communication_protocol.md`
    was briefly a real copy when HQ was founded; made a symlink
    2026-07-31 for consistency with the other three.
  - the ruling asked for was: version control `<WORKSPACE_DIR>/DevComms/`
    as its own repo, or move the authority into PseudoCoupHQ, or leave
    as is.
  - 2026-08-01 **done**: the owner ruled for its own repo and pushed it.
    Verified on disk: `<WORKSPACE_DIR>/DevComms/` is a git repo with
    remote `github.com/TheStudent00/DevComms_root`, working tree
    clean, commit "DevComms founding: communication protocol,
    plan_and_code, vocabulary analysis." — so the authority the
    symlinks point at is now version controlled. `plan_and_code.md`
    is gone from DevComms, completing its recorded move to
    `<WORKSPACE_DIR>/PseudoCoupHQ/plan_and_code.md`.
  - still true after the closure: cloning any one line repo alone
    yields a dangling protocol symlink, since the target resolves
    outside that repo. the difference is that the target now has a
    repo of its own to clone beside it.
