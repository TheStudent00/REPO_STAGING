// arch-unit 154  --  go  `a * b`  lhs=float32 rhs=float32
// symbol main.op_81   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fmul.s fa0, fa0, fa1, rne          float    emulation:f32_mul_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_154_go_mul_f32_f32(p0, p1) {
  // fa0: operand `a` (float32) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // fa1: operand `b` (float32) arrives in fa1
  const v2 = ((p1) & 0xffffffffn);
  const v3 = AF.f32_mul_rm0(v1, v2);
  return ((v3) & 0xffffffffn);
}

module.exports = { au_154_go_mul_f32_f32 };
