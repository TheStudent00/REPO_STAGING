// arch-unit 411  --  go  `+a`  lhs=uint64 rhs=None
// symbol main.op_2   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_411_go_pos_u64(p0: u64) -> u64 {
    // a0: operand `a` (uint64) arrives in a0
    let v1: u64 = p0;
    // the answer is uint64, 64 bits
    v1
}
