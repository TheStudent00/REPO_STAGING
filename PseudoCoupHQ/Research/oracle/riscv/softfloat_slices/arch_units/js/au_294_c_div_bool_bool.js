// arch-unit 294  --  c  `a / b`  lhs=bool rhs=bool
// symbol op_245   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int32_t, 32 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_294_c_div_bool_bool(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  // the answer is int32_t, 32 bits
  return ((v1) & 0xffffffffn);
}

module.exports = { au_294_c_div_bool_bool };
