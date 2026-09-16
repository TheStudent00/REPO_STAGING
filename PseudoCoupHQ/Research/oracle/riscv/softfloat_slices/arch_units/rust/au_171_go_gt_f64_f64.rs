// arch-unit 171  --  go  `a > b`  lhs=float64 rhs=float64
// symbol main.op_628   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   flt.d a0, fa1, fa0                 float    emulation:f64_lt_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_171_go_gt_f64_f64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float64) arrives in fa0
    let v1: u64 = p0;
    // fa1: operand `b` (float64) arrives in fa1
    let v2: u64 = p1;
    let v3: u64 = b2u(sfemul::f64_lt::f64_lt_rm0(v2, v1));
    v3
}
