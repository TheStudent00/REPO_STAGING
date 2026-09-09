# autopoly2.md -- task ap2: AutoPoly's loop, second pass

Node `hq.research.arch_unit_oracle.cross_construction.autopoly`. Written by `autopoly.py`; never hand-edited.

**What this is, one sentence.** the owner's loop -- for every arch opcode of the model table that the corpus attests, for each of the four compiled targets, `find_emulation(cell, lang)` -- run for the first time over its whole measured outer set: 253 cells x 4 targets = 1012 runs, of which 1012 are recorded here.

The route is `handful.py` as task g1b left it (`handful.py as task g1b left it, TASK g1c: the two printing fixes of task h2, the primitive route before the term route, and the primitive lookup widened by one zero-operand setup step`), imported and called; this task's own program is the loop around it and the bookkeeping, nothing else.

Every count below is of the run's own DESTINATION PLACE -- `handful.destination_place`, the first place the cell writes that is not the flags -- which is the place tasks h1, h2, g1 and g1b's own tables already summarize. The denominator of every share is 133044, the attested ledger rows of the whole outer set.

## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 199 cells, 122994 rows, 92.45% | 199 cells, 122994 rows, 92.45% | 190 cells, 118618 rows, 89.16% | 190 cells, 118618 rows, 89.16% |
| `compiled` | 199 cells, 122994 rows, 92.45% | 199 cells, 122994 rows, 92.45% | 190 cells, 118618 rows, 89.16% | 190 cells, 118618 rows, 89.16% |
| `LANDED` | 75 cells, 40302 rows, 30.29% | 72 cells, 39199 rows, 29.46% | 30 cells, 22970 rows, 17.26% | 70 cells, 38915 rows, 29.25% |
| `LANDED_ELSEWHERE` | 16 cells, 11111 rows, 8.35% | 17 cells, 11855 rows, 8.91% | 10 cells, 5418 rows, 4.07% | 29 cells, 18684 rows, 14.04% |
| `NOT_COLLAPSED` | 108 cells, 71581 rows, 53.8% | 110 cells, 71940 rows, 54.07% | 150 cells, 90230 rows, 67.82% | 91 cells, 61019 rows, 45.86% |
| `proved` | 156 cells, 89468 rows, 67.25% | 159 cells, 94617 rows, 71.12% | 160 cells, 97840 rows, 73.54% | 152 cells, 87836 rows, 66.02% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 15 cells, 4228 rows, 3.18% | 14 cells, 5069 rows, 3.81% | 16 cells, 5157 rows, 3.88% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 8 cells, 8768 rows, 6.59% | 5 cells, 1806 rows, 1.36% | 14 cells, 15621 rows, 11.74% | 16 cells, 7281 rows, 5.47% |
| `refused` | 54 cells, 10050 rows, 7.55% | 54 cells, 10050 rows, 7.55% | 63 cells, 14426 rows, 10.84% | 63 cells, 14426 rows, 10.84% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 29 cells, 19706 rows, 14.81% | 22 cells, 12245 rows, 9.2% | 17 cells, 10351 rows, 7.78% | 9 cells, 7774 rows, 5.84% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 190 cells, 110041 rows, 82.71% | 199 cells, 119228 rows, 89.62% | 204 cells, 121122 rows, 91.04% | 212 cells, 123699 rows, 92.98% |
| `no route reached` | 32 cells, 1571 rows, 1.18% | 32 cells, 1571 rows, 1.18% | 32 cells, 1571 rows, 1.18% | 32 cells, 1571 rows, 1.18% |

## 3. Refusals and non-proofs, by cause

