// arch-unit 2  --  c  `-a`  lhs=float rhs=None
// symbol op_15   outcome WALK_REFUSED
//
// the arch-unit, arch-opcode by arch-opcode:
//   fsgnjn.s fa0, fa0, fa0             float    bit-manipulation
//   c.jr ra                            integer  return
//
// answer: f32, 32 bits.  parameters are operand bit patterns.
'use strict';
const AF = require('./au_float.js');

function au_002_c_neg_f32(p0) {
  // fa0: operand `a` (float) arrives in fa0
  const v1 = ((p0) & 0xffffffffn);
  const v2 = (((v1) & 0x7fffffffn) | (((~(v1)) & 0xffffffffffffffffn) & 0x80000000n));
  return ((v2) & 0xffffffffn);
}

module.exports = { au_002_c_neg_f32 };
