---
id: pir.tools.support.slicer
status: projected
---

# SUPPORT — slicer

projected 2026-07-30 from the previous plan, now archived at
`PRIVATE/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_5_slicer/CORE_0_0_5_slicer.md  (208 words)
verdict: substitute
changed: appended the required [SUBSTITUTED] ground-truth block;
  body text carried unaltered (no banned strings appear in the
  source itself — the substitution is about what the node treats
  as ground truth, not its wording).

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
  CPython, typed cells, import hook — the hook part dropped
  2026-07-31, see the hub's SUPPORT_surface.md).
- Harvest: `output_ring.py`, `rust_cell.py`, ~~`pc_import.py`~~, the
  TyCtxt-refusal ledger pattern; PCv5's hand-built slices are the
  worked examples the automation must reproduce.
- **Acceptance**: pointed at the intentions data for integer
  arithmetic, the slicer reproduces the PCv5 end-to-end result —
  hub expression → sliced routing → bytes → executed, grid
  byte-identical to native rustc — WITHOUT hand-chosen slices.
- Depends on: T2, T3, T4, T5.

## Nodes (depth layer, 2026-07-28)

- `node_0_0_5_0_selection` (previous plan)
  — read the intentions artifact, resolve a seam, prune by scope
  filter, emit an ordered slice plan.
- `node_0_0_5_1_extraction` (previous plan)
  — execute a plan through T1/T2/T3/T4; acceptance is behavioral
  equivalence with the four proven PCv5 slices.
- `node_0_0_5_2_insertion` (previous plan)
  — mount and border-cross; platform assumptions become asserted
  rather than implicit.

## [SUBSTITUTED] ground truth

the worked examples this node names as ground truth were cut against
the retired backend and are no longer ground truth. the forward
direction is LLVM / rustc-LLVM; replacement worked examples have to
be re-derived against that target.

## where those nodes went

the previous plan had one `slicer` tool covering all three of these.
this project splits it into three tools, one per stage.

- selection, extraction — `PRIVATE/PseudoIR/Planning/node_0_0_tools/node_0_0_1_slice/SUPPORT_selection_and_extraction.md`
- insertion — `PRIVATE/PseudoIR/Planning/node_0_0_tools/node_0_0_2_insert/SUPPORT_insertion.md`
- the transpile stage was never part of the old slicer; it is
  `PRIVATE/PseudoIR/Planning/node_0_0_tools/node_0_0_0_transpile/`
