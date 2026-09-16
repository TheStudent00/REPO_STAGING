// arch-unit 218  --  c  `_Alignof a`  lhs=float rhs=None
// symbol op_81   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_218_c_alignof_c11_f32(p0: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0 as a bit pattern
    let v1: u64 = ((p0) & 0xffffffffu64);
    let v2: u64 = 0x4u64;
    // the answer is uint64_t, 64 bits
    v2
}
