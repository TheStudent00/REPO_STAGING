# autopoly3.md -- task ap3: AutoPoly's loop, third pass

Node `hq.research.arch_unit_oracle.cross_construction.autopoly`. Written by `autopoly.py`; never hand-edited.

**What this is, one sentence.** the owner's loop -- for every arch opcode of the model table that the corpus attests, for each of the four compiled targets, `find_emulation(cell, lang)` -- run for the first time over its whole measured outer set: 253 cells x 4 targets = 1012 runs, of which 1012 are recorded here.

The route is `handful.py` as task g1b left it (`handful.py as task g1b left it, TASK g1c: the two printing fixes of task h2, the primitive route before the term route, and the primitive lookup widened by one zero-operand setup step`), imported and called; this task's own program is the loop around it and the bookkeeping, nothing else.

Every count below is of the run's own DESTINATION PLACE -- `handful.destination_place`, the first place the cell writes that is not the flags -- which is the place tasks h1, h2, g1 and g1b's own tables already summarize. The denominator of every share is 133044, the attested ledger rows of the whole outer set.

## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `compiled` | 245 cells, 127079 rows, 95.52% | 209 cells, 124394 rows, 93.5% | 200 cells, 120018 rows, 90.21% | 200 cells, 120018 rows, 90.21% |
| `LANDED` | 76 cells, 41829 rows, 31.44% | 72 cells, 39199 rows, 29.46% | 30 cells, 22970 rows, 17.26% | 70 cells, 38915 rows, 29.25% |
| `LANDED_ELSEWHERE` | 27 cells, 11867 rows, 8.92% | 23 cells, 11885 rows, 8.93% | 16 cells, 5448 rows, 4.09% | 35 cells, 18714 rows, 14.07% |
| `NOT_COLLAPSED` | 142 cells, 73383 rows, 55.16% | 114 cells, 73310 rows, 55.1% | 154 cells, 91600 rows, 68.85% | 95 cells, 62389 rows, 46.89% |
| `proved` | 163 cells, 89630 rows, 67.37% | 166 cells, 94779 rows, 71.24% | 170 cells, 99240 rows, 74.59% | 159 cells, 87998 rows, 66.14% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 14 cells, 4212 rows, 3.17% | 15 cells, 5085 rows, 3.82% | 16 cells, 5157 rows, 3.88% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 48 cells, 12707 rows, 9.55% | 7 cells, 3028 rows, 2.28% | 14 cells, 15621 rows, 11.74% | 19 cells, 8519 rows, 6.4% |
| `refused` | 8 cells, 5965 rows, 4.48% | 44 cells, 8650 rows, 6.5% | 53 cells, 13026 rows, 9.79% | 53 cells, 13026 rows, 9.79% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 29 cells, 19706 rows, 14.81% | 22 cells, 12245 rows, 9.2% | 17 cells, 10351 rows, 7.78% | 9 cells, 7774 rows, 5.84% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 222 cells, 111612 rows, 83.89% | 231 cells, 120799 rows, 90.8% | 236 cells, 122693 rows, 92.22% | 244 cells, 125270 rows, 94.16% |
| `no route reached` | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |

## 3. Refusals and non-proofs, by cause

