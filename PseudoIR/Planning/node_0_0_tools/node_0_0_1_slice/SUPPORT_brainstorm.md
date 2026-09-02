---
id: pir.slice.support.brainstorm
status: draft
---

# SUPPORT — brainstorm

the owner's idea for automating slicing, stated 2026-07-31. Captured here
unsettled: this file records the idea and what it connects to, and
does not decide anything.

Everything in "the idea" below is the owner's. Everything under "what this
already connects to" is drafted by Claude from recorded decisions,
with the lines cited so the connection can be checked rather than
taken.

---

## The idea

Stated by the owner, 2026-07-31:

> the ledgerer is meant to have a detailed flow graph. but it lacks
> the ability to track live runtime connections.
>
> i want to develop a UR-AST node detection system that uses the
> ledgerer to map detectors into nodes. it is what we will use to
> automate slicing. we will need an understanding of a language
> compiler test suite in order to extract the test suite modules that
> represent what we want to slice out of the transpiler-compiler.
>
> when we run that test suite module(s), we will track the detected
> node activations and generate a live flow graph of the UR-AST. and
> that will give us the slice we want.

### The chain, in order

1. **The ledgerer records the compiler's structure.** It already
   produces a flow graph over the transpiled compiler's UR-AST. What
   it does not produce is any record of which of those nodes actually
   run.
2. **Detectors are mapped into nodes.** The ledgerer, which already
   holds an id per node, is what places a detector at a node — so a
   detector is addressed by ledger id rather than by position in a
   file.
3. **A compiler's own test suite supplies the driver.** Rather than
   writing a program that exercises the semantics we want, we find
   the modules of the source compiler's test suite that exercise
   them. This requires understanding that test suite well enough to
   say which modules correspond to which intentions.
4. **Running those test modules activates nodes.** Each detector that
   fires records that its node was reached, under that test.
5. **The activations are assembled into a live flow graph** — the
   sub-set of the UR-AST that actually executed, with the order and
   connections observed rather than inferred.
6. **That graph is the slice.** The part of the compiler the test
   suite drove is, by construction, the part that implements what the
   test suite tests.

### What is attractive about it

- The slice is **observed, not judged**. The current design has a
  human declare a seam and derive everything downstream of it
  mechanically. This proposal replaces the judgment with a
  measurement.
- The test suite is **written by the compiler's own authors**, so the
  question "does this test exercise the semantics we mean" is
  answered by people who knew the compiler, not by us reading it.
- It produces a slice with a **ready-made acceptance test**: the same
  test module that selected the slice can check it.

---

## Terms used above

These four are the owner's words. The definitions are Claude's reading of
them and are the first thing to confirm or correct — if a definition
below is wrong, everything reasoned from it is wrong too.

```
detector
    an instrument attached to one UR-AST node that records when
    execution reaches that node. placed by ledger id, so it survives
    the file moving or the line numbers shifting.
    example tied to context:
        a detector on the UR-AST node for rustc's integer-division
        routing arm fires whenever a transpiled test drives an
        integer division through it.

activation
    one detector firing: the record that its node was reached during
    a particular run. the raw observation the live flow graph is
    assembled from.
    example tied to context:
        running rustc's own division tests produces activations on
        the routing arm, on the type_sign call it makes, and on
        nothing in the float paths.

live flow graph
    the sub-set of the UR-AST that actually executed in a run, with
    the connections between nodes as observed rather than as read out
    of the source. "live" distinguishes it from the ledgerer's
    existing structural flow graph, which is derived from the code
    without running it.
    example tied to context:
        the structural graph shows every arm of a routing match; the
        live graph from the division tests shows only the arms those
        tests took.

test suite module
    the unit of a source compiler's own test suite that we select
    because it exercises an intention we want sliced. the driver, not
    the oracle — though it can be both.
    example tied to context:
        whichever file in rustc's test tree drives signed integer
        division to its edge cases, including MIN / -1.
```

---

## Prior art: this was already built once, in Kotlin

the owner recalled a global function object called from inside nodes with
their ids. It exists. Found 2026-07-31; it is not in
`<WORKSPACE_DIR>/WFL_Projects/` but under
`<WORKSPACE_DIR>/StressBot/RelevantProjects/`.

