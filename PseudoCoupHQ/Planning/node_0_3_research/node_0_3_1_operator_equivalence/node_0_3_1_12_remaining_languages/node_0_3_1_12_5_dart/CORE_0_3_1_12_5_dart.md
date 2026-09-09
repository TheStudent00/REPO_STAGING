---
id: hq.research.remaining_languages.dart
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: work
node:
    name: dart
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages/node_0_3_1_12_5_dart/CORE_0_3_1_12_5_dart.md
super_node:
    name: remaining_languages
    path: ../CORE_0_3_1_12_remaining_languages.md
sub_nodes: []
---

# CORE 0_3_1_12_5 — dart

## metadata

- **id:** hq.research.remaining_languages.dart
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [remaining_languages](../CORE_0_3_1_12_remaining_languages.md)

## sub_nodes

*(none yet)*

## definition

Integration of the Dart VM. We leverage Dart VM's optimized compilation logs (via `--print-flow-graph-optimized` and `--disassemble`) to formally trace AST nodes through their lowering phases down to exact machine instructions and register allocations. We auto-generate all Dart operator probes mechanically via `operator_arity.json` and use the diary/tracing concepts from the `compiler_graph` to prove argument identities, building a complete, formal graph path.

## state, 2026-09-06

Designed, not started. Toolchain: the Dart SDK in the persist volume (`/persist/dart-sdk`, log_062 §1). Arch-units on disk: none.
The fuzz census (intentions / kind_fuzz_clustering, log_062) ran this
language's operators over its holders and measured behaviour; it did
not produce machine code. The unit boundary rule applies to the
emitted method's body; deoptimization is a recorded mode.
