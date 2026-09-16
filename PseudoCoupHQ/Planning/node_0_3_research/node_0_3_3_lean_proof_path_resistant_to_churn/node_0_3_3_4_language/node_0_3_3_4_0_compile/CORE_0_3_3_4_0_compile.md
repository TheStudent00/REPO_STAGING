---
id: hq.research.lean_proof_path_resistant_to_churn.language.compile
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: compile
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_4_language/node_0_3_3_4_0_compile/CORE_0_3_3_4_0_compile.md
super_node:
    name: language
    path: ../CORE_0_3_3_4_language.md
sub_nodes: []
---

# CORE 0_3_3_4_0 — compile

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.language.compile
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [language](../CORE_0_3_3_4_language.md)

## sub_nodes

*(none yet)*

## definition

`compile(language, source, symbol) -> ArchUnit | Refusal`

Input: the source text of one function-wrapped operator (a probe of the
operator pipeline, or a rendered emulation) and the symbol of its
function. Output: the `ArchUnit`: that function's words in address
order, cut out of the object at the symbol.

Steps, in order:

1. write the source into a work directory under the name the language's
   compiler accepts (`unit.c`, `unit.cpp`, `unit.rs`; go: a module
   directory with a `go.mod`) — plumbing
2. run `language.compiler`, the invocation at the corpus's own ship
   flags for riscv64 (`-O1`; the line is the language's one attribute a
   person wrote)
3. disassemble the object and cut from the symbol's first word to its
   return (`carve`); go spells the symbol `main.<symbol>`
4. return the unit (language, source, symbol, words); a compiler
   refusal returns a `Refusal` carrying the compiler's first error line,
   never a retry with an edited source

Home: `Research/oracle/riscv/leanpath/leanpath/walk.py`, `compile_unit`
and `carve` — kept as they are. Measured on the set they were built for
and on this node's set: 1,040 printed emulations of the retired run of
2026-09-14 (not arch-units; the owner, log 279 §7), and c's 750 probes of the
handful (lane l52, 2026-09-15).

On the name of what comes out: an `ArchUnit` only when the source is a
function-wrapped compiler-operator (the owner's definition). When the source
is a rendered emulation, the lowered body is NOT an arch-unit (the owner,
2026-09-14); the code calls it a lowered body and its name is the owner's to
give (`lowered_emulated_arch_opcode` was proposed in log 279 §1).

Refusals: the compiler's, verbatim; a symbol not found in the object.
