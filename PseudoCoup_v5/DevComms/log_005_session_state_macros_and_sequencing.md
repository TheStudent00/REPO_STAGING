# log 005 — session state: the macro model, sequencing, and the ledgerer's shape

2026-08-04, at the owner's request, so nothing from this stretch of
conversation is lost. This is the index; the detail lives in the
documents each section points at.

---

## 1. What was settled, in order

**The metaprogramming model** — representation always and losslessly;
evaluation as a separate, optional, derived operation. Three kinds of
Rust macro, split by where the definition lives. The full statement is
`PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_metaprogramming.md`;
the measurements and wrong turns are in
`PseudoCoup_v5/DevComms/log_003_metaprogramming_model.md`.

**Churn, measured** (log_003 §6): across 1.56 -> 1.97 (five years, both
recent editions), no stable macro was ever removed; built-ins only grew
(30 -> 42); the `proc_macro` public surface changed by zero lines
across the last two releases. One expansion-shape change found in five
years (`assert_matches!` gaining braces at stabilization). Backwards
compatibility protects what INVOCATIONS are accepted, not what
expansions look like — so the toolchain version is recorded in the
ledger, and re-derivation is rare but real.

**Resolution and names, measured** (log_004): tree-sitter's queries
point every invocation at a name and every in-corpus definition at a
file and line for free; coverage is a corpus question (7.9% in the two
crates, most of the rest becomes readable when `library/core` is added).
A `macro_rules!` template CANNOT compute an identifier, so produced
names are always statically readable for kinds one and two. Kind three
in the target is 149 derive uses, six names, all rustc-internal,
two-thirds `Diagnostic`.

**The syn-shim spike** (log_004 §6,
`PseudoCoup_v5/Research/syn_shim/`): a syn-shaped API
backed by tree-sitter works — demonstrated by reproducing the real
`TryFromU32` expansion for the real `CovmapVersion` enum, output
re-parsing as valid Rust. `rustc_macros` touches ~50 syn types; the
handwork for kind three is three shims (`proc_macro` API, syn slice,
quote templating) plus `synstructure`, and then zero per macro — the
macro bodies are transpiled, not rewritten.

**The compiler is not kind three.** Its source CONTAINS kind-three
invocations, but the macros behind them are defined in
`compiler/rustc_macros` — ordinary Rust in the same checkout,
transpilable.

## 2. The sequencing the owner set

```
1. ledgerer, complete — kinds one and two expanded,
   kind three represented-not-expanded (unresolvable on produced names)
2. transpiler for everything except kind-three bodies
3. transpiler picks up kind-three bodies -> an expansion pass
   upgrades existing ledgers in place
4. complete transpiler
```

- **The PCv5 objective — supporting PseudoIR's transpile/slice/insert
  into the hub — closes at step 2**, resting on one checkable
  judgement: the kind-three macros in the target generate diagnostics
  and serialization, not routing logic (log_004 §5, unverified).
- Whether steps 3–4 land in PCv5 or PCv6 is sequencing the tree can
  state either way; the owner leans toward not postponing macros to PCv6 but
  is flexible.
- The kind-one engine (pattern/template expansion,
  `PseudoCoup_v5/Research/macro_engine.py`) is pulled
  INTO the ledgerer's scope: small, data-driven, and it covers the
  structure-generating macros whose absence leaves dangling names
  (`sdiv`).
- Late arrival is already designed for: expansions upgrade a ledger
  the same way the tracer's runtime connections do — new nodes and
  connectors against existing ids. Nothing is rebuilt.

## 3. Development order inside the ledgerer

the owner's proposed order: ur -> ledger -> ts_to_ur_mapper ->
ur_to_ledger_mapper -> builder. Dependency-correct as stated.

**Raised by the owner at the same time, currently OPEN — two merge
questions:**

- should `ts_to_ur_mapper` + `ur_to_ledger_mapper` have always been one
  `ts_to_ledger_mapper`?
- how would the UR-AST not BE the ledger?

The assessment given (chat, 2026-08-04): the two questions are one
question — is UR a real intermediate layer? — and the data-model half
of the owner's instinct is already the settled design: one vocabulary, one
node shape, the "two trees that never met" finding resolved by layers
on a single tree. What remains genuinely distinct is lifecycle and
mechanics, not representation: UR is per-file and rebuilt by
re-parsing; the ledger is durable, id-keyed, merged across files, and
extended by writers (tracer, expansion pass) that have no UR tree in
hand. Ruling is the owner's; the drift risk he named is real and cuts
toward whichever shape leaves ONE vocabulary with no second copy.

**CLOSED, same day.** the owner ruled: keep the nodes separate, sharpen the
definitions to one data model. Executed 2026-08-04/05: `ur`'s CORE
states it is THE vocabulary; `ledger`'s CORE states it defines no
second vocabulary and owns mechanics (keying, durability, merge); the
suffix question was settled by dropping suffixes — `ts_to_ur` and
`ur_to_ledger` — with the deriver framing moved into `ur_to_ledger`'s
definition text. Checks 0 errors after the renames.

## 4. Standing constraints carried forward

- The prohibition recorded in
  `PseudoCoupHQ/CRANELIFT_IS_BANNED.md` stands; the
  checkout still contains the banned crate's directory (sparse-checkout
  config predates the ban; removal command is in log_003 §1a's context
  and is the owner's to run).
- Six files in the target do not parse under the stock grammar
  (decl_macro syntax); upgrading the grammar does not fix it; the
  cheap fix is a grammar patch, since the pin is already ours.
  `TryFromU32`'s definition and four of its five users sit in those
  files.
- The communication protocol gained §5a (contrast must be visible) and
  §5b (one idea per sentence; the walkthrough test) during this
  stretch. Both are in
  `DevComms/LLM_communication_protocol.md`.
