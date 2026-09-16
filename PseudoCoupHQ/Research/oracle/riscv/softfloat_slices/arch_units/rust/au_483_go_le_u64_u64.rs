// arch-unit 483  --  go  `a <= b`  lhs=uint64 rhs=uint64
// symbol main.op_578   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu t0, a1, a0                      integer    operator:< unsigned
//   sltiu a0, t0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_483_go_le_u64_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64) arrives in a0
    let v1: u64 = p0;
    // a1: operand `b` (uint64) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_sltu(v2, v1);
    let v4: u64 = au_sltu(v3, 0x1u64);
    // the answer is bool, 1 bits
    ((v4) & 0x1u64)
}