### 3.1 c

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 5190 | `xor` gpr_same 32 (5190 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| the gate answered sat: the body holds on a region, not on every input | 14 | 4212 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 40 | 3927 | `fldt` mem_one 80 (1527 rows); `movaps` xmm_xmm 128 (980 rows); `fildll` mem_one 80 (332 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 1726 | `idiv` gpr_one 64 (948 rows); `idiv` gpr_one 32 (778 rows) |
| answer home or arrival on the x87 stack | 3 | 1460 | `fucomip` st_st 80 (1031 rows); `fldz` st_none 80 (321 rows); `fucomi` st_st 80 (108 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 840 | `mov` imm_gpr 32 (835 rows); `mov` imm_gpr 8 (5 rows) |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | `div` gpr_one 64 (624 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 2 | 400 | `div` gpr_one 32 (384 rows); `idiv` gpr_one 16 (16 rows) |

### 3.2 rust

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| the gate answered sat: the body holds on a region, not on every input | 15 | 5085 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `idiv` gpr_one 64 (948 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| answer home or arrival on the x87 stack | 37 | 3006 | `fldt` mem_one 80 (1527 rows); `fildll` mem_one 80 (332 rows); `fldz` st_none 80 (321 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 3 | 1786 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 64 (624 rows); `div` gpr_one 32 (384 rows) |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 4 | 1242 | `movaps` xmm_xmm 128 (980 rows); `movapd` xmm_xmm 128 (230 rows); `movdqa` xmm_xmm 128 (28 rows) |
| a width c has no holder for | 2 | 1139 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows) |

### 3.3 go

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 8 | 14371 | `mov` gpr_gpr 64 (7194 rows); `cmp` gpr_gpr 64 (4011 rows); `test` gpr_same 64 (2425 rows) |
| a width c has no holder for | 11 | 5515 | `sbb` gpr_gpr 64 (1478 rows); `fucomip` st_st 80 (1031 rows); `idiv` gpr_one 64 (948 rows) |
| the gate answered sat: the body holds on a region, not on every input | 16 | 5157 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| answer home or arrival on the x87 stack | 37 | 3006 | `fldt` mem_one 80 (1527 rows); `fildll` mem_one 80 (332 rows); `fldz` st_none 80 (321 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 4 | 1214 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |

### 3.4 swift

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 16 | 8071 | `movslq` widen_gpr_gpr 64 (3728 rows); `setp` gpr_one 8 (2125 rows); `movaps` xmm_xmm 128 (980 rows) |
| a width c has no holder for | 11 | 5515 | `sbb` gpr_gpr 64 (1478 rows); `fucomip` st_st 80 (1031 rows); `idiv` gpr_one 64 (948 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| the gate answered sat: the body holds on a region, not on every input | 5 | 3723 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| answer home or arrival on the x87 stack | 37 | 3006 | `fldt` mem_one 80 (1527 rows); `fildll` mem_one 80 (332 rows); `fldz` st_none 80 (321 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 2 | 420 | `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |

## 4. Cells proved on all four targets, on three, two, one, none

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose. The polyfill-complete set is the row `4`.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 151 | 85530 | 64.29% |
| 3 of 4 | 29 | 27938 | 21.0% |
| 2 of 4 | 8 | 3081 | 2.32% |
| 1 of 4 | 9 | 1361 | 1.02% |
| 0 of 4 | 56 | 15134 | 11.38% |

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
| `andpd` xmm_xmm 128 | 6 |
| `andps` xmm_xmm 128 | 6 |
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
| `orpd` xmm_xmm 128 | 6 |
| `orps` xmm_xmm 128 | 6 |
| `pand` xmm_xmm 128 | 2 |
| `pextrw` imm_xmm_gpr 128 | 2317 |
| `punpckldq` mem_xmm 128 | 132 |
| `pxor` xmm_same 128 | 36 |
| `pxor` xmm_xmm 128 | 4 |
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
| `unpckhpd` xmm_xmm 128 | 132 |
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
| `fldt` mem_one 80 | 1527 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fucomip` st_st 80 | 1031 | answer home or arrival on the x87 stack | a width c has no holder for | a width c has no holder for | a width c has no holder for |
| `ucomisd` xmm_xmm 64 | 1026 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `idiv` gpr_one 64 | 948 | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | the gate answered sat: the body holds on a region, not on every input | a width c has no holder for | a width c has no holder for |
| `movaps` mem_xmm 128 | 942 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `idiv` gpr_one 32 | 778 | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `div` gpr_one 64 | 624 | the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | a width c has no holder for | a width c has no holder for |
| `div` gpr_one 32 | 384 | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `ucomiss` mem_xmm 32 | 342 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `fildll` mem_one 80 | 332 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fldz` st_none 80 | 321 | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `filds` mem_one 80 | 194 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `subpd` mem_xmm 128 | 132 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fildl` mem_one 80 | 116 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fucomi` st_st 80 | 108 | answer home or arrival on the x87 stack | a width c has no holder for | a width c has no holder for | a width c has no holder for |
| `fadds` mem_one 80 | 96 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `flds` mem_one 80 | 56 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `div` gpr_one 16 | 36 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `faddp` st_st 80 | 30 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fmulp` st_st 80 | 30 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `div` gpr_one 8 | 28 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | None | None |
| `fiadds` mem_one 80 | 28 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fimuls` mem_one 80 | 28 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fldl` mem_one 80 | 28 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `ucomisd` mem_xmm 64 | 24 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | the gate answered sat: the body holds on a region, not on every input |
| `xorps` mem_xmm 128 | 21 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fiaddl` mem_one 80 | 16 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fimull` mem_one 80 | 16 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `idiv` gpr_one 16 | 16 | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `fdivp` st_st 80 | 15 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fdivrp` st_st 80 | 15 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fsubp` st_st 80 | 15 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fsubrp` st_st 80 | 15 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fidivrs` mem_one 80 | 14 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fidivs` mem_one 80 | 14 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fisubrs` mem_one 80 | 14 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fisubs` mem_one 80 | 14 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fidivl` mem_one 80 | 8 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fidivrl` mem_one 80 | 8 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fisubl` mem_one 80 | 8 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fisubrl` mem_one 80 | 8 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fmuls` mem_one 80 | 8 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `idiv` gpr_one 8 | 8 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | None | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `faddl` mem_one 80 | 4 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fdivrs` mem_one 80 | 4 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fdivs` mem_one 80 | 4 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fmull` mem_one 80 | 4 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fsubrs` mem_one 80 | 4 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fsubs` mem_one 80 | 4 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fdivl` mem_one 80 | 2 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fdivrl` mem_one 80 | 2 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fsubl` mem_one 80 | 2 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `fsubrl` mem_one 80 | 2 | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `pxor` mem_xmm 128 | 2 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |

## 5. Every `sat` verdict, with its counterexample and the region it names

A `sat` is where the target's edge region differs from the opcode's: z3 found a starting state under which the compiled body and the cell's term answer differently. The counterexample is z3's own, LITERAL.

TWO COUNTS, and they are two different things.

- **`sat` at the plain comparison: 152 places.** z3 answered `sat` when the emulation's arriving values are whatever fits the register.
- **`sat` that survives the caller-extension re-pose: 67 places.** Task o7's own rule: pose the same comparison again with every narrow-holder input row zero-extended from its holder width to the register, which is what the target's own calling rule guarantees the caller did. What is left is where the target's edge region really differs from the opcode's.

Table 1's `sat` row counts the second of these at the destination place; this table lists every written place, the flags included.

| cell | lang | place | route | ledger rows | survives the re-pose | region | counterexample (LITERAL) |
|---|---|---|---|---|---|---|---|
| `setne` gpr_one 8 | c | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `setne` gpr_one 8 | rust | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `setne` gpr_one 8 | swift | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `or` gpr_gpr 8 | c | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` gpr_gpr 8 | rust | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` gpr_gpr 8 | swift | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `ucomiss` xmm_xmm 32 | c | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2139666200, IN_1 = 1144878877, fp.to_ieee_bv = [NaN -> 2139633432, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2139666200, IN_1 = 1144878877, fp.to_ieee_bv = [NaN -> 2139633432, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | go | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2147481143, IN_1 = 4168296306, fp.to_ieee_bv = [NaN -> 2147481207, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2147481143, IN_1 = 4168296306, fp.to_ieee_bv = [NaN -> 2147481207, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | rust | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2139111425, IN_1 = 3229581310, fp.to_ieee_bv = [NaN -> 2139119617, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2139111425, IN_1 = 3229581310, fp.to_ieee_bv = [NaN -> 2139119617, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | swift | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4287134992, IN_1 = 2684380471, fp.to_ieee_bv = [NaN -> 4287397136, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 4287134992, IN_1 = 2684380471, fp.to_ieee_bv = [NaN -> 4287397136, else -> fp.to_ieee_bv(Var(0))]] |
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
| `idiv` gpr_one 64 | rust | reg_rax | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 17, IN_1 = 6148914691236517161, seed_MEM_m0x30_rbp_ = 2, IN_0 = 14822379391721547801] | [IN_2 = 17, IN_1 = 6148914691236517161, seed_MEM_m0x30_rbp_ = 2, IN_0 = 14822379391721547801] |
| `idiv` gpr_one 64 | rust | reg_rdx | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 16100368667849523200, IN_1 = 7705658962430918656, IN_0 = 7658299244035912388, seed_MEM_m0x20_rbp_ = 6148914691236519549] | [IN_2 = 16100368667849523200, IN_1 = 7705658962430918656, IN_0 = 7658299244035912388, seed_MEM_m0x20_rbp_ = 6148914691236519549] |
| `and` gpr_gpr 8 | c | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | rust | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | swift | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `add` gpr_gpr 64 | c | reg_rdi | primitive | 744 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 18428729636545363968] |
| `cmp` gpr_gpr 16 | c | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 850067456, IN_0 = 59051] |
| `cmp` gpr_gpr 16 | rust | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2516844544, IN_0 = 47101] |
| `cmp` gpr_gpr 16 | swift | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 989265920, IN_0 = 8867] |
| `div` gpr_one 32 | rust | reg_rdx | term | 384 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 0, IN_1 = 1384140546, IN_0 = 2113929216] | [IN_2 = 0, IN_1 = 1384140546, IN_0 = 2113929216] |
| `ucomiss` mem_xmm 32 | c | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2155872254, IN_1 = 4287282022, fp.to_ieee_bv = [NaN -> 2146780313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2155872254, IN_1 = 4287282022, fp.to_ieee_bv = [NaN -> 2146780313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | go | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 544626079, IN_1 = 4289952606, fp.to_ieee_bv = [NaN -> 4289952094, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 544626079, IN_1 = 4289952606, fp.to_ieee_bv = [NaN -> 4289952094, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | rust | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2155871710, IN_1 = 2141330209, fp.to_ieee_bv = [NaN -> 2141346593, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2155871710, IN_1 = 2141330209, fp.to_ieee_bv = [NaN -> 2141346593, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | swift | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2180968332, IN_1 = 2146933726, fp.to_ieee_bv = [NaN -> 2146671582, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2180968332, IN_1 = 2146933726, fp.to_ieee_bv = [NaN -> 2146671582, else -> fp.to_ieee_bv(Var(0))]] |
| `cmpneqss` xmm_xmm 32 | go | reg_xmm0 | term | 307 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 64 | c | reg_rdi | primitive | 277 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `sbb` gpr_same 32 | rust | reg_rdi | term | 268 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 4294963201, IN_0 = 4294963201] | [IN_1 = 4294963201, IN_0 = 4294963201] |
| `sub` cl_gpr 8 | c | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 43776, IN_0 = 169] |
| `sub` cl_gpr 8 | rust | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 5120, IN_0 = 247] |
| `sub` cl_gpr 8 | swift | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 13312, IN_0 = 247] |
| `add` cl_gpr 8 | c | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 11008, IN_0 = 235] |
| `add` cl_gpr 8 | rust | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 101, IN_1 = 26112] |
| `add` cl_gpr 8 | swift | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 44032, IN_0 = 151] |
| `subss` xmm_xmm 32 | go | reg_xmm0 | term | 230 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 403301736, IN_0 = 3514826716, IN_1 = 1218828155, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 403301736, IN_0 = 3514826716, IN_1 = 1218828155, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqss` xmm_xmm 32 | go | reg_xmm0 | term | 198 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `cmp` gpr_gpr 8 | c | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 21248, IN_0 = 247] |
| `cmp` gpr_gpr 8 | rust | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 14848, IN_0 = 250] |
| `cmp` gpr_gpr 8 | swift | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 11264, IN_0 = 235] |
| `cmpneqsd` xmm_xmm 64 | go | reg_xmm0 | term | 190 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `sbb` imm_gpr 8 | rust | reg_rdi | term | 164 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2147487809, IN_0 = 2147479489] |
| `cmpneqss` mem_xmm 32 | go | reg_xmm0 | term | 154 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `subsd` xmm_xmm 64 | go | reg_xmm0 | term | 118 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 2537702707518591666, IN_0 = 11525362149736170574, IN_1 = 11531778024674963571, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 2537702707518591666, IN_0 = 11525362149736170574, IN_1 = 11531778024674963571, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqsd` xmm_xmm 64 | go | reg_xmm0 | term | 116 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `cmpeqss` mem_xmm 32 | go | reg_xmm0 | term | 101 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 32 | c | reg_rdi | primitive | 82 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `subss` mem_xmm 32 | go | reg_xmm0 | term | 65 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 9668224, IN_0 = 3750516606, IN_1 = 3744482434, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 9668224, IN_0 = 3750516606, IN_1 = 3744482434, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `movzwl` widen_gpr_gpr 32 | c | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_gpr_gpr 32 | rust | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_gpr_gpr 32 | swift | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294836224] |
| `xor` imm_gpr 8 | c | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | rust | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | swift | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_same 8 | c | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | rust | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | swift | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `neg` gpr_one 64 | c | flags.high | primitive | 43 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4611686018427387906] | [IN_0 = 4611686018427387906] |
| `neg` gpr_one 64 | go | flags.high | primitive | 43 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4611686018427387905] | [IN_0 = 4611686018427387905] |
| `neg` gpr_one 64 | rust | flags.high | primitive | 43 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4611686018427387905] | [IN_0 = 4611686018427387905] |
| `shr` cl_gpr 8 | c | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3, IN_0 = 611240728] |
| `shr` cl_gpr 8 | rust | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 7, IN_0 = 3007184640] |
| `shr` cl_gpr 8 | swift | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1, IN_0 = 2128923182] |
| `div` gpr_one 16 | c | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 813708420, IN_0 = 61678, IN_1 = 53774] | [IN_2 = 813708420, IN_0 = 61678, IN_1 = 53774] |
| `div` gpr_one 16 | c | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 3342335, IN_1 = 920583907, IN_0 = 286] | [IN_2 = 3342335, IN_1 = 920583907, IN_0 = 286] |
| `div` gpr_one 16 | rust | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 2206728195, IN_1 = 56571, IN_0 = 60547] | [IN_2 = 2206728195, IN_1 = 56571, IN_0 = 60547] |
| `div` gpr_one 16 | rust | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 1073741824, IN_1 = 1048575, IN_0 = 52208] | [IN_2 = 1073741824, IN_1 = 1048575, IN_0 = 52208] |
| `or` gpr_gpr 16 | c | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | rust | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | swift | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `div` gpr_one 8 | c | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 536870912, IN_0 = 65535] | [IN_1 = 536870912, IN_0 = 65535] |
| `div` gpr_one 8 | rust | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 503709678, IN_0 = 7166] | [IN_1 = 503709678, IN_0 = 7166] |
| `ucomisd` mem_xmm 64 | c | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | c | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | go | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | rust | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | rust | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | swift | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | swift | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `cwtl` none 64 | c | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 288230376153808896, IN_0 = 3913449472] | [seed_r8 = 288230376153808896, IN_0 = 3913449472] |
| `cwtl` none 64 | rust | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 97527, IN_0 = 86376448] | [seed_r8 = 97527, IN_0 = 86376448] |
| `movswl` widen_gpr_gpr 32 | c | reg_rdi | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 31640, IN_0 = 1785004032] | [seed_r8 = 31640, IN_0 = 1785004032] |
| `movswl` widen_gpr_gpr 32 | rust | reg_rdi | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 93502, IN_0 = 3831201792] | [seed_r8 = 93502, IN_0 = 3831201792] |
| `sub` gpr_gpr 8 | c | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 235, IN_1 = 24320] |
| `sub` gpr_gpr 8 | rust | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 43776, IN_0 = 139] |
| `sub` gpr_gpr 8 | swift | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 37888, IN_0 = 149] |
| `cmpneqsd` mem_xmm 64 | go | reg_xmm0 | term | 18 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `idiv` gpr_one 16 | c | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 2151645184, IN_1 = 4201610667, IN_0 = 34192] | [IN_2 = 2151645184, IN_1 = 4201610667, IN_0 = 34192] |
| `idiv` gpr_one 16 | rust | reg_rax | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 32768, IN_1 = 0, IN_2 = 673554405] | [IN_0 = 32768, IN_1 = 0, IN_2 = 673554405] |
| `idiv` gpr_one 16 | rust | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 8421376, IN_1 = 92747264, IN_0 = 0] | [IN_2 = 8421376, IN_1 = 92747264, IN_0 = 0] |
| `cmpeqsd` mem_xmm 64 | go | reg_xmm0 | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `movsbl` widen_gpr_gpr 32 | c | reg_rdi | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4294967040] | [IN_0 = 4294967040] |
| `movsbl` widen_gpr_gpr 32 | rust | reg_rdi | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4294967040] | [IN_0 = 4294967040] |
| `shr` cl_gpr 16 | c | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 3757506560, IN_1 = 13] |
| `shr` cl_gpr 16 | rust | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 15, IN_0 = 4286513152] |
| `shr` cl_gpr 16 | swift | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 2784858112, IN_1 = 11] |
| `idiv` gpr_one 8 | c | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 0, IN_0 = 30721, seed_rdx = 8] | [IN_1 = 0, IN_0 = 30721, seed_rdx = 8] |
| `idiv` gpr_one 8 | rust | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 47996, IN_1 = 46584] | [IN_0 = 47996, IN_1 = 46584] |
| `movzbl` widen_mem_gpr 32 | c | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` widen_mem_gpr 32 | rust | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294966528] |
| `movzbl` widen_mem_gpr 32 | swift | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `mul` gpr_one 8 | c | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1921631423, IN_0 = 5793910882531] |
| `mul` gpr_one 8 | rust | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3556198911, IN_0 = 239] |
| `mul` gpr_one 8 | swift | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2357657085, IN_0 = 238] |
| `subsd` mem_xmm 64 | go | reg_xmm0 | term | 6 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 2251730434235355, IN_0 = 7160702421695039866, IN_1 = 16381864561113818721, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 2251730434235355, IN_0 = 7160702421695039866, IN_1 = 16381864561113818721, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `movsbq` widen_gpr_gpr 64 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movsbq` widen_gpr_gpr 64 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzwl` widen_mem_gpr 32 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_mem_gpr 32 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_mem_gpr 32 | swift | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `seto` gpr_one 8 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `seto` gpr_one 8 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `xor` imm_gpr 32 | go | reg_rdi | primitive | 4 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_gpr 8 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 19200, IN_0 = 219] |
| `add` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2494234624, IN_0 = 45995] |
| `add` gpr_gpr 8 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 10240, IN_0 = 107] |
| `add` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2492661760, IN_0 = 46519] |
| `add` gpr_gpr 8 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 12800, IN_0 = 243] |
| `add` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2859204608, IN_0 = 43499] |
| `imul` gpr_one 8 | c | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 36969, seed_rdx = 17607, IN_0 = 50] | [IN_1 = 36969, seed_rdx = 17607, IN_0 = 50] |
| `imul` gpr_one 8 | rust | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 16637, seed_rcx = 3875, IN_0 = 142] | [IN_1 = 16637, seed_rcx = 3875, IN_0 = 142] |
| `mul` gpr_one 16 | c | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1308409511, IN_0 = 4152187579] |
| `mul` gpr_one 16 | rust | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3737403391, IN_0 = 1011728383] |
| `mul` gpr_one 16 | swift | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 133169006, IN_0 = 652369919] |
| `sub` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 56699, IN_1 = 1162543104] |
| `sub` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 44759, IN_1 = 2731737088] |
| `sub` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1263861760, IN_0 = 22989] |
| `xor` gpr_gpr 8 | c | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | rust | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | swift | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `imul` gpr_gpr 16 | c | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2327052288, IN_0 = 47783] |
| `imul` gpr_gpr 16 | rust | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1160511488, IN_0 = 56683] |
| `imul` gpr_gpr 16 | swift | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3836411904, IN_0 = 36267] |

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


## 7. Task ap3's appendix

Three things the brief asks this report to carry which the loop does not compute: the probe that had to land before fix 2 was written, the tally of the `check` that fix 3 un-blocked, and the measurement of task h2's normalise-before-render on its own.

### 7.1 The x87 probe, LITERAL

The brief's rule: probe first, and only render the x87 cells as `long double` if clang emits the x87 opcode for one at the corpus's own ship flags. The compiler is `/usr/bin/clang` and the flags are `-std=c17 -O1 -c` (lane_gen.py compile_probe: `[CLANG, "-std=c17"] + ["-O1"] + ["-c", src, "-o", obj]` -- the ship build of every c unit in the corpus).

| the source | the carved body |
|---|---|
| `long double emu_probe_ld_add(long double a, long double b) {     return a + b; } ` | `fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret` |
| `long double emu_probe_ld_mul(long double a, long double b) {     return a * b; } ` | `fldt 0x18(%rsp); fldt 0x8(%rsp); fmulp %st,%st(1); ret` |

The probe LANDS: clang emits the x87 opcode, so c's `long double` is the 80-bit holder the fix uses. rust, go and swift have none, and their rows are refused by nature.

### 7.2 The `check` tally, after fix 3

`model_translate.py check` stopped on `KeyError: 'mnemonic'` in `load_rows` from log_237 until this task; the one line the brief authorises reads `row["mnem"]`, which is what task mn1 renamed the field to, with `mnemonic` accepted as a fallback for the older artifact.

| artifact | rows | STATED | DISCREPANCY | REFUSED |
|---|---|---|---|---|
| the stored `check_L2.json` | 259 | 153 | 19 | 87 |
| this task's re-derivation | 259 | 172 | 0 | 87 |

The two agree: 259 rows, 87 REFUSED, and 172 the check STATES -- of which the Lean run of record turned 19 into DISCREPANCY, which is why the stored artifact reads 153 + 19. The stored artifact was restored byte for byte after the re-derivation; the re-derived file is beside this report as `autopoly3_check_L2_rerun.json`.

### 7.3 Fix 4: task h2's normalise-before-render, measured alone on 1,012 runs

runs with the fix ON  (autopoly3_runs.jsonl): 1012
runs with the fix OFF (autopoly3_off_runs.jsonl): 1012
pairs on both: 1012

runs whose RENDERED SOURCE differs between the two loops: 15
runs whose VERDICT differs between the two loops: 9

| run | the place | the FIRST line that differs, with the fix OFF | the same line with the fix ON |
|---|---|---|---|
| addsd|xmm_xmm|64|rust | `reg_xmm0` | `f64::from_bits((((((b) + (a))).to_bits() as u64)) as u64)` | `f64::from_bits((((((a) + (b))).to_bits() as u64)) as u64)` |
| addss|xmm_xmm|32|rust | `reg_xmm0` | `f32::from_bits((((((b) + (a))).to_bits() as u32)) as u32)` | `f32::from_bits((((((a) + (b))).to_bits() as u32)) as u32)` |
| addss|xmm_xmm|32|swift | `reg_xmm0` | `return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32((((b) + (a))).bitPattern))))` | `return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32((((a) + (b))).bitPattern))))` |
| setnp|gpr_one|8|c | `reg_rdi` | `return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((((((((((((((((((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1))) + (uint32_t)(UINT32_C(0x1) ...` | `return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) * (uint32_t)(UINT32_C(0xff))) ...` |
| setnp|gpr_one|8|go | `reg_rdi` | `return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(sel32(((((((((((((((((uint32(((uint32((uint32(((uint32((uint32(b)) >> 0)) & uint32(0x1)))) + (uint32(uint32(0x1))))) & uint32(0x1)))) == (u ...` | `return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32 ...` |
| setnp|gpr_one|8|rust | `reg_rdi` | `(((((((0x0u64) as u64) << 8) | (((if (((((((((((((((((((((((((((((b as u32)) >> 0) as u32) & 0x1u32)) as u32)).wrapping_add(((0x1u32) as u32))) as u32) & 0x1u32)) as u32) == (((((((a as u32)) >> 0) as ...` | `(((((((0x0u64) as u64) << 8) | (((if ((((((((((((((((((((((b as u32)) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32)) as u32)).wrapping_add((((a as u32)) as u32))) as u32) & 0xffu32)) a ...` |
| setnp|gpr_one|8|swift | `reg_rdi` | `return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | (UInt64(truncatingIfNeeded: ((((((((((((((((((UInt32(truncatingIfNeeded: ((UInt32(trun ...` | `return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | (UInt64(truncatingIfNeeded: ((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded ...` |
| setp|gpr_one|8|c | `reg_rdi` | `return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((((((((((((((((((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1))) + (uint32_t)(UINT32_C(0x1) ...` | `return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)(((uint32_t)((uint32_t)((uint32_t)b) * (uint32_t)(UINT32_C(0xff))) ...` |
| setp|gpr_one|8|go | `reg_rdi` | `return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(sel32(((((((((((((((((uint32(((uint32((uint32(((uint32((uint32(b)) >> 0)) & uint32(0x1)))) + (uint32(uint32(0x1))))) & uint32(0x1)))) == (u ...` | `return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32 ...` |
| setp|gpr_one|8|rust | `reg_rdi` | `(((((((0x0u64) as u64) << 8) | (((if (((((((((((((((((((((((((((((b as u32)) >> 0) as u32) & 0x1u32)) as u32)).wrapping_add(((0x1u32) as u32))) as u32) & 0x1u32)) as u32) == (((((((a as u32)) >> 0) as ...` | `(((((((0x0u64) as u64) << 8) | (((if ((((((((((((((((((((((b as u32)) as u32)).wrapping_mul(((0xffu32) as u32))) as u32) & 0xffu32)) as u32)).wrapping_add((((a as u32)) as u32))) as u32) & 0xffu32)) a ...` |
| setp|gpr_one|8|swift | `reg_rdi` | `return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | (UInt64(truncatingIfNeeded: ((((((((((((((((((UInt32(truncatingIfNeeded: ((UInt32(trun ...` | `return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | (UInt64(truncatingIfNeeded: ((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded ...` |
| subsd|xmm_xmm|64|rust | `reg_xmm0` | `f64::from_bits(((((((-(b))) + (a))).to_bits() as u64)) as u64)` | `f64::from_bits(((((((-(a))) + (b))).to_bits() as u64)) as u64)` |
| subss|xmm_xmm|32|c | `reg_xmm0` | `return bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)(((-(b))) + (a))))));` | `return bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)(((-(a))) + (b))))));` |
| subss|xmm_xmm|32|rust | `reg_xmm0` | `f32::from_bits(((((((-(a))) + (b))).to_bits() as u32)) as u32)` | `f32::from_bits(((((((-(b))) + (a))).to_bits() as u32)) as u32)` |
| subss|xmm_xmm|32|swift | `reg_xmm0` | `return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32(((((-(b))) + (a))).bitPattern))))` | `return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32(((((-(a))) + (b))).bitPattern))))` |

| run | the verdict with the fix OFF | the verdict with the fix ON |
|---|---|---|
| div|gpr_one|8|rust | NOT_COLLAPSED (8) / DISPROVED, DISPROVED under caller extension | NOT_COLLAPSED (8) / DISPROVED, UNDECIDED under caller extension |
| idiv|gpr_one|16|c | NOT_COLLAPSED (21) / DISPROVED, DISPROVED under caller extension | NOT_COLLAPSED (21) / UNDECIDED, DISPROVED at 30000 ms |
| idiv|gpr_one|16|rust | NOT_COLLAPSED (21) / DISPROVED, UNDECIDED under caller extension | NOT_COLLAPSED (21) / DISPROVED, DISPROVED under caller extension |
| setnp|gpr_one|8|c | NOT_COLLAPSED (26) / PROVED_ON_SHIP | NOT_COLLAPSED (19) / PROVED_ON_SHIP |
| setnp|gpr_one|8|go | NOT_COLLAPSED (42) / PROVED_ON_SHIP | NOT_COLLAPSED (49) / PROVED_ON_SHIP |
| setnp|gpr_one|8|rust | NOT_COLLAPSED (26) / PROVED_ON_SHIP | NOT_COLLAPSED (19) / PROVED_ON_SHIP |
| setp|gpr_one|8|c | NOT_COLLAPSED (27) / PROVED_ON_SHIP | NOT_COLLAPSED (20) / PROVED_ON_SHIP |
| setp|gpr_one|8|go | NOT_COLLAPSED (42) / PROVED_ON_SHIP | NOT_COLLAPSED (49) / PROVED_ON_SHIP |
| setp|gpr_one|8|rust | NOT_COLLAPSED (27) / PROVED_ON_SHIP | NOT_COLLAPSED (20) / PROVED_ON_SHIP |


