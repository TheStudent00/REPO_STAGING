// arch-unit 420  --  go  `^a`  lhs=uint64 rhs=None
// symbol main.op_20   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori a0, a0, -0x1                    integer    operator:^
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_420_go_cmpl_u64(p0: u64) -> u64 {
    // a0: operand `a` (uint64) arrives in a0
    let v1: u64 = p0;
    let v2: u64 = au_xor(v1, 0xffffffffffffffffu64);
    // the answer is uint64, 64 bits
    v2
}
