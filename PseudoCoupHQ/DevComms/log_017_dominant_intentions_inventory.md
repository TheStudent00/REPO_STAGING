# log_017 — dominant_intentions phase 0 inventory (2026-08-13)

Node: `Planning/node_0_3_research/node_0_3_1_dominant_intentions/`. Measurement
only — no design, no harness building. Three things measured: the Tier-1
registry, the probers, the container toolchains.

## §1 verdict

The runtime-equivalence architecture already exists END TO END at operator
level — a populated 10-op / 2-xform registry with semantic test vectors and
93/120 runtime-confirmed columns — but the probers that populated it are
referenced everywhere and present nowhere in PseudoIR (the `v2/` working tree
they lived in is gone), so phase 1 must rebuild the harness while inheriting
the registry's data shape, and the container can execute 8 of the 11 active
languages today (typescript, kotlin, dart, csharp are the gaps, three of them
cheap).

## §2 registry findings

Files: `PseudoIR/pseudoir/registry/data/{ops.json,xforms.json,schema.md}`.
Per `schema.md` §5 and `pseudoir/registry/__init__.py`, these are packaged
COPIES of a `v2/registry/` working tree that no longer exists in the repo.

### ops.json

- Schema `tier1-v1`; 12-language list (swift still listed 12th).
- **10 op rows**, 5 families: `op.null_coalesce`, `op.safe_call`,
  `op.coalesce_assign`, `op.not_null_assert` (null-safety); `op.destructure`;
  `op.overloaded_binary`; `op.range`; `op.spread_call`; `op.string_interp`;
  `op.match_expr`.
- **Test vectors: 10/10 rows filled** (none empty). Counts per op:
  null_coalesce 4, safe_call 3, coalesce_assign 3, not_null_assert 2,
  destructure 3, overloaded_binary 6, range 4, spread_call 3, string_interp 4,
  match_expr 3 — 35 vectors total. Vectors are `{name, inputs, expect}` with
  `"<raise>"` for expected throws; fracture-trap vectors (e.g. `falsy_trap_zero`)
  exist specifically to reject naive lowerings like `a or b`.
- **Per-language columns: all 120 filled** (10 ops x 12 languages; a column is
  `{source_binding, strategy, lowering, status, evidence}`). Filled is not
  confirmed — status per language:

| language | runtime-confirmed | parse-confirmed | parse-confirmed, runtime-pending | pending |
|---|---|---|---|---|
| python | 10 | 0 | 0 | 0 |
| typescript | 6 | 4 | 0 | 0 |
| java | 10 | 0 | 0 | 0 |
| csharp | 0 | 0 | 3 | 7 |
| go | 10 | 0 | 0 | 0 |
| rust | 10 | 0 | 0 | 0 |
| ruby | 10 | 0 | 0 | 0 |
| php | 10 | 0 | 0 | 0 |
| kotlin | 10 | 0 | 0 | 0 |
| cpp | 7 | 0 | 0 | 3 |
| dart | 10 | 0 | 0 | 0 |
| swift | 0 | 0 | 3 | 7 |

- **Confirmation status totals** (values defined in `_confirmation_status`:
  `runtime-confirmed`, `parse-confirmed`, `pending`, `rejected`, plus the
  compound `"parse-confirmed, runtime-pending"`): runtime-confirmed **93**,
  parse-confirmed **4**, parse-confirmed+runtime-pending **6**, pending **17**,
  rejected **0** (defined but never instantiated). Every `pending` traces to
  "runtime absent in sandbox" — csharp/swift wholesale, cpp partially (the cpp
  runtime has since landed; see §4).
- Strategy ranks: 13 defined in `_strategy_ranks` (`native`, `sugar`,
  `synthetic`, `polyfill`, `fail`, `native_limited`, `native_operator`,
  `method_call`, `native_macro_interp`, `native_spread`,
  `coupled_variadic_spread`, `collection_literal_spread_only`, `manual_unpack`).

One full row verbatim (smallest, `op.not_null_assert`):

