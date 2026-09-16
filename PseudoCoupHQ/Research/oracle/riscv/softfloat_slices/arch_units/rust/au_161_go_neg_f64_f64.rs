// arch-unit 161  --  go  `a - b`  lhs=float64 rhs=float64
// symbol main.op_376   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsub.d fa0, fa0, fa1, rne          float    emulation:f64_sub_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_161_go_neg_f64_f64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float64) arrives in fa0
    let v1: u64 = p0;
    // fa1: operand `b` (float64) arrives in fa1
    let v2: u64 = p1;
    let v3: u64 = sfemul::f64_sub::f64_sub_rm0(v1, v2);
    v3
}
