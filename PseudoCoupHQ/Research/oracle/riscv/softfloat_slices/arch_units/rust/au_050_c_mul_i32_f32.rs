// arch-unit 50  --  c  `a * b`  lhs=int32_t rhs=float
// symbol op_177   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_050_c_mul_i32_f32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32_t) sign-extended to XLEN
    let v1: u64 = (((p0) as u32) as i32 as i64) as u64;
    // fa0: operand `b` (float) arrives in fa0
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = sfemul::i32_to_f32::i32_to_f32_rm0(((v1) as u32));
    let v4: u64 = sfemul::f32_mul::f32_mul_rm0(v2, v3);
    ((v4) & 0xffffffffu64)
}
