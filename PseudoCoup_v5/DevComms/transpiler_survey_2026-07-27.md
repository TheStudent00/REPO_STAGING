# Transpiler Survey — 2026-07-27

Purpose: capability inventory across every version-state of the
PseudoCoup transpiler lineage and its precursor projects, toward
finding or building the most advanced version — where "most
advanced" means most sophisticated at ACCURATELY transpiling (the owner),
not most advanced with respect to any particular source/target pair.

Method: two parallel read-only survey agents, every claim from
reading files (line counts from `wc -l`); inference is marked. This
document condenses their reports; paths are absolute.

---

## 1. Identity findings (corrections to the assumed version list)

- `0_Archive/PseudoCoup_v4/` and `PseudoCoup/` are **byte-identical**
  (`diff -rq` clean). One version-state, reported as v4/PseudoCoup.
- `0_Archive/PseudoCoup_v3/` contains a full vendored copy of v2.
- `StressBot/RelevantProjects/PseudoCoup_v0/` is a **different
  transpiler family** (Kotlin→Python single-target + a py2many
  Python→Kotlin experiment); it shares no code with v1–v4.
- `0_Archive/WFL_PseudoCoup_Briefing/` is NOT a variant of
  WFL_PseudoCoup — it is a curated v0-era briefing bundle, and the
  only holder of `PseudoDart/`+`PseudoFlutter/` copies alongside the
  v0 tools.
- `PseudoIR/` is five artifacts in one repo: the packaged `pseudoir/`
  product, `v2/` (op harvester + prober + registry research), `v3/`
  (compiler-IR mining), `v4/` (IR→machine-opcode planning), and
  `archive/experiments/` exp01–09 (nine bidirectional pair
  transpilers + round-trip harness).
- `SourceIRs/` (~5.5 GB) is the vendored compiler-source substrate
  (Go, .NET runtime, Dart SDK, OpenJDK, LLVM, GraalVM) that
  PseudoIR v3/v4 extraction depends on. Keep.

## 2. Cross-version comparison (PseudoCoup lineage)

| Dimension | v0 | v1 | v2 | v3 | v4/PseudoCoup | WFL_PseudoCoup |
|---|---|---|---|---|---|---|
| Ingress | tree-sitter (Kotlin) + py2many | tree-sitter, 13 langs | tree-sitter, 1 lang | tree-sitter, 11 langs | tree-sitter, 11 langs | tree-sitter, 11 langs |
| Targets | Python | 14 emitters | 1 generic | 12 | 12 | 12 (Dart live) |
| IR | none (direct visitor) | linear IR→CFG→SSA | same | UR-AST (nested) | UR-AST | UR-AST |
| Ledger | 4 modules, 1,585 lines | none | none | 45 lines | 289 lines | 289 (origin) |
| Polyfill | 5,700+ line runtime shims | wrapper registry w/ fail | wrapper registry | none | polyfill_engine.py (115) | kit.dart in emitted app |
| Verification | oracle + fuzzer + gauges | parity + daisy chain | 1 roundtrip | 12 roundtrip artifacts | 54 pytest incl. byte-snapshots | coverage gate + error census, 325 files |
| Recorded numbers | extensive | none | none | none | yes | extensive (15,951→6,323 error trajectory) |
| Scale (py lines) | ~21,400 | ~5,400 | 1,334 | ~5,900 | ~15,200 | ~16,600 |

Recorded highlights (quoted in the full agent reports; sources:
`PseudoCoup_v0/PROGRESS.md`, `PseudoCoup/.planning/00_Upgrade_Plan.md`,
`WFL_PseudoCoup/.planning/00_Master_Plan.md`):

- v0: Kotlin test suite passes in Python 160/160; parse 280/281;
  layout fidelity 377/377; extern wrappers 338/345.
- v4/PseudoCoup: 54 tests passing incl. 24 byte-snapshot; BUT its
  pseudoir upgrade units U2 (registry consultation in the 12
  emitters) and U3 (hoister unification) are recorded "not started".
- WFL: transpile gate clean across 8 sweeps (Ingest 0/325, Emit
  0/325); analyzer errors 15,951 → 6,323 over sweeps; run-22 gate
  outstanding.

## 3. Precursor/adjacent projects (essentials)

- **PseudoIR `pseudoir/`**: Python-only ingress (tree-sitter), 4
  emitters (py/ts/go/dart), thin `OpNode`/`Raw` IR, and the
  lineage's only machine-confirmed per-op-per-language lowering
  REGISTRY (`registry/data/ops.json` + `schema.md`, 13 strategy
  ranks) with a gate that refuses to emit unconfirmed lowerings
  BEFORE emission. Three-way byte-identical oracle test passing.
- **PseudoIR v2**: the falsification engine — `runtime_prober.py`
  (815) executes candidate lowerings against real runtimes with
  per-op test vectors (falsy traps, swap traps, reference-equality
  traps); 12 pinned grammars; 10/12 language columns
  runtime-confirmed. "ORIGINAL PLAN COMPLETE (2026-07-14)."
- **PseudoIR v3**: mutational opcode-differencing solvers (5) that
  derive node→IR-opcode maps by compiling probes and diffing —
  the only automated map-derivation technique in the lineage.
  Includes a recorded rollback episode ("undoing LLM slop" ×3).
- **PseudoIR v4**: planning-only; the Go SSA ↔ RyuJIT ↔ Dart IL
  `Unified_SSA_Opcode_Matrix.md` (340 lines) + vendored per-arch
  compiler backend files.
