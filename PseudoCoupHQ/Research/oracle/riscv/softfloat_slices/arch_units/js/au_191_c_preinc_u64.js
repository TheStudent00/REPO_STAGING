// arch-unit 191  --  c  `++a`  lhs=uint64_t rhs=None
// symbol op_38   outcome LIFTED   2 arch-opcodes
//
// the arch-unit, arch-opcode by arch-opcode:
//   c.addi a0, 0x1                       integer    operator:+
//   c.jr ra                              integer    return
//
// answer: uint64_t, 64 bits.  parameters are operand bit patterns.
'use strict';
const AU = require('./au_int.js');

function au_191_c_preinc_u64(p0) {
  // a0: operand `a` (uint64_t) arrives in a0
  const v1 = p0;
  const v2 = AU.au_add(v1, 0x1n);
  // the answer is uint64_t, 64 bits
  return v2;
}

module.exports = { au_191_c_preinc_u64 };
