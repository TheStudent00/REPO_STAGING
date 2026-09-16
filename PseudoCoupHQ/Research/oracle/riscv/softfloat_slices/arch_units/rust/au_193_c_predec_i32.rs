// arch-unit 193  --  c  `--a`  lhs=int32_t rhs=None
// symbol op_42   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addiw a0, -0x1                     integer    operator:+ then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_193_c_predec_i32(p0: u64) -> u64 {
    // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    let v2: u64 = au_addw(v1, 0xffffffffffffffffu64);
    // the answer is int32_t, 32 bits
    ((v2) & 0xffffffffu64)
}
