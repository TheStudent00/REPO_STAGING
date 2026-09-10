# level 0 checked against an independent reading

Our reference's mappings (`Research/op_pipeline/reference.py`, through the model table) against the K-framework x86-64 semantics (Dasgupta et al., PLDI 2019), read from `/sources/X86-64-semantics` under the University of Illinois/NCSA Open Source License and never copied here.

Every rendering below is printed by ONE printer, ours: `term.Term.normalize`, the pipeline's own layer-5 re-render. A term shown as `theirs` is THEIR rule as this grammar parsed it, printed by our printer -- not their file's text.

Table 1 -- the headline.

| what | count |
|---|---|
| their variants | 3070 |
| variants both readings hold | 397 |
| our translated triples | 5912 |
| our triples an independent reading reaches | 368 |
| places compared (`unsat` + `sat`) | 1143 |
| places that AGREE (`unsat`) | 760 |
| places that DISAGREE (`sat`) | 383 |
| places `unknown` at the ceiling | 0 |
| places their reading leaves UNDEFINED | 197 |
| places `refused` | 439 |
| variants agreeing on every place compared | 192 |
| variants with at least one disagreement | 157 |

Table 2 -- per mnemonic, every outcome. `attested rows` is the corpus's own ledger rows behind those cells, carried from the model table.

| mnem | variants | places | agree | disagree | unknown | undefined | refused | attested rows |
|---|---|---|---|---|---|---|---|---|
| `adc` | 19 | 133 | 8 | 102 | 0 | 0 | 23 | 520 |
| `sbb` | 19 | 133 | 8 | 102 | 0 | 0 | 23 | 2510 |
| `add` | 19 | 133 | 46 | 64 | 0 | 0 | 23 | 795 |
| `sub` | 19 | 133 | 91 | 19 | 0 | 0 | 23 | 938 |
| `neg` | 4 | 28 | 14 | 10 | 0 | 0 | 4 | 211 |
| `and` | 19 | 133 | 103 | 7 | 0 | 19 | 4 | 5626 |
| `or` | 19 | 133 | 103 | 7 | 0 | 19 | 4 | 5902 |
| `xor` | 19 | 133 | 103 | 7 | 0 | 19 | 4 | 2311 |
| `xchg` | 9 | 18 | 6 | 4 | 0 | 0 | 8 | 0 |
| `sar` | 8 | 56 | 4 | 4 | 0 | 4 | 44 | 2182 |
| `shl` | 8 | 56 | 4 | 4 | 0 | 4 | 44 | 3666 |
| `shr` | 8 | 56 | 4 | 4 | 0 | 4 | 44 | 963 |
| `mov` | 6 | 6 | 3 | 3 | 0 | 0 | 0 | 11089 |
| `movb` | 3 | 3 | 0 | 3 | 0 | 0 | 0 | 0 |
| `inc` | 4 | 24 | 14 | 2 | 0 | 0 | 8 | 0 |
| `cmova` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 0 |
| `cmovae` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 35 |
| `cmovb` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 80 |
| `cmovbe` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 502 |
| `cmove` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 287 |
| `cmovge` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 18 |
| `cmovl` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 12 |
| `cmovle` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 53 |
| `cmovne` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 400 |
| `cmovns` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 55 |
| `cmovs` | 6 | 6 | 4 | 2 | 0 | 0 | 0 | 2 |
| `imul` | 10 | 80 | 4 | 2 | 0 | 40 | 34 | 877 |
| `not` | 4 | 4 | 2 | 2 | 0 | 0 | 0 | 220 |
| `seta` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1407 |
| `setae` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1552 |
| `setb` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 499 |
| `setbe` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 314 |
| `sete` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1339 |
| `setg` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 872 |
| `setge` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 675 |
| `setl` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 984 |
| `setle` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 643 |
| `setne` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 10335 |
| `setnp` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 108 |
| `setns` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 176 |
| `seto` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 4 |
| `setp` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 2125 |
| `sets` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 264 |
| `cmp` | 19 | 114 | 95 | 0 | 0 | 0 | 19 | 8059 |
| `test` | 12 | 72 | 60 | 0 | 0 | 12 | 0 | 276 |
| `movq` | 6 | 6 | 6 | 0 | 0 | 0 | 0 | 452 |
| `bt` | 3 | 15 | 3 | 0 | 0 | 12 | 0 | 0 |
| `movd` | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 3073 |
| `andpd` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 6 |
| `andps` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 6 |
| `movapd` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 230 |
| `movaps` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 1922 |
| `movdqa` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 28 |
| `movsd` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 58 |
| `movss` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 1281 |
| `orpd` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 6 |
| `orps` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 6 |
| `pand` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 2 |
| `punpckldq` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 132 |
| `punpcklqdq` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 4 |
| `pxor` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 6 |
| `unpckhpd` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 132 |
| `xorpd` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| `xorps` | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 21 |
| `addsd` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 264 |
| `addss` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 317 |
| `cvtsi2sd` | 4 | 8 | 0 | 0 | 0 | 0 | 8 | 1720 |
| `cvtsi2ss` | 4 | 8 | 0 | 0 | 0 | 0 | 8 | 5872 |
| `cvtss2sd` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 4 |
| `div` | 4 | 38 | 0 | 0 | 0 | 24 | 14 | 1072 |
| `divsd` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 124 |
| `divss` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 295 |
| `idiv` | 4 | 38 | 0 | 0 | 0 | 24 | 14 | 1750 |
| `mul` | 4 | 38 | 0 | 0 | 0 | 16 | 22 | 320 |
| `mulsd` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 124 |
| `mulss` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 301 |
| `subpd` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 132 |
| `subsd` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 124 |
| `subss` | 2 | 4 | 0 | 0 | 0 | 0 | 4 | 295 |
| `ucomisd` | 2 | 12 | 0 | 0 | 0 | 0 | 12 | 1050 |
| `ucomiss` | 2 | 12 | 0 | 0 | 0 | 0 | 12 | 2612 |

