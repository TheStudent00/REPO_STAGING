# twins.md -- the RISC-V model table's cells matched to x86's, by TERM

Task rv2, node `hq.research.arch_unit_oracle`. Written by `twins.py`; never hand-edited.

**What this is, one sentence.** For every RISC-V cell of `model_table_rv.json`, the x86 cell of `model_table_rows.json` whose place term is the same function -- identical after `term.Term.normalize` (a TEXT twin) or proved equal by z3 (a Z3 twin) -- so a certificate proved about the x86 cell can be inherited on riscv64.

**THE HEADLINE CARRIES ITS READING, and there are two.** READING 1 is the WHOLE WRITTEN PLACE: RISC-V always writes all 64 bits of a register and its 32-bit forms SIGN-extend, where x86's 32-bit write ZERO-extends, so at the whole place a `w` form can never twin an x86 32-bit form. READING 2 cuts both sides to the RISC-V cell's own `key_width`, the width the operation computes at and the width the gate compares an emulation on. Neither replaces the other.

Table 1 -- the two readings, side by side.

| twin | reading 1: the whole written place | reading 2: at the cell's own `key_width` |
|---|---|---|
| TEXT | 101 | 158 |
| Z3 | 1 | 3 |
| NONE | 153 | 94 |
| **total RISC-V cells** | **255** | **255** |

Table 2 -- the x86 side, as it was read.

| what | value |
|---|---|
| the x86 reference imported | `PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals/reference.py` |
| its sha256 | `3893363145df57944286222c18756465757d4e69a6eea0783e0f03265b7156e0` |
| distinct x86 cells | 5912 |
| distinct x86 place terms | 679 |
| place rows where the re-run reproduced the table's own recorded text | 8403 |
| place rows where it differed | 0 |
| solver calls | 1041 |
| seconds | 343.5 |

Table 3 -- every RISC-V cell, its twin and how it was found.

