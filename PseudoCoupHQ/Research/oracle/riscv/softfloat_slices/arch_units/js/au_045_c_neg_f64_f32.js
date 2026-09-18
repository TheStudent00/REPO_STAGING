// arch-unit 45  --  c  `a - b`  lhs=double rhs=float
// symbol op_165   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.s fa5, fa1                  float    emulation:f32_to_f64_rm0
//   fsub.d fa0, fa0, fa5, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_045_c_neg_f64_f32(p0, p1) {
  // fa0: operand `a` (double) arrives in fa0
  const v1 = p0;
  // fa1: operand `b` (float) arrives in fa1
  const v2 = ((p1) & 0xffffffffn);
  const v3 = AF.f32_to_f64_rm0(v2);
  const v4 = AF.f64_sub_rm0(v1, v3);
  return v4;
}

module.exports = { au_045_c_neg_f64_f32 };
