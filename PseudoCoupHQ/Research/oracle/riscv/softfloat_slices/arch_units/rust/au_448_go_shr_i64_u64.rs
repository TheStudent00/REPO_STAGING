// arch-unit 448  --  go  `a >> b`  lhs=int64 rhs=uint64
// symbol main.op_212   outcome LIFTED   5 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu t0, a1, 0x40                   integer    operator:< unsigned
//   c.addi t0, -0x1                      integer    operator:+
//   or t0, a1, t0                        integer    operator:|
//   sra a0, a0, t0                       integer    arithmetic right shift, written out in unsigned bit operations
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: int64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_448_go_shr_i64_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (uint64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_sltu(v2, 0x40u64);
    let v4: u64 = au_add(v3, 0xffffffffffffffffu64);
    let v5: u64 = au_or(v2, v4);
    let v6: u64 = au_sra(v1, v5);
    // the answer is int64, 64 bits
    v6
}
