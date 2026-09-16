// arch-unit 417  --  go  `!a`  lhs=bool rhs=None
// symbol main.op_17   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   jalr zero, 0x0(ra)                   integer    return
//
// answer: bool, 1 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_417_go_not_bool(p0: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    let v2: u64 = au_sltu(v1, 0x1u64);
    // the answer is bool, 1 bits
    ((v2) & 0x1u64)
}
