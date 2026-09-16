// arch-unit 9  --  c  `--a`  lhs=double rhs=None
// symbol op_46   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fli.d fa5, -1.0                    float    bit-manipulation
//   fadd.d fa0, fa0, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_009_c_predec_f64(p0: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    let v2: u64 = 0xbff0000000000000u64;
    let v3: u64 = sfemul::f64_add::f64_add_rm0(v1, v2);
    v3
}
