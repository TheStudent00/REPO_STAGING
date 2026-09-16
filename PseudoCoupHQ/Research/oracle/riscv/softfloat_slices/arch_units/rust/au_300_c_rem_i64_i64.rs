// arch-unit 300  --  c  `a % b`  lhs=int64_t rhs=int64_t
// symbol op_253   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   rem a0, a0, a1                       integer    written-out restoring division (NOT the language's %)
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_300_c_rem_i64_i64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64_t) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (int64_t) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_rem(v1, v2);
    // the answer is int64_t, 64 bits
    v3
}