### 3.1 c

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| term reads state that is not an arrival register | 12 | 7079 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movaps` mem_xmm 128 (942 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 5190 | `xor` gpr_same 32 (5190 rows) |
| the gate answered sat: the body holds on a region, not on every input | 15 | 4228 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 1726 | `idiv` gpr_one 64 (948 rows); `idiv` gpr_one 32 (778 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| vector arrival used beyond its low lane | 10 | 1400 | `movaps` xmm_xmm 128 (980 rows); `movapd` xmm_xmm 128 (230 rows); `unpckhpd` xmm_xmm 128 (132 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 840 | `mov` imm_gpr 32 (835 rows); `mov` imm_gpr 8 (5 rows) |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | `div` gpr_one 64 (624 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 1 | 384 | `div` gpr_one 32 (384 rows) |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 1 | 4 | `punpcklqdq` xmm_xmm 128 (4 rows) |

### 3.2 rust

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| term reads state that is not an arrival register | 12 | 7079 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movaps` mem_xmm 128 (942 rows) |
| the gate answered sat: the body holds on a region, not on every input | 14 | 5069 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `idiv` gpr_one 64 (948 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 4 | 1802 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 64 (624 rows); `div` gpr_one 32 (384 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| vector arrival used beyond its low lane | 10 | 1400 | `movaps` xmm_xmm 128 (980 rows); `movapd` xmm_xmm 128 (230 rows); `unpckhpd` xmm_xmm 128 (132 rows) |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 1 | 4 | `punpcklqdq` xmm_xmm 128 (4 rows) |

### 3.3 go

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 8 | 14371 | `mov` gpr_gpr 64 (7194 rows); `cmp` gpr_gpr 64 (4011 rows); `test` gpr_same 64 (2425 rows) |
| term reads state that is not an arrival register | 12 | 7079 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movaps` mem_xmm 128 (942 rows) |
| the gate answered sat: the body holds on a region, not on every input | 16 | 5157 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| a width c has no holder for | 9 | 4376 | `sbb` gpr_gpr 64 (1478 rows); `idiv` gpr_one 64 (948 rows); `div` gpr_one 64 (624 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| vector arrival used beyond its low lane | 10 | 1400 | `movaps` xmm_xmm 128 (980 rows); `movapd` xmm_xmm 128 (230 rows); `unpckhpd` xmm_xmm 128 (132 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 4 | 1214 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |

### 3.4 swift

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| term reads state that is not an arrival register | 12 | 7079 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movaps` mem_xmm 128 (942 rows) |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 13 | 6833 | `movslq` widen_gpr_gpr 64 (3728 rows); `setp` gpr_one 8 (2125 rows); `idiv` gpr_one 32 (778 rows) |
| a width c has no holder for | 9 | 4376 | `sbb` gpr_gpr 64 (1478 rows); `idiv` gpr_one 64 (948 rows); `div` gpr_one 64 (624 rows) |
| the gate answered sat: the body holds on a region, not on every input | 5 | 3723 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| vector arrival used beyond its low lane | 10 | 1400 | `movaps` xmm_xmm 128 (980 rows); `movapd` xmm_xmm 128 (230 rows); `unpckhpd` xmm_xmm 128 (132 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 2 | 420 | `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |

## 4. Cells proved on all four targets, on three, two, one, none

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose. The polyfill-complete set is the row `4`.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 144 | 85368 | 64.17% |
| 3 of 4 | 29 | 27938 | 21.0% |
| 2 of 4 | 8 | 3081 | 2.32% |
| 1 of 4 | 6 | 123 | 0.09% |
| 0 of 4 | 66 | 16534 | 12.43% |

### 4.1 The polyfill-complete set, in full


| cell | ledger rows |
|---|---|
| `add` cl_gpr 8 | 251 |
| `add` gpr_gpr 16 | 2 |
| `add` gpr_gpr 32 | 11 |
| `add` gpr_gpr 64 | 744 |
| `add` gpr_gpr 8 | 2 |
| `add` gpr_same 8 | 53 |
| `add` imm_gpr 64 | 18 |
| `addsd` mem_xmm 64 | 20 |
| `addsd` xmm_xmm 64 | 244 |
| `addss` mem_xmm 32 | 107 |
| `addss` xmm_same 32 | 308 |
| `addss` xmm_xmm 32 | 210 |
| `and` cl_gpr 8 | 1664 |
| `and` gpr_gpr 32 | 999 |
| `and` gpr_gpr 64 | 809 |
| `and` gpr_gpr 8 | 896 |
| `and` imm_gpr 32 | 1366 |
| `and` imm_gpr 8 | 190 |
| `cltd` none 64 | 267 |
| `cmovae` gpr_gpr 32 | 21 |
| `cmovae` gpr_gpr 64 | 14 |
| `cmovb` gpr_gpr 32 | 42 |
| `cmovb` gpr_gpr 64 | 38 |
| `cmovbe` gpr_gpr 32 | 502 |
| `cmove` gpr_gpr 32 | 69 |
| `cmove` gpr_gpr 64 | 218 |
| `cmovge` gpr_gpr 32 | 12 |
| `cmovge` gpr_gpr 64 | 6 |
| `cmovl` gpr_gpr 32 | 4 |
| `cmovl` gpr_gpr 64 | 8 |
| `cmovle` gpr_gpr 32 | 53 |
| `cmovne` gpr_gpr 32 | 2 |
| `cmovne` gpr_gpr 64 | 398 |
| `cmovns` gpr_gpr 32 | 53 |
| `cmovns` gpr_gpr 64 | 2 |
| `cmovs` gpr_gpr 64 | 2 |
| `cmp` gpr_gpr 16 | 410 |
| `cmp` gpr_gpr 32 | 1944 |
| `cmp` gpr_gpr 8 | 194 |
| `cmp` imm_gpr 16 | 117 |
| `cmp` imm_gpr 32 | 161 |
| `cmp` imm_gpr 8 | 116 |
| `cqto` none 64 | 374 |
| `cvtsi2sd` gpr_xmm 64 | 860 |
| `cvtsi2ss` gpr_xmm 32 | 2936 |
| `cvtss2sd` xmm_same 64 | 172 |
| `cvtss2sd` xmm_xmm 64 | 4 |
| `divsd` mem_xmm 64 | 6 |
| `divsd` xmm_xmm 64 | 118 |
| `divss` mem_xmm 32 | 65 |
| `divss` xmm_xmm 32 | 230 |
| `imul` gpr_gpr 16 | 1 |
| `imul` gpr_gpr 32 | 266 |
| `imul` gpr_gpr 64 | 608 |
| `lea` lea_mem 32 | 334 |
| `lea` lea_mem 64 | 86 |
| `mov` gpr_gpr 32 | 10245 |
| `mov` gpr_same 32 | 84 |
| `mov` imm_gpr 16 | 1 |
| `mov` imm_gpr 64 | 14 |
| `mov` mem_gpr 32 | 8 |
| `movabs` imm_gpr 64 | 14 |
| `movd` gpr_xmm 32 | 2313 |
| `movd` xmm_gpr 32 | 760 |
| `movq` gpr_xmm 64 | 140 |
| `movq` xmm_gpr 64 | 312 |
| `movsd` mem_xmm 64 | 58 |
| `movss` mem_xmm 32 | 1281 |
| `movzbl` cl_gpr 32 | 968 |
| `movzbl` widen_gpr_gpr 32 | 1033 |
| `movzbl` widen_mem_gpr 32 | 8 |
| `movzwl` widen_gpr_gpr 32 | 63 |
| `movzwl` widen_mem_gpr 32 | 4 |
| `mul` gpr_one 16 | 2 |
| `mul` gpr_one 32 | 2 |
| `mul` gpr_one 64 | 310 |
| `mul` gpr_one 8 | 6 |
| `mulsd` mem_xmm 64 | 12 |
| `mulsd` xmm_xmm 64 | 112 |
| `mulss` mem_xmm 32 | 91 |
| `mulss` xmm_xmm 32 | 210 |
| `neg` gpr_one 16 | 5 |
| `neg` gpr_one 32 | 45 |
| `neg` gpr_one 64 | 43 |
| `neg` gpr_one 8 | 118 |
| `not` gpr_one 32 | 101 |
| `not` gpr_one 64 | 105 |
| `not` gpr_one 8 | 14 |
| `or` cl_gpr 8 | 1702 |
| `or` gpr_gpr 16 | 34 |
| `or` gpr_gpr 32 | 805 |
| `or` gpr_gpr 64 | 2654 |
| `or` gpr_gpr 8 | 2407 |
| `or` imm_gpr 8 | 2 |
| `pextrw` imm_xmm_gpr 128 | 2317 |
| `punpckldq` mem_xmm 128 | 132 |
| `pxor` xmm_same 128 | 36 |
| `sar` cl_gpr 16 | 11 |
| `sar` cl_gpr 32 | 335 |
| `sar` cl_gpr 64 | 315 |
| `sar` cl_gpr 8 | 42 |
| `sar` imm_gpr 64 | 1467 |
| `sar` imm_gpr 8 | 12 |
| `sbb` imm_gpr 8 | 164 |
| `seta` gpr_one 8 | 1407 |
| `setae` gpr_one 8 | 1552 |
| `setb` gpr_one 8 | 499 |
| `setbe` gpr_one 8 | 314 |
| `sete` gpr_one 8 | 1339 |
| `setg` gpr_one 8 | 872 |
| `setge` gpr_one 8 | 675 |
| `setl` gpr_one 8 | 984 |
| `setle` gpr_one 8 | 643 |
| `setne` gpr_one 8 | 10335 |
| `setns` gpr_one 8 | 176 |
| `sets` gpr_one 8 | 264 |
| `shl` cl_gpr 32 | 707 |
| `shl` cl_gpr 64 | 564 |
| `shl` cl_gpr 8 | 60 |
| `shl` imm_gpr 32 | 2329 |
| `shl` imm_gpr 64 | 6 |
| `shr` cl_gpr 16 | 11 |
| `shr` cl_gpr 32 | 328 |
| `shr` cl_gpr 64 | 251 |
| `shr` cl_gpr 8 | 41 |
| `shr` imm_gpr 32 | 12 |
| `shr` imm_gpr 64 | 320 |
| `sub` cl_gpr 8 | 253 |
| `sub` gpr_gpr 16 | 2 |
| `sub` gpr_gpr 32 | 340 |
| `sub` gpr_gpr 64 | 577 |
| `sub` gpr_gpr 8 | 19 |
| `test` cl_gpr 8 | 8 |
| `test` gpr_gpr 8 | 2 |
| `test` gpr_same 16 | 710 |
| `test` gpr_same 32 | 3617 |
| `test` gpr_same 8 | 720 |
| `test` imm_gpr 64 | 2 |
| `test` imm_gpr 8 | 272 |
| `xor` gpr_gpr 32 | 572 |
| `xor` gpr_gpr 64 | 1668 |
| `xor` gpr_gpr 8 | 2 |
| `xorpd` xmm_same 128 | 378 |
| `xorps` xmm_same 128 | 3013 |

### 4.2 The cells proved on no target, in full, with the cause on each

| cell | ledger rows | c | rust | go | swift |
|---|---|---|---|---|---|
| `push` gpr_one 64 | 3408 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `ucomiss` xmm_xmm 32 | 2270 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `fldt` mem_one 80 | 1527 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fucomip` st_st 80 | 1031 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `ucomisd` xmm_xmm 64 | 1026 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `movaps` xmm_xmm 128 | 980 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `idiv` gpr_one 64 | 948 | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | the gate answered sat: the body holds on a region, not on every input | a width c has no holder for | a width c has no holder for |
| `movaps` mem_xmm 128 | 942 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `idiv` gpr_one 32 | 778 | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `div` gpr_one 64 | 624 | the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | a width c has no holder for | a width c has no holder for |
| `div` gpr_one 32 | 384 | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `ucomiss` mem_xmm 32 | 342 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `fildll` mem_one 80 | 332 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fldz` st_none 80 | 321 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movapd` xmm_xmm 128 | 230 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `filds` mem_one 80 | 194 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `subpd` mem_xmm 128 | 132 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `unpckhpd` xmm_xmm 128 | 132 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `fildl` mem_one 80 | 116 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fucomi` st_st 80 | 108 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fadds` mem_one 80 | 96 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `flds` mem_one 80 | 56 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `div` gpr_one 16 | 36 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `faddp` st_st 80 | 30 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fmulp` st_st 80 | 30 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `div` gpr_one 8 | 28 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | None | None |
| `fiadds` mem_one 80 | 28 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fimuls` mem_one 80 | 28 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fldl` mem_one 80 | 28 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movdqa` xmm_xmm 128 | 28 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `ucomisd` mem_xmm 64 | 24 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | the gate answered sat: the body holds on a region, not on every input |
| `xorps` mem_xmm 128 | 21 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fiaddl` mem_one 80 | 16 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fimull` mem_one 80 | 16 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `idiv` gpr_one 16 | 16 | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `fdivp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivrp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubrp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fidivrs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fidivs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubrs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fidivl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fidivrl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubrl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fmuls` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `idiv` gpr_one 8 | 8 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | None | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `andpd` xmm_xmm 128 | 6 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `andps` xmm_xmm 128 | 6 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `orpd` xmm_xmm 128 | 6 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `orps` xmm_xmm 128 | 6 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `faddl` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivrs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fmull` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubrs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `pxor` xmm_xmm 128 | 4 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `fdivl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivrl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubrl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `pand` xmm_xmm 128 | 2 | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane | vector arrival used beyond its low lane |
| `pxor` mem_xmm 128 | 2 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |

## 5. Every `sat` verdict, with its counterexample and the region it names

A `sat` is where the target's edge region differs from the opcode's: z3 found a starting state under which the compiled body and the cell's term answer differently. The counterexample is z3's own, LITERAL.

TWO COUNTS, and they are two different things.

- **`sat` at the plain comparison: 154 places.** z3 answered `sat` when the emulation's arriving values are whatever fits the register.
- **`sat` that survives the caller-extension re-pose: 69 places.** Task o7's own rule: pose the same comparison again with every narrow-holder input row zero-extended from its holder width to the register, which is what the target's own calling rule guarantees the caller did. What is left is where the target's edge region really differs from the opcode's.

Table 1's `sat` row counts the second of these at the destination place; this table lists every written place, the flags included.

| cell | lang | place | route | ledger rows | survives the re-pose | region | counterexample (LITERAL) |
|---|---|---|---|---|---|---|---|
| `setne` gpr_one 8 | c | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `setne` gpr_one 8 | rust | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `setne` gpr_one 8 | swift | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `or` gpr_gpr 8 | c | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` gpr_gpr 8 | rust | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` gpr_gpr 8 | swift | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `ucomiss` xmm_xmm 32 | c | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2155806718, IN_1 = 2139359232, fp.to_ieee_bv = [NaN -> 2139097088, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2155806718, IN_1 = 2139359232, fp.to_ieee_bv = [NaN -> 2139097088, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | go | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4290164324, IN_1 = 2354832038, fp.to_ieee_bv = [NaN -> 4290180708, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 4290164324, IN_1 = 2354832038, fp.to_ieee_bv = [NaN -> 4290180708, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | rust | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 3665292120, IN_1 = 4293037052, fp.to_ieee_bv = [NaN -> 4293038076, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 3665292120, IN_1 = 4293037052, fp.to_ieee_bv = [NaN -> 4293038076, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | swift | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2130837537, IN_1 = 4294836126, fp.to_ieee_bv = [NaN -> 4294836190, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2130837537, IN_1 = 4294836126, fp.to_ieee_bv = [NaN -> 4294836190, else -> fp.to_ieee_bv(Var(0))]] |
| `or` cl_gpr 8 | c | reg_rdi | term | 1702 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` cl_gpr 8 | rust | reg_rdi | term | 1702 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` cl_gpr 8 | swift | reg_rdi | term | 1702 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `and` cl_gpr 8 | c | reg_rdi | term | 1664 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` cl_gpr 8 | rust | reg_rdi | term | 1664 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` cl_gpr 8 | swift | reg_rdi | term | 1664 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `setae` gpr_one 8 | rust | reg_rdi | term | 1552 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2147487809, IN_0 = 2147479489] |
| `movzbl` widen_gpr_gpr 32 | c | reg_rdi | term | 1033 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` widen_gpr_gpr 32 | rust | reg_rdi | term | 1033 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` widen_gpr_gpr 32 | swift | reg_rdi | term | 1033 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `ucomisd` xmm_xmm 64 | c | flags.low | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | c | flags.high | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | go | flags.low | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | go | flags.high | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | rust | flags.low | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | rust | flags.high | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | swift | flags.low | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | swift | flags.high | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `movzbl` cl_gpr 32 | c | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` cl_gpr 32 | rust | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` cl_gpr 32 | swift | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `idiv` gpr_one 64 | rust | reg_rax | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 17, seed_MEM_m0x30_rbp_ = 2, IN_1 = 6148914691236517161, IN_0 = 14822379391721547801] | [IN_2 = 17, seed_MEM_m0x30_rbp_ = 2, IN_1 = 6148914691236517161, IN_0 = 14822379391721547801] |
| `idiv` gpr_one 64 | rust | reg_rdx | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 17870283321406128128, IN_1 = 576460752303423488, IN_0 = 10394933699525738496, seed_MEM_m0x20_rbp_ = 14801643057929257219] | [IN_2 = 17870283321406128128, IN_1 = 576460752303423488, IN_0 = 10394933699525738496, seed_MEM_m0x20_rbp_ = 14801643057929257219] |
| `and` gpr_gpr 8 | c | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | rust | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | swift | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `add` gpr_gpr 64 | c | reg_rdi | primitive | 744 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 18428729670905102336] |
| `cmp` gpr_gpr 16 | c | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1486028800, IN_0 = 54199] |
| `cmp` gpr_gpr 16 | rust | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2437087232, IN_0 = 46975] |
| `cmp` gpr_gpr 16 | swift | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1513816064, IN_0 = 53779] |
| `div` gpr_one 32 | c | reg_rdx | term | 384 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 1660033990, IN_2 = 0, IN_0 = 2114887688] | [IN_1 = 1660033990, IN_2 = 0, IN_0 = 2114887688] |
| `div` gpr_one 32 | rust | reg_rdx | term | 384 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 0, IN_0 = 16777216, IN_1 = 257835015] | [IN_2 = 0, IN_0 = 16777216, IN_1 = 257835015] |
| `ucomiss` mem_xmm 32 | c | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 1143849285, IN_1 = 4287229765, fp.to_ieee_bv = [NaN -> 2143300291, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 1143849285, IN_1 = 4287229765, fp.to_ieee_bv = [NaN -> 2143300291, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | go | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2370037759, IN_1 = 2143616306, fp.to_ieee_bv = [NaN -> 2143616310, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2370037759, IN_1 = 2143616306, fp.to_ieee_bv = [NaN -> 2143616310, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | rust | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 2155872254, IN_0 = 2146316818, fp.to_ieee_bv = [NaN -> 4287745517, else -> fp.to_ieee_bv(Var(0))]] | [IN_1 = 2155872254, IN_0 = 2146316818, fp.to_ieee_bv = [NaN -> 4287745517, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | swift | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2147405694, IN_1 = 3100639, fp.to_ieee_bv = [NaN -> 2147405630, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2147405694, IN_1 = 3100639, fp.to_ieee_bv = [NaN -> 2147405630, else -> fp.to_ieee_bv(Var(0))]] |
| `cmpneqss` xmm_xmm 32 | go | reg_xmm0 | term | 307 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 64 | c | reg_rdi | primitive | 277 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `sbb` gpr_same 32 | rust | reg_rdi | term | 268 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 2047, IN_0 = 4294965247] | [IN_1 = 2047, IN_0 = 4294965247] |
| `sub` cl_gpr 8 | c | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 15104, IN_0 = 251] |
| `sub` cl_gpr 8 | rust | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 15360, IN_0 = 255] |
| `sub` cl_gpr 8 | swift | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 42240, IN_0 = 173] |
| `add` cl_gpr 8 | c | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 35840, IN_0 = 155] |
| `add` cl_gpr 8 | rust | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 39680, IN_0 = 145] |
| `add` cl_gpr 8 | swift | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 21504, IN_0 = 215] |
| `subss` xmm_xmm 32 | go | reg_xmm0 | term | 230 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 4074883714, IN_0 = 2368524363, IN_1 = 2370503730, fp.to_ieee_bv = [NaN -> 2139619521, else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 4074883714, IN_0 = 2368524363, IN_1 = 2370503730, fp.to_ieee_bv = [NaN -> 2139619521, else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqss` xmm_xmm 32 | go | reg_xmm0 | term | 198 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `cmp` gpr_gpr 8 | c | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 247, IN_1 = 13056] |
| `cmp` gpr_gpr 8 | rust | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 11264, IN_0 = 47] |
| `cmp` gpr_gpr 8 | swift | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 219, IN_1 = 19200] |
| `cmpneqsd` xmm_xmm 64 | go | reg_xmm0 | term | 190 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `sbb` imm_gpr 8 | rust | reg_rdi | term | 164 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2147487809, IN_0 = 2147479489] |
| `cmpneqss` mem_xmm 32 | go | reg_xmm0 | term | 154 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `subsd` xmm_xmm 64 | go | reg_xmm0 | term | 118 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 9477145627446182849, IN_0 = 9209861237972664320, IN_1 = 8959231539382565798, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 9477145627446182849, IN_0 = 9209861237972664320, IN_1 = 8959231539382565798, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqsd` xmm_xmm 64 | go | reg_xmm0 | term | 116 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `cmpeqss` mem_xmm 32 | go | reg_xmm0 | term | 101 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 32 | c | reg_rdi | primitive | 82 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `subss` mem_xmm 32 | go | reg_xmm0 | term | 65 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 4264895866, IN_0 = 32719098, IN_1 = 2139095040, fp.to_ieee_bv = [NaN -> 4290412758, else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 4264895866, IN_0 = 32719098, IN_1 = 2139095040, fp.to_ieee_bv = [NaN -> 4290412758, else -> fp.to_ieee_bv(Var(0))]] |
| `movzwl` widen_gpr_gpr 32 | c | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_gpr_gpr 32 | rust | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_gpr_gpr 32 | swift | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `xor` imm_gpr 8 | c | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | rust | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | swift | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_same 8 | c | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | rust | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | swift | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `neg` gpr_one 64 | c | flags.high | primitive | 43 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4611686018427387905] | [IN_0 = 4611686018427387905] |
| `neg` gpr_one 64 | go | flags.high | primitive | 43 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4611686018427387905] | [IN_0 = 4611686018427387905] |
| `neg` gpr_one 64 | rust | flags.high | primitive | 43 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4611686018427387905] | [IN_0 = 4611686018427387905] |
| `shr` cl_gpr 8 | c | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1, IN_0 = 3243334624] |
| `shr` cl_gpr 8 | rust | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 7, IN_0 = 4026400128] |
| `shr` cl_gpr 8 | swift | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 7, IN_0 = 4239351552] |
| `div` gpr_one 16 | c | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 3556853248, IN_1 = 65534, IN_0 = 65535] | [IN_2 = 3556853248, IN_1 = 65534, IN_0 = 65535] |
| `div` gpr_one 16 | c | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 0, IN_1 = 2281799680, IN_0 = 32767] | [IN_2 = 0, IN_1 = 2281799680, IN_0 = 32767] |
| `div` gpr_one 16 | rust | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 7143424, IN_1 = 52, IN_0 = 34048] | [IN_2 = 7143424, IN_1 = 52, IN_0 = 34048] |
| `div` gpr_one 16 | rust | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 0, IN_1 = 803274747, IN_0 = 53279] | [IN_2 = 0, IN_1 = 803274747, IN_0 = 53279] |
| `div` gpr_one 16 | swift | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 0, IN_0 = 2, IN_1 = 32768] | [IN_2 = 0, IN_0 = 2, IN_1 = 32768] |
| `or` gpr_gpr 16 | c | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | rust | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | swift | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `div` gpr_one 8 | c | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 1216366848, IN_0 = 65535] | [IN_1 = 1216366848, IN_0 = 65535] |
| `div` gpr_one 8 | rust | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 0, IN_0 = 49150] | [IN_1 = 0, IN_0 = 49150] |
| `ucomisd` mem_xmm 64 | c | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | c | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | go | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | rust | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | rust | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | swift | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | swift | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `cwtl` none 64 | c | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 65535, IN_0 = 2626289664] | [seed_r8 = 65535, IN_0 = 2626289664] |
| `cwtl` none 64 | rust | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 131071, IN_0 = 3905421312] | [seed_r8 = 131071, IN_0 = 3905421312] |
| `movswl` widen_gpr_gpr 32 | c | reg_rdi | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 50338772, IN_0 = 2081783808] | [seed_r8 = 50338772, IN_0 = 2081783808] |
| `movswl` widen_gpr_gpr 32 | rust | reg_rdi | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 16379, IN_0 = 2426241024] | [seed_r8 = 16379, IN_0 = 2426241024] |
| `sub` gpr_gpr 8 | c | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 46080, IN_0 = 183] |
| `sub` gpr_gpr 8 | rust | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 13312, IN_0 = 247] |
| `sub` gpr_gpr 8 | swift | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 67, IN_1 = 31744] |
| `cmpneqsd` mem_xmm 64 | go | reg_xmm0 | term | 18 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `idiv` gpr_one 16 | c | reg_rax | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 538443776, IN_1 = 0, IN_0 = 16384] | [IN_2 = 538443776, IN_1 = 0, IN_0 = 16384] |
| `idiv` gpr_one 16 | c | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 28798, IN_1 = 3841508390, IN_0 = 57649] | [IN_2 = 28798, IN_1 = 3841508390, IN_0 = 57649] |
| `idiv` gpr_one 16 | rust | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 20, IN_0 = 8199, IN_1 = 135315437] | [IN_2 = 20, IN_0 = 8199, IN_1 = 135315437] |
| `cmpeqsd` mem_xmm 64 | go | reg_xmm0 | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `movsbl` widen_gpr_gpr 32 | c | reg_rdi | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4294967040] | [IN_0 = 4294967040] |
| `movsbl` widen_gpr_gpr 32 | rust | reg_rdi | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4294967040] | [IN_0 = 4294967040] |
| `shr` cl_gpr 16 | c | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 13, IN_0 = 2615083008] |
| `shr` cl_gpr 16 | rust | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 2113863680, IN_1 = 15] |
| `shr` cl_gpr 16 | swift | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 3220119552, IN_1 = 15] |
| `idiv` gpr_one 8 | c | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 2576, IN_0 = 32768, seed_rdx = 24704] | [IN_1 = 2576, IN_0 = 32768, seed_rdx = 24704] |
| `idiv` gpr_one 8 | rust | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 64, IN_1 = 45120] | [IN_0 = 64, IN_1 = 45120] |
| `movzbl` widen_mem_gpr 32 | c | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` widen_mem_gpr 32 | rust | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` widen_mem_gpr 32 | swift | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294934272] |
| `mul` gpr_one 8 | c | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3779056275, IN_0 = 251] |
| `mul` gpr_one 8 | rust | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1371865840, IN_0 = 247] |
| `mul` gpr_one 8 | swift | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4175896313, IN_0 = 68] |
| `subsd` mem_xmm 64 | go | reg_xmm0 | term | 6 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 2004101834179097081, IN_0 = 14560137595288039929, IN_1 = 5187948951877272940, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 2004101834179097081, IN_0 = 14560137595288039929, IN_1 = 5187948951877272940, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `movsbq` widen_gpr_gpr 64 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movsbq` widen_gpr_gpr 64 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzwl` widen_mem_gpr 32 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_mem_gpr 32 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_mem_gpr 32 | swift | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `seto` gpr_one 8 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `seto` gpr_one 8 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `xor` imm_gpr 32 | go | reg_rdi | primitive | 4 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_gpr 8 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 56064, IN_0 = 147] |
| `add` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 388235264, IN_0 = 63023] |
| `add` gpr_gpr 8 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 247, IN_1 = 21504] |
| `add` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 42325, IN_1 = 2907897856] |
| `add` gpr_gpr 8 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 41984, IN_0 = 175] |
| `add` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3127115776, IN_0 = 41711] |
| `imul` gpr_one 8 | c | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 7723, seed_rdx = 33253, IN_0 = 2] | [IN_1 = 7723, seed_rdx = 33253, IN_0 = 2] |
| `imul` gpr_one 8 | rust | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 3041, seed_rcx = 25707, IN_0 = 90] | [IN_1 = 3041, seed_rcx = 25707, IN_0 = 90] |
| `mul` gpr_one 16 | c | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2002877303, IN_0 = 463536111] |
| `mul` gpr_one 16 | rust | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2369093103, IN_0 = 1454240911] |
| `mul` gpr_one 16 | swift | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 317774007, IN_0 = 3614958288] |
| `sub` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 40295, IN_1 = 3367239680] |
| `sub` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1255407616, IN_0 = 51927] |
| `sub` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 43193, IN_1 = 2897936384] |
| `xor` gpr_gpr 8 | c | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | rust | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | swift | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `imul` gpr_gpr 16 | c | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 60363, IN_1 = 675938304] |
| `imul` gpr_gpr 16 | rust | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2428764160, IN_0 = 46047] |
| `imul` gpr_gpr 16 | swift | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 45007, IN_1 = 2924150784] |

