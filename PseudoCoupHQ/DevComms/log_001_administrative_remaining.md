# log 001 — what is left before branch work starts

Opened 2026-07-31 because the owner said the administrative stuff has to
settle before diving into branches. **Rewritten the same day** — most
of it closed within hours, so the original list would have misled more
than it helped.

Every state below was checked on disk when this was written. Nothing
is from memory.

---

## 1. What is actually left

**One item, and it is not a list.**

- **Ratify as we deepen.** All 36 CORE files are `status: draft`.
  Under the framework's governance rule, `CORE_0` and level-1 COREs
  change only through the owner. He has settled how this happens: **not a
  pass, and not by Claude.** the owner, 2026-07-31: "we will work through
  with depth together to make it conform as we go. no offense but i
  dont trust you to do it."
  - So conformance — `designation` fields, ratification, deepening —
    happens branch by branch, together, as each branch is worked.
    There is no conformance sweep to schedule and no go-ahead to wait
    for.
  - PseudoCoup_v5 is where it starts, since v5 is the basis for v6 and
    v6's decisions wait on it.

- **PseudoCoup_v5's definition line — CONFIRMED** by the owner, 2026-07-31.
  Marked in the file.

That is the whole of the administration. Everything below either
closed or turned out not to be a question.

## 2. Things that were on this list and should not have been

- ~~Two shape questions inside PCv5~~ — whether `api` is the right
  third node, and whether PCv6's `Tools/` move. the owner: "idk why this is
  coming up as an open problem right now. when we dive into planning
  for PCv5, these will be resolved." Recording work-that-happens-later
  as a blocking question made the list look longer than the job.
  - Also a wording error worth keeping: "move there as THE composition
    seed" implied a privileged source, which the parts-come-from-
    anywhere ruling had already denied. Parts are parts.
- ~~The `designation` conformance pass, mechanical, say the word~~ —
  it is neither mechanical nor Claude's to run. See above.
- ~~What a by-hand CHECK contains, blocking the first CHECK files~~ —
  the owner gave a first check (completeness) and said "we can figure out
  better checks later". All 36 CHECK files are written.

## 3. Closed since this log was opened

Recorded so none of it is re-opened.

- **HQ's node names** — `projects`, `exchange`, `conventions`. the owner:
  "those are good. if i dont like something, we can change it later."
- **`DevComms` version control** — ruled its own thing,
  not under HQ's authority. Repo created and pushed as
  `DevComms_root`; first commit `0b6d3de`.
- **PseudoCoup_v5 has no planning tree** — founded. Level 0 and level
  1, shallow clone of v6's shape, no AgentMemory per the owner.
- **PCv5 gutting** — done. 550 MB to 55 MB.
- **The `PCV5_ROOT` dependency** — gone. It was the item blocking a
  clean PCv5 gutting, and it blocked in two repos rather than one. The
  four files anything read are vendored with manifests; 135 tests pass
  across three repos with no environment variable set anywhere.
- **The CORE format rule** — sub-node listing first, in §1 and
  enforced.
- **The `CHECK_` file location** — settled and in the grammar.
- **PCv6's goals** — replaced with the owner's wording.
- **The hub slot** — `hub/` exists in PCv5, inert and refusing, 7
  tests.

## 4. What happens next

Not a sequence of administrative steps any more, because there is only
one item and it is not separable from the work.

**Start deepening PseudoCoup_v5, branch by branch, together.**
Ratification and `designation` happen as each branch is worked rather
than before. v5 first because it is the basis for v6.

## 3a. Final sweep, 2026-07-31

Run to answer "anything else?" rather than answering from memory.
Everything green: 135 tests across three repos, 0 check errors, four
trees at 0 grammar problems, all five commit messages staged.

One class of real staleness found, which no tool catches: **four
READMEs still instructed the reader to set `PCV5_ROOT`**, an
environment variable that no longer exists in any code after the
vendoring. Fixed in
`PseudoCoup_v6/Tools/{ledgerer,polyfill}/README.md`,
`PseudoIR/Tools/README.md` and
`PseudoIR/Tools/intentions/README.md`, plus two stale code comments
citing the same pattern. Each README's run command was then executed
as written to confirm it works: 19, 68, 19 and 14 passed.

Worth naming the gap: `check_plans.py` verifies that a PATH resolves,
not that an INSTRUCTION is still true. A README saying "set this
variable" survives the variable's deletion silently. That is the same
shape as the stale PROGRESS entry earlier in the day — prose going out
of date is invisible to a checker that reads references.

## 4a. Which hat — got wrong, now recorded

Not a permission question, a scope one. the owner's framing, 2026-07-31:

- Wearing the **HQ hat** we are devs of this repo and only USERS of
  `PlanPlan`; from here we can only request a
  framework change, and HQ does not dictate specifics to it.
- Wearing the **PlanPlan hat** we are devs of that repo, and a
  request gets made if it is **abstract enough to serve every project
  using the framework**.

So the test before editing PlanPlan is *"would this be right for a
project with nothing to do with PseudoCoup?"* Yes means make it — it
is new and changes often. No means it belongs in HQ.

`DevComms` is a third thing again: very high level, for
decisions affecting most of the owner's LLM work, and light on purpose. It
takes no line-specific content, which was the error —
`plan_and_code.md` is about how THIS line maps plans to code and had
been written there. Moved to `PseudoCoupHQ/` 2026-07-31
with every reference repointed.

Recorded as failure mode F12 and in full in
`PseudoCoupHQ/Planning/node_0_2_conventions/CORE_0_2_conventions.md`.

## 5. One thing not on any list

`PseudoCoup_v6/AgentMemory/` still holds line-wide
material — the vocabulary, the lineage and harvest maps, the settled
decisions, the lessons — inside one version's repo. the owner ruled that new
versions get no AgentMemory, which stops it multiplying, but it does
not answer where the line-wide half belongs now.
`PseudoIR/Agent_Memory.md` §5 has flagged this as
pending since before this session. Not blocking anything; will get
worse quietly.
