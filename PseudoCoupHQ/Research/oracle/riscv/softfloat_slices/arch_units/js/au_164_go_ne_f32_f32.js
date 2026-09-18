// arch-unit 164  --  go  `a != b`  lhs=float32 rhs=float32
// symbol main.op_513   outcome LIFTED
//
// the arch-unit, arch-opcode by arch-opcode:
//   feq.s a0, fa0, fa1                 float    emulation:f32_eq_rm0
//   xori a0, a0, 0x1                   integer  operator:^
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: int, 64 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_164_go_ne_f32_f32(p0, p1) {
  // fa0: operand `a` (float32) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  // fa1: operand `b` (float32) arrives in fa1
  const v2 = ((p1) & 0xffffffffn);
  const v3 = AF.f32_eq_rm0(v1, v2);
  const v4 = ((v3) ^ 0x1n);
  return v4;
}

module.exports = { au_164_go_ne_f32_f32 };
