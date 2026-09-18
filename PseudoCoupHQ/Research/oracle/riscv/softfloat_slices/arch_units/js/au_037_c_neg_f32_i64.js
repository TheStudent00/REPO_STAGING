// arch-unit 37  --  c  `a - b`  lhs=float rhs=int64_t
// symbol op_157   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.l fa5, a0, dyn              float    emulation:i64_to_f32_rm0
//   fsub.s fa0, fa0, fa5, dyn          float    emulation:f32_sub_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_037_c_neg_f32_i64(p0, p1) {
  // fa0: operand `a` (float) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // a0: operand `b` (int64_t) arrives in a0
  const v2 = p1;
  const v3 = AF.i64_to_f32_rm0(v2);
  const v4 = AF.f32_sub_rm0(v1, v3);
  return ((v4) & 0xffffffffn);
}

module.exports = { au_037_c_neg_f32_i64 };
