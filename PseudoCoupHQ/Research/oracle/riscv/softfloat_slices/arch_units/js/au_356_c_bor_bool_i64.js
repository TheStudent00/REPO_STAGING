// arch-unit 356  --  c  `a | b`  lhs=bool rhs=int64_t
// symbol op_385   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.or a0, a1                          integer    operator:|
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_356_c_bor_bool_i64(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (int64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_or(v1, v2);
  // the answer is int64_t, 64 bits
  return v3;
}

module.exports = { au_356_c_bor_bool_i64 };
