---
id: hq.research.lean_proof_path_resistant_to_churn.language.compiler_corpus
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (attribute)
node:
    name: compiler_corpus
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_4_language/node_0_3_3_4_1_compiler_corpus/CORE_0_3_3_4_1_compiler_corpus.md
super_node:
    name: language
    path: ../CORE_0_3_3_4_language.md
sub_nodes: []
---

# CORE 0_3_3_4_1 — compiler_corpus

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.language.compiler_corpus
- **level:** 4
- **status:** draft
- **designation:** code (attribute)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [language](../CORE_0_3_3_4_language.md)

## sub_nodes

*(none yet)*

## definition

`compiler_corpus : list[ArchUnit]`

EVERY compiler-operator of the language, function-wrapped and lowered
(the owner's definition of an arch-unit): one unit per (operator, operand
types) the compiler accepts.

- built: the probe set of the operator pipeline
  (`PRIVATE/PseudoCoupHQ/Research/op_pipeline/lane_gen.py`,
  the `probes` table of each language's lane: one probe per (operator,
  lhs holder, rhs holder), generated from the language's own grammar and
  holders, never typed), each probe through `compile`. A probe the
  compiler refuses is recorded as refused (the compiler's own type
  checker is the acceptance oracle) and is not in the corpus.
- if we take every probe of every language, compile each for riscv64 and
  keep the ones the compiler accepted, that is the set of
  compiler_corpora.

Steps, in order:

1. read the language's probe table
2. for each probe: `compile`
3. keep the units; record every refusal with the compiler's line, so the
   corpus and the refusals together account for every probe

Measured so far for riscv64 (task rv2, 2026-09-11,
`PRIVATE/PseudoCoupHQ/Research/oracle/riscv/attest_rv.json`):
c: the manifest holds 750 probes; the pipeline's own acceptance gate
(the compiler's type checker) refused 250; 500 were compiled for riscv64
and 400 lowered. go: 744 in the manifest, 107 lowered. cpp and rust:
the same route, not yet run for riscv64. The handful of 2026-09-14/15
took all 750 c probes through `compile`: 346 meanings certified, 404
refused (248 float probes the pruned decoder does not know, 140 the
compiler refused, 16 walk shapes).

What a person writes: nothing. Churn: a new compiler is a rerun; a new
operator in the grammar grows the probe table and is a rerun.
