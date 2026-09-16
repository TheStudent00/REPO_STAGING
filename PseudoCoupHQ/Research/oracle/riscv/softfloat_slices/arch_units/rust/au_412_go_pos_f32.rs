// arch-unit 412  --  go  `+a`  lhs=float32 rhs=None
// symbol main.op_3   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: float32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_412_go_pos_f32(p0: u64) -> u64 {
    // fa0: operand `a` (float32) arrives in fa0 as a bit pattern
    let v1: u64 = ((p0) & 0xffffffffu64);
    // the answer is float32, 32 bits
    ((v1) & 0xffffffffu64)
}
