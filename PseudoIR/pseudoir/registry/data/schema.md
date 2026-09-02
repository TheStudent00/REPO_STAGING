# ops.json Schema

`ops.json` is DATA, not code. It is a Tier-1 operator registry: a catalog of small cross-language operators (like null-coalescing), each with a language-neutral definition and, per language, a record of how that language realizes the operator. Two probers write into this file, and one consumer (`demo_pipeline.py`) reads from it. This document describes the shape of the file as it stands today.

## 1. Top-level keys

`ops.json` is a single JSON object with six top-level keys.

| key | type | purpose |
|---|---|---|
| `_doc` | string | Human-readable description of the whole file, embedded in the data itself. |
| `_schema_version` | string | Version tag for this schema. Current value: `"tier1-v1"`. |
| `_strategy_ranks` | object | Definitions of the strategy values a column's `strategy` field can hold (see section 4). Started at five; grown as later work units added ranks — as of P2 (2026-07-14) there are thirteen (`native`, `sugar`, `synthetic`, `polyfill`, `fail`, `native_limited`, `native_operator`, `method_call`, `native_macro_interp`, `native_spread`, `coupled_variadic_spread`, `collection_literal_spread_only`, `manual_unpack`). Section 4 documents the original five; the rest are defined verbatim in `_strategy_ranks` itself and in the REPORT for the unit that added them. |
| `_confirmation_status` | object | Definitions of the status values a column's `status` field can hold (see section 4). |
| `languages` | array of strings | The fixed list of target languages every op is scored against. Currently: `python`, `typescript`, `java`, `csharp`, `go`, `rust`, `ruby`, `php`, `kotlin`, `cpp`, `dart`, `swift` (12 languages). |
| `ops` | array of objects | The op rows themselves (see section 2). As of P2 (2026-07-14) there are 10 rows across 5 families: `op.null_coalesce`, `op.safe_call`, `op.coalesce_assign`, `op.not_null_assert` (`null-safety`); `op.destructure` (`destructuring`, R2); `op.overloaded_binary` (`operator-overloading`, R3); `op.range` (`ranges`, P2); `op.spread_call` (`spread`, P2); `op.string_interp` (`interpolation`, P2); `op.match_expr` (`multiway-branch`, P2). Some rows carry extra sibling fields beyond the five in section 2 — e.g. `non_goals`, `parameters` (op.range), `operators` (op.overloaded_binary), `exhaustiveness` (op.match_expr), `requires_statement_hoisting` (op.destructure); these are per-op annotations, documented in each op's own entry. The declaration-side sibling registry `xforms.json` (schema `xform-v1`) holds call-convention transforms `xform.named_args` (R1) and `decl.variadic` (P2). |

## 2. Shape of one op row

Each entry in `ops` is an object with five fields.

| field | type | meaning |
|---|---|---|
| `id` | string | Unique identifier, dotted form. Example: `"op.null_coalesce"`. |
| `family` | string | Grouping label. All four current ops use `"null-safety"`. |
| `signature` | string | Type signature in a language-neutral pseudo-notation. Example: `"null_coalesce(lhs: T?, rhs: T) -> T"`. |
| `meaning` | string | Prose definition of the operator's semantics, including any traps the vectors are designed to catch. Example, from `op.null_coalesce`: "evaluate lhs; if lhs is null/None yield rhs, else yield lhs. MUST NOT treat falsy-but-non-null values (0, '', false, empty list) as absent." |
| `test_vectors` | array of objects | The semantic test cases used to confirm a lowering actually implements the meaning (see below). |
| `columns` | object | One entry per language in `languages`, keyed by language name (see section 3). |

### Shape of one test vector

Each entry in `test_vectors` has three fields: `name` (string identifier for the case), `inputs` (object of named argument values), `expect` (the value the op must produce for those inputs, or the string `"<raise>"` for cases expected to throw/raise).

Example, from `op.null_coalesce.test_vectors`:

| name | inputs | expect |
|---|---|---|
| `null_yields_rhs` | `lhs: null, rhs: "B"` | `"B"` |
| `present_yields_lhs` | `lhs: "A", rhs: "B"` | `"A"` |
| `falsy_trap_zero` | `lhs: 0, rhs: 99` | `0` |
| `falsy_trap_emptystr` | `lhs: "", rhs: "X"` | `""` |

The `falsy_trap_*` vectors exist specifically to reject a lowering like `a or b`, which would incorrectly return `99` and `"X"` instead of `0` and `""`. This is why `ruby`'s column for `op.null_coalesce` (lowering `a || b`) is flagged as `"naive_or"` in its evidence string even though its status is `runtime-confirmed` — it passed the vectors in this registry's current form, but the naming records that the lowering relies on Ruby's `||` treating only `nil`/`false` as absent, not the general falsy set other languages worry about.

## 3. Shape of one column

A column is one language's realization of one op — the value at `ops[i].columns.<language>`. It has five fields.

