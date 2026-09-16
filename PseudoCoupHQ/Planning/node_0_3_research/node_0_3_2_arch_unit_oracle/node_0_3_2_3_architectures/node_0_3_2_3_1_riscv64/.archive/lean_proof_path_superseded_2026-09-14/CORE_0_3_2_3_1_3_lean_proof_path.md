---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: lean_proof_path
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/CORE_0_3_2_3_1_3_lean_proof_path.md
super_node:
    name: riscv64
    path: ../CORE_0_3_2_3_1_riscv64.md
sub_nodes:
    - name: sail_model
      path: node_0_3_2_3_1_3_0_sail_model/CORE_0_3_2_3_1_3_0_sail_model.md
    - name: arch_opcode
      path: node_0_3_2_3_1_3_1_arch_opcode/CORE_0_3_2_3_1_3_1_arch_opcode.md
    - name: lean_expr
      path: node_0_3_2_3_1_3_2_lean_expr/CORE_0_3_2_3_1_3_2_lean_expr.md
    - name: arch_unit
      path: node_0_3_2_3_1_3_3_arch_unit/CORE_0_3_2_3_1_3_3_arch_unit.md
    - name: language
      path: node_0_3_2_3_1_3_4_language/CORE_0_3_2_3_1_3_4_language.md
    - name: emulation
      path: node_0_3_2_3_1_3_5_emulation/CORE_0_3_2_3_1_3_5_emulation.md
    - name: dictionary
      path: node_0_3_2_3_1_3_6_dictionary/CORE_0_3_2_3_1_3_6_dictionary.md
    - name: system
      path: node_0_3_2_3_1_3_7_system/CORE_0_3_2_3_1_3_7_system.md
    - name: the_run
      path: node_0_3_2_3_1_3_8_the_run/CORE_0_3_2_3_1_3_8_the_run.md
    - name: emit_measured
      path: node_0_3_2_3_1_3_9_emit_measured/CORE_0_3_2_3_1_3_9_emit_measured.md
---

# CORE 0_3_2_3_1_3 — lean_proof_path

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path
- **level:** 5
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [riscv64](../CORE_0_3_2_3_1_riscv64.md)

## sub_nodes

- [sail_model](node_0_3_2_3_1_3_0_sail_model/CORE_0_3_2_3_1_3_0_sail_model.md) — The ratified Sail RISC-V model as the one source of every definition, read by the sail compiler's Lean backend, never by a person.
- [arch_opcode](node_0_3_2_3_1_3_1_arch_opcode/CORE_0_3_2_3_1_3_1_arch_opcode.md) — One machine instruction the compiler can write, keyed by mnemonic, operand form and width, with its definition as a Lean expression taken from the model.
- [lean_expr](node_0_3_2_3_1_3_2_lean_expr/CORE_0_3_2_3_1_3_2_lean_expr.md) — An expression in Lean over unknowns of fixed width, with one question answerable of any two: are they the same function of their unknowns.
- [arch_unit](node_0_3_2_3_1_3_3_arch_unit/CORE_0_3_2_3_1_3_3_arch_unit.md) — The compiled machine code of one source operator at one type pair, cut out of the binary at its function symbol, with its meaning as a Lean expression computed by Sail's own definitions applied in order.
- [language](node_0_3_2_3_1_3_4_language/CORE_0_3_2_3_1_3_4_language.md) — One language PCHQ covers, with its compiler at ship flags, its corpus of compiled units, and the swap table `operator_for` that pass A fills: which of its own units computes each Sail primitive at each width.
- [emulation](node_0_3_2_3_1_3_5_emulation/CORE_0_3_2_3_1_3_5_emulation.md) — One proved answer: an arch-opcode, a language, the compiled unit that computes the arch-opcode's definition, and the Lean theorem file that proves it.
- [dictionary](node_0_3_2_3_1_3_6_dictionary/CORE_0_3_2_3_1_3_6_dictionary.md) — The table keyed by (language, arch-opcode) whose entries are proved emulations: the line's bank, regenerable from the model and the compilers by running the system.
- [system](node_0_3_2_3_1_3_7_system/CORE_0_3_2_3_1_3_7_system.md) — The three passes over the model and the languages, in one method, producing the dictionary; the loop the owner wrote on 2026-09-13, as code.
- [the_run](node_0_3_2_3_1_3_8_the_run/CORE_0_3_2_3_1_3_8_the_run.md) — Running the system, in the owner's order: a handful first to see that it is making sense, then everything, then the two tests that show it resists churn.
- [emit_measured](node_0_3_2_3_1_3_9_emit_measured/CORE_0_3_2_3_1_3_9_emit_measured.md) — What the sail compiler's Lean backend produced and cost on 2026-09-13, the five lanes of log 274 §3: refused without network on the laptop (the C emulator's build fetches a dependency); stopped by the OS at 6 GB; flat at 16.5 GB for 22 minutes at 16 GB; 47.5 minutes and 17.0 GB on the tower for the wrong (group) module names with no instruction clause emitted; 45.5 minutes and 62,893 lines for the leaf names `I_insts M_insts postlude main`, with `execute_DIV` at `InstsEnd.lean:4362`.

## definition

The proof path for RISC-V that resists churn: Sail's own Lean output is
the definition of every arch-opcode, a compiled unit's meaning is Sail's
own `execute` applied per instruction with the registers unknown, and
every equality is a Lean theorem; nothing in it is written for any
opcode, compiler or language release. Decided with the owner on 2026-09-13 and
banked in `PRIVATE/PseudoCoupHQ/DevComms/log_274_the_lean_proof_path_resistant_to_churn.md` (log 274), which holds the literals, the measured emit
cost and the churn table; this node is that log as a tree.

the owner's criterion, which every leaf below is measured against: "if i stop
making updates to the repo and things that it processes churn, the
system will still be able to re-generate essentially all the proofs,
Hub, and whatever else downstream by running the system"; and "no human
intelligence (LLM or biological) is pointing to a spelling and saying
'that's div!'".

`written once`
- part of the system, like the algorithm: it mentions no opcode, no
  compiler, no language version. The walk, the prover call, the render
  rule, the widening rule, a closed set of once-proved theorems.

`never written`
- anything per opcode, per compiler, per language release. No row in a
  table, no case in a walk.

The module is `Research/oracle/riscv/leanpath/`; each `code (class)`
sub-node is one class in it and each `code (method)` leaf one method,
under the same names. The three passes, as the code will read:

```python
defs = model.definitions()                 # once per model commit
for lang in langs:
    for unit in lang.corpus:
        unit.lean = unit.meaning(defs)     # Sail's execute, composed
# pass A: find what each language already computes
# pass B: build what pass A did not find, prove it the same way
# pass C: units against units across languages (the Hub's claim)
```

What rests on what, with no arrow back up: a dictionary entry rests on
`LeanExpr.equals`, which rests on Lean; both sides rest on
`SailModel.definitions`, which rest on the sail compiler reading the
model; the model is the ratified definition. An emulation is never
proved against itself.
