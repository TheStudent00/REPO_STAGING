// arch-unit 349  --  c  `a | b`  lhs=int64_t rhs=uint64_t
// symbol op_362   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_349_c_bor_i64_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64_t) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (uint64_t) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_or(v1, v2);
    // the answer is uint64_t, 64 bits
    v3
}
