// arch-unit 382  --  c  `a & b`  lhs=int64_t rhs=bool
// symbol op_437   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_382_c_band_i64_bool(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (bool) zero-extended to XLEN
  const v2 = ((p1) & 0x1n);
  const v3 = AU.au_and(v1, v2);
  // the answer is int64_t, 64 bits
  return v3;
}

module.exports = { au_382_c_band_i64_bool };
