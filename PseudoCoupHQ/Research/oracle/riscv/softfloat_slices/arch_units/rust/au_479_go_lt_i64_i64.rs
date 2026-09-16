// arch-unit 479  --  go  `a < b`  lhs=int64 rhs=int64
// symbol main.op_535   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt a0, a0, a1                       integer    operator:< signed
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_479_go_lt_i64_i64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (int64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_slt(v1, v2);
    // the answer is bool, 1 bits
    ((v3) & 0x1u64)
}
