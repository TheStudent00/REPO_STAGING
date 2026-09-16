// arch-unit 394  --  c  `a == b`  lhs=int32_t rhs=bool
// symbol op_467   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_394_c_eq_i32_bool(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    // a1: operand `b` (bool) zero-extended to XLEN
    let v2: u64 = ((p1) & 0x1u64);
    let v3: u64 = au_xor(v1, v2);
    let v4: u64 = au_sltu(v3, 0x1u64);
    // the answer is int32_t, 32 bits
    ((v4) & 0xffffffffu64)
}
