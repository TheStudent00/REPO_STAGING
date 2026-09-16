// arch-unit 135  --  c  `a == b`  lhs=uint64_t rhs=double
// symbol op_478   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.lu fa5, a0, dyn             float    emulation:ui64_to_f64_rm0
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_135_c_eq_u64_f64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64_t) arrives in a0
    let v1: u64 = p0;
    // fa0: operand `b` (double) arrives in fa0
    let v2: u64 = p1;
    let v3: u64 = sfemul::ui64_to_f64::ui64_to_f64_rm0(v1);
    let v4: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v2, v3));
    v4
}
