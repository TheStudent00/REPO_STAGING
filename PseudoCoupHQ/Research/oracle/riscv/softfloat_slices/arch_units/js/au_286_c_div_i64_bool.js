// arch-unit 286  --  c  `a / b`  lhs=int64_t rhs=bool
// symbol op_221   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_286_c_div_i64_bool(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  // the answer is int64_t, 64 bits
  return v1;
}

module.exports = { au_286_c_div_i64_bool };
