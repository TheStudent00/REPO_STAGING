# autopoly4.md -- task ap4: AutoPoly's loop, fourth pass

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
| `NOT_COLLAPSED` | 138 cells, 72141 rows, 54.22% | 110 cells, 72068 rows, 54.17% | 146 cells, 77229 rows, 58.05% | 91 cells, 61147 rows, 45.96% |
| `proved` | 204 cells, 98747 rows, 74.22% | 170 cells, 96021 rows, 72.17% | 177 cells, 113587 rows, 85.38% | 163 cells, 89240 rows, 67.08% |
| `proved under caller extension` | 20 cells, 20530 rows, 15.43% | 21 cells, 21502 rows, 16.16% | 0 cells, 0 rows, 0.0% | 17 cells, 19778 rows, 14.87% |
| `sat` | 19 cells, 6794 rows, 5.11% | 15 cells, 5085 rows, 3.82% | 17 cells, 5181 rows, 3.89% | 5 cells, 3723 rows, 2.8% |
| `undecided` | 2 cells, 1008 rows, 0.76% | 3 cells, 1786 rows, 1.34% | 6 cells, 1250 rows, 0.94% | 15 cells, 7277 rows, 5.47% |
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
| the gate answered sat: the body holds on a region, not on every input | 19 | 6794 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `idiv` gpr_one 64 (948 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| answer home or arrival on the x87 stack | 3 | 1460 | `fucomip` st_st 80 (1031 rows); `fldz` st_none 80 (321 rows); `fucomi` st_st 80 (108 rows) |
| the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | 1 | 624 | `div` gpr_one 64 (624 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 1 | 384 | `div` gpr_one 32 (384 rows) |

### 3.2 rust

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| the gate answered sat: the body holds on a region, not on every input | 15 | 5085 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `idiv` gpr_one 64 (948 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| answer home or arrival on the x87 stack | 37 | 3006 | `fldt` mem_one 80 (1527 rows); `fildll` mem_one 80 (332 rows); `fldz` st_none 80 (321 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 3 | 1786 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 64 (624 rows); `div` gpr_one 32 (384 rows) |
| a width c has no holder for | 2 | 1139 | `fucomip` st_st 80 (1031 rows); `fucomi` st_st 80 (108 rows) |

### 3.3 go

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| a width c has no holder for | 11 | 5515 | `sbb` gpr_gpr 64 (1478 rows); `fucomip` st_st 80 (1031 rows); `idiv` gpr_one 64 (948 rows) |
| the gate answered sat: the body holds on a region, not on every input | 17 | 5181 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| answer home or arrival on the x87 stack | 37 | 3006 | `fldt` mem_one 80 (1527 rows); `fildll` mem_one 80 (332 rows); `fldz` st_none 80 (321 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 4 | 1214 | `idiv` gpr_one 32 (778 rows); `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |

### 3.4 swift

| cause | cells | ledger rows | three examples |
|---|---|---|---|
| the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either | 12 | 6829 | `movslq` widen_gpr_gpr 64 (3728 rows); `setp` gpr_one 8 (2125 rows); `idiv` gpr_one 32 (778 rows) |
| a width c has no holder for | 11 | 5515 | `sbb` gpr_gpr 64 (1478 rows); `fucomip` st_st 80 (1031 rows); `idiv` gpr_one 64 (948 rows) |
| term reads state that is not an arrival register | 5 | 4505 | `push` gpr_one 64 (3408 rows); `movaps` mem_xmm 128 (942 rows); `subpd` mem_xmm 128 (132 rows) |
| the gate answered sat: the body holds on a region, not on every input | 5 | 3723 | `ucomiss` xmm_xmm 32 (2270 rows); `ucomisd` xmm_xmm 64 (1026 rows); `ucomiss` mem_xmm 32 (342 rows) |
| answer home or arrival on the x87 stack | 37 | 3006 | `fldt` mem_one 80 (1527 rows); `fildll` mem_one 80 (332 rows); `fldz` st_none 80 (321 rows) |
| the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | 2 | 420 | `div` gpr_one 32 (384 rows); `div` gpr_one 16 (36 rows) |

## 4. Cells proved on all four targets, on three, two, one, none

Table 3 -- a cell counts as proved on a target when the gate answered `unsat` at that target's destination place, at the 3,000 ms ceiling of record or under the caller-extension re-pose. The polyfill-complete set is the row `4`.

| proved on | cells | ledger rows | share |
|---|---|---|---|
| 4 of 4 | 162 | 106032 | 79.7% |
| 3 of 4 | 23 | 8955 | 6.73% |
| 2 of 4 | 7 | 2804 | 2.11% |
| 1 of 4 | 41 | 2804 | 2.11% |
| 0 of 4 | 20 | 12449 | 9.36% |

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
| `cmp` gpr_gpr 64 | 4011 |
| `cmp` gpr_gpr 8 | 194 |
| `cmp` imm_gpr 16 | 117 |
| `cmp` imm_gpr 32 | 161 |
| `cmp` imm_gpr 64 | 404 |
| `cmp` imm_gpr 8 | 116 |
| `cmp` mem_gpr 64 | 20 |
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
| `mov` gpr_gpr 64 | 7194 |
| `mov` gpr_same 32 | 84 |
| `mov` imm_gpr 16 | 1 |
| `mov` imm_gpr 64 | 14 |
| `mov` mem_gpr 32 | 8 |
| `mov` mem_gpr 64 | 16 |
| `movabs` imm_gpr 64 | 14 |
| `movapd` xmm_xmm 128 | 230 |
| `movaps` xmm_xmm 128 | 980 |
| `movd` gpr_xmm 32 | 2313 |
| `movd` xmm_gpr 32 | 760 |
| `movdqa` xmm_xmm 128 | 28 |
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
| `punpcklqdq` xmm_xmm 128 | 4 |
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
| `test` gpr_same 64 | 2425 |
| `test` gpr_same 8 | 720 |
| `test` imm_gpr 64 | 2 |
| `test` imm_gpr 8 | 272 |
| `unpckhpd` xmm_xmm 128 | 132 |
| `xor` gpr_gpr 32 | 572 |
| `xor` gpr_gpr 64 | 1668 |
| `xor` gpr_gpr 8 | 2 |
| `xor` gpr_same 32 | 5190 |
| `xorpd` xmm_same 128 | 378 |
| `xorps` xmm_same 128 | 3013 |

### 4.2 The cells proved on no target, in full, with the cause on each

| cell | ledger rows | c | rust | go | swift |
|---|---|---|---|---|---|
| `push` gpr_one 64 | 3408 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `ucomiss` xmm_xmm 32 | 2270 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `fucomip` st_st 80 | 1031 | answer home or arrival on the x87 stack | a width c has no holder for | a width c has no holder for | a width c has no holder for |
| `ucomisd` xmm_xmm 64 | 1026 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `idiv` gpr_one 64 | 948 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | a width c has no holder for | a width c has no holder for |
| `movaps` mem_xmm 128 | 942 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `idiv` gpr_one 32 | 778 | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `div` gpr_one 64 | 624 | the gate did not answer: the carved body: the reference: every path through this body leaves the unit or is unreachable, so the body leaves no answer to read; and no term either | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | a width c has no holder for | a width c has no holder for |
| `div` gpr_one 32 | 384 | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `ucomiss` mem_xmm 32 | 342 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `fldz` st_none 80 | 321 | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack | answer home or arrival on the x87 stack |
| `subpd` mem_xmm 128 | 132 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `fucomi` st_st 80 | 108 | answer home or arrival on the x87 stack | a width c has no holder for | a width c has no holder for | a width c has no holder for |
| `div` gpr_one 16 | 36 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |
| `div` gpr_one 8 | 28 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | None | None |
| `ucomisd` mem_xmm 64 | 24 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input |
| `xorps` mem_xmm 128 | 21 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |
| `idiv` gpr_one 16 | 16 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | the gate did not answer: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `idiv` gpr_one 8 | 8 | the gate answered sat: the body holds on a region, not on every input | the gate answered sat: the body holds on a region, not on every input | None | the gate did not answer: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |
| `pxor` mem_xmm 128 | 2 | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register | term reads state that is not an arrival register |

## 5. Every `sat` verdict, with its counterexample and the region it names

A `sat` is where the target's edge region differs from the opcode's: z3 found a starting state under which the compiled body and the cell's term answer differently. The counterexample is z3's own, LITERAL.

TWO COUNTS, and they are two different things.

- **`sat` at the plain comparison: 155 places.** z3 answered `sat` when the emulation's arriving values are whatever fits the register.
- **`sat` that survives the caller-extension re-pose: 70 places.** Task o7's own rule: pose the same comparison again with every narrow-holder input row zero-extended from its holder width to the register, which is what the target's own calling rule guarantees the caller did. What is left is where the target's edge region really differs from the opcode's.

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
| `movzbl` cl_gpr 32 | rust | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294934272] |
| `movzbl` cl_gpr 32 | swift | reg_rdi | term | 968 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `idiv` gpr_one 64 | c | reg_rax | primitive+setup | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 9223372036854775808, IN_0 = 9223372036854775808] | [IN_1 = 9223372036854775808, IN_0 = 9223372036854775808] |
| `idiv` gpr_one 64 | rust | reg_rax | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 7, IN_1 = 12649735990349546496, IN_0 = 3803103737137711046, seed_MEM_m0x30_rbp_ = 9872865596828980816] | [IN_2 = 7, IN_1 = 12649735990349546496, IN_0 = 3803103737137711046, seed_MEM_m0x30_rbp_ = 9872865596828980816] |
| `idiv` gpr_one 64 | rust | reg_rdx | term | 948 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 5064076304905293826, IN_1 = 9766348185539085879, IN_0 = 14174280118870834934, seed_MEM_m0x20_rbp_ = 5071832184407457794] | [IN_2 = 5064076304905293826, IN_1 = 9766348185539085879, IN_0 = 14174280118870834934, seed_MEM_m0x20_rbp_ = 5071832184407457794] |
| `and` gpr_gpr 8 | c | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | rust | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `and` gpr_gpr 8 | swift | reg_rdi | term | 896 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 4294967040, IN_0 = 4294967040] |
| `mov` imm_gpr 32 | c | reg_rdi | primitive | 835 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `idiv` gpr_one 32 | c | reg_rax | primitive+setup | 778 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2148532224, IN_1 = 0] | [IN_0 = 2148532224, IN_1 = 0] |
| `add` gpr_gpr 64 | c | reg_rdi | primitive | 744 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 18446744000695107584] |
| `cmp` gpr_gpr 16 | c | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 850067456, IN_0 = 59051] |
| `cmp` gpr_gpr 16 | rust | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2755919872, IN_0 = 44543] |
| `cmp` gpr_gpr 16 | swift | flags | term | 410 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 27319, IN_1 = 714473472] |
| `div` gpr_one 32 | rust | reg_rdx | term | 384 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 3, IN_1 = 4293394431, IN_2 = 0] | [IN_0 = 3, IN_1 = 4293394431, IN_2 = 0] |
| `ucomiss` mem_xmm 32 | c | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 2139649398, IN_0 = 625245351, fp.to_ieee_bv = [NaN -> 2139911542, else -> fp.to_ieee_bv(Var(0))]] | [IN_1 = 2139649398, IN_0 = 625245351, fp.to_ieee_bv = [NaN -> 2139911542, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | go | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2144953990, IN_1 = 3448085980, fp.to_ieee_bv = [NaN -> 2143905414, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2144953990, IN_1 = 3448085980, fp.to_ieee_bv = [NaN -> 2143905414, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | rust | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 2221932542, IN_1 = 2139095136, fp.to_ieee_bv = [NaN -> 2139095104, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 2221932542, IN_1 = 2139095136, fp.to_ieee_bv = [NaN -> 2139095104, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomiss` mem_xmm 32 | swift | flags | term | 342 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4293521774, IN_1 = 157454751, fp.to_ieee_bv = [NaN -> 4289327470, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 4293521774, IN_1 = 157454751, fp.to_ieee_bv = [NaN -> 4289327470, else -> fp.to_ieee_bv(Var(0))]] |
| `cmpneqss` xmm_xmm 32 | go | reg_xmm0 | term | 307 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 64 | c | reg_rdi | primitive | 277 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `sbb` gpr_same 32 | rust | reg_rdi | term | 268 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4294965247, IN_1 = 2047] | [IN_0 = 4294965247, IN_1 = 2047] |
| `sub` cl_gpr 8 | c | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 22784, IN_0 = 89] |
| `sub` cl_gpr 8 | rust | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 37888, IN_0 = 151] |
| `sub` cl_gpr 8 | swift | flags | term | 253 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 247, IN_1 = 13312] |
| `add` cl_gpr 8 | c | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 29696, IN_0 = 117] |
| `add` cl_gpr 8 | rust | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 239, IN_1 = 9216] |
| `add` cl_gpr 8 | swift | flags | term | 251 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 43776, IN_0 = 171] |
| `subss` xmm_xmm 32 | go | reg_xmm0 | term | 230 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 2779313256, IN_0 = 758203452, IN_1 = 0, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 2779313256, IN_0 = 758203452, IN_1 = 0, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqss` xmm_xmm 32 | go | reg_xmm0 | term | 198 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `cmp` gpr_gpr 8 | c | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 31744, IN_0 = 251] |
| `cmp` gpr_gpr 8 | rust | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 182, IN_1 = 37888] |
| `cmp` gpr_gpr 8 | swift | flags | term | 194 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 103, IN_1 = 62208] |
| `cmpneqsd` xmm_xmm 64 | go | reg_xmm0 | term | 190 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `sbb` imm_gpr 8 | rust | reg_rdi | term | 164 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2147487809, IN_0 = 2147479489] |
| `cmpneqss` mem_xmm 32 | go | reg_xmm0 | term | 154 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `subsd` xmm_xmm 64 | go | reg_xmm0 | term | 118 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 11696391265926980741, IN_0 = 15898249743227232388, IN_1 = 18370182922994844673, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 11696391265926980741, IN_0 = 15898249743227232388, IN_1 = 18370182922994844673, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `cmpeqsd` xmm_xmm 64 | go | reg_xmm0 | term | 116 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `cmpeqss` mem_xmm 32 | go | reg_xmm0 | term | 101 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `lea` mem_gpr 32 | c | reg_rdi | primitive | 82 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `subss` mem_xmm 32 | go | reg_xmm0 | term | 65 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 1896253558, IN_0 = 2088943616, IN_1 = 2147483648, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 1896253558, IN_0 = 2088943616, IN_1 = 2147483648, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `movzwl` widen_gpr_gpr 32 | c | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4261347328] |
| `movzwl` widen_gpr_gpr 32 | rust | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_gpr_gpr 32 | swift | reg_rdi | term | 63 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `xor` imm_gpr 8 | c | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | rust | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `xor` imm_gpr 8 | swift | reg_rdi | primitive | 61 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_same 8 | c | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | rust | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `add` gpr_same 8 | swift | flags | term | 53 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 65280] |
| `shr` cl_gpr 8 | c | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 7, IN_0 = 4155244416] |
| `shr` cl_gpr 8 | rust | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 3976373140] |
| `shr` cl_gpr 8 | swift | reg_rdi | term | 41 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 7, IN_0 = 4135059328] |
| `div` gpr_one 16 | c | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 723787776, IN_0 = 22083, IN_1 = 65535] | [IN_2 = 723787776, IN_0 = 22083, IN_1 = 65535] |
| `div` gpr_one 16 | c | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 3221291008, IN_1 = 2953543713, IN_0 = 12278] | [IN_2 = 3221291008, IN_1 = 2953543713, IN_0 = 12278] |
| `div` gpr_one 16 | rust | reg_rax | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 65461, IN_2 = 28191773, IN_0 = 65535] | [IN_1 = 65461, IN_2 = 28191773, IN_0 = 65535] |
| `div` gpr_one 16 | rust | reg_rdx | term | 36 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 0, IN_1 = 2147518161, IN_0 = 32767] | [IN_2 = 0, IN_1 = 2147518161, IN_0 = 32767] |
| `or` gpr_gpr 16 | c | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | rust | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `or` gpr_gpr 16 | swift | reg_rdi | term | 34 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760, IN_1 = 0] |
| `div` gpr_one 8 | c | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 0, IN_0 = 65534] | [IN_1 = 0, IN_0 = 65534] |
| `div` gpr_one 8 | rust | reg_rax | term | 28 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 1073741824, IN_0 = 65535] | [IN_1 = 1073741824, IN_0 = 65535] |
| `ucomisd` mem_xmm 64 | c | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | c | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | go | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | go | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | rust | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | rust | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | swift | flags.low | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `ucomisd` mem_xmm 64 | swift | flags.high | term | 24 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] | [IN_0 = 18446744073709551614, fp.to_ieee_bv = [NaN -> 9218868437227405313, else -> fp.to_ieee_bv(Var(0))]] |
| `cwtl` none 64 | c | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 31743, IN_0 = 2202468352] | [seed_r8 = 31743, IN_0 = 2202468352] |
| `cwtl` none 64 | rust | reg_rax | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 2162687, IN_0 = 1680211968] | [seed_r8 = 2162687, IN_0 = 1680211968] |
| `movswl` widen_gpr_gpr 32 | c | reg_rdi | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 8912895, IN_0 = 2198339584] | [seed_r8 = 8912895, IN_0 = 2198339584] |
| `movswl` widen_gpr_gpr 32 | rust | reg_rdi | term | 22 | yes | holds on a region, not on every input; z3's counterexample: [seed_r8 = 65535, IN_0 = 3696132096] | [seed_r8 = 65535, IN_0 = 3696132096] |
| `sub` gpr_gpr 8 | c | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 239, IN_1 = 25600] |
| `sub` gpr_gpr 8 | rust | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 183, IN_1 = 37632] |
| `sub` gpr_gpr 8 | swift | flags | term | 19 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 171, IN_1 = 43776] |
| `cmpneqsd` mem_xmm 64 | go | reg_xmm0 | term | 18 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `idiv` gpr_one 16 | c | reg_rax | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 3825412232, IN_0 = 9398, IN_1 = 14977] | [IN_2 = 3825412232, IN_0 = 9398, IN_1 = 14977] |
| `idiv` gpr_one 16 | c | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 841037869, IN_1 = 1192830392, IN_0 = 9499] | [IN_2 = 841037869, IN_1 = 1192830392, IN_0 = 9499] |
| `idiv` gpr_one 16 | rust | reg_rax | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 2256601088, IN_0 = 1139, IN_1 = 55389] | [IN_2 = 2256601088, IN_0 = 1139, IN_1 = 55389] |
| `idiv` gpr_one 16 | rust | reg_rdx | term | 16 | yes | holds on a region, not on every input; z3's counterexample: [IN_2 = 2776643837, IN_0 = 78, IN_1 = 1081591557] | [IN_2 = 2776643837, IN_0 = 78, IN_1 = 1081591557] |
| `cmpeqsd` mem_xmm 64 | go | reg_xmm0 | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0, IN_1 = 0] | [IN_0 = 0, IN_1 = 0] |
| `movsbl` widen_gpr_gpr 32 | c | reg_rdi | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4294967040] | [IN_0 = 4294967040] |
| `movsbl` widen_gpr_gpr 32 | rust | reg_rdi | term | 12 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 4294967040] | [IN_0 = 4294967040] |
| `shr` cl_gpr 16 | c | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4290183168, IN_1 = 15] |
| `shr` cl_gpr 16 | rust | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 1141122230] |
| `shr` cl_gpr 16 | swift | reg_rdi | term | 11 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4290707456, IN_1 = 15] |
| `idiv` gpr_one 8 | c | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 32768, IN_0 = 48315, seed_rdx = 0] | [IN_1 = 32768, IN_0 = 48315, seed_rdx = 0] |
| `idiv` gpr_one 8 | rust | reg_rax | term | 8 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 9872, IN_0 = 12856] | [IN_1 = 9872, IN_0 = 12856] |
| `movzbl` widen_mem_gpr 32 | c | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` widen_mem_gpr 32 | rust | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzbl` widen_mem_gpr 32 | swift | reg_rdi | term | 8 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `mul` gpr_one 8 | c | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1208891262, IN_0 = 163] |
| `mul` gpr_one 8 | rust | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2164466863, IN_0 = 254] |
| `mul` gpr_one 8 | swift | reg_rax | term | 6 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2641859989, IN_0 = 225] |
| `subsd` mem_xmm 64 | go | reg_xmm0 | term | 6 | yes | holds on a region, not on every input; z3's counterexample: [ripconst_0_body = 4607542336843613507, IN_0 = 4607542336843613507, IN_1 = 13840078179776608847, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] | [ripconst_0_body = 4607542336843613507, IN_0 = 4607542336843613507, IN_1 = 13840078179776608847, fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]] |
| `mov` imm_gpr 8 | c | reg_rdi | primitive | 5 | yes | holds on a region, not on every input; z3's counterexample: [] | [] |
| `movsbq` widen_gpr_gpr 64 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movsbq` widen_gpr_gpr 64 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294967040] |
| `movzwl` widen_mem_gpr 32 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4026466304] |
| `movzwl` widen_mem_gpr 32 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `movzwl` widen_mem_gpr 32 | swift | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 4294901760] |
| `seto` gpr_one 8 | c | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `seto` gpr_one 8 | rust | reg_rdi | term | 4 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 110, IN_0 = 374] |
| `xor` imm_gpr 32 | go | reg_rdi | primitive | 4 | yes | holds on a region, not on every input; z3's counterexample: [IN_0 = 0] | [IN_0 = 0] |
| `add` gpr_gpr 8 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 30208, IN_0 = 181] |
| `add` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 382992384, IN_0 = 37525] |
| `add` gpr_gpr 8 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 27392, IN_0 = 235] |
| `add` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 303759360, IN_0 = 63211] |
| `add` gpr_gpr 8 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 46080, IN_0 = 165] |
| `add` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3124363264, IN_0 = 41483] |
| `imul` gpr_one 8 | c | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 233, seed_rdx = 34519, IN_0 = 82] | [IN_1 = 233, seed_rdx = 34519, IN_0 = 82] |
| `imul` gpr_one 8 | rust | reg_rax | term | 2 | yes | holds on a region, not on every input; z3's counterexample: [IN_1 = 102, seed_rcx = 32171, IN_0 = 148] | [IN_1 = 102, seed_rcx = 32171, IN_0 = 148] |
| `mul` gpr_one 16 | c | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1030553599, IN_0 = 823852913] |
| `mul` gpr_one 16 | rust | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3144744958, IN_0 = 821280767] |
| `mul` gpr_one 16 | swift | reg_rdx | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1128356839, IN_0 = 3512917903] |
| `sub` gpr_gpr 16 | c | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2838691840, IN_0 = 43895] |
| `sub` gpr_gpr 16 | rust | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 2771058688, IN_0 = 42283] |
| `sub` gpr_gpr 16 | swift | flags | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_0 = 47855, IN_1 = 2317549568] |
| `xor` gpr_gpr 8 | c | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | rust | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `xor` gpr_gpr 8 | swift | reg_rdi | term | 2 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 0, IN_0 = 4294967040] |
| `imul` gpr_gpr 16 | c | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 3042705408, IN_0 = 38215] |
| `imul` gpr_gpr 16 | rust | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 902430720, IN_0 = 62731] |
| `imul` gpr_gpr 16 | swift | flags | term | 1 | no, proved once zero-extended | holds on every input once each narrow-holder row is zero-extended to the register | [IN_1 = 1361313792, IN_0 = 55151] |

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
| `idiv` gpr_one 32 | c | primitive+setup / NOT_COLLAPSED (2) / DISPROVED | primitive+setup / NOT_COLLAPSED (2) / UNDECIDED, UNDECIDED at 300000 ms | **no** | **no** |
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

Agree character for character: 32 of 40. Agree on the verdict, the re-pose's own ceiling aside: 35 -- this loop re-poses an UNDECIDED once at 30,000 ms where the handful re-posed at 300,000 ms, which is this brief's own instruction, so the two differ in that number and in nothing else.