- **0_Archive/PseudoIR exp01–09**: nine bidirectional pair
  transpilers with per-experiment ledger.json sidecars; exp09 is a
  4-language dynamic-oracle round-trip harness (egress → ingress →
  run → diff vs canonical). Design doctrine docs live here
  (`Map_Wrap_Fail_Contract.md`, `Historical_Transpiler_Lessons.md`
  — the regex post-mortem, `The_Oracle_Discipline.md`) plus 24
  written per-language ingestor/emitter specs.
- **PyHaxe**: Python-ast ingress; the largest single emitter
  surveyed (`haxe_emitter.py` 3,877) with the deepest lowering
  tricks (truthy(), TupleN on demand, kwargs structs, override
  detection, comment preservation via tokenize) and an unusually
  candid failure catalogue (`docs/DEVELOPMENT_NOTES.md`).
- **PseudoDart**: Python-ast→Dart (1,402-line emitter); 3-tier
  verification ending in emit → `dart analyze` → `dart run` →
  assert stdout; 32-row lowering table; honest gap list (e.g.
  dynamic record index `t[i]` structurally impossible in Dart).
- **PseudoFlutter**: not a transpiler; the two-engine differential
  rendering oracle (Flutter vs Kivy, ~70 golden PNG pairs from one
  Python source) proving PseudoDart output end to end.
- **PseudoSyntax**: 164-line VS Code linter prototype. Negligible.

## 4. Synthesis

- **"Most advanced" is confirmed distributed.** No version-state
  holds the best of more than two capabilities. The most advanced
  transpiler does not exist yet; its parts do.
- **Two IR philosophies coexist, never unified**: the tagged-tree +
  registry line (UR-AST, pseudoir OpNode+registry) and the flat
  opcode/SSA line (v1's CFG/SSA; PseudoIR v3/v4 compiled-probe
  mining — the line PCv5's compiler-slicing continues). Any "build
  the most advanced" effort must decide their relationship.
- **Precedent for combining exists**: WFL's planning already made
  the harvest decision from v0 — "Mine, don't resurrect" — and
  documents exactly what it took (coverage gate, construct
  handlers, Compose tables) and what it deferred (oracle/fuzzer).
- **The fidelity doctrine appears twice independently** —
  PCv5's uniform-polyfill rule and PseudoIR's
  `compiler_transpilation_experiment.md` boundary rule ("every
  operator on the polyfilled type routes through the simulator, or
  none do") — same law, derived from different bugs. Cross-validated.

## 5. Best-in-class per capability (harvest map)

| Capability | Best holder | Where |
|---|---|---|
| Behavioral verification | v0 oracle + differential fuzzer | `PseudoCoup_v0/tools/pseudokotlin/oracle.py` (297), `fuzz.py` (192) |
| Lowering knowledge as data | pseudoir registry (+ gate-before-emit) | `PseudoIR/pseudoir/registry/data/`, `gate.py` |
| Lowering falsification | v2 runtime prober w/ trap vectors | `PseudoIR/v2/prober/runtime_prober.py` |
| Ingress coverage gate | WFL recorder + justified baseline + driver | `WFL_PseudoCoup/pseudocoup/ingress/coverage.py`, `tools/coverage_baseline.json`, `tools/transpile_wfl.py` |
| Deep-semantics emission | WFL dart emitter (async fixpoint, bounded type resolver, hide injection) | `WFL_PseudoCoup/pseudocoup/egress/dart.py` (3,845) |
| Semantic ledger (emission-driving) | v4/WFL 289-line ledger | `PseudoCoup/pseudocoup/core/ledger.py` |
| Structural ledger (verification) + node identity | v0 structural ledger + idgen/unified | `PseudoCoup_v0/tools/pseudokotlin/ledger.py`, `idgen.py`, `ledger_unified.py` |
| Runtime polyfill breadth | v0 runtime tree (incl. numbers.py int-width) | `PseudoCoup_v0/tools/pseudokotlin/runtime/` |
| Compiler-source ingress + oracle-checked bytes | PCv5 grammar tools + differential | `PseudoCoup_v5/Research/{vocab_transpiler,cpp_ingress}/` |
| Automated node→IR map derivation | PseudoIR v3 mutational solvers | `PseudoIR/v3/scripts/full_matrix_solver.py` + 4 siblings |
| Regression net (cheap) | v4 byte-snapshot tests | `PseudoCoup/tests/test_snapshot.py` + `snapshot_pre_upgrade/` |
| Error-cause instrumentation | WFL error census | `WFL_PseudoCoup/tools/error_census.py` (723) |
| Compile-as-oracle per construct | v0 py2many gate | `PseudoCoup_v0/tools/py2many_kotlin/gate.py` (91) |
| Discipline spec to measure against | v3 12-language × 8-rule matrix | `0_Archive/PseudoCoup_v3/.planning/.archive/initial_discipline_assessment_log.md` |
| Doctrine + post-mortems | old-PseudoIR design docs; PyHaxe failure notes | `0_Archive/PseudoIR/DevComms/.planning/design/`, `0_Archive/PyHaxe/docs/DEVELOPMENT_NOTES.md` |

## 6. Open decisions this survey creates (the owner's)

1. Relationship of the two IR philosophies in the combined
   transpiler (tagged-tree/registry vs flat-opcode mining).
2. Which ledger seeds the hub ledger — assessed in depth in
   `ledger_survey_2026-07-27.md`: no single system is most advanced;
   the composition (what to take from each, component by component)
   is mapped there in §4.
3. Whether combining happens by porting components into one chosen
   base (and which base) or by building a fresh spine that imports
   the harvest map.
