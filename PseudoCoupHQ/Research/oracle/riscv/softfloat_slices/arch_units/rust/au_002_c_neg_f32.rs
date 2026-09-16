// arch-unit 2  --  c  `-a`  lhs=float rhs=None
// symbol op_15   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_002_c_neg_f32(p0: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    let v2: u64 = (((v1) & 0x7fffffffu64) | ((!(v1)) & 0x80000000u64));
    ((v2) & 0xffffffffu64)
}
