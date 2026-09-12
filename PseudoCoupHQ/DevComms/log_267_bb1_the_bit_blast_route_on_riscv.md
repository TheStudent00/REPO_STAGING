# log 267 — bb1: the bit-blast route on every RISC-V arch-opcode, beside the native route and the backstop

Written 2026-09-12 by the coordinator (Fable). The implementer built
`construct/general/bitblast.py` and `bb1_run.py` and launched the run,
then its session dropped on a server timeout; the lane ran to the end on
the tower by itself. Lane `bb1_l6_every_cell_four_languages.sh`: started
05:45:28Z, done 06:24:50Z; 1,020 checks, one process, peak 261 MB.
Sample lanes l1–l5 hold the sizes and the cost at the largest six.

`bit-blast`
- z3's own tactic turns each definition into an and-or-not circuit over
  the input bits; the renderer writes one named boolean per gate in the
  target; no adder, multiplier or divider authored by anyone.

## the three routes, population 255 on every row
| language | native route (rv6) | backstop (rv6) | bit-blast (this) | any route | of |
|---|---|---|---|---|---|
| c | 241 | 143 | 136 | 243 | 255 |
| c++ | 241 | 143 | 136 | 243 | 255 |
| rust | 246 | 196 | 202 | 247 | 255 |
| go | 238 | 183 | 203 | 241 | 255 |
| any language | | | 203 | 251 | 255 |
| all four languages | | | | 235 | 255 |

## the bit-blast outcomes, by language and cause
| language | proved | undecided | refused | the causes |
|---|---|---|---|---|
| c, c++ | 136 | 67 | 52 | the lifter has no entry for `bexti` (41), `orn` (12), `c.not` (10) — bit-manipulation instructions clang writes for gate code; 26 float places the blast refuses (a circuit over bits has no float node) |
| rust | 202 | 0 | 52 | the 26 float places; 26 more over the size ceiling |
| go | 203 | 0 | 52 | the same |
Proved bit-blast bodies: 677, median 17 instructions, largest 3,837
(the ceiling is 4,000). The divide and multiply-high family compiles to
98,000–250,000 instructions (l4) and is NOT_GATED by size.

## the sizes and the cost (l3, l4)
Gates per definition over 229 places: median 1, mean 5,642, largest
85,095 (`mulh`); 137 places under 100 gates, 14 over 50,000. Blast
seconds: median 0.018, largest 7.3. At the largest six: source
77,000–85,000 lines; compile 13–14 s (c/c++), 16–21 s (rust), 3–5 s
(go) with two go divides hitting the 600 s cap; bodies 98k–250k
instructions; the check not offered.

## what is left, on every route and language
`mulh` and `mulhsu` at 64 bits, two forms each: the 128-bit product's
high half. The owed Lean lemma (`construct/lean/OWED.md` §2).

## flags
- the RISC-V lifter's next rows: `bexti`, `orn`, `c.not` (and rv5's
  `binvi`, `fsgnjn.s`).
- c/c++ undecided 67 where rust/go prove the same circuits: not
  measured; the bodies are in the store (`bb1_all.jsonl`, text kept).
- the eager-select render defect (log_265's queue note) stands.
