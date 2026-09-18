// arch-unit 166  --  go  `a < b`  lhs=float32 rhs=float32
// symbol main.op_549   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   flt.s a0, fa0, fa1                 float    emulation:f32_lt_rm0
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_166_go_lt_f32_f32(p0, p1) {
  // fa0: operand `a` (float32) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // fa1: operand `b` (float32) arrives in fa1
  const v2 = ((p1) & 0xffffffffn);
  const v3 = AF.f32_lt_rm0(v1, v2);
  return v3;
}

module.exports = { au_166_go_lt_f32_f32 };
