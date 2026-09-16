// arch-unit 142  --  c  `a == b`  lhs=double rhs=int32_t
// symbol op_486   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.w fa5, a0                   float    emulation:i32_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_142_c_eq_f64_i32(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    // a0: operand `b` (int32_t) sign-extended to XLEN
    let v2: u64 = (((p1) as u32) as i32 as i64) as u64;
    let v3: u64 = sfemul::i32_to_f64::i32_to_f64_rm0(((v2) as u32));
    let v4: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v1, v3));
    v4
}
