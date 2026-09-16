---
id: hq.research.lean_proof_path_resistant_to_churn.sail_model.strip
level: 4
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.strip
designation: code (method)
node:
    name: strip
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_0_sail_model/node_0_3_3_0_2_strip/CORE_0_3_3_0_2_strip.md
super_node:
    name: sail_model
    path: ../CORE_0_3_3_0_sail_model.md
sub_nodes: []
---

# CORE 0_3_3_0_2 — strip

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.sail_model.strip
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.sail_model.strip

## super_node

- [sail_model](../CORE_0_3_3_0_sail_model.md)

## sub_nodes

*(none yet)*

## definition

`strip(execute_clause) -> LeanExpr`

Input: `def execute_<NAME> ... : SailM ExecutionResult := do ...`. Output: the pure expression each written register holds, as a `LeanExpr` over the read registers left unknown.

Steps, in order:

1. replace each `rX_bits r` read by an unknown named for `r`
2. keep every `let` as a binding of a pure expression
3. take the argument of each `wX_bits rd e` as the value written to `rd`
4. refuse, with the construct named, any clause that reads memory, raises, or branches on machine state this leaf does not model; the refusal is a row

This is the one place the wrapper `SailM` is unpacked; it knows `rX_bits`, `wX_bits`, `let`, `if`, `match` and no instruction.
