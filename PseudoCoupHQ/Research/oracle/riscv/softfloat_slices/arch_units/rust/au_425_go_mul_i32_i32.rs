// arch-unit 425  --  go  `a * b`  lhs=int32 rhs=int32
// symbol main.op_60   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   mulw a0, a0, a1                      integer    operator:* then sign-extend the low 32 bits
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_425_go_mul_i32_i32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
    let v2: u64 = au_sext32(p1);
    let v3: u64 = au_mulw(v1, v2);
    // the answer is int32, 32 bits
    ((v3) & 0xffffffffu64)
}
