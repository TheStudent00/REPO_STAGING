// arch-unit 29  --  c  `a + b`  lhs=bool rhs=double
// symbol op_136   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.wu fa5, a0                  float    emulation:ui32_to_f64_rm0
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_029_c_add_bool_f64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended
    let v1: u64 = ((p0) & 0x1u64);
    // fa0: operand `b` (double) arrives in fa0
    let v2: u64 = p1;
    let v3: u64 = sfemul::ui32_to_f64::ui32_to_f64_rm0(((v1) as u32));
    let v4: u64 = sfemul::f64_add::f64_add_rm0(v2, v3);
    v4
}
