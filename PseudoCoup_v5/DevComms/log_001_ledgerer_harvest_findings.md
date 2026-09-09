# log 001 — the ledgerer harvest: what the survey found, and the parts it names

2026-08-02, written at the owner's request while deepening
`pcv5.tools.ledgerer`. The chat response carried the conclusion; this
is the material behind it.

**What this log is for.** The next step in deepening the ledgerer node
is to produce its sub-nodes. The 2026-07-27 ledger survey already
decomposed "the most advanced ledger" into parts, each with a named
source. This log gathers that decomposition in one place, with every
source path verified against disk today, so the node-writing can work
from checked material rather than from a survey read once.

**It is a working record, not a plan and not a ruling.** Per the
communication protocol §18a: a fact here that turns out to be
load-bearing graduates into
`PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/`
or into agent memory. Nothing here settles anything.

## Sources

- `PseudoCoup_v5/DevComms/ledger_survey_2026-07-27.md`
  — the component-level survey with line citations. The primary
  source for everything below.
- `PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md`
  — its companion. Relevant here only where the two overlap.
- `PseudoCoupHQ/DevComms/log_003_harvest_reminder.md`
  — the condensed index over both, which separates what the owner said from
  what the surveys found.

---

## 1. The headline finding, and why it shapes the node list

**No single ledger system in the lineage is the most advanced one.**
The survey's §1 verdict is that two families evolved separately and
never met:

- The **semantic family** — `PseudoCoup/pseudocoup/core/ledger.py`,
  289 lines, grown from a v3 seed. It is the ONLY family that drives
  emission: eight registries consumed by `egress/dart.py` for real
  decisions (import `hide` injection, await/async gating, singleton
  rewrite, enum lowering).
  - Its recorded weaknesses: bare-name keying in two registries with
    documented last-writer-wins collisions; a spec-violating
    Dart-ingress write path that puts bare names into `types`,
    bypassing the fully-qualified name; dead `wrappers` and
    `memory_erasure` fields that nothing writes; no identity model;
    no integrity checking.
- The **verification family** —
  `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/`.
  It holds the identity model, integrity checking, divergence
  taxonomy and layout-intent schema, but records nothing any emitter
  reads. Its output is Markdown and JSON for humans, plus one
  id-stamping injector.

`ledger_unified.py` is the closest thing to a synthesis and names its
own gap in its docstring at L28–34: the exec-and-introspect
verification half was never folded into the id-keyed record.

**Why this shapes the node list.** The ledgerer is not a port of any
one system. It is a composition, and the survey has already done the
decomposition — so the parts below are the natural candidates for
sub-nodes, because each is a capability with exactly one best-in-class
source and a stated reason it wins.

---

## 2. The parts

Nine. Eight are from the survey's §4 "what a combined most-advanced
ledger takes from each"; the ninth is §3's design opportunity, which
differs from the rest in having no existing code to transplant.

Each part below gives: what it is mechanically, where it lives, why
the survey chose that source, and what condition it carries.

### 2.1 primary key — positional-path ids

- **What it is.** Every ledger entry is keyed by an id built from the
  parse position: `childIndex:nodeKind` composed along the path from
  the root. Anchors are carried as metadata and never used as keys.
  Files and directories are themselves positioned nodes.
- **Where.**
  `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/idgen.py`,
  294 lines.
- **Why this source.** The survey calls it the single
  highest-value transplant in the whole harvest, on the grounds that
  it kills two defective keying schemes at once — bare-name keying
  (which collides) and anchor keying (which moves). `check_uniqueness`
  was proved at application scale, and the ids were demonstrated
  reaching emitted output by `inject_emitid.py`.
- **Condition.** This is the part every other part depends on. The
  semantic payload is described as "re-keyed onto ids", the
  verification half joins "on id equality", and the integrity check
  asserts properties of ids. If the node order matters anywhere, it
  matters here first.
- **Connects to the settled definition.** `pcv5.tools.ledgerer`'s
  CORE already states the id as a runtime-observable signal —
  per-call-site positional-path id plus a per-instance key, emitted
  identically into every transpiled side, joined by id equality. That
  is this part, already written into the plan.

