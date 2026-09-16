// arch-unit 148  --  c  `a == b`  lhs=bool rhs=float
// symbol op_495   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_148_c_eq_bool_f32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (bool) zero-extended
    let v1: u64 = ((p0) & 0x1u64);
    // fa0: operand `b` (float) arrives in fa0
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = sfemul::ui32_to_f32::ui32_to_f32_rm0(((v1) as u32));
    let v4: u64 = b2u(sfemul::f32_eq::f32_eq_rm0(v2, v3));
    v4
}
