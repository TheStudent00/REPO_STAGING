---
id: hq.research.arch_unit_oracle.architectures.riscv64
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: riscv64
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/CORE_0_3_2_3_1_riscv64.md
super_node:
    name: architectures
    path: ../CORE_0_3_2_3_architectures.md
sub_nodes: []
---

# CORE 0_3_2_3_1 — riscv64

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [architectures](../CORE_0_3_2_3_architectures.md)

## sub_nodes

*(none yet)*

## definition

The second architecture: an exploration, not a pivot (the owner,
2026-09-10: "not that we need a hard pivot ... we could pivot or even
run them in parallel"). The question is how much of the line transfers
untouched, and the answer is measured as a `surface` (lines written
per layer) and as `the claim` (x86 term equals riscv64 term, per unit).

`lifter`
- `Research/oracle/riscv/riscv_reference.py`: RV64I + M (44
  mnemonics, 858 operand variants) in `reference.py`'s own shape; no
  flags register anywhere, so every place is a register.

`level 0 check`
- the ratified Sail model (`Sources/sail-riscv`) run CONCRETELY through
  its C simulator `sail_riscv_sim`, one instruction between loads and a
  store, at edge values first then random points: A CHECK AT POINTS,
  NOT AN EQUALITY. Isla (the symbolic route) builds only against Sail's
  unreleased master and is not in the image.

`carve`, `calling convention`
- `llvm-objdump` with `--mattr=+m,+a,+f,+d,+c` and `-M no-aliases`;
  a0–a7 arrive and a0 answers, fa0–fa7 and fa0 for floats; a narrow
  integer argument is SIGN-EXTENDED to 64 bits by the ABI where x86
  reads its low bits: a contract difference, stated as a constraint.

`transfer by term identity` (rv2)
- RISC-V's own model table; each of its cells twinned to an x86 cell
  when the two terms are equal after `Term.normalize` (or by z3); a
  banked certificate inherited on riscv64 is re-verified by compiling
  its source for riscv64 and gating; the loop runs only over cells with
  no twin.

## state, 2026-09-10

| piece | task | result |
|---|---|---|
| the image | coordinator | rust `riscv64gc-unknown-none-elf`, clang 21, go 1.26, Sail 0.20.2, `sail_riscv_sim`; no riscv64 glibc headers (`-nostdlibinc`) |
| the handful | rv1 (log_258) | ten units carved; the claim 7 equal / 3 differ by contract (ABI extension; `idiv` traps where `divw` defines) / 1 no unit |
| level 0 check | rv1 | 860,304 points, 0 disagreements; 54 refused by name (loads, stores, branches 19; floats 34; auipc 1) |
| the surface | rv1 | 2,644 lines in 5 files, the lifter 1,174 (44%); term store, table, bank, proofs untouched |
| the transfer | rv2 (log_259) | 255 cells; twins 102 at the whole place / 161 at the cell's own width; 734 inherited certificates compiled for riscv64: 103 proved, 0 disproved; the loop over 94 untwinned cells proved 82; 116 of 255 (45.5%) hold a proved riscv64 emulation; the three readings coincide (no flags) at 74 |
| owed | rv3 (brief written) | Zba/Zbb/Zbs in the lifter (27 rows); twins against ref2's corrected table; rust std target, c/cpp headers for riscv64 in the image; the 734 certificates into the bank with `arch` |
