// arch-unit 251  --  c  `a + b`  lhs=bool rhs=int32_t
// symbol op_132   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addw a0, a1                        integer    operator:+ then sign-extend the low 32 bits
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::au_int::*;

pub fn au_251_c_add_bool_i32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended to XLEN
    let v1: u64 = ((p0) & 0x1u64);
    // a1: operand `b` (int32_t) sign-extended to XLEN, as the ABI presents it
    let v2: u64 = au_sext32(p1);
    let v3: u64 = au_addw(v1, v2);
    // the answer is int32_t, 32 bits
    ((v3) & 0xffffffffu64)
}
