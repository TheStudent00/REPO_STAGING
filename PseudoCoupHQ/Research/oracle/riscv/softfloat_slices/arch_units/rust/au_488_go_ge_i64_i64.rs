// arch-unit 488  --  go  `a >= b`  lhs=int64 rhs=int64
// symbol main.op_643   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   slt t0, a0, a1                       integer    operator:< signed
//   sltiu a0, t0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_488_go_ge_i64_i64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (int64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_slt(v1, v2);
    let v4: u64 = au_sltu(v3, 0x1u64);
    // the answer is bool, 1 bits
    ((v4) & 0x1u64)
}
