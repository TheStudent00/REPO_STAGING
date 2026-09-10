# expand1 -- task ex1: beyond the four

Node: hq.research.arch_unit_oracle.cross_construction.autopoly; the interpreted half also serves node_0_3_1_12_remaining_languages.

Written by `expand1.py report`. Every table is the output of a command of this program, captured: `tables`, `handful`, `causes`, `interp_table` and `interp_sample`.

## 1. cpp, the fifth compiled target

The route is task ap4's, unchanged: the primitive lookup first, the cell's term in the target's own operators where there is no primitive, compiled at the corpus's own cpp ship flags (`/usr/bin/clang++ -std=c++20 -O1 -c`), carved by `lane_gen.DRIVER`'s own `extract`, and put back to z3 against the cell's own term.

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.  cpp's column is this task's own aggregate; the other four are task ap4's, read off `autopoly4.json` and not re-run.

| step or verdict | c | cpp | rust | go | swift |
|---|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 245 cells, 127079 rows, 95.52% | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `compiled` | 245 cells, 127079 rows, 95.52% | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `LANDED` | 76 cells, 41829 rows, 31.44% | 76 cells, 41829 rows, 31.44% | 72 cells, 39199 rows, 29.46% | 30 cells, 22970 rows, 17.26% | 70 cells, 38915 rows, 29.25% |
| `LANDED_ELSEWHERE` | 27 cells, 11867 rows, 8.92% | 27 cells, 11867 rows, 8.92% | 23 cells, 11885 rows, 8.93% | 16 cells, 5448 rows, 4.09% | 35 cells, 18714 rows, 14.07% |
| `NOT_COLLAPSED` | 138 cells, 72141 rows, 54.22% | 138 cells, 72141 rows, 54.22% | 110 cells, 72068 rows, 54.17% | 146 cells, 77229 rows, 58.05% | 91 cells, 61147 rows, 45.96% |
| `proved` | 204 cells, 98747 rows, 74.22% | 202 cells, 93853 rows, 70.54% | 170 cells, 96021 rows, 72.17% | 177 cells, 113587 rows, 85.38% | 163 cells, 89240 rows, 67.08% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 23 cells, 25429 rows, 19.11% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 19 cells, 6794 rows, 5.11% | 17 cells, 5841 rows, 4.39% | 15 cells, 5085 rows, 3.82% | 17 cells, 5181 rows, 3.89% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 2 cells, 1008 rows, 0.76% | 3 cells, 1956 rows, 1.47% | 3 cells, 1786 rows, 1.34% | 6 cells, 1250 rows, 0.94% | 15 cells, 7277 rows, 5.47% |
| `refused` | 8 cells, 5965 rows, 4.48% | 8 cells, 5965 rows, 4.48% | 44 cells, 8650 rows, 6.5% | 53 cells, 13026 rows, 9.79% | 53 cells, 13026 rows, 9.79% |

Table 2 -- the polyfill-complete set at BOTH widths, which is what the brief asks for until the owner says which counts.  A cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose.

| width | targets | cells | ledger rows | share |
|---|---|---|---|---|
| all four | c, rust, go, swift | 162 | 106032 | 79.7% |
| all five | c, cpp, rust, go, swift | 162 | 106032 | 79.7% |

cells proved on all four and NOT on cpp: 0

cpp's own proved set: 225 cells
cells proved on cpp that are not in the all-four set: 63

Table 3 -- how many of the five each cell is proved on, from task ap4's own per-cell list plus cpp's.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 5 of 5 | 162 | 106032 | 79.7% |
| 4 of 5 | 20 | 7761 | 5.83% |
| 3 of 5 | 10 | 3998 | 3.01% |
| 2 of 5 | 36 | 2685 | 2.02% |
| 1 of 5 | 5 | 119 | 0.09% |
| 0 of 5 | 20 | 12449 | 9.36% |

## 2. the handful's ten cells on cpp, beside c