### 2.2 record shape — the superset entry

- **What it is.** One entry shape wide enough to hold what every
  family recorded:
  `{id, file, node_kind, anchor, span, ui, connectivity}`, plus a new
  `semantic` slot that does not exist in any current implementation.
- **Where.** `ledger_unified.build`, in
  `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger_unified.py`,
  323 lines.
- **Why this source.** It is already the union of the structural and
  layout records; the survey's addition is the `semantic` slot, which
  is what makes it a superset over BOTH families rather than one.
- **Condition.** The `semantic` slot is new work, not a transplant.
  Everything else in the shape exists.

### 2.3 semantic payload — the eight registries, re-keyed

- **What it is.** The registries that actually drive emission —
  `method_returns` / `suspend`, `async_required`, `symbol_owners`,
  `singletons`, `param_shapes` — moved onto positional-path ids, with
  the fully-qualified name kept as a SECONDARY index for call sites
  that only know a name.
- **Where.** `PseudoCoup/pseudocoup/core/ledger.py`,
  289 lines. WFL's copy is byte-identical.
- **Why this source.** No competitor drives emission at all. This is
  the only place where a ledger record causes an emitter to make a
  different decision.
- **Condition.** The re-keying IS the repair. Two of these registries
  are the ones with documented last-writer-wins collisions under
  bare-name keying, so moving them onto ids is not tidying — it fixes
  the defect the survey recorded against them.
- **Carried detail worth keeping.** The same file's `dump`/`load`
  maintains set and tuple round-trip fidelity, and deliberately does
  NOT serialize `async_required` — the recorded reason being that it
  goes stale on reload and is always recomputed. That is a serialization
  discipline the survey lists as best-in-class in its own right (§2).

### 2.4 keying rule — three-tier qualified names, and refusal

- **What it is.** Two things that travel together. The secondary
  index is a three-tier fully-qualified name reaching down to
  parameter scope: global, class, parameter. The posture is
  halt-on-unresolvable — ingest never guesses; it writes
  `unresolvable`, and consumers stop.
- **Where.** The schema specs at
  `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/`
  (a directory, verified present). The refusing style has a working
  implementation at
  `PseudoCoup_v5/Research/rust_routing/ledger.py`, 56 lines.
- **Why this source.** The survey's §2 marks these specs as **more
  advanced than any implementation**: no implementation reaches the
  three-tier scheme, none implements the wrapper injection/erasure
  handshake, and none enforces the halt-on-unresolvable Discipline
  Violation rule. The rust_routing ledger is called "the only
  rejecting write path and raising `type_of`" — conceptually the most
  advanced idea at the smallest scale.
- **Condition, and the one that matters for the gutting.** The
  implementation of the posture lives inside PCv5's `Research/`, which
  is exactly the material the gutting removes. It is 56 lines. If it
  is to be a source, it is harvested BEFORE the gutting or read out of
  version control afterwards under the `PCv5-archived-research`
  annotation.
- **Discrepancy, noted rather than resolved.** The survey cites this
  file as 57 lines; `wc -l` gives 56 today. One line, almost certainly
  a counting convention, recorded here only so the number is not
  quietly different later.

### 2.5 integrity — the only `--check` in the lineage

- **What it is.** A verification mode that asserts: ids are globally
  unique, every id appears exactly once, `entry_count` equals the node
  count, and a nonzero exit on failure.
- **Where.** `ledger_unified.check()`, L243–281 of
  `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger_unified.py`.
- **Why this source.** The survey states plainly it is the only
  `--check` anywhere in the lineage.
- **Condition.** The survey asks for it "verbatim, extended" with two
  invariants that do not exist yet:
  - a COVERAGE invariant — every emitted node traces back to a ledger
    id;
  - a SEMANTIC invariant — every declaration id carries either a type
    or an explicit `unresolvable` marker.
  - The second is how §2.4's posture becomes mechanically enforced
    rather than a convention someone follows.

### 2.6 divergence — one taxonomy from three vocabularies

- **What it is.** A single enumerated vocabulary for "how did the two
  sides differ", replacing three partial ones.
