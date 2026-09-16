// arch-unit 80  --  c  `a / b`  lhs=float rhs=double
// symbol op_232   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
//   fdiv.d fa0, fa5, fa1, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_080_c_div_f32_f64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // fa1: operand `b` (double) arrives in fa1
    let v2: u64 = p1;
    let v3: u64 = sfemul::f32_to_f64::f32_to_f64_rm0(v1);
    let v4: u64 = sfemul::f64_div::f64_div_rm0(v3, v2);
    v4
}
