// arch-unit 150  --  go  `-a`  lhs=float32 rhs=None
// symbol main.op_9   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
//   jalr zero, 0x0(ra)                 integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_150_go_neg_f32(p0) {
  // fa0: operand `a` (float32) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  const v2 = (((v1) & 0x7fffffffn) | (((~(v1)) & 0xffffffffffffffffn) & 0x80000000n));
  return ((v2) & 0xffffffffn);
}

module.exports = { au_150_go_neg_f32 };
