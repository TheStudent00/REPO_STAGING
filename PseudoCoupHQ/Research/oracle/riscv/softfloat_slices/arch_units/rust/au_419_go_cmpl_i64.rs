// arch-unit 419  --  go  `^a`  lhs=int64 rhs=None
// symbol main.op_19   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, -0x1                    integer    operator:^
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_419_go_cmpl_i64(p0: u64) -> u64 {
    // a0: operand `a` (int64) arrives in a0
    let v1: u64 = p0;
    let v2: u64 = au_xor(v1, 0xffffffffffffffffu64);
    // the answer is int64, 64 bits
    v2
}
