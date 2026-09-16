// arch-unit 34  --  c  `a - b`  lhs=uint64_t rhs=float
// symbol op_153   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   fsub.s fa0, fa5, fa0, dyn          float    emulation:f32_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_034_c_neg_u64_f32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (uint64_t) arrives in a0
    let v1: u64 = p0;
    // fa0: operand `b` (float) arrives in fa0
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = sfemul::ui64_to_f32::ui64_to_f32_rm0(v1);
    let v4: u64 = sfemul::f32_sub::f32_sub_rm0(v3, v2);
    ((v4) & 0xffffffffu64)
}