```json
{
  "id": "op.not_null_assert",
  "family": "null-safety",
  "signature": "not_null_assert(x: T?) -> T",
  "meaning": "assert x is non-null and yield it as non-nullable; if x is null raise/throw at runtime. This is an assertion, NOT a default -- distinct from null_coalesce.",
  "test_vectors": [
    { "name": "present_passes_through", "inputs": { "x": "A" }, "expect": "A" },
    { "name": "null_raises", "inputs": { "x": null }, "expect": "<raise>" }
  ],
  "columns": {
    "python":     { "source_binding": "hub-notation: node:call function:U.not_null (recognized at ingest; see prober/u_namespace)", "strategy": "polyfill", "lowering": "def not_null_assert(x):\\n    if x is None: raise ValueError(...)\\n    return x", "status": "runtime-confirmed", "evidence": "runtime_results.json op.not_null_assert.python.helper_raise; R4 hub/U.py U.not_null + prober/u_namespace/test_U_results.out 2026-07-14" },
    "typescript": { "source_binding": "node:non_null_expression token:!", "strategy": "native", "lowering": null, "status": "parse-confirmed", "evidence": null },
    "java":       { "source_binding": null, "strategy": "synthetic", "lowering": "T result = Objects.requireNonNull(x, \\\"null\\\");  // (no compiler/jshell available)", "status": "runtime-confirmed", "evidence": "r1_results/r0_java_retry.out 2026-07-14 host run (patched snippet)" },
    "csharp":     { "source_binding": null, "strategy": "synthetic", "lowering": "var result = x!;  // C# nullable annotation, compile-time hint only (like TS !) with no runtime check", "status": "pending", "evidence": "runtime_results.json op.not_null_assert.csharp.pending (runtime absent in sandbox)" },
    "go":         { "source_binding": null, "strategy": "synthetic", "lowering": "if x == nil { panic(\\\"null\\\") }; result := *x", "status": "runtime-confirmed", "evidence": "r0_results/go.out 2026-07-13 host run" },
    "rust":       { "source_binding": null, "strategy": "synthetic", "lowering": "let result = x.expect(\\\"null\\\");  // Option::expect panics on None", "status": "runtime-confirmed", "evidence": "r0_results/rust.out 2026-07-13 host run" },
    "ruby":       { "source_binding": null, "strategy": "polyfill", "lowering": "def not_null_assert(x)\\n  raise RuntimeError, ... if x.nil?\\n  x\\nend", "status": "runtime-confirmed", "evidence": "runtime_results.json op.not_null_assert.ruby.helper_raise" },
    "php":        { "source_binding": null, "strategy": "synthetic", "lowering": "$result = $x ?? throw new RuntimeException('null');  // PHP 8 throw expression", "status": "runtime-confirmed", "evidence": "r0_results/php.out 2026-07-13 host run" },
    "kotlin":     { "source_binding": "node:unary_expression token:!!", "strategy": "native", "lowering": "val result = x!!  // native non-null assertion operator, throws NPE", "status": "runtime-confirmed", "evidence": "r0_results/kotlin.out 2026-07-13 host run" },
    "cpp":        { "source_binding": null, "strategy": "synthetic", "lowering": "template<typename T> T not_null_assert(std::optional<T> x) { if (!x) throw std::runtime_error(...); return *x; }", "status": "pending", "evidence": "runtime_results.json op.not_null_assert.cpp.pending (runtime absent in sandbox)" },
    "dart":       { "source_binding": null, "strategy": "native", "lowering": "var result = x!;  // native non-null assertion, throws at runtime", "status": "runtime-confirmed", "evidence": "r0_results/dart.out 2026-07-13 host run" },
    "swift":      { "source_binding": "node:postfix_expression token:!", "strategy": "native", "lowering": "let result = x!  // force-unwrap, traps at runtime on nil", "status": "parse-confirmed, runtime-pending", "evidence": "runtime_results.json op.not_null_assert.swift.pending (runtime absent in sandbox)" }
  }
}
```

(Note the "many host run" evidence lines: much of the 93 runtime-confirmed
total came from HOST runs on 2026-07-13/14, not in-sandbox — the sandbox of
that era lacked most runtimes.)

### xforms.json

- Schema `xform-v1`; **2 rows**: `xform.named_args` (R1, call-convention) and
  `decl.variadic` (P2). Rows carry richer per-row structure than ops
  (`param_shape_record`, `evaluate_once_caveat`) and use `targets` (not
  `columns`) keyed by the same 12 languages.
- Test vectors: 2/2 rows filled (named_args 5, variadic 2 — 7 total).
- All 24 targets filled. Status both rows identically: **runtime-confirmed 10,
  pending 2** (csharp, swift — same absent-runtime story). Per-language:
  every language 2/2 runtime-confirmed except csharp 0/2 and swift 0/2
  (both pending).

## §3 prober findings — code vs design

**Verdict: the probers exist only as design/record. Zero prober code is
present anywhere in PseudoIR.**

- `find PseudoIR -type d -name 'prober*'` → nothing.
  `parse_prober.py`, `runtime_prober.py`, `demo_pipeline.py`,
  `candidate_alignment.json`, `runtime_results.json` — none exist in the repo.
  `PseudoIR/archive/` is EMPTY; `v5/` is empty; `tests/` is empty.
- The design is fully documented in `pseudoir/registry/data/schema.md` §5:
  "**`parse_prober.py`** fills `source_binding`. It runs a real snippet
  through the language's tree-sitter grammar and checks whether a vendored
  alignment file, `candidate_alignment.json`, correctly predicted which
  grammar node/token realizes the op" and "**`runtime_prober.py`** fills
  `lowering` and `status`. It takes the op's `test_vectors`, executes the
  candidate lowering snippet against a real runtime for that language, and
  checks the output against each vector's `expect` value."
