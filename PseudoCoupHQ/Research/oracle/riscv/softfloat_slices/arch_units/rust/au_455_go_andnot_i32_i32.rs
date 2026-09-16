// arch-unit 455  --  go  `a &^ b`  lhs=int32 rhs=int32
// symbol main.op_276   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   xori t6, a1, -0x1                    integer    operator:^
//   and a0, a0, t6                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_455_go_andnot_i32_i32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    // a1: operand `b` (int32) sign-extended to XLEN, as the ABI presents it
    let v2: u64 = au_sext32(p1);
    let v3: u64 = au_xor(v2, 0xffffffffffffffffu64);
    let v4: u64 = au_and(v1, v3);
    // the answer is int32, 32 bits
    ((v4) & 0xffffffffu64)
}