| field | type | meaning |
|---|---|---|
| `source_binding` | string or `null` | The parser-level identity of the language's native syntax for this op, in the form `node:<grammar-node> token:<literal-token>`, or `null` if there is no native syntax to bind to (synthetic/polyfill/fail cases). |
| `strategy` | string | One of the five ranks defined in `_strategy_ranks` (section 4). |
| `lowering` | string or `null` | The actual code snippet used to realize the op in this language, or `null` when the op is `native` and self-evident (no lowering snippet needed beyond the source binding itself). |
| `status` | string | One of the confirmation statuses defined in `_confirmation_status` (section 4), sometimes compounded (e.g. `"parse-confirmed, runtime-pending"`). |
| `evidence` | string or `null` | Pointer to where the confirmation was recorded — typically a dotted path into `runtime_results.json`, or `null` when no runtime evidence exists yet (native, self-evident cases). |

Real example — `ops[0]` (`op.null_coalesce`), column `python`:

```json
{
  "source_binding": null,
  "strategy": "synthetic",
  "lowering": "(a if a is not None else b)",
  "status": "runtime-confirmed",
  "evidence": "runtime_results.json op.null_coalesce.python.correct_conditional"
}
```

Reading this row: Python has no dedicated null-coalescing operator, so `source_binding` is `null`. The registry instead emits the inline expression `(a if a is not None else b)` — that is the `strategy: "synthetic"` case defined in section 4. `status: "runtime-confirmed"` means this exact snippet was executed against all four test vectors for `op.null_coalesce` and passed, and `evidence` points at the specific result record `op.null_coalesce.python.correct_conditional` inside `runtime_results.json`.

Contrast with `ops[0]`, column `typescript`:

```json
{
  "source_binding": "node:binary_expression token:??",
  "strategy": "native",
  "lowering": null,
  "status": "parse-confirmed",
  "evidence": null
}
```

TypeScript has a dedicated `??` operator, so `source_binding` names the tree-sitter grammar node (`binary_expression`) and token (`??`) that a parser confirmed exists in a real snippet. Because the operator is native and self-evident, `lowering` is `null` (there is nothing to synthesize) and `evidence` is `null` (no `runtime_results.json` entry — parsing was the only confirmation performed).

## 4. Strategy ranks and confirmation statuses

### `_strategy_ranks`

Quoted directly from `ops.json._strategy_ranks`, with one example drawn from the actual op rows for each.

| rank | definition (verbatim from `ops.json`) | example from this registry |
|---|---|---|
| `native` | "the language has a dedicated operator/syntax whose runtime semantics already match the op's vectors. example: kotlin '?:' for op.null_coalesce." | `op.null_coalesce.columns.kotlin`: `source_binding: "node:binary_expression token:?:"`, `lowering: "val result = a ?: b"`. |
| `sugar` | "a thin built-in shorthand that lowers to an already-present op with matching semantics, no helper needed. example: coalesce_assign 'x ??= y' as sugar for 'x = x ?? y' where both exist." | No column in the current data is tagged `sugar`; the definition exists in `_strategy_ranks` as a rank but is not yet instantiated by any of the 4 ops x 12 languages = 48 columns. |
| `synthetic` | "no dedicated operator; the op is emitted as a small inline expression built from other ops that DOES pass the vectors. example: python null_coalesce lowered to a conditional expression '(a if a is not None else b)' -- NOT 'a or b', which fails the falsy vector." | `op.null_coalesce.columns.python`, shown in full in section 3 above. |
| `polyfill` | "requires a named helper function/import emitted alongside the call site. example: a language with no inline conditional would get a helper 'def _coalesce(a,b): ...'." | `op.not_null_assert.columns.python`: `lowering: "def not_null_assert(x):\n    if x is None: raise ValueError(...)\n    return x"` — a named helper function, not an inline expression. |
| `fail` | "the op cannot be realized in this language with matching semantics; no lowering known." | `op.safe_call.columns.cpp`: `lowering: "N/A -- no native optional chaining in C++17; a std::optional-based helper would require per-call-site lambda wrapping or a member-pointer template, which is convoluted and not representative of a clean lowering."` |

### `_confirmation_status`

Quoted directly from `ops.json._confirmation_status`, with one example each. Note the registry also uses a compound value, `"parse-confirmed, runtime-pending"`, which is not a separate key in `_confirmation_status` but a concatenation of `parse-confirmed` (source binding confirmed) with the runtime half still `pending`.

