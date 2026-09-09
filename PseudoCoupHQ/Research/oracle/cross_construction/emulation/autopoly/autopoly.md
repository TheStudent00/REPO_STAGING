# autopoly.md -- task ap1: AutoPoly's first full loop

Node `hq.research.arch_unit_oracle.cross_construction.autopoly`. Written by `autopoly.py`; never hand-edited.

**What this is, one sentence.** the owner's loop -- for every arch opcode of the model table that the corpus attests, for each of the four compiled targets, `find_emulation(cell, lang)` -- run for the first time over its whole measured outer set: 253 cells x 4 targets = 1012 runs, of which 1012 are recorded here.

The route is `handful.py` as task g1b left it (`handful.py as task g1b left it, TASK g1c: the two printing fixes of task h2, the primitive route before the term route, and the primitive lookup widened by one zero-operand setup step`), imported and called; this task's own program is the loop around it and the bookkeeping, nothing else.

Every count below is of the run's own DESTINATION PLACE -- `handful.destination_place`, the first place the cell writes that is not the flags -- which is the place tasks h1, h2, g1 and g1b's own tables already summarize. The denominator of every share is 133044, the attested ledger rows of the whole outer set.

## 1. THE table: per target, what the loop reached

Table 1 -- one row per target. `cells` counts runs; `rows` is the attested ledger rows those cells cover and `share` that as a percentage of 133044.

| step or verdict | c | rust | go | swift |
|---|---|---|---|---|
| `attempted` | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% | 253 cells, 133044 rows, 100.0% |
| `rendered` | 167 cells, 112151 rows, 84.3% | 167 cells, 112151 rows, 84.3% | 153 cells, 99907 rows, 75.09% | 153 cells, 99907 rows, 75.09% |
| `compiled` | 167 cells, 112151 rows, 84.3% | 167 cells, 112151 rows, 84.3% | 153 cells, 99907 rows, 75.09% | 153 cells, 99907 rows, 75.09% |
| `LANDED` | 62 cells, 36632 rows, 27.53% | 59 cells, 35529 rows, 26.7% | 25 cells, 18849 rows, 14.17% | 57 cells, 35245 rows, 26.49% |
| `LANDED_ELSEWHERE` | 15 cells, 13524 rows, 10.17% | 16 cells, 14268 rows, 10.72% | 8 cells, 5004 rows, 3.76% | 22 cells, 14502 rows, 10.9% |
| `NOT_COLLAPSED` | 90 cells, 61995 rows, 46.6% | 92 cells, 62354 rows, 46.87% | 120 cells, 76054 rows, 57.16% | 74 cells, 50160 rows, 37.7% |
| `proved` | 129 cells, 77735 rows, 58.43% | 132 cells, 82884 rows, 62.3% | 136 cells, 87742 rows, 65.95% | 124 cells, 73007 rows, 54.87% |
| `proved under caller extension` | 15 cells, 19418 rows, 14.6% | 16 cells, 20390 rows, 15.33% | 0 cells, 0 rows, 0.0% | 13 cells, 18670 rows, 14.03% |
| `sat` | 10 cells, 3812 rows, 2.87% | 11 cells, 4685 rows, 3.52% | 8 cells, 3433 rows, 2.58% | 2 cells, 2331 rows, 1.75% |
| `undecided` | 13 cells, 11186 rows, 8.41% | 8 cells, 4192 rows, 3.15% | 9 cells, 8732 rows, 6.56% | 14 cells, 5899 rows, 4.43% |
| `refused` | 86 cells, 20893 rows, 15.7% | 86 cells, 20893 rows, 15.7% | 100 cells, 33137 rows, 24.91% | 100 cells, 33137 rows, 24.91% |

## 2. Per target, how far the primitive route reached

