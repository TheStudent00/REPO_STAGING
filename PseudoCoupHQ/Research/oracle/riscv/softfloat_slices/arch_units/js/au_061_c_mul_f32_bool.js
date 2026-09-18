// arch-unit 61  --  c  `a * b`  lhs=float rhs=bool
// symbol op_197   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fcvt.s.wu fa5, a0, dyn             float    emulation:ui32_to_f32_rm0
//   fmul.s fa0, fa0, fa5, dyn          float    emulation:f32_mul_rm0
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_061_c_mul_f32_bool(p0, p1) {
  // fa0: operand `a` (float) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // a0: operand `b` (bool) zero-extended
  const v2 = ((p1) & 0x1n);
  const v3 = AF.ui32_to_f32_rm0(((v2) & 0xffffffffn));
  const v4 = AF.f32_mul_rm0(v1, v3);
  return ((v4) & 0xffffffffn);
}

module.exports = { au_061_c_mul_f32_bool };
