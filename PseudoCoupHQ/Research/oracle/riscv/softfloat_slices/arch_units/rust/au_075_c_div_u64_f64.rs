// arch-unit 75  --  c  `a / b`  lhs=uint64_t rhs=double
// symbol op_226   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
//   fdiv.d fa0, fa5, fa0, dyn          float    emulation:f64_div_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_075_c_div_u64_f64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64_t) arrives in a0
    let v1: u64 = p0;
    // fa0: operand `b` (double) arrives in fa0
    let v2: u64 = p1;
    let v3: u64 = sfemul::ui64_to_f64::ui64_to_f64_rm0(v1);
    let v4: u64 = sfemul::f64_div::f64_div_rm0(v3, v2);
    v4
}
