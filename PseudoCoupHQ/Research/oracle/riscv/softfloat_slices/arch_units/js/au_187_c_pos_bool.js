// arch-unit 187  --  c  `+a`  lhs=bool rhs=None
// symbol op_23   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_187_c_pos_bool(p0) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // the answer is int32_t, 32 bits
  return ((v1) & 0xffffffffn);
}

module.exports = { au_187_c_pos_bool };
