// arch-unit 224  --  c  `__extension__ a`  lhs=float rhs=None
// symbol op_87   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: float, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_224_c_ext_f32(p0) {
  // fa0: operand `a` (float) arrives in fa0 as a bit pattern
  const v1 = ((p0) & 0xffffffffn);
  // the answer is float, 32 bits
  return ((v1) & 0xffffffffn);
}

module.exports = { au_224_c_ext_f32 };
