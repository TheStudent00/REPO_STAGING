// arch-unit 268  --  c  `a - b`  lhs=bool rhs=int64_t
// symbol op_169   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   c.jr ra                              integer    return
//
// answer: int64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_268_c_sub_bool_i64(p0, p1) {
  // a0: operand `a` (bool) zero-extended to XLEN
  const v1 = ((p0) & 0x1n);
  // a1: operand `b` (int64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_sub(v1, v2);
  // the answer is int64_t, 64 bits
  return v3;
}

module.exports = { au_268_c_sub_bool_i64 };
