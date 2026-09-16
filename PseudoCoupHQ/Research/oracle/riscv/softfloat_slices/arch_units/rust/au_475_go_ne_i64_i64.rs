// arch-unit 475  --  go  `a != b`  lhs=int64 rhs=int64
// symbol main.op_499   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub t0, a0, a1                       integer    operator:-
//   sltu a0, zero, t0                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_475_go_ne_i64_i64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (int64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_sub(v1, v2);
    let v4: u64 = au_sltu(0x0u64, v3);
    // the answer is bool, 1 bits
    ((v4) & 0x1u64)
}