Table 3 -- the disagreements, grouped by cause. Nothing here is decided: both readings are quoted and the ruling is the owner's.

| cause | places | operand shapes | mnemonics |
|---|---|---|---|
| the destination written at width 16 | 66 | `cl_gpr` `gpr_gpr` `gpr_mem` `gpr_one` `imm_gpr` `mem_gpr` | `adc` `add` `and` `cmova` `cmovae` `cmovb` `cmovbe` `cmove` `cmovge` `cmovl` `cmovle` `cmovne` `cmovns` `cmovs` `imul` `inc` `mov` `neg` `not` `or` `sar` `sbb` `shl` `shr` `sub` `xchg` `xor` |
| the flag SF | 64 | `gpr_gpr` `gpr_mem` `gpr_one` `imm_gpr` `mem_gpr` | `adc` `add` `neg` `sbb` `sub` |
| the flag PF | 61 | `gpr_gpr` `gpr_mem` `gpr_one` `imm_gpr` `mem_gpr` | `adc` `add` `neg` `sbb` |
| the flag ZF | 60 | `gpr_gpr` `gpr_mem` `imm_gpr` `mem_gpr` | `adc` `add` `sbb` `sub` |
| the destination written at width 8 | 50 | `cl_gpr` `gpr_gpr` `gpr_mem` `gpr_one` `imm_gpr` `mem_gpr` | `adc` `add` `and` `inc` `movb` `neg` `not` `or` `sar` `sbb` `seta` `setae` `setb` `setbe` `sete` `setg` `setge` `setl` `setle` `setne` `setnp` `setns` `seto` `setp` `sets` `shl` `shr` `sub` `xchg` `xor` |
| the flag CF | 41 | `gpr_gpr` `gpr_mem` `imm_gpr` `mem_gpr` | `adc` `sbb` `sub` |
| the flag OF | 41 | `gpr_gpr` `gpr_mem` `imm_gpr` `mem_gpr` | `adc` `sbb` `sub` |

### the destination written at width 16 -- 66 places

`adcw_r16_imm16` -- our line `adc $0x3,%di`, shape `imm_gpr` at width 16, the place `reg_rdi`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `Concat(0, 3 + Extract(15, 0, seed_rdi) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 0, 1))` | 0x4 |
| theirs | `Concat(Extract(63, 16, seed_rdi), Extract(15, 0, seed_rdi) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4))` | 0xffffffffffff0004 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0xffffffffffff0000`

`addw_r16_imm16` -- our line `add $0x3,%di`, shape `imm_gpr` at width 16, the place `reg_rdi`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `Concat(0, 3 + Extract(15, 0, seed_rdi))` | 0x3 |
| theirs | `Concat(Extract(63, 16, seed_rdi), 3 + Extract(15, 0, seed_rdi))` | 0xffffffffffff0003 |

the counterexample, LITERAL: `seed_rdi` = `0xffffffffffff0000`

`andw_r16_imm8` -- our line `and $0x3,%di`, shape `imm_gpr` at width 16, the place `reg_rdi`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `Concat(0, Extract(1, 0, seed_rdi))` | 0x0 |
| theirs | `Concat(Extract(63, 16, seed_rdi), 0, Extract(1, 0, seed_rdi))` | 0xffffffffffff0000 |

the counterexample, LITERAL: `seed_rdi` = `0xffffffffffff0000`

### the flag SF -- 64 places

`adcb_r8_imm8` -- our line `adc $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:SF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(0 <= 253 + Extract(7, 0, seed_rdi), 0, 1)` | 0x1 |
| theirs | `Extract(7, 7, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4))` | 0x0 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0x0`