| cell | route on cpp | landed on cpp | cpp's verdict | c's verdict | the two sources |
|---|---|---|---|---|---|
| `add` gpr_gpr 32 | term | LANDED_ELSEWHERE | LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | the same text but for the header and the linkage |
| `sub` imm_gpr 64 | -- | -- | not run | -- | -- |
| `imul` gpr_gpr 32 | primitive | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | different text |
| `sar` cl_gpr 32 | primitive | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | different text |
| `shr` cl_gpr 64 | primitive | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | different text |
| `idiv` gpr_one 32 | primitive+setup | NOT_COLLAPSED | NOT_COLLAPSED (2) / DISPROVED | NOT_COLLAPSED (2) / DISPROVED | different text |
| `cmovne` gpr_gpr 32 | term | NOT_COLLAPSED | NOT_COLLAPSED (2) / PROVED_ON_SHIP | NOT_COLLAPSED (2) / PROVED_ON_SHIP | the same text but for the header and the linkage |
| `setne` gpr_one 8 | term | NOT_COLLAPSED | NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | the same text but for the header and the linkage |
| `addss` xmm_xmm 32 | term | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | the same text but for the header and the linkage |
| `cvtsi2sd` gpr_xmm 64 | term | LANDED | LANDED / PROVED_ON_SHIP | LANDED / PROVED_ON_SHIP | the same text but for the header and the linkage |

`sub` imm_gpr 64 is one of the handful's ten and is NOT in the 253-cell outer set this loop walks, so no run of it exists on either store; task ap4's own reproduction line says the same of it, LITERAL: `the handful's forty pairs: 32 agree character for character, 35 agree on the verdict, 4 not in this outer set`.

of the ten, cpp's verdict is c's: 9
of the ten, cpp's source is c's but for the header and the linkage: 5

## 3. what did not work on cpp, by cause

Table -- what did not work on cpp, by cause.  One target, so `runs` is cells and `rows` is their attested ledger rows.

| cause | runs | ledger rows |
|---|---|---|
| the gate answered sat: the body holds on a region, not on every input | 17 | 5841 |
| term reads state that is not an arrival register | 5 | 4505 |
| answer home or arrival on the x87 stack | 3 | 1460 |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 |
| the gate did not answer: the carved body: the reference: this body's control flow has a cycle (a transfer back to a block already on the walk), and no loop invariant is invented here; and no term either | 1 | 948 |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 1 | 384 |

runs carrying a cause: 28 of 253

## 4. the interpreted handful

There is no carve for an interpreted target, so the emulation is SOURCE in that language and the check is the fuzz census's method over a stated sample. An agreement is not a proof and no interpreted run carries a gate verdict.

