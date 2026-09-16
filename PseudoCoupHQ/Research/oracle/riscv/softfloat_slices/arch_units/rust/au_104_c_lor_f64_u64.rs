// arch-unit 104  --  c  `a || b`  lhs=double rhs=uint64_t
// symbol op_308   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   sltu a0, zero, a0                  integer  operator:<
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_104_c_lor_f64_u64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    // a0: operand `b` (uint64_t) arrives in a0
    let v2: u64 = p1;
    let v3: u64 = 0x0u64;
    let v4: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v1, v3));
    let v5: u64 = ((v4) ^ 0x1u64);
    let v6: u64 = b2u((0x0u64) < (v2));
    let v7: u64 = ((v6) | (v5));
    v7
}
