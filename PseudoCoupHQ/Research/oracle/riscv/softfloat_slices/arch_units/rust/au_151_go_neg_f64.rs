// arch-unit 151  --  go  `-a`  lhs=float64 rhs=None
// symbol main.op_10   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.d fa0, fa0, fa0             float    bit-manipulation
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_151_go_neg_f64(p0: u64) -> u64 {
    // fa0: operand `a` (float64) arrives in fa0
    let v1: u64 = p0;
    let v2: u64 = (((v1) & 0x7fffffffffffffffu64) | ((!(v1)) & 0x8000000000000000u64));
    v2
}
