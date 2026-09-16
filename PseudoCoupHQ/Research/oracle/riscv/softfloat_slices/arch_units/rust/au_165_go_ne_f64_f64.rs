// arch-unit 165  --  go  `a != b`  lhs=float64 rhs=float64
// symbol main.op_520   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.d a0, fa0, fa1                 float    emulation:f64_eq_rm0
//   xori a0, a0, 0x1                   integer  operator:^
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_165_go_ne_f64_f64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float64) arrives in fa0
    let v1: u64 = p0;
    // fa1: operand `b` (float64) arrives in fa1
    let v2: u64 = p1;
    let v3: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v1, v2));
    let v4: u64 = ((v3) ^ 0x1u64);
    v4
}
