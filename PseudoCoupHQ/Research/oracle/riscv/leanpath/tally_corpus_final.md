# tally of the corpus: per language, per arch-opcode, per arch-unit, with totals

Computed from `walk_corpus_{0,1,2,3,fix2}/walk.json`, `equals_corpus_j_*/equals.json` and `equals_corpus_survivors3_*/equals.json` by `tally_corpus_final.py` beside this file; the tower's `tally_corpus_final.json` gives the same totals.

## per language (one arch-unit compiled from each of the 490 rendered sources per language; the same 255 cells for every language, log 279)

| language | rendered sources | proof 1 certified | proof 2 matched | same text | integer level | bit level | identity (bare return) | own opcode not a candidate (immediate) | composite, all candidates refuted | open | refused |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | 490 | 336 | 28 | 22 | 1 | 5 | 99 | 66 | 143 | 0 | 154 |
| cpp | 490 | 336 | 28 | 22 | 1 | 5 | 99 | 66 | 143 | 0 | 154 |
| rust | 490 | 355 | 28 | 21 | 2 | 5 | 99 | 54 | 164 | 10 | 135 |
| go | 490 | 182 | 30 | 11 | 0 | 19 | 66 | 18 | 68 | 0 | 308 |
| all | 1960 | 1209 | 114 | 76 | 4 | 34 | 363 | 204 | 518 | 10 | 751 |

## per language and route

| language | route | units | certified | matched | refused |
|---|---|---|---|---|---|
| c | native_first | 255 | 167 | 20 | 88 |
| c | all_constructed | 235 | 169 | 8 | 66 |
| cpp | native_first | 255 | 167 | 20 | 88 |
| cpp | all_constructed | 235 | 169 | 8 | 66 |
| rust | native_first | 255 | 170 | 20 | 85 |
| rust | all_constructed | 235 | 185 | 8 | 50 |
| go | native_first | 255 | 95 | 22 | 160 |
| go | all_constructed | 235 | 87 | 8 | 148 |

## per arch-opcode (the Sail clauses)

Sail clauses in the emit: 339. Certified by strip, so usable as definitions: 93 (42 straight, 51 aliases). Refused: 243. Failed: 3.

### matched as the meaning of a unit (proof 2), per language

| Sail clause | c | cpp | rust | go | total |
|---|---|---|---|---|---|
| RTYPE | 24 | 24 | 24 | 13 | 85 |
| ZBB_EXTOP | 0 | 0 | 0 | 16 | 16 |
| MUL | 2 | 2 | 2 | 1 | 7 |
| RTYPEW | 2 | 2 | 2 | 0 | 6 |
| total | 28 | 28 | 28 | 30 | 114 |

### present in a certified unit's expression (proof 1), per language (units containing the clause)

| Sail clause | enumerable params | c | cpp | rust | go | total |
|---|---|---|---|---|---|---|
| RTYPE | yes | 141 | 141 | 180 | 64 | 526 |
| ITYPE | no (immediate) | 135 | 135 | 154 | 72 | 496 |
| SHIFTIOP | no (immediate) | 108 | 108 | 141 | 65 | 422 |
| ZBA_RTYPEUW | no (immediate) | 54 | 54 | 0 | 0 | 108 |
| ZBA_RTYPE | no (immediate) | 31 | 31 | 0 | 0 | 62 |
| SHIFTIWOP | no (immediate) | 18 | 18 | 19 | 0 | 55 |
| ADDIW | no (immediate) | 16 | 16 | 16 | 0 | 48 |
| ZBB_RTYPE | yes | 13 | 13 | 0 | 0 | 26 |
| MUL | yes | 4 | 4 | 4 | 2 | 14 |
| ZBS_IOP | no (immediate) | 5 | 5 | 0 | 0 | 10 |
| RTYPEW | yes | 3 | 3 | 4 | 0 | 10 |
| REM | yes | 1 | 1 | 2 | 0 | 4 |
| DIV | yes | 1 | 1 | 1 | 0 | 3 |
| total (clause-unit pairs) | | 530 | 530 | 521 | 203 | 1784 |

### all 42 straight clauses certified by strip

