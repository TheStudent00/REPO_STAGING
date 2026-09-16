// arch-unit 139  --  c  `a == b`  lhs=float rhs=float
// symbol op_483   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_139_c_eq_f32_f32(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // fa1: operand `b` (float) arrives in fa1
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = b2u(sfemul::f32_eq::f32_eq_rm0(v1, v2));
    v3
}
