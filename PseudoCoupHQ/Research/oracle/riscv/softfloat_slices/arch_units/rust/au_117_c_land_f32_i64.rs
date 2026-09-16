// arch-unit 117  --  c  `a && b`  lhs=float rhs=int64_t
// symbol op_337   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   sltu a0, zero, a0                  integer  operator:<
//   andn a0, a0, a1                    integer  operator:& ~
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_117_c_land_f32_i64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // a0: operand `b` (int64_t) arrives in a0
    let v2: u64 = p1;
    let v3: u64 = ((0x0u64) & 0xffffffffu64);
    let v4: u64 = b2u(sfemul::f32_eq::f32_eq_rm0(v1, v3));
    let v5: u64 = b2u((0x0u64) < (v2));
    let v6: u64 = ((v5) & (!(v4)));
    v6
}
