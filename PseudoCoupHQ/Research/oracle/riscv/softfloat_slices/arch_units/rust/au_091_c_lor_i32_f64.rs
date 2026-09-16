// arch-unit 91  --  c  `a || b`  lhs=int32_t rhs=double
// symbol op_286   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   sltu a0, zero, a0                  integer  operator:<
//   fmv.d.x fa5, zero                  float    bit-manipulation
//   feq.d a1, fa0, fa5                 float    emulation:f64_eq_rm0
//   xori a1, a1, 0x1                   integer  operator:^
//   c.or a0, a1                        integer  operator:|
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_091_c_lor_i32_f64(p0: u64, p1: u64) -> u64 {
    // a0: operand `a` (int32_t) sign-extended to XLEN
    let v1: u64 = (((p0) as u32) as i32 as i64) as u64;
    // fa0: operand `b` (double) arrives in fa0
    let v2: u64 = p1;
    let v3: u64 = b2u((0x0u64) < (v1));
    let v4: u64 = 0x0u64;
    let v5: u64 = b2u(sfemul::f64_eq::f64_eq_rm0(v2, v4));
    let v6: u64 = ((v5) ^ 0x1u64);
    let v7: u64 = ((v3) | (v6));
    v7
}
