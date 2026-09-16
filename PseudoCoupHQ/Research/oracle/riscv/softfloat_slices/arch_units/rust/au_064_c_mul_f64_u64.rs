// arch-unit 64  --  c  `a * b`  lhs=double rhs=uint64_t
// symbol op_200   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
//   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_064_c_mul_f64_u64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    // a0: operand `b` (uint64_t) arrives in a0
    let v2: u64 = p1;
    let v3: u64 = sfemul::ui64_to_f64::ui64_to_f64_rm0(v2);
    let v4: u64 = sfemul::f64_mul::f64_mul_rm0(v1, v3);
    v4
}
