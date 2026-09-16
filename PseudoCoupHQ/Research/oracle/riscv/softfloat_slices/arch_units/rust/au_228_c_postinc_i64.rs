// arch-unit 228  --  c  `a++`  lhs=int64_t rhs=None
// symbol op_91   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_228_c_postinc_i64(p0: u64) -> u64 {
    // a0: operand `a` (int64_t) arrives in a0
    let v1: u64 = p0;
    // the answer is int64_t, 64 bits
    v1
}
