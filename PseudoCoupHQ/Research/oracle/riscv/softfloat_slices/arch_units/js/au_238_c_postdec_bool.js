// arch-unit 238  --  c  `a--`  lhs=bool rhs=None
// symbol op_101   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: _Bool, 1 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_238_c_postdec_bool(p0) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // the answer is _Bool, 1 bits
  return ((v1) & 0x1n);
}

module.exports = { au_238_c_postdec_bool };
