// arch-unit 302  --  c  `a % b`  lhs=int64_t rhs=bool
// symbol op_257   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x0                         integer    constant
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_302_c_rem_i64_bool(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  const v3 = 0x0n;
  // the answer is int64_t, 64 bits
  return v3;
}

module.exports = { au_302_c_rem_i64_bool };
