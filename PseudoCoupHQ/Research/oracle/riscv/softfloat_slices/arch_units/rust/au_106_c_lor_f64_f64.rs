// arch-unit 106  --  c  `a || b`  lhs=double rhs=double
// symbol op_310   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a0, fa0, fa5                 float    emulation:f64_eq_rm0
//   feq.d a1, fa1, fa5                 float    emulation:f64_eq_rm0
//   c.and a0, a1                       integer  operator:&
//   xori a0, a0, 0x1                   integer  operator:^
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_106_c_lor_f64_f64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    // fa1: operand `b` (double) arrives in fa1
    let v2: u64 = p1;
    let v3: u64 = 0x0u64;
    let v4: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v1, v3));
    let v5: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v2, v3));
    let v6: u64 = ((v4) & (v5));
    let v7: u64 = ((v6) ^ 0x1u64);
    v7
}
