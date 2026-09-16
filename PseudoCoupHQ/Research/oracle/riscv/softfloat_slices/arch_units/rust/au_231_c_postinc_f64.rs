// arch-unit 231  --  c  `a++`  lhs=double rhs=None
// symbol op_94   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: double, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_231_c_postinc_f64(p0: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0 as a bit pattern
    let v1: u64 = p0;
    // the answer is double, 64 bits
    v1
}
