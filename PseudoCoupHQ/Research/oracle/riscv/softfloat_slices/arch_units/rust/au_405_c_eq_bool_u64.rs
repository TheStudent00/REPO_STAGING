// arch-unit 405  --  c  `a == b`  lhs=bool rhs=uint64_t
// symbol op_494   outcome LIFTED   3 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.xor a0, a1                         integer    operator:^
//   sltiu a0, a0, 0x1                    integer    operator:< unsigned
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_405_c_eq_bool_u64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    // a1: operand `b` (uint64_t) arrives in a1
    let v2: u64 = p1;
    let v3: u64 = au_xor(v1, v2);
    let v4: u64 = au_sltu(v3, 0x1u64);
    // the answer is int32_t, 32 bits
    ((v4) & 0xffffffffu64)
}
