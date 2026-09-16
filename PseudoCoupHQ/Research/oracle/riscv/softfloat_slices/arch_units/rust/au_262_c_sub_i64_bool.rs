// arch-unit 262  --  c  `a - b`  lhs=int64_t rhs=bool
// symbol op_149   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_262_c_sub_i64_bool(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64_t) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (bool) zero-extended to XLEN
    let v2: u64 = ((p1) & 0x1u64);
    let v3: u64 = au_sub(v1, v2);
    // the answer is int64_t, 64 bits
    v3
}
