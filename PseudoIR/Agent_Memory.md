# Agent Memory — PseudoIR

Written 2026-07-31.

**This file does not restate the plan.** The plan is at
`~/Programming/PseudoIR/Planning/`, starting from `CORE_0.md`. If a
fact belongs in a node's CORE, it goes there and not here — two
stores of the same fact drift apart, and that has already cost this
project once.

What lives here is what the plan cannot hold: the other project, the
rules of engagement, what is banned, what is currently unsettled, and
the failures worth not repeating.

---

## 1. Read these first, in this order

1. `~/Programming/DevComms/LLM_communication_protocol.md` — the owner's
   communication protocol. Not optional. A local copy sits at
   `~/Programming/PseudoIR/DevComms/LLM_communication_protocol.md`;
   the one in `~/Programming/DevComms/` is the authority.
2. `~/Programming/PseudoCoupHQ/plan_and_code.md` — plan names ARE code
   names; code is written top-down with logic last; every node
   carries a `designation`. **This plan does not conform yet.**
   Bringing it into conformance is the next job, and nothing below
   describes the conforming state.
3. `~/Programming/PseudoIR/Planning/CORE_0.md` — what this project
   is, what it exchanges with the other one, and why the bootstrap
   cycle closes.
4. This file.

To see the plan as a tree rather than as folders:

```
python3 ~/Programming/PlanPlan/framework/render_plan.py \
    ~/Programming/PseudoIR/Planning -o /tmp/pir.html
```

---

## 2. The other project

PseudoIR does not stand alone, and an agent working only in this
repo will not otherwise know that.

- **PseudoCoup** lives at `~/Programming/PseudoCoup_v6/`. Its plan is
  at `~/Programming/PseudoCoup_v6/Planning/`. It is the tool that
  transpiles from source languages into the hub.
- **PseudoIR** is the system the hub is constructed with.

Exactly two artifacts cross between them:

- PseudoCoup gives PseudoIR a **transpiler**. PseudoIR has to get a
  compiler's source into hub source before it can slice it.
- PseudoIR gives PseudoCoup the **hub**. That is what PseudoCoup
  transpiles into.

Nothing else crosses. If you find yourself wanting a third thing to
cross, that is a signal the split is being violated — raise it with
the owner rather than reaching across.

**The hub is described in this project's plan and only here.**
PseudoCoup deliberately carries no second description of it. Do not
add one there, and do not let one grow.

---

## 3. Hard rules

- **The retired backend is banned.** A code-generation backend was
  purged from this project's lineage on 2026-07-30 after four
  separate work requests were aimed at its internals instead of at
  the settled direction. Do not name it, do not import it, do not
  cite it as an oracle, do not restore it from an archive. The
  settled direction is LLVM, via rustc's own LLVM path.
  - Guarding against the *name* is not enough. The failure was
    **direction**: work aimed at that backend's instruction
    selector, assembler, or lowering language is wrong even when
    scrubbed of its vocabulary. Judge by what a task points at.
- **The import-hook rewrite is dropped** (the owner, 2026-07-31). The hub
  surface is a parser-level fork of CPython where `r./` is a real
  token. The interim mechanism — a meta-path finder rewriting `.pc`
  modules before Python parsed them — is dropped, not deferred. It
  broke the debugger: after rewriting, line and column numbers no
  longer match the file on disk.
- **Names must be readable without opening the file.** the owner rejects
  titles that compress meaning into jargon. `isel_gap` was renamed
  to `choosing_machine_instructions` for exactly this reason.
  Acronyms that are not already in the owner's speech are not acceptable.
- **The term is IRMapping, never ISel** (the owner, 2026-07-31). Mapping an
  llvm ir operation to the machine instruction that implements it.
- **The transpiler works a file at a time from tree-sitter output**,
  building a UR-AST and wrapping what the file does not define. It is
  NOT function-at-a-time; that phrase came from the previous plan and
  is wrong. Do not repeat a claim about the transpiler that is not in
  its own CORE.
- **No socio-familial structure words.** Not parent/child, not
  siblings, not ancestors, not inherit. Use super/sub, co-node,
  super-chain, sub-tree, derive.
- **Full paths, always.** `~/Programming/...` or absolute. Never a
  bare filename, never a relative path in prose.
- **Claims about code come with the code.** Actual lines, actual
  output, actual error. Anything asserted from memory rather than
  checked this session gets marked "unverified".

---

## 4. Unsettled, as of 2026-07-31

Each of these is recorded in the plan too; listed here so a fresh
agent sees them without walking the tree.

