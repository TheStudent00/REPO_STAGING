// arch-unit 183  --  c  `+a`  lhs=int64_t rhs=None
// symbol op_19   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_183_c_pos_i64(p0) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // the answer is int64_t, 64 bits
  return v1;
}

module.exports = { au_183_c_pos_i64 };