**`WalkEmit`** — a Kotlin `object`, which is to say a literal global
singleton — at
`<WORKSPACE_DIR>/StressBot/RelevantProjects/WFL_MixingCenter/WFL/app/src/main/java/com/sara/workoutforlife/core/debug/WalkEmit.kt`.

The call-site surface takes ONE argument, the id:

```kotlin
fun emitId(id: String)                              // line 79
fun tag(id: String): String                         // line 120, returns "$id#$instanceIndex"
fun interface Sink { fun onEmit(id: String, instanceIndex: Int) }   // lines 43-44
```

- **The second argument the owner half-remembered is `instanceIndex: Int`.**
  It is not passed IN at the call site — `WalkEmit` computes it, by
  bumping a per-id counter under a lock, and passes it OUT to the
  installed sink. So a node supplies its identity and the global
  supplies how many times that identity has fired this run.
- **The id is an idgen positional path** — the same id design the T2
  ledger keying decision adopted. Generated by
  `<WORKSPACE_DIR>/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/idgen.py`,
  proven globally unique (11,698 nodes, 11,698 distinct ids for one
  source folder).
- **The calls are INSERTED, not hand-written**, by
  `<WORKSPACE_DIR>/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/inject_emitid.py`
  (837 lines, tree-sitter driven). One run injected 928 calls across
  86 files.
- **With no sink installed it does nothing observable** — one map
  bump, no I/O. That is how the instrument ships inside production
  code without dragging a test dependency into it.
- **It builds a graph.** Activations land as the `walk_id` field on
  each edge of a walk graph JSON, consumed by `render/walker.py`,
  `render/walk_diff.py`, `render/identity.py`.
- **A transpiled Python mirror of the same global exists** at
  `<WORKSPACE_DIR>/StressBot/RelevantProjects/WFL_MixingCenter/core/debug/WalkEmit.py`,
  which is what let the two engines' walks be diffed against each
  other.
- Written up in that repo's own DevComms logs, fullest account in
  `<WORKSPACE_DIR>/StressBot/RelevantProjects/WFL_MixingCenter/DevComms/log_139_walktag_broadening.md`.

### Two hazards this proposal inherits

Both were found the hard way there and are recorded in that code.

- **The injector is not idempotent.** Running it twice over a file
  double-injects. Documented in `inject_emitid.py` itself. Any
  detector-placing step here needs an answer to "what happens when it
  runs again", and the project's standing rule that emitted artifacts
  regenerate byte-identically is the obvious form of that answer.
- **A per-instance counter drifts.** `WalkEmit.kt` lines 136-148
  record a case where the same call site was `baseId#3` when recorded
  and `baseId#37` when replayed, because the counter counted
  recompositions. The fix was to stamp the BASE id only and re-derive
  the instance by rank in enumeration order. Any per-instance keying
  in this proposal walks into the same problem.

Whether this transplants or only informs is unexamined. Note that the
project rule is that past-project artifacts inform and never anchor
an acceptance test — so this is a design reference, not an oracle.

---

## What this already connects to

Two recorded decisions feed this proposal directly. Neither was made
with this proposal in view, which is why the fit is worth noting
rather than assuming.

- **The ledger already has a runtime axis, decided for exactly this
  kind of use.**
  `<WORKSPACE_DIR>/PseudoCoup_v6/AgentMemory/02_decisions.md` lines
  174–180: "T2 one-record ledger schema across THREE axes (semantic,
  structural, runtime) — not separate ledgers joined later" and "T2
  keying: ledger id is a runtime-observable signal ... per-call-site
  id (idgen positional path) + per-instance key, emitted identically
  into every transpiled side, joins by id equality."
  - Read against this proposal: the `runtime` slot is where an
    activation would live, and "ledger id is a runtime-observable
    signal" is precisely the property that lets a detector report
    against a node identity rather than a source position.
  - The same file records that coordinate and anchor joins were
    REJECTED on evidence from the R4 survey
    (`<WORKSPACE_DIR>/PseudoCoup_v6/Research/r4_runtime_ledger_survey/REPORT.md`).
    So the id-join is not a free choice to revisit.
  - `<WORKSPACE_DIR>/PseudoCoup_v6/AgentMemory/05_state.md` lines 81–84
    states the consequence in the same terms: "the ledger id must be
    a runtime-observable signal stamped into emitted output; the
    unified record gains a `runtime` slot".

