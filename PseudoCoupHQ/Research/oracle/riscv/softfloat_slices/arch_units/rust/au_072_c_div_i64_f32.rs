// arch-unit 72  --  c  `a / b`  lhs=int64_t rhs=float
// symbol op_219   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
//   fdiv.s fa0, fa5, fa0, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_072_c_div_i64_f32(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int64_t) arrives in a0
    let v1: u64 = p0;
    // fa0: operand `b` (float) arrives in fa0
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = sfemul::i64_to_f32::i64_to_f32_rm0(v1);
    let v4: u64 = sfemul::f32_div::f32_div_rm0(v3, v2);
    ((v4) & 0xffffffffu64)
}
