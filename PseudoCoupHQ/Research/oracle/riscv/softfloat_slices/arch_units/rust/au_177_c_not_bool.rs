// arch-unit 177  --  c  `!a`  lhs=bool rhs=None
// symbol op_5   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, 0x1                     integer    operator:^
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_177_c_not_bool(p0: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    let v2: u64 = au_xor(v1, 0x1u64);
    // the answer is int32_t, 32 bits
    ((v2) & 0xffffffffu64)
}
