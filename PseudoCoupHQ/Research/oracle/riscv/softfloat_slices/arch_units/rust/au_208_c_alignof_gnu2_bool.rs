// arch-unit 208  --  c  `__alignof__ a`  lhs=bool rhs=None
// symbol op_59   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x1                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_208_c_alignof_gnu2_bool(p0: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    let v2: u64 = 0x1u64;
    // the answer is uint64_t, 64 bits
    v2
}
