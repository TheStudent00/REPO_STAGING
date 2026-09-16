// arch-unit 26  --  c  `a + b`  lhs=double rhs=double
// symbol op_130   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fadd.d fa0, fa0, fa1, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
#![allow(unused_parens, unused_variables, unused_imports, clippy::all)]
use crate::b2u;

pub fn au_026_c_add_f64_f64(p0: u64, p1: u64) -> u64 {
    // fa0: operand `a` (double) arrives in fa0
    let v1: u64 = p0;
    // fa1: operand `b` (double) arrives in fa1
    let v2: u64 = p1;
    let v3: u64 = sfemul::f64_add::f64_add_rm0(v1, v2);
    v3
}