- Why absent: `pseudoir/registry/__init__.py` says the data files "are COPIES
  of v2/registry/ (copied at package build, not moved); **v2/registry/ stays
  the probers' working copy**" — but no `v2/` directory exists in PseudoIR
  today. The research tree that held `prober/u_namespace/`,
  `prober/xform_named_args/`, `prober/range/` etc. (all cited verbatim in
  evidence strings and in `pseudoir/ir.py`: "Every prober demo
  (prober/u_namespace/demo_u_namespace.py, prober/destructure/
  demo_destructure.py, prober/overloaded_ops/demo_overloaded.py, the P2
  demos)...") is gone from the working tree.
- What survives as CODE from that lineage: the registry CONSUMER
  (`pseudoir/registry/__init__.py`, the T1.4 load-and-index API with
  `source_binding` as a column slot) and the `Hoister`
  (`pseudoir/hoister.py`, the R4 statement-hoisting mechanism schema.md §6
  describes). Consumers, not probers.
- Consequence: nothing runs today that can add a row, add a vector, or flip a
  `pending` to `runtime-confirmed`. The registry is a frozen artifact of a
  harness that must be rebuilt.

## §4 container toolchain table (verified by execution, agent lane)

Run: `SandboxDesign/agent/drop/lang_inventory.sh`, 2026-08-13T16:55Z, exit 0,
5.3 s (log `20260813T165519Z__lang_inventory.sh.log`). PRESENT means a real
hello-world executed (or, for typescript/kotlin/csharp/dart, the toolchain
command answered); compile+run verified for java, go, rust, cpp.

| language | status | version | install cost if absent (toolchain skill §4) |
|---|---|---|---|
| python | PRESENT | Python 3.13.14 (/opt/venv) | — |
| typescript | ABSENT (node v22.22.1 present, tsc not installed) | — | trivial: `npm install -g typescript`, seconds, npm registry already allowlisted |
| java | PRESENT | javac 25.0.3 | — |
| csharp | ABSENT (deliberately, per skill §3) | — | heavy: .NET SDK ~200MB+; apt `dotnet-sdk-8.0` or MS feed; Containerfile edit + `./build.sh` |
| go | PRESENT | go 1.26.0 linux/amd64 | — |
| rust | PRESENT | rustc 1.96.1 | — |
| ruby | PRESENT | ruby 3.3.8 | — |
| php | PRESENT | PHP 8.5.4 (cli) | — |
| kotlin | ABSENT | — | moderate: SDKMAN or standalone kotlinc zip (~90MB) + JDK already present; Containerfile edit + `./build.sh` |
| cpp | PRESENT | g++ 15.2.0 (clang-21 also in image) | — |
| dart | ABSENT | — | moderate: Dart SDK tarball/apt (~200MB); Containerfile edit + `./build.sh` |

8 of 11 execute today. Ruby and php are PRESENT despite not appearing in the
skill's §3 image list — the image has drifted ahead of the skill; skill worth
refreshing. (Swift, excluded from the 11: still absent; its probe scripts
exited 127 on 2026-08-13, blocked behind the host-side `allow.sh sync`.)

## §5 gap list — what phase 1 (harness design) must supply

1. **A runtime prober, from scratch.** Nothing executable exists. Phase 1 must
   design the vector-runner: take `{inputs, expect}` vectors, wrap a candidate
   realization per language, execute in the sandbox via the agent lane, diff
   against `expect` (including `"<raise>"`), emit a results file.
2. **A results format.** `runtime_results.json` is cited by ~40 evidence
   strings but does not exist anywhere; phase 1 defines it (or a successor)
   as the evidence store.
3. **An object-level row schema.** ops.json rows are OPERATORS (one signature,
   scalar vectors). Dominant intentions are OBJECTS (boolean, float, integer,
   string, list, dict) — a row must hold a method/behavior surface and
   behavioral-subsumption vectors (fracture points as vectors, per the CORE),
   scaling `tier1-v1` beyond single expressions.
4. **Per-language runner templates for 11 languages** — the harness half the
   old probers embodied: how a vector becomes a compilable/runnable snippet in
   each language (main-wrapper, printing convention for comparing results
   cross-language, raise-detection).
5. **Three toolchain installs** (or explicit deferral): typescript (trivial),
   kotlin and dart (moderate, Containerfile + `./build.sh`). Without them the
   csharp/swift "runtime absent in sandbox" pending-hole repeats for 3 of 11.
   csharp stays a design decision — .NET is deliberately absent.
6. **A vector-synthesis discipline** — the old vectors were hand-written per
   op; the CORE wants synthesized vectors with the hand seeding candidates and
   ruling residue. No tooling for synthesis exists.
7. **An agent-lane orchestration layer** — the lane runs one dropped script
   serially; phase 1 needs a shape for batching N languages x M vectors into
   lane runs and collecting `/out` products back into the tree.
