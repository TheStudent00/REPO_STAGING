// arch-unit 178  --  c  `-a`  lhs=int32_t rhs=None
// symbol op_12   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   subw a0, zero, a0                    integer    operator:- then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_178_c_neg_i32(p0: u64) -> u64 {
    // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    let v2: u64 = au_subw(0x0u64, v1);
    // the answer is int32_t, 32 bits
    ((v2) & 0xffffffffu64)
}
