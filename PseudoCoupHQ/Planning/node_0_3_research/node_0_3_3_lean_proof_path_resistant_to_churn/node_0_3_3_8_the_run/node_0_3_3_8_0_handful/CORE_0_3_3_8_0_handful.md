---
id: hq.research.lean_proof_path_resistant_to_churn.the_run.handful
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: handful
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_8_the_run/node_0_3_3_8_0_handful/CORE_0_3_3_8_0_handful.md
super_node:
    name: the_run
    path: ../CORE_0_3_3_8_the_run.md
sub_nodes: []
---

# CORE 0_3_3_8_0 — handful

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.the_run.handful
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [the_run](../CORE_0_3_3_8_the_run.md)

## sub_nodes

*(none yet)*

## definition

The smallest run that exercises every method once:

1. one language (c): its `compiler_corpus` compiled for riscv64, every
   unit's meaning through Sail
2. pass A over it: the found entries; `operator_for` filled — the
   expected shape is that the `+` probe's meaning proves equal to
   `BitVec.add` at 64, `^` to xor, `<<` to `shift_bits_left`, and the
   table says so with a proof file beside each
3. pass B for three definitions (an add, an xor, a shift): rendered from
   that table only, compiled, read back
4. `equals` on those three, right after each meaning
5. the eye table, read by the owner: does it look right, and what to expect
   from `everything`; `everything` starts only after that read

Done when the table exists and the three proofs close, or the refusal
rows say exactly which primitive has no unit.
