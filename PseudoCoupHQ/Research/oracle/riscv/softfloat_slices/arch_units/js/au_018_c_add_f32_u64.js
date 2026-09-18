// arch-unit 18  --  c  `a + b`  lhs=float rhs=uint64_t
// symbol op_122   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.lu fa5, a0, dyn             float    emulation:ui64_to_f32_rm0
//   fadd.s fa0, fa0, fa5, dyn          float    emulation:f32_add_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_018_c_add_f32_u64(p0, p1) {
  // fa0: operand `a` (float) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // a0: operand `b` (uint64_t) arrives in a0
  const v2 = p1;
  const v3 = AF.ui64_to_f32_rm0(v2);
  const v4 = AF.f32_add_rm0(v1, v3);
  return ((v4) & 0xffffffffn);
}

module.exports = { au_018_c_add_f32_u64 };