- **Where, and this is the part that is split three ways.**
  - In-code kinds: `classify_methods` in
    `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger.py`,
    370 lines — six kinds, counted.
  - Vocabulary breadth: the `ledger.json` sidecars under
    `0_Archive/PseudoIR/archive/experiments/` — 13
    `reason` values, including `pointer-erasure`,
    `control-flow-unroll`, `type-coercion`.
  - Confidence model: the pseudoir registry's strategy ranks and
    confirmation statuses.
- **Why three sources.** No one of them is complete: the in-code kinds
  are implemented but narrow, the sidecar vocabulary is broad but not
  executable, and the confidence model is neither — it comes from a
  different kind of store entirely (see §3 below).
- **Condition.** The merge produces a per-divergence confidence field
  carrying registry strategy and status. That is what turns a
  divergence from prose into evidence.

### 2.7 verification half — execute, introspect, compare

- **What it is.** The half `ledger_unified.py`'s docstring says was
  never folded in. Two pieces:
  - v0's exec-and-introspect: the Kotlin static side is compared
    against the Python side by importing and inspecting the transpiled
    module at runtime, with `dropped` versus `relocated` connectivity
    discrimination at L283–288 of `ledger.py`.
  - `kit_ledger`'s comparison algorithm: `_lcs` plus `_sig_match` —
    static leaves matched by content, dynamic bindings by type and
    order, robust to differing instance counts.
- **Where.**
  `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger.py`
  (370) and `.../kit_ledger.py` (374).
- **Why this source.** It is the whole of the verification family's
  contribution, and the survey's §1 verdict is that nothing else has
  it.
- **Condition.** It joins the rest **on id equality**, which is why
  §2.1 comes first. The survey notes the id-in-output half of that
  join is already demonstrated by `inject_emitid.py`.

### 2.8 layout intent — the policy/geometry boundary

- **What it is.** A record of UI layout intent in an
  absolute/relative vocabulary, target-agnostic, with nothing silently
  dropped, plus an explicit honesty boundary between what is policy
  and what is geometry.
- **Where.** `ui_ledger._norm`, in
  `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ui_ledger.py`,
  518 lines.
- **Why this source.** Sole holder; no competitor.
- **Condition.** Taken unchanged, with one addition: an explicit
  `layer` field preserving the policy-versus-geometry boundary that is
  currently maintained by convention.
- **Open question this raises, not answered by the survey.** Whether
  UI layout intent belongs in the ledgerer serving PseudoIR at all.
  This part comes from an application-transpilation lineage (Kotlin to
  Python, WFL), and `pcv5`'s stated goal is the transpilation of
  COMPILERS. It is listed here because the survey lists it; whether it
  is in scope for version 5 is a judgement the node-writing has to
  make.

### 2.9 registry linkage — the one part with no existing code

- **What it is.** A divergence entry carrying a registry `op_id` and a
  confirmation status, so that "why does this node diverge" resolves
  to a confirmed lowering with evidence, rather than to prose.
- **Where.** Nowhere. The survey marks this as inference with **no
  existing linkage found**, and notes that pseudoir itself has no
  ledger at all.
- **Why it is on the list anyway.** It is the mechanism that makes
  §2.6's confidence field mean something. Without it the field is a
  label; with it, every divergence points at executed evidence.
- **Condition.** This is design work, not harvest. It is the one part
  that cannot be scheduled as a transplant.

---

## 3. Registry is not ledger — a distinction to preserve in the node names

The survey's §3 draws a line that matters for naming, because both
things get called "the ledger" in conversation:

- A **registry** is class-level and program-independent, keyed by
  (op_id, target language). It answers: *how does this construct lower
  in that language, with what confidence and evidence.*
- A **ledger** is instance-level and per-program, keyed by identity
  and scope. It answers: *what type and shape does THIS identifier
  have in THIS program.*

The registry's epistemics are described as leading everything in the
lineage: 13 strategy ranks, 4 confirmation statuses, evidence pointers
into executed runtime results, and adversarial test vectors kept even
when rejected. That is what §2.6 and §2.9 draw on — but the registry
is not part of the ledgerer, and a sub-node named for it would put a
second thing under one name.

## 4. What is out of scope for this node

