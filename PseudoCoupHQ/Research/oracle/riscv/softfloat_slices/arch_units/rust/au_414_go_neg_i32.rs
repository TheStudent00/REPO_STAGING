// arch-unit 414  --  go  `-a`  lhs=int32 rhs=None
// symbol main.op_6   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sub a0, zero, a0                     integer    operator:-
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_414_go_neg_i32(p0: u64) -> u64 {
    // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    let v2: u64 = au_sub(0x0u64, v1);
    // the answer is int32, 32 bits
    ((v2) & 0xffffffffu64)
}
