// arch-unit 341  --  c  `a && b`  lhs=bool rhs=uint64_t
// symbol op_350   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a1, zero, a1                    integer    operator:< unsigned
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_341_c_land_bool_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    // a1: operand `b` (uint64_t) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_sltu(0x0u64, v2);
    let v4: u64 = au_and(v1, v3);
    // the answer is int32_t, 32 bits
    ((v4) & 0xffffffffu64)
}