## 6. The handful, reproduced

Table 4 -- the ten cells tasks h1, h2, g1 and g1b ran, on the same four targets, as they came out of THIS loop, beside task g1b's own answer for the same pair. The handful's side is read from `handful3b.json` and, for the one pair the widened lookup changes, `handful3c.json`.

| cell | lang | this loop: route / landed / gate | the handful: route / landed / gate | agrees | agrees on the verdict |
|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | yes | yes |
| `add` gpr_gpr 32 | rust | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | yes | yes |
| `add` gpr_gpr 32 | go | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `add` gpr_gpr 32 | swift | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | yes | yes |
| `sub` imm_gpr 64 | c | -- | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | **no** | **no** |
| `sub` imm_gpr 64 | rust | -- | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | **no** | **no** |
| `sub` imm_gpr 64 | go | -- | term / LANDED_ELSEWHERE on `add` / PROVED_ON_SHIP | **no** | **no** |
| `sub` imm_gpr 64 | swift | -- | term / LANDED_ELSEWHERE on `lea` / PROVED_ON_SHIP | **no** | **no** |
| `imul` gpr_gpr 32 | c | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `imul` gpr_gpr 32 | rust | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `imul` gpr_gpr 32 | go | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `imul` gpr_gpr 32 | swift | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `sar` cl_gpr 32 | c | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `sar` cl_gpr 32 | rust | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `sar` cl_gpr 32 | go | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | yes | yes |
| `sar` cl_gpr 32 | swift | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `shr` cl_gpr 64 | c | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `shr` cl_gpr 64 | rust | primitive / LANDED / PROVED_ON_SHIP | primitive / LANDED / PROVED_ON_SHIP | yes | yes |
| `shr` cl_gpr 64 | go | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | yes | yes |
| `shr` cl_gpr 64 | swift | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `idiv` gpr_one 32 | c | primitive+setup / NOT_COLLAPSED (2) / UNDECIDED, UNDECIDED at 30000 ms | primitive+setup / NOT_COLLAPSED (2) / UNDECIDED, UNDECIDED at 300000 ms | **no** | yes |
| `idiv` gpr_one 32 | rust | term / NOT_COLLAPSED (51) / UNDECIDED, UNDECIDED at 30000 ms | term / NOT_COLLAPSED (51) / UNDECIDED, UNDECIDED at 300000 ms | **no** | yes |
| `idiv` gpr_one 32 | go | term / NOT_COLLAPSED (85) / UNDECIDED, UNDECIDED at 30000 ms | term / NOT_COLLAPSED (85) / UNDECIDED, UNDECIDED at 300000 ms | **no** | yes |
| `idiv` gpr_one 32 | swift | term / LANDED_ELSEWHERE on `jmp` / UNDECIDED, UNDECIDED at 30000 ms | term / LANDED_ELSEWHERE on `jmp` / UNDECIDED, UNDECIDED at 300000 ms | **no** | yes |
| `cmovne` gpr_gpr 32 | c | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | yes | yes |
| `cmovne` gpr_gpr 32 | rust | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | yes | yes |
| `cmovne` gpr_gpr 32 | go | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | yes | yes |
| `cmovne` gpr_gpr 32 | swift | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | term / NOT_COLLAPSED (2) / PROVED_ON_SHIP | yes | yes |
| `setne` gpr_one 8 | c | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | yes | yes |
| `setne` gpr_one 8 | rust | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | yes | yes |
| `setne` gpr_one 8 | go | term / NOT_COLLAPSED (13) / PROVED_ON_SHIP | term / NOT_COLLAPSED (13) / PROVED_ON_SHIP | yes | yes |
| `setne` gpr_one 8 | swift | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | term / NOT_COLLAPSED (3) / DISPROVED, PROVED_ON_SHIP under caller extension | yes | yes |
| `addss` xmm_xmm 32 | c | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `addss` xmm_xmm 32 | rust | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `addss` xmm_xmm 32 | go | term / NOT_COLLAPSED (3) / PROVED_ON_SHIP | term / NOT_COLLAPSED (3) / PROVED_ON_SHIP | yes | yes |
| `addss` xmm_xmm 32 | swift | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `cvtsi2sd` gpr_xmm 64 | c | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `cvtsi2sd` gpr_xmm 64 | rust | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |
| `cvtsi2sd` gpr_xmm 64 | go | term / NOT_COLLAPSED (4) / PROVED_ON_SHIP | term / NOT_COLLAPSED (4) / PROVED_ON_SHIP | yes | yes |
| `cvtsi2sd` gpr_xmm 64 | swift | term / LANDED / PROVED_ON_SHIP | term / LANDED / PROVED_ON_SHIP | yes | yes |

Agree character for character: 32 of 40. Agree on the verdict, the re-pose's own ceiling aside: 36 -- this loop re-poses an UNDECIDED once at 30,000 ms where the handful re-posed at 300,000 ms, which is this brief's own instruction, so the two differ in that number and in nothing else.

