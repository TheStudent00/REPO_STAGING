---
id: hq.research.arch_unit_oracle.architectures.riscv64.lifter_from_sail
level: 5
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: lifter_from_sail
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_0_lifter_from_sail/CORE_0_3_2_3_1_0_lifter_from_sail.md
super_node:
    name: riscv64
    path: ../CORE_0_3_2_3_1_riscv64.md
sub_nodes: []
---

# CORE 0_3_2_3_1_0 — lifter_from_sail

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lifter_from_sail
- **level:** 5
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [riscv64](../CORE_0_3_2_3_1_riscv64.md)

## sub_nodes

*(none yet)*

## definition

The lifter's table, instruction → definition as a z3 formula per
written register, PRODUCED BY A TOOL from the Sail model on every
run. Nobody types a row. Nobody names an instruction. Created
2026-09-13 on the owner's criterion: "if i stop making updates to the repo
and things that it processes churn, the system will still be able to
re-generate essentially all the proofs, Hub, and whatever else
downstream by running the system"; and "no human intelligence (LLM
or biological) is pointing to a spelling and saying 'that's div!'".

`lifter`
- the reader that turns machine code back into logic: applies each
  instruction's definition in order and returns the formula each
  output register holds. The check receives that formula.
- as it stands: `riscv_reference.py`, 49 instructions typed in by a
  person from Sail's text, checked at 860,304 points against Sail's
  simulator. Every "the lifter has no entry for `bexti`" row in logs
  258–267 is a person in the loop; this node removes the person.

`the generated table`
- every instruction the model defines in the subset the compilers
  target (rv64gc + Zba/Zbb/Zbs + Zicond at least), produced by a Sail
  backend or exporter: Sail's own SMT export, the Lean backend, Isla
  pinned to its Sail version, or a symbolic walk of Sail's
  intermediate form that knows Sail's dozen constructs and nothing
  about any instruction. Any route needing a per-instruction case in
  our code is refused.
- the guard: the point check against the C simulator on every
  generated instruction; a disagreement is a defect in the generator,
  never a row edited by hand.
- the regeneration test: delete the table, run, the table is back.

```
table = generate(sail_model)            # every run; cached by Sail's commit
for instruction in body:
    state = apply(table[instruction], state)   # the lifter, unchanged interface
```

The brief: `Research/briefs/task_sl1_brief.md`.