`addb_m8_r8` -- our line `add %sil,(%rax)`, shape `gpr_mem` at width 8, the place `flags:SF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(0 <= Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi), 0, 1)` | 0x1 |
| theirs | `Extract(7, 7, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_)))` | 0x0 |

the counterexample, LITERAL: `seed_MEM__rax_` = `0x80`, `seed_rsi` = `0x88`

`negl_r32` -- our line `neg %edi`, shape `gpr_one` at width 32, the place `flags:SF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(0 <= Extract(31, 0, seed_rdi), 0, 1)` | 0x0 |
| theirs | `Extract(31, 31, 1 + ~Extract(31, 0, seed_rdi))` | 0x1 |

the counterexample, LITERAL: `seed_rdi` = `0x40000000`

### the flag PF -- 61 places

`adcb_r8_imm8` -- our line `adc $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:PF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If((Extract(1, 1, 253 + Extract(7, 0, seed_rdi)) == 1) == ((Extract(2, 2, 253 + Extract(7, 0, seed_rdi)) == 1) == ((Extract(3, 3, 253 + Extract(7, 0, seed_rdi)) == 1) == ((Extract(4, 4, 253 + Extract(7, 0, seed_rdi)) == 1) == ((Extract(5, 5, 253 + Extract(7, 0, seed_rdi)) == 1) == ((Extract(6, 6, 253 + Extract(7, 0, seed_rdi)) == 1) == ((Extract(7, 7, 253 + Extract(7, 0, seed_rdi)) == 1) == (Extract(0, 0, seed_rdi) == 0))))))), 1, 0)` | 0x1 |
| theirs | `If((((((((Extract(0, 0, seed_rdi) == 1 + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 1, 0)) == (Extract(1, 1, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 1)) == (Extract(2, 2, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 1)) == (Extract(3, 3, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 1)) == (Extract(4, 4, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 1)) == (Extract(5, 5, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 1)) == (Extract(6, 6, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 1)) == (Extract(7, 7, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 1), 1, 0)` | 0x0 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0xf3`

`addb_m8_r8` -- our line `add %sil,(%rax)`, shape `gpr_mem` at width 8, the place `flags:PF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If((Extract(1, 1, Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi)) == 1) == ((Extract(2, 2, Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi)) == 1) == ((Extract(3, 3, Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi)) == 1) == ((Extract(4, 4, Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi)) == 1) == ((Extract(5, 5, Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi)) == 1) == ((Extract(6, 6, Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi)) == 1) == ((Extract(7, 7, Extract(7, 0, seed_MEM__rax_) + 255*Extract(7, 0, seed_rsi)) == 1) == (Extract(0, 0, seed_rsi) == 1 + Extract(0, 0, seed_MEM__rax_)))))))), 1, 0)` | 0x1 |
| theirs | `If((((((((Extract(0, 0, seed_rsi) == 1 + Extract(0, 0, seed_MEM__rax_)) == (Extract(1, 1, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_))) == 1)) == (Extract(2, 2, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_))) == 1)) == (Extract(3, 3, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_))) == 1)) == (Extract(4, 4, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_))) == 1)) == (Extract(5, 5, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_))) == 1)) == (Extract(6, 6, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_))) == 1)) == (Extract(7, 7, Concat(0, Extract(7, 0, seed_rsi)) + Concat(0, Extract(7, 0, seed_MEM__rax_))) == 1), 1, 0)` | 0x0 |

the counterexample, LITERAL: `seed_MEM__rax_` = `0xc4`, `seed_rsi` = `0x40`

`negl_r32` -- our line `neg %edi`, shape `gpr_one` at width 32, the place `flags:PF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If((Extract(0, 0, seed_rdi) == 1) == ((Extract(1, 1, seed_rdi) == 1) == ((Extract(2, 2, seed_rdi) == 1) == ((Extract(3, 3, seed_rdi) == 1) == ((Extract(4, 4, seed_rdi) == 1) == ((Extract(5, 5, seed_rdi) == 1) == ((Extract(6, 6, seed_rdi) == 1) == (Extract(7, 7, seed_rdi) == 1))))))), 1, 0)` | 0x0 |
| theirs | `If((((((((~Extract(0, 0, seed_rdi) == 0) == (Extract(1, 1, 1 + ~Extract(31, 0, seed_rdi)) == 1)) == (Extract(2, 2, 1 + ~Extract(31, 0, seed_rdi)) == 1)) == (Extract(3, 3, 1 + ~Extract(31, 0, seed_rdi)) == 1)) == (Extract(4, 4, 1 + ~Extract(31, 0, seed_rdi)) == 1)) == (Extract(5, 5, 1 + ~Extract(31, 0, seed_rdi)) == 1)) == (Extract(6, 6, 1 + ~Extract(31, 0, seed_rdi)) == 1)) == (Extract(7, 7, 1 + ~Extract(31, 0, seed_rdi)) == 1), 1, 0)` | 0x1 |

the counterexample, LITERAL: `seed_rdi` = `0xfd`

### the flag ZF -- 60 places

`adcb_r8_imm8` -- our line `adc $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:ZF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(Extract(7, 0, seed_rdi) == 3, 1, 0)` | 0x0 |
| theirs | `If(Extract(7, 0, seed_rdi) == 255*If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4), 1, 0)` | 0x1 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0xfc`

