# log_012 — Discipline history: what "discipline" meant across the PseudoCoup lineage, and how it relates to the fidelity doctrine

Research memo, archival only. Answers the owner's 2026-08-05 question: what did "discipline" mean in the PseudoCoup lineage — especially PseudoCoup v3 — and is it the same thing as, or different from, the "fidelity doctrine"? No settling of the question happens below; findings are marked as readings, the owner rules.

## 1. What "discipline" IS in v3

The core artifact is `0_Archive/PseudoCoup_v3/.planning/.archive/initial_discipline_assessment_log.md` (filesystem mtime 2026-07-09; landed in this super-repo's git history at commit `c6addfd`, 2026-07-10). It lays out a "Discipline Rules Matrix" — the 12-language by 8-rule matrix cited by the transpiler survey as the spec to measure against. The 8 rules, quoted verbatim:

| # | Rule | Quoted verdict |
|---|---|---|
| 1 | Static Type Annotations | "REQUIRED. The source code must be 100% statically typed. Without types, C++, Java, and Rust cannot compile." |
| 2 | Null Safety (Explicit `?`) | "REQUIRED. Source must explicitly mark `Optional[T]`. Languages like Swift, Rust, and Kotlin will crash if nulls are implicit." |
| 3 | Multiple Inheritance | "FORBIDDEN. Because Java, C#, Dart, etc., only support single inheritance, the source code must never use multiple inheritance." |
| 4 | Generators (`yield`) | "FORBIDDEN. Go, Java, and Swift do not have clean native generator equivalents. Iteration must use standard collections." |
| 5 | Keyword Arguments (kwargs) | "RESOLVED AT COMPILE. Java, C++, and Go do not support kwargs natively. The transpiler must automatically convert kwargs to positional arguments or an options-struct." |
| 6 | Try / Catch / Exceptions | "RESTRICTED. Go uses `error` returns; Rust uses `Result`. The discipline must restrict exceptions to broad boundaries, or the transpiler must wrap functions in `Result` types for Go/Rust targets." |
| 7 | Tuple Unpacking | "RESTRICTED. Java does not support native tuple unpacking natively without custom Pair classes." |
| 8 | Operator Overloading | "FORBIDDEN. Java, Go, and TypeScript do not support operator overloading. Operations must use named methods (e.g., `add()`)." |

Purpose of the matrix, quoted from the same file: "If even one target language strictly forbids a paradigm (like multiple inheritance) or requires a paradigm (like static typing), the Universal Discipline must enforce that rule at the source." And: "The transpilation becomes *mechanical* rather than *interpretive*."

Path: `0_Archive/PseudoCoup_v3/.planning/.archive/initial_discipline_assessment_log.md`

A co-located file, `0_Archive/PseudoCoup_v3/.planning/.archive/05_discipline_oracle_log.md` (git: added `a25ef79` 2026-07-08, amended `23173e7` 2026-07-09, touched `c6addfd` 2026-07-10), restates the same 8 rules as "Oracle" demands and frames a longer-term aspiration: "the goal of PseudoCoup is to eventually reduce the burden of explicit discipline by building intelligent, interpretive transpilation skills that handle these strict rules mechanically behind the scenes."

The v3 architecture overview names the concept and cross-references the log:

> "**The Oracle Discipline:** Developers must write disciplined, strongly typed pseudo-code (typically starting in Python) avoiding magic runtime reflection. See `05_discipline_oracle_log.md`."

Path: `0_Archive/PseudoCoup_v3/.planning/.archive/00_architecture_overview.md`

A retrospective in the same directory, comparing v3 to v1, states plainly what discipline is *for*:

> "V1 did not have a discipline. V1 was a catastrophic architectural failure." … "3. **The LCD Discipline is Non-Negotiable:** V1 tried to guess how to translate dynamic Python into Rust and C++, and it panicked (`/* unhandled call */`). By strictly enforcing the Java/Go LCD Discipline *in the Python source code*, V3 eliminates the guesswork."

Path: `0_Archive/PseudoCoup_v3/.planning/.archive/06_v1_solutions_reference.md`

The canonical spec-form statement of the same rules lives one repo over, in old-PseudoIR's design tree:

Path: `0_Archive/PseudoIR/DevComms/.planning/design/The_Oracle_Discipline.md` (git: `5049d45` 2026-07-09 added, `9c2d05b` 2026-07-09 "Restored full 12-language matrix to Oracle Discipline", `a6d42b4` 2026-07-09 final).

In short: in v3, "discipline" IS a fixed, prose-form checklist of 8 source-code constraints (typing, null-safety, no multi-inheritance, no generators, kwargs, exceptions, tuple-unpacking, operator overloading), each justified by naming which of the 12 target languages breaks without it. Its stated purpose is to make transpilation mechanical instead of interpretive by moving the burden of cross-language compatibility into the Python source itself, upstream of the transpile step.

## 2. What the fidelity doctrine IS

`PRIVATE/PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md`, §4 ("Synthesis"), lines ~117-121 (git: commit `8c6ea51`, 2026-07-31), states it as a cross-validated finding:

> "The fidelity doctrine appears twice independently — PCv5's uniform-polyfill rule and PseudoIR's `compiler_transpilation_experiment.md` boundary rule ('every operator on the polyfilled type routes through the simulator, or none do') — same law, derived from different bugs. Cross-validated."

Source A — PCv5's uniform-polyfill rule. Stated as a bare standing rule in two places:

- `PRIVATE/PseudoCoup_v5/DevComms/HANDOFF_2026-07-25.md`, line 625: "Uniform polyfill wrapping; no proof-as-exemption."
- `PRIVATE/PseudoCoup_v5/DevComms/plan_2026-07-25.md`, line 149 (under "Standing rules"): "Uniform polyfill wrapping; no proof-as-exemption."

And with rationale in `PRIVATE/PseudoCoup_v5/Research/cpp_ingress/transpile_cpp.py`, lines 40-45:

> "MANDATORY POLICY (uniform polyfill wrapping, the owner 2026-07-25, restated from vocab_support.py's header for this second source language): every arithmetic node (|, ^, &, <<, >>, +, -) in a uint8_t-typed C++ expression is wrapped in u8(), with NO exemptions — not even where overflow is provably impossible (e.g. W/R/X/B are always single bits here). Uniform depth is what makes an unwrapped node unambiguously a transpiler bug instead of a 'proof-based' omission that can't be told apart from a miss. Comparison (<, <=, ==, ...) and logical (&&, ||) operators are NOT arithmetic and are therefore never wrapped — same rule the Rust transpiler already applies (see transpile_support.py's parse_cmp)."

Source B — PseudoIR's `compiler_transpilation_experiment.md`. This file is in the *retired* PseudoIR repo, not the live or archived-non-retired one: `0_Archive/PseudoIR_(retired)/DevComms/compiler_transpilation_experiment.md` (git: `dc01b9c` 2026-07-22 original, `be2203d` 2026-07-23 revision). §5, "The Solution: The Semantic Polyfill Engine":

> "Two corrections to the original polyfill policy: 1. Width comes from the Ledger's declared type, not a default. … 2. **Every operator on the polyfilled type routes through the simulator, or none do.** The original output applied raw Dart `~` and only routed `&` through the simulator. A polyfill boundary that some operators bypass is not a boundary."

Related mechanized enforcement in the same lineage, from the retired-PseudoIR v2 gate:

> "5. **Enforcement:** If a type cannot be resolved from the syntax AND is missing from the Ledger, the Ingestor must halt execution and throw a Discipline Violation."

Path: `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/master.md`, §3, Phase 1 step 5, line 63 (git: `7a944e3` 2026-07-09 "Drafted Ledger Specification", `852733c` 2026-07-09). This is the only literal occurrence of the exact phrase "Discipline Violation" found anywhere in the searched trees.

## 3. The comparison (a reading — the owner rules)

| | v3's "discipline" (Oracle Discipline) | The fidelity doctrine |
|---|---|---|
| Object governed | The Hub-language *source code* the owner/agents write | The *transpiled output*, specifically how polyfilled/simulated types get their operators wired |
| Form | An 8-item prose checklist keyed to 12 target languages ("REQUIRED"/"FORBIDDEN"/"RESTRICTED"/"RESOLVED AT COMPILE") | A single boundary law: "every operator on the polyfilled type routes through the simulator, or none do" |
| Instance | Rule 8: "FORBIDDEN. Java, Go, and TypeScript do not support operator overloading. Operations must use named methods (e.g., `add()`)." — a constraint on what may appear in the Hub source | "The original output applied raw Dart `~` and only routed `&` through the simulator. A polyfill boundary that some operators bypass is not a boundary." — a constraint on how the *emitter* must treat an already-chosen polyfill type, uniformly, no matter which operator |
| Direction of enforcement | Upstream — restricts the developer's Python before transpilation runs | Downstream — restricts the transpiler/emitter's own output after a polyfill decision has been made |
| Failure mode it prevents | The transpiler having to *guess* how to render an unsupported Python construct in a target language ("V1 tried to guess... and it panicked") | A polyfill silently leaking un-simulated behavior through the one operator someone forgot to route, i.e. partial coverage passing as complete |

Reading: these read as two different scopes of the same underlying value — "make behavior mechanical and total instead of partial and guessed" — but they are not the same rule and are not stated as such anywhere in the lineage. Nothing in `The_Oracle_Discipline.md`, `initial_discipline_assessment_log.md`, or the ledger specs mentions polyfill-operator routing; nothing in `compiler_transpilation_experiment.md` or the PCv5 uniform-polyfill-wrapping rule references the 8-rule/12-language matrix. The transpiler survey itself treats them as separate things that happen to rhyme — it calls the fidelity doctrine something that "appears twice independently... same law, derived from different bugs," a claim made about the *two fidelity-doctrine sightings* (PCv5 and retired-PseudoIR), not about a claimed equivalence with v3's Oracle Discipline. No source found asserts v3's discipline and the fidelity doctrine are the same instrument. My reading is that they are two ideas under one recurring word — "discipline"/"doctrine" is being used across this lineage as a generic label for "the mechanical rule that removes a category of guesswork," and each project instance picks a different guesswork category to remove. the owner rules on whether that's a distinction worth preserving or a naming coincidence worth collapsing.

## 4. Every other distinct sense of "discipline"/"doctrine" found in the lineage

| Sense | Path |
|---|---|
| "Universal Discipline" as 3 abstract principles (Intent not Mechanism; Concrete Constructs; Map→Wrap→Fail) | `0_Archive/PseudoCoup_v1/README.md` |
| Same 3-principle "Universal Discipline" restated, v4/live-twin copies | `0_Archive/PseudoCoup_v4/README.md`, `PUBLIC/PseudoCoup/README.md` |
| Discipline as a pre-transpile CLI gate flag ("pseudoir.gate pre-transpile discipline check"; "--no-gate ... discipline should be opt-out, not opt-in") | `0_Archive/PseudoCoup_v4/pseudocoup/cli.py`, `PUBLIC/PseudoCoup/pseudocoup/cli.py` (byte-identical), `0_Archive/PseudoCoup_v4/.planning/21_two_gates.md`, `PUBLIC/PseudoCoup/.planning/21_two_gates.md`, `0_Archive/PseudoCoup_v4/.planning/00_Upgrade_Plan.md`, `PUBLIC/PseudoCoup/.planning/00_Upgrade_Plan.md` |
| Discipline mechanized as a gate module with a relaxation policy (kwargs/tuple-unpacking/operator-overloading/null-handling relaxed via "registered ops," generators/exceptions/multi-inheritance/static-typing still hard rules) | `0_Archive/PseudoIR_(retired)/v2/gate/DISCIPLINE_CHECK.md`, `0_Archive/PseudoIR_(retired)/v2/discipline_relaxation.md` |
| Memory-model discipline: "The Universal Discipline mandates that the Python Hub acts as a memory-abstracted environment," forbidding explicit pointers/addresses/pass-by-reference in Hub source | `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/memory_erasure_schema.md` |
| Discipline as enforced by the Ledger's type registry across language boundaries | `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/type_registry_schema.md` |
| "discipline" defined explicitly as a floor, not dogma: "a Python subset chosen so translation is mechanical... a lighter target (Dart) gets a lighter discipline" | `PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/README.md` |
| "MAIN-SOURCE DISCIPLINE" — an unrelated app-hygiene sense: disciplining a WFL Kotlin app's source so a Kotlin↔Python transpile pair agrees, not the Oracle Discipline matrix | `PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/DevComms/main_source_discipline.md` |
| "Discipline-checker gauge first" — treated as a measuring instrument analogous to a test gauge | `PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/HANDOFF.md` |
| "Retraction discipline" — generic session-conduct sense, unrelated to transpilation | `PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/Agent_Memory.md` |
| "One discipline, two directions" thesis for forward/backward PseudoDart translation | `PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/DevComms/log_0_pseudodart_forward_backward_discipline.md` |
| "Discipline reminders" as a named section in a handoff report | `PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/DevComms/PseudoCoup_handoff_report.md` |
| "disciplined Kotlin→Python transpiler" as a tool tagline | `PRIVATE/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/README.md` |
| Doctrine as a citation label for old design docs plus failure post-mortems, bundled together | `PRIVATE/PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md` ("Doctrine + post-mortems \| old-PseudoIR design docs; PyHaxe failure notes \| `0_Archive/PseudoIR/DevComms/.planning/design/`, `0_Archive/PyHaxe/docs/DEVELOPMENT_NOTES.md`") |

## open questions for the owner

- Is the fidelity doctrine meant to formally supersede/absorb v3's Oracle Discipline as PCv5's governing rule, or are they meant to coexist as separate concerns (source-side constraint vs. emitter-side constraint)?
- The retired-PseudoIR ledger's "halt-on-unresolvable Discipline Violation" is the only literal use of that phrase found — is that the intended enforcement mechanism for the fidelity doctrine going forward, or a v2-era artifact that should not be treated as binding?
- StressBot's `PseudoCoup_v0/README.md` defines discipline explicitly as "a floor, not dogma... a lighter target gets a lighter discipline" — does that graduated-strictness model apply to PCv5's uniform-polyfill rule, which currently states "no exemptions" without qualification?
- Several PCv5-internal files (`hub/__init__.py`, `project_state.md`, `log_002_ur_brainstorm.md`, `log_001_ledgerer_harvest_findings.md`, `dev_plan_log.md`, `language_divergence_study_log.md`, `log_006_ur_kinds_vocabulary.md`, `ledger_survey_2026-07-27.md`, `README.md`, `Research/vocab_transpiler/transpile_support.py`, `Research/divergence_suite/README.md`) use "discipline" in passing but were not individually quote-extracted for this log — worth a follow-up pass if any of them state a rule not captured above.
- Three separate repos are all named "PseudoIR" (`0_Archive/PseudoIR/`, `0_Archive/PseudoIR_(retired)/`, `PRIVATE/PseudoIR/` live) — is the live PseudoIR repo's planning tree (which also has "discipline" hits, e.g. `Planning/CORE_0.md`, `Planning/node_0_2_hub/SUPPORT_hub.md`) a continuation of either archived lineage's discipline concept, or a fresh redefinition? Not checked in this pass.