| Sail clause | enumerable params | in a unit's expression | matched as a meaning |
|---|---|---|---|
| ADDIW | no (immediate) | 48 | 0 |
| BREV8 | yes | 0 | 0 |
| CLMUL | yes | 0 | 0 |
| CLMULH | yes | 0 | 0 |
| CLMULR | yes | 0 | 0 |
| CLZ | yes | 0 | 0 |
| CLZW | yes | 0 | 0 |
| CTZ | yes | 0 | 0 |
| CTZW | yes | 0 | 0 |
| C_NOT | no (immediate) | 0 | 0 |
| C_ZEXT_B | no (immediate) | 0 | 0 |
| DIV | yes | 3 | 0 |
| DIVW | yes | 0 | 0 |
| ITYPE | no (immediate) | 496 | 0 |
| MUL | yes | 14 | 7 |
| MULW | yes | 0 | 0 |
| REM | yes | 4 | 0 |
| REMW | yes | 0 | 0 |
| REV8 | yes | 0 | 0 |
| RORI | no (immediate) | 0 | 0 |
| RORIW | no (immediate) | 0 | 0 |
| RTYPE | yes | 526 | 85 |
| RTYPEW | yes | 10 | 6 |
| SHA512SIG0H | yes | 0 | 0 |
| SHA512SIG0L | yes | 0 | 0 |
| SHA512SIG1H | yes | 0 | 0 |
| SHA512SIG1L | yes | 0 | 0 |
| SHA512SUM0R | yes | 0 | 0 |
| SHA512SUM1R | yes | 0 | 0 |
| SHIFTIOP | no (immediate) | 422 | 0 |
| SHIFTIWOP | no (immediate) | 55 | 0 |
| SLLIUW | no (immediate) | 0 | 0 |
| ZBA_RTYPE | no (immediate) | 62 | 0 |
| ZBA_RTYPEUW | no (immediate) | 108 | 0 |
| ZBB_EXTOP | yes | 0 | 16 |
| ZBB_RTYPE | yes | 26 | 0 |
| ZBB_RTYPEW | yes | 0 | 0 |
| ZBKB_RTYPE | yes | 0 | 0 |
| ZBS_IOP | no (immediate) | 10 | 0 |
| ZBS_RTYPE | yes | 0 | 0 |
| ZIMOP_MOP_R | no (immediate) | 0 | 0 |
| ZIMOP_MOP_RR | no (immediate) | 0 | 0 |
| total | | 13 clauses used | 4 clauses matched |

## per arch-unit (all 1960)

