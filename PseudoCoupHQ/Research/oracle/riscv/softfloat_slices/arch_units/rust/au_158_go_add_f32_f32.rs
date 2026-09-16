// arch-unit 158  --  go  `a + b`  lhs=float32 rhs=float32
// symbol main.op_333   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fadd.s fa0, fa0, fa1, rne          float    emulation:f32_add_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_158_go_add_f32_f32(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float32) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // fa1: operand `b` (float32) arrives in fa1
    let v2: u64 = ((p1) & 0xffffffffu64);
    let v3: u64 = sfemul::f32_add::f32_add_rm0(v1, v2);
    ((v3) & 0xffffffffu64)
}
