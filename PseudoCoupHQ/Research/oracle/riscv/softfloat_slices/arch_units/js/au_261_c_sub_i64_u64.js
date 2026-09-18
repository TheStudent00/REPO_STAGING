// arch-unit 261  --  c  `a - b`  lhs=int64_t rhs=uint64_t
// symbol op_146   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.sub a0, a1                         integer    operator:-
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_261_c_sub_i64_u64(p0, p1) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (uint64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_sub(v1, v2);
  // the answer is uint64_t, 64 bits
  return v3;
}

module.exports = { au_261_c_sub_i64_u64 };
