# 05 — Current State

As of 2026-07-28. The most volatile file; update every session.

**PURGE NOTE (2026-07-30, the owner's order — read before trusting anything
below about T3's rust ingestor or T6 selection/extraction):** those
increments were built pointing at a retired reference backend instead
of the settled LLVM/rustc-LLVM direction. All of it — the
generated-vocabulary reproduction, the support-layer ingestor, the
selection plan, the four-seam extraction chain, their tests and build
counts — was removed as mis-aimed. The narrative below is kept as a
historical record (it was true when written) but none of those
artifacts or numbers describe the current repo. See
`Planning/node_0_0_tools/PROGRESS.md` and
`Planning/node_0_0_tools/node_0_0_5_slicer/PROGRESS.md` for the
current, post-purge state.

## Where things stand

- **PCv6 founded** (this repo): commit system carried from PCv5
  (`git_commit_push.sh`, `DevComms/next_commit_message.txt`
  procedure), `create_github_repo.sh` ready for the owner to run
  (private GitHub repo; needs `chmod +x` first, sandbox could not
  set the bit), AgentMemory built. No git repo initialized yet —
  `create_github_repo.sh` does that too.
- **Planning documents** (currently in PCv5, migration pending
  the owner's call on what moves):
  - `PseudoCoup_v5/DevComms/project_plan.md` — the owner's Level 1
    (components + goals) + Level 2 expansion. THE frame.
  - `PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md` and
    `ledger_survey_2026-07-27.md` — the harvest maps.
  - `PseudoCoup_v5/DevComms/plan_llvm_rust_2026-07-27.md` — Level 3
    draft of the intermediate goal; pre-dates the component frame
    and the tree-sitter decision; needs rework before use.
  - `PseudoCoup_v5/DevComms/HANDOFF_2026-07-25.md` — the PCv5
    record (state, findings, error record, corrections).
- **Conversation model**: the original conversation is being kept
  clean — one or two more turns max, then forks. Forked
  conversations brief from AgentMemory/ + the owner's communication
  protocol, zero scrollback.

## Structure (founded 2026-07-28, the owner's ruling)

`Planning/ Research/ Tools/ Application/ DevComms/ AgentMemory/`
— READMEs in each of the first four state their change thresholds
and rules. Per-folder `.archive/` convention project-wide
(created on first use). `pseudocoup/` package comes later; repo
stays private.

**Repo live**: private GitHub repo created by the owner (2026-07-28),
remote synced with local. Commit flow: agent stages
`DevComms/next_commit_message.txt`, the owner runs
`./git_commit_push.sh`.

## Open questions

None pending from the founding. Next questions will come from
Planning/Research.

## Validation queue

- **FIRST: verify PCv5's intentions data** (the owner: best work of
  PCv5, but must be checked for context-corruption artifacts).
  `pc_verdicts.json` + the table generation
  (`Designing/build_verdicts.py`, `intention_tables_gen.py`,
  the intention/basis markdowns). Verify: regeneration
  reproducibility, internal consistency, agreement with the probe
  results (`Research/basis_audit/`), and whether dominance is in
  the data or only in prose.
- lessons: separate measured-fact from characterization in PCv5
  docs (ongoing as material migrates; provenance marked).
- (done) transpiler survey; ledger survey; **R4 runtime-ledger /
  walker / flow-graph survey**
  (`Research/r4_runtime_ledger_survey/REPORT.md`, 2026-07-28):
  found the WALKER suite in `WFL_MixingCenter/render/` — runtime
  state graphs from a driven app, cross-engine walk diffing,
  runtime→source identity bridge, mermaid/dot visualizers, and
  the unmade node-identity design decision
  (`walk_node_identity_decision.md`, direction (b): transpiler
  emits per-call-site ledger id + per-instance key on both
  sides). Consequence for T2: the ledger id must be a
  runtime-observable signal stamped into emitted output; the
  unified record gains a `runtime` slot; ledger has THREE axes
  (semantic, structural, runtime), not two.

## Planning stands (restructured 2026-07-28 to the node grammar)

`Planning/` is `node_0` under the PlanPlan framework
(`PlanPlan/framework/PROTOCOL.md` — CORE/SUPPORT/
node_<indexpath>_<description>; NODE chosen over level/branch).
Tree: `CORE_0.md` + `SUPPORT_0_dee_frame.md` (the owner's frame
verbatim) → `node_0_0_tools/` (T1–T6, one node each; T2 ledger has
depth-3 nodes schema/keying/integrity; T3 transpiler has
ingress_framework/rust_ingestor/emission) + `node_0_1_research/`
(R1/R4 done, R2/R3 queued). Old flat docs are tombstones awaiting
a host-side move to `Planning/.archive/`. Frontmatter ids are the
stable identity; node addresses may shift.

Ids normalized 2026-07-28 (the owner): single namespace rooted `pcv6.`
(tool nodes are `pcv6.tools.t2_ledger.schema` etc.). All
ledger/transpiler nodes SETTLED by the owner (schema, keying, integrity;
ingress_framework, rust_ingestor; emission = settled-deferred).

**R3 COMPLETE (2026-07-28,
`Research/r3_harvest_verification/REPORT.md`): every harvest
source healthy — zero source failures; three harness/environment
causes found and fixed in the script (v4 CLI needs pseudoir on
PYTHONPATH — real coupling the T3 fresh spine must not inherit;
pytest repo-wide collection trips scratch files; emitted-program
subprocesses need pseudoir importable). Transplant order stands.**

Sandbox: back up after app restart; provisioned with pytest +
tree-sitter 0.26.0 + python/rust/cpp grammar packages (T1
prerequisite). NOTE: sandbox provisioning is per-session — a new
session may need `pip install --break-system-packages tree-sitter
tree-sitter-python tree-sitter-rust tree-sitter-cpp pytest`.

**T1 BUILT AND GRADUATED (2026-07-28):**
`Tools/tree_sitter_base/` — parser factory (python/rust/cpp,
pip-pinned in `pins/MANIFEST.md`), deterministic census recorder
with total partition (leftover == worklist), pinned fixtures +
frozen censuses. Acceptance 12/12 in-session. Deviation flagged to
the owner: pip-pinned packages instead of the CORE's vendored-repo
pattern (same churn guard, lighter; full vendoring addable per
grammar if a pin proves insufficient).

**BUILD STATUS 2026-07-28 — stack 104 passed** (tree_sitter_base
+ ledger + transpiler + polyfill):
- T1 done (12/12). T2 phase-1 done (7/7).
- T3: ingress framework + THREE ingestors, each byte-identical to
  its PCv5 oracle at the time — a Rust generated-vocabulary ingestor
  (1071/1071, statement-level CST) and a Rust support-layer ingestor
  (both later removed as mis-aimed, 2026-07-30 — see the note at the
  top of this file), and the LLVM C++ encoder (agreement suite
  re-verified, stands). Emission still deferred.
- T4 polyfill done; **one deviation needs the owner's ruling**: MIN/-1
  wraps here, Rust panics, PCv5 refused it (see the T4 node
  PROGRESS).
- R1–R4 all complete.

**Delegation practice (proven 2026-07-28)**: heavy source reading
and tool builds go to Sonnet subagents with the plan node, the
oracle, the acceptance command, and the protocol reporting rules
in the prompt; the main context stays small and only reviews +
records. Two builds delivered this way in one turn, both green.

**BUILD STATUS 2026-07-29 — six tools, stack green.** T1 (12),
T2 phase-1 (7), T3 (framework + 3 ingestors), T4 polyfill (68,
MIN/-1 trap implemented), T5 intentions (27, slicing request
forms), T6 slicer: SELECTION built (14, persisted plan) +
EXTRACTION core built (14, routing seam executes end-to-end,
follow-the-calls live). Verified independently this session:
slicer 28/28, neighbors 131/131. Acceptance rule settled:
past-project oracles INFORM never ANCHOR — expectations written
from source/CPU-manual, execution-based results, live rustc are
the legitimate anchors.

Recorded open (marked, not faked): the generated-table stages
(a lowering table, a retired reference backend's encoders,
CheckedSRemSeq guard) are too large for the current extraction
renderer — anchors written,
awaiting execution. The execution-based semantic grid + live-rustc
diff land with the T6 INSERTION increment (next). T3 deepening
(rvalue.rs front half, assembler-scale ledger) still open.

Next: T6 insertion — transplant PCv5's output-ring mechanism
(mmap/mprotect/ctypes, proven) as a PCv6 tool; then the
executed-machine-code semantic grid closes the extraction stages.
- `Research/r1_intentions_validation/` — **R1 COMPLETE
  (2026-07-28), REPORT.md written.** Verdict: no
  context-corruption artifacts; checks 1–3 PASS (byte-identical
  regeneration, counts reconcile, 108/108 basis cells agree with
  probe ground truth); check 4 PARTIAL — the slicer-steering
  facts are prose-only: row satisfiers, canon-per-verdict,
  minimum-intention-set membership, policy links. These four
  become T5's additive work and T6's schema input.

## R5 + depth layers (Opus branch, recorded by review 2026-07-28)

R5 (`Research/r5_slice_mechanism_survey/REPORT.md`) surveyed the
PCv5 proven chain and produced the AUTOMATION BOUNDARY finding:
seam selection is human judgment; everything downstream of a
declared seam is mechanical. New ontology: "seam", "stand-in"
(glossary entries in 01). T5 gained a seam-declarations node; T6
gained selection/extraction/insertion depth nodes — all
delegation-ready with executable acceptance, status draft pending
the owner. THREE RULINGS PENDING (see 02, "Pending"): the boundary
itself; T4's MIN/-1 wrap-vs-trap; T6 plan persistence. Review
note: the Opus branch's builds conform to settled decisions and
acceptance oracles (byte-identity everywhere); its memory
discipline slipped once — R5's ontology reached Planning but not
AgentMemory until this review backfilled it.

## T5/T6 build wave (2026-07-28/29; verified by the Fable branch)

- T5 DONE: `Tools/intentions/` — pc_intentions.json (verdicts
  copied forward + satisfiers/canon/minimum-set/policy-links as
  data) + slicing request forms (the owner's term; four proven-chain
  forms, tree-sitter-validated). 27/27.
- T6 selection DONE (at the time; removed as mis-aimed 2026-07-30 —
  see the note at the top of this file): `Tools/slicer/select_slices.py`
  + persisted `plans/` (drift-as-diff observed live: a lowering
  table's Udiv arm line moved vs PCv5's comment). 14/14.
- T6 extraction CORE DONE (built in the branched Opus
  conversation; INDEPENDENTLY VERIFIED here 2026-07-29): routing
  seam end to end — emitted `extracted/routing_slice.py` matches
  the vendored num.rs arms (checked against the source directly),
  follow-the-calls observed (type_sign pulled from common.rs),
  determinism re-proven by re-extraction, expectations written
  from the Intel manual (cqto 48 99 / idiv ModRM arithmetic
  hand-checked). Slicer 28/28; all tools 131/131 (this branch's
  own runs). RECORDED OPEN: executable extraction of the lowering
  table, assembler encoders, and the CheckedSRemSeq
  guard; semantic grid + rustc diff land with insertion.
  - Note: extraction tests read the vendored UPSTREAM compiler
    sources that physically live under PCv5's tree (corpus root
    via PCV5_ROOT) — upstream source, not PCv5 artifacts; open
    point: vendor those sources into PCv6 so the archive isn't
    load-bearing.
  - One protocol fix applied in review: local variable `parent`
    renamed `enclosing` in extract_slices.py (API attributes
    remain quoted-theirs). Suite re-run green.

