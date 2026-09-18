// arch-unit 218  --  c  `_Alignof a`  lhs=float rhs=None
// symbol op_81   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x4                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_218_c_alignof_c11_f32(p0) {
  // fa0: operand `a` (float) arrives in fa0 as a bit pattern
  const v1 = ((p0) & 0xffffffffn);
  const v2 = 0x4n;
  // the answer is uint64_t, 64 bits
  return v2;
}

module.exports = { au_218_c_alignof_c11_f32 };
