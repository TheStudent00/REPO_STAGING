// arch-unit 204  --  c  `__alignof__ a`  lhs=int64_t rhs=None
// symbol op_55   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.li a0, 0x8                         integer    constant
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_204_c_alignof_gnu2_i64(p0) {
  // a0: operand `a` (int64_t) arrives in a0
  const v1 = p0;
  const v2 = 0x8n;
  // the answer is uint64_t, 64 bits
  return v2;
}

module.exports = { au_204_c_alignof_gnu2_i64 };
