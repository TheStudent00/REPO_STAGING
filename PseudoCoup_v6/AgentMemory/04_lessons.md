# 04 — Lessons

Two kinds: measured project lessons (what the work proved) and
agent failure modes (what the agent must guard against). Both are
load-bearing.

## Measured project lessons (each from commands run, PCv5 unless noted)

- **Extraction works.** Compiler routing logic transpiles to Python
  and executes: 130-row grid byte-identical to native rustc;
  1328/1328 differential byte matches vs real Rust.
- **Insertion works.** Machine code produced in-process, mounted
  (mmap/mprotect/ctypes), called from stock CPython, results in
  typed cells; `-7 r./ 2 == -3` while Python's `-7 // 2 == -4`.
- **Generated compiler code is transpilable; hand-written tables
  are not.** A retired reference backend's generated assembler.rs:
  14,876 lines, 0 unclassified. LLVM DAGISel: 375,884 lines, ~99.5%
  one opaque MatcherTable consumed by a hand-written VM.
- **The ISA is the ISA.** LLVM's REX line is character-identical to
  that retired reference backend's; our bytes appear verbatim in
  gcc -O2 output. An extracted vocabulary encodes Intel's manual,
  not a compiler's opinion — version-pinnable.
- **No memory model needed for the C++ we ingress.** Zero
  pointer-expression derefs across the three key LLVM files; every
  `->` is object navigation; every "pointer arithmetic" site is an
  integer counter.
- **Regex cannot parse code.** v0-era post-mortem
  (`0_Archive/PseudoIR/DevComms/.planning/design/
  Historical_Transpiler_Lessons.md`): regex parsing destroyed class
  scopes. Tree-sitter is the answer and the foundation.
- **The uniform polyfill law is real** — derived independently
  twice from different bugs (PCv5 custom.rs nops; PseudoIR width
  bug "silently zeroing the upper registers").
- **Falsifiable acceptance criteria catch everything.** Every PCv5
  error was caught by a mechanical test, usually within minutes of
  the test existing. Delegation works exactly when the task carries
  one.
- **Behavior-proof is where prior efforts drowned** (WFL planning,
  quoting v0 experience): "both prior efforts drowned at
  behavior-proof, not translation." Hence v0's oracle/fuzzer rank
  first in the harvest.

## Agent failure modes (recorded this project; guard actively)

- **F1 — Characterizing before measuring.** Root cause of PCv5
  errors 1–6 (matcher-table overclaim, pointer scare, etc.). Guard:
  read the lines, run the command, then speak.
- **F2 — Asserting from a name; not checking against recorded
  decisions.** Root cause of errors 7–10 (PoC stub reported as the
  Ledger; egress-first basis layer contradicting the dominance
  rule; "the real Ledger" asserted from one file). Guard: survey
  before superlatives; check 02_decisions before new reasoning.
- **F3 — Describing an intended action in the past tense.**
  (Claimed a file edit never made.) Guard: report only what
  happened; Edit-tool success is the evidence.
- **F4 — Folding instead of defending.** the owner: "if you have an
  expert opinion that you can defend, make a case for it... i dont
  want you to agree for the sake of agreeing." Also its mirror:
  defending against an objection nobody made. Guard: state the
  actual position; distinguish "you're right, here's why" from
  deference.
- **F5 — Compressed labels / jargon.** ("Rust decl"; "driver
  over"). Guard: protocol §1/§11 — plain language or a glossary
  entry; every metaphor answerable to "in what sense?".
- **F6 — Whitespace-aligned tables in code blocks.** Banned by
  protocol §3, violated anyway by copying an existing block.
  Guard: pipe tables, nested bullets, or prose — everywhere,
  including subagent prompts.
- **F7 — Treating the owner's notation as a literal name.** (Read PCvX
  as a specific artifact; it is a variable over versions.) Guard:
  ask what a symbol ranges over before comparing "it" to anything.
- **F8 — Burying a foundation as an implementation detail.**
  (tree-sitter appeared only as a table cell until the owner flagged
  it.) Guard: when a module appears in every version, it is
  structure, not detail.