| cell | target | route | rendered (GLOSS) | sample points | agreements / disagreements | the first disagreement LITERAL | JIT carve verdict |
|---|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | cpython | source | `m(cat(0, add(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `add` gpr_gpr 32 | php | source | `ex_m(ex_cat(0, ex_add($a, $b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `add` gpr_gpr 32 | ruby | source | `m(cat(0, add(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `add` gpr_gpr 32 | java | source | `m(cat(0L, add(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `add` gpr_gpr 32 | javascript | source | `m(cat(0n, add(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | see the JIT section |
| `add` gpr_gpr 32 | dart | source | `m(cat(0, add(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | see the JIT section |
| `add` gpr_gpr 32 | csharp | source | `m(cat(0L, add(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | see the JIT section |
| `sub` imm_gpr 64 | cpython | source | `m(add(a, 18446744073709551613, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `sub` imm_gpr 64 | php | source | `ex_m(ex_add($a, -3, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `sub` imm_gpr 64 | ruby | source | `m(add(a, 18446744073709551613, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `sub` imm_gpr 64 | java | source | `m(add(a, -3L, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `sub` imm_gpr 64 | javascript | source | `m(add(a, 18446744073709551613n, 64), 64)` | 30 | 30 / 0 | -- | see the JIT section |
| `sub` imm_gpr 64 | dart | source | `m(add(a, -3, 64), 64)` | 30 | 30 / 0 | -- | see the JIT section |
| `sub` imm_gpr 64 | csharp | source | `m(add(a, -3L, 64), 64)` | 30 | 30 / 0 | -- | see the JIT section |
| `imul` gpr_gpr 32 | cpython | source | `m(cat(0, mul(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `imul` gpr_gpr 32 | php | source | `ex_m(ex_cat(0, ex_mul($a, $b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `imul` gpr_gpr 32 | ruby | source | `m(cat(0, mul(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `imul` gpr_gpr 32 | java | source | `m(cat(0L, mul(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | no JIT output in the corpus |
| `imul` gpr_gpr 32 | javascript | source | `m(cat(0n, mul(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | see the JIT section |
| `imul` gpr_gpr 32 | dart | source | `m(cat(0, mul(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | see the JIT section |
| `imul` gpr_gpr 32 | csharp | source | `m(cat(0L, mul(a, b, 32), 32), 64)` | 900 | 900 / 0 | -- | see the JIT section |
| `sar` cl_gpr 32 | cpython | source | `m(cat(0, ashr(a, cat(0, ext(b, 4, 0), 5), 32), 32), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `sar` cl_gpr 32 | php | source | `ex_m(ex_cat(0, ex_ashr($a, ex_cat(0, ex_ext($b, 4, 0), 5), 32), 32), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `sar` cl_gpr 32 | ruby | source | `m(cat(0, ashr(a, cat(0, ext(b, 4, 0), 5), 32), 32), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `sar` cl_gpr 32 | java | source | `m(cat(0L, ashr(a, cat(0L, ext(b, 4, 0), 5), 32), 32), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `sar` cl_gpr 32 | javascript | source | `m(cat(0n, ashr(a, cat(0n, ext(b, 4, 0), 5), 32), 32), 64)` | 810 | 810 / 0 | -- | see the JIT section |
| `sar` cl_gpr 32 | dart | source | `m(cat(0, ashr(a, cat(0, ext(b, 4, 0), 5), 32), 32), 64)` | 810 | 810 / 0 | -- | see the JIT section |
| `sar` cl_gpr 32 | csharp | source | `m(cat(0L, ashr(a, cat(0L, ext(b, 4, 0), 5), 32), 32), 64)` | 810 | 810 / 0 | -- | see the JIT section |
| `shr` cl_gpr 64 | cpython | source | `m(lshr(a, cat(0, ext(b, 5, 0), 6), 64), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `shr` cl_gpr 64 | php | source | `ex_m(ex_lshr($a, ex_cat(0, ex_ext($b, 5, 0), 6), 64), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `shr` cl_gpr 64 | ruby | source | `m(lshr(a, cat(0, ext(b, 5, 0), 6), 64), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `shr` cl_gpr 64 | java | source | `m(lshr(a, cat(0L, ext(b, 5, 0), 6), 64), 64)` | 810 | 810 / 0 | -- | no JIT output in the corpus |
| `shr` cl_gpr 64 | javascript | source | `m(lshr(a, cat(0n, ext(b, 5, 0), 6), 64), 64)` | 810 | 810 / 0 | -- | see the JIT section |
| `shr` cl_gpr 64 | dart | source | `m(lshr(a, cat(0, ext(b, 5, 0), 6), 64), 64)` | 810 | 810 / 0 | -- | see the JIT section |
| `shr` cl_gpr 64 | csharp | source | `m(lshr(a, cat(0L, ext(b, 5, 0), 6), 64), 64)` | 810 | 810 / 0 | -- | see the JIT section |
| `idiv` gpr_one 32 | cpython | source | `m(cat(0, ext(sdiv(cat(a, b, 32), cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(ca...` | 19683 | 18954 / 0 | -- | no JIT output in the corpus |
| `idiv` gpr_one 32 | php | source | `ex_m(ex_cat(0, ex_ext(ex_sdiv(ex_cat($a, $b, 32), ex_cat(ex_cat(ex_cat(ex_cat(ex_cat(ex...` | 19683 | 18953 / 0 | -- | no JIT output in the corpus |
| `idiv` gpr_one 32 | ruby | source | `m(cat(0, ext(sdiv(cat(a, b, 32), cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(ca...` | 19683 | 18954 / 0 | -- | no JIT output in the corpus |
| `idiv` gpr_one 32 | java | source | `m(cat(0L, ext(sdiv(cat(a, b, 32), cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(c...` | 19683 | 18954 / 0 | -- | no JIT output in the corpus |
| `idiv` gpr_one 32 | javascript | source | `m(cat(0n, ext(sdiv(cat(a, b, 32), cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(c...` | 19683 | 18954 / 0 | -- | see the JIT section |
| `idiv` gpr_one 32 | dart | source | `m(cat(0, ext(sdiv(cat(a, b, 32), cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(ca...` | 19683 | 18954 / 0 | -- | see the JIT section |
| `idiv` gpr_one 32 | csharp | source | `m(cat(0L, ext(sdiv(cat(a, b, 32), cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(cat(c...` | 19683 | 18953 / 0 | -- | see the JIT section |
| `cmovne` gpr_gpr 32 | cpython | source | `m(cat(0, ((d) if (eq(bnot(bor(bnot(b, 32), bnot(a, 32), 32), 32), 0, 32)) else (c)), 32...` | 14641 | 14641 / 0 | -- | no JIT output in the corpus |
| `cmovne` gpr_gpr 32 | php | source | `ex_m(ex_cat(0, ((ex_eq(ex_bnot(ex_bor(ex_bnot($b, 32), ex_bnot($a, 32), 32), 32), 0, 32...` | 14641 | 14641 / 0 | -- | no JIT output in the corpus |
| `cmovne` gpr_gpr 32 | ruby | source | `m(cat(0, ((eq(bnot(bor(bnot(b, 32), bnot(a, 32), 32), 32), 0, 32)) ? (d) : (c)), 32), 64)` | 14641 | 14641 / 0 | -- | no JIT output in the corpus |
| `cmovne` gpr_gpr 32 | java | source | `m(cat(0L, ((eq(bnot(bor(bnot(b, 32), bnot(a, 32), 32), 32), 0L, 32)) ? (d) : (c)), 32),...` | 14641 | 14641 / 0 | -- | no JIT output in the corpus |
| `cmovne` gpr_gpr 32 | javascript | source | `m(cat(0n, ((eq(bnot(bor(bnot(b, 32), bnot(a, 32), 32), 32), 0n, 32)) ? (d) : (c)), 32),...` | 14641 | 14641 / 0 | -- | see the JIT section |
| `cmovne` gpr_gpr 32 | dart | source | `m(cat(0, ((eq(bnot(bor(bnot(b, 32), bnot(a, 32), 32), 32), 0, 32)) ? (d) : (c)), 32), 64)` | 14641 | 14641 / 0 | -- | see the JIT section |
| `cmovne` gpr_gpr 32 | csharp | source | `m(cat(0L, ((eq(bnot(bor(bnot(b, 32), bnot(a, 32), 32), 32), 0L, 32)) ? (d) : (c)), 32),...` | 14641 | 14641 / 0 | -- | see the JIT section |
| `setne` gpr_one 8 | cpython | source | `m(cat(0, ((0) if (eq(bnot(bor(bnot(a, 8), bnot(b, 8), 8), 8), 0, 8)) else (1)), 8), 64)` | 729 | 729 / 0 | -- | no JIT output in the corpus |
| `setne` gpr_one 8 | php | source | `ex_m(ex_cat(0, ((ex_eq(ex_bnot(ex_bor(ex_bnot($a, 8), ex_bnot($b, 8), 8), 8), 0, 8)) ? ...` | 729 | 729 / 0 | -- | no JIT output in the corpus |
| `setne` gpr_one 8 | ruby | source | `m(cat(0, ((eq(bnot(bor(bnot(a, 8), bnot(b, 8), 8), 8), 0, 8)) ? (0) : (1)), 8), 64)` | 729 | 729 / 0 | -- | no JIT output in the corpus |
| `setne` gpr_one 8 | java | source | `m(cat(0L, ((eq(bnot(bor(bnot(a, 8), bnot(b, 8), 8), 8), 0L, 8)) ? (0L) : (1L)), 8), 64)` | 729 | 729 / 0 | -- | no JIT output in the corpus |
| `setne` gpr_one 8 | javascript | source | `m(cat(0n, ((eq(bnot(bor(bnot(a, 8), bnot(b, 8), 8), 8), 0n, 8)) ? (0n) : (1n)), 8), 64)` | 729 | 729 / 0 | -- | see the JIT section |
| `setne` gpr_one 8 | dart | source | `m(cat(0, ((eq(bnot(bor(bnot(a, 8), bnot(b, 8), 8), 8), 0, 8)) ? (0) : (1)), 8), 64)` | 729 | 729 / 0 | -- | see the JIT section |
| `setne` gpr_one 8 | csharp | source | `m(cat(0L, ((eq(bnot(bor(bnot(a, 8), bnot(b, 8), 8), 8), 0L, 8)) ? (0L) : (1L)), 8), 64)` | 729 | 729 / 0 | -- | see the JIT section |
| `addss` xmm_xmm 32 | cpython | source | `m(fadd(a, b, 32), 32)` | 529 | 439 / 0 | -- | no JIT output in the corpus |
| `addss` xmm_xmm 32 | php | source | `ex_m(ex_fadd($a, $b, 32), 32)` | 529 | 439 / 0 | -- | no JIT output in the corpus |
| `addss` xmm_xmm 32 | ruby | source | `m(fadd(a, b, 32), 32)` | 529 | 439 / 0 | -- | no JIT output in the corpus |
| `addss` xmm_xmm 32 | java | source | `m(fadd(a, b, 32), 32)` | 529 | 439 / 0 | -- | no JIT output in the corpus |
| `addss` xmm_xmm 32 | javascript | source | `m(fadd(a, b, 32), 32)` | 529 | 439 / 0 | -- | see the JIT section |
| `addss` xmm_xmm 32 | dart | source | `m(fadd(a, b, 32), 32)` | 529 | 439 / 0 | -- | see the JIT section |
| `addss` xmm_xmm 32 | csharp | source | `m(fadd(a, b, 32), 32)` | 529 | 439 / 0 | -- | see the JIT section |
| `cvtsi2sd` gpr_xmm 64 | cpython | source | `m(i2f(a, 64, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `cvtsi2sd` gpr_xmm 64 | php | source | `ex_m(ex_i2f($a, 64, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `cvtsi2sd` gpr_xmm 64 | ruby | source | `m(i2f(a, 64, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `cvtsi2sd` gpr_xmm 64 | java | source | `m(i2f(a, 64, 64), 64)` | 30 | 30 / 0 | -- | no JIT output in the corpus |
| `cvtsi2sd` gpr_xmm 64 | javascript | source | `m(i2f(a, 64, 64), 64)` | 30 | 30 / 0 | -- | see the JIT section |
| `cvtsi2sd` gpr_xmm 64 | dart | source | `m(i2f(a, 64, 64), 64)` | 30 | 30 / 0 | -- | see the JIT section |
| `cvtsi2sd` gpr_xmm 64 | csharp | source | `m(i2f(a, 64, 64), 64)` | 30 | 30 / 0 | -- | see the JIT section |

| target | runs | rendered | cells whose whole sample agrees | points | agreements | disagreements | declines |
|---|---|---|---|---|---|---|---|
| cpython | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| php | 10 | 10 | 10 | 39062 | 38242 | 0 | 820 |
| ruby | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| java | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| javascript | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| dart | 10 | 10 | 10 | 39062 | 38243 | 0 | 819 |
| csharp | 10 | 10 | 10 | 39062 | 38242 | 0 | 820 |

what did not run, by cause:

| cause | runs | targets |
|---|---|---|

the declines, by cause, over every run (never scored, this line's own standing rule):

| cause | points |
|---|---|
| the interpreter RAISE:ZeroDivisionError | 1458 |
| the interpreter RAISE:DivisionByZeroError | 729 |
| the interpreter RAISE:ArithmeticException | 729 |
| the interpreter RAISE:RangeError | 729 |
| the interpreter RAISE:IntegerDivisionByZeroException | 729 |
| the interpreter RAISE:DivideByZeroException | 729 |
| the reference's own term does not evaluate to a numeral at this point | 630 |
| the interpreter RAISE:ArithmeticError | 1 |
| the interpreter RAISE:OverflowException | 1 |

## 5. the JIT output the corpus holds

The brief's instruction is conditional -- ALSO carve and gate the JIT output where the corpus already carves it -- and the condition does not hold. What `jit_out_*` holds is each JIT's OWN dump text, in three different formats, none of them objdump's; the carve this line uses is `lane_gen.DRIVER`'s `extract` over objdump, and the corpus holds no arch-unit for javascript, dart or csharp at all. Building a reader for three new instruction-text formats is a new instrument, which is a flag for the coordinator and not something this task works around.

| folder | files | the first line of its dump, LITERAL |
|---|---|---|
| jit_out_javascript | 822 | `---------------------------------------------------` |
| jit_out_dart | 3 | `Code for function 'dart:io__Platform@16069316_set__nativeScript@16069316' (SetterFunction) {` |
| jit_out_csharp | 2 | `; Assembly listing for method Program:op_638(float,ulong):bool (MinOpts)` |

what the corpus holds as ARCH-UNITS, per language (`oracle/arch_opcodes/single_opcode_units.json`):

| language | in the file | narrow single-opcode groups |
|---|---|---|
| c | yes | 83 |
| cpp | yes | 82 |
| rust | yes | 48 |
| go | yes | 27 |
| swift | yes | 19 |
| java | yes | 0 |
| cpython | yes | 1 |
| php | yes | 3 |
| ruby | yes | 2 |
| javascript | no | -- |
| dart | no | -- |
| csharp | no | -- |

## 6. the sample rule, LITERAL, as it was run

```
THE SAMPLE, for a place whose emulation takes k arrivals of widths
w_1 .. w_k.

  the per-arrival budget b = max(4, int(20000 ** (1.0 / k)))

  P(an INTEGER arrival of width w) is this list, in this order,
  deduplicated, every value taken modulo nothing and dropped when it
  is not less than 2^w, then cut to its first b entries:
      0, 1, 2, 3, 7, 100,
      2^(w-1) - 1, 2^(w-1), 2^(w-1) + 1,          the sign boundary
      2^w - 2, 2^w - 1,                           the top, and -1
      w - 1, w, w + 1,                            this width's shift counts
      7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, the other widths'
      then 8 values from random.Random(20260909).randrange(2^w)

  P(a FLOAT arrival of width w, which reaches the emulation as its
  IEEE bit pattern) is this list, in this order, deduplicated, cut to
  its first b entries:
      +0, -0, 1.0, -1.0, 2.0, 0.5, -0.5,
      the smallest subnormal, the largest subnormal,
      the smallest normal, the largest finite,
      +inf, -inf, a quiet NaN, a signalling NaN,
      then 8 values from random.Random(20260909).randrange(2^w)

  THE SAMPLE is the ordered cross product P(a_1) x ... x P(a_k), in
  that order.  Its size is at most 20,000 by the budget above, and the
  run record carries the exact count.

  WHY b IS A CEILING AND NOT A CHOICE OF POINTS: the edge values come
  FIRST in every list, so cutting to b drops ordinary values before it
  drops an edge.  A place with one or two arrivals is never cut at all
  (b is 20000 and 141), so the handful's edges are all present; a
  place with four is cut to 11 per arrival, and the run record says
  which values those were.
```

THE SAMPLE, for a place whose emulation takes k arrivals of widths
w_1 .. w_k.

  the per-arrival budget b = max(4, int(20000 ** (1.0 / k)))

  P(an INTEGER arrival of width w) is this list, in this order,
  deduplicated, every value taken modulo nothing and dropped when it
  is not less than 2^w, then cut to its first b entries:
      0, 1, 2, 3, 7, 100,
      2^(w-1) - 1, 2^(w-1), 2^(w-1) + 1,          the sign boundary
      2^w - 2, 2^w - 1,                           the top, and -1
      w - 1, w, w + 1,                            this width's shift counts
      7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, the other widths'
      then 8 values from random.Random(20260909).randrange(2^w)

  P(a FLOAT arrival of width w, which reaches the emulation as its
  IEEE bit pattern) is this list, in this order, deduplicated, cut to
  its first b entries:
      +0, -0, 1.0, -1.0, 2.0, 0.5, -0.5,
      the smallest subnormal, the largest subnormal,
      the smallest normal, the largest finite,
      +inf, -inf, a quiet NaN, a signalling NaN,
      then 8 values from random.Random(20260909).randrange(2^w)

  THE SAMPLE is the ordered cross product P(a_1) x ... x P(a_k), in
  that order.  Its size is at most 20,000 by the budget above, and the
  run record carries the exact count.

  WHY b IS A CEILING AND NOT A CHOICE OF POINTS: the edge values come
  FIRST in every list, so cutting to b drops ordinary values before it
  drops an edge.  A place with one or two arrivals is never cut at all
  (b is 20000 and 141), so the handful's edges are all present; a
  place with four is cut to 11 per arrival, and the run record says
  which values those were.

the point counts the rule gives, per arrival width:

| arrivals | budget | an 8-bit list | a 32-bit list | a 64-bit list |
|---|---|---|---|---|
| 1 | 20000 | 27 | 30 | 30 |
| 2 | 141 | 27 | 30 | 30 |
| 3 | 27 | 27 | 27 | 27 |
| 4 | 11 | 11 | 11 | 11 |

a 32-bit integer list in full, LITERAL: [0, 1, 2, 3, 7, 100, 2147483647, 2147483648, 2147483649, 4294967294, 4294967295, 31, 32, 33, 8, 9, 15, 16, 17, 63, 64, 65, 389011218, 2331439129, 2029787120, 3026389180, 2533586177, 3307009030, 839636273, 1229552792]

a 32-bit float list in full, as bit patterns, LITERAL: ['0x0', '0x80000000', '0x3f800000', '0xbf800000', '0x40000000', '0x3f000000', '0xbf000000', '0x1', '0x7fffff', '0x800000', '0x7f7fffff', '0x7f800000', '0xff800000', '0x7fc00000', '0x7f800001', '0x172fd712', '0x8af6f019', '0x78fc17f0', '0xb46308bc', '0x97037501', '0xc51cf406', '0x320bd531', '0x49497c98']