- ~~**Does PseudoIR need its own transpiler?**~~ **ANSWERED (the owner,
  2026-07-31): no.** PseudoIR uses the Frankenstein transpiler and
  the Frankenstein ledgerer — tools composed from the best parts
  already scattered across the PseudoCoup lineage (the parts list is
  `~/Programming/PseudoCoup_v6/AgentMemory/03_lineage_and_harvest.md`).
  Neither exists yet; building them is what the PCv5 rebuild is.
  - The rebuild: `~/Programming/PseudoCoup_v5/` is gutted and
    commandeered as PCv6's precursor, and the two Frankensteins
    become version 5. Recorded in
    `~/Programming/PseudoCoup_v6/AgentMemory/02_decisions.md`
    under Direction, superseding the 2026-07-28 "PCv5 is archived
    research" decision.
  - The old open question at
    `Planning/node_0_0_tools/node_0_0_0_transpile/` was about what
    the first run transpiles INTO, with no hub to target. That half
    is still open; only "whose transpiler" is now settled.
  - **Not settled, and do not assume it**: whether §7's
    `PSEUDOCOUP_ROOT` borrow re-points at the rebuilt PCv5 once the
    Frankensteins live there, or stays on PseudoCoup_v6. the owner has not
    said.
- **Ledger population at scale has no anchor.** The measured figure
  (a 1.27M-node generated file) came from the retired backend's
  output, which is gone. No LLVM-side file of comparable size has
  been named to re-measure against. Blocks a step. Recorded in
  `Planning/node_0_2_hub/node_0_2_0_construction/node_0_2_0_0_rust_llvm/node_0_2_0_0_0_transpile/`
  support and in PseudoCoup's ledgerer `SUPPORT_todos.md`.
- **Seam declarations are retired, not replaced.** The previous plan
  held a 585-word specification for the one human judgment call
  before slicing became mechanical. It was written in the retired
  backend's vocabulary and is not projected. Rebuilding it against
  LLVM entry points is a fresh design job. See
  `Planning/node_0_1_research/node_0_1_0_intentions/SUPPORT_retired_seam_declarations.md`.
- **The insert stage's demo lost its surface** when the import-hook
  was dropped. It needs either the fork or a surface with no
  qualifier spelling.

---

## 5. Where things are

| What | Where |
|---|---|
| This plan | `~/Programming/PseudoIR/Planning/` |
| PseudoCoup's plan | `~/Programming/PseudoCoup_v6/Planning/` |
| PseudoCoup's previous plan, superseded but intact | `~/Programming/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/` |
| The planning framework and its renderer | `~/Programming/PlanPlan/framework/` |
| Communication protocol | `~/Programming/DevComms/LLM_communication_protocol.md` |
| Research reports (R1–R4) referenced by the plan | `~/Programming/PseudoCoup_v6/Research/` |
| This project's code, such as it is | `~/Programming/PseudoIR/pseudoir/` |
| Retired PseudoIR contents | `~/Programming/PseudoIR/archive/`, `~/Programming/0_Archive/PseudoIR/` |
| Sandbox for unattended shell runs | `~/Programming/SandboxDesign/` |

**`~/Programming/PseudoCoup_v6/AgentMemory/` currently holds material
that is more relevant to this project than to that one** — the
lineage map, the purge record, the vocabulary. It has not been split
yet. Read it, but expect the PseudoIR-relevant parts to migrate here.

---

## 6. Failures worth not repeating

- **Direction drift, 2026-07-30.** Four work requests were aimed at
  the retired backend because one planning node said "express the
  already-proven chain" without bounding what was still in scope.
  Deliveries were reviewed for "tests pass" and never for "does this
  point where the project decided to go." Review for direction, not
  only for correctness.
- **Over-deletion during the purge.** Roughly 1,900 lines of
  direction-neutral machinery were deleted to remove 16 lines that
  named the retired backend. The deletion scope was accepted without
  being measured. Measure before deleting.
- **Disk exhaustion, 2026-07-29.** Parallel agents dumping full
  ledgers over generated files filled the sandbox and killed the
  shell for a session. `/work` is now capped at 4GB tmpfs. Check
  headroom before any bulk ledger run.
- **Four parallel stores of one fact.** COREs, PROGRESS files, agent
  memory and a dashboard all restated the same facts and drifted
  apart independently. That is why this file points at the plan
  rather than summarising it.

---

## 7. Borrowing from PseudoCoup, mechanically

The plan says PseudoIR borrows PseudoCoup's toolchain. In code that is
one environment variable.

- `PSEUDOCOUP_ROOT`, defaulting to `~/Programming/PseudoCoup_v6`.
- Two modules use it today: `Tools/insert/cross_border.py` (the i64
  range, from PseudoCoup's polyfill) and `Tools/intentions/validate_form.py`
  (the parser, from PseudoCoup's ledgerer).
- Both refuse with a named error if the directory is absent, rather
  than failing with an unexplained ImportError.
- Same pattern the test suites already use for `PCV5_ROOT`.

Run PseudoIR's suite with:

    PSEUDOCOUP_ROOT=~/Programming/PseudoCoup_v6 \
        python3 -m pytest ~/Programming/PseudoIR/Tools -q
