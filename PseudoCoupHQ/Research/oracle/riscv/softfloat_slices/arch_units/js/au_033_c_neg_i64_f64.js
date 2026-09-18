// arch-unit 33  --  c  `a - b`  lhs=int64_t rhs=double
// symbol op_148   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.d.l fa5, a0, dyn              float    emulation:i64_to_f64_rm0
//   fsub.d fa0, fa5, fa0, dyn          float    emulation:f64_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f64, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_033_c_neg_i64_f64(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // fa0: operand `b` (double) arrives in fa0
  const v2 = p1;
  const v3 = AF.i64_to_f64_rm0(v1);
  const v4 = AF.f64_sub_rm0(v3, v2);
  return v4;
}

module.exports = { au_033_c_neg_i64_f64 };
