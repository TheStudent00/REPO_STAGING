# Ledger Survey — 2026-07-27

Companion to `transpiler_survey_2026-07-27.md`. Component-level
assessment of every ledger system in the lineage, toward the most
advanced ledger — most sophisticated at accurately supporting
transpilation (recording intent/identity/types; driving or
verifying emission). Read-and-verified by a survey agent with line
citations; inference marked. Condensed here; full detail per file
below.

---

## 1. Verdict: no single system is most advanced

Two families evolved separately and never met:

- The **semantic family** (v3 seed → `PseudoCoup/pseudocoup/core/ledger.py`, 289 lines; WFL's copy is byte-identical) is the ONLY family that drives emission — eight registries consumed by `egress/dart.py` for real decisions (import `hide` injection, await/async gating, singleton rewrite, enum lowering). Its weaknesses: bare-name keying in two registries (documented last-writer-wins collisions), a spec-violating Dart-ingress write path (bare names into `types`, bypassing FQDN), dead `wrappers`/`memory_erasure` fields (nothing writes them), no identity model, no integrity checking.
- The **verification family** (`PseudoCoup_v0/tools/pseudokotlin/`) holds the identity model, integrity checking, divergence taxonomy, and layout-intent schema — but records nothing any emitter reads; output is Markdown and JSON for humans plus one id-stamping injector.

`ledger_unified.py` is the closest synthesis and names its own gap
(docstring L28–34): the exec+introspect verification half was never
folded into the id-keyed record.

## 2. Component verdict (most advanced implementation per capability)

| Capability | Holder | Evidence |
|---|---|---|
| Semantic emission-driving records | `PseudoCoup/pseudocoup/core/ledger.py` | 8 registries beyond the v3 seed, all consumed by `egress/dart.py`; no competitor drives emission at all |
| Structural verification records | `PseudoCoup_v0/tools/pseudokotlin/ledger.py` (370) | Kotlin static side vs Python side read by EXEC+INTROSPECTION of the transpiled module; `dropped` vs `relocated` connectivity discrimination (L283–288) |
| Cross-side comparison algorithm | `.../kit_ledger.py` (374) | `_lcs` + `_sig_match`: static leaves match by content, dynamic bindings by type+order; instance-count-robust |
| Node identity | `.../idgen.py` (294) | Unconditional positional-path ids (`childIndex:nodeKind`), anchors as metadata never keys, files/dirs as positioned nodes, `check_uniqueness` proved at app scale; ids stamped into emitted output by `inject_emitid.py` |
| UI-layout intent | `.../ui_ledger.py` (518) | abs/rel vocabulary with nothing silently dropped; target-agnostic; explicit policy-vs-geometry honesty boundary |
| Divergence taxonomy | split three ways | in-code kinds: v0 `ledger.py` `classify_methods` (6 kinds, counted); vocabulary breadth: `0_Archive/PseudoIR/archive/experiments/*/ledger.json` sidecars (13 `reason` values, e.g. `pointer-erasure`, `control-flow-unroll`, `type-coercion`); confidence model: pseudoir registry strategy ranks + confirmation statuses |
| Integrity checking | `.../ledger_unified.py` `check()` (L243–281) | the only `--check` anywhere: ids globally unique, every id exactly once, entry_count == node count, nonzero exit on failure |
| Serialization discipline | `PseudoCoup/.../ledger.py` `dump`/`load` | set/tuple round-trip fidelity; `async_required` deliberately NOT serialized ("stale on reload, always recomputed") |
| Schema specs | `0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/` | **more advanced than any implementation**: three-tier FQDN down to parameter scope (no implementation reaches it); the wrapper injection/erasure handshake (unimplemented); the halt-on-unresolvable Discipline Violation rule (no implementation enforces it) |
| Type-oracle posture | `PseudoCoup_v5/Research/rust_routing/ledger.py` (57) | the only rejecting write path and raising `type_of` — refuses rather than guesses; conceptually the most advanced idea at the smallest scale |

Out of scope, confirmed: `StressBot/StressBot/core/ledger.py` is an
app-state exploration graph, no transpilation content.

## 3. Registry vs ledger (pseudoir)

- The pseudoir registry is NOT a ledger. Registry = class-level,
  program-independent steering data keyed (op_id, target language):
  "how does this construct lower in that language, with what
  confidence and evidence." Ledger = instance-level, per-program
  record keyed by identity/scope: "what type/shape does THIS
  identifier have in THIS program."
- The registry's epistemics lead everything: 13 strategy ranks, 4
  confirmation statuses, evidence pointers into executed runtime
  results, adversarial test vectors kept even when rejected.
- Design opportunity (inference, no existing linkage found): a
  ledger divergence entry should carry a registry op_id + status, so
  "why does this node diverge" resolves to a confirmed lowering with
  evidence rather than prose. pseudoir itself has no ledger at all.

## 4. What a combined most-advanced ledger takes from each

- **Primary key**: `idgen.Record` positional-path ids for every
  entry — the single highest-value transplant; replaces bare-name
  and anchor keying at once.
- **Record shape**: `ledger_unified.build`'s superset entry
  `{id, file, node_kind, anchor, span, ui, connectivity}` plus a new
  `semantic` slot.
- **Semantic payload**: the 289-line ledger's registries
  (method_returns/suspend, async_required, symbol_owners,
  singletons, param_shapes), re-keyed on ids with FQDN kept as a
  secondary index for call sites that only know a name.
- **Keying rule**: the spec's three-tier FQDN (global/class/
  parameter) as the secondary index; the halt-on-unresolvable rule
  as posture, implemented in the rejecting style of the PCv5
  TyCtxt ledger.
- **Integrity**: `ledger_unified.check()` verbatim, extended with a
  coverage invariant (every emitted node traces to a ledger id) and
  a semantic invariant (every declaration id has a type or an
  explicit `unresolvable` marker).
- **Divergence**: one enumerated taxonomy merging the three
  vocabularies, with registry strategy/status as the per-divergence
  confidence field.
- **Verification half**: v0's exec+introspect and dropped/relocated
  logic plus kit_ledger's LCS/signature comparison, joining on id
  equality (id-in-output already demonstrated by
  `inject_emitid.py`).
- **Layout intent**: `ui_ledger._norm` unchanged, with an explicit
  `layer` field preserving the policy-vs-geometry boundary.
- **Wrapper/erasure**: implement the spec's handshake for real,
  sourcing wrapper ids from registry op ids so the
  anti-hallucination constraint is mechanical.

## 5. Open decision (the owner's)

Composition confirmed as the right frame (the three-way seed choice
in `plan_llvm_rust_2026-07-27.md` §3 is superseded by §4 above):
the combined ledger is id-keyed (v0 identity), superset-shaped
(unified), semantically loaded (289-line), spec-enforced (02_ledger
schemas), refusal-postured (PCv5 TyCtxt). Whether to build it as its
own component now or grow it inside the intermediate (Rust/LLVM)
goal is the scheduling call.
