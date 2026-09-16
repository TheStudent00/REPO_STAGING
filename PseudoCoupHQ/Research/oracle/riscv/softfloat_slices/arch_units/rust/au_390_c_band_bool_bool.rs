// arch-unit 390  --  c  `a & b`  lhs=bool rhs=bool
// symbol op_461   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_390_c_band_bool_bool(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    // a1: operand `b` (bool) zero-extended to XLEN
    let v2: u64 = ((p1) & 0x1u64);
    let v3: u64 = au_and(v1, v2);
    // the answer is int32_t, 32 bits
    ((v3) & 0xffffffffu64)
}
