// arch-unit 426  --  go  `a * b`  lhs=int64 rhs=int64
// symbol main.op_67   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   mul a0, a0, a1                       integer    operator:*
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_426_go_mul_i64_i64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (int64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_mul(v1, v2);
    // the answer is int64, 64 bits
    v3
}
