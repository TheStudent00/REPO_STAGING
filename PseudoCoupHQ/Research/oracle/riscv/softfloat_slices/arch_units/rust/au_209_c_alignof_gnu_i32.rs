// arch-unit 209  --  c  `__alignof a`  lhs=int32_t rhs=None
// symbol op_60   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_209_c_alignof_gnu_i32(p0: u64) -> u64 {
    // a0: operand `a` (int32_t) sign-extended to XLEN, as the ABI presents it
    let v1: u64 = au_sext32(p0);
    let v2: u64 = 0x4u64;
    // the answer is uint64_t, 64 bits
    v2
}