| status | definition (verbatim from `ops.json`) | example from this registry |
|---|---|---|
| `runtime-confirmed` | "the lowering template was executed on a real runtime in-sandbox and passed every semantic vector." | `op.null_coalesce.columns.cpp`: `strategy: "synthetic"`, `lowering: "std::optional<T> a = ...; T result = a.value_or(b);"`, `evidence: "runtime_results.json op.null_coalesce.cpp.optional_value_or"`. |
| `parse-confirmed` | "the source binding (grammar node/token) was confirmed present by parsing a real snippet with the real tree-sitter grammar; runtime not exercised." | `op.null_coalesce.columns.typescript`, shown in full in section 3 above — `source_binding` is set, `lowering` and `evidence` are `null` because only parsing was performed. |
| `pending` | "neither runtime nor parse confirmation performed in-sandbox (e.g. no wheel/runtime available); a ready-to-run snippet is provided for host execution." | `op.null_coalesce.columns.java`: `status: "pending"`, `evidence: "runtime_results.json op.null_coalesce.java.pending (runtime absent in sandbox)"` — the lowering snippet (`T result = (a != null) ? a : b;`) is present and ready to run on a host with a JVM, but no JVM was available in-sandbox. |
| `rejected` | "a candidate binding or lowering was tried and FAILED (wrong node type, or lowering failed a vector). kept as evidence, not hidden." | No column in the current 4-op data carries a bare `rejected` status; the `_confirmation_status` entry documents the outcome for when a prober's candidate binding or lowering fails a vector, and the intent (per `_doc`) is to keep that failure recorded rather than delete the row. |

The compound status `"parse-confirmed, runtime-pending"` appears on columns where the source binding was confirmed by the parser but the runtime prober had no runtime available in-sandbox — e.g. `op.null_coalesce.columns.csharp`: `source_binding: "node:binary_expression token:??"` (parse-confirmed) combined with `evidence: "runtime_results.json op.null_coalesce.csharp.pending (runtime absent in sandbox)"` (runtime-pending).

## 5. How the probers and the pipeline use columns

Two probers populate a column's fields in two separate passes, and one consumer reads the finished columns.

- **`parse_prober.py`** fills `source_binding`. It runs a real snippet through the language's tree-sitter grammar and checks whether a vendored alignment file, `candidate_alignment.json`, correctly predicted which grammar node/token realizes the op. A successful match produces the `node:... token:...` string seen in `source_binding` and sets `status` to `parse-confirmed` (or the parse-confirmed half of a compound status). If the predicted node type is wrong, that attempt is recorded as `rejected` per `_confirmation_status`, not discarded.
- **`runtime_prober.py`** fills `lowering` and `status`. It takes the op's `test_vectors`, executes the candidate lowering snippet against a real runtime for that language, and checks the output against each vector's `expect` value. All vectors passing sets `status` to `runtime-confirmed` and writes the pointer into `evidence` (into `runtime_results.json`); a runtime being unavailable in-sandbox leaves `status` as `pending` with an evidence note explaining why (e.g. `"(runtime absent in sandbox)"`); a vector failing sets `status` toward `rejected`.
- **`demo_pipeline.py`** consumes the finished columns as its only source of per-language operator behavior: for a given op and target language it reads `columns.<language>.lowering` (or treats the op as native via `source_binding` when `lowering` is `null`) to know what code to emit, and reads `columns.<language>.status`/`strategy` to decide whether that emission is trustworthy enough to use as-is or should be flagged as unconfirmed/pending in its output.

## 6. The `requires: statement_hoisting` contract (R4)

Some op columns cannot be realized as a target EXPRESSION — the only honest lowering is one or more target STATEMENTS. The clearest case is Go's `op.null_coalesce`: Go has no null-coalescing operator and no ternary, so the realization is an `if` statement (`h := a; if a == nil { h = b }`). A statement cannot sit inside a larger expression, so any such op that appears in expression position must be HOISTED: its statements run before the enclosing statement, and a plain temporary variable stands in its place in the expression.

A column whose `strategy` is `synthetic` AND whose lowering is statement-shaped (not an inline expression) carries the contract `requires: statement_hoisting`. Concretely this is the field already spelled `requires_statement_hoisting` on `op.destructure` (the R2 Java column) and, from R4 forward, the same contract binds every synthetic_stmt column across ops — Go's `op.null_coalesce`, `op.safe_call`, `op.not_null_assert`, and any future statement-only column. The contract means: this column's emitter MUST route the op through the ONE shared hoisting mechanism, never a bespoke per-op hoist.

The single mechanism is `prober/u_namespace/hoist.py` (`Hoister`), built in R4. Its interface, mechanically: `Hoister.hoist_stmt(stmt_lines, result_expr) -> (temp_name, ...)` appends target statement lines (with `@TMP@` replaced by a fresh temp name) to an accumulating `prelude` list and returns the fresh temp to use in the enclosing expression; sub-expressions are hoisted depth-first so their preludes run first, preserving left-to-right evaluation order. The double-hoist case — `total = U.coalesce(a, 0) + U.coalesce(b, 0)` — proves it: two statement-only ops in one expression produce two temps (`_h0` from `a`, `_h1` from `b`, in source order) and a final `total := _h0 + _h1`, executed and agreeing with the CPython oracle (`prober/u_namespace/u_r4_results.out` STAGE 4b/5c). The five ad-hoc hoisting mechanisms in WFL_PseudoCoup V3 are slated to collapse onto this one (PLAN.md X1).