| `mnem` | shape | `key_width` | reading 1 | reading 2 | x86 twin `mnem` | x86 twin shape | x86 twin `key_width` | x86 twin place |
|---|---|---|---|---|---|---|---|---|
| `add` | gpr_gpr_gpr | 64 | TEXT | TEXT | `add` | cl_gpr | 64 | reg_rdi |
| `add` | gpr_gpr_same | 64 | TEXT | TEXT | `add` | gpr_same | 64 | reg_rdi |
| `addi` | gpr_gpr_imm | 64 | TEXT | TEXT | `add` | imm_gpr | 64 | reg_rdi |
| `addiw` | gpr_gpr_imm | 32 | NONE | TEXT | `add` | imm_gpr | 32 | reg_rdi |
| `addw` | gpr_gpr_gpr | 32 | NONE | TEXT | `add` | cl_gpr | 32 | reg_rdi |
| `addw` | gpr_gpr_same | 32 | NONE | TEXT | `add` | gpr_same | 32 | reg_rdi |
| `and` | gpr_gpr_gpr | 64 | TEXT | TEXT | `and` | cl_gpr | 64 | reg_rdi |
| `and` | gpr_gpr_same | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `andi` | gpr_gpr_imm | 64 | TEXT | TEXT | `and` | imm_gpr | 8 | reg_rdi |
| `auipc` | gpr_imm | 32 | NONE | NONE | - | - | - | - |
| `beq` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `beq` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `beq` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `beq` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bge` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bge` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `bge` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `bge` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bgeu` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bgeu` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `bgeu` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `bgeu` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `blt` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `blt` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `blt` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `blt` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bltu` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bltu` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `bltu` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `bltu` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bne` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `bne` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `bne` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `bne` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `czero.eqz` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `czero.eqz` | gpr_gpr_same | 64 | Z3 | Z3 | `and` | gpr_same | 64 | reg_rdi |
| `czero.nez` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `czero.nez` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `div` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `div` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `divu` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `divu` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `divuw` | gpr_gpr_gpr | 32 | NONE | NONE | - | - | - | - |
| `divuw` | gpr_gpr_same | 32 | NONE | NONE | - | - | - | - |
| `divw` | gpr_gpr_gpr | 32 | NONE | NONE | - | - | - | - |
| `divw` | gpr_gpr_same | 32 | NONE | NONE | - | - | - | - |
| `fadd.d` | fpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `fadd.s` | fpr_fpr_fpr | 32 | NONE | TEXT | `addss` | gpr_mem | 32 | mem__rax_ |
| `fcvt.d.l` | fpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `fcvt.d.lu` | fpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `fcvt.d.s` | fpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `fcvt.d.s` | fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `fcvt.d.w` | fpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `fcvt.d.wu` | fpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `fcvt.s.d` | fpr_fpr_fpr | 32 | NONE | NONE | - | - | - | - |
| `fcvt.s.d` | fpr_fpr | 32 | NONE | NONE | - | - | - | - |
| `fcvt.s.l` | fpr_gpr | 32 | NONE | TEXT | `cvtsi2ss` | xmm_mem | 32 | mem__rax_ |
| `fcvt.s.lu` | fpr_gpr | 32 | NONE | NONE | - | - | - | - |
| `fcvt.s.w` | fpr_gpr | 32 | NONE | NONE | - | - | - | - |
| `fcvt.s.wu` | fpr_gpr | 32 | NONE | NONE | - | - | - | - |
| `fdiv.d` | fpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `fdiv.s` | fpr_fpr_fpr | 32 | NONE | TEXT | `divss` | gpr_mem | 32 | mem__rax_ |
| `feq.d` | gpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `feq.s` | gpr_fpr_fpr | 32 | NONE | NONE | - | - | - | - |
| `fld` | fpr_fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fld` | fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fld` | fpr_gpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fld` | fpr_mem | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fle.d` | gpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `fle.s` | gpr_fpr_fpr | 32 | NONE | NONE | - | - | - | - |
| `flt.d` | gpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `flt.s` | gpr_fpr_fpr | 32 | NONE | NONE | - | - | - | - |
| `flw` | fpr_fpr_fpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `flw` | fpr_fpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `flw` | fpr_gpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `flw` | fpr_mem | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `fmul.d` | fpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `fmul.s` | fpr_fpr_fpr | 32 | NONE | TEXT | `mulss` | gpr_mem | 32 | mem__rax_ |
| `fmv.d` | fpr_fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fmv.d` | fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fmv.d.x` | fpr_gpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fmv.s` | fpr_fpr_fpr | 32 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fmv.s` | fpr_fpr | 32 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fmv.w.x` | fpr_gpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `fmv.x.d` | gpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fmv.x.d` | gpr_fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fmv.x.w` | gpr_fpr | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `fmv.x.w` | gpr_fpr_fpr | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `fsd` | fpr_fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fsd` | fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fsd` | fpr_gpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fsd` | fpr_mem | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `fsub.d` | fpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `fsub.s` | fpr_fpr_fpr | 32 | NONE | TEXT | `subss` | gpr_mem | 32 | mem__rax_ |
| `fsw` | fpr_fpr_fpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `fsw` | fpr_fpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `fsw` | fpr_gpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `fsw` | fpr_mem | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `jal` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `jal` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `jal` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `jal` | gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `jal` | gpr_mem | 64 | NONE | NONE | - | - | - | - |
| `jal` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `jal` | gpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `jal` | gpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_mem | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `jalr` | gpr_fpr_fpr | 64 | NONE | NONE | - | - | - | - |
| `lb` | gpr_gpr_gpr | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lb` | gpr_gpr_same | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lb` | gpr_gpr_imm | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lb` | gpr_imm | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lb` | gpr_mem | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lb` | gpr_gpr | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lb` | gpr_fpr | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lb` | gpr_fpr_fpr | 8 | TEXT | TEXT | `movsbq` | cl_gpr | 64 | reg_rdi |
| `lbu` | gpr_gpr_gpr | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `lbu` | gpr_gpr_same | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `lbu` | gpr_gpr_imm | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `lbu` | gpr_imm | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `lbu` | gpr_mem | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `lbu` | gpr_gpr | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `lbu` | gpr_fpr | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `lbu` | gpr_fpr_fpr | 8 | TEXT | TEXT | `and` | gpr_same | 8 | reg_rdi |
| `ld` | gpr_gpr_gpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ld` | gpr_gpr_same | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ld` | gpr_gpr_imm | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ld` | gpr_imm | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ld` | gpr_mem | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ld` | gpr_gpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ld` | gpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ld` | gpr_fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `lh` | gpr_gpr_gpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lh` | gpr_gpr_same | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lh` | gpr_gpr_imm | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lh` | gpr_imm | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lh` | gpr_mem | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lh` | gpr_gpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lh` | gpr_fpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lh` | gpr_fpr_fpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `lhu` | gpr_gpr_gpr | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lhu` | gpr_gpr_same | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lhu` | gpr_gpr_imm | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lhu` | gpr_imm | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lhu` | gpr_mem | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lhu` | gpr_gpr | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lhu` | gpr_fpr | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lhu` | gpr_fpr_fpr | 16 | TEXT | TEXT | `and` | gpr_same | 16 | reg_rdi |
| `lui` | gpr_imm | 32 | NONE | NONE | - | - | - | - |
| `lw` | gpr_gpr_gpr | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lw` | gpr_gpr_same | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lw` | gpr_gpr_imm | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lw` | gpr_imm | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lw` | gpr_mem | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lw` | gpr_gpr | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lw` | gpr_fpr | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lw` | gpr_fpr_fpr | 32 | TEXT | TEXT | `movslq` | cl_gpr | 64 | reg_rdi |
| `lwu` | gpr_gpr_gpr | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `lwu` | gpr_gpr_same | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `lwu` | gpr_gpr_imm | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `lwu` | gpr_imm | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `lwu` | gpr_mem | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `lwu` | gpr_gpr | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `lwu` | gpr_fpr | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `lwu` | gpr_fpr_fpr | 32 | TEXT | TEXT | `and` | gpr_same | 32 | reg_rdi |
| `mul` | gpr_gpr_gpr | 64 | TEXT | TEXT | `imul` | cl_gpr | 64 | reg_rdi |
| `mul` | gpr_gpr_same | 64 | TEXT | TEXT | `imul` | gpr_same | 64 | reg_rdi |
| `mulh` | gpr_gpr_gpr | 64 | TEXT | TEXT | `imul` | gpr_one | 64 | reg_rdx |
| `mulh` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `mulhsu` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `mulhsu` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `mulhu` | gpr_gpr_gpr | 64 | TEXT | TEXT | `mul` | gpr_gpr | 64 | reg_rdx |
| `mulhu` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `mulw` | gpr_gpr_gpr | 32 | NONE | TEXT | `imul` | cl_gpr | 32 | reg_rdi |
| `mulw` | gpr_gpr_same | 32 | NONE | TEXT | `imul` | gpr_same | 32 | reg_rdi |
| `or` | gpr_gpr_gpr | 64 | TEXT | TEXT | `or` | cl_gpr | 64 | reg_rdi |
| `or` | gpr_gpr_same | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `ori` | gpr_gpr_imm | 64 | TEXT | TEXT | `or` | imm_gpr | 64 | reg_rdi |
| `rem` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `rem` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `remu` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `remu` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `remuw` | gpr_gpr_gpr | 32 | NONE | NONE | - | - | - | - |
| `remuw` | gpr_gpr_same | 32 | NONE | Z3 | `cvtsi2sd` | gpr_mem | 64 | mem__rax_ |
| `remw` | gpr_gpr_gpr | 32 | NONE | NONE | - | - | - | - |
| `remw` | gpr_gpr_same | 32 | NONE | Z3 | `cvtsi2sd` | gpr_mem | 64 | mem__rax_ |
| `sb` | gpr_gpr_gpr | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sb` | gpr_gpr_same | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sb` | gpr_gpr_imm | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sb` | gpr_imm | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sb` | gpr_mem | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sb` | gpr_gpr | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sb` | gpr_fpr | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sb` | gpr_fpr_fpr | 8 | NONE | TEXT | `adc` | cl_gpr | 8 | flags |
| `sd` | gpr_gpr_gpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sd` | gpr_gpr_same | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sd` | gpr_gpr_imm | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sd` | gpr_imm | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sd` | gpr_mem | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sd` | gpr_gpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sd` | gpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sd` | gpr_fpr_fpr | 64 | TEXT | TEXT | `and` | gpr_same | 64 | reg_rdi |
| `sh` | gpr_gpr_gpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sh` | gpr_gpr_same | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sh` | gpr_gpr_imm | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sh` | gpr_imm | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sh` | gpr_mem | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sh` | gpr_gpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sh` | gpr_fpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sh` | gpr_fpr_fpr | 16 | NONE | TEXT | `adc` | cl_gpr | 16 | flags |
| `sll` | gpr_gpr_gpr | 64 | TEXT | TEXT | `shl` | cl_gpr | 64 | reg_rdi |
| `sll` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `slli` | gpr_gpr_imm | 64 | TEXT | TEXT | `shl` | imm_gpr | 64 | reg_rdi |
| `slliw` | gpr_gpr_imm | 32 | NONE | TEXT | `shl` | imm_gpr | 32 | reg_rdi |
| `sllw` | gpr_gpr_gpr | 32 | NONE | TEXT | `shl` | cl_gpr | 32 | reg_rdi |
| `sllw` | gpr_gpr_same | 32 | NONE | NONE | - | - | - | - |
| `slt` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `slt` | gpr_gpr_same | 64 | TEXT | TEXT | `fldz` | cl_gpr | 80 | x87_7 |
| `slti` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `sltiu` | gpr_gpr_imm | 64 | NONE | NONE | - | - | - | - |
| `sltu` | gpr_gpr_gpr | 64 | NONE | NONE | - | - | - | - |
| `sltu` | gpr_gpr_same | 64 | TEXT | TEXT | `fldz` | cl_gpr | 80 | x87_7 |
| `sra` | gpr_gpr_gpr | 64 | TEXT | TEXT | `sar` | cl_gpr | 64 | reg_rdi |
| `sra` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `srai` | gpr_gpr_imm | 64 | TEXT | TEXT | `sar` | imm_gpr | 64 | reg_rdi |
| `sraiw` | gpr_gpr_imm | 32 | NONE | TEXT | `sar` | imm_gpr | 32 | reg_rdi |
| `sraw` | gpr_gpr_gpr | 32 | NONE | TEXT | `sar` | cl_gpr | 32 | reg_rdi |
| `sraw` | gpr_gpr_same | 32 | NONE | NONE | - | - | - | - |
| `srl` | gpr_gpr_gpr | 64 | TEXT | TEXT | `shr` | cl_gpr | 64 | reg_rdi |
| `srl` | gpr_gpr_same | 64 | NONE | NONE | - | - | - | - |
| `srli` | gpr_gpr_imm | 64 | TEXT | TEXT | `shr` | imm_gpr | 64 | reg_rdi |
| `srliw` | gpr_gpr_imm | 32 | TEXT | TEXT | `shr` | imm_gpr | 32 | reg_rdi |
| `srlw` | gpr_gpr_gpr | 32 | NONE | TEXT | `shr` | cl_gpr | 32 | reg_rdi |
| `srlw` | gpr_gpr_same | 32 | NONE | NONE | - | - | - | - |
| `sub` | gpr_gpr_gpr | 64 | TEXT | TEXT | `sub` | cl_gpr | 64 | reg_rdi |
| `sub` | gpr_gpr_same | 64 | TEXT | TEXT | `fldz` | cl_gpr | 80 | x87_7 |
| `subw` | gpr_gpr_gpr | 32 | NONE | TEXT | `sub` | cl_gpr | 32 | reg_rdi |
| `subw` | gpr_gpr_same | 32 | TEXT | TEXT | `fldz` | cl_gpr | 80 | x87_7 |
| `sw` | gpr_gpr_gpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `sw` | gpr_gpr_same | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `sw` | gpr_gpr_imm | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `sw` | gpr_imm | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `sw` | gpr_mem | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `sw` | gpr_gpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `sw` | gpr_fpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `sw` | gpr_fpr_fpr | 32 | NONE | TEXT | `adc` | cl_gpr | 32 | flags |
| `xor` | gpr_gpr_gpr | 64 | TEXT | TEXT | `pxor` | mem_xmm | 128 | reg_xmm0 |
| `xor` | gpr_gpr_same | 64 | TEXT | TEXT | `fldz` | cl_gpr | 80 | x87_7 |
| `xori` | gpr_gpr_imm | 64 | TEXT | TEXT | `xor` | imm_gpr | 64 | reg_rdi |

Table 4 -- the cells with NO twin under either reading, one row per mnemonic, with how many of its shapes are untwinned.

| `mnem` | untwinned shapes |
|---|---|
| `auipc` | 1 |
| `beq` | 4 |
| `bge` | 4 |
| `bgeu` | 4 |
| `blt` | 4 |
| `bltu` | 4 |
| `bne` | 4 |
| `czero.eqz` | 1 |
| `czero.nez` | 2 |
| `div` | 2 |
| `divu` | 2 |
| `divuw` | 2 |
| `divw` | 2 |
| `fadd.d` | 1 |
| `fcvt.d.l` | 1 |
| `fcvt.d.lu` | 1 |
| `fcvt.d.s` | 2 |
| `fcvt.d.w` | 1 |
| `fcvt.d.wu` | 1 |
| `fcvt.s.d` | 2 |
| `fcvt.s.lu` | 1 |
| `fcvt.s.w` | 1 |
| `fcvt.s.wu` | 1 |
| `fdiv.d` | 1 |
| `feq.d` | 1 |
| `feq.s` | 1 |
| `fle.d` | 1 |
| `fle.s` | 1 |
| `flt.d` | 1 |
| `flt.s` | 1 |
| `fmul.d` | 1 |
| `fsub.d` | 1 |
| `jal` | 8 |
| `jalr` | 8 |
| `lui` | 1 |
| `mulh` | 1 |
| `mulhsu` | 2 |
| `mulhu` | 1 |
| `rem` | 2 |
| `remu` | 2 |
| `remuw` | 1 |
| `remw` | 1 |
| `sll` | 1 |
| `sllw` | 1 |
| `slt` | 1 |
| `slti` | 1 |
| `sltiu` | 1 |
| `sltu` | 1 |
| `sra` | 1 |
| `sraw` | 1 |
| `srl` | 1 |
| `srlw` | 1 |

