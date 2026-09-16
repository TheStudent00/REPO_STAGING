// arch-unit 436  --  go  `a << b`  lhs=int32 rhs=uint64
// symbol main.op_170   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sll t0, a0, a1                       integer    operator:<< (count masked to 6 bits)
//   sltiu t1, a1, 0x40                   integer    operator:< unsigned
//   sub t1, zero, t1                     integer    operator:-
//   and a0, t0, t1                       integer    operator:&
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_436_go_shl_i32_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    // a1: operand `b` (uint64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_sll(v1, v2);
    let v4: u64 = au_sltu(v2, 0x40u64);
    let v5: u64 = au_sub(0x0u64, v4);
    let v6: u64 = au_and(v3, v5);
    // the answer is int32, 32 bits
    ((v6) & 0xffffffffu64)
}
