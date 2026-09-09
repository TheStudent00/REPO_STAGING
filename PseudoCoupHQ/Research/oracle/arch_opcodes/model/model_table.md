# model_table.md — the arch-opcode model table

Tasks m1 and m1b, node `hq.research.arch_unit_oracle`. Written by `model_table.py`; never hand-edited. Sections 7, 8 and 9 are task m1b's: the one width rule, the coverage table over the corpus's 162 mnemonics, and the control transfers' guard rows.

**What this table is, one sentence.** Every mapping the reference simulator's `opcode_table` holds, one row per (`mnem`, operand shape, width) the sweep in `op_pipeline/lean/model_translate.py` spells, with the z3 term each written place receives printed by the pipeline's layer-5 rule, the corpus's own attestation beside it, and the equivalences between rows reported rather than applied.

The printer is `term.Term.normalize`, the pipeline's own fixed-rule re-render; it applies to a bare z3 expression, so the fallback the brief allowed (`str(z3.simplify(t))`) was not used. Every term below is LITERAL.

| what | count |
|---|---|
| sweep attempts | 71778 |
| rows TRANSLATED | 36903 |
| table mnemonics | 171 |
| corpus mnemonics | 162 |

## 1. Five rows in full, LITERAL

### `add` gpr_gpr 32

Block — the row as `model_table.json` holds it:

```
{
 "attestation": {
  "example_units": [
   "go/op_312",
   "swift/op_222",
   "java/op_1"
  ],
  "flag_pair_rows": 0,
  "ledger_rows": 11,
  "setter": [],
  "units": 11
 },
 "builder": "build_binary",
 "condition": "raise NotModeled( \"a one-operand line of %r is not modeled: the one-operand \" \"form is the accumulator-pair widening multiply, which is \" \"not this mnemonic's\" % ops.mnemonic)",
 "key_width": 32,
 "mapping": [
  {
   "text": "Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))",
   "writes": "reg_rdi"
  },
  {
   "mnem": "add",
   "text": "Concat(Extract(31, 0, v0), Extract(31, 0, v1))",
   "writes": "flags"
  }
 ],
 "mnem": "add",
 "operands": [
  "%esi",
  "%edi"
 ],
 "outcome": "TRANSLATED",
 "preseeded": false,
 "reads": [
  "the operands the opcode names"
 ],
 "reads_the_flags": false,
 "row_id": "r00138",
 "shape": "gpr_gpr",
 "text": "add %esi,%edi",
 "width": 32,
 "writes": [
  "the last named operand",
  "the flags"
 ],
 "writes_the_flags": true
}
```

### `imul` gpr_one 32

Block — the row as `model_table.json` holds it:

```
{
 "attestation": {
  "ledger_rows": 0,
  "units": 0
 },
 "builder": "build_binary",
 "condition": "raise NotModeled( \"a one-operand line of %r is not modeled: the one-operand \" \"form is the accumulator-pair widening multiply, which is \" \"not this mnemonic's\" % ops.mnemonic)",
 "key_width": 32,
 "mapping": [
  {
   "text": "Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))",
   "writes": "reg_rax"
  },
  {
   "text": "Concat(0, Extract(63, 32, Concat(Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 0, v0))*Concat(Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 31, v1), Extract(31, 0, v1))))",
   "writes": "reg_rdx"
  }
 ],
 "mnem": "imul",
 "operands": [
  "%edi"
 ],
 "outcome": "TRANSLATED",
 "preseeded": false,
 "reads": [
  "the operands the opcode names"
 ],
 "reads_the_flags": false,
 "row_id": "r07501",
 "shape": "gpr_one",
 "text": "imul %edi",
 "width": 32,
 "writes": [
  "the last named operand",
  "the flags"
 ],
 "writes_the_flags": true
}
```

### `imul` gpr_gpr 32

Block — the row as `model_table.json` holds it:

```
{
 "attestation": {
  "example_units": [
   "c/op_174",
   "cpp/op_174",
   "go/op_60"
  ],
  "flag_pair_rows": 0,
  "ledger_rows": 266,
  "setter": [],
  "units": 266
 },
 "builder": "build_binary",
 "condition": "raise NotModeled( \"a one-operand line of %r is not modeled: the one-operand \" \"form is the accumulator-pair widening multiply, which is \" \"not this mnemonic's\" % ops.mnemonic)",
 "key_width": 32,
 "mapping": [
  {
   "text": "Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))",
   "writes": "reg_rdi"
  },
  {
   "mnem": "imul",
   "text": "Concat(Extract(31, 0, v0), Extract(31, 0, v1))",
   "writes": "flags"
  }
 ],
 "mnem": "imul",
 "operands": [
  "%esi",
  "%edi"
 ],
 "outcome": "TRANSLATED",
 "preseeded": false,
 "reads": [
  "the operands the opcode names"
 ],
 "reads_the_flags": false,
 "row_id": "r07499",
 "shape": "gpr_gpr",
 "text": "imul %esi,%edi",
 "width": 32,
 "writes": [
  "the last named operand",
  "the flags"
 ],
 "writes_the_flags": true
}
```

### `sar` cl_gpr 32

Block — the row as `model_table.json` holds it:

```
{
 "attestation": {
  "example_units": [
   "c/op_714",
   "c/op_715",
   "c/op_716"
  ],
  "flag_pair_rows": 0,
  "ledger_rows": 335,
  "setter": [],
  "units": 335
 },
 "builder": "build_shift",
 "condition": "raise NotModeled( \"a shift count operand %r that is neither %%cl nor an \" \"immediate is not modeled\" % count_text) || masked = count & z3.BitVecVal(shift_mask(width), 8)",
 "key_width": 32,
 "mapping": [
  {
   "text": "Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))",
   "writes": "reg_rdi"
  }
 ],
 "mnem": "sar",
 "operands": [
  "%cl",
  "%edi"
 ],
 "outcome": "TRANSLATED",
 "preseeded": false,
 "reads": [
  "the operands the opcode names"
 ],
 "reads_the_flags": false,
 "row_id": "r12211",
 "shape": "cl_gpr",
 "text": "sar %cl,%edi",
 "width": 32,
 "writes": [
  "the last named operand"
 ],
 "writes_the_flags": false
}
```

### `idiv` gpr_one 32

Block — the row as `model_table.json` holds it:

```
{
 "attestation": {
  "example_units": [
   "c/op_210",
   "c/op_240",
   "c/op_246"
  ],
  "flag_pair_rows": 0,
  "ledger_rows": 778,
  "setter": [],
  "units": 389
 },
 "builder": "build_division",
 "condition": "raise NotModeled( \"a division at width %d is not modeled\" % width)",
 "key_width": 32,
 "mapping": [
  {
   "text": "Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))",
   "writes": "reg_rax"
  },
  {
   "text": "Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))",
   "writes": "reg_rdx"
  }
 ],
 "mnem": "idiv",
 "operands": [
  "%edi"
 ],
 "outcome": "TRANSLATED",
 "preseeded": false,
 "reads": [
  "the operands the opcode names",
  "the accumulator and the data register"
 ],
 "reads_the_flags": false,
 "row_id": "r07409",
 "shape": "gpr_one",
 "text": "idiv %edi",
 "width": 32,
 "writes": [
  "the accumulator and the data register"
 ],
 "writes_the_flags": false
}
```

## 2. The partial region, read from each builder's own source

The rule, LITERAL: every statement of a builder's source carrying one of the marks `raise NotModeled(`, `shift_mask(`, `z3.If(` is quoted whole; a builder carrying none of them is recorded as total on bit patterns.