Table 2 -- `primitive` is a target operator whose whole lowered body IS the cell; `primitive+setup` is that plus zero-operand accumulator setup (task g1c's widened lookup); `term` is the cell's own term written in the target's operators, which is the fallback.

| route | c | rust | go | swift |
|---|---|---|---|---|
| `primitive` | 29 cells, 19706 rows, 14.81% | 22 cells, 12245 rows, 9.2% | 17 cells, 10351 rows, 7.78% | 9 cells, 7774 rows, 5.84% |
| `primitive+setup` | 2 cells, 1726 rows, 1.3% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% | 0 cells, 0 rows, 0.0% |
| `term` | 184 cells, 105179 rows, 79.06% | 193 cells, 114366 rows, 85.96% | 198 cells, 116260 rows, 87.38% | 206 cells, 118837 rows, 89.32% |
| `no route reached` | 38 cells, 6433 rows, 4.84% | 38 cells, 6433 rows, 4.84% | 38 cells, 6433 rows, 4.84% | 38 cells, 6433 rows, 4.84% |

## 3. Refusals and non-proofs, by cause

### 3.1 c

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| term reads state that is not an arrival register | 34 | 9629 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movss` mem_xmm 32 (1281 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 1 and 2 IN rows | 1 | 5190 | `xor` gpr_same 32 (5190 rows) |
| the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | 6 | 4862 | `movslq` widen_gpr_gpr None (3728 rows); `movzbl` widen_gpr_gpr None (1033 rows); `movzwl` widen_gpr_gpr None (63 rows) |
| the cell's own key_width is not narrower than the place, so there is no lane to project | 14 | 4831 | `xorps` xmm_same 128 (3013 rows); `movaps` xmm_xmm 128 (980 rows); `xorpd` xmm_same 128 (378 rows) |
| the gate answered sat: the body holds on a region, not on every input | 10 | 3812 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `lea` mem_gpr 64 (277 rows) |
| the gate did not answer: the carved body: the reference: lea addressing form '0x0(,%rdi,8)' is not the (displacement, base, index, scale) shape this file models; and no term either | 2 | 2335 | `shl` imm_gpr 32 (2329 rows); `shl` imm_gpr 64 (6 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | 2 | 1726 | `idiv` gpr_one 64 (948 rows); `idiv` gpr_one 32 (778 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 0 and 1 IN rows | 2 | 840 | `mov` imm_gpr 32 (835 rows); `mov` imm_gpr 8 (5 rows) |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | `div` gpr_one 64 (624 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 2 | 400 | `div` gpr_one 32 (384 rows); `idiv` gpr_one 16 (16 rows) |
| the gate did not answer: the carved body: the reference: arch opcode 'cmovg' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 3 | 71 | `cmovle` gpr_gpr 32 (53 rows); `cmovge` gpr_gpr 32 (12 rows); `cmovge` gpr_gpr 64 (6 rows) |

### 3.2 rust

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| term reads state that is not an arrival register | 34 | 9629 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movss` mem_xmm 32 (1281 rows) |
| the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | 6 | 4862 | `movslq` widen_gpr_gpr None (3728 rows); `movzbl` widen_gpr_gpr None (1033 rows); `movzwl` widen_gpr_gpr None (63 rows) |
| the cell's own key_width is not narrower than the place, so there is no lane to project | 14 | 4831 | `xorps` xmm_same 128 (3013 rows); `movaps` xmm_xmm 128 (980 rows); `xorpd` xmm_same 128 (378 rows) |
| the gate answered sat: the body holds on a region, not on every input | 11 | 4685 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `idiv` gpr_one 64 (948 rows) |
| the gate did not answer: the carved body: the reference: lea addressing form '0x0(,%rdi,8)' is not the (displacement, base, index, scale) shape this file models; and no term either | 2 | 2335 | `shl` imm_gpr 32 (2329 rows); `shl` imm_gpr 64 (6 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 3 | 1786 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 64 (624 rows); `div` gpr_one 32 (384 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| the gate did not answer: the carved body: the reference: arch opcode 'cmovg' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 3 | 71 | `cmovle` gpr_gpr 32 (53 rows); `cmovge` gpr_gpr 32 (12 rows); `cmovge` gpr_gpr 64 (6 rows) |

### 3.3 go

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| a width c has no holder for | 15 | 12565 | `cmp` gpr_gpr 64 (4011 rows); `test` gpr_same 64 (2425 rows); `sbb` gpr_gpr 64 (1478 rows) |
| term reads state that is not an arrival register | 33 | 9308 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movss` mem_xmm 32 (1281 rows) |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 2 | 7471 | `mov` gpr_gpr 64 (7194 rows); `lea` mem_gpr 64 (277 rows) |
| the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | 6 | 4862 | `movslq` widen_gpr_gpr None (3728 rows); `movzbl` widen_gpr_gpr None (1033 rows); `movzwl` widen_gpr_gpr None (63 rows) |
| the cell's own key_width is not narrower than the place, so there is no lane to project | 14 | 4831 | `xorps` xmm_same 128 (3013 rows); `movaps` xmm_xmm 128 (980 rows); `xorpd` xmm_same 128 (378 rows) |
| the gate answered sat: the body holds on a region, not on every input | 8 | 3433 | `ucomiss` xmm_xmm 32 (2270 rows); `cmpneqss` xmm_xmm 32 (307 rows); `subss` xmm_xmm 32 (230 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 4 | 1214 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |
| the gate did not answer: the carved body: the reference: arch opcode 'movswq' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 2 | 19 | `sar` cl_gpr 16 (11 rows); `idiv` gpr_one 8 (8 rows) |

### 3.4 swift

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| a width c has no holder for | 15 | 12565 | `cmp` gpr_gpr 64 (4011 rows); `test` gpr_same 64 (2425 rows); `sbb` gpr_gpr 64 (1478 rows) |
| term reads state that is not an arrival register | 33 | 9308 | `push` gpr_one 64 (3408 rows); `fldt` mem_one 80 (1527 rows); `movss` mem_xmm 32 (1281 rows) |
| the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | 6 | 4862 | `movslq` widen_gpr_gpr None (3728 rows); `movzbl` widen_gpr_gpr None (1033 rows); `movzwl` widen_gpr_gpr None (63 rows) |
| the cell's own key_width is not narrower than the place, so there is no lane to project | 14 | 4831 | `xorps` xmm_same 128 (3013 rows); `movaps` xmm_xmm 128 (980 rows); `xorpd` xmm_same 128 (378 rows) |
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 8 | 3063 | `setp` gpr_one 8 (2125 rows); `idiv` gpr_one 32 (778 rows); `setnp` gpr_one 8 (108 rows) |
| the gate did not answer: the carved body: the reference: lea addressing form '0x0(,%rdi,8)' is not the (displacement, base, index, scale) shape this file models; and no term either | 2 | 2335 | `shl` imm_gpr 32 (2329 rows); `shl` imm_gpr 64 (6 rows) |
| the gate answered sat: the body holds on a region, not on every input | 2 | 2331 | `ucomiss` xmm_xmm 32 (2270 rows); `xor` imm_gpr 8 (61 rows) |
| no setter row to compose the flag pair from: None at width 8 | 32 | 1571 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows); `fadds` mem_one 80 (96 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 2 | 420 | `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |
| the gate did not answer: the carved body: the reference: arch opcode 'cmovg' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | 1 | 53 | `cmovle` gpr_gpr 32 (53 rows) |

## 4. Cells proved on all four targets, on three, two, one, none

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose. The polyfill-complete set is the row `4`.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 120 | 76634 | 57.6% |
| 3 of 4 | 17 | 16985 | 12.77% |
| 2 of 4 | 14 | 9941 | 7.47% |
| 1 of 4 | 6 | 2473 | 1.86% |
| 0 of 4 | 96 | 27011 | 20.3% |

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
| `addsd` xmm_xmm 64 | 244 |
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
| `cmovl` gpr_gpr 32 | 4 |
| `cmovl` gpr_gpr 64 | 8 |
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
| `divsd` xmm_xmm 64 | 118 |
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
| `movabs` imm_gpr 64 | 14 |
| `movd` gpr_xmm 32 | 2313 |
| `movd` xmm_gpr 32 | 760 |
| `movq` gpr_xmm 64 | 140 |
| `movq` xmm_gpr 64 | 312 |
| `movzbl` cl_gpr 32 | 968 |
| `mul` gpr_one 16 | 2 |
| `mul` gpr_one 32 | 2 |
| `mul` gpr_one 64 | 310 |
| `mul` gpr_one 8 | 6 |
| `mulsd` xmm_xmm 64 | 112 |
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
| `test` imm_gpr 8 | 272 |
| `xor` gpr_gpr 32 | 572 |
| `xor` gpr_gpr 64 | 1668 |
| `xor` gpr_gpr 8 | 2 |

### 4.2 The cells proved on no target, in full, with the cause on each

| cell | ledger rows | c | rust | go | swift |
|---|---|---|---|---|---|
| `movslq` widen_gpr_gpr None | 3728 | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType |
| `push` gpr_one 64 | 3408 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `xorps` xmm_same 128 | 3013 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `ucomiss` xmm_xmm 32 | 2270 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `fldt` mem_one 80 | 1527 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movss` mem_xmm 32 | 1281 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movzbl` widen_gpr_gpr None | 1033 | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType |
| `fucomip` st_st 80 | 1031 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `ucomisd` xmm_xmm 64 | 1026 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | a width c has no holder for | a width c has no holder for |
| `movaps` xmm_xmm 128 | 980 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `idiv` gpr_one 64 | 948 | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | the gate answered sat: the body holds on a region, not on every input | a width c has no holder for | a width c has no holder for |
| `movaps` mem_xmm 128 | 942 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `idiv` gpr_one 32 | 778 | the gate did not answer: the IN rows cannot be aligned: the two representatives' canon40 arrival contracts name 3 and 2 IN rows | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `div` gpr_one 64 | 624 | the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | a width c has no holder for | a width c has no holder for |
| `div` gpr_one 32 | 384 | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `xorpd` xmm_same 128 | 378 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `ucomiss` mem_xmm 32 | 342 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fildll` mem_one 80 | 332 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fldz` st_none 80 | 321 | term reads state that is not an arrival register | term reads state that is not an arrival register | a width c has no holder for | a width c has no holder for |
| `movapd` xmm_xmm 128 | 230 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `filds` mem_one 80 | 194 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `cmpneqss` mem_xmm 32 | 154 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `punpckldq` mem_xmm 128 | 132 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `subpd` mem_xmm 128 | 132 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `unpckhpd` xmm_xmm 128 | 132 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `fildl` mem_one 80 | 116 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fucomi` st_st 80 | 108 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `addss` mem_xmm 32 | 107 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `cmpeqss` mem_xmm 32 | 101 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fadds` mem_one 80 | 96 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `mulss` mem_xmm 32 | 91 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `divss` mem_xmm 32 | 65 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `subss` mem_xmm 32 | 65 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movzwl` widen_gpr_gpr None | 63 | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType |
| `movsd` mem_xmm 64 | 58 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `flds` mem_one 80 | 56 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `div` gpr_one 16 | 36 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `pxor` xmm_same 128 | 36 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `faddp` st_st 80 | 30 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fmulp` st_st 80 | 30 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `div` gpr_one 8 | 28 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | None | None |
| `fiadds` mem_one 80 | 28 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fimuls` mem_one 80 | 28 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fldl` mem_one 80 | 28 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movdqa` xmm_xmm 128 | 28 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `ucomisd` mem_xmm 64 | 24 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movswl` widen_gpr_gpr None | 22 | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType |
| `xorps` mem_xmm 128 | 21 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `addsd` mem_xmm 64 | 20 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `cmp` mem_gpr 64 | 20 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `cmpneqsd` mem_xmm 64 | 18 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fiaddl` mem_one 80 | 16 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fimull` mem_one 80 | 16 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `idiv` gpr_one 16 | 16 | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `mov` mem_gpr 64 | 16 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fdivp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivrp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubrp` st_st 80 | 15 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fidivrs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fidivs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubrs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubs` mem_one 80 | 14 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `cmpeqsd` mem_xmm 64 | 12 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movsbl` widen_gpr_gpr None | 12 | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType |
| `mulsd` mem_xmm 64 | 12 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fidivl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fidivrl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fisubrl` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fmuls` mem_one 80 | 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `idiv` gpr_one 8 | 8 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the carved body: the reference: arch opcode 'movswq' has no entry in the opcode table -- no body in the corpus this table was built over spells it; and no term either | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `mov` mem_gpr 32 | 8 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `movzbl` widen_mem_gpr None | 8 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `andpd` xmm_xmm 128 | 6 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `andps` xmm_xmm 128 | 6 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `divsd` mem_xmm 64 | 6 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `orpd` xmm_xmm 128 | 6 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `orps` xmm_xmm 128 | 6 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `subsd` mem_xmm 64 | 6 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `faddl` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivrs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fmull` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubrs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubs` mem_one 80 | 4 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `movsbq` widen_gpr_gpr None | 4 | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType | the driver raised on this (cell, target) pair: TypeError: %d format: a real number is required, not NoneType |
| `movzwl` widen_mem_gpr None | 4 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `punpcklqdq` xmm_xmm 128 | 4 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `pxor` xmm_xmm 128 | 4 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `fdivl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fdivrl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `fsubrl` mem_one 80 | 2 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 | no setter row to compose the flag pair from: None at width 8 |
| `pand` xmm_xmm 128 | 2 | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project | the cell's own key_width is not narrower than the place, so there is no lane to project |
| `pxor` mem_xmm 128 | 2 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |

## 5. Every `sat` verdict, with its counterexample and the region it names

A `sat` is where the target's edge region differs from the opcode's: z3 found a starting state under which the compiled body and the cell's term answer differently. The counterexample is z3's own, LITERAL.

TWO COUNTS, and they are two different things.

- **`sat` at the plain comparison: 110 places.** z3 answered `sat` when the emulation's arriving values are whatever fits the register.
- **`sat` that survives the caller-extension re-pose: 39 places.** Task o7's own rule: pose the same comparison again with every narrow-holder input row zero-extended from its holder width to the register, which is what the target's own calling rule guarantees the caller did. What is left is where the target's edge region really differs from the opcode's.

Table 1's `sat` row counts the second of these at the destination place; this table lists every written place, the flags included.

| cell | lang | place | route | ledger rows | survives the re-pose | region | counterexample (LITERAL) |
|---|---|---|---|---|---|---|---|
| `setne` gpr_one 8 | c | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `setne` gpr_one 8 | rust | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `setne` gpr_one 8 | swift | reg_rdi | term | 10335 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3841776640, IN_0 = 3841776640] |
| `or` gpr_gpr 8 | c | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` gpr_gpr 8 | rust | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` gpr_gpr 8 | swift | reg_rdi | term | 2407 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `ucomiss` xmm_xmm 32 | c | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 2139180370, IN_0 = 2139180354, fp.to_ieee_bv = [NaN -> 2139180370, else -> fp.to_ieee_bv(Var(0))]] | [IN_1 = 2139180370, IN_0 = 2139180354, fp.to_ieee_bv = [NaN -> 2139180370, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | go | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 1048592389, IN_1 = 4294948858, fp.to_ieee_bv = [NaN -> 4294965242, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 1048592389, IN_1 = 4294948858, fp.to_ieee_bv = [NaN -> 4294965242, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | rust | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2139096064, IN_1 = 2692742014, fp.to_ieee_bv = [NaN -> 2139620352, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2139096064, IN_1 = 2692742014, fp.to_ieee_bv = [NaN -> 2139620352, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` xmm_xmm 32 | swift | flags | term | 2270 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2222718846, IN_1 = 2139357249, fp.to_ieee_bv = [NaN -> 2139357185, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2222718846, IN_1 = 2139357249, fp.to_ieee_bv = [NaN -> 2139357185, else -> fp.to_ieee_bv(Var(0))]] |
| `or` cl_gpr 8 | c | reg_rdi | term | 1702 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` cl_gpr 8 | rust | reg_rdi | term | 1702 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `or` cl_gpr 8 | swift | reg_rdi | term | 1702 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040, IN_1 = 0] |
| `and` cl_gpr 8 | c | reg_rdi | term | 1664 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` cl_gpr 8 | rust | reg_rdi | term | 1664 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` cl_gpr 8 | swift | reg_rdi | term | 1664 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `setae` gpr_one 8 | rust | reg_rdi | term | 1552 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2147487809, IN_0 = 2147479489] |
| `ucomisd` xmm_xmm 64 | c | flags | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_1 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` xmm_xmm 64 | rust | flags | term | 1026 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_1 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `movzbl` cl_gpr 32 | c | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` cl_gpr 32 | rust | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4278189824] |
| `movzbl` cl_gpr 32 | swift | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `idiv` gpr_one 64 | rust | reg_rax | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 327, IN_1 = 0, IN_0 = 9223372036854775808, seed_MEM_m0x30_rbp_ = 9223372036854775814] | [IN_2 = 327, IN_1 = 0, IN_0 = 9223372036854775808, seed_MEM_m0x30_rbp_ = 9223372036854775814] |
| `idiv` gpr_one 64 | rust | reg_rdx | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [seed_MEM_m0x20_rbp_ = 6990020241853513728, IN_2 = 11240342942477974528, IN_1 = 1758129895554531707, IN_0 = 10339983088957361747] | [seed_MEM_m0x20_rbp_ = 6990020241853513728, IN_2 = 11240342942477974528, IN_1 = 1758129895554531707, IN_0 = 10339983088957361747] |
| `and` gpr_gpr 8 | c | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | rust | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | swift | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `add` gpr_gpr 64 | c | reg_rdi | primitive | 744 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 9223372028264841216] |
| `cmp` gpr_gpr 16 | c | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2762670080, IN_0 = 44395] |
| `cmp` gpr_gpr 16 | rust | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1363345408, IN_0 = 55167] |
| `cmp` gpr_gpr 16 | swift | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 710148096, IN_0 = 60119] |
| `div` gpr_one 32 | c | reg_rdx | term | 384 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 0, IN_1 = 1404940345, IN_0 = 1862566266] | [IN_2 = 0, IN_1 = 1404940345, IN_0 = 1862566266] |
| `div` gpr_one 32 | rust | reg_rdx | term | 384 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 1147387202, IN_0 = 2114510848, IN_2 = 0] | [IN_1 = 1147387202, IN_0 = 2114510848, IN_2 = 0] |
| `cmpneqss` xmm_xmm 32 | go | reg_xmm0 | term | 307 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 64 | c | reg_rdi | primitive | 277 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `sbb` gpr_same 32 | rust | reg_rdi | term | 268 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 2047, IN_0 = 4294965247] | [IN_1 = 2047, IN_0 = 4294965247] |
| `sub` cl_gpr 8 | c | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 29696, IN_0 = 117] |
| `sub` cl_gpr 8 | rust | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 5120, IN_0 = 247] |
| `sub` cl_gpr 8 | swift | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 139, IN_1 = 51200] |
| `add` cl_gpr 8 | c | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 35328, IN_0 = 187] |
| `add` cl_gpr 8 | rust | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 39680, IN_0 = 179] |
| `add` cl_gpr 8 | swift | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 43776, IN_0 = 171] |
| `subss` xmm_xmm 32 | go | reg_xmm0 | term | 230 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 15275064, IN_0 = 3774874985, IN_1 = 3774873187, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 15275064, IN_0 = 3774874985, IN_1 = 3774873187, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqss` xmm_xmm 32 | go | reg_xmm0 | term | 198 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `cmp` gpr_gpr 8 | c | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 37888, IN_0 = 181] |
| `cmp` gpr_gpr 8 | rust | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 13312, IN_0 = 247] |
| `cmp` gpr_gpr 8 | swift | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 43, IN_1 = 27648] |
| `cmpneqsd` xmm_xmm 64 | go | reg_xmm0 | term | 190 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `sbb` imm_gpr 8 | rust | reg_rdi | term | 164 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2147487809, IN_0 = 2147479489] |
| `subsd` xmm_xmm 64 | go | reg_xmm0 | term | 118 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 17527547440773425954, IN_0 = 9218868437227405312, IN_1 = 15400966384218192703, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 17527547440773425954, IN_0 = 9218868437227405312, IN_1 = 15400966384218192703, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqsd` xmm_xmm 64 | go | reg_xmm0 | term | 116 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 32 | c | reg_rdi | primitive | 82 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `xor` imm_gpr 8 | c | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | rust | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | swift | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_same 8 | c | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | rust | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | swift | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `shr` cl_gpr 8 | c | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2, IN_0 = 2395763544] |
| `shr` cl_gpr 8 | rust | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4238248362] |
| `shr` cl_gpr 8 | swift | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 7, IN_0 = 3755999136] |
| `div` gpr_one 16 | c | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 1073872897, IN_0 = 49207, IN_1 = 0] | [IN_2 = 1073872897, IN_0 = 49207, IN_1 = 0] |
| `div` gpr_one 16 | c | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 196608, IN_1 = 535855141, IN_0 = 32767] | [IN_2 = 196608, IN_1 = 535855141, IN_0 = 32767] |
| `div` gpr_one 16 | rust | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 16384, IN_2 = 131072, IN_1 = 2111] | [IN_0 = 16384, IN_2 = 131072, IN_1 = 2111] |
| `div` gpr_one 16 | rust | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 2147491840, IN_1 = 2147487744, IN_0 = 0] | [IN_2 = 2147491840, IN_1 = 2147487744, IN_0 = 0] |
| `div` gpr_one 16 | swift | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 40459, IN_1 = 39940, IN_2 = 0] | [IN_0 = 40459, IN_1 = 39940, IN_2 = 0] |
| `or` gpr_gpr 16 | c | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | rust | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | swift | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `div` gpr_one 8 | c | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 1140891648, IN_0 = 65535] | [IN_1 = 1140891648, IN_0 = 65535] |
| `div` gpr_one 8 | rust | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 3472914431, IN_0 = 65535] | [IN_1 = 3472914431, IN_0 = 65535] |
| `cwtl` none 64 | c | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 10114, IN_0 = 3365076992] | [seed_r8 = 10114, IN_0 = 3365076992] |
| `cwtl` none 64 | rust | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 65535, IN_0 = 1566769152] | [seed_r8 = 65535, IN_0 = 1566769152] |
| `sub` gpr_gpr 8 | c | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 35584, IN_0 = 187] |
| `sub` gpr_gpr 8 | rust | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 18944, IN_0 = 251] |
| `sub` gpr_gpr 8 | swift | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 18944, IN_0 = 75] |
| `idiv` gpr_one 16 | c | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 560209920, IN_1 = 661331444, IN_0 = 32768] | [IN_2 = 560209920, IN_1 = 661331444, IN_0 = 32768] |
| `idiv` gpr_one 16 | rust | reg_rax | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 294557861, IN_1 = 47257, IN_0 = 39188] | [IN_2 = 294557861, IN_1 = 47257, IN_0 = 39188] |
| `idiv` gpr_one 16 | rust | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 7962624, IN_0 = 8077, IN_1 = 3765619200] | [IN_2 = 7962624, IN_0 = 8077, IN_1 = 3765619200] |
| `shr` cl_gpr 16 | c | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 1662855168, IN_1 = 10] |
| `shr` cl_gpr 16 | rust | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 11, IN_0 = 66003008] |
| `shr` cl_gpr 16 | swift | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 15, IN_0 = 4290707456] |
| `idiv` gpr_one 8 | c | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 64000, IN_0 = 32768, seed_rdx = 64000] | [IN_1 = 64000, IN_0 = 32768, seed_rdx = 64000] |
| `idiv` gpr_one 8 | rust | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 24577, IN_0 = 46544] | [IN_1 = 24577, IN_0 = 46544] |
| `mul` gpr_one 8 | c | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1659852671, IN_0 = 190] |
| `mul` gpr_one 8 | rust | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1984951797, IN_0 = 119] |
| `mul` gpr_one 8 | swift | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3583898879, IN_0 = 126] |
| `seto` gpr_one 8 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `seto` gpr_one 8 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `xor` imm_gpr 32 | go | reg_rdi | primitive | 4 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_gpr 8 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 31744, IN_0 = 167] |
| `add` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1666449408, IN_0 = 50711] |
| `add` gpr_gpr 8 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 27392, IN_0 = 235] |
| `add` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1427374080, IN_0 = 54391] |
| `add` gpr_gpr 8 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 43776, IN_0 = 171] |
| `add` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 718536704, IN_0 = 31383] |
| `imul` gpr_one 8 | c | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 33225, seed_rdx = 8839, IN_0 = 114] | [IN_1 = 33225, seed_rdx = 8839, IN_0 = 114] |
| `imul` gpr_one 8 | rust | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 203, seed_rcx = 63973, IN_0 = 18] | [IN_1 = 203, seed_rcx = 63973, IN_0 = 18] |
| `mul` gpr_one 16 | c | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 628031358, IN_0 = 1879048191] |
| `mul` gpr_one 16 | rust | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1883847935, IN_0 = 3108892613] |
| `mul` gpr_one 16 | swift | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1787577967, IN_0 = 2537914199] |
| `sub` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 999555072, IN_0 = 29245] |
| `sub` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 45679, IN_1 = 2603548672] |
| `sub` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 44527, IN_1 = 2762211328] |
| `xor` gpr_gpr 8 | c | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | rust | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | swift | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `imul` gpr_gpr 16 | c | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2770927616, IN_0 = 42347] |
| `imul` gpr_gpr 16 | rust | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2451832832, IN_0 = 46831] |
| `imul` gpr_gpr 16 | swift | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1428422656, IN_0 = 54639] |

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

