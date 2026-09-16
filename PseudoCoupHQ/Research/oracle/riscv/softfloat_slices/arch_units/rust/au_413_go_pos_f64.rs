// arch-unit 413  --  go  `+a`  lhs=float64 rhs=None
// symbol main.op_4   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: float64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_413_go_pos_f64(p0: u64) -> u64 {
    // fa0: operand `a` (float64) arrives in fa0 as a bit pattern
    let v1: u64 = p0;
    // the answer is float64, 64 bits
    v1
}
