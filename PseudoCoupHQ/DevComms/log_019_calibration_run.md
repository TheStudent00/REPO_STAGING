# log 019 — the boolean/float calibration run (WP2, phase 1 first light)

2026-08-14. Work package WP2 from log 018, first suggested run: build the
verification harness and point it at the calibration pair only — boolean and
float — before the heavy census pages. Design constraints were settled in log
018 and were not re-opened.

## §1 — plain-words walkthrough

A quick reintroduction of the cold words before anything else, because this
log will lean on them:

- **census page** — a hand-written page in
  `Research/dominant_intentions/`, one per data structure, listing what that
  structure does in each of the target languages. Every line on it was written
  from knowledge, never executed, and is marked UNVERIFIED by design.
- **fact** — one such line. `F-f1` is the census's name for "what happens when
  you divide a float by zero".
- **owner** — a ruling from 2026-08-13: each fact belongs to exactly one of
  *structure* (what values the thing can hold), *operation* (what you can do
  to it, where the doing belongs to this thing), or *border* (this thing
  meeting some other machinery — an `if`, a print, a sort). Border facts get
  billed to the other party and are not this structure's problem.
- **universal** — a fact the census believes all languages agree on.
- **fracture** — a fact the census believes the languages split on, with named
  camps.
- **vector** — a fact turned into something executable: an identifier, a tiny
  expression, and the answer each language is supposed to give.
- **the lane** — the SandboxDesign agent lane. This session cannot run
  containers itself; it writes a shell script into a watched directory, a
  daemon runs it inside the sandbox one script at a time, and the products
  come back in a directory this session can read.

What was built, in the order it runs:

1. `harness/vectors_boolean_float.json` — every fact on the boolean/float
   census page, written out as executable vectors. Ten facts: five for
   boolean (two structure, three operation), five for float (two structure,
   two operation, plus the one fracture `F-f1`). The universals are in there
   too, not assumed — a claim that "all eleven languages agree" is still a
   claim, and it gets checked like everything else. The border facts that the
   census page deliberately files away from boolean and float (which values
   `if` accepts, what `and`/`or` answer, how a float prints, how NaN sorts)
   are out of scope here; they belong to the machinery that owns them. The one
   exception is `F-f1`, division by zero, which stays on float's page because
   division is float's own operation.
   Each fact expands into small **probes** — 40 of them — so that a fact fails
   in a nameable place rather than as a shrug.
2. `harness/templates/` — one runner template per language, ten of them, plus
   a one-line probe pattern per language. A template is a minimal program: a
   handful of helper functions and a slot where the probes get pasted. No test
   framework anywhere; the whole apparatus is "print one line per probe, in
   the shape `FACT.PROBE|RESULT`". The helpers exist so the probe expressions
   themselves can be written once in a shared C-ish syntax — `d(0.1)` for a
   double, `nan()`, `inf()`, `identb(x)` for a bool that has been through a
   variable and a call. Only python needs its text bent (`true`→`True`,
   `||`→`or`), and c++ needs one rename because `<cmath>` already owns the
   name `nan()`.
3. `harness/generate_run.py` — reads the vectors, pastes the probes into the
   templates, and writes ONE lane script that compiles and runs every
   language's program in turn. One script because the lane is serial anyway,
   and because that way a late language failing cannot lose the earlier
   results. Any probe a compiler is expected to REFUSE gets its own tiny
   separate program, so the refusal costs one small program rather than the
   whole batch — the refusal is then recorded as the result, which is the
   point.
4. `harness/compare.py` — diffs what came back against what the census
   claimed, and writes `verified_boolean_float.json` (a copy also lands in
   `Research/dominant_intentions/verified/`). Canonicalisation of float text
   happens here, in the harness, never in the probed language, so no
   language's printing habits can manufacture a disagreement.

