// arch-unit 213  --  c  `__alignof a`  lhs=double rhs=None
// symbol op_64   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_213_c_alignof_gnu_f64(p0: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0 as a bit pattern
    let v1: u64 = p0;
    let v2: u64 = 0x8u64;
    // the answer is uint64_t, 64 bits
    v2
}