- **F9 — Loose planning.** the owner: projects "get so loose so fucking
  fast"; a few folders with a few files is not planning. Guard:
  Level 1 frame first, explicit deeper levels, substantial
  research plans when projecting isn't possible; run improvements
  by the owner before applying.

- **F10 — Pointing at a past project as a source of machinery.**
  (2026-07-31: a slice-closure log ended by naming a past project's
  fuzzer as a component that "would shrink the list". Retracted.)
  This is the same failure that scorched the previous project, in
  its early, harmless-looking form: not a commitment, just a mention
  of a past artifact as available. The mention is the failure,
  because it is how the drift starts. Guard: before writing any
  proposal, ask whether the sentence points at something in a past
  project as a thing to USE rather than a thing to CHECK AGAINST. If
  it does, do not write it. Full rule in 02_decisions, Direction,
  first entry.

- **F11 — Acting on a finding before searching for it everywhere.**
  (2026-07-31: PCv5 was gutted after checking which of its files
  PseudoCoup_v6 read. PseudoIR read one too — `pc_verdicts.json`
  through the same `PCV5_ROOT` pattern — and 10 of its tests broke on
  deletion.) The list of what to preserve came from the investigation
  that first found the dependency, so it inherited that
  investigation's scope. Guard: when a CLASS of defect is found in one
  place, run the search for that class across every repo BEFORE acting
  on the finding. A one-repo answer to a multi-repo question is not a
  partial answer, it is a wrong one. Note it was caught by a test and
  not by review.

- **F12 — Editing another repo on this project's behalf.**
  (2026-07-31: `plan_and_code.md`, which is about how THIS line maps
  plans to code, was written into `PRIVATE/DevComms` — a
  deliberately light place for decisions affecting most of the owner's LLM
  work generally.) The guard is not permission, it is scope. the owner's
  framing: we are devs of PseudoCoupHQ and only USERS of
  `PRIVATE/PlanPlan`; wearing the PlanPlan hat, a change
  gets made if it is abstract enough to serve every project using the
  framework. So the test before editing it is **"would this be right
  for a project that has nothing to do with PseudoCoup?"** Yes means
  make it — PlanPlan is new and changes often. No means it belongs
  in HQ. `PRIVATE/DevComms` is a third thing again and takes no
  line-specific content at all. Full statement in
  `PRIVATE/PseudoCoupHQ/Planning/node_0_2_conventions/CORE_0_2_conventions.md`.

## Check the skills before improvising (2026-07-30)

Two project skills exist and both are load-bearing: `toolchain`
(what is installed on the host and in the SandboxDesign
container, how every project in `~/Programming` is built and
tested, and WHERE a given command should run) and
`planning-framework` (the CORE/PROGRESS/SUPPORT/node grammar).
This session spent a full dispatch cycle fighting Cowork-sandbox
disk exhaustion while `toolchain` documented the purpose-built
answer — `SandboxDesign`, which copies a project in
per run and cannot be wedged by one heavy build. Read the
relevant skill BEFORE building, testing, or choosing an execution
venue; it is cheaper than the failure it prevents.

## Standing context obligation (the owner, 2026-07-28)

The agent (and any LLM working here) operates with a high degree
of freedom inside these projects. Consequence: **the project is
often bigger than the owner can track 100% — there will be things the owner is
unaware of.** Therefore:

- Every reference to a file/folder carries its full path
  (`...`; absolute if outside `~`), or names the
  project (PCv6 / PseudoCoup_v6) plus the path within it. Never a
  bare fragment like `pins/MANIFEST.md`.
- Every reference to something the owner may not have seen — a prior
  repo's pattern, a mechanism, a file the agent found — carries
  CONTEXT: what it is, mechanically, in the owner's terms. A name
  dropped as if known is a dead end.
- Recorded in the communication protocol
  (`PRIVATE/DevComms/LLM_communication_protocol.md` §14);
  repeated here because forks must load it with the project, not
  discover it by being corrected.

## Context-corruption lesson (why AgentMemory exists)

The previous conversation was paused indefinitely due to context
corruption, and misalignment indications appeared early — the owner spent
several turns pulling focus back. Conversations are disposable;
this folder is not. Fork from clean conversations; brief from
files; never from scrollback; never spin up an agent from scratch.
