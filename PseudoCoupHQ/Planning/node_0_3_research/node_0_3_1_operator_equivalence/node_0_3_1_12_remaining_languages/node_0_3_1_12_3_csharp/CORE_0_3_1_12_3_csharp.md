---
id: hq.research.remaining_languages.csharp
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: work
node:
    name: csharp
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_12_remaining_languages/node_0_3_1_12_3_csharp/CORE_0_3_1_12_3_csharp.md
super_node:
    name: remaining_languages
    path: ../CORE_0_3_1_12_remaining_languages.md
sub_nodes: []
---

# CORE 0_3_1_12_3 — csharp

## metadata

- **id:** hq.research.remaining_languages.csharp
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

Integration of C# (CoreCLR). We leverage RyuJIT compilation logs (via `COMPlus_JitDisasm`) to formally trace AST nodes through their lowering phases down to exact machine instructions and register allocations. We auto-generate all C# operator probes mechanically via `operator_arity.json` and use the diary/tracing concepts from the `compiler_graph` to prove argument identities, establishing a formal graph path instead of guessing.

## state, 2026-09-06

Designed, not started. Toolchain: the .NET SDK 10.0.400 in the persist volume (`/persist/dotnet`, log_062 §1). Arch-units on disk: none.
The fuzz census (intentions / kind_fuzz_clustering, log_062) ran this
language's operators over its holders and measured behaviour; it did
not produce machine code. The unit boundary rule applies to the
emitted method's body; deoptimization is a recorded mode.
