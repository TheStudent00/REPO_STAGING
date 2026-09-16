// arch-unit 416  --  go  `-a`  lhs=uint64 rhs=None
// symbol main.op_8   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: uint64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_416_go_neg_u64(p0: u64) -> u64 {
    // a0: operand `a` (uint64) arrives in a0
    let v1: u64 = p0;
    let v2: u64 = au_sub(0x0u64, v1);
    // the answer is uint64, 64 bits
    v2
}
