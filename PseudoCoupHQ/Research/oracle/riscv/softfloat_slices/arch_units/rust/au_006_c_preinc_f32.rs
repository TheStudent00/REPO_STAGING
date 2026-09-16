// arch-unit 6  --  c  `++a`  lhs=float rhs=None
// symbol op_39   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fli.s fa5, 1.0                     float    bit-manipulation
//   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_006_c_preinc_f32(p0: u64) -> u64 {
    // fa0: operand `a` (float) arrives in fa0
    let v1: u64 = ((p0) & 0xffffffffu64);
    let v2: u64 = 0x3f800000u64;
    let v3: u64 = sfemul::f32_add::f32_add_rm0(v1, v2);
    ((v3) & 0xffffffffu64)
}
