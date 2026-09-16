// arch-unit 79  --  c  `a / b`  lhs=float rhs=float
// symbol op_231   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fdiv.s fa0, fa0, fa1, dyn          float    emulation:f32_div_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_079_c_div_f32_f32(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // fa1: operand `b` (float) arrives in fa1
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = sfemul::f32_div::f32_div_rm0(v1, v2);
    ((v3) & 0xffffffffu64)
}