`addb_m8_r8` -- our line `add %sil,(%rax)`, shape `gpr_mem` at width 8, the place `flags:ZF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(Extract(7, 0, seed_MEM__rax_) == Extract(7, 0, seed_rsi), 1, 0)` | 0x1 |
| theirs | `If(Extract(7, 0, seed_rsi) == 255*Extract(7, 0, seed_MEM__rax_), 1, 0)` | 0x0 |

the counterexample, LITERAL: `seed_MEM__rax_` = `0x8`, `seed_rsi` = `0x8`

`sbbb_r8_imm8` -- our line `sbb $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:ZF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(Extract(7, 0, seed_rdi) == 3, 1, 0)` | 0x1 |
| theirs | `If(Extract(7, 0, seed_rdi) == 255*If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 253, 252), 1, 0)` | 0x0 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0x3`

### the destination written at width 8 -- 50 places

`adcb_r8_imm8` -- our line `adc $0x3,%dil`, shape `imm_gpr` at width 8, the place `reg_rdi`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `Concat(0, 3 + Extract(7, 0, seed_rdi) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 0, 1))` | 0x4 |
| theirs | `Concat(Extract(63, 8, seed_rdi), Extract(7, 0, seed_rdi) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4))` | 0xffffffffffffff04 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0xffffffffffffff00`

`addb_r8_imm8` -- our line `add $0x3,%dil`, shape `imm_gpr` at width 8, the place `reg_rdi`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `Concat(0, 3 + Extract(7, 0, seed_rdi))` | 0x3 |
| theirs | `Concat(Extract(63, 8, seed_rdi), 3 + Extract(7, 0, seed_rdi))` | 0xffffffffffffff03 |

the counterexample, LITERAL: `seed_rdi` = `0xffffffffffffff00`

`andb_r8_imm8` -- our line `and $0x3,%dil`, shape `imm_gpr` at width 8, the place `reg_rdi`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `Concat(0, Extract(1, 0, seed_rdi))` | 0x0 |
| theirs | `Concat(Extract(63, 8, seed_rdi), 0, Extract(1, 0, seed_rdi))` | 0xffffffffffffff00 |

the counterexample, LITERAL: `seed_rdi` = `0xffffffffffffff00`

### the flag CF -- 41 places

`adcb_r8_imm8` -- our line `adc $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:CF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `Extract(8, 8, 3 + Concat(0, Extract(7, 0, seed_rdi)))` | 0x0 |
| theirs | `Extract(8, 8, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4))` | 0x1 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0xfc`