## Planning frontier built out (2026-07-29, Fable branch)

Deep planning added where the tree was shallow — three new level-1
nodes, all `status: draft` pending the owner, none superseding a settled
decision:
- **node_0_2_hub** — the Hub as a deliverable (intention objects
  from `canon` data; borders from the border-lattice; surface
  spelling: import-hook now, CPython fork as end state). Assembles
  after T6 insertion; first surface = PC.int64 on the inserted
  chain.
- **node_0_3_application_rust_llvm** — the intermediate goal as a
  campaign, re-derived on the component frame (supersedes the flat
  PCv5-era plan): MIR→IR front half, the ISel gap (three options,
  decide after the front half's ISD-node count is known),
  all-LLVM chain, architectures (aarch64 has NO oracle — native
  rustc only).
- **node_0_4_application_ingress** — the OTHER half, previously
  unplanned (dashboard row 5): converting the 12 languages'
  APPLICATION programs into the Hub. Reuses T1–T3, needs the
  v4/WFL application-transpiler harvest + v0's behavioral oracle.
  Independently startable (needs only T1–T3); sequencing vs the
  T6/Hub line is the owner's call, current plan holds tools-order first.
- Plus deepening CORES: T3 emission (activates downstream of Hub +
  application ingress, not the tools line), T2 ledger growth
  (slots + assembler-scale storage), rust-ingestor deepening
  (rvalue.rs front half — shared with node_0_3_0, build once).
- Key cross-cutting fact recorded: the rvalue.rs front-half work
  is SHARED between the rust-ingestor deepening and the Rust/LLVM
  application front half — one build, two consumers.

## T6 dispatch — VERIFIED GREEN 2026-07-30: 179 passed, exit 0

Run through the agent lane against the read-only `/projects` mounts.
Both increments are real: insertion mount core green, and extraction
deepening now genuinely complete — the regenerated manifest emits all
FOUR seams (routing, lowering, srem guard, encoding) with **0 stages
recorded open**. Three failures found and fixed by cause: stale
committed artifacts (regenerated), and a `cqto`/`cqto_zo` encoder-key
mismatch that had the test file disagreeing with itself. Detail in the
T6 slicer PROGRESS "VERIFIED GREEN" block. The section below is the
superseded pre-verification record, kept for the lesson.

## T6 parallel dispatch (2026-07-29) — superseded, was unverified

Dispatched two subagents in parallel on settled-plan work:
extraction-deepening (Sonnet), insertion mount core (Opus). Both
delivered files; the reviewing sandbox then went DISK-WEDGED
(bash dead, 8 consecutive failures) before any suite could be
re-run here. STATUS:
- insertion mount (`Tools/slicer/mount_bytes.py`, `cross_border.py`,
  `insertion_cache.py`, `test_insertion.py`) — likely sound: Opus
  ran to completion, self-reported 42 slicer + 173 full green,
  -7/2→-3 mounted-and-executed. Unverified by review.
- extraction deepening (`extract_lowering.py`, `extract_encoding.py`,
  `extract_srem_guard.py`) — INCOMPLETE: modules exist and each
  verified by direct execution, but full-plan regen never ran, so
  `extracted/extraction_manifest.json` is STALE (routing-only) and
  the combined suite is unconfirmed. NOT integrated.
- LESSON (recorded in node_0_0_1_3_growth): dumping ledgers over
  the generated files (a lowering table's 226k / an assembler's
  720k records) exhausted the disk — the assembler-scale storage
  problem is now live, and named-subset/lazy is a REQUIRED
  precondition for generated-file extraction, not future work,
  regardless of which compiler is being sliced.
- DELEGATION LESSON: two agents in one folder + one reviewing
  shell = the disk pressure compounded and I lost verification
  ability. Prefer ONE heavy generated-file build at a time, or
  give each its own worktree.
- RECOVERY: see the SandboxDesign entry below — the disk-wedge
  class of failure has a purpose-built answer that this session
  did not know about.

## VERIFICATION VENUE: SandboxDesign (found 2026-07-30)

`SandboxDesign/` is the owner's rootless-Podman sandbox —
the right place to run PCv6 suites, and the structural answer to
the Cowork-sandbox disk-wedge failures. Documented by the
`toolchain` skill (read it before building/testing anything in
`~/Programming`).

- It COPIES a project in (`/work` is wiped on restart and
  re-copied per run), so a heavy generated-file run cannot wedge
  a long-lived workspace the way it wedged the Cowork sandbox.
- `uv` handles deps with no PEP 668 problem; egress is
  allowlist-proxied (`./allow.sh denied` names a refused host).
- The skill records PCv6 **verified at 176 passed** in that
  sandbox on 2026-07-30 — three more than the Opus agent's
  self-reported 173, consistent with the extraction-deepening
  tests having landed and passing. That is EVIDENCE the dispatch
  work is green, but it is the skill's measurement, not this
  session's — the manifest-staleness question is separate and
  still needs the refresh run.
- Standing rule going forward: heavy or generated-file-scale runs
  go to SandboxDesign, not the Cowork sandbox. The Cowork shell
  is for light checks and file work.

**THE AGENT LANE (built 2026-07-30, the owner approved): a file write is
a sandbox run — no shell needed, no waiting on the owner.**

- Write a script to `SandboxDesign/agent/drop/x.sh`.
  The daemon watches `close_write`, so a direct write runs; no
  rename needed.
- Poll `SandboxDesign/agent/status/x.sh.status` —
  key=value, `state=running` then `state=done exit=<rc>` with
  `elapsed_s`, `log=`, `work_consumed_mb`. The path derives from
  the script name; the LOG name embeds a timestamp and cannot be
  predicted, which is why the status file exists.
- Read products from `agent/out/`, logs from `agent/logs/`.
- Scripts see `PseudoCoup_v6` and `PseudoCoup_v5`
  READ-ONLY (no copy step, originals unalterable). Products go to
  `/out` and THE SESSION places them into the real tree — the
  session is the write path, which is why read-only suffices even
  for regenerating artifacts.
- `/work` is a 4 GB tmpfs: a runaway fails with ENOSPC in the
  container instead of wedging the host disk. `/persist` is a
  named volume for opt-in cross-run state.
- Execution is SERIAL (the daemon's event loop calls run_script
  synchronously) — two dropped scripts run one after the other,
  which is deliberate: concurrent heavy runs caused the wedge.
- Ready-made suite run: copy the text of
  `SandboxDesign/agent/templates/pcv6_suite.sh` into
  `agent/drop/<name>.sh`.
- **FULLY OPERATIONAL as of 2026-07-30** (image rebuilt, quadlet
  reinstalled, both repos pushed). Status files confirmed working;
  a full suite run costs ~60s and 6 MB of the 4 GB cap. The
  `toolchain` skill was updated the same day with §1a documenting
  this lane, so a fresh session learns it from the skill.
- ONE-TIME (already done 2026-07-30), and the command matters:
  the sandbox on the owner's machine
  runs under QUADLET/systemd (`sandbox-runner.service`,
  `Linger=yes`), not `up.sh`. Quadlet unit files are COPIES living
  in `~/.config/containers/systemd/`, so editing
  `SandboxDesign/quadlet/*.container` in the repo changes nothing
  until `cd SandboxDesign && ./install_quadlet.sh`
  re-installs them (it stops units, re-copies, daemon-reloads,
  restarts). `./down.sh && ./up.sh` is the MANUAL path and fights
  systemd — under quadlet, `podman rm -f` just triggers a restart
  from the OLD unit. Diagnosing this remotely is possible because
  `./report.sh` and `./install_quadlet.sh` both write their output
  into `SandboxDesign/DevComms/`, which a session can read.

## Immediate next actions

1. the owner rules on the three remaining pending items (02 →
   "Pending": automation boundary, MIN/-1, plan persistence) —
   each now explained in plain mechanism there.
2. Then T5/T6 builds proceed against their depth nodes; T3
   deepening (rvalue.rs front half, assembler-scale ledger) stays
   open in parallel.
3. RESOLVED: the Fable original conversation holds write
   ownership; the Opus fork is read-only (the owner, 2026-07-28).
