# log 003 — what has been said about transpiler and ledgerer components

2026-07-31, written because the owner asked to be reminded.

Everything below is quoted or condensed from recorded files, with the
file named. **Section 1 is what the owner said. Section 2 is what the two
surveys FOUND** — the distinction matters, because the maps are
survey output that the owner directed rather than statements he made.

Sources:
`~/Programming/PseudoCoup_v6/AgentMemory/03_lineage_and_harvest.md`
(the condensed maps),
`~/Programming/PseudoCoup_v6/AgentMemory/02_decisions.md` (the
rulings), and the two full surveys with line-cited evidence, which
still exist at
`~/Programming/PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md`
and `~/Programming/PseudoCoup_v5/DevComms/ledger_survey_2026-07-27.md`.

---

## 1. What the owner has said

- **Build by composition, not by porting.** "The most advanced
  transpiler/ledger are built by COMPOSITION from best-in-class
  components across versions" (2026-07-28).
- **Mine, don't resurrect.** "T3 fresh spine, mining the lineage — no
  wholesale port of any version-base; components transplant with
  provenance headers and acceptance tests." The phrase is WFL's, and
  it is the precedent being followed.
- **Parts can come from anywhere** (2026-07-31, on the rebuilt PCv5).
- **Generalize then specialize.** tree-sitter handling, the ledger,
  and most transpiler machinery overlap massively across languages;
  generalize what overlaps, specialize only where a language demands
  it. the owner calls this the automation goal expressed as design.
- **tree-sitter is the parsing foundation**, no exceptions without
  extraordinary proof — and "arguably the most significant module in
  the project".
- **The ledger is an independent tool.** PseudoCoup is a module of
  tools; centralised control comes later, "hopefully ontology will
  reveal itself."
- **The ledger is ONE record across three axes** — semantic,
  structural, runtime — not separate ledgers joined afterwards.
- **The ledger's id is a runtime-observable signal**: per-call-site
  positional-path id plus a per-instance key, emitted identically
  into every transpiled side, joined by id equality. Coordinate and
  anchor joins were rejected on evidence.
- **Ingest never guesses.** It records `unresolvable` honestly, and
  the consumers — emitter, slicer — halt on it.
- **Every tool ships with its own acceptance test**, and the oracle
  assets live beside the tool. Not a separate component.
- **Emitted artifacts are the stability layer**: deterministic, no
  timestamps, provenance headers, regeneration byte-identical.
- **The 289-line semantic ledger and v0's verification tooling are
  two families that never met** — see §2.

---

## 2. What the surveys found

the owner directed these; the findings are the surveys'.

### The headline

**"Most advanced" is distributed.** No version-state holds the best
of more than two capabilities. The most advanced transpiler and
ledger do not exist yet — their parts do.

### Transpiler parts, best-in-class per capability

| capability | where the best version lives |
|---|---|
| behavioral verification | v0 `oracle.py` + `fuzz.py` |
| lowering knowledge as data, gate before emit | pseudoir registry + `gate.py` |
| lowering falsification | PseudoIR v2 `runtime_prober.py`, trap vectors |
| ingress coverage gate | WFL `ingress/coverage.py` + baseline + driver |
| deep-semantics emission | WFL `egress/dart.py` |
| compiler-source ingress, oracle-checked | PCv5 `Research/{vocab_transpiler,cpp_ingress}` |
| automated node-to-IR map derivation | PseudoIR v3 mutational solvers |
| cheap regression net | v4 byte-snapshot tests |
| error-cause instrumentation | WFL `error_census.py` |
| compile-as-oracle per construct | v0 py2many `gate.py` |
| discipline spec to measure against | v3's 12-language by 8-rule matrix |
| doctrine and post-mortems | old-PseudoIR design docs; PyHaxe DEVELOPMENT_NOTES |

One entry is superseded: the automated node-to-IR derivation. the owner
closed the "IR question" — probe-mining reconstructs the table,
whereas slicing runs the table-generator, which is the project's
founding insight. The solvers are archived history, not a candidate.

### Ledger parts

Two families that never met — **semantic** (drives emission; the
289-line ledger) and **verification** (identity, integrity,
divergence taxonomy; v0's tools). The combined ledger was mapped as:

- **primary key** — v0 `idgen.py` positional-path ids. Called the
  highest-value single transplant in the survey, because it kills
  bare-name keying and anchor keying at once.
- **record shape** — v0 `ledger_unified.py` superset entry, plus its
  `check()` integrity mode.
- **semantic payload** — the 289-line ledger's registries, re-keyed
  onto ids, with the fully-qualified name as a secondary index.
- **enforcement** — three-tier qualified naming plus
  halt-on-unresolvable, in the refusing style of PCv5's TyCtxt stub.
- **divergence** — one taxonomy merging v0's `classify_methods`
  kinds, the experimental `ledger.json` reason vocabulary, and
  registry strategy/status as a confidence signal.
- **verification half** — v0's execute-and-introspect,
  dropped/relocated logic, and `kit_ledger` longest-common-
  subsequence and signature comparison, joined on id equality.
- **registry linkage** — flagged as a design opportunity with NO
  existing code: a divergence entry carrying a registry op id and a
  confirmation status, so every divergence is evidence-backed.

### Where the version-states are

Condensed from the version map. Deepest verification is v0
(`~/Programming/StressBot/RelevantProjects/PseudoCoup_v0/`) — oracle,
fuzzer, ledgers, idgen, with a Kotlin test suite passing in Python
160/160. The only CFG/SSA middle-end is v1. The UR-AST was born in
v3. The 289-line semantic ledger and polyfill engine are v4. The
deepest emitter is WFL's `dart.py` at 3,845 lines. Compiler-source
ingress and the extraction/insertion proof are PCv5's.

---

## 3. Two things worth re-reading before harvesting

- **The full surveys carry line-cited evidence** that the condensed
  maps do not. If a map entry is going to be acted on, the survey is
  where the claim can be checked.
- **The maps are dated 2026-07-27** and predate both the purge and
  the split. At least one entry is already void (the IR solvers), and
  the PCv5 row describes a repo that is about to be gutted. Treat the
  maps as a reading list, not as current state.

---

## 4. Not in the maps, and probably should be

`WalkEmit` — the global runtime tracer found 2026-07-31 at
`~/Programming/StressBot/RelevantProjects/WFL_MixingCenter/WFL/app/src/main/java/com/sara/workoutforlife/core/debug/WalkEmit.kt`,
with its tree-sitter driven injector in
`~/Programming/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/inject_emitid.py`.

It is the working precedent for the detector idea, it is keyed on the
same idgen ids the ledger map already selects, and it appears in
neither survey — the surveys were written before it was looked for.
Detail in
`~/Programming/PseudoIR/Planning/node_0_0_tools/node_0_0_1_slice/SUPPORT_brainstorm.md`.

**the owner, 2026-07-31: this tooling belongs in PCv5** — "i think we do
need that tooling in PCv5. or rather, it would be better to have that
tool than not." So it is a harvest target, not only a design
reference. Two parts, and the second is the one that makes it a tool
rather than a trick:

- the global tracer itself, `WalkEmit` — small, and its shape is
  already understood;
- the INJECTOR, `inject_emitid.py` — 837 lines, tree-sitter driven,
  which places the calls at node granularity. This is the part that
  makes instrumentation mechanical rather than hand-written.

Inherited hazards recorded with it: the injector is not idempotent,
and the per-instance counter drifts. Both are in the brainstorm.
