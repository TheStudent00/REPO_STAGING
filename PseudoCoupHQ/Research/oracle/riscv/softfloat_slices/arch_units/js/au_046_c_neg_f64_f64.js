// arch-unit 46  --  c  `a - b`  lhs=double rhs=double
// symbol op_166   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsub.d fa0, fa0, fa1, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_046_c_neg_f64_f64(p0, p1) {
  // fa0: operand `a` (double) arrives in fa0
  const v1 = p0;
  // fa1: operand `b` (double) arrives in fa1
  const v2 = p1;
  const v3 = AF.f64_sub_rm0(v1, v2);
  return v3;
}

module.exports = { au_046_c_neg_f64_f64 };
