// arch-unit 67  --  c  `a * b`  lhs=double rhs=bool
// symbol op_203   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fmul.d fa0, fa0, fa5, dyn          float    emulation:f64_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_067_c_mul_f64_bool(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    // a0: operand `b` (bool) zero-extended
    let v2: u64 = ((p1) & 0x1u64);
    let v3: u64 = sfemul::ui32_to_f64::ui32_to_f64_rm0(((v2) as u32));
    let v4: u64 = sfemul::f64_mul::f64_mul_rm0(v1, v3);
    v4
}
