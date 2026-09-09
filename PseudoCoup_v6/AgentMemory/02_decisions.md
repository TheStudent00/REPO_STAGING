# 02 — Settled Decisions

Every entry: the decision, who, why. New reasoning MUST be checked
against this file before being asserted — contradicting a recorded
decision without noticing is a logged failure mode (04, F2).

## Direction

- **NOTHING IS BUILT ON A PAST PROJECT. EVER.** (the owner, 2026-07-31,
  hardening the 2026-07-28 "inform never anchor" rule below.)
  - the owner, verbatim: "past project oracles are for verify correctness.
    they absolutely will not be used to develop things around ...
    dont ever suggest the use of past projects to build dependencies
    on ever again."
  - The permitted use is ONE: check a result AGAINST a past project's
    oracle to see whether the result is correct. That is the whole
    of it.
  - Forbidden: naming a past project's code as a component, a
    starting point, a library, a source of machinery, or a thing to
    harvest INTO a build. Forbidden whether or not the past project
    is named, and whether or not the wording is hedged with
    "unexamined" or "could inform" — the failure mode is the
    SUGGESTION, not the commitment.
  - **Why this is absolute**: the previous project was scorched over
    exactly this. Work drifted onto a retired backend because it kept
    being cited as a resource, and the drift was not visible until 34
    files had to be deleted. The cost of one more instance is not
    another scorched project.
  - Guard, applied before writing any proposal: does this sentence
    point at something in a past project as a thing to USE? If yes,
    it does not get written. Judge by what the sentence points at,
    not by whether a name appears in it.
  - This supersedes the softer statement of the same idea recorded
    under "Intentions and slicing requests" below ("Past-project
    oracles INFORM, never ANCHOR"), which remains accurate about
    acceptance tests and is not the whole rule.
  - **HARVESTING IS NOT THIS, and the line is testable.** the owner,
    2026-07-31: "PCv5 Frankenstein parts can be from anywhere."
    Composing a tool from best-in-class components across the
    lineage is the settled method (see "built by COMPOSITION" and
    "mine, don't resurrect" below). The difference:
    - a TRANSPLANT moves code in, with a provenance header and its
      own acceptance test, after which the source repo is irrelevant
      to whether it runs;
    - a DEPENDENCY leaves the code where it is and reaches for it.
    - **The test: after the harvest, could the source repo be
      deleted without anything breaking?** Yes means transplant.
      No means dependency, which is banned.
    - One live violation by that test, predating the ruling: PCv6's
      suite needs PCv5 on disk, six tests resolving vendored rustc
      source through `PCV5_ROOT`. Already queued to fix by vendoring
      those sources in.

- **PCv5 is gutted and rebuilt as the Frankenstein precursor to
  PCv6** (the owner, 2026-07-31). PseudoCoup_v5 stops being a preserved
  research tree and is commandeered: all the PseudoCoup research is
  gathered and composed ("Frankensteined") into a transpiler and a
  ledgerer, and THAT becomes version 5. PseudoIR then uses those two
  tools — which is the answer to PseudoIR's open question of whether
  it needs a transpiler of its own.
  - **Why gutting is safe**: the research is in version control.
    the owner: "the VCS tracks the research. we can safely commandeer it."
    Deleting from the working tree does not delete the record.
  - **Existing references to PCv5 are ANNOTATED, not deleted.** A
    reference to pre-gutting PCv5 material is marked
    `PCv5-archived-research` (glossary entry in 01), meaning: exists
    in VCS, not in the current tree. Removal is optional; annotation
    is what is required.
  - This SUPERSEDES the 2026-07-28 decision below without erasing
    it, per the standing rule that a fallen position keeps its record
    and its reason.
- ~~**PCv6 is the build; PCv5 is archived research** (the owner,
  2026-07-28). PCv5 was the experimental stage proving the
  mechanism; its structure is not carried, its lessons and oracle
  assets are.~~ **SUPERSEDED 2026-07-31** by the gutting decision
  above. It fell because "archived" was a weaker use of the repo than
  it could carry: the research it holds is the parts list for the
  Frankensteins, and VCS makes preserving the tree unnecessary for
  keeping the research.
  - **Load-bearing consequence, measured this session (2026-07-31,
    unresolved)**: PCv6's own suite does not pass without PCv5 on
    disk. `python3 -m pytest Tools -q` in PseudoCoup_v6 gives 6
    errors resolving
    `PseudoCoup_v5/Research/rust_routing/sources/rust/compiler/rustc_codegen_llvm/src/declare.rs`
    via `PCV5_ROOT`, and 95 passed once `PCV5_ROOT` is set. That path
    is VENDORED UPSTREAM RUSTC SOURCE that happens to live under
    PCv5's tree — not a PCv5 artifact. 05_state.md already recorded
    the open point ("vendor those sources into PCv6 so the archive
    isn't load-bearing"); the gutting decision makes it a
    precondition rather than a cleanup. Files reading PCV5_ROOT:
    `Tools/ledgerer/test_ledger.py`, `Tools/transpiler/render_cpp.py`,
    `Tools/transpiler/test_llvm_encoder.py`,
    `Tools/polyfill/wrap_fixed_width.py`,
    `Research/r2_compiler_source_census/census_sources.py`, plus the
    R1/R3 `run_checks.sh` scripts.
- **Rust (LLVM) first** — the intermediate goal (the owner, 2026-07-25).
  Rust's intentions are the most dominant (rows A/C/D/G).
- **LLVM x86-64 before any other architecture** (the owner, 2026-07-26).
  A retired reference backend's generated-vocabulary oracle was
  x86-64-only, so x86-64 was the one architecture where every
  LLVM-derived piece was byte-checkable against an independent
  extraction. aarch64 only after the chain stands. (See the
  2026-07-30 entry below: that oracle itself was later purged.)
- **A retired reference backend is retired to oracle status**
  (the owner, 2026-07-25). Proof of concept and verification reference;
  not a forward path. Its generated-vocabulary artifact was to stay
  live as the frozen, version-pinned x86-64 oracle.
- **PURGE: the retired reference backend removed entirely, oracle
  role included** (the owner, 2026-07-30). The 2026-07-25 ruling above
  kept it on as a verification-only oracle; a drift occurred where
  forward work got built pointing AT that backend (a rust ingestor
  reproducing its generated vocabulary, a support-layer ingestor,
  the T6 selection/extraction chain) instead of at LLVM/rustc-LLVM,
  the settled direction. All of it — code, tests, plan claims,
  the oracle role itself — is purged from PCv6. The oracle relation
  described in the two entries above no longer holds; LLVM-derived
  stages are now checked directly against native rustc/LLVM ground
  truth. This entry supersedes the oracle status of the two entries
  above without erasing that they were once true.

## Architecture & method

- **tree-sitter is the parsing foundation, no exceptions without
  extraordinary proof** (the owner, 2026-07-28). Mature, exceptionally
  reliable; any argument against it must be more powerful than
  tree-sitter itself. The PCv5 bespoke parsers are archived
  expedience. (Agent searched for the counter-argument and
  concluded none exists; census+assert discipline transfers onto
  tree-sitter trees.)
- **The hub dominates intentions; shortfalls are recorded, not
  designed around** (the owner, 2026-07-27). The basis layer is NOT
  defined by what target languages can supply — that inversion was
  an error, twice. Performance-primitive completeness dissolved
  under this rule.
- **Uniform polyfill wrapping, no exemptions** (the owner, PCv5). Mixed
  depth makes an unwrapped node ambiguous between "proven safe"
  and "tool missed it". Independently derived twice (PCv5;
  PseudoIR compiler_transpilation_experiment.md).
- **Stubs carry reachability invariants, asserted at the site**
  (PCv5 standing rule).
- **Emitted artifacts are the stability layer**: deterministic,
  no timestamps, provenance headers; regeneration byte-identical
  (the owner, PCv5). Emit .py files, whole vocabulary, generated output
  not meta-generator.
- **Measure, do not estimate.** Every number comes from a command
  run. A policy is formal when a runnable artifact could falsify
  it. (PCv5 standing rules, carried forward.)
- **The most advanced transpiler/ledger are built by COMPOSITION**
  from best-in-class components across versions (the owner, 2026-07-28
  direction; harvest maps in 03). Precedent: WFL's "Mine, don't
  resurrect."

## Intentions and slicing requests (the owner, 2026-07-28)

- **Intentions data is largely made BY HAND.** Evaluating
  intentions is exceptionally high-level work — at least
  human-level intelligence. No pretense of automating it.
- **The realistic mechanism is a SLICING REQUEST FORM** (the owner's
  term): human+LLM analysis fills a formalized, validatable form
  against the hand-made intentions data; the slicer consumes the
  form. Formalizing the process is what makes it easy.
- Future outlook (not scheduled): an interface presenting a
  searchable/selectable menu of operators/data-structures, and
  possibly interfacing with the UR-AST directly, could fill forms
  interactively. Meanwhile: forms filled by hand+LLM.
- The seam declaration is the core CONTENT of a form; "slicing
  request form" is the artifact's name.
- **Follow-the-calls rule (the owner, 2026-07-28)** — for COMPILER
  transpiling: if sliced code calls something resolvable in the
  compiler source we have (any module/operator/function), that
  callee is TRANSPILED+SLICED TOO, across files, under a generous
  configurable depth limit; hitting the limit emits a loud
  TRUNCATION WARNING, and a human decides whether the truncated
  callee becomes a wrapper. Evidence it was already true by hand:
  PCv5 transpiled `type_sign`'s definition from outside num.rs.
- **Script vs compiler transpiling differ**: application-script
  transpiling does NOT chase imported modules (often logically
  and/or legally impossible) — the wrapper-registry / Map-Wrap-Fail
  lineage governs there.
- **stand-in ≡ transpiling-wrapper at a slice boundary**: every
  stand-in is a human-ruled wrapper point — pre-declared in the
  form (known infrastructure like TyCtxt, where following would
  drag in half the compiler) or created at a truncation warning.
  Both terms glossaried; collapse to one word is the owner's call.
- **Field names settled (the owner, 2026-07-28)**: `row_satisfiers`,
  `canon`, `minimum_set`, `policy_refs` confirmed as-is.
- **Past-project oracles INFORM, never ANCHOR (the owner, 2026-07-28)**:
  no acceptance test may depend on a past project's artifacts
  (PCv5 included). Legitimate anchors: expectations written from
  the compiler source / CPU manual, execution-based semantic
  results, and the live source compiler itself (rustc — an
  inherent dependency, since it is what we slice). Past artifacts
  may be consulted during development as reference only.
  (Note: earlier T3 acceptances used PCv5 byte-identity — those
  verified the REPLACEMENT of PCv5 tooling specifically and
  stand as historical; the rule governs everything forward.)
  Clarification (the owner): this is not PCv5-avoidance. Verifiably good
  past tools (oracles especially) are used freely; the rule only
  forbids DEPENDENCE in the pass/fail path.
- **Compiler test suites as a future oracle (the owner, 2026-07-28,
  noted not scheduled)**: a compiler ships tests written by its
  authors — intent statements. Extracting a slice's relevant test
  and transpiling it too gives that slice a native-born hub test
  (compare Rust-original vs hub-transpiled against the authors'
  own checks). Recorded in the extraction CORE's "Future
  resource"; revisit when manual-derived expectations feel thin.

## Transpiler + ledger upgrade design (the owner-aligned, 2026-07-28)

- **T3 fresh spine, mining the lineage** — no wholesale port of
  any version-base; components transplant with provenance headers
  and acceptance tests (precedent: WFL "mine, don't resurrect").
- **T3 first milestone: ingress only** (Rust→hub); acceptance was
  reproducing an earlier generated-vocabulary artifact byte-for-byte
  + the 1328/1328 differential (that milestone was later removed as
  mis-aimed, 2026-07-30 — see Direction above). Emission later.
- **Coverage gate and gate-before-emit are framework features**,
  not add-ons.
- **T2 one-record ledger schema** across THREE axes (semantic,
  structural, runtime) — not separate ledgers joined later.
- **T2 keying: ledger id is a runtime-observable signal** —
  direction (b) of `walk_node_identity_decision.md`: per-call-site
  id (idgen positional path) + per-instance key, emitted
  identically into every transpiled side, joins by id equality.
  Coordinate/anchor joins rejected on recorded evidence (R4).
- **Refusal at consumption**: ingest records `unresolvable`
  honestly; consumers (emitter/slicer) halt on it. Softens the
  02_ledger spec's halt location, keeps the principle.
- **T2 ships minimal core first** (identity+span+type+integrity),
  grows additively as T3 demands.
- **Walker-class runtime instruments are Application-phase**, but
  the `runtime` slot and id-emission contract are fixed in T2 now
  so they join later without rekeying.

## Vocabulary

- "target language" (one of the 12) vs "architecture" (instruction
  set); egress/ingress are directions relative to a perspective,
  never categories; slice=extracted, stub=excluded (the owner,
  2026-07-27/28). See 01.

## Planning framework (the owner, 2026-07-28)

- **PlanPlan** (`PlanPlan/`, private repo):
  the owner's research into ontology evolution in project development;
  hosts the planning framework as a template. Plans carry prose +
  YAML frontmatter metadata (stable dotted ids, status,
  supersedes-chains) so planning instances are extractable and
  VCS-analyzable.
- **Framework protocol** (draft, the owner settles):
  `PlanPlan/framework/PROTOCOL.md` — the CORE/SUPPORT/level
  grammar (the owner, 2026-07-28): each folder holds exactly ONE CORE
  markdown describing its branch at its level, any SUPPORT files
  (any type), and level-N+1 sub-folders named
  `level_<indexpath>_<description>`; index chain = address
  (positional-path, same design as idgen ids), frontmatter id =
  identity. Completeness rule (nothing essential only at a lower
  level); higher levels govern lower levels, corrections go
  high-first; plain relative markdown links, no wikilinks.
  ("MASTER" renamed to CORE.)
- **PROGRESS.md per node** (the owner, 2026-07-28): every node folder
  carries a living `PROGRESS.md` — item statuses (planned /
  in-progress / done / blocked / deferred) with dates and evidence
  links, updated at the moment progress happens. CORE says what
  the branch IS; PROGRESS says where its implementation STANDS.
  Implemented across all 12 PCv6 nodes same day.
- **PCv6 `Planning/` restructures to conform** once the protocol
  settles; the ledger/transpiler detail layer is written under it.
- **Viewing tool: SilverBullet** (open source; the owner may also use
  VS Code/Antigravity). Install script in `framework/`.
- **Terminology (protocol §1, extended 2026-07-28)**: ALL
  socio-familial constructs banned for object relationships, not
  just parent-child. Replacement lexicon: super/sub +
  higher/lower; children→sub-nodes/sub-objects; siblings→
  co-nodes/co-objects; ancestors→super-chain; descendants→
  sub-tree; orphaned→unlinked/detached; adopt→conform;
  inherit (our designs)→derive/extend. Botanical terms fine
  (root, leaf, branch, prune). Third-party familial terms quoted
  as theirs, never carried into our prose.

## Workflow

- **Commit system** (the owner+agent, PCv5, carried to PCv6): sandbox
  writes `DevComms/next_commit_message.txt`; the owner runs
  `./git_commit_push.sh` on the host (sandbox cannot push; script
  clears stale sandbox git locks). One-time repo creation:
  `./create_github_repo.sh` (private GitHub repo via gh).
- **Conversation hygiene** (the owner, 2026-07-28): the original
  conversation is kept clean and forked from; all project state
  lives in files (AgentMemory + DevComms), never chat-only; bulk
  reading is delegated to survey subagents so the main context
  stays small. Never spin up a fresh agent from scratch — brief it
  from AgentMemory.
- **Planning discipline** (the owner, 2026-07-28): Level 1 (high level)
  first, then explicitly deeper levels in separate document areas;
  research-based planning is acceptable when projection isn't
  possible, but must be substantial. Improvements to the owner's drafts
  are proposed in conversation BEFORE being applied.
- **Decision split** (the owner's protocol §6): the owner decides architecture,
  ontology, naming, structure; agent decides mechanical execution
  details; when unsure, ask — one turn is cheaper than a redo.

## Structure & organization (the owner, 2026-07-28)

- **PCv6 directory structure**: `Planning/`, `Research/`, `Tools/`,
  `Application/` (agent-recommended co-folder of Tools, pending the owner's
  confirm), `DevComms/`, `AgentMemory/`, top-level `.archive/`;
  `pseudocoup/` package later, when nearing production shape. PCv6
  stays PRIVATE — strictly for our own benefit.
- **Per-folder `.archive/` convention**: every folder keeps old
  files/folders in a local `.archive/` (created on first use) —
  tidy but accessible. Truly dead material is deleted; VCS
  remembers.
- **Change thresholds**: Tools HIGH (no litter); Planning moderate
  (Research informs course-corrections); Research flexible but
  contained (nested subfolders, no loose files).
- **Generalize then specialize** (the owner): tree-sitter handling, the
  ledger, and most transpiler machinery overlap massively across
  languages — generalize what we can, specialize where a language
  demands it. This is the automation goal expressed as design.
- **Ledger is an independent tool** (the owner): PseudoCoup is a module
  of tools; centralized control over the tools will come later —
  "hopefully ontology will reveal itself." Keep tools independent
  until it does.
- **Tools first** (the owner): initial PCv6 work is constructing the
  tools; PCv5 gave a glimpse of what's ahead and informed the tool
  updates needed.
- **PCv5 migration**: migrate whatever makes sense — better safe
  than sorry — and every migrated item clearly marks its
  provenance (which repo/file it came from). PCv5 itself is left
  in place on the owner's system. Caution: much of PCv5 was misaligned
  with the project spirit; migrated content is reference, not
  gospel.
- **No vocabulary sweep of PCv5** (the owner): PCv5's strength was not
  communication; don't retrofit it. Settled vocabulary (01) applies
  to everything new.
- **PCv5's intentions data needs verification before reliance**
  (the owner): the tables and `pc_verdicts.json` are some of the best
  PCv5 work, BUT must be checked for context-corruption artifacts
  before anything builds on them. Early Research task.

## Pending the owner's ruling (as of the 2026-07-28 review)

- **The automation boundary — RESOLVED by the owner's churn-resilience
  framing (2026-07-28, level-0 note in
  `PseudoCoup_v6/Planning/CORE_0.md`)**: the goal is
  a MOSTLY automated transpile+slice+insert system whose purpose
  is keeping the repo current when the intention-landscape or the
  source compilers churn. Human seam declarations fit inside
  "mostly": compiler-version churn lands BELOW existing seams
  (mechanical re-slice); intention-landscape changes may need new
  seams (rare, human). Extraction precision is a dial:
  imprecise-but-safe (cut generously + asserted stubs) is the
  default; minimal slicing optional (the owner's precision point).
- **T4 MIN/-1 — RESOLVED (the owner, 2026-07-28): TRAP. IMPLEMENTED
  same day.** `MIN / -1` and `MIN % -1` raise `OverflowError` in
  `PseudoCoup_v6/Tools/polyfill/wrap_fixed_width.py`
  (real Rust panics on both; remainder inclusion is the agent's
  mechanical extension — PCv5's srem(MIN,-1)=0 was a retired
  reference backend's machine-level guard, not Rust surface
  semantics). Full stack re-verified: 104 passed (that count
  included increments later removed as mis-aimed, 2026-07-30).
- **T6 selection plans — RESOLVED (the owner, 2026-07-28): PERSISTED.**
  The slicer's slice plan (which regions, which branches survive
  the filter, which stand-ins) is written to a committed file —
  reviewable before extraction runs; compiler-source drift shows
  as a plan diff.
- ~~Branch ownership~~ **RESOLVED (the owner, 2026-07-28)**: the Fable
  original conversation is the most advanced project intelligence
  and holds WRITE OWNERSHIP of this repo; the Opus fork is
  read-only until the owner says otherwise.

## Resolved 2026-07-28 (the owner)

- **`Application/` is a top-level folder.** Tools' high threshold
  would otherwise force application churn into Tools. First
  application: Rust (LLVM).
- **Oracle standing rule**: every tool ships with its own
  acceptance test; oracle assets live in Tools next to the tool
  they check. Not a component.
- **The "IR question" is closed — probe-mining is superseded.**
  PseudoIR v3/v4's opcode probe-mining predates the owner's decision
  that transpiling the compiler and slicing is how
  lowering-to-IR and lowering-to-arch logic gets inserted into the
  hub. Mining reconstructs the table; slicing runs the
  table-generator — the project's founding insight. UR-AST does
  the transpiler's heavy lifting; the mining line is archived
  history, not a current tool. (The survey's listing of the
  solvers as harvest candidates was an F2 instance: capability
  noted without checking against the recorded decision.)
