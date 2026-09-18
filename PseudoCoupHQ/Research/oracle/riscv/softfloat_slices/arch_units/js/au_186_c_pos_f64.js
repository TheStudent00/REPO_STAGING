// arch-unit 186  --  c  `+a`  lhs=double rhs=None
// symbol op_22   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: double, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_186_c_pos_f64(p0) {
  // fa0: operand `a` (double) arrives in fa0 as a bit pattern
  const v1 = p0;
  // the answer is double, 64 bits
  return v1;
}

module.exports = { au_186_c_pos_f64 };
