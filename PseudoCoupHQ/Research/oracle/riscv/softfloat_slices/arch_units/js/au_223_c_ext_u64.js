// arch-unit 223  --  c  `__extension__ a`  lhs=uint64_t rhs=None
// symbol op_86   outcome LIFTED   1 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_223_c_ext_u64(p0) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  // the answer is uint64_t, 64 bits
  return v1;
}

module.exports = { au_223_c_ext_u64 };