`sbbb_r8_imm8` -- our line `sbb $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:CF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(Or(Not(Extract(7, 2, seed_rdi) == 0), Extract(1, 0, seed_rdi) == 3), 0, 1)` | 0x0 |
| theirs | `~Extract(8, 8, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 253, 252))` | 0x1 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0x3`

`subl_m32_r32` -- our line `sub %esi,(%rax)`, shape `gpr_mem` at width 32, the place `flags:CF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(ULE(Extract(7, 0, seed_rsi), Extract(7, 0, seed_MEM__rax_)), 0, 1)` | 0x0 |
| theirs | `~Extract(32, 32, 1 + Concat(0, Extract(31, 0, seed_MEM__rax_)) + Concat(0, ~Extract(31, 0, seed_rsi)))` | 0x1 |

the counterexample, LITERAL: `seed_MEM__rax_` = `0x7ffffe`, `seed_rsi` = `0x800000`

### the flag OF -- 41 places

`adcb_r8_imm8` -- our line `adc $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:OF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(Extract(8, 8, 3 + Concat(Extract(7, 7, seed_rdi), Extract(7, 0, seed_rdi))) == Extract(7, 7, 3 + Concat(Extract(7, 7, seed_rdi), Extract(7, 0, seed_rdi))), 0, 1)` | 0x0 |
| theirs | `If(And(Extract(7, 7, seed_rdi) == 0, Not(Extract(7, 7, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 3, 4)) == 0)), 1, 0)` | 0x1 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0x7c`

`sbbb_r8_imm8` -- our line `sbb $0x3,%dil`, shape `imm_gpr` at width 8, the place `flags:OF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(Extract(8, 8, 509 + Concat(Extract(7, 7, seed_rdi), Extract(7, 0, seed_rdi))) == Extract(7, 7, 509 + Concat(Extract(7, 7, seed_rdi), Extract(7, 0, seed_rdi))), 0, 1)` | 0x0 |
| theirs | `If(And(Extract(7, 7, seed_rdi) == 1, Not(Extract(7, 7, Concat(0, Extract(7, 0, seed_rdi)) + If(ULE(Extract(31, 0, seed_r10), Extract(31, 0, seed_r11)), 253, 252)) == 1)), 1, 0)` | 0x1 |

the counterexample, LITERAL: `seed_r10` = `0x1`, `seed_r11` = `0x0`, `seed_rdi` = `0x83`

`subl_m32_r32` -- our line `sub %esi,(%rax)`, shape `gpr_mem` at width 32, the place `flags:OF`:

| reading | term, LITERAL (z3's printing of the simplified term, the register symbols keeping our reference's names) | its value at the counterexample |
|---|---|---|
| ours | `If(Extract(8, 8, Concat(Extract(7, 7, seed_MEM__rax_), Extract(7, 0, seed_MEM__rax_)) + 511*Concat(Extract(7, 7, seed_rsi), Extract(7, 0, seed_rsi))) == Extract(7, 7, Concat(Extract(7, 7, seed_MEM__rax_), Extract(7, 0, seed_MEM__rax_)) + 511*Concat(Extract(7, 7, seed_rsi), Extract(7, 0, seed_rsi))), 0, 1)` | 0x0 |
| theirs | `If(And(Extract(31, 31, seed_rsi) == ~Extract(31, 31, seed_MEM__rax_), Not(Extract(31, 31, seed_rsi) == ~Extract(31, 31, 1 + Concat(0, Extract(31, 0, seed_MEM__rax_)) + Concat(0, ~Extract(31, 0, seed_rsi))))), 1, 0)` | 0x1 |

the counterexample, LITERAL: `seed_MEM__rax_` = `0x50900fff`, `seed_rsi` = `0x90902010`

Table 4 -- the undefined regions, per mnemonic: the flags their reading writes Intel's undefined value into. `whole` is undefined on every input; `partial` is undefined on part of the input space, and the comparison was asked on the rest.

| mnem | undefined on every input | undefined on part |
|---|---|---|
| `and` | AF | -- |
| `bt` | AF OF PF SF | -- |
| `div` | AF CF OF PF SF ZF | -- |
| `idiv` | AF CF OF PF SF ZF | -- |
| `imul` | AF PF SF ZF | -- |
| `mul` | AF PF SF ZF | -- |
| `or` | AF | -- |
| `sar` | OF | OF |
| `shl` | OF | CF OF |
| `shr` | OF | CF OF |
| `test` | AF | -- |
| `xor` | AF | -- |

Table 5 -- the refusals, by cause.