- **The runtime tracer.** `WalkEmit` and its injector
  `inject_emitid.py` are a harvest target the owner confirmed for PCv5
  (recorded in `PseudoCoupHQ/DevComms/log_003_harvest_reminder.md`
  §4), but the tracer was settled as a CO-NODE of the ledgerer on
  2026-08-01 — it is `pcv5.tools.tracer`, node `node_0_0_3_tracer`.
  (`PseudoCoup_v5/Planning/node_0_0_tools/PROGRESS.md`
  records that ruling with the word "SIBLING", which the
  communication protocol §1 bans; the term is left alone where it
  already sits and not carried forward here.)
  The ledgerer's only interest in it is that it is the demonstration
  that ids survive into emitted output, which §2.7's join depends on.
  - Hazards that come with the injector, which belong to the tracer
    node rather than here: it is not idempotent, and the per-instance
    counter drifts.
- **`StressBot/StressBot/core/ledger.py`** — confirmed
  out of scope by the survey. It is an application-state exploration
  graph with no transpilation content, sharing only the word "ledger".

---

## 5. Source inventory, verified 2026-08-02

Every path the survey names, checked against disk today. The "survey
says" column is the survey's own citation, so a mismatch is visible
rather than assumed away.

| source | survey says | on disk today |
| --- | --- | --- |
| `PseudoCoup/pseudocoup/core/ledger.py` | 289 lines | 289 |
| `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger.py` | 370 lines | 370 |
| `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/kit_ledger.py` | 374 lines | 374 |
| `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/idgen.py` | 294 lines | 294 |
| `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ui_ledger.py` | 518 lines | 518 |
| `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger_unified.py` | `check()` at L243–281 | present, 323 lines |
| `StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/inject_emitid.py` | 837 lines | 837 |
| `PseudoCoup_v5/Research/rust_routing/ledger.py` | 57 lines | **56** |
| `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/` | schema specs | directory present |

Two facts follow from the table that are worth stating rather than
leaving to be noticed:

- **Seven of the nine sources live outside the three live repos**, under
  `StressBot/RelevantProjects/PseudoCoup_v0/`,
  `PseudoCoup/`, and `0_Archive/`. The
  gutting of PCv5 does not touch any of them.
- **Exactly one source is inside the material the gutting removes** —
  the 56-line rust_routing ledger, §2.4. It is the only part of this
  harvest with a deadline attached to it.

---

## 6. The open decision, which is the owner's

The survey's §5 records the framing as settled and one question as
open.

- **Settled framing** (survey §5, superseding the three-way seed
  choice in `PseudoCoup_v5/DevComms/plan_llvm_rust_2026-07-27.md`
  §3): the combined ledger is id-keyed from v0's identity model,
  superset-shaped from `ledger_unified`, semantically loaded from the
  289-line ledger, spec-enforced by the `02_ledger` schemas, and
  refusal-postured after the PCv5 TyCtxt ledger.
- **Open, and named as the owner's:** whether to build it as its own
  component now, or grow it inside the intermediate Rust/LLVM goal.
  The survey calls this the scheduling call.
  - It bears on the node list directly. Built as its own component,
    the nine parts above are sub-nodes of `pcv5.tools.ledgerer`.
    Grown inside the Rust/LLVM goal, some of them are stages of that
    work instead, and the ledgerer node stays thinner.

## 7. How much of this to trust, and for how long

Both surveys are dated **2026-07-27**, which predates the purge and
the 2026-07-31 split. `PseudoCoupHQ/DevComms/log_003_harvest_reminder.md`
§3 states the standing caution: treat the condensed maps as a reading
list, not as current state.

- One entry in the companion transpiler map is already void — the
  automated node-to-IR derivation solvers, closed by the owner's ruling that
  probe-mining reconstructs the table whereas slicing runs the
  table-generator.
- No entry in the LEDGER map has been found void. Every source path it
  names still exists, per §5 above. That is the check this log
  performs; it is not a re-verification of the survey's line-cited
  claims about what those files do.
- The surveys carry line-cited evidence the condensed maps do not. If
  a part above is going to be acted on, the survey is where the claim
  can be checked before the code is opened.
