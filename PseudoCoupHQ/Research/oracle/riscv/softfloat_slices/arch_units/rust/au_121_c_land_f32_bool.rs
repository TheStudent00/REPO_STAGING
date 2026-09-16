// arch-unit 121  --  c  `a && b`  lhs=float rhs=bool
// symbol op_341   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmv.w.x fa5, zero                  float    bit-manipulation
//   feq.s a1, fa0, fa5                 float    emulation:f32_eq_rm0
//   andn a0, a0, a1                    integer  operator:& ~
//   c.jr ra                            integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_121_c_land_f32_bool(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    // a0: operand `b` (bool) zero-extended
    let v2: u64 = ((p1) & 0x1u64);
    let v3: u64 = ((0x0u64) & 0xffffffffu64);
    let v4: u64 = b2u(sfemul::f32_eq::f32_eq_rm0(v1, v3));
    let v5: u64 = ((v2) & (!(v4)));
    v5
}
