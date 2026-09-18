// arch-unit 20  --  c  `a + b`  lhs=float rhs=double
// symbol op_124   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa0                  float    emulation:f32_to_f64_rm0
//   fadd.d fa0, fa1, fa5, dyn          float    emulation:f64_add_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_020_c_add_f32_f64(p0, p1) {
  // fa0: operand `a` (float) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // fa1: operand `b` (double) arrives in fa1
  const v2 = p1;
  const v3 = AF.f32_to_f64_rm0(v1);
  const v4 = AF.f64_add_rm0(v2, v3);
  return v4;
}

module.exports = { au_020_c_add_f32_f64 };