| unit | language | route | proof 1 | instructions | classification | opcode | stage |
|---|---|---|---|---|---|---|---|
| add_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | matched | RTYPE | fixed_width |
| add_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| add_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | matched | RTYPE | fixed_width |
| add_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| add_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| add_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| add_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | matched | RTYPE | fixed_width |
| add_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| add_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| add_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| add_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| add_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| add_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| add_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| add_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| add_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| addi_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| addi_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| addi_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| addi_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| addi_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| addi_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| addi_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| addi_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 170 instructions, above the walk's bound |  | refused |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 68 instructions, above the walk's bound  |  | refused |  |  |
| addiw_gpr_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 170 instructions, above the walk's bound |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 68 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 44 | composite, every candidate refuted |  |  |
| addw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 44 | composite, every candidate refuted |  |  |
| addw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 144 instructions, above the walk's bound |  | refused |  |  |
| addw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| addw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 41 | composite, every candidate refuted |  |  |
| addw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| and_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| and_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| and_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| and_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| and_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| and_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| and_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| and_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| and_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| and_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| and_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| and_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| and_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| and_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| and_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| and_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| andi_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| andi_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| andi_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| andi_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| andi_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| andi_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| andi_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| andi_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| auipc_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| auipc_gpr_imm_32__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| auipc_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| auipc_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| auipc_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| auipc_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| auipc_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| auipc_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| beq_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| beq_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_imm_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_imm_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_imm_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_imm_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_imm_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_imm_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| beq_gpr_gpr_imm_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_imm_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_same_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_same_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_same_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_same_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_same_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_same_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| beq_gpr_gpr_same_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 15 | composite, every candidate refuted |  |  |
| beq_gpr_gpr_same_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bge_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bge_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 38 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 38 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_imm_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_imm_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_imm_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_imm_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_imm_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bge_gpr_gpr_imm_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bge_gpr_gpr_imm_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 38 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_imm_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_same_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_same_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_same_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 36 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_same_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_same_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bge_gpr_gpr_same_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bge_gpr_gpr_same_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 38 | composite, every candidate refuted |  |  |
| bge_gpr_gpr_same_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 37 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bgeu_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 34 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 37 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 34 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 37 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 34 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_imm_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 33 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__go__all_constructed | go | all_constructed | CERTIFIED | 37 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 34 | composite, every candidate refuted |  |  |
| bgeu_gpr_gpr_same_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| blt_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| blt_gpr_gpr_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 39 | open (survived evaluation) |  |  |
| blt_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| blt_gpr_gpr_gpr_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 39 | open (survived evaluation) |  |  |
| blt_gpr_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_imm_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_imm_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_imm_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_imm_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_imm_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| blt_gpr_gpr_imm_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_imm_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 39 | open (survived evaluation) |  |  |
| blt_gpr_gpr_imm_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_same_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_same_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_same_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| blt_gpr_gpr_same_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_same_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| blt_gpr_gpr_same_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| blt_gpr_gpr_same_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 39 | open (survived evaluation) |  |  |
| blt_gpr_gpr_same_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bltu_gpr_gpr_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 35 | open (survived evaluation) |  |  |
| bltu_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bltu_gpr_gpr_gpr_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 35 | open (survived evaluation) |  |  |
| bltu_gpr_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_imm_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_imm_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_imm_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_imm_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_imm_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bltu_gpr_gpr_imm_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_imm_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 35 | open (survived evaluation) |  |  |
| bltu_gpr_gpr_imm_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_same_64__branch_condition__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_same_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_same_64__branch_condition__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| bltu_gpr_gpr_same_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_same_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bltu_gpr_gpr_same_64__branch_condition__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bltu_gpr_gpr_same_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 35 | open (survived evaluation) |  |  |
| bltu_gpr_gpr_same_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| bne_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bne_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bne_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_gpr_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_imm_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_imm_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_imm_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_imm_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_imm_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bne_gpr_gpr_imm_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bne_gpr_gpr_imm_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_imm_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_same_64__branch_condition__c__all_constructed | c | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_same_64__branch_condition__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_same_64__branch_condition__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_same_64__branch_condition__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_same_64__branch_condition__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| bne_gpr_gpr_same_64__branch_condition__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| bne_gpr_gpr_same_64__branch_condition__rust__all_constructed | rust | all_constructed | CERTIFIED | 14 | composite, every candidate refuted |  |  |
| bne_gpr_gpr_same_64__branch_condition__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 17 | composite, every candidate refuted |  |  |
| czero_eqz_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 17 | composite, every candidate refuted |  |  |
| czero_eqz_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 17 | composite, every candidate refuted |  |  |
| czero_nez_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 17 | composite, every candidate refuted |  |  |
| czero_nez_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| div_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6428 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| div_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6428 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| div_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 9109 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| div_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5562 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for BTYPE (an ele |  | refused |  |  |
| div_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6345 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| div_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6345 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| div_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 9021 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| div_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5485 instructions, above the walk's boun |  | refused |  |  |
| div_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6270 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6270 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 8927 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5406 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| divu_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6266 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| divu_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6266 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| divu_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 8925 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| divu_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5407 instructions, above the walk's boun |  | refused |  |  |
| divu_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1459 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1459 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 1998 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 89 instructions, above the walk's bound  |  | refused |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1612 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| divuw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1463 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| divuw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1463 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| divuw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 1997 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 86 instructions, above the walk's bound  |  | refused |  |  |
| divuw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1615 instructions, above the walk's boun |  | refused |  |  |
| divuw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1610 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 87 instructions, above the walk's bound  |  | refused |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1610 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 87 instructions, above the walk's bound  |  | refused |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 2159 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 115 instructions, above the walk's bound |  | refused |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1753 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| divw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1543 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| divw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1543 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| divw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 2082 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 109 instructions, above the walk's bound |  | refused |  |  |
| divw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1690 instructions, above the walk's boun |  | refused |  |  |
| divw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| fadd_d_fpr_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fadd_d_fpr_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fadd_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fadd_s_fpr_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fadd_s_fpr_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fadd_s_fpr_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fadd_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_l_fpr_gpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_l_fpr_gpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_l_fpr_gpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_l_fpr_gpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_lu_fpr_gpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_lu_fpr_gpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_lu_fpr_gpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for BTYPE (an ele |  | refused |  |  |
| fcvt_d_lu_fpr_gpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_s_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_s_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_s_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fcvt_d_s_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_s_fpr_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_s_fpr_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_s_fpr_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fcvt_d_s_fpr_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_w_fpr_gpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_w_fpr_gpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_w_fpr_gpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_w_fpr_gpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_wu_fpr_gpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_wu_fpr_gpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_wu_fpr_gpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_d_wu_fpr_gpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_d_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_d_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_d_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fcvt_s_d_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_d_fpr_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_d_fpr_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_d_fpr_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fcvt_s_d_fpr_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_l_fpr_gpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_l_fpr_gpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_l_fpr_gpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_l_fpr_gpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_lu_fpr_gpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_lu_fpr_gpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_lu_fpr_gpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for BTYPE (an ele |  | refused |  |  |
| fcvt_s_lu_fpr_gpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_w_fpr_gpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_w_fpr_gpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_w_fpr_gpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_w_fpr_gpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_wu_fpr_gpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_wu_fpr_gpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_wu_fpr_gpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fcvt_s_wu_fpr_gpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fdiv_d_fpr_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fdiv_d_fpr_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fdiv_d_fpr_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fdiv_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fdiv_s_fpr_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fdiv_s_fpr_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fdiv_s_fpr_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fdiv_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 90 instructions, above the walk's bound  |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 90 instructions, above the walk's bound  |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 115 instructions, above the walk's bound |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 91 instructions, above the walk's bound  |  | refused |  |  |
| feq_d_gpr_fpr_fpr_64__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 143 instructions, above the walk's bound |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 73 instructions, above the walk's bound  |  | refused |  |  |
| feq_s_gpr_fpr_fpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fld_fpr_fpr_64__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_64__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_64__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_64__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_gpr_64__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fld_fpr_mem_64__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 147 instructions, above the walk's bound |  | refused |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 147 instructions, above the walk's bound |  | refused |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 166 instructions, above the walk's bound |  | refused |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 141 instructions, above the walk's bound |  | refused |  |  |
| fle_d_gpr_fpr_fpr_64__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 188 instructions, above the walk's bound |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 119 instructions, above the walk's bound |  | refused |  |  |
| fle_s_gpr_fpr_fpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 130 instructions, above the walk's bound |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 130 instructions, above the walk's bound |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 149 instructions, above the walk's bound |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 121 instructions, above the walk's bound |  | refused |  |  |
| flt_d_gpr_fpr_fpr_64__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 112 instructions, above the walk's bound |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 112 instructions, above the walk's bound |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 175 instructions, above the walk's bound |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 107 instructions, above the walk's bound |  | refused |  |  |
| flt_s_gpr_fpr_fpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| flw_fpr_fpr_32__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_32__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_32__freg_fa0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_fpr_32__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_gpr_32__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_gpr_32__freg_fa0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_gpr_32__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_gpr_32__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_gpr_32__freg_fa0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_gpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_gpr_32__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_gpr_32__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_mem_32__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_mem_32__freg_fa0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_mem_32__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_mem_32__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_mem_32__freg_fa0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_mem_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| flw_fpr_mem_32__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| flw_fpr_mem_32__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fmul_d_fpr_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fmul_d_fpr_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fmul_d_fpr_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fmul_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fmul_s_fpr_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fmul_s_fpr_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fmul_s_fpr_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fmul_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_d_x_fpr_gpr_64__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__rust__all_constructed | rust | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fmv_w_x_fpr_gpr_32__freg_fa0__rust__native_first | rust | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fmv_x_d_gpr_fpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| fmv_x_w_gpr_fpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| fmv_x_w_gpr_fpr_fpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_64__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_fpr_fpr_64__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_gpr_64__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| fsd_fpr_mem_64__mem_MEM_0x0_a1___rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| fsub_d_fpr_fpr_fpr_64__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fsub_d_fpr_fpr_fpr_64__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fsub_d_fpr_fpr_fpr_64__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fsub_d_fpr_fpr_fpr_64__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fsub_s_fpr_fpr_fpr_32__freg_fa0__c__native_first | c | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fsub_s_fpr_fpr_fpr_32__freg_fa0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fsub_s_fpr_fpr_fpr_32__freg_fa0__go__native_first | go | native_first | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| fsub_s_fpr_fpr_fpr_32__freg_fa0__rust__native_first | rust | native_first | REFUSED: no certified pure form for ILLEGAL (a pu |  | refused |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_32__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| fsw_fpr_fpr_fpr_32__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| fsw_fpr_gpr_32__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| fsw_fpr_mem_32__mem_MEM_0x0_a1___rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| jal_gpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_fpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_fpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_mem_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_mem_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_mem_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_mem_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jal_gpr_mem_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_mem_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jal_gpr_mem_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jal_gpr_mem_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_fpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_fpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_mem_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_mem_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_mem_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_mem_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| jalr_gpr_mem_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_mem_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| jalr_gpr_mem_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| jalr_gpr_mem_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lb_gpr_fpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_fpr_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_fpr_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_fpr_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_fpr_fpr_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_gpr_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_imm_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_imm_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_imm_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_imm_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_imm_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_imm_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_imm_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_imm_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_same_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_same_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_same_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_same_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_same_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_same_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_gpr_same_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_gpr_same_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_imm_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_imm_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_imm_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_imm_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_imm_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_imm_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_imm_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_imm_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_mem_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_mem_8__reg_a0__c__native_first | c | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_mem_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 31 | composite, every candidate refuted |  |  |
| lb_gpr_mem_8__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_mem_8__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 263 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_mem_8__reg_a0__go__native_first | go | native_first | REFUSED: 177 instructions, above the walk's bound |  | refused |  |  |
| lb_gpr_mem_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 32 | composite, every candidate refuted |  |  |
| lb_gpr_mem_8__reg_a0__rust__native_first | rust | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| lbu_gpr_fpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_fpr_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_fpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_fpr_fpr_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_gpr_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_imm_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_same_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_same_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_same_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_same_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_same_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_same_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_gpr_same_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_gpr_same_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_imm_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_imm_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_imm_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_imm_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_imm_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_imm_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_imm_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_imm_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_mem_8__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_mem_8__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_mem_8__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_mem_8__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_mem_8__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_mem_8__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lbu_gpr_mem_8__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lbu_gpr_mem_8__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_fpr_fpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| ld_gpr_mem_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lh_gpr_fpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_fpr_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_fpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_fpr_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_fpr_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_fpr_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_fpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_fpr_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_fpr_fpr_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_gpr_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_imm_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_imm_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_imm_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_imm_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_imm_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_imm_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_imm_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_imm_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_same_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_same_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_same_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_same_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_gpr_same_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_same_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_gpr_same_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_gpr_same_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_imm_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_imm_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_imm_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_imm_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_imm_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_imm_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_imm_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_imm_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_mem_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_mem_16__reg_a0__c__native_first | c | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_mem_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 23 | composite, every candidate refuted |  |  |
| lh_gpr_mem_16__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lh_gpr_mem_16__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 222 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_mem_16__reg_a0__go__native_first | go | native_first | REFUSED: 145 instructions, above the walk's bound |  | refused |  |  |
| lh_gpr_mem_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 24 | composite, every candidate refuted |  |  |
| lh_gpr_mem_16__reg_a0__rust__native_first | rust | native_first | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| lhu_gpr_fpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_fpr_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_fpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_fpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_fpr_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_fpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_fpr_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_fpr_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_fpr_fpr_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_fpr_fpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_fpr_fpr_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_gpr_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_gpr_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_gpr_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_gpr_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_gpr_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_gpr_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_gpr_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_gpr_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_imm_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_imm_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_imm_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_imm_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_imm_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_imm_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_imm_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_imm_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_same_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_same_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_same_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_same_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_same_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_same_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_gpr_same_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_gpr_same_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_imm_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_imm_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_imm_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_imm_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_imm_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_imm_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_imm_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_imm_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_mem_16__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_mem_16__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_mem_16__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_mem_16__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_mem_16__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_mem_16__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | matched | ZBB_EXTOP | fixed_width |
| lhu_gpr_mem_16__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| lhu_gpr_mem_16__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| lui_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lui_gpr_imm_32__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lui_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lui_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lui_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lui_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lui_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lui_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| lw_gpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_fpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_fpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_fpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_fpr_fpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_imm_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_imm_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_mem_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_mem_32__reg_a0__c__native_first | c | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_mem_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 43 | composite, every candidate refuted |  |  |
| lw_gpr_mem_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 66 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_mem_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 140 instructions, above the walk's bound |  | refused |  |  |
| lw_gpr_mem_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| lw_gpr_mem_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 40 | composite, every candidate refuted |  |  |
| lw_gpr_mem_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| lwu_gpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_fpr_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_fpr_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_fpr_fpr_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_imm_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_imm_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_mem_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_mem_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_mem_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_mem_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| lwu_gpr_mem_32__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_mem_32__reg_a0__go__native_first | go | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_mem_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| lwu_gpr_mem_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| mul_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 2255 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | MUL | same_text |
| mul_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 2255 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | MUL | same_text |
| mul_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 2626 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | matched | MUL | same_text |
| mul_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 2323 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | MUL | integer_level |
| mul_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 2257 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| mul_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 2257 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| mul_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 2626 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| mul_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 2256 instructions, above the walk's boun |  | refused |  |  |
| mul_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 10283 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | REFUSED: 274 instructions, above the walk's bound |  | refused |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 10283 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 274 instructions, above the walk's bound |  | refused |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 18837 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: 18837 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 11270 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | REFUSED: 274 instructions, above the walk's bound |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 9855 instructions, above the walk's boun |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | REFUSED: 126 instructions, above the walk's bound |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 9855 instructions, above the walk's boun |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 126 instructions, above the walk's bound |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 18878 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: 18878 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 10655 instructions, above the walk's bou |  | refused |  |  |
| mulh_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | REFUSED: 126 instructions, above the walk's bound |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 7807 instructions, above the walk's boun |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 7807 instructions, above the walk's boun |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 14534 instructions, above the walk's bou |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: 14534 instructions, above the walk's bou |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 8296 instructions, above the walk's boun |  | refused |  |  |
| mulhsu_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 7780 instructions, above the walk's boun |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 7780 instructions, above the walk's boun |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 14834 instructions, above the walk's bou |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: 14834 instructions, above the walk's bou |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 8237 instructions, above the walk's boun |  | refused |  |  |
| mulhsu_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | REFUSED: 125 instructions, above the walk's bound |  | refused |  |  |
| mulhu_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 7086 instructions, above the walk's boun |  | refused |  |  |
| mulhu_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | MUL | integer_level |
| mulhu_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 7086 instructions, above the walk's boun |  | refused |  |  |
| mulhu_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | MUL | integer_level |
| mulhu_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 14083 instructions, above the walk's bou |  | refused |  |  |
| mulhu_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: 14083 instructions, above the walk's bou |  | refused |  |  |
| mulhu_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 7681 instructions, above the walk's boun |  | refused |  |  |
| mulhu_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | MUL | integer_level |
| mulhu_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 7087 instructions, above the walk's boun |  | refused |  |  |
| mulhu_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| mulhu_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 7087 instructions, above the walk's boun |  | refused |  |  |
| mulhu_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| mulhu_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 14392 instructions, above the walk's bou |  | refused |  |  |
| mulhu_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: 14392 instructions, above the walk's bou |  | refused |  |  |
| mulhu_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 7607 instructions, above the walk's boun |  | refused |  |  |
| mulhu_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 971 instructions, above the walk's bound |  | refused |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 971 instructions, above the walk's bound |  | refused |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 1264 instructions, above the walk's boun |  | refused |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1002 instructions, above the walk's boun |  | refused |  |  |
| mulw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 971 instructions, above the walk's bound |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 971 instructions, above the walk's bound |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 1264 instructions, above the walk's boun |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 967 instructions, above the walk's bound |  | refused |  |  |
| mulw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| or_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| or_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| or_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| or_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| or_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| or_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| or_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| or_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| or_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| or_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| or_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| or_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| or_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| or_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| or_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| or_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| ori_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| ori_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| ori_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| ori_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| ori_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| ori_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| ori_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| ori_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6167 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6167 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 8784 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5411 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 9 | composite, every candidate refuted |  |  |
| rem_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6127 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| rem_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6127 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| rem_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 8738 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| rem_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5371 instructions, above the walk's boun |  | refused |  |  |
| rem_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6014 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6014 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 8597 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5259 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| remu_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 6014 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remu_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 6014 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remu_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 8595 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for LOAD (an elem |  | refused |  |  |
| remu_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 5258 instructions, above the walk's boun |  | refused |  |  |
| remu_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1401 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1401 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 1894 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 89 instructions, above the walk's bound  |  | refused |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1528 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| remuw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1405 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remuw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1405 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remuw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 1890 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 86 instructions, above the walk's bound  |  | refused |  |  |
| remuw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1527 instructions, above the walk's boun |  | refused |  |  |
| remuw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1545 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 82 instructions, above the walk's bound  |  | refused |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1545 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 82 instructions, above the walk's bound  |  | refused |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 2041 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 110 instructions, above the walk's bound |  | refused |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1661 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| remw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 1512 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 1512 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| remw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 2005 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 105 instructions, above the walk's bound |  | refused |  |  |
| remw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 1626 instructions, above the walk's boun |  | refused |  |  |
| remw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_8__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_fpr_fpr_8__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_8__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_gpr_8__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_imm_8__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_gpr_same_8__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_imm_8__mem_MEM_0x3__rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___c__all_constructed | c | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___c__native_first | c | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___cpp__all_constructed | cpp | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___cpp__native_first | cpp | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___go__all_constructed | go | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___go__native_first | go | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___rust__all_constructed | rust | all_constructed | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sb_gpr_mem_8__mem_MEM_0x0_a1___rust__native_first | rust | native_first | CERTIFIED | 2 | composite, every candidate refuted |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_64__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_fpr_fpr_64__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_64__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_gpr_64__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_imm_64__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_gpr_same_64__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_imm_64__mem_MEM_0x3__rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___c__all_constructed | c | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___c__native_first | c | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___cpp__all_constructed | cpp | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___cpp__native_first | cpp | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___go__all_constructed | go | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___go__native_first | go | native_first | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___rust__all_constructed | rust | all_constructed | CERTIFIED | 0 | identity |  |  |
| sd_gpr_mem_64__mem_MEM_0x0_a1___rust__native_first | rust | native_first | CERTIFIED | 0 | identity |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_16__mem_MEM_fa1__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_fpr_fpr_16__mem_MEM_fa1__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_16__mem_MEM_a1__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_gpr_16__mem_MEM_a1__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_imm_16__mem_MEM_a1__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_gpr_same_16__mem_MEM_a1__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_imm_16__mem_MEM_0x3__rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___c__all_constructed | c | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___c__native_first | c | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___cpp__native_first | cpp | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sh_gpr_mem_16__mem_MEM_0x0_a1___rust__native_first | rust | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| sll_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 12 | matched | RTYPE | fixed_width |
| sll_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sll_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 12 | matched | RTYPE | fixed_width |
| sll_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sll_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 106 instructions, above the walk's bound |  | refused |  |  |
| sll_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 3 | matched | RTYPE | fixed_width |
| sll_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 12 | matched | RTYPE | fixed_width |
| sll_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sll_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 12 | composite, every candidate refuted |  |  |
| sll_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| sll_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 12 | composite, every candidate refuted |  |  |
| sll_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| sll_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 107 instructions, above the walk's bound |  | refused |  |  |
| sll_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| sll_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 12 | composite, every candidate refuted |  |  |
| sll_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| slli_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slli_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slli_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slli_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slli_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| slli_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| slli_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slli_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__c__native_first | c | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 148 instructions, above the walk's bound |  | refused |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slliw_gpr_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 53 | matched | RTYPEW | fixed_width |
| sllw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 53 | matched | RTYPEW | fixed_width |
| sllw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 230 instructions, above the walk's bound |  | refused |  |  |
| sllw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 74 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 50 | matched | RTYPEW | fixed_width |
| sllw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 53 | composite, every candidate refuted |  |  |
| sllw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 53 | composite, every candidate refuted |  |  |
| sllw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 227 instructions, above the walk's bound |  | refused |  |  |
| sllw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| sllw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 50 | composite, every candidate refuted |  |  |
| sllw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| slt_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| slt_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| slt_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| slt_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| slt_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| slt_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| slt_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 39 | open (survived evaluation) |  |  |
| slt_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| slt_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slt_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slt_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slt_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slt_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| slt_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| slt_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slt_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slti_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| slti_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slti_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| slti_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| slti_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| slti_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| slti_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 34 | composite, every candidate refuted |  |  |
| slti_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 20 | composite, every candidate refuted |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 20 | composite, every candidate refuted |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for BTYPE (an ele |  | refused |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 10 | composite, every candidate refuted |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 21 | composite, every candidate refuted |  |  |
| sltiu_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltu_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| sltu_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sltu_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: register of read r not resolved |  | refused |  |  |
| sltu_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sltu_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for C_NOP (a pure |  | refused |  |  |
| sltu_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sltu_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 35 | open (survived evaluation) |  |  |
| sltu_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sltu_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltu_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltu_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltu_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltu_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| sltu_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| sltu_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sltu_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sra_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| sra_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sra_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| sra_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sra_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 155 instructions, above the walk's bound |  | refused |  |  |
| sra_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 3 | matched | RTYPE | fixed_width |
| sra_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for BTYPE (an ele |  | refused |  |  |
| sra_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sra_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| sra_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| sra_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| sra_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| sra_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 153 instructions, above the walk's bound |  | refused |  |  |
| sra_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| sra_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: no certified pure form for BTYPE (an ele |  | refused |  |  |
| sra_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| srai_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 8 | composite, every candidate refuted |  |  |
| srai_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srai_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 8 | composite, every candidate refuted |  |  |
| srai_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srai_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for BTYPE (an ele |  | refused |  |  |
| srai_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| srai_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 8 | composite, every candidate refuted |  |  |
| srai_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 50 | composite, every candidate refuted |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__c__native_first | c | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 50 | composite, every candidate refuted |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 161 instructions, above the walk's bound |  | refused |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 45 | composite, every candidate refuted |  |  |
| sraiw_gpr_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 70 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 89 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 89 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 268 instructions, above the walk's bound |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 74 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 85 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 88 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 69 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 268 instructions, above the walk's bound |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 84 instructions, above the walk's bound  |  | refused |  |  |
| sraw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| srl_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 12 | matched | RTYPE | fixed_width |
| srl_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| srl_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 12 | matched | RTYPE | fixed_width |
| srl_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| srl_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 106 instructions, above the walk's bound |  | refused |  |  |
| srl_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 3 | matched | RTYPE | fixed_width |
| srl_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 12 | matched | RTYPE | fixed_width |
| srl_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| srl_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 12 | composite, every candidate refuted |  |  |
| srl_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| srl_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 12 | composite, every candidate refuted |  |  |
| srl_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| srl_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 106 instructions, above the walk's bound |  | refused |  |  |
| srl_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| srl_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 12 | composite, every candidate refuted |  |  |
| srl_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | composite, every candidate refuted |  |  |
| srli_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srli_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srli_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srli_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srli_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| srli_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| srli_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srli_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for UTYPE (an eff |  | refused |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srliw_gpr_gpr_imm_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| srlw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 53 | matched | RTYPEW | fixed_width |
| srlw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| srlw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 53 | matched | RTYPEW | fixed_width |
| srlw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| srlw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 230 instructions, above the walk's bound |  | refused |  |  |
| srlw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 74 instructions, above the walk's bound  |  | refused |  |  |
| srlw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 50 | matched | RTYPEW | fixed_width |
| srlw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| srlw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| srlw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| srlw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: no certified pure form for ZICOND_RTYPE  |  | refused |  |  |
| srlw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| srlw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 227 instructions, above the walk's bound |  | refused |  |  |
| srlw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| srlw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 50 | composite, every candidate refuted |  |  |
| srlw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| sub_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 2028 instructions, above the walk's boun |  | refused |  |  |
| sub_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sub_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 2028 instructions, above the walk's boun |  | refused |  |  |
| sub_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sub_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: compile rc=1: ./main.go:220:29: too many |  | refused |  |  |
| sub_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| sub_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 2028 instructions, above the walk's boun |  | refused |  |  |
| sub_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| sub_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sub_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sub_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sub_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sub_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| sub_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| sub_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sub_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__c__all_constructed | c | all_constructed | REFUSED: 870 instructions, above the walk's bound |  | refused |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__c__native_first | c | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__cpp__all_constructed | cpp | all_constructed | REFUSED: 870 instructions, above the walk's bound |  | refused |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__cpp__native_first | cpp | native_first | REFUSED: 67 instructions, above the walk's bound  |  | refused |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: 1070 instructions, above the walk's boun |  | refused |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__go__native_first | go | native_first | REFUSED: 72 instructions, above the walk's bound  |  | refused |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__rust__all_constructed | rust | all_constructed | REFUSED: 867 instructions, above the walk's bound |  | refused |  |  |
| subw_gpr_gpr_gpr_32__reg_a0__rust__native_first | rust | native_first | REFUSED: 71 instructions, above the walk's bound  |  | refused |  |  |
| subw_gpr_gpr_same_32__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| subw_gpr_gpr_same_32__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| subw_gpr_gpr_same_32__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| subw_gpr_gpr_same_32__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| subw_gpr_gpr_same_32__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| subw_gpr_gpr_same_32__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| subw_gpr_gpr_same_32__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| subw_gpr_gpr_same_32__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_32__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_fpr_fpr_32__mem_MEM_fa1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_32__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_gpr_32__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_imm_32__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_gpr_same_32__mem_MEM_a1__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_imm_32__mem_MEM_0x3__rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___c__all_constructed | c | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___c__native_first | c | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___cpp__all_constructed | cpp | all_constructed | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___cpp__native_first | cpp | native_first | CERTIFIED | 3 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___go__all_constructed | go | all_constructed | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___go__native_first | go | native_first | CERTIFIED | 6 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___rust__all_constructed | rust | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| sw_gpr_mem_32__mem_MEM_0x0_a1___rust__native_first | rust | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| xor_gpr_gpr_gpr_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| xor_gpr_gpr_gpr_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| xor_gpr_gpr_gpr_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| xor_gpr_gpr_gpr_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| xor_gpr_gpr_gpr_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| xor_gpr_gpr_gpr_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| xor_gpr_gpr_gpr_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | matched | RTYPE | same_text |
| xor_gpr_gpr_gpr_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | matched | RTYPE | same_text |
| xor_gpr_gpr_same_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xor_gpr_gpr_same_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xor_gpr_gpr_same_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xor_gpr_gpr_same_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xor_gpr_gpr_same_64__reg_a0__go__all_constructed | go | all_constructed | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| xor_gpr_gpr_same_64__reg_a0__go__native_first | go | native_first | REFUSED: no certified pure form for JALR (an elem |  | refused |  |  |
| xor_gpr_gpr_same_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xor_gpr_gpr_same_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xori_gpr_gpr_imm_64__reg_a0__c__all_constructed | c | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xori_gpr_gpr_imm_64__reg_a0__c__native_first | c | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xori_gpr_gpr_imm_64__reg_a0__cpp__all_constructed | cpp | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xori_gpr_gpr_imm_64__reg_a0__cpp__native_first | cpp | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xori_gpr_gpr_imm_64__reg_a0__go__all_constructed | go | all_constructed | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| xori_gpr_gpr_imm_64__reg_a0__go__native_first | go | native_first | CERTIFIED | 5 | composite, every candidate refuted |  |  |
| xori_gpr_gpr_imm_64__reg_a0__rust__all_constructed | rust | all_constructed | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
| xori_gpr_gpr_imm_64__reg_a0__rust__native_first | rust | native_first | CERTIFIED | 1 | own opcode not a candidate (immediate) |  |  |
