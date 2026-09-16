// arch-unit 292  --  c  `a / b`  lhs=bool rhs=int64_t
// symbol op_241   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   div a0, a0, a1                       integer    written-out restoring division (NOT the language's /)
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_292_c_div_bool_i64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    // a1: operand `b` (int64_t) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_div(v1, v2);
    // the answer is int64_t, 64 bits
    v3
}
