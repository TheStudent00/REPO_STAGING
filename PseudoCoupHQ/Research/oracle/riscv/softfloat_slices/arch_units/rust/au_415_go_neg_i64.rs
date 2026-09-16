// arch-unit 415  --  go  `-a`  lhs=int64 rhs=None
// symbol main.op_7   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_415_go_neg_i64(p0: u64) -> u64 {
    // a0: operand `a` (int64) arrives in a0
    let v1: u64 = p0;
    let v2: u64 = au_sub(0x0u64, v1);
    // the answer is int64, 64 bits
    v2
}
