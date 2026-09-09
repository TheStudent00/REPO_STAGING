---
id: hq.research.arch_unit_oracle.cross_construction.autopoly
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: autopoly
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/node_0_3_2_2_3_autopoly/CORE_0_3_2_2_3_autopoly.md
super_node:
    name: cross_construction
    path: ../CORE_0_3_2_2_cross_construction.md
sub_nodes: []
---

# CORE 0_3_2_2_3 — autopoly

## metadata

- **id:** hq.research.arch_unit_oracle.cross_construction.autopoly
- **level:** 4
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [cross_construction](../CORE_0_3_2_2_cross_construction.md)

## sub_nodes

*(none yet)*

## definition

AutoPoly, the automated polyfiller: for one dominant operator (a pool
entry) and one target language y, the proved source-level function in
y that computes it — rendered from the entry's term by one renderer
per target, compiled with y's own compiler at ship flags, carved at
the function body, gated against the entry's unit — kept per (entry,
y) with its proof as the polyfill library the Hub's egress composes.
Adopted 2026-09-07 as the research's route to the Hub
(`../../../SUPPORT_BRAINSTORM_autopoly.md`, logs 219, 229).

## what exists

| piece | task | result |
|---|---|---|
| c renderer, the collapse test, the c→c control | o7 (log_218) | 168/204 proved, 193/204 under the caller-extension reading; byte identity 5/204 against a 14/33 control ceiling |
| per-opcode: does the compiler land on the primitive | o8 (log_220) | 197/217 LANDED on c; never: `movb mul pxor xorps` |
| rust renderer and the coverage table | o11 (log_226) | 42 direct / 20 idiom / 0 none; one missing sort `f16`; 243/320 proved, 284/320 under caller extension; 99/107 LANDED; rustc's byte ceiling 69% |
| the preservation theorem, integer subset | L1 (log_227) | proved; the source-level half of derivability |

## what is next, in order (ruled 2026-09-07)

1. **Render the mode**: emit the guard from the ledger's guard-outcome
   rows so a trapping operator traps; re-run the disproved (36 on c,
   59 on rust); the data for the mode-axis ruling.
2. **The synthesis route**, the second producer: compose y's
   arch-units directly, counterexample-guided, no compiler; agreement
   with the compiler route is the oracle.
3. **Size and cycles** of proved emulations against native units: the
   "as fast as slice insertion" claim, measured.
4. **go and swift renderers**, each with its coverage table first.
5. The `mnem` field rename in o2/o8 artifacts; `cmpordss`/`cmpordsd`
   into the shared opcode table.

## artifacts

`~/Programming/PseudoCoupHQ/Research/oracle/cross_construction/emulation/`
(`emulate.py`, `per_opcode/`, `rust/`, `src/`, lane folders).
