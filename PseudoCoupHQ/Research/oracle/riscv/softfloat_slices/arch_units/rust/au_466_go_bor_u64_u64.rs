// arch-unit 466  --  go  `a | b`  lhs=uint64 rhs=uint64
// symbol main.op_398   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_466_go_bor_u64_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (uint64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_or(v1, v2);
    // the answer is uint64, 64 bits
    v3
}