What ran: one lane script, `bf_calibration2.sh`, eleven language runs
(python, ruby, php, typescript, go, c++, java, rust in debug, rust in release,
kotlin, swift), three programs each, 430 probe results. **The whole run took
11.7 seconds**, which is the single most useful number in this log and is
discussed in §4. c# was skipped on purpose (no toolchain, not pursued); dart
was skipped because its SDK is still blocked behind the egress allowlist sync.
Rust ran twice, debug and release, honouring the record-both-modes rule from
integer's page — a rule that costs almost nothing here and will matter later.

The headline outcome: **109 CONFIRMED, 1 REFUTED, 20 SKIPPED** across 130
fact-by-language cells. The calibration pair calibrated. Boolean is exactly as
featureless as the census predicted; float's value layer is the same 64-bit
IEEE double in every language that has one, down to `0.1 + 0.2` landing on the
identical wrong answer everywhere; and `F-f1`, the one genuine fracture, came
back with its camps drawn precisely as written, including the sub-camp detail
that go refuses a *constant* division by zero at compile time while dividing
happily by a zero-valued variable at runtime. Nothing in the census's
boolean/float claims had to be withdrawn.

The single refutation is typescript's, and it is not a bug in the census so
much as a fact the census did not have a slot for: written with two literals,
`true == false` does not run in typescript, because the checker rejects the
comparison before there is a program. Discussed in §3.

## §2 — the verified table

