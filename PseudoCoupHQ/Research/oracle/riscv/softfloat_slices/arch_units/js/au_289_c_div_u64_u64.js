// arch-unit 289  --  c  `a / b`  lhs=uint64_t rhs=uint64_t
// symbol op_224   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   divu a0, a0, a1                      integer    written-out restoring division (NOT the language's /)
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_289_c_div_u64_u64(p0, p1) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  // a1: operand `b` (uint64_t) arrives in a1
  const v2 = p1;
  const v3 = AU.au_divu(v1, v2);
  // the answer is uint64_t, 64 bits
  return v3;
}

module.exports = { au_289_c_div_u64_u64 };
