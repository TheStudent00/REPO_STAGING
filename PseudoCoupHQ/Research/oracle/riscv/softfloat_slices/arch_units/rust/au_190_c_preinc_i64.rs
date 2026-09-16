// arch-unit 190  --  c  `++a`  lhs=int64_t rhs=None
// symbol op_37   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi a0, 0x1                       integer    operator:+
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_190_c_preinc_i64(p0: u64) -> u64 {
    // a0: operand `a` (int64_t) arrives in a0
    let v1: u64 = p0;
    let v2: u64 = au_add(v1, 0x1u64);
    // the answer is int64_t, 64 bits
    v2
}