Ten facts down, thirteen language columns across (eleven census targets, plus
rust split into its two build modes, plus swift as a bonus outside the
census's target list). `OK` = CONFIRMED, `XX` = REFUTED, `--` = SKIPPED.

| fact | owner | kind | python | typescript | java | csharp | go | rust | rust-release | ruby | php | kotlin | cpp | dart | swift |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bool-U1 two values true/false | structure | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| bool-U2 nothing else (featureless) | structure | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| bool-U3 negation flips | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| bool-U4 bools compare correctly | operation | universal | OK | **XX** | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| bool-U5 storable/passable/returnable | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| float-U1 same 64-bit IEEE double | structure | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| float-U2 NaN/+Inf/-Inf/-0.0 exist | structure | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| float-U3 arithmetic is IEEE round-to-nearest | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| float-U4 NaN/-0.0/infinity comparisons | operation | universal | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |
| F-f1 division by zero | operation | **fracture** | OK | OK | OK | -- | OK | OK | OK | OK | OK | OK | OK | -- | OK |

Totals: **CONFIRMED 109, REFUTED 1, SKIPPED 20** (csharp 10 + dart 10).

The fracture cell deserves its evidence spelled out, since "OK" on a fracture
means "the split is where the census said it was", not "everybody agreed":

| probe | expression | python | php | go | everyone else |
|---|---|---|---|---|---|
| F-f1.a | `one() / z()` | `<raise:ZeroDivisionError>` | `<raise:DivisionByZeroError>` | `inf` | `inf` |
| F-f1.b | `negone() / z()` | `<raise:ZeroDivisionError>` | `<raise:DivisionByZeroError>` | `-inf` | `-inf` |
| F-f1.c | `z() / z()` | `<raise:ZeroDivisionError>` | `<raise:DivisionByZeroError>` | `nan` | `nan` |
| F-f1.d | literal `1.0 / 0.0` | `<raise:ZeroDivisionError>` | `<raise:DivisionByZeroError>` | `<compile-error>` | `inf` |
| F-f1.e | `fdiv(1.0, 0.0)` | — | `inf` | — | — |

Go's compile refusal reads, verbatim:
`./main.go:41:135: invalid operation: division by zero`.

So the guarantees actually on offer for float division by zero are three, not
two: **quiet IEEE** (nine languages), **refuse at runtime** (python, php), and
**refuse at compile time when the divisor is a literal zero** (go, on top of
its runtime IEEE behaviour). php additionally ships the quiet IEEE answer
under a different name, `fdiv`, exactly as the census said — which is worth
noting for ingress, because a php source calling `fdiv` has *chosen* the quiet
guarantee explicitly and that intent should survive translation.

## §3 — the one REFUTED cell, discussed

**bool-U4 / typescript — "two bools compare equal/unequal correctly".**

- What was expected: `true == false` prints `false`, `true != false` prints
  `true`.
- What happened: `<compile-error>`, twice.
  `main.ts(18,39): error TS2367: This comparison appears to be unintentional
  because the types 'true' and 'false' have no overlap.`
- The other four probes of bool-U4 — the same comparisons written over values
  that have been through a variable and a function call — all passed in
  typescript. So typescript compares bools correctly; it simply refuses to
  compile the *literal* form.

Verdict: **not census-wrong, not harness-wrong — genuinely instructive.** The
census's claim is true of typescript at the level the census meant it. What
the probe caught is a different animal: typescript narrows a literal `true` to
the singleton type `true`, and its checker then reports a comparison between
two provably disjoint types as a mistake. This is a fact about typescript's
*checker*, not about its booleans, and by the owner ruling it is not a
structure fact and not an operation fact — it is a border fact, boolean
meeting the type checker.

Proposed correction for the owner — **not applied; the census page is untouched, as
instructed**:

1. Add to `census_boolean_float.md`, under boolean's border list, a fourth
   entry: **"→ the type checker: comparing two bool LITERALS."** typescript
   refuses (TS2367, disjoint literal types); the other ten accept it. Owner:
   the pair (boolean, checker), billed to the checker.
2. Leave bool-U4 itself standing as an 11/11 universal, since it is one.
3. A general note worth adding to the standing rules, if the owner agrees: a
   language may refuse a program at COMPILE time for a reason that says
   nothing about the values involved. The harness now has a mechanism for
   this (isolated one-probe programs, refusals recorded as
   `<compile-error>`), and go's `F-f1.d` is the second example already in
   hand. Compile-time refusal is a third result category alongside "answers"
   and "raises", and the dominant will need to know which of the three a
   source language was relying on.

No other cell refuted, so there is nothing else to discuss here — which is the
correct outcome for a calibration pair, and is what makes the one refutation
worth the whole run.

## §4 — harness lessons for the full run

**Compile times are a non-problem.** The entire run — eleven language runs,
three programs each, from cold — took 11.7 seconds and consumed 11 MB of
scratch. kotlinc, budgeted for at roughly a minute per compile, was not
noticeably slower than the rest once it was invoked as
`kotlinc main.kt -d classes` and run against
`/persist/kotlinc/lib/kotlin-stdlib.jar`, instead of asked to build a
self-contained jar with `-include-runtime`. **Recommendation: build classes,
not jars.** The heavy census pages can be batched exactly like this one, and
there is no need to split runs per object to stay inside the lane's timeout.

**Batching: one script, isolated programs inside it.** The important structure
is not one-script-per-language but one-program-per-refusal-risk. Probes that a
compiler may reject must not share a program with probes that must run. This
came up twice in ten facts (go's constant zero divisor, typescript's literal
comparison), and integer's page — with its fixed widths, its overflow modes
and its three divisions — will hit it far more often. `generate_run.py` now
takes a `program` name on any probe and emits a separate tiny program for it,
recording every probe in a refused program as `<compile-error>`.

**Canonicalisation gotchas, in the order they bit:**

- *Go's untyped constants are arbitrary precision.* This is the serious one.
  Written naively, `0.1 + 0.2 == 0.3` in go is evaluated by the compiler at
  something like 256 bits and answers **true** — the opposite of every other
  language, and a completely false fracture. Every float literal in every
  probe therefore goes through a helper `d(x)` whose parameter is typed
  `float64`, which forces the value into a 64-bit double before any
  arithmetic. Any future numeric census page must do the same or it will
  invent disagreements that do not exist.
- *Compilers fold constants.* `1.0 / 0.0` written literally is answered at
  compile time by several languages, which is a different question from
  dividing a runtime value by a runtime zero. Both are interesting, so both
  are probed, separately and by name (`F-f1.a` vs `F-f1.d`).
- *Never compare printed floats.* Every numeric universal is probed as a
  comparison against a hand-computed binary64 value (`d(0.1) + d(0.2) ==
  d(0.30000000000000004)`) rather than by printing and diffing text. Printing
  is costume — c++ defaults to 6 significant digits, php to a precision
  setting, go to a format verb — and the census already suspects printing
  should be excluded from dominance entirely. Only the special values
  (`inf`, `-inf`, `nan`) are emitted as text, and those spellings are the
  harness's shared convention, not any language's.
- *`-0.0` cannot be fully probed here.* Showing that `-0.0` is a genuinely
  separate value from `0.0` needs either `1.0 / -0.0` (which borrows F-f1's
  fracture and raises in python and php) or a sign-bit helper that not every
  language spells the same way. `float-U2` therefore only asserts that `-0.0`
  is writable and compares equal to `0.0`. Flagged for the owner: if the separateness
  of `-0.0` matters to the dominant float, it needs its own vector with a
  per-language snippet rather than a shared expression.
- *Compiler diagnostics on stdout.* tsc reports type errors on stdout, not
  stderr, so a build log briefly ended up inside a results file. The harness
  now harvests only lines containing a pipe, and the first line for a given
  probe identifier wins.

**One honest gap:** swift was run as a bonus and confirmed everything, but it
is outside the census's target list and its ncurses symlink must be reapplied
per session (the lane script does this itself now). Its cells are
informational and should not be read as census evidence.

## §5 — next-run readiness

Ready now, no new machinery needed:

- The pipeline is `vectors_*.json` → `generate_run.py` → lane →
  `results/` → `compare.py` → `verified_*.json`. Adding an object means
  writing one more vectors file; the templates, the runners and the comparison
  are object-agnostic already.
- Runtime is not a constraint. The remaining four pages (integer, string,
  list, dict) can plausibly go in one or two lane scripts.

Needed before the heavy pages run:

- **Integer will need per-language probe text, not one shared expression.**
  Its first structure fact is already a three-way fracture — fixed-width,
  unbounded, and typescript having no integer at all — so there is no single
  expression that means the same thing everywhere. The vectors format supports
  this (a probe may carry a per-language expression); the boolean/float run
  simply never needed it.
- **Mode-dependent facts.** Rust debug versus release is wired and cost
  nothing here; dart's native-versus-web modes cannot be exercised until the
  SDK is unblocked.
- **Two toolchain gaps to record honestly rather than fix:** csharp is
  blocked-deliberate (no toolchain, not pursued), dart is
  blocked-on-allowlist-sync (`.googleapis.com` staged in the proxy allowlist,
  awaiting the owner's `allow.sh sync`). If dart lands before the heavy run, it
  slots in by adding one entry to `RUN_ORDER` and one template.
- **the owner's ruling on §3** — whether the typescript literal-comparison fact
  joins boolean's border list, and whether compile-time refusal becomes a
  named third result category in the standing rules.

Nothing in the census pages was edited by this run. Corrections are proposed
above and wait on the owner.

### artifacts

- `Research/dominant_intentions/harness/vectors_boolean_float.json`
- `Research/dominant_intentions/harness/templates/` (10 languages)
- `Research/dominant_intentions/harness/generate_run.py`
- `Research/dominant_intentions/harness/compare.py`
- `Research/dominant_intentions/harness/lane_bf.sh` (generated; the exact
  script the lane ran, as `bf_calibration2.sh`)
- `Research/dominant_intentions/harness/results/bf_*.txt` (11 raw result
  files, the evidence)
- `Research/dominant_intentions/harness/verified_boolean_float.json` and a
  copy at `Research/dominant_intentions/verified/verified_boolean_float.json`
- lane log: `SandboxDesign/agent/logs/20260814T150500Z__bf_calibration2.sh.log`
