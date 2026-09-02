---
id: pcv6.tools.t6_slicer
level: 2
status: settled
settled_by: the owner
supersedes: null
---

# CORE 0_0_5 — T6: Slicer (built last)

The novel component; automation lives here. Consumes the
intentions data (T5) to SELECT what to slice from a source
compiler; drives extraction (T3) and insertion (the proven
output-ring mechanism) into the hub interpreter. Lowering-to-IR
and lowering-to-arch logic enters the hub this way — by running
the transpiled table-generator, never by mining tables (closed
decision).

- Both halves proven separately in PCv5: extraction (compiler
  routing transpiled, byte-identical to native rustc) and
  insertion (mmap/mprotect/ctypes machine code executed in stock
  CPython, typed cells, import hook).
- Harvest: `output_ring.py`, `rust_cell.py`, `pc_import.py`, the
  TyCtxt-refusal ledger pattern; PCv5's hand-built slices are the
  worked examples the automation must reproduce.
- **Acceptance**: pointed at the intentions data for integer
  arithmetic, the slicer reproduces the PCv5 end-to-end result —
  hub expression → sliced routing → bytes → executed, grid
  byte-identical to native rustc — WITHOUT hand-chosen slices.
- Depends on: T2, T3, T4, T5.

## Nodes (depth layer, 2026-07-28)

- [node_0_0_5_0_selection](node_0_0_5_0_selection/CORE_0_0_5_0_selection.md)
  — read the intentions artifact, resolve a seam, prune by scope
  filter, emit an ordered slice plan.
- [node_0_0_5_1_extraction](node_0_0_5_1_extraction/CORE_0_0_5_1_extraction.md)
  — execute a plan through T1/T2/T3/T4; acceptance is behavioral
  equivalence with the four proven PCv5 slices.
- [node_0_0_5_2_insertion](node_0_0_5_2_insertion/CORE_0_0_5_2_insertion.md)
  — mount and border-cross; platform assumptions become asserted
  rather than implicit.
