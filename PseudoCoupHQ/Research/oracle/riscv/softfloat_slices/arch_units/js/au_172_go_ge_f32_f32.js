// arch-unit 172  --  go  `a >= b`  lhs=float32 rhs=float32
// symbol main.op_657   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fle.s a0, fa1, fa0                 float    emulation:f32_le_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_172_go_ge_f32_f32(p0, p1) {
  // fa0: operand `a` (float32) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // fa1: operand `b` (float32) arrives in fa1
  const v2 = ((p1) & 0xffffffffn);
  const v3 = AF.f32_le_rm0(v2, v1);
  return v3;
}

module.exports = { au_172_go_ge_f32_f32 };
