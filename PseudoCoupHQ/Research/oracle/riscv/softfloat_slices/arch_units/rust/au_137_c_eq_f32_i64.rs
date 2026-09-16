// arch-unit 137  --  c  `a == b`  lhs=float rhs=int64_t
// symbol op_481   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_137_c_eq_f32_i64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // a0: operand `b` (int64_t) arrives in a0
    let v2: u64 = p1;
    let v3: u64 = sfemul::i64_to_f32::i64_to_f32_rm0(v2);
    let v4: u64 = b2u(sfemul::f32_eq::f32_eq_rm0(v1, v3));
    v4
}
