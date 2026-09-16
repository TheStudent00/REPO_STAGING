// arch-unit 176  --  c  `!a`  lhs=uint64_t rhs=None
// symbol op_2   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_176_c_not_u64(p0: u64) -> u64 {
    // a0: operand `a` (uint64_t) arrives in a0
    let v1: u64 = p0;
    let v2: u64 = au_sltu(v1, 0x1u64);
    // the answer is int32_t, 32 bits
    ((v2) & 0xffffffffu64)
}
