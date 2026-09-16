// arch-unit 140  --  c  `a == b`  lhs=float rhs=double
// symbol op_484   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
//   feq.d a0, fa1, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_140_c_eq_f32_f64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // fa1: operand `b` (double) arrives in fa1
    let v2: u64 = p1;
    let v3: u64 = sfemul::f32_to_f64::f32_to_f64_rm0(v1);
    let v4: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v2, v3));
    v4
}
