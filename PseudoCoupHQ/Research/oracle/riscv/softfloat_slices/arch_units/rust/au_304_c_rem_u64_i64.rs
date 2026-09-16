// arch-unit 304  --  c  `a % b`  lhs=uint64_t rhs=int64_t
// symbol op_259   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   remu a0, a0, a1                      integer    written-out restoring division (NOT the language's %)
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_304_c_rem_u64_i64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64_t) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (int64_t) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_remu(v1, v2);
    // the answer is uint64_t, 64 bits
    v3
}
