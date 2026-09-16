// arch-unit 484  --  go  `a > b`  lhs=int32 rhs=int32
// symbol main.op_600   outcome LIFTED   4 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   addiw t0, a1, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   addiw t1, a0, 0x0                    integer    operator:+ then sign-extend the low 32 bits
//   slt a0, t0, t1                       integer    operator:< signed
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_484_go_gt_i32_i32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
    let v2: u64 = au_sext32(p1);
    let v3: u64 = au_addw(v2, 0x0u64);
    let v4: u64 = au_addw(v1, 0x0u64);
    let v5: u64 = au_slt(v3, v4);
    // the answer is bool, 1 bits
    ((v5) & 0x1u64)
}
