// arch-unit 236  --  c  `a--`  lhs=float rhs=None
// symbol op_99   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: float, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_236_c_postdec_f32(p0: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0 as a bit pattern
    let v1: u64 = ((p0) & 0xffffffffu64);
    // the answer is float, 32 bits
    ((v1) & 0xffffffffu64)
}
