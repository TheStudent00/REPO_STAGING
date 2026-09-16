// arch-unit 141  --  c  `a == b`  lhs=float rhs=bool
// symbol op_485   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_141_c_eq_f32_bool(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // a0: operand `b` (bool) zero-extended
    let v2: u64 = ((p1) & 0x1u64);
    let v3: u64 = sfemul::ui32_to_f32::ui32_to_f32_rm0(((v2) as u32));
    let v4: u64 = b2u(sfemul::f32_eq::f32_eq_rm0(v1, v3));
    v4
}
