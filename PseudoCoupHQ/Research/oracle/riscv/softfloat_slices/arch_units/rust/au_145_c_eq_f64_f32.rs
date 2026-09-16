// arch-unit 145  --  c  `a == b`  lhs=double rhs=float
// symbol op_489   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa1                  float    emulation:f32_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_145_c_eq_f64_f32(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    // fa1: operand `b` (float) arrives in fa1
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = sfemul::f32_to_f64::f32_to_f64_rm0(v2);
    let v4: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v1, v3));
    v4
}