- **Using a compiler's own test suite was already recorded, as an
  oracle rather than as a driver.**
  `<WORKSPACE_DIR>/PseudoCoup_v6/AgentMemory/02_decisions.md` lines
  155–161: "a compiler ships tests written by its authors — intent
  statements. Extracting a slice's relevant test and transpiling it
  too gives that slice a native-born hub test ... revisit when
  manual-derived expectations feel thin."
  - The difference this proposal makes: there, the test checks a
    slice we already cut. Here, the test SELECTS the slice. Same
    asset, promoted from checking the answer to producing it.
  - The 2026-07-28 note says "noted not scheduled". This proposal is
    the reason to schedule it.

- **R4 found runtime-observation machinery that already exists in the
  lineage.** `05_state.md` records the WALKER suite in
  `WFL_MixingCenter/render/` — "runtime state graphs from a driven
  app, cross-engine walk diffing, runtime→source identity bridge".
  That is a prior implementation of "observe a running program and
  join what you saw back to source identity", which is the mechanical
  core of this proposal. Whether it transplants or only informs is
  unexamined.

---

## Open questions

Recorded as questions, not answered here.

- **Does an activation-derived slice CLOSE?** A test suite drives the
  paths the tests take. Code the tests never reach is not in the live
  graph — including error paths, rare arms, and anything the authors
  under-tested. A slice that is missing an arm is wrong in a way that
  passes its own acceptance test, because the test that selected it
  is the test that checks it. This looks like the central risk.
  - Explained in full, with the `i64::MIN / -1` case worked through,
    at `<WORKSPACE_DIR>/PseudoIR/DevComms/log_001_activation_slice_closure.md`.
  - That log also proposes a fix: subtract the live graph from the
    ledgerer's structural graph, giving a named list of every arm the
    tests did not take. What lit up is the slice; what did not light
    up is the review queue. Claude's proposal, unsettled.
  - **the owner's answer goes further** (2026-07-31,
    `<WORKSPACE_DIR>/PseudoIR/DevComms/log_002_directed_input_generation.md`):
    do not stop at naming the dark arms — REACH them. Generate typed
    inputs for the operator, run them, read the conditions gating the
    branches beneath whatever lit up, and generate inputs satisfying
    those conditions until nothing reachable stays dark. Subtraction
    names; this reaches.

- ~~**How does this relate to the seam declaration?**~~ **ANSWERED
  (the owner, 2026-07-31)**: no seam declaration is needed. The boundary is
  "nodes activated or activatable on the path from the starting node
  to arch opcodes" — computed from the operator's entry and its
  opcodes rather than declared by a person. See log 002 §2.
  - **"Activatable" is over-approximated** (the owner, settled same day):
    "sufficient and substantially easier". Everything the control
    flow says might be reached counts as in-region, without proving
    each is genuinely reachable. Accepted cost: some nodes will stay
    dark because nothing can reach them rather than because nothing
    tested them, and the dark list cannot tell the two apart.
- **What runs the tests?** The chain says "run that test suite
  module". Run where — as original Rust against real rustc, or
  transpiled into the hub, or both and compared? Each answers a
  different question, and only the transpiled run can activate
  detectors on UR-AST nodes.
- **Instrumenting every node, or a bounded region?** Ledger
  population at scale is already an unsettled problem with no current
  anchor (recorded in `<WORKSPACE_DIR>/PseudoIR/Agent_Memory.md` §4).
  A detector per node over a whole compiler is that problem again,
  with a runtime cost added.
- **How is a test module matched to an intention?** Step 3 needs
  "an understanding of a language compiler test suite". That
  understanding is currently nobody's task and lives in no node.

---

## Moved out: progress tracking through tests

The thought that arrived with this idea — "a protocol for tracking
progress. unit test, especially intermediate kinds" — was briefly
recorded here and does not belong in this node.

the owner ruled 2026-07-31 that it is a PLANNING FRAMEWORK policy, to be
implemented throughout PseudoCoupHQ and any project using
PlanPlan. It now lives at
`<WORKSPACE_DIR>/PlanPlan/framework/PROTOCOL.md` §3b.
