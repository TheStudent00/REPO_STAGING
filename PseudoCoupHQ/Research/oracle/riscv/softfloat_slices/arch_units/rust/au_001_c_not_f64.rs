// arch-unit 1  --  c  `!a`  lhs=double rhs=None
// symbol op_4   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_001_c_not_f64(p0: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    let v2: u64 = 0x0u64;
    let v3: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v1, v2));
    v3
}
