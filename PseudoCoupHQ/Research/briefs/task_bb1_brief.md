# Task bb1 — the bit-blast route: every RISC-V definition turned into an and-or-not circuit by z3 itself, no authored arithmetic, beside the backstop in one table

Priority (the owner, 2026-09-12): "we dont need it as an immediate product but
it is high priority. place it just behind the rest of work." So: after
the RISC-V rows now open (the walk that follows branches; the lifter's
missing mnemonics; the float bit-cast node; the remu refusal), and
before any new line.

Law: `PRIVATE/PseudoCoupHQ/Research/LAW.md`. Then
`Research/GLOSSARY.md`, `log_262` (t4), `log_264` (rv5),
`construct/general/build.py` (the authored constructions this route
stands beside), `render_general.py`.

## 1. What this is
`bit-blast`
- z3's own tactic: any bit-vector formula becomes a propositional
  circuit of and, or, not (and xor) over the input BITS, one gate at a
  time, by z3, with no adder, multiplier or divider ever written by a
  person. Correct by z3's own construction, which we already trust as
  the checker.
- rendered: each gate becomes one boolean operation in the target
  language on single bits (or packed 64 per word by the renderer, which
  is optional); every node named; the language's own operator wins
  where it exists (whoever gets there first), exactly as the backstop.

```
for cell in riscv_cells (255):                       # the definitions, from the lifter
    circuit = z3.Tactic('bit-blast')(cell.term)      # gates over input bits, by z3
    for lang in (c, cpp, go, rust):
        source = render_gates(circuit, lang)         # one line per gate, named
        verdict = gate(carve(compile(source)) == cell.term)
```

## 2. What to measure
Per language, of 255: proved / disproved / undecided / refused, beside
the backstop's own column (rv5, log_264) and the native route's; the
circuit sizes (gates per definition); the compiled body sizes; the
seconds per check. The three routes in ONE table with "of 255" on every
row. The multiply and divide checks are expected to run out here as
they do on the backstop; say where, LITERAL.

## 3. Discipline
One process; guard; log; verifier; PROGRESS on the riscv64 node and the
simplification node; sync-back; instance down. Memory bound 6g, abort
`ABORT_MEMORY_BB1`. Nothing under `Research/op_pipeline/` touched.

## 4. Added 2026-09-12 05:00 UTC, on the owner's word ("we might as well just do it now")
- Runs NOW, on RISC-V, all 255 arch-opcodes, on c, cpp, go, rust (rv3's
  compile routes via `inherit_rv3.install()`, as `rv6_all_langs.py`
  does; swift has no riscv64 SDK: a flag). One process; no pool.
- The sample of the cost is in the tower log of
  `lanes_bb/bb0_l1_bit_blast_sample.sh`: a 64-bit divide with its cases
  is 13,700 gates in 0.09 s; add is 320 gates. So blasting is free and
  the cost is the compile of the gate source and the check of the
  compiled body. Store, per attempt, the gate count, the source line
  count, the compile seconds, the carved body's instruction count AND
  ITS TEXT (the owner wants bodies comparable across languages next), the
  check's outcome and seconds.
- The gate ceiling: keep 4,000 instructions for the check; a body above
  it is NOT_GATED with its size, never silently skipped; report how many.
- The table: one row per language with "N of 255", three columns —
  native route (rv6, log_265), backstop (rv6's all_constructed column),
  bit-blast (this task) — and the union.
- Instance `bb1.conf`. Lanes under `Research/oracle/riscv/lanes_bb/`.
  Log: next free number (log_265 is rv6's, written by the coordinator).
