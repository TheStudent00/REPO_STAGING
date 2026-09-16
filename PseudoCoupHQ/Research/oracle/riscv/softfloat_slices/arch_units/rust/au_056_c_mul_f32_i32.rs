// arch-unit 56  --  c  `a * b`  lhs=float rhs=int32_t
// symbol op_192   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.w fa5, a0, dyn              float    emulation:i32_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_056_c_mul_f32_i32(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // a0: operand `b` (int32_t) sign-extended to XLEN
    let v2: u64 = (((p1) as u32) as i32 as i64) as u64;
    let v3: u64 = sfemul::i32_to_f32::i32_to_f32_rm0(((v2) as u32));
    let v4: u64 = sfemul::f32_mul::f32_mul_rm0(v1, v3);
    ((v4) & 0xffffffffu64)
}
