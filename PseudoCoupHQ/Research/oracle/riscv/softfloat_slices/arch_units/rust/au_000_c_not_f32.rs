// arch-unit 0  --  c  `!a`  lhs=float rhs=None
// symbol op_3   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a0, fa0, fa5                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_000_c_not_f32(p0: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    let v2: u64 = ((0x0u64) & 0xffffffffu64);
    let v3: u64 = b2u(sfemul::f32_eq::f32_eq_rm0(v1, v2));
    v3
}
