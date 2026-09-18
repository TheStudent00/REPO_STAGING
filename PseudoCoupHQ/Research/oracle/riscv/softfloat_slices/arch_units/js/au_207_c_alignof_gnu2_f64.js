// arch-unit 207  --  c  `__alignof__ a`  lhs=double rhs=None
// symbol op_58   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_207_c_alignof_gnu2_f64(p0) {
  // fa0: operand `a` (double) arrives in fa0 as a bit pattern
  const v1 = p0;
  const v2 = 0x8n;
  // the answer is uint64_t, 64 bits
  return v2;
}

module.exports = { au_207_c_alignof_gnu2_f64 };
