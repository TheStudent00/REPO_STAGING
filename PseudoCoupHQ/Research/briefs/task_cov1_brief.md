# Task cov1 — how far the PROVED emulations reach: for every language pair (x, y), the share of x's arch-units every one of whose arch-opcodes has a proved emulation in y

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`, ALL of it.
Then `Research/GLOSSARY.md`, `log_265` (rv6: the RISC-V table, 251 of
255), the bank (`certificates.jsonl`: x86 proofs per (cell, target)),
the model table's attestation (`model/model_table_attest.json`: cells
with their unit counts and example units), the ledger / canon stores
under `Research/op_pipeline/` (every unit per language with its
instruction rows; READ ONLY), and for RISC-V: `Research/oracle/riscv/`
(rv2's riscv64-compiled corpus units and `twins.json`;
`construct/general/rv6_all.jsonl` for the proofs). Instance `cov1.conf`
(copy `rv4.conf`). Artifact folder: `Research/oracle/coverage/`; lanes
under `lanes_cov1/`.

## 1. the owner's question, 2026-09-12
"how far would we get if we used only the proven emulations? if we are
connecting languages, how well could one language effectively polyfill?
if we had all of them proven, every arch-opcode can be expressed in
another language but if only some of the arch-opcodes emulated..."

`arch-unit`
- one compiled body of language x from the corpus, with the set of
  arch-opcodes (cells: mnemonic, operand form, width) it contains.
`expressible in y`
- every cell the unit contains has a PROVED emulation on y (the
  destination-only reading, the line's standard), so the whole unit can
  be written in y out of proved pieces.

```
for arch in (x86_64, riscv64):
    for x in languages_with_a_corpus(arch):            # x86: c cpp rust go swift; riscv64: c go (rv2's corpus)
        for unit in units_of(x, arch):
            cells = cells_of(unit)                       # from the ledger / the sweep's attestation, never re-derived
            for y in target_languages(arch):
                expressible[x][y] += all(proved(cell, y, arch) for cell in cells)
        table[x][y] = expressible[x][y] / len(units_of(x, arch))
```

## 2. Report
1. per architecture, the x-by-y matrix: share of x's units expressible
   in y, with the counts ("N of M units") in every cell; the diagonal
   too (x in x: a unit's own cells all proved on its own language).
2. the blocking cells: for each (x, y), the cells that most often make
   a unit inexpressible, top ten, with how many units each blocks — the
   worklist ordering for the proofs still missing.
3. the same matrix under the strict reading beside the destination-only
   one, so the flags' cost is visible.
4. a units-by-length view: expressibility by unit length (1, 2, 3–5,
   6–10, over 10 instructions).
Guard over every json; log (next free number); verifier lane; PROGRESS
on the autopoly node and the riscv64 node; sync-back; instance down.
Memory bound 6g, abort `ABORT_MEMORY_COV1`. No file under
`Research/op_pipeline/` is written. Reply with the two matrices, the
blockers, the length view, every flag LITERAL.
