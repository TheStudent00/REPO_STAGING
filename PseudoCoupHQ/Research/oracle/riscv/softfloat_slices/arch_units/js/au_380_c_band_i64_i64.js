// arch-unit 380  --  c  `a & b`  lhs=int64_t rhs=int64_t
// symbol op_433   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.and a0, a1                         integer    operator:&
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_380_c_band_i64_i64(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (int64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_and(v1, v2);
  // the answer is int64_t, 64 bits
  return v3;
}

module.exports = { au_380_c_band_i64_i64 };