| cause | places | mnemonics |
|---|---|---|
| our reference's builder leaves the flags untouched for this opcode, so it writes no flag | 138 | `imul` `mul` `sar` `shl` `shr` |
| our reference writes no route to the auxiliary carry: it holds the flags as (setter, left, right) and rebuilds a bit on demand, and neither carry_bit, overflow_bit nor predicate_of answers AF | 107 | `adc` `add` `cmp` `inc` `neg` `sbb` `sub` `ucomisd` `ucomiss` |
| our reference writes this place and their rule states nothing at it | 92 | `adc` `add` `addsd` `addss` `and` `cvtsi2sd` `cvtsi2ss` `cvtss2sd` `div` `divsd` |
| the rule reads a flag the comparison did not bind: getFlag('AF') -- this variant's mapping is a function of the flags a previous instruction left | 24 | `sar` `shl` `shr` |
| this opcode reads the carry bit and the flag-setting arch opcode 'imul' has no carry model in this file | 6 | `imul` |
| this opcode reads the signed-overflow bit and the flag-setting arch opcode 'imul' has no overflow model in this file | 6 | `imul` |
| a function this grammar does not know: the rule applies comisd/2 | 6 | `ucomisd` |
| a function this grammar does not know: the rule applies comiss/2 | 6 | `ucomiss` |
| this opcode reads the signed-overflow bit and the flag-setting arch opcode 'inc' has no overflow model in this file | 4 | `inc` |
| a function this grammar does not know: the rule applies sub_double/2 | 4 | `subpd` `subsd` |
| condition 'CondSGN' has no float-flag reading written for it | 4 | `ucomisd` `ucomiss` |
| our reference's route to this flag stopped on its own flag triple: AttributeError: 'FPRef' object has no attribute 'size' | 4 | `ucomisd` `ucomiss` |
| a function this grammar does not know: the rule applies add_double/2 | 2 | `addsd` |
| a function this grammar does not know: the rule applies add_single/2 | 2 | `addss` |
| a function this grammar does not know: the rule applies cvt_int32_to_double/1 | 2 | `cvtsi2sd` |
| a function this grammar does not know: the rule applies cvt_int64_to_double/1 | 2 | `cvtsi2sd` |
| a function this grammar does not know: the rule applies cvt_int32_to_single/1 | 2 | `cvtsi2ss` |
| a function this grammar does not know: the rule applies cvt_int64_to_single/1 | 2 | `cvtsi2ss` |
| a function this grammar does not know: the rule applies cvt_single_to_double/1 | 2 | `cvtss2sd` |
| a function this grammar does not know: the rule applies div_double/2 | 2 | `divsd` |
| a function this grammar does not know: the rule applies div_single/2 | 2 | `divss` |
| a function this grammar does not know: the rule applies mul_double/2 | 2 | `mulsd` |
| a function this grammar does not know: the rule applies mul_single/2 | 2 | `mulss` |
| a function this grammar does not know: the rule applies sub_single/2 | 2 | `subss` |
| a function this grammar does not know: the rule applies div_remainder_int8/2 | 1 | `div` |
| a function this grammar does not know: the rule applies div_quotient_int32/2 | 1 | `div` |
| a function this grammar does not know: the rule applies div_remainder_int32/2 | 1 | `div` |
| a function this grammar does not know: the rule applies div_quotient_int64/2 | 1 | `div` |
| a function this grammar does not know: the rule applies div_remainder_int64/2 | 1 | `div` |
| a function this grammar does not know: the rule applies div_quotient_int16/2 | 1 | `div` |
| a function this grammar does not know: the rule applies div_remainder_int16/2 | 1 | `div` |
| a function this grammar does not know: the rule applies idiv_remainder_int8/2 | 1 | `idiv` |
| a function this grammar does not know: the rule applies idiv_quotient_int64/2 | 1 | `idiv` |
| a function this grammar does not know: the rule applies idiv_remainder_int64/2 | 1 | `idiv` |
| a function this grammar does not know: the rule applies idiv_quotient_int32/2 | 1 | `idiv` |
| a function this grammar does not know: the rule applies idiv_remainder_int32/2 | 1 | `idiv` |
| a function this grammar does not know: the rule applies idiv_quotient_int16/2 | 1 | `idiv` |
| a function this grammar does not know: the rule applies idiv_remainder_int16/2 | 1 | `idiv` |

Wall clock 5.0 s; peak resident memory 66.0 MB against the stated 6144 MB ceiling and the named abort `ABORT_MEMORY_REF1`.
