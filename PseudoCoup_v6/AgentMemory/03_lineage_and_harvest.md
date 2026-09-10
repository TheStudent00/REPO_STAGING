# 03 — Lineage and Harvest

Condensed from the two surveys (full evidence, line-cited):
- `PRIVATE/PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md`
- `PRIVATE/PseudoCoup_v5/DevComms/ledger_survey_2026-07-27.md`

## Version map (identity-corrected)

| Version-state | Where | Character |
|---|---|---|
| v0 | `StressBot/RelevantProjects/PseudoCoup_v0/` | different family: Kotlin→Python, deepest VERIFICATION (oracle, fuzzer, ledgers, idgen); Kotlin test suite passes in Python 160/160 |
| v1 | `0_Archive/PseudoCoup_v1/` | 13-language tree-sitter ingress, 14 emitters, the only CFG/SSA middle-end; daisy-chain roundtrip |
| v2 | `0_Archive/PseudoCoup_v2/` | strip-down checkpoint (1,334 lines); v3's refactor baseline |
| v3 | `0_Archive/PseudoCoup_v3/` | birth of UR-AST (nested, replacing linear IR); 11 ingress / 12 egress; 45-line ledger seed; discipline matrix docs |
| v4 ≡ `PseudoCoup/` | byte-identical pair | 289-line semantic ledger; polyfill_engine; byte-snapshot tests; pseudoir gate (its U2/U3 units unbuilt) |
| WFL | `WFL_Projects/WFL_PseudoCoup/` | deepest emitter (dart.py 3,845: async fixpoint, bounded type resolver, hide injection); ingress coverage gate; error census (15,951→6,323) |
| PCv5 | `PseudoCoup_v5/` | compiler-source ingress (Rust+C++→Python), polyfill law, oracle-checked bytes; the extraction/insertion proof |
| PseudoIR | `PseudoIR/` | five artifacts: pseudoir package (registry + gate-before-emit), v2 (runtime prober/falsification), v3 (mutational opcode solvers), v4 (SSA matrix planning), exp01–09 (pair transpilers + roundtrip harness + doctrine docs) |
| precursors | `0_Archive/{PyHaxe,PseudoDart,PseudoFlutter,PseudoSyntax}` | PyHaxe: largest single emitter + failure catalogue; PseudoDart: emit→analyze→run→assert tiers; PseudoFlutter: two-engine pixel-diff oracle |
| substrate | `SourceIRs/` | ~5.5 GB vendored compiler sources (Go, .NET, Dart SDK, JDK, LLVM, Graal). Keep. |

## Headline

**"Most advanced" is distributed.** No version-state holds the best
of more than two capabilities. The most advanced transpiler and
ledger do not exist yet; their parts do. PCv6 composes them.

## Transpiler harvest map (best-in-class per capability)

| Capability | Holder |
|---|---|
| Behavioral verification | v0 `oracle.py` + `fuzz.py` |
| Lowering knowledge as data + gate-before-emit | pseudoir registry + `gate.py` |
| Lowering falsification | PseudoIR v2 `runtime_prober.py` (trap vectors) |
| Ingress coverage gate | WFL `ingress/coverage.py` + baseline + driver |
| Deep-semantics emission | WFL `egress/dart.py` |
| Compiler-source ingress, oracle-checked | PCv5 `Research/{vocab_transpiler,cpp_ingress}` |
| Automated node→IR map derivation | PseudoIR v3 mutational solvers |
| Cheap regression net | v4 byte-snapshot tests |
| Error-cause instrumentation | WFL `error_census.py` |
| Compile-as-oracle per construct | v0 py2many `gate.py` |
| Discipline spec to measure against | v3 12-language × 8-rule matrix |
| Doctrine + post-mortems | old-PseudoIR design docs; PyHaxe DEVELOPMENT_NOTES |

## Ledger harvest map (combined most-advanced ledger)

Two families never met: semantic (drives emission; 289-line) vs
verification (identity, integrity, divergence taxonomy; v0 tools).
The combined ledger takes:

- primary key: v0 `idgen.py` positional-path ids (highest-value
  single transplant; kills bare-name and anchor keying at once)
- record shape: v0 `ledger_unified.py` superset entry + `check()`
  integrity mode
- semantic payload: the 289-line ledger's registries, re-keyed on
  ids, FQDN as secondary index
- enforcement: 02_ledger specs' three-tier FQDN +
  halt-on-unresolvable, in the refusing style of PCv5's TyCtxt stub
- divergence: one taxonomy merging v0 classify_methods kinds + the
  exp ledger.json reason vocabulary + registry strategy/status as
  confidence
- verification half: v0 exec+introspect + dropped/relocated logic +
  kit_ledger LCS/signature compare, joined on id equality
- registry linkage (design opportunity, no existing code): a
  divergence entry carries a registry op_id + confirmation status,
  making every divergence evidence-backed

## PCv5 assets that stay live (not archived)

- ~~an earlier generated-vocabulary artifact — rustc-verified x86-64
  encoder oracle~~ **REMOVED 2026-07-30**: that artifact and the
  ingestor work reproducing it were built pointing at a retired
  reference backend instead of the settled LLVM/rustc-LLVM
  direction, and were purged as mis-aimed. No longer live in PCv6.
- differential harnesses (`vocab_transpiler/differential/`,
  `cpp_ingress/test_agreement.py`)
- divergence suite, basis audit results, `pc_verdicts.json`
- output ring / rust_cell / import-hook mechanism (insertion proof)
- the three grammar tools — as lessons and as reference for what
  the tree-sitter-based ingress must reproduce
