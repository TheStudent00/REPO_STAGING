---
id: hq.research.remaining_languages
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: remaining_languages
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages/CORE_0_3_1_12_remaining_languages.md
super_node:
    name: operator_equivalence
    path: ../CORE_0_3_1_operator_equivalence.md
sub_nodes:
    - name: ruby
      path: node_0_3_1_12_0_ruby/CORE_0_3_1_12_0_ruby.md
    - name: php
      path: node_0_3_1_12_1_php/CORE_0_3_1_12_1_php.md
    - name: v8
      path: node_0_3_1_12_2_v8/CORE_0_3_1_12_2_v8.md
    - name: csharp
      path: node_0_3_1_12_3_csharp/CORE_0_3_1_12_3_csharp.md
    - name: kotlin
      path: node_0_3_1_12_4_kotlin/CORE_0_3_1_12_4_kotlin.md
    - name: dart
      path: node_0_3_1_12_5_dart/CORE_0_3_1_12_5_dart.md
---

# CORE 0_3_1_12 — remaining_languages

## metadata

- **id:** hq.research.remaining_languages
- **level:** 3
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [operator_equivalence](../CORE_0_3_1_operator_equivalence.md)

## sub_nodes

- [ruby](node_0_3_1_12_0_ruby/CORE_0_3_1_12_0_ruby.md) — Ruby's route into the corpus: the interpreter shape.
- [php](node_0_3_1_12_1_php/CORE_0_3_1_12_1_php.md) — PHP's route into the corpus: the interpreter shape.
- [v8](node_0_3_1_12_2_v8/CORE_0_3_1_12_2_v8.md) — Integration of the JavaScript V8 Engine.
- [csharp](node_0_3_1_12_3_csharp/CORE_0_3_1_12_3_csharp.md) — Integration of C# (CoreCLR).
- [kotlin](node_0_3_1_12_4_kotlin/CORE_0_3_1_12_4_kotlin.md) — Kotlin's route into the corpus: the JIT shape by way of the JVM.
- [dart](node_0_3_1_12_5_dart/CORE_0_3_1_12_5_dart.md) — Integration of the Dart VM.

## definition

The per-language route, one sub-node per language, for the target
languages that have no arch-unit corpus: how each one's operators
become arch-units, given that none of them compiles
our wrapper function to a machine-code body the way c, cpp, go, rust
and swift do. Each sub-node names the toolchain, the evidence route
(handler body, or JIT dump), what is on disk, and what is blocked.

Moved under operator_equivalence 2026-09-06; it was the research
node's seventh co-node. Java and cpython have no sub-node here
because their units were produced on the interp_feeder route
directly ([interp_feeder](../node_0_3_1_11_interp_feeder/CORE_0_3_1_11_interp_feeder.md)
§3); typescript rides with v8.

## 1. The two shapes, and which language has which

- **Interpreter shape**: the operator's machine code is a handler
  function inside the interpreter binary. The unit is that
  function's body (the owner, 2026-09-04). Languages: ruby, php, cpython.
  Locating WHICH handler a probe reaches needs the diary over the
  interpreter's source, the same instrument the compiler graph uses.
- **JIT shape**: the operator's machine code is emitted at run time
  after warm-up. The unit is the emitted code for the probe method,
  read from the JIT's own dump switch, carved at the method's body.
  Languages: java (HotSpot C2), kotlin (the JVM, so java's route
  after kotlinc), c# (RyuJIT, `DOTNET_JitDisasm`), dart (the Dart VM,
  `--disassemble`), javascript/typescript (V8 TurboFan,
  `--print-opt-code`). Deoptimization is a MODE, recorded, not a
  defect.

## 2. State per language, 2026-09-06

| language | shape | toolchain in Airlock | arch-units on disk | route status |
|---|---|---|---|---|
| ruby | interpreter | ruby 3.3.0 instrumented build (`Airlock/ruby-3.3.0.tar.gz`) | 4 (`rb_fix_plus`, `rb_int_plus` with bodies; `rb_big_plus`, `vm_opt_plus` without) | handler slices (logs 095, 113); operator set not generated |
| php | interpreter | php 8.3.0 / 8.2.13 / 7.4.33 builds | 4 (`ZEND_ADD_*_HANDLER` ×3, `add_function`) | as ruby |
| v8 (javascript, typescript) | JIT | node in the image; typescript checker in `/persist` | 0 | designed only (§3) |
| csharp | JIT | .NET SDK 10.0.400 in the persist volume (`/persist/dotnet`, log_062 §1) | 0 | designed only (§3) |
| kotlin | JIT via JVM | kotlinc in `/persist/kotlinc` | 0 | java's route after kotlinc; not started |
| dart | JIT | Dart SDK in the persist volume (`/persist/dart-sdk`, log_062 §1) | 0 | designed only (§3) |

The fuzz census (intentions / kind_fuzz_clustering, logs 052 to 062)
DID run all twelve languages; that measured behaviour, not machine
code, and is the population for those languages' operator MODES,
not their arch-units.

## 3. The designed route for the JIT languages (v8, csharp, dart)

Written into the three sub-nodes 2026-08 and unchanged: probes
generated from `operator_arity.json` as for the compiled languages;
the probe method warmed until the optimizing tier compiles it; the
tier's own dump read for the emitted code and the register
assignment; argument identity proved by the diary over the JIT's
source, never guessed. The unit boundary rule applies unchanged:
the emitted method's body.

## 4. Open

- Not a decision: generate each interpreted language's probe set
  and locate handlers by diary; the JIT dumps for v8 and dart on the
  toolchains already present.
- Order among these languages is the owner's; the SUPPORT scaling design
  (operator_equivalence) ruled cpython first (2026-08-26).

## record

- artifacts: `PseudoCoupHQ/Research/op_pipeline/`
  (`build_op_units_{php,ruby}.py`, `canon_interp_units_ruby_php.json`,
  `interp_php.md`); emitters for the fuzz census in
  `PseudoCoupHQ/Research/kind_fuzz_clustering/`.
- logs: 062 (the remaining eight emitters, fuzz line), 095, 113
  (ruby and php handler slices).