WHAT THE THREE MARKS DO NOT CATCH, named rather than left implicit: a branch on the NUMBER of operands. `reference.build_binary` opens `if len(ops.texts) == 1: build_wide_multiply(ops); return`, so a one-operand line of any BINARY-family mnemonic is given the accumulator-pair widening multiply. That is why `add`, `and`, `or`, `sub` and `xor` carry `gpr_one` and `mem_one` rows whose mapping is a multiply, and it is recorded here as a fact about the reference, not repaired: `reference.py` is a shared file this task did not touch. Measured: 28 such rows, of which only `imul`'s are attested by the corpus at all (2 ledger rows).

THE DIVISION ROWS, since the brief asks for them by name: `build_division`'s only stated condition is a WIDTH refusal. It writes z3's `SDiv`/`UDiv` and `SRem`/`URem`, which are TOTAL functions on bit patterns, so division by zero and the `MIN / -1` case are not branched on and no fault region is named in the model. The fault is the machine's, and this reference does not carry it.

Table 1 — one line per builder in the table, with the condition its own source states.

| builder | condition, quoted |
|---|---|
| `<lambda>` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_accumulator_widen` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_binary` | raise NotModeled( "a one-operand line of %r is not modeled: the one-operand " "form is the accumulator-pair widening multiply, which is " "not this mnemonic's" % ops.mnemonic) |
| `build_bit_scan_reverse` | result = z3.If(bit == z3.BitVecVal(1, 1), z3.BitVecVal(position, destination_width), result) |
| `build_bit_test` | raise NotModeled( "a bit test whose index %r is not an immediate is not " "modeled" % index_text) |
| `build_bitwise_128` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_branch_condition` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_carry_binary` | carry_value = z3.If(carry_in, z3.BitVecVal(1, width), z3.BitVecVal(0, width)) |
| `build_convert_to_float` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_convert_widen` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_division` | raise NotModeled( "a division at width %d is not modeled" % width) |
| `build_double_shift` | raise NotModeled( "a double-shift count operand %r that is neither %%cl nor " "an immediate is not modeled" % count_text) \|\| masked = count & z3.BitVecVal(shift_mask(width), 8) |
| `build_exchange` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_extract_word` | raise NotModeled( "a word extraction whose index %r is not an immediate is " "not modeled" % index_text) |
| `build_flag_only` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_float_binary` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_float_compare_mask` | mask = z3.If(taken, z3.BitVecVal(-1, width), z3.BitVecVal(0, width)) |
| `build_float_flag_only` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_increment` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_insert_word` | raise NotModeled( "a word insertion whose index %r is not an immediate is " "not modeled" % index_text) |
| `build_lane_move` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_lea` | raise NotModeled( "lea addressing form %r is not the (displacement, base, " "index, scale) shape this file models" % text) \|\| raise NotModeled( "an address computation over base register %r: this " "reference has no model for the address that register " "holds, only for the value a read through it returns" % base) |
| `build_move_condition` | ops.write(1, z3.If(predicate, new, old)) |
| `build_no_operation` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_packed_float` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_plain_move` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_pop` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_push` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_set_condition` | ops.write(0, z3.If(predicate, z3.BitVecVal(1, 8), z3.BitVecVal(0, 8))) |
| `build_shift` | raise NotModeled( "a shift count operand %r that is neither %%cl nor an " "immediate is not modeled" % count_text) \|\| masked = count & z3.BitVecVal(shift_mask(width), 8) |
| `build_spread_sign` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_unary` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_unpack_high_pairs` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_unpack_low_double_words` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_unpack_low_quad_words` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_whole_move` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_wide_multiply` | raise NotModeled( "a widening multiply at width %d is not modeled: its " "destination pair is the accumulator's own two halves, " "which are not two families" % width) |
| `build_x87_arithmetic` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_x87_compare` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_x87_exchange` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |
| `build_x87_load` | raise NotModeled( "the x87 load %r names no memory operand this file can " "read" % ops.mnemonic) |
| `build_x87_store` | total on bit patterns: this builder's own source states no refusal, no hardware mask and no branch on an operand value |

## 3. The corpus's attestation

Every arch-opcode ledger row AND every flag-pair ledger row of every canon40 unit is classified into the sweep's own operand shapes by the operand TEXTS of the body line that made it (`term.relink` gives the line). The classifier is `operand_class` and `SHAPE_OF_CLASSES` in `model_table.py`, LITERAL there.

A FLAG-PAIR row's producer is the pair (flag-setting opcode, flag-reading opcode), and the READING half is the mnemonic attested: its operands come from the relinked line like any other, its cell is keyed like any other, and the cell records the setter, since what the mapping computes is a function of the flags that setter wrote. Task m1 attested none of them, having copied `ledger_signatures.census_pass`, which records the consumer in `seen_as_flag_pair_element` and moves on.

| what | count |
|---|---|
| shards streamed | 332 |
| units seen | 31078 |
| units relinked | 30436 |
| units the relink refused | 642 |
| attested (mnem, shape, key_width) cells | 257 |
| arch-opcode ledger rows seen | 130108 |
| flag-pair ledger rows seen (the OUT block's repeats excluded) | 23942 |
| of those, guard rows for a branch | 1201 |
| of those, value cells for a flag consumer | 22741 |
| arch-opcode rows placed into a cell | 110311 |
| attested cells that land on a TRANSLATED row | 253 |

Table 2 — the rows the classifier could not place, by cause.

| cause | rows | an example line |
|---|---|---|
| the answer row of the OUT block, which canonical_form.wrap_unit adds AFTER the dataflow walk: it repeats the producer of the row it copies, so the relink gives it no line of its own and counting it would count one instruction twice | 19797 | `` |
| the unit's body could not be relinked, so no row of it has a line | 0 | `` |

## 4. The equivalences, REPORTED and never applied

Table 3 — the same-builder groups and z3's verdicts over their cells. A cell is one (pair, shape, width) at which both mnemonics carry a TRANSLATED row; the verdict words are z3's own (`unsat` = no differing point exists, `sat` = one does, `unknown` = the 3,000 ms ceiling).

| group | members | cells | equal everywhere | not equal | alias group |
|---|---|---|---|---|---|
| g00 | `faddl` `faddp` `fadds` `fdivl` `fdivp` `fdivrl` `fdivrp` `fdivrs` `fdivs` `fiaddl` `fiadds` `fidivl` `fidivrl` `fidivrs` `fidivs` `fimull` `fimuls` `fisubl` `fisubrl` `fisubrs` `fisubs` `fmull` `fmulp` `fmuls` `fsubl` `fsubp` `fsubrl` `fsubrp` `fsubrs` `fsubs` | 30984 | 4168 | 26816 | False |
| g01 | `seta` `setae` `setb` `setbe` `sete` `setg` `setge` `setl` `setle` `setne` `setnp` `setns` `seto` `setp` `sets` | 6300 | 0 | 6300 | False |
| g02 | `ja` `jae` `jb` `jbe` `je` `jg` `jge` `jl` `jle` `jne` `jns` `jo` `js` | 6240 | 0 | 6240 | False |
| g03 | `cmova` `cmovae` `cmovb` `cmovbe` `cmove` `cmovge` `cmovl` `cmovle` `cmovne` `cmovns` `cmovs` | 3740 | 440 | 3300 | False |
| g04 | `addsd` `addss` `divsd` `divss` `mulsd` `mulss` `subsd` `subss` | 784 | 0 | 784 | False |
| g05 | `andpd` `andps` `orpd` `orps` `pand` `pxor` `xorpd` `xorps` | 448 | 136 | 312 | False |
| g06 | `fildl` `fildll` `filds` `fld` `fldl` `flds` `fldt` `fldz` | 672 | 504 | 168 | False |
| g07 | `add` `and` `imul` `or` `sub` `xor` | 1020 | 8 | 1012 | False |
| g08 | `cs` `endbr64` `nop` `nopl` `ret` | 0 | 0 | 0 | False |
| g09 | `cmpeqsd` `cmpeqss` `cmpneqsd` `cmpneqss` | 168 | 0 | 168 | False |
| g10 | `mov` `movabs` `movb` `movq` | 378 | 362 | 16 | False |
| g11 | `cltd` `cqto` `cwtd` | 240 | 0 | 240 | False |
| g12 | `movapd` `movaps` `movdqa` | 72 | 72 | 0 | True |
| g13 | `movd` `movsd` `movss` | 148 | 68 | 80 | False |
| g14 | `sar` `shl` `shr` | 72 | 4 | 68 | False |
| g15 | `adc` `sbb` | 68 | 0 | 68 | False |
| g16 | `cmp` `test` | 68 | 0 | 68 | False |
| g17 | `cvtsi2sd` `cvtsi2ss` | 28 | 0 | 28 | False |
| g18 | `div` `idiv` | 36 | 0 | 36 | False |
| g19 | `fstp` `fstpt` | 24 | 24 | 0 | True |
| g20 | `fucomi` `fucomip` | 80 | 0 | 80 | False |
| g21 | `neg` `not` | 56 | 0 | 56 | False |
| g22 | `shld` `shrd` | 16 | 0 | 16 | False |
| g23 | `ucomisd` `ucomiss` | 28 | 0 | 28 | False |

Table 4 — the pair the brief names, decided the same way. These two do not share a builder, so this is not a `same_builder` edge.

| shape | width | destination | flags | left writes flags | right writes flags |
|---|---|---|---|---|---|
| mem_gpr | 8 | sat | one of the two places is not written at all | True | False |
| lea_mem | 8 | sat | one of the two places is not written at all | True | False |
| mem_xmm | 8 | sat | one of the two places is not written at all | True | False |
| mem_gpr | 16 | sat | one of the two places is not written at all | True | False |
| lea_mem | 16 | sat | one of the two places is not written at all | True | False |
| mem_xmm | 16 | sat | one of the two places is not written at all | True | False |
| mem_gpr | 32 | sat | one of the two places is not written at all | True | False |
| lea_mem | 32 | sat | one of the two places is not written at all | True | False |
| mem_xmm | 32 | sat | one of the two places is not written at all | True | False |
| mem_gpr | 64 | sat | one of the two places is not written at all | True | False |
| lea_mem | 64 | sat | one of the two places is not written at all | True | False |
| mem_xmm | 64 | sat | one of the two places is not written at all | True | False |

## 5. The counts, beside the 162

| what | count |
|---|---|
| table mnemonics | 171 |
| corpus mnemonics | 162 |
| in both | 162 |
| table only | 9 |
| corpus only | 0 |
| rows TRANSLATED | 36903 |
| distinct mappings after `identical_text` | 5311 |
| `identical_text` pairs | 1072270 |
| distinct (mnem, shape, key_width) triples with a TRANSLATED row | 6218 |
| attested cells | 257 |
| attested cells that land on a TRANSLATED row | 253 |
| attested cells with no TRANSLATED row | 4 |
| corpus mnemonics with at least one placed cell | 134 |
| guard rows, over the branch mnemonics | 1201 |

`identical_text` is textual identity after normalisation, which is an UNDER-COUNT of true equivalence: two rows can compute one function and print differently, and only a solver call decides that. The 1072270 pairs are written as the 2291 equivalence CLASSES they form, keyed by row ids (`identical_text_classes`), because textual identity is an equivalence relation and the classes carry the same information as the pairs.

Table only, LITERAL: `bsr` `bt` `cmova` `cs` `endbr64` `fld` `inc` `pinsrw` `xchg`

Corpus only, LITERAL: (none)

Table 5 — the SPLITS: the mnemonics whose TRANSLATED rows do not all write the same multiset of place KINDS, which is the split the ruling of 2026-09-08 names read mechanically (one-operand `imul` writes two registers, the accumulator pair; two-operand `imul` writes one register and the flags). The last two columns are the finer readings, before the kind abstraction and then over destination texts; both are larger by construction.

| mnem | place kind sets | place-name sets | destination texts |
|---|---|---|---|
| `imul` | `flags mem` / `flags reg` / `reg` / `reg reg` | 7 | 38 |
| `xchg` | `mem reg` / `reg` / `reg reg` | 12 | 32 |
| `adc` | `flags mem` / `flags reg` | 5 | 52 |
| `add` | `flags mem` / `flags reg` | 5 | 34 |
| `addsd` | `mem` / `reg` | 3 | 7 |
| `addss` | `mem` / `reg` | 3 | 5 |
| `and` | `flags mem` / `flags reg` | 5 | 25 |
| `andpd` | `mem` / `reg` | 2 | 3 |
| `andps` | `mem` / `reg` | 2 | 3 |
| `bsr` | `flags mem` / `flags reg` | 4 | 30 |
| `cmova` | `flags mem` / `flags reg` | 5 | 34 |
| `cmovae` | `flags mem` / `flags reg` | 5 | 49 |
| `cmovb` | `flags mem` / `flags reg` | 5 | 49 |
| `cmovbe` | `flags mem` / `flags reg` | 5 | 34 |
| `cmove` | `flags mem` / `flags reg` | 5 | 34 |
| `cmovge` | `flags mem` / `flags reg` | 5 | 34 |
| `cmovl` | `flags mem` / `flags reg` | 5 | 34 |
| `cmovle` | `flags mem` / `flags reg` | 5 | 34 |
| `cmovne` | `flags mem` / `flags reg` | 5 | 34 |
| `cmovns` | `flags mem` / `flags reg` | 5 | 49 |
| `cmovs` | `flags mem` / `flags reg` | 5 | 49 |
| `cmpeqsd` | `mem` / `reg` | 3 | 7 |
| `cmpeqss` | `mem` / `reg` | 3 | 5 |
| `cmpneqsd` | `mem` / `reg` | 3 | 7 |
| `cmpneqss` | `mem` / `reg` | 3 | 5 |
| `cvtsi2sd` | `mem` / `reg` | 3 | 11 |
| `cvtsi2ss` | `mem` / `reg` | 3 | 11 |
| `cvtss2sd` | `mem` / `reg` | 3 | 4 |
| `div` | `reg` / `reg reg` | 2 | 5 |
| `divsd` | `mem` / `reg` | 3 | 6 |
| `divss` | `mem` / `reg` | 3 | 4 |
| `idiv` | `reg` / `reg reg` | 2 | 5 |
| `inc` | `flags mem` / `flags reg` | 7 | 24 |
| `mov` | `mem` / `reg` | 4 | 21 |
| `movabs` | `mem` / `reg` | 4 | 21 |
| `movapd` | `mem` / `reg` | 3 | 3 |
| `movaps` | `mem` / `reg` | 3 | 3 |
| `movb` | `mem` / `reg` | 4 | 18 |
| `movd` | `mem` / `reg` | 3 | 6 |
| `movdqa` | `mem` / `reg` | 3 | 3 |
| `movq` | `mem` / `reg` | 4 | 18 |
| `movsbl` | `mem` / `reg` | 5 | 8 |
| `movsbq` | `mem` / `reg` | 5 | 8 |
| `movsd` | `mem` / `reg` | 3 | 9 |
| `movslq` | `mem` / `reg` | 5 | 8 |
| `movss` | `mem` / `reg` | 3 | 6 |
| `movswl` | `mem` / `reg` | 5 | 8 |
| `movzbl` | `mem` / `reg` | 5 | 8 |
| `movzwl` | `mem` / `reg` | 5 | 8 |
| `mul` | `reg` / `reg reg` | 2 | 7 |
| `mulsd` | `mem` / `reg` | 3 | 7 |
| `mulss` | `mem` / `reg` | 3 | 5 |
| `neg` | `flags mem` / `flags reg` | 7 | 24 |
| `not` | `mem` / `reg` | 7 | 24 |
| `or` | `flags mem` / `flags reg` | 5 | 34 |
| `orpd` | `mem` / `reg` | 2 | 3 |
| `orps` | `mem` / `reg` | 2 | 3 |
| `pand` | `mem` / `reg` | 2 | 3 |
| `pop` | `mem` / `reg` | 7 | 7 |
| `punpckldq` | `mem` / `reg` | 2 | 3 |
| `punpcklqdq` | `mem` / `reg` | 2 | 3 |
| `pxor` | `mem` / `reg` | 2 | 3 |
| `sbb` | `flags mem` / `flags reg` | 5 | 48 |
| `seta` | `flags mem` / `flags reg` | 7 | 7 |
| `setae` | `flags mem` / `flags reg` | 7 | 28 |
| `setb` | `flags mem` / `flags reg` | 7 | 28 |
| `setbe` | `flags mem` / `flags reg` | 7 | 7 |
| `sete` | `flags mem` / `flags reg` | 7 | 7 |
| `setg` | `flags mem` / `flags reg` | 7 | 7 |
| `setge` | `flags mem` / `flags reg` | 7 | 7 |
| `setl` | `flags mem` / `flags reg` | 7 | 7 |
| `setle` | `flags mem` / `flags reg` | 7 | 7 |
| `setne` | `flags mem` / `flags reg` | 7 | 7 |
| `setnp` | `flags mem` / `flags reg` | 7 | 14 |
| `setns` | `flags mem` / `flags reg` | 7 | 28 |
| `seto` | `flags mem` / `flags reg` | 7 | 28 |
| `setp` | `flags mem` / `flags reg` | 7 | 14 |
| `sets` | `flags mem` / `flags reg` | 7 | 28 |
| `sub` | `flags mem` / `flags reg` | 5 | 27 |
| `subpd` | `mem` / `reg` | 2 | 3 |
| `subsd` | `mem` / `reg` | 3 | 6 |
| `subss` | `mem` / `reg` | 3 | 4 |
| `unpckhpd` | `mem` / `reg` | 2 | 3 |
| `xor` | `flags mem` / `flags reg` | 5 | 31 |
| `xorpd` | `mem` / `reg` | 2 | 3 |
| `xorps` | `mem` / `reg` | 2 | 3 |

Table 6 — the (mnem, shape, width) cells the corpus attests for which the table carries no TRANSLATED row. The sweep spells vector operands at the four general-register widths only, so a corpus row at a 128-bit vector width has no cell of its own in the table.

| mnem | shape | width | ledger rows | units |
|---|---|---|---|---|
| `pcmpeqb` | mem_xmm | 128 | 2 | 2 |
| `pcmpeqb` | xmm_xmm | 128 | 2 | 2 |
| `pcmpeqd` | xmm_same | 128 | 2 | 2 |
| `pmovmskb` | xmm_gpr | 32 | 2 | 2 |

## 6. NO_BUILDER and NOT_MODELLED, by cause

### NOTHING_WRITTEN

| rows | cause, quoted from the sweep row |
|---|---|
| 1229 | the builder ran and changed no register and no flag |

### NOT_MODELLED_BY_THE_REFERENCE

| rows | cause, quoted from the sweep row |
|---|---|
| 6808 | Z3Exception: First argument must be a Z3 floating-point expression |
| 4060 | IndexError: list index out of range |
| 3404 | a flag-reading arch opcode with no flag-setting arch opcode before it in this body |
| 3072 | this body reads x87 stack position 0 without having loaded it inside the body |
| 1312 | operand '%st(1)' states no width |
| 1288 | operand '$0x1' is not a place this file can write |
| 1288 | operand '$0x3' is not a place this file can write |
| 688 | AttributeError: 'BitVecRef' object has no attribute 'as_long' |
| 688 | this opcode reads the carry bit and the flag-setting arch opcode 'bsr' has no carry model in this file |
| 688 | this opcode reads the carry bit and the flag-setting arch opcode 'imul' has no carry model in this file |
| 688 | this opcode reads the carry bit and the flag-setting arch opcode 'inc' has no carry model in this file |
| 628 | operand '%st' is not a place this file can write |
| 628 | operand '%st(1)' is not a place this file can write |
| 313 | a 128-bit read of operand '%rdi' is not modeled |
| 276 | the condition 'a' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 'be' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 'e' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 'ge' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 'l' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 'le' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 'ne' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 'ns' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 276 | the condition 's' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 204 | this body reads x87 stack position 1 without having loaded it inside the body |
| 197 | a 128-bit read of operand '%di' is not modeled |
| 197 | a 128-bit read of operand '%dil' is not modeled |
| 197 | a 128-bit read of operand '%edi' is not modeled |
| 184 | the condition 'g' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 184 | this opcode reads the signed-overflow bit and no flag-setting arch opcode precedes it in this body |
| 184 | this opcode reads the signed-overflow bit and the flag-setting arch opcode 'bsr' has no overflow model in this file |
| 184 | this opcode reads the signed-overflow bit and the flag-setting arch opcode 'bt' has no overflow model in this file |
| 184 | this opcode reads the signed-overflow bit and the flag-setting arch opcode 'imul' has no overflow model in this file |
| 184 | this opcode reads the signed-overflow bit and the flag-setting arch opcode 'inc' has no overflow model in this file |
| 184 | this opcode reads the signed-overflow bit and the flag-setting arch opcode 'ucomisd' has no overflow model in this file |
| 184 | this opcode reads the signed-overflow bit and the flag-setting arch opcode 'ucomiss' has no overflow model in this file |
| 136 | this opcode reads the carry bit and no flag-setting arch opcode precedes it in this body |
| 136 | this opcode reads the carry bit and the flag-setting arch opcode 'ucomisd' has no carry model in this file |
| 136 | this opcode reads the carry bit and the flag-setting arch opcode 'ucomiss' has no carry model in this file |
| 116 | a 128-bit read of operand '%st(1)' is not modeled |
| 112 | ValueError: not enough values to unpack (expected 3, got 2) |
| 107 | a 128-bit read of operand '%esi' is not modeled |
| 107 | a 128-bit read of operand '%rsi' is not modeled |
| 107 | a 128-bit read of operand '%si' is not modeled |
| 107 | a 128-bit read of operand '%sil' is not modeled |
| 92 | a pop at stack offset 0 that this body never wrote -- the value came from outside the unit |
| 92 | the condition 'np' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 92 | the condition 'p' is read after `bt`, which sets only the carry flag and leaves the zero and sign flags undefined |
| 72 | a 128-bit read of operand '$0x1' is not modeled |
| 64 | ValueError: too many values to unpack (expected 2) |
| 60 | the memory operand '(%rsi)' of 'adc' states no width, and no other operand of the line states one |
| 60 | the x87 load 'fildl' names no memory operand this file can read |
| 60 | the x87 load 'fildll' names no memory operand this file can read |
| 60 | the x87 load 'filds' names no memory operand this file can read |
| 60 | the x87 load 'fld' names no memory operand this file can read |
| 60 | the x87 load 'fldl' names no memory operand this file can read |
| 60 | the x87 load 'flds' names no memory operand this file can read |
| 60 | the x87 load 'fldt' names no memory operand this file can read |
| 48 | operand '%st' is neither an immediate, a register nor a memory operand this file reads |
| 44 | the memory operand '(%rsi)' of 'cmova' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmovbe' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmove' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmovge' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmovl' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmovle' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmovne' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmovns' states no width, and no other operand of the line states one |
| 44 | the memory operand '(%rsi)' of 'cmovs' states no width, and no other operand of the line states one |
| 40 | a division at width 128 is not modeled |
| 40 | operand '$0x1' states no width |
| 40 | operand '$0x3' states no width |
| 36 | ValueError: not enough values to unpack (expected 2, got 1) |
| 36 | a shift count operand '%xmm1' that is neither %cl nor an immediate is not modeled |
| 36 | operand '%st(1)' is neither an immediate, a register nor a memory operand this file reads |
| 32 | the memory operand '(%rsi)' of 'cmovae' states no width, and no other operand of the line states one |
| 32 | the memory operand '(%rsi)' of 'cmovb' states no width, and no other operand of the line states one |
| 24 | ValueError: not enough values to unpack (expected 2, got 0) |
| 24 | ValueError: not enough values to unpack (expected 3, got 1) |
| 24 | a 128-bit read of operand '$0x3' is not modeled |
| 24 | a 128-bit read of operand '%cl' is not modeled |
| 24 | a double-shift count operand '%xmm1' that is neither %cl nor an immediate is not modeled |
| 24 | a shift count operand '(%rsi)' that is neither %cl nor an immediate is not modeled |
| 20 | a widening multiply at width 128 is not modeled: its destination pair is the accumulator's own two halves, which are not two families |
| 20 | operand '%st' states no width |
| 16 | ValueError: not enough values to unpack (expected 3, got 0) |
| 16 | a double-shift count operand '(%rsi)' that is neither %cl nor an immediate is not modeled |
| 12 | a 128-bit read of operand '%st' is not modeled |
| 12 | a bit test whose index '%xmm1' is not an immediate is not modeled |
| 12 | a bit test whose index '(%rsi)' is not an immediate is not modeled |
| 12 | a one-operand line of 'add' is not modeled: the one-operand form is the accumulator-pair widening multiply, which is not this mnemonic's |
| 12 | a one-operand line of 'and' is not modeled: the one-operand form is the accumulator-pair widening multiply, which is not this mnemonic's |
| 12 | a one-operand line of 'or' is not modeled: the one-operand form is the accumulator-pair widening multiply, which is not this mnemonic's |
| 12 | a one-operand line of 'sub' is not modeled: the one-operand form is the accumulator-pair widening multiply, which is not this mnemonic's |
| 12 | a one-operand line of 'xor' is not modeled: the one-operand form is the accumulator-pair widening multiply, which is not this mnemonic's |
| 12 | a shift count operand '%xmm0' that is neither %cl nor an immediate is not modeled |
| 12 | a shift count operand '(%rsi,%rcx,1)' that is neither %cl nor an immediate is not modeled |
| 12 | lea addressing form '%xmm1' is not the (displacement, base, index, scale) shape this file models |
| 9 | a shift count operand '%di' that is neither %cl nor an immediate is not modeled |
| 9 | a shift count operand '%dil' that is neither %cl nor an immediate is not modeled |
| 9 | a shift count operand '%edi' that is neither %cl nor an immediate is not modeled |
| 9 | a shift count operand '%rdi' that is neither %cl nor an immediate is not modeled |
| 8 | a bit test whose index '%cl' is not an immediate is not modeled |
| 8 | a double-shift count operand '%xmm0' that is neither %cl nor an immediate is not modeled |
| 8 | a double-shift count operand '(%rsi,%rcx,1)' that is neither %cl nor an immediate is not modeled |
| 8 | lea addressing form '$0x1' is not the (displacement, base, index, scale) shape this file models |
| 8 | lea addressing form '$0x3' is not the (displacement, base, index, scale) shape this file models |
| 8 | lea addressing form '%cl' is not the (displacement, base, index, scale) shape this file models |
| 6 | a double-shift count operand '%di' that is neither %cl nor an immediate is not modeled |
| 6 | a double-shift count operand '%dil' that is neither %cl nor an immediate is not modeled |
| 6 | a double-shift count operand '%edi' that is neither %cl nor an immediate is not modeled |
| 6 | a double-shift count operand '%rdi' that is neither %cl nor an immediate is not modeled |
| 6 | a shift count operand '%esi' that is neither %cl nor an immediate is not modeled |
| 6 | a shift count operand '%rsi' that is neither %cl nor an immediate is not modeled |
| 6 | a shift count operand '%si' that is neither %cl nor an immediate is not modeled |
| 6 | a shift count operand '%sil' that is neither %cl nor an immediate is not modeled |
| 4 | a bit test whose index '%st' is not an immediate is not modeled |
| 4 | a bit test whose index '%st(1)' is not an immediate is not modeled |
| 4 | a bit test whose index '%xmm0' is not an immediate is not modeled |
| 4 | a bit test whose index '(%rsi,%rcx,1)' is not an immediate is not modeled |
| 4 | a double-shift count operand '%esi' that is neither %cl nor an immediate is not modeled |
| 4 | a double-shift count operand '%rsi' that is neither %cl nor an immediate is not modeled |
| 4 | a double-shift count operand '%si' that is neither %cl nor an immediate is not modeled |
| 4 | a double-shift count operand '%sil' that is neither %cl nor an immediate is not modeled |
| 4 | a word extraction whose index '%cl' is not an immediate is not modeled |
| 4 | a word insertion whose index '%cl' is not an immediate is not modeled |
| 4 | lea addressing form '%st' is not the (displacement, base, index, scale) shape this file models |
| 4 | lea addressing form '%st(1)' is not the (displacement, base, index, scale) shape this file models |
| 4 | lea addressing form '%xmm0' is not the (displacement, base, index, scale) shape this file models |
| 4 | the memory operand '(%rsi)' of 'bsr' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'cmp' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'div' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'idiv' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'imul' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'inc' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'lea' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'mul' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'neg' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'not' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'push' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'sar' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'shl' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'shld' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'shr' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'shrd' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'test' states no width, and no other operand of the line states one |
| 4 | the memory operand '(%rsi)' of 'xchg' states no width, and no other operand of the line states one |
| 3 | a bit test whose index '%di' is not an immediate is not modeled |
| 3 | a bit test whose index '%dil' is not an immediate is not modeled |
| 3 | a bit test whose index '%edi' is not an immediate is not modeled |
| 3 | a bit test whose index '%rdi' is not an immediate is not modeled |
| 3 | lea addressing form '%di' is not the (displacement, base, index, scale) shape this file models |
| 3 | lea addressing form '%dil' is not the (displacement, base, index, scale) shape this file models |
| 3 | lea addressing form '%edi' is not the (displacement, base, index, scale) shape this file models |
| 3 | lea addressing form '%rdi' is not the (displacement, base, index, scale) shape this file models |
| 2 | a bit test whose index '%esi' is not an immediate is not modeled |
| 2 | a bit test whose index '%rsi' is not an immediate is not modeled |
| 2 | a bit test whose index '%si' is not an immediate is not modeled |
| 2 | a bit test whose index '%sil' is not an immediate is not modeled |
| 2 | lea addressing form '%esi' is not the (displacement, base, index, scale) shape this file models |
| 2 | lea addressing form '%rsi' is not the (displacement, base, index, scale) shape this file models |
| 2 | lea addressing form '%si' is not the (displacement, base, index, scale) shape this file models |
| 2 | lea addressing form '%sil' is not the (displacement, base, index, scale) shape this file models |

### NO_BUILDER

| rows | cause, quoted from the sweep row |
|---|---|
| 3 | no z3 term is written for this arch opcode yet |
| 2 | a transfer or trap, and this reference walks a body in text order |
| 1 | runtime callee not yet attached (Task 59, node 0_3_5_1_8): the callee's body is to be extracted from the toolchain's libgcc / compiler-rt archive and attached as an ArchUnit this caller references, with the producer {"kind": "runtime_callee"} |

## 7. The one width rule, `key_width`

**What it is, one sentence.** `key_width` is the width the JOIN between the table's rows and the corpus's attestation is keyed by -- the operation's own lane width as the reference's own tables state it -- as against the field `width`, which stays what it always was: the loop variable on a sweep row, and the operand register's width or the ledger row's byte size on an attested cell.

Why it exists: the two sides did not spell `width` the same way for a vector or an x87 operand. The corpus said `addss xmm_xmm 128` (its ledger row holds sixteen bytes) where the table said 8, 16, 32 and 64 (the four general-register widths the sweep's loop walks), and `addss` adds one 32-bit lane, which is neither number.

Table 7 — the rule, LITERAL, and where each number is read from. `model_table.key_width` is the one function; both sides call it.

| the mnemonic is | `key_width` | read from |
|---|---|---|
| an x87 mnemonic (`ledger48.x87_base` names it) | 80 | the x87 register's own width, `reference.X87_SORT` = `z3.FPSort(15, 64)` |
| in `reference.FLOAT_BINARY` | 32 or 64 | the table's own second field |
| in `reference.FLOAT_COMPARE_MASK` | 32 or 64 | the table's own second field |
| in `reference.CONVERT_TO_FLOAT` | 32 or 64 | the table's own value (the destination lane) |
| in `reference.LANE_MOVE` | 32 or 64 | the table's own value |
| in `reference.FLOAT_FLAG_ONLY` | 32 or 64 | `build_float_flag_only`'s own line, `width = 32 if ops.mnemonic.endswith("ss") else 64` |
| `cvtss2sd` | 64 | `build_convert_widen`'s own `FLOAT_SORT[64]` |
| in `reference.PACKED_FLOAT`, `BITWISE_128` or `WHOLE_MOVE` | 128 | the whole vector register |
| one of the six further whole-register vector mnemonics (`model_table.FURTHER_WHOLE_REGISTER`) | 128 | each builder's own `ops.read_128` |
| anything else | the row's own `width` | unchanged |

Table 8 — the cells where the one rule MERGES more than one of the classifier's own widths under a single `key_width`, listed so the merge is visible. The convert family is the case: what varies between its two forms is the SOURCE width, and the rule reads the destination lane, so both forms land on one key. The sweep's own `width` sits beside `key_width` on every row, so nothing is lost.

| mnem | shape | key_width | the classifier's widths |
|---|---|---|---|
| `cvtsi2sd` | gpr_xmm | 64 | 32 64 |
| `cvtsi2ss` | gpr_xmm | 32 | 32 64 |

## 8. The coverage table: one row per corpus mnemonic

Every one of the corpus's 162 mnemonics sits in exactly ONE of four categories, so the four counts sum to 162.

Table 9 — the four categories and their totals.

| category | mnemonics |
|---|---|
| a value cell on a TRANSLATED row | 134 |
| attested at a form the sweep does not spell | 3 |
| a control transfer -- attested by guard rows and never by a value cell | 17 |
| never placed | 8 |

Table 10 — one row per corpus mnemonic. `placed` is the count of that mnemonic's attested value cells that land on a TRANSLATED row of the table; `unspelled` the count that land on none; `guard` the ledger's GUARD-block rows that name it as the reading half of a flag pair; `flag pair` the ledger rows of its value cells that came from a flag pair rather than from an arch-opcode row.

| mnem | placed | unspelled | guard | ledger rows | flag pair | category | cause, quoted |
|---|---|---|---|---|---|---|---|
| `adc` | 2 | 0 | 0 | 356 | 0 | a value cell on a TRANSLATED row |  |
| `add` | 7 | 0 | 0 | 1081 | 0 | a value cell on a TRANSLATED row |  |
| `addsd` | 2 | 0 | 0 | 264 | 0 | a value cell on a TRANSLATED row |  |
| `addss` | 3 | 0 | 0 | 625 | 0 | a value cell on a TRANSLATED row |  |
| `and` | 6 | 0 | 0 | 5924 | 0 | a value cell on a TRANSLATED row |  |
| `andpd` | 1 | 0 | 0 | 6 | 0 | a value cell on a TRANSLATED row |  |
| `andps` | 1 | 0 | 0 | 6 | 0 | a value cell on a TRANSLATED row |  |
| `call` | 0 | 0 | 0 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | an unconditional transfer: it produces no ledger row of any kind, because the ledger records one row per value produced and this opcode produces none; the reference registers it with no builder -- 'runtime callee not yet attached (Task 59, node 0_3_5_1_8): the callee\'s body is to be extracted from the toolchain\'s libgcc / compiler-rt archive and attached as an ArchUnit this caller references, with the producer {"kind": "runtime_callee"}' |
| `cltd` | 1 | 0 | 0 | 267 | 0 | a value cell on a TRANSLATED row |  |
| `cmovae` | 2 | 0 | 0 | 35 | 35 | a value cell on a TRANSLATED row |  |
| `cmovb` | 2 | 0 | 0 | 80 | 80 | a value cell on a TRANSLATED row |  |
| `cmovbe` | 1 | 0 | 0 | 502 | 502 | a value cell on a TRANSLATED row |  |
| `cmove` | 2 | 0 | 0 | 287 | 287 | a value cell on a TRANSLATED row |  |
| `cmovge` | 2 | 0 | 0 | 18 | 18 | a value cell on a TRANSLATED row |  |
| `cmovl` | 2 | 0 | 0 | 12 | 12 | a value cell on a TRANSLATED row |  |
| `cmovle` | 1 | 0 | 0 | 53 | 53 | a value cell on a TRANSLATED row |  |
| `cmovne` | 2 | 0 | 0 | 400 | 400 | a value cell on a TRANSLATED row |  |
| `cmovns` | 2 | 0 | 0 | 55 | 55 | a value cell on a TRANSLATED row |  |
| `cmovs` | 1 | 0 | 0 | 2 | 2 | a value cell on a TRANSLATED row |  |
| `cmp` | 9 | 0 | 0 | 7377 | 0 | a value cell on a TRANSLATED row |  |
| `cmpeqsd` | 2 | 0 | 0 | 128 | 0 | a value cell on a TRANSLATED row |  |
| `cmpeqss` | 2 | 0 | 0 | 299 | 0 | a value cell on a TRANSLATED row |  |
| `cmpneqsd` | 2 | 0 | 0 | 208 | 0 | a value cell on a TRANSLATED row |  |
| `cmpneqss` | 2 | 0 | 0 | 461 | 0 | a value cell on a TRANSLATED row |  |
| `cqto` | 1 | 0 | 0 | 374 | 0 | a value cell on a TRANSLATED row |  |
| `cvtsi2sd` | 1 | 0 | 0 | 860 | 0 | a value cell on a TRANSLATED row |  |
| `cvtsi2ss` | 1 | 0 | 0 | 2936 | 0 | a value cell on a TRANSLATED row |  |
| `cvtss2sd` | 2 | 0 | 0 | 176 | 0 | a value cell on a TRANSLATED row |  |
| `cwtd` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 8 times (unique_opcodes.json) |
| `cwtl` | 1 | 0 | 0 | 22 | 0 | a value cell on a TRANSLATED row |  |
| `div` | 4 | 0 | 0 | 1072 | 0 | a value cell on a TRANSLATED row |  |
| `divsd` | 2 | 0 | 0 | 124 | 0 | a value cell on a TRANSLATED row |  |
| `divss` | 2 | 0 | 0 | 295 | 0 | a value cell on a TRANSLATED row |  |
| `faddl` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `faddp` | 1 | 0 | 0 | 30 | 0 | a value cell on a TRANSLATED row |  |
| `fadds` | 1 | 0 | 0 | 96 | 0 | a value cell on a TRANSLATED row |  |
| `fdivl` | 1 | 0 | 0 | 2 | 0 | a value cell on a TRANSLATED row |  |
| `fdivp` | 1 | 0 | 0 | 15 | 0 | a value cell on a TRANSLATED row |  |
| `fdivrl` | 1 | 0 | 0 | 2 | 0 | a value cell on a TRANSLATED row |  |
| `fdivrp` | 1 | 0 | 0 | 15 | 0 | a value cell on a TRANSLATED row |  |
| `fdivrs` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `fdivs` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `fiaddl` | 1 | 0 | 0 | 16 | 0 | a value cell on a TRANSLATED row |  |
| `fiadds` | 1 | 0 | 0 | 28 | 0 | a value cell on a TRANSLATED row |  |
| `fidivl` | 1 | 0 | 0 | 8 | 0 | a value cell on a TRANSLATED row |  |
| `fidivrl` | 1 | 0 | 0 | 8 | 0 | a value cell on a TRANSLATED row |  |
| `fidivrs` | 1 | 0 | 0 | 14 | 0 | a value cell on a TRANSLATED row |  |
| `fidivs` | 1 | 0 | 0 | 14 | 0 | a value cell on a TRANSLATED row |  |
| `fildl` | 1 | 0 | 0 | 116 | 0 | a value cell on a TRANSLATED row |  |
| `fildll` | 1 | 0 | 0 | 332 | 0 | a value cell on a TRANSLATED row |  |
| `filds` | 1 | 0 | 0 | 194 | 0 | a value cell on a TRANSLATED row |  |
| `fimull` | 1 | 0 | 0 | 16 | 0 | a value cell on a TRANSLATED row |  |
| `fimuls` | 1 | 0 | 0 | 28 | 0 | a value cell on a TRANSLATED row |  |
| `fisubl` | 1 | 0 | 0 | 8 | 0 | a value cell on a TRANSLATED row |  |
| `fisubrl` | 1 | 0 | 0 | 8 | 0 | a value cell on a TRANSLATED row |  |
| `fisubrs` | 1 | 0 | 0 | 14 | 0 | a value cell on a TRANSLATED row |  |
| `fisubs` | 1 | 0 | 0 | 14 | 0 | a value cell on a TRANSLATED row |  |
| `fldl` | 1 | 0 | 0 | 28 | 0 | a value cell on a TRANSLATED row |  |
| `flds` | 1 | 0 | 0 | 56 | 0 | a value cell on a TRANSLATED row |  |
| `fldt` | 1 | 0 | 0 | 1527 | 0 | a value cell on a TRANSLATED row |  |
| `fldz` | 1 | 0 | 0 | 321 | 0 | a value cell on a TRANSLATED row |  |
| `fmull` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `fmulp` | 1 | 0 | 0 | 30 | 0 | a value cell on a TRANSLATED row |  |
| `fmuls` | 1 | 0 | 0 | 8 | 0 | a value cell on a TRANSLATED row |  |
| `fstp` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 1031 times (unique_opcodes.json) |
| `fstpt` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 126 times (unique_opcodes.json) |
| `fsubl` | 1 | 0 | 0 | 2 | 0 | a value cell on a TRANSLATED row |  |
| `fsubp` | 1 | 0 | 0 | 15 | 0 | a value cell on a TRANSLATED row |  |
| `fsubrl` | 1 | 0 | 0 | 2 | 0 | a value cell on a TRANSLATED row |  |
| `fsubrp` | 1 | 0 | 0 | 15 | 0 | a value cell on a TRANSLATED row |  |
| `fsubrs` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `fsubs` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `fucomi` | 1 | 0 | 0 | 108 | 0 | a value cell on a TRANSLATED row |  |
| `fucomip` | 1 | 0 | 0 | 1031 | 0 | a value cell on a TRANSLATED row |  |
| `fxch` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 289 times (unique_opcodes.json) |
| `idiv` | 4 | 0 | 0 | 1750 | 0 | a value cell on a TRANSLATED row |  |
| `imul` | 4 | 0 | 0 | 877 | 0 | a value cell on a TRANSLATED row |  |
| `ja` | 0 | 0 | 6 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 6 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jae` | 0 | 0 | 164 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 164 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jb` | 0 | 0 | 50 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 50 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jbe` | 0 | 0 | 126 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 126 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `je` | 0 | 0 | 139 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 139 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jg` | 0 | 0 | 15 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 15 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jge` | 0 | 0 | 20 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 20 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jl` | 0 | 0 | 155 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 155 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jle` | 0 | 0 | 29 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 29 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jmp` | 0 | 0 | 0 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | an unconditional transfer: it produces no ledger row of any kind, because the ledger records one row per value produced and this opcode produces none; the reference registers it with no builder -- 'a transfer or trap, and this reference walks a body in text order' |
| `jne` | 0 | 0 | 34 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 34 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jns` | 0 | 0 | 1 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 1 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `jo` | 0 | 0 | 37 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 37 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `js` | 0 | 0 | 425 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | a flag-reading transfer: the ledger records it as the reading half of a GUARD-block flag pair, 425 rows, and it writes 'the branch condition the walk forks on' rather than a value |
| `lea` | 4 | 0 | 0 | 779 | 0 | a value cell on a TRANSLATED row |  |
| `mov` | 9 | 0 | 0 | 18402 | 0 | a value cell on a TRANSLATED row |  |
| `movabs` | 1 | 0 | 0 | 14 | 0 | a value cell on a TRANSLATED row |  |
| `movapd` | 1 | 0 | 0 | 230 | 0 | a value cell on a TRANSLATED row |  |
| `movaps` | 2 | 0 | 0 | 1922 | 0 | a value cell on a TRANSLATED row |  |
| `movb` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 15 times (unique_opcodes.json) |
| `movd` | 2 | 0 | 0 | 3073 | 0 | a value cell on a TRANSLATED row |  |
| `movdqa` | 1 | 0 | 0 | 28 | 0 | a value cell on a TRANSLATED row |  |
| `movq` | 2 | 0 | 0 | 452 | 0 | a value cell on a TRANSLATED row |  |
| `movsbl` | 1 | 0 | 0 | 12 | 0 | a value cell on a TRANSLATED row |  |
| `movsbq` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `movsd` | 1 | 0 | 0 | 58 | 0 | a value cell on a TRANSLATED row |  |
| `movslq` | 1 | 0 | 0 | 3728 | 0 | a value cell on a TRANSLATED row |  |
| `movss` | 1 | 0 | 0 | 1281 | 0 | a value cell on a TRANSLATED row |  |
| `movswl` | 1 | 0 | 0 | 22 | 0 | a value cell on a TRANSLATED row |  |
| `movzbl` | 3 | 0 | 0 | 2009 | 0 | a value cell on a TRANSLATED row |  |
| `movzwl` | 2 | 0 | 0 | 67 | 0 | a value cell on a TRANSLATED row |  |
| `mul` | 4 | 0 | 0 | 320 | 0 | a value cell on a TRANSLATED row |  |
| `mulsd` | 2 | 0 | 0 | 124 | 0 | a value cell on a TRANSLATED row |  |
| `mulss` | 2 | 0 | 0 | 301 | 0 | a value cell on a TRANSLATED row |  |
| `neg` | 4 | 0 | 0 | 211 | 0 | a value cell on a TRANSLATED row |  |
| `nop` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 150 times (unique_opcodes.json) |
| `nopl` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 34 times (unique_opcodes.json) |
| `not` | 3 | 0 | 0 | 220 | 0 | a value cell on a TRANSLATED row |  |
| `or` | 6 | 0 | 0 | 7604 | 0 | a value cell on a TRANSLATED row |  |
| `orpd` | 1 | 0 | 0 | 6 | 0 | a value cell on a TRANSLATED row |  |
| `orps` | 1 | 0 | 0 | 6 | 0 | a value cell on a TRANSLATED row |  |
| `pand` | 1 | 0 | 0 | 2 | 0 | a value cell on a TRANSLATED row |  |
| `pcmpeqb` | 0 | 2 | 0 | 4 | 0 | attested at a form the sweep does not spell | the reference registers it with no builder -- 'no z3 term is written for this arch opcode yet' -- so the sweep states one NO_BUILDER row for it and no row at any shape; the corpus spells it at shape 'mem_xmm' |
| `pcmpeqd` | 0 | 1 | 0 | 2 | 0 | attested at a form the sweep does not spell | the reference registers it with no builder -- 'no z3 term is written for this arch opcode yet' -- so the sweep states one NO_BUILDER row for it and no row at any shape; the corpus spells it at shape 'xmm_same' |
| `pextrw` | 1 | 0 | 0 | 2317 | 0 | a value cell on a TRANSLATED row |  |
| `pmovmskb` | 0 | 1 | 0 | 2 | 0 | attested at a form the sweep does not spell | the reference registers it with no builder -- 'no z3 term is written for this arch opcode yet' -- so the sweep states one NO_BUILDER row for it and no row at any shape; the corpus spells it at shape 'xmm_gpr' |
| `pop` | 0 | 0 | 0 | 0 | 0 | never placed | no ledger row of the corpus names it as a producer, so the classifier never saw a line of it; the corpus's own body lines spell it 3348 times (unique_opcodes.json) |
| `punpckldq` | 1 | 0 | 0 | 132 | 0 | a value cell on a TRANSLATED row |  |
| `punpcklqdq` | 1 | 0 | 0 | 4 | 0 | a value cell on a TRANSLATED row |  |
| `push` | 1 | 0 | 0 | 3408 | 0 | a value cell on a TRANSLATED row |  |
| `pxor` | 3 | 0 | 0 | 42 | 0 | a value cell on a TRANSLATED row |  |
| `ret` | 0 | 0 | 0 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | an unconditional transfer: it produces no ledger row of any kind, because the ledger records one row per value produced and this opcode produces none |
| `sar` | 6 | 0 | 0 | 2182 | 0 | a value cell on a TRANSLATED row |  |
| `sbb` | 5 | 0 | 0 | 2596 | 0 | a value cell on a TRANSLATED row |  |
| `seta` | 1 | 0 | 0 | 1407 | 1407 | a value cell on a TRANSLATED row |  |
| `setae` | 1 | 0 | 0 | 1552 | 1552 | a value cell on a TRANSLATED row |  |
| `setb` | 1 | 0 | 0 | 499 | 499 | a value cell on a TRANSLATED row |  |
| `setbe` | 1 | 0 | 0 | 314 | 314 | a value cell on a TRANSLATED row |  |
| `sete` | 1 | 0 | 0 | 1339 | 1339 | a value cell on a TRANSLATED row |  |
| `setg` | 1 | 0 | 0 | 872 | 872 | a value cell on a TRANSLATED row |  |
| `setge` | 1 | 0 | 0 | 675 | 675 | a value cell on a TRANSLATED row |  |
| `setl` | 1 | 0 | 0 | 984 | 984 | a value cell on a TRANSLATED row |  |
| `setle` | 1 | 0 | 0 | 643 | 643 | a value cell on a TRANSLATED row |  |
| `setne` | 1 | 0 | 0 | 10335 | 10335 | a value cell on a TRANSLATED row |  |
| `setnp` | 1 | 0 | 0 | 108 | 108 | a value cell on a TRANSLATED row |  |
| `setns` | 1 | 0 | 0 | 176 | 176 | a value cell on a TRANSLATED row |  |
| `seto` | 1 | 0 | 0 | 4 | 4 | a value cell on a TRANSLATED row |  |
| `setp` | 1 | 0 | 0 | 2125 | 2125 | a value cell on a TRANSLATED row |  |
| `sets` | 1 | 0 | 0 | 264 | 264 | a value cell on a TRANSLATED row |  |
| `shl` | 5 | 0 | 0 | 3666 | 0 | a value cell on a TRANSLATED row |  |
| `shld` | 1 | 0 | 0 | 142 | 0 | a value cell on a TRANSLATED row |  |
| `shr` | 6 | 0 | 0 | 963 | 0 | a value cell on a TRANSLATED row |  |
| `shrd` | 1 | 0 | 0 | 142 | 0 | a value cell on a TRANSLATED row |  |
| `sub` | 5 | 0 | 0 | 1191 | 0 | a value cell on a TRANSLATED row |  |
| `subpd` | 1 | 0 | 0 | 132 | 0 | a value cell on a TRANSLATED row |  |
| `subsd` | 2 | 0 | 0 | 124 | 0 | a value cell on a TRANSLATED row |  |
| `subss` | 2 | 0 | 0 | 295 | 0 | a value cell on a TRANSLATED row |  |
| `test` | 8 | 0 | 0 | 7756 | 0 | a value cell on a TRANSLATED row |  |
| `ucomisd` | 2 | 0 | 0 | 1050 | 0 | a value cell on a TRANSLATED row |  |
| `ucomiss` | 2 | 0 | 0 | 2612 | 0 | a value cell on a TRANSLATED row |  |
| `ud2` | 0 | 0 | 0 | 0 | 0 | a control transfer -- attested by guard rows and never by a value cell | an unconditional transfer: it produces no ledger row of any kind, because the ledger records one row per value produced and this opcode produces none; the reference registers it with no builder -- 'a transfer or trap, and this reference walks a body in text order' |
| `unpckhpd` | 1 | 0 | 0 | 132 | 0 | a value cell on a TRANSLATED row |  |
| `xor` | 6 | 0 | 0 | 7497 | 0 | a value cell on a TRANSLATED row |  |
| `xorpd` | 1 | 0 | 0 | 378 | 0 | a value cell on a TRANSLATED row |  |
| `xorps` | 2 | 0 | 0 | 3034 | 0 | a value cell on a TRANSLATED row |  |

## 9. The control transfers, and the guard rows that attest them

A conditional transfer writes no value: the reference's entry for it writes 'the branch condition the walk forks on', the fork the walk takes. So it can carry no value cell by nature, and the ledger attests it in a different population -- the GUARD block, where the producer is the PAIR (flag-setting opcode, flag-reading opcode) and this mnemonic is the reading half. An UNCONDITIONAL transfer produces no ledger row of any kind, and its count is 0 by nature rather than by omission.

Table 11 — the guard rows, per branch mnemonic, with the flag-setting mnemonics whose flags it read.

| mnem | guard rows | units | an example line | the setters, with their row counts |
|---|---|---|---|---|
| `ja` | 6 | 6 | `ja L1` | `cmp` 6 |
| `jae` | 164 | 116 | `jae L0` | `cmp` 153 `sbb` 11 |
| `jb` | 50 | 50 | `jb L0` | `cmp` 22 `add` 6 `sub` 6 `ucomiss` 6 `sbb` 5 `ucomisd` 4 `adc` 1 |
| `jbe` | 126 | 126 | `jbe L0` | `cmp` 126 |
| `je` | 139 | 96 | `je L2` | `test` 80 `or` 22 `cmp` 22 `shr` 12 `sar` 3 |
| `jg` | 15 | 15 | `jg L1` | `cmp` 15 |
| `jge` | 20 | 20 | `jge L2` | `cmp` 15 `sbb` 5 |
| `jl` | 155 | 154 | `jl L0` | `test` 122 `cmp` 23 `sbb` 10 |
| `jle` | 29 | 29 | `jle L3` | `cmp` 29 |
| `jne` | 34 | 32 | `jne L0` | `cmp` 29 `or` 3 `test` 2 |
| `jns` | 1 | 1 | `jns L1` | `test` 1 |
| `jo` | 37 | 37 | `jo L0` | `imul` 7 `neg` 7 `add` 7 `sub` 7 `mul` 6 `sbb` 2 `adc` 1 |
| `js` | 425 | 425 | `js L0` | `test` 424 `xor` 1 |

